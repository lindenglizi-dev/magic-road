// Minimal behavioral model for road-vision unit tests only.
module PH1P_LOGIC_ERAM #(
    parameter DATA_WIDTH_A=8, DATA_WIDTH_B=8,
    parameter ADDR_WIDTH_A=11, ADDR_WIDTH_B=11,
    parameter DATA_DEPTH_A=2048, DATA_DEPTH_B=2048,
    parameter MODE="DP", REGMODE_A="NOREG", REGMODE_B="NOREG",
    parameter WRITEMODE_A="NORMAL", WRITEMODE_B="NORMAL",
    parameter IMPLEMENT="20K(FAST)", ECC_ENCODE="DISABLE",
    parameter ECC_DECODE="DISABLE", CLKMODE="ASYNC",
    parameter SSROVERCE="DISABLE", OREGSET_A="RESET",
    parameter OREGSET_B="RESET", RESETMODE_A="ASYNC",
    parameter RESETMODE_B="ASYNC", ASYNC_RESET_RELEASE_A="ASYNC",
    parameter ASYNC_RESET_RELEASE_B="ASYNC", INIT_FILE="NONE",
    parameter FILL_ALL="NONE"
)(
    input wire [DATA_WIDTH_A-1:0] dia,
    input wire [DATA_WIDTH_B-1:0] dib,
    input wire [ADDR_WIDTH_A-1:0] addra,
    input wire [ADDR_WIDTH_B-1:0] addrb,
    input wire cea, ceb, ocea, oceb, clka, clkb, wea, web, bea, beb,
    input wire rsta, rstb, ecc_sbiterrinj, ecc_dbiterrinj,
    output reg [DATA_WIDTH_A-1:0] doa,
    output reg [DATA_WIDTH_B-1:0] dob,
    output wire ecc_sbiterr, ecc_dbiterr
);
    reg [DATA_WIDTH_A-1:0] mem [0:DATA_DEPTH_A-1];
    assign ecc_sbiterr = 1'b0;
    assign ecc_dbiterr = 1'b0;
    always @(posedge clka) begin
        if (cea) begin
            if (wea) mem[addra] <= dia;
            doa <= mem[addra];
        end
    end
    always @(posedge clkb) begin
        if (ceb) begin
            if (web) mem[addrb] <= dib;
            dob <= mem[addrb];
        end
    end
endmodule
