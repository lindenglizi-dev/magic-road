`timescale 1ns / 1ps
// Company: RoadYOLO project
// Engineer: Codex
// Create Date: 2026-10-15
// Design Name: Shared numeric ROM LUT service
// Module Name: road_shared_lut_service
// Description: description/road_shared_lut_service_spec.md
// Simulations: testbench/tb_road_shared_lut_service.v
// Referrences: Frozen model manifest and ROM-R1 request/response contract
// Dependencies: External single-outstanding road_numeric_rom_reader
// Version: V1.0
// Revision Date: 2026-10-15
// History: 2026-10-15 V1.0 Single-owner byte extraction and cancel draining
// 版权所有: RoadYOLO工程
// 设计人员: Codex
// 创建日期: 2026-10-15
// 设计名称: 共享模型ROM查表服务
// 模块名称: road_shared_lut_service
// 模块说明: Description/road_shared_lut_service_spec.md
// 仿真工程: TestBench/tb_road_shared_lut_service.v
// 参考资料: 冻结模型清单与ROM-R1握手合同
// 依赖文件: 外部唯一未决读服务road_numeric_rom_reader
// 当前版本: V1.0
// 修订日期: 2026-10-15
// 修订历史: 2026-10-15 V1.0 字节提取与已接受请求取消排空
module road_shared_lut_service #(
    parameter [17:0] C_SIGMOID_BYTE_OFFSET = 18'd137962, // 冻结manifest中的sigmoid起始字节
    parameter [17:0] C_EXP_BYTE_OFFSET = 18'd140010      // 冻结manifest中的exp起始字节
)(
    // 同域控制；取消不复位外部reader。
    input i_clk,                                     // 统一100MHz上升沿
    input i_rstn,                                    // 与reader共同低有效异步断言
    input i_cancel,                                  // 撤销客户端事务并排空已接受读
    // 一次未决的查表请求，完整身份必须回显。
    input i_lut_req_valid,                           // 查表请求有效
    input i_lut_req_kind,                            // 零选sigmoid，一选exp
    input [9:0] i_lut_req_address,                    // 表内UINT16条目索引
    input [15:0] i_lut_req_tag,                       // 请求标签原样返回
    input [31:0] i_lut_req_frame_token,               // 源任务标识原样返回
    input [31:0] i_lut_req_model_id,                  // 必须匹配冻结模型标识
    output o_lut_req_ready,                          // 空闲且无旧ROM读时接收
    // 完整查表响应；反压期间身份和数值不变。
    output o_lut_rsp_valid,                          // 读出两字节后响应有效
    output o_lut_rsp_kind,                           // 已锁定表类别
    output [9:0] o_lut_rsp_address,                   // 已锁定原始索引
    output [15:0] o_lut_rsp_tag,                      // 已锁定请求标签
    output [31:0] o_lut_rsp_frame_token,              // 已锁定任务标识
    output [31:0] o_lut_rsp_model_id,                 // 已锁定模型标识
    output [15:0] o_lut_rsp_data,                     // 小端二字节UINT16值
    output o_lut_rsp_error,                          // 非法模型/范围或reader故障
    input i_lut_rsp_ready,                           // 客户端完整消费响应
    // 外部ROM-R1原读口，不增加标签、取消或等待周期字段。
    output o_rom_request_valid,                      // 物理160bit词读请求
    output [12:0] o_rom_request_addr,                // 20字节词号
    input i_rom_request_ready,                       // reader本拍接收地址
    input i_rom_response_valid,                      // reader已冻结完整词
    input [159:0] i_rom_response_data,               // 低字节对应词内lane零
    output o_rom_response_ready,                     // 正常返回或取消排空均可消费
    input i_rom_fault,                               // reader故障直到共同复位
    output o_fault                                  // 本服务锁存的ROM故障
);
    //-------------配置参数区域-------------//
    // 唯一模型身份，不以参数放宽模型检查。
    localparam [31:0] C_MODEL_ID = 32'hB35D4A66;      // 完整payload SHA的已冻结短标识

    //-------------状态参数区域-------------//
    // 三段式状态机独占查表、定位和ROM返回。
    localparam [2:0] ST_IDLE = 3'd0;                 // 等待下一条合法所有权
    localparam [2:0] ST_DIVIDE = 3'd1;               // 串行除20得到词号和lane
    localparam [2:0] ST_LOCATE = 3'd2;               // 注册词地址及提取位偏移
    localparam [2:0] ST_REQUEST = 3'd3;              // 保持ROM请求至接受
    localparam [2:0] ST_WAIT = 3'd4;                 // 等待当前已接受词返回
    localparam [2:0] ST_RESPONSE = 3'd5;             // 保持完整客户端响应
    localparam [2:0] ST_DRAIN = 3'd6;                // 丢弃取消后的旧ROM返回
    localparam [2:0] ST_FAULT = 3'd7;                // 等待reader共同复位

    //--------------状态机信号--------------//
    // 状态寄存器与独立组合下一状态。
    reg [2:0] state_current;                        // 当前事务阶段
    reg [2:0] state_next;                           // 下一拍控制阶段

    //--------------寄存器信号--------------//
    // 请求身份在一个事务内冻结，取消仅撤销有效性。
    reg [1:0] reg_release;                          // 两级本地复位同步释放
    reg reg_kind;                                  // 冻结的表类别
    reg [9:0] reg_index;                            // 冻结的表内索引
    reg [15:0] reg_tag;                             // 冻结的查表标签
    reg [31:0] reg_frame_token;                     // 冻结的源任务
    reg [31:0] reg_model_id;                        // 冻结的模型身份

    // 字节地址串行定位，不使用乘法器或组合除法器。
    reg [17:0] reg_dividend;                        // 逐位移入的18位字节偏移
    reg [12:0] reg_quotient;                        // 除20所得物理词号
    reg [5:0] reg_remainder;                        // 每步小于20的余数
    reg [4:0] cnt_divide;                           // 已执行的0至17除法步
    reg [12:0] reg_word_address;                    // 保持至ROM请求接受的词地址
    reg [7:0] reg_bit_shift;                        // lane乘8的字节提取偏移
    reg reg_crosses;                               // lane19需要相邻词高字节
    reg reg_second;                                // 当前等候跨词第二次读
    reg [7:0] reg_low_byte;                         // 跨词第一字节，不复制整词
    reg reg_rom_pending;                           // reader已接受尚未消费的读

    //--------------输出信号--------------//
    // 这些寄存值在响应被反压时保持。
    reg [15:0] response_data_o;                     // 完整二字节响应数值
    reg response_error_o;                          // 当前请求的错误结果
    reg fault_o;                                   // reader故障粘滞位

    //--------------其他信号--------------//
    // 握手及除法中间量只表达当前拥有者。
    wire flag_active;                              // 共同复位已释放
    wire flag_accept;                              // 完整客户端请求传输
    wire flag_bad_request;                         // 模型或exp索引非法
    wire flag_rom_request;                         // reader实际接受本次词读
    wire flag_rom_response;                        // reader实际返回并消费本次词
    wire [5:0] shifted_remainder;                   // 余数移入被除数下一位
    wire flag_subtract;                            // 本步可减20并置商末位
    wire [17:0] selected_base;                      // 按kind选择冻结表起点
    wire [17:0] index_bytes;                        // 索引左移一位的字节量

    //-------------其他信号连线-------------//
    assign flag_active = reg_release[1] && i_rstn;   // 复位断言立即关闭客户端
    assign flag_accept = i_lut_req_valid && o_lut_req_ready; // 只在双端同意时锁定身份
    assign flag_bad_request = (i_lut_req_model_id != C_MODEL_ID) || (i_lut_req_kind && (i_lut_req_address >= 10'd256)); // 错误请求不读ROM
    assign flag_rom_request = o_rom_request_valid && i_rom_request_ready; // 登记实际已接受读
    assign flag_rom_response = i_rom_response_valid && o_rom_response_ready; // 正常或排空只消费一次
    assign shifted_remainder = {reg_remainder[4:0], reg_dividend[17]}; // 恢复除法移入最高待处理位
    assign flag_subtract = shifted_remainder >= 6'd20; // 商本步判定
    assign selected_base = i_lut_req_kind ? C_EXP_BYTE_OFFSET : C_SIGMOID_BYTE_OFFSET; // 两个固定表基址
    assign index_bytes = {7'd0, i_lut_req_address, 1'b0}; // UINT16小端条目占两字节

    //-------------输出信号连线-------------//
    assign o_lut_req_ready = (state_current == ST_IDLE) && flag_active && !i_cancel && !fault_o && !i_rom_fault; // 旧读排空前不可重用
    assign o_lut_rsp_valid = (state_current == ST_RESPONSE) && flag_active && !i_cancel; // 取消优先于响应发布
    assign o_lut_rsp_kind = reg_kind;                // 表类别保持到消费
    assign o_lut_rsp_address = reg_index;            // 原索引保持到消费
    assign o_lut_rsp_tag = reg_tag;                  // 标签保持到消费
    assign o_lut_rsp_frame_token = reg_frame_token;  // 源任务保持到消费
    assign o_lut_rsp_model_id = reg_model_id;        // 模型身份保持到消费
    assign o_lut_rsp_data = response_data_o;         // 注册数值输出桥
    assign o_lut_rsp_error = response_error_o;       // 注册错误输出桥
    assign o_rom_request_valid = (state_current == ST_REQUEST) && flag_active && !i_cancel && !fault_o && !i_rom_fault; // 不取消已接受事务
    assign o_rom_request_addr = reg_word_address;    // reader接受前地址不变
    assign o_rom_response_ready = ((state_current == ST_WAIT) || (state_current == ST_DRAIN)) && flag_active && !i_rom_fault; // cancel也必须排空旧响应
    assign o_fault = fault_o;                        // 故障只由共同复位清除

    //--------------状态机区域--------------//
    // 异步断言时立即失去客户端所有权，释放等待两级同步。
    always @(posedge i_clk or negedge i_rstn) begin
        if (!i_rstn) begin
            reg_release <= 2'b00;                   // 本地许可在复位时关闭
        end else begin
            reg_release <= {reg_release[0], 1'b1};  // 两拍后释放
        end
    end

    // 状态寄存器不直接产生任何ROM完成或成功响应。
    always @(posedge i_clk or negedge i_rstn) begin
        if (!i_rstn) begin
            state_current <= ST_IDLE;              // 共同复位撤销旧状态
        end else begin
            state_current <= state_next;           // 独立组合决策生效
        end
    end

    // 取消排空优先于正常工作；没有标签的reader不得立即重新归属。
    always @(*) begin
        state_next = state_current;                 // 默认保持当前阶段
        if (!flag_active) begin
            state_next = ST_IDLE;                   // 未释放前不接受任务
        end else if (i_cancel) begin
            if (fault_o || i_rom_fault) begin
                state_next = ST_FAULT;              // 取消不能清reader粘滞故障
            end else if (reg_rom_pending && !flag_rom_response) begin
                state_next = ST_DRAIN;              // 已接受的读必须等旧返回
            end else begin
                state_next = ST_IDLE;               // 无在途或本拍已排空
            end
        end else begin
            case (state_current)
                // 空闲只接收一个请求，非法请求走错误响应。
                ST_IDLE: begin
                    if (fault_o || i_rom_fault) begin
                        state_next = ST_FAULT;      // 无任务故障不得新接收
                    end else if (flag_accept) begin
                        if (flag_bad_request) begin
                            state_next = ST_RESPONSE; // 保持原身份的错误返回
                        end else begin
                            state_next = ST_DIVIDE; // 合法请求开始逐位定位
                        end
                    end else begin
                        state_next = ST_IDLE;       // 没有传输时不推进
                    end
                end

                // 完整18步除20后才能使用商与余数。
                ST_DIVIDE: begin
                    if (cnt_divide == 5'd17) begin
                        state_next = ST_LOCATE;     // 最后一步在该边沿注册
                    end else begin
                        state_next = ST_DIVIDE;     // 继续下一被除数位
                    end
                end

                // 商和余数先注册成稳定外部地址。
                ST_LOCATE: begin
                    state_next = ST_REQUEST;        // 下一拍才发布物理请求
                end

                // reader等待时间保持原合同，不以计数猜测响应。
                ST_REQUEST: begin
                    if (i_rom_fault) begin
                        state_next = ST_RESPONSE;   // 对当前任务报告ROM错误
                    end else if (flag_rom_request) begin
                        state_next = ST_WAIT;       // 已接受读的归属锁定
                    end else begin
                        state_next = ST_REQUEST;    // 反压时保持词地址
                    end
                end

                // 正常词返回；只有lane19需要第二词。
                ST_WAIT: begin
                    if (i_rom_fault) begin
                        state_next = ST_RESPONSE;   // 不发布故障词的数值
                    end else if (flag_rom_response) begin
                        if (reg_crosses && !reg_second) begin
                            state_next = ST_REQUEST; // 聚合前再读相邻词
                        end else begin
                            state_next = ST_RESPONSE; // 两字节完整可见
                        end
                    end else begin
                        state_next = ST_WAIT;       // 等待真实valid事件
                    end
                end

                // 客户端未消费期间不接新任务。
                ST_RESPONSE: begin
                    if (i_lut_rsp_ready) begin
                        if (fault_o || i_rom_fault) begin
                            state_next = ST_FAULT;  // 错误响应消费后仍隔离reader
                        end else begin
                            state_next = ST_IDLE;   // 正常响应完整消费后释放
                        end
                    end else begin
                        state_next = ST_RESPONSE;   // 身份和数据继续保持
                    end
                end

                // 旧响应消费之前不允许新客户端抢占。
                ST_DRAIN: begin
                    if (i_rom_fault) begin
                        state_next = ST_FAULT;      // reader失败需共同复位
                    end else if (flag_rom_response) begin
                        state_next = ST_IDLE;       // 旧返回丢弃后才能重用
                    end else begin
                        state_next = ST_DRAIN;      // 无任意超时提前释放
                    end
                end

                // 粘滞故障必须由共同复位恢复。
                ST_FAULT: begin
                    state_next = ST_FAULT;          // 不自动重试失败读
                end

                // 非法状态隔离，不制造成功返回。
                default: begin
                    state_next = ST_FAULT;          // 失败封闭
                end
            endcase
        end
    end

    //-------------主要任务处理区域-------------//
    // 表类别在一次查表内保持。
    always @(posedge i_clk or negedge i_rstn) begin
        if (!i_rstn) reg_kind <= 1'b0;               // 复位身份无效
        else if (flag_accept) reg_kind <= i_lut_req_kind; // 接收时锁表类别
    end

    // 原始索引只跟随接受的客户端请求。
    always @(posedge i_clk or negedge i_rstn) begin
        if (!i_rstn) reg_index <= 10'd0;             // 复位索引零
        else if (flag_accept) reg_index <= i_lut_req_address; // 接收时锁索引
    end

    // 标签不被ROM背压或取消排空改写。
    always @(posedge i_clk or negedge i_rstn) begin
        if (!i_rstn) reg_tag <= 16'd0;               // 复位标签零
        else if (flag_accept) reg_tag <= i_lut_req_tag; // 完整请求标签
    end

    // 源任务标识直到完整响应消费才可复用。
    always @(posedge i_clk or negedge i_rstn) begin
        if (!i_rstn) reg_frame_token <= 32'd0;       // 复位任务零
        else if (flag_accept) reg_frame_token <= i_lut_req_frame_token; // 锁定当前帧任务
    end

    // 非法模型仍原样回显，避免错误被伪装为当前模型。
    always @(posedge i_clk or negedge i_rstn) begin
        if (!i_rstn) reg_model_id <= 32'd0;          // 复位模型零
        else if (flag_accept) reg_model_id <= i_lut_req_model_id; // 锁定请求模型
    end

    // 字节偏移左移并逐位送入除20余数。
    always @(posedge i_clk or negedge i_rstn) begin
        if (!i_rstn) reg_dividend <= 18'd0;          // 复位除法输入
        else if (flag_accept) reg_dividend <= selected_base + index_bytes; // base加2倍索引
        else if (state_current == ST_DIVIDE) reg_dividend <= {reg_dividend[16:0], 1'b0}; // 移入下一位
    end

    // 每次移位得到一个商位，不使用组合除法。
    always @(posedge i_clk or negedge i_rstn) begin
        if (!i_rstn) reg_quotient <= 13'd0;          // 复位商
        else if (flag_accept) reg_quotient <= 13'd0; // 新请求从零商开始
        else if (state_current == ST_DIVIDE) reg_quotient <= {reg_quotient[11:0], flag_subtract}; // 追加本步商位
    end

    // 恢复除法保证每步余数小于20。
    always @(posedge i_clk or negedge i_rstn) begin
        if (!i_rstn) reg_remainder <= 6'd0;          // 复位余数
        else if (flag_accept) reg_remainder <= 6'd0; // 新请求清余数
        else if (state_current == ST_DIVIDE) begin
            if (flag_subtract) reg_remainder <= shifted_remainder - 6'd20; // 减去除数并保留余数
            else reg_remainder <= shifted_remainder; // 不足20时直接保留
        end
    end

    // 定长18步只用于地址数学，不替代reader响应握手。
    always @(posedge i_clk or negedge i_rstn) begin
        if (!i_rstn) cnt_divide <= 5'd0;             // 复位步数
        else if (flag_accept) cnt_divide <= 5'd0;    // 新请求从最高位开始
        else if (state_current == ST_DIVIDE) cnt_divide <= cnt_divide + 5'd1; // 每拍处理一位
    end

    // 跨词第二请求只在第一返回已经消费后发出。
    always @(posedge i_clk or negedge i_rstn) begin
        if (!i_rstn) reg_word_address <= 13'd0;      // 复位物理地址
        else if (state_current == ST_LOCATE) reg_word_address <= reg_quotient; // 注册除法词号
        else if ((state_current == ST_WAIT) && flag_rom_response && reg_crosses && !reg_second) reg_word_address <= reg_word_address + 13'd1; // 相邻词顺序读取
    end

    // 一个lane对应8位，最大lane19的低字节先单独保存。
    always @(posedge i_clk or negedge i_rstn) begin
        if (!i_rstn) reg_bit_shift <= 8'd0;          // 复位提取位偏移
        else if (state_current == ST_LOCATE) reg_bit_shift <= {reg_remainder[4:0], 3'b000}; // lane乘8仅连线
    end

    // 只有lane19的二字节条目会越过160位词边界。
    always @(posedge i_clk or negedge i_rstn) begin
        if (!i_rstn) reg_crosses <= 1'b0;            // 复位跨词标志
        else if (state_current == ST_LOCATE) reg_crosses <= reg_remainder == 6'd19; // 标记必要聚合
    end

    // 第二读标志不随裸valid重复推进。
    always @(posedge i_clk or negedge i_rstn) begin
        if (!i_rstn) reg_second <= 1'b0;             // 复位读序
        else if (flag_accept) reg_second <= 1'b0;    // 新任务从第一词开始
        else if ((state_current == ST_WAIT) && flag_rom_response && reg_crosses) reg_second <= 1'b1; // 第一返回已完整消费
    end

    // 只保存跨词的一个字节，不保存完整ROM副本。
    always @(posedge i_clk or negedge i_rstn) begin
        if (!i_rstn) reg_low_byte <= 8'd0;           // 复位暂存字节
        else if ((state_current == ST_WAIT) && flag_rom_response && reg_crosses && !reg_second) reg_low_byte <= i_rom_response_data[159:152]; // 第一词lane19
    end

    // 取消不直接清在途位，真实返回消费才能释放无标签reader。
    always @(posedge i_clk or negedge i_rstn) begin
        if (!i_rstn) reg_rom_pending <= 1'b0;        // 共同复位清外设所有权
        else if (flag_rom_response) reg_rom_pending <= 1'b0; // 包括DRAIN丢弃旧返回
        else if (flag_rom_request) reg_rom_pending <= 1'b1; // 只登记已接受读
    end

    //-------------输出信号处理区域-------------//
    // 成功字节提取仅发生在正常WAIT消费，DRAIN永远不写成功数据。
    always @(posedge i_clk or negedge i_rstn) begin
        if (!i_rstn) response_data_o <= 16'd0;       // 复位响应数值
        else if (flag_accept || i_rom_fault) response_data_o <= 16'd0; // 新任务/错误不得继承旧值
        else if ((state_current == ST_WAIT) && flag_rom_response && !i_cancel) begin
            if (reg_second) response_data_o <= {i_rom_response_data[7:0], reg_low_byte}; // 小端跨词高低字节拼接
            else if (!reg_crosses) response_data_o <= i_rom_response_data[reg_bit_shift +: 16]; // 非跨词条目显式提取16位
        end
    end

    // 请求级错误保持到响应被消费，不把故障转换成零值成功。
    always @(posedge i_clk or negedge i_rstn) begin
        if (!i_rstn) response_error_o <= 1'b0;       // 复位错误位
        else if (i_rom_fault) response_error_o <= 1'b1; // reader错误传播给拥有者
        else if (flag_accept) response_error_o <= flag_bad_request; // 非法身份/索引不读ROM
    end

    // reader故障只有共同复位能恢复，取消不自动重试。
    always @(posedge i_clk or negedge i_rstn) begin
        if (!i_rstn) fault_o <= 1'b0;                // 共同复位清故障
        else if (i_rom_fault || (state_current == ST_FAULT)) fault_o <= 1'b1; // 锁存外设或状态故障
    end
endmodule
