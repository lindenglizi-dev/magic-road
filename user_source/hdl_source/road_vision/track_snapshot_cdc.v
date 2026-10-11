// Read the four tracker entries after each processed frame, freeze them, then
// transfer the stable snapshot to the HDMI clock domain with a toggle event.
// One 40-bit entry:
// {valid, visible, confirmed, class[1:0], xmin, xmax, ymin, ymax, 3'b0}.
module track_snapshot_cdc (
    input  wire         src_clk,
    input  wire         src_rst_n,
    input  wire         track_frame_done,
    output reg  [1:0]   track_rd_index,
    input  wire         track_valid,
    input  wire         track_visible,
    input  wire         track_confirmed,
    input  wire [1:0]   track_class,
    input  wire [7:0]   track_xmin,
    input  wire [7:0]   track_xmax,
    input  wire [7:0]   track_ymin,
    input  wire [7:0]   track_ymax,

    input  wire         dst_clk,
    input  wire         dst_rst_n,
    output reg  [159:0] dst_tracks,
    output reg          dst_update
);
    wire [39:0] track_word = {track_valid, track_visible,
                              track_confirmed, track_class,
                              track_xmin, track_xmax,
                              track_ymin, track_ymax, 3'b000};

    reg          capture_active;
    reg  [159:0] src_tracks;
    reg          src_toggle;

    always @(posedge src_clk or negedge src_rst_n) begin
        if (!src_rst_n) begin
            track_rd_index <= 2'd0;
            capture_active <= 1'b0;
            src_tracks <= 160'd0;
            src_toggle <= 1'b0;
        end else begin
            if (track_frame_done && !capture_active) begin
                track_rd_index <= 2'd0;
                capture_active <= 1'b1;
            end else if (capture_active) begin
                case (track_rd_index)
                    2'd0: src_tracks[39:0]    <= track_word;
                    2'd1: src_tracks[79:40]   <= track_word;
                    2'd2: src_tracks[119:80]  <= track_word;
                    2'd3: src_tracks[159:120] <= track_word;
                endcase
                if (track_rd_index == 2'd3) begin
                    capture_active <= 1'b0;
                    src_toggle <= ~src_toggle;
                end else begin
                    track_rd_index <= track_rd_index + 1'b1;
                end
            end
        end
    end

    (* async_reg = "true" *) reg toggle_meta, toggle_sync;
    reg toggle_seen;
    reg [159:0] tracks_meta;

    always @(posedge dst_clk or negedge dst_rst_n) begin
        if (!dst_rst_n) begin
            toggle_meta <= 1'b0;
            toggle_sync <= 1'b0;
            toggle_seen <= 1'b0;
            tracks_meta <= 160'd0;
            dst_tracks <= 160'd0;
            dst_update <= 1'b0;
        end else begin
            // The source bus remains unchanged for a complete video frame.
            // The synchronized toggle arrives only after that bus is stable.
            tracks_meta <= src_tracks;
            toggle_meta <= src_toggle;
            toggle_sync <= toggle_meta;
            dst_update <= 1'b0;
            if (toggle_sync != toggle_seen) begin
                dst_tracks <= tracks_meta;
                toggle_seen <= toggle_sync;
                dst_update <= 1'b1;
            end
        end
    end
endmodule
