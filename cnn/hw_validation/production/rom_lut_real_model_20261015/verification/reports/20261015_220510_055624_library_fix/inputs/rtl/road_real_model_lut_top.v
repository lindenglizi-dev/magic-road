`timescale 1ns / 1ps
////////////////////////////////////English///////////////////////////////////////
// Company:         RoadYOLO project
// Engineer:        Codex
// Create Date:     2026/10/15
// Design Name:     Real trained-model ROM LUT wiring
// Module Name:     road_real_model_lut_top
// Description:     description/road_real_model_lut_top_Design.pdf
// Simulations:     testbench/modelsim/2020.4/road_real_model_lut_top
// Referrences:     Frozen G10 package manifest and ROM-R1/LUT contracts
// Dependencies:    road_numeric_rom_reader, road_shared_lut_service
// Version:         V1.0
// Revision Date:   2026/10/15
// History:
// Time             Version     Revised by        Contents
// 2026/10/15        V1.0        Codex             Connect one unchanged reader and LUT service.
///////////////////////////////////Chinese////////////////////////////////////////
// 版权归属:        RoadYOLO工程
// 开发人员:        Codex
// 创建日期:        2026年10月15日
// 设计名称:        真实训练模型ROM查表纯接线
// 模块名称:        road_real_model_lut_top
// 模块说明:        Description/road_real_model_lut_top_Design.pdf
// 仿真工程:        TestBench/ModelSim/2020.4/road_real_model_lut_top
// 参考资料:        冻结G10清单及ROM-R1、共享查表接口
// 依赖文件:        road_numeric_rom_reader、road_shared_lut_service
// 当前版本:        V1.0
// 修订日期:        2026年10月15日
// 修订历史:
// 时间             版本        修订人            修订内容
// 2026年10月15日   V1.0        Codex             连接唯一未修改reader及LUT服务。
module road_real_model_lut_top(
    // 同一时钟与共同复位，取消只作用于服务所有权。
    input i_clk,                                  // 统一ROM/查表100MHz时钟
    input i_rstn,                                 // reader与服务共同低有效复位
    input i_cancel,                               // 客户端取消，不复位已接受ROM读
    // 动态请求身份在ready前由上游保持。
    input i_lut_req_valid,                        // 客户端查询有效
    input i_lut_req_kind,                         // sigmoid或exp选择
    input [9:0] i_lut_req_address,                 // 所选表内条目索引
    input [15:0] i_lut_req_tag,                    // 查询标签完整回显
    input [31:0] i_lut_req_frame_token,            // 查询所属任务
    input [31:0] i_lut_req_model_id,               // 绑定G10完整包的短身份
    output o_lut_req_ready,                       // 服务允许接收一个查询
    // 完整响应保持到客户端消费，不增加额外一级延迟。
    output o_lut_rsp_valid,                       // 两字节结果完整可见
    output o_lut_rsp_kind,                        // 回显原表选择
    output [9:0] o_lut_rsp_address,                // 回显原表索引
    output [15:0] o_lut_rsp_tag,                   // 回显原查询标签
    output [31:0] o_lut_rsp_frame_token,           // 回显原任务标识
    output [31:0] o_lut_rsp_model_id,              // 回显原模型标识
    output [15:0] o_lut_rsp_data,                  // 真实ROM提取的UINT16条目
    output o_lut_rsp_error,                       // 非法请求或ROM故障，不是零值成功
    input i_lut_rsp_ready,                        // 客户端完整消费结果
    output o_fault                               // 沿原服务保留粘滞故障
);
    //--------------模块实例化信号--------------//
    // 一条未决物理词事务，无仲裁或第二ROM副本。
    wire rom_request_valid;                       // 服务持有的物理读请求
    wire [12:0] rom_request_addr;                  // 唯一reader的20字节词号
    wire rom_request_ready;                       // reader本拍锁定词号许可
    wire rom_response_valid;                      // reader已冻结完整物理词
    wire [159:0] rom_response_data;                // 从G10初始化读出的160位载荷
    wire rom_response_ready;                      // 正常读或取消排空的消费许可
    wire rom_fault;                               // reader原粘滞故障输出

    //---------------模块例化区域---------------//
    // 原服务负责定位、身份、反压和取消排空；源代码字节不变。
    road_shared_lut_service road_shared_lut_service_Inst(
        .i_clk(i_clk),                             // 与reader同域
        .i_rstn(i_rstn),                           // 共同复位沿既有释放规则
        .i_cancel(i_cancel),                       // 不生成reader复位
        .i_lut_req_valid(i_lut_req_valid),          // 原查询握手入口
        .i_lut_req_kind(i_lut_req_kind),            // 动态表选择直连
        .i_lut_req_address(i_lut_req_address),      // 动态索引直连
        .i_lut_req_tag(i_lut_req_tag),              // 标签不改写
        .i_lut_req_frame_token(i_lut_req_frame_token), // 任务身份不改写
        .i_lut_req_model_id(i_lut_req_model_id),     // 模型检查仍由原服务执行
        .o_lut_req_ready(o_lut_req_ready),          // 原服务所有权许可
        .o_lut_rsp_valid(o_lut_rsp_valid),          // 完整结果有效直连
        .o_lut_rsp_kind(o_lut_rsp_kind),            // 原表选择回显
        .o_lut_rsp_address(o_lut_rsp_address),      // 原索引回显
        .o_lut_rsp_tag(o_lut_rsp_tag),              // 原标签回显
        .o_lut_rsp_frame_token(o_lut_rsp_frame_token), // 原任务回显
        .o_lut_rsp_model_id(o_lut_rsp_model_id),    // 原模型回显
        .o_lut_rsp_data(o_lut_rsp_data),            // 不再次舍入或量化
        .o_lut_rsp_error(o_lut_rsp_error),          // 原错误状态传播
        .i_lut_rsp_ready(i_lut_rsp_ready),          // 客户端反压直达原服务
        .o_rom_request_valid(rom_request_valid),   // 唯一物理读口请求
        .o_rom_request_addr(rom_request_addr),     // 单个保持的词号
        .i_rom_request_ready(rom_request_ready),   // 等待真实reader许可
        .i_rom_response_valid(rom_response_valid), // 等待真实reader返回
        .i_rom_response_data(rom_response_data),   // 真实厂商模型数据
        .o_rom_response_ready(rom_response_ready), // 保留取消晚返回排空
        .i_rom_fault(rom_fault),                   // 不伪造可注入ROM故障
        .o_fault(o_fault)                          // 无额外状态或延迟
    );

    // 原reader内部14组56个ERAM，每个初始化路径在本候选artifacts内。
    road_numeric_rom_reader road_numeric_rom_reader_Inst(
        .i_clk(i_clk),                             // 原reader工作时钟
        .i_rstn(i_rstn),                           // 只接共同复位，不接cancel
        .i_request_valid(rom_request_valid),       // 原请求协议不增加字段
        .i_request_addr(rom_request_addr),         // 13位物理词地址
        .o_request_ready(rom_request_ready),       // 原空闲许可
        .o_response_valid(rom_response_valid),     // 原WAIT计数7之后的有效
        .o_response_data(rom_response_data),       // 原注册160位输出
        .i_response_ready(rom_response_ready),     // 服务真实消费或排空
        .o_fault(rom_fault)                        // 原非法地址粘滞故障
    );
endmodule
