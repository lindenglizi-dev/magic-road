`timescale 1ns / 1ps
`include "counts.vh"
module tb_road_dynamic_postprocess;
	reg clk = 0, rstn = 0, table_valid = 0, input_valid = 0, output_ready = 0;
	reg [9:0]table_addr = 0;
	reg signed [15:0]table_data = 0;
	reg [95:0]accumulators = 0, multipliers = 0;
	reg [17:0]shifts = 0;
	reg [31:0]post_multiplier = 1;
	reg [5:0]post_shift = 0;
	reg activate = 0, input_fault = 0;
	reg [2:0]mask = 7;
	reg [47:0]tags = 0;
	wire table_ready, table_loaded, input_ready, output_valid, output_int16, fault;
	wire signed [15:0]output_data;
	wire [15:0]output_tag;
	reg [15:0]table_words [0:1023];
	reg [47:0]expected_results;
	reg [47:0]expected_tags;
	reg [2:0]expected_mask;
	reg expected_int16;
	integer file_handle, trace_handle, fields, batch, lane, cycles = 0;
	integer start_cycle, core_sum = 0, raw_sum = 0, activated_sum = 0;
	integer result_count = 0, seed = 42, noise, hold_count, stage, variant;
	reg [32:0]held_payload;
	reg held = 0;
	always #5 clk = !clk;
	always @(posedge clk) begin
		cycles = cycles + 1;
		if (cycles > 1000000) $fatal(1, "watchdog");
		if (!rstn) held = 0;
		else begin
			if (held && (!output_valid || {output_int16, output_tag, output_data} !== held_payload)) $fatal(1, "held output changed");
			held = output_valid && !output_ready;
			held_payload = {output_int16, output_tag, output_data};
		end
	end
	road_dynamic_postprocess dut(
		.i_clk(clk), .i_rstn(rstn), .i_table_valid(table_valid), .i_table_addr(table_addr), .i_table_data(table_data),
		.o_table_ready(table_ready), .o_table_loaded(table_loaded), .i_input_valid(input_valid),
		.i_accumulators(accumulators), .i_pre_multipliers(multipliers), .i_pre_shifts(shifts),
		.i_post_multiplier(post_multiplier), .i_post_shift(post_shift), .i_activate(activate),
		.i_lane_mask(mask), .i_tags(tags), .i_input_fault(input_fault), .o_input_ready(input_ready),
		.i_output_ready(output_ready), .o_output_valid(output_valid), .o_output_data(output_data),
		.o_output_tag(output_tag), .o_output_int16(output_int16), .o_fault(fault)
	);
	task reset_and_load;
		integer address;
		begin
			@(negedge clk); rstn = 0; input_valid = 0; table_valid = 0; output_ready = 0;
			repeat (3) @(negedge clk);
			rstn = 1;
			for (address = 0; address < 1024; address = address + 1) begin
				@(negedge clk); table_valid = 1; table_addr = address; table_data = table_words[address];
				@(posedge clk);
				if (!table_ready || input_ready || output_valid) $fatal(1, "load protocol");
			end
			@(negedge clk); table_valid = 0;
			if (!table_loaded || !input_ready) $fatal(1, "table not loaded");
		end
	endtask
	task send_batch;
		begin
			@(negedge clk); input_valid = 1;
			@(posedge clk);
			while (!input_ready) @(posedge clk);
			start_cycle = cycles;
			@(negedge clk); input_valid = 0;
		end
	endtask
	initial begin
		$readmemh("table.hex", table_words);
		file_handle = $fopen("batches.txt", "r");
		trace_handle = $fopen("results.csv", "w");
		if (!file_handle || !trace_handle) $fatal(1, "file open");
		reset_and_load;
		for (batch = 0; batch < `BATCH_COUNT; batch = batch + 1) begin
			fields = $fscanf(file_handle, "%h %h %h %h %h %h %h %h %h\n", accumulators, multipliers, shifts, post_multiplier, post_shift, activate, mask, tags, expected_results);
			if (fields != 9) $fatal(1, "vector parse");
			expected_tags = tags; expected_mask = mask; expected_int16 = !activate; input_fault = 0;
			send_batch;
			// 输入接受后故意改变所有输入字段，输出须仍使用缓存参数。
			accumulators = 0; multipliers = 0; shifts = 0; post_multiplier = 0; post_shift = 0;
			activate = !activate; tags = 48'hffffffffffff; mask = 0;
			hold_count = 0;
			for (lane = 0; lane < 3; lane = lane + 1) begin
				if (expected_mask[lane]) begin
					begin: wait_result
						forever begin
							@(negedge clk);
							noise = $random(seed) & 32'h7fffffff;
							if (batch % 17 == 0 && output_valid && hold_count < 64) begin
								output_ready = 0; hold_count = hold_count + 1;
								// 队列满时尝试下一输入，但必须保持反压。
								input_valid = 1;
							end else begin output_ready = noise % 4 != 0; input_valid = 0; end
							@(posedge clk);
							if (input_ready || fault) $fatal(1, "busy input or unexpected fault");
							if (output_valid && output_ready) begin
								if (output_tag !== expected_tags[lane*16 +: 16] || output_data !== expected_results[lane*16 +: 16] || output_int16 !== expected_int16) $fatal(1, "batch=%0d lane=%0d data=%h expected=%h", batch, lane, output_data, expected_results[lane*16 +: 16]);
								$fdisplay(trace_handle, "%0d,%0d,%0d", output_tag, $signed(output_data), output_int16);
								result_count = result_count + 1;
								disable wait_result;
							end
						end
					end
				end
			end
			core_sum = core_sum + cycles - start_cycle;
			if (expected_int16) raw_sum = raw_sum + cycles - start_cycle;
			else activated_sum = activated_sum + cycles - start_cycle;
			@(negedge clk); input_valid = 0;
		end
		$fclose(file_handle); $fclose(trace_handle);
		$display("NUMERIC_PASS batches=%0d outputs=%0d core_cycles=%0d raw=%0d activated=%0d", `BATCH_COUNT, result_count, core_sum, raw_sum, activated_sum);
		// 每个处理/导出状态中复位，恢复后先重装表，不能漏出旧结果。
		for (stage = 1; stage <= 8; stage = stage + 1) begin
			accumulators = {32'd512, 32'd256, 32'd128}; multipliers = {32'd1,32'd1,32'd1};
			shifts = 0; post_multiplier = 1; post_shift = 4; activate = 1; mask = 7; tags = 48'habcdabcdabcd;
			send_batch;
			while (dut.state_current != stage) @(negedge clk);
			#1 rstn = 0; input_valid = 0; output_ready = 1;
			#1 if (output_valid || input_ready) $fatal(1, "reset not immediate");
			repeat (3) @(negedge clk);
			rstn = 1;
			repeat (50) begin @(posedge clk); if (output_valid || input_ready) $fatal(1, "reset ghost or stale table"); end
			reset_and_load;
		end
		// 装表中复位及恢复；完整装表前必须禁止启动。
		@(negedge clk); rstn = 0;
		repeat (3) @(negedge clk); rstn = 1;
		for (stage = 0; stage < 12; stage = stage + 1) begin
			@(negedge clk); table_valid = 1; table_addr = stage; table_data = table_words[stage];
			@(posedge clk); if (input_ready || output_valid) $fatal(1, "partial load started");
		end
		reset_and_load;
		for (variant = 0; variant < 6; variant = variant + 1) begin
			accumulators = 0; multipliers = {32'd1,32'd1,32'd1}; shifts = 0;
			post_multiplier = 1; post_shift = 0; activate = 1; mask = 7; input_fault = 0;
			case (variant)
				0: input_fault = 1;
				1: shifts[17:12] = 63;
				2: multipliers[95] = 1;
				3: post_shift = 63;
				4: post_multiplier = 32'h80000000;
				5: mask = 0;
			endcase
			send_batch;
			repeat (80) begin @(posedge clk); if (!fault || output_valid || input_ready) $fatal(1, "atomic fault failure"); end
			reset_and_load;
		end
		// 恢复后实际提交新结果；无效 lane 的坏系数应被忽略。
		accumulators = 4; multipliers = {32'h80000000, 32'h80000000, 32'd1};
		shifts = {6'd63, 6'd63, 6'd0}; activate = 0; post_shift = 63;
		post_multiplier = 32'h80000000; mask = 1; tags = 48'h004200420042; input_fault = 0;
		send_batch;
		@(negedge clk); output_ready = 1;
		@(posedge clk); while (!output_valid) @(posedge clk);
		if (fault || output_data !== 16'd4 || output_tag !== 16'h42 || !output_int16) $fatal(1, "recovery result");
		@(negedge clk);
		repeat (30) begin @(posedge clk); if (output_valid) $fatal(1, "duplicate recovery result"); end
		// 顺序错误的装表必须锁故障；复位再重装才恢复。
		@(negedge clk); rstn = 0;
		repeat (3) @(negedge clk); rstn = 1;
		@(negedge clk); table_valid = 1; table_addr = 1; table_data = 0;
		@(posedge clk); @(negedge clk); table_valid = 0;
		repeat (20) begin @(posedge clk); if (!fault || input_ready || output_valid) $fatal(1, "table order fault"); end
		reset_and_load;
		$display("TB_PASS_DYNAMIC_POSTPROCESS reset_stages=8 partial_table=1 atomic_faults=6 recovery=1 table_fault=1");
		$finish;
	end
endmodule
