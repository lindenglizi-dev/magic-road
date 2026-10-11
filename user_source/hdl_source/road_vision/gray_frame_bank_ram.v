// One 256x144x8 frame bank built from 18 native 2048x8 ERAM20K blocks.
// Port A writes in the camera clock domain; port B reads in the algorithm
// clock domain.  Explicit tiling avoids TD expanding a large inferred
// asynchronous dual-clock array into MSLICE muxes.
module gray_frame_bank_ram #(
    parameter ADDR_WIDTH = 16,
    parameter FRAME_PIXELS = 256*144,
    parameter TILE_COUNT = 18
)(
    input  wire                  wr_clk,
    input  wire                  wr_en,
    input  wire [ADDR_WIDTH-1:0] wr_addr,
    input  wire [7:0]            wr_data,
    input  wire                  rd_clk,
    input  wire                  rd_en,
    input  wire [ADDR_WIDTH-1:0] rd_addr,
    output reg                   rd_valid,
    output wire [7:0]            rd_data
);
    wire [TILE_COUNT*8-1:0] tile_dout;
    reg [4:0] rd_tile_q;
    wire [4:0] wr_tile = wr_addr[15:11];
    wire [4:0] rd_tile = rd_addr[15:11];
    genvar g;

    always @(posedge rd_clk) begin
        rd_valid <= rd_en;
        if (rd_en)
            rd_tile_q <= rd_tile;
    end

    assign rd_data = tile_dout[rd_tile_q*8 +: 8];

    generate
        for (g = 0; g < TILE_COUNT; g = g + 1) begin : g_eram
            PH1P_LOGIC_ERAM #(
                .DATA_WIDTH_A(8), .DATA_WIDTH_B(8),
                .ADDR_WIDTH_A(11), .ADDR_WIDTH_B(11),
                .DATA_DEPTH_A(2048), .DATA_DEPTH_B(2048),
                .MODE("DP"), .REGMODE_A("NOREG"),
                .REGMODE_B("NOREG"),
                .WRITEMODE_A("NORMAL"), .WRITEMODE_B("NORMAL"),
                .IMPLEMENT("20K(FAST)"),
                .ECC_ENCODE("DISABLE"), .ECC_DECODE("DISABLE"),
                .CLKMODE("ASYNC"), .SSROVERCE("DISABLE"),
                .OREGSET_A("RESET"), .OREGSET_B("RESET"),
                .RESETMODE_A("ASYNC"), .RESETMODE_B("ASYNC"),
                .ASYNC_RESET_RELEASE_A("ASYNC"),
                .ASYNC_RESET_RELEASE_B("ASYNC"),
                .INIT_FILE("NONE"), .FILL_ALL("NONE")
            ) u_eram (
                .dia(wr_data), .dib(8'd0),
                .addra(wr_addr[10:0]), .addrb(rd_addr[10:0]),
                .cea(wr_en && (wr_tile == g)),
                .ceb(rd_en && (rd_tile == g)),
                .ocea(1'b0), .oceb(1'b0),
                .clka(wr_clk), .clkb(rd_clk),
                .wea(wr_en && (wr_tile == g)), .web(1'b0),
                .bea(1'b0), .beb(1'b0),
                .rsta(1'b0), .rstb(1'b0),
                .doa(), .dob(tile_dout[g*8 +: 8]),
                .ecc_sbiterr(), .ecc_dbiterr(),
                .ecc_sbiterrinj(1'b0), .ecc_dbiterrinj(1'b0)
            );
        end
    endgenerate
endmodule
