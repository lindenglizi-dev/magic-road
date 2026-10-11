`timescale 1ns / 1ps

module tb_down2_overlap_tile_runner;

	reg i_clk = 1'b0;
	reg i_rstn = 1'b0;
	reg i_table_valid = 1'b0;
	reg [9:0]i_table_addr = 10'd0;
	reg signed [15:0]i_table_data = 16'sd0;
	reg i_load_valid = 1'b0;
	reg [2:0]i_load_kind = 3'd0;
	reg [10:0]i_load_addr = 11'd0;
	reg signed [31:0]i_load_data = 32'sd0;
	reg i_start = 1'b0;
	reg i_pw_only = 1'b0;
	reg i_commit_ready = 1'b1;
	reg i_export_start = 1'b0;
	reg i_output_ready = 1'b0;

	wire o_table_ready;
	wire o_table_loaded;
	wire o_table_fault;
	wire o_load_ready;
	wire o_busy;
	wire o_done;
	wire o_fault;
	wire o_output_valid;
	wire signed [7:0]o_output_data;
	wire [8:0]o_output_index;
	wire o_export_done;
	wire o_debug_valid;
	wire [1:0]o_debug_phase;
	wire o_debug_layer;
	wire [3:0]o_debug_position;
	wire [4:0]o_debug_channel;
	wire signed [31:0]o_debug_value;
	wire [31:0]o_preload_writes;
	wire [31:0]o_core_cycles;
	wire [31:0]o_mac_cycles;
	wire [31:0]o_pre_cycles;
	wire [31:0]o_silu_cycles;
	wire [31:0]o_post_cycles;
	wire [31:0]o_writeback_cycles;
	wire [31:0]o_storage_wait_cycles;
	wire [31:0]o_scheduler_idle_cycles;
	wire [31:0]o_export_cycles;
	wire [1:0]o_result_queue_count;
	wire o_result_reserved;
	wire [3:0]o_meta_count;
	wire [31:0]o_mac_result_count;
	wire [31:0]o_pre_accept_count;
	wire [31:0]o_silu_accept_count;
	wire [31:0]o_post_accept_count;
	wire [31:0]o_writeback_count;

	reg signed [15:0]mem_silu [0:1023];
	reg signed [7:0]mem_halo [0:1295];
	reg signed [7:0]mem_pw_input [0:255];
	reg signed [7:0]mem_dw_weight [0:143];
	reg signed [31:0]mem_dw_bias [0:15];
	reg signed [7:0]mem_pw_weight [0:383];
	reg signed [31:0]mem_pw_bias [0:23];
	reg signed [31:0]mem_expected_stage [0:2559];
	reg signed [7:0]mem_expected_output [0:383];

	integer cycle_count = 0;
	integer start_cycle = 0;
	integer preload_start_cycle = 0;
	integer preload_endpoint_cycles = 0;
	integer table_write_count = 0;
	integer done_cycle = 0;
	integer acc_count = 0;
	integer pre_count = 0;
	integer silu_count = 0;
	integer post_count = 0;
	integer expected_record_count = 0;
	integer export_index = 0;
	integer error_count = 0;
	integer case_index = 0;
	integer record_index = 0;
	integer record_offset = 0;
	integer expected_layer = 0;
	integer expected_position = 0;
	integer expected_channel = 0;
	integer expected_phase = 0;
	integer expected_preload = 0;
	integer dw_endpoint = 0;
	integer pw_endpoint = 0;
	integer max_capacity = 0;
	integer max_meta = 0;
	integer trace_job_count = 0;
	integer trace_storage_cycles = 0;
	integer trace_send_cycles = 0;
	integer trace_wait_cycles = 0;
	integer trace_post_cycles = 0;
	integer trace_input_accepts = 0;
	integer turn_dw_jobs = 0;
	integer turn_pw_jobs = 0;
	integer turn_first_accept = 0;
	integer turn_last_accept = 0;
	integer turn_result_ack = 0;
	integer random_commit_stalls = 0;
	integer ack_local_high_accepts = 0;
	integer cache_write_compare_count = 0;
	integer cache_load_write_count = 0;
	integer cache_commit_write_count = 0;
	integer dw_mac_beat_count = 0;
	integer dw_mac_result_count = 0;
	integer dw_post_scalar_count = 0;
	integer dw_tail_scalar_count = 0;
	integer dw_post_queue_wait_count = 0;
	integer dw_post_ready_wait_count = 0;
	integer union_test_index = 0;
	integer dw_address = 0;
	integer state_storage_count = 0;
	integer state_send_count = 0;
	integer state_wait_count = 0;
	integer state_dw_post_count = 0;
	integer state_drain_count = 0;
	integer state_done_count = 0;
	integer state_other_count = 0;
	reg check_active = 1'b0;
	reg check_pw_only = 1'b0;
	reg commit_stall_enable = 1'b0;
	reg seen_pw = 1'b0;
	reg held_valid = 1'b0;
	reg signed [7:0]held_data = 8'sd0;
	reg [8:0]held_index = 9'd0;
	reg trace_job_active = 1'b0;
	reg turn_capture_active = 1'b0;
	reg turn_waiting_next = 1'b0;
	reg turn_layer_pw = 1'b0;
	reg ack_local_force_active = 1'b0;
	reg reference_cache_write = 1'b0;
	reg reference_cache_known = 1'b1;
	reg [10:0]reference_cache_address = 11'd0;
	reg signed [7:0]reference_cache_data = 8'sd0;
	reg [15:0]commit_lfsr = 16'h5eed;
	reg [255:0]seen_dw_address = 256'd0;
	reg probe_reserved = 1'b0;
	reg [1:0]probe_queue = 2'd0;
	reg probe_fault = 1'b0;
	reg probe_ready = 1'b0;
	reg [3:0]probe_counter_state = 4'd0;
	reg [4:0]probe_counter_output = 5'd0;
	reg [3:0]probe_counter_position = 4'd0;
	reg probe_counter_start = 1'b0;
	reg probe_counter_mac_accept = 1'b0;
	reg probe_counter_mac_fault = 1'b0;
	reg probe_counter_layer_pw = 1'b0;
	reg probe_counter_pp_accept = 1'b0;
	reg [1:0]probe_counter_dw_lane = 2'd0;
	reg [8:0]probe_counter_dw_writes = 9'd0;
	reg probe_counter_pp_fault = 1'b0;
	reg probe_counter_load_fault = 1'b0;
	wire [1:0]probe_old_capacity;
	wire probe_old_can_reserve;
	wire probe_old_first_valid;
	wire probe_old_first_accept;
	wire probe_old_continue_accept;

	assign probe_old_capacity = {1'b0, probe_reserved} + probe_queue;
	assign probe_old_can_reserve = (~probe_reserved) && (probe_old_capacity < 2'd2) && (~probe_fault);
	assign probe_old_first_valid = probe_old_can_reserve;
	assign probe_old_first_accept = probe_old_first_valid && probe_ready;
	assign probe_old_continue_accept = 1'b1 && probe_ready;

	always #5 i_clk = ~i_clk;

	always@(posedge i_clk)begin
		cycle_count = cycle_count + 1;
		if(check_active && ack_local_force_active &&
		   down2_overlap_tile_runner_Inst_tb.flag_mac_result_accept)
			ack_local_high_accepts = ack_local_high_accepts + 1;
	end

	// Compare the reachable old two-write behavior with the new unified cache port every cycle.
	always@(posedge i_clk)begin
		if(i_rstn)begin
			reference_cache_write = 1'b0;
			reference_cache_known = 1'b1;
			reference_cache_address = 11'd0;
			reference_cache_data = 8'sd0;
			if(down2_overlap_tile_runner_Inst_tb.flag_load_accept &&
			   (i_load_kind == 3'd1) &&
			   ((i_load_addr == down2_overlap_tile_runner_Inst_tb.cnt_expected_dw_cache) ||
			    (i_load_addr == 11'd0)))begin
				reference_cache_write = 1'b1;
				reference_cache_address = i_load_addr;
				reference_cache_data = i_load_data[7:0];
				cache_load_write_count = cache_load_write_count + 1;
			end
			if(down2_overlap_tile_runner_Inst_tb.flag_commit_accept)begin
				if((down2_overlap_tile_runner_Inst_tb.pp_output_tag[15] !== 1'b0) &&
				   (down2_overlap_tile_runner_Inst_tb.pp_output_tag[15] !== 1'b1))begin
					$display("TB_ERROR_CACHE_PORT commit layer tag is X/Z");
					error_count = error_count + 1;
					reference_cache_known = 1'b0;
				end else if(down2_overlap_tile_runner_Inst_tb.pp_output_tag[15] == 1'b0)begin
					if((^down2_overlap_tile_runner_Inst_tb.pp_output_tag[14:6]) === 1'bx)begin
						$display("TB_ERROR_CACHE_PORT DW commit address tag is X/Z");
						error_count = error_count + 1;
						reference_cache_known = 1'b0;
					end else begin
						reference_cache_write = 1'b1;
						reference_cache_address =
							down2_overlap_tile_runner_Inst_tb.pp_output_tag[14:11] * 16 +
							down2_overlap_tile_runner_Inst_tb.pp_output_tag[10:6];
						reference_cache_data = down2_overlap_tile_runner_Inst_tb.pp_output_data;
						cache_commit_write_count = cache_commit_write_count + 1;
						if(down2_overlap_tile_runner_Inst_tb.pp_output_tag[10:6] > 5'd15)begin
							$display("TB_ERROR_CACHE_PORT reachable DW channel exceeds 15");
							error_count = error_count + 1;
						end
					end
				end
			end
			if(reference_cache_known)begin
				if(reference_cache_write !==
				   (down2_overlap_tile_runner_Inst_tb.flag_dw_cache_write === 1'b1))begin
					$display("TB_ERROR_CACHE_PORT enable mismatch old=%b new=%b",
					         reference_cache_write,
					         down2_overlap_tile_runner_Inst_tb.flag_dw_cache_write);
					error_count = error_count + 1;
				end
				if(reference_cache_write)begin
					cache_write_compare_count = cache_write_compare_count + 1;
					if(reference_cache_address > 11'd255)begin
						$display("TB_ERROR_CACHE_PORT full address exceeds 255 addr=%0d", reference_cache_address);
						error_count = error_count + 1;
					end
					if((down2_overlap_tile_runner_Inst_tb.wire_dw_cache_write_address !==
					    reference_cache_address[7:0]) ||
					   (down2_overlap_tile_runner_Inst_tb.wire_dw_cache_write_data !== reference_cache_data))begin
						$display("TB_ERROR_CACHE_PORT payload mismatch old_addr=%0d new_addr=%0d old_data=%0d new_data=%0d",
						         reference_cache_address,
						         down2_overlap_tile_runner_Inst_tb.wire_dw_cache_write_address,
						         reference_cache_data,
						         down2_overlap_tile_runner_Inst_tb.wire_dw_cache_write_data);
						error_count = error_count + 1;
					end
				end
			end
		end
	end

	// Keep the parent table request asserted in each active MAC wait; child table-valid stays gated off.
	always@(negedge i_clk)begin
		if(check_active && (down2_overlap_tile_runner_Inst_tb.state_current == 4'd3))begin
			force down2_overlap_tile_runner_Inst_tb.i_table_valid = 1'b1;
			ack_local_force_active = 1'b1;
			#1;
			if(down2_overlap_tile_runner_Inst_tb.flag_mac_result_ready_local !==
			   ((down2_overlap_tile_runner_Inst_tb.state_current == 4'd3) &&
			    down2_overlap_tile_runner_Inst_tb.flag_result_reserved &&
			    down2_overlap_tile_runner_Inst_tb.pp_input_ready))begin
				$display("TB_ERROR_ACK_LOCAL old/new ready mismatch");
				error_count = error_count + 1;
			end
		end else if(ack_local_force_active)begin
			release down2_overlap_tile_runner_Inst_tb.i_table_valid;
			ack_local_force_active = 1'b0;
		end
	end

	// Read-only job-turnaround timestamps for two representative DW and PW jobs.
	always@(posedge i_clk or negedge i_rstn)begin
		if(!i_rstn)begin
			turn_dw_jobs = 0;
			turn_pw_jobs = 0;
			turn_first_accept = 0;
			turn_last_accept = 0;
			turn_result_ack = 0;
			turn_capture_active = 1'b0;
			turn_waiting_next = 1'b0;
			turn_layer_pw = 1'b0;
		end else if((case_index == 0) && check_active)begin
			if(down2_overlap_tile_runner_Inst_tb.flag_mac_input_accept &&
			   !down2_overlap_tile_runner_Inst_tb.cnt_mac_group)begin
				if(turn_waiting_next)begin
					$display("JOB_TURN_TRACE layer=%s first=%0d last=%0d ack=%0d next_first=%0d first_to_last=%0d last_to_ack=%0d ack_to_next=%0d",
					         turn_layer_pw ? "PW" : "DW", turn_first_accept,
					         turn_last_accept, turn_result_ack, cycle_count,
					         turn_last_accept - turn_first_accept,
					         turn_result_ack - turn_last_accept,
					         cycle_count - turn_result_ack);
					if((turn_last_accept - turn_first_accept != (turn_layer_pw ? 2 : 4)) ||
					   (turn_result_ack - turn_last_accept != 10) ||
					   (cycle_count - turn_result_ack != (turn_layer_pw ? 2 : 7)))begin
						$display("TB_ERROR_JOB_TURN layer=%s", turn_layer_pw ? "PW" : "DW");
						error_count = error_count + 1;
					end
					turn_waiting_next = 1'b0;
				end
				if((!down2_overlap_tile_runner_Inst_tb.flag_layer_pw && turn_dw_jobs < 2) ||
				   (down2_overlap_tile_runner_Inst_tb.flag_layer_pw && turn_pw_jobs < 2))begin
					turn_capture_active = 1'b1;
					turn_layer_pw = down2_overlap_tile_runner_Inst_tb.flag_layer_pw;
					turn_first_accept = cycle_count;
					if(down2_overlap_tile_runner_Inst_tb.flag_layer_pw)
						turn_pw_jobs = turn_pw_jobs + 1;
					else turn_dw_jobs = turn_dw_jobs + 1;
				end else turn_capture_active = 1'b0;
			end else if(down2_overlap_tile_runner_Inst_tb.flag_mac_input_accept &&
			            down2_overlap_tile_runner_Inst_tb.cnt_mac_group &&
			            turn_capture_active)begin
				turn_last_accept = cycle_count;
			end
			if(down2_overlap_tile_runner_Inst_tb.flag_mac_result_accept && turn_capture_active)begin
				turn_result_ack = cycle_count;
				turn_waiting_next = 1'b1;
				turn_capture_active = 1'b0;
			end
		end
	end

	// Mutually exclusive runner-state accounting for the first four no-stall jobs.
	always@(posedge i_clk or negedge i_rstn)begin
		if(!i_rstn)begin
			trace_job_count = 0;
			trace_storage_cycles = 0;
			trace_send_cycles = 0;
			trace_wait_cycles = 0;
			trace_post_cycles = 0;
			trace_input_accepts = 0;
			trace_job_active = 1'b0;
		end else if((case_index == 0) && check_active && (trace_job_count < 4))begin
			if(!trace_job_active &&
			   (down2_overlap_tile_runner_Inst_tb.state_current == 4'd1) &&
			   (down2_overlap_tile_runner_Inst_tb.cnt_mac_group == 1'b0))begin
				trace_job_active = 1'b1;
				trace_storage_cycles = 0;
				trace_send_cycles = 0;
				trace_wait_cycles = 0;
				trace_post_cycles = 0;
				trace_input_accepts = 0;
			end
			if(trace_job_active)begin
				case(down2_overlap_tile_runner_Inst_tb.state_current)
					4'd1: trace_storage_cycles = trace_storage_cycles + 1;
					4'd2: trace_send_cycles = trace_send_cycles + 1;
					4'd3: trace_wait_cycles = trace_wait_cycles + 1;
					4'd9: trace_post_cycles = trace_post_cycles + 1;
					default: begin end
				endcase
				if(down2_overlap_tile_runner_Inst_tb.flag_mac_input_accept)
					trace_input_accepts = trace_input_accepts + 1;
				if((down2_overlap_tile_runner_Inst_tb.flag_layer_pw &&
				    down2_overlap_tile_runner_Inst_tb.flag_mac_result_accept) ||
				   ((!down2_overlap_tile_runner_Inst_tb.flag_layer_pw) &&
				    down2_overlap_tile_runner_Inst_tb.flag_pp_input_accept &&
				    (down2_overlap_tile_runner_Inst_tb.cnt_dw_post_lane + 1'b1 ==
				     down2_overlap_tile_runner_Inst_tb.wire_dw_post_count)))begin
					$display("JOB_TRACE job=%0d storage=%0d send=%0d wait=%0d post=%0d accepts=%0d total=%0d",
					         trace_job_count, trace_storage_cycles, trace_send_cycles,
					         trace_wait_cycles, trace_post_cycles, trace_input_accepts,
					         trace_storage_cycles + trace_send_cycles + trace_wait_cycles + trace_post_cycles);
					if((trace_storage_cycles != 3) || (trace_send_cycles != 3) ||
					   (trace_wait_cycles != 10) || (trace_post_cycles != 5) ||
					   (trace_input_accepts != 3))begin
						$display("TB_ERROR_JOB_TRACE job=%0d", trace_job_count);
						error_count = error_count + 1;
					end
					trace_job_count = trace_job_count + 1;
					trace_job_active = 1'b0;
				end
			end
		end
	end

	function integer stage_record;
		input layer;
		input [3:0]position;
		input [4:0]channel;
		begin
			if(check_pw_only) stage_record = position * 24 + channel;
			else if(!layer) stage_record = position * 16 + channel;
			else stage_record = 256 + position * 24 + channel;
		end
	endfunction

	task check_stage;
		input [1:0]phase;
		input layer;
		input [3:0]position;
		input [4:0]channel;
		input signed [31:0]value;
		integer stage_address;
		begin
			stage_address = stage_record(layer, position, channel) * 4 + phase;
			if($signed(value) !== $signed(mem_expected_stage[stage_address]))begin
				$display("TB_ERROR_STAGE case=%0d phase=%0d layer=%0d pos=%0d ch=%0d got=%0d exp=%0d",
				         case_index, phase, layer, position, channel, $signed(value),
				         $signed(mem_expected_stage[stage_address]));
				error_count = error_count + 1;
			end
		end
	endtask

	always@(posedge i_clk)begin
		if(check_active)begin
			if((o_result_queue_count + o_result_reserved) > 2)begin
				$display("TB_ERROR_CREDIT q=%0d r=%0d", o_result_queue_count, o_result_reserved);
				error_count = error_count + 1;
			end
			if(o_meta_count > 6)begin
				$display("TB_ERROR_META_COUNT count=%0d", o_meta_count);
				error_count = error_count + 1;
			end
			if((o_result_queue_count + o_result_reserved) > max_capacity)
				max_capacity = o_result_queue_count + o_result_reserved;
			if(o_meta_count > max_meta) max_meta = o_meta_count;
			case(down2_overlap_tile_runner_Inst_tb.state_current)
				4'd1: state_storage_count = state_storage_count + 1;
				4'd2: state_send_count = state_send_count + 1;
				4'd3: state_wait_count = state_wait_count + 1;
				4'd4, 4'd5: state_drain_count = state_drain_count + 1;
				4'd6: state_done_count = state_done_count + 1;
				4'd9: state_dw_post_count = state_dw_post_count + 1;
				default: state_other_count = state_other_count + 1;
			endcase
			if(!check_pw_only && !seen_pw && down2_overlap_tile_runner_Inst_tb.flag_layer_pw)begin
				seen_pw = 1'b1;
				dw_endpoint = cycle_count - start_cycle;
			end
			if(down2_overlap_tile_runner_Inst_tb.flag_mac_input_accept &&
			   !down2_overlap_tile_runner_Inst_tb.flag_layer_pw)begin
				dw_mac_beat_count = dw_mac_beat_count + 1;
				if(((down2_overlap_tile_runner_Inst_tb.cnt_mac_group < 2'd2) &&
				    (down2_overlap_tile_runner_Inst_tb.reg_mac_mask !== 8'hff)) ||
				   ((down2_overlap_tile_runner_Inst_tb.cnt_mac_group == 2'd2) &&
				    (down2_overlap_tile_runner_Inst_tb.reg_mac_mask !== 8'h1f)))begin
					$display("TB_ERROR_TRIPLET_MASK group=%0d mask=%h",
					         down2_overlap_tile_runner_Inst_tb.cnt_mac_group,
					         down2_overlap_tile_runner_Inst_tb.reg_mac_mask);
					error_count = error_count + 1;
				end
				if(down2_overlap_tile_runner_Inst_tb.cnt_position[1:0] == 2'd3)begin
					if((down2_overlap_tile_runner_Inst_tb.reg_mac_weight[191:64] !== 128'd0) ||
					   (down2_overlap_tile_runner_Inst_tb.reg_mac_bias[95:32] !== 64'd0))begin
						$display("TB_ERROR_TRIPLET_TAIL inactive lane payload is nonzero");
						error_count = error_count + 1;
					end
					for(expected_phase = 0; expected_phase < 8; expected_phase = expected_phase + 1)begin
						union_test_index = down2_overlap_tile_runner_Inst_tb.cnt_mac_group * 8 + expected_phase;
						if((union_test_index < 21) && ((union_test_index % 7) >= 3) &&
						   (down2_overlap_tile_runner_Inst_tb.reg_mac_activation[expected_phase*8 +:8] !== 8'd0))begin
							$display("TB_ERROR_TRIPLET_TAIL halo OOB did not zero union=%0d value=%0d",
							         union_test_index,
							         $signed(down2_overlap_tile_runner_Inst_tb.reg_mac_activation[expected_phase*8 +:8]));
							error_count = error_count + 1;
						end
					end
				end else if((down2_overlap_tile_runner_Inst_tb.reg_mac_bias[31:0] !==
				             down2_overlap_tile_runner_Inst_tb.reg_mac_bias[63:32]) ||
				            (down2_overlap_tile_runner_Inst_tb.reg_mac_bias[31:0] !==
				             down2_overlap_tile_runner_Inst_tb.reg_mac_bias[95:64]))begin
					$display("TB_ERROR_TRIPLET_BIAS valid spatial lanes differ");
					error_count = error_count + 1;
				end
			end
			if((down2_overlap_tile_runner_Inst_tb.state_current == 4'd9) &&
			   !down2_overlap_tile_runner_Inst_tb.flag_pp_input_valid)
				dw_post_queue_wait_count = dw_post_queue_wait_count + 1;
			if(down2_overlap_tile_runner_Inst_tb.flag_pp_input_valid &&
			   !down2_overlap_tile_runner_Inst_tb.pp_input_ready)
				dw_post_ready_wait_count = dw_post_ready_wait_count + 1;
			if(down2_overlap_tile_runner_Inst_tb.flag_pp_input_accept &&
			   !down2_overlap_tile_runner_Inst_tb.flag_layer_pw)begin
				dw_address = down2_overlap_tile_runner_Inst_tb.wire_pp_position * 16 +
				             down2_overlap_tile_runner_Inst_tb.cnt_output;
				if((dw_address < 0) || (dw_address > 255) || seen_dw_address[dw_address])begin
					$display("TB_ERROR_TRIPLET_ADDRESS addr=%0d duplicate=%0d", dw_address,
					         (dw_address >= 0 && dw_address <= 255) ? seen_dw_address[dw_address] : 1'bx);
					error_count = error_count + 1;
				end else begin
					seen_dw_address[dw_address] = 1'b1;
				end
				if((down2_overlap_tile_runner_Inst_tb.wire_result_lane_mask !==
				    (3'b001 << down2_overlap_tile_runner_Inst_tb.wire_dw_lane)) ||
				   ((down2_overlap_tile_runner_Inst_tb.wire_result_channel_base +
				     down2_overlap_tile_runner_Inst_tb.wire_dw_lane) !==
				    down2_overlap_tile_runner_Inst_tb.cnt_output))begin
					$display("TB_ERROR_TRIPLET_METADATA pos=%0d ch=%0d base=%0d lane=%0d mask=%b",
					         down2_overlap_tile_runner_Inst_tb.wire_pp_position,
					         down2_overlap_tile_runner_Inst_tb.cnt_output,
					         down2_overlap_tile_runner_Inst_tb.wire_result_channel_base,
					         down2_overlap_tile_runner_Inst_tb.wire_dw_lane,
					         down2_overlap_tile_runner_Inst_tb.wire_result_lane_mask);
					error_count = error_count + 1;
				end
				dw_post_scalar_count = dw_post_scalar_count + 1;
				if(down2_overlap_tile_runner_Inst_tb.cnt_position[1:0] == 2'd3)
					dw_tail_scalar_count = dw_tail_scalar_count + 1;
			end
			if(down2_overlap_tile_runner_Inst_tb.flag_mac_result_accept)begin
				if(down2_overlap_tile_runner_Inst_tb.flag_layer_pw)begin
					for(expected_phase = 0; expected_phase < 3; expected_phase = expected_phase + 1)begin
						check_stage(2'd0, down2_overlap_tile_runner_Inst_tb.flag_layer_pw,
						            down2_overlap_tile_runner_Inst_tb.cnt_position,
						            down2_overlap_tile_runner_Inst_tb.wire_result_channel_base + expected_phase,
						            $signed(down2_overlap_tile_runner_Inst_tb.mac_result_data[expected_phase*32 +: 32]));
						acc_count = acc_count + 1;
					end
				end else begin
					dw_mac_result_count = dw_mac_result_count + 1;
					for(expected_phase = 0;
					    expected_phase < down2_overlap_tile_runner_Inst_tb.wire_dw_post_count;
					    expected_phase = expected_phase + 1)begin
						check_stage(2'd0, 1'b0,
						            down2_overlap_tile_runner_Inst_tb.cnt_position + expected_phase,
						            down2_overlap_tile_runner_Inst_tb.cnt_output,
						            $signed(down2_overlap_tile_runner_Inst_tb.mac_result_data[expected_phase*32 +: 32]));
						acc_count = acc_count + 1;
					end
				end
			end
			if(down2_overlap_tile_runner_Inst_tb.pp_silu_accept)begin
				check_stage(2'd1,
				            down2_overlap_tile_runner_Inst_tb.road_postprocess_stream_Inst_tile.pre_result_tag[15],
				            down2_overlap_tile_runner_Inst_tb.road_postprocess_stream_Inst_tile.pre_result_tag[14:11],
				            down2_overlap_tile_runner_Inst_tb.road_postprocess_stream_Inst_tile.pre_result_tag[10:6],
				            $signed(down2_overlap_tile_runner_Inst_tb.road_postprocess_stream_Inst_tile.pre_result_data));
				pre_count = pre_count + 1;
			end
			if(down2_overlap_tile_runner_Inst_tb.pp_post_accept)begin
				check_stage(2'd2,
				            down2_overlap_tile_runner_Inst_tb.road_postprocess_stream_Inst_tile.reg_meta_fifo[down2_overlap_tile_runner_Inst_tb.road_postprocess_stream_Inst_tile.cnt_meta_read][15],
				            down2_overlap_tile_runner_Inst_tb.road_postprocess_stream_Inst_tile.reg_meta_fifo[down2_overlap_tile_runner_Inst_tb.road_postprocess_stream_Inst_tile.cnt_meta_read][14:11],
				            down2_overlap_tile_runner_Inst_tb.road_postprocess_stream_Inst_tile.reg_meta_fifo[down2_overlap_tile_runner_Inst_tb.road_postprocess_stream_Inst_tile.cnt_meta_read][10:6],
				            $signed(down2_overlap_tile_runner_Inst_tb.road_postprocess_stream_Inst_tile.silu_output_data));
				silu_count = silu_count + 1;
			end
			if(down2_overlap_tile_runner_Inst_tb.flag_commit_accept)begin
				check_stage(2'd3,
				            down2_overlap_tile_runner_Inst_tb.pp_output_tag[15],
				            down2_overlap_tile_runner_Inst_tb.pp_output_tag[14:11],
				            down2_overlap_tile_runner_Inst_tb.pp_output_tag[10:6],
				            $signed(down2_overlap_tile_runner_Inst_tb.road_postprocess_stream_Inst_tile.post_result_data));
				post_count = post_count + 1;
			end
		end
	end

	task reset_dut;
	begin
		i_rstn = 1'b0;
		i_table_valid = 1'b0;
		i_load_valid = 1'b0;
		i_start = 1'b0;
		i_export_start = 1'b0;
		i_output_ready = 1'b0;
		i_commit_ready = 1'b1;
		repeat(5) @(negedge i_clk);
		i_rstn = 1'b1;
		repeat(3) @(negedge i_clk);
		if(o_busy || o_done || o_output_valid || o_table_loaded || o_fault)begin
			$display("TB_ERROR_RESET outputs not cancelled");
			error_count = error_count + 1;
		end
	end
	endtask

	task load_table;
	integer index;
	begin
		table_write_count = 0;
		for(index = 0; index < 1024; index = index + 1)begin
			@(negedge i_clk);
			i_table_valid = 1'b1;
			i_table_addr = index[9:0];
			i_table_data = mem_silu[index];
			while(!o_table_ready) @(negedge i_clk);
			if(index == 0) preload_start_cycle = cycle_count + 1;
			table_write_count = table_write_count + 1;
		end
		@(negedge i_clk);
		i_table_valid = 1'b0;
		if(!o_table_loaded || o_table_fault)begin
			$display("TB_ERROR_TABLE load failed loaded=%0d fault=%0d", o_table_loaded, o_table_fault);
			error_count = error_count + 1;
		end
	end
	endtask

	task load_kind;
	input [2:0]kind;
	input integer count;
	integer index;
	begin
		for(index = 0; index < count; index = index + 1)begin
			@(negedge i_clk);
			i_load_valid = 1'b1;
			i_load_kind = kind;
			i_load_addr = index[10:0];
			case(kind)
				3'd0: i_load_data = {{24{mem_halo[index][7]}}, mem_halo[index]};
				3'd1: i_load_data = {{24{mem_pw_input[index][7]}}, mem_pw_input[index]};
				3'd2: i_load_data = {{24{mem_dw_weight[index][7]}}, mem_dw_weight[index]};
				3'd3: i_load_data = mem_dw_bias[index];
				3'd4: i_load_data = {{24{mem_pw_weight[index][7]}}, mem_pw_weight[index]};
				default: i_load_data = mem_pw_bias[index];
			endcase
			while(!o_load_ready) @(negedge i_clk);
		end
		@(negedge i_clk);
		i_load_valid = 1'b0;
	end
	endtask

	task preload_case;
	input pw_only;
	begin
		if(pw_only)begin
			load_kind(3'd1, 256);
		end else begin
			load_kind(3'd0, 1296);
			load_kind(3'd2, 144);
			load_kind(3'd3, 16);
		end
		load_kind(3'd4, 384);
		load_kind(3'd5, 24);
		expected_preload = pw_only ? 664 : 1864;
		if(o_preload_writes !== expected_preload)begin
			$display("TB_ERROR_PRELOAD got=%0d exp=%0d", o_preload_writes, expected_preload);
			error_count = error_count + 1;
		end
	end
	endtask

	task start_and_wait;
	input pw_only;
	begin
		acc_count = 0;
		pre_count = 0;
		silu_count = 0;
		post_count = 0;
		check_pw_only = pw_only;
		expected_record_count = pw_only ? 384 : 640;
		seen_pw = pw_only;
		dw_endpoint = 0;
		max_capacity = 0;
		max_meta = 0;
		dw_mac_beat_count = 0;
		dw_mac_result_count = 0;
		dw_post_scalar_count = 0;
		dw_tail_scalar_count = 0;
		dw_post_queue_wait_count = 0;
		dw_post_ready_wait_count = 0;
		seen_dw_address = 256'd0;
		state_storage_count = 0;
		state_send_count = 0;
		state_wait_count = 0;
		state_dw_post_count = 0;
		state_drain_count = 0;
		state_done_count = 0;
		state_other_count = 0;
		commit_stall_enable = (case_index == 2);
		commit_lfsr = 16'h5eed;
		random_commit_stalls = 0;
		@(negedge i_clk);
		i_pw_only = pw_only;
		i_start = 1'b1;
		@(negedge i_clk);
		i_start = 1'b0;
		start_cycle = cycle_count;
		preload_endpoint_cycles = start_cycle - preload_start_cycle;
		check_active = 1'b1;
		repeat(12) @(negedge i_clk);
		i_table_valid = 1'b1;
		i_table_addr = 10'd0;
		i_table_data = 16'sd123;
		@(negedge i_clk);
		if(o_table_ready)begin
			$display("TB_ERROR_TABLE_GUARD table accepted during core");
			error_count = error_count + 1;
		end
		i_table_valid = 1'b0;
		while(!o_done && !o_fault)begin
			@(negedge i_clk);
			if(commit_stall_enable)begin
				commit_lfsr = {commit_lfsr[14:0],
				               commit_lfsr[15] ^ commit_lfsr[13] ^
				               commit_lfsr[12] ^ commit_lfsr[10]};
				i_commit_ready = commit_lfsr[0] | commit_lfsr[3];
				if(!i_commit_ready) random_commit_stalls = random_commit_stalls + 1;
			end else begin
				i_commit_ready = 1'b1;
			end
		end
		i_commit_ready = 1'b1;
		done_cycle = cycle_count;
		check_active = 1'b0;
		if(o_fault)begin
			$display("TB_ERROR_CORE fault before done case=%0d", case_index);
			error_count = error_count + 1;
		end
		if((acc_count != expected_record_count) || (pre_count != expected_record_count) ||
		   (silu_count != expected_record_count) || (post_count != expected_record_count))begin
			$display("TB_ERROR_STAGE_COUNT acc=%0d pre=%0d silu=%0d post=%0d exp=%0d",
			         acc_count, pre_count, silu_count, post_count, expected_record_count);
			error_count = error_count + 1;
		end
		if(!pw_only && ((dw_mac_beat_count != 384) || (dw_mac_result_count != 128) ||
		                (dw_post_scalar_count != 256) || (dw_tail_scalar_count != 64) ||
		                (seen_dw_address !== {256{1'b1}}) ||
		                (dw_post_queue_wait_count == 0)))begin
			$display("TB_ERROR_TRIPLET_COUNT beats=%0d results=%0d scalars=%0d tail=%0d queue_wait=%0d ready_wait=%0d unique_all=%0d",
			         dw_mac_beat_count, dw_mac_result_count, dw_post_scalar_count,
			         dw_tail_scalar_count, dw_post_queue_wait_count, dw_post_ready_wait_count,
			         seen_dw_address === {256{1'b1}});
			error_count = error_count + 1;
		end
		if((done_cycle - start_cycle) !== o_core_cycles)begin
			$display("TB_ERROR_ENDPOINT diff=%0d core=%0d", done_cycle - start_cycle, o_core_cycles);
			error_count = error_count + 1;
		end
		if((state_storage_count + state_send_count + state_wait_count +
		    state_dw_post_count + state_drain_count + state_done_count +
		    state_other_count) != o_core_cycles)begin
			$display("TB_ERROR_STATE_ACCOUNT storage=%0d send=%0d wait=%0d dw_post=%0d drain=%0d done=%0d other=%0d core=%0d",
			         state_storage_count, state_send_count, state_wait_count,
			         state_dw_post_count, state_drain_count, state_done_count,
			         state_other_count, o_core_cycles);
			error_count = error_count + 1;
		end
		if(!pw_only && ((state_storage_count != 640) || (state_send_count != 640) ||
		                (state_wait_count != 2560) || (state_dw_post_count != 384) ||
		                (state_drain_count != 56) || (state_done_count != 1) ||
		                (state_other_count != 0)))begin
			$display("TB_ERROR_FULL_STATE_COUNTS storage=%0d send=%0d wait=%0d dw_post=%0d drain=%0d done=%0d other=%0d",
			         state_storage_count, state_send_count, state_wait_count,
			         state_dw_post_count, state_drain_count, state_done_count,
			         state_other_count);
			error_count = error_count + 1;
		end
		$display("CYCLE_RESULT case=%0d preload=%0d core=%0d endpoint=%0d mac=%0d pre=%0d silu=%0d post=%0d writeback=%0d storage_wait=%0d scheduler_idle=%0d",
		         case_index, o_preload_writes, o_core_cycles, done_cycle - start_cycle,
		         o_mac_cycles, o_pre_cycles, o_silu_cycles, o_post_cycles,
		         o_writeback_cycles, o_storage_wait_cycles, o_scheduler_idle_cycles);
		$display("PRELOAD_RESULT case=%0d endpoint=%0d table_writes=%0d cache_writes=%0d",
		         case_index, preload_endpoint_cycles, table_write_count, o_preload_writes);
		pw_endpoint = check_pw_only ? o_core_cycles : o_core_cycles - dw_endpoint;
		$display("OVERLAP_RESULT case=%0d dw_endpoint=%0d pw_endpoint=%0d max_credit=%0d max_meta=%0d mac_results=%0d pre_accepts=%0d silu_accepts=%0d post_accepts=%0d writebacks=%0d",
		         case_index, dw_endpoint, pw_endpoint, max_capacity, max_meta,
		         o_mac_result_count, o_pre_accept_count, o_silu_accept_count,
		         o_post_accept_count, o_writeback_count);
		if(!pw_only)
			$display("TRIPLET_RESULT case=%0d tasks=%0d beats=%0d scalars=%0d tail_scalars=%0d queue_wait=%0d ready_wait=%0d",
			         case_index, dw_mac_result_count, dw_mac_beat_count, dw_post_scalar_count,
			         dw_tail_scalar_count, dw_post_queue_wait_count, dw_post_ready_wait_count);
		$display("STATE_ACCOUNT_RESULT case=%0d storage=%0d send=%0d wait=%0d dw_post=%0d drain=%0d done=%0d other=%0d sum=%0d",
		         case_index, state_storage_count, state_send_count, state_wait_count,
		         state_dw_post_count, state_drain_count, state_done_count,
		         state_other_count, state_storage_count + state_send_count + state_wait_count +
		         state_dw_post_count + state_drain_count + state_done_count + state_other_count);
		if(commit_stall_enable)
			$display("RANDOM_COMMIT_RESULT case=%0d seed=5eed stall_cycles=%0d",
			         case_index, random_commit_stalls);
	end
	endtask

	task export_and_check;
	begin
		export_index = 0;
		held_valid = 1'b0;
		@(negedge i_clk);
		i_export_start = 1'b1;
		@(negedge i_clk);
		i_export_start = 1'b0;
		while(!o_export_done)begin
			@(negedge i_clk);
			i_output_ready = ((cycle_count % 7) != 3);
			if(held_valid && ((o_output_data !== held_data) || (o_output_index !== held_index)))begin
				$display("TB_ERROR_BACKPRESSURE data/index changed while stalled");
				error_count = error_count + 1;
			end
			held_valid = o_output_valid && !i_output_ready;
			held_data = o_output_data;
			held_index = o_output_index;
			if(o_output_valid && i_output_ready)begin
				if((o_output_index !== export_index[8:0]) ||
				   ($signed(o_output_data) !== $signed(mem_expected_output[export_index])))begin
					$display("TB_ERROR_OUTPUT index=%0d/%0d got=%0d exp=%0d",
					         o_output_index, export_index, $signed(o_output_data),
					         $signed(mem_expected_output[export_index]));
					error_count = error_count + 1;
				end
				export_index = export_index + 1;
			end
			@(posedge i_clk);
		end
		i_output_ready = 1'b0;
		if(export_index != 384)begin
			$display("TB_ERROR_EXPORT_COUNT got=%0d", export_index);
			error_count = error_count + 1;
		end
		$display("EXPORT_RESULT case=%0d transfers=%0d cycles=%0d", case_index, export_index, o_export_cycles);
	end
	endtask

	task run_full_case;
	input integer which_case;
	begin
		case_index = which_case;
		case(which_case)
			0:begin
				$readmemh("vectors/edge_full_halo.hex", mem_halo);
				$readmemh("vectors/edge_full_stages.hex", mem_expected_stage);
				$readmemh("vectors/edge_full_output.hex", mem_expected_output);
			end
			1:begin
				$readmemh("vectors/interior_full_halo.hex", mem_halo);
				$readmemh("vectors/interior_full_stages.hex", mem_expected_stage);
				$readmemh("vectors/interior_full_output.hex", mem_expected_output);
			end
			default:begin
				$readmemh("vectors/bottom_right_full_halo.hex", mem_halo);
				$readmemh("vectors/bottom_right_full_stages.hex", mem_expected_stage);
				$readmemh("vectors/bottom_right_full_output.hex", mem_expected_output);
			end
		endcase
		reset_dut;
		load_table;
		preload_case(1'b0);
		start_and_wait(1'b0);
		export_and_check;
	end
	endtask

	task reset_inflight_probe;
	integer index;
	begin
		case_index = 4;
		$readmemh("vectors/pw_standalone_pw_input.hex", mem_pw_input);
		reset_dut;
		load_table;
		preload_case(1'b1);
		@(negedge i_clk);
		i_pw_only = 1'b1;
		i_start = 1'b1;
		@(negedge i_clk);
		i_start = 1'b0;
		repeat(12) @(negedge i_clk);
		if(!o_busy)begin
			$display("TB_ERROR_RESET_PROBE did not enter core");
			error_count = error_count + 1;
		end
		i_rstn = 1'b0;
		repeat(3) @(negedge i_clk);
		if(o_busy || o_done || o_output_valid || o_debug_valid || o_table_loaded)begin
			$display("TB_ERROR_RESET_PROBE in-flight state not cancelled");
			error_count = error_count + 1;
		end
		i_rstn = 1'b1;
		for(index = 0; index < 20; index = index + 1)begin
			@(negedge i_clk);
			if(o_done || o_output_valid || o_debug_valid)begin
				$display("TB_ERROR_RESET_PROBE ghost event cycle=%0d", index);
				error_count = error_count + 1;
			end
		end
		$display("RESET_RESULT in_flight_cancel=pass ghost_window=20");
	end
	endtask

	task reset_dw_post_probe;
	integer hold_index;
	integer target_lane;
	integer ghost_index;
	reg [1:0]held_lane;
	reg [95:0]held_triplet;
	reg [95:0]held_pp_data;
	reg [3:0]held_pp_position;
	reg [4:0]held_pp_channel_base;
	reg [2:0]held_pp_mask;
	begin
		case_index = 6;
		$readmemh("vectors/edge_full_halo.hex", mem_halo);
		reset_dut;
		load_table;
		preload_case(1'b0);
		@(negedge i_clk);
		i_pw_only = 1'b0;
		i_start = 1'b1;
		@(negedge i_clk);
		i_start = 1'b0;
		for(target_lane = 0; target_lane < 3; target_lane = target_lane + 1)begin
			while((down2_overlap_tile_runner_Inst_tb.state_current != 4'd9) ||
			      (down2_overlap_tile_runner_Inst_tb.cnt_dw_post_lane != target_lane))
				@(negedge i_clk);
			held_lane = down2_overlap_tile_runner_Inst_tb.cnt_dw_post_lane;
			held_triplet = down2_overlap_tile_runner_Inst_tb.reg_dw_triplet_result;
			held_pp_data = down2_overlap_tile_runner_Inst_tb.wire_pp_result_data;
			held_pp_position = down2_overlap_tile_runner_Inst_tb.wire_pp_position;
			held_pp_channel_base = down2_overlap_tile_runner_Inst_tb.wire_result_channel_base;
			held_pp_mask = down2_overlap_tile_runner_Inst_tb.wire_result_lane_mask;
			force down2_overlap_tile_runner_Inst_tb.pp_input_ready = 1'b0;
			for(hold_index = 0; hold_index < 64; hold_index = hold_index + 1)begin
				@(negedge i_clk);
				if((down2_overlap_tile_runner_Inst_tb.state_current != 4'd9) ||
				   (down2_overlap_tile_runner_Inst_tb.cnt_dw_post_lane !== held_lane) ||
				   (down2_overlap_tile_runner_Inst_tb.reg_dw_triplet_result !== held_triplet) ||
				   (down2_overlap_tile_runner_Inst_tb.wire_pp_result_data !== held_pp_data) ||
				   (down2_overlap_tile_runner_Inst_tb.wire_pp_position !== held_pp_position) ||
				   (down2_overlap_tile_runner_Inst_tb.wire_result_channel_base !== held_pp_channel_base) ||
				   (down2_overlap_tile_runner_Inst_tb.wire_result_lane_mask !== held_pp_mask) ||
				   !down2_overlap_tile_runner_Inst_tb.flag_result_reserved)begin
					$display("TB_ERROR_DW_POST_BACKPRESSURE lane=%0d state/payload/meta/reservation changed",
					         target_lane);
					error_count = error_count + 1;
				end
			end
			if(target_lane < 2)
				release down2_overlap_tile_runner_Inst_tb.pp_input_ready;
		end
		i_rstn = 1'b0;
		repeat(2) @(negedge i_clk);
		release down2_overlap_tile_runner_Inst_tb.pp_input_ready;
		if(o_busy || o_done || o_output_valid || o_debug_valid || o_table_loaded ||
		   down2_overlap_tile_runner_Inst_tb.flag_result_reserved ||
		   (down2_overlap_tile_runner_Inst_tb.cnt_dw_post_lane != 2'd0))begin
			$display("TB_ERROR_DW_POST_RESET did not cancel buffered triplet");
			error_count = error_count + 1;
		end
		i_rstn = 1'b1;
		for(ghost_index = 0; ghost_index < 20; ghost_index = ghost_index + 1)begin
			@(negedge i_clk);
			if(o_done || o_output_valid || o_debug_valid)begin
				$display("TB_ERROR_DW_POST_RESET ghost event cycle=%0d", ghost_index);
				error_count = error_count + 1;
			end
		end
		$display("DW_POST_BACKPRESSURE_RESET_PASS lanes=3 hold_cycles_each=64 ghost_window=20");
	end
	endtask

	task fault_atomic_probe;
	integer index;
	begin
		case_index = 5;
		for(index = 0; index < 256; index = index + 1) mem_pw_input[index] = 8'sd127;
		for(index = 0; index < 384; index = index + 1) mem_pw_weight[index] = 8'sd127;
		for(index = 0; index < 24; index = index + 1) mem_pw_bias[index] = 32'sh7fffffff;
		reset_dut;
		load_table;
		preload_case(1'b1);
		@(negedge i_clk);
		i_pw_only = 1'b1;
		i_start = 1'b1;
		@(negedge i_clk);
		i_start = 1'b0;
		while(o_busy && !o_fault) @(negedge i_clk);
		if(!o_fault || o_done)begin
			$display("TB_ERROR_FAULT_PROBE fault=%0d done=%0d", o_fault, o_done);
			error_count = error_count + 1;
		end
		@(negedge i_clk);
		i_export_start = 1'b1;
		@(negedge i_clk);
		i_export_start = 1'b0;
		repeat(5)begin
			@(negedge i_clk);
			if(o_output_valid)begin
				$display("TB_ERROR_FAULT_PROBE partial tile became visible");
				error_count = error_count + 1;
			end
		end
		$display("FAULT_RESULT mac_overflow_atomic_publish=pass");
	end
	endtask

	task dw_triplet_numeric_probe;
	input integer target_lane;
	input integer polarity;
	input expect_fault;
	integer index;
	integer center_address;
	integer wait_cycles;
	begin
		case_index = 7;
		for(index = 0; index < 1296; index = index + 1) mem_halo[index] = 8'sd0;
		for(index = 0; index < 144; index = index + 1) mem_dw_weight[index] = 8'sd0;
		for(index = 0; index < 16; index = index + 1) mem_dw_bias[index] = 32'sd0;
		for(index = 0; index < 384; index = index + 1) mem_pw_weight[index] = 8'sd0;
		for(index = 0; index < 24; index = index + 1) mem_pw_bias[index] = 32'sd0;
		center_address = (9 + 1 + target_lane * 2) * 16;
		mem_halo[center_address] = expect_fault ? polarity * 2 : polarity;
		mem_dw_weight[4] = 8'sd1;
		mem_dw_bias[0] = (polarity > 0) ? 32'sh7ffffffe : 32'sh80000001;
		reset_dut;
		load_table;
		preload_case(1'b0);
		@(negedge i_clk);
		i_pw_only = 1'b0;
		i_start = 1'b1;
		@(negedge i_clk);
		i_start = 1'b0;
		wait_cycles = 0;
		while((o_mac_result_count == 0) && (wait_cycles < 100))begin
			@(negedge i_clk);
			wait_cycles = wait_cycles + 1;
		end
		if(expect_fault)begin
			if(!o_fault || o_done || (o_pre_accept_count != 0) ||
			   (o_writeback_count != 0) ||
			   (down2_overlap_tile_runner_Inst_tb.cnt_dw_writes != 0))begin
				$display("TB_ERROR_TRIPLET_FAULT lane=%0d polarity=%0d fault=%0d done=%0d pre=%0d wb=%0d dw_writes=%0d",
				         target_lane, polarity, o_fault, o_done, o_pre_accept_count,
				         o_writeback_count, down2_overlap_tile_runner_Inst_tb.cnt_dw_writes);
				error_count = error_count + 1;
			end
			@(negedge i_clk);
			i_export_start = 1'b1;
			@(negedge i_clk);
			i_export_start = 1'b0;
			repeat(5)begin
				@(negedge i_clk);
				if(o_output_valid)begin
					$display("TB_ERROR_TRIPLET_FAULT partial triplet became export-visible");
					error_count = error_count + 1;
				end
			end
		end else begin
			if(o_fault || down2_overlap_tile_runner_Inst_tb.mac_fault ||
			   (down2_overlap_tile_runner_Inst_tb.state_current != 4'd9))begin
				$display("TB_ERROR_TRIPLET_LIMIT lane=%0d polarity=%0d false fault or missing DW_POST",
				         target_lane, polarity);
				error_count = error_count + 1;
			end
		end
		$display("DW_TRIPLET_NUMERIC_RESULT lane=%0d polarity=%0d expected_fault=%0d pass=1",
		         target_lane, polarity, expect_fault);
	end
	endtask

	task cache_control_fault_probe;
		reg signed [7:0]saved_cache_zero;
	begin
		reset_dut;
		@(negedge i_clk);
		i_load_valid = 1'b1;
		i_load_kind = 3'd1;
		i_load_addr = 11'd0;
		i_load_data = 32'sh00000012;
		@(negedge i_clk);
		i_load_valid = 1'b0;
		saved_cache_zero = down2_overlap_tile_runner_Inst_tb.reg_dw_cache[0];
		if(saved_cache_zero !== 8'sh12)begin
			$display("TB_ERROR_CACHE_PORT valid preload did not write cache[0]");
			error_count = error_count + 1;
		end

		@(negedge i_clk);
		i_load_valid = 1'b1;
		i_load_kind = 3'd1;
		i_load_addr = 11'd256;
		i_load_data = 32'sh00000055;
		@(negedge i_clk);
		i_load_valid = 1'b0;
		repeat(2) @(negedge i_clk);
		if(!o_fault || (down2_overlap_tile_runner_Inst_tb.reg_dw_cache[0] !== saved_cache_zero))begin
			$display("TB_ERROR_CACHE_PORT invalid full address wrote cache or missed fault");
			error_count = error_count + 1;
		end

		reset_dut;
		@(negedge i_clk);
		i_load_valid = 1'b1;
		i_load_kind = 3'd1;
		i_load_addr = {11{1'bx}};
		i_load_data = 32'sh00000066;
		@(negedge i_clk);
		i_load_valid = 1'b0;
		i_load_addr = 11'd0;
		repeat(2) @(negedge i_clk);
		if(!o_fault || (down2_overlap_tile_runner_Inst_tb.reg_dw_cache[0] !== saved_cache_zero))begin
			$display("TB_ERROR_CACHE_PORT X address wrote cache or missed fault");
			error_count = error_count + 1;
		end

		reset_dut;
		@(negedge i_clk);
		i_load_valid = 1'b1;
		i_load_kind = 3'd1;
		i_load_addr = 11'd0;
		i_load_data = 32'sh00000077;
		i_rstn = 1'b0;
		repeat(2) @(negedge i_clk);
		if(down2_overlap_tile_runner_Inst_tb.reg_dw_cache[0] !== saved_cache_zero)begin
			$display("TB_ERROR_CACHE_PORT reset allowed a cache write");
			error_count = error_count + 1;
		end
		i_load_valid = 1'b0;
		i_rstn = 1'b1;
		repeat(3) @(negedge i_clk);

		@(negedge i_clk);
		i_table_valid = 1'b1;
		i_table_addr = 10'd1;
		i_table_data = 16'sd0;
		@(negedge i_clk);
		i_table_valid = 1'b0;
		repeat(2) @(negedge i_clk);
		if(!o_fault || o_load_ready)begin
			$display("TB_ERROR_CACHE_PORT IDLE table fault did not close load ready");
			error_count = error_count + 1;
		end
		i_load_valid = 1'b1;
		i_load_kind = 3'd1;
		i_load_addr = 11'd0;
		i_load_data = 32'sh00000033;
		@(negedge i_clk);
		i_load_valid = 1'b0;
		if(down2_overlap_tile_runner_Inst_tb.reg_dw_cache[0] !== saved_cache_zero)begin
			$display("TB_ERROR_CACHE_PORT IDLE table fault allowed a cache write");
			error_count = error_count + 1;
		end
		$display("CACHE_CONTROL_FAULT_PASS invalid_addr=256 x_addr=1 reset_no_write=1 idle_table_fault=1");
	end
	endtask

	function four_state_bit;
	input integer state_code;
	begin
		case(state_code)
			0: four_state_bit = 1'b0;
			1: four_state_bit = 1'b1;
			2: four_state_bit = 1'bx;
			default: four_state_bit = 1'bz;
		endcase
	end
	endfunction

	// Exhaustively compare the old and candidate reservation expressions in four-state simulation.
	task can_reserve_four_state_probe;
	integer reserved_code;
	integer queue_high_code;
	integer queue_low_code;
	integer fault_code;
	integer ready_code;
	integer comparison_count;
	begin
		comparison_count = 0;
		force down2_overlap_tile_runner_Inst_tb.flag_result_reserved = probe_reserved;
		force down2_overlap_tile_runner_Inst_tb.pp_result_queue_count = probe_queue;
		force down2_overlap_tile_runner_Inst_tb.pp_fault = probe_fault;
		force down2_overlap_tile_runner_Inst_tb.mac_input_ready = probe_ready;
		force down2_overlap_tile_runner_Inst_tb.state_current = 4'd2;
		for(reserved_code = 0; reserved_code < 4; reserved_code = reserved_code + 1)begin
			for(queue_high_code = 0; queue_high_code < 4; queue_high_code = queue_high_code + 1)begin
				for(queue_low_code = 0; queue_low_code < 4; queue_low_code = queue_low_code + 1)begin
					for(fault_code = 0; fault_code < 4; fault_code = fault_code + 1)begin
						for(ready_code = 0; ready_code < 4; ready_code = ready_code + 1)begin
							probe_reserved = four_state_bit(reserved_code);
							probe_queue = {four_state_bit(queue_high_code), four_state_bit(queue_low_code)};
							probe_fault = four_state_bit(fault_code);
							probe_ready = four_state_bit(ready_code);
							force down2_overlap_tile_runner_Inst_tb.cnt_mac_group = 2'd0;
							#1;
							if((down2_overlap_tile_runner_Inst_tb.flag_can_reserve !== probe_old_can_reserve) ||
							   (down2_overlap_tile_runner_Inst_tb.flag_mac_input_valid !== probe_old_first_valid) ||
							   (down2_overlap_tile_runner_Inst_tb.flag_mac_input_accept !== probe_old_first_accept))begin
								$display("TB_ERROR_CAN_RESERVE_4STATE reserved=%b queue=%b fault=%b ready=%b old=%b/%b/%b new=%b/%b/%b",
								         probe_reserved, probe_queue, probe_fault, probe_ready,
								         probe_old_can_reserve, probe_old_first_valid, probe_old_first_accept,
								         down2_overlap_tile_runner_Inst_tb.flag_can_reserve,
								         down2_overlap_tile_runner_Inst_tb.flag_mac_input_valid,
								         down2_overlap_tile_runner_Inst_tb.flag_mac_input_accept);
								error_count = error_count + 1;
							end
							force down2_overlap_tile_runner_Inst_tb.cnt_mac_group = 2'd1;
							#1;
							if((down2_overlap_tile_runner_Inst_tb.flag_mac_input_valid !== 1'b1) ||
							   (down2_overlap_tile_runner_Inst_tb.flag_mac_input_accept !== probe_old_continue_accept))begin
								$display("TB_ERROR_MAC_CONTINUE_4STATE reserved=%b queue=%b fault=%b ready=%b valid=%b accept=%b",
								         probe_reserved, probe_queue, probe_fault, probe_ready,
								         down2_overlap_tile_runner_Inst_tb.flag_mac_input_valid,
								         down2_overlap_tile_runner_Inst_tb.flag_mac_input_accept);
								error_count = error_count + 1;
							end
							comparison_count = comparison_count + 1;
						end
					end
				end
			end
		end
		release down2_overlap_tile_runner_Inst_tb.flag_result_reserved;
		release down2_overlap_tile_runner_Inst_tb.pp_result_queue_count;
		release down2_overlap_tile_runner_Inst_tb.pp_fault;
		release down2_overlap_tile_runner_Inst_tb.mac_input_ready;
		release down2_overlap_tile_runner_Inst_tb.state_current;
		release down2_overlap_tile_runner_Inst_tb.cnt_mac_group;
		$display("CAN_RESERVE_4STATE_PASS combinations=%0d mac_paths=%0d", comparison_count, comparison_count * 2);
	end
	endtask

	// Compare the extracted v15 counter events and transition against the v14 procedural hierarchy.
	task check_counter_transition_now;
	reg expected_clear;
	reg expected_increment;
	reg [4:0]expected_next;
	reg [4:0]candidate_next;
	begin
		expected_clear = 1'b0;
		expected_increment = 1'b0;
		case(probe_counter_state)
			4'd0:begin
				if(probe_counter_start) expected_clear = 1'b1;
			end
			4'd3:begin
				if(probe_counter_mac_accept)begin
					if(probe_counter_mac_fault)begin
					end else if(probe_counter_layer_pw == 1'b0)begin
					end else begin
						if(probe_counter_output < 5'd7) expected_increment = 1'b1;
						else if(probe_counter_position < 4'd15) expected_clear = 1'b1;
					end
				end
			end
			4'd9:begin
				if(probe_counter_pp_accept)begin
					if(probe_counter_dw_lane + 1'b1 ==
					   ((probe_counter_position[1:0] == 2'd0) ? 2'd3 : 2'd1))begin
						if(probe_counter_output < 5'd15) expected_increment = 1'b1;
						else if(probe_counter_position[1:0] == 2'd0) expected_clear = 1'b1;
						else if(probe_counter_position < 4'd15) expected_clear = 1'b1;
					end
				end
			end
			4'd4:begin
				if(probe_counter_dw_writes == 9'd256) expected_clear = 1'b1;
			end
			default:begin
				expected_clear = 1'b0;
				expected_increment = 1'b0;
			end
		endcase
		expected_next = probe_counter_output;
		if(probe_counter_pp_fault || probe_counter_load_fault)begin
		end else if(expected_clear)begin
			expected_next = 5'd0;
		end else if(expected_increment)begin
			expected_next = probe_counter_output + 1'b1;
		end
		// Let the forced source values propagate through the extracted event logic
		// before sampling the candidate transition.
		#1;
		candidate_next = probe_counter_output;
		if(probe_counter_pp_fault || probe_counter_load_fault)begin
		end else if(down2_overlap_tile_runner_Inst_tb.flag_cnt_output_clear)begin
			candidate_next = 5'd0;
		end else if(down2_overlap_tile_runner_Inst_tb.flag_cnt_output_increment)begin
			candidate_next = probe_counter_output + 1'b1;
		end
		if((down2_overlap_tile_runner_Inst_tb.flag_cnt_output_clear !== expected_clear) ||
		   (down2_overlap_tile_runner_Inst_tb.flag_cnt_output_increment !== expected_increment) ||
		   (candidate_next !== expected_next))begin
			$display("TB_ERROR_COUNTER_TRANSITION state=%b out=%b pos=%b start=%b macacc=%b macfault=%b layer=%b ppacc=%b lane=%b writes=%b ppfault=%b loadfault=%b event=%b/%b expected=%b/%b next=%b/%b",
			         probe_counter_state, probe_counter_output, probe_counter_position,
			         probe_counter_start, probe_counter_mac_accept, probe_counter_mac_fault,
			         probe_counter_layer_pw, probe_counter_pp_accept, probe_counter_dw_lane,
			         probe_counter_dw_writes, probe_counter_pp_fault, probe_counter_load_fault,
			         down2_overlap_tile_runner_Inst_tb.flag_cnt_output_clear,
			         down2_overlap_tile_runner_Inst_tb.flag_cnt_output_increment,
			         expected_clear, expected_increment, candidate_next, expected_next);
			error_count = error_count + 1;
		end
	end
	endtask

	task counter_transition_probe;
	integer state_code;
	integer output_code;
	integer position_code;
	integer control_a;
	integer control_b;
	integer control_c;
	integer known_count;
	integer boundary_count;
	begin
		known_count = 0;
		boundary_count = 0;
		force down2_overlap_tile_runner_Inst_tb.state_current = probe_counter_state;
		force down2_overlap_tile_runner_Inst_tb.cnt_output = probe_counter_output;
		force down2_overlap_tile_runner_Inst_tb.cnt_position = probe_counter_position;
		force down2_overlap_tile_runner_Inst_tb.flag_start_accept = probe_counter_start;
		force down2_overlap_tile_runner_Inst_tb.flag_mac_result_accept = probe_counter_mac_accept;
		force down2_overlap_tile_runner_Inst_tb.mac_fault = probe_counter_mac_fault;
		force down2_overlap_tile_runner_Inst_tb.flag_layer_pw = probe_counter_layer_pw;
		force down2_overlap_tile_runner_Inst_tb.flag_pp_input_accept = probe_counter_pp_accept;
		force down2_overlap_tile_runner_Inst_tb.cnt_dw_post_lane = probe_counter_dw_lane;
		force down2_overlap_tile_runner_Inst_tb.cnt_dw_writes = probe_counter_dw_writes;
		force down2_overlap_tile_runner_Inst_tb.pp_fault = probe_counter_pp_fault;
		force down2_overlap_tile_runner_Inst_tb.flag_load_fault = probe_counter_load_fault;
		probe_counter_pp_fault = 1'b0;
		probe_counter_load_fault = 1'b0;
		for(state_code = 0; state_code < 16; state_code = state_code + 1)begin
			for(output_code = 0; output_code < 32; output_code = output_code + 1)begin
				for(position_code = 0; position_code < 16; position_code = position_code + 1)begin
					probe_counter_state = state_code[3:0];
					probe_counter_output = output_code[4:0];
					probe_counter_position = position_code[3:0];
					probe_counter_start = 1'b0;
					probe_counter_mac_accept = 1'b0;
					probe_counter_mac_fault = 1'b0;
					probe_counter_layer_pw = 1'b0;
					probe_counter_pp_accept = 1'b0;
					probe_counter_dw_lane = 2'd0;
					probe_counter_dw_writes = 9'd0;
					case(state_code)
						0:begin
							for(control_a = 0; control_a < 2; control_a = control_a + 1)begin
								probe_counter_start = control_a[0];
								check_counter_transition_now;
								known_count = known_count + 1;
							end
						end
						3:begin
							for(control_a = 0; control_a < 2; control_a = control_a + 1)begin
								for(control_b = 0; control_b < 2; control_b = control_b + 1)begin
									for(control_c = 0; control_c < 2; control_c = control_c + 1)begin
										probe_counter_mac_accept = control_a[0];
										probe_counter_mac_fault = control_b[0];
										probe_counter_layer_pw = control_c[0];
										check_counter_transition_now;
										known_count = known_count + 1;
									end
								end
							end
						end
						9:begin
							for(control_a = 0; control_a < 2; control_a = control_a + 1)begin
								for(control_b = 0; control_b < 4; control_b = control_b + 1)begin
									probe_counter_pp_accept = control_a[0];
									probe_counter_dw_lane = control_b[1:0];
									check_counter_transition_now;
									known_count = known_count + 1;
								end
							end
						end
						4:begin
							for(control_a = 0; control_a < 3; control_a = control_a + 1)begin
								probe_counter_dw_writes = (control_a == 0) ? 9'd255 :
								                          (control_a == 1) ? 9'd256 : 9'd257;
								check_counter_transition_now;
								known_count = known_count + 1;
							end
						end
						default:begin
							check_counter_transition_now;
							known_count = known_count + 1;
						end
					endcase
				end
			end
		end
		probe_counter_state = 4'd3;
		probe_counter_output = 5'd2;
		probe_counter_position = 4'd4;
		probe_counter_start = 1'b0;
		probe_counter_mac_accept = 1'b1;
		probe_counter_mac_fault = 1'b0;
		probe_counter_layer_pw = 1'b1;
		probe_counter_pp_accept = 1'b0;
		probe_counter_dw_lane = 2'd0;
		probe_counter_dw_writes = 9'd0;
		probe_counter_pp_fault = 1'bx; check_counter_transition_now; boundary_count = boundary_count + 1;
		probe_counter_pp_fault = 1'bz; check_counter_transition_now; boundary_count = boundary_count + 1;
		probe_counter_pp_fault = 1'b0;
		probe_counter_load_fault = 1'bx; check_counter_transition_now; boundary_count = boundary_count + 1;
		probe_counter_load_fault = 1'bz; check_counter_transition_now; boundary_count = boundary_count + 1;
		probe_counter_load_fault = 1'b0;
		probe_counter_layer_pw = 1'bx; check_counter_transition_now; boundary_count = boundary_count + 1;
		probe_counter_layer_pw = 1'bz; check_counter_transition_now; boundary_count = boundary_count + 1;
		probe_counter_layer_pw = 1'b1;
		probe_counter_mac_accept = 1'bx; check_counter_transition_now; boundary_count = boundary_count + 1;
		probe_counter_mac_accept = 1'bz; check_counter_transition_now; boundary_count = boundary_count + 1;
		probe_counter_mac_accept = 1'b1;
		probe_counter_mac_fault = 1'bx; check_counter_transition_now; boundary_count = boundary_count + 1;
		probe_counter_mac_fault = 1'bz; check_counter_transition_now; boundary_count = boundary_count + 1;
		probe_counter_mac_fault = 1'b0;
		probe_counter_output = 5'bx0010; check_counter_transition_now; boundary_count = boundary_count + 1;
		probe_counter_output = 5'bz0010; check_counter_transition_now; boundary_count = boundary_count + 1;
		probe_counter_output = 5'd2;
		probe_counter_state = 4'bx011; check_counter_transition_now; boundary_count = boundary_count + 1;
		probe_counter_state = 4'bz011; check_counter_transition_now; boundary_count = boundary_count + 1;
		probe_counter_state = 4'd9;
		probe_counter_pp_accept = 1'bx; check_counter_transition_now; boundary_count = boundary_count + 1;
		probe_counter_pp_accept = 1'bz; check_counter_transition_now; boundary_count = boundary_count + 1;
		probe_counter_pp_accept = 1'b1;
		probe_counter_position = 4'bx000; check_counter_transition_now; boundary_count = boundary_count + 1;
		probe_counter_position = 4'bz000; check_counter_transition_now; boundary_count = boundary_count + 1;
		// DRAIN clear is generated in the same cycle, while a known fault holds
		// the counter and an X/Z guard follows the original procedural if rule.
		probe_counter_state = 4'd4;
		probe_counter_output = 5'd11;
		probe_counter_position = 4'd0;
		probe_counter_pp_accept = 1'b0;
		probe_counter_dw_writes = 9'd256;
		probe_counter_pp_fault = 1'b1; check_counter_transition_now; boundary_count = boundary_count + 1;
		probe_counter_pp_fault = 1'bx; check_counter_transition_now; boundary_count = boundary_count + 1;
		probe_counter_pp_fault = 1'bz; check_counter_transition_now; boundary_count = boundary_count + 1;
		probe_counter_pp_fault = 1'b0;
		probe_counter_load_fault = 1'b1; check_counter_transition_now; boundary_count = boundary_count + 1;
		probe_counter_load_fault = 1'bx; check_counter_transition_now; boundary_count = boundary_count + 1;
		probe_counter_load_fault = 1'bz; check_counter_transition_now; boundary_count = boundary_count + 1;
		release down2_overlap_tile_runner_Inst_tb.state_current;
		release down2_overlap_tile_runner_Inst_tb.cnt_output;
		release down2_overlap_tile_runner_Inst_tb.cnt_position;
		release down2_overlap_tile_runner_Inst_tb.flag_start_accept;
		release down2_overlap_tile_runner_Inst_tb.flag_mac_result_accept;
		release down2_overlap_tile_runner_Inst_tb.mac_fault;
		release down2_overlap_tile_runner_Inst_tb.flag_layer_pw;
		release down2_overlap_tile_runner_Inst_tb.flag_pp_input_accept;
		release down2_overlap_tile_runner_Inst_tb.cnt_dw_post_lane;
		release down2_overlap_tile_runner_Inst_tb.cnt_dw_writes;
		release down2_overlap_tile_runner_Inst_tb.pp_fault;
		release down2_overlap_tile_runner_Inst_tb.flag_load_fault;
		$display("COUNTER_TRANSITION_PASS known_cases=%0d xz_boundaries=%0d width=5", known_count, boundary_count);
	end
	endtask

	// Check the isolated halo RAM write enable against valid, invalid, X-address and reset cases.
	task halo_control_timing_probe;
	reg signed [7:0]saved_halo_zero;
	reg signed [7:0]saved_halo_two;
	begin
		reset_dut;
		@(negedge i_clk);
		i_load_valid = 1'b1;
		i_load_kind = 3'd0;
		i_load_addr = 11'd0;
		i_load_data = 32'sh00000012;
		@(negedge i_clk);
		i_load_valid = 1'b0;
		saved_halo_zero = down2_overlap_tile_runner_Inst_tb.reg_halo[0];
		if(saved_halo_zero !== 8'sh12)begin
			$display("TB_ERROR_HALO_WRITE valid load did not write halo[0]");
			error_count = error_count + 1;
		end
		saved_halo_two = down2_overlap_tile_runner_Inst_tb.reg_halo[2];

		@(negedge i_clk);
		i_load_valid = 1'b1;
		i_load_kind = 3'd0;
		i_load_addr = 11'd2;
		i_load_data = 32'sh00000055;
		@(negedge i_clk);
		i_load_valid = 1'b0;
		repeat(2) @(negedge i_clk);
		if(!o_fault || (down2_overlap_tile_runner_Inst_tb.reg_halo[2] !== saved_halo_two))begin
			$display("TB_ERROR_HALO_WRITE invalid sequence wrote halo or missed fault");
			error_count = error_count + 1;
		end

		reset_dut;
		@(negedge i_clk);
		i_load_valid = 1'b1;
		i_load_kind = 3'd0;
		i_load_addr = {11{1'bx}};
		i_load_data = 32'sh00000066;
		@(negedge i_clk);
		i_load_valid = 1'b0;
		i_load_addr = 11'd0;
		repeat(2) @(negedge i_clk);
		if(!o_fault || (down2_overlap_tile_runner_Inst_tb.reg_halo[0] !== saved_halo_zero))begin
			$display("TB_ERROR_HALO_WRITE X address wrote halo or missed fault");
			error_count = error_count + 1;
		end

		reset_dut;
		@(negedge i_clk);
		i_load_valid = 1'b1;
		i_load_kind = 3'd0;
		i_load_addr = 11'd0;
		i_load_data = 32'sh00000077;
		i_rstn = 1'b0;
		repeat(2) @(negedge i_clk);
		if(down2_overlap_tile_runner_Inst_tb.reg_halo[0] !== saved_halo_zero)begin
			$display("TB_ERROR_HALO_WRITE reset allowed halo write");
			error_count = error_count + 1;
		end
		i_load_valid = 1'b0;
		i_rstn = 1'b1;
		repeat(3) @(negedge i_clk);
		$display("HALO_CONTROL_TIMING_PASS valid=1 invalid_sequence=1 x_addr=1 reset_no_write=1");
	end
	endtask

	// Directed four-state comparison against the previous cross-module ready expression.
	task ack_local_xprop_case;
	input [3:0]forced_state;
	input forced_reserved;
	input forced_layer;
	input forced_table_valid;
	input [1:0]forced_queue;
	input forced_loaded;
	input forced_table_fault;
	input forced_fatal;
	begin
		force down2_overlap_tile_runner_Inst_tb.state_current = forced_state;
		force down2_overlap_tile_runner_Inst_tb.flag_result_reserved = forced_reserved;
		force down2_overlap_tile_runner_Inst_tb.flag_layer_pw = forced_layer;
		force down2_overlap_tile_runner_Inst_tb.i_table_valid = forced_table_valid;
		force down2_overlap_tile_runner_Inst_tb.road_postprocess_stream_Inst_tile.cnt_result_queue = forced_queue;
		force down2_overlap_tile_runner_Inst_tb.road_postprocess_stream_Inst_tile.silu_table_loaded = forced_loaded;
		force down2_overlap_tile_runner_Inst_tb.road_postprocess_stream_Inst_tile.silu_table_fault = forced_table_fault;
		force down2_overlap_tile_runner_Inst_tb.road_postprocess_stream_Inst_tile.flag_fatal = forced_fatal;
		#1;
		if(down2_overlap_tile_runner_Inst_tb.flag_mac_result_ready_local !==
		   ((down2_overlap_tile_runner_Inst_tb.state_current == 4'd3) &&
		    down2_overlap_tile_runner_Inst_tb.flag_result_reserved &&
		    (forced_layer ? down2_overlap_tile_runner_Inst_tb.pp_input_ready :
		                    (~down2_overlap_tile_runner_Inst_tb.pp_fault))))begin
			$display("TB_ERROR_ACK_LOCAL_XPROP state=%b reserved=%b layer=%b table=%b queue=%b loaded=%b table_fault=%b fatal=%b expected=%b new=%b",
			         forced_state, forced_reserved, forced_layer, forced_table_valid, forced_queue,
			         forced_loaded, forced_table_fault, forced_fatal,
			         ((down2_overlap_tile_runner_Inst_tb.state_current == 4'd3) &&
			          down2_overlap_tile_runner_Inst_tb.flag_result_reserved &&
			          (forced_layer ? down2_overlap_tile_runner_Inst_tb.pp_input_ready :
			                          (~down2_overlap_tile_runner_Inst_tb.pp_fault))),
			         down2_overlap_tile_runner_Inst_tb.flag_mac_result_ready_local);
			error_count = error_count + 1;
		end
		release down2_overlap_tile_runner_Inst_tb.state_current;
		release down2_overlap_tile_runner_Inst_tb.flag_result_reserved;
		release down2_overlap_tile_runner_Inst_tb.flag_layer_pw;
		release down2_overlap_tile_runner_Inst_tb.i_table_valid;
		release down2_overlap_tile_runner_Inst_tb.road_postprocess_stream_Inst_tile.cnt_result_queue;
		release down2_overlap_tile_runner_Inst_tb.road_postprocess_stream_Inst_tile.silu_table_loaded;
		release down2_overlap_tile_runner_Inst_tb.road_postprocess_stream_Inst_tile.silu_table_fault;
		release down2_overlap_tile_runner_Inst_tb.road_postprocess_stream_Inst_tile.flag_fatal;
		#1;
	end
	endtask

	initial begin
		can_reserve_four_state_probe;
		counter_transition_probe;
		ack_local_xprop_case(4'd3, 1'b1, 1'b1, 1'b1, 2'd0, 1'b1, 1'b0, 1'b0);
		ack_local_xprop_case(4'bx011, 1'b1, 1'b1, 1'b1, 2'd0, 1'b1, 1'b0, 1'b0);
		ack_local_xprop_case(4'd3, 1'bx, 1'b1, 1'b1, 2'd0, 1'b1, 1'b0, 1'b0);
		ack_local_xprop_case(4'd3, 1'b1, 1'b1, 1'b1, 2'bx0, 1'b1, 1'b0, 1'b0);
		ack_local_xprop_case(4'd3, 1'b1, 1'b1, 1'b1, 2'd0, 1'bx, 1'b0, 1'b0);
		ack_local_xprop_case(4'd3, 1'b1, 1'b1, 1'b1, 2'd0, 1'b1, 1'bx, 1'b0);
		ack_local_xprop_case(4'd3, 1'b1, 1'b1, 1'b1, 2'd0, 1'b1, 1'b0, 1'bx);
		ack_local_xprop_case(4'd3, 1'b1, 1'b0, 1'b1, 2'd0, 1'b1, 1'b0, 1'b0);
		ack_local_xprop_case(4'd3, 1'b1, 1'b0, 1'b1, 2'bx0, 1'b1, 1'b0, 1'b0);
		ack_local_xprop_case(4'd3, 1'b1, 1'b0, 1'b1, 2'd0, 1'bx, 1'b0, 1'b0);
		$display("ACK_LOCAL_XPROP_PASS pw_cases=7 dw_capture_cases=3");
		cache_control_fault_probe;
		halo_control_timing_probe;
		$readmemh("vectors/silu.hex", mem_silu);
		$readmemh("vectors/dw_weights.hex", mem_dw_weight);
		$readmemh("vectors/dw_biases.hex", mem_dw_bias);
		$readmemh("vectors/pw_weights.hex", mem_pw_weight);
		$readmemh("vectors/pw_biases.hex", mem_pw_bias);
		reset_inflight_probe;
		reset_dw_post_probe;
		$readmemh("vectors/pw_weights.hex", mem_pw_weight);
		$readmemh("vectors/pw_biases.hex", mem_pw_bias);
		run_full_case(0);
		run_full_case(1);
		run_full_case(2);

		case_index = 3;
		$readmemh("vectors/pw_standalone_pw_input.hex", mem_pw_input);
		$readmemh("vectors/pw_standalone_stages.hex", mem_expected_stage, 0, 1535);
		$readmemh("vectors/pw_standalone_output.hex", mem_expected_output);
		reset_dut;
		load_table;
		preload_case(1'b1);
		start_and_wait(1'b1);
		export_and_check;
		fault_atomic_probe;
		dw_triplet_numeric_probe(1, 1, 1'b1);
		dw_triplet_numeric_probe(1, -1, 1'b1);
		dw_triplet_numeric_probe(2, 1, 1'b1);
		dw_triplet_numeric_probe(2, -1, 1'b1);
		dw_triplet_numeric_probe(1, 1, 1'b0);
		dw_triplet_numeric_probe(2, -1, 1'b0);

		reset_dut;
		load_table;
		load_kind(3'd4, 384);
		load_kind(3'd5, 24);
		@(negedge i_clk);
		i_pw_only = 1'b1;
		i_start = 1'b1;
		@(negedge i_clk);
		i_start = 1'b0;
		repeat(5) @(negedge i_clk);
		if(o_busy || o_done || o_fault)begin
			$display("TB_ERROR_PARTIAL_PRELOAD incomplete preload started or faulted");
			error_count = error_count + 1;
		end

		if(ack_local_high_accepts == 0)begin
			$display("TB_ERROR_ACK_LOCAL no result accepted with parent table-valid high");
			error_count = error_count + 1;
		end else begin
			$display("ACK_LOCAL_TABLE_HIGH_PASS accepts=%0d", ack_local_high_accepts);
		end
		$display("CACHE_PORT_COMPARE_PASS writes=%0d loads=%0d commits=%0d",
		         cache_write_compare_count, cache_load_write_count, cache_commit_write_count);

		if(error_count == 0)begin
			$display("TB_PASS_DOWN2_TILE cases=4");
		end else begin
			$display("TB_FAIL_DOWN2_TILE errors=%0d", error_count);
		end
		$finish;
	end

	initial begin
		#19000000;
		$display("TB_FAIL_DOWN2_TILE timeout");
		$finish;
	end

	down2_overlap_tile_runner down2_overlap_tile_runner_Inst_tb(
		.i_clk(i_clk), .i_rstn(i_rstn),
		.i_table_valid(i_table_valid), .i_table_addr(i_table_addr),
		.i_table_data(i_table_data), .o_table_ready(o_table_ready),
		.o_table_loaded(o_table_loaded), .o_table_fault(o_table_fault),
		.i_load_valid(i_load_valid), .i_load_kind(i_load_kind),
		.i_load_addr(i_load_addr), .i_load_data(i_load_data), .o_load_ready(o_load_ready),
		.i_start(i_start), .i_pw_only(i_pw_only), .i_commit_ready(i_commit_ready), .o_busy(o_busy),
		.o_done(o_done), .o_fault(o_fault), .i_export_start(i_export_start),
		.i_output_ready(i_output_ready), .o_output_valid(o_output_valid),
		.o_output_data(o_output_data), .o_output_index(o_output_index),
		.o_export_done(o_export_done), .o_debug_valid(o_debug_valid),
		.o_debug_phase(o_debug_phase), .o_debug_layer(o_debug_layer),
		.o_debug_position(o_debug_position), .o_debug_channel(o_debug_channel),
		.o_debug_value(o_debug_value), .o_preload_writes(o_preload_writes),
		.o_core_cycles(o_core_cycles), .o_mac_cycles(o_mac_cycles),
		.o_pre_cycles(o_pre_cycles), .o_silu_cycles(o_silu_cycles),
		.o_post_cycles(o_post_cycles), .o_writeback_cycles(o_writeback_cycles),
		.o_storage_wait_cycles(o_storage_wait_cycles),
		.o_scheduler_idle_cycles(o_scheduler_idle_cycles),
		.o_export_cycles(o_export_cycles), .o_result_queue_count(o_result_queue_count),
		.o_result_reserved(o_result_reserved), .o_meta_count(o_meta_count),
		.o_mac_result_count(o_mac_result_count), .o_pre_accept_count(o_pre_accept_count),
		.o_silu_accept_count(o_silu_accept_count), .o_post_accept_count(o_post_accept_count),
		.o_writeback_count(o_writeback_count)
	);

endmodule
