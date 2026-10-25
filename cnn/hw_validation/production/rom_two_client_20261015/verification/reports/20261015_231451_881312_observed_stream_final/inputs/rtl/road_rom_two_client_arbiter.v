`timescale 1ns / 1ps
////////////////////////////////////English///////////////////////////////////////
// Company:         RoadYOLO project
// Engineer:        Codex
// Create Date:     2026/10/15
// Design Name:     Single-owner two-client ROM arbitration
// Module Name:     road_rom_two_client_arbiter
// Description:     description/road_rom_two_client_arbiter_Design.pdf
// Simulations:     testbench/modelsim/2020.4/road_rom_two_client_arbiter
// Referrences:     Frozen reader and sixth-batch ownership contract
// Dependencies:    External unchanged road_numeric_rom_reader
// Version:         V1.0
// Revision Date:   2026/10/15
// History:
// Time             Version     Revised by        Contents
// 2026/10/15        V1.0        Codex             Lock one owner until its response is consumed.
///////////////////////////////////Chinese////////////////////////////////////////
// 版权归属:        RoadYOLO工程
// 开发人员:        Codex
// 创建日期:        2026年10月15日
// 设计名称:        唯一ROM两客户单事务仲裁
// 模块名称:        road_rom_two_client_arbiter
// 模块说明:        Description/road_rom_two_client_arbiter_Design.pdf
// 仿真工程:        TestBench/ModelSim/2020.4/road_rom_two_client_arbiter
// 参考资料:        冻结reader及第六批归属协议
// 依赖文件:        外部未修改road_numeric_rom_reader
// 当前版本:        V1.0
// 修订日期:        2026年10月15日
// 修订历史:
// 时间             版本        修订人            修订内容
// 2026年10月15日   V1.0        Codex             响应消费后才释放单个owner。
module road_rom_two_client_arbiter(
    // 共同复位，仲裁无单独取消输入。
    input i_clk,                                     // 唯一100MHz仲裁时钟
    input i_rstn,                                    // 与reader和两客户共同复位
    // 参数客户请求和返回。
    input i_param_request_valid,                     // 参数客户独立发布请求
    input [12:0] i_param_request_addr,                // 参数客户保持的20字节词号
    output o_param_request_ready,                    // 允许参数客户进入唯一事务槽
    output o_param_response_valid,                   // 只有参数owner才收到有效返回
    output [159:0] o_param_response_data,             // 非owner为零，不广播数据
    input i_param_response_ready,                    // 参数owner完整消费返回
    // 查表客户请求和返回；其取消由原服务DRAIN实现。
    input i_lut_request_valid,                       // 查表服务独立发布物理词请求
    input [12:0] i_lut_request_addr,                  // 查表服务保持的20字节词号
    output o_lut_request_ready,                      // 允许查表客户进入唯一事务槽
    output o_lut_response_valid,                     // 只有查表owner才收到有效返回
    output [159:0] o_lut_response_data,               // 参数owner期间保持零
    input i_lut_response_ready,                      // 包括取消后旧返回排空许可
    // 唯一现有reader接口，等待和数据布局不变。
    output o_rom_request_valid,                      // 注册后的唯一物理读请求
    output [12:0] o_rom_request_addr,                 // 已接受客户端的锁定地址
    input i_rom_request_ready,                       // reader实际接受请求
    input i_rom_response_valid,                      // reader完整词已可消费
    input [159:0] i_rom_response_data,                // reader保持的完整词载荷
    output o_rom_response_ready,                     // 只由当前owner的ready决定
    input i_rom_fault,                               // reader粘滞故障
    output o_fault                                  // 全局故障直到共同复位
);
    //-------------状态参数区域-------------//
    // 一个事务依次接受、发给reader、返回给owner。
    localparam [1:0] ST_IDLE = 2'd0;                 // 可接受任一客户
    localparam [1:0] ST_REQUEST = 2'd1;              // 保持注册地址直至reader接受
    localparam [1:0] ST_WAIT = 2'd2;                 // 返回消费之前不更换owner
    localparam [1:0] ST_FAULT = 2'd3;                // 不伪造成功退休

    //--------------状态机信号--------------//
    // 控制状态只由独立下一状态过程更新。
    reg [1:0] state_current;                        // 当前事务阶段
    reg [1:0] state_next;                           // 下一拍阶段

    //--------------寄存器信号--------------//
    // 唯一地址槽与请求轮转位，不缓存完整返回。
    reg [1:0] reg_release;                          // 异步断言后的两级释放
    reg reg_owner_lut;                              // 零参数、一查表的已接受owner
    reg reg_prefer_lut;                             // 双方等待时的下次优先客户
    reg [12:0] transaction_addr;                    // 一次admission锁定的地址
    reg flag_selected_lut;                          // 空闲时组合选择，忙时不改owner
    reg fault_o;                                    // reader/非法状态的粘滞故障

    //--------------其他信号--------------//
    // 客户接受、物理接受、返回消费分别可观察。
    wire flag_active;                              // 复位释放且接口可用
    wire flag_idle;                                // 唯一事务槽空闲
    wire flag_wait;                                // reader已接受且owner未退休
    wire flag_client_accept;                       // 恰一个客户完成admission
    wire flag_reader_accept;                       // 物理reader接受事件
    wire flag_response_accept;                     // 当前owner消费真实返回
    wire owner_response_ready;                     // 非owner ready不参与

    //-------------其他信号连线-------------//
    assign flag_active = reg_release[1] && i_rstn;   // 断言复位时立即阻断传输
    assign flag_idle = state_current == ST_IDLE;    // 解码空槽阶段
    assign flag_wait = state_current == ST_WAIT;    // 解码返回归属阶段
    assign flag_client_accept = (i_param_request_valid && o_param_request_ready) || (i_lut_request_valid && o_lut_request_ready); // 不用裸valid计数
    assign flag_reader_accept = o_rom_request_valid && i_rom_request_ready; // 与admission分拍
    assign flag_response_accept = i_rom_response_valid && o_rom_response_ready; // 最后消费才退休
    assign owner_response_ready = reg_owner_lut ? i_lut_response_ready : i_param_response_ready; // 绝不OR两个ready

    //-------------输出信号连线-------------//
    assign o_param_request_ready = flag_idle && flag_active && !flag_selected_lut && !fault_o && !i_rom_fault; // 只有被选客户可接受
    assign o_lut_request_ready = flag_idle && flag_active && flag_selected_lut && !fault_o && !i_rom_fault; // 不因reader暂忙改选择
    assign o_param_response_valid = flag_wait && !reg_owner_lut && i_rom_response_valid && flag_active && !i_rom_fault; // 返回只属于参数owner
    assign o_lut_response_valid = flag_wait && reg_owner_lut && i_rom_response_valid && flag_active && !i_rom_fault; // 返回只属于查表owner
    assign o_param_response_data = (flag_wait && !reg_owner_lut) ? i_rom_response_data : 160'd0; // 非参数owner不接收载荷
    assign o_lut_response_data = (flag_wait && reg_owner_lut) ? i_rom_response_data : 160'd0; // 非查表owner不接收载荷
    assign o_rom_request_valid = (state_current == ST_REQUEST) && flag_active && !fault_o && !i_rom_fault; // 地址已注册才发物理请求
    assign o_rom_request_addr = transaction_addr;    // 反压期间保持已接受地址
    assign o_rom_response_ready = flag_wait && owner_response_ready && flag_active && !i_rom_fault; // 取消客户仍可DRAIN
    assign o_fault = fault_o;                       // 故障只有共同复位清除

    //--------------状态机区域--------------//
    // 双请求按上次admission后的轮转位决定，无请求时保留优先方向。
    always @(*) begin
        flag_selected_lut = reg_prefer_lut;          // 默认轮转选择
        case ({i_param_request_valid, i_lut_request_valid})
            2'b10: flag_selected_lut = 1'b0;         // 只有参数请求可立即获选
            2'b01: flag_selected_lut = 1'b1;         // 只有查表请求可立即获选
            default: flag_selected_lut = reg_prefer_lut; // 双方等待或都空闲按轮转
        endcase
    end

    // 本地同步释放不改变其他三个原模块的复位端口。
    always @(posedge i_clk or negedge i_rstn) begin
        if (!i_rstn) reg_release <= 2'b00;          // 共同断言时许可清零
        else reg_release <= {reg_release[0], 1'b1}; // 最早第三沿接收
    end

    // 状态寄存器只落实组合决策。
    always @(posedge i_clk or negedge i_rstn) begin
        if (!i_rstn) state_current <= ST_IDLE;      // 共同复位撤销所有在途
        else state_current <= state_next;           // 不由客户cancel改写
    end

    // owner在返回消费前保持，包括长反压与客户取消排空。
    always @(*) begin
        state_next = state_current;                 // 默认保持事务
        if (!flag_active) begin
            state_next = ST_IDLE;                   // 释放前不接受新owner
        end else begin
            case (state_current)
                // 空闲admission先锁地址/owner，下一拍才发reader。
                ST_IDLE: begin
                    if (i_rom_fault || fault_o) state_next = ST_FAULT; // 故障封闭新请求
                    else if (flag_client_accept) state_next = ST_REQUEST; // 唯一槽获得归属
                    else state_next = ST_IDLE;      // 没有接受不推进
                end

                // physical ready不能重新选择客户或地址。
                ST_REQUEST: begin
                    if (i_rom_fault) state_next = ST_FAULT; // 已接受任务报全局失败
                    else if (flag_reader_accept) state_next = ST_WAIT; // 实际读已在途
                    else state_next = ST_REQUEST;   // 保持注册payload
                end

                // 仅当前owner接受返回才能释放。
                ST_WAIT: begin
                    if (i_rom_fault) state_next = ST_FAULT; // 不能用坏读假造成功
                    else if (flag_response_accept) state_next = ST_IDLE; // 完整词消费后退休
                    else state_next = ST_WAIT;      // 非owner ready不生效
                end

                // 原prefetch无ROMfault入口，全局须协调共同复位。
                ST_FAULT: begin
                    state_next = ST_FAULT;          // 不自动清owner或重试
                end

                // 非法状态失败封闭。
                default: begin
                    state_next = ST_FAULT;          // 不制造未知归属响应
                end
            endcase
        end
    end

    //-------------主要任务处理区域-------------//
    // owner只跟随一次客户端双端握手。
    always @(posedge i_clk or negedge i_rstn) begin
        if (!i_rstn) reg_owner_lut <= 1'b0;         // 复位后的无效owner默认参数
        else if (flag_client_accept) reg_owner_lut <= flag_selected_lut; // 锁定到返回消费
    end

    // 每次已接受请求后把双请求优先权交给另一客户。
    always @(posedge i_clk or negedge i_rstn) begin
        if (!i_rstn) reg_prefer_lut <= 1'b0;        // 首次同时请求先参数
        else if (flag_client_accept) reg_prefer_lut <= !flag_selected_lut; // 逐请求而非逐时钟轮转
    end

    // 唯一13位地址存储，不新增完整参数或表RAM。
    always @(posedge i_clk or negedge i_rstn) begin
        if (!i_rstn) transaction_addr <= 13'd0;     // 复位时地址无效
        else if (flag_client_accept) begin
            if (flag_selected_lut) transaction_addr <= i_lut_request_addr; // 锁存查表物理词号
            else transaction_addr <= i_param_request_addr; // 锁存参数物理词号
        end
    end

    // 全局粘滞故障不因取消或等待清除。
    always @(posedge i_clk or negedge i_rstn) begin
        if (!i_rstn) fault_o <= 1'b0;               // 共同复位才恢复所有权
        else if (i_rom_fault || (state_current == ST_FAULT)) fault_o <= 1'b1; // 锁存真实外设或非法状态
    end
endmodule
