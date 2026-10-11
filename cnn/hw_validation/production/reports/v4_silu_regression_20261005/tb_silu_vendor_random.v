`timescale 1ns / 1ps

module tb_silu_vendor_random;

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
	reg [15:0] random_state;
	integer accepted_count;
	integer received_count;
	integer error_count;
	integer stall_cycle_count;
	integer consecutive_stalls;
	integer maximum_stalls;
	integer cycle_count;
	integer index;

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

	always #5 i_clk = ~i_clk;

	always@(posedge i_clk)begin
		cycle_count = cycle_count + 1;
		if((i_table_valid === 1'b1) && (o_table_ready === 1'b1) && (dut.flag_pipeline_enable !== 1'b1))begin
			$display("TB_ERROR table transfer occurred while RAM enable was low address=%0d", i_table_addr);
			error_count = error_count + 1;
		end
		if((i_input_valid === 1'b1) && (o_input_ready === 1'b1))begin
			accepted_count = accepted_count + 1;
		end
		if((o_output_valid === 1'b1) && (i_output_ready === 1'b1))begin
			if(o_output_data !== expected_words[received_count + 30720])begin
				$display("TB_MISMATCH cycle=%0d txn=%0d raw=%0d got=%0d expected=%0d", cycle_count, received_count, received_count - 2048, $signed(o_output_data), $signed(expected_words[received_count + 30720]));
				error_count = error_count + 1;
			end
			received_count = received_count + 1;
		end
		if((o_output_valid === 1'b1) && (i_output_ready === 1'b0))begin
			stall_cycle_count = stall_cycle_count + 1;
			consecutive_stalls = consecutive_stalls + 1;
			if(consecutive_stalls > maximum_stalls) maximum_stalls = consecutive_stalls;
		end else begin
			consecutive_stalls = 0;
		end
	end

	initial begin
		i_clk = 1'b0;
		i_rstn = 1'b0;
		i_table_valid = 1'b0;
		i_table_addr = 10'd0;
		i_table_data = 16'sd0;
		i_input_valid = 1'b0;
		i_input_data = -16'sd2048;
		i_output_ready = 1'b1;
		random_state = 16'h002a;
		accepted_count = 0;
		received_count = 0;
		error_count = 0;
		stall_cycle_count = 0;
		consecutive_stalls = 0;
		maximum_stalls = 0;
		cycle_count = 0;

		$readmemh("../../silu/generated/silu_table.hex", table_words);
		$readmemh("../../silu/generated/silu_expected.hex", expected_words);
		#70;
		@(negedge i_clk);
		i_rstn = 1'b1;
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

		i_input_valid = 1'b1;
		while((received_count < 4096) && (cycle_count < 20000))begin
			@(negedge i_clk);
			random_state = {random_state[14:0], random_state[15] ^ random_state[13] ^ random_state[12] ^ random_state[10]};
			i_output_ready = random_state[0] | random_state[2];
			if(accepted_count < 4096)begin
				i_input_valid = 1'b1;
				i_input_data = accepted_count - 2048;
			end else begin
				i_input_valid = 1'b0;
			end
		end
		@(negedge i_clk);
		i_input_valid = 1'b0;
		i_output_ready = 1'b1;
		if((accepted_count != 4096) || (received_count != 4096))begin
			$display("TB_ERROR conservation accepted=%0d received=%0d", accepted_count, received_count);
			error_count = error_count + 1;
		end
		if(error_count == 0)begin
			$display("TB_PASS_RANDOM seed=42 inputs=4096 accepted=%0d received=%0d stall_cycles=%0d max_stall=%0d", accepted_count, received_count, stall_cycle_count, maximum_stalls);
		end else begin
			$display("TB_FAIL_RANDOM seed=42 accepted=%0d received=%0d errors=%0d", accepted_count, received_count, error_count);
		end
		$finish;
	end

endmodule
