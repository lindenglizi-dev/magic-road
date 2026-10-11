`timescale 1ns/1ps

module tb_track_overlay;
    reg src_clk = 0;
    reg dst_clk = 0;
    always #5 src_clk = ~src_clk;
    always #7 dst_clk = ~dst_clk;

    reg src_rst_n = 0;
    reg dst_rst_n = 0;
    reg track_frame_done = 0;
    wire [1:0] track_rd_index;
    reg track_valid, track_visible, track_confirmed;
    reg [1:0] track_class;
    reg [7:0] track_xmin, track_xmax, track_ymin, track_ymax;
    wire [159:0] dst_tracks;
    wire dst_update;

    reg in_vsync = 0;
    reg in_hsync = 0;
    reg in_de = 0;
    reg [23:0] in_rgb = 24'h112233;
    wire out_vsync, out_hsync, out_de;
    wire [23:0] out_rgb;
    integer green_count = 0;
    integer cyan_count = 0;
    integer i, line;

    always @* begin
        track_valid = 1'b0;
        track_visible = 1'b0;
        track_confirmed = 1'b0;
        track_class = 2'd0;
        track_xmin = 8'd0;
        track_xmax = 8'd0;
        track_ymin = 8'd0;
        track_ymax = 8'd0;
        case (track_rd_index)
            2'd0: begin
                track_valid = 1'b1; track_visible = 1'b1;
                track_confirmed = 1'b1; track_class = 2'd1;
                track_xmin = 8'd2; track_xmax = 8'd3;
                track_ymin = 8'd1; track_ymax = 8'd2;
            end
            2'd1: begin
                track_valid = 1'b1; track_visible = 1'b1;
                track_confirmed = 1'b1; track_class = 2'd2;
                track_xmin = 8'd5; track_xmax = 8'd6;
                track_ymin = 8'd1; track_ymax = 8'd2;
            end
        endcase
    end

    track_snapshot_cdc u_cdc (
        .src_clk(src_clk), .src_rst_n(src_rst_n),
        .track_frame_done(track_frame_done),
        .track_rd_index(track_rd_index),
        .track_valid(track_valid), .track_visible(track_visible),
        .track_confirmed(track_confirmed), .track_class(track_class),
        .track_xmin(track_xmin), .track_xmax(track_xmax),
        .track_ymin(track_ymin), .track_ymax(track_ymax),
        .dst_clk(dst_clk), .dst_rst_n(dst_rst_n),
        .dst_tracks(dst_tracks), .dst_update(dst_update)
    );

    road_box_overlay u_overlay (
        .clk(dst_clk), .rst_n(dst_rst_n),
        .in_vsync(in_vsync), .in_hsync(in_hsync),
        .in_de(in_de), .in_rgb(in_rgb), .tracks(dst_tracks),
        .out_vsync(out_vsync), .out_hsync(out_hsync),
        .out_de(out_de), .out_rgb(out_rgb)
    );

    always @(posedge dst_clk) begin
        if (out_de && out_rgb == 24'h00ff00)
            green_count <= green_count + 1;
        if (out_de && out_rgb == 24'h00ffff)
            cyan_count <= cyan_count + 1;
    end

    initial begin
        repeat (4) @(posedge src_clk);
        src_rst_n = 1;
        repeat (2) @(posedge dst_clk);
        dst_rst_n = 1;

        @(posedge src_clk);
        track_frame_done = 1;
        @(posedge src_clk);
        track_frame_done = 0;

        @(posedge dst_update);
        #1;
        if (!dst_tracks[39] || dst_tracks[36:35] != 2'd1 ||
            dst_tracks[34:27] != 8'd2 || dst_tracks[26:19] != 8'd3)
            $fatal(1, "track 0 snapshot mismatch");
        if (!dst_tracks[79] || dst_tracks[76:75] != 2'd2 ||
            dst_tracks[74:67] != 8'd5 || dst_tracks[66:59] != 8'd6)
            $fatal(1, "track 1 snapshot mismatch");

        @(negedge dst_clk);
        in_vsync = 1;
        @(negedge dst_clk);
        in_vsync = 0;
        for (line = 0; line < 20; line = line + 1) begin
            in_de = 1;
            for (i = 0; i < 50; i = i + 1)
                @(negedge dst_clk);
            in_de = 0;
            @(negedge dst_clk);
        end
        repeat (3) @(posedge dst_clk);

        if (green_count == 0)
            $fatal(1, "pedestrian box was not drawn");
        if (cyan_count == 0)
            $fatal(1, "vehicle box was not drawn");
        $display("PASS: tracker snapshot CDC and HDMI box overlay");
        $finish;
    end
endmodule
