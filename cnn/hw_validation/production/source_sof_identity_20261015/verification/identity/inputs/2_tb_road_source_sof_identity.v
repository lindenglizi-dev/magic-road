`timescale 1ns / 1ps
// Selfchecking digital contract; physical CDC timing is outside this simulation.
module tb_road_source_sof_identity;
    reg time_clk = 0;
    reg camera_clk = 0;
    reg time_clock_run = 1;
    reg camera_clock_run = 1;
    reg rstn = 0;
    reg camera_sof = 1;
    reg capture_credit = 1;
    reg desc_ready = 0;
    reg publish_enable = 1;
    reg [31:0] epoch = 32'h31;
    wire [63:0] now_ms;
    wire time_tick;
    wire frame_admit;
    wire [31:0] admit_epoch, admit_frame_id, source_frame_id;
    wire [63:0] admit_capture_ms, mirror_ms;
    wire [31:0] mirror_epoch;
    wire mirror_valid, event_busy, frame_skip, wrap_fault, desc_valid;
    wire [127:0] desc_payload;
    reg [127:0] expected [0:127];
    reg [127:0] stalled_payload;
    reg stalled_previous = 0;
    integer enqueue = 0;
    integer dequeue = 0;
    reg [31:0] physical_count = 0;
    integer admits = 0;
    integer skips = 0;
    integer consumed = 0;
    integer stalled_edges = 0;
    integer resets = 0;
    integer timeout_edges = 0;
    integer case_id = 0;
    integer count_before;
    integer held_time_edges = 0;
    integer held_event_edges = 0;
    reg [95:0] held_time_before;
    reg [127:0] held_event_before;
    reg time_busy_before;
    reg event_busy_before;
    reg [63:0] old_mirror;
    reg [127:0] hold_descriptor;

    always #5 if (time_clock_run) time_clk = !time_clk;
    initial begin
        #3.4;
        forever #8.333 if (camera_clock_run) camera_clk = !camera_clk;
    end

    // Source held buses cannot change before their two-stage returned ack.
    always @(posedge time_clk) begin
        held_time_before = dut.reg_time_payload;
        time_busy_before = dut.flag_time_request != dut.reg_time_acknowledge_sync[1];
        #1;
        if (rstn && time_busy_before) begin
            if (dut.reg_time_payload !== held_time_before)
                $fatal(1, "held96 changed before returned acknowledgement");
            held_time_edges = held_time_edges + 1;
        end
    end
    always @(posedge camera_clk) begin
        held_event_before = dut.reg_event_payload;
        event_busy_before = event_busy;
        #1;
        if (rstn && event_busy_before) begin
            if (dut.reg_event_payload !== held_event_before)
                $fatal(1, "held128 changed before returned acknowledgement");
            held_event_edges = held_event_edges + 1;
        end
    end

    // This frozen module is the only absolute millisecond counter.
    road_time_snapshot time_source (
        .i_src_clk(time_clk), .i_dst_clk(camera_clk), .i_rstn(rstn),
        .i_src_epoch(epoch), .o_src_now_ms(now_ms), .o_src_tick(time_tick),
        .o_src_busy(), .o_dst_now_ms(), .o_dst_epoch(),
        .o_dst_time_valid(), .o_dst_update()
    );
    road_source_sof_identity dut (
        .i_time_clk(time_clk), .i_camera_clk(camera_clk), .i_rstn(rstn),
        .i_time_now_ms(now_ms), .i_time_tick(time_tick && publish_enable),
        .i_time_epoch(epoch), .i_camera_sof(camera_sof),
        .i_capture_credit(capture_credit), .o_frame_admit(frame_admit),
        .o_admit_epoch(admit_epoch), .o_admit_frame_id(admit_frame_id),
        .o_admit_capture_ms(admit_capture_ms), .o_source_frame_id(source_frame_id),
        .o_mirror_ms(mirror_ms), .o_mirror_epoch(mirror_epoch),
        .o_mirror_valid(mirror_valid), .o_event_busy(event_busy),
        .o_frame_skip(frame_skip), .o_wrap_fault(wrap_fault),
        .o_desc_valid(desc_valid), .i_desc_ready(desc_ready),
        .o_desc_payload(desc_payload)
    );

    // Every actual destination transfer must equal the source-edge tuple.
    always @(posedge time_clk) begin
        if (rstn) begin
            if (stalled_previous && (desc_valid !== 1 || desc_payload !== stalled_payload))
                $fatal(1, "descriptor changed while valid stalled case=%0d", case_id);
            if (desc_valid) begin
                if (dequeue >= enqueue || desc_payload !== expected[dequeue])
                    $fatal(1, "descriptor tuple mismatch case=%0d index=%0d got=%h expected=%h", case_id, dequeue, desc_payload, expected[dequeue]);
                if (desc_ready) begin
                    dequeue = dequeue + 1;
                    consumed = consumed + 1;
                end else stalled_edges = stalled_edges + 1;
            end
            stalled_previous = desc_valid && !desc_ready;
            stalled_payload = desc_payload;
        end else stalled_previous = 0;
    end

    task reset_common;
        input high_sof;
        begin
            @(negedge camera_clk);
            rstn = 0;
            camera_sof = high_sof;
            epoch = epoch + 1;
            enqueue = 0;
            dequeue = 0;
            physical_count = 0;
            stalled_previous = 0;
            resets = resets + 1;
            repeat (5) @(negedge camera_clk);
            rstn = 1;
            repeat (8) @(negedge camera_clk);
            if (source_frame_id !== 0 || desc_valid !== 0 || event_busy !== 0 || mirror_valid !== 0)
                $fatal(1, "common reset did not cancel identity/time case=%0d", case_id);
            if (high_sof) begin
                repeat (8) @(negedge camera_clk);
                if (source_frame_id !== 0 || frame_admit !== 0)
                    $fatal(1, "SOF high across reset created phantom frame");
            end
            camera_sof = 0;
            repeat (3) @(negedge camera_clk);
        end
    endtask

    task sof;
        input expect_admit;
        input integer high_edges;
        reg [127:0] tuple;
        integer held;
        begin
            @(negedge camera_clk);
            camera_sof = 1;
            #1;
            if (frame_admit !== expect_admit)
                $fatal(1, "pre-edge admit mismatch case=%0d expected=%0d got=%b mirror=%b busy=%b credit=%b", case_id, expect_admit, frame_admit, mirror_valid, event_busy, capture_credit);
            if (expect_admit) begin
                tuple = {admit_epoch, admit_frame_id, admit_capture_ms};
                if (admit_epoch !== epoch || admit_frame_id !== physical_count + 1 || admit_capture_ms > now_ms || admit_capture_ms !== mirror_ms)
                    $fatal(1, "admission identity/time not source anchored case=%0d", case_id);
                expected[enqueue] = tuple;
                enqueue = enqueue + 1;
                admits = admits + 1;
                // Stamping an older mirror may only increase snapshot-based age.
                if ((now_ms - admit_capture_ms + 4) < 4)
                    $fatal(1, "age underflow at admission");
            end else skips = skips + 1;
            @(posedge camera_clk);
            if (physical_count != 32'hffffffff) physical_count = physical_count + 1;
            #1;
            if (source_frame_id !== physical_count || frame_skip !== !expect_admit)
                $fatal(1, "physical SOF not counted/skipped case=%0d got=%0d wanted=%0d", case_id, source_frame_id, physical_count);
            for (held = 1; held < high_edges; held = held + 1) begin
                @(posedge camera_clk);
                #1;
                if (source_frame_id !== physical_count || frame_admit !== 0)
                    $fatal(1, "held-high SOF counted more than once case=%0d", case_id);
            end
            @(negedge camera_clk);
            camera_sof = 0;
            repeat (2) @(negedge camera_clk);
        end
    endtask

    task await_idle;
        integer waited;
        begin
            waited = 0;
            while (event_busy || desc_valid) begin
                @(negedge camera_clk);
                waited = waited + 1;
                if (waited > 100) $fatal(1, "event ack did not resume case=%0d", case_id);
            end
        end
    endtask

    initial begin
        case_id = 1;
        reset_common(1);
        sof(0, 5); // No first mirror; SOF is not qualified by pixel valid.
        sof(0, 1);
        wait (dut.flag_time_capture_wait);
        sof(0, 1); // The first mirror arriving on this SOF edge is not eligible.
        if (!mirror_valid) $fatal(1, "same-edge first mirror did not complete");
        @(negedge camera_clk);
        case_id = 2;
        capture_credit = 0;
        sof(0, 1);
        capture_credit = 1;
        sof(1, 5);
        wait (desc_valid);
        hold_descriptor = desc_payload;
        old_mirror = mirror_ms;
        // Stall actual descriptor ready over a real millisecond publication.
        wait (mirror_ms != old_mirror);
        if (!event_busy || desc_payload !== hold_descriptor)
            $fatal(1, "event backpressure blocked or corrupted independent mirror");
        repeat (20) @(negedge time_clk);
        sof(0, 1); // Outstanding descriptor inhibits capture, never frame count.
        sof(0, 1);
        if (desc_payload !== hold_descriptor || !event_busy)
            $fatal(1, "source payload changed under descriptor backpressure");
        @(negedge time_clk);
        desc_ready = 1;
        await_idle;
        sof(1, 1);
        await_idle;

        case_id = 21;
        // Completion and SOF share an edge, but admission must use old mirror.
        wait (dut.flag_time_capture_wait);
        old_mirror = mirror_ms;
        sof(1, 1);
        if (expected[enqueue-1][63:0] !== old_mirror || mirror_ms <= old_mirror)
            $fatal(1, "same-edge mirror update replaced admission's old mirror");
        await_idle;

        case_id = 3;
        // Reset while destination holds valid, then no old tuple may reappear.
        desc_ready = 0;
        sof(1, 1);
        wait (desc_valid);
        reset_common(0);
        desc_ready = 1;
        repeat (40) @(negedge time_clk);
        if (desc_valid) $fatal(1, "old held descriptor survived reset");

        case_id = 31;
        // Cancel a mirror copy in its stable wait phase.
        wait (dut.flag_time_capture_wait);
        reset_common(0);
        repeat (40) @(negedge time_clk);
        if (mirror_valid || desc_valid) $fatal(1, "pending mirror survived reset");

        case_id = 32;
        wait (mirror_valid);
        desc_ready = 0;
        sof(1, 1);
        // Event may still be in synchronizer/copy stage at common reset.
        reset_common(0);
        desc_ready = 1;
        repeat (40) @(negedge time_clk);
        if (desc_valid) $fatal(1, "pending event survived reset");

        case_id = 4;
        wait (dut.flag_time_capture_wait);
        @(negedge camera_clk);
        publish_enable = 0;
        @(posedge camera_clk);
        #1;
        if (!mirror_valid || dut.cnt_mirror_silence !== 0)
            $fatal(1, "mirror capture did not reset watchdog");
        old_mirror = mirror_ms;
        timeout_edges = 0;
        repeat (120000) begin
            @(posedge camera_clk);
            #1;
            timeout_edges = timeout_edges + 1;
            if (mirror_ms !== old_mirror) $fatal(1, "publication disabled but mirror changed");
            if (!mirror_valid) $fatal(1, "mirror expired early edge=%0d", timeout_edges);
        end
        @(posedge camera_clk);
        #1;
        timeout_edges = timeout_edges + 1;
        if (mirror_valid) $fatal(1, "mirror did not expire on edge120001");
        sof(0, 1);
        publish_enable = 1;
        wait (mirror_valid);
        sof(1, 1);
        await_idle;

        case_id = 5;
        // A genuine time-clock stop also expires in camera cycles; restart resumes.
        @(negedge time_clk);
        time_clock_run = 0;
        repeat (120010) @(negedge camera_clk);
        if (mirror_valid !== 0) $fatal(1, "time-clock stop did not expire mirror");
        sof(0, 1);
        time_clock_run = 1;
        wait (mirror_valid);
        sof(1, 1);
        await_idle;

        case_id = 6;
        // Camera stop is not a freshness guarantee; test only held96 stability.
        @(negedge camera_clk);
        camera_clock_run = 0;
        #2100000;
        camera_clock_run = 1;
        wait (dut.flag_time_capture_wait);
        repeat (5) @(negedge camera_clk);
        if (!mirror_valid) $fatal(1, "camera resumed without completing held snapshot");

        case_id = 7;
        // ARTIFICIAL STATE FORCING: reach uint32 wrap without 4billion frames.
        @(negedge camera_clk);
        dut.source_frame_id_o = 32'hfffffffe;
        physical_count = 32'hfffffffe;
        sof(1, 1);
        await_idle;
        sof(0, 1);
        if (!wrap_fault || source_frame_id !== 32'hffffffff)
            $fatal(1, "counter wrap failed to saturate/set sticky fault");
        sof(0, 1);
        if (!wrap_fault || source_frame_id !== 32'hffffffff)
            $fatal(1, "wrap fault did not remain sticky");
        reset_common(0);
        wait (mirror_valid);
        sof(1, 1);
        await_idle;
        $display("TB_PASS_IDENTITY admits=%0d consumed=%0d skips=%0d stalled_edges=%0d held96_edges=%0d held128_edges=%0d resets=%0d timeout_observed=%0d artificial_wrap_forcing=1", admits, consumed, skips, stalled_edges, held_time_edges, held_event_edges, resets, timeout_edges);
        $finish;
    end

    initial begin
        #40000000;
        $fatal(1, "identity simulation watchdog case=%0d", case_id);
    end
endmodule
