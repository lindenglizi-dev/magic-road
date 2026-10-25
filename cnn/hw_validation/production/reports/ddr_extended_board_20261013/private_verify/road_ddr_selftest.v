`timescale 1ns / 1ps

// Company: RoadYOLO project
// Engineer: Codex
// Create Date: 2026-10-13
// Module Name: road_ddr_selftest
// Description: ROM-driven native PAXI boundary and byte-mask diagnostic.
// Dependencies: vectors.hex; original PH1P DDR IP.
// Version: V1.0
// 模块说明：顺序执行固定命令，独立接受写地址和写数据，逐字比较读回。
module road_ddr_selftest #(
    parameter [26:0] C_TIMEOUT = 27'h7ffffff // 每个等待阶段的看门狗上限
) (
    input i_clk,                          // 原厂DDR用户时钟
    input i_rstn,                         // 与整个DDR控制器共同复位
    input i_phy_ready,                    // 初始化完成许可
    input i_awready,                      // 写地址接受条件
    input i_wready,                       // 写数据接受条件
    input i_arready,                      // 读地址接受条件
    input i_rvalid,                       // 实际读返回有效
    input i_rlast,                        // 单拍响应结束标志
    input [127:0] i_rdata,                 // 全位宽读回数据
    output [24:0] o_awaddr,                // native16位字地址
    output o_awvalid,                     // 保持至AW握手
    output [127:0] o_wdata,                // 不随背压变化的写数据
    output [15:0] o_wstrb,                // 位为一则禁止该字节写入
    output o_wvalid,                      // 保持至独立W握手
    output o_wlast,                       // 每个命令仅一拍
    output [24:0] o_araddr,                // 当前唯一读命令地址
    output o_arvalid,                     // 读地址提交
    output o_rready,                      // 已登记或同拍登记读许可
    output [1:0] o_status,                 // 零运行、一通过、二首错
    output [3:0] o_error,                  // 失败原因锁存
    output [3:0] o_state,                  // 当前协议阶段
    output [9:0] o_writes,                 // 完整AW/W对接受数
    output [9:0] o_reads,                  // 正确比较读字数
    output [24:0] o_address,               // 当前或失败地址
    output [127:0] o_expected,             // 当前写字或读期望
    output [127:0] o_actual,               // 最近实际响应
    output [31:0] o_cycles,                // PHY就绪后的运行周期
    output [31:0] o_init_cycles,           // 初始化等待周期
    output [31:0] o_wait_both,             // AW/W均未完成的等待拍
    output [31:0] o_wait_aw,               // 仅AW尚未完成的等待拍
    output [31:0] o_wait_w,                // 仅W尚未完成的等待拍
    output [31:0] o_wait_ar,               // AR尚未接受的等待拍
    output [31:0] o_wait_r                 // AR接受后缺少响应的等待拍
);
    //-------------状态参数区域-------------//
    // 命令装载与原生通道分阶段推进
    localparam [3:0] ST_WAIT = 4'd0;       // 等待PHY
    localparam [3:0] ST_FETCH = 4'd1;      // 同步ROM读取
    localparam [3:0] ST_LOAD = 4'd2;       // 捕获本条完整命令
    localparam [3:0] ST_ISSUE = 4'd3;      // 检查已寄存命令
    localparam [3:0] ST_WRITE = 4'd4;      // 分别接受AW/W
    localparam [3:0] ST_READ_ADDR = 4'd5;  // 接受唯一读地址
    localparam [3:0] ST_READ_DATA = 4'd6;  // 等待唯一返回
    localparam [3:0] ST_CHECK = 4'd7;      // 检查全字与RLAST
    localparam [3:0] ST_ADVANCE = 4'd8;    // 推进指令或核对总数
    localparam [3:0] ST_PASS = 4'd9;       // 全部1056条命令完成
    localparam [3:0] ST_FAIL = 4'd10;      // 保留首错等待公共复位

    //---------------计数信号---------------//
    // 请求计数与互斥等待统计
    reg [10:0] cnt_command = 0;           // 命令索引0到1055
    reg [9:0] cnt_writes = 0;             // 完整写对数量
    reg [9:0] cnt_reads = 0;              // 比较成功次数
    reg [26:0] cnt_wait = 0;              // 当前阶段等待预算
    reg [31:0] cnt_cycles = 0;            // 核心运行经过拍
    reg [31:0] cnt_init = 0;              // PHY初始化经过拍
    reg [31:0] cnt_both = 0;              // 写地址与数据一起等待
    reg [31:0] cnt_aw = 0;                // 数据已接受而地址等待
    reg [31:0] cnt_w = 0;                 // 地址已接受而数据等待
    reg [31:0] cnt_ar = 0;                // 读地址背压
    reg [31:0] cnt_r = 0;                 // 已接受读的返回等待

    //--------------状态机信号--------------//
    // 三段式控制
    reg [3:0] state_current = 0;          // 当前阶段寄存器
    reg [3:0] state_next = 0;             // 完整默认保持的下一阶段

    //--------------寄存器信号--------------//
    // 同步命令ROM及当前请求缓存
    reg [191:0] reg_commands [0:2047];    // 打包的边界与掩码命令
    reg [191:0] reg_rom = 0;             // ROM同步读出
    reg [24:0] reg_address = 0;          // 已寄存native地址
    reg [127:0] reg_expected = 0;        // 已寄存写字或读期望
    reg [15:0] reg_mask = 0;             // 当前高有效字节屏蔽
    reg reg_write = 0;                   // 当前命令方向
    reg reg_command_ok = 0;             // 标记、索引、地址和保留位合法
    reg [127:0] reg_actual = 0;          // 最近返回的完整字
    reg reg_last = 0;                    // 与返回同拍捕获RLAST
    reg reg_aw_seen = 0;                 // 写地址已接受账目
    reg reg_w_seen = 0;                  // 写数据已接受账目
    reg [3:0] reg_error = 0;             // 首个失败原因

    //---------------标志信号---------------//
    // 所有接受条件绑定真实ready
    wire flag_aw_accept;                 // 本拍AW握手
    wire flag_w_accept;                  // 本拍W握手
    wire flag_aw_done;                   // 历史或本拍AW已接受
    wire flag_w_done;                    // 历史或本拍W已接受
    wire flag_write_complete;            // 完整写对已被接受
    wire flag_ar_accept;                 // 本拍AR握手
    wire flag_r_accept;                  // 本拍R握手
    wire flag_unexpected;                // 没有读归属的返回
    wire flag_phy_lost;                  // 初始化后失去PHY许可
    wire flag_timeout;                   // 当前等待超时

    //-------------其他信号连线-------------//
    // 读写通道独立接受与唯一返回归属
    assign flag_aw_accept = o_awvalid && i_awready; // AW专属条件
    assign flag_w_accept = o_wvalid && i_wready; // W专属条件
    assign flag_aw_done = reg_aw_seen || flag_aw_accept; // 保留已完成地址账目
    assign flag_w_done = reg_w_seen || flag_w_accept; // 保留已完成数据账目
    assign flag_write_complete = flag_aw_done && flag_w_done; // 不解释为DRAM提交
    assign flag_ar_accept = o_arvalid && i_arready; // 唯一读登记
    assign flag_r_accept = i_rvalid && o_rready; // 响应消费
    assign flag_unexpected = i_rvalid && !((state_current == ST_READ_DATA) || ((state_current == ST_READ_ADDR) && flag_ar_accept)); // 阻止串事务返回
    assign flag_phy_lost = (state_current != ST_WAIT) && !i_phy_ready; // 运行中PHY异常
    assign flag_timeout = cnt_wait == C_TIMEOUT; // 固定等待上限

    //-------------输出信号连线-------------//
    // 当前请求寄存器驱动原生接口
    assign o_awaddr = reg_address;        // 写背压不移动地址
    assign o_awvalid = i_rstn && (state_current == ST_WRITE) && !reg_aw_seen; // 已接受后撤销AW
    assign o_wdata = reg_expected;        // 写数据从命令缓存提供
    assign o_wstrb = reg_mask;            // 保留PH1P高有效屏蔽
    assign o_wvalid = i_rstn && (state_current == ST_WRITE) && !reg_w_seen; // 已接受后撤销W
    assign o_wlast = o_wvalid;            // 单拍写末尾
    assign o_araddr = reg_address;        // 读地址独立保持
    assign o_arvalid = i_rstn && (state_current == ST_READ_ADDR); // AR等待真实接受
    assign o_rready = i_rstn && ((state_current == ST_READ_DATA) || ((state_current == ST_READ_ADDR) && i_arready)); // 容许AR同拍返回
    assign o_status = (state_current == ST_FAIL) ? 2'd2 : ((state_current == ST_PASS) ? 2'd1 : 2'd0); // TEST颜色编码
    assign o_error = reg_error;           // 失败后不覆盖错误号
    assign o_state = state_current;      // 协议阶段观测
    assign o_writes = cnt_writes;         // 十位足以容纳528
    assign o_reads = cnt_reads;           // 正确读数量
    assign o_address = reg_address;      // 首错地址保持
    assign o_expected = reg_expected;    // 完整期望字
    assign o_actual = reg_actual;        // 完整实读字
    assign o_cycles = cnt_cycles;        // 含装载与等待的运行窗口
    assign o_init_cycles = cnt_init;      // 初始化单独统计
    assign o_wait_both = cnt_both;        // 双通道等待分类
    assign o_wait_aw = cnt_aw;            // 仅地址等待分类
    assign o_wait_w = cnt_w;              // 仅数据等待分类
    assign o_wait_ar = cnt_ar;            // 读请求等待分类
    assign o_wait_r = cnt_r;              // 读响应等待分类

    //--------------状态机区域--------------//
    // 复位取消旧事务；板顶层同时清空DDR控制器。
    always @(posedge i_clk or negedge i_rstn) begin
        if (!i_rstn) begin
            state_current <= ST_WAIT;    // 从PHY初始化重新开始
        end else begin
            state_current <= state_next; // 状态唯一驱动
        end
    end

    // 完整指令读取后才产生外部请求。
    always @(*) begin
        state_next = state_current;      // 背压默认保持
        case (state_current)
            // 初始化之后进入同步ROM读取。
            ST_WAIT: begin
                if (i_phy_ready) begin
                    state_next = ST_FETCH;
                end
            end
            // 同步读取一拍。
            ST_FETCH: begin
                state_next = ST_LOAD;
            end
            // 完整命令捕获一拍。
            ST_LOAD: begin
                state_next = ST_ISSUE;
            end
            // 合法命令才允许发到控制器。
            ST_ISSUE: begin
                if (!reg_command_ok) begin
                    state_next = ST_FAIL;
                end else begin
                    state_next = reg_write ? ST_WRITE : ST_READ_ADDR;
                end
            end
            // AW/W接受时间可以不同。
            ST_WRITE: begin
                if (flag_write_complete) begin
                    state_next = ST_ADVANCE;
                end
            end
            // AR同时返回数据时直接转入比较。
            ST_READ_ADDR: begin
                if (flag_ar_accept) begin
                    state_next = flag_r_accept ? ST_CHECK : ST_READ_DATA;
                end
            end
            // 不使用固定等待拍假装写可见。
            ST_READ_DATA: begin
                if (flag_r_accept) begin
                    state_next = ST_CHECK;
                end
            end
            // 完整数据与末拍均须匹配。
            ST_CHECK: begin
                state_next = ((reg_actual == reg_expected) && reg_last) ? ST_ADVANCE : ST_FAIL;
            end
            // 末条完成后再检查读写总数。
            ST_ADVANCE: begin
                if (cnt_command == 11'd1055) begin
                    state_next = ((cnt_writes == 10'd528) && (cnt_reads == 10'd528)) ? ST_PASS : ST_FAIL;
                end else begin
                    state_next = ST_FETCH;
                end
            end
            // 持续通过，仍监测意外返回。
            ST_PASS: begin
                state_next = ST_PASS;
            end
            // 首错现场仅公共复位清除。
            ST_FAIL: begin
                state_next = ST_FAIL;
            end
            // 非法状态不能误报通过。
            default: begin
                state_next = ST_FAIL;
            end
        endcase
        if (state_current != ST_FAIL) begin
            if (flag_unexpected || flag_phy_lost) begin
                state_next = ST_FAIL;    // 协议错误优先终止
            end else if (flag_timeout && (state_current != ST_PASS)) begin
                state_next = ST_FAIL;    // 超时保持失败
            end
        end
    end

    //-----------状态任务处理区域-----------//
    // ROM没有复位写入；FETCH后的LOAD只消费最新同步读值。
    always @(posedge i_clk) begin
        if (state_current == ST_FETCH) begin
            reg_rom <= reg_commands[cnt_command]; // 片上只读命令存储
        end
    end

    // 当前命令在整个协议阶段保持，包括分离的AW和W。
    always @(posedge i_clk or negedge i_rstn) begin
        if (!i_rstn) begin
            reg_address <= 25'd0;
            reg_expected <= 128'd0;
            reg_mask <= 16'd0;
            reg_write <= 1'b0;
            reg_command_ok <= 1'b0;
        end else if (state_current == ST_LOAD) begin
            reg_address <= reg_rom[168:144];
            reg_expected <= reg_rom[127:0];
            reg_mask <= reg_rom[143:128];
            reg_write <= reg_rom[169];
            reg_command_ok <= (reg_rom[191:181] == {3'd0, 8'ha5}) && (reg_rom[180:170] == cnt_command) && (reg_rom[146:144] == 3'd0) && (reg_rom[168:144] >= 25'h1a00000);
        end
    end

    // 推进仅发生于已完成命令之后。
    always @(posedge i_clk or negedge i_rstn) begin
        if (!i_rstn) begin
            cnt_command <= 11'd0;
        end else if ((state_current == ST_ADVANCE) && (state_next == ST_FETCH)) begin
            cnt_command <= cnt_command + 11'd1;
        end
    end

    // 新命令清空局部接受账目，累计数仅在完整配对时递增。
    always @(posedge i_clk or negedge i_rstn) begin
        if (!i_rstn) begin
            reg_aw_seen <= 1'b0;
            reg_w_seen <= 1'b0;
            cnt_writes <= 10'd0;
        end else if (state_current == ST_LOAD) begin
            reg_aw_seen <= 1'b0;
            reg_w_seen <= 1'b0;
        end else if (state_current == ST_WRITE) begin
            if (flag_aw_accept) begin
                reg_aw_seen <= 1'b1;
            end
            if (flag_w_accept) begin
                reg_w_seen <= 1'b1;
            end
            if (flag_write_complete) begin
                cnt_writes <= cnt_writes + 10'd1;
            end
        end
    end

    // 捕获全部返回位，比较通过才增加读数量。
    always @(posedge i_clk or negedge i_rstn) begin
        if (!i_rstn) begin
            reg_actual <= 128'd0;
            reg_last <= 1'b0;
            cnt_reads <= 10'd0;
        end else begin
            if (flag_r_accept || (flag_unexpected && (state_current != ST_FAIL))) begin
                reg_actual <= i_rdata;
                reg_last <= i_rlast;
            end
            if ((state_current == ST_CHECK) && (state_next == ST_ADVANCE)) begin
                cnt_reads <= cnt_reads + 10'd1;
            end
        end
    end

    // 原错误号保留，新命令保护使用九和十。
    always @(posedge i_clk or negedge i_rstn) begin
        if (!i_rstn) begin
            reg_error <= 4'd0;
        end else if ((state_next == ST_FAIL) && (state_current != ST_FAIL)) begin
            if (flag_unexpected) begin
                reg_error <= 4'd7;
            end else if (flag_phy_lost) begin
                reg_error <= 4'd8;
            end else if (flag_timeout) begin
                case (state_current)
                    ST_WAIT: reg_error <= 4'd1;
                    ST_WRITE: reg_error <= 4'd2;
                    ST_READ_ADDR: reg_error <= 4'd3;
                    default: reg_error <= 4'd4;
                endcase
            end else if (state_current == ST_ISSUE) begin
                reg_error <= 4'd9;
            end else if (state_current != ST_CHECK) begin
                reg_error <= 4'd10;
            end else begin
                reg_error <= reg_last ? 4'd5 : 4'd6;
            end
        end
    end

    // 初始化和运行窗口分开；互斥等待按本拍接受后的缺失通道分类。
    always @(posedge i_clk or negedge i_rstn) begin
        if (!i_rstn) begin
            cnt_wait <= 27'd0;
            cnt_cycles <= 32'd0;
            cnt_init <= 32'd0;
            cnt_both <= 32'd0;
            cnt_aw <= 32'd0;
            cnt_w <= 32'd0;
            cnt_ar <= 32'd0;
            cnt_r <= 32'd0;
        end else if ((state_current != ST_PASS) && (state_current != ST_FAIL)) begin
            if (state_current == ST_WAIT) begin
                cnt_init <= cnt_init + 32'd1;
            end else begin
                cnt_cycles <= cnt_cycles + 32'd1;
            end
            cnt_wait <= (state_next != state_current) ? 27'd0 : cnt_wait + 27'd1;
            if ((state_current == ST_WRITE) && !flag_write_complete) begin
                if (!flag_aw_done && !flag_w_done) begin
                    cnt_both <= cnt_both + 32'd1;
                end else if (!flag_aw_done) begin
                    cnt_aw <= cnt_aw + 32'd1;
                end else begin
                    cnt_w <= cnt_w + 32'd1;
                end
            end else if ((state_current == ST_READ_ADDR) && !flag_ar_accept) begin
                cnt_ar <= cnt_ar + 32'd1;
            end else if ((state_current == ST_READ_DATA) && !flag_r_accept) begin
                cnt_r <= cnt_r + 32'd1;
            end
        end
    end

    //--------------初始化区域--------------//
    // 固定诊断向量随位流初始化，标记及命令索引另在执行时核对。
    initial begin
        $readmemh("vectors.hex", reg_commands);
    end
endmodule
