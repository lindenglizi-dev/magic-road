`timescale 1ns / 1ps

////////////////////////////////////English///////////////////////////////////////
// Company:         Erie
// Engineer:        Erie
//
// Create Date:     2026/10/16 00:00:00
// Design Name:     Standard convolution arithmetic ownership
// Module Name:     road_standard_arithmetic_owner
// Description:     description/road_standard_arithmetic_owner_Design.pdf
// Simulations:     testbench/vivado/2021.1/road_standard_arithmetic_owner
//
// Referrences:
// File Format      File Name
// 1.Markdown       road_standard_arithmetic_owner_spec.md
//
// Dependencies:
// Module Name      Version
// road_mac_probe, road_dynamic_postprocess
//
// Version:         V1.0
// Revision Date:   2026/10/16 00:00:00
// History:
// Time             Version     Revised by        Contents
// 2026/10/16       V1.0        Codex             Create bounded owner.
///////////////////////////////////Chinese////////////////////////////////////////
// 版权归属:        Erie
// 开发人员:        Erie
//
// 创建日期:        2026年10月16日
// 设计名称:        Standard convolution arithmetic ownership
// 模块名称:        road_standard_arithmetic_owner
// 模块说明:        Description/road_standard_arithmetic_owner_Design.pdf
// 仿真工程:        TestBench/Vivado/2021.1/road_standard_arithmetic_owner
//
// 参考资料:
// 文件格式         文件名称
// 1.Markdown       road_standard_arithmetic_owner_spec.md
//
// 依赖文件:
// 模块名称         版本
// road_mac_probe, road_dynamic_postprocess
//
// 当前版本:        V1.0
// 修订日期:        2026年10月16日
// 修订历史:
// 时间             版本        修订人            修订内容
// 2026年10月16日   V1.0        Codex             创建单事务占有

module road_standard_arithmetic_owner
(
	//-----------------全局信号-----------------//
	input i_clk,                                // 原五核共同100MHz时钟
	input i_rstn,                               // 原核与owner共同低有效异步复位

	//-----------------用户接口-----------------//

	//TABLE接口
	input i_table_valid,                        // 空闲时保持一个待装SiLU表项
	input [9:0]i_table_addr,                    // 原SiLU严格递增装载地址
	input signed [15:0]i_table_data,            // 冻结模型Q7.8表项
	input i_input_valid,                        // 当前八输入组保持至接受
	input i_first,                              // 首组锁存全部任务属性
	input i_last,                               // 当前组关闭本次归约
	input [7:0]i_lane_mask,                     // 八输入槽共享有效掩码
	input [63:0]i_activation_data,              // 低字节优先八路INT8输入
	input [191:0]i_weight_data,                 // 三路各八个INT8权重
	input [95:0]i_bias_data,                    // 仅原MAC首组计入三路INT32偏置
	input [2:0]i_output_mask,                   // 首组声明有效输出路
	input [47:0]i_tags,                         // 首组声明三路不透明标识
	input [95:0]i_addresses,                    // 首组声明三路逻辑写地址
	input [95:0]i_pre_multipliers,              // 首组锁存三路前重定标乘数
	input [17:0]i_pre_shifts,                   // 首组锁存三路前重定标移位
	input [31:0]i_post_multiplier,              // 首组锁存本层后乘数
	input [5:0]i_post_shift,                    // 首组锁存本层后移位
	input i_activate,                           // 首组选择SiLU INT8或raw INT16
	input i_input_fault,                        // 接受组携带的任务错误
	input i_output_ready,                       // 单写端真实接收完整结果
	output o_table_ready,                       // 原核允许且当前空闲的表接收条件
	output o_table_loaded,                      // 原核完整SiLU表状态原样转发
	output o_input_ready,                       // 当前归约可接受下一组

	//OUTPUT接口
	output o_output_valid,                      // 身份类型正确的保持输出
	output signed [15:0]o_output_data,          // 符号扩展INT8或完整raw INT16
	output o_output_int16,                      // 当前结果属于raw类型
	output [15:0]o_output_tag,                  // 与结果保持一致的任务标识
	output [31:0]o_output_address,              // 对应标识的首组写地址
	output o_fault,                             // 任一核或占有协议故障
	output o_busy                               // 首组至末有效输出退休全程占有
);

	//---------------状态参数区域---------------//
	//任务阶段编码
	localparam [2:0]ST_IDLE = 3'd0;             // 等待首组或装表
	localparam [2:0]ST_GROUP = 3'd1;            // 接收当前任务后续组
	localparam [2:0]ST_ACC = 3'd2;              // 等待MAC完整结果向DPP交接
	localparam [2:0]ST_OUTPUT = 3'd3;           // 等待全部输出真实写端退休
	localparam [2:0]ST_FAULT = 3'd4;            // 故障保持直到共同复位

	//--------------模块实例化信号--------------//
	//road_mac_probe--用户接口
	wire [95:0]wire_mac_data;                   // 原MAC最终INT32结果

	//----------------状态机信号----------------//
	//控制状态
	reg [2:0]state_current = 0;                 // 当前唯一任务阶段
	reg [2:0]state_next = 0;                    // 下一拍控制阶段

	//----------------寄存器信号----------------//
	//首组拥有的固定元数据
	reg [1:0]reg_release = 0;                   // 两级准入释放流水
	reg [2:0]reg_remaining = 0;                 // 尚未真实退休的有效输出路
	reg [2:0]reg_output_mask = 0;               // 本任务DPP输出掩码
	reg [47:0]reg_tags = 0;                     // 本任务不透明输出身份
	reg [95:0]reg_addresses = 0;                // 本任务三路写地址
	reg [95:0]reg_pre_multipliers = 0;          // 本任务三路前乘数
	reg [17:0]reg_pre_shifts = 0;               // 本任务三路前移位
	reg [31:0]reg_post_multiplier = 0;          // 本任务共享后乘数
	reg [5:0]reg_post_shift = 0;                // 本任务共享后移位

	//-----------------标志信号-----------------//
	//原算术核边界
	wire flag_mac_ready;                        // 原MAC组入口许可
	wire flag_mac_valid;                        // 原MAC三路完整结果有效
	wire flag_mac_fault;                        // 原MAC末组原子越界
	wire flag_pp_ready;                         // 原DPP完整batch入口许可
	wire flag_pp_valid;                         // 原DPP保持型逐路结果有效
	wire flag_pp_fault;                         // 原DPP粘滞故障
	wire flag_pp_table_ready;                   // 原DPP装表握手条件
	reg flag_activate = 0;                      // 本任务固定数值模式

	//握手与信任边界
	wire flag_idle;                             // 空闲阶段解码
	wire flag_group;                            // 后续组阶段解码
	wire flag_acc;                              // 累加交接阶段解码
	wire flag_output;                           // 结果退休阶段解码
	wire flag_input_window;                     // 接收组阶段合并
	wire flag_input_accept;                     // 外部组真实握手
	wire flag_first_accept;                     // 首组元数据真实锁存事件
	wire flag_duplicate_alpha;                  // 首两路有效身份冲突
	wire flag_duplicate_beta;                   // 首末路有效身份冲突
	wire flag_duplicate_gamma;                  // 后两路有效身份冲突
	wire flag_bad_metadata;                     // 首组掩码或身份非法
	wire flag_bad_sequence;                     // 首组标志不符合当前归约阶段
	wire flag_bad_group;                        // 本拍已接受组不可送原MAC
	wire flag_mac_input;                        // 仅合法接受组进入MAC
	wire flag_acc_ready;                        // 完整结果真实转交许可
	wire flag_acc_accept;                       // 本任务唯一MAC到DPP握手
	wire flag_identity;                         // 当前tag恰好属于一个未退休路
	wire flag_bad_type;                         // raw属性与首组模式不符
	wire flag_bad_sign;                         // 激活输出高字节未符号扩展
	wire flag_bad_output;                       // 输出身份或数值类型损坏
	wire flag_output_accept;                    // 当前逐路写端真实退休
	wire flag_last_accept;                      // 最后一条有效路真实退休
	wire flag_fault_now;                        // 进入故障保持的同步原因
	wire flag_core_fault;                       // 不依赖当前输入valid的立即故障原因
	wire flag_table_enable;                     // 表写入仅空闲释放后允许
	wire flag_pp_input;                         // 完整MAC结果对DPP保持有效
	wire flag_pp_output_ready;                  // 合法输出才能由写端消费

	//-----------------其他信号-----------------//
	wire [2:0]wire_match;                       // 当前tag在remaining中的匹配路

	//-----------------输出信号-----------------//
	//用户接口TABLE接口
	//用户接口
	//对外握手桥接
	wire table_ready_o;                         // 表接收准入结果
	wire table_loaded_o;                        // 原完整表标志
	wire input_ready_o;                         // 外部组接收准入

	//用户接口OUTPUT接口
	wire output_valid_o;                        // 原保持槽的安全发布许可
	wire signed [15:0]output_data_o;            // 原DPP逐路数值
	wire output_int16_o;                        // 原DPP输出类型
	wire [15:0]output_tag_o;                    // 原DPP外部输出身份
	wire [31:0]output_address_o;                // 身份选择对应地址
	//用户接口
	wire fault_o;                               // 故障即时阻止成功传输
	wire busy_o;                                // 归约与故障的占有状态

	//---------------其他信号连线---------------//
	//其他信号连线
	//固定任务阶段和准入
	assign flag_idle = state_current == ST_IDLE; // 空闲阶段不拥有旧任务
	assign flag_group = state_current == ST_GROUP; // 已接首组但未接末组
	assign flag_acc = state_current == ST_ACC;  // 末组已接且等待完整累加
	assign flag_output = state_current == ST_OUTPUT; // 完整累加已由DPP接管
	assign flag_input_window = flag_idle || flag_group; // 只在组阶段接纳操作数
	assign input_ready_o = reg_release[1] && table_loaded_o && flag_mac_ready && flag_input_window && !(flag_idle && i_table_valid) && !flag_pp_fault; // 空闲表请求优先
	assign flag_acc_ready = flag_acc && flag_pp_ready && !flag_mac_fault && !flag_pp_fault; // MAC结果仅完整交接阶段退休
	assign flag_acc_accept = flag_mac_valid && flag_acc_ready; // 一次完整三路结果由DPP保管
	assign flag_pp_input = flag_acc && flag_mac_valid && !flag_mac_fault && !flag_pp_fault; // DPP输入有效保持至接受
	assign wire_match[0] = reg_remaining[0] && output_tag_o == reg_tags[15:0]; // 只匹配未退休的首路身份
	assign wire_match[1] = reg_remaining[1] && output_tag_o == reg_tags[31:16]; // 只匹配未退休的中路身份
	assign wire_match[2] = reg_remaining[2] && output_tag_o == reg_tags[47:32]; // 只匹配未退休的末路身份
	assign flag_identity = wire_match == 3'b001 || wire_match == 3'b010 || wire_match == 3'b100; // 输出必须恰好归属一个有效路
	assign flag_bad_type = output_int16_o == flag_activate; // raw标志必须等于激活反值
	assign flag_bad_sign = flag_activate && output_data_o[15:8] != {8{output_data_o[7]}}; // 激活路径高字节只允许符号扩展
	assign flag_bad_output = !flag_identity || flag_bad_type || flag_bad_sign; // 直接发布前核验归属和完整类型
	assign flag_core_fault = flag_pp_fault || (flag_mac_valid && flag_mac_fault) || (flag_output && flag_pp_valid && flag_bad_output); // 原核及输出错误立即关闭成功出口
	assign fault_o = state_current == ST_FAULT || flag_core_fault; // 当前inputvalid不组合反馈至上游fault门控
	assign busy_o = !flag_idle || fault_o;      // 错误任务不返回空闲
	assign output_valid_o = reg_release[1] && flag_output && flag_pp_valid && !fault_o; // 错误payload不得成功写端传输
	assign flag_table_enable = reg_release[1] && flag_idle && !fault_o; // 任务占有期间禁止重载表
	assign table_ready_o = flag_table_enable && flag_pp_table_ready; // 表ready必须来自原DPP真实许可
	assign output_address_o = wire_match[0] ? reg_addresses[31:0] : wire_match[1] ? reg_addresses[63:32] : reg_addresses[95:64]; // 地址只选首组固定字段

	//TABLE接口
	assign flag_input_accept = i_input_valid && input_ready_o; // 外部输入仅双边成立时消费
	assign flag_first_accept = flag_input_accept && flag_idle; // 空闲接受组拥有全部固定属性
	assign flag_mac_input = flag_input_accept && !flag_bad_group; // 保持MAC现有握手和II
	assign flag_fault_now = flag_core_fault || (flag_input_accept && flag_bad_group); // 坏输入只在真实接受沿进入故障状态
	assign flag_bad_sequence = flag_idle ? !i_first : i_first; // 空闲需要首组且后续禁止再次首组
	assign flag_bad_group = i_input_fault || flag_bad_sequence || (flag_idle && flag_bad_metadata); // 组输入错误不得进入原核
	assign flag_duplicate_alpha = i_output_mask[0] && i_output_mask[1] && i_tags[15:0] == i_tags[31:16]; // 两条有效路不能共享首个身份
	assign flag_duplicate_beta = i_output_mask[0] && i_output_mask[2] && i_tags[15:0] == i_tags[47:32]; // 跨首末有效路检查身份冲突
	assign flag_duplicate_gamma = i_output_mask[1] && i_output_mask[2] && i_tags[31:16] == i_tags[47:32]; // 后两条有效路保持身份唯一
	assign flag_bad_metadata = i_output_mask == 3'd0 || flag_duplicate_alpha || flag_duplicate_beta || flag_duplicate_gamma; // 无输出或歧义身份拒绝整个任务
	assign flag_pp_output_ready = output_valid_o && i_output_ready; // 原保持槽与真实写端同拍退休
	assign flag_output_accept = output_valid_o && i_output_ready; // 唯一结果消费事件
	assign flag_last_accept = flag_output_accept && reg_remaining == wire_match; // 仅最后有效路解除占有

	//---------------输出信号连线---------------//
	//用户接口TABLE接口
	//用户接口
	//对外端口保持原核输出生存期
	assign o_table_ready = table_ready_o;       // 发布真实装表握手条件
	assign o_table_loaded = table_loaded_o;     // 不伪造原核完整表状态
	assign o_input_ready = input_ready_o;       // 发布唯一任务输入准入

	//用户接口OUTPUT接口
	assign o_output_valid = output_valid_o;     // 数据身份类型同时通过后发布
	assign o_output_data = output_data_o;       // 直接保留原INT16数值不截断
	assign o_output_int16 = output_int16_o;     // 原DPP类型随结果保持
	assign o_output_tag = output_tag_o;         // 原DPP不透明标识随结果保持
	assign o_output_address = output_address_o; // 真实匹配路对应锁存地址

	//用户接口
	assign o_fault = fault_o;                   // 故障阻止后续任务与成功输出
	assign o_busy = busy_o;                     // 完整结果退休前不释放算术owner

	//----------------状态机区域----------------//
	//共同复位异步取消旧任务，释放后按独立转移过程推进
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			state_current <= ST_IDLE;           // 复位归还本地任务状态
		end else begin
			state_current <= state_next;        // 采用组合转移结果
		end
	end

	//故障优先，末输出真实握手才回空闲
	always@(*)begin
		state_next = state_current;             // 无阶段事件保持控制状态
		if(flag_fault_now == 1'b1)begin
			state_next = ST_FAULT;              // 核或占有错误禁止成功退休
		end else begin
			case(state_current)

				//首组接受后选择继续归约或等待结果
				ST_IDLE:begin
					if(flag_input_accept == 1'b1)begin
						if(i_last == 1'b1)begin
							state_next = ST_ACC; // 单组任务已关闭归约
						end else begin
							state_next = ST_GROUP; // 多组任务继续拥有归约
						end
					end else begin
						state_next = ST_IDLE;   // 装表或空拍不建立任务
					end
				end

				//末组接受后停止接收新操作数
				ST_GROUP:begin
					if(flag_input_accept == 1'b1 && i_last == 1'b1)begin
						state_next = ST_ACC;    // 等待最后累加流水完成
					end else begin
						state_next = ST_GROUP;  // 已开启任务持续占有
					end
				end

				//完整累加只能转交一次
				ST_ACC:begin
					if(flag_acc_accept == 1'b1)begin
						state_next = ST_OUTPUT; // 原DPP接管三路结果
					end else begin
						state_next = ST_ACC;    // MAC或DPP等待不能释放
					end
				end

				//最后实际写端接收才允许后继任务
				ST_OUTPUT:begin
					if(flag_last_accept == 1'b1)begin
						state_next = ST_IDLE;   // 全部有效结果已真实退休
					end else begin
						state_next = ST_OUTPUT; // 背压和部分退休都保持占有
					end
				end

				//错误所有权只由共同reset撤销
				ST_FAULT:begin
					state_next = ST_FAULT;      // 禁止故障后复用旧事务
				end

				//非法状态转入故障而非假成功
				default:begin
					state_next = ST_FAULT;      // 状态损坏保持保守占有
				end
			endcase
		end
	end

	//-------------状态任务处理区域-------------//
	//仅首组建立有效路集合，写端真实接受逐路移除
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_remaining <= 3'd0;              // 共同复位取消未退休身份
		end else begin
			case(state_current)

				//空闲接受的首组建立退休责任
				ST_IDLE:begin
					if(flag_first_accept == 1'b1)begin
						reg_remaining <= i_output_mask; // 首组拥有所有输出路
					end
				end

				//只有结果阶段的真实握手消除身份
				ST_OUTPUT:begin
					if(flag_output_accept == 1'b1)begin
						reg_remaining <= reg_remaining & ~wire_match; // 背压期间剩余路不推进
					end
				end

				//归约交接和故障阶段不改变未退休集合
				default:begin
					reg_remaining <= reg_remaining; // 计算完成不能提前解除责任
				end
			endcase
		end
	end

	//-------------主要任务处理区域-------------//
	//两沿释放准入不改原核复位端口
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_release <= 2'b00;               // 断言立即关闭owner准入
		end else begin
			reg_release <= {reg_release[0], 1'b1}; // 最早第三沿可接受外部传输
		end
	end

	//原DPP输出掩码仅由任务首组确定
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_output_mask <= 3'd0;            // 复位不携带旧任务有效路
		end else if(flag_first_accept == 1'b1)begin
			reg_output_mask <= i_output_mask;   // 后续组不改变算术输出数量
		end
	end

	//不透明身份在整个任务生存期冻结
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_tags <= 48'd0;                  // 取消旧身份映射
		end else if(flag_first_accept == 1'b1)begin
			reg_tags <= i_tags;                 // 首组建立固定身份三元组
		end
	end

	//写回地址与首组身份共同冻结
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_addresses <= 96'd0;             // 撤销旧逻辑地址上下文
		end else if(flag_first_accept == 1'b1)begin
			reg_addresses <= i_addresses;       // 后续外部扰动不改变目标
		end
	end

	//前乘数先于完整累加交接锁定
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_pre_multipliers <= 96'd0;       // 清除前比例上下文
		end else if(flag_first_accept == 1'b1)begin
			reg_pre_multipliers <= i_pre_multipliers; // 三路前乘数按首组固定
		end
	end

	//前移位在MAC归约期间保持不变
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_pre_shifts <= 18'd0;            // 复位撤销旧前移位
		end else if(flag_first_accept == 1'b1)begin
			reg_pre_shifts <= i_pre_shifts;     // 原DPP接收同任务固定舍入量
		end
	end

	//共享后乘数不随后续组字段变化
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_post_multiplier <= 32'd0;       // 复位取消后比例属性
		end else if(flag_first_accept == 1'b1)begin
			reg_post_multiplier <= i_post_multiplier; // 激活路径使用首组系数
		end
	end

	//后移位仅首组采样
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_post_shift <= 6'd0;             // 清除上次任务后舍入量
		end else if(flag_first_accept == 1'b1)begin
			reg_post_shift <= i_post_shift;     // 维持本任务量化尺度
		end
	end

	//数值模式先于原DPP batch接受固定
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			flag_activate <= 1'b0;              // 取消旧激活模式
		end else if(flag_first_accept == 1'b1)begin
			flag_activate <= i_activate;        // raw与SiLU路径不接受中途切换
		end
	end

	//--------------模块实例化区域--------------//
	//唯一原MAC计算，全部算术语义沿冻结实现
	road_mac_probe road_mac_probe_Inst (        // 单一三路归约实例
		.i_clk(i_clk),                          // 同域计算时钟不门控
		.i_rstn(i_rstn),                        // 与owner共同取消流水
		.i_input_valid(flag_mac_input),         // 仅合法已接受组进入核
		.i_first(i_first),                      // 原核first仅计一次偏置
		.i_last(i_last),                        // 原核last生成完整终态
		.i_lane_mask(i_lane_mask),              // 输入尾槽沿原掩码禁止乘积
		.i_activation_data(i_activation_data),  // 本拍真实输入操作数
		.i_weight_data(i_weight_data),          // 本拍三路对应权重
		.i_bias_data(i_bias_data),              // 原MAC自行在first采样使用
		.i_result_ready(flag_acc_ready),        // 完整结果仅ACC阶段转交
		.o_input_ready(flag_mac_ready),         // 原核流水准入条件
		.o_result_valid(flag_mac_valid),        // 三路末组终态保持
		.o_result_data(wire_mac_data),          // signed33检查后的INT32三元组
		.o_fault(flag_mac_fault)                // 原核原子末组故障
	);

	//唯一动态后处理，内部原PRE/SiLU/POST队列均不改
	road_dynamic_postprocess road_dynamic_postprocess_Inst ( // 单一动态量化实例
		.i_clk(i_clk),                          // 重定标和SiLU共同工作时钟
		.i_rstn(i_rstn),                        // 共同复位取消原队列
		.i_table_valid(i_table_valid && flag_table_enable), // 表项只能空闲时进入原DPP
		.i_table_addr(i_table_addr),            // 原模型表装载顺序
		.i_table_data(i_table_data),            // 完整有符号表项保留
		.o_table_ready(flag_pp_table_ready),    // 原装表端真实接受状态
		.o_table_loaded(table_loaded_o),        // 原核装满标志不再编码
		.i_input_valid(flag_pp_input),          // 当前任务完整累加持续有效
		.i_accumulators(wire_mac_data),         // 三路MAC结果原样转交
		.i_pre_multipliers(reg_pre_multipliers), // 首组拥有前乘数
		.i_pre_shifts(reg_pre_shifts),          // 首组拥有前移位
		.i_post_multiplier(reg_post_multiplier), // 首组拥有共享后乘数
		.i_post_shift(reg_post_shift),          // 首组拥有共享后移位
		.i_activate(flag_activate),             // 原核raw与SiLU选择保留
		.i_lane_mask(reg_output_mask),          // 原DPP只处理有效输出路
		.i_tags(reg_tags),                      // 不透明身份随数值穿过原队列
		.i_input_fault(1'b0),                   // 输入故障已在owner保持拒绝
		.o_input_ready(flag_pp_ready),          // 原batch预留许可
		.i_output_ready(flag_pp_output_ready),  // 直接使用真实写端退休事件
		.o_output_valid(flag_pp_valid),         // 原保持输出槽无需新增副本
		.o_output_data(output_data_o),          // raw完整INT16或激活符号扩展
		.o_output_tag(output_tag_o),            // 原队列输出不透明身份
		.o_output_int16(output_int16_o),        // 原模式属性供owner复核
		.o_fault(flag_pp_fault),                // 原DPP故障参与共同保持
		.o_queue_count(),                       // 原内部入口计数只供调试
		.o_pending_count(),                     // 原退休队列不由owner复制
		.o_meta_count(),                        // SiLU身份FIFO保持原实现
		.o_pre_busy(),                          // PRE活动由原核管理
		.o_silu_busy(),                         // SiLU流水活动不当完成条件
		.o_post_busy(),                         // POST活动不当释放条件
		.o_pre_accept(),                        // PRE真实握手可在TB层次观察
		.o_silu_accept(),                       // SiLU真实接受用于逐级对拍
		.o_post_accept()                        // POST真实接受由原DPP负责
	);

endmodule
