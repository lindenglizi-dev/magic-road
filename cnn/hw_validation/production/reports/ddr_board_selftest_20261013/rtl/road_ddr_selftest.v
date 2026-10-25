`timescale 1ns / 1ps

// Company: RoadYOLO project
// Engineer: Codex
// Create Date: 2026-10-13
// Module Name: road_ddr_selftest
// Description: Single-client native PAXI write/read diagnostic.
// Dependencies: Original PH1P DDR IP, no synthetic completion response.
// Version: V1.0
// 模块说明：独占四地址、两轮取反、先写后逆序读；结果仅说明本序列。
module road_ddr_selftest #(
    parameter [26:0] C_TIMEOUT = 27'h7ffffff // 每个等待阶段的看门狗上限
) (
    input i_clk,                           // 原厂DDR用户域时钟
    input i_rstn,                          // 顶层异步断言、同步释放复位
    input i_phy_ready,                     // 初始化状态，不代表存储已经通过
    input i_awready,                       // 写地址实际接受许可
    input i_wready,                        // 写数据实际接受许可
    input i_arready,                       // 读地址实际接受许可
    input i_rvalid,                        // 控制器返回数据有效
    input i_rlast,                         // 当前单拍读响应结束标记
    input [127:0] i_rdata,                  // 本次真实读回数据
    output [24:0] o_awaddr,                 // 原生PAXI写地址，不解释字节单位
    output o_awvalid,                      // 写地址保持到自身握手
    output [127:0] o_wdata,                 // 当前地址对应确定性测试字
    output [15:0] o_wstrb,                  // 沿当前PH1P工程的零掩码
    output o_wvalid,                       // 写数据保持到自身握手
    output o_wlast,                        // 每个写命令只有一拍
    output [24:0] o_araddr,                 // 逆序访问四个原生地址
    output o_arvalid,                      // 独立读请求有效
    output o_rready,                       // 只为已接受读请求接收数据
    output [1:0] o_status,                  // 零运行、一观察通过、二失败
    output [3:0] o_error,                   // 首错类型，复位前不覆盖
    output [3:0] o_state,                   // 当前实验阶段
    output [3:0] o_writes,                  // 地址和数据都已接受的写次数
    output [3:0] o_reads,                   // 比较正确的读次数
    output [24:0] o_address,                // 当前或首错地址
    output [127:0] o_expected,              // 当前或首错的完整期望字
    output [127:0] o_actual,                // 最近或首错的完整实际字
    output [31:0] o_cycles                 // 核心域经过周期，不折算带宽
);
    //-------------状态参数区域-------------//
    // 固定实验阶段
    localparam [3:0] ST_WAIT = 4'd0;        // 等待初始化完成
    localparam [3:0] ST_PREP_WRITE = 4'd1;  // 装载本次写地址和数据
    localparam [3:0] ST_WRITE = 4'd2;       // AW与W分别握手
    localparam [3:0] ST_STEP_WRITE = 4'd3;  // 推进四地址写序列
    localparam [3:0] ST_PREP_READ = 4'd4;   // 选择本次逆序读期望
    localparam [3:0] ST_READ_ADDR = 4'd5;   // 提交一个读地址
    localparam [3:0] ST_READ_DATA = 4'd6;   // 等待唯一读返回
    localparam [3:0] ST_CHECK = 4'd7;       // 比较已寄存的完整数据
    localparam [3:0] ST_STEP_READ = 4'd8;   // 推进读索引或第二轮
    localparam [3:0] ST_PASS = 4'd9;        // 八次读比较正确
    localparam [3:0] ST_FAIL = 4'd10;       // 首错锁存，等待整机复位

    //---------------计数信号---------------//
    // 接受次数与实际耗时
    reg [3:0] cnt_writes = 0;              // 已接受完整AW/W对数量
    reg [3:0] cnt_reads = 0;               // 数据与末拍均正确的数量
    reg [26:0] cnt_wait = 0;               // 当前状态的连续等待时长
    reg [31:0] cnt_cycles = 0;             // 从释放复位开始的核心周期

    //--------------状态机信号--------------//
    // 三段式实验控制
    reg [3:0] state_current = 0;           // 已寄存阶段
    reg [3:0] state_next = 0;              // 组合计算的下一阶段

    //--------------寄存器信号--------------//
    // 当前请求和失败现场
    reg [1:0] reg_index = 0;               // 四地址中的索引
    reg reg_round = 0;                     // 第二轮使用取反数据
    reg [24:0] reg_address = 0;            // 停顿期间保持的地址
    reg [127:0] reg_expected = 0;          // 停顿期间保持的期望字
    reg [127:0] reg_actual = 0;            // 返回握手时捕获完整字
    reg reg_last = 0;                      // 返回握手时捕获RLAST
    reg reg_aw_seen = 0;                   // 本次AW已接受，不再重发
    reg reg_w_seen = 0;                    // 本次W已接受，不再重发
    reg [3:0] reg_error = 0;               // 首错优先锁存

    //---------------标志信号---------------//
    // 只按各通道真实握手推进
    wire flag_aw_accept;                  // 当前AW成功接受
    wire flag_w_accept;                   // 当前W成功接受
    wire flag_write_complete;             // AW和W都已接受，不代表DRAM提交
    wire flag_ar_accept;                  // 当前AR成功接受
    wire flag_r_accept;                   // 已登记请求对应的数据接受
    wire flag_unexpected;                 // 没有读请求却出现返回
    wire flag_timeout;                    // 当前等待状态耗尽预算
    wire flag_phy_lost;                   // 运行中初始化状态失效

    //-------------其他信号连线-------------//
    // 通道计数及错误分类的公共条件
    assign flag_aw_accept = o_awvalid && i_awready; // 仅AW握手计一次
    assign flag_w_accept = o_wvalid && i_wready; // 独立于AWREADY消费数据
    assign flag_write_complete = (reg_aw_seen || flag_aw_accept) && (reg_w_seen || flag_w_accept); // 两侧接受账目齐全
    assign flag_ar_accept = o_arvalid && i_arready; // 读地址登记事件
    assign flag_r_accept = i_rvalid && o_rready; // 实际接收的返回事件
    assign flag_unexpected = i_rvalid && !((state_current == ST_READ_DATA) || ((state_current == ST_READ_ADDR) && flag_ar_accept)); // 单在途读之外的返回
    assign flag_timeout = (cnt_wait == C_TIMEOUT); // 状态等待上限比较
    assign flag_phy_lost = (state_current != ST_WAIT) && !i_phy_ready; // 初始化后掉ready单独报错

    //-------------输出信号连线-------------//
    // 原生控制器端口及持续诊断数据
    assign o_awaddr = reg_address;         // AW背压期间地址不变
    assign o_awvalid = i_rstn && (state_current == ST_WRITE) && !reg_aw_seen; // 接受后撤销AW
    assign o_wdata = reg_expected;         // W背压期间数据不变
    assign o_wstrb = 16'h0000;             // 与当前mc_to_user_interface相同
    assign o_wvalid = i_rstn && (state_current == ST_WRITE) && !reg_w_seen; // 接受后撤销W
    assign o_wlast = o_wvalid;             // 本实验每次仅一拍
    assign o_araddr = reg_address;         // 读请求使用同一冻结地址
    assign o_arvalid = i_rstn && (state_current == ST_READ_ADDR); // 直到AR接受才撤销
    assign o_rready = i_rstn && ((state_current == ST_READ_DATA) || ((state_current == ST_READ_ADDR) && i_arready)); // 支持AR同拍返回
    assign o_status = (state_current == ST_FAIL) ? 2'd2 : ((state_current == ST_PASS) ? 2'd1 : 2'd0); // 与既有TEST颜色编码一致
    assign o_error = reg_error;            // 完整保留首错类别
    assign o_state = state_current;        // 观察停在哪个协议阶段
    assign o_writes = cnt_writes;          // 只能解释为接受次数
    assign o_reads = cnt_reads;            // 八次正确读回才允许通过
    assign o_address = reg_address;        // 失败时索引推进停止
    assign o_expected = reg_expected;      // 完整128位期望保留
    assign o_actual = reg_actual;          // 完整128位实际保留
    assign o_cycles = cnt_cycles;          // 端点经过时钟数

    //--------------状态机区域--------------//
    // 复位立即取消请求；板顶层同时复位原厂DDR控制器。
    always @(posedge i_clk or negedge i_rstn) begin
        if (!i_rstn) begin
            state_current <= ST_WAIT;     // 全部协议从初始化重新开始
        end else begin
            state_current <= state_next;  // 仅此过程写状态寄存器
        end
    end

    // 下一阶段只根据真实接受、已捕获比较结果和等待预算决定。
    always @(*) begin
        state_next = state_current;       // 默认保持当前请求
        case (state_current)
            // 初始化完成才准备第一次写
            ST_WAIT: begin
                if (i_phy_ready) begin
                    state_next = ST_PREP_WRITE; // 转入测试数据准备
                end
            end
            // 请求准备一整拍后才能发出
            ST_PREP_WRITE: begin
                state_next = ST_WRITE;    // 下一拍并行提供AW和W
            end
            // 允许AW和W接受时刻不同
            ST_WRITE: begin
                if (flag_write_complete) begin
                    state_next = ST_STEP_WRITE; // 仅完成接受账目
                end
            end
            // 一轮四个地址全部写完再读
            ST_STEP_WRITE: begin
                state_next = (reg_index == 2'd3) ? ST_PREP_READ : ST_PREP_WRITE; // 选择写或逆序读
            end
            // 期望数据先寄存，避免与读握手错位
            ST_PREP_READ: begin
                state_next = ST_READ_ADDR; // 提交一个原生读地址
            end
            // 控制端点也覆盖AR同拍立即返回
            ST_READ_ADDR: begin
                if (flag_ar_accept) begin
                    state_next = flag_r_accept ? ST_CHECK : ST_READ_DATA; // 无固定等待屏障
                end
            end
            // 返回延迟由实际控制器决定
            ST_READ_DATA: begin
                if (flag_r_accept) begin
                    state_next = ST_CHECK; // 数据已冻结后再做比较
                end
            end
            // RLAST与128位数据都必须正确
            ST_CHECK: begin
                state_next = ((reg_actual == reg_expected) && reg_last) ? ST_STEP_READ : ST_FAIL; // 任一错误终止
            end
            // 第一轮结束取反，第二轮结束才通过
            ST_STEP_READ: begin
                if (reg_index != 2'd0) begin
                    state_next = ST_PREP_READ; // 继续逆序下一个地址
                end else begin
                    state_next = reg_round ? ST_PASS : ST_PREP_WRITE; // 两轮严格区分
                end
            end
            // 持续终态仍检查异常返回
            ST_PASS: begin
                state_next = ST_PASS;     // 不伪装成持续内存压力测试
            end
            // 失败后等待整板复位
            ST_FAIL: begin
                state_next = ST_FAIL;     // 首错现场保持
            end
            // 非法状态封锁所有请求
            default: begin
                state_next = ST_FAIL;     // 不回空闲掩盖状态错误
            end
        endcase
        if (state_current != ST_FAIL) begin
            if (flag_unexpected || flag_phy_lost) begin
                state_next = ST_FAIL;     // 协议错误优先于通过
            end else if (flag_timeout && (state_current != ST_PASS)) begin
                state_next = ST_FAIL;     // 超时不自动重试
            end
        end
    end

    //-----------状态任务处理区域-----------//
    // 索引推进只在独立步进状态发生，停顿不会改变payload。
    always @(posedge i_clk or negedge i_rstn) begin
        if (!i_rstn) begin
            reg_index <= 2'd0;            // 首轮从第一地址写起
            reg_round <= 1'b0;            // 复位恢复未取反向量
        end else if (state_current == ST_STEP_WRITE) begin
            if (reg_index != 2'd3) begin
                reg_index <= reg_index + 2'd1; // 写地址顺序递增
            end
        end else if (state_current == ST_STEP_READ) begin
            if (reg_index != 2'd0) begin
                reg_index <= reg_index - 2'd1; // 读地址顺序递减
            end else if (!reg_round) begin
                reg_round <= 1'b1;        // 第二轮数据全部取反
            end
        end
    end

    // 原生地址和小端测试字由有限case装入寄存器。
    always @(posedge i_clk or negedge i_rstn) begin
        if (!i_rstn) begin
            reg_address <= 25'd0;         // 不依赖配置初始化
            reg_expected <= 128'd0;       // 释放前无有效数据
        end else if ((state_current == ST_PREP_WRITE) || (state_current == ST_PREP_READ)) begin
            case (reg_index)
                2'd0: reg_address <= 25'd0; // 第一个原生对齐地址
                2'd1: reg_address <= 25'd8; // 相隔一个BL8候选步长
                2'd2: reg_address <= 25'd16; // 保持小范围独占测试
                default: reg_address <= 25'd24; // 第四个不同地址
            endcase
            case ({reg_round, reg_index})
                3'd0: reg_expected <= 128'hc3b6a99c8f8275685b4e4134271a0d00; // 第一地址逐字节递增
                3'd1: reg_expected <= 128'he8dbcec1b4a79a8d807366594c3f3225; // 第二地址不同字节偏移
                3'd2: reg_expected <= 128'h0d00f3e6d9ccbfb2a5988b7e7164574a; // 第三地址覆盖高低字节
                3'd3: reg_expected <= 128'h3225180bfef1e4d7cabdb0a396897c6f; // 第四地址避免同值别名
                3'd4: reg_expected <= 128'h3c495663707d8a97a4b1becbd8e5f2ff; // 首地址互补数据
                3'd5: reg_expected <= 128'h1724313e4b5865727f8c99a6b3c0cdda; // 第二地址互补数据
                3'd6: reg_expected <= 128'hf2ff0c192633404d5a6774818e9ba8b5; // 第三地址互补数据
                default: reg_expected <= 128'hcddae7f4010e1b2835424f5c69768390; // 末地址互补数据
            endcase
        end
    end

    // 地址和数据接受分别锁存，任一ready不能代替另一侧。
    always @(posedge i_clk or negedge i_rstn) begin
        if (!i_rstn) begin
            reg_aw_seen <= 1'b0;          // 取消旧AW账目
            reg_w_seen <= 1'b0;           // 取消旧W账目
            cnt_writes <= 4'd0;           // 从零统计本次复位后的事务
        end else if (state_current == ST_PREP_WRITE) begin
            reg_aw_seen <= 1'b0;          // 新写对的地址尚未接受
            reg_w_seen <= 1'b0;           // 新写对的数据尚未接受
        end else if (state_current == ST_WRITE) begin
            if (flag_aw_accept) begin
                reg_aw_seen <= 1'b1;      // 已接受地址不重复提交
            end
            if (flag_w_accept) begin
                reg_w_seen <= 1'b1;       // 已接受数据不重复提交
            end
            if (flag_write_complete) begin
                cnt_writes <= cnt_writes + 4'd1; // 统计成对接受，不称写提交
            end
        end
    end

    // 每次响应握手捕获一次，在下一状态比较。
    always @(posedge i_clk or negedge i_rstn) begin
        if (!i_rstn) begin
            reg_actual <= 128'd0;         // 不泄漏旧错误数据
            reg_last <= 1'b0;             // 旧末拍取消
            cnt_reads <= 4'd0;            // 新实验比较计数清零
        end else begin
            if (flag_r_accept || (flag_unexpected && (state_current != ST_FAIL))) begin
                reg_actual <= i_rdata;    // 保留完整实际字
                reg_last <= i_rlast;      // 与数据同拍保留末拍
            end
            if ((state_current == ST_CHECK) && (state_next == ST_STEP_READ)) begin
                cnt_reads <= cnt_reads + 4'd1; // 只有完全正确响应才计入
            end
        end
    end

    // 首错锁存按协议、初始化、超时、返回比较优先分类。
    always @(posedge i_clk or negedge i_rstn) begin
        if (!i_rstn) begin
            reg_error <= 4'd0;            // 新实验没有历史首错
        end else if ((state_next == ST_FAIL) && (state_current != ST_FAIL)) begin
            if (flag_unexpected) begin
                reg_error <= 4'd7;        // 没有登记读请求却返回
            end else if (flag_phy_lost) begin
                reg_error <= 4'd8;        // ready在实验过程中掉落
            end else if (flag_timeout) begin
                case (state_current)
                    ST_WAIT: reg_error <= 4'd1; // 初始化等待超时
                    ST_WRITE: reg_error <= 4'd2; // AW或W接受超时
                    ST_READ_ADDR: reg_error <= 4'd3; // AR接受超时
                    default: reg_error <= 4'd4; // 已接受AR但没有数据
                endcase
            end else if (!reg_last) begin
                reg_error <= 4'd6;        // 单拍响应缺少末拍标记
            end else begin
                reg_error <= 4'd5;        // 实际数据与期望不一致
            end
        end
    end

    // 实际经过时间包含ready停顿，不用有效工作拍替代总耗时。
    always @(posedge i_clk or negedge i_rstn) begin
        if (!i_rstn) begin
            cnt_wait <= 27'd0;            // 启动时从零等待
            cnt_cycles <= 32'd0;          // 新事务时基重新开始
        end else if ((state_current != ST_PASS) && (state_current != ST_FAIL)) begin
            cnt_cycles <= cnt_cycles + 32'd1; // 所有运行拍都计入
            if (state_next != state_current) begin
                cnt_wait <= 27'd0;        // 新阶段重新计时
            end else begin
                cnt_wait <= cnt_wait + 27'd1; // 背压和返回等待继续累计
            end
        end
    end
endmodule
