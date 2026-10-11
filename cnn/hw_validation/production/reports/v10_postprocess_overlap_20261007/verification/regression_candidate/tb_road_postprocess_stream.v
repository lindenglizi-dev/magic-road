`timescale 1ns / 1ps

module tb_road_postprocess_stream;
	reg i_clk = 1'b0;
	reg i_rstn = 1'b0;
	reg i_table_valid = 1'b0;
	reg [9:0]i_table_addr = 10'd0;
	reg signed [15:0]i_table_data = 16'sd0;
	reg i_input_valid = 1'b0;
	reg [95:0]i_result_data = 96'd0;
	reg i_result_fault = 1'b0;
	reg i_layer = 1'b0;
	reg [3:0]i_position = 4'd0;
	reg [4:0]i_channel_base = 5'd0;
	reg [2:0]i_lane_mask = 3'd0;
	reg i_output_ready = 1'b0;

	wire o_table_ready;
	wire o_table_loaded;
	wire o_table_fault;
	wire o_input_ready;
	wire o_output_valid;
	wire signed [7:0]o_output_data;
	wire [15:0]o_output_tag;
	wire o_fault;
	wire [1:0]o_result_queue_count;
	wire [3:0]o_meta_count;
	wire o_pre_busy;
	wire o_silu_busy;
	wire o_post_busy;
	wire o_pre_accept;
	wire o_silu_accept;
	wire o_post_accept;

	reg signed [15:0]mem_silu [0:1023];
	reg expected_valid [0:1023];
	reg seen_pre [0:1023];
	reg seen_silu [0:1023];
	reg seen_post [0:1023];
	reg seen_output [0:1023];
	reg signed [15:0]expected_pre [0:1023];
	reg signed [15:0]expected_silu [0:1023];
	reg signed [15:0]expected_post [0:1023];
	reg signed [7:0]expected_output [0:1023];

	integer cycle_count = 0;
	integer error_count = 0;
	integer input_groups = 0;
	integer expected_scalars = 0;
	integer output_scalars = 0;
	integer blocked_cycles = 0;
	integer max_queue = 0;
	integer max_meta = 0;
	integer max_pre = 0;
	integer max_post = 0;
	integer max_obligations = 0;
	integer first_pre_cycle = -1;
	integer first_valid_cycle = -1;
	integer first_write_cycle = -1;
	integer continuous_group;
	integer pressure_group;
	integer reset_age;
	integer reset_age_executed = 0;
	integer reset_age_errors_before;
	integer pressure_mode = 0;
	integer pressure_withdraw_cycle = -1;
	integer pressure_release_cycle = -1;
	integer pressure_last_accept_cycle = -1;
	integer pressure_accept_groups = 0;
	integer pressure_accept_scalars = 0;
	integer pressure_deny_streak = 0;
	integer pressure_final_deny_streak = 0;
	integer random_group;
	integer random_index;
	integer random_gap;
	integer random_gap_cycles = 0;
	integer random_ready_stalls = 0;
	integer lane;
	integer key;
	integer tag;
	integer value32;
	reg held_valid = 1'b0;
	reg signed [7:0]held_data = 8'sd0;
	reg [15:0]held_tag = 16'd0;
	reg [15:0]gap_lfsr = 16'h1d0f;
	reg [15:0]ready_lfsr = 16'hace1;
	reg input_held = 1'b0;
	reg [95:0]held_result_data = 96'd0;
	reg held_result_fault = 1'b0;
	reg held_layer = 1'b0;
	reg [3:0]held_position = 4'd0;
	reg [4:0]held_channel_base = 5'd0;
	reg [2:0]held_lane_mask = 3'd0;

	always #5 i_clk = ~i_clk;

	function signed [15:0]round16;
		input signed [63:0]value;
		input [5:0]shift;
		reg [63:0]magnitude;
		reg [63:0]quotient;
		reg [63:0]remainder;
		reg [63:0]half;
		reg signed [63:0]rounded;
		begin
			magnitude = value[63] ? -value : value;
			quotient = magnitude >> shift;
			remainder = magnitude & ~(64'hffffffffffffffff << shift);
			half = shift == 0 ? 0 : (64'd1 << (shift - 1));
			if(shift != 0 && ((remainder > half) ||
			   ((remainder == half) && quotient[0]))) quotient = quotient + 1'b1;
			rounded = value[63] ? -$signed(quotient) : $signed(quotient);
			if(rounded < -64'sd32768) round16 = -16'sd32768;
			else if(rounded > 64'sd32767) round16 = 16'sd32767;
			else round16 = rounded[15:0];
		end
	endfunction

	function signed [15:0]silu16;
		input signed [15:0]value;
		integer address;
		begin
			if(value <= -16'sd2048) silu16 = 16'sd0;
			else if(value >= 16'sd2048) silu16 = value;
			else begin
				address = $signed(round16({{48{value[15]}}, value}, 6'd2)) + 512;
				if(address == 1024) silu16 = 16'sd2047;
				else silu16 = mem_silu[address];
			end
		end
	endfunction

	function signed [7:0]sat8;
		input signed [15:0]value;
		begin
			if(value > 16'sd127) sat8 = 8'sd127;
			else if(value < -16'sd128) sat8 = -8'sd128;
			else sat8 = value[7:0];
		end
	endfunction

	function integer popcount3;
		input [2:0]value;
		begin popcount3 = value[0] + value[1] + value[2]; end
	endfunction

	task clear_scoreboard;
		integer scan_index;
		begin
			for(scan_index = 0; scan_index < 1024; scan_index = scan_index + 1)begin
				expected_valid[scan_index] = 1'b0;
				seen_pre[scan_index] = 1'b0;
				seen_silu[scan_index] = 1'b0;
				seen_post[scan_index] = 1'b0;
				seen_output[scan_index] = 1'b0;
			end
			input_groups = 0;
			expected_scalars = 0;
			output_scalars = 0;
			blocked_cycles = 0;
			max_queue = 0;
			max_meta = 0;
			max_pre = 0;
			max_post = 0;
			max_obligations = 0;
			first_pre_cycle = -1;
			first_valid_cycle = -1;
			first_write_cycle = -1;
		end
	endtask

	task reset_dut;
		begin
			@(negedge i_clk);
			i_rstn = 1'b0;
			i_table_valid = 1'b0;
			i_input_valid = 1'b0;
			i_result_fault = 1'b0;
			i_output_ready = 1'b0;
			repeat(3) @(negedge i_clk);
			i_rstn = 1'b1;
			repeat(2) @(negedge i_clk);
			clear_scoreboard;
			if(o_table_loaded || o_output_valid || o_fault || o_result_queue_count != 0 ||
			   o_meta_count != 0 || o_pre_busy || o_silu_busy || o_post_busy)begin
				$display("TB_ERROR_RESET state not cancelled");
				error_count = error_count + 1;
			end
		end
	endtask

	task load_table_range;
		input integer first;
		input integer last;
		integer load_index;
		begin
			for(load_index = first; load_index <= last; load_index = load_index + 1)begin
				@(negedge i_clk);
				i_table_valid = 1'b1;
				i_table_addr = load_index[9:0];
				i_table_data = mem_silu[load_index];
				while(!o_table_ready) @(negedge i_clk);
			end
			@(negedge i_clk);
			i_table_valid = 1'b0;
		end
	endtask

	task load_full_table;
		begin
			load_table_range(0, 1023);
			if(!o_table_loaded || o_table_fault)begin
				$display("TB_ERROR_TABLE full load failed");
				error_count = error_count + 1;
			end
		end
	endtask

	task set_group;
		input integer number;
		input integer position;
		input integer base;
		input [2:0]mask;
		begin
			i_layer = (mask == 3'b111);
			i_position = position[3:0];
			i_channel_base = base[4:0];
			i_lane_mask = mask;
			i_result_data[31:0] = $signed(number * 17 - 90);
			i_result_data[63:32] = $signed(number * 23 - 70);
			i_result_data[95:64] = $signed(100 - number * 19);
		end
	endtask

	task drive_one_group;
		input integer number;
		input integer position;
		input integer base;
		input [2:0]mask;
		input integer gap;
		begin
			@(negedge i_clk);
			set_group(number, position, base, mask);
			i_input_valid = 1'b1;
			while(!o_input_ready) @(negedge i_clk);
			@(negedge i_clk);
			i_input_valid = 1'b0;
			repeat(gap) @(negedge i_clk);
		end
	endtask

	task wait_outputs;
		input integer count;
		integer timeout;
		begin
			timeout = 0;
			while(output_scalars < count && timeout < 400)begin
				@(negedge i_clk);
				timeout = timeout + 1;
			end
			if(output_scalars != count)begin
				$display("TB_ERROR_OUTPUT_TIMEOUT got=%0d exp=%0d", output_scalars, count);
				error_count = error_count + 1;
			end
		end
	endtask

	always@(posedge i_clk)begin
		cycle_count = cycle_count + 1;
		if(i_rstn)begin
			if(input_held && ((i_result_data !== held_result_data) ||
			   (i_result_fault !== held_result_fault) || (i_layer !== held_layer) ||
			   (i_position !== held_position) ||
			   (i_channel_base !== held_channel_base) ||
			   (i_lane_mask !== held_lane_mask) || !i_input_valid))begin
				$display("TB_ERROR_INPUT_HOLD source changed before handshake");
				error_count = error_count + 1;
			end
			input_held = i_input_valid && !o_input_ready;
			held_result_data = i_result_data;
			held_result_fault = i_result_fault;
			held_layer = i_layer;
			held_position = i_position;
			held_channel_base = i_channel_base;
			held_lane_mask = i_lane_mask;
			if(o_result_queue_count > max_queue) max_queue = o_result_queue_count;
			if(o_meta_count > max_meta) max_meta = o_meta_count;
			if(dut.cnt_pre_inflight > max_pre) max_pre = dut.cnt_pre_inflight;
			if(dut.cnt_post_inflight > max_post) max_post = dut.cnt_post_inflight;
			if(o_result_queue_count > 2 || o_meta_count > 6 ||
			   dut.cnt_pre_inflight > 9 || dut.cnt_post_inflight > 9)begin
				$display("TB_ERROR_CAPACITY q=%0d pre=%0d meta=%0d post=%0d",
				         o_result_queue_count, dut.cnt_pre_inflight, o_meta_count,
				         dut.cnt_post_inflight);
				error_count = error_count + 1;
			end
			if(i_input_valid && o_input_ready)begin
				input_groups = input_groups + 1;
				if(pressure_mode != 0 && !i_output_ready)begin
					pressure_last_accept_cycle = cycle_count;
					pressure_accept_groups = pressure_accept_groups + 1;
					pressure_accept_scalars = pressure_accept_scalars + popcount3(i_lane_mask);
					pressure_deny_streak = 0;
				end
				for(lane = 0; lane < 3; lane = lane + 1)begin
					if(i_lane_mask[lane] && !i_result_fault)begin
						tag = (i_layer << 15) | (i_position << 11) |
						      ((i_channel_base + lane) << 6);
						key = tag >> 6;
						value32 = $signed(i_result_data[lane*32 +: 32]);
						expected_pre[key] = round16(value32 * (lane == 0 ? 1 : lane == 1 ? 3 : 5),
						                                lane == 0 ? 0 : lane == 1 ? 2 : 4);
						expected_silu[key] = silu16(expected_pre[key]);
						expected_post[key] = round16(expected_silu[key], 6'd4);
						expected_output[key] = sat8(expected_post[key]);
						expected_valid[key] = 1'b1;
						expected_scalars = expected_scalars + 1;
					end
				end
			end
			if(o_pre_accept && first_pre_cycle < 0) first_pre_cycle = cycle_count;
			if(o_silu_accept)begin
				key = dut.pre_result_tag[15:6];
				if(!expected_valid[key] || $signed(dut.pre_result_data) !== $signed(expected_pre[key]) ||
				   seen_pre[key])begin
					$display("TB_ERROR_PRE tag=%h got=%0d exp=%0d seen=%0d", dut.pre_result_tag,
					         $signed(dut.pre_result_data), $signed(expected_pre[key]), seen_pre[key]);
					error_count = error_count + 1;
				end
				seen_pre[key] = 1'b1;
			end
			if(o_post_accept)begin
				key = dut.reg_meta_fifo[dut.cnt_meta_read][15:6];
				if(!expected_valid[key] || $signed(dut.silu_output_data) !== $signed(expected_silu[key]) ||
				   seen_silu[key])begin
					$display("TB_ERROR_SILU key=%0d got=%0d exp=%0d seen=%0d", key,
					         $signed(dut.silu_output_data), $signed(expected_silu[key]), seen_silu[key]);
					error_count = error_count + 1;
				end
				seen_silu[key] = 1'b1;
			end
			if(o_output_valid && i_output_ready)begin
				key = o_output_tag[15:6];
				if(!expected_valid[key] || $signed(dut.post_result_data) !== $signed(expected_post[key]) ||
				   $signed(o_output_data) !== $signed(expected_output[key]) || seen_output[key])begin
					$display("TB_ERROR_OUTPUT tag=%h post=%0d/%0d out=%0d/%0d seen=%0d", o_output_tag,
					         $signed(dut.post_result_data), $signed(expected_post[key]),
					         $signed(o_output_data), $signed(expected_output[key]), seen_output[key]);
					error_count = error_count + 1;
				end
				seen_post[key] = 1'b1;
				seen_output[key] = 1'b1;
				output_scalars = output_scalars + 1;
				if(first_write_cycle < 0) first_write_cycle = cycle_count;
			end
			if(held_valid && ((o_output_data !== held_data) || (o_output_tag !== held_tag)))begin
				$display("TB_ERROR_HOLD output changed under backpressure");
				error_count = error_count + 1;
			end
			held_valid = o_output_valid && !i_output_ready;
			held_data = o_output_data;
			held_tag = o_output_tag;
			if(!i_output_ready && o_output_valid) blocked_cycles = blocked_cycles + 1;
			if((expected_scalars - output_scalars) > max_obligations)
				max_obligations = expected_scalars - output_scalars;
			if(pressure_mode != 0 && !i_output_ready && i_input_valid && !o_input_ready)
				pressure_deny_streak = pressure_deny_streak + 1;
		end else begin
			input_held = 1'b0;
			held_valid = 1'b0;
		end
	end

	always@(negedge i_clk)begin
		if(i_rstn && o_output_valid && first_valid_cycle < 0)
			first_valid_cycle = cycle_count;
	end

	initial begin
		$readmemh("vectors/silu.hex", mem_silu);
		reset_dut;
		load_table_range(0, 1022);
		if(o_table_loaded || o_input_ready)begin
			$display("TB_ERROR_PARTIAL_TABLE accepted inference");
			error_count = error_count + 1;
		end
		load_table_range(1023, 1023);
		i_output_ready = 1'b1;

		// Continuous triples exercise push while alpha/beta of the head serialize.
		for(continuous_group = 0; continuous_group < 5;
		    continuous_group = continuous_group + 1)begin
			@(negedge i_clk);
			set_group(continuous_group, continuous_group, 0, 3'b111);
			i_input_valid = 1'b1;
			while(!o_input_ready) @(negedge i_clk);
		end
		@(negedge i_clk); i_input_valid = 1'b0;
		wait_outputs(15);
		if(first_valid_cycle - first_pre_cycle != 23 || first_write_cycle - first_pre_cycle != 24)begin
			$display("TB_ERROR_LATENCY pre=%0d valid=%0d write=%0d", first_pre_cycle,
			         first_valid_cycle, first_write_cycle);
			error_count = error_count + 1;
		end

		// Input bubbles and lane-specific fixed coefficients, including DW lane switch.
		drive_one_group(6, 6, 0, 3'b001, 2);
		drive_one_group(7, 7, 0, 3'b010, 3);
		drive_one_group(8, 8, 0, 3'b100, 1);
		wait_outputs(18);

		// Long output backpressure from an empty pipeline; source remains valid.
		reset_dut;
		load_full_table;
		i_output_ready = 1'b0;
		pressure_mode = 1;
		pressure_withdraw_cycle = cycle_count;
		pressure_last_accept_cycle = -1;
		pressure_accept_groups = 0;
		pressure_accept_scalars = 0;
		pressure_deny_streak = 0;
		fork
			begin
				for(pressure_group = 0; pressure_group < 12;
				    pressure_group = pressure_group + 1)begin
					@(negedge i_clk);
					set_group(pressure_group + 20, pressure_group, 0, 3'b111);
					i_input_valid = 1'b1;
					while(!o_input_ready) @(negedge i_clk);
				end
				@(negedge i_clk); i_input_valid = 1'b0;
			end
			begin
				repeat(70) @(negedge i_clk);
				pressure_release_cycle = cycle_count;
				pressure_final_deny_streak = pressure_deny_streak;
				i_output_ready = 1'b1;
			end
		join
		wait_outputs(36);
		if(blocked_cycles < 20 || max_queue != 2 || max_meta > 6 ||
		   max_pre > 9 || max_post > 9 || max_obligations > 30 ||
		   pressure_accept_groups != 10 || pressure_accept_scalars != 30 ||
		   pressure_final_deny_streak < 10)begin
			$display("TB_ERROR_PRESSURE blocked=%0d q=%0d pre=%0d meta=%0d post=%0d",
			         blocked_cycles, max_queue, max_pre, max_meta, max_post);
			error_count = error_count + 1;
		end
		$display("TB_PRESSURE_EMPTY withdraw=%0d last_accept=%0d release=%0d response=%0d groups=%0d scalars=%0d deny_tail=%0d q=%0d pre=%0d meta=%0d post=%0d obligations=%0d",
		         pressure_withdraw_cycle, pressure_last_accept_cycle, pressure_release_cycle,
		         pressure_last_accept_cycle - pressure_withdraw_cycle + 1,
		         pressure_accept_groups, pressure_accept_scalars, pressure_final_deny_streak,
		         max_queue, max_pre, max_meta, max_post, max_obligations);
		pressure_mode = 0;

		// Fixed-seed random input bubbles and random output ready, mixed PW/DW lanes.
		reset_dut;
		load_full_table;
		gap_lfsr = 16'h1d0f;
		ready_lfsr = 16'hace1;
		random_gap_cycles = 0;
		random_ready_stalls = 0;
		fork
			begin
				for(random_group = 0; random_group < 48;
				    random_group = random_group + 1)begin
					gap_lfsr = {gap_lfsr[14:0],
					            gap_lfsr[15] ^ gap_lfsr[13] ^ gap_lfsr[12] ^ gap_lfsr[10]};
					random_gap = gap_lfsr[2:0];
					random_gap_cycles = random_gap_cycles + random_gap;
					random_index = random_group >> 1;
					if(!random_group[0])
						drive_one_group(random_group + 300, random_index / 8,
						                (random_index % 8) * 3, 3'b111, random_gap);
					else begin
						case(random_index % 3)
							0: drive_one_group(random_group + 300, random_index / 3,
							                   0, 3'b001, random_gap);
							1: drive_one_group(random_group + 300, random_index / 3,
							                   0, 3'b010, random_gap);
							default: drive_one_group(random_group + 300, random_index / 3,
							                         0, 3'b100, random_gap);
						endcase
					end
				end
			end
			begin
				while(output_scalars < 96)begin
					@(negedge i_clk);
					ready_lfsr = {ready_lfsr[14:0],
					              ready_lfsr[15] ^ ready_lfsr[13] ^
					              ready_lfsr[12] ^ ready_lfsr[10]};
					i_output_ready = ready_lfsr[0] | ready_lfsr[3];
					if(!i_output_ready) random_ready_stalls = random_ready_stalls + 1;
				end
				i_output_ready = 1'b1;
			end
		join
		wait_outputs(96);
		if((input_groups != 48) || (expected_scalars != 96) ||
		   (output_scalars != 96) || (random_gap_cycles < 48) ||
		   (random_ready_stalls < 10))begin
			$display("TB_ERROR_RANDOM groups=%0d expected=%0d outputs=%0d gaps=%0d stalls=%0d",
			         input_groups, expected_scalars, output_scalars,
			         random_gap_cycles, random_ready_stalls);
			error_count = error_count + 1;
		end
		$display("TB_RANDOM seed_gap=1d0f seed_ready=ace1 groups=%0d scalars=%0d gap_cycles=%0d ready_stalls=%0d",
		         input_groups, output_scalars, random_gap_cycles, random_ready_stalls);

		// Withdraw ready exactly when a tail scalar first becomes valid, then fill.
		reset_dut;
		load_full_table;
		i_output_ready = 1'b1;
		drive_one_group(44, 0, 0, 3'b111, 0);
		while(!o_output_valid) @(negedge i_clk);
		i_output_ready = 1'b0;
		pressure_mode = 2;
		pressure_withdraw_cycle = cycle_count;
		pressure_last_accept_cycle = -1;
		pressure_accept_groups = 0;
		pressure_accept_scalars = 0;
		pressure_deny_streak = 0;
		fork
			begin
				for(pressure_group = 0; pressure_group < 12;
				    pressure_group = pressure_group + 1)begin
					@(negedge i_clk);
					set_group(pressure_group + 100, pressure_group + 1, 0, 3'b111);
					i_input_valid = 1'b1;
					while(!o_input_ready) @(negedge i_clk);
				end
				@(negedge i_clk); i_input_valid = 1'b0;
			end
			begin
				repeat(70) @(negedge i_clk);
				pressure_release_cycle = cycle_count;
				pressure_final_deny_streak = pressure_deny_streak;
				i_output_ready = 1'b1;
			end
		join
		wait_outputs(39);
		if(max_queue != 2 || max_meta > 6 || max_pre > 9 || max_post > 9 ||
		   max_obligations > 30 || pressure_accept_groups != 7 ||
		   pressure_accept_scalars != 21 || pressure_final_deny_streak < 10)begin
			$display("TB_ERROR_PRESSURE_TAIL groups=%0d scalars=%0d deny=%0d q=%0d pre=%0d meta=%0d post=%0d obligations=%0d",
			         pressure_accept_groups, pressure_accept_scalars,
			         pressure_final_deny_streak, max_queue, max_pre, max_meta,
			         max_post, max_obligations);
			error_count = error_count + 1;
		end
		$display("TB_PRESSURE_TAIL withdraw=%0d last_accept=%0d release=%0d response=%0d groups=%0d scalars=%0d deny_tail=%0d q=%0d pre=%0d meta=%0d post=%0d obligations=%0d",
		         pressure_withdraw_cycle, pressure_last_accept_cycle, pressure_release_cycle,
		         pressure_last_accept_cycle - pressure_withdraw_cycle + 1,
		         pressure_accept_groups, pressure_accept_scalars, pressure_final_deny_streak,
		         max_queue, max_pre, max_meta, max_post, max_obligations);
		pressure_mode = 0;

		// Hold table address zero until all accepted old-table work drains.
		reset_dut;
		load_full_table;
		i_output_ready = 1'b1;
		drive_one_group(50, 2, 0, 3'b111, 0);
		@(negedge i_clk);
		i_table_valid = 1'b1;
		i_table_addr = 10'd0;
		i_table_data = mem_silu[0];
		while(!o_table_ready)begin
			@(negedge i_clk);
			if(!o_table_ready && dut.flag_table_forward)begin
				$display("TB_ERROR_RELOAD forwarded before global drain");
				error_count = error_count + 1;
			end
		end
		@(negedge i_clk); i_table_valid = 1'b0;
		if(output_scalars != 3 || o_table_loaded)begin
			$display("TB_ERROR_RELOAD outputs=%0d loaded=%0d", output_scalars, o_table_loaded);
			error_count = error_count + 1;
		end

		// Reset at every scalar pipeline age; no ghost may survive.
		for(reset_age = 1; reset_age <= 24; reset_age = reset_age + 1)begin
			reset_dut;
			load_full_table;
			i_output_ready = 1'b1;
			drive_one_group(reset_age + 60, reset_age % 16, 0, 3'b111, 0);
			repeat(reset_age) @(negedge i_clk);
			i_rstn = 1'b0;
			repeat(2) @(negedge i_clk);
			i_rstn = 1'b1;
			reset_age_errors_before = error_count;
			repeat(30)begin
				@(negedge i_clk);
				if(o_output_valid || o_fault || o_result_queue_count != 0 ||
				   o_meta_count != 0 || o_table_loaded || o_input_ready)begin
					$display("TB_ERROR_RESET_GHOST age=%0d loaded=%0d ready=%0d",
					         reset_age, o_table_loaded, o_input_ready);
					error_count = error_count + 1;
				end
			end
			clear_scoreboard;
			load_full_table;
			i_output_ready = 1'b1;
			drive_one_group(reset_age + 200, reset_age % 16, 0, 3'b001, 0);
			wait_outputs(1);
			if(output_scalars != 1 || o_fault)begin
				$display("TB_ERROR_RESET_RECOVERY age=%0d outputs=%0d fault=%0d",
				         reset_age, output_scalars, o_fault);
				error_count = error_count + 1;
			end
			reset_age_executed = reset_age_executed + 1;
			if(error_count == reset_age_errors_before)
				$display("TB_RESET_AGE_PASS age=%0d", reset_age);
		end
		if(reset_age_executed != 24)begin
			$display("TB_ERROR_RESET_COVERAGE ages=%0d", reset_age_executed);
			error_count = error_count + 1;
		end

		// Atomic terminal MAC fault suppresses every lane and latches until reset.
		reset_dut;
		load_full_table;
		i_output_ready = 1'b1;
		@(negedge i_clk);
		set_group(99, 0, 0, 3'b111);
		i_result_fault = 1'b1;
		i_input_valid = 1'b1;
		while(!o_input_ready) @(negedge i_clk);
		@(negedge i_clk);
		i_input_valid = 1'b0;
		i_result_fault = 1'b0;
		repeat(40) @(negedge i_clk);
		if(!o_fault || output_scalars != 0 || o_input_ready)begin
			$display("TB_ERROR_ATOMIC_FAULT fault=%0d outputs=%0d ready=%0d",
			         o_fault, output_scalars, o_input_ready);
			error_count = error_count + 1;
		end

		if(error_count == 0)begin
			$display("TB_PASS_POSTPROCESS continuous=5 fixed_bubbles=3 random_groups=48 random_scalars=96 pressure_groups=12 reset_ages=24 fault=1 latency=23/24");
		end else begin
			$display("TB_FAIL_POSTPROCESS errors=%0d", error_count);
		end
		$finish;
	end

	initial begin
		#15000000;
		$display("TB_FAIL_POSTPROCESS timeout");
		$finish;
	end

	road_postprocess_stream dut(
		.i_clk(i_clk), .i_rstn(i_rstn), .i_table_valid(i_table_valid),
		.i_table_addr(i_table_addr), .i_table_data(i_table_data),
		.o_table_ready(o_table_ready), .o_table_loaded(o_table_loaded),
		.o_table_fault(o_table_fault), .i_input_valid(i_input_valid),
		.i_result_data(i_result_data), .i_result_fault(i_result_fault),
		.i_layer(i_layer), .i_position(i_position), .i_channel_base(i_channel_base),
		.i_lane_mask(i_lane_mask), .o_input_ready(o_input_ready),
		.i_output_ready(i_output_ready), .o_output_valid(o_output_valid),
		.o_output_data(o_output_data), .o_output_tag(o_output_tag), .o_fault(o_fault),
		.o_result_queue_count(o_result_queue_count), .o_meta_count(o_meta_count),
		.o_pre_busy(o_pre_busy), .o_silu_busy(o_silu_busy), .o_post_busy(o_post_busy),
		.o_pre_accept(o_pre_accept), .o_silu_accept(o_silu_accept),
		.o_post_accept(o_post_accept)
	);
endmodule
