`timescale 1ns / 1ps
// 受控tile完成端点只验证6240个发令，不执行卷积或DDR。
module tb_standard_layer_sequence(output o_test_complete);
	reg i_clk = 0;
	reg i_rstn = 0;
	reg i_cancel = 0;
	reg i_start_valid = 0;
	reg [6:0]i_layer_id = 0;
	reg i_tile_start_ready = 0;
	reg i_tile_done = 0;
	reg i_tile_fault = 0;
	wire o_start_ready, o_busy, o_done, o_fault, o_tile_start_valid;
	wire [6:0]o_layer_id, o_tile_y, o_tile_x;
	reg [21:0]jobs [0:6239];
	reg [1023:0]jobs_path;
	reg [31:0]random_state = 32'hc25b7101;
	reg pending = 0;
	reg previous_stall = 0;
	reg [20:0]previous_payload = 0;
	integer index = 0;
	integer delay = 0;
	integer layer = 0;
	integer cycles = 0;
	integer layers_done = 0;
	reg test_complete = 0;
	assign o_test_complete = test_complete;
	road_standard_layer_sequence road_standard_layer_sequence_Inst_dut(
		.i_clk(i_clk), .i_rstn(i_rstn), .i_cancel(i_cancel), .i_start_valid(i_start_valid), .i_layer_id(i_layer_id),
		.i_tile_start_ready(i_tile_start_ready), .i_tile_done(i_tile_done), .i_tile_fault(i_tile_fault),
		.o_start_ready(o_start_ready), .o_busy(o_busy), .o_done(o_done), .o_fault(o_fault),
		.o_tile_start_valid(o_tile_start_valid), .o_layer_id(o_layer_id), .o_tile_y(o_tile_y), .o_tile_x(o_tile_x)
	);
	// 显式时钟过程，不依赖formatter不支持的always延迟简写。
	initial begin
		forever begin #5 i_clk = !i_clk; end
	end
	// 准入背压独立于完成延迟，模拟不同计算等待。
	always @(negedge i_clk) begin
		random_state = {random_state[30:0],random_state[31]^random_state[21]^random_state[1]^random_state[0]};
		i_tile_start_ready = i_rstn && !pending && !i_tile_done && random_state[0];
	end
	// 每接受一个tile，后续有界随机拍才给一个完成脉冲。
	always @(posedge i_clk) begin
		cycles = cycles + 1;
		if(cycles > 300000) $fatal(1,"SEQUENCE_TIMEOUT");
		if(!i_rstn) begin
			pending <= 0; i_tile_done <= 0; previous_stall <= 0; index = 0;
		end else begin
			if(previous_stall && (!o_tile_start_valid || {o_layer_id,o_tile_y,o_tile_x} !== previous_payload)) $fatal(1,"SEQUENCE_STALL_CHANGED");
			previous_stall <= o_tile_start_valid && !i_tile_start_ready && !i_cancel;
			previous_payload <= {o_layer_id,o_tile_y,o_tile_x};
			i_tile_done <= 0;
			if(pending) begin
				if(delay == 0) begin i_tile_done <= 1; pending <= 0; end
				else delay = delay - 1;
			end
			if(o_tile_start_valid && i_tile_start_ready) begin
				if(pending || i_tile_done || index >= 6240) $fatal(1,"SEQUENCE_OWNER_OVERLAP");
				if({o_layer_id,o_tile_y,o_tile_x} !== jobs[index][20:0]) $fatal(1,"SEQUENCE_JOB_MISMATCH index=%0d",index);
				index = index + 1; pending <= 1; delay = random_state[4:1];
			end
			if(pending && !o_busy) $fatal(1,"SEQUENCE_OWNER_EARLY_RELEASE");
		end
	end
	// 整层start只采样一次，随后扰动外部层号不能改变发令。
	initial begin
		if(!$value$plusargs("JOBS=%s",jobs_path)) $fatal(1,"JOBS_REQUIRED");
		$readmemh(jobs_path,jobs);
		repeat(4) @(negedge i_clk); i_rstn = 1;
		for(layer = 0; layer < 31; layer = layer + 1) begin
			while(!o_start_ready) @(negedge i_clk);
			i_layer_id = jobs[index][20:14]; i_start_valid = 1;
			@(negedge i_clk); i_start_valid = 0; i_layer_id = 127;
			while(!o_done) begin @(negedge i_clk); if(o_fault) $fatal(1,"SEQUENCE_UNEXPECTED_FAULT"); end
			if(index == 0 || !jobs[index-1][21] || pending) $fatal(1,"SEQUENCE_EARLY_LAYER_DONE");
			layers_done = layers_done + 1;
			@(negedge i_clk);
		end
		if(index != 6240 || layers_done != 31) $fatal(1,"SEQUENCE_COUNTS");
		$display("SEQUENCE_NORMAL_PASS layers=%0d tiles=%0d cycles=%0d",layers_done,index,cycles);
		while(!o_start_ready) @(negedge i_clk);
		i_layer_id = 0; i_start_valid = 1;
		@(negedge i_clk); i_start_valid = 0;
		repeat(5) @(negedge i_clk);
		if(!o_fault || !o_busy || o_start_ready || o_tile_start_valid || o_done) $fatal(1,"SEQUENCE_ILLEGAL_LAYER");
		i_rstn = 0; repeat(4) @(negedge i_clk); i_rstn = 1;
		while(!o_start_ready) @(negedge i_clk);
		i_layer_id = jobs[0][20:14]; i_start_valid = 1;
		@(negedge i_clk); i_start_valid = 0;
		while(!pending) @(negedge i_clk);
		i_cancel = 1; repeat(3) @(negedge i_clk);
		if(!o_fault || !o_busy || o_start_ready || o_tile_start_valid || o_done) $fatal(1,"SEQUENCE_CANCEL_RELEASE");
		i_rstn = 0; i_cancel = 0; repeat(4) @(negedge i_clk); i_rstn = 1;
		repeat(4) @(negedge i_clk);
		if(!o_start_ready || o_fault || o_busy) $fatal(1,"SEQUENCE_RESET_RECOVERY");
		test_complete = 1;
		$display("SEQUENCE_PASS controlled_tile_endpoint=1 numerical_compute=0 layers=31 tiles=6240");
		$finish;
	end
endmodule
