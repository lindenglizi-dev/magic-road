`timescale 1ns/1ps

// Replay 256x144 grayscale frame memories through the synthesizable analysis
// core. MIPI/ISP/DDR are deliberately excluded: this test evaluates the road
// algorithm and produces machine-readable objects, tracks, events and masks.
module tb_video_replay;
    localparam FRAME_WIDTH = 256;
    localparam FRAME_HEIGHT = 144;
    localparam FRAME_PIXELS = FRAME_WIDTH * FRAME_HEIGHT;

    reg clk = 0;
    reg rst_n = 0;
    always #5 clk = ~clk;

    reg analysis_valid = 0;
    reg [7:0] analysis_gray = 0;
    reg [7:0] analysis_x = 0;
    reg [7:0] analysis_y = 0;
    reg analysis_sof = 0;
    reg analysis_eol = 0;
    reg analysis_eof = 0;
    reg [7:0] diff_threshold = 20;
    reg [1:0] object_rd_index = 0;
    reg [1:0] track_rd_index = 0;

    reg [7:0] frame_memory [0:FRAME_PIXELS-1];
    reg [2047:0] frame_dir;
    reg [2047:0] result_dir;
    reg [2047:0] frame_file;
    reg [2047:0] mask_file;
    reg [2047:0] csv_file;
    integer frame_count = 0;
    integer active_frame = 0;
    integer row, col, idx, frame_index, table_index;
    integer wait_cycles;
    integer row_gap_cycles = 1280;
    integer gap_cycle;
    integer summary_fd, objects_fd, tracks_fd, events_fd, mask_fd;

    wire mask_valid, foreground_mask, mask_sof;
    wire [7:0] mask_x, mask_y;
    wire background_learning, background_ready;
    wire [7:0] learned_frame_count;
    wire [2:0] object_count, stored_object_count;
    wire object_frame_done, object_table_valid;
    wire [5:0] object_table_label;
    wire [7:0] object_table_xmin, object_table_xmax;
    wire [7:0] object_table_ymin, object_table_ymax;
    wire [7:0] object_table_center_x, object_table_center_y;
    wire [15:0] object_table_area;
    wire [8:0] object_table_width, object_table_height;
    wire [1:0] object_table_fill_level, object_table_class;
    wire track_valid, track_visible, track_confirmed;
    wire [15:0] track_id;
    wire [7:0] track_center_x, track_center_y;
    wire [7:0] track_xmin, track_xmax, track_ymin, track_ymax;
    wire signed [8:0] track_vx, track_vy;
    wire [1:0] track_class;
    wire [2:0] track_miss_count;
    wire track_frame_done;
    wire event_valid, event_frame_done;
    wire [2:0] event_type;
    wire [15:0] event_track_id, line_cross_count;
    wire [1:0] event_track_class;
    wire run_overflow, label_overflow, raw_overrun, labeled_overflow;
    wire background_protocol_error, ccl_protocol_error;
    wire classifier_protocol_error, object_store_protocol_error;
    wire tracker_protocol_error, event_protocol_error, track_overflow;
    wire core_error;

    foreground_ccl_top #(
        .FRAME_WIDTH(FRAME_WIDTH), .FRAME_HEIGHT(FRAME_HEIGHT),
        .LEARN_FRAMES(4), .MIN_AREA(16), .CLASS_MIN_AREA(16),
        .PED_MIN_HEIGHT(8), .VEH_MIN_WIDTH(8),
        .ZONE_X_MIN(80), .ZONE_X_MAX(175),
        .ZONE_Y_MIN(50), .ZONE_Y_MAX(143),
        .LINE_X(128), .DWELL_FRAMES(30)
    ) dut (
        .clk(clk), .rst_n(rst_n),
        .analysis_valid(analysis_valid), .analysis_gray(analysis_gray),
        .analysis_x(analysis_x), .analysis_y(analysis_y),
        .analysis_sof(analysis_sof), .analysis_eol(analysis_eol),
        .analysis_eof(analysis_eof),
        .diff_threshold(diff_threshold),
        .background_update_enable(1'b1),
        .freeze_foreground(1'b1), .background_relearn(1'b0),
        .object_rd_index(object_rd_index), .track_rd_index(track_rd_index),
        .mask_valid(mask_valid), .foreground_mask(foreground_mask),
        .mask_x(mask_x), .mask_y(mask_y), .mask_sof(mask_sof),
        .background_learning(background_learning),
        .background_ready(background_ready),
        .learned_frame_count(learned_frame_count),
        .object_count(object_count), .object_frame_done(object_frame_done),
        .object_table_valid(object_table_valid),
        .object_table_label(object_table_label),
        .object_table_xmin(object_table_xmin),
        .object_table_xmax(object_table_xmax),
        .object_table_ymin(object_table_ymin),
        .object_table_ymax(object_table_ymax),
        .object_table_center_x(object_table_center_x),
        .object_table_center_y(object_table_center_y),
        .object_table_area(object_table_area),
        .object_table_width(object_table_width),
        .object_table_height(object_table_height),
        .object_table_fill_level(object_table_fill_level),
        .object_table_class(object_table_class),
        .stored_object_count(stored_object_count),
        .track_valid(track_valid), .track_visible(track_visible),
        .track_confirmed(track_confirmed), .track_id(track_id),
        .track_center_x(track_center_x), .track_center_y(track_center_y),
        .track_xmin(track_xmin), .track_xmax(track_xmax),
        .track_ymin(track_ymin), .track_ymax(track_ymax),
        .track_vx(track_vx), .track_vy(track_vy),
        .track_class(track_class), .track_miss_count(track_miss_count),
        .track_frame_done(track_frame_done),
        .event_valid(event_valid), .event_type(event_type),
        .event_track_id(event_track_id),
        .event_track_class(event_track_class),
        .line_cross_count(line_cross_count),
        .event_frame_done(event_frame_done),
        .run_overflow(run_overflow), .label_overflow(label_overflow),
        .raw_overrun(raw_overrun), .labeled_overflow(labeled_overflow),
        .background_protocol_error(background_protocol_error),
        .ccl_protocol_error(ccl_protocol_error),
        .classifier_protocol_error(classifier_protocol_error),
        .object_store_protocol_error(object_store_protocol_error),
        .tracker_protocol_error(tracker_protocol_error),
        .event_protocol_error(event_protocol_error),
        .track_overflow(track_overflow),
        .core_error(core_error)
    );

    always @(posedge clk) begin
        if (event_valid)
            $fwrite(events_fd, "%0d,%0d,%0d,%0d,%0d\n",
                    active_frame, event_type, event_track_id,
                    event_track_class, line_cross_count);
        if (mask_valid && mask_fd != 0)
            $fwrite(mask_fd, "%02x\n", foreground_mask ? 8'hff : 8'h00);
    end

    task open_result_files;
        begin
            $sformat(csv_file, "%0s/frame_summary.csv", result_dir);
            summary_fd = $fopen(csv_file, "w");
            $sformat(csv_file, "%0s/objects.csv", result_dir);
            objects_fd = $fopen(csv_file, "w");
            $sformat(csv_file, "%0s/tracks.csv", result_dir);
            tracks_fd = $fopen(csv_file, "w");
            $sformat(csv_file, "%0s/events.csv", result_dir);
            events_fd = $fopen(csv_file, "w");
            if (!summary_fd || !objects_fd || !tracks_fd || !events_fd)
                $fatal(1, "cannot open result CSV files under %0s", result_dir);
            $fwrite(summary_fd, "frame,background_ready,learned_frames,object_count,run_overflow,label_overflow,raw_overrun,labeled_overflow,background_protocol_error,ccl_protocol_error,classifier_protocol_error,object_store_protocol_error,tracker_protocol_error,event_protocol_error,track_overflow,core_error\n");
            $fwrite(objects_fd, "frame,slot,valid,label,class,xmin,ymin,xmax,ymax,center_x,center_y,width,height,area,fill_level\n");
            $fwrite(tracks_fd, "frame,slot,valid,visible,confirmed,id,class,xmin,ymin,xmax,ymax,center_x,center_y,vx,vy,miss_count\n");
            $fwrite(events_fd, "frame,event_type,track_id,class,line_cross_count\n");
        end
    endtask

    task send_frame;
        input integer number;
        begin
            active_frame = number;
            $sformat(frame_file, "%0s/frame_%04d.hex", frame_dir, number);
            $readmemh(frame_file, frame_memory);
            $sformat(mask_file, "%0s/mask_%04d.hex", result_dir, number);
            mask_fd = $fopen(mask_file, "w");
            if (!mask_fd)
                $fatal(1, "cannot open mask output %0s", mask_file);

            idx = 0;
            for (row = 0; row < FRAME_HEIGHT; row = row + 1) begin
                for (col = 0; col < FRAME_WIDTH; col = col + 1) begin
                    @(negedge clk);
                    analysis_valid = 1'b1;
                    analysis_gray = frame_memory[idx];
                    analysis_x = col[7:0];
                    analysis_y = row[7:0];
                    analysis_sof = (row == 0 && col == 0);
                    analysis_eol = 1'b0;
                    analysis_eof = 1'b0;
                    idx = idx + 1;
                end
                @(negedge clk);
                analysis_valid = 1'b0;
                analysis_sof = 1'b0;
                analysis_eol = 1'b1;
                analysis_eof = 1'b0;
                @(negedge clk);
                analysis_eol = 1'b0;
                // The 5x vertical sampler skips four complete 1280-pixel
                // source rows before the next analysis row. Preserve that
                // processing window so CCL throughput matches the board.
                for (gap_cycle = 0; gap_cycle < row_gap_cycles;
                     gap_cycle = gap_cycle + 1)
                    @(negedge clk);
            end
            // The real 5x adapter emits the final sampled-row EOL before the
            // source-frame EOF. Keep EOF on its own empty cycle as required by
            // background_model and run_detector.
            @(negedge clk);
            analysis_eof = 1'b1;
            @(negedge clk);
            analysis_eof = 1'b0;
            $fclose(mask_fd);
            mask_fd = 0;

            wait_cycles = 0;
            while (!event_frame_done && wait_cycles < 1000000) begin
                @(posedge clk);
                wait_cycles = wait_cycles + 1;
            end
            if (!event_frame_done)
                $fatal(1, "frame %0d processing timeout", number);

            $fwrite(summary_fd, "%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d\n",
                    number, background_ready, learned_frame_count,
                    stored_object_count, run_overflow, label_overflow,
                    raw_overrun, labeled_overflow,
                    background_protocol_error, ccl_protocol_error,
                    classifier_protocol_error, object_store_protocol_error,
                    tracker_protocol_error, event_protocol_error,
                    track_overflow, core_error);

            for (table_index = 0; table_index < 4; table_index = table_index + 1) begin
                object_rd_index = table_index[1:0];
                @(negedge clk);
                $fwrite(objects_fd, "%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d\n",
                        number, table_index, object_table_valid,
                        object_table_label, object_table_class,
                        object_table_xmin, object_table_ymin,
                        object_table_xmax, object_table_ymax,
                        object_table_center_x, object_table_center_y,
                        object_table_width, object_table_height,
                        object_table_area, object_table_fill_level);
                track_rd_index = table_index[1:0];
                @(negedge clk);
                $fwrite(tracks_fd, "%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d\n",
                        number, table_index, track_valid, track_visible,
                        track_confirmed, track_id, track_class,
                        track_xmin, track_ymin, track_xmax, track_ymax,
                        track_center_x, track_center_y,
                        $signed(track_vx), $signed(track_vy),
                        track_miss_count);
            end
            @(negedge clk);
        end
    endtask

    initial begin
        if (!$value$plusargs("FRAME_DIR=%s", frame_dir))
            $fatal(1, "missing +FRAME_DIR=<directory>");
        if (!$value$plusargs("RESULT_DIR=%s", result_dir))
            $fatal(1, "missing +RESULT_DIR=<directory>");
        if (!$value$plusargs("FRAMES=%d", frame_count) || frame_count <= 0)
            $fatal(1, "missing or invalid +FRAMES=<count>");
        if (!$value$plusargs("THRESHOLD=%d", diff_threshold))
            diff_threshold = 8'd20;
        if (!$value$plusargs("ROW_GAP=%d", row_gap_cycles))
            row_gap_cycles = 1280;
        if (row_gap_cycles < 0)
            $fatal(1, "ROW_GAP must not be negative");

        summary_fd = 0; objects_fd = 0; tracks_fd = 0;
        events_fd = 0; mask_fd = 0;
        open_result_files();
        repeat (5) @(posedge clk);
        @(negedge clk); rst_n = 1'b1;

        for (frame_index = 0; frame_index < frame_count; frame_index = frame_index + 1) begin
            send_frame(frame_index);
            $display("FRAME %0d/%0d complete, objects=%0d, error=%0d",
                     frame_index + 1, frame_count, stored_object_count, core_error);
        end

        $fclose(summary_fd); $fclose(objects_fd);
        $fclose(tracks_fd); $fclose(events_fd);
        $display("PASS: video replay completed, frames=%0d", frame_count);
        $finish;
    end
endmodule
