`timescale 1ns / 1ps
////////////////////////////////////English///////////////////////////////////////
// Company:         RoadYOLO project
// Engineer:        Codex
// Create Date:     2026/10/15
// Design Name:     Existing parameter and LUT clients on one G10 reader
// Module Name:     road_rom_two_client_top
// Description:     description/road_rom_two_client_top_Design.pdf
// Simulations:     testbench/modelsim/2020.4/road_rom_two_client_top
// Referrences:     Sixth-batch single-owner ROM contract
// Dependencies:    Frozen down2 prefetch, LUT service, ROM-R1 and two-client arbiter
// Version:         V1.0
// Revision Date:   2026/10/15
// History:
// Time             Version     Revised by        Contents
// 2026/10/15        V1.0        Codex             Wire both clients to the only trained-model ROM.
///////////////////////////////////Chinese////////////////////////////////////////
// 版权归属:        RoadYOLO工程
// 开发人员:        Codex
// 创建日期:        2026年10月15日
// 设计名称:        既有参数与查表客户共用G10读口
// 模块名称:        road_rom_two_client_top
// 模块说明:        Description/road_rom_two_client_top_Design.pdf
// 仿真工程:        TestBench/ModelSim/2020.4/road_rom_two_client_top
// 参考资料:        第六批唯一ROM归属合同
// 依赖文件:        原down2预取、查表服务、ROM-R1及新两客户仲裁
// 当前版本:        V1.0
// 修订日期:        2026年10月15日
// 修订历史:
// 时间             版本        修订人            修订内容
// 2026年10月15日   V1.0        Codex             两客户只接一个训练模型ROM。
module road_rom_two_client_top(
    // 所有实例共同时钟/复位；只取消LUT客户。
    input i_clk,                                    // 统一100MHz域
    input i_rstn,                                   // reader/仲裁/两客户共同复位
    input i_cancel,                                 // 查表取消，仲裁owner不清除
    // 原参数预取输出，不加入第二份参数RAM。
    output o_load_valid,                            // down2单条参数已组装
    output [2:0] o_load_kind,                        // 原kind编码保持
    output [10:0] o_load_addr,                       // 原参数目的索引
    output signed [31:0] o_load_data,                // 原符号扩展或32位系数值
    input i_load_ready,                             // 参数消费者反压
    output o_table_valid,                           // 原共享SiLU装表条目
    output [9:0] o_table_addr,                       // SiLU表0至1023索引
    output signed [15:0] o_table_data,               // 原INT16 SiLU值
    input i_table_ready,                            // SiLU表消费者反压
    output o_prefetch_done,                         // 仅原down2两层及SiLU加载完成
    output [31:0] o_prefetch_cycles,                 // 原预取起止计数含ROM竞争
    // 动态查表客户端身份。
    input i_lut_req_valid,                          // 一个未决查询请求
    input i_lut_req_kind,                           // sigmoid或exp类别
    input [9:0] i_lut_req_address,                   // 动态表内索引
    input [15:0] i_lut_req_tag,                      // 动态标签完整回显
    input [31:0] i_lut_req_frame_token,              // 帧任务标识完整回显
    input [31:0] i_lut_req_model_id,                 // 冻结G10模型身份
    output o_lut_req_ready,                         // 查表服务空闲许可
    output o_lut_rsp_valid,                         // 完整查表结果有效
    output o_lut_rsp_kind,                          // 原查询类别
    output [9:0] o_lut_rsp_address,                  // 原查询索引
    output [15:0] o_lut_rsp_tag,                     // 原查询标签
    output [31:0] o_lut_rsp_frame_token,             // 原任务标识
    output [31:0] o_lut_rsp_model_id,                // 原模型身份
    output [15:0] o_lut_rsp_data,                    // 真实共享ROM提取的结果
    output o_lut_rsp_error,                         // 原查表错误传播
    input i_lut_rsp_ready,                          // 查表结果消费者反压
    output o_fault                                 // 任一客户/reader/仲裁故障
);
    //--------------模块实例化信号--------------//
    // 两客户与物理reader分别握手，三组事件不混计。
    wire param_request_valid;                       // 参数客户请求
    wire [12:0] param_request_addr;                 // 参数物理词地址
    wire param_request_ready;                       // 参数进入仲裁槽许可
    wire param_response_valid;                      // 归属于参数客户的返回
    wire [159:0] param_response_data;                // 非参数owner时为零
    wire param_response_ready;                      // 原预取消费完整返回
    wire lut_rom_request_valid;                     // LUT客户物理词请求
    wire [12:0] lut_rom_request_addr;                // LUT物理词地址
    wire lut_rom_request_ready;                     // LUT进入仲裁槽许可
    wire lut_rom_response_valid;                    // 归属于LUT客户的返回
    wire [159:0] lut_rom_response_data;               // 非LUT owner时为零
    wire lut_rom_response_ready;                    // 包括原服务DRAIN许可
    wire rom_request_valid;                         // 仲裁转发至唯一reader
    wire [12:0] rom_request_addr;                    // 注册后的物理词地址
    wire rom_request_ready;                         // reader实际接受许可
    wire rom_response_valid;                        // reader原返回有效
    wire [159:0] rom_response_data;                  // reader原160位返回
    wire rom_response_ready;                        // 仅当前owner决定返回消费
    wire rom_fault;                                 // reader粘滞故障
    wire arbiter_fault;                             // 仲裁失败封闭状态
    wire prefetch_fault;                            // 原参数非法值检查结果
    wire lut_fault;                                 // 原查表服务故障
    wire shared_fault;                              // 原LUT服务可以观察的总线故障

    //-------------输出信号连线-------------//
    assign shared_fault = rom_fault || arbiter_fault; // 不向LUT伪造成功读
    assign o_fault = shared_fault || prefetch_fault || lut_fault; // 原预取无ROMfault入口，协调者必须共同复位

    //---------------模块例化区域---------------//
    // 原固定预取只支持down2两层652参数及1024SiLU，不扩为67层加载器。
    road_down2_parameter_prefetch road_down2_parameter_prefetch_Inst(
        .i_clk(i_clk), .i_rstn(i_rstn),              // 共同复位沿原行为
        .o_rom_valid(param_request_valid),          // 原参数请求入口
        .o_rom_addr(param_request_addr),            // 原byte组装所需物理词号
        .i_rom_ready(param_request_ready),          // 仲裁admission而非物理接受
        .i_rom_valid(param_response_valid),         // 只有参数owner的真实返回
        .i_rom_data(param_response_data),           // 不混入LUT返回
        .o_rom_ready(param_response_ready),         // 原WAIT消费完整词
        .o_load_valid(o_load_valid), .o_load_kind(o_load_kind), // 参数输出协议不变
        .o_load_addr(o_load_addr), .o_load_data(o_load_data), // 原目的索引与数值
        .i_load_ready(i_load_ready),                // 参数输出反压不变
        .o_table_valid(o_table_valid), .o_table_addr(o_table_addr), // 原SiLU装表接口
        .o_table_data(o_table_data), .i_table_ready(i_table_ready), // 原INT16表数据与反压
        .o_done(o_prefetch_done), .o_fault(prefetch_fault), // 不把局部done当全网准备完成
        .o_cycles(o_prefetch_cycles)                // 保留原实际周期计数
    );

    // 原服务取消后继续消费已被仲裁接收的事务，不能丢晚返回。
    road_shared_lut_service road_shared_lut_service_Inst(
        .i_clk(i_clk), .i_rstn(i_rstn), .i_cancel(i_cancel), // 取消不连仲裁或reader复位
        .i_lut_req_valid(i_lut_req_valid), .i_lut_req_kind(i_lut_req_kind), // 动态请求类别
        .i_lut_req_address(i_lut_req_address), .i_lut_req_tag(i_lut_req_tag), // 原索引与标签
        .i_lut_req_frame_token(i_lut_req_frame_token), .i_lut_req_model_id(i_lut_req_model_id), // 完整身份
        .o_lut_req_ready(o_lut_req_ready), .o_lut_rsp_valid(o_lut_rsp_valid), // 原客户端握手
        .o_lut_rsp_kind(o_lut_rsp_kind), .o_lut_rsp_address(o_lut_rsp_address), // 类别/索引回显
        .o_lut_rsp_tag(o_lut_rsp_tag), .o_lut_rsp_frame_token(o_lut_rsp_frame_token), // 标签/任务回显
        .o_lut_rsp_model_id(o_lut_rsp_model_id), .o_lut_rsp_data(o_lut_rsp_data), // 模型/数值回显
        .o_lut_rsp_error(o_lut_rsp_error), .i_lut_rsp_ready(i_lut_rsp_ready), // 原错误与反压
        .o_rom_request_valid(lut_rom_request_valid), .o_rom_request_addr(lut_rom_request_addr), // 原单词请求
        .i_rom_request_ready(lut_rom_request_ready), // 仲裁接受后原服务登记在途
        .i_rom_response_valid(lut_rom_response_valid), .i_rom_response_data(lut_rom_response_data), // 只收到LUT owner返回
        .o_rom_response_ready(lut_rom_response_ready), // 正常消费或取消排空
        .i_rom_fault(shared_fault), .o_fault(lut_fault) // 原服务处理总线故障
    );

    // 新仲裁唯一owner，不复制任何完整参数/表/ROM存储。
    road_rom_two_client_arbiter road_rom_two_client_arbiter_Inst(
        .i_clk(i_clk), .i_rstn(i_rstn),              // 与两个客户及reader共同复位
        .i_param_request_valid(param_request_valid), .i_param_request_addr(param_request_addr), // 参数请求
        .o_param_request_ready(param_request_ready), // 参数admission许可
        .o_param_response_valid(param_response_valid), .o_param_response_data(param_response_data), // 参数专属返回
        .i_param_response_ready(param_response_ready), // 参数owner消费许可
        .i_lut_request_valid(lut_rom_request_valid), .i_lut_request_addr(lut_rom_request_addr), // LUT请求
        .o_lut_request_ready(lut_rom_request_ready), // LUT admission许可
        .o_lut_response_valid(lut_rom_response_valid), .o_lut_response_data(lut_rom_response_data), // LUT专属返回
        .i_lut_response_ready(lut_rom_response_ready), // LUT owner消费/DRAIN许可
        .o_rom_request_valid(rom_request_valid), .o_rom_request_addr(rom_request_addr), // 唯一物理请求
        .i_rom_request_ready(rom_request_ready),     // reader实际接受
        .i_rom_response_valid(rom_response_valid), .i_rom_response_data(rom_response_data), // reader完整返回
        .o_rom_response_ready(rom_response_ready), .i_rom_fault(rom_fault), // 单owner反压与真实故障
        .o_fault(arbiter_fault)                     // 原参数客户缺fault入口，外部统一观察
    );

    // 唯一正确G10 reader，原等待/14组初始化路径不改。
    road_numeric_rom_reader road_numeric_rom_reader_Inst(
        .i_clk(i_clk), .i_rstn(i_rstn),              // 原共同复位
        .i_request_valid(rom_request_valid), .i_request_addr(rom_request_addr), // 注册物理词请求
        .o_request_ready(rom_request_ready),        // 原reader空闲许可
        .o_response_valid(rom_response_valid), .o_response_data(rom_response_data), // 原真实返回
        .i_response_ready(rom_response_ready), .o_fault(rom_fault) // 返回消费后才可读下一词
    );
endmodule
