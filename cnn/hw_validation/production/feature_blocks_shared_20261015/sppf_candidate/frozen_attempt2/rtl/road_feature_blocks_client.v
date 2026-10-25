`timescale 1ns / 1ps
////////////////////////////////////English///////////////////////////////////////
// Company: RoadYOLO
// Engineer: Codex
// Create Date: 2026-10-15
// Design Name: Fixed CSP and SPPF shared client
// Module Name: road_feature_blocks_client
// Description: road_feature_blocks_client_spec.md
// Simulations: tb_feature_blocks_client
// Referrences: Frozen graph.json and sealed CSP2 layer client
// Dependencies: External arithmetic owner, parameter reader and memory service
// Version: V1.0
// Revision Date: 2026-10-15
// History: 2026-10-15 V1.0 Codex Create file
///////////////////////////////////Chinese////////////////////////////////////////
// 版权归属: RoadYOLO
// 开发人员: Codex
// 创建日期: 2026-10-15
// 设计名称: 固定CSP与SPPF共享逐层客户
// 模块名称: road_feature_blocks_client
// 模块说明: 锁存块身份、唯一状态机与工作缓存、单算术owner控制
// 仿真工程: tb_feature_blocks_client
// 参考资料: 冻结graph.json与封存CSP2逐层客户
// 依赖文件: 外部唯一算术owner、参数读取与16字节逻辑内存服务
// 当前版本: V1.0
// 修订日期: 2026-10-15
// 修订历史: 2026-10-15 V1.0 Codex 创建文件
module road_feature_blocks_client(
	input i_clk, // 与算术owner同域100MHz
	input i_rstn, // 共同异步复位，服务同时撤销旧响应
	input [3:0]i_block_id, // 仅start握手锁存的固定块编号
	output [3:0]o_block_id, // 当前任务身份直到下一次start保持
	input i_start, // ready时启动一次完整固定图任务
	input i_cancel, // 取消后故障占有至共同复位
	input i_table_loaded, // 外部owner已装入同包SiLU表
	output o_start_ready, // 空闲、无故障且表有效
	output o_busy, // 包含完成拍和故障占有
	output o_done, // 末阶段可见性确认后单拍完成
	output o_fault, // 信任边界错误粘滞指示
	output [2:0]o_layer, // 当前块内阶段编号
	output [6:0]o_tile_y, // 当前四行块起点诊断
	output [7:0]o_tile_x, // 当前四列块起点诊断
	output o_parameter_valid, // 当前参数分片请求有效
	output [6:0]o_parameter_channel, // DW通道或PW输出三通道起点
	output [4:0]o_parameter_group, // 八输入归约组编号
	output [2:0]o_parameter_window, // DW窗口并集宽度，PW为零
	input i_parameter_ready, // 参数请求被服务接受
	input i_parameter_response_valid, // 参数响应保持至ready
	output o_parameter_response_ready, // 只消费当前未完成请求
	input [3:0]i_parameter_response_block_id, // 响应必须属于当前锁存块
	input [2:0]i_parameter_response_layer, // 参数响应阶段身份
	input [6:0]i_parameter_response_channel, // 参数响应输出通道身份
	input [4:0]i_parameter_response_group, // 参数响应归约组身份
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
	input [3:0]i_barrier_block_id, // 屏障必须属于当前锁存块
	input [2:0]i_barrier_layer, // 屏障确认所属阶段
	output o_core_valid, // 原算术核输入组有效
	input i_core_ready, // 原算术核输入组接受
	output o_core_first, // 当前任务首归约组
	output o_core_last, // 当前任务末归约组
	output [7:0]o_core_input_mask, // 当前八输入有效掩码
	output [63:0]o_core_activation, // 串行拼装的八个INT8输入
	output [191:0]o_core_weight, // 当前归约组驻留参数
	output [95:0]o_core_bias, // 三路首组偏置
	output [2:0]o_core_output_mask, // DW行尾任务只启用lane零
	output [47:0]o_core_tags, // 固定三路任务身份
	output [95:0]o_core_addresses, // 三路完整写地址
	output [95:0]o_core_pre_multiplier, // 三路动态前乘数
	output [17:0]o_core_pre_shift, // 三路六位前移位
	output [31:0]o_core_post_multiplier, // 当前层共享后乘数
	output [5:0]o_core_post_shift, // 当前层共享后移位
	output o_core_residual, // PW残差阶段使能
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
	localparam [4:0]ST_FINISH = 15; // 当前块末阶段完成单拍
	localparam [4:0]ST_FAULT = 16; // 故障占有直到共同复位
	localparam [4:0]ST_POOL_READ = 17; // 单byte读取当前池化样本
	localparam [4:0]ST_POOL_COMPARE = 18; // signed比较并计入当前最大值
	localparam [4:0]ST_POOL_WRITE = 19; // 保持一个池化结果至写接受

	//-----------------状态机信号-----------------//
	reg [4:0]state_current; // 当前控制状态
	reg [4:0]state_next; // 下一控制状态

	//-----------------寄存器信号-----------------//
	reg [3:0]reg_block_id; // 仅空闲start握手更新的身份
	reg [2:0]reg_layer; // 当前卷积阶段
	reg [6:0]reg_tile_y; // 当前块全图行起点
	reg [7:0]reg_tile_x; // 当前块全图列起点
	reg [6:0]reg_channel; // DW通道或PW三输出起点
	reg [4:0]reg_group; // 当前归约组
	reg [1:0]reg_spatial_row; // DW块内真实输出行
	reg flag_spatial_tail; // DW三空间点后的单点尾任务
	reg [4:0]reg_pixel; // PW块内有效像素序号
	reg [11:0]reg_prefetch_index; // 3072字节工作缓存填充索引
	reg [4:0]reg_parameter_slot; // 最多24个驻留权重分片
	reg [2:0]reg_cache_lane; // 单端口输入拼装槽
	reg [1:0]reg_bypass_lane; // 单端口旁路拼装槽
	reg [31:0]reg_read_address; // 未完成行请求地址
	reg [31:0]reg_line_address; // 当前16字节行标签
	reg [127:0]reg_line_data; // 当前16字节行数据
	reg flag_line_valid; // 行标签和数据可用
	reg [7:0]reg_tile_cache [0:3071]; // 单owner工作byte缓存，PAN最大形状仅预留
	reg [191:0]reg_weight_bank [0:23]; // 唯一24槽权重bank，使用槽均先完整覆盖
	reg [247:0]reg_parameter; // 当前输出组量化字段
	reg [63:0]reg_activation; // 当前核输入组
	reg [23:0]reg_bypass; // 当前任务三路旁路
	reg [2:0]reg_output_mask; // 当前任务有效输出路
	reg [2:0]reg_written; // 当前任务已接受写路
	reg [95:0]reg_addresses; // 当前任务三路写地址
	reg flag_task_done; // 末次真实写后一拍凭据
	reg flag_fault; // 协议错误粘滞寄存器
	reg [4:0]reg_pool_sample_index; // 五乘五窗口样本编号零至24
	reg signed [7:0]reg_pool_sample; // 共享byte口读出的有符号样本
	reg signed [7:0]reg_pool_max; // 当前池化输出的有符号最大值
	reg [31:0]reg_pool_address; // 池化写等待期间冻结的逻辑地址

	//-----------------其他信号-----------------//
	wire flag_pool; // block5的三个固定池化阶段
	wire flag_pool_write_accept; // 单池化输出实际写接受
	integer dec_pool_index; // 八乘八池化halo缓存读地址
	wire flag_dw; // 三个深度卷积阶段
	wire flag_residual; // 三个残差PW阶段
	wire [4:0]wire_last_group; // 当前任务末归约组
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
	integer dec_valid_rows; // 当前块真实有效行数
	integer dec_task_y; // 当前任务输出行
	integer dec_task_x; // 当前任务输出列
	integer dec_task_channel; // 当前任务输出通道
	integer dec_task_lane; // 当前任务输出lane
	integer dec_cache_slot; // 当前归约输入槽
	integer dec_cache_row; // DW缓存行
	integer dec_cache_column; // DW缓存列
	integer dec_cache_index; // 单端口缓存读取索引
	integer dec_bypass_index; // 单端口旁路读取索引
	reg [11:0]dec_prefetch_bytes; // 当前块需要覆盖的缓存字节
	reg [31:0]dec_prefetch_base; // 当前源张量基址
	reg [31:0]dec_prefetch_address; // 当前源逻辑字节地址
	reg flag_prefetch_padding; // 全幅图像外补零
	reg [2:0]dec_parameter_window; // 当前请求参数窗口
	reg [4:0]dec_parameter_group; // 当前请求参数组
	reg [31:0]dec_task_base; // 当前输出阶段基址
	reg [2:0]dec_task_mask; // 当前任务输出有效路
	reg [95:0]dec_task_addresses; // 当前任务三路输出地址
	reg [191:0]dec_selected_weight; // 当前归约组驻留权重

	reg [6:0]dec_height; // 锁存身份选定的真实高度
	reg [7:0]dec_width; // 固定图输出宽度
	reg [6:0]dec_half_channels; // 固定残差半支路宽度
	reg [6:0]dec_full_channels; // 固定融合通道宽度
	reg [2:0]dec_final_layer; // CSP2第五阶段、其余第七阶段
	reg [31:0]dec_source_base; // split父张量固定基址
	reg [31:0]dec_destination_zero; // 固定阶段0写张量基址
	reg [31:0]dec_destination_one; // 固定阶段1写张量基址
	reg [31:0]dec_destination_two; // 固定阶段2写张量基址
	reg [31:0]dec_destination_three; // 固定阶段3写张量基址
	reg [31:0]dec_destination_four; // 固定阶段4写张量基址
	reg [31:0]dec_destination_five; // 固定阶段5写张量基址
	reg [31:0]dec_destination_six; // 固定阶段6写张量基址
	wire flag_block_legal; // 仅start采样时检查输入块编号
	wire flag_bad_start; // 已接受非法块编号
	wire flag_bad_barrier; // 已消费屏障身份错误

	//-----------------其他信号连线-----------------//
	assign flag_block_legal = i_block_id == 2 || i_block_id == 3 || i_block_id == 4 || i_block_id == 5; // 当前只接受CSP与SPPF
	assign flag_bad_start = i_start && o_start_ready && !flag_block_legal; // 接受后直接占有故障
	assign flag_bad_barrier = o_barrier_valid && i_barrier_ready &&
		(i_barrier_block_id != reg_block_id || i_barrier_layer != reg_layer); // 层与块身份同时核验
	assign flag_pool = reg_block_id == 5 && (reg_layer == 1 || reg_layer == 2 || reg_layer == 3); // 池化不发参数或算术核组
	assign flag_pool_write_accept = state_current == ST_POOL_WRITE && o_write_valid && i_write_ready; // 池化独立写退休
	assign flag_dw = reg_block_id != 5 && reg_layer != dec_final_layer && (reg_layer == 0 || reg_layer == 2 || reg_layer == 4); // DW阶段使用空间三加尾一
	assign flag_residual = reg_block_id != 5 && (reg_layer == 1 || reg_layer == 3 || reg_layer == 5); // 三个PW阶段进行残差
	assign wire_last_group = reg_block_id == 5 ? 5'd11 : flag_dw ? 5'd1 :
		(reg_layer == dec_final_layer ? dec_full_channels / 8 - 1 : (dec_half_channels + 7) / 8 - 1); // PW覆盖全部真实输入通道
	assign wire_input_count = flag_dw ? (reg_group == 0 ? 4'd8 : (flag_spatial_tail ? 4'd1 : 4'd7)) :
		(reg_block_id == 2 && flag_residual && reg_group == 1 ? 4'd4 : 4'd8); // CSP2半支路PW仅四个尾lane
	assign wire_input_mask = wire_input_count == 8 ? 8'hff : (8'h01 << wire_input_count) - 1'b1; // 低lane连续有效
	assign flag_prefetch_hit = flag_line_valid && reg_line_address == {dec_prefetch_address[31:4],4'b0000}; // 单行全地址标签
	assign flag_prefetch_fill = flag_prefetch_padding || flag_prefetch_hit; // padding和命中均每拍写一字节
	assign flag_prefetch_last = reg_prefetch_index == dec_prefetch_bytes - 1'b1; // 整个块输入已经覆盖
	assign flag_parameter_last = reg_parameter_slot == (flag_dw ? 5'd3 : wire_last_group); // DW保留两种窗口权重
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
	assign flag_write_accept = state_current == ST_WRITE_WAIT && o_write_valid && i_write_ready; // 核和外部写同拍退休
	assign flag_last_write = flag_write_accept && (reg_written | wire_write_lane) == reg_output_mask; // 以实际接受结束任务
	assign flag_bad_parameter = flag_parameter_accept && (i_parameter_error || i_parameter_response_block_id != reg_block_id || i_parameter_response_layer != reg_layer ||
		i_parameter_response_channel != reg_channel || i_parameter_response_group != dec_parameter_group ||
		i_parameter_response_window != dec_parameter_window || (reg_parameter_slot != 0 && i_parameter_data != reg_parameter)); // 禁止错路由与组间漂移
	assign flag_bad_read = flag_read_accept && (i_read_error || i_read_response_address != reg_read_address ||
		i_read_response_address[3:0] != 0); // 对齐地址必须严格匹配
	assign flag_bad_write = i_core_output_valid && (state_current != ST_WRITE_WAIT || !flag_write_legal); // 非当前任务结果拒写
	assign flag_task_series_last = flag_dw ?
		(reg_spatial_row == dec_valid_rows - 1 && flag_spatial_tail) : reg_pixel == dec_valid_rows * 4 - 1; // 只遍历当前块真实行
	assign flag_channel_last = flag_pool ? reg_channel == 23 : reg_channel == (flag_dw ? dec_half_channels - 1 :
		(reg_layer == dec_final_layer ? dec_full_channels - 3 : dec_half_channels - 3)); // 输出通道均整除三路
	assign flag_tile_last = reg_tile_y == ((dec_height - 1) / 4) * 4 && reg_tile_x == dec_width - 4; // 最后物理块坐标

	//-----------------输出信号连线-----------------//
	assign o_start_ready = state_current == ST_IDLE && i_rstn && i_table_loaded && !o_fault; // 不在表未装或故障时启动
	assign o_busy = state_current != ST_IDLE; // 故障状态不冒充排空
	assign o_done = state_current == ST_FINISH && !o_fault; // 最终整层屏障之后完成
	assign o_fault = flag_fault || i_core_fault || i_cancel; // 外部取消和核错误立即阻止传输
	assign o_block_id = reg_block_id; // 应用参数及屏障共有归属
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
	assign o_write_valid = !o_fault && (state_current == ST_POOL_WRITE ? !i_core_output_valid :
		(state_current == ST_WRITE_WAIT && i_core_output_valid && flag_write_legal)); // 池化与核写回互斥，旧核结果拒写
	assign o_write_address = state_current == ST_POOL_WRITE ? reg_pool_address : i_core_output_address; // 池化地址独立冻结
	assign o_write_data = state_current == ST_POOL_WRITE ? reg_pool_max : i_core_output_data; // 池化无需量化或SiLU
	assign o_write_sum = state_current == ST_POOL_WRITE ? {reg_pool_max[7],reg_pool_max} : i_core_output_sum; // 池化最大值符号扩展至signed9
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
	assign o_core_residual = flag_residual; // 最终融合不做残差
	assign o_core_bypass = reg_bypass; // 仅残差PW首组使用的旁路数据
	assign o_core_output_ready = state_current == ST_WRITE_WAIT && i_write_ready && flag_write_legal && !o_fault; // 双端共同接受

	// 固定case只看锁存身份；没有任意形状或外部层列表。
	always @(*)begin
		dec_height = 0;
		dec_width = 0;
		dec_half_channels = 0;
		dec_full_channels = 0;
		dec_final_layer = 0;
		dec_source_base = 0;
		dec_destination_zero = 0;
		dec_destination_one = 0;
		dec_destination_two = 0;
		dec_destination_three = 0;
		dec_destination_four = 0;
		dec_destination_five = 0;
		dec_destination_six = 0;
		case(reg_block_id)
			4'd2:begin
				dec_height = 72;
				dec_width = 128;
				dec_half_channels = 12;
				dec_full_channels = 24;
				dec_final_layer = 4;
				dec_source_base = 32'h035b4000;
				dec_destination_zero = 32'h035ea000;
				dec_destination_one = 32'h03605000;
				dec_destination_two = 32'h03620000;
				dec_destination_three = 32'h0363b000;
				dec_destination_four = 32'h03656000;
				dec_destination_five = 32'h0363b000;
				dec_destination_six = 32'h03656000;
			end
			4'd3:begin
				dec_height = 36;
				dec_width = 64;
				dec_half_channels = 24;
				dec_full_channels = 48;
				dec_final_layer = 6;
				dec_source_base = 32'h0369a000;
				dec_destination_zero = 32'h036b5000;
				dec_destination_one = 32'h036c3000;
				dec_destination_two = 32'h036d1000;
				dec_destination_three = 32'h036df000;
				dec_destination_four = 32'h036ed000;
				dec_destination_five = 32'h036fb000;
				dec_destination_six = 32'h03709000;
			end
			4'd4:begin
				dec_height = 18;
				dec_width = 32;
				dec_half_channels = 48;
				dec_full_channels = 96;
				dec_final_layer = 6;
				dec_source_base = 32'h0372c000;
				dec_destination_zero = 32'h0373b000;
				dec_destination_one = 32'h03743000;
				dec_destination_two = 32'h0374b000;
				dec_destination_three = 32'h03753000;
				dec_destination_four = 32'h0375b000;
				dec_destination_five = 32'h03763000;
				dec_destination_six = 32'h0376b000;
			end
			4'd5:begin
				dec_height = 18;
				dec_width = 32;
				dec_half_channels = 24;
				dec_full_channels = 96;
				dec_final_layer = 4;
				dec_source_base = 32'h0376b000;
				dec_destination_zero = 32'h0377a000;
				dec_destination_one = 32'h0377e000;
				dec_destination_two = 32'h03782000;
				dec_destination_three = 32'h03786000;
				dec_destination_four = 32'h0378a000;
			end
			default:begin
			end
		endcase
	end

	// 当前CSP4尾块仅有两行，CSP3所有块均有四行。
	always @(*)begin
		dec_valid_rows = dec_height - reg_tile_y;
		if(dec_valid_rows > 4)dec_valid_rows = 4;
	end

	// 参数槽零一是DW五列窗口，槽二三是DW三列尾窗口；PW按归约组编号。
	always @(*)begin
		dec_parameter_group = reg_parameter_slot;
		dec_parameter_window = 0;
		if(flag_dw)begin
			dec_parameter_group = {4'b0000,reg_parameter_slot[0]};
			dec_parameter_window = reg_parameter_slot[1] ? 3'd3 : 3'd5;
		end
	end

	// 固定图源地址只在块预取期间使用，每个使用字节都在任务开始前覆盖。
	always @(*)begin
		case(reg_block_id)
			4'd2:begin
				dec_prefetch_bytes = flag_dw ? 36 * 12 :
					(flag_residual ? 32 * 12 : 16 * 24);
				dec_prefetch_y = reg_tile_y;
				dec_prefetch_x = reg_tile_x;
				dec_prefetch_channel = 0;
				dec_prefetch_channels = 12;
				dec_prefetch_local = reg_prefetch_index;
				dec_prefetch_pixel = 0;
				dec_prefetch_base = dec_source_base;
				flag_prefetch_padding = 0;
				if(flag_dw)begin
					dec_prefetch_y = reg_tile_y + reg_prefetch_index / (6 * 12) - 1;
					dec_prefetch_x = reg_tile_x + (reg_prefetch_index % (6 * 12)) / 12 - 1;
					dec_prefetch_channel = reg_prefetch_index % 12;
					case(reg_layer)
						0:begin
							dec_prefetch_base = dec_source_base;
							dec_prefetch_channels = 24;
							dec_prefetch_channel = dec_prefetch_channel + 12;
						end
						2:dec_prefetch_base = dec_destination_one;
						default:dec_prefetch_base = dec_destination_three;
					endcase
					flag_prefetch_padding = dec_prefetch_y < 0 || dec_prefetch_y >= 72 ||
						dec_prefetch_x < 0 || dec_prefetch_x >= 128;
				end else if(flag_residual)begin
					if(reg_prefetch_index >= 16 * 12)dec_prefetch_local = reg_prefetch_index - 16 * 12;
					dec_prefetch_pixel = dec_prefetch_local / 12;
					dec_prefetch_y = reg_tile_y + dec_prefetch_pixel / 4;
					dec_prefetch_x = reg_tile_x + dec_prefetch_pixel % 4;
					dec_prefetch_channel = dec_prefetch_local % 12;
					case(reg_layer)
						1:begin
							if(reg_prefetch_index < 16 * 12)dec_prefetch_base = dec_destination_zero;
							else begin
								dec_prefetch_base = dec_source_base;
								dec_prefetch_channels = 24;
								dec_prefetch_channel = dec_prefetch_channel + 12;
							end
						end
						3:dec_prefetch_base = reg_prefetch_index < 16 * 12 ? dec_destination_two : dec_destination_one;
						default:dec_prefetch_base = reg_prefetch_index < 16 * 12 ? dec_destination_four : dec_destination_three;
					endcase
					flag_prefetch_padding = dec_prefetch_y >= 72;
				end else begin
					dec_prefetch_pixel = reg_prefetch_index / 24;
					dec_prefetch_y = reg_tile_y + dec_prefetch_pixel / 4;
					dec_prefetch_x = reg_tile_x + dec_prefetch_pixel % 4;
					dec_prefetch_channel = reg_prefetch_index % 24;
					dec_prefetch_channels = dec_prefetch_channel < 12 ? 24 : 12;
					if(dec_prefetch_channel < 12)dec_prefetch_base = dec_source_base;
					else begin
						dec_prefetch_base = dec_destination_five;
						dec_prefetch_channel = dec_prefetch_channel - 12;
					end
					flag_prefetch_padding = dec_prefetch_y >= 72;
				end
				dec_prefetch_address = 0;
				if(!flag_prefetch_padding)begin
					if(dec_prefetch_channels == 24)begin
						dec_prefetch_address = dec_prefetch_base + (((dec_prefetch_y / 4) * 32 + dec_prefetch_x / 4) * 16 +
							(dec_prefetch_y % 4) * 4 + dec_prefetch_x % 4) * 24 + dec_prefetch_channel;
					end else begin
						dec_prefetch_address = dec_prefetch_base + (((dec_prefetch_y / 4) * 32 + dec_prefetch_x / 4) * 16 +
							(dec_prefetch_y % 4) * 4 + dec_prefetch_x % 4) * 12 + dec_prefetch_channel;
					end
				end
		
			end
			4'd3:begin
				dec_prefetch_bytes = flag_dw ? 36 * 24 :
					(flag_residual ? 32 * 24 : 16 * 48);
				dec_prefetch_y = reg_tile_y;
				dec_prefetch_x = reg_tile_x;
				dec_prefetch_channel = 0;
				dec_prefetch_channels = 24;
				dec_prefetch_local = reg_prefetch_index;
				dec_prefetch_pixel = 0;
				dec_prefetch_base = dec_source_base;
				flag_prefetch_padding = 0;
				if(flag_dw)begin
					dec_prefetch_y = reg_tile_y + reg_prefetch_index / (6 * 24) - 1;
					dec_prefetch_x = reg_tile_x + (reg_prefetch_index % (6 * 24)) / 24 - 1;
					dec_prefetch_channel = reg_prefetch_index % 24;
					case(reg_layer)
						0:begin
							dec_prefetch_base = dec_source_base;
							dec_prefetch_channels = 48;
							dec_prefetch_channel = dec_prefetch_channel + 24;
						end
						2:dec_prefetch_base = dec_destination_one;
						default:dec_prefetch_base = dec_destination_three;
					endcase
					flag_prefetch_padding = dec_prefetch_y < 0 || dec_prefetch_y >= 36 ||
						dec_prefetch_x < 0 || dec_prefetch_x >= 64;
				end else if(flag_residual)begin
					if(reg_prefetch_index >= 16 * 24)dec_prefetch_local = reg_prefetch_index - 16 * 24;
					dec_prefetch_pixel = dec_prefetch_local / 24;
					dec_prefetch_y = reg_tile_y + dec_prefetch_pixel / 4;
					dec_prefetch_x = reg_tile_x + dec_prefetch_pixel % 4;
					dec_prefetch_channel = dec_prefetch_local % 24;
					case(reg_layer)
						1:begin
							if(reg_prefetch_index < 16 * 24)dec_prefetch_base = dec_destination_zero;
							else begin
								dec_prefetch_base = dec_source_base;
								dec_prefetch_channels = 48;
								dec_prefetch_channel = dec_prefetch_channel + 24;
							end
						end
						3:dec_prefetch_base = reg_prefetch_index < 16 * 24 ? dec_destination_two : dec_destination_one;
						default:dec_prefetch_base = reg_prefetch_index < 16 * 24 ? dec_destination_four : dec_destination_three;
					endcase
					flag_prefetch_padding = dec_prefetch_y >= 36;
				end else begin
					dec_prefetch_pixel = reg_prefetch_index / 48;
					dec_prefetch_y = reg_tile_y + dec_prefetch_pixel / 4;
					dec_prefetch_x = reg_tile_x + dec_prefetch_pixel % 4;
					dec_prefetch_channel = reg_prefetch_index % 48;
					dec_prefetch_channels = dec_prefetch_channel < 24 ? 48 : 24;
					if(dec_prefetch_channel < 24)dec_prefetch_base = dec_source_base;
					else begin
						dec_prefetch_base = dec_destination_five;
						dec_prefetch_channel = dec_prefetch_channel - 24;
					end
					flag_prefetch_padding = dec_prefetch_y >= 36;
				end
				dec_prefetch_address = 0;
				if(!flag_prefetch_padding)begin
					if(dec_prefetch_channels == 48)begin
						dec_prefetch_address = dec_prefetch_base + (((dec_prefetch_y / 4) * 16 + dec_prefetch_x / 4) * 16 +
							(dec_prefetch_y % 4) * 4 + dec_prefetch_x % 4) * 48 + dec_prefetch_channel;
					end else begin
						dec_prefetch_address = dec_prefetch_base + (((dec_prefetch_y / 4) * 16 + dec_prefetch_x / 4) * 16 +
							(dec_prefetch_y % 4) * 4 + dec_prefetch_x % 4) * 24 + dec_prefetch_channel;
					end
				end
		
			end
			4'd4:begin
				dec_prefetch_bytes = flag_dw ? 36 * 48 :
					(flag_residual ? 32 * 48 : 16 * 96);
				dec_prefetch_y = reg_tile_y;
				dec_prefetch_x = reg_tile_x;
				dec_prefetch_channel = 0;
				dec_prefetch_channels = 48;
				dec_prefetch_local = reg_prefetch_index;
				dec_prefetch_pixel = 0;
				dec_prefetch_base = dec_source_base;
				flag_prefetch_padding = 0;
				if(flag_dw)begin
					dec_prefetch_y = reg_tile_y + reg_prefetch_index / (6 * 48) - 1;
					dec_prefetch_x = reg_tile_x + (reg_prefetch_index % (6 * 48)) / 48 - 1;
					dec_prefetch_channel = reg_prefetch_index % 48;
					case(reg_layer)
						0:begin
							dec_prefetch_base = dec_source_base;
							dec_prefetch_channels = 96;
							dec_prefetch_channel = dec_prefetch_channel + 48;
						end
						2:dec_prefetch_base = dec_destination_one;
						default:dec_prefetch_base = dec_destination_three;
					endcase
					flag_prefetch_padding = dec_prefetch_y < 0 || dec_prefetch_y >= 18 ||
						dec_prefetch_x < 0 || dec_prefetch_x >= 32;
				end else if(flag_residual)begin
					if(reg_prefetch_index >= 16 * 48)dec_prefetch_local = reg_prefetch_index - 16 * 48;
					dec_prefetch_pixel = dec_prefetch_local / 48;
					dec_prefetch_y = reg_tile_y + dec_prefetch_pixel / 4;
					dec_prefetch_x = reg_tile_x + dec_prefetch_pixel % 4;
					dec_prefetch_channel = dec_prefetch_local % 48;
					case(reg_layer)
						1:begin
							if(reg_prefetch_index < 16 * 48)dec_prefetch_base = dec_destination_zero;
							else begin
								dec_prefetch_base = dec_source_base;
								dec_prefetch_channels = 96;
								dec_prefetch_channel = dec_prefetch_channel + 48;
							end
						end
						3:dec_prefetch_base = reg_prefetch_index < 16 * 48 ? dec_destination_two : dec_destination_one;
						default:dec_prefetch_base = reg_prefetch_index < 16 * 48 ? dec_destination_four : dec_destination_three;
					endcase
					flag_prefetch_padding = dec_prefetch_y >= 18;
				end else begin
					dec_prefetch_pixel = reg_prefetch_index / 96;
					dec_prefetch_y = reg_tile_y + dec_prefetch_pixel / 4;
					dec_prefetch_x = reg_tile_x + dec_prefetch_pixel % 4;
					dec_prefetch_channel = reg_prefetch_index % 96;
					dec_prefetch_channels = dec_prefetch_channel < 48 ? 96 : 48;
					if(dec_prefetch_channel < 48)dec_prefetch_base = dec_source_base;
					else begin
						dec_prefetch_base = dec_destination_five;
						dec_prefetch_channel = dec_prefetch_channel - 48;
					end
					flag_prefetch_padding = dec_prefetch_y >= 18;
				end
				dec_prefetch_address = 0;
				if(!flag_prefetch_padding)begin
					if(dec_prefetch_channels == 96)begin
						dec_prefetch_address = dec_prefetch_base + (((dec_prefetch_y / 4) * 8 + dec_prefetch_x / 4) * 16 +
							(dec_prefetch_y % 4) * 4 + dec_prefetch_x % 4) * 96 + dec_prefetch_channel;
					end else begin
						dec_prefetch_address = dec_prefetch_base + (((dec_prefetch_y / 4) * 8 + dec_prefetch_x / 4) * 16 +
							(dec_prefetch_y % 4) * 4 + dec_prefetch_x % 4) * 48 + dec_prefetch_channel;
					end
				end
		
			end
			4'd5:begin
				dec_prefetch_bytes = 12'd1536;
				dec_prefetch_local = reg_prefetch_index;
				dec_prefetch_pixel = reg_prefetch_index / 96;
				dec_prefetch_y = reg_tile_y + dec_prefetch_pixel / 4;
				dec_prefetch_x = reg_tile_x + dec_prefetch_pixel % 4;
				dec_prefetch_channel = reg_prefetch_index % 96;
				dec_prefetch_channels = 96;
				dec_prefetch_base = 32'h0376b000;
				flag_prefetch_padding = dec_prefetch_y >= 18;
				if(flag_pool)begin
					dec_prefetch_y = reg_tile_y + reg_prefetch_index / 192 - 2;
					dec_prefetch_x = reg_tile_x + (reg_prefetch_index % 192) / 24 - 2;
					dec_prefetch_channel = reg_prefetch_index % 24;
					dec_prefetch_channels = 24;
					case(reg_layer)
						1:dec_prefetch_base = 32'h0377a000;
						2:dec_prefetch_base = 32'h0377e000;
						default:dec_prefetch_base = 32'h03782000;
					endcase
					flag_prefetch_padding = dec_prefetch_y < 0 || dec_prefetch_y >= 18 ||
						dec_prefetch_x < 0 || dec_prefetch_x >= 32;
				end else if(reg_layer == 4)begin
					case(dec_prefetch_channel / 24)
						0:dec_prefetch_base = 32'h0377a000;
						1:dec_prefetch_base = 32'h0377e000;
						2:dec_prefetch_base = 32'h03782000;
						default:dec_prefetch_base = 32'h03786000;
					endcase
					dec_prefetch_channel = dec_prefetch_channel % 24;
					dec_prefetch_channels = 24;
				end
				dec_prefetch_address = 0;
				if(!flag_prefetch_padding)begin
					if(reg_layer == 0)begin
						dec_prefetch_address = dec_prefetch_base +
							(((dec_prefetch_y / 4) * 8 + dec_prefetch_x / 4) * 16 +
							(dec_prefetch_y % 4) * 4 + dec_prefetch_x % 4) * 96 + dec_prefetch_channel;
					end else begin
						dec_prefetch_address = dec_prefetch_base +
							(((dec_prefetch_y / 4) * 8 + dec_prefetch_x / 4) * 16 +
							(dec_prefetch_y % 4) * 4 + dec_prefetch_x % 4) * 24 + dec_prefetch_channel;
					end
				end
			end
			default:begin
				dec_prefetch_bytes = 0;
				dec_prefetch_y = 0;
				dec_prefetch_x = 0;
				dec_prefetch_channel = 0;
				dec_prefetch_channels = 0;
				dec_prefetch_local = 0;
				dec_prefetch_pixel = 0;
				dec_prefetch_base = 0;
				dec_prefetch_address = 0;
				flag_prefetch_padding = 1'b1;
			end
		endcase
	end

	// 任务地址沿tile4x4_hwc布局生成；CSP4尾块不产生第十八行以后的写请求。
	always @(*)begin
		case(reg_block_id)
			4'd2:begin
				case(reg_layer)
					0:dec_task_base = dec_destination_zero;
					1:dec_task_base = dec_destination_one;
					2:dec_task_base = dec_destination_two;
					3:dec_task_base = dec_destination_three;
					4:dec_task_base = dec_destination_four;
					5:dec_task_base = dec_destination_five;
					default:dec_task_base = dec_destination_six;
				endcase
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
						if(reg_layer == 4)begin
							dec_task_addresses[dec_task_lane * 32 +: 32] = dec_task_base + (((dec_task_y / 4) * 32 + (dec_task_x + (flag_dw ? dec_task_lane : 0)) / 4) * 16 +
								(dec_task_y % 4) * 4 + (dec_task_x + (flag_dw ? dec_task_lane : 0)) % 4) * 24 + dec_task_channel;
						end else begin
							dec_task_addresses[dec_task_lane * 32 +: 32] = dec_task_base + (((dec_task_y / 4) * 32 + (dec_task_x + (flag_dw ? dec_task_lane : 0)) / 4) * 16 +
								(dec_task_y % 4) * 4 + (dec_task_x + (flag_dw ? dec_task_lane : 0)) % 4) * 12 + dec_task_channel;
						end
					end
				end
		
			end
			4'd3:begin
				case(reg_layer)
					0:dec_task_base = dec_destination_zero;
					1:dec_task_base = dec_destination_one;
					2:dec_task_base = dec_destination_two;
					3:dec_task_base = dec_destination_three;
					4:dec_task_base = dec_destination_four;
					5:dec_task_base = dec_destination_five;
					default:dec_task_base = dec_destination_six;
				endcase
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
						if(reg_layer == 6)begin
							dec_task_addresses[dec_task_lane * 32 +: 32] = dec_task_base + (((dec_task_y / 4) * 16 + (dec_task_x + (flag_dw ? dec_task_lane : 0)) / 4) * 16 +
								(dec_task_y % 4) * 4 + (dec_task_x + (flag_dw ? dec_task_lane : 0)) % 4) * 48 + dec_task_channel;
						end else begin
							dec_task_addresses[dec_task_lane * 32 +: 32] = dec_task_base + (((dec_task_y / 4) * 16 + (dec_task_x + (flag_dw ? dec_task_lane : 0)) / 4) * 16 +
								(dec_task_y % 4) * 4 + (dec_task_x + (flag_dw ? dec_task_lane : 0)) % 4) * 24 + dec_task_channel;
						end
					end
				end
		
			end
			4'd4:begin
				case(reg_layer)
					0:dec_task_base = dec_destination_zero;
					1:dec_task_base = dec_destination_one;
					2:dec_task_base = dec_destination_two;
					3:dec_task_base = dec_destination_three;
					4:dec_task_base = dec_destination_four;
					5:dec_task_base = dec_destination_five;
					default:dec_task_base = dec_destination_six;
				endcase
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
						if(reg_layer == 6)begin
							dec_task_addresses[dec_task_lane * 32 +: 32] = dec_task_base + (((dec_task_y / 4) * 8 + (dec_task_x + (flag_dw ? dec_task_lane : 0)) / 4) * 16 +
								(dec_task_y % 4) * 4 + (dec_task_x + (flag_dw ? dec_task_lane : 0)) % 4) * 96 + dec_task_channel;
						end else begin
							dec_task_addresses[dec_task_lane * 32 +: 32] = dec_task_base + (((dec_task_y / 4) * 8 + (dec_task_x + (flag_dw ? dec_task_lane : 0)) / 4) * 16 +
								(dec_task_y % 4) * 4 + (dec_task_x + (flag_dw ? dec_task_lane : 0)) % 4) * 48 + dec_task_channel;
						end
					end
				end
		
			end
			4'd5:begin
				case(reg_layer)
					0:dec_task_base = 32'h0377a000;
					1:dec_task_base = 32'h0377e000;
					2:dec_task_base = 32'h03782000;
					3:dec_task_base = 32'h03786000;
					default:dec_task_base = 32'h0378a000;
				endcase
				dec_task_mask = flag_pool ? 3'b001 : 3'b111;
				dec_task_addresses = 0;
				dec_task_y = reg_tile_y + reg_pixel / 4;
				dec_task_x = reg_tile_x + reg_pixel % 4;
				dec_task_channel = reg_channel;
				for(dec_task_lane = 0; dec_task_lane < 3; dec_task_lane = dec_task_lane + 1)begin
					if(dec_task_mask[dec_task_lane])begin
						dec_task_channel = reg_channel + (flag_pool ? 0 : dec_task_lane);
						if(reg_layer == 4)begin
							dec_task_addresses[dec_task_lane * 32 +: 32] = dec_task_base +
								(((dec_task_y / 4) * 8 + dec_task_x / 4) * 16 +
								(dec_task_y % 4) * 4 + dec_task_x % 4) * 96 + dec_task_channel;
						end else begin
							dec_task_addresses[dec_task_lane * 32 +: 32] = dec_task_base +
								(((dec_task_y / 4) * 8 + dec_task_x / 4) * 16 +
								(dec_task_y % 4) * 4 + dec_task_x % 4) * 24 + dec_task_channel;
						end
					end
				end
			end
			default:begin
				dec_task_base = 0;
				dec_task_mask = 0;
				dec_task_addresses = 0;
				dec_task_y = 0;
				dec_task_x = 0;
				dec_task_lane = 0;
				dec_task_channel = 0;
			end
		endcase
	end

	// 单端口缓存读地址按当前归约槽逐拍变化，尾组只读取真实输入字节。
	always @(*)begin
		case(reg_block_id)
			4'd2:begin
				dec_cache_slot = reg_group * 8 + reg_cache_lane;
				dec_cache_row = 0;
				dec_cache_column = 0;
				dec_cache_index = 0;
				dec_bypass_index = 16 * 12 + reg_pixel * 12 + reg_channel + reg_bypass_lane;
				if(flag_dw)begin
					if(flag_spatial_tail)begin
						dec_cache_row = dec_cache_slot / 3;
						dec_cache_column = dec_cache_slot % 3;
					end else begin
						dec_cache_row = dec_cache_slot / 5;
						dec_cache_column = dec_cache_slot % 5;
					end
					dec_cache_index = ((reg_spatial_row + dec_cache_row) * 6 +
						(flag_spatial_tail ? 3 : 0) + dec_cache_column) * 12 + reg_channel;
				end else if(reg_layer == 4)begin
					dec_cache_index = reg_pixel * 24 + dec_cache_slot;
				end else begin
					dec_cache_index = reg_pixel * 12 + dec_cache_slot;
				end
		
			end
			4'd3:begin
				dec_cache_slot = reg_group * 8 + reg_cache_lane;
				dec_cache_row = 0;
				dec_cache_column = 0;
				dec_cache_index = 0;
				dec_bypass_index = 16 * 24 + reg_pixel * 24 + reg_channel + reg_bypass_lane;
				if(flag_dw)begin
					if(flag_spatial_tail)begin
						dec_cache_row = dec_cache_slot / 3;
						dec_cache_column = dec_cache_slot % 3;
					end else begin
						dec_cache_row = dec_cache_slot / 5;
						dec_cache_column = dec_cache_slot % 5;
					end
					dec_cache_index = ((reg_spatial_row + dec_cache_row) * 6 +
						(flag_spatial_tail ? 3 : 0) + dec_cache_column) * 24 + reg_channel;
				end else if(reg_layer == 6)begin
					dec_cache_index = reg_pixel * 48 + dec_cache_slot;
				end else begin
					dec_cache_index = reg_pixel * 24 + dec_cache_slot;
				end
		
			end
			4'd4:begin
				dec_cache_slot = reg_group * 8 + reg_cache_lane;
				dec_cache_row = 0;
				dec_cache_column = 0;
				dec_cache_index = 0;
				dec_bypass_index = 16 * 48 + reg_pixel * 48 + reg_channel + reg_bypass_lane;
				if(flag_dw)begin
					if(flag_spatial_tail)begin
						dec_cache_row = dec_cache_slot / 3;
						dec_cache_column = dec_cache_slot % 3;
					end else begin
						dec_cache_row = dec_cache_slot / 5;
						dec_cache_column = dec_cache_slot % 5;
					end
					dec_cache_index = ((reg_spatial_row + dec_cache_row) * 6 +
						(flag_spatial_tail ? 3 : 0) + dec_cache_column) * 48 + reg_channel;
				end else if(reg_layer == 6)begin
					dec_cache_index = reg_pixel * 96 + dec_cache_slot;
				end else begin
					dec_cache_index = reg_pixel * 48 + dec_cache_slot;
				end
		
			end
			4'd5:begin
				dec_cache_slot = reg_group * 8 + reg_cache_lane;
				dec_cache_row = 0;
				dec_cache_column = 0;
				dec_cache_index = reg_pixel * 96 + dec_cache_slot;
				dec_bypass_index = 0;
			end
			default:begin
				dec_cache_slot = 0;
				dec_cache_row = 0;
				dec_cache_column = 0;
				dec_cache_index = 0;
				dec_bypass_index = 0;
			end
		endcase
	end

	// 池化样本在八乘八halo中的位置，窗口与通道均为固定规模。
	always @(*)begin
		dec_pool_index = ((reg_pixel / 4 + reg_pool_sample_index / 5) * 8 +
			reg_pixel % 4 + reg_pool_sample_index % 5) * 24 + reg_channel;
	end

	// 24槽只保存当前输出组三路权重，首批最多使用12槽，切换输出组即完整覆盖需要的槽。
	always @(*)begin
		dec_selected_weight = reg_weight_bank[reg_group];
		if(flag_dw)begin
			if(flag_spatial_tail)dec_selected_weight = reg_weight_bank[reg_group + 2];
			else dec_selected_weight = reg_weight_bank[reg_group];
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
			ST_TILE_SETUP:state_next = ST_PREFETCH;
			ST_PREFETCH:begin
				if(flag_prefetch_fill)begin
					if(flag_prefetch_last)begin
						if(flag_pool)state_next = ST_TASK_SETUP;
						else state_next = ST_PARAMETER;
					end
				end else state_next = ST_READ;
			end
			ST_READ:begin
				if(o_read_valid && i_read_ready)state_next = ST_READ_WAIT;
			end
			ST_READ_WAIT:begin
				if(flag_read_accept)state_next = ST_PREFETCH;
			end
			ST_PARAMETER:begin
				if(o_parameter_valid && i_parameter_ready)state_next = ST_PARAMETER_WAIT;
			end
			ST_PARAMETER_WAIT:begin
				if(flag_parameter_accept)begin
					if(flag_parameter_last)state_next = ST_TASK_SETUP;
					else state_next = ST_PARAMETER;
				end
			end
			ST_TASK_SETUP:begin
				if(flag_pool)state_next = ST_POOL_READ;
				else state_next = ST_CACHE_ACTIVATION;
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
				else if(!flag_channel_last)begin
					if(flag_pool)state_next = ST_TASK_SETUP;
					else state_next = ST_PARAMETER;
				end
				else if(flag_tile_last)state_next = ST_BARRIER;
				else state_next = ST_TILE_SETUP;
			end
			ST_BARRIER:begin
				if(o_barrier_valid && i_barrier_ready && i_barrier_block_id == reg_block_id && i_barrier_layer == reg_layer)begin
					if(reg_layer == dec_final_layer)state_next = ST_FINISH;
					else state_next = ST_TILE_SETUP;
				end
			end
			ST_POOL_READ:state_next = ST_POOL_COMPARE;
			ST_POOL_COMPARE:begin
				if(reg_pool_sample_index == 24)state_next = ST_POOL_WRITE;
				else state_next = ST_POOL_READ;
			end
			ST_POOL_WRITE:begin
				if(flag_pool_write_accept)state_next = ST_ADVANCE;
			end
			ST_FINISH:state_next = ST_IDLE;
			ST_FAULT:state_next = ST_FAULT;
			default:state_next = ST_FAULT;
		endcase
		if(i_cancel || i_core_fault || flag_bad_parameter || flag_bad_read || flag_bad_write ||
			flag_bad_barrier || flag_bad_start)state_next = ST_FAULT;
	end

	// 状态任务过程维护缓存、参数、任务遍历和粘滞故障，不复位两个大数组。
	always @(posedge i_clk or negedge i_rstn)begin
		if(!i_rstn)begin
			reg_block_id <= 0;
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
			reg_parameter <= 0;
			reg_activation <= 0;
			reg_bypass <= 0;
			reg_output_mask <= 0;
			reg_written <= 0;
			reg_addresses <= 0;
			flag_task_done <= 0;
			flag_fault <= 0;
			reg_pool_sample_index <= 0;
			reg_pool_sample <= 8'h80;
			reg_pool_max <= 8'h80;
			reg_pool_address <= 0;
		end else begin
			flag_task_done <= flag_last_write;
			if(i_cancel || i_core_fault || flag_bad_parameter || flag_bad_read || flag_bad_write ||
				flag_bad_barrier || flag_bad_start)flag_fault <= 1'b1;
			if(i_start && o_start_ready)begin
				reg_block_id <= i_block_id;
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
					if(flag_prefetch_padding)reg_tile_cache[reg_prefetch_index] <= flag_pool ? 8'h80 : 8'h00;
					else reg_tile_cache[reg_prefetch_index] <= reg_line_data[dec_prefetch_address[3:0] * 8 +: 8];
					if(!flag_prefetch_last)reg_prefetch_index <= reg_prefetch_index + 1'b1;
				end else reg_read_address <= {dec_prefetch_address[31:4],4'b0000};
			end
			if(flag_read_accept && !flag_bad_read)begin
				reg_line_address <= i_read_response_address;
				reg_line_data <= i_read_response_data;
				flag_line_valid <= 1'b1;
			end
			if(flag_parameter_accept && !flag_bad_parameter)begin
				reg_weight_bank[reg_parameter_slot] <= i_parameter_weight;
				if(reg_parameter_slot == 0)reg_parameter <= i_parameter_data;
				if(!flag_parameter_last)reg_parameter_slot <= reg_parameter_slot + 1'b1;
			end
			if(state_current == ST_TASK_SETUP && !flag_pool)begin
				reg_group <= 0;
				reg_cache_lane <= 0;
				reg_bypass_lane <= 0;
				reg_activation <= 0;
				reg_bypass <= 0;
				reg_output_mask <= dec_task_mask;
				reg_addresses <= dec_task_addresses;
				reg_written <= 0;
			end
			if(state_current == ST_TASK_SETUP && flag_pool)begin
				reg_pool_sample_index <= 0;
				reg_pool_max <= 8'h80;
				reg_pool_address <= dec_task_addresses[31:0];
			end
			if(state_current == ST_POOL_READ)begin
				reg_pool_sample <= reg_tile_cache[dec_pool_index];
			end
			if(state_current == ST_POOL_COMPARE)begin
				if($signed(reg_pool_sample) > $signed(reg_pool_max))reg_pool_max <= reg_pool_sample;
				if(reg_pool_sample_index != 24)reg_pool_sample_index <= reg_pool_sample_index + 1'b1;
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
						end else flag_spatial_tail <= 1'b1;
					end else reg_pixel <= reg_pixel + 1'b1;
				end else if(!flag_channel_last)begin
					reg_channel <= reg_channel + (flag_pool ? 1 : (flag_dw ? 1 : 3));
					reg_parameter_slot <= 0;
					reg_group <= 0;
					reg_spatial_row <= 0;
					flag_spatial_tail <= 0;
					reg_pixel <= 0;
				end else if(!flag_tile_last)begin
					if(reg_tile_x == dec_width - 4)begin
						reg_tile_x <= 0;
						reg_tile_y <= reg_tile_y + 4;
					end else reg_tile_x <= reg_tile_x + 4;
				end
			end
			if(o_barrier_valid && i_barrier_ready && i_barrier_block_id == reg_block_id && i_barrier_layer == reg_layer && reg_layer != dec_final_layer)begin
				reg_layer <= reg_layer + 1'b1;
				reg_tile_y <= 0;
				reg_tile_x <= 0;
				flag_line_valid <= 0;
			end
		end
	end
endmodule
