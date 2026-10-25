`timescale 1ns / 1ps

// Company: RoadYOLO project
// Engineer: Codex
// Create Date: 2026-10-13
// Module Name: road_ddr_selftest_top
// Description: Dedicated DDR experiment with the board-proven HDMI observer.
// Dependencies: Original ddr2 IP and frozen official PLL/HDMI sources.
// Version: V1.0
// 独立DDR实验：无摄像头、CNN、Flash控制或其他DDR客户。
module road_ddr_selftest_top (
    input i_sys_clk,                       // C4板载50MHz
    input i_rstn,                          // C7按键同时复位DDR和测试器
    output o_tmds_blue_p,                  // HDMI1蓝色正端
    output o_tmds_green_p,                 // HDMI1绿色正端
    output o_tmds_red_p,                   // HDMI1红色正端
    output o_tmds_clock_p,                 // HDMI1时钟正端
    output [0:0] ddr_ck_p,                 // 原厂IP封装内DDR专用端口
    output [0:0] ddr_ck_n,                 // 沿原厂IP固定物理位置
    output [0:0] ddr_cke,                  // DDR时钟使能
    output [0:0] ddr_odt,                  // DDR终端控制
    output [0:0] ddr_cs_n,                 // DDR片选
    output [0:0] ddr_ras_n,                // DDR行命令
    output [0:0] ddr_cas_n,                // DDR列命令
    output [0:0] ddr_we_n,                 // DDR写命令
    output [1:0] ddr_ba,                   // DDR bank地址
    output [12:0] ddr_addr,                // DDR行列复用地址
    inout [1:0] ddr_dqs_p,                 // DDR双向差分选通
    inout [1:0] ddr_dqs_n,                 // DDR双向差分选通负端
    inout [15:0] ddr_dq,                   // DDR物理数据总线
    inout [1:0] ddr_dm                     // DDR数据掩码物理端口
);
    //-------------模块实例化信号-------------//
    wire clk_ref;                         // DDR原厂要求100MHz参考
    wire clk_pixel;                       // 已验证HDMI 75MHz像素时钟
    wire clk_serial;                      // 已验证HDMI 375MHz串行时钟
    wire pll_locked;                      // 板级PLL锁定状态
    wire raw_rstn;                        // 立即断言全部复位
    wire dhi_clk;                         // 原厂用户侧约133.33MHz
    wire ddrphy_rst_n;                    // 原厂用户域复位许可
    wire ddrphy_ready;                    // 原厂初始化状态
    wire user_raw_rstn;                   // 受DDR内部复位共同约束
    wire [24:0] awaddr;                    // 独占测试写地址
    wire awvalid;                         // 写地址有效
    wire awready;                         // 原厂真实AW接受
    wire [127:0] wdata;                    // 全位宽动态测试字
    wire [15:0] wstrb;                     // 原生高有效屏蔽，零为全写
    wire wvalid;                          // 写字有效
    wire wlast;                           // 单拍写尾
    wire wready;                          // 原厂真实W接受
    wire [24:0] araddr;                    // 唯一在途读地址
    wire arvalid;                         // 读地址有效
    wire arready;                         // 原厂真实AR接受
    wire [127:0] rdata;                    // 原厂真实返回，禁止期望回环
    wire rvalid;                          // 原厂返回有效
    wire rlast;                           // 原厂返回末拍
    wire rready;                          // 唯一读槽接受许可
    wire [1:0] status;                     // 背景状态颜色
    wire [3:0] error_kind;                 // 首错类型
    wire [3:0] state_value;                // 当前实验阶段
    wire [3:0] writes;                     // 写对接受计数
    wire [3:0] reads;                      // 正确读回计数
    wire [24:0] address;                   // 当前或首错地址
    wire [127:0] expected_data;            // 完整首错期望数据
    wire [127:0] actual_data;              // 完整首错实际数据
    wire [31:0] cycles;                    // 测试经过周期
    wire [255:0] payload;                  // 复用原有冻结载荷CDC
    wire vtc_vs;                          // HDMI帧边界
    wire vtc_de;                          // HDMI有效像素
    wire display_vs;                      // 显示模块对齐VS
    wire display_de;                      // 显示模块对齐DE
    wire [23:0] display_rgb;               // 测试状态画面

    //---------------寄存器信号---------------//
    reg reg_ref_meta;                     // 参考域复位第一级
    reg reg_ref_release;                  // 参考域复位第二级
    reg reg_user_meta;                    // DDR用户域复位第一级
    reg reg_user_release;                 // DDR用户域复位第二级
    reg reg_pixel_meta;                   // HDMI复位第一级
    reg reg_pixel_release;                // HDMI复位第二级
    reg [26:0] cnt_page;                   // 在完整期望字与实际字之间翻页

    //---------------其他信号连线---------------//
    assign raw_rstn = i_rstn && pll_locked; // 外部按键立即取消全部客户和IP
    assign user_raw_rstn = raw_rstn && ddrphy_rst_n; // 不早于原厂用户域复位释放
    assign payload = {status, cnt_page[26], state_value, error_kind, writes, reads,
                      address, cycles, 52'h4444523254455,
                      (cnt_page[26] ? actual_data : expected_data)}; // 256位含DDR2标记及完整字

    //---------------主要任务处理区域---------------//
    // 各域分别异步断言、两拍同步释放；不复制同步器首级。
    always @(posedge clk_ref or negedge raw_rstn) begin
        if (!raw_rstn) begin
            reg_ref_meta <= 1'b0;         // 立即清除参考域许可
            reg_ref_release <= 1'b0;      // 同时复位整个DDR控制器
        end else begin
            reg_ref_meta <= 1'b1;         // 第一拍观察复位撤销
            reg_ref_release <= reg_ref_meta; // 第二拍释放
        end
    end
    always @(posedge dhi_clk or negedge user_raw_rstn) begin
        if (!user_raw_rstn) begin
            reg_user_meta <= 1'b0;        // 立即取消请求器事务
            reg_user_release <= 1'b0;     // 不保留旧请求账目
        end else begin
            reg_user_meta <= 1'b1;        // 用户域第一释放拍
            reg_user_release <= reg_user_meta; // 用户域第二释放拍
        end
    end
    always @(posedge clk_pixel or negedge raw_rstn) begin
        if (!raw_rstn) begin
            reg_pixel_meta <= 1'b0;       // 显示域立即复位
            reg_pixel_release <= 1'b0;    // 不显示旧快照
        end else begin
            reg_pixel_meta <= 1'b1;       // 显示第一释放拍
            reg_pixel_release <= reg_pixel_meta; // 显示第二释放拍
        end
    end
    always @(posedge dhi_clk or negedge user_raw_rstn) begin
        if (!user_raw_rstn) begin
            cnt_page <= 27'd0;           // 先显示期望字页
        end else begin
            cnt_page <= cnt_page + 27'd1; // 约每0.50s切换一次完整128位页
        end
    end

    //----------------模块实例化----------------//
    PLL u_PLL (
        .refclk(i_sys_clk), .reset(~i_rstn), .clk0_out(clk_ref), .clk1_out(),
        .clk4_out(clk_pixel), .clk5_out(clk_serial), .lock(pll_locked)
    );
    ddr2 u_ddr2 (
        .ref_clk(clk_ref), .sys_rst_n(reg_ref_release), .apb_pclk(clk_ref),
        .apb_prst_n(reg_ref_release), .apb_pready(), .apb_psel(1'b0),
        .apb_penable(1'b0), .apb_pwrite(1'b0), .apb_paddr(16'd0), .apb_pwdata(32'd0),
        .apb_prdata(), .dhi_clk(dhi_clk), .cfg_clk(), .cfg_rst_n(),
        .ddrphy_rst_n(ddrphy_rst_n), .ddrphy_rdy(ddrphy_ready),
        .paxi_awaddr(awaddr), .paxi_awvalid(awvalid), .paxi_awready(awready),
        .paxi_wdata(wdata), .paxi_wstrb(wstrb), .paxi_wvalid(wvalid), .paxi_wlast(wlast),
        .paxi_wready(wready), .paxi_araddr(araddr), .paxi_arvalid(arvalid), .paxi_arready(arready),
        .paxi_rdata(rdata), .paxi_rlast(rlast), .paxi_rvalid(rvalid), .paxi_rready(rready),
        .ddr_ck_p(ddr_ck_p), .ddr_ck_n(ddr_ck_n), .ddr_cke(ddr_cke), .ddr_odt(ddr_odt),
        .ddr_cs_n(ddr_cs_n), .ddr_ras_n(ddr_ras_n), .ddr_cas_n(ddr_cas_n), .ddr_we_n(ddr_we_n),
        .ddr_ba(ddr_ba), .ddr_addr(ddr_addr), .ddr_dqs_p(ddr_dqs_p),
        .ddr_dqs_n(ddr_dqs_n), .ddr_dq(ddr_dq), .ddr_dm(ddr_dm)
    );
    road_ddr_selftest road_ddr_selftest_Inst (
        .i_clk(dhi_clk), .i_rstn(reg_user_release), .i_phy_ready(ddrphy_ready),
        .i_awready(awready), .i_wready(wready), .i_arready(arready),
        .i_rvalid(rvalid), .i_rlast(rlast), .i_rdata(rdata),
        .o_awaddr(awaddr), .o_awvalid(awvalid), .o_wdata(wdata), .o_wstrb(wstrb),
        .o_wvalid(wvalid), .o_wlast(wlast), .o_araddr(araddr), .o_arvalid(arvalid), .o_rready(rready),
        .o_status(status), .o_error(error_kind), .o_state(state_value), .o_writes(writes), .o_reads(reads),
        .o_address(address), .o_expected(expected_data), .o_actual(actual_data), .o_cycles(cycles)
    );
    uivtc #(
        .H_ActiveSize(1280), .H_FrameSize(1650), .H_SyncStart(1390), .H_SyncEnd(1430),
        .V_ActiveSize(720), .V_FrameSize(750), .V_SyncStart(725), .V_SyncEnd(730)
    ) u_hdmi_vtc (
        .I_vtc_rstn(reg_pixel_release), .I_vtc_clk(clk_pixel), .O_vtc_vs(vtc_vs),
        .O_vtc_hs(), .O_vtc_de_valid(vtc_de), .O_vtc_user(), .O_vtc_last()
    );
    road_selftest_display road_selftest_display_Inst (
        .i_clk(dhi_clk), .i_rstn(reg_user_release), .i_payload(payload),
        .i_pixel_clk(clk_pixel), .i_pixel_rstn(reg_pixel_release), .i_vsync(vtc_vs), .i_de(vtc_de),
        .o_rgb(display_rgb), .o_vsync(display_vs), .o_de(display_de), .o_active_payload()
    );
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
