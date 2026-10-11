`timescale 1ns / 1ps

module tb_down2_tile_runner;

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
	integer stage_index = 0;
	integer expected_stage_count = 0;
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
	integer core_sum = 0;
	integer dw_sum = 0;
	integer pw_sum = 0;
	reg check_active = 1'b0;
	reg check_pw_only = 1'b0;
	reg held_valid = 1'b0;
	reg signed [7:0]held_data = 8'sd0;
	reg [8:0]held_index = 9'd0;

	always #5 i_clk = ~i_clk;

	always@(posedge i_clk)begin
		cycle_count = cycle_count + 1;
	end

	always@(negedge i_clk)begin
		if(check_active && o_debug_valid)begin
			record_index = stage_index / 4;
			expected_phase = stage_index % 4;
			if(check_pw_only)begin
				expected_layer = 1;
				expected_position = record_index / 24;
				expected_channel = record_index % 24;
			end else if(record_index < 256)begin
				expected_layer = 0;
				expected_position = record_index / 16;
				expected_channel = record_index % 16;
			end else begin
				record_offset = record_index - 256;
				expected_layer = 1;
				expected_position = record_offset / 24;
				expected_channel = record_offset % 24;
			end
			if((o_debug_phase !== expected_phase[1:0]) ||
			   (o_debug_layer !== expected_layer[0]) ||
			   (o_debug_position !== expected_position[3:0]) ||
			   (o_debug_channel !== expected_channel[4:0]) ||
			   ($signed(o_debug_value) !== $signed(mem_expected_stage[stage_index])))begin
				$display("TB_ERROR_STAGE case=%0d index=%0d phase=%0d/%0d layer=%0d/%0d pos=%0d/%0d ch=%0d/%0d got=%0d exp=%0d",
				         case_index, stage_index, o_debug_phase, expected_phase,
				         o_debug_layer, expected_layer, o_debug_position,
				         expected_position, o_debug_channel, expected_channel,
				         $signed(o_debug_value), $signed(mem_expected_stage[stage_index]));
				error_count = error_count + 1;
			end
			stage_index = stage_index + 1;
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
		stage_index = 0;
		check_pw_only = pw_only;
		expected_stage_count = pw_only ? 1536 : 2560;
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
		while(!o_done && !o_fault) @(negedge i_clk);
		done_cycle = cycle_count;
		check_active = 1'b0;
		if(o_fault)begin
			$display("TB_ERROR_CORE fault before done case=%0d", case_index);
			error_count = error_count + 1;
		end
		if(stage_index != expected_stage_count)begin
			$display("TB_ERROR_STAGE_COUNT got=%0d exp=%0d", stage_index, expected_stage_count);
			error_count = error_count + 1;
		end
		core_sum = o_mac_cycles + o_pre_cycles + o_silu_cycles + o_post_cycles +
		           o_writeback_cycles + o_storage_wait_cycles + o_scheduler_idle_cycles;
		if(core_sum !== o_core_cycles)begin
			$display("TB_ERROR_CYCLE_SUM sum=%0d core=%0d", core_sum, o_core_cycles);
			error_count = error_count + 1;
		end
		dw_sum = down2_tile_runner_Inst_tb.cnt_dw_mac_cycles +
		         down2_tile_runner_Inst_tb.cnt_dw_pre_cycles +
		         down2_tile_runner_Inst_tb.cnt_dw_silu_cycles +
		         down2_tile_runner_Inst_tb.cnt_dw_post_cycles +
		         down2_tile_runner_Inst_tb.cnt_dw_writeback_cycles +
		         down2_tile_runner_Inst_tb.cnt_dw_storage_wait_cycles +
		         down2_tile_runner_Inst_tb.cnt_dw_scheduler_idle_cycles;
		pw_sum = down2_tile_runner_Inst_tb.cnt_pw_mac_cycles +
		         down2_tile_runner_Inst_tb.cnt_pw_pre_cycles +
		         down2_tile_runner_Inst_tb.cnt_pw_silu_cycles +
		         down2_tile_runner_Inst_tb.cnt_pw_post_cycles +
		         down2_tile_runner_Inst_tb.cnt_pw_writeback_cycles +
		         down2_tile_runner_Inst_tb.cnt_pw_storage_wait_cycles +
		         down2_tile_runner_Inst_tb.cnt_pw_scheduler_idle_cycles;
		if((dw_sum !== down2_tile_runner_Inst_tb.cnt_dw_core_cycles) ||
		   (pw_sum !== down2_tile_runner_Inst_tb.cnt_pw_core_cycles) ||
		   ((dw_sum + pw_sum) !== o_core_cycles))begin
			$display("TB_ERROR_LAYER_CYCLE_SUM dw=%0d/%0d pw=%0d/%0d total=%0d",
			         dw_sum, down2_tile_runner_Inst_tb.cnt_dw_core_cycles,
			         pw_sum, down2_tile_runner_Inst_tb.cnt_pw_core_cycles,
			         o_core_cycles);
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
		$display("LAYER_CYCLE_RESULT case=%0d dw_core=%0d dw_mac=%0d dw_pre=%0d dw_silu=%0d dw_post=%0d dw_writeback=%0d dw_storage_wait=%0d dw_scheduler_idle=%0d pw_core=%0d pw_mac=%0d pw_pre=%0d pw_silu=%0d pw_post=%0d pw_writeback=%0d pw_storage_wait=%0d pw_scheduler_idle=%0d",
		         case_index,
		         down2_tile_runner_Inst_tb.cnt_dw_core_cycles,
		         down2_tile_runner_Inst_tb.cnt_dw_mac_cycles,
		         down2_tile_runner_Inst_tb.cnt_dw_pre_cycles,
		         down2_tile_runner_Inst_tb.cnt_dw_silu_cycles,
		         down2_tile_runner_Inst_tb.cnt_dw_post_cycles,
		         down2_tile_runner_Inst_tb.cnt_dw_writeback_cycles,
		         down2_tile_runner_Inst_tb.cnt_dw_storage_wait_cycles,
		         down2_tile_runner_Inst_tb.cnt_dw_scheduler_idle_cycles,
		         down2_tile_runner_Inst_tb.cnt_pw_core_cycles,
		         down2_tile_runner_Inst_tb.cnt_pw_mac_cycles,
		         down2_tile_runner_Inst_tb.cnt_pw_pre_cycles,
		         down2_tile_runner_Inst_tb.cnt_pw_silu_cycles,
		         down2_tile_runner_Inst_tb.cnt_pw_post_cycles,
		         down2_tile_runner_Inst_tb.cnt_pw_writeback_cycles,
		         down2_tile_runner_Inst_tb.cnt_pw_storage_wait_cycles,
		         down2_tile_runner_Inst_tb.cnt_pw_scheduler_idle_cycles);
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

	initial begin
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

	down2_tile_runner down2_tile_runner_Inst_tb(
		.i_clk(i_clk), .i_rstn(i_rstn),
		.i_table_valid(i_table_valid), .i_table_addr(i_table_addr),
		.i_table_data(i_table_data), .o_table_ready(o_table_ready),
		.o_table_loaded(o_table_loaded), .o_table_fault(o_table_fault),
		.i_load_valid(i_load_valid), .i_load_kind(i_load_kind),
		.i_load_addr(i_load_addr), .i_load_data(i_load_data), .o_load_ready(o_load_ready),
		.i_start(i_start), .i_pw_only(i_pw_only), .o_busy(o_busy),
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
		.o_export_cycles(o_export_cycles)
	);

endmodule
