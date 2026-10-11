// AWB output is four RGB888 pixels per valid beat, lane 0 in bits [23:0].
// Select one pixel every five columns and one row every five rows.
// 1280x720 becomes 256x144 without touching the original DDR/HDMI stream.
module awb96_analysis_adapter #(
    parameter SRC_WIDTH = 1280,
    parameter SRC_HEIGHT = 720,
    parameter OUT_WIDTH = SRC_WIDTH / 5,
    parameter OUT_HEIGHT = SRC_HEIGHT / 5
)(
    input  wire        clk,
    input  wire        rst_n,
    input  wire [95:0] in_rgb,
    input  wire        in_valid,
    input  wire        in_sof,
    input  wire        in_eol,
    output reg         analysis_valid,
    output reg  [7:0]  analysis_gray,
    output reg  [7:0]  analysis_x,
    output reg  [7:0]  analysis_y,
    output reg         analysis_sof,
    output reg         analysis_eol,
    output reg         analysis_eof,
    output reg         protocol_error
);
    localparam BEATS_PER_LINE = SRC_WIDTH / 4;
    reg frame_active, sof_pending;
    reg [9:0] row_index;
    reg [8:0] beat_index;
    reg [2:0] row_mod5, beat_mod5;
    reg [8:0] sampled_in_row;
    reg [8:0] sampled_rows;
    reg [7:0] out_x, out_y;
    reg [23:0] selected_rgb;
    wire [2:0] effective_row_mod = in_sof ? 3'd0 : row_mod5;
    wire [2:0] effective_beat_mod = in_sof ? 3'd0 : beat_mod5;
    wire sample_pixel = in_valid && (effective_row_mod == 0) &&
                        (effective_beat_mod != 4);
    wire [7:0] gray_value =
        {2'b00, selected_rgb[23:18]} +
        {1'b0, selected_rgb[15:9]} +
        {2'b00, selected_rgb[7:2]};

    always @(*) begin
        case (effective_beat_mod)
            3'd0: selected_rgb = in_rgb[23:0];
            3'd1: selected_rgb = in_rgb[47:24];
            3'd2: selected_rgb = in_rgb[71:48];
            3'd3: selected_rgb = in_rgb[95:72];
            default: selected_rgb = 24'd0;
        endcase
    end

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            frame_active <= 1'b0;
            sof_pending <= 1'b0;
            row_index <= 10'd0;
            beat_index <= 9'd0;
            row_mod5 <= 3'd0;
            beat_mod5 <= 3'd0;
            sampled_in_row <= 9'd0;
            sampled_rows <= 9'd0;
            out_x <= 8'd0;
            out_y <= 8'd0;
            analysis_valid <= 1'b0;
            analysis_gray <= 8'd0;
            analysis_x <= 8'd0;
            analysis_y <= 8'd0;
            analysis_sof <= 1'b0;
            analysis_eol <= 1'b0;
            analysis_eof <= 1'b0;
            protocol_error <= 1'b0;
        end else begin
            analysis_valid <= 1'b0;
            analysis_sof <= 1'b0;
            analysis_eol <= 1'b0;
            analysis_eof <= 1'b0;
            if (in_sof) begin
                if (frame_active)
                    protocol_error <= 1'b1;
                frame_active <= 1'b1;
                sof_pending <= 1'b1;
                row_index <= 10'd0;
                beat_index <= 9'd0;
                row_mod5 <= 3'd0;
                beat_mod5 <= 3'd0;
                sampled_in_row <= 9'd0;
                sampled_rows <= 9'd0;
                out_x <= 8'd0;
                out_y <= 8'd0;
            end
            if (in_valid) begin
                if (!frame_active && !in_sof)
                    protocol_error <= 1'b1;
                if ((in_sof ? 9'd0 : beat_index) >= BEATS_PER_LINE)
                    protocol_error <= 1'b1;
                beat_index <= (in_sof ? 9'd0 : beat_index) + 1'b1;
                beat_mod5 <= (effective_beat_mod == 4) ? 3'd0 :
                             effective_beat_mod + 1'b1;
                if (sample_pixel) begin
                    analysis_valid <= 1'b1;
                    analysis_gray <= gray_value;
                    analysis_x <= in_sof ? 8'd0 : out_x;
                    analysis_y <= in_sof ? 8'd0 : out_y;
                    analysis_sof <= in_sof || sof_pending;
                    sof_pending <= 1'b0;
                    out_x <= (in_sof ? 8'd0 : out_x) + 1'b1;
                    sampled_in_row <=
                        (in_sof ? 9'd0 : sampled_in_row) + 1'b1;
                end
            end
            if (in_eol) begin
                if (in_valid || !frame_active ||
                    beat_index != BEATS_PER_LINE)
                    protocol_error <= 1'b1;
                if (row_mod5 == 0) begin
                    if (sampled_in_row != OUT_WIDTH)
                        protocol_error <= 1'b1;
                    analysis_eol <= 1'b1;
                    out_x <= 8'd0;
                    out_y <= out_y + 1'b1;
                    sampled_rows <= sampled_rows + 1'b1;
                end else if (sampled_in_row != 0)
                    protocol_error <= 1'b1;
                sampled_in_row <= 9'd0;
                beat_index <= 9'd0;
                beat_mod5 <= 3'd0;
                row_index <= row_index + 1'b1;
                row_mod5 <= (row_mod5 == 4) ? 3'd0 : row_mod5 + 1'b1;
                if (row_index == SRC_HEIGHT-1) begin
                    if (sampled_rows != OUT_HEIGHT)
                        protocol_error <= 1'b1;
                    analysis_eof <= 1'b1;
                    frame_active <= 1'b0;
                end
            end
        end
    end
endmodule
