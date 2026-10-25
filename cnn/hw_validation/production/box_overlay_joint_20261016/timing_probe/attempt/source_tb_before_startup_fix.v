`timescale 1ns / 1ps
// Only measures existing official VTC/mixer cycle intervals, not a new video design.
module tb_official_video_budget;
    reg clk = 0;
    reg rstn = 0;
    wire vs, hs, de, user, last;
    wire mixed_vs, mixed_hs, mixed_de;
    wire [23:0] mixed_rgb;
    wire unused_read;
    reg previous_vs = 0;
    wire sof = mixed_vs && !previous_vs;
    reg sampled_de = 0;
    reg observed_de = 0;
    reg observed_vs = 0;
    integer cycle = 0;
    integer last_high_cycle = -1;
    integer blank_checks = 0;
    integer vs_rise_cycle = -1;
    integer sof_consume_cycle = -1;
    integer first_de_transition = -1;
    integer sof_checks = 0;
    integer active_width = 0;
    integer full_line_checks = 0;

    initial begin
        forever begin
            #6.667 clk = ~clk;
            #6.666 clk = ~clk;
            #6.667 clk = ~clk;
        end
    end
    initial begin
        repeat (10) @(negedge clk);
        rstn = 1;
    end

    uivtc #(.H_ActiveSize(1280), .H_FrameSize(1650), .H_SyncStart(1390), .H_SyncEnd(1430),
            .V_ActiveSize(720), .V_FrameSize(750), .V_SyncStart(725), .V_SyncEnd(730)) Vtc_Inst (
        .I_vtc_rstn(rstn), .I_vtc_clk(clk), .O_vtc_vs(vs), .O_vtc_hs(hs),
        .O_vtc_de_valid(de), .O_vtc_user(user), .O_vtc_last(last));
    hdmi_mixer #(.H_OFFSET(0), .V_OFFSET(0), .IMG_WIDTH(1280), .IMG_HEIGHT(720), .DEBUG_MODE(0)) Mixer_Inst (
        .I_clk(clk), .I_rst_n(rstn), .I_video_vsync(vs), .I_video_hsync(hs), .I_video_de(de),
        .I_video_user(user), .I_video_last(last), .I_debug_status(4'd0),
        .O_video_rd_en(unused_read), .I_video_rd_data(24'h123456),
        .O_hdmi_vsync(mixed_vs), .O_hdmi_hsync(mixed_hs), .O_hdmi_de(mixed_de), .O_hdmi_data(mixed_rgb));

    always @(posedge clk) begin
        cycle = cycle + 1;
        previous_vs <= mixed_vs;
        if (rstn && cycle > 30) begin
            if (sof) sof_consume_cycle = cycle;
            if (mixed_de && !sampled_de) begin
                if (last_high_cycle >= 0 && cycle-last_high_cycle < 1000) begin
                    if (cycle-last_high_cycle != 371) $fatal(1,"official line blank is not370 samples");
                    blank_checks = blank_checks + 1;
                end
                if (first_de_transition >= 0) begin
                    if (cycle-sof_consume_cycle != 39971) $fatal(1,"SOF-consumer to first-pixel-consumer changed got=%0d",cycle-sof_consume_cycle);
                    $display("OFFICIAL_BUDGET vs_to_de_transition=%0d sof_to_de_transition=%0d sof_to_pixel_consumption=%0d blank_samples=370", first_de_transition-vs_rise_cycle, first_de_transition-sof_consume_cycle, cycle-sof_consume_cycle);
                    first_de_transition = -1;
                    sof_checks = sof_checks + 1;
                end
            end
            if (mixed_de) begin
                active_width = active_width + 1;
                last_high_cycle = cycle;
            end else if (sampled_de) begin
                if (active_width != 1280) $fatal(1,"official active width got=%0d",active_width);
                active_width = 0;
                full_line_checks = full_line_checks + 1;
            end
            sampled_de = mixed_de;
        end
        #0.001;
        if (rstn && cycle > 30) begin
            if (mixed_vs && !observed_vs) vs_rise_cycle = cycle;
            if (mixed_de && !observed_de && vs_rise_cycle >= 0 && cycle>vs_rise_cycle) begin
                if (cycle-vs_rise_cycle != 39971) $fatal(1,"VS-to-DE transition changed got=%0d",cycle-vs_rise_cycle);
                first_de_transition = cycle;
                vs_rise_cycle = vs_rise_cycle;
            end
            observed_vs = mixed_vs;
            observed_de = mixed_de;
            if (sof_checks == 2) begin
                $display("TB_PASS_OFFICIAL_VIDEO_BUDGET blank_checks=%0d full_width_checks=%0d sof_checks=%0d",blank_checks,full_line_checks,sof_checks);
                $finish;
            end
        end
    end
    initial begin
        #40000000;
        $fatal(1,"official timing probe timeout");
    end
endmodule
