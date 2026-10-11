`timescale 1ns / 1ps

module tb_road_onchip_chain;

	reg i_clk;
	reg i_rstn;
	reg i_input_valid;
	reg i_first;
	reg i_last;
	reg [7:0]i_lane_mask;
	reg [63:0]i_activation_data;
	reg [191:0]i_weight_data;
	reg [95:0]i_bias_data;
	wire o_input_ready;
	wire o_fault;
	reg i_table_valid;
	reg [9:0]i_table_addr;
	reg signed [15:0]i_table_data;
	wire o_table_ready;
	wire o_table_loaded;
	wire o_table_fault;
	reg i_cache_read_valid;
	reg [3:0]i_cache_read_addr;
	wire o_cache_read_ready;
	wire o_cache_result_valid;
	wire signed [7:0]o_cache_result_data;
	wire o_cache_result_fault;
	reg i_cache_result_ready;

	reg [15:0]table_words [0:1023];
	reg [215:0]expected_stage [0:11];
	reg [7:0]expected_feature [0:11];
	integer cycle_count;
	integer error_count;
	integer mac_check_count;
	integer pre_check_count;
	integer silu_check_count;
	integer post_check_count;
	integer read_check_count;
	integer atomic_hidden_checks;
	integer reset_case_count;
	integer directed_case_count;
	integer reset_index;
	integer cycle_file;
	integer first_accept_cycle;
	integer last_read_cycle;
	reg flag_stage_check;
	reg flag_first_accept_seen;
	reg signed [7:0]held_cache_data;
	reg held_cache_fault;

	road_onchip_chain dut(
		.i_clk(i_clk),
		.i_rstn(i_rstn),
		.i_input_valid(i_input_valid),
		.i_first(i_first),
		.i_last(i_last),
		.i_lane_mask(i_lane_mask),
		.i_activation_data(i_activation_data),
		.i_weight_data(i_weight_data),
		.i_bias_data(i_bias_data),
		.o_input_ready(o_input_ready),
		.o_fault(o_fault),
		.i_table_valid(i_table_valid),
		.i_table_addr(i_table_addr),
		.i_table_data(i_table_data),
		.o_table_ready(o_table_ready),
		.o_table_loaded(o_table_loaded),
		.o_table_fault(o_table_fault),
		.i_cache_read_valid(i_cache_read_valid),
		.i_cache_read_addr(i_cache_read_addr),
		.o_cache_read_ready(o_cache_read_ready),
		.o_cache_result_valid(o_cache_result_valid),
		.o_cache_result_data(o_cache_result_data),
		.o_cache_result_fault(o_cache_result_fault),
		.i_cache_result_ready(i_cache_result_ready)
	);

	always #5 i_clk = ~i_clk;

	always@(posedge i_clk)begin
		cycle_count = cycle_count + 1;
		if((i_input_valid === 1'b1) && (o_input_ready === 1'b1))begin
			$fwrite(cycle_file, "%0d,input_accept,%0d,%0d,%0d\n", cycle_count, dut.cnt_position, dut.cnt_channel, i_last);
			if(flag_first_accept_seen == 1'b0)begin
				first_accept_cycle = cycle_count;
				flag_first_accept_seen = 1'b1;
			end
		end
		if(flag_stage_check && dut.flag_mac_result_transfer)begin
			if(dut.mac_result_data[31:0] !== expected_stage[(dut.cnt_position * 3)][215:184])begin
				$display("TB_ERROR MAC alpha position=%0d got=%h expected=%h", dut.cnt_position, dut.mac_result_data[31:0], expected_stage[(dut.cnt_position * 3)][215:184]);
				error_count = error_count + 1;
			end
			if(dut.mac_result_data[63:32] !== expected_stage[(dut.cnt_position * 3) + 1][215:184])begin
				$display("TB_ERROR MAC beta position=%0d", dut.cnt_position);
				error_count = error_count + 1;
			end
			if(dut.mac_result_data[95:64] !== expected_stage[(dut.cnt_position * 3) + 2][215:184])begin
				$display("TB_ERROR MAC gamma position=%0d", dut.cnt_position);
				error_count = error_count + 1;
			end
			if(dut.mac_fault !== 1'b0)begin
				$display("TB_ERROR unexpected MAC fault position=%0d", dut.cnt_position);
				error_count = error_count + 1;
			end
			mac_check_count = mac_check_count + 1;
			$fwrite(cycle_file, "%0d,mac_terminal,%0d,0,%0d\n", cycle_count, dut.cnt_position, $signed(dut.mac_result_data[31:0]));
		end
		if(flag_stage_check && (dut.state_current == 4'd3) && dut.round_result_valid)begin
			if(dut.scaled_product !== expected_stage[(dut.cnt_position * 3) + dut.cnt_channel][183:120])begin
				$display("TB_ERROR pre product position=%0d channel=%0d got=%h expected=%h", dut.cnt_position, dut.cnt_channel, dut.scaled_product, expected_stage[(dut.cnt_position * 3) + dut.cnt_channel][183:120]);
				error_count = error_count + 1;
			end
			if(dut.round_result_data !== expected_stage[(dut.cnt_position * 3) + dut.cnt_channel][119:104])begin
				$display("TB_ERROR pre round position=%0d channel=%0d got=%h expected=%h", dut.cnt_position, dut.cnt_channel, dut.round_result_data, expected_stage[(dut.cnt_position * 3) + dut.cnt_channel][119:104]);
				error_count = error_count + 1;
			end
			pre_check_count = pre_check_count + 1;
			$fwrite(cycle_file, "%0d,pre_round,%0d,%0d,%0d\n", cycle_count, dut.cnt_position, dut.cnt_channel, $signed(dut.round_result_data));
		end
		if(flag_stage_check && dut.flag_silu_input_transfer)begin
			if(dut.reg_silu_input !== expected_stage[(dut.cnt_position * 3) + dut.cnt_channel][119:104])begin
				$display("TB_ERROR SiLU input position=%0d channel=%0d", dut.cnt_position, dut.cnt_channel);
				error_count = error_count + 1;
			end
		end
		if(flag_stage_check && dut.flag_silu_output_transfer)begin
			if(dut.silu_output_data !== expected_stage[(dut.cnt_position * 3) + dut.cnt_channel][103:88])begin
				$display("TB_ERROR SiLU output position=%0d channel=%0d got=%h expected=%h", dut.cnt_position, dut.cnt_channel, dut.silu_output_data, expected_stage[(dut.cnt_position * 3) + dut.cnt_channel][103:88]);
				error_count = error_count + 1;
			end
			silu_check_count = silu_check_count + 1;
			$fwrite(cycle_file, "%0d,silu_output,%0d,%0d,%0d\n", cycle_count, dut.cnt_position, dut.cnt_channel, $signed(dut.silu_output_data));
		end
		if(flag_stage_check && (dut.state_current == 4'd7) && dut.round_result_valid)begin
			if(dut.scaled_product !== expected_stage[(dut.cnt_position * 3) + dut.cnt_channel][87:24])begin
				$display("TB_ERROR post product position=%0d channel=%0d got=%h expected=%h", dut.cnt_position, dut.cnt_channel, dut.scaled_product, expected_stage[(dut.cnt_position * 3) + dut.cnt_channel][87:24]);
				error_count = error_count + 1;
			end
			if(dut.round_result_data !== expected_stage[(dut.cnt_position * 3) + dut.cnt_channel][23:8])begin
				$display("TB_ERROR post round position=%0d channel=%0d got=%h expected=%h", dut.cnt_position, dut.cnt_channel, dut.round_result_data, expected_stage[(dut.cnt_position * 3) + dut.cnt_channel][23:8]);
				error_count = error_count + 1;
			end
			if(dut.post_saturated_data !== expected_stage[(dut.cnt_position * 3) + dut.cnt_channel][7:0])begin
				$display("TB_ERROR final feature position=%0d channel=%0d got=%h expected=%h", dut.cnt_position, dut.cnt_channel, dut.post_saturated_data, expected_stage[(dut.cnt_position * 3) + dut.cnt_channel][7:0]);
				error_count = error_count + 1;
			end
			post_check_count = post_check_count + 1;
			$fwrite(cycle_file, "%0d,post_round,%0d,%0d,%0d\n", cycle_count, dut.cnt_position, dut.cnt_channel, $signed(dut.round_result_data));
		end
		if(dut.state_current == 4'd10)begin
			$fwrite(cycle_file, "%0d,position_commit,%0d,2,0\n", cycle_count, dut.cnt_position);
		end
		if(flag_stage_check && ((dut.state_current == 4'd8) || (dut.state_current == 4'd9)))begin
			case(dut.reg_write_base)
				4'd0:begin
					if(dut.reg_cache_valid[2:0] !== 3'b000)begin
						$display("TB_ERROR position zero became visible before gamma commit");
						error_count = error_count + 1;
					end
				end
				4'd3:begin
					if(dut.reg_cache_valid[5:3] !== 3'b000)begin
						$display("TB_ERROR position one became visible before gamma commit");
						error_count = error_count + 1;
					end
				end
				4'd6:begin
					if(dut.reg_cache_valid[8:6] !== 3'b000)begin
						$display("TB_ERROR position two became visible before gamma commit");
						error_count = error_count + 1;
					end
				end
				default:begin
					if(dut.reg_cache_valid[11:9] !== 3'b000)begin
						$display("TB_ERROR position three became visible before gamma commit");
						error_count = error_count + 1;
					end
				end
			endcase
			atomic_hidden_checks = atomic_hidden_checks + 1;
		end
		if((o_cache_result_valid === 1'b1) && (i_cache_result_ready === 1'b1))begin
			last_read_cycle = cycle_count;
			$fwrite(cycle_file, "%0d,cache_consume,0,%0d,%0d\n", cycle_count, i_cache_read_addr, $signed(o_cache_result_data));
		end
	end

	task apply_reset;
		begin
			@(negedge i_clk);
			i_rstn = 1'b0;
			i_input_valid = 1'b0;
			i_table_valid = 1'b0;
			i_cache_read_valid = 1'b0;
			i_cache_result_ready = 1'b0;
			repeat(4) @(posedge i_clk);
			@(negedge i_clk);
			i_rstn = 1'b1;
			repeat(2) @(posedge i_clk);
		end
	endtask

	task load_table;
		integer table_index;
		begin
			@(negedge i_clk);
			i_table_valid = 1'b1;
			for(table_index = 0; table_index < 1024; table_index = table_index + 1)begin
				i_table_addr = table_index[9:0];
				i_table_data = table_words[table_index];
				while(o_table_ready !== 1'b1)begin
					@(negedge i_clk);
				end
				@(posedge i_clk);
				@(negedge i_clk);
			end
			i_table_valid = 1'b0;
			if((o_table_loaded !== 1'b1) || (o_table_fault !== 1'b0))begin
				$display("TB_ERROR true SiLU table load failed loaded=%b fault=%b", o_table_loaded, o_table_fault);
				error_count = error_count + 1;
			end
			$fwrite(cycle_file, "%0d,table_loaded,0,0,0\n", cycle_count);
		end
	endtask

	task run_tensor;
		input [1023:0]vector_name;
		integer vector_file;
		integer beat_index;
		integer scan_count;
		integer vector_first;
		integer vector_last;
		integer unused_valid;
		integer unused_fault;
		reg [7:0]vector_mask;
		reg [63:0]vector_activation;
		reg [191:0]vector_weight;
		reg [95:0]vector_bias;
		reg [95:0]unused_result;
		reg [383:0]unused_products;
		reg [203:0]unused_pairs;
		reg [107:0]unused_quads;
		reg [59:0]unused_dots;
		begin
			vector_file = $fopen(vector_name, "r");
			if(vector_file == 0)begin
				$display("TB_ERROR cannot open vector file %s", vector_name);
				error_count = error_count + 1;
			end
			for(beat_index = 0; beat_index < 8; beat_index = beat_index + 1)begin
				scan_count = $fscanf(vector_file, "%d %d %h %h %h %h %d %d %h %h %h %h %h\n", vector_first, vector_last, vector_mask, vector_activation, vector_weight, vector_bias, unused_valid, unused_fault, unused_result, unused_products, unused_pairs, unused_quads, unused_dots);
				if(scan_count != 13)begin
					$display("TB_ERROR vector parse beat=%0d fields=%0d", beat_index, scan_count);
					error_count = error_count + 1;
				end
				@(negedge i_clk);
				i_first = vector_first[0];
				i_last = vector_last[0];
				i_lane_mask = vector_mask;
				i_activation_data = vector_activation;
				i_weight_data = vector_weight;
				i_bias_data = vector_bias;
				i_input_valid = 1'b1;
				while(o_input_ready !== 1'b1)begin
					@(negedge i_clk);
				end
				@(posedge i_clk);
				@(negedge i_clk);
				i_input_valid = 1'b0;
				repeat(beat_index % 3) @(posedge i_clk);
			end
			$fclose(vector_file);
			while((dut.state_current != 4'd0) || (o_input_ready !== 1'b1))begin
				@(posedge i_clk);
			end
		end
	endtask

	task drive_beat;
		input beat_first;
		input beat_last;
		input [7:0]beat_mask;
		input [63:0]beat_activation;
		input [191:0]beat_weight;
		input [95:0]beat_bias;
		begin
			@(negedge i_clk);
			i_first = beat_first;
			i_last = beat_last;
			i_lane_mask = beat_mask;
			i_activation_data = beat_activation;
			i_weight_data = beat_weight;
			i_bias_data = beat_bias;
			i_input_valid = 1'b1;
			while(o_input_ready !== 1'b1)begin
				@(negedge i_clk);
			end
			@(posedge i_clk);
			@(negedge i_clk);
			i_input_valid = 1'b0;
		end
	endtask

	task reset_during_chain;
		input integer reset_case;
		integer target_state;
		begin
			if(reset_case == 0)begin
				drive_beat(1'b1, 1'b0, 8'hff, 64'hebedf1fcff007f80, 192'h0d0808f40bfaf9f70b00fff800f90d09f2fef304fe01080d, 96'h0000006700000081fffffdfb);
				repeat(3) @(posedge i_clk);
			end else begin
				drive_beat(1'b1, 1'b0, 8'hff, 64'hebedf1fcff007f80, 192'h0d0808f40bfaf9f70b00fff800f90d09f2fef304fe01080d, 96'h0000006700000081fffffdfb);
				drive_beat(1'b0, 1'b1, 8'hff, 64'he320fdfbebe3e416, 192'h0b02f70501f7f000f3f50f10f8fe07090ffd04fdf4010904, 96'h0000006700000081fffffdfb);
				case(reset_case)
					1: target_state = 4'd3;
					2: target_state = 4'd5;
					3: target_state = 4'd7;
					4: target_state = 4'd8;
					default: target_state = 4'd9;
				endcase
				while(dut.state_current != target_state[3:0])begin
					@(negedge i_clk);
				end
			end
			@(negedge i_clk);
			$fwrite(cycle_file, "%0d,reset_assert,0,0,%0d\n", cycle_count, reset_case);
			i_rstn = 1'b0;
			repeat(3) @(posedge i_clk);
			if((dut.state_current !== 4'd0) || (dut.cnt_position !== 2'd0) || (dut.cnt_channel !== 2'd0) || (dut.reg_write_base !== 4'd0) || (dut.reg_cache_valid !== 12'd0) || (dut.mac_result_valid !== 1'b0) || (dut.round_result_valid !== 1'b0) || (dut.silu_output_valid !== 1'b0) || (o_cache_result_valid !== 1'b0) || (o_table_loaded !== 1'b0))begin
				$display("TB_ERROR reset case=%0d did not cancel shared valid, metadata, cache, or table state", reset_case);
				error_count = error_count + 1;
			end
			@(negedge i_clk);
			i_rstn = 1'b1;
			repeat(20) @(posedge i_clk);
			if((dut.reg_cache_valid !== 12'd0) || (o_cache_result_valid !== 1'b0) || (dut.mac_result_valid !== 1'b0) || (dut.round_result_valid !== 1'b0) || (dut.silu_output_valid !== 1'b0))begin
				$display("TB_ERROR reset case=%0d leaked a ghost result after release", reset_case);
				error_count = error_count + 1;
			end
			reset_case_count = reset_case_count + 1;
		end
	endtask

	task read_and_check;
		input integer address_value;
		input integer stall_cycles;
		integer stall_index;
		begin
			@(negedge i_clk);
			i_cache_read_addr = address_value[3:0];
			i_cache_read_valid = 1'b1;
			i_cache_result_ready = (stall_cycles == 0);
			while(o_cache_read_ready !== 1'b1)begin
				@(negedge i_clk);
			end
			@(posedge i_clk);
			@(negedge i_clk);
			i_cache_read_valid = 1'b0;
			while(o_cache_result_valid !== 1'b1)begin
				@(negedge i_clk);
			end
			held_cache_data = o_cache_result_data;
			held_cache_fault = o_cache_result_fault;
			for(stall_index = 0; stall_index < stall_cycles; stall_index = stall_index + 1)begin
				@(posedge i_clk);
				#1;
				if((o_cache_result_valid !== 1'b1) || (o_cache_result_data !== held_cache_data) || (o_cache_result_fault !== held_cache_fault))begin
					$display("TB_ERROR cache response changed under backpressure address=%0d", address_value);
					error_count = error_count + 1;
				end
			end
			if((o_cache_result_fault !== 1'b0) || (o_cache_result_data !== expected_feature[address_value]))begin
				$display("TB_ERROR cache address=%0d got=%h fault=%b expected=%h", address_value, o_cache_result_data, o_cache_result_fault, expected_feature[address_value]);
				error_count = error_count + 1;
			end
			read_check_count = read_check_count + 1;
			@(negedge i_clk);
			i_cache_result_ready = 1'b1;
			@(posedge i_clk);
			@(negedge i_clk);
			i_cache_result_ready = 1'b0;
		end
	endtask

	task read_expect_fault;
		input integer address_value;
		begin
			@(negedge i_clk);
			i_cache_read_addr = address_value[3:0];
			i_cache_read_valid = 1'b1;
			i_cache_result_ready = 1'b1;
			while(o_cache_read_ready !== 1'b1)begin
				@(negedge i_clk);
			end
			@(posedge i_clk);
			@(negedge i_clk);
			i_cache_read_valid = 1'b0;
			while(o_cache_result_valid !== 1'b1)begin
				@(negedge i_clk);
			end
			if((o_cache_result_fault !== 1'b1) || (o_cache_result_data !== 8'sd0))begin
				$display("TB_ERROR fault position address=%0d became readable data=%h fault=%b", address_value, o_cache_result_data, o_cache_result_fault);
				error_count = error_count + 1;
			end
			@(posedge i_clk);
			@(negedge i_clk);
			i_cache_result_ready = 1'b0;
		end
	endtask

	task send_fault_position;
		begin
			@(negedge i_clk);
			i_first = 1'b1;
			i_last = 1'b1;
			i_lane_mask = 8'hff;
			i_activation_data = 64'h0101010101010101;
			i_weight_data = 192'h0303030303030303fefefefefefefefe0101010101010101;
			i_bias_data = 96'h0000012fffffff367ffffffb;
			i_input_valid = 1'b1;
			while(o_input_ready !== 1'b1)begin
				@(negedge i_clk);
			end
			@(posedge i_clk);
			@(negedge i_clk);
			i_input_valid = 1'b0;
			while(dut.state_current != 4'd11)begin
				@(posedge i_clk);
			end
			@(posedge i_clk);
			if(o_fault !== 1'b1)begin
				$display("TB_ERROR atomic MAC fault was not published");
				error_count = error_count + 1;
			end
			if(dut.reg_cache_valid[2:0] !== 3'b000)begin
				$display("TB_ERROR fault position committed cache valid bits=%b", dut.reg_cache_valid[2:0]);
				error_count = error_count + 1;
			end
		end
	endtask

	initial begin
		i_clk = 1'b0;
		i_rstn = 1'b0;
		i_input_valid = 1'b0;
		i_first = 1'b0;
		i_last = 1'b0;
		i_lane_mask = 8'd0;
		i_activation_data = 64'd0;
		i_weight_data = 192'd0;
		i_bias_data = 96'd0;
		i_table_valid = 1'b0;
		i_table_addr = 10'd0;
		i_table_data = 16'sd0;
		i_cache_read_valid = 1'b0;
		i_cache_read_addr = 4'd0;
		i_cache_result_ready = 1'b0;
		cycle_count = 0;
		error_count = 0;
		mac_check_count = 0;
		pre_check_count = 0;
		silu_check_count = 0;
		post_check_count = 0;
		read_check_count = 0;
		atomic_hidden_checks = 0;
		reset_case_count = 0;
		directed_case_count = 0;
		first_accept_cycle = 0;
		last_read_cycle = 0;
		flag_stage_check = 1'b0;
		flag_first_accept_seen = 1'b0;
		cycle_file = $fopen("cycle_trace.csv", "w");
		$fwrite(cycle_file, "cycle,event,position,channel,value\n");
		$readmemh("inputs/silu_table.hex", table_words);

		apply_reset;
		load_table;
		$readmemh("inputs/expected_stages_16.hex", expected_stage);
		$readmemh("inputs/expected_features_16.hex", expected_feature);
		flag_stage_check = 1'b1;
		flag_first_accept_seen = 1'b0;
		run_tensor("inputs/mac_16_channels.txt");
		read_and_check(0, 0);
		read_and_check(1, 0);
		read_and_check(2, 0);
		read_and_check(3, 0);
		read_and_check(4, 0);
		read_and_check(5, 0);
		read_and_check(6, 0);
		read_and_check(7, 0);
		read_and_check(8, 0);
		read_and_check(9, 0);
		read_and_check(10, 0);
		read_and_check(11, 0);
		$display("TB_CASE base16 accept_to_last_read=%0d", last_read_cycle - first_accept_cycle);

		flag_stage_check = 1'b0;
		apply_reset;
		load_table;
		$readmemh("inputs/expected_stages_13.hex", expected_stage);
		$readmemh("inputs/expected_features_13.hex", expected_feature);
		flag_stage_check = 1'b1;
		flag_first_accept_seen = 1'b0;
		run_tensor("inputs/mac_13_channels.txt");
		read_and_check(0, 3);
		read_and_check(1, 0);
		read_and_check(2, 0);
		read_and_check(3, 0);
		read_and_check(4, 0);
		read_and_check(5, 20);
		read_and_check(6, 0);
		read_and_check(7, 0);
		read_and_check(8, 0);
		read_and_check(9, 0);
		read_and_check(10, 0);
		read_and_check(11, 0);
		$display("TB_CASE tail13 accept_to_last_read=%0d", last_read_cycle - first_accept_cycle);

		flag_stage_check = 1'b0;
		apply_reset;
		load_table;
		$readmemh("inputs/expected_stages_saturation.hex", expected_stage);
		$readmemh("inputs/expected_features_saturation.hex", expected_feature);
		flag_stage_check = 1'b1;
		drive_beat(1'b1, 1'b1, 8'hff, 64'd0, 192'd0, 96'h00000008fffe7960000186a0);
		while((dut.state_current != 4'd0) || (o_input_ready !== 1'b1))begin
			@(posedge i_clk);
		end
		read_and_check(0, 0);
		read_and_check(1, 0);
		read_and_check(2, 0);
		directed_case_count = directed_case_count + 1;
		$display("TB_CASE directed_saturation pre_pos=32767 pre_neg=-32768 tie_even=2 feature_pos=127");

		flag_stage_check = 1'b0;
		@(negedge i_clk);
		i_cache_read_addr = 4'd0;
		i_cache_read_valid = 1'b1;
		i_cache_result_ready = 1'b0;
		@(posedge i_clk);
		@(negedge i_clk);
		i_cache_read_valid = 1'b0;
		while(o_cache_result_valid !== 1'b1)begin
			@(negedge i_clk);
		end
		i_rstn = 1'b0;
		repeat(2) @(posedge i_clk);
		if(o_cache_result_valid !== 1'b0)begin
			$display("TB_ERROR reset did not cancel held cache response");
			error_count = error_count + 1;
		end
		@(negedge i_clk);
		i_rstn = 1'b1;
		for(reset_index = 0; reset_index < 6; reset_index = reset_index + 1)begin
			load_table;
			reset_during_chain(reset_index);
			read_expect_fault(0);
		end
		load_table;
		send_fault_position;
		read_expect_fault(0);
		read_expect_fault(1);
		read_expect_fault(2);

		if((mac_check_count != 9) || (pre_check_count != 27) || (silu_check_count != 27) || (post_check_count != 27) || (read_check_count != 27) || (atomic_hidden_checks != 18) || (reset_case_count != 6) || (directed_case_count != 1))begin
			$display("TB_ERROR incomplete stage coverage mac=%0d pre=%0d silu=%0d post=%0d read=%0d atomic_hidden=%0d reset=%0d directed=%0d", mac_check_count, pre_check_count, silu_check_count, post_check_count, read_check_count, atomic_hidden_checks, reset_case_count, directed_case_count);
			error_count = error_count + 1;
		end
		$fclose(cycle_file);
		if(error_count == 0)begin
			$display("TB_PASS_CHAIN mac=%0d pre=%0d silu=%0d post=%0d read=%0d atomic_hidden=%0d reset=%0d directed=%0d errors=0", mac_check_count, pre_check_count, silu_check_count, post_check_count, read_check_count, atomic_hidden_checks, reset_case_count, directed_case_count);
		end else begin
			$display("TB_FAIL_CHAIN errors=%0d", error_count);
		end
		$finish;
	end

	initial begin
		#2000000;
		$display("TB_FAIL_CHAIN timeout errors=%0d", error_count + 1);
		$finish;
	end

endmodule
