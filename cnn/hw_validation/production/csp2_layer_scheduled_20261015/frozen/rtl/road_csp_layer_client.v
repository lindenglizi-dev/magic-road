`timescale 1ns / 1ps
////////////////////////////////////English///////////////////////////////////////
// Company: RoadYOLO
// Engineer: Codex
// Create Date: 2026-10-15
// Design Name: CSP full-frame layer client
// Module Name: road_csp_layer_client
// Description: road_csp_layer_client_spec.md
// Simulations: tb_csp_layer_client
// Referrences: Frozen CSP graph and complete tile client
// Dependencies: External arithmetic owner, parameter reader and memory service
// Version: V1.0
// Revision Date: 2026-10-15
// History: 2026-10-15 V1.0 Codex Create file
///////////////////////////////////Chinese////////////////////////////////////////
// 版权归属: RoadYOLO
// 开发人员: Codex
// 创建日期: 2026-10-15
// 设计名称: CSP全幅逐层客户
// 模块名称: road_csp_layer_client
// 模块说明: 五阶段全幅调度、块输入缓存及单算术owner外围控制
// 仿真工程: tb_csp_layer_client
// 参考资料: 冻结CSP图、完整块客户及原算术接口
// 依赖文件: 外部唯一算术owner、参数读取与16字节逻辑内存服务
// 当前版本: V1.0
// 修订日期: 2026-10-15
// 修订历史: 2026-10-15 V1.0 Codex 创建文件
module road_csp_layer_client(
	input i_clk, // 与算术owner同域100MHz
	input i_rstn, // 共同异步复位，服务同时撤销旧响应
	input i_start, // ready时启动一次完整72乘128任务
	input i_cancel, // 取消后故障占有至共同复位
	input i_table_loaded, // 外部owner已装入同包SiLU表
	output o_start_ready, // 空闲、无故障且表有效
	output o_busy, // 包含完成拍和故障占有
	output o_done, // 末阶段可见性确认后单拍完成
	output o_fault, // 信任边界错误粘滞指示
	output [2:0]o_layer, // 当前五阶段编号
	output [6:0]o_tile_y, // 当前四行块起点诊断
	output [7:0]o_tile_x, // 当前四列块起点诊断
	output o_parameter_valid, // 当前参数分片请求有效
	output [4:0]o_parameter_channel, // DW通道或PW输出三通道起点
	output [1:0]o_parameter_group, // 八输入归约组编号
	output [2:0]o_parameter_window, // DW窗口并集宽度，PW为零
	input i_parameter_ready, // 参数请求被服务接受
	input i_parameter_response_valid, // 参数响应保持至ready
	output o_parameter_response_ready, // 只消费当前未完成请求
	input [2:0]i_parameter_response_layer, // 参数响应阶段身份
	input [4:0]i_parameter_response_channel, // 参数响应输出通道身份
	input [1:0]i_parameter_response_group, // 参数响应归约组身份
	input [2:0]i_parameter_response_window, // 参数响应DW窗口形态
	input [191:0]i_parameter_weight, // 三路八输入权重
	input [247:0]i_parameter_data, // bias及动态量化字段
	input i_parameter_error, // 参数服务显式错误
	output o_read_valid, // 单个16字节行请求有效
	output [31:0]o_read_address, // 十六字节对齐逻辑地址
	input i_read_ready, // 行请求被内存服务接受
	input i_read_response_valid, // 行响应保持至ready
	output o_read_response_ready, // 只消费当前未完成行请求
	input [31:0]i_read_response_address, // 必须匹配请求的对齐地址
	input [127:0]i_read_response_data, // 低字节对应地址偏移零
	input i_read_error, // 内存服务显式读错误
	output o_write_valid, // 合法核结果写请求
	output [31:0]o_write_address, // 完整冻结图字节地址
	output [7:0]o_write_data, // 最终饱和INT8结果
	output signed [8:0]o_write_sum, // 饱和前signed9残差和
	input i_write_ready, // 外部写服务接受
	output o_barrier_valid, // 当前整层全部写接受后的屏障
	input i_barrier_ready, // 此层此前写已经可读
	input [2:0]i_barrier_layer, // 屏障确认所属阶段
	output o_core_valid, // 原算术核输入组有效
	input i_core_ready, // 原算术核输入组接受
	output o_core_first, // 当前任务首归约组
	output o_core_last, // 当前任务末归约组
	output [7:0]o_core_input_mask, // 当前八输入有效掩码
	output [63:0]o_core_activation, // 串行拼装的八个INT8输入
	output [191:0]o_core_weight, // 驻留参数分片
	output [95:0]o_core_bias, // 三路首组偏置
	output [2:0]o_core_output_mask, // DW尾空间任务只启用lane零
	output [47:0]o_core_tags, // 固定三路任务身份
	output [95:0]o_core_addresses, // 三路完整写地址
	output [95:0]o_core_pre_multiplier, // 三路动态前乘数
	output [17:0]o_core_pre_shift, // 三路六位前移位
	output [31:0]o_core_post_multiplier, // 当前层共享后乘数
	output [5:0]o_core_post_shift, // 当前层共享后移位
	output o_core_residual, // 两个PW残差阶段使能
	output [23:0]o_core_bypass, // 三路真实旁路值
	input i_core_output_valid, // 原五级写回结果有效
	output o_core_output_ready, // 核结果和外部写原子接受
	input [15:0]i_core_output_tag, // 原核返回任务lane
	input [31:0]i_core_output_address, // 原核返回完整地址
	input [7:0]i_core_output_data, // 原核返回sat8数据
	input signed [8:0]i_core_output_sum, // 原核返回signed9和
	input i_core_fault // 原核错误保持原语义
);
	//-----------------状态参数区域-----------------//
	localparam [4:0]ST_IDLE = 0; // 等待完整表与全幅启动
	localparam [4:0]ST_TILE_SETUP = 1; // 初始化四乘四块预取
	localparam [4:0]ST_PREFETCH = 2; // 每拍写一个块缓存字节
	localparam [4:0]ST_READ = 3; // 保持对齐行请求至接受
	localparam [4:0]ST_READ_WAIT = 4; // 等待匹配的128位行响应
	localparam [4:0]ST_PARAMETER = 5; // 保持参数请求至接受
	localparam [4:0]ST_PARAMETER_WAIT = 6; // 等待匹配参数响应
	localparam [4:0]ST_TASK_SETUP = 7; // 冻结当前算术任务元数据
	localparam [4:0]ST_CACHE_ACTIVATION = 8; // 单端口逐字节拼装输入
	localparam [4:0]ST_CACHE_BYPASS = 9; // 单端口逐字节拼装旁路
	localparam [4:0]ST_SEND = 10; // 保持完整核输入组至接受
	localparam [4:0]ST_WRITE_WAIT = 11; // 原子退休全部合法输出
	localparam [4:0]ST_RETIRE = 12; // 等待注册的任务完成凭据
	localparam [4:0]ST_ADVANCE = 13; // 推进任务、通道或块
	localparam [4:0]ST_BARRIER = 14; // 等待完整阶段写可见
	localparam [4:0]ST_FINISH = 15; // 完整五阶段完成单拍
	localparam [4:0]ST_FAULT = 16; // 故障占有直到共同复位

	//-----------------状态机信号-----------------//
	reg [4:0]state_current; // 当前控制状态
	reg [4:0]state_next; // 下一控制状态

	//-----------------寄存器信号-----------------//
	reg [2:0]reg_layer; // 当前卷积阶段
	reg [6:0]reg_tile_y; // 当前块全图行起点
	reg [7:0]reg_tile_x; // 当前块全图列起点
	reg [4:0]reg_channel; // DW通道或PW三输出起点
	reg [1:0]reg_group; // 当前归约组
	reg [1:0]reg_spatial_row; // DW块内输出行
	reg flag_spatial_tail; // DW三空间点后的单点尾任务
	reg [3:0]reg_pixel; // PW块内像素序号
	reg [8:0]reg_prefetch_index; // 块缓存填充索引
	reg [2:0]reg_parameter_slot; // 驻留参数分片索引
	reg [2:0]reg_cache_lane; // 单端口输入拼装槽
	reg [1:0]reg_bypass_lane; // 单端口旁路拼装槽
	reg [31:0]reg_read_address; // 未完成行请求地址
	reg [31:0]reg_line_address; // 当前16字节行标签
	reg [127:0]reg_line_data; // 当前16字节行数据
	reg flag_line_valid; // 行标签和数据可用
	reg [7:0]reg_tile_cache [0:431]; // 最大DW六乘六乘十二块缓存
	reg [191:0]reg_weight_primary; // 参数槽零驻留权重
	reg [191:0]reg_weight_secondary; // 参数槽一驻留权重
	reg [191:0]reg_weight_tertiary; // 参数槽二驻留权重
	reg [191:0]reg_weight_tail; // 参数槽三驻留权重
	reg [247:0]reg_parameter; // 当前输出组量化字段
	reg [63:0]reg_activation; // 当前核输入组
	reg [23:0]reg_bypass; // 当前任务三路旁路
	reg [2:0]reg_output_mask; // 当前任务有效输出路
	reg [2:0]reg_written; // 当前任务已接受写路
	reg [95:0]reg_addresses; // 当前任务三路写地址
	reg flag_task_done; // 末次真实写后一拍凭据
	reg flag_fault; // 协议错误粘滞寄存器

	//-----------------其他信号-----------------//
	wire flag_dw; // 两个深度卷积阶段
	wire flag_residual; // 两个残差PW阶段
	wire [1:0]wire_last_group; // 当前任务末归约组
	wire [3:0]wire_input_count; // 当前组真实输入字节数
	wire [7:0]wire_input_mask; // 当前组真实输入掩码
	wire flag_prefetch_hit; // 当前源字节命中行缓存
	wire flag_prefetch_fill; // 当前周期可写一个缓存字节
	wire flag_prefetch_last; // 当前为块缓存末字节
	wire flag_parameter_last; // 当前为输出组末参数分片
	wire flag_activation_last; // 当前为核输入末字节
	wire flag_bypass_last; // 当前为旁路末字节
	wire flag_core_accept; // 原核输入组真实接受
	wire flag_parameter_accept; // 参数响应真实消费
	wire flag_read_accept; // 行响应真实消费
	wire [2:0]wire_write_lane; // 返回tag对应onehot路
	wire flag_write_legal; // 核结果身份地址均合法
	wire flag_write_accept; // 外部写与核退休原子接受
	wire flag_last_write; // 当前任务最后一路写接受
	wire flag_bad_parameter; // 参数身份、错误或量化漂移
	wire flag_bad_read; // 行错误、错地址或非对齐
	wire flag_bad_write; // 旧结果、错tag、重复或错地址
	wire flag_task_series_last; // 当前通道最后空间任务
	wire flag_channel_last; // 当前块最后输出通道组
	wire flag_tile_last; // 当前层最后四乘四块
	integer dec_prefetch_y; // 预取字节全图行
	integer dec_prefetch_x; // 预取字节全图列
	integer dec_prefetch_channel; // 预取物理通道
	integer dec_prefetch_channels; // 预取张量通道数
	integer dec_prefetch_local; // 预取索引局部偏移
	integer dec_prefetch_pixel; // 预取块内像素
	integer dec_task_y; // 当前任务输出行
	integer dec_task_x; // 当前任务输出列
	integer dec_task_channel; // 当前任务输出通道
	integer dec_task_channels; // 当前任务输出张量通道数
	integer dec_task_lane; // 当前任务输出lane
	integer dec_cache_slot; // 当前归约输入槽
	integer dec_cache_row; // DW缓存行
	integer dec_cache_column; // DW缓存列
	integer dec_cache_index; // 单端口缓存读取索引
	integer dec_bypass_index; // 单端口旁路读取索引
	reg [8:0]dec_prefetch_bytes; // 当前块需要覆盖的缓存字节
	reg [31:0]dec_prefetch_base; // 当前源张量基址
	reg [31:0]dec_prefetch_address; // 当前源逻辑字节地址
	reg flag_prefetch_padding; // 全幅图像外补零
	reg [2:0]dec_parameter_window; // 当前请求参数窗口
	reg [1:0]dec_parameter_group; // 当前请求参数组
	reg [31:0]dec_task_base; // 当前输出阶段基址
	reg [2:0]dec_task_mask; // 当前任务输出有效路
	reg [95:0]dec_task_addresses; // 当前任务三路输出地址
	reg [191:0]dec_selected_weight; // 当前驻留参数选择

	//-----------------其他信号连线-----------------//
	assign flag_dw = reg_layer == 0 || reg_layer == 2; // DW阶段使用空间三加尾一
	assign flag_residual = reg_layer == 1 || reg_layer == 3; // PW残差只在两层使能
	assign wire_last_group = reg_layer == 4 ? 2'd2 : 2'd1; // 融合层具有三个八输入组
	assign wire_input_count = flag_dw ? (reg_group == 0 ? 4'd8 : (flag_spatial_tail ? 4'd1 : 4'd7)) :
		(reg_layer == 4 ? 4'd8 : (reg_group == 0 ? 4'd8 : 4'd4)); // 尾输入不浪费缓存读拍
	assign wire_input_mask = wire_input_count == 8 ? 8'hff : (8'h01 << wire_input_count) - 1'b1; // 低lane连续有效
	assign flag_prefetch_hit = flag_line_valid && reg_line_address == {dec_prefetch_address[31:4],4'b0000}; // 单行全地址标签
	assign flag_prefetch_fill = flag_prefetch_padding || flag_prefetch_hit; // padding和命中均每拍写一字节
	assign flag_prefetch_last = reg_prefetch_index == dec_prefetch_bytes - 1'b1; // 整个块输入已经覆盖
	assign flag_parameter_last = flag_dw ? reg_parameter_slot == 3 : reg_parameter_slot == wire_last_group; // DW驻留两种窗口
	assign flag_activation_last = reg_cache_lane == wire_input_count - 1'b1; // 单端口拼装完成
	assign flag_bypass_last = reg_bypass_lane == 2; // 三路旁路完成
	assign flag_core_accept = o_core_valid && i_core_ready; // 核只随共同握手推进
	assign flag_parameter_accept = i_parameter_response_valid && o_parameter_response_ready; // 响应只消费一次
	assign flag_read_accept = i_read_response_valid && o_read_response_ready; // 行响应只消费一次
	assign wire_write_lane = i_core_output_tag == 0 ? 3'b001 : i_core_output_tag == 1 ? 3'b010 :
		(i_core_output_tag == 2 ? 3'b100 : 3'b000); // 只允许固定三路tag
	assign flag_write_legal = wire_write_lane != 0 && (wire_write_lane & reg_output_mask) != 0 &&
		(wire_write_lane & reg_written) == 0 && i_core_output_address ==
		(i_core_output_tag == 0 ? reg_addresses[31:0] :
		(i_core_output_tag == 1 ? reg_addresses[63:32] : reg_addresses[95:64])); // 地址及唯一性同时核对
	assign flag_write_accept = o_write_valid && i_write_ready; // 核和外部写同拍退休
	assign flag_last_write = flag_write_accept && (reg_written | wire_write_lane) == reg_output_mask; // 以实际接受结束任务
	assign flag_bad_parameter = flag_parameter_accept && (i_parameter_error || i_parameter_response_layer != reg_layer ||
		i_parameter_response_channel != reg_channel || i_parameter_response_group != dec_parameter_group ||
		i_parameter_response_window != dec_parameter_window || (reg_parameter_slot != 0 && i_parameter_data != reg_parameter)); // 禁止错路由与组间漂移
	assign flag_bad_read = flag_read_accept && (i_read_error || i_read_response_address != reg_read_address ||
		i_read_response_address[3:0] != 0); // 对齐地址必须严格匹配
	assign flag_bad_write = i_core_output_valid && (state_current != ST_WRITE_WAIT || !flag_write_legal); // 非当前任务结果拒写
	assign flag_task_series_last = flag_dw ? (reg_spatial_row == 3 && flag_spatial_tail) : reg_pixel == 15; // 通道内空间遍历完成
	assign flag_channel_last = reg_channel == (flag_dw ? 11 : (reg_layer == 4 ? 21 : 9)); // 当前块通道遍历完成
	assign flag_tile_last = reg_tile_y == 68 && reg_tile_x == 124; // 576个块的末块

	//-----------------输出信号连线-----------------//
	assign o_start_ready = state_current == ST_IDLE && i_rstn && i_table_loaded && !o_fault; // 不在表未装或故障时启动
	assign o_busy = state_current != ST_IDLE; // 故障状态不冒充排空
	assign o_done = state_current == ST_FINISH && !o_fault; // 最终整层屏障之后完成
	assign o_fault = flag_fault || i_core_fault || i_cancel; // 外部取消和核错误立即阻止传输
	assign o_layer = reg_layer; // 当前阶段诊断及屏障身份
	assign o_tile_y = reg_tile_y; // 当前块行诊断
	assign o_tile_x = reg_tile_x; // 当前块列诊断
	assign o_parameter_valid = state_current == ST_PARAMETER && !o_fault; // 请求载荷由寄存器保持
	assign o_parameter_channel = reg_channel; // 当前输出通道组
	assign o_parameter_group = dec_parameter_group; // DW两套窗口各自组编号
	assign o_parameter_window = dec_parameter_window; // window五和window三绝不混用
	assign o_parameter_response_ready = state_current == ST_PARAMETER_WAIT && !o_fault; // 只接受当前请求响应
	assign o_read_valid = state_current == ST_READ && !o_fault; // 最多一个未完成行请求
	assign o_read_address = reg_read_address; // 请求保持期间不变
	assign o_read_response_ready = state_current == ST_READ_WAIT && !o_fault; // 不消费旧任务响应
	assign o_write_valid = state_current == ST_WRITE_WAIT && i_core_output_valid && flag_write_legal && !o_fault; // 非法结果不外泄
	assign o_write_address = i_core_output_address; // 使用核冻结完整地址
	assign o_write_data = i_core_output_data; // 使用核最终sat8值
	assign o_write_sum = i_core_output_sum; // 保留signed9诊断
	assign o_barrier_valid = state_current == ST_BARRIER && !o_fault; // 每完整阶段仅一个屏障
	assign o_core_valid = state_current == ST_SEND && !o_fault; // 组载荷保持至ready
	assign o_core_first = reg_group == 0; // 首组加入偏置和元数据
	assign o_core_last = reg_group == wire_last_group; // 末组关闭归约
	assign o_core_input_mask = wire_input_mask; // 串行拼装数对应掩码
	assign o_core_activation = reg_activation; // 缓存读口逐字节拼装结果
	assign o_core_weight = {reg_output_mask[2] ? dec_selected_weight[191:128] : 64'd0,
		reg_output_mask[1] ? dec_selected_weight[127:64] : 64'd0,
		reg_output_mask[0] ? dec_selected_weight[63:0] : 64'd0}; // 无效空间路权重清零
	assign o_core_bias = {reg_output_mask[2] ? reg_parameter[95:64] : 32'd0,
		reg_output_mask[1] ? reg_parameter[63:32] : 32'd0,
		reg_output_mask[0] ? reg_parameter[31:0] : 32'd0}; // 无效空间路偏置清零
	assign o_core_output_mask = reg_output_mask; // 当前任务固定输出掩码
	assign o_core_tags = 48'h000200010000; // lane零一二身份保持旧接口
	assign o_core_addresses = reg_addresses; // 三路真实目标地址
	assign o_core_pre_multiplier = {reg_output_mask[2] ? reg_parameter[191:160] : 32'd0,
		reg_output_mask[1] ? reg_parameter[159:128] : 32'd0,
		reg_output_mask[0] ? reg_parameter[127:96] : 32'd0}; // 通道量化参数与输出路绑定
	assign o_core_pre_shift = {reg_output_mask[2] ? reg_parameter[209:204] : 6'd0,
		reg_output_mask[1] ? reg_parameter[203:198] : 6'd0,
		reg_output_mask[0] ? reg_parameter[197:192] : 6'd0}; // 六位移位保持原布局
	assign o_core_post_multiplier = reg_parameter[241:210]; // 当前层共享后乘数
	assign o_core_post_shift = reg_parameter[247:242]; // 当前层共享后移位
	assign o_core_residual = flag_residual; // 末端融合不做残差
	assign o_core_bypass = reg_bypass; // 仅PW首组使用的旁路数据
	assign o_core_output_ready = state_current == ST_WRITE_WAIT && i_write_ready && flag_write_legal && !o_fault; // 双端共同接受

	// 参数槽零一是DW五列窗口，槽二三是DW三列尾窗口；PW直接按归约组编号。
	always @(*)begin
		dec_parameter_group = reg_parameter_slot[1:0];
		dec_parameter_window = 0;
		if(flag_dw)begin
			dec_parameter_group = {1'b0,reg_parameter_slot[0]};
			dec_parameter_window = reg_parameter_slot[1] ? 3'd3 : 3'd5;
		end
	end

	// 固定图源地址仅在块预取期间使用，物理块缓存每字节都在任务前覆盖。
	always @(*)begin
		dec_prefetch_bytes = flag_dw ? 9'd432 : 9'd384;
		dec_prefetch_y = reg_tile_y;
		dec_prefetch_x = reg_tile_x;
		dec_prefetch_channel = 0;
		dec_prefetch_channels = 12;
		dec_prefetch_local = reg_prefetch_index;
		dec_prefetch_pixel = 0;
		dec_prefetch_base = 32'h035b4000;
		flag_prefetch_padding = 0;
		if(flag_dw)begin
			dec_prefetch_y = reg_tile_y + reg_prefetch_index / 72 - 1;
			dec_prefetch_x = reg_tile_x + (reg_prefetch_index % 72) / 12 - 1;
			dec_prefetch_channel = reg_prefetch_index % 12;
			if(reg_layer == 0)begin
				dec_prefetch_channels = 24;
				dec_prefetch_channel = dec_prefetch_channel + 12;
			end else begin
				dec_prefetch_base = 32'h03605000;
			end
			flag_prefetch_padding = dec_prefetch_y < 0 || dec_prefetch_y >= 72 ||
				dec_prefetch_x < 0 || dec_prefetch_x >= 128;
		end else if(reg_layer == 1 || reg_layer == 3)begin
			if(reg_prefetch_index >= 192)dec_prefetch_local = reg_prefetch_index - 192;
			dec_prefetch_pixel = dec_prefetch_local / 12;
			dec_prefetch_y = reg_tile_y + dec_prefetch_pixel / 4;
			dec_prefetch_x = reg_tile_x + dec_prefetch_pixel % 4;
			dec_prefetch_channel = dec_prefetch_local % 12;
			if(reg_layer == 1)begin
				if(reg_prefetch_index < 192)dec_prefetch_base = 32'h035ea000;
				else begin
					dec_prefetch_base = 32'h035b4000;
					dec_prefetch_channels = 24;
					dec_prefetch_channel = dec_prefetch_channel + 12;
				end
			end else begin
				dec_prefetch_base = reg_prefetch_index < 192 ? 32'h03620000 : 32'h03605000;
			end
		end else begin
			dec_prefetch_pixel = reg_prefetch_index / 24;
			dec_prefetch_y = reg_tile_y + dec_prefetch_pixel / 4;
			dec_prefetch_x = reg_tile_x + dec_prefetch_pixel % 4;
			dec_prefetch_channel = reg_prefetch_index % 24;
			dec_prefetch_channels = dec_prefetch_channel < 12 ? 24 : 12;
			if(dec_prefetch_channel < 12)dec_prefetch_base = 32'h035b4000;
			else begin
				dec_prefetch_base = 32'h0363b000;
				dec_prefetch_channel = dec_prefetch_channel - 12;
			end
		end
		dec_prefetch_address = 0;
		if(!flag_prefetch_padding)begin
			dec_prefetch_address = dec_prefetch_base +
				(((dec_prefetch_y / 4) * 32 + dec_prefetch_x / 4) * 16 +
				(dec_prefetch_y % 4) * 4 + dec_prefetch_x % 4) *
				dec_prefetch_channels + dec_prefetch_channel;
		end
	end

	// 任务地址沿tile4x4_hwc布局生成；每个全幅逻辑输出只由一个块任务拥有。
	always @(*)begin
		case(reg_layer)
			0:dec_task_base = 32'h035ea000;
			1:dec_task_base = 32'h03605000;
			2:dec_task_base = 32'h03620000;
			3:dec_task_base = 32'h0363b000;
			default:dec_task_base = 32'h03656000;
		endcase
		dec_task_channels = reg_layer == 4 ? 24 : 12;
		dec_task_mask = flag_dw && flag_spatial_tail ? 3'b001 : 3'b111;
		dec_task_addresses = 0;
		if(flag_dw)begin
			dec_task_y = reg_tile_y + reg_spatial_row;
			dec_task_x = reg_tile_x + (flag_spatial_tail ? 3 : 0);
		end else begin
			dec_task_y = reg_tile_y + reg_pixel / 4;
			dec_task_x = reg_tile_x + reg_pixel % 4;
		end
		for(dec_task_lane = 0; dec_task_lane < 3; dec_task_lane = dec_task_lane + 1)begin
			if(dec_task_mask[dec_task_lane])begin
				dec_task_channel = reg_channel + (flag_dw ? 0 : dec_task_lane);
				dec_task_addresses[dec_task_lane * 32 +: 32] = dec_task_base +
					(((dec_task_y / 4) * 32 + (dec_task_x + (flag_dw ? dec_task_lane : 0)) / 4) * 16 +
					(dec_task_y % 4) * 4 + (dec_task_x + (flag_dw ? dec_task_lane : 0)) % 4) *
					dec_task_channels + dec_task_channel;
			end
		end
	end

	// 单端口缓存读地址按当前归约槽逐拍变化，尾组只读取真实输入字节。
	always @(*)begin
		dec_cache_slot = reg_group * 8 + reg_cache_lane;
		dec_cache_row = 0;
		dec_cache_column = 0;
		dec_cache_index = 0;
		dec_bypass_index = 192 + reg_pixel * 12 + reg_channel + reg_bypass_lane;
		if(flag_dw)begin
			dec_cache_row = dec_cache_slot / (flag_spatial_tail ? 3 : 5);
			dec_cache_column = dec_cache_slot % (flag_spatial_tail ? 3 : 5);
			dec_cache_index = ((reg_spatial_row + dec_cache_row) * 6 +
				(flag_spatial_tail ? 3 : 0) + dec_cache_column) * 12 + reg_channel;
		end else if(reg_layer == 4)begin
			dec_cache_index = reg_pixel * 24 + dec_cache_slot;
		end else begin
			dec_cache_index = reg_pixel * 12 + dec_cache_slot;
		end
	end

	// 驻留参数仅在输出组切换时重取，DW两种窗口保留各自独立权重集合。
	always @(*)begin
		dec_selected_weight = reg_weight_primary;
		if(flag_dw)begin
			if(flag_spatial_tail)dec_selected_weight = reg_group == 0 ? reg_weight_tertiary : reg_weight_tail;
			else dec_selected_weight = reg_group == 0 ? reg_weight_primary : reg_weight_secondary;
		end else begin
			case(reg_group)
				0:dec_selected_weight = reg_weight_primary;
				1:dec_selected_weight = reg_weight_secondary;
				default:dec_selected_weight = reg_weight_tertiary;
			endcase
		end
	end

	// 状态寄存器独立更新，故障态只能由共同复位释放。
	always @(posedge i_clk or negedge i_rstn)begin
		if(!i_rstn)state_current <= ST_IDLE;
		else state_current <= state_next;
	end

	// 下一状态只依赖已注册身份和明确握手事件。
	always @(*)begin
		state_next = state_current;
		case(state_current)
			ST_IDLE:begin
				if(i_start && o_start_ready)state_next = ST_TILE_SETUP;
			end
			ST_TILE_SETUP:begin
				state_next = ST_PREFETCH;
			end
			ST_PREFETCH:begin
				if(flag_prefetch_fill)begin
					if(flag_prefetch_last)state_next = ST_PARAMETER;
				end else begin
					state_next = ST_READ;
				end
			end
			ST_READ:begin
				if(i_read_ready)state_next = ST_READ_WAIT;
			end
			ST_READ_WAIT:begin
				if(flag_read_accept)state_next = ST_PREFETCH;
			end
			ST_PARAMETER:begin
				if(i_parameter_ready)state_next = ST_PARAMETER_WAIT;
			end
			ST_PARAMETER_WAIT:begin
				if(flag_parameter_accept)begin
					if(flag_parameter_last)state_next = ST_TASK_SETUP;
					else state_next = ST_PARAMETER;
				end
			end
			ST_TASK_SETUP:begin
				state_next = ST_CACHE_ACTIVATION;
			end
			ST_CACHE_ACTIVATION:begin
				if(flag_activation_last)begin
					if(flag_residual && reg_group == 0)state_next = ST_CACHE_BYPASS;
					else state_next = ST_SEND;
				end
			end
			ST_CACHE_BYPASS:begin
				if(flag_bypass_last)state_next = ST_SEND;
			end
			ST_SEND:begin
				if(flag_core_accept)begin
					if(reg_group == wire_last_group)state_next = ST_WRITE_WAIT;
					else state_next = ST_CACHE_ACTIVATION;
				end
			end
			ST_WRITE_WAIT:begin
				if(flag_last_write)state_next = ST_RETIRE;
			end
			ST_RETIRE:begin
				if(flag_task_done)state_next = ST_ADVANCE;
			end
			ST_ADVANCE:begin
				if(!flag_task_series_last)state_next = ST_TASK_SETUP;
				else if(!flag_channel_last)state_next = ST_PARAMETER;
				else if(flag_tile_last)state_next = ST_BARRIER;
				else state_next = ST_TILE_SETUP;
			end
			ST_BARRIER:begin
				if(i_barrier_ready && i_barrier_layer == reg_layer)begin
					if(reg_layer == 4)state_next = ST_FINISH;
					else state_next = ST_TILE_SETUP;
				end
			end
			ST_FINISH:begin
				state_next = ST_IDLE;
			end
			ST_FAULT:begin
				state_next = ST_FAULT;
			end
			default:begin
				state_next = ST_FAULT;
			end
		endcase
		if(i_cancel || i_core_fault || flag_bad_parameter || flag_bad_read || flag_bad_write ||
			(o_barrier_valid && i_barrier_ready && i_barrier_layer != reg_layer))state_next = ST_FAULT;
	end

	// 状态任务过程集中维护缓存、参数、任务遍历和粘滞故障，不复位大字节数组。
	always @(posedge i_clk or negedge i_rstn)begin
		if(!i_rstn)begin
			reg_layer <= 0;
			reg_tile_y <= 0;
			reg_tile_x <= 0;
			reg_channel <= 0;
			reg_group <= 0;
			reg_spatial_row <= 0;
			flag_spatial_tail <= 0;
			reg_pixel <= 0;
			reg_prefetch_index <= 0;
			reg_parameter_slot <= 0;
			reg_cache_lane <= 0;
			reg_bypass_lane <= 0;
			reg_read_address <= 0;
			reg_line_address <= 0;
			reg_line_data <= 0;
			flag_line_valid <= 0;
			reg_weight_primary <= 0;
			reg_weight_secondary <= 0;
			reg_weight_tertiary <= 0;
			reg_weight_tail <= 0;
			reg_parameter <= 0;
			reg_activation <= 0;
			reg_bypass <= 0;
			reg_output_mask <= 0;
			reg_written <= 0;
			reg_addresses <= 0;
			flag_task_done <= 0;
			flag_fault <= 0;
		end else begin
			flag_task_done <= flag_last_write;
			if(i_cancel || i_core_fault || flag_bad_parameter || flag_bad_read || flag_bad_write ||
				(o_barrier_valid && i_barrier_ready && i_barrier_layer != reg_layer))flag_fault <= 1'b1;
			if(i_start && o_start_ready)begin
				reg_layer <= 0;
				reg_tile_y <= 0;
				reg_tile_x <= 0;
				flag_line_valid <= 0;
			end
			if(state_current == ST_TILE_SETUP)begin
				reg_prefetch_index <= 0;
				reg_channel <= 0;
				reg_group <= 0;
				reg_spatial_row <= 0;
				flag_spatial_tail <= 0;
				reg_pixel <= 0;
				reg_parameter_slot <= 0;
			end
			if(state_current == ST_PREFETCH)begin
				if(flag_prefetch_fill)begin
					if(flag_prefetch_padding)reg_tile_cache[reg_prefetch_index] <= 0;
					else reg_tile_cache[reg_prefetch_index] <= reg_line_data[dec_prefetch_address[3:0] * 8 +: 8];
					if(!flag_prefetch_last)reg_prefetch_index <= reg_prefetch_index + 1'b1;
				end else begin
					reg_read_address <= {dec_prefetch_address[31:4],4'b0000};
				end
			end
			if(flag_read_accept && !flag_bad_read)begin
				reg_line_address <= i_read_response_address;
				reg_line_data <= i_read_response_data;
				flag_line_valid <= 1'b1;
			end
			if(flag_parameter_accept && !flag_bad_parameter)begin
				case(reg_parameter_slot)
					0:begin
						reg_weight_primary <= i_parameter_weight;
						reg_parameter <= i_parameter_data;
					end
					1:reg_weight_secondary <= i_parameter_weight;
					2:reg_weight_tertiary <= i_parameter_weight;
					default:reg_weight_tail <= i_parameter_weight;
				endcase
				if(!flag_parameter_last)reg_parameter_slot <= reg_parameter_slot + 1'b1;
			end
			if(state_current == ST_TASK_SETUP)begin
				reg_group <= 0;
				reg_cache_lane <= 0;
				reg_bypass_lane <= 0;
				reg_activation <= 0;
				reg_bypass <= 0;
				reg_output_mask <= dec_task_mask;
				reg_addresses <= dec_task_addresses;
				reg_written <= 0;
			end
			if(state_current == ST_CACHE_ACTIVATION)begin
				reg_activation[reg_cache_lane * 8 +: 8] <= reg_tile_cache[dec_cache_index];
				if(!flag_activation_last)reg_cache_lane <= reg_cache_lane + 1'b1;
			end
			if(state_current == ST_CACHE_BYPASS)begin
				reg_bypass[reg_bypass_lane * 8 +: 8] <= reg_tile_cache[dec_bypass_index];
				if(!flag_bypass_last)reg_bypass_lane <= reg_bypass_lane + 1'b1;
			end
			if(flag_core_accept && reg_group != wire_last_group)begin
				reg_group <= reg_group + 1'b1;
				reg_cache_lane <= 0;
				reg_activation <= 0;
			end
			if(flag_write_accept)reg_written <= reg_written | wire_write_lane;
			if(state_current == ST_ADVANCE)begin
				if(!flag_task_series_last)begin
					if(flag_dw)begin
						if(flag_spatial_tail)begin
							flag_spatial_tail <= 0;
							reg_spatial_row <= reg_spatial_row + 1'b1;
						end else begin
							flag_spatial_tail <= 1'b1;
						end
					end else begin
						reg_pixel <= reg_pixel + 1'b1;
					end
				end else if(!flag_channel_last)begin
					reg_channel <= reg_channel + (flag_dw ? 1 : 3);
					reg_parameter_slot <= 0;
					reg_group <= 0;
					reg_spatial_row <= 0;
					flag_spatial_tail <= 0;
					reg_pixel <= 0;
				end else if(!flag_tile_last)begin
					if(reg_tile_x == 124)begin
						reg_tile_x <= 0;
						reg_tile_y <= reg_tile_y + 4;
					end else begin
						reg_tile_x <= reg_tile_x + 4;
					end
				end
			end
			if(state_current == ST_BARRIER && i_barrier_ready && i_barrier_layer == reg_layer && reg_layer != 4)begin
				reg_layer <= reg_layer + 1'b1;
				reg_tile_y <= 0;
				reg_tile_x <= 0;
				flag_line_valid <= 0;
			end
		end
	end
endmodule
