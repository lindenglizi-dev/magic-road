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
					if((turn_last_accept - turn_first_accept != 2) ||
					   (turn_result_ack - turn_last_accept != 10) ||
					   (cycle_count - turn_result_ack != 2))begin
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
				trace_input_accepts = 0;
			end
			if(trace_job_active)begin
				case(down2_overlap_tile_runner_Inst_tb.state_current)
					4'd1: trace_storage_cycles = trace_storage_cycles + 1;
					4'd2: trace_send_cycles = trace_send_cycles + 1;
					4'd3: trace_wait_cycles = trace_wait_cycles + 1;
					default: begin end
				endcase
				if(down2_overlap_tile_runner_Inst_tb.flag_mac_input_accept)
					trace_input_accepts = trace_input_accepts + 1;
				if(down2_overlap_tile_runner_Inst_tb.flag_mac_result_accept)begin
					$display("JOB_TRACE job=%0d storage=%0d send=%0d wait=%0d accepts=%0d total=%0d",
					         trace_job_count, trace_storage_cycles, trace_send_cycles,
					         trace_wait_cycles, trace_input_accepts,
					         trace_storage_cycles + trace_send_cycles + trace_wait_cycles);
					if((trace_storage_cycles != 2) || (trace_send_cycles != 2) ||
					   (trace_wait_cycles != 10) || (trace_input_accepts != 2))begin
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
			if(!check_pw_only && !seen_pw && down2_overlap_tile_runner_Inst_tb.flag_layer_pw)begin
				seen_pw = 1'b1;
				dw_endpoint = cycle_count - start_cycle;
			end
			if(down2_overlap_tile_runner_Inst_tb.flag_mac_result_accept)begin
				for(expected_phase = 0; expected_phase < 3; expected_phase = expected_phase + 1)begin
					if(down2_overlap_tile_runner_Inst_tb.wire_result_lane_mask[expected_phase])begin
						check_stage(2'd0, down2_overlap_tile_runner_Inst_tb.flag_layer_pw,
						            down2_overlap_tile_runner_Inst_tb.cnt_position,
						            down2_overlap_tile_runner_Inst_tb.wire_result_channel_base + expected_phase,
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
		if((done_cycle - start_cycle) !== o_core_cycles)begin
			$display("TB_ERROR_ENDPOINT diff=%0d core=%0d", done_cycle - start_cycle, o_core_cycles);
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

	// Directed four-state comparison against the previous cross-module ready expression.
	task ack_local_xprop_case;
	input [3:0]forced_state;
	input forced_reserved;
	input forced_table_valid;
	input [1:0]forced_queue;
	input forced_loaded;
	input forced_table_fault;
	input forced_fatal;
	begin
		force down2_overlap_tile_runner_Inst_tb.state_current = forced_state;
		force down2_overlap_tile_runner_Inst_tb.flag_result_reserved = forced_reserved;
		force down2_overlap_tile_runner_Inst_tb.i_table_valid = forced_table_valid;
		force down2_overlap_tile_runner_Inst_tb.road_postprocess_stream_Inst_tile.cnt_result_queue = forced_queue;
		force down2_overlap_tile_runner_Inst_tb.road_postprocess_stream_Inst_tile.silu_table_loaded = forced_loaded;
		force down2_overlap_tile_runner_Inst_tb.road_postprocess_stream_Inst_tile.silu_table_fault = forced_table_fault;
		force down2_overlap_tile_runner_Inst_tb.road_postprocess_stream_Inst_tile.flag_fatal = forced_fatal;
		#1;
		if(down2_overlap_tile_runner_Inst_tb.flag_mac_result_ready_local !==
		   ((down2_overlap_tile_runner_Inst_tb.state_current == 4'd3) &&
		    down2_overlap_tile_runner_Inst_tb.flag_result_reserved &&
		    down2_overlap_tile_runner_Inst_tb.pp_input_ready))begin
			$display("TB_ERROR_ACK_LOCAL_XPROP state=%b reserved=%b table=%b queue=%b loaded=%b table_fault=%b fatal=%b old=%b new=%b",
			         forced_state, forced_reserved, forced_table_valid, forced_queue,
			         forced_loaded, forced_table_fault, forced_fatal,
			         ((down2_overlap_tile_runner_Inst_tb.state_current == 4'd3) &&
			          down2_overlap_tile_runner_Inst_tb.flag_result_reserved &&
			          down2_overlap_tile_runner_Inst_tb.pp_input_ready),
			         down2_overlap_tile_runner_Inst_tb.flag_mac_result_ready_local);
			error_count = error_count + 1;
		end
		release down2_overlap_tile_runner_Inst_tb.state_current;
		release down2_overlap_tile_runner_Inst_tb.flag_result_reserved;
		release down2_overlap_tile_runner_Inst_tb.i_table_valid;
		release down2_overlap_tile_runner_Inst_tb.road_postprocess_stream_Inst_tile.cnt_result_queue;
		release down2_overlap_tile_runner_Inst_tb.road_postprocess_stream_Inst_tile.silu_table_loaded;
		release down2_overlap_tile_runner_Inst_tb.road_postprocess_stream_Inst_tile.silu_table_fault;
		release down2_overlap_tile_runner_Inst_tb.road_postprocess_stream_Inst_tile.flag_fatal;
		#1;
	end
	endtask

	initial begin
		ack_local_xprop_case(4'd3, 1'b1, 1'b1, 2'd0, 1'b1, 1'b0, 1'b0);
		ack_local_xprop_case(4'bx011, 1'b1, 1'b1, 2'd0, 1'b1, 1'b0, 1'b0);
		ack_local_xprop_case(4'd3, 1'bx, 1'b1, 2'd0, 1'b1, 1'b0, 1'b0);
		ack_local_xprop_case(4'd3, 1'b1, 1'b1, 2'bx0, 1'b1, 1'b0, 1'b0);
		ack_local_xprop_case(4'd3, 1'b1, 1'b1, 2'd0, 1'bx, 1'b0, 1'b0);
		ack_local_xprop_case(4'd3, 1'b1, 1'b1, 2'd0, 1'b1, 1'bx, 1'b0);
		ack_local_xprop_case(4'd3, 1'b1, 1'b1, 2'd0, 1'b1, 1'b0, 1'bx);
		$display("ACK_LOCAL_XPROP_PASS cases=7");
		cache_control_fault_probe;
		$readmemh("vectors/silu.hex", mem_silu);
		$readmemh("vectors/dw_weights.hex", mem_dw_weight);
		$readmemh("vectors/dw_biases.hex", mem_dw_bias);
		$readmemh("vectors/pw_weights.hex", mem_pw_weight);
		$readmemh("vectors/pw_biases.hex", mem_pw_bias);
		reset_inflight_probe;
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
