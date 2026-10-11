`timescale 1ns / 1ps

module tb_road_postprocess_low_io_top;

	reg i_clk = 1'b0;
	reg i_rstn = 1'b0;
	reg i_rx_valid = 1'b0;
	reg [15:0]i_rx_data = 16'd0;
	reg i_tx_ready = 1'b0;
	wire o_rx_ready;
	wire o_tx_valid;
	wire [15:0]o_tx_data;

	reg [15:0]status_words [0:30];
	reg [15:0]received_word;
	reg [31:0]received_count;
	integer index;

	always #5 i_clk = ~i_clk;

	task fail;
		input [255:0]message;
		begin
			$display("TB_FAIL_LOW_IO %0s", message);
			$finish;
		end
	endtask

	task apply_reset;
		begin
			@(negedge i_clk);
			i_rstn = 1'b0;
			i_rx_valid = 1'b0;
			i_tx_ready = 1'b0;
			repeat(3) @(negedge i_clk);
			i_rstn = 1'b1;
			while(o_rx_ready !== 1'b1) @(negedge i_clk);
		end
	endtask

	task send_word;
		input [15:0]value;
		begin
			@(negedge i_clk);
			i_rx_data = value;
			i_rx_valid = 1'b1;
			while(o_rx_ready !== 1'b1) @(negedge i_clk);
			@(negedge i_clk);
			i_rx_valid = 1'b0;
			i_rx_data = 16'd0;
		end
	endtask

	task receive_word_stalled;
		input integer stall_cycles;
		output [15:0]value;
		reg [15:0]held_value;
		integer stall_index;
		begin
			i_tx_ready = 1'b0;
			while(o_tx_valid !== 1'b1) @(negedge i_clk);
			held_value = o_tx_data;
			for(stall_index = 0; stall_index < stall_cycles; stall_index = stall_index + 1)begin
				@(negedge i_clk);
				if((o_tx_valid !== 1'b1) || (o_tx_data !== held_value))begin
					fail("TX changed under backpressure");
				end
			end
			i_tx_ready = 1'b1;
			@(negedge i_clk);
			value = held_value;
			i_tx_ready = 1'b0;
		end
	endtask

	task load_value;
		input [2:0]kind;
		input [10:0]address;
		input [31:0]value;
		begin
			send_word(16'h2000);
			send_word({kind, 2'b00, address});
			send_word(value[15:0]);
			send_word(value[31:16]);
		end
	endtask

	task read_status;
		begin
			send_word(16'h5000);
			for(index = 0; index < 31; index = index + 1)begin
				receive_word_stalled((index % 4) + 1, status_words[index]);
			end
		end
	endtask

	initial begin
		apply_reset();

		//非法导出必须立即结束，不能等待不存在的runner事件
		send_word(16'h4000);
		receive_word_stalled(2, received_word);
		if(received_word !== 16'he001) fail("premature export was not rejected");

		apply_reset();
		//非法装载类别在描述符处拒绝，不得进入LOAD_WAIT
		send_word(16'h2000);
		send_word({3'd6, 2'b00, 11'd0});
		receive_word_stalled(2, received_word);
		if(received_word !== 16'he001) fail("load kind 6 was not rejected");

		apply_reset();
		//动态开启写回；此路径不能在物理综合中被常量化
		send_word(16'h6001);

		//完整运行时SiLU表，零表用于可判定的零结果
		send_word(16'h1000);
		for(index = 0; index < 1024; index = index + 1)begin
			send_word(16'd0);
		end

		//完整PW-only闭包：256个DW缓存、384个PW权重、24个PW偏置
		for(index = 0; index < 256; index = index + 1)begin
			load_value(3'd1, index[10:0], 32'd0);
		end
		for(index = 0; index < 384; index = index + 1)begin
			load_value(3'd4, index[10:0], 32'd0);
		end
		for(index = 0; index < 24; index = index + 1)begin
			load_value(3'd5, index[10:0], 32'd0);
		end

		send_word(16'h3001);
		repeat(30000) @(negedge i_clk);
		read_status();

		if(status_words[0][13] !== 1'b1) fail("commit-ready status missing");
		if(status_words[0][12] !== 1'b0) fail("shell fault after legal preload");
		if(status_words[0][11] !== 1'b0) fail("runner fault after legal preload");
		if(status_words[0][10] !== 1'b1) fail("runner completion was not latched");
		if(status_words[0][9] !== 1'b0) fail("runner still busy after wait window");
		if(status_words[0][8] !== 1'b0) fail("table fault after complete table");
		if(status_words[0][7] !== 1'b1) fail("table loaded status missing");
		if(status_words[0][6:0] !== 7'd0) fail("queues or metadata not drained");
		if({status_words[2], status_words[1]} !== 32'd664) fail("runtime load count mismatch");
		if({status_words[4], status_words[3]} == 32'd0) fail("core cycle count was zero");
		if({status_words[22], status_words[21]} !== 32'd128) fail("MAC result count mismatch");
		if({status_words[24], status_words[23]} !== 32'd384) fail("pre accept count mismatch");
		if({status_words[26], status_words[25]} !== 32'd384) fail("SiLU accept count mismatch");
		if({status_words[28], status_words[27]} !== 32'd384) fail("post accept count mismatch");
		if({status_words[30], status_words[29]} !== 32'd384) fail("writeback count mismatch");

		//真实结果缓存逐项导出；每项索引和零数据都位精确比较
		send_word(16'h4000);
		received_count = 32'd0;
		for(index = 0; index < 384; index = index + 1)begin
			receive_word_stalled(index % 3, received_word);
			if(received_word !== (16'h8000 | index[8:0])) fail("export index mismatch");
			receive_word_stalled((index + 1) % 3, received_word);
			if(received_word !== 16'h9000) fail("export data mismatch");
			received_count = received_count + 1'b1;
		end
		receive_word_stalled(3, received_word);
		if(received_word[15:12] !== 4'hc) fail("export completion missing");
		if(received_word[11] !== 1'b0) fail("runner fault in export completion");
		if(received_count !== 32'd384) fail("export count mismatch");

		$display("TB_PASS_POSTPROCESS_LOW_IO table=1024 loads=664 mac=128 scalars=384 exports=384 status_words=31");
		$finish;
	end

	road_postprocess_low_io_top dut(
		.i_clk(i_clk),
		.i_rstn(i_rstn),
		.i_rx_valid(i_rx_valid),
		.i_rx_data(i_rx_data),
		.o_rx_ready(o_rx_ready),
		.o_tx_valid(o_tx_valid),
		.o_tx_data(o_tx_data),
		.i_tx_ready(i_tx_ready)
	);

	initial begin
		#2000000;
		fail("timeout");
	end

endmodule
