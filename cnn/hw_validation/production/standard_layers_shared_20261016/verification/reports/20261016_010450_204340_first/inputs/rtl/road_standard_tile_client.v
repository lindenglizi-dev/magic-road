`timescale 1ns / 1ps
////////////////////////////////////English///////////////////////////////////////
// Company: RoadYOLO
// Engineer: Codex
// Create Date: 2026-10-16
// Design Name: Fixed standard convolution tile client
// Module Name: road_standard_tile_client
// Description: description/road_standard_tile_client_Design.pdf
// Simulations: testbench/vivado/2021.1/road_standard_tile_client
// Referrences: Frozen graph and WIF1
// Dependencies: External sole arithmetic owner and C4 workstore
// Version: V1.0
// Revision Date: 2026-10-16
// History: 2026-10-16 V1.0 Codex Create file
///////////////////////////////////Chinese////////////////////////////////////////
// 版权归属: RoadYOLO
// 开发人员: Codex
// 创建日期: 2026-10-16
// 设计名称: 固定标准卷积共享仓客户
// 模块名称: road_standard_tile_client
// 模块说明: Description/road_standard_tile_client_Design.pdf
// 仿真工程: TestBench/Vivado/2021.1/road_standard_tile_client
// 参考资料: 冻结graph与WIF1
// 依赖文件: 外部唯一算术owner与C4工作仓
// 当前版本: V1.0
// 修订日期: 2026-10-16
// 修订历史: 2026-10-16 V1.0 Codex 创建文件

module road_standard_tile_client
(
	//-----------------全局信号-----------------//
	input i_clk, // 唯一计算owner同域时钟
	input i_rstn, // 全部服务共同异步低有效复位
	//-----------------用户接口-----------------//
	input i_cancel, // 取消后保持占有直到共同复位
	input i_start_valid, // 对齐tile任务有效
	input [6:0]i_layer_id, // 固定graph节点12/13/26/27
	input [5:0]i_tile_y, // 输出tile四行对齐起点
	input [6:0]i_tile_x, // 输出tile四列对齐起点
	input i_table_loaded, // 唯一owner已完整装载SiLU
	input i_parameter_ready, // 接受当前参数切片
	input i_parameter_rsp_valid, // 参数切片完整有效
	input [6:0]i_parameter_rsp_layer, // 参数所属冻结节点
	input [6:0]i_parameter_rsp_channel, // 参数所属输出组
	input [2:0]i_parameter_rsp_window, // DW并集宽度或PW零
	input [4:0]i_parameter_rsp_group, // 参数归约组回显
	input [191:0]i_parameter_weight, // 三输出各八权重
	input [247:0]i_parameter_quant, // 三路偏置与动态量化
	input i_parameter_error, // 参数服务拒绝此切片
	input i_read_ready, // 接受源张量对齐行请求
	input i_read_rsp_valid, // 源张量128位行返回
	input [31:0]i_read_rsp_address, // 返回源行完整地址
	input [127:0]i_read_rsp_data, // 低字节对应对齐地址
	input i_read_error, // 源读服务错误
	input i_write_ready, // 外部接受一个真实输出字节
	input i_barrier_ready, // 之前所有输出写已可读
	input [6:0]i_barrier_layer, // 屏障返回层身份
	input [5:0]i_barrier_tile_y, // 屏障返回行身份
	input [6:0]i_barrier_tile_x, // 屏障返回列身份
	input i_byte_req_ready, // WIF1 byte请求接受
	input i_byte_rsp_valid, // WIF1 byte完成响应
	input [7:0]i_byte_rsp_data, // WIF1读到的一个字节
	input i_byte_rsp_error, // WIF1 byte范围错误
	input i_weight_req_ready, // WIF1 weight请求接受
	input i_weight_rsp_valid, // WIF1 weight完成响应
	input [191:0]i_weight_rsp_data, // WIF1完整权重组
	input i_weight_rsp_error, // WIF1 weight范围错误
	input i_work_fault, // 工作仓粘滞错误
	input i_core_ready, // 冻结算术组可接受
	input i_core_output_valid, // 唯一owner最终输出有效
	input [15:0]i_core_output_tag, // 原核输出lane身份
	input [31:0]i_core_output_address, // 原核完整写地址
	input [7:0]i_core_output_data, // 原核最终INT8
	input i_core_fault, // 原算术核粘滞错误
	output o_start_ready, // 无未退休事务时接受任务
	output o_busy, // 包括故障占有与屏障等待
	output o_done, // 本tile屏障完成后单拍
	output o_fault, // 禁止发布成功的全局错误
	output [6:0]o_layer_id, // 当前锁定graph节点
	output [5:0]o_tile_y, // 当前锁定输出tile行
	output [6:0]o_tile_x, // 当前锁定输出tile列
	output o_parameter_valid, // 参数请求保持有效
	output [6:0]o_parameter_channel, // 当前输出通道起点
	output [2:0]o_parameter_window, // 三点宽七或单点宽三
	output [4:0]o_parameter_group, // 当前并集的八输入组
	output o_parameter_rsp_ready, // 消费唯一参数返回
	output o_read_valid, // 请求当前源行
	output [31:0]o_read_address, // 128位对齐源地址
	output o_read_rsp_ready, // 消费匹配源返回
	output o_write_valid, // 合法核结果与外部写原子退休
	output [31:0]o_write_address, // 当前输出实际字节地址
	output [7:0]o_write_data, // 当前输出实际INT8数据
	output o_barrier_valid, // tile全部写接受后的屏障
	output o_byte_req_valid, // WIF1覆盖或输入读取请求
	output o_byte_req_write, // 高为填仓，低为操作数读
	output [11:0]o_byte_req_addr, // WIF1唯一byte位置
	output [7:0]o_byte_req_data, // 待完整提交的填仓字节
	output o_byte_rsp_ready, // 仅等待对应byte完成时消费
	output o_weight_req_valid, // WIF1权重提交或读请求
	output o_weight_req_write, // 高为提交当前参数权重
	output [4:0]o_weight_req_group, // 五DW槽或PW归约槽
	output [191:0]o_weight_req_data, // 当前切片真实权重
	output o_weight_rsp_ready, // 仅当前权重完成可退休
	output o_core_valid, // 拼装完成的归约组
	output o_core_first, // 当前任务唯一加偏置组
	output o_core_last, // 当前任务关闭组
	output [7:0]o_core_input_mask, // 真正输入lane有效掩码
	output [63:0]o_core_activation, // 八INT8当前输入
	output [191:0]o_core_weight, // 当前同步读权重组
	output [95:0]o_core_bias, // 三路偏置首组使用
	output [2:0]o_core_output_mask, // DW尾点只启用lane零
	output [47:0]o_core_tags, // 固定输出lane标签
	output [95:0]o_core_addresses, // 三路真实字节地址
	output [95:0]o_core_pre_multiplier, // 三路前重定标乘数
	output [17:0]o_core_pre_shift, // 三路前移位
	output [31:0]o_core_post_multiplier, // 本层共享后乘数
	output [5:0]o_core_post_shift, // 本层共享后移位
	output o_core_output_ready // 输出写和核消费共同握手
);
	//-------------状态参数区域-------------//
	localparam [4:0]ST_IDLE = 0; // 无owner且可接新tile
	localparam [4:0]ST_CONFIG = 1; // 核验锁定固定层与边界
	localparam [4:0]ST_FILL_SETUP = 2; // 初始化本次完整覆盖
	localparam [4:0]ST_FILL = 3; // 从源行或padding取字节
	localparam [4:0]ST_READ = 4; // 保持源行读请求
	localparam [4:0]ST_READ_WAIT = 5; // 等待完整匹配源行
	localparam [4:0]ST_BYTE_WRITE = 6; // byte仓写请求
	localparam [4:0]ST_BYTE_WRITE_WAIT = 7; // 等实际native写完成
	localparam [4:0]ST_PARAMETER_SETUP = 8; // 初始化权重切片组
	localparam [4:0]ST_PARAMETER = 9; // 参数请求保持
	localparam [4:0]ST_PARAMETER_WAIT = 10; // 参数身份与数值检查
	localparam [4:0]ST_WEIGHT_WRITE = 11; // 提交权重仓切片
	localparam [4:0]ST_WEIGHT_WRITE_WAIT = 12; // 等全部权重word完成
	localparam [4:0]ST_TASK_SETUP = 13; // 固定三输出元数据
	localparam [4:0]ST_WEIGHT_READ = 14; // 请求当前归约权重
	localparam [4:0]ST_WEIGHT_READ_WAIT = 15; // 同步权重返回
	localparam [4:0]ST_BYTE_READ = 16; // 请求当前输入lane
	localparam [4:0]ST_BYTE_READ_WAIT = 17; // 拼装单个读字节
	localparam [4:0]ST_SEND = 18; // 等冻结核接受归约组
	localparam [4:0]ST_OUTPUT = 19; // 核与外部写共同退休
	localparam [4:0]ST_ADVANCE = 20; // 推进空间或输出通道
	localparam [4:0]ST_BARRIER = 21; // 所有写可见后才完成
	localparam [4:0]ST_FINISH = 22; // 完成脉冲且仍持owner
	localparam [4:0]ST_FAULT = 23; // 故障占有至共同reset

	//--------------状态机信号--------------//
	reg [4:0]state_current = ST_IDLE; // 当前事务阶段
	reg [4:0]state_next = ST_IDLE; // 组合下一阶段

	//--------------寄存器信号--------------//
	reg [1:0]reg_release = 0; // 异步断言两拍释放
	reg [6:0]reg_layer = 0; // start锁定的graph节点
	reg [5:0]reg_tile_y = 0; // 当前输出tile行
	reg [6:0]reg_tile_x = 0; // 当前输出tile列
	reg [6:0]reg_channel = 0; // DW通道或PW三输出起点
	reg [1:0]reg_row = 0; // DW有效输出行
	reg [3:0]reg_pixel = 0; // PW当前有效像素
	reg [9:0]reg_fill_index = 0; // 最多768填仓字节
	reg [4:0]reg_slot = 0; // 当前权重提交槽
	reg [4:0]reg_group = 0; // 当前MAC归约组
	reg [2:0]reg_lane = 0; // 当前拼装输入lane
	reg [31:0]reg_read_address = 0; // 单未决源行请求
	reg [31:0]reg_line_address = 0; // 行寄存器标签
	reg [127:0]reg_line_data = 0; // 当前源行非tile缓存
	reg [7:0]reg_fill_data = 0; // 正在提交的单字节
	reg [247:0]reg_quant = 0; // 当前输出组量化字段
	reg [191:0]reg_weight = 0; // 当前操作数而非权重数组
	reg [63:0]reg_activation = 0; // 当前八输入组
	reg [95:0]reg_addresses = 0; // 当前三个输出地址
	reg [2:0]reg_output_mask = 0; // 当前任务真实输出路
	reg [2:0]reg_written = 0; // 当前任务已消费的路

	//---------------标志信号---------------//
	reg flag_line_valid = 0; // 源行内容当前有效
	reg flag_tail = 0; // DW每行第四点单独任务
	reg flag_fault = 0; // 错误粘滞直到共同复位
	wire flag_active; // 释放且无取消错误
	wire flag_parameter_bad; // 参数回显或量化漂移
	wire flag_read_bad; // 源响应地址或服务错误
	wire flag_work_bad; // 工作仓错误完成响应
	wire flag_output_legal; // 当前三路结果唯一性
	wire flag_output_bad; // 非法或未拥有的核结果
	wire flag_last_write; // 最后一个有效结果退休
	wire flag_barrier_bad; // 可见性确认属于别的任务
	wire flag_series_last; // 当前通道最后空间任务
	wire flag_channel_last; // tile全部输出通道结束
	wire flag_fill_hit; // 源行寄存器命中

	//---------------译码信号---------------//
	reg dec_dw = 0; // 固定层是否深度卷积
	reg [6:0]dec_height = 0; // 本层输出高度
	reg [6:0]dec_width = 0; // 本层输出宽度
	reg [6:0]dec_cin = 0; // 源张量真实通道
	reg [6:0]dec_cout = 0; // 输出真实通道
	reg [31:0]dec_source_base = 0; // 冻结图源字节基址
	reg [31:0]dec_destination_base = 0; // 冻结图输出字节基址
	integer dec_source_y; // 填仓源逻辑行允许负数
	integer dec_source_x; // 填仓源逻辑列允许负数
	integer dec_source_channel; // 填仓源物理通道
	integer dec_source_height; // 当前源张量高度
	integer dec_source_width; // 当前源张量宽度
	integer dec_fill_bytes; // 全量覆盖字节数
	integer dec_valid_rows; // 末tile有效行仅二
	integer dec_sample; // DW并集或PW组内输入
	integer dec_cache_address; // 当前byte读位置
	integer dec_task_y; // 当前真实输出行
	integer dec_task_x; // 当前真实输出列
	integer dec_destination_offset; // 输出tile内像素偏移
	reg [31:0]dec_source_address = 0; // 非padding源字节地址
	reg dec_padding = 0; // 算法越界及物理尾行零
	reg [95:0]dec_addresses = 0; // 当前任务三路输出位置
	reg [2:0]dec_output_mask = 0; // 当前任务空间路数
	wire [4:0]dec_last_group; // 最后归约编号
	wire [3:0]dec_input_count; // 当前八槽中的真实数量
	wire [7:0]dec_input_mask; // 连续低位lane掩码
	wire [2:0]dec_parameter_window; // DW并集窗口请求身份
	wire [4:0]dec_parameter_group; // DW两形态独立组号
	wire [4:0]dec_weight_slot; // 当前任务读驻留槽
	wire [2:0]dec_write_lane; // 结果tag解为onehot
	wire [31:0]dec_write_address; // 结果tag对应冻结位置

	//-------------其他信号连线-------------//
	assign flag_active = reg_release[1] && !o_fault; // 共同释放后才传输
	assign dec_last_group = dec_dw ? (flag_tail ? 5'd1 : 5'd2) : (dec_cin / 8 - 1); // 固定Cin均整除八
	assign dec_input_count = dec_dw ? (reg_group == dec_last_group ? (flag_tail ? 4'd1 : 4'd5) : 4'd8) : 4'd8; // 并集最后五或一
	assign dec_input_mask = dec_input_count == 8 ? 8'hff : ((8'h01 << dec_input_count) - 1'b1); // 尾lane显式禁用
	assign dec_parameter_window = dec_dw ? (reg_slot < 3 ? 3'd7 : 3'd3) : 3'd0; // DW三点与末点区分
	assign dec_parameter_group = dec_dw && reg_slot >= 3 ? reg_slot - 5'd3 : reg_slot; // tail从零独立编号
	assign dec_weight_slot = dec_dw && flag_tail ? reg_group + 5'd3 : reg_group; // 与已提交槽一致
	assign dec_write_lane = i_core_output_tag == 0 ? 3'b001 : (i_core_output_tag == 1 ? 3'b010 : (i_core_output_tag == 2 ? 3'b100 : 3'b000)); // 拒绝任意旧标签
	assign dec_write_address = i_core_output_tag == 0 ? reg_addresses[31:0] : (i_core_output_tag == 1 ? reg_addresses[63:32] : reg_addresses[95:64]); // lane选对应地址
	assign flag_output_legal = dec_write_lane != 0 && (dec_write_lane & reg_output_mask) != 0 && (dec_write_lane & reg_written) == 0 && i_core_output_address == dec_write_address; // 唯一有效路且全地址相等
	assign flag_output_bad = i_core_output_valid && (state_current != ST_OUTPUT || !flag_output_legal); // 未拥有返回不得外泄
	assign flag_last_write = o_write_valid && i_write_ready && (reg_written | dec_write_lane) == reg_output_mask; // 真正接受的末路
	assign flag_series_last = dec_dw ? (flag_tail && reg_row == dec_valid_rows - 1) : reg_pixel == dec_valid_rows * 4 - 1; // 不计算H18空行
	assign flag_channel_last = reg_channel == (dec_dw ? dec_cout - 1 : dec_cout - 3); // 首批PW都整除三
	assign flag_fill_hit = flag_line_valid && reg_line_address == {dec_source_address[31:4],4'b0000}; // 地址标签匹配才使用
	assign flag_read_bad = i_read_rsp_valid && o_read_rsp_ready && (i_read_error || i_read_rsp_address != reg_read_address); // 比较完整已接受地址
	assign flag_parameter_bad = i_parameter_rsp_valid && o_parameter_rsp_ready &&
		(i_parameter_error || i_parameter_rsp_layer != reg_layer || i_parameter_rsp_channel != reg_channel ||
		i_parameter_rsp_window != dec_parameter_window || i_parameter_rsp_group != dec_parameter_group ||
		(reg_slot != 0 && i_parameter_quant != reg_quant) || i_parameter_quant[127] || i_parameter_quant[159] ||
		i_parameter_quant[191] || i_parameter_quant[241] || i_parameter_quant[197:192] == 63 ||
		i_parameter_quant[203:198] == 63 || i_parameter_quant[209:204] == 63 || i_parameter_quant[247:242] == 63); // 原量化合法域
	assign flag_work_bad = (i_byte_rsp_valid && o_byte_rsp_ready && (i_byte_rsp_error || (state_current == ST_BYTE_WRITE_WAIT && i_byte_rsp_data != 0))) ||
		(i_weight_rsp_valid && o_weight_rsp_ready && (i_weight_rsp_error || (state_current == ST_WEIGHT_WRITE_WAIT && i_weight_rsp_data != 0))); // 写完成数据必须为零
	assign flag_barrier_bad = o_barrier_valid && i_barrier_ready && (i_barrier_layer != reg_layer || i_barrier_tile_y != reg_tile_y || i_barrier_tile_x != reg_tile_x); // 防旧任务确认

	//-------------输出信号连线-------------//
	assign o_fault = flag_fault || i_cancel || i_work_fault || i_core_fault; // 外部错误立即禁止成功
	assign o_start_ready = state_current == ST_IDLE && flag_active && i_table_loaded; // 空闲无旧响应
	assign o_busy = state_current != ST_IDLE; // 错误不会释放owner
	assign o_done = state_current == ST_FINISH && flag_active; // 仅屏障完成之后
	assign o_layer_id = reg_layer; // 锁定graph身份输出
	assign o_tile_y = reg_tile_y; // 行身份全任务保持
	assign o_tile_x = reg_tile_x; // 列身份全任务保持
	assign o_parameter_valid = state_current == ST_PARAMETER && flag_active; // 参数请求可反压
	assign o_parameter_channel = reg_channel; // DW单通道或PW三通道
	assign o_parameter_window = dec_parameter_window; // 已锁定切片窗口
	assign o_parameter_group = dec_parameter_group; // 已锁定归约位置
	assign o_parameter_rsp_ready = state_current == ST_PARAMETER_WAIT && flag_active; // 单未决响应消费
	assign o_read_valid = state_current == ST_READ && flag_active; // 源读请求保持
	assign o_read_address = reg_read_address; // 不随空闲输入改变
	assign o_read_rsp_ready = state_current == ST_READ_WAIT && flag_active; // 当前源返回专属
	assign o_write_valid = state_current == ST_OUTPUT && flag_active && i_core_output_valid && flag_output_legal; // 合法才写
	assign o_write_address = i_core_output_address; // 核绑定输出地址
	assign o_write_data = i_core_output_data; // 核最终数据直达写端
	assign o_barrier_valid = state_current == ST_BARRIER && flag_active; // 必须由真实服务确认可见
	assign o_byte_req_valid = (state_current == ST_BYTE_WRITE || state_current == ST_BYTE_READ) && flag_active; // 单byte未决
	assign o_byte_req_write = state_current == ST_BYTE_WRITE; // 明确读写方向
	assign o_byte_req_addr = state_current == ST_BYTE_WRITE ? {2'b00,reg_fill_index} : dec_cache_address[11:0]; // 同步锁步索引
	assign o_byte_req_data = reg_fill_data; // 反压期间单字节保持
	assign o_byte_rsp_ready = (state_current == ST_BYTE_WRITE_WAIT || state_current == ST_BYTE_READ_WAIT) && flag_active; // 接受真实完成
	assign o_weight_req_valid = (state_current == ST_WEIGHT_WRITE || state_current == ST_WEIGHT_READ) && flag_active; // 不覆盖未完成组
	assign o_weight_req_write = state_current == ST_WEIGHT_WRITE; // 参数提交或操作数读
	assign o_weight_req_group = state_current == ST_WEIGHT_WRITE ? reg_slot : dec_weight_slot; // 事务地址全程不漂移
	assign o_weight_req_data = reg_weight; // 当前192位切片
	assign o_weight_rsp_ready = (state_current == ST_WEIGHT_WRITE_WAIT || state_current == ST_WEIGHT_READ_WAIT) && flag_active; // 等全部word完成
	assign o_core_valid = state_current == ST_SEND && flag_active; // 完整拼装后发射
	assign o_core_first = reg_group == 0; // 原核只在此组加偏置
	assign o_core_last = reg_group == dec_last_group; // 末并集或末输入通道
	assign o_core_input_mask = dec_input_mask; // 输入尾槽禁止乘加
	assign o_core_activation = reg_activation; // 未使用槽在组开始清零
	assign o_core_weight = reg_weight; // 来自WIF1同步读完成
	assign o_core_bias = {reg_output_mask[2] ? reg_quant[95:64] : 32'd0,reg_output_mask[1] ? reg_quant[63:32] : 32'd0,reg_quant[31:0]}; // 无效输出偏置零
	assign o_core_output_mask = reg_output_mask; // 三点或单点空间路
	assign o_core_tags = 48'h000200010000; // 原owner透明标签契约
	assign o_core_addresses = reg_addresses; // 元数据首组锁入owner
	assign o_core_pre_multiplier = {reg_output_mask[2] ? reg_quant[191:160] : 32'd0,reg_output_mask[1] ? reg_quant[159:128] : 32'd0,reg_quant[127:96]}; // 当前输出量化
	assign o_core_pre_shift = {reg_output_mask[2] ? reg_quant[209:204] : 6'd0,reg_output_mask[1] ? reg_quant[203:198] : 6'd0,reg_quant[197:192]}; // 移位不截断非法六十三
	assign o_core_post_multiplier = reg_quant[241:210]; // 同层按张量参数
	assign o_core_post_shift = reg_quant[247:242]; // 原后量化移位
	assign o_core_output_ready = state_current == ST_OUTPUT && flag_active && i_write_ready && flag_output_legal; // 核与外部写同拍

	// 固定层选择仅使用握手时锁定的graph编号，不解析任意网络。
	always@(*)begin
		dec_dw = 0;
		dec_height = 0;
		dec_width = 0;
		dec_cin = 0;
		dec_cout = 0;
		dec_source_base = 0;
		dec_destination_base = 0;
		case(reg_layer)
			12:begin
				dec_dw = 1;
				dec_height = 36;
				dec_width = 64;
				dec_cin = 24;
				dec_cout = 24;
				dec_source_base = 56975360;
				dec_destination_base = 57196544;
			end
			13:begin
				dec_height = 36;
				dec_width = 64;
				dec_cin = 24;
				dec_cout = 48;
				dec_source_base = 57196544;
				dec_destination_base = 57253888;
			end
			26:begin
				dec_dw = 1;
				dec_height = 18;
				dec_width = 32;
				dec_cin = 48;
				dec_cout = 48;
				dec_source_base = 57708544;
				dec_destination_base = 57819136;
			end
			27:begin
				dec_height = 18;
				dec_width = 32;
				dec_cin = 48;
				dec_cout = 96;
				dec_source_base = 57819136;
				dec_destination_base = 57851904;
			end
			default:begin
				dec_height = 0;
			end
		endcase
	end

	// 逻辑源坐标与物理tile地址区分，padding不触发外部读。
	always@(*)begin
		dec_source_height = dec_dw ? dec_height * 2 : dec_height;
		dec_source_width = dec_dw ? dec_width * 2 : dec_width;
		dec_fill_bytes = dec_dw ? 81 : 16 * dec_cin;
		dec_valid_rows = dec_height - reg_tile_y < 4 ? dec_height - reg_tile_y : 4;
		dec_source_y = reg_tile_y + reg_fill_index / (dec_cin == 0 ? 1 : 4 * dec_cin);
		dec_source_x = reg_tile_x + (reg_fill_index / (dec_cin == 0 ? 1 : dec_cin)) % 4;
		dec_source_channel = reg_fill_index % (dec_cin == 0 ? 1 : dec_cin);
		if(dec_dw)begin
			dec_source_y = reg_tile_y * 2 + reg_fill_index / 9 - 1;
			dec_source_x = reg_tile_x * 2 + reg_fill_index % 9 - 1;
			dec_source_channel = reg_channel;
		end
		dec_padding = dec_source_y < 0 || dec_source_y >= dec_source_height || dec_source_x < 0 || dec_source_x >= dec_source_width;
		dec_source_address = 0;
		if(!dec_padding)begin
			dec_source_address = dec_source_base + (((dec_source_y / 4) * (dec_source_width / 4) + dec_source_x / 4) * 16 +
				(dec_source_y % 4) * 4 + dec_source_x % 4) * dec_cin + dec_source_channel;
		end
		dec_sample = reg_group * 8 + reg_lane;
		dec_cache_address = reg_pixel * dec_cin + dec_sample;
		if(dec_dw)begin
			dec_cache_address = (reg_row * 2 + dec_sample / (flag_tail ? 3 : 7)) * 9 +
				(flag_tail ? 6 : 0) + dec_sample % (flag_tail ? 3 : 7);
		end
		dec_task_y = reg_tile_y + (dec_dw ? reg_row : reg_pixel / 4);
		dec_task_x = reg_tile_x + (dec_dw ? (flag_tail ? 3 : 0) : reg_pixel % 4);
		dec_destination_offset = (((dec_task_y / 4) * (dec_width / 4) + dec_task_x / 4) * 16 + (dec_task_y % 4) * 4 + dec_task_x % 4) * dec_cout;
		dec_addresses[31:0] = dec_destination_base + dec_destination_offset + reg_channel;
		dec_addresses[63:32] = dec_addresses[31:0] + (dec_dw ? dec_cout : 1);
		dec_addresses[95:64] = dec_addresses[31:0] + (dec_dw ? dec_cout * 2 : 2);
		dec_output_mask = dec_dw && flag_tail ? 3'b001 : 3'b111;
	end

	//--------------状态机区域--------------//
	// 异步断言后两级释放只门控新应用，不改变外部冻结核复位。
	always@(posedge i_clk or negedge i_rstn)begin
		if(!i_rstn)begin
			reg_release <= 0;
		end else begin
			reg_release <= {reg_release[0],1'b1};
		end
	end

	// 状态寄存器在共同复位清空本地未决控制。
	always@(posedge i_clk or negedge i_rstn)begin
		if(!i_rstn)begin
			state_current <= ST_IDLE;
		end else begin
			state_current <= state_next;
		end
	end

	// 所有推进依赖本端valid和对端ready；不以固定延迟冒充完成。
	always@(*)begin
		state_next = state_current;
		case(state_current)
			// 空闲只有start握手才能获得owner。
			ST_IDLE:begin
				if(i_start_valid && o_start_ready)begin
					state_next = ST_CONFIG;
				end
			end
			// 不合法固定层或非对齐tile保持错误占有。
			ST_CONFIG:begin
				if(dec_height == 0 || reg_tile_y >= dec_height || reg_tile_x >= dec_width || reg_tile_y[1:0] != 0 || reg_tile_x[1:0] != 0)begin
					state_next = ST_FAULT;
				end else begin
					state_next = ST_FILL_SETUP;
				end
			end
			// 开始覆盖共享仓使用范围。
			ST_FILL_SETUP:begin
				state_next = ST_FILL;
			end
			// padding直接填零，未命中则请求源行。
			ST_FILL:begin
				if(dec_padding || flag_fill_hit)begin
					state_next = ST_BYTE_WRITE;
				end else begin
					state_next = ST_READ;
				end
			end
			// 源读地址保持到接受。
			ST_READ:begin
				if(o_read_valid && i_read_ready)begin
					state_next = ST_READ_WAIT;
				end
			end
			// 完整行消费后再取单字节。
			ST_READ_WAIT:begin
				if(i_read_rsp_valid && o_read_rsp_ready)begin
					state_next = ST_FILL;
				end
			end
			// 提交一个填仓字节。
			ST_BYTE_WRITE:begin
				if(o_byte_req_valid && i_byte_req_ready)begin
					state_next = ST_BYTE_WRITE_WAIT;
				end
			end
			// native提交确认后才推进填仓索引。
			ST_BYTE_WRITE_WAIT:begin
				if(i_byte_rsp_valid && o_byte_rsp_ready)begin
					if(reg_fill_index == dec_fill_bytes - 1)begin
						state_next = ST_PARAMETER_SETUP;
					end else begin
						state_next = ST_FILL;
					end
				end
			end
			// 新通道的权重全部覆盖。
			ST_PARAMETER_SETUP:begin
				state_next = ST_PARAMETER;
			end
			// 参数请求只发一次。
			ST_PARAMETER:begin
				if(o_parameter_valid && i_parameter_ready)begin
					state_next = ST_PARAMETER_WAIT;
				end
			end
			// 合法参数返回后交WIF1权重仓。
			ST_PARAMETER_WAIT:begin
				if(i_parameter_rsp_valid && o_parameter_rsp_ready)begin
					state_next = ST_WEIGHT_WRITE;
				end
			end
			// 192位组写事务保持至接受。
			ST_WEIGHT_WRITE:begin
				if(o_weight_req_valid && i_weight_req_ready)begin
					state_next = ST_WEIGHT_WRITE_WAIT;
				end
			end
			// 不以request接受替代全部word提交。
			ST_WEIGHT_WRITE_WAIT:begin
				if(i_weight_rsp_valid && o_weight_rsp_ready)begin
					if(reg_slot == (dec_dw ? 4 : dec_last_group))begin
						state_next = ST_TASK_SETUP;
					end else begin
						state_next = ST_PARAMETER;
					end
				end
			end
			// 新任务清除输入尾槽与退休标志。
			ST_TASK_SETUP:begin
				state_next = ST_WEIGHT_READ;
			end
			// 每归约组读取实际驻留权重。
			ST_WEIGHT_READ:begin
				if(o_weight_req_valid && i_weight_req_ready)begin
					state_next = ST_WEIGHT_READ_WAIT;
				end
			end
			// 同步返回后才读操作数字节。
			ST_WEIGHT_READ_WAIT:begin
				if(i_weight_rsp_valid && o_weight_rsp_ready)begin
					state_next = ST_BYTE_READ;
				end
			end
			// 每次只请求一byte。
			ST_BYTE_READ:begin
				if(o_byte_req_valid && i_byte_req_ready)begin
					state_next = ST_BYTE_READ_WAIT;
				end
			end
			// 响应消费后拼入指定lane。
			ST_BYTE_READ_WAIT:begin
				if(i_byte_rsp_valid && o_byte_rsp_ready)begin
					if(reg_lane == dec_input_count - 1)begin
						state_next = ST_SEND;
					end else begin
						state_next = ST_BYTE_READ;
					end
				end
			end
			// 末组后等待所有有效输出写接受。
			ST_SEND:begin
				if(o_core_valid && i_core_ready)begin
					if(reg_group == dec_last_group)begin
						state_next = ST_OUTPUT;
					end else begin
						state_next = ST_WEIGHT_READ;
					end
				end
			end
			// 只在最后一路真正写接受后推进。
			ST_OUTPUT:begin
				if(flag_last_write)begin
					state_next = ST_ADVANCE;
				end
			end
			// 未完成空间任务复用权重，新通道重装权重。
			ST_ADVANCE:begin
				if(!flag_series_last)begin
					state_next = ST_TASK_SETUP;
				end else if(!flag_channel_last)begin
					if(dec_dw)begin
						state_next = ST_FILL_SETUP;
					end else begin
						state_next = ST_PARAMETER_SETUP;
					end
				end else begin
					state_next = ST_BARRIER;
				end
			end
			// 共享仓此时已无未退休事务；仍等外部写可见。
			ST_BARRIER:begin
				if(o_barrier_valid && i_barrier_ready)begin
					state_next = ST_FINISH;
				end
			end
			// 完成脉冲结束后释放本地计算owner。
			ST_FINISH:begin
				state_next = ST_IDLE;
			end
			// 取消不冒充排空，只共同reset能恢复。
			ST_FAULT:begin
				state_next = ST_FAULT;
			end
			// 非法状态保守占有。
			default:begin
				state_next = ST_FAULT;
			end
		endcase
		if(o_fault || flag_parameter_bad || flag_read_bad || flag_work_bad || flag_output_bad || flag_barrier_bad)begin
			state_next = ST_FAULT;
		end
	end

	//-----------状态任务处理区域-----------//
	// 只维护当前事务小寄存器；共享仓数组由C4外部唯一模块拥有。
	always@(posedge i_clk or negedge i_rstn)begin
		if(!i_rstn)begin
			reg_layer <= 0; // 清除旧graph身份
			reg_tile_y <= 0; // 清除旧tile行
			reg_tile_x <= 0; // 清除旧tile列
			reg_channel <= 0; // 通道遍历从零开始
			reg_row <= 0; // DW局部行归零
			reg_pixel <= 0; // PW像素位置归零
			reg_fill_index <= 0; // 填仓覆盖位置归零
			reg_slot <= 0; // 参数提交位置归零
			reg_group <= 0; // MAC归约位置归零
			reg_lane <= 0; // 操作数拼装位置归零
			reg_read_address <= 0; // 源未决地址撤销
			reg_line_address <= 0; // 行标签不再属于旧任务
			reg_line_data <= 0; // 小行寄存器同步取消
			reg_fill_data <= 0; // 单字节提交载荷取消
			reg_quant <= 0; // 当前输出组量化取消
			reg_weight <= 0; // 当前权重操作数取消
			reg_activation <= 0; // 当前八输入操作数取消
			reg_addresses <= 0; // 三输出元数据撤销
			reg_output_mask <= 0; // 无合法旧输出路
			reg_written <= 0; // 无旧退休凭据
			flag_line_valid <= 0; // 不使用复位前源行
			flag_tail <= 0; // 每行先运行三空间点
			flag_fault <= 0; // 共同reset唯一清故障
		end else begin
			if(state_next == ST_FAULT)begin
				flag_fault <= 1; // 故障占有不自动恢复
			end
			if(i_start_valid && o_start_ready)begin
				reg_layer <= i_layer_id; // start握手唯一身份采样点
				reg_tile_y <= i_tile_y; // 输出行整任务冻结
				reg_tile_x <= i_tile_x; // 输出列整任务冻结
				reg_channel <= 0; // 新tile从首通道开始
				reg_row <= 0; // 新DW从首有效行开始
				reg_pixel <= 0; // 新PW从首像素开始
				flag_tail <= 0; // 新DW先三点再尾点
				flag_line_valid <= 0; // 新源任务不可继承行命中
			end
			if(state_current == ST_FILL_SETUP)begin
				reg_fill_index <= 0; // 每次覆盖都从仓首字节开始
			end
			if(state_current == ST_FILL)begin
				if(dec_padding || flag_fill_hit)begin
					reg_fill_data <= dec_padding ? 8'd0 : reg_line_data[dec_source_address[3:0] * 8 +: 8]; // 取单字节或明确padding零
				end else begin
					reg_read_address <= {dec_source_address[31:4],4'b0000}; // 请求前锁定完整对齐地址
				end
			end
			if(i_read_rsp_valid && o_read_rsp_ready && !flag_read_bad)begin
				reg_line_data <= i_read_rsp_data; // 只保存已消费正确源行
				reg_line_address <= i_read_rsp_address; // 源行标签与载荷同拍登记
				flag_line_valid <= 1; // 后续填仓才可命中
			end
			if(state_current == ST_BYTE_WRITE_WAIT && i_byte_rsp_valid && o_byte_rsp_ready)begin
				reg_fill_index <= reg_fill_index + 1'b1; // 实际提交完成才推进
			end
			if(state_current == ST_PARAMETER_SETUP)begin
				reg_slot <= 0; // 新输出组覆盖所有使用槽
			end
			if(i_parameter_rsp_valid && o_parameter_rsp_ready && !flag_parameter_bad)begin
				reg_weight <= i_parameter_weight; // 当前参数权重等待WIF1提交
				if(reg_slot == 0)begin
					reg_quant <= i_parameter_quant; // 首槽锁存并核验后续相同
				end
			end
			if(state_current == ST_WEIGHT_WRITE_WAIT && i_weight_rsp_valid && o_weight_rsp_ready)begin
				reg_slot <= reg_slot + 1'b1; // 所有native权重word完成才推进
			end
			if(state_current == ST_TASK_SETUP)begin
				reg_group <= 0; // 新三输出任务从first组开始
				reg_lane <= 0; // 操作数从低lane拼装
				reg_activation <= 0; // 未使用尾lane显式清零
				reg_addresses <= dec_addresses; // 首组前冻结真实三路地址
				reg_output_mask <= dec_output_mask; // 三点与尾点固定有效路
				reg_written <= 0; // 新任务不得继承退休掩码
			end
			if(state_current == ST_WEIGHT_READ_WAIT && i_weight_rsp_valid && o_weight_rsp_ready && !flag_work_bad)begin
				reg_weight <= i_weight_rsp_data; // 同步工作仓读完才能发射
			end
			if(state_current == ST_BYTE_READ_WAIT && i_byte_rsp_valid && o_byte_rsp_ready && !flag_work_bad)begin
				reg_activation[reg_lane * 8 +: 8] <= i_byte_rsp_data; // 已消费字节进入相应INT8槽
				if(reg_lane != dec_input_count - 1)begin
					reg_lane <= reg_lane + 1'b1; // 只走真正有效输入数
				end
			end
			if(o_core_valid && i_core_ready && reg_group != dec_last_group)begin
				reg_group <= reg_group + 1'b1; // 冻结核接受才进入下一归约
				reg_lane <= 0; // 下一组重新串行读八槽
				reg_activation <= 0; // 新组尾槽不得泄漏旧输入
			end
			if(o_write_valid && i_write_ready)begin
				reg_written <= reg_written | dec_write_lane; // 每路实际写只退休一次
			end
			if(state_current == ST_ADVANCE)begin
				if(!flag_series_last)begin
					if(dec_dw)begin
						if(flag_tail)begin
							flag_tail <= 0; // 下一行重新先三点
							reg_row <= reg_row + 1'b1; // 单点退休后推进DW行
						end else begin
							flag_tail <= 1; // 三点退休后执行第四点
						end
					end else begin
						reg_pixel <= reg_pixel + 1'b1; // PW按局部HWC空间顺序
					end
				end else if(!flag_channel_last)begin
					reg_channel <= reg_channel + (dec_dw ? 1 : 3); // DW下一通道或PW下一输出三组
					reg_row <= 0; // 新通道空间行从零
					flag_tail <= 0; // 新通道先宽并集
					reg_pixel <= 0; // 新PW输出组从首像素
				end
			end
		end
	end
endmodule
