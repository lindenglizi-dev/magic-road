`timescale 1ns / 1ps

// Independent streaming, arithmetic, handshake, backpressure, and reset checker.
module tb_road_mac_stream;

	parameter MAX_VECTORS = 160;

	reg i_clk = 1'b0;
	reg i_rstn = 1'b0;
	reg i_input_valid = 1'b0;
	reg i_first = 1'b0;
	reg i_last = 1'b0;
	reg [7:0]i_lane_mask = 8'd0;
	reg [63:0]i_activation_data = 64'd0;
	reg [191:0]i_weight_data = 192'd0;
	reg [95:0]i_bias_data = 96'd0;
	reg i_result_ready = 1'b0;

	wire o_input_ready;
	wire o_result_valid;
	wire [95:0]o_result_data;
	wire o_fault;
	wire [56:0]dot_bank_observed;
	wire [101:0]candidate_bank_observed;
	wire [98:0]accumulator_bank_observed;
	wire [8:0]pipeline_valid_observed;

	integer vec_case [0:MAX_VECTORS-1];
	integer vec_beat [0:MAX_VECTORS-1];
	integer vec_first [0:MAX_VECTORS-1];
	integer vec_last [0:MAX_VECTORS-1];
	integer vec_gap [0:MAX_VECTORS-1];
	integer vec_stall [0:MAX_VECTORS-1];
	integer vec_blocked_probe [0:MAX_VECTORS-1];
	reg [7:0]vec_mask [0:MAX_VECTORS-1];
	reg [63:0]vec_activation [0:MAX_VECTORS-1];
	reg [191:0]vec_weight [0:MAX_VECTORS-1];
	reg [95:0]vec_bias [0:MAX_VECTORS-1];
	reg [56:0]vec_dot [0:MAX_VECTORS-1];
	reg [101:0]vec_candidate [0:MAX_VECTORS-1];
	reg [98:0]vec_accumulator [0:MAX_VECTORS-1];
	integer vec_fault [0:MAX_VECTORS-1];
	reg [95:0]vec_result [0:MAX_VECTORS-1];
	integer accept_cycle [0:MAX_VECTORS-1];

	reg [2047:0]vector_path = 0;
	reg [2047:0]trace_path = 0;
	integer vector_file = 0;
	integer trace_file = 0;
	integer scan_count = 0;
	integer vector_count = 0;
	integer cycle_count = 0;
	integer error_count = 0;
	integer current_drive_index = -1;
	integer reset_probe_active = 0;
	integer last_pending = 0;
	integer last_accept_cycle = -1;
	integer accept_count = 0;
	integer dot_check_count = 0;
	integer candidate_check_count = 0;
	integer result_count = 0;
	integer fault_count = 0;
	integer reset_count = 0;
	integer ghost_window_count = 0;
	integer ii_one_intervals = 0;
	integer bubble_intervals = 0;
	integer monitor_index = 0;
	integer monitor_scan = 0;
	integer previous_accept_index = -1;
	integer interval = 0;
	integer expected_interval = 0;
	reg [95:0]held_result = 96'd0;
	reg held_fault = 1'b0;

	always #5 i_clk = ~i_clk;

	road_mac_probe road_mac_probe_Inst_dut(
		.i_clk(i_clk), .i_rstn(i_rstn), .i_input_valid(i_input_valid),
		.i_first(i_first), .i_last(i_last), .i_lane_mask(i_lane_mask),
		.i_activation_data(i_activation_data), .i_weight_data(i_weight_data),
		.i_bias_data(i_bias_data), .i_result_ready(i_result_ready),
		.o_input_ready(o_input_ready), .o_result_valid(o_result_valid),
		.o_result_data(o_result_data), .o_fault(o_fault)
	);

	assign dot_bank_observed = {
		road_mac_probe_Inst_dut.reg_dot_gamma,
		road_mac_probe_Inst_dut.reg_dot_beta,
		road_mac_probe_Inst_dut.reg_dot_alpha
	};
	assign candidate_bank_observed = {
		road_mac_probe_Inst_dut.reg_candidate_gamma,
		road_mac_probe_Inst_dut.reg_candidate_beta,
		road_mac_probe_Inst_dut.reg_candidate_alpha
	};
	assign accumulator_bank_observed = {
		road_mac_probe_Inst_dut.reg_accumulator_gamma,
		road_mac_probe_Inst_dut.reg_accumulator_beta,
		road_mac_probe_Inst_dut.reg_accumulator_alpha
	};
	assign pipeline_valid_observed = {
		3'b000,
		road_mac_probe_Inst_dut.flag_final_valid_stage0,
		road_mac_probe_Inst_dut.flag_candidate_valid,
		road_mac_probe_Inst_dut.flag_dot_valid,
		road_mac_probe_Inst_dut.flag_quad_valid,
		road_mac_probe_Inst_dut.flag_pair_valid,
		road_mac_probe_Inst_dut.flag_product_valid
	};

	always@(posedge i_clk)begin
		cycle_count = cycle_count + 1;
		if(i_rstn && i_input_valid && o_input_ready)begin
			if(reset_probe_active == 0)begin
				if((current_drive_index < 0) || (accept_cycle[current_drive_index] >= 0))begin
					$display("TB_ERROR unexpected_or_duplicate_accept cycle=%0d index=%0d", cycle_count, current_drive_index);
					error_count = error_count + 1;
				end else begin
					accept_cycle[current_drive_index] = cycle_count;
					accept_count = accept_count + 1;
					$fwrite(trace_file, "%0d,accept,%0d,%0d,%0d,%0d,%024h\n", cycle_count,
						vec_case[current_drive_index], vec_beat[current_drive_index], 0, 0, 96'd0);
					if((previous_accept_index >= 0) &&
					   (vec_case[previous_accept_index] == vec_case[current_drive_index]))begin
						interval = cycle_count - accept_cycle[previous_accept_index];
						expected_interval = vec_gap[current_drive_index] + 1;
						if(interval != expected_interval)begin
							$display("TB_ERROR accept_interval index=%0d got=%0d exp=%0d",
								current_drive_index, interval, expected_interval);
							error_count = error_count + 1;
						end
						if(interval == 1) ii_one_intervals = ii_one_intervals + 1;
						else bubble_intervals = bubble_intervals + 1;
					end
					previous_accept_index = current_drive_index;
					if(vec_last[current_drive_index] != 0)begin
						last_pending = 1;
						last_accept_cycle = cycle_count;
					end
				end
			end
		end
		if(i_rstn && o_result_valid && i_result_ready)begin
			last_pending = 0;
		end
		#1;
		if(i_rstn && last_pending && o_input_ready)begin
			$display("TB_ERROR input_reopened_before_result_handshake cycle=%0d", cycle_count);
			error_count = error_count + 1;
		end
		for(monitor_scan = 0; monitor_scan < vector_count; monitor_scan = monitor_scan + 1)begin
			if(accept_cycle[monitor_scan] >= 0)begin
				if(cycle_count == accept_cycle[monitor_scan] + 4)begin
					if((road_mac_probe_Inst_dut.flag_dot_valid !== 1'b1) ||
					   (dot_bank_observed !== vec_dot[monitor_scan]))begin
						$display("TB_ERROR dot index=%0d got=%015h exp=%015h",
							monitor_scan, dot_bank_observed, vec_dot[monitor_scan]);
						error_count = error_count + 1;
					end
					dot_check_count = dot_check_count + 1;
					$fwrite(trace_file, "%0d,dot,%0d,%0d,0,4,%024h\n", cycle_count,
						vec_case[monitor_scan], vec_beat[monitor_scan], {39'd0, dot_bank_observed});
				end
				if(cycle_count == accept_cycle[monitor_scan] + 5)begin
					if((road_mac_probe_Inst_dut.flag_candidate_valid !== 1'b1) ||
					   (candidate_bank_observed !== vec_candidate[monitor_scan]) ||
					   (accumulator_bank_observed !== vec_accumulator[monitor_scan]))begin
						$display("TB_ERROR candidate index=%0d got=%026h exp=%026h acc=%025h exp_acc=%025h",
							monitor_scan, candidate_bank_observed, vec_candidate[monitor_scan],
							accumulator_bank_observed, vec_accumulator[monitor_scan]);
						error_count = error_count + 1;
					end
					candidate_check_count = candidate_check_count + 1;
					$fwrite(trace_file, "%0d,candidate,%0d,%0d,%0d,5,%024h\n", cycle_count,
						vec_case[monitor_scan], vec_beat[monitor_scan], vec_fault[monitor_scan],
						accumulator_bank_observed[95:0]);
				end
			end
		end
	end

	task drive_vector;
		input integer index;
		begin
			i_first = vec_first[index][0];
			i_last = vec_last[index][0];
			i_lane_mask = vec_mask[index];
			i_activation_data = vec_activation[index];
			i_weight_data = vec_weight[index];
			i_bias_data = vec_bias[index];
			current_drive_index = index;
			i_input_valid = 1'b1;
		end
	endtask

	task drive_sequence;
		input integer first_index;
		input integer last_index;
		integer index;
		integer gap_index;
		begin
			for(index = first_index; index <= last_index; index = index + 1)begin
				for(gap_index = 0; gap_index < vec_gap[index]; gap_index = gap_index + 1)begin
					@(negedge i_clk);
					i_input_valid = 1'b0;
					current_drive_index = -1;
				end
				@(negedge i_clk);
				drive_vector(index);
				while(accept_cycle[index] < 0)begin
					@(posedge i_clk);
					#2;
				end
			end
			@(negedge i_clk);
			i_input_valid = 1'b0;
			current_drive_index = -1;
		end
	endtask

	task wait_result;
		input integer index;
		integer hold_index;
		integer expected_cycle;
		begin
			expected_cycle = accept_cycle[index] + 6;
			if(vec_blocked_probe[index] != 0)begin
				@(negedge i_clk);
				i_input_valid = 1'b1;
				i_first = 1'b1;
				i_last = 1'b1;
				i_lane_mask = 8'h5a;
				i_activation_data = 64'h8877665544332211;
				i_weight_data = 192'h123456789abcdef0112233445566778899aabbccddeeff00;
				i_bias_data = 96'hfedcba987654321001234567;
				current_drive_index = -1;
			end
			while(cycle_count < expected_cycle)begin
				@(posedge i_clk);
				#2;
				if((cycle_count < expected_cycle) && o_result_valid)begin
					$display("TB_ERROR early_result index=%0d latency=%0d", index, cycle_count-accept_cycle[index]);
					error_count = error_count + 1;
				end
			end
			if((cycle_count != expected_cycle) || !o_result_valid ||
			   (o_fault !== vec_fault[index][0]) || (o_result_data !== vec_result[index]))begin
				$display("TB_ERROR result index=%0d cycle=%0d/%0d valid=%0b fault=%0b/%0b data=%024h/%024h",
					index, cycle_count, expected_cycle, o_result_valid, o_fault,
					vec_fault[index][0], o_result_data, vec_result[index]);
				error_count = error_count + 1;
			end
			if((vec_fault[index] != 0) && (o_result_data !== 96'd0))begin
				$display("TB_ERROR atomic_fault_nonzero index=%0d", index);
				error_count = error_count + 1;
			end
			result_count = result_count + 1;
			if(vec_fault[index] != 0) fault_count = fault_count + 1;
			$fwrite(trace_file, "%0d,result_valid,%0d,%0d,%0d,6,%024h\n", cycle_count,
				vec_case[index], vec_beat[index], vec_fault[index], o_result_data);
			held_result = o_result_data;
			held_fault = o_fault;
			for(hold_index = 0; hold_index < vec_stall[index]; hold_index = hold_index + 1)begin
				@(posedge i_clk);
				#2;
				if(!o_result_valid || (o_result_data !== held_result) || (o_fault !== held_fault) || o_input_ready)begin
					$display("TB_ERROR stalled_output index=%0d hold=%0d", index, hold_index);
					error_count = error_count + 1;
				end
			end
			@(negedge i_clk);
			i_input_valid = 1'b0;
			current_drive_index = -1;
			i_result_ready = 1'b1;
			@(posedge i_clk);
			#2;
			$fwrite(trace_file, "%0d,result_accept,%0d,%0d,%0d,%0d,%024h\n", cycle_count,
				vec_case[index], vec_beat[index], vec_fault[index], cycle_count-accept_cycle[index], held_result);
			@(negedge i_clk);
			i_result_ready = 1'b0;
			#1;
			if(o_result_valid || !o_input_ready)begin
				$display("TB_ERROR result_release index=%0d valid=%0b ready=%0b", index, o_result_valid, o_input_ready);
				error_count = error_count + 1;
			end
		end
	endtask

	task reset_pipeline_stage;
		input integer offset;
		integer wait_index;
		begin
			while(!o_input_ready) @(negedge i_clk);
			@(negedge i_clk);
			reset_probe_active = 1;
			i_first = 1'b1;
			i_last = 1'b1;
			i_lane_mask = 8'hff;
			i_activation_data = {8{8'hfe}};
			i_weight_data = {24{8'h03}};
			i_bias_data = 96'd0;
			i_input_valid = 1'b1;
			@(posedge i_clk);
			#2;
			@(negedge i_clk);
			i_input_valid = 1'b0;
			for(wait_index = 0; wait_index < offset; wait_index = wait_index + 1)begin
				@(posedge i_clk);
				#2;
			end
			@(negedge i_clk);
			i_rstn = 1'b0;
			#1;
			reset_count = reset_count + 1;
			$fwrite(trace_file, "%0d,reset_assert,%0d,%0d,0,%0d,%024h\n",
				cycle_count, 100+offset, offset, offset, o_result_data);
			if((o_input_ready !== 1'b1) || (o_result_valid !== 1'b0) ||
			   (o_result_data !== 96'd0) || (o_fault !== 1'b0) ||
			   (pipeline_valid_observed !== 9'd0) ||
			   (accumulator_bank_observed !== 99'd0))begin
				$display("TB_ERROR reset_clear offset=%0d ready=%0b valid=%0b pipe=%03h acc=%025h",
					offset, o_input_ready, o_result_valid, pipeline_valid_observed, accumulator_bank_observed);
				error_count = error_count + 1;
			end
			repeat(2) @(posedge i_clk);
			@(negedge i_clk);
			i_rstn = 1'b1;
			reset_probe_active = 0;
			last_pending = 0;
			for(wait_index = 0; wait_index < 15; wait_index = wait_index + 1)begin
				@(posedge i_clk);
				#2;
				if(o_result_valid)begin
					$display("TB_ERROR ghost_after_reset offset=%0d ghost=%0d", offset, wait_index);
					error_count = error_count + 1;
				end
				ghost_window_count = ghost_window_count + 1;
			end
		end
	endtask

	initial begin
		for(monitor_index = 0; monitor_index < MAX_VECTORS; monitor_index = monitor_index + 1)
			accept_cycle[monitor_index] = -1;
		if(!$value$plusargs("VECTORS=%s", vector_path)) vector_path = "stream_vectors.txt";
		if(!$value$plusargs("TRACE=%s", trace_path)) trace_path = "stream_trace.csv";
		vector_file = $fopen(vector_path, "r");
		trace_file = $fopen(trace_path, "w");
		if((vector_file == 0) || (trace_file == 0))begin
			$display("TB_ERROR cannot_open_input_or_trace");
			$finish;
		end
		$fwrite(trace_file, "cycle,event,case,beat,fault,latency_or_offset,data\n");
		while((!$feof(vector_file)) && (vector_count < MAX_VECTORS))begin
			scan_count = $fscanf(vector_file,
				"%d %d %d %d %d %d %d %h %h %h %h %h %h %h %d %h\n",
				vec_case[vector_count], vec_beat[vector_count], vec_first[vector_count],
				vec_last[vector_count], vec_gap[vector_count], vec_stall[vector_count],
				vec_blocked_probe[vector_count], vec_mask[vector_count],
				vec_activation[vector_count], vec_weight[vector_count], vec_bias[vector_count],
				vec_dot[vector_count], vec_candidate[vector_count], vec_accumulator[vector_count],
				vec_fault[vector_count], vec_result[vector_count]);
			if(scan_count == 16) vector_count = vector_count + 1;
			else if(scan_count != -1)begin
				$display("TB_ERROR malformed_vector index=%0d fields=%0d", vector_count, scan_count);
				$finish;
			end
		end
		$fclose(vector_file);
		// 在同一黄金输入上另跑64拍输出背压，不改变数值向量。
		if($test$plusargs("LONG_HOLD"))begin
			for(monitor_index = 0; monitor_index < vector_count; monitor_index = monitor_index + 1)
				if(vec_last[monitor_index] != 0) vec_stall[monitor_index] = 64;
		end
		if(vector_count != 123)begin
			$display("TB_ERROR vector_count got=%0d exp=123", vector_count);
			$finish;
		end

		repeat(4) @(posedge i_clk);
		@(negedge i_clk);
		i_rstn = 1'b1;
		#1;
		if(!o_input_ready || o_result_valid || o_fault)begin
			$display("TB_ERROR reset_release");
			error_count = error_count + 1;
		end

		monitor_index = 0;
		while(monitor_index < vector_count)begin : run_all_vectors
			integer final_index;
			final_index = monitor_index;
			while((final_index < vector_count - 1) && (vec_last[final_index] == 0))
				final_index = final_index + 1;
			drive_sequence(monitor_index, final_index);
			wait_result(final_index);
			monitor_index = final_index + 1;
		end

		for(monitor_index = 0; monitor_index <= 9; monitor_index = monitor_index + 1)
			reset_pipeline_stage(monitor_index);

		if((error_count == 0) && (accept_count == 123) && (dot_check_count == 123) &&
		   (candidate_check_count == 123) && (result_count == 17) && (fault_count == 9) &&
		   (reset_count == 10) && (ii_one_intervals >= 80))begin
			$display("TB_PASS_MAC_STREAM vectors=%0d accepts=%0d dots=%0d candidates=%0d results=%0d faults=%0d ii1=%0d bubbles=%0d resets=%0d ghost_window=%0d latency=6",
				vector_count, accept_count, dot_check_count, candidate_check_count,
				result_count, fault_count, ii_one_intervals, bubble_intervals,
				reset_count, ghost_window_count);
		end else begin
			$display("TB_FAIL_MAC_STREAM errors=%0d vectors=%0d accepts=%0d dots=%0d candidates=%0d results=%0d faults=%0d ii1=%0d bubbles=%0d resets=%0d ghost_window=%0d",
				error_count, vector_count, accept_count, dot_check_count, candidate_check_count,
				result_count, fault_count, ii_one_intervals, bubble_intervals,
				reset_count, ghost_window_count);
		end
		$fclose(trace_file);
		$finish;
	end

	initial begin
		#5000000;
		$display("TB_FAIL_MAC_STREAM timeout");
		$finish;
	end

endmodule
