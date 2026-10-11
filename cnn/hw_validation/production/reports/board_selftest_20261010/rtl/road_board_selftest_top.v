`timescale 1ns / 1ps

// 独立首板自检顶层：不包含摄像头、DDR、完整模型ROM或识别框。
module road_board_selftest_top (
    input i_sys_clk,                     // 板载50MHz，实物仍待核实
    input i_rstn,                        // 外部低有效复位，立即取消
    output o_tmds_blue_p,                // 官方HDMI通道0正端
    output o_tmds_green_p,               // 官方HDMI通道1正端
    output o_tmds_red_p,                 // 官方HDMI通道2正端
    output o_tmds_clock_p                // 官方HDMI时钟正端
);
    //--------------模块实例化信号--------------//
    wire clk_compute;
    wire clk_pixel;
    wire clk_serial;
    wire pll_locked;
    wire raw_rstn;
    wire core_rstn;
    wire rx_valid;
    wire [15:0] rx_data;
    wire rx_ready;
    wire tx_valid;
    wire [15:0] tx_data;
    wire tx_ready;
    wire [255:0] payload;
    wire vtc_vs;
    wire vtc_de;
    wire display_vs;
    wire display_de;
    wire [23:0] display_rgb;

    //---------------寄存器信号-----------------//
    reg reg_compute_meta;
    reg reg_compute_release;
    reg reg_pixel_meta;
    reg reg_pixel_release;

    //---------------其他信号连线---------------//
    assign raw_rstn = i_rstn & pll_locked;

    //---------------主要任务处理区域---------------//
    // 外部复位不等待PLL失锁；每个使用域分别两级同步释放。
    always @(posedge clk_compute or negedge raw_rstn) begin
        if (!raw_rstn) begin
            reg_compute_meta <= 1'b0;
            reg_compute_release <= 1'b0;
        end else begin
            reg_compute_meta <= 1'b1;
            reg_compute_release <= reg_compute_meta;
        end
    end
    always @(posedge clk_pixel or negedge raw_rstn) begin
        if (!raw_rstn) begin
            reg_pixel_meta <= 1'b0;
            reg_pixel_release <= 1'b0;
        end else begin
            reg_pixel_meta <= 1'b1;
            reg_pixel_release <= reg_pixel_meta;
        end
    end

    //----------------模块实例化----------------//
    PLL u_PLL (
        .refclk(i_sys_clk), .reset(~i_rstn), .clk0_out(clk_compute), .clk1_out(),
        .clk4_out(clk_pixel), .clk5_out(clk_serial), .lock(pll_locked)
    );
    road_board_selftest_player road_board_selftest_player_Inst (
        .i_clk(clk_compute), .i_rstn(reg_compute_release), .i_rx_ready(rx_ready),
        .i_tx_valid(tx_valid), .i_tx_data(tx_data), .o_rx_valid(rx_valid),
        .o_rx_data(rx_data), .o_tx_ready(tx_ready), .o_core_rstn(core_rstn), .o_payload(payload)
    );
    road_dynamic_overlap_low_io_top road_dynamic_overlap_low_io_top_Inst (
        .i_clk(clk_compute), .i_rstn(core_rstn), .i_rx_valid(rx_valid), .i_rx_data(rx_data),
        .o_rx_ready(rx_ready), .o_tx_valid(tx_valid), .o_tx_data(tx_data), .i_tx_ready(tx_ready)
    );
    uivtc #(
        .H_ActiveSize(1280), .H_FrameSize(1650), .H_SyncStart(1390), .H_SyncEnd(1430),
        .V_ActiveSize(720), .V_FrameSize(750), .V_SyncStart(725), .V_SyncEnd(730)
    ) u_hdmi_vtc (
        .I_vtc_rstn(reg_pixel_release), .I_vtc_clk(clk_pixel), .O_vtc_vs(vtc_vs),
        .O_vtc_hs(), .O_vtc_de_valid(vtc_de), .O_vtc_user(), .O_vtc_last()
    );
    road_selftest_display road_selftest_display_Inst (
        .i_clk(clk_compute), .i_rstn(reg_compute_release), .i_payload(payload),
        .i_pixel_clk(clk_pixel), .i_pixel_rstn(reg_pixel_release), .i_vsync(vtc_vs), .i_de(vtc_de),
        .o_rgb(display_rgb), .o_vsync(display_vs), .o_de(display_de), .o_active_payload()
    );
    // 沿官方RGB模式；未用音频/EDID不接板外，不修改官方IP内部。
    hdmi_tx u_hdmi_tx (
        .I_pixel_clk(clk_pixel), .I_serial_clk(clk_serial), .I_rst(~reg_pixel_release),
        .I_key_in(1'b0), .I_edid_read_trig(1'b0), .O_edid_read_valid(), .O_edid_read_data(),
        .I_video_rgb_enable(1'b1), .I_video_in_de(display_de), .I_video_in_vs(display_vs),
        .I_video_in_user(1'b0), .I_video_in_valid(1'b0), .I_video_in_last(1'b0),
        .O_video_in_ready(), .I_video_in_data(display_rgb), .I_audio_valid(1'b0),
        .I_audio_left_data(24'd0), .I_audio_right_data(24'd0), .I_i2s_BCLK(1'b0),
        .I_i2s_LRCK(1'b0), .I_i2s_DOUT(1'b0), .O_ddc_scl(), .IO_ddc_sda(),
        .O_hdmi_clk_p(), .O_hdmi_tx_p(), .O_tmds_ch0_p(o_tmds_blue_p),
        .O_tmds_ch1_p(o_tmds_green_p), .O_tmds_ch2_p(o_tmds_red_p), .O_tmds_clk_p(o_tmds_clock_p)
    );
endmodule
