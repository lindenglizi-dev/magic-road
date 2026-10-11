`timescale 1ns / 1ps

////////////////////////////////////English///////////////////////////////////////
// Company:         Erie
// Engineer:        Erie
//
// Create Date:     2026/10/06 00:00:00
// Design Name:     road_low_io_physical_shell
// Module Name:     road_low_io_physical_shell
// Description:     description/road_low_io_physical_shell_Design.pdf
// Simulations:     testbench/vivado/2021.1/road_low_io_physical_shell
//
// Referrences:
// File Format      File Name
// 1.Book           road_low_io_physical_shell.contract.json
//
// Dependencies:
// Module Name      Version
// road_onchip_chain V1.0
//
// Version:         V1.0
// Revision Date:   2026/10/06 00:00:00
// History:
// Time             Version     Revised by        Contents
// 2026/10/06       V1.0        Erie              Create file.
///////////////////////////////////Chinese////////////////////////////////////////
// 版权归属:        Erie
// 开发人员:        Erie
//
// 创建日期:        2026年10月06日
// 设计名称:        road_low_io_physical_shell
// 模块名称:        road_low_io_physical_shell
// 模块说明:        Description/road_low_io_physical_shell_Design.pdf
// 仿真工程:        TestBench/Vivado/2021.1/road_low_io_physical_shell
//
// 参考资料:
// 文件格式         文件名称
// 1.Book           road_low_io_physical_shell.contract.json
//
// 依赖文件:
// 模块名称         版本
// road_onchip_chain V1.0
//
// 当前版本:        V1.0
// 修订日期:        2026年10月06日
// 修订历史:
// 时间             版本        修订人            修订内容
// 2026年10月06日   V1.0        Erie              创建文件

module road_low_io_physical_shell
(
	//-----------------全局信号-----------------//
	input i_clk,                                // 一百兆隔离物理验证时钟
	input i_rstn,                               // 异步低有效事务取消复位

	//------------------RX接口------------------//
	input i_rx_valid,                           // 十六位命令或负载保持有效标志
	input [15:0]i_rx_data,                      // 十六位低字优先接收数据
	output o_rx_ready,                          // 当前接收状态允许一次传输

	//------------------TX接口------------------//
	output o_tx_valid,                          // 十六位响应保持有效标志
	output [15:0]o_tx_data,                     // 结果完成或状态响应数据
	input i_tx_ready                            // 外部接收响应许可
);

	//---------------配置参数区域---------------//
	//有限缓存与状态响应长度
	localparam [6:0]MAX_PACKET_COUNT = 7'd96;   // 四位置各二十四组的总包上限
	localparam [4:0]STATUS_LAST_INDEX = 5'd17;  // 状态快照最后一个十六位字索引

	//---------------状态参数区域---------------//
	//命令与计算调度状态
	localparam [3:0]ST_IDLE = 4'd0;             // 等待一个完整命令头
	localparam [3:0]ST_TABLE_DATA = 4'd1;       // 接收并转发一千零二十四项表
	localparam [3:0]ST_TABLE_WAIT = 4'd2;       // 等待冻结SiLU确认完整表
	localparam [3:0]ST_PACKET_PAYLOAD = 4'd3;   // 接收一个包的二十二个负载字
	localparam [3:0]ST_PACKET_COMMIT = 4'd4;    // 检查归约边界后原子保存包
	localparam [3:0]ST_RUN_SEND = 4'd5;         // 顺序向冻结计算链接受口发送包
	localparam [3:0]ST_RUN_DRAIN = 4'd6;        // 等待末包忙低后重新就绪
	localparam [3:0]ST_RUN_REPORT = 4'd7;       // 保持完整运行完成响应
	localparam [3:0]ST_EXPORT_REQUEST = 4'd8;   // 通过真实缓存口发起读请求
	localparam [3:0]ST_EXPORT_WAIT = 4'd9;      // 等待真实缓存读响应
	localparam [3:0]ST_EXPORT_SEND = 4'd10;     // 保持逐项真实结果响应
	localparam [3:0]ST_EXPORT_REPORT = 4'd11;   // 保持本次导出完成响应
	localparam [3:0]ST_STATUS_SEND = 4'd12;     // 顺序发送冻结状态快照
	localparam [3:0]ST_DIAG_REQUEST = 4'd13;    // 发起一个显式诊断缓存读
	localparam [3:0]ST_DIAG_WAIT = 4'd14;       // 等待显式诊断缓存响应
	localparam [3:0]ST_DIAG_SEND = 4'd15;       // 保持显式诊断缓存结果

	//命令高四位编码
	localparam [3:0]CMD_TABLE_BEGIN = 4'h1;      // 开始复位后的完整SiLU表装载
	localparam [3:0]CMD_PACKET_BEGIN = 4'h2;     // 开始一个动态计算包装载
	localparam [3:0]CMD_RUN = 4'h3;              // 运行已封闭的一到四个位置
	localparam [3:0]CMD_EXPORT = 4'h4;           // 导出本次运行的已提交结果
	localparam [3:0]CMD_STATUS = 4'h5;           // 读取一个稳定的多字状态快照
	localparam [3:0]CMD_DIAGNOSTIC_READ = 4'h6;  // 显式读取任一缓存地址的故障语义

	//首个保持故障的诊断码
	localparam [7:0]ERR_COMMAND = 8'h01;         // 未知命令或命令保留位非零
	localparam [7:0]ERR_TABLE_SEQUENCE = 8'h02;  // 重复或不允许的表装载命令
	localparam [7:0]ERR_PACKET_SEQUENCE = 8'h03; // 包头或位置边界不合法
	localparam [7:0]ERR_REDUCTION_RANGE = 8'h04; // 归约超过包组或有效项上限
	localparam [7:0]ERR_RUN_GUARD = 8'h05;       // 表包数量或单运行守卫不满足
	localparam [7:0]ERR_EXPORT_GUARD = 8'h06;    // 核心未完成前请求结果导出
	localparam [7:0]ERR_DIAGNOSTIC = 8'h07;      // 显式缓存读命令地址保留位错误
	localparam [7:0]ERR_TABLE_CORE = 8'h08;      // 冻结SiLU报告表装载故障

	//--------------模块实例化信号--------------//
	//冻结最小计算链接口
	wire chain_input_ready;                     // 冻结链输入包接收许可
	wire chain_fault;                           // 冻结链粘滞计算故障
	wire chain_table_ready;                     // 冻结SiLU表项接收许可
	wire chain_table_loaded;                    // 冻结SiLU完整表激活状态
	wire chain_table_fault;                     // 冻结SiLU表装载协议故障
	wire chain_cache_read_ready;                // 冻结特征缓存请求接收许可
	wire chain_cache_result_valid;              // 冻结特征缓存响应有效标志
	wire signed [7:0]chain_cache_result_data;    // 冻结特征缓存真实数据
	wire chain_cache_result_fault;              // 冻结特征缓存读故障

	//----------------计数信号------------------//
	//接收帧与有限归约计数
	reg [9:0]cnt_table_entry = 10'd0;            // 下一项隐式递增表地址
	reg [4:0]cnt_payload_word = 5'd0;            // 当前包负载字零到二十一
	reg [6:0]cnt_packet_loaded = 7'd0;           // 已原子保存的完整动态包数
	reg [2:0]cnt_position_loaded = 3'd0;         // 已由last封闭的一到四个位置数
	reg [4:0]cnt_group_position = 5'd0;          // 当前开放位置完整包组数
	reg [7:0]cnt_term_position = 8'd0;           // 当前开放位置有效乘积数
	reg [6:0]cnt_run_index = 7'd0;               // 下一项送入冻结链的包索引
	reg [3:0]cnt_export_addr = 4'd0;             // 下一项真实缓存读地址
	reg [4:0]cnt_status_index = 5'd0;            // 当前状态快照输出字索引

	//外部传输与分段周期计数
	reg [31:0]cnt_rx_words = 32'd0;              // 复位后外部接收握手总数
	reg [31:0]cnt_tx_words = 32'd0;              // 复位后外部发送握手总数
	reg [31:0]cnt_core_inputs = 32'd0;           // 本次运行冻结链接受包数
	reg [31:0]cnt_result_outputs = 32'd0;        // 本次导出真实缓存响应数
	reg [31:0]cnt_preload_cycles = 32'd0;        // TABLE头后到合法RUN头前墙钟周期
	reg [31:0]cnt_core_cycles = 32'd0;           // RUN后发送和排空阶段墙钟周期
	reg [31:0]cnt_export_cycles = 32'd0;         // EXPORT后读回和发送阶段墙钟周期

	//----------------状态机信号----------------//
	//单时钟命令调度状态
	reg [3:0]state_current = ST_IDLE;            // 当前窄口调度阶段
	reg [3:0]state_next = ST_IDLE;               // 下一窄口调度阶段

	//----------------寄存器信号----------------//
	//一个完整包的装配寄存器
	reg reg_packet_first = 1'b0;                 // 当前包位置首组标志
	reg reg_packet_last = 1'b0;                  // 当前包位置末组标志
	reg [7:0]reg_packet_mask = 8'd0;             // 当前包八路有效掩码
	reg [63:0]reg_packet_activation = 64'd0;      // 当前包完整动态激活值
	reg [191:0]reg_packet_weight = 192'd0;        // 当前包完整动态三路权重
	reg [95:0]reg_packet_bias = 96'd0;            // 当前包完整动态三路偏置
	reg reg_packet_header_legal = 1'b0;          // 当前包头保留位合法状态

	//九十六包有限预装缓存
	reg reg_first_memory [0:95];                 // 每包位置首组标志缓存
	reg reg_last_memory [0:95];                  // 每包位置末组标志缓存
	reg [7:0]reg_mask_memory [0:95];             // 每包八路掩码缓存
	reg [63:0]reg_activation_memory [0:95];       // 每包完整激活缓存
	reg [191:0]reg_weight_memory [0:95];          // 每包三路完整权重缓存
	reg [95:0]reg_bias_memory [0:95];             // 每包三路完整偏置缓存

	//表项与运行命令保持
	reg reg_table_pending_valid = 1'b0;          // 一个未被冻结SiLU接受的表项
	reg signed [15:0]reg_table_pending_data = 16'sd0; // 表项背压保持数据
	reg [6:0]reg_run_packet_count = 7'd0;        // 合法RUN声明的完整包数量
	reg [3:0]reg_export_count = 4'd0;             // 本次正常导出结果数量
	reg [3:0]reg_diagnostic_addr = 4'd0;          // 显式诊断缓存读地址

	//状态响应保持与快照
	reg tx_valid_o = 1'b0;                       // 一个外部响应字保持有效代理
	reg [15:0]tx_data_o = 16'd0;                 // 一个外部响应字保持数据代理
	reg [15:0]reg_result_checksum = 16'd0;        // 真实逐项结果的辅助异或校验
	reg [31:0]reg_snapshot_rx_words = 32'd0;      // 状态命令时冻结接收字计数
	reg [31:0]reg_snapshot_tx_words = 32'd0;      // 状态命令时冻结发送字计数
	reg [31:0]reg_snapshot_core_inputs = 32'd0;   // 状态命令时冻结核心输入计数
	reg [31:0]reg_snapshot_results = 32'd0;       // 状态命令时冻结结果计数
	reg [31:0]reg_snapshot_preload = 32'd0;       // 状态命令时冻结预装载周期
	reg [31:0]reg_snapshot_core = 32'd0;          // 状态命令时冻结核心运行周期
	reg [31:0]reg_snapshot_export = 32'd0;        // 状态命令时冻结结果导出周期

	//-----------------标志信号-----------------//
	//命令和事务生命期标志
	reg flag_table_complete = 1'b0;              // 本次复位后完整表已由冻结核确认
	reg flag_position_open = 1'b0;               // 当前预装位置仍等待last包
	reg flag_preload_active = 1'b0;              // 预装墙钟计数处于活动区间
	reg flag_run_issued = 1'b0;                  // 本次复位已经接受唯一RUN命令
	reg flag_run_complete = 1'b0;                // 末包完整终态已经完成
	reg flag_core_busy_observed = 1'b0;          // 末包握手后确实观察过ready低
	reg flag_core_timing_active = 1'b0;          // 首包握手到末位置完成的计时窗口
	reg flag_export_timing_active = 1'b0;        // EXPORT命令到末结果消费的计时窗口
	reg flag_shell_fault = 1'b0;                 // 窄口协议或范围故障保持标志
	reg [7:0]reg_shell_error = 8'd0;              // 首个窄口故障原因码

	//组合命令与握手事件
	wire flag_rx_transfer;                       // 十六位接收真实握手事件
	wire flag_tx_transfer;                       // 十六位发送真实握手事件
	wire flag_table_transfer;                    // 表项进入冻结SiLU的握手事件
	wire flag_table_last_transfer;               // 第一千零二十四项进入冻结SiLU
	wire flag_core_input_transfer;               // 完整动态包进入冻结链的事件
	wire flag_core_last_transfer;                // RUN声明的最后一个包被接受
	wire flag_cache_request_transfer;            // 真实缓存读请求握手事件
	wire flag_cache_result_transfer;             // 真实缓存响应握手事件
	wire flag_run_command_legal;                 // RUN满足表位置数量和单次守卫
	wire flag_packet_commit_legal;               // 当前完整包满足有限归约守卫
	wire flag_normal_export_legal;                // 当前运行完成且有已封闭位置
	wire flag_diagnostic_legal;                   // 显式诊断读命令保留位合法

	//-----------------其他信号-----------------//
	//范围检查和快照选择
	wire [3:0]enc_packet_terms;                   // 当前包掩码中有效乘积数
	wire [5:0]next_group_count;                   // 保存当前包后的组数候选
	wire [8:0]next_term_count;                    // 保存当前包后的有效项候选
	reg [15:0]dec_status_word = 16'd0;            // 当前状态索引选择的快照字

	//-----------------输出信号-----------------//
	//窄口桥接代理
	reg rx_ready_o = 1'b0;                       // 当前状态外部接收许可代理

	//---------------其他信号连线---------------//
	//外部握手和有限范围
	assign flag_rx_transfer = i_rx_valid & rx_ready_o; // 只在ready同时为高时消费接收字
	assign flag_tx_transfer = tx_valid_o & i_tx_ready; // 只在ready同时为高时消费响应字
	assign enc_packet_terms = {3'd0, reg_packet_mask[0]} + {3'd0, reg_packet_mask[1]} + {3'd0, reg_packet_mask[2]} + {3'd0, reg_packet_mask[3]} + {3'd0, reg_packet_mask[4]} + {3'd0, reg_packet_mask[5]} + {3'd0, reg_packet_mask[6]} + {3'd0, reg_packet_mask[7]}; // 统计最多八个动态有效乘积
	assign next_group_count = {1'b0, cnt_group_position} + 6'd1; // 计算保存当前包后的组数
	assign next_term_count = {1'b0, cnt_term_position} + {5'd0, enc_packet_terms}; // 计算保存当前包后的有效项数

	//冻结链表和计算输入握手
	assign flag_table_transfer = reg_table_pending_valid & chain_table_ready; // 未决表项由冻结SiLU接受
	assign flag_table_last_transfer = flag_table_transfer & (cnt_table_entry == 10'd1023); // 标记完整表最后一项
	assign flag_core_input_transfer = (state_current == ST_RUN_SEND) & chain_input_ready; // RUN阶段每拍保持有效直到接受
	assign flag_core_last_transfer = flag_core_input_transfer & ({1'b0, cnt_run_index} + 8'd1 == {1'b0, reg_run_packet_count}); // 精确识别声明末包

	//冻结链缓存读回握手
	assign flag_cache_request_transfer = ((state_current == ST_EXPORT_REQUEST) || (state_current == ST_DIAG_REQUEST)) & chain_cache_read_ready; // 真实缓存请求已被接受
	assign flag_cache_result_transfer = ((state_current == ST_EXPORT_WAIT) || (state_current == ST_DIAG_WAIT)) & chain_cache_result_valid & (~tx_valid_o); // 空发送槽接受真实缓存响应

	//命令与完整包合法性
	assign flag_run_command_legal = (i_rx_data[11:7] == 5'd0) & (i_rx_data[6:0] != 7'd0) & (i_rx_data[6:0] == cnt_packet_loaded) & flag_table_complete & (~flag_position_open) & (cnt_position_loaded != 3'd0) & (~flag_run_issued) & (~flag_shell_fault); // 仅运行一次完整预装集合
	assign flag_packet_commit_legal = reg_packet_header_legal & (cnt_packet_loaded < MAX_PACKET_COUNT) & (((~flag_position_open) & reg_packet_first) | (flag_position_open & (~reg_packet_first))) & (next_group_count <= 6'd24) & (next_term_count <= 9'd192) & (flag_position_open | (cnt_position_loaded < 3'd4)); // 保证一到二十四组和一百九十二项边界
	assign flag_normal_export_legal = flag_run_complete & (cnt_position_loaded != 3'd0); // 正常导出必须等待完整终态
	assign flag_diagnostic_legal = (i_rx_data[11:4] == 8'd0); // 诊断命令仅允许低四位地址

	//冻结链输入负载
	wire chain_input_valid = (state_current == ST_RUN_SEND); // RUN阶段保持当前完整包有效
	wire chain_first = reg_first_memory[cnt_run_index]; // 当前缓存包首组标志
	wire chain_last = reg_last_memory[cnt_run_index]; // 当前缓存包末组标志
	wire [7:0]chain_lane_mask = reg_mask_memory[cnt_run_index]; // 当前缓存包八路掩码
	wire [63:0]chain_activation_data = reg_activation_memory[cnt_run_index]; // 当前缓存包完整激活
	wire [191:0]chain_weight_data = reg_weight_memory[cnt_run_index]; // 当前缓存包完整三路权重
	wire [95:0]chain_bias_data = reg_bias_memory[cnt_run_index]; // 当前缓存包完整三路偏置
	wire chain_table_valid = reg_table_pending_valid; // 一项表数据保持到冻结SiLU接受
	wire [9:0]chain_table_addr = cnt_table_entry; // 表地址按真实握手严格递增
	wire signed [15:0]chain_table_data = reg_table_pending_data; // 表项数据在背压期间稳定
	wire chain_cache_read_valid = (state_current == ST_EXPORT_REQUEST) | (state_current == ST_DIAG_REQUEST); // 读请求保持到冻结缓存接受
	wire [3:0]chain_cache_read_addr = (state_current == ST_DIAG_REQUEST) ? reg_diagnostic_addr : cnt_export_addr; // 选择正常或显式诊断地址
	wire chain_cache_result_ready = ((state_current == ST_EXPORT_WAIT) || (state_current == ST_DIAG_WAIT)) & (~tx_valid_o); // 仅空发送槽消费真实响应

	//---------------输出信号连线---------------//
	//窄口顶层输出桥接
	assign o_rx_ready = rx_ready_o;              // 外部接收许可桥接
	assign o_tx_valid = tx_valid_o;              // 外部发送有效桥接
	assign o_tx_data = tx_data_o;                // 外部发送数据桥接

	//-------------输出信号处理区域-------------//
	//接收许可只在命令头或当前负载字可被保存时开放
	always@(*)begin
		rx_ready_o = 1'b0;                        // 运行导出和报告阶段默认阻止新命令
		if(state_current == ST_IDLE)begin
			rx_ready_o = ~tx_valid_o;               // 无未消费响应时接收一个命令头
		end else if(state_current == ST_TABLE_DATA)begin
			rx_ready_o = ~reg_table_pending_valid;  // 一项表skid为空时接收下一字
		end else if(state_current == ST_PACKET_PAYLOAD)begin
			rx_ready_o = 1'b1;                     // 包装配寄存器每拍可收一个负载字
		end else begin
			rx_ready_o = 1'b0;                     // 其余状态不解释接收总线
		end
	end

	//状态快照按固定索引选择且在整个响应期间稳定
	always@(*)begin
		case(cnt_status_index)
			5'd0: dec_status_word = {4'hb, chain_fault, chain_table_fault, flag_shell_fault, flag_table_complete, flag_run_complete, flag_run_issued, 3'd0, cnt_position_loaded}; // 快照头与关键状态
			5'd1: dec_status_word = {1'b0, cnt_packet_loaded, reg_shell_error}; // 包数量和首故障码
			5'd2: dec_status_word = reg_snapshot_rx_words[15:0]; // 接收字计数低半字
			5'd3: dec_status_word = reg_snapshot_rx_words[31:16]; // 接收字计数高半字
			5'd4: dec_status_word = reg_snapshot_tx_words[15:0]; // 发送字计数低半字
			5'd5: dec_status_word = reg_snapshot_tx_words[31:16]; // 发送字计数高半字
			5'd6: dec_status_word = reg_snapshot_core_inputs[15:0]; // 核心输入计数低半字
			5'd7: dec_status_word = reg_snapshot_core_inputs[31:16]; // 核心输入计数高半字
			5'd8: dec_status_word = reg_snapshot_results[15:0]; // 结果计数低半字
			5'd9: dec_status_word = reg_snapshot_results[31:16]; // 结果计数高半字
			5'd10: dec_status_word = reg_snapshot_preload[15:0]; // 预装周期低半字
			5'd11: dec_status_word = reg_snapshot_preload[31:16]; // 预装周期高半字
			5'd12: dec_status_word = reg_snapshot_core[15:0]; // 核心运行周期低半字
			5'd13: dec_status_word = reg_snapshot_core[31:16]; // 核心运行周期高半字
			5'd14: dec_status_word = reg_snapshot_export[15:0]; // 结果导出周期低半字
			5'd15: dec_status_word = reg_snapshot_export[31:16]; // 结果导出周期高半字
			5'd16: dec_status_word = reg_result_checksum; // 本次逐项结果辅助异或值
			default: dec_status_word = {6'd0, cnt_table_entry}; // 已真实转移的表项计数模一千零二十四
		endcase
	end

	//----------------状态机区域----------------//
	//当前状态寄存器
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			state_current <= ST_IDLE;               // 复位取消所有部分帧与事务
		end else begin
			state_current <= state_next;           // 进入组合逻辑判定的下一阶段
		end
	end

	//命令与冻结链接口事件判定下一状态
	always@(*)begin
		state_next = state_current;              // 默认保持当前调度阶段
		case(state_current)
			ST_IDLE:begin
				if(flag_rx_transfer == 1'b1)begin
					case(i_rx_data[15:12])
						CMD_TABLE_BEGIN: state_next = ((i_rx_data[11:0] == 12'd0) && (~flag_table_complete) && (~flag_run_issued) && (~flag_shell_fault)) ? ST_TABLE_DATA : ST_IDLE; // 合法表头进入逐项装载
						CMD_PACKET_BEGIN: state_next = (flag_table_complete && (~flag_run_issued) && (~flag_shell_fault)) ? ST_PACKET_PAYLOAD : ST_IDLE; // 表确认后才允许动态包
						CMD_RUN: state_next = flag_run_command_legal ? ST_RUN_SEND : ST_IDLE; // 仅完整封闭集合进入运行
						CMD_EXPORT: state_next = ((i_rx_data[11:0] == 12'd0) && flag_normal_export_legal) ? ST_EXPORT_REQUEST : ST_IDLE; // 完整终态后从地址零导出
						CMD_STATUS: state_next = (i_rx_data[11:0] == 12'd0) ? ST_STATUS_SEND : ST_IDLE; // 合法状态命令发送冻结快照
						CMD_DIAGNOSTIC_READ: state_next = flag_diagnostic_legal ? ST_DIAG_REQUEST : ST_IDLE; // 显式读允许观察未提交故障
						default: state_next = ST_IDLE; // 未知命令只记录故障而不执行
					endcase
				end
			end
			ST_TABLE_DATA:begin
				if(flag_table_last_transfer == 1'b1)begin
					state_next = ST_TABLE_WAIT;       // 完整表最后一项已进入冻结SiLU
				end
			end
			ST_TABLE_WAIT:begin
				if(chain_table_loaded || chain_table_fault)begin
					state_next = ST_IDLE;             // 只接受冻结SiLU实际确认结果
				end
			end
			ST_PACKET_PAYLOAD:begin
				if(flag_rx_transfer && (cnt_payload_word == 5'd21))begin
					state_next = ST_PACKET_COMMIT;    // 二十二个负载字完整后再验证保存
				end
			end
			ST_PACKET_COMMIT:begin
				state_next = ST_IDLE;             // 一拍原子保存或拒绝当前包
			end
			ST_RUN_SEND:begin
				if(flag_core_last_transfer == 1'b1)begin
					state_next = ST_RUN_DRAIN;        // 末包接受不是完整运行完成
				end
			end
			ST_RUN_DRAIN:begin
				if(flag_core_busy_observed && chain_input_ready)begin
					state_next = ST_RUN_REPORT;       // 确认忙低后重新就绪才发布完成
				end
			end
			ST_RUN_REPORT:begin
				if(flag_tx_transfer == 1'b1)begin
					state_next = ST_IDLE;             // 完成响应被接收后开放下一命令
				end
			end
			ST_EXPORT_REQUEST:begin
				if(flag_cache_request_transfer == 1'b1)begin
					state_next = ST_EXPORT_WAIT;      // 等待真实缓存响应而非内部窥视
				end
			end
			ST_EXPORT_WAIT:begin
				if(flag_cache_result_transfer == 1'b1)begin
					state_next = ST_EXPORT_SEND;      // 一个真实结果已进入发送保持槽
				end
			end
			ST_EXPORT_SEND:begin
				if(flag_tx_transfer == 1'b1)begin
					state_next = ({1'b0, cnt_export_addr} + 5'd1 < {1'b0, reg_export_count}) ? ST_EXPORT_REQUEST : ST_EXPORT_REPORT; // 逐项读完后报告导出结束
				end
			end
			ST_EXPORT_REPORT:begin
				if(flag_tx_transfer == 1'b1)begin
					state_next = ST_IDLE;             // 导出完成响应被接收后结束本次命令
				end
			end
			ST_STATUS_SEND:begin
				if(flag_tx_transfer && (cnt_status_index == STATUS_LAST_INDEX))begin
					state_next = ST_IDLE;             // 固定十八字状态快照发送完成
				end
			end
			ST_DIAG_REQUEST:begin
				if(flag_cache_request_transfer == 1'b1)begin
					state_next = ST_DIAG_WAIT;        // 等待指定地址真实缓存响应
				end
			end
			ST_DIAG_WAIT:begin
				if(flag_cache_result_transfer == 1'b1)begin
					state_next = ST_DIAG_SEND;        // 显式诊断结果进入发送保持槽
				end
			end
			ST_DIAG_SEND:begin
				if(flag_tx_transfer == 1'b1)begin
					state_next = ST_IDLE;             // 显式诊断结果已由外部接收
				end
			end
			default:begin
				state_next = ST_IDLE;             // 状态损坏时回到命令等待
			end
		endcase
	end

	//-------------主要任务处理区域-------------//
	//外部握手总数独立累计
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			cnt_rx_words <= 32'd0;                 // 复位清除接收字统计
			cnt_tx_words <= 32'd0;                 // 复位清除发送字统计
		end else begin
			if(flag_rx_transfer)begin
				cnt_rx_words <= cnt_rx_words + 32'd1; // 每个真实接收握手只计一次
			end
			if(flag_tx_transfer)begin
				cnt_tx_words <= cnt_tx_words + 32'd1; // 每个真实发送握手只计一次
			end
		end
	end

	//表项skid保持数据直到冻结SiLU接受
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_table_pending_valid <= 1'b0;       // 复位取消未转移表项
			reg_table_pending_data <= 16'sd0;      // 复位清空保持数据
			cnt_table_entry <= 10'd0;              // 复位要求从地址零重新装表
			flag_table_complete <= 1'b0;           // 复位禁止直接使用旧表内容
		end else begin
			if((state_current == ST_IDLE) && flag_rx_transfer && (i_rx_data == 16'h1000))begin
				cnt_table_entry <= 10'd0;            // 合法表头重新建立隐式地址
				flag_table_complete <= 1'b0;         // 仅冻结SiLU确认后恢复完整标志
			end
			if((state_current == ST_TABLE_DATA) && flag_rx_transfer)begin
				reg_table_pending_valid <= 1'b1;     // 保存一个十六位动态表项
				reg_table_pending_data <= i_rx_data; // 背压期间保持原始表值
			end else if(flag_table_transfer)begin
				reg_table_pending_valid <= 1'b0;     // 冻结SiLU接受后释放skid
				cnt_table_entry <= cnt_table_entry + 10'd1; // 真实握手驱动下一隐式地址
			end
			if((state_current == ST_TABLE_WAIT) && chain_table_loaded && (~chain_table_fault))begin
				flag_table_complete <= 1'b1;         // 一千零二十四项由冻结核实际确认
			end
		end
	end

	//包头建立完整动态负载装配上下文
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_packet_first <= 1'b0;              // 复位清除部分包首标志
			reg_packet_last <= 1'b0;               // 复位清除部分包末标志
			reg_packet_mask <= 8'd0;               // 复位清除部分包掩码
			reg_packet_header_legal <= 1'b0;       // 复位使部分包不可提交
			cnt_payload_word <= 5'd0;              // 复位回到第一个负载字
		end else if((state_current == ST_IDLE) && flag_rx_transfer && (i_rx_data[15:12] == CMD_PACKET_BEGIN) && flag_table_complete && (~flag_run_issued) && (~flag_shell_fault))begin
			reg_packet_first <= i_rx_data[11];     // 保存动态first字段
			reg_packet_last <= i_rx_data[10];      // 保存动态last字段
			reg_packet_mask <= i_rx_data[9:2];     // 保存动态八路掩码
			reg_packet_header_legal <= (i_rx_data[1:0] == 2'd0); // 保留位必须为零
			cnt_payload_word <= 5'd0;              // 下一接收字是激活低十六位
		end else if((state_current == ST_PACKET_PAYLOAD) && flag_rx_transfer)begin
			cnt_payload_word <= cnt_payload_word + 5'd1; // 每次接收一个负载字
		end
	end

	//二十二个负载字按低字优先装入完整并行字段
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_packet_activation <= 64'd0;        // 复位取消部分激活负载
			reg_packet_weight <= 192'd0;           // 复位取消部分权重负载
			reg_packet_bias <= 96'd0;              // 复位取消部分偏置负载
		end else if((state_current == ST_IDLE) && flag_rx_transfer && (i_rx_data[15:12] == CMD_PACKET_BEGIN))begin
			reg_packet_activation <= 64'd0;        // 新包先清除历史激活字
			reg_packet_weight <= 192'd0;           // 新包先清除历史权重字
			reg_packet_bias <= 96'd0;              // 新包先清除历史偏置字
		end else if((state_current == ST_PACKET_PAYLOAD) && flag_rx_transfer)begin
			if(cnt_payload_word < 5'd4)begin
				reg_packet_activation[cnt_payload_word * 16 +: 16] <= i_rx_data; // 装入四个激活字
			end else if(cnt_payload_word < 5'd16)begin
				reg_packet_weight[(cnt_payload_word - 5'd4) * 16 +: 16] <= i_rx_data; // 装入十二个权重字
			end else begin
				reg_packet_bias[(cnt_payload_word - 5'd16) * 16 +: 16] <= i_rx_data; // 装入六个偏置字
			end
		end
	end

	//完整包通过有限归约守卫后写入九十六项缓存
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			cnt_packet_loaded <= 7'd0;             // 复位使所有旧包不可运行
			cnt_position_loaded <= 3'd0;           // 复位清除封闭位置数量
			cnt_group_position <= 5'd0;            // 复位清除开放位置组计数
			cnt_term_position <= 8'd0;             // 复位清除开放位置有效项计数
			flag_position_open <= 1'b0;            // 复位取消部分位置
		end else if((state_current == ST_PACKET_COMMIT) && flag_packet_commit_legal)begin
			reg_first_memory[cnt_packet_loaded] <= reg_packet_first; // 保存动态first不改为常量
			reg_last_memory[cnt_packet_loaded] <= reg_packet_last; // 保存动态last不改为常量
			reg_mask_memory[cnt_packet_loaded] <= reg_packet_mask; // 保存动态lane mask
			reg_activation_memory[cnt_packet_loaded] <= reg_packet_activation; // 保存完整动态激活
			reg_weight_memory[cnt_packet_loaded] <= reg_packet_weight; // 保存完整动态权重
			reg_bias_memory[cnt_packet_loaded] <= reg_packet_bias; // 保存完整动态偏置
			cnt_packet_loaded <= cnt_packet_loaded + 7'd1; // 完整包才增加可运行数量
			if(reg_packet_last)begin
				cnt_position_loaded <= cnt_position_loaded + 3'd1; // last封闭一个完整位置
				cnt_group_position <= 5'd0;        // 下一位置重新统计包组
				cnt_term_position <= 8'd0;         // 下一位置重新统计有效乘积
				flag_position_open <= 1'b0;        // 位置闭合后允许下一个first
			end else begin
				cnt_group_position <= next_group_count[4:0]; // 保留开放位置累计组数
				cnt_term_position <= next_term_count[7:0]; // 保留开放位置累计有效项
				flag_position_open <= 1'b1;        // 后续包不得再次声明first
			end
		end
	end

	//单次RUN发送计数并等待末包真实握手
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_run_packet_count <= 7'd0;          // 复位取消旧运行声明
			cnt_run_index <= 7'd0;                 // 复位从缓存零开始
			cnt_core_inputs <= 32'd0;              // 复位清除核心输入统计
			flag_run_issued <= 1'b0;               // 每次复位只允许一次RUN
			flag_run_complete <= 1'b0;             // 复位清除完整终态状态
			flag_core_busy_observed <= 1'b0;       // 复位清除末包忙低证据
		end else begin
			if((state_current == ST_IDLE) && flag_rx_transfer && (i_rx_data[15:12] == CMD_RUN) && flag_run_command_legal)begin
				reg_run_packet_count <= i_rx_data[6:0]; // 冻结本次RUN精确包数量
				cnt_run_index <= 7'd0;               // 从第一项预装缓存开始发送
				cnt_core_inputs <= 32'd0;           // 核心输入统计限定当前RUN
				flag_run_issued <= 1'b1;            // 拒绝复位前第二次RUN
				flag_run_complete <= 1'b0;          // 末包完整终态尚未完成
				flag_core_busy_observed <= 1'b0;    // 必须重新观察ready忙低
			end else if(flag_core_input_transfer)begin
				cnt_run_index <= cnt_run_index + 7'd1; // 只有真实握手推进缓存索引
				cnt_core_inputs <= cnt_core_inputs + 32'd1; // 记录冻结链接受包数
			end
			if((state_current == ST_RUN_DRAIN) && (~chain_input_ready))begin
				flag_core_busy_observed <= 1'b1;    // 记录末包后真实ready低区间
			end
			if((state_current == ST_RUN_DRAIN) && flag_core_busy_observed && chain_input_ready)begin
				flag_run_complete <= 1'b1;          // 忙低后重新就绪定义完整RUN完成
			end
		end
	end

	//三个互斥阶段周期独立统计
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			cnt_preload_cycles <= 32'd0;           // 复位清除预装墙钟周期
			cnt_core_cycles <= 32'd0;              // 复位清除核心运行周期
			cnt_export_cycles <= 32'd0;            // 复位清除结果导出周期
			flag_preload_active <= 1'b0;           // 复位尚未接受TABLE头
			flag_core_timing_active <= 1'b0;       // 复位关闭核心周期窗口
			flag_export_timing_active <= 1'b0;     // 复位关闭导出周期窗口
		end else begin
			if((state_current == ST_IDLE) && flag_rx_transfer && (i_rx_data == 16'h1000) && (~flag_table_complete) && (~flag_run_issued) && (~flag_shell_fault))begin
				flag_preload_active <= 1'b1;         // 从合法表头后开始预装墙钟计数
				cnt_preload_cycles <= 32'd0;        // 新复位会话只建立一次预装区间
			end else if((state_current == ST_IDLE) && flag_rx_transfer && (i_rx_data[15:12] == CMD_RUN) && flag_run_command_legal)begin
				flag_preload_active <= 1'b0;         // 合法RUN头结束预装区间
				cnt_core_cycles <= 32'd0;           // 等待首个并行输入握手建立计时起点
			end else if(flag_preload_active)begin
				cnt_preload_cycles <= cnt_preload_cycles + 32'd1; // 包含外部装载停顿但不混入核心运行
			end
			if(flag_core_input_transfer && (cnt_core_inputs == 32'd0))begin
				flag_core_timing_active <= 1'b1;     // 首个并行输入握手是核心周期起点
				cnt_core_cycles <= 32'd1;            // 起点握手周期计入核心运行
			end else if(flag_core_timing_active)begin
				cnt_core_cycles <= cnt_core_cycles + 32'd1; // 统计到末位置完整终态
			end
			if((state_current == ST_RUN_DRAIN) && flag_core_busy_observed && chain_input_ready)begin
				flag_core_timing_active <= 1'b0;     // 完整终态周期计入后关闭窗口
			end
			if((state_current == ST_IDLE) && flag_rx_transfer && (i_rx_data[15:12] == CMD_EXPORT) && (i_rx_data[11:0] == 12'd0) && flag_normal_export_legal)begin
				cnt_export_cycles <= 32'd1;         // EXPORT请求握手周期是导出起点
				flag_export_timing_active <= 1'b1; // 开始统计真实读口和窄口发送
			end else if(flag_export_timing_active)begin
				cnt_export_cycles <= cnt_export_cycles + 32'd1; // 包含真实读口和TX背压等待
			end
			if((state_current == ST_EXPORT_SEND) && flag_tx_transfer && ({1'b0, cnt_export_addr} + 5'd1 >= {1'b0, reg_export_count}))begin
				flag_export_timing_active <= 1'b0;   // 最后一个逐项结果消费后停止计时
			end
		end
	end

	//正常导出和显式诊断地址控制
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			cnt_export_addr <= 4'd0;               // 复位从真实缓存地址零开始
			reg_export_count <= 4'd0;              // 复位清除正常导出数量
			reg_diagnostic_addr <= 4'd0;           // 复位清除显式诊断地址
			cnt_result_outputs <= 32'd0;           // 复位清除本次结果数量
			reg_result_checksum <= 16'd0;          // 复位清除辅助校验值
		end else begin
			if((state_current == ST_IDLE) && flag_rx_transfer && (i_rx_data[15:12] == CMD_EXPORT) && (i_rx_data[11:0] == 12'd0) && flag_normal_export_legal)begin
				cnt_export_addr <= 4'd0;             // 正常导出每次从地址零开始
				reg_export_count <= {1'b0, cnt_position_loaded} + {cnt_position_loaded, 1'b0}; // 每个完整位置恰好三项结果
				cnt_result_outputs <= 32'd0;         // 结果计数限定当前导出命令
				reg_result_checksum <= 16'd0;        // 辅助校验限定当前导出命令
			end else if((state_current == ST_EXPORT_SEND) && flag_tx_transfer)begin
				cnt_export_addr <= cnt_export_addr + 4'd1; // 一个结果真正发送后推进地址
			end
			if((state_current == ST_IDLE) && flag_rx_transfer && (i_rx_data[15:12] == CMD_DIAGNOSTIC_READ) && flag_diagnostic_legal)begin
				reg_diagnostic_addr <= i_rx_data[3:0]; // 保存显式诊断缓存地址
			end
			if((state_current == ST_EXPORT_WAIT) && flag_cache_result_transfer)begin
				cnt_result_outputs <= cnt_result_outputs + 32'd1; // 每个真实缓存响应只计一次
				reg_result_checksum <= reg_result_checksum ^ {4'd0, cnt_export_addr, chain_cache_result_data}; // 地址和真实数据形成辅助异或
			end
		end
	end

	//首个壳协议故障保持到复位且禁止RUN
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			flag_shell_fault <= 1'b0;              // 复位清除窄口协议故障
			reg_shell_error <= 8'd0;               // 复位清除首故障原因
		end else if(~flag_shell_fault)begin
			if((state_current == ST_TABLE_WAIT) && chain_table_fault)begin
				flag_shell_fault <= 1'b1;            // 冻结SiLU拒绝表序列
				reg_shell_error <= ERR_TABLE_CORE;   // 保存表核心故障原因
			end else if((state_current == ST_PACKET_COMMIT) && (~flag_packet_commit_legal))begin
				flag_shell_fault <= 1'b1;            // 拒绝包序列或归约越界
				reg_shell_error <= ((next_group_count > 6'd24) || (next_term_count > 9'd192)) ? ERR_REDUCTION_RANGE : ERR_PACKET_SEQUENCE; // 区分有限范围与序列错误
			end else if((state_current == ST_IDLE) && flag_rx_transfer)begin
				case(i_rx_data[15:12])
					CMD_TABLE_BEGIN:begin
						if((i_rx_data[11:0] != 12'd0) || flag_table_complete || flag_run_issued)begin
							flag_shell_fault <= 1'b1;        // 拒绝重复或带保留位的表头
							reg_shell_error <= ERR_TABLE_SEQUENCE; // 保存表命令序列原因
						end
					end
					CMD_PACKET_BEGIN:begin
						if((~flag_table_complete) || flag_run_issued)begin
							flag_shell_fault <= 1'b1;        // 表未完成或RUN后禁止装新包
							reg_shell_error <= ERR_PACKET_SEQUENCE; // 保存包命令序列原因
						end
					end
					CMD_RUN:begin
						if(~flag_run_command_legal)begin
							flag_shell_fault <= 1'b1;        // RUN数量或完整性守卫失败
							reg_shell_error <= ERR_RUN_GUARD; // 保存运行守卫原因
						end
					end
					CMD_EXPORT:begin
						if((i_rx_data[11:0] != 12'd0) || (~flag_normal_export_legal))begin
							flag_shell_fault <= 1'b1;        // 完整终态前不得正常导出
							reg_shell_error <= ERR_EXPORT_GUARD; // 保存结果导出守卫原因
						end
					end
					CMD_STATUS:begin
						if(i_rx_data[11:0] != 12'd0)begin
							flag_shell_fault <= 1'b1;        // 状态命令保留位必须为零
							reg_shell_error <= ERR_COMMAND;  // 保存通用命令编码原因
						end
					end
					CMD_DIAGNOSTIC_READ:begin
						if(~flag_diagnostic_legal)begin
							flag_shell_fault <= 1'b1;        // 诊断读只解释低四位地址
							reg_shell_error <= ERR_DIAGNOSTIC; // 保存诊断命令原因
						end
					end
					default:begin
						flag_shell_fault <= 1'b1;        // 拒绝未知高四位命令
						reg_shell_error <= ERR_COMMAND;  // 保存未知命令原因
					end
				endcase
			end
		end
	end

	//状态命令一次冻结所有多字字段
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_snapshot_rx_words <= 32'd0;        // 复位清除接收快照
			reg_snapshot_tx_words <= 32'd0;        // 复位清除发送快照
			reg_snapshot_core_inputs <= 32'd0;     // 复位清除核心输入快照
			reg_snapshot_results <= 32'd0;         // 复位清除结果快照
			reg_snapshot_preload <= 32'd0;         // 复位清除预装周期快照
			reg_snapshot_core <= 32'd0;            // 复位清除核心周期快照
			reg_snapshot_export <= 32'd0;          // 复位清除导出周期快照
			cnt_status_index <= 5'd0;              // 复位指向状态头
		end else if((state_current == ST_IDLE) && flag_rx_transfer && (i_rx_data == 16'h5000))begin
			reg_snapshot_rx_words <= cnt_rx_words; // 命令接收前已完成接收计数
			reg_snapshot_tx_words <= cnt_tx_words; // 命令时冻结历史发送计数
			reg_snapshot_core_inputs <= cnt_core_inputs; // 冻结当前RUN包接受总数
			reg_snapshot_results <= cnt_result_outputs; // 冻结最近导出真实结果数
			reg_snapshot_preload <= cnt_preload_cycles; // 冻结预装墙钟周期
			reg_snapshot_core <= cnt_core_cycles; // 冻结核心发送排空墙钟周期
			reg_snapshot_export <= cnt_export_cycles; // 冻结最近导出墙钟周期
			cnt_status_index <= 5'd0;              // 状态响应从头字开始
		end else if((state_current == ST_STATUS_SEND) && flag_tx_transfer)begin
			cnt_status_index <= cnt_status_index + 5'd1; // 每个真实发送握手推进一次
		end
	end

	//单字发送槽保证背压期间数据和有效位不变
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			tx_valid_o <= 1'b0;                    // 复位取消未消费响应
			tx_data_o <= 16'd0;                    // 复位清空响应数据
		end else begin
			if((state_current == ST_RUN_DRAIN) && flag_core_busy_observed && chain_input_ready)begin
				tx_valid_o <= 1'b1;                  // 完整终态完成后发布RUN响应
				tx_data_o <= {4'ha, chain_fault, chain_table_fault, flag_shell_fault, cnt_position_loaded, 6'd0}; // 携带故障与完整位置数量
			end else if((state_current == ST_EXPORT_WAIT) && flag_cache_result_transfer)begin
				tx_valid_o <= 1'b1;                  // 保存一个真实缓存结果
				tx_data_o <= {3'b100, chain_cache_result_fault, cnt_export_addr, chain_cache_result_data}; // 地址故障和逐项数据同字返回
			end else if((state_current == ST_EXPORT_SEND) && flag_tx_transfer)begin
				tx_valid_o <= ({1'b0, cnt_export_addr} + 5'd1 < {1'b0, reg_export_count}) ? 1'b0 : 1'b1; // 末项后直接建立导出完成字
				tx_data_o <= 16'hc000 | {8'd0, cnt_result_outputs[7:0]}; // 报告本次真实响应数量
			end else if((state_current == ST_EXPORT_REPORT) && flag_tx_transfer)begin
				tx_valid_o <= 1'b0;                  // 导出完成字已被外部接受
			end else if((state_current == ST_IDLE) && flag_rx_transfer && (i_rx_data == 16'h5000))begin
				tx_valid_o <= 1'b1;                  // 合法状态命令立即建立快照头
				tx_data_o <= {4'hb, chain_fault, chain_table_fault, flag_shell_fault, flag_table_complete, flag_run_complete, flag_run_issued, 3'd0, cnt_position_loaded}; // 第一字使用命令边沿状态
			end else if((state_current == ST_STATUS_SEND) && flag_tx_transfer)begin
				if(cnt_status_index == STATUS_LAST_INDEX)begin
					tx_valid_o <= 1'b0;                // 最后快照字已被外部接受
				end else begin
					tx_valid_o <= 1'b1;                // 下一快照字无气泡替换保持槽
					case(cnt_status_index)
						5'd0: tx_data_o <= {1'b0, cnt_packet_loaded, reg_shell_error}; // 状态字一包数和故障码
						5'd1: tx_data_o <= reg_snapshot_rx_words[15:0]; // 状态字二接收低半字
						5'd2: tx_data_o <= reg_snapshot_rx_words[31:16]; // 状态字三接收高半字
						5'd3: tx_data_o <= reg_snapshot_tx_words[15:0]; // 状态字四发送低半字
						5'd4: tx_data_o <= reg_snapshot_tx_words[31:16]; // 状态字五发送高半字
						5'd5: tx_data_o <= reg_snapshot_core_inputs[15:0]; // 状态字六核心输入低半字
						5'd6: tx_data_o <= reg_snapshot_core_inputs[31:16]; // 状态字七核心输入高半字
						5'd7: tx_data_o <= reg_snapshot_results[15:0]; // 状态字八结果低半字
						5'd8: tx_data_o <= reg_snapshot_results[31:16]; // 状态字九结果高半字
						5'd9: tx_data_o <= reg_snapshot_preload[15:0]; // 状态字十预装低半字
						5'd10: tx_data_o <= reg_snapshot_preload[31:16]; // 状态字十一预装高半字
						5'd11: tx_data_o <= reg_snapshot_core[15:0]; // 状态字十二核心低半字
						5'd12: tx_data_o <= reg_snapshot_core[31:16]; // 状态字十三核心高半字
						5'd13: tx_data_o <= reg_snapshot_export[15:0]; // 状态字十四导出低半字
						5'd14: tx_data_o <= reg_snapshot_export[31:16]; // 状态字十五导出高半字
						5'd15: tx_data_o <= reg_result_checksum; // 状态字十六辅助逐项校验
						default: tx_data_o <= {6'd0, cnt_table_entry}; // 状态字十七表项握手计数模值
					endcase
				end
			end else if((state_current == ST_DIAG_WAIT) && flag_cache_result_transfer)begin
				tx_valid_o <= 1'b1;                  // 保存显式诊断缓存响应
				tx_data_o <= {3'b100, chain_cache_result_fault, reg_diagnostic_addr, chain_cache_result_data}; // 与正常结果使用同一逐项编码
			end else if((state_current == ST_DIAG_SEND) && flag_tx_transfer)begin
				tx_valid_o <= 1'b0;                  // 显式诊断结果已被外部接受
			end
		end
	end

	//----------------模块实例化----------------//
	//冻结最小计算链实例仅由窄口壳缓存适配
	road_onchip_chain road_onchip_chain_Inst_shell(
		.i_clk(i_clk),                          // 共用一百兆时钟
		.i_rstn(i_rstn),                        // 共用异步低有效取消复位
		.i_input_valid(chain_input_valid),      // 预装完整包保持有效
		.i_first(chain_first),                  // 动态位置首组标志
		.i_last(chain_last),                    // 动态位置末组标志
		.i_lane_mask(chain_lane_mask),          // 动态八路有效掩码
		.i_activation_data(chain_activation_data), // 动态六十四位激活
		.i_weight_data(chain_weight_data),      // 动态一百九十二位权重
		.i_bias_data(chain_bias_data),          // 动态九十六位偏置
		.o_input_ready(chain_input_ready),      // 冻结链接收许可
		.o_fault(chain_fault),                  // 冻结链粘滞故障
		.i_table_valid(chain_table_valid),      // skid表项保持有效
		.i_table_addr(chain_table_addr),        // 真实握手递增表地址
		.i_table_data(chain_table_data),        // 动态Q7.8表项
		.o_table_ready(chain_table_ready),      // 冻结SiLU表接收许可
		.o_table_loaded(chain_table_loaded),    // 冻结SiLU完整表确认
		.o_table_fault(chain_table_fault),      // 冻结SiLU表序列故障
		.i_cache_read_valid(chain_cache_read_valid), // 正常或诊断读请求保持有效
		.i_cache_read_addr(chain_cache_read_addr), // 真实缓存读地址
		.o_cache_read_ready(chain_cache_read_ready), // 真实缓存请求许可
		.o_cache_result_valid(chain_cache_result_valid), // 真实缓存响应有效
		.o_cache_result_data(chain_cache_result_data), // 真实缓存逐项INT8结果
		.o_cache_result_fault(chain_cache_result_fault), // 真实缓存未提交或越界故障
		.i_cache_result_ready(chain_cache_result_ready) // 空发送槽接受真实响应
	);

endmodule
