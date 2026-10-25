`timescale 1ns / 1ps

// 实际调度器的取指存储测试；不把强制状态下的PASS当CNN通过。
module tb_program_banks;
	reg clk = 0;
	reg rstn = 0;
	reg [12:0] address = 0;
	reg [63:0] expected[0:8191];
	reg [63:0] held;
	integer index;
	integer count = 0;
	always #5 clk = ~clk;
	road_stem_ddr_sequence dut(
		.i_clk(clk),.i_rstn(rstn),.i_phy_ready(1'b0),.i_ddr_fault(1'b0),
		.i_req_ready(1'b0),.i_rsp_valid(1'b0),.i_rsp_data(128'd0),.i_rsp_error(4'd0),
		.o_req_valid(),.o_req_write(),.o_req_addr(),.o_req_data(),.o_rsp_ready(),
		.o_status(),.o_error(),.o_phase(),.o_writes(),.o_reads(),.o_output_bytes(),
		.o_cycles(),.o_cycle_bins(),.o_address(),.o_expected(),.o_actual()
	);
	initial begin
		$readmemh("program.hex",expected);
		#31;
		rstn = 1;
		force dut.cnt_program = address;
		for(index=0;index<8192;index=index+1)begin
			@(negedge clk);
			address = index;
			force dut.state_current = 5'd1;
			@(posedge clk);
			#1;
			if(dut.reg_command !== expected[index])begin
				$fatal(1,"BANK_WORD_MISMATCH address=%0d",index);
			end
			if(dut.flag_command_bank !== address[12])begin
				$fatal(1,"BANK_SELECT_NOT_ALIGNED address=%0d",index);
			end
			held = dut.reg_command;
			count = count + 1;
			@(negedge clk);
			force dut.state_current = 5'd0;
			address = address ^ 13'h1000;
			repeat(2)begin
				@(posedge clk);
				#1;
				if(dut.reg_command !== held)begin
					$fatal(1,"COMMAND_CHANGED_OUTSIDE_FETCH address=%0d",index);
				end
			end
		end
		release dut.cnt_program;
		release dut.state_current;
		@(negedge clk);
		rstn = 0;
		#1;
		if(dut.o_req_valid !== 1'b0 || dut.o_rsp_ready !== 1'b0)begin
			$fatal(1,"RESET_DID_NOT_CANCEL_TRANSPORT");
		end
		$display("PROGRAM_BANKS_PASS words=%0d hold_checks=%0d latency_change=0",count,count*2);
		$finish;
	end
endmodule
