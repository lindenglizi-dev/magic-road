`timescale 1ns/1ps

// Functional end-to-end test from the lab1 AWB tap to tracking/events.
// Proprietary MIPI, DDR and HDMI PHY IP are not part of this RTL test.
module tb_lab1_road_chain;
    reg clk, rst_n, in_valid, in_sof, in_eol;
    reg [95:0] in_rgb;
    wire analysis_valid, analysis_sof, analysis_eol, analysis_eof;
    wire [7:0] analysis_gray, analysis_x, analysis_y;
    wire adapter_error, core_error;
    wire obj_valid, track_valid, track_confirmed, event_valid;
    wire [2:0] object_count, event_type;
    wire [15:0] track_id, event_track_id;
    wire track_frame_done, event_frame_done;
    integer errors, pixels, lines, frames, zone_entries;
    integer row, beat, wait_cycles;
    reg [15:0] first_track_id;

    awb96_analysis_adapter #(
        .SRC_WIDTH(40), .SRC_HEIGHT(20),
        .OUT_WIDTH(8), .OUT_HEIGHT(4)
    ) adapter (
        .clk(clk), .rst_n(rst_n),
        .in_rgb(in_rgb), .in_valid(in_valid),
        .in_sof(in_sof), .in_eol(in_eol),
        .analysis_valid(analysis_valid),
        .analysis_gray(analysis_gray),
        .analysis_x(analysis_x), .analysis_y(analysis_y),
        .analysis_sof(analysis_sof),
        .analysis_eol(analysis_eol),
        .analysis_eof(analysis_eof),
        .protocol_error(adapter_error)
    );

    foreground_ccl_top #(
        .X_WIDTH(8), .Y_WIDTH(8), .BG_ADDR_WIDTH(5),
        .FRAME_WIDTH(8), .FRAME_HEIGHT(4),
        .LEARN_FRAMES(2), .LEARN_SHIFT(1), .UPDATE_SHIFT(2),
        .LABEL_WIDTH(4), .RUN_ADDR_WIDTH(3), .AREA_WIDTH(8),
        .MAX_RUN(8), .MAX_LABEL(7), .MIN_AREA(1),
        .CLASS_MIN_AREA(1), .PED_MIN_HEIGHT(2), .VEH_MIN_WIDTH(2),
        .ZONE_X_MIN(2), .ZONE_X_MAX(3),
        .ZONE_Y_MIN(1), .ZONE_Y_MAX(2),
        .LINE_X(3), .DWELL_FRAMES(3)
    ) core (
        .clk(clk), .rst_n(rst_n),
        .analysis_valid(analysis_valid),
        .analysis_gray(analysis_gray),
        .analysis_x(analysis_x), .analysis_y(analysis_y),
        .analysis_sof(analysis_sof),
        .analysis_eol(analysis_eol),
        .analysis_eof(analysis_eof),
        .diff_threshold(8'd10),
        .background_update_enable(1'b1),
        .freeze_foreground(1'b1),
        .background_relearn(1'b0),
        .object_rd_index(2'd0), .track_rd_index(2'd0),
        .obj_valid(obj_valid), .object_count(object_count),
        .track_valid(track_valid),
        .track_confirmed(track_confirmed), .track_id(track_id),
        .track_frame_done(track_frame_done),
        .event_valid(event_valid), .event_type(event_type),
        .event_track_id(event_track_id),
        .event_frame_done(event_frame_done),
        .core_error(core_error)
    );

    always #5 clk = ~clk;

    function [23:0] pixel_rgb;
        input integer px, py;
        input object_on;
        reg [7:0] level;
        begin
            level = (object_on && ((px == 10) || (px == 15)) &&
                     ((py == 5) || (py == 10))) ? 8'd150 : 8'd100;
            pixel_rgb = {level, level, level};
        end
    endfunction

    always @(posedge clk) begin
        #1;
        if (analysis_valid) begin
            if (analysis_x !== (pixels % 8) ||
                analysis_y !== (pixels / 8)) begin
                $display("FAIL: analysis coordinate pixel=%0d x=%0d y=%0d",
                         pixels, analysis_x, analysis_y);
                errors = errors + 1;
            end
            if (analysis_sof !== (pixels == 0)) begin
                $display("FAIL: analysis SOF position");
                errors = errors + 1;
            end
            pixels = pixels + 1;
        end
        if (analysis_eol) lines = lines + 1;
        if (analysis_eof) frames = frames + 1;
        if (event_valid && event_type[0]) zone_entries = zone_entries + 1;
    end

    task check_true;
        input condition;
        input [8*100-1:0] message;
        begin
            if (!condition) begin
                $display("FAIL: %0s", message);
                errors = errors + 1;
            end
        end
    endtask

    task send_frame;
        input object_on;
        begin
            pixels = 0; lines = 0; frames = 0;
            @(negedge clk); in_sof = 1'b1;
            @(negedge clk); in_sof = 1'b0;
            for (row = 0; row < 20; row = row + 1) begin
                for (beat = 0; beat < 10; beat = beat + 1) begin
                    @(negedge clk);
                    in_valid = 1'b1;
                    in_rgb = {
                        pixel_rgb(beat*4+3, row, object_on),
                        pixel_rgb(beat*4+2, row, object_on),
                        pixel_rgb(beat*4+1, row, object_on),
                        pixel_rgb(beat*4, row, object_on)
                    };
                end
                @(negedge clk); in_valid = 1'b0; in_eol = 1'b1;
                @(negedge clk); in_eol = 1'b0;
            end
            wait_cycles = 0;
            while (!event_frame_done && wait_cycles < 10000) begin
                @(posedge clk); #2;
                wait_cycles = wait_cycles + 1;
            end
            check_true(event_frame_done, "core/event completion timeout");
            check_true(pixels == 32 && lines == 4 && frames == 1,
                       "40x20 to 8x4 adapter output count mismatch");
            check_true(!adapter_error && !core_error,
                       "analysis adapter or core protocol error");
            @(negedge clk);
        end
    endtask

    initial begin
        clk = 0; rst_n = 0; in_valid = 0; in_sof = 0; in_eol = 0;
        in_rgb = 0; errors = 0; pixels = 0; lines = 0; frames = 0;
        zone_entries = 0;
        repeat (3) @(posedge clk);
        @(negedge clk); rst_n = 1;
        send_frame(1'b0);
        send_frame(1'b0);
        send_frame(1'b1);
        check_true(object_count == 1 && track_valid && !track_confirmed,
                   "first detected object/track missing");
        first_track_id = track_id;
        send_frame(1'b1);
        check_true(object_count == 1 && track_confirmed &&
                   track_id == first_track_id,
                   "confirmed track lost after second object frame");
        check_true(zone_entries == 1 && event_track_id == first_track_id,
                   "confirmed track zone event missing or duplicated");
        if (errors == 0)
            $display("PASS: lab1 AWB tap to adapter/background/CCL/track/event");
        else
            $display("FAIL: lab1 road chain errors=%0d", errors);
        $finish;
    end
endmodule
