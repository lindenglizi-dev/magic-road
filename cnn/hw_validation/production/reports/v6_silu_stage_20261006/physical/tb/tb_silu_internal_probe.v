`timescale 1ns / 1ps

module tb_silu_internal_probe();
	reg i_clk = 1'b0;
	reg i_rstn = 1'b0;
	wire o_done;
	wire o_error;
	wire [2:0]o_phase;
	wire [5:0]o_result_count;
	wire [31:0]o_checksum;
	integer stall_cycles = 0;

	silu_internal_probe silu_internal_probe_Inst_dut(
		.i_clk(i_clk),
		.i_rstn(i_rstn),
		.o_done(o_done),
		.o_error(o_error),
		.o_phase(o_phase),
		.o_result_count(o_result_count),
		.o_checksum(o_checksum)
	);

	always #5 i_clk = ~i_clk;

	always@(posedge i_clk)begin
		if(silu_internal_probe_Inst_dut.wire_output_valid &&
		   !silu_internal_probe_Inst_dut.reg_output_ready)begin
			stall_cycles = stall_cycles + 1;
		end
	end

	initial begin
		#200000;
		$display("FAIL timeout phase=%0d table=%0d input=%0d result=%0d",
		         o_phase,
		         silu_internal_probe_Inst_dut.cnt_table,
		         silu_internal_probe_Inst_dut.cnt_input,
		         o_result_count);
		$finish_and_return(1);
	end

	initial begin
		repeat(4) @(negedge i_clk);
		i_rstn = 1'b1;
		wait(o_done == 1'b1);
		@(posedge i_clk);
		#1;
		if(o_error !== 1'b0 || o_result_count !== 6'd18 ||
		   o_checksum !== 32'h00001E01 ||
		   silu_internal_probe_Inst_dut.cnt_table !== 11'd1024 ||
		   silu_internal_probe_Inst_dut.cnt_input !== 6'd18 ||
		   stall_cycles == 0)begin
			$display("FAIL error=%b results=%0d checksum=%h table=%0d input=%0d stalls=%0d",
			         o_error, o_result_count, o_checksum,
			         silu_internal_probe_Inst_dut.cnt_table,
			         silu_internal_probe_Inst_dut.cnt_input,
			         stall_cycles);
			$finish_and_return(1);
		end
		$display("PASS table_writes=%0d inputs=%0d results=%0d stalls=%0d checksum=%h",
		         silu_internal_probe_Inst_dut.cnt_table,
		         silu_internal_probe_Inst_dut.cnt_input,
		         o_result_count, stall_cycles, o_checksum);
		$finish;
	end
endmodule
