`timescale 1ns/1ps

// Icarus-only stand-in for the encrypted vendor simulation model.
module PH1P_LOGIC_ERAM #(
    parameter DATA_WIDTH_A = 20,
    parameter DATA_WIDTH_B = DATA_WIDTH_A,
    parameter ADDR_WIDTH_A = 10,
    parameter ADDR_WIDTH_B = ADDR_WIDTH_A,
    parameter DATA_DEPTH_A = 1024,
    parameter DATA_DEPTH_B = DATA_DEPTH_A,
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
    parameter FORCE_KEEP = "OFF",
    parameter INIT_FILE = "NONE",
    parameter FILL_ALL = "NONE",
    parameter IMPLEMENT = "20K"
) (
    input  wire [DATA_WIDTH_A-1:0] dia,
    input  wire [ADDR_WIDTH_A-1:0] addra,
    input  wire cea,
    input  wire ocea,
    input  wire clka,
    input  wire wea,
    input  wire rsta,
    input  wire [BYTE_A-1:0] bea,
    input  wire [DATA_WIDTH_B-1:0] dib,
    input  wire [ADDR_WIDTH_B-1:0] addrb,
    input  wire ceb,
    input  wire oceb,
    input  wire clkb,
    input  wire web,
    input  wire rstb,
    input  wire [BYTE_B-1:0] beb,
    input  wire ecc_sbiterrinj,
    input  wire ecc_dbiterrinj,
    output reg  [DATA_WIDTH_A-1:0] doa,
    output wire [DATA_WIDTH_B-1:0] dob,
    output wire ecc_sbiterr,
    output wire ecc_dbiterr
);

    reg [DATA_WIDTH_A-1:0] memory [0:DATA_DEPTH_A-1];

    assign dob = {DATA_WIDTH_B{1'b0}};
    assign ecc_sbiterr = 1'b0;
    assign ecc_dbiterr = 1'b0;

    initial begin
        doa = {DATA_WIDTH_A{1'b0}};
        $readmemh(INIT_FILE, memory);
    end

    always @(posedge clka or posedge rsta) begin
        if (rsta)
            doa <= {DATA_WIDTH_A{1'b0}};
        else if (cea)
            doa <= memory[addra];
    end

endmodule
