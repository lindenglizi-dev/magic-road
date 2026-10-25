`timescale 1ns / 1ps
// 测试实际DDR用户/显示域频率附近的冻结载荷协议；不是亚稳态证明。
module tb_ddr_display_cdc;
    reg clk = 0, pixel_clk = 0;
    reg rstn = 0, pixel_rstn = 0, vs = 0;
    reg [255:0] payload = 0;
    wire [255:0] active;
    reg [255:0] previous_hold, expected_active = 0;
    reg pending, capture;
    realtime changed_at = 0, age, minimum_age = 1000000;
    integer transfers = 0, iteration;
    always #3.75 clk = ~clk;
    always #6.667 pixel_clk = ~pixel_clk;

    road_selftest_display dut (.i_clk(clk), .i_rstn(rstn), .i_payload(payload),
        .i_pixel_clk(pixel_clk), .i_pixel_rstn(pixel_rstn), .i_vsync(vs), .i_de(1'b0),
        .o_rgb(), .o_vsync(), .o_de(), .o_active_payload(active));

    always @(posedge clk) begin
        previous_hold = dut.reg_hold_payload;
        pending = dut.reg_request != dut.reg_ack_sync;
        #0.1;
        if (rstn && pending && dut.reg_hold_payload !== previous_hold)
            $fatal(1, "Frozen payload changed before acknowledgement");
        if (rstn && dut.reg_hold_payload !== previous_hold) changed_at = $realtime;
    end
    always @(posedge pixel_clk) begin
        capture = pixel_rstn && vs && !dut.reg_vsync_previous &&
                  (dut.reg_request_sync != dut.reg_acknowledge);
        if (!pixel_rstn) expected_active = 0;
        else if (capture) begin
            expected_active = dut.reg_hold_payload;
            age = $realtime - changed_at;
            if (age < 26.5) $fatal(1, "Bundled payload sampled before two target cycles: %f", age);
            if (age < minimum_age) minimum_age = age;
            transfers = transfers + 1;
        end
        #0.2;
        if (active !== expected_active) $fatal(1, "Torn payload or mid-frame update");
    end
    initial begin
        #31; rstn = 1;
        #17; pixel_rstn = 1;
        for (iteration = 0; iteration < 64; iteration = iteration + 1) begin
            @(negedge clk);
            payload = {$random, $random, $random, $random, $random, $random, $random, $random};
            repeat ((iteration % 9)+1) @(negedge pixel_clk);
            vs = 1;
            @(negedge pixel_clk); vs = 0;
            if (iteration == 31) begin
                #0.7; rstn = 0; pixel_rstn = 0;
                #0.2; if (active !== 0) $fatal(1, "Reset leaked snapshot");
                #25; rstn = 1;
                #3; pixel_rstn = 1;
            end
        end
        @(negedge clk); payload = {2'd1, 254'd987};
        repeat (4) begin
            repeat (8) @(negedge pixel_clk);
            vs = 1;
            @(negedge pixel_clk); vs = 0;
        end
        #1;
        if (active !== payload || transfers < 20) $fatal(1, "Final snapshot lost");
        $display("DDR_DISPLAY_CDC_PASS captures=%0d minimum_payload_age_ns=%f", transfers, minimum_age);
        $finish;
    end
    initial begin
        #100000;
        $fatal(1, "CDC test timeout");
    end
endmodule
