`timescale 1ns / 1ps

module tb_silu_vendor_stall;

	reg i_clk;
	reg i_rstn;
	reg i_table_valid;
	reg [9:0] i_table_addr;
	reg signed [15:0] i_table_data;
	reg i_input_valid;
	reg signed [15:0] i_input_data;
	reg i_output_ready;
	wire o_table_ready;
	wire o_input_ready;
	wire o_output_valid;
	wire signed [15:0] o_output_data;
	wire o_table_loaded;
	wire o_table_fault;

	reg [15:0] table_words [0:1023];
	reg [15:0] expected_words [0:65535];
	reg [15:0] expected_queue [0:31];
	reg signed [15:0] raw_queue [0:31];
	integer address_queue [0:31];
	reg signed [15:0] central_inputs [0:3];
	reg signed [15:0] boundary_inputs [0:4];
	reg [1023:0] trace_name;
	integer trace_file;
	integer stall_cycles;
	integer cycle_count;
	integer accepted_count;
	integer received_count;
	integer error_count;
	integer index;
	integer timeout_count;

	silu_shared_unit dut (
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
		input integer raw_value;
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

	always #5 i_clk = ~i_clk;

	always@(posedge i_clk)begin
		cycle_count = cycle_count + 1;
		if((i_input_valid === 1'b1) && (o_input_ready === 1'b1))begin
			expected_queue[accepted_count] = expected_words[$signed(i_input_data) + 32768];
			raw_queue[accepted_count] = i_input_data;
			address_queue[accepted_count] = lookup_address($signed(i_input_data));
			accepted_count = accepted_count + 1;
		end
		if((o_output_valid === 1'b1) && (i_output_ready === 1'b1))begin
			if(received_count >= accepted_count)begin
				$display("TB_ERROR unexpected output cycle=%0d data=%0d", cycle_count, $signed(o_output_data));
				error_count = error_count + 1;
			end else if(o_output_data !== expected_queue[received_count])begin
				$display("TB_MISMATCH stall=%0d cycle=%0d txn=%0d raw=%0d lookup=%0d got=%0d expected=%0d", stall_cycles, cycle_count, received_count, $signed(raw_queue[received_count]), address_queue[received_count], $signed(o_output_data), $signed(expected_queue[received_count]));
				error_count = error_count + 1;
			end
			received_count = received_count + 1;
		end
	end

	always@(negedge i_clk)begin
		if(trace_file != 0)begin
			$fwrite(trace_file, "%0d,%0t,%0d,%0d,%0d,%0d,%0d,%0d,%0h,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d\n",
				cycle_count, $time, i_input_valid, $signed(i_input_data), o_input_ready,
				dut.reg_lookup_address, dut.wire_table_address, dut.flag_address_valid,
				dut.wire_table_read_data, dut.reg_ram_address, dut.flag_ram_valid,
				dut.flag_ram_lower, dut.flag_ram_upper, dut.flag_pipeline_enable,
				o_output_valid, i_output_ready, $signed(o_output_data), received_count);
		end
	end

	initial begin
		i_clk = 1'b0;
		i_rstn = 1'b0;
		i_table_valid = 1'b0;
		i_table_addr = 10'd0;
		i_table_data = 16'sd0;
		i_input_valid = 1'b0;
		i_input_data = 16'sd0;
		i_output_ready = 1'b1;
		cycle_count = 0;
		accepted_count = 0;
		received_count = 0;
		error_count = 0;
		trace_file = 0;
		if(!$value$plusargs("STALL=%d", stall_cycles)) stall_cycles = 1;
		if(!$value$plusargs("TRACE=%s", trace_name)) trace_name = "cycle_trace.csv";
		trace_file = $fopen(trace_name, "w");
		$fwrite(trace_file, "cycle,time_ns,input_valid,input_data,input_ready,lookupaddr,ram_addr,addr_valid,ram_data,control_addr,control_valid,control_lower,control_upper,advance,output_valid,output_ready,output_data,received_count\n");

		$readmemh("../../silu/generated/silu_table.hex", table_words);
		$readmemh("../../silu/generated/silu_expected.hex", expected_words);
		central_inputs[0] = 16'sd0;
		central_inputs[1] = 16'sd4;
		central_inputs[2] = 16'sd8;
		central_inputs[3] = 16'sd12;
		boundary_inputs[0] = -16'sd2048;
		boundary_inputs[1] = -16'sd2047;
		boundary_inputs[2] = 16'sd2044;
		boundary_inputs[3] = 16'sd2046;
		boundary_inputs[4] = 16'sd2048;

		#70;
		@(negedge i_clk);
		i_rstn = 1'b1;
		i_input_valid = 1'b1;
		i_input_data = 16'sd4;
		#1;
		if(o_input_ready !== 1'b0)begin
			$display("TB_ERROR inference opened before complete table load");
			error_count = error_count + 1;
		end
		i_input_valid = 1'b0;

		// Load the complete production table through the full SiLU wrapper.
		i_table_valid = 1'b1;
		for(index = 0; index < 1024; index = index + 1)begin
			i_table_addr = index[9:0];
			i_table_data = table_words[index];
			#1;
			if(o_table_ready !== 1'b1)begin
				$display("TB_ERROR table ready low before address=%0d transfer", index);
				error_count = error_count + 1;
			end
			@(posedge i_clk);
			#1;
			@(negedge i_clk);
		end
		i_table_valid = 1'b0;
		if((o_table_loaded !== 1'b1) || (o_table_fault !== 1'b0))begin
			$display("TB_ERROR complete table load failed loaded=%b fault=%b", o_table_loaded, o_table_fault);
			error_count = error_count + 1;
		end

		// A/B/C/D are central-table samples with distinct addresses and values.
		i_output_ready = 1'b0;
		i_input_valid = 1'b1;
		for(index = 0; index < 4; index = index + 1)begin
			i_input_data = central_inputs[index];
			@(posedge i_clk);
			#1;
			if(o_input_ready !== 1'b1)begin
				$display("TB_ERROR central input not accepted index=%0d", index);
				error_count = error_count + 1;
			end
			@(negedge i_clk);
		end
		i_input_valid = 1'b0;
		wait(o_output_valid === 1'b1);
		i_table_valid = 1'b1;
		i_table_addr = 10'd0;
		#1;
		if((o_table_ready !== 1'b0) || (o_input_ready !== 1'b0))begin
			$display("TB_ERROR reload or input opened while samples were pending");
			error_count = error_count + 1;
		end
		i_table_valid = 1'b0;
		repeat(stall_cycles) @(posedge i_clk);
		@(negedge i_clk);
		i_output_ready = 1'b1;
		timeout_count = 0;
		while((received_count < 4) && (timeout_count < 100))begin
			@(posedge i_clk);
			timeout_count = timeout_count + 1;
		end
		if(received_count != 4)begin
			$display("TB_ERROR central sequence timed out accepted=%0d received=%0d", accepted_count, received_count);
			error_count = error_count + 1;
		end
		@(negedge i_clk);
		i_table_addr = 10'd0;
		#1;
		if(o_table_ready !== 1'b1)begin
			$display("TB_ERROR reload did not open after pending samples drained");
			error_count = error_count + 1;
		end
		i_table_addr = 10'd1023;

		// Exercise lower bypass, table address 0, table address 1023, address 1024, and upper bypass.
		@(negedge i_clk);
		i_input_valid = 1'b1;
		for(index = 0; index < 5; index = index + 1)begin
			i_input_data = boundary_inputs[index];
			@(posedge i_clk);
			#1;
			if(o_input_ready !== 1'b1)begin
				$display("TB_ERROR boundary input not accepted index=%0d", index);
				error_count = error_count + 1;
			end
			@(negedge i_clk);
		end
		i_input_valid = 1'b0;
		timeout_count = 0;
		while((received_count < 9) && (timeout_count < 100))begin
			@(posedge i_clk);
			timeout_count = timeout_count + 1;
		end
		if(received_count != 9)begin
			$display("TB_ERROR boundary sequence timed out accepted=%0d received=%0d", accepted_count, received_count);
			error_count = error_count + 1;
		end

		@(negedge i_clk);
		$fclose(trace_file);
		if(error_count == 0)begin
			$display("TB_PASS stall=%0d accepted=%0d received=%0d errors=0", stall_cycles, accepted_count, received_count);
		end else begin
			$display("TB_FAIL stall=%0d accepted=%0d received=%0d errors=%0d", stall_cycles, accepted_count, received_count, error_count);
		end
		$finish;
	end

endmodule
