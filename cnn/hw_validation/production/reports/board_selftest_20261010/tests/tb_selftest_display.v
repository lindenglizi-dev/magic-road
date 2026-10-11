`timescale 1ns / 1ps
// 不同相位时钟验证冻结载荷和VS边界；不代表亚稳态或HDMI PHY板测。
module tb_selftest_display;
    reg clk = 0, pixel_clk = 0;
    always #5 clk = ~clk;
    always #7 pixel_clk = ~pixel_clk;
    reg rstn = 0, pixel_rstn = 0, vs = 0, de = 0;
    reg [255:0] payload = 0;
    wire [255:0] active;
    wire [23:0] rgb;
    wire out_vs, out_de;
    reg [255:0] previous_active = 0, previous_hold = 0;
    reg old_pending, allowed_change;
    integer transfers = 0;
    integer x_ref = 0, y_ref = 0, pixel_checks = 0;
    reg last_vs_ref = 0, last_de_ref = 0;
    reg [23:0] expected_rgb;
    reg [19:0] glyph;
    road_selftest_display dut (.i_clk(clk), .i_rstn(rstn), .i_payload(payload),
        .i_pixel_clk(pixel_clk), .i_pixel_rstn(pixel_rstn), .i_vsync(vs), .i_de(de),
        .o_rgb(rgb), .o_vsync(out_vs), .o_de(out_de), .o_active_payload(active));

    always @(posedge clk) begin
        old_pending = dut.reg_request != dut.reg_ack_sync;
        previous_hold = dut.reg_hold_payload;
        #1;
        if (rstn && old_pending && dut.reg_hold_payload !== previous_hold) $fatal(1, "Payload changed before acknowledgement");
    end
    always @(posedge pixel_clk) begin
        allowed_change = vs && !dut.reg_vsync_previous;
        case ((y_ref / 8) % 8)
            0: glyph = 20'b11110111100111011110;
            1, 2: glyph = 20'b00100100001000000100;
            3: glyph = 20'b00100111000110000100;
            4, 5: glyph = 20'b00100100000001000100;
            6: glyph = 20'b00100111101110000100;
            default: glyph = 0;
        endcase
        case (active[255:254])
            1: expected_rgb = 24'h00c040;
            2: expected_rgb = 24'hd02020;
            default: expected_rgb = 24'hd0a000;
        endcase
        if (y_ref < 56 && x_ref < 160) expected_rgb = glyph[19-x_ref/8] ? 24'hffffff : 24'h502080;
        if (y_ref >= 80 && y_ref < 112 && x_ref < 1024) expected_rgb = active[255-x_ref/4] ? 24'hffffff : 24'h000000;
        if (y_ref < 64 && x_ref >= 1152) expected_rgb = dut.cnt_frames[4] ? 24'h4080ff : 24'h102040;
        if (!de) expected_rgb = 0;
        if (!pixel_rstn || (vs && !last_vs_ref)) begin x_ref = 0; y_ref = 0; end
        else if (de) x_ref = x_ref + 1;
        else begin x_ref = 0; if (last_de_ref) y_ref = y_ref + 1; end
        last_vs_ref = vs; last_de_ref = de;
        #1;
        if (pixel_rstn && active !== previous_active && !allowed_change) $fatal(1, "Display changed midframe");
        if (pixel_rstn && (out_vs !== vs || out_de !== de)) $fatal(1, "RGB timing registers differ");
        if (pixel_rstn && rgb !== expected_rgb) $fatal(1, "RGB coordinate mismatch x=%0d y=%0d expected=%h got=%h", x_ref, y_ref, expected_rgb, rgb);
        if (pixel_rstn) pixel_checks = pixel_checks + 1;
        previous_active = active;
    end

    task frame_boundary;
        begin
            repeat (8) @(negedge pixel_clk);
            vs = 1; de = 0;
            @(negedge pixel_clk); vs = 0;
            repeat (8) @(negedge pixel_clk);
            transfers = transfers + 1;
        end
    endtask
    task draw_region;
        integer row;
        begin
            for (row = 0; row < 114; row = row + 1) begin
                @(negedge pixel_clk); de = 1;
                repeat (1280) @(negedge pixel_clk);
                de = 0;
                repeat (2) @(negedge pixel_clk);
            end
        end
    endtask
    initial begin
        #31; rstn = 1;
        #17; pixel_rstn = 1;
        payload = {2'd0, 254'd123};
        repeat (5) @(negedge clk);
        payload = {2'd1, 254'd456}; // 前一快照未确认时终态仍必须最终送达。
        frame_boundary;
        frame_boundary;
        frame_boundary;
        if (active !== payload) $fatal(1, "Terminal snapshot lost");
        de = 1; repeat (20) @(negedge pixel_clk); de = 0;
        payload = {2'd2, 254'd789};
        repeat (8) @(negedge clk);
        #2; rstn = 0; pixel_rstn = 0;
        #1; if (active !== 256'd0 || out_de) $fatal(1, "Reset leaked old display");
        repeat (5) @(negedge clk);
        payload = {2'd1, 254'd987}; rstn = 1;
        #3; pixel_rstn = 1;
        frame_boundary;
        frame_boundary;
        if (active !== payload) $fatal(1, "Recovery snapshot lost");
        draw_region;
        payload = {2'd2, 254'd789};
        frame_boundary; frame_boundary;
        draw_region;
        $display("TB_PASS_SELFTEST_DISPLAY boundaries=%0d pixel_checks=%0d final=%h", transfers, pixel_checks, active);
        $finish;
    end
endmodule
