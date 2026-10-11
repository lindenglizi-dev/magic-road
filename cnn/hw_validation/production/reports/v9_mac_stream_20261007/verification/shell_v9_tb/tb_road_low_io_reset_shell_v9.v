`timescale 1ns / 1ps

module tb_road_low_io_reset_shell;

	reg i_clk;
	reg i_rstn;
	reg i_rx_valid;
	reg [15:0]i_rx_data;
	wire o_rx_ready;
	wire o_tx_valid;
	wire [15:0]o_tx_data;
	reg i_tx_ready;

	reg signed [15:0]table_words [0:1023];
	integer error_count;
	integer case_count;
	integer table_index;
	integer wait_count;
	reg [15:0]received_word;

	road_low_io_reset_shell dut(
		.i_clk(i_clk),
		.i_rstn(i_rstn),
		.i_rx_valid(i_rx_valid),
		.i_rx_data(i_rx_data),
		.o_rx_ready(o_rx_ready),
		.o_tx_valid(o_tx_valid),
		.o_tx_data(o_tx_data),
		.i_tx_ready(i_tx_ready)
	);

	always #5 i_clk = ~i_clk;

	task check_blocked;
		begin
			#1;
			if((o_rx_ready !== 1'b0) || (o_tx_valid !== 1'b0))begin
				$display("TB_ERROR_RESET interface not blocked rstn=%b release=%b ready=%b valid=%b", i_rstn, dut.reg_release_done, o_rx_ready, o_tx_valid);
				error_count = error_count + 1;
			end
		end
	endtask

	task assert_reset;
		begin
			#2;
			i_rstn = 1'b0;
			check_blocked;
			if((dut.reg_release_meta !== 1'b0) || (dut.reg_release_done !== 1'b0) || (dut.shell_rstn !== 1'b0))begin
				$display("TB_ERROR_RESET asynchronous assertion did not clear release chain");
				error_count = error_count + 1;
			end
		end
	endtask

	task release_and_check;
		begin
			@(negedge i_clk);
			#2;
			i_rstn = 1'b1;
			i_rx_valid = 1'b0;
			i_rx_data = 16'd0;
			i_tx_ready = 1'b0;
			@(posedge i_clk);
			#1;
			if((dut.reg_release_meta !== 1'b1) || (dut.reg_release_done !== 1'b0))begin
				$display("TB_ERROR_RESET first release edge meta=%b done=%b", dut.reg_release_meta, dut.reg_release_done);
				error_count = error_count + 1;
			end
			if((o_rx_ready !== 1'b0) || (o_tx_valid !== 1'b0))begin
				$display("TB_ERROR_RESET interface opened on first release edge");
				error_count = error_count + 1;
			end
			@(negedge i_clk);
			check_blocked;
			@(posedge i_clk);
			#1;
			if((dut.reg_release_done !== 1'b1) || (dut.shell_rstn !== 1'b1))begin
				$display("TB_ERROR_RESET second release edge did not open shell reset");
				error_count = error_count + 1;
			end
		end
	endtask

	task release_close_before_edge;
		begin
			@(negedge i_clk);
			#4.9;
			i_rstn = 1'b1;
			@(posedge i_clk);
			#0.01;
			if((dut.reg_release_meta !== 1'b1) || (dut.reg_release_done !== 1'b0) || (o_rx_ready !== 1'b0) || (o_tx_valid !== 1'b0))begin
				$display("TB_ERROR_RESET close-before first sampled edge violated release rule");
				error_count = error_count + 1;
			end
			@(posedge i_clk);
			#0.01;
			if((dut.reg_release_done !== 1'b1) || (dut.shell_rstn !== 1'b1))begin
				$display("TB_ERROR_RESET close-before second sampled edge did not release");
				error_count = error_count + 1;
			end
		end
	endtask

	task release_close_after_edge;
		begin
			@(posedge i_clk);
			#0.1;
			i_rstn = 1'b1;
			check_blocked;
			@(posedge i_clk);
			#0.01;
			if((dut.reg_release_meta !== 1'b1) || (dut.reg_release_done !== 1'b0) || (o_rx_ready !== 1'b0) || (o_tx_valid !== 1'b0))begin
				$display("TB_ERROR_RESET close-after first sampled edge violated release rule");
				error_count = error_count + 1;
			end
			@(posedge i_clk);
			#0.01;
			if((dut.reg_release_done !== 1'b1) || (dut.shell_rstn !== 1'b1))begin
				$display("TB_ERROR_RESET close-after second sampled edge did not release");
				error_count = error_count + 1;
			end
		end
	endtask

	task send_word;
		input [15:0]word_value;
		begin
			@(negedge i_clk);
			i_rx_valid = 1'b1;
			i_rx_data = word_value;
			while(o_rx_ready !== 1'b1)begin
				@(negedge i_clk);
			end
			@(posedge i_clk);
			#1;
			@(negedge i_clk);
			i_rx_valid = 1'b0;
			i_rx_data = 16'd0;
		end
	endtask

	task load_table;
		begin
			send_word(16'h1000);
			for(table_index = 0; table_index < 1024; table_index = table_index + 1)begin
				send_word(table_words[table_index]);
			end
			wait_count = 0;
			while((dut.road_low_io_physical_shell_Inst_reset.flag_table_complete !== 1'b1) && (wait_count < 32))begin
				@(negedge i_clk);
				wait_count = wait_count + 1;
			end
			if(dut.road_low_io_physical_shell_Inst_reset.flag_table_complete !== 1'b1)begin
				$display("TB_ERROR_RESET complete table did not become active");
				error_count = error_count + 1;
			end
		end
	endtask

	task receive_word;
		output [15:0]word_value;
		begin
			wait_count = 0;
			while((o_tx_valid !== 1'b1) && (wait_count < 64))begin
				@(negedge i_clk);
				wait_count = wait_count + 1;
			end
			if(o_tx_valid !== 1'b1)begin
				$display("TB_ERROR_RESET response timeout");
				error_count = error_count + 1;
				word_value = 16'd0;
			end else begin
				word_value = o_tx_data;
				i_tx_ready = 1'b1;
				@(posedge i_clk);
				#1;
				@(negedge i_clk);
				i_tx_ready = 1'b0;
			end
		end
	endtask

	initial begin
		i_clk = 1'b0;
		i_rstn = 1'b0;
		i_rx_valid = 1'b1;
		i_rx_data = 16'hdead;
		i_tx_ready = 1'b1;
		error_count = 0;
		case_count = 0;
		$readmemh("../../v7_low_io_physical_20261006/shell/inputs/silu_table.hex", table_words);

		repeat(3) @(posedge i_clk);
		check_blocked;
		release_and_check;
		if(dut.road_low_io_physical_shell_Inst_reset.cnt_rx_words !== 32'd0)begin
			$display("TB_ERROR_RESET stale valid transferred before the third edge");
			error_count = error_count + 1;
		end
		assert_reset;
		i_rx_valid = 1'b0;
		i_rx_data = 16'd0;
		release_close_before_edge;
		if(dut.road_low_io_physical_shell_Inst_reset.cnt_rx_words !== 32'd0)begin
			$display("TB_ERROR_RESET close-before release consumed stale data");
			error_count = error_count + 1;
		end
		case_count = case_count + 1;
		assert_reset;
		release_close_after_edge;
		if(dut.road_low_io_physical_shell_Inst_reset.cnt_rx_words !== 32'd0)begin
			$display("TB_ERROR_RESET close-after release consumed stale data");
			error_count = error_count + 1;
		end
		case_count = case_count + 1;
		send_word(16'h1000);
		if(dut.road_low_io_physical_shell_Inst_reset.cnt_rx_words !== 32'd1)begin
			$display("TB_ERROR_RESET first new frame did not transfer after release");
			error_count = error_count + 1;
		end
		case_count = case_count + 1;

		for(table_index = 0; table_index < 8; table_index = table_index + 1)begin
			send_word(table_words[table_index]);
		end
		@(negedge i_clk);
		i_rx_valid = 1'b1;
		i_rx_data = 16'h55aa;
		assert_reset;
		if((dut.road_low_io_physical_shell_Inst_reset.flag_table_complete !== 1'b0) ||
		   (dut.road_low_io_physical_shell_Inst_reset.reg_table_pending_valid !== 1'b0) ||
		   (dut.road_low_io_physical_shell_Inst_reset.cnt_table_entry !== 10'd0))begin
			$display("TB_ERROR_RESET partial table survived reset");
			error_count = error_count + 1;
		end
		i_rx_valid = 1'b0;
		i_rx_data = 16'd0;
		repeat(2) @(posedge i_clk);
		release_and_check;
		case_count = case_count + 1;

		load_table;
		send_word(16'h5000);
		wait_count = 0;
		while((o_tx_valid !== 1'b1) && (wait_count < 64))begin
			@(negedge i_clk);
			wait_count = wait_count + 1;
		end
		if(o_tx_valid !== 1'b1)begin
			$display("TB_ERROR_RESET status response did not enter stalled state");
			error_count = error_count + 1;
		end
		@(negedge i_clk);
		assert_reset;
		if(dut.road_low_io_physical_shell_Inst_reset.tx_valid_o !== 1'b0)begin
			$display("TB_ERROR_RESET stalled response survived reset");
			error_count = error_count + 1;
		end
		repeat(2) @(posedge i_clk);
		release_and_check;
		if((o_tx_valid !== 1'b0) ||
		   (dut.road_low_io_physical_shell_Inst_reset.flag_table_complete !== 1'b0) ||
		   (dut.road_low_io_physical_shell_Inst_reset.cnt_rx_words !== 32'd0))begin
			$display("TB_ERROR_RESET old transaction leaked after stalled reset");
			error_count = error_count + 1;
		end
		case_count = case_count + 1;

		load_table;
		if(dut.road_low_io_physical_shell_Inst_reset.cnt_rx_words !== 32'd1025)begin
			$display("TB_ERROR_RESET recovery count includes an old frame count=%0d", dut.road_low_io_physical_shell_Inst_reset.cnt_rx_words);
			error_count = error_count + 1;
		end
		send_word(16'h5000);
		receive_word(received_word);
		if((received_word[15:12] !== 4'hb) || (received_word[8] !== 1'b1) || (received_word[7:6] !== 2'b00) || (received_word[2:0] !== 3'd0))begin
			$display("TB_ERROR_RESET recovered status contains stale state word=%h", received_word);
			error_count = error_count + 1;
		end
		case_count = case_count + 1;

		if((error_count == 0) && (case_count == 6))begin
			$display("TB_PASS_RESET cases=%0d errors=0 release_stages=2 first_consume_edge=3", case_count);
		end else begin
			$display("TB_FAIL_RESET cases=%0d errors=%0d", case_count, error_count);
		end
		$finish;
	end

	initial begin
		#2000000;
		$display("TB_FAIL_RESET timeout errors=%0d", error_count + 1);
		$finish;
	end

endmodule
