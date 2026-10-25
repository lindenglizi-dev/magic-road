module PH1P_LOGIC_DRAM
#(
    parameter DATA_WIDTH_W = 8,
    parameter DATA_WIDTH_R = DATA_WIDTH_W,
    parameter ADDR_WIDTH_W = 6,
    parameter ADDR_WIDTH_R = ADDR_WIDTH_W,
    parameter DATA_DEPTH_W = 2 ** ADDR_WIDTH_W,
    parameter DATA_DEPTH_R = 2 ** ADDR_WIDTH_R,
    parameter INIT_FILE = "NONE",
    parameter FILL_ALL = "NONE",
    parameter READREG = "DISABLE",
    parameter RESETMODE = "SYNC"
)
(
    input wire [DATA_WIDTH_W-1:0] di,
    input wire [ADDR_WIDTH_W-1:0] waddr,
    input wire we,
    input wire wclk,
    input wire rclk,
    input wire rrst,
    input wire rce,
    input wire [ADDR_WIDTH_R-1:0] raddr,
    output wire [DATA_WIDTH_R-1:0] rdoq,
    output wire [DATA_WIDTH_R-1:0] rdo
);
endmodule
