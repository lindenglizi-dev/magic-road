`timescale 1ns / 1ps

module tb_road_low_io_physical_shell;

	reg i_clk;
	reg i_rstn;
	reg i_rx_valid;
	reg [15:0]i_rx_data;
	wire o_rx_ready;
	wire o_tx_valid;
	wire [15:0]o_tx_data;
	reg i_tx_ready;

	reg signed [15:0]table_words [0:1023];
	reg [7:0]expected_feature [0:11];
	integer error_count;
	integer case_count;
	integer cycle_count;
	integer trace_file;
	integer loop_index;
	integer session_send_count;
	integer table_begin_cycle;
	integer run_command_cycle;
	integer first_core_cycle;
	integer core_done_cycle;
	integer export_command_cycle;
	integer last_result_cycle;
	integer core_hold_checks;
	reg [15:0]received_word;
	reg [15:0]status_words [0:17];
	reg flag_core_hold;
	reg held_chain_first;
	reg held_chain_last;
	reg [7:0]held_chain_mask;
	reg [63:0]held_chain_activation;
	reg [191:0]held_chain_weight;
	reg [95:0]held_chain_bias;

	road_low_io_physical_shell dut(
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

	always@(posedge i_clk)begin
		cycle_count = cycle_count + 1;
		$fwrite(trace_file, "%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d\n",
			cycle_count,
			i_rstn,
			dut.state_current,
			dut.road_onchip_chain_Inst_shell.state_current,
			dut.flag_rx_transfer,
			dut.flag_core_input_transfer,
			dut.road_onchip_chain_Inst_shell.flag_mac_result_transfer,
			dut.road_onchip_chain_Inst_shell.round_result_valid,
			dut.road_onchip_chain_Inst_shell.flag_silu_output_transfer,
			(dut.road_onchip_chain_Inst_shell.state_current == 4'd10),
			dut.flag_cache_request_transfer,
			dut.flag_cache_result_transfer,
			dut.flag_tx_transfer);
		if(dut.flag_rx_transfer && (i_rx_data == 16'h1000))begin
			table_begin_cycle = cycle_count;
		end
		if(dut.flag_rx_transfer && (i_rx_data[15:12] == 4'h3) && dut.flag_run_command_legal)begin
			run_command_cycle = cycle_count;
		end
		if(dut.flag_core_input_transfer && (first_core_cycle == 0))begin
			first_core_cycle = cycle_count;
		end
		if((dut.state_current == 4'd6) && dut.flag_core_busy_observed && dut.chain_input_ready)begin
			core_done_cycle = cycle_count;
		end
		if(dut.flag_rx_transfer && (i_rx_data == 16'h4000) && dut.flag_normal_export_legal)begin
			export_command_cycle = cycle_count;
		end
		if((dut.state_current == 4'd10) && dut.flag_tx_transfer && ({1'b0, dut.cnt_export_addr} + 5'd1 >= {1'b0, dut.reg_export_count}))begin
			last_result_cycle = cycle_count;
		end
	end

	always@(negedge i_clk)begin
		if(i_rstn == 1'b0)begin
			flag_core_hold = 1'b0;
		end else if(dut.chain_input_valid && (~dut.chain_input_ready))begin
			if(~flag_core_hold)begin
				flag_core_hold = 1'b1;
				held_chain_first = dut.chain_first;
				held_chain_last = dut.chain_last;
				held_chain_mask = dut.chain_lane_mask;
				held_chain_activation = dut.chain_activation_data;
				held_chain_weight = dut.chain_weight_data;
				held_chain_bias = dut.chain_bias_data;
			end else begin
				core_hold_checks = core_hold_checks + 1;
				if((dut.chain_first !== held_chain_first) || (dut.chain_last !== held_chain_last) || (dut.chain_lane_mask !== held_chain_mask) || (dut.chain_activation_data !== held_chain_activation) || (dut.chain_weight_data !== held_chain_weight) || (dut.chain_bias_data !== held_chain_bias))begin
					$display("TB_ERROR buffered parallel packet changed under core backpressure");
					error_count = error_count + 1;
				end
			end
		end else begin
			flag_core_hold = 1'b0;
		end
	end

	task apply_reset;
		begin
			@(negedge i_clk);
			i_rstn = 1'b0;
			i_rx_valid = 1'b0;
			i_rx_data = 16'd0;
			i_tx_ready = 1'b0;
			session_send_count = 0;
			table_begin_cycle = 0;
			run_command_cycle = 0;
			first_core_cycle = 0;
			core_done_cycle = 0;
			export_command_cycle = 0;
			last_result_cycle = 0;
			repeat(4) @(posedge i_clk);
			@(negedge i_clk);
			i_rstn = 1'b1;
			repeat(2) @(posedge i_clk);
		end
	endtask

	task send_word;
		input [15:0]word_value;
		input integer hold_cycles;
		integer hold_index;
		begin
			for(hold_index = 0; hold_index < hold_cycles; hold_index = hold_index + 1)begin
				@(posedge i_clk);
			end
			@(negedge i_clk);
			i_rx_valid = 1'b1;
			i_rx_data = word_value;
			while(o_rx_ready !== 1'b1)begin
				@(posedge i_clk);
				#1;
				if(i_rx_data !== word_value)begin
					$display("TB_ERROR RX source payload changed before handshake");
					error_count = error_count + 1;
				end
				@(negedge i_clk);
			end
			@(posedge i_clk);
			session_send_count = session_send_count + 1;
			@(negedge i_clk);
			i_rx_valid = 1'b0;
			i_rx_data = 16'd0;
			if(dut.cnt_rx_words !== session_send_count)begin
				$display("TB_ERROR RX handshake count got=%0d expected=%0d", dut.cnt_rx_words, session_send_count);
				error_count = error_count + 1;
			end
		end
	endtask

	task receive_word;
		output [15:0]word_value;
		input integer stall_cycles;
		integer stall_index;
		reg [15:0]held_word;
		begin
			while(o_tx_valid !== 1'b1)begin
				@(negedge i_clk);
			end
			held_word = o_tx_data;
			for(stall_index = 0; stall_index < stall_cycles; stall_index = stall_index + 1)begin
				@(posedge i_clk);
				#1;
				if((o_tx_valid !== 1'b1) || (o_tx_data !== held_word))begin
					$display("TB_ERROR TX payload changed under backpressure");
					error_count = error_count + 1;
				end
			end
			@(negedge i_clk);
			i_tx_ready = 1'b1;
			@(posedge i_clk);
			@(negedge i_clk);
			i_tx_ready = 1'b0;
			word_value = held_word;
		end
	endtask

	task load_table;
		integer table_index;
		begin
			send_word(16'h1000, 0);
			for(table_index = 0; table_index < 1024; table_index = table_index + 1)begin
				send_word(table_words[table_index], table_index % 3 == 0);
			end
			while(dut.flag_table_complete !== 1'b1)begin
				@(negedge i_clk);
				if(dut.flag_shell_fault)begin
					$display("TB_ERROR table load raised shell fault code=%h", dut.reg_shell_error);
					error_count = error_count + 1;
				end
			end
		end
	endtask

	task send_packet;
		input packet_first;
		input packet_last;
		input [7:0]packet_mask;
		input [63:0]packet_activation;
		input [191:0]packet_weight;
		input [95:0]packet_bias;
		integer word_index;
		begin
			send_word({4'h2, packet_first, packet_last, packet_mask, 2'd0}, 0);
			for(word_index = 0; word_index < 4; word_index = word_index + 1)begin
				send_word(packet_activation[word_index * 16 +: 16], word_index % 2);
			end
			for(word_index = 0; word_index < 12; word_index = word_index + 1)begin
				send_word(packet_weight[word_index * 16 +: 16], word_index % 2);
			end
			for(word_index = 0; word_index < 6; word_index = word_index + 1)begin
				send_word(packet_bias[word_index * 16 +: 16], word_index % 2);
			end
			while(dut.state_current != 4'd0)begin
				@(negedge i_clk);
			end
		end
	endtask

	task load_vector_file;
		input [1023:0]vector_name;
		input integer beat_count;
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
			for(beat_index = 0; beat_index < beat_count; beat_index = beat_index + 1)begin
				scan_count = $fscanf(vector_file, "%d %d %h %h %h %h %d %d %h %h %h %h %h\n", vector_first, vector_last, vector_mask, vector_activation, vector_weight, vector_bias, unused_valid, unused_fault, unused_result, unused_products, unused_pairs, unused_quads, unused_dots);
				if(scan_count != 13)begin
					$display("TB_ERROR vector parse beat=%0d fields=%0d", beat_index, scan_count);
					error_count = error_count + 1;
				end
				send_packet(vector_first[0], vector_last[0], vector_mask, vector_activation, vector_weight, vector_bias);
			end
			$fclose(vector_file);
		end
	endtask

	task run_and_check_done;
		input [6:0]packet_count;
		input expected_chain_fault;
		reg [15:0]done_word;
		begin
			send_word({4'h3, 5'd0, packet_count}, 0);
			receive_word(done_word, 7);
			if((done_word[15:12] !== 4'ha) || (done_word[11] !== expected_chain_fault))begin
				$display("TB_ERROR RUN completion word=%h expected_chain_fault=%b", done_word, expected_chain_fault);
				error_count = error_count + 1;
			end
			@(posedge i_clk);
			#1;
			if((o_tx_valid !== 1'b0) || (o_rx_ready !== 1'b1))begin
				$display("TB_ERROR RUN response did not release TX and command input valid=%b ready=%b", o_tx_valid, o_rx_ready);
				error_count = error_count + 1;
			end
		end
	endtask

	task export_and_check;
		input integer result_count;
		input expect_fault;
		integer result_index;
		reg [15:0]result_word;
		begin
			send_word(16'h4000, 0);
			for(result_index = 0; result_index < result_count; result_index = result_index + 1)begin
				receive_word(result_word, result_index % 5);
				if((result_word[15:13] !== 3'b100) || (result_word[12] !== expect_fault) || (result_word[11:8] !== result_index[3:0]))begin
					$display("TB_ERROR result framing index=%0d word=%h", result_index, result_word);
					error_count = error_count + 1;
				end
				if(expect_fault)begin
					if(result_word[7:0] !== 8'd0)begin
						$display("TB_ERROR fault result index=%0d data=%h", result_index, result_word[7:0]);
						error_count = error_count + 1;
					end
				end else if(result_word[7:0] !== expected_feature[result_index])begin
					$display("TB_ERROR result index=%0d got=%h expected=%h", result_index, result_word[7:0], expected_feature[result_index]);
					error_count = error_count + 1;
				end
			end
			receive_word(result_word, 2);
			if((result_word[15:12] !== 4'hc) || (result_word[7:0] !== result_count[7:0]))begin
				$display("TB_ERROR export completion word=%h count=%0d", result_word, result_count);
				error_count = error_count + 1;
			end
		end
	endtask

	task status_and_check;
		input [2:0]expected_positions;
		input [31:0]expected_core_inputs;
		input [31:0]expected_results;
		integer status_index;
		begin
			send_word(16'h5000, 0);
			for(status_index = 0; status_index < 18; status_index = status_index + 1)begin
				receive_word(status_words[status_index], status_index % 4);
			end
			if((status_words[0][15:12] !== 4'hb) || (status_words[0][2:0] !== expected_positions))begin
				$display("TB_ERROR status header=%h positions=%0d", status_words[0], expected_positions);
				error_count = error_count + 1;
			end
			if({status_words[7], status_words[6]} !== expected_core_inputs)begin
				$display("TB_ERROR status core inputs=%h_%h expected=%0d", status_words[7], status_words[6], expected_core_inputs);
				error_count = error_count + 1;
			end
			if({status_words[9], status_words[8]} !== expected_results)begin
				$display("TB_ERROR status results=%h_%h expected=%0d", status_words[9], status_words[8], expected_results);
				error_count = error_count + 1;
			end
			if(({status_words[13], status_words[12]} == 32'd0) || ({status_words[15], status_words[14]} == 32'd0))begin
				$display("TB_ERROR status did not record core/export cycle endpoints");
				error_count = error_count + 1;
			end
			if(({status_words[11], status_words[10]} !== (run_command_cycle - table_begin_cycle)) || ({status_words[13], status_words[12]} !== (core_done_cycle - first_core_cycle)) || ({status_words[15], status_words[14]} !== (last_result_cycle - export_command_cycle)))begin
				$display("TB_ERROR endpoint cycle mismatch preload=%0d/%0d core=%0d/%0d export=%0d/%0d", {status_words[11], status_words[10]}, run_command_cycle - table_begin_cycle, {status_words[13], status_words[12]}, core_done_cycle - first_core_cycle, {status_words[15], status_words[14]}, last_result_cycle - export_command_cycle);
				error_count = error_count + 1;
			end
		end
	endtask

	task fill_expected_zero;
		integer expected_index;
		begin
			for(expected_index = 0; expected_index < 12; expected_index = expected_index + 1)begin
				expected_feature[expected_index] = 8'd0;
			end
		end
	endtask

	initial begin
		i_clk = 1'b0;
		i_rstn = 1'b0;
		i_rx_valid = 1'b0;
		i_rx_data = 16'd0;
		i_tx_ready = 1'b0;
		error_count = 0;
		case_count = 0;
		cycle_count = 0;
		session_send_count = 0;
		table_begin_cycle = 0;
		run_command_cycle = 0;
		first_core_cycle = 0;
		core_done_cycle = 0;
		export_command_cycle = 0;
		last_result_cycle = 0;
		core_hold_checks = 0;
		flag_core_hold = 1'b0;
		trace_file = $fopen("shell_cycle_trace.csv", "w");
		$fwrite(trace_file, "cycle,rstn,shell_state,chain_state,rx_transfer,core_input,mac_terminal,round_valid,silu_output,commit_gamma,cache_request,cache_result,tx_transfer\n");
		$readmemh("inputs/silu_table.hex", table_words);

		apply_reset;
		send_word(16'h1000, 0);
		for(loop_index = 0; loop_index < 10; loop_index = loop_index + 1)begin
			send_word(table_words[loop_index], 0);
		end
		repeat(20) @(posedge i_clk);
		if(dut.flag_table_complete || dut.flag_run_issued || dut.chain_input_valid)begin
			$display("TB_ERROR partial table enabled computation");
			error_count = error_count + 1;
		end
		case_count = case_count + 1;

		apply_reset;
		load_table;
		$readmemh("inputs/expected_features_16.hex", expected_feature);
		load_vector_file("inputs/mac_16_channels.txt", 8);
		run_and_check_done(7'd8, 1'b0);
		export_and_check(12, 1'b0);
		status_and_check(3'd4, 32'd8, 32'd12);
		send_word(16'h3008, 0);
		repeat(10) @(posedge i_clk);
		if((~dut.flag_shell_fault) || dut.flag_run_issued !== 1'b1)begin
			$display("TB_ERROR second RUN was not explicitly rejected");
			error_count = error_count + 1;
		end
		case_count = case_count + 1;

		apply_reset;
		load_table;
		$readmemh("inputs/expected_features_13.hex", expected_feature);
		load_vector_file("inputs/mac_13_channels.txt", 8);
		run_and_check_done(7'd8, 1'b0);
		export_and_check(12, 1'b0);
		case_count = case_count + 1;

		apply_reset;
		load_table;
		$readmemh("inputs/expected_features_saturation.hex", expected_feature);
		send_packet(1'b1, 1'b1, 8'hff, 64'd0, 192'd0, 96'h00000008fffe7960000186a0);
		run_and_check_done(7'd1, 1'b0);
		export_and_check(3, 1'b0);
		case_count = case_count + 1;

		apply_reset;
		load_table;
		fill_expected_zero;
		send_packet(1'b1, 1'b1, 8'hff, 64'h0101010101010101, 192'h0303030303030303fefefefefefefefe0101010101010101, 96'h0000012fffffff367ffffffb);
		run_and_check_done(7'd1, 1'b1);
		export_and_check(3, 1'b1);
		case_count = case_count + 1;

		apply_reset;
		load_table;
		$readmemh("inputs/signed_case_1_expected.hex", expected_feature);
		load_vector_file("inputs/signed_case_1.txt", 2);
		run_and_check_done(7'd2, 1'b0);
		export_and_check(3, 1'b0);
		case_count = case_count + 1;

		apply_reset;
		load_table;
		$readmemh("inputs/signed_case_2_expected.hex", expected_feature);
		load_vector_file("inputs/signed_case_2.txt", 2);
		run_and_check_done(7'd2, 1'b0);
		export_and_check(3, 1'b0);
		case_count = case_count + 1;

		apply_reset;
		load_table;
		$readmemh("inputs/signed_case_9_expected.hex", expected_feature);
		load_vector_file("inputs/signed_case_9.txt", 24);
		run_and_check_done(7'd24, 1'b0);
		export_and_check(3, 1'b0);
		status_and_check(3'd1, 32'd24, 32'd3);
		case_count = case_count + 1;

		apply_reset;
		load_table;
		fill_expected_zero;
		load_vector_file("inputs/signed_case_10.txt", 24);
		run_and_check_done(7'd24, 1'b1);
		export_and_check(3, 1'b1);
		case_count = case_count + 1;

		apply_reset;
		load_table;
		send_word({4'h2, 1'b1, 1'b1, 8'hff, 2'd0}, 0);
		send_word(16'h1234, 0);
		send_word(16'h5678, 0);
		send_word(16'h9abc, 0);
		repeat(10) @(posedge i_clk);
		if((dut.state_current !== 4'd3) || (dut.cnt_packet_loaded !== 7'd0) || dut.flag_run_issued || dut.chain_input_valid)begin
			$display("TB_ERROR partial packet started or published computation state=%0d packets=%0d", dut.state_current, dut.cnt_packet_loaded);
			error_count = error_count + 1;
		end
		apply_reset;
		case_count = case_count + 1;

		apply_reset;
		send_word(16'h6000, 0);
		receive_word(received_word, 5);
		if((received_word[15:13] !== 3'b100) || (received_word[12] !== 1'b1) || (received_word[11:8] !== 4'd0) || (received_word[7:0] !== 8'd0))begin
			$display("TB_ERROR explicit uncommitted diagnostic read word=%h", received_word);
			error_count = error_count + 1;
		end
		send_word(16'h600f, 0);
		receive_word(received_word, 3);
		if((received_word[15:13] !== 3'b100) || (received_word[12] !== 1'b1) || (received_word[11:8] !== 4'd15) || (received_word[7:0] !== 8'd0))begin
			$display("TB_ERROR explicit out-of-range diagnostic read word=%h", received_word);
			error_count = error_count + 1;
		end
		case_count = case_count + 1;

		apply_reset;
		load_table;
		fill_expected_zero;
		for(loop_index = 0; loop_index < 96; loop_index = loop_index + 1)begin
			send_packet((loop_index % 24) == 0, (loop_index % 24) == 23, 8'hff, 64'd0, 192'd0, 96'd0);
		end
		if((dut.cnt_packet_loaded !== 7'd96) || (dut.cnt_position_loaded !== 3'd4))begin
			$display("TB_ERROR maximum buffer counters packets=%0d positions=%0d", dut.cnt_packet_loaded, dut.cnt_position_loaded);
			error_count = error_count + 1;
		end
		run_and_check_done(7'd96, 1'b0);
		export_and_check(12, 1'b0);
		status_and_check(3'd4, 32'd96, 32'd12);
		case_count = case_count + 1;

		apply_reset;
		load_table;
		for(loop_index = 0; loop_index < 25; loop_index = loop_index + 1)begin
			send_packet(loop_index == 0, loop_index == 24, 8'hff, 64'd0, 192'd0, 96'd0);
		end
		if((~dut.flag_shell_fault) || (dut.reg_shell_error !== 8'h04) || (dut.cnt_packet_loaded !== 7'd24) || dut.flag_run_issued)begin
			$display("TB_ERROR 25-group guard fault=%b code=%h packets=%0d run=%b", dut.flag_shell_fault, dut.reg_shell_error, dut.cnt_packet_loaded, dut.flag_run_issued);
			error_count = error_count + 1;
		end
		case_count = case_count + 1;

		apply_reset;
		load_table;
		send_packet(1'b1, 1'b1, 8'hff, 64'd0, 192'd0, 96'd0);
		send_word(16'h3001, 0);
		while(dut.state_current != 4'd6)begin
			@(negedge i_clk);
		end
		apply_reset;
		if(dut.flag_table_complete || dut.flag_run_complete || o_tx_valid || (dut.cnt_packet_loaded != 0))begin
			$display("TB_ERROR reset leaked old run or packet state");
			error_count = error_count + 1;
		end
		load_table;
		fill_expected_zero;
		send_packet(1'b1, 1'b1, 8'hff, 64'd0, 192'd0, 96'd0);
		run_and_check_done(7'd1, 1'b0);
		send_word(16'h4000, 0);
		while(o_tx_valid !== 1'b1)begin
			@(negedge i_clk);
		end
		apply_reset;
		if(o_tx_valid || dut.flag_table_complete || dut.flag_run_complete)begin
			$display("TB_ERROR reset did not cancel held export result and run state");
			error_count = error_count + 1;
		end
		load_table;
		fill_expected_zero;
		send_packet(1'b1, 1'b1, 8'hff, 64'd0, 192'd0, 96'd0);
		run_and_check_done(7'd1, 1'b0);
		export_and_check(3, 1'b0);
		send_word(16'h5000, 0);
		while(o_tx_valid !== 1'b1)begin
			@(negedge i_clk);
		end
		apply_reset;
		if(o_tx_valid !== 1'b0)begin
			$display("TB_ERROR reset did not cancel held status response");
			error_count = error_count + 1;
		end
		case_count = case_count + 1;

		$fclose(trace_file);
		if((core_hold_checks == 0))begin
			$display("TB_ERROR no core-backpressure payload-hold checks executed");
			error_count = error_count + 1;
		end
		if((error_count == 0) && (case_count == 14))begin
			$display("TB_PASS_LOW_IO cases=%0d errors=0 io_bits=38 max_packets=96 max_groups=24 max_terms=192", case_count);
		end else begin
			$display("TB_FAIL_LOW_IO cases=%0d errors=%0d", case_count, error_count);
		end
		$finish;
	end

	initial begin
		#10000000;
		$display("TB_FAIL_LOW_IO timeout errors=%0d", error_count + 1);
		$finish;
	end

endmodule
