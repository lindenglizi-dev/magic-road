`timescale 1ns / 1ps

// 直接比较已上板程序，随机停顿和半程复位不由候选逻辑计算期望值。
module tb_frontend_load_sequence;
	reg clk = 0;
	reg rstn = 0;
	reg fetch = 0;
	reg advance = 0;
	reg [15:0]reg_random = 16'hace1;
	reg [63:0]reg_expected[0:8191];
	reg [63:0]reg_held = 0;
	wire [63:0]command;
	integer pass;
	integer index;
	integer delay;
	integer checks = 0;
	integer holds = 0;
	always #5 clk = ~clk;
	always@(posedge clk)begin
		reg_random <= {reg_random[14:0],reg_random[15]^reg_random[13]^reg_random[12]^reg_random[10]};
	end
	road_frontend_load_sequence dut(.i_clk(clk),.i_rstn(rstn),.i_fetch(fetch),.i_advance(advance),.o_command(command));
	initial begin
		$readmemh("program.hex",reg_expected);
		for(pass=0;pass<3;pass=pass+1)begin
			@(negedge clk); rstn = 0; fetch = 0; advance = 0;
			#1;
			if(command !== 64'd0)begin $fatal(1,"LOOP_RESET_OUTPUT_NOT_CANCELLED"); end
			repeat(3)begin @(negedge clk); end
			rstn = 1;
			for(index=0;index<(pass==0 ? 5520 : 6092);index=index+1)begin
				@(negedge clk); fetch = 1;
				@(posedge clk); #1;
				if(command !== reg_expected[index])begin
					$fatal(1,"LOOP_COMMAND_MISMATCH pass=%0d index=%0d actual=%h expected=%h",pass,index,command,reg_expected[index]);
				end
				checks = checks + 1;
				reg_held = command;
				@(negedge clk); fetch = 0;
				delay = pass==1 ? 2 : 2+reg_random[2:0];
				if(index==1506 || index==6079)begin delay = 512; end
				repeat(delay)begin
					@(posedge clk); #1;
					if(command !== reg_held)begin $fatal(1,"LOOP_HOLD_MISMATCH index=%0d",index); end
					holds = holds + 1;
				end
				if(index!=6091)begin
					@(negedge clk); advance = 1;
					@(posedge clk); #1;
					if(command !== reg_held)begin $fatal(1,"ADVANCE_CHANGED_COMMAND_BEFORE_FETCH"); end
					@(negedge clk); advance = 0;
				end
			end
		end
		$display("LOOP_COMMAND_PASS comparisons=%0d holds=%0d full_runs=2 reset_mid_parameter=1",checks,holds);
		$finish;
	end
endmodule
