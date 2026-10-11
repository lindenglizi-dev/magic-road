// Dual-clock, two-bank grayscale frame store for the future ROI/HOG engine.
// The camera domain writes one complete analysis frame while the algorithm
// domain owns (and reads) the other bank.  If the reader misses its one-frame
// deadline, capture of the conflicting analysis frame is skipped instead of
// corrupting a bank that is still being read.
module gray_frame_pingpong #(
    parameter X_WIDTH = 8,
    parameter Y_WIDTH = 8,
    parameter ADDR_WIDTH = 16,
    parameter FRAME_WIDTH = 256,
    parameter FRAME_HEIGHT = 144
)(
    input  wire                  wr_clk,
    input  wire                  wr_rst_n,
    input  wire                  wr_valid,
    input  wire [7:0]            wr_gray,
    input  wire [X_WIDTH-1:0]    wr_x,
    input  wire [Y_WIDTH-1:0]    wr_y,
    input  wire                  wr_sof,
    input  wire                  wr_eol,
    input  wire                  wr_eof,
    output reg                   wr_protocol_error,
    output reg                   wr_frame_drop,
    output reg [31:0]            wr_captured_count,

    input  wire                  rd_clk,
    input  wire                  rd_rst_n,
    output reg                   rd_frame_ready,
    output reg [31:0]            rd_frame_id,
    output reg                   rd_frame_bank,
    output reg                   rd_owned,
    input  wire                  rd_release,
    input  wire                  rd_req_valid,
    input  wire [ADDR_WIDTH-1:0] rd_req_addr,
    output wire                  rd_rsp_valid,
    output wire [7:0]            rd_rsp_gray,
    output reg                   rd_protocol_error
);
    localparam FRAME_PIXELS = FRAME_WIDTH * FRAME_HEIGHT;

    wire [ADDR_WIDTH-1:0] wr_addr;
    generate
        if ((FRAME_WIDTH == 256) && (X_WIDTH == 8) &&
            (Y_WIDTH == 8) && (ADDR_WIDTH == 16)) begin : g_addr_256
            assign wr_addr = {wr_y, wr_x};
        end else begin : g_addr_generic
            assign wr_addr = (wr_y * FRAME_WIDTH) + wr_x;
        end
    endgenerate

    reg wr_bank;
    reg wr_frame_active, wr_store_frame, wr_frame_bad;
    reg [X_WIDTH:0] wr_expected_x;
    reg [Y_WIDTH:0] wr_expected_y;
    reg [ADDR_WIDTH:0] wr_pixel_count;
    reg published_toggle, published_bank;
    reg [31:0] published_frame_id;
    reg [31:0] wr_source_frame_id;

    reg rd_owned_sync1, rd_owned_sync2;
    reg rd_bank_sync1, rd_bank_sync2;
    wire bank_conflict = rd_owned_sync2 && (rd_bank_sync2 == wr_bank);
    wire start_store = wr_sof && !bank_conflict;
    wire write_this_pixel = wr_valid &&
                            (wr_frame_active ? wr_store_frame : start_store);

    reg published_sync1, published_sync2, published_seen;
    wire bank0_rd_valid, bank1_rd_valid;
    wire [7:0] bank0_rd_data, bank1_rd_data;
    wire rd_request_ok = rd_req_valid && rd_owned &&
                         (rd_req_addr < FRAME_PIXELS);

    gray_frame_bank_ram #(.ADDR_WIDTH(ADDR_WIDTH),
                          .FRAME_PIXELS(FRAME_PIXELS)) u_frame_bank0 (
        .wr_clk(wr_clk), .wr_en(write_this_pixel && !wr_bank),
        .wr_addr(wr_addr), .wr_data(wr_gray),
        .rd_clk(rd_clk), .rd_en(rd_request_ok && !rd_frame_bank),
        .rd_addr(rd_req_addr), .rd_valid(bank0_rd_valid),
        .rd_data(bank0_rd_data)
    );

    gray_frame_bank_ram #(.ADDR_WIDTH(ADDR_WIDTH),
                          .FRAME_PIXELS(FRAME_PIXELS)) u_frame_bank1 (
        .wr_clk(wr_clk), .wr_en(write_this_pixel && wr_bank),
        .wr_addr(wr_addr), .wr_data(wr_gray),
        .rd_clk(rd_clk), .rd_en(rd_request_ok && rd_frame_bank),
        .rd_addr(rd_req_addr), .rd_valid(bank1_rd_valid),
        .rd_data(bank1_rd_data)
    );

    assign rd_rsp_valid = bank0_rd_valid || bank1_rd_valid;
    assign rd_rsp_gray = bank1_rd_valid ? bank1_rd_data : bank0_rd_data;

    always @(posedge wr_clk or negedge wr_rst_n) begin
        if (!wr_rst_n) begin
            rd_owned_sync1 <= 1'b0;
            rd_owned_sync2 <= 1'b0;
            rd_bank_sync1 <= 1'b0;
            rd_bank_sync2 <= 1'b0;
        end else begin
            rd_owned_sync1 <= rd_owned;
            rd_owned_sync2 <= rd_owned_sync1;
            rd_bank_sync1 <= rd_frame_bank;
            rd_bank_sync2 <= rd_bank_sync1;
        end
    end

    always @(posedge wr_clk or negedge wr_rst_n) begin
        if (!wr_rst_n) begin
            wr_bank <= 1'b0;
            wr_frame_active <= 1'b0;
            wr_store_frame <= 1'b0;
            wr_frame_bad <= 1'b0;
            wr_expected_x <= 0;
            wr_expected_y <= 0;
            wr_pixel_count <= 0;
            published_toggle <= 1'b0;
            published_bank <= 1'b0;
            published_frame_id <= 0;
            wr_source_frame_id <= 0;
            wr_protocol_error <= 1'b0;
            wr_frame_drop <= 1'b0;
            wr_captured_count <= 0;
        end else begin
            wr_frame_drop <= 1'b0;

            if (wr_sof) begin
                if (!wr_valid || wr_eol || wr_eof || wr_frame_active ||
                    (wr_x != 0) || (wr_y != 0)) begin
                    wr_protocol_error <= 1'b1;
                    wr_frame_bad <= 1'b1;
                end else begin
                    wr_frame_bad <= 1'b0;
                end
                wr_frame_active <= 1'b1;
                wr_store_frame <= !bank_conflict;
                wr_expected_x <= 0;
                wr_expected_y <= 0;
                wr_pixel_count <= 0;
                if (bank_conflict)
                    wr_frame_drop <= 1'b1;
            end

            if (wr_valid) begin
                if (wr_sof) begin
                    if ((wr_x != 0) || (wr_y != 0))
                        wr_protocol_error <= 1'b1;
                end else if (!wr_frame_active || wr_eol || wr_eof ||
                             (wr_x != wr_expected_x[X_WIDTH-1:0]) ||
                             (wr_y != wr_expected_y[Y_WIDTH-1:0]) ||
                             (wr_x >= FRAME_WIDTH) ||
                             (wr_y >= FRAME_HEIGHT)) begin
                    wr_protocol_error <= 1'b1;
                    wr_frame_bad <= 1'b1;
                end

                if (wr_sof) begin
                    wr_expected_x <= 1;
                    wr_expected_y <= 0;
                    wr_pixel_count <= 1;
                end else begin
                    wr_expected_x <= wr_expected_x + 1'b1;
                    wr_pixel_count <= wr_pixel_count + 1'b1;
                end
            end

            if (wr_eol) begin
                if (wr_valid || wr_eof || !wr_frame_active ||
                    (wr_expected_x != FRAME_WIDTH)) begin
                    wr_protocol_error <= 1'b1;
                    wr_frame_bad <= 1'b1;
                end
                wr_expected_x <= 0;
                wr_expected_y <= wr_expected_y + 1'b1;
            end

            if (wr_eof) begin
                if (wr_valid || wr_eol || !wr_frame_active ||
                    (wr_expected_x != 0) ||
                    (wr_expected_y != FRAME_HEIGHT) ||
                    (wr_pixel_count != FRAME_PIXELS)) begin
                    wr_protocol_error <= 1'b1;
                    wr_frame_bad <= 1'b1;
                end
                wr_frame_active <= 1'b0;
                if (wr_store_frame && !wr_frame_bad &&
                    !wr_valid && !wr_eol && wr_frame_active &&
                    (wr_expected_x == 0) &&
                    (wr_expected_y == FRAME_HEIGHT) &&
                    (wr_pixel_count == FRAME_PIXELS)) begin
                    published_bank <= wr_bank;
                    // Source-frame numbering stays aligned with the CCL
                    // result stream even when an intermediate frame is
                    // deliberately not captured.
                    published_frame_id <= wr_source_frame_id;
                    published_toggle <= ~published_toggle;
                    wr_captured_count <= wr_captured_count + 1'b1;
                    wr_bank <= ~wr_bank;
                end
                wr_store_frame <= 1'b0;
                wr_frame_bad <= 1'b0;
                wr_source_frame_id <= wr_source_frame_id + 1'b1;
            end
        end
    end

    // Toggle CDC: bank/id are held stable by the writer around the toggle.
    always @(posedge rd_clk or negedge rd_rst_n) begin
        if (!rd_rst_n) begin
            published_sync1 <= 1'b0;
            published_sync2 <= 1'b0;
            published_seen <= 1'b0;
            rd_frame_ready <= 1'b0;
            rd_frame_id <= 0;
            rd_frame_bank <= 1'b0;
            rd_owned <= 1'b0;
            rd_protocol_error <= 1'b0;
        end else begin
            published_sync1 <= published_toggle;
            published_sync2 <= published_sync1;
            rd_frame_ready <= 1'b0;

            if (rd_release) begin
                if (!rd_owned)
                    rd_protocol_error <= 1'b1;
                rd_owned <= 1'b0;
            end

            if (rd_req_valid &&
                (!rd_owned || (rd_req_addr >= FRAME_PIXELS)))
                rd_protocol_error <= 1'b1;

            if (published_sync2 != published_seen) begin
                published_seen <= published_sync2;
                if (!rd_owned || rd_release) begin
                    rd_frame_id <= published_frame_id;
                    rd_frame_bank <= published_bank;
                    rd_owned <= 1'b1;
                    rd_frame_ready <= 1'b1;
                end else begin
                    // Reader missed a completed frame; keep its current bank
                    // protected and deliberately discard the new notification.
                    rd_protocol_error <= 1'b1;
                end
            end
        end
    end

endmodule
