`timescale 1ns / 1ps

// Icarus-only behavioral model of the exact PH1P_LOGIC_ERAM public interface.
// It models synchronous A/B-port read and runtime write behavior; it does not
// initialize or reset the storage array and is never synthesis evidence.
module PH1P_LOGIC_ERAM #(
	parameter DATA_WIDTH_A = 20,
	parameter DATA_WIDTH_B = DATA_WIDTH_A,
	parameter ADDR_WIDTH_A = 10,
	parameter ADDR_WIDTH_B = ADDR_WIDTH_A,
	parameter DATA_DEPTH_A = 1024,
	parameter DATA_DEPTH_B = 1024,
	parameter BYTE_ENABLE = 0,
	parameter BYTE_A = 1,
	parameter BYTE_B = 1,
	parameter MODE = "DP",
	parameter REGMODE_A = "NOREG",
	parameter REGMODE_B = "NOREG",
	parameter WRITEMODE_A = "NORMAL",
	parameter WRITEMODE_B = "NORMAL",
	parameter RESETMODE_A = "ASYNC",
	parameter RESETMODE_B = "ASYNC",
	parameter OREGSET_A = "RESET",
	parameter OREGSET_B = "RESET",
	parameter SSROVERCE = "DISABLE",
	parameter ECC_DECODE = "DISABLE",
	parameter ECC_ENCODE = "DISABLE",
	parameter ASYNC_RESET_RELEASE_A = "ASYNC",
	parameter ASYNC_RESET_RELEASE_B = "ASYNC",
	parameter CLKMODE = "ASYNC",
	parameter DEBUGGABLE = "NO",
	parameter PACKABLE = "NO",
	parameter FORCE_KEEP = "ON",
	parameter INIT_FILE = "NONE",
	parameter FILL_ALL = "NONE",
	parameter IMPLEMENT = "20K"
)(
	input [DATA_WIDTH_A-1:0]dia,
	input [ADDR_WIDTH_A-1:0]addra,
	input cea,
	input ocea,
	input clka,
	input wea,
	input rsta,
	input [BYTE_A-1:0]bea,
	input [DATA_WIDTH_B-1:0]dib,
	input [ADDR_WIDTH_B-1:0]addrb,
	input ceb,
	input oceb,
	input clkb,
	input web,
	input rstb,
	input [BYTE_B-1:0]beb,
	input ecc_sbiterrinj,
	input ecc_dbiterrinj,
	output reg [DATA_WIDTH_A-1:0]doa,
	output reg [DATA_WIDTH_B-1:0]dob,
	output ecc_sbiterr,
	output ecc_dbiterr
);

	reg [DATA_WIDTH_A-1:0]memory_words[0:DATA_DEPTH_A-1];

	assign ecc_sbiterr = 1'b0;
	assign ecc_dbiterr = 1'b0;

	always@(posedge clka)begin
		if(cea)begin
			if(wea)begin
				memory_words[addra] <= dia;
			end
			doa <= memory_words[addra];
		end
	end

	always@(posedge clkb)begin
		if(ceb)begin
			if(web)begin
				memory_words[addrb] <= dib;
			end
			dob <= memory_words[addrb];
		end
	end

endmodule
