// Streaming 3x3 binary-mask cleanup with zero padding at image boundaries.
//
// The input video has no ready signal.  This block therefore relies on the
// natural blanking of the analysis stream: at least two idle clocks after an
// input EOL, and at least FRAME_WIDTH+4 idle clocks after input EOF.  The
// deployed AWB 5x5 sampler provides much larger gaps than these minima.
//
// A pixel is kept when at least MIN_NEIGHBORS of its 3x3 neighbourhood are 1.
// MIN_NEIGHBORS=3 removes isolated pixels and two-pixel speckle while retaining
// substantially more thin foreground than a fixed 3x3 majority/erosion.
module binary_cleanup_3x3 #(
    parameter X_WIDTH = 8,
    parameter Y_WIDTH = 8,
    parameter FRAME_WIDTH = 256,
    parameter FRAME_HEIGHT = 144,
    parameter ENABLE = 1,
    parameter MIN_NEIGHBORS = 3,
    parameter REQUIRE_CENTER = 1
)(
    input  wire                   clk,
    input  wire                   rst_n,
    input  wire                   in_valid,
    input  wire                   in_mask,
    input  wire [X_WIDTH-1:0]     in_x,
    input  wire [Y_WIDTH-1:0]     in_y,
    input  wire                   in_sof,
    input  wire                   in_eol,
    input  wire                   in_eof,
    output reg                    out_valid,
    output reg                    out_mask,
    output reg [X_WIDTH-1:0]      out_x,
    output reg [Y_WIDTH-1:0]      out_y,
    output reg                    out_sof,
    output reg                    out_eol,
    output reg                    out_eof,
    output reg                    protocol_error
);
    // Three banks avoid relying on vendor-specific read-during-write RAM mode.
    // Only 3*256 bits are required in the deployed configuration.
    reg line_bank0 [0:FRAME_WIDTH-1];
    reg line_bank1 [0:FRAME_WIDTH-1];
    reg line_bank2 [0:FRAME_WIDTH-1];

    reg [1:0] write_bank;
    reg [1:0] last_bank;
    reg row_seen;
    reg [X_WIDTH-1:0] last_x;
    reg [Y_WIDTH-1:0] row_y;

    reg top_l2, top_l1, mid_l2, mid_l1, bot_l2, bot_l1;
    reg right_pending, eol_pending;
    reg right_mask;
    reg [Y_WIDTH-1:0] right_y;

    reg flush_active, flush_right_pending;
    reg flush_eol_pending, flush_eof_pending;
    reg [X_WIDTH-1:0] flush_x;
    reg flush_top_l2, flush_top_l1;
    reg flush_mid_l2, flush_mid_l1;
    reg flush_right_mask;

    reg top_now, mid_now;
    reg flush_top_now, flush_mid_now;
    reg [3:0] neighbourhood_sum;
    reg [3:0] right_sum;
    reg [3:0] flush_sum;
    reg [3:0] flush_right_sum;

    wire busy = right_pending || eol_pending || flush_active ||
                flush_right_pending || flush_eol_pending ||
                flush_eof_pending;

    always @(*) begin
        top_now = 1'b0;
        mid_now = 1'b0;
        case (write_bank)
            2'd0: begin top_now = line_bank1[in_x]; mid_now = line_bank2[in_x]; end
            2'd1: begin top_now = line_bank2[in_x]; mid_now = line_bank0[in_x]; end
            default: begin top_now = line_bank0[in_x]; mid_now = line_bank1[in_x]; end
        endcase

        flush_top_now = 1'b0;
        flush_mid_now = 1'b0;
        case (last_bank)
            2'd0: begin flush_top_now = line_bank2[flush_x]; flush_mid_now = line_bank0[flush_x]; end
            2'd1: begin flush_top_now = line_bank0[flush_x]; flush_mid_now = line_bank1[flush_x]; end
            default: begin flush_top_now = line_bank1[flush_x]; flush_mid_now = line_bank2[flush_x]; end
        endcase

        // Interior/left-border result produced while the following row arrives.
        neighbourhood_sum = 4'd0;
        if (in_y >= 2) begin
            neighbourhood_sum = neighbourhood_sum + top_l1 + top_now;
            if (in_x >= 2)
                neighbourhood_sum = neighbourhood_sum + top_l2;
        end
        neighbourhood_sum = neighbourhood_sum + mid_l1 + mid_now;
        if (in_x >= 2)
            neighbourhood_sum = neighbourhood_sum + mid_l2;
        neighbourhood_sum = neighbourhood_sum + bot_l1 + in_mask;
        if (in_x >= 2)
            neighbourhood_sum = neighbourhood_sum + bot_l2;

        // Right border has no right-hand column.
        right_sum = 4'd0;
        if (in_y >= 2)
            right_sum = right_sum + top_l1 + top_now;
        right_sum = right_sum + mid_l1 + mid_now + bot_l1 + in_mask;

        // Bottom row has no row below it.
        flush_sum = flush_top_l1 + flush_top_now +
                    flush_mid_l1 + flush_mid_now;
        if (flush_x >= 2)
            flush_sum = flush_sum + flush_top_l2 + flush_mid_l2;
        flush_right_sum = flush_top_l1 + flush_top_now +
                          flush_mid_l1 + flush_mid_now;
    end

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            write_bank <= 2'd0;
            last_bank <= 2'd0;
            row_seen <= 1'b0;
            last_x <= {X_WIDTH{1'b0}};
            row_y <= {Y_WIDTH{1'b0}};
            top_l2 <= 1'b0; top_l1 <= 1'b0;
            mid_l2 <= 1'b0; mid_l1 <= 1'b0;
            bot_l2 <= 1'b0; bot_l1 <= 1'b0;
            right_pending <= 1'b0;
            eol_pending <= 1'b0;
            right_mask <= 1'b0;
            right_y <= {Y_WIDTH{1'b0}};
            flush_active <= 1'b0;
            flush_right_pending <= 1'b0;
            flush_eol_pending <= 1'b0;
            flush_eof_pending <= 1'b0;
            flush_x <= {X_WIDTH{1'b0}};
            flush_top_l2 <= 1'b0; flush_top_l1 <= 1'b0;
            flush_mid_l2 <= 1'b0; flush_mid_l1 <= 1'b0;
            flush_right_mask <= 1'b0;
            out_valid <= 1'b0;
            out_mask <= 1'b0;
            out_x <= {X_WIDTH{1'b0}};
            out_y <= {Y_WIDTH{1'b0}};
            out_sof <= 1'b0;
            out_eol <= 1'b0;
            out_eof <= 1'b0;
            protocol_error <= 1'b0;
        end else begin
            out_valid <= 1'b0;
            out_mask <= 1'b0;
            out_sof <= 1'b0;
            out_eol <= 1'b0;
            out_eof <= 1'b0;

            if (busy && (in_valid || in_eol || in_eof))
                protocol_error <= 1'b1;

            if (right_pending) begin
                out_valid <= 1'b1;
                out_mask <= right_mask;
                out_x <= FRAME_WIDTH-1;
                out_y <= right_y;
                right_pending <= 1'b0;
                eol_pending <= 1'b1;
            end else if (eol_pending) begin
                out_eol <= 1'b1;
                eol_pending <= 1'b0;
            end else if (flush_active) begin
                if (flush_x == 0) begin
                    flush_top_l2 <= 1'b0;
                    flush_top_l1 <= flush_top_now;
                    flush_mid_l2 <= 1'b0;
                    flush_mid_l1 <= flush_mid_now;
                    flush_x <= 1'b1;
                end else begin
                    out_valid <= 1'b1;
                    out_x <= flush_x - 1'b1;
                    out_y <= FRAME_HEIGHT-1;
                    out_mask <= (ENABLE == 0) ? flush_mid_l1 :
                                ((REQUIRE_CENTER == 0) ?
                                 (flush_sum >= MIN_NEIGHBORS) :
                                 (flush_mid_l1 &&
                                  (flush_sum >= MIN_NEIGHBORS)));
                    flush_top_l2 <= flush_top_l1;
                    flush_top_l1 <= flush_top_now;
                    flush_mid_l2 <= flush_mid_l1;
                    flush_mid_l1 <= flush_mid_now;
                    if (flush_x == FRAME_WIDTH-1) begin
                        flush_right_mask <= (ENABLE == 0) ? flush_mid_now :
                            ((REQUIRE_CENTER == 0) ?
                             (flush_right_sum >= MIN_NEIGHBORS) :
                             (flush_mid_now &&
                              (flush_right_sum >= MIN_NEIGHBORS)));
                        flush_active <= 1'b0;
                        flush_right_pending <= 1'b1;
                    end else begin
                        flush_x <= flush_x + 1'b1;
                    end
                end
            end else if (flush_right_pending) begin
                out_valid <= 1'b1;
                out_mask <= flush_right_mask;
                out_x <= FRAME_WIDTH-1;
                out_y <= FRAME_HEIGHT-1;
                flush_right_pending <= 1'b0;
                flush_eol_pending <= 1'b1;
            end else if (flush_eol_pending) begin
                out_eol <= 1'b1;
                flush_eol_pending <= 1'b0;
                flush_eof_pending <= 1'b1;
            end else if (flush_eof_pending) begin
                out_eof <= 1'b1;
                flush_eof_pending <= 1'b0;
            end else begin
                if (in_valid) begin
                    if (!row_seen) begin
                        if (in_x != 0)
                            protocol_error <= 1'b1;
                        row_seen <= 1'b1;
                        row_y <= in_y;
                        top_l2 <= 1'b0; top_l1 <= top_now;
                        mid_l2 <= 1'b0; mid_l1 <= mid_now;
                        bot_l2 <= 1'b0; bot_l1 <= in_mask;
                    end else begin
                        if ((in_y != row_y) || (in_x != last_x + 1'b1))
                            protocol_error <= 1'b1;
                        top_l2 <= top_l1; top_l1 <= top_now;
                        mid_l2 <= mid_l1; mid_l1 <= mid_now;
                        bot_l2 <= bot_l1; bot_l1 <= in_mask;

                        if (in_y != 0) begin
                            out_valid <= 1'b1;
                            out_x <= in_x - 1'b1;
                            out_y <= in_y - 1'b1;
                            out_sof <= (in_y == 1) && (in_x == 1);
                            out_mask <= (ENABLE == 0) ? mid_l1 :
                                ((REQUIRE_CENTER == 0) ?
                                 (neighbourhood_sum >= MIN_NEIGHBORS) :
                                 (mid_l1 &&
                                  (neighbourhood_sum >= MIN_NEIGHBORS)));
                        end
                    end
                    last_x <= in_x;
                    // SOF explicitly starts in bank 0.  Do not depend on
                    // FRAME_HEIGHT being a multiple of three across frames.
                    if (in_sof)
                        line_bank0[in_x] <= in_mask;
                    else begin
                        case (write_bank)
                            2'd0: line_bank0[in_x] <= in_mask;
                            2'd1: line_bank1[in_x] <= in_mask;
                            default: line_bank2[in_x] <= in_mask;
                        endcase
                    end

                    if (in_sof) begin
                        if ((in_x != 0) || (in_y != 0) || row_seen)
                            protocol_error <= 1'b1;
                        write_bank <= 2'd0;
                    end

                    if ((in_x == FRAME_WIDTH-1) && (in_y != 0)) begin
                        right_mask <= (ENABLE == 0) ? mid_now :
                            ((REQUIRE_CENTER == 0) ?
                             (right_sum >= MIN_NEIGHBORS) :
                             (mid_now && (right_sum >= MIN_NEIGHBORS)));
                        right_y <= in_y - 1'b1;
                    end
                end

                if (in_eol) begin
                    if (!row_seen || (last_x != FRAME_WIDTH-1))
                        protocol_error <= 1'b1;
                    row_seen <= 1'b0;
                    last_bank <= write_bank;
                    write_bank <= (write_bank == 2) ? 2'd0 : write_bank + 1'b1;
                    if (row_y != 0)
                        right_pending <= 1'b1;
                end

                if (in_eof) begin
                    if (row_seen || (row_y != FRAME_HEIGHT-1))
                        protocol_error <= 1'b1;
                    flush_x <= {X_WIDTH{1'b0}};
                    flush_active <= 1'b1;
                end
            end
        end
    end
endmodule
