`timescale 1ns / 1ps

module tb_silu_shared_unit;

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
	reg [15:0]expected_words [0:65535];
	reg [15:0]held_output;
	integer cycle_count;
	integer sent_count;
	integer received_count;
	integer first_accept_cycle;
	integer first_output_cycle;
	integer error_count;
	integer index;
	integer unloaded_output_errors;
	integer observed_table_writes;

	silu_shared_unit silu_shared_unit_Inst_dut(
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
		cycle_count <= cycle_count + 1;
		if((i_rstn === 1'b1) && (o_table_loaded === 1'b0) && (o_output_valid !== 1'b0))begin
			$display("TB_ERROR stale output while table invalid after reset or reload");
			unloaded_output_errors = unloaded_output_errors + 1;
		end
		if(silu_shared_unit_Inst_dut.flag_table_write_enable === 1'b1)begin
			observed_table_writes = observed_table_writes + 1;
			if((observed_table_writes < 4) || (i_table_addr == 0) || (i_table_addr == 1023))begin
				$display("TB_LOAD_WRITE cycle=%0d count=%0d address=%0d pending=%0d", cycle_count, observed_table_writes, i_table_addr, silu_shared_unit_Inst_dut.cnt_pending);
			end
			if(silu_shared_unit_Inst_dut.flag_pipeline_enable !== 1'b1)begin
				$display("TB_ERROR legal table write while CEA disabled");
				unloaded_output_errors = unloaded_output_errors + 1;
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
			#1;                                 // 先让地址相关ready组合更新，避免重复接收地址零
			while(o_table_ready !== 1'b1)begin
				@(negedge i_clk);
			end
			@(posedge i_clk);
			#1;
			i_table_valid = 1'b0;
		end
	endtask

	task load_complete_table;
		integer table_index;
		begin
			for(table_index = 0; table_index < 1024; table_index = table_index + 1)begin
				drive_table_word(table_index[9:0], table_words[table_index]);
			end
			if(o_table_loaded !== 1'b1)begin
				$display("TB_ERROR table did not become loaded");
				error_count = error_count + 1;
			end
			if(o_table_fault !== 1'b0)begin
				$display("TB_ERROR load fault remained after complete image");
				error_count = error_count + 1;
			end
		end
	endtask

	task send_sample;
		input [15:0]data;
		begin
			@(negedge i_clk);
			i_input_valid = 1'b1;
			i_input_data = data;
			while(o_input_ready !== 1'b1)begin
				@(negedge i_clk);
			end
			@(posedge i_clk);
			#1;
			i_input_valid = 1'b0;
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
		cycle_count = 0;
		sent_count = 0;
		received_count = 0;
		first_accept_cycle = -1;
		first_output_cycle = -1;
		error_count = 0;
		unloaded_output_errors = 0;
		observed_table_writes = 0;

		$readmemh("frozen_data/silu_table.hex", table_words);
		$readmemh("frozen_data/silu_expected.hex", expected_words);

		repeat(3) @(posedge i_clk);
		@(negedge i_clk);
		i_rstn = 1'b1;
		@(posedge i_clk);
		#1;
		if(o_input_ready !== 1'b0 || o_table_loaded !== 1'b0)begin
			$display("TB_ERROR inference opened before table load");
			error_count = error_count + 1;
		end

		// An unexpected first address must fault without writing or enabling inference.
		drive_table_word(10'd5, table_words[5]);
		if(o_table_fault !== 1'b1 || o_table_loaded !== 1'b0)begin
			$display("TB_ERROR illegal load order was not fail-closed");
			error_count = error_count + 1;
		end
		load_complete_table;

		// Hold one visible result for three cycles and require stable valid/data.
		i_output_ready = 1'b0;
		send_sample(16'hf801);
		while(o_output_valid !== 1'b1)begin
			@(posedge i_clk);
			#1;
		end
		held_output = o_output_data;
		if(held_output !== expected_words[30721])begin
			$display("TB_ERROR directed -2047 result mismatch");
			error_count = error_count + 1;
		end
		repeat(3)begin
			@(posedge i_clk);
			#1;
			if(o_output_valid !== 1'b1 || o_output_data !== held_output || o_input_ready !== 1'b0)begin
				$display("TB_ERROR output or pipeline changed under backpressure");
				error_count = error_count + 1;
			end
		end
		@(negedge i_clk);
		i_output_ready = 1'b1;
		@(posedge i_clk);
		#1;

		// A new address-zero image waits until a pending result drains.
		send_sample(16'h0002);
		@(negedge i_clk);
		i_table_valid = 1'b1;
		i_table_addr = 10'd0;
		i_table_data = table_words[0];
		if(o_table_ready !== 1'b0)begin
			$display("TB_ERROR reload accepted with a pending sample");
			error_count = error_count + 1;
		end
		while(o_table_ready !== 1'b1)begin
			@(negedge i_clk);
		end
		@(posedge i_clk);
		#1;
		i_table_valid = 1'b0;
		if(o_table_loaded !== 1'b0 || o_input_ready !== 1'b0)begin
			$display("TB_ERROR address-zero restart did not close inference");
			error_count = error_count + 1;
		end
		for(index = 1; index < 1024; index = index + 1)begin
			drive_table_word(index[9:0], table_words[index]);
		end

		// Reset cancels a sample, invalidates metadata, and requires another full load.
		send_sample(16'h0100);
		@(negedge i_clk);
		i_rstn = 1'b0;
		repeat(2) @(posedge i_clk);
		#1;
		if(o_output_valid !== 1'b0 || o_table_loaded !== 1'b0 || o_input_ready !== 1'b0)begin
			$display("TB_ERROR reset did not cancel pipeline and loaded state");
			error_count = error_count + 1;
		end
		@(negedge i_clk);
		i_rstn = 1'b1;
		load_complete_table;

		// Stream every signed code with no downstream stall.
		@(negedge i_clk);
		i_output_ready = 1'b1;
		i_input_valid = 1'b1;
		i_input_data = 16'sh8000;
		sent_count = 0;
		received_count = 0;
		first_accept_cycle = -1;
		first_output_cycle = -1;
		while(received_count < 65536)begin
			@(posedge i_clk);
			#1;
			if((sent_count < 65536) && (o_input_ready !== 1'b1))begin
				$display("TB_ERROR unexpected input bubble at sent=%0d", sent_count);
				error_count = error_count + 1;
			end
			if((i_input_valid == 1'b1) && (o_input_ready == 1'b1))begin
				if(first_accept_cycle < 0)begin
					first_accept_cycle = cycle_count;
				end
				sent_count = sent_count + 1;
				if(sent_count < 65536)begin
					i_input_data = sent_count - 32768;
				end else begin
					i_input_valid = 1'b0;
				end
			end
			if((o_output_valid == 1'b1) && (i_output_ready == 1'b1))begin
				if(first_output_cycle < 0)begin
					first_output_cycle = cycle_count;
				end
				if(o_output_data !== expected_words[received_count])begin
					$display("TB_ERROR exhaustive mismatch raw=%0d got=%0d expected=%0d", received_count - 32768, $signed(o_output_data), $signed(expected_words[received_count]));
					error_count = error_count + 1;
				end
				received_count = received_count + 1;
			end
		end

		if((first_output_cycle - first_accept_cycle) != 5)begin
			$display("TB_ERROR measured latency=%0d expected=5", first_output_cycle - first_accept_cycle);
			error_count = error_count + 1;
		end
		if(sent_count != 65536 || received_count != 65536)begin
			$display("TB_ERROR conservation sent=%0d received=%0d", sent_count, received_count);
			error_count = error_count + 1;
		end

		if((error_count == 0) && (unloaded_output_errors == 0) && (observed_table_writes == 3072))begin
			$display("TB_PASS inputs=65536 latency=5 ii=1 table_words=1024 legal_writes=%0d stale_output_errors=%0d", observed_table_writes, unloaded_output_errors);
		end else begin
			$display("TB_FAIL errors=%0d legal_writes=%0d stale_output_errors=%0d", error_count, observed_table_writes, unloaded_output_errors);
		end
		$finish;
	end

endmodule
