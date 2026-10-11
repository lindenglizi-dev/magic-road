`timescale 1ns / 1ps

module tb_silu_semantic_assertions
(
	output reg o_test_done
);

	reg i_clk;
	reg i_rstn;
	reg i_table_valid;
	reg [9:0]i_table_addr;
	reg signed [15:0]i_table_data;
	reg i_input_valid;
	reg signed [15:0]i_input_data;
	reg i_output_ready;
	wire o_table_ready;
	wire o_input_ready;
	wire o_output_valid;
	wire signed [15:0]o_output_data;
	wire o_table_loaded;
	wire o_table_fault;

	reg [15:0]table_words [0:1023];
	reg signed [15:0]directed_inputs [0:6];
	reg signed [15:0]expected_queue [0:15];
	reg [511:0]control_before;
	reg [19:0]ram_before;
	reg accept_before;
	reg consume_before;
	reg table_transfer_before;
	reg table_restart_before;
	reg table_write_before;
	reg pipeline_frozen_before;
	reg [9:0]table_address_before;
	integer pending_before;
	integer table_expected_before;
	integer expected_pending;
	integer expected_table;
	integer valid_sum_after;
	integer error_count;
	integer accepted_count;
	integer received_count;
	integer observed_table_writes;
	integer stall_checks;
	integer simultaneous_checks;
	integer maximum_pending;
	integer lookup_minimum;
	integer lookup_maximum;
	integer lookup_zero_hits;
	integer lookup_endpoint_hits;
	integer index;
	integer timeout_count;
	reg scoreboard_enable;

	wire [511:0]control_state;
	assign control_state = {
		dut.cnt_table_expected, dut.cnt_pending,
		dut.reg_input_raw, dut.reg_input_quotient, dut.reg_input_remainder,
		dut.reg_round_raw, dut.reg_round_quotient, dut.reg_value_raw,
		dut.reg_rounded_value, dut.reg_address_raw, dut.reg_lookup_address,
		dut.reg_ram_raw, dut.reg_ram_address,
		dut.flag_input_valid, dut.flag_input_lower, dut.flag_input_upper,
		dut.flag_round_valid, dut.flag_round_lower, dut.flag_round_upper,
		dut.flag_round_above, dut.flag_round_tie, dut.flag_round_odd,
		dut.flag_value_valid, dut.flag_value_lower, dut.flag_value_upper,
		dut.flag_address_valid, dut.flag_address_lower, dut.flag_address_upper,
		dut.flag_ram_valid, dut.flag_ram_lower, dut.flag_ram_upper,
		dut.output_valid_o, dut.output_data_o, dut.table_loaded_o, dut.table_fault_o
	};

	silu_shared_unit dut
	(
		.i_clk(i_clk),
		.i_rstn(i_rstn),
		.i_table_valid(i_table_valid),
		.i_table_addr(i_table_addr),
		.i_table_data(i_table_data),
		.i_input_valid(i_input_valid),
		.i_input_data(i_input_data),
		.i_output_ready(i_output_ready),
		.o_table_ready(o_table_ready),
		.o_input_ready(o_input_ready),
		.o_output_valid(o_output_valid),
		.o_output_data(o_output_data),
		.o_table_loaded(o_table_loaded),
		.o_table_fault(o_table_fault)
	);

	function integer lookup_address;
		input signed [15:0]raw_value;
		integer quotient;
		integer remainder;
		begin
			quotient = raw_value >>> 2;
			remainder = raw_value & 3;
			lookup_address = quotient + 512;
			if((remainder == 3) || ((remainder == 2) && ((quotient & 1) == 1)))begin
				lookup_address = lookup_address + 1;
			end
		end
	endfunction

	function signed [15:0]expected_value;
		input signed [15:0]raw_value;
		integer address;
		begin
			address = lookup_address(raw_value);
			if(raw_value <= -16'sd2048)begin
				expected_value = 16'sd0;
			end else if(raw_value >= 16'sd2048)begin
				expected_value = raw_value;
			end else if(address == 1024)begin
				expected_value = 16'sd2047;
			end else begin
				expected_value = table_words[address];
			end
		end
	endfunction

	always #5 i_clk = ~i_clk;

	always@(posedge i_clk)begin
		pending_before = dut.cnt_pending;
		table_expected_before = dut.cnt_table_expected;
		accept_before = dut.flag_input_transfer;
		consume_before = dut.flag_output_transfer;
		table_transfer_before = dut.flag_table_transfer;
		table_restart_before = dut.flag_table_restart;
		table_write_before = dut.flag_table_write_enable;
		table_address_before = i_table_addr;
		pipeline_frozen_before = (i_rstn === 1'b1) && (dut.flag_pipeline_enable === 1'b0);
		control_before = control_state;
		ram_before = dut.wire_table_read_data;

		if(scoreboard_enable && accept_before)begin
			expected_queue[accepted_count] = expected_value(i_input_data);
			accepted_count = accepted_count + 1;
		end
		if(scoreboard_enable && consume_before)begin
			if(received_count >= accepted_count)begin
				$display("ASSERT_FAIL unexpected output transfer");
				error_count = error_count + 1;
			end else if(o_output_data !== expected_queue[received_count])begin
				$display("ASSERT_FAIL output order/data txn=%0d got=%0d expected=%0d", received_count, $signed(o_output_data), $signed(expected_queue[received_count]));
				error_count = error_count + 1;
			end
			received_count = received_count + 1;
		end
		if(table_write_before)begin
			observed_table_writes = observed_table_writes + 1;
			if((table_address_before != 0) && (table_address_before != table_expected_before[9:0]))begin
				$display("ASSERT_FAIL illegal table address wrote physical RAM address=%0d expected=%0d", table_address_before, table_expected_before);
				error_count = error_count + 1;
			end
		end

		#1;
		if(i_rstn === 1'b0)begin
			if((dut.cnt_pending !== 3'd0) || (dut.cnt_table_expected !== 11'd0))begin
				$display("ASSERT_FAIL reset did not cancel counters");
				error_count = error_count + 1;
			end
		end else begin
			expected_pending = pending_before + accept_before - consume_before;
			if(dut.cnt_pending !== expected_pending[2:0])begin
				$display("ASSERT_FAIL pending conservation before=%0d accept=%0d consume=%0d after=%0d", pending_before, accept_before, consume_before, dut.cnt_pending);
				error_count = error_count + 1;
			end

			valid_sum_after = dut.flag_input_valid;
			valid_sum_after = valid_sum_after + dut.flag_round_valid;
			valid_sum_after = valid_sum_after + dut.flag_value_valid;
			valid_sum_after = valid_sum_after + dut.flag_address_valid;
			valid_sum_after = valid_sum_after + dut.flag_ram_valid;
			valid_sum_after = valid_sum_after + dut.output_valid_o;
			if(dut.cnt_pending !== valid_sum_after[2:0])begin
				$display("ASSERT_FAIL pending=%0d differs from six valid stages=%0d", dut.cnt_pending, valid_sum_after);
				error_count = error_count + 1;
			end
			if(dut.cnt_pending > 3'd6)begin
				$display("ASSERT_FAIL pending exceeded real six-stage capacity value=%0d", dut.cnt_pending);
				error_count = error_count + 1;
			end
			if(dut.cnt_pending > maximum_pending)begin
				maximum_pending = dut.cnt_pending;
			end
			if(accept_before && consume_before)begin
				simultaneous_checks = simultaneous_checks + 1;
				if(dut.cnt_pending !== pending_before[2:0])begin
					$display("ASSERT_FAIL simultaneous input/output changed pending");
					error_count = error_count + 1;
				end
			end

			if(table_restart_before)begin
				expected_table = 1;
			end else if(table_transfer_before)begin
				if((table_address_before != table_expected_before[9:0]) || (table_address_before == 1023))begin
					expected_table = 0;
				end else begin
					expected_table = table_expected_before + 1;
				end
			end else begin
				expected_table = table_expected_before;
			end
			if(dut.cnt_table_expected !== expected_table[10:0])begin
				$display("ASSERT_FAIL table_expected before=%0d address=%0d after=%0d expected=%0d", table_expected_before, table_address_before, dut.cnt_table_expected, expected_table);
				error_count = error_count + 1;
			end
			if(dut.cnt_table_expected > 11'd1023)begin
				$display("ASSERT_FAIL table_expected reached forbidden 1024 state value=%0d", dut.cnt_table_expected);
				error_count = error_count + 1;
			end

			if(dut.flag_address_valid)begin
				if(($signed(dut.reg_lookup_address) < -7680) || ($signed(dut.reg_lookup_address) > 8704))begin
					$display("ASSERT_FAIL full signed lookup range value=%0d", $signed(dut.reg_lookup_address));
					error_count = error_count + 1;
				end
				if((~dut.flag_address_lower) && (~dut.flag_address_upper) && (($signed(dut.reg_lookup_address) < 0) || ($signed(dut.reg_lookup_address) > 1024)))begin
					$display("ASSERT_FAIL central lookup range value=%0d", $signed(dut.reg_lookup_address));
					error_count = error_count + 1;
				end
				if($signed(dut.reg_lookup_address) < lookup_minimum) lookup_minimum = $signed(dut.reg_lookup_address);
				if($signed(dut.reg_lookup_address) > lookup_maximum) lookup_maximum = $signed(dut.reg_lookup_address);
				if($signed(dut.reg_lookup_address) == 0) lookup_zero_hits = lookup_zero_hits + 1;
				if($signed(dut.reg_lookup_address) == 1024) lookup_endpoint_hits = lookup_endpoint_hits + 1;
			end

			if(pipeline_frozen_before)begin
				stall_checks = stall_checks + 1;
				if(control_state !== control_before)begin
					$display("ASSERT_FAIL pipeline state changed during stall");
					error_count = error_count + 1;
				end
				if(dut.wire_table_read_data !== ram_before)begin
					$display("ASSERT_FAIL official RAM output changed during CEA stall");
					error_count = error_count + 1;
				end
			end
		end
	end

	task drive_table_word;
		input [9:0]address;
		input [15:0]data;
		begin
			@(negedge i_clk);
			i_table_valid = 1'b1;
			i_table_addr = address;
			i_table_data = data;
			#1;
			if(o_table_ready !== 1'b1)begin
				$display("ASSERT_FAIL table transfer not accepted address=%0d", address);
				error_count = error_count + 1;
			end
			@(posedge i_clk);
			#2;
			i_table_valid = 1'b0;
		end
	endtask

	task load_complete_table;
		integer table_index;
		begin
			for(table_index = 0; table_index < 1024; table_index = table_index + 1)begin
				drive_table_word(table_index[9:0], table_words[table_index]);
			end
			if((o_table_loaded !== 1'b1) || (o_table_fault !== 1'b0))begin
				$display("ASSERT_FAIL complete table load loaded=%b fault=%b", o_table_loaded, o_table_fault);
				error_count = error_count + 1;
			end
		end
	endtask

	initial begin
		i_clk = 1'b0;
		i_rstn = 1'b0;
		i_table_valid = 1'b0;
		i_table_addr = 10'd0;
		i_table_data = 16'sd0;
		i_input_valid = 1'b0;
		i_input_data = 16'sd0;
		i_output_ready = 1'b1;
		o_test_done = 1'b0;
		error_count = 0;
		accepted_count = 0;
		received_count = 0;
		observed_table_writes = 0;
		stall_checks = 0;
		simultaneous_checks = 0;
		maximum_pending = 0;
		lookup_minimum = 32767;
		lookup_maximum = -32768;
		lookup_zero_hits = 0;
		lookup_endpoint_hits = 0;
		scoreboard_enable = 1'b0;

		directed_inputs[0] = -16'sd32768;
		directed_inputs[1] = -16'sd2047;
		directed_inputs[2] = -16'sd2046;
		directed_inputs[3] = 16'sd0;
		directed_inputs[4] = 16'sd2046;
		directed_inputs[5] = 16'sd2048;
		directed_inputs[6] = 16'sd32767;
		$readmemh("../../v4_silu_regression_20261005/frozen_data/silu_table.hex", table_words);

		repeat(4) @(posedge i_clk);
		@(negedge i_clk);
		i_rstn = 1'b1;
		load_complete_table;

		scoreboard_enable = 1'b1;
		@(negedge i_clk);
		i_output_ready = 1'b0;
		i_input_valid = 1'b1;
		for(index = 0; index < 6; index = index + 1)begin
			i_input_data = directed_inputs[index];
			@(posedge i_clk);
			#2;
			@(negedge i_clk);
		end
		i_input_valid = 1'b0;
		#1;
		if((dut.cnt_pending !== 3'd6) || (o_output_valid !== 1'b1))begin
			$display("ASSERT_FAIL six-stage fill pending=%0d output_valid=%b", dut.cnt_pending, o_output_valid);
			error_count = error_count + 1;
		end
		if(o_table_ready !== 1'b0)begin
			$display("ASSERT_FAIL reload opened with six pending transactions");
			error_count = error_count + 1;
		end
		repeat(4)begin
			@(posedge i_clk);
			#2;
		end

		@(negedge i_clk);
		i_input_valid = 1'b1;
		i_input_data = directed_inputs[6];
		i_output_ready = 1'b1;
		#1;
		if((o_input_ready !== 1'b1) || (o_output_valid !== 1'b1))begin
			$display("ASSERT_FAIL simultaneous transfer setup missing");
			error_count = error_count + 1;
		end
		@(posedge i_clk);
		#2;
		if(dut.cnt_pending !== 3'd6)begin
			$display("ASSERT_FAIL pending changed on simultaneous transfer value=%0d", dut.cnt_pending);
			error_count = error_count + 1;
		end
		@(negedge i_clk);
		i_input_valid = 1'b0;

		timeout_count = 0;
		while((received_count < 7) && (timeout_count < 40))begin
			@(posedge i_clk);
			#2;
			timeout_count = timeout_count + 1;
		end
		if((accepted_count != 7) || (received_count != 7) || (dut.cnt_pending != 0))begin
			$display("ASSERT_FAIL directed conservation accepted=%0d received=%0d pending=%0d", accepted_count, received_count, dut.cnt_pending);
			error_count = error_count + 1;
		end
		scoreboard_enable = 1'b0;

		drive_table_word(10'd0, table_words[0]);
		drive_table_word(10'd2, table_words[2]);
		if((o_table_fault !== 1'b1) || (dut.cnt_table_expected !== 11'd0))begin
			$display("ASSERT_FAIL wrong-order table negative did not fail closed");
			error_count = error_count + 1;
		end else begin
			$display("TB_EXPECTED_NEGATIVE wrong_order_address=2 physical_write_suppressed=1");
		end
		drive_table_word(10'd0, table_words[0]);
		for(index = 1; index < 1024; index = index + 1)begin
			drive_table_word(index[9:0], table_words[index]);
		end

		@(negedge i_clk);
		i_output_ready = 1'b0;
		i_input_valid = 1'b1;
		for(index = 0; index < 3; index = index + 1)begin
			i_input_data = directed_inputs[index + 2];
			@(posedge i_clk);
			#2;
			@(negedge i_clk);
		end
		i_input_valid = 1'b0;
		if(dut.cnt_pending !== 3'd3)begin
			$display("ASSERT_FAIL reset-cancel setup pending=%0d", dut.cnt_pending);
			error_count = error_count + 1;
		end
		i_rstn = 1'b0;
		#2;
		if((dut.cnt_pending !== 3'd0) || (o_output_valid !== 1'b0) || (o_table_loaded !== 1'b0))begin
			$display("ASSERT_FAIL asynchronous reset did not cancel in-flight transactions");
			error_count = error_count + 1;
		end

		if(maximum_pending != 6)begin
			$display("ASSERT_FAIL maximum pending=%0d expected=6", maximum_pending);
			error_count = error_count + 1;
		end
		if((simultaneous_checks < 1) || (stall_checks < 4))begin
			$display("ASSERT_FAIL transfer coverage simultaneous=%0d stalls=%0d", simultaneous_checks, stall_checks);
			error_count = error_count + 1;
		end
		if((lookup_minimum != -7680) || (lookup_maximum != 8704) || (lookup_zero_hits < 1) || (lookup_endpoint_hits < 1))begin
			$display("ASSERT_FAIL lookup coverage min=%0d max=%0d addr0=%0d endpoint1024=%0d", lookup_minimum, lookup_maximum, lookup_zero_hits, lookup_endpoint_hits);
			error_count = error_count + 1;
		end
		if(observed_table_writes != 2049)begin
			$display("ASSERT_FAIL legal table writes=%0d expected=2049", observed_table_writes);
			error_count = error_count + 1;
		end

		o_test_done = 1'b1;
		if(error_count == 0)begin
			$display("TB_PASS_SEMANTIC pending_capacity=6 table_expected_max=1023 legal_write_range=0..1023 lookup_full=-7680..8704 lookup_central=0..1024 endpoint1024_special=1");
		end else begin
			$display("TB_FAIL_SEMANTIC errors=%0d", error_count);
		end
		$finish;
	end

	initial begin
		#500000;
		if(o_test_done !== 1'b1)begin
			$display("TB_FAIL_SEMANTIC timeout");
			$finish;
		end
	end

endmodule
