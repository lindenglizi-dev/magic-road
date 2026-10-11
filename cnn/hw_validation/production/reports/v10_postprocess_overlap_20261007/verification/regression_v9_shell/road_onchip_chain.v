`timescale 1ns / 1ps

////////////////////////////////////English///////////////////////////////////////
// Company:         Erie
// Engineer:        Erie
//
// Create Date:     2026/10/06 00:00:00
// Design Name:     road_onchip_chain
// Module Name:     road_onchip_chain
// Description:     description/road_onchip_chain_Design.pdf
// Simulations:     testbench/vivado/2021.1/road_onchip_chain
//
// Referrences:
// File Format      File Name
// 1.Book           road_onchip_chain.contract.json
//
// Dependencies:
// Module Name      Version
// road_mac_probe   V1.0
// road_round_shift V1.0
// silu_shared_unit V1.0
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
// 设计名称:        road_onchip_chain
// 模块名称:        road_onchip_chain
// 模块说明:        Description/road_onchip_chain_Design.pdf
// 仿真工程:        TestBench/Vivado/2021.1/road_onchip_chain
//
// 参考资料:
// 文件格式         文件名称
// 1.Book           road_onchip_chain.contract.json
//
// 依赖文件:
// 模块名称         版本
// road_mac_probe   V1.0
// road_round_shift V1.0
// silu_shared_unit V1.0
//
// 当前版本:        V1.0
// 修订日期:        2026年10月06日
// 修订历史:
// 时间             版本        修订人            修订内容
// 2026年10月06日   V1.0        Erie              创建文件

module road_onchip_chain
(
	//-----------------全局信号-----------------//
	input i_clk,                                // 百兆串行计算链工作时钟
	input i_rstn,                               // 异步低有效事务取消复位

	//-----------------用户接口-----------------//
	input i_input_valid,                        // MAC输入负载保持有效标志
	input i_first,                              // 当前位置首输入通道组标志
	input i_last,                               // 当前位置末输入通道组标志
	input [7:0]i_lane_mask,                     // 八条输入通道共享使能掩码
	input [63:0]i_activation_data,              // 八个低字节优先有符号激活值
	input [191:0]i_weight_data,                 // 三组低字节优先有符号权重
	input [95:0]i_bias_data,                    // 三个低字优先有符号偏置
	output o_input_ready,                       // 最小链允许接受MAC输入拍
	output o_fault,                             // 复位前保持的计算链故障标志

	//----------------TABLE接口-----------------//
	input i_table_valid,                        // 真实SiLU表项装载有效标志
	input [9:0]i_table_addr,                    // 严格递增SiLU表项地址
	input signed [15:0]i_table_data,            // 有符号Q7.8 SiLU表项
	output o_table_ready,                       // 当前表项装载接收许可
	output o_table_loaded,                      // 完整真实SiLU表已激活
	output o_table_fault,                       // 表装载顺序故障标志

	//--------------CACHE_READ接口-------------//
	input i_cache_read_valid,                   // 缓存读请求保持有效标志
	input [3:0]i_cache_read_addr,               // 十二项输出缓存读取地址
	output o_cache_read_ready,                  // 缓存读请求接收许可
	output o_cache_result_valid,                // 缓存读响应保持有效标志
	output signed [7:0]o_cache_result_data,      // 已提交的有符号INT8特征
	output o_cache_result_fault,                // 越界或未提交地址读故障
	input i_cache_result_ready                  // 下游接受缓存读响应
);

	//---------------配置参数区域---------------//
	//测试量化参数
	localparam signed [31:0]PRE_FACTOR_ALPHA = 32'sd1; // 甲通道SiLU前整数乘数
	localparam signed [31:0]PRE_FACTOR_BETA = 32'sd3; // 乙通道SiLU前整数乘数
	localparam signed [31:0]PRE_FACTOR_GAMMA = 32'sd5; // 丙通道SiLU前整数乘数
	localparam [5:0]PRE_SHIFT_ALPHA = 6'd0;      // 甲通道SiLU前右移指数
	localparam [5:0]PRE_SHIFT_BETA = 6'd2;       // 乙通道SiLU前右移指数
	localparam [5:0]PRE_SHIFT_GAMMA = 6'd4;      // 丙通道SiLU前右移指数
	localparam signed [31:0]POST_FACTOR = 32'sd1; // SiLU后输出比例整数乘数
	localparam [5:0]POST_SHIFT = 6'd4;           // SiLU后输出比例右移指数

	//---------------状态参数区域---------------//
	//串行控制状态
	localparam [3:0]ST_MAC = 4'd0;              // 接收当前位置MAC输入组
	localparam [3:0]ST_PREPARE = 4'd1;          // 选择当前输出通道量化参数
	localparam [3:0]ST_PRE_SEND = 4'd2;         // 向共享舍入核发送前乘积
	localparam [3:0]ST_PRE_WAIT = 4'd3;         // 等待共享舍入核前结果
	localparam [3:0]ST_SILU_SEND = 4'd4;        // 向真实SiLU发送Q7.8输入
	localparam [3:0]ST_SILU_WAIT = 4'd5;        // 等待真实SiLU输出握手
	localparam [3:0]ST_POST_SEND = 4'd6;        // 向共享舍入核发送后乘积
	localparam [3:0]ST_POST_WAIT = 4'd7;        // 等待共享舍入核后结果
	localparam [3:0]ST_COMMIT_ALPHA = 4'd8;     // 原子提交甲通道临时特征
	localparam [3:0]ST_COMMIT_BETA = 4'd9;      // 原子提交乙通道临时特征
	localparam [3:0]ST_COMMIT_GAMMA = 4'd10;    // 原子提交丙通道临时特征
	localparam [3:0]ST_FAULT = 4'd11;           // 取消当前位置且不提交缓存

	//--------------模块实例化信号--------------//
	//MAC实例接口
	wire mac_input_ready;                       // 独立MAC输入接收许可
	wire mac_result_valid;                      // 独立MAC终态有效标志
	wire [95:0]mac_result_data;                 // 独立MAC三路INT32结果
	wire mac_fault;                             // 独立MAC三路原子故障

	//共享舍入实例接口
	wire round_result_valid;                    // 舍入结果有效标志
	wire [15:0]round_result_data;               // 舍入后饱和INT16位型
	wire [15:0]round_result_tag;                // 舍入核返回身份
	wire round_fault;                           // 舍入非法输入故障

	//真实SiLU实例接口
	wire silu_table_ready;                      // SiLU表装载接收许可
	wire silu_input_ready;                      // SiLU推理输入接收许可
	wire silu_output_valid;                     // SiLU推理结果有效标志
	wire signed [15:0]silu_output_data;          // SiLU有符号Q7.8结果
	wire silu_table_loaded;                     // SiLU完整表激活状态
	wire silu_table_fault;                      // SiLU表装载故障状态

	//----------------计数信号------------------//
	//外层位置与输出通道身份
	reg [1:0]cnt_position = 2'd0;               // 当前二乘二空间位置编号
	reg [1:0]cnt_channel = 2'd0;                // 当前三输出通道编号

	//----------------状态机信号----------------//
	//串行链控制状态
	reg [3:0]state_current = ST_MAC;             // 当前串行处理阶段
	reg [3:0]state_next = ST_MAC;                // 下一串行处理阶段

	//----------------寄存器信号----------------//
	//MAC终态保持
	reg signed [31:0]reg_accumulator_alpha = 32'sd0; // 甲输出通道完整累加值
	reg signed [31:0]reg_accumulator_beta = 32'sd0; // 乙输出通道完整累加值
	reg signed [31:0]reg_accumulator_gamma = 32'sd0; // 丙输出通道完整累加值

	//唯一乘法点操作数
	reg signed [31:0]reg_multiplier_value = 32'sd0; // 当前INT32累加或符号扩展SiLU值
	reg signed [31:0]reg_multiplier_factor = 32'sd0; // 当前含零符号位的非负31位乘数
	reg [5:0]reg_round_shift = 6'd0;             // 当前共享舍入右移指数
	reg [15:0]reg_round_tag = 16'd0;             // 当前位置通道与阶段身份
	reg signed [15:0]reg_silu_input = 16'sd0;   // 已完成前量化的Q7.8输入

	//提交前临时特征
	reg signed [7:0]reg_feature_alpha = 8'sd0;   // 当前空间位置甲通道临时特征
	reg signed [7:0]reg_feature_beta = 8'sd0;    // 当前空间位置乙通道临时特征
	reg signed [7:0]reg_feature_gamma = 8'sd0;   // 当前空间位置丙通道临时特征
	reg signed [7:0]reg_feature_cache [0:11];    // 十二项独立读口片上特征缓存
	reg [11:0]reg_cache_valid = 12'd0;           // 十二项缓存已提交有效位
	reg [3:0]reg_write_base = 4'd0;              // 当前位置三个连续写地址基址

	//-----------------标志信号-----------------//
	//握手与故障事件
	wire flag_mac_input_enable;                 // 表可用且控制器接收MAC输入
	wire flag_mac_input_valid;                  // 送入独立MAC的门控有效标志
	wire flag_mac_result_ready;                 // 控制器接受独立MAC终态
	wire flag_mac_result_transfer;              // 独立MAC终态握手事件
	wire flag_mac_input_transfer;               // 独立MAC输入握手事件
	wire flag_table_enable;                     // 无在途计算时允许表装载
	wire flag_table_valid;                      // 送入SiLU的门控表项有效标志
	wire flag_round_input_valid;                // 前后乘积进入共享舍入核
	wire flag_round_failure;                    // 舍入故障或身份错位事件
	wire flag_silu_input_valid;                 // 当前Q7.8输入保持有效
	wire flag_silu_input_transfer;              // SiLU推理输入握手事件
	wire flag_silu_output_ready;                // 外层允许接受SiLU结果
	wire flag_silu_output_transfer;             // SiLU推理输出握手事件
	wire flag_cache_request;                    // 缓存读请求握手事件
	wire flag_cache_response;                   // 缓存读响应握手事件

	//-----------------其他信号-----------------//
	//共享数值路径
	wire signed [63:0]scaled_product;            // 唯一有符号六十四位重定标乘积
	wire signed [15:0]round_signed_data;         // 舍入结果有符号解释
	wire signed [7:0]post_saturated_data;        // SiLU后直接INT8饱和结果
	wire cache_address_legal;                   // 缓存读地址位于零到十一

	//-----------------输出信号-----------------//
	//用户接口
	wire input_ready_o;                         // MAC输入接收许可内部连线
	reg fault_o = 1'b0;                         // 计算或身份故障保持输出

	//TABLE接口
	wire table_ready_o;                         // 表装载接收许可内部连线
	wire table_loaded_o;                        // 完整表激活内部连线
	wire table_fault_o;                         // 表装载故障内部连线

	//CACHE_READ接口
	wire cache_read_ready_o;                    // 一项缓存响应缓冲接收许可
	reg cache_result_valid_o = 1'b0;            // 缓存读响应保持有效代理
	reg signed [7:0]cache_result_data_o = 8'sd0; // 缓存读响应数据代理
	reg cache_result_fault_o = 1'b0;            // 缓存读响应故障代理

	//---------------其他信号连线---------------//
	//MAC输入输出握手
	assign flag_mac_input_enable = (state_current == ST_MAC) & silu_table_loaded & (~silu_table_fault) & (~i_table_valid); // 只在真实表健康时开放MAC输入
	assign flag_mac_input_valid = i_input_valid & flag_mac_input_enable; // 屏蔽非接收阶段的上游有效负载
	assign flag_mac_result_ready = (state_current == ST_MAC) & silu_table_loaded & (~silu_table_fault); // 串行控制器在MAC阶段接受终态
	assign flag_mac_result_transfer = mac_result_valid & flag_mac_result_ready; // 捕获三通道终态握手
	assign flag_mac_input_transfer = flag_mac_input_valid & mac_input_ready; // 捕获真实MAC输入拍

	//表装载只在MAC无在途输入时开放
	assign flag_table_enable = (state_current == ST_MAC) & mac_input_ready; // 防止装载覆盖在途推理访问
	assign flag_table_valid = i_table_valid & flag_table_enable; // 仅向真实SiLU转发合法装载阶段

	//共享舍入与真实SiLU握手
	assign flag_round_input_valid = (state_current == ST_PRE_SEND) | (state_current == ST_POST_SEND); // 前后阶段复用同一舍入核
	assign flag_round_failure = round_fault | (round_result_tag != reg_round_tag); // 拒绝故障或身份错位结果
	assign flag_silu_input_valid = (state_current == ST_SILU_SEND); // 前量化结果保持到SiLU接受
	assign flag_silu_input_transfer = flag_silu_input_valid & silu_input_ready; // 记录SiLU输入真实转移
	assign flag_silu_output_ready = (state_current == ST_SILU_WAIT); // 外层仅在等待阶段消费SiLU结果
	assign flag_silu_output_transfer = silu_output_valid & flag_silu_output_ready; // 记录SiLU输出真实转移

	//唯一有符号乘法点和饱和边界
	assign scaled_product = reg_multiplier_value * reg_multiplier_factor; // 完整保留INT32乘非负INT32结果
	assign round_signed_data = round_result_data; // 将舍入位型解释为有符号INT16
	assign post_saturated_data = (round_signed_data < -16'sd128) ? -8'sd128 : ((round_signed_data > 16'sd127) ? 8'sd127 : round_signed_data[7:0]); // 同一舍入整数直接饱和到INT8

	//缓存独立读响应握手
	assign cache_read_ready_o = (~cache_result_valid_o) | i_cache_result_ready; // 空响应槽或同拍消费时接受请求
	assign flag_cache_request = i_cache_read_valid & cache_read_ready_o; // 缓存读请求真实转移事件
	assign flag_cache_response = cache_result_valid_o & i_cache_result_ready; // 缓存读响应真实转移事件
	assign cache_address_legal = (i_cache_read_addr < 4'd12); // 拒绝十二项之外的读地址

	//---------------输出信号连线---------------//
	//用户接口
	assign input_ready_o = mac_input_ready & flag_mac_input_enable; // 发布门控后的MAC输入许可
	assign o_input_ready = input_ready_o;       // MAC输入接收许可桥接
	assign o_fault = fault_o;                   // 计算链故障保持桥接

	//TABLE接口
	assign table_ready_o = silu_table_ready & flag_table_enable; // 发布门控后的表项接收许可
	assign table_loaded_o = silu_table_loaded;  // 发布真实SiLU完整表状态
	assign table_fault_o = silu_table_fault;    // 发布真实SiLU装载故障
	assign o_table_ready = table_ready_o;       // 表装载接收许可桥接
	assign o_table_loaded = table_loaded_o;     // 完整表激活状态桥接
	assign o_table_fault = table_fault_o;       // 表装载故障状态桥接

	//CACHE_READ接口
	assign o_cache_read_ready = cache_read_ready_o; // 缓存请求接收许可桥接
	assign o_cache_result_valid = cache_result_valid_o; // 缓存响应有效标志桥接
	assign o_cache_result_data = cache_result_data_o; // 缓存响应有符号特征桥接
	assign o_cache_result_fault = cache_result_fault_o; // 缓存响应故障属性桥接

	//-------------输出信号处理区域-------------//
	//计算链故障保持到外部复位
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			fault_o <= 1'b0;                       // 复位清除历史故障
		end else if(silu_table_fault == 1'b1)begin
			fault_o <= 1'b1;                       // 保留真实表装载故障
		end else if((state_current == ST_FAULT) || ((state_current == ST_PRE_WAIT) && round_result_valid && flag_round_failure) || ((state_current == ST_POST_WAIT) && round_result_valid && flag_round_failure))begin
			fault_o <= 1'b1;                       // 保留位置取消或舍入身份故障
		end else begin
			fault_o <= fault_o;                    // 无新故障时保持历史状态
		end
	end

	//缓存响应有效位支持同拍消费并替换
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			cache_result_valid_o <= 1'b0;          // 复位取消未消费读响应
		end else if(flag_cache_request == 1'b1)begin
			cache_result_valid_o <= 1'b1;          // 新请求占用响应保持槽
		end else if(flag_cache_response == 1'b1)begin
			cache_result_valid_o <= 1'b0;          // 已消费响应释放保持槽
		end else begin
			cache_result_valid_o <= cache_result_valid_o; // 背压期间保持响应有效
		end
	end

	//合法且已提交的地址返回缓存数据
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			cache_result_data_o <= 8'sd0;          // 复位清空读响应数据
		end else if(flag_cache_request == 1'b1)begin
			if(cache_address_legal && reg_cache_valid[i_cache_read_addr])begin
				cache_result_data_o <= reg_feature_cache[i_cache_read_addr]; // 读取已提交特征
			end else begin
				cache_result_data_o <= 8'sd0;        // 非法或未提交地址返回确定零值
			end
		end else begin
			cache_result_data_o <= cache_result_data_o; // 无新请求时保持响应数据
		end
	end

	//缓存响应故障限定地址和提交状态
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			cache_result_fault_o <= 1'b0;          // 复位清除读响应故障
		end else if(flag_cache_request == 1'b1)begin
			cache_result_fault_o <= (~cache_address_legal) | (~reg_cache_valid[i_cache_read_addr]); // 标记越界或未提交读取
		end else begin
			cache_result_fault_o <= cache_result_fault_o; // 背压期间保持响应故障
		end
	end

	//----------------状态机区域----------------//
	//当前状态寄存器
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			state_current <= ST_MAC;               // 复位回到MAC输入阶段
		end else begin
			state_current <= state_next;           // 每拍进入已判定下一状态
		end
	end

	//串行计算链下一状态判定
	always@(*)begin
		state_next = state_current;               // 默认保持当前处理阶段
		case(state_current)
			//MAC终态决定继续量化或原子取消
			ST_MAC:begin
				if(flag_mac_result_transfer == 1'b1)begin
					if(mac_fault == 1'b1)begin
						state_next = ST_FAULT;          // 三路MAC故障进入取消阶段
					end else begin
						state_next = ST_PREPARE;        // 正常终态开始甲通道处理
					end
				end else begin
					state_next = ST_MAC;             // 等待末组或下一输入组
				end
			end
			//通道参数准备完成后发送前乘积
			ST_PREPARE:begin
				state_next = ST_PRE_SEND;             // 操作数寄存一拍后送入舍入核
			end
			//共享舍入核在本拍接受前乘积
			ST_PRE_SEND:begin
				state_next = ST_PRE_WAIT;             // 单令牌进入九级舍入流水
			end
			//前舍入结果进入真实SiLU或故障取消
			ST_PRE_WAIT:begin
				if(round_result_valid == 1'b1)begin
					if(flag_round_failure == 1'b1)begin
						state_next = ST_FAULT;          // 非法舍入输入禁止后续写回
					end else begin
						state_next = ST_SILU_SEND;      // 正常Q7.8进入激活阶段
					end
				end else begin
					state_next = ST_PRE_WAIT;        // 等待共享舍入结果有效
				end
			end
			//SiLU输入保持到真实握手
			ST_SILU_SEND:begin
				if(flag_silu_input_transfer == 1'b1)begin
					state_next = ST_SILU_WAIT;       // 输入已归真实SiLU所有
				end else begin
					state_next = ST_SILU_SEND;       // SiLU未就绪时保持输入阶段
				end
			end
			//无tag SiLU由外层单上下文维持身份
			ST_SILU_WAIT:begin
				if(flag_silu_output_transfer == 1'b1)begin
					state_next = ST_POST_SEND;       // SiLU结果乘后比例并复用舍入核
				end else begin
					state_next = ST_SILU_WAIT;       // 等待真实SiLU结果握手
				end
			end
			//共享舍入核在本拍接受后乘积
			ST_POST_SEND:begin
				state_next = ST_POST_WAIT;            // 单令牌再次进入九级舍入流水
			end
			//后舍入结果暂存而不立即写缓存
			ST_POST_WAIT:begin
				if(round_result_valid == 1'b1)begin
					if(flag_round_failure == 1'b1)begin
						state_next = ST_FAULT;          // 身份或数值故障取消当前位置
					end else if(cnt_channel == 2'd2)begin
						state_next = ST_COMMIT_ALPHA;   // 三通道齐备后才开始提交
					end else begin
						state_next = ST_PREPARE;        // 选择下一输出通道
					end
				end else begin
					state_next = ST_POST_WAIT;       // 等待共享舍入后结果
				end
			end
			//三项提交阶段已无可失败运算
			ST_COMMIT_ALPHA:begin
				state_next = ST_COMMIT_BETA;          // 提交甲后继续提交乙
			end
			//第二项提交保持位置原子完成边界
			ST_COMMIT_BETA:begin
				state_next = ST_COMMIT_GAMMA;         // 提交乙后继续提交丙
			end
			//末项提交后开放下一位置MAC输入
			ST_COMMIT_GAMMA:begin
				state_next = ST_MAC;                  // 三项缓存写入全部完成
			end
			//故障位置不写缓存并前进位置身份
			ST_FAULT:begin
				state_next = ST_MAC;                  // 一拍取消后恢复接收
			end
			//非法状态安全返回空闲输入阶段
			default:begin
				state_next = ST_MAC;                  // 状态损坏时不触发缓存提交
			end
		endcase
	end

	//-------------主要任务处理区域-------------//
	//位置编号只在完整提交或原子取消后推进
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			cnt_position <= 2'd0;                  // 复位从空间位置零开始
		end else if((state_current == ST_COMMIT_GAMMA) || (state_current == ST_FAULT))begin
			cnt_position <= cnt_position + 2'd1;   // 四个空间位置自然回绕
		end else begin
			cnt_position <= cnt_position;          // 位置处理期间保持身份
		end
	end

	//输出通道在正常MAC终态和逐通道结束时更新
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			cnt_channel <= 2'd0;                   // 复位选择甲输出通道
		end else if(flag_mac_result_transfer == 1'b1)begin
			cnt_channel <= 2'd0;                   // 每个位置从甲通道开始
		end else if((state_current == ST_POST_WAIT) && round_result_valid && (~flag_round_failure) && (cnt_channel != 2'd2))begin
			cnt_channel <= cnt_channel + 2'd1;     // 完成一个正常通道后选择下一路
		end else begin
			cnt_channel <= cnt_channel;            // 其余阶段保持通道身份
		end
	end

	//捕获甲输出MAC终态
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_accumulator_alpha <= 32'sd0;       // 复位清除甲累加保持
		end else if(flag_mac_result_transfer == 1'b1)begin
			reg_accumulator_alpha <= mac_result_data[31:0]; // 保存甲通道完整INT32结果
		end else begin
			reg_accumulator_alpha <= reg_accumulator_alpha; // 非终态周期保持甲结果
		end
	end

	//捕获乙输出MAC终态
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_accumulator_beta <= 32'sd0;        // 复位清除乙累加保持
		end else if(flag_mac_result_transfer == 1'b1)begin
			reg_accumulator_beta <= mac_result_data[63:32]; // 保存乙通道完整INT32结果
		end else begin
			reg_accumulator_beta <= reg_accumulator_beta; // 非终态周期保持乙结果
		end
	end

	//捕获丙输出MAC终态
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_accumulator_gamma <= 32'sd0;       // 复位清除丙累加保持
		end else if(flag_mac_result_transfer == 1'b1)begin
			reg_accumulator_gamma <= mac_result_data[95:64]; // 保存丙通道完整INT32结果
		end else begin
			reg_accumulator_gamma <= reg_accumulator_gamma; // 非终态周期保持丙结果
		end
	end

	//前量化选择当前通道累加值，后量化选择真实SiLU输出
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_multiplier_value <= 32'sd0;        // 复位清除共享乘法原值
		end else if(state_current == ST_PREPARE)begin
			case(cnt_channel)
				//甲通道选择
				2'd0:begin
					reg_multiplier_value <= reg_accumulator_alpha; // 选择甲通道完整INT32累加值
				end
				//乙通道选择
				2'd1:begin
					reg_multiplier_value <= reg_accumulator_beta; // 选择乙通道完整INT32累加值
				end
				//丙通道及保护选择
				default:begin
					reg_multiplier_value <= reg_accumulator_gamma; // 选择丙通道完整INT32累加值
				end
			endcase
		end else if(flag_silu_output_transfer == 1'b1)begin
			reg_multiplier_value <= {{16{silu_output_data[15]}}, silu_output_data}; // 符号扩展真实SiLU结果到INT32
		end else begin
			reg_multiplier_value <= reg_multiplier_value; // 非装载阶段保持乘法原值
		end
	end

	//同一乘法点按阶段选择测试比例乘数
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_multiplier_factor <= 32'sd0;       // 复位清除共享比例乘数
		end else if(state_current == ST_PREPARE)begin
			case(cnt_channel)
				//甲通道前比例
				2'd0:begin
					reg_multiplier_factor <= PRE_FACTOR_ALPHA; // 选择甲通道非负整数乘数
				end
				//乙通道前比例
				2'd1:begin
					reg_multiplier_factor <= PRE_FACTOR_BETA; // 选择乙通道非负整数乘数
				end
				//丙通道前比例
				default:begin
					reg_multiplier_factor <= PRE_FACTOR_GAMMA; // 选择丙通道非负整数乘数
				end
			endcase
		end else if(flag_silu_output_transfer == 1'b1)begin
			reg_multiplier_factor <= POST_FACTOR;   // 选择统一SiLU后非负整数乘数
		end else begin
			reg_multiplier_factor <= reg_multiplier_factor; // 非装载阶段保持比例乘数
		end
	end

	//共享舍入指数区分前后量化阶段
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_round_shift <= 6'd0;               // 复位清除右移指数
		end else if(state_current == ST_PREPARE)begin
			case(cnt_channel)
				//甲通道前右移
				2'd0:begin
					reg_round_shift <= PRE_SHIFT_ALPHA; // 甲通道保持原整数尺度
				end
				//乙通道前右移
				2'd1:begin
					reg_round_shift <= PRE_SHIFT_BETA; // 乙通道除以四并最近偶数
				end
				//丙通道前右移
				default:begin
					reg_round_shift <= PRE_SHIFT_GAMMA; // 丙通道除以十六并最近偶数
				end
			endcase
		end else if(flag_silu_output_transfer == 1'b1)begin
			reg_round_shift <= POST_SHIFT;          // SiLU后统一除以十六
		end else begin
			reg_round_shift <= reg_round_shift;     // 舍入在途时保持指数
		end
	end

	//round真实tag携带位置通道和前后阶段
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_round_tag <= 16'd0;                 // 复位清除舍入身份
		end else if(state_current == ST_PREPARE)begin
			reg_round_tag <= {11'd0, 1'b0, cnt_position, cnt_channel}; // 标记前量化位置和通道
		end else if(flag_silu_output_transfer == 1'b1)begin
			reg_round_tag <= {11'd0, 1'b1, cnt_position, cnt_channel}; // 标记后量化位置和通道
		end else begin
			reg_round_tag <= reg_round_tag;         // 流水等待期间保持期望身份
		end
	end

	//前舍入结果保持为真实SiLU输入
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_silu_input <= 16'sd0;               // 复位清除SiLU输入保持
		end else if((state_current == ST_PRE_WAIT) && round_result_valid && (~flag_round_failure))begin
			reg_silu_input <= round_signed_data;    // 保存前量化Q7.8整数
		end else begin
			reg_silu_input <= reg_silu_input;       // SiLU接受前保持负载稳定
		end
	end

	//甲通道后量化结果暂存
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_feature_alpha <= 8'sd0;             // 复位清除甲临时特征
		end else if((state_current == ST_POST_WAIT) && round_result_valid && (~flag_round_failure) && (cnt_channel == 2'd0))begin
			reg_feature_alpha <= post_saturated_data; // 暂存甲通道INT8特征
		end else begin
			reg_feature_alpha <= reg_feature_alpha; // 提交前保持甲临时特征
		end
	end

	//乙通道后量化结果暂存
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_feature_beta <= 8'sd0;              // 复位清除乙临时特征
		end else if((state_current == ST_POST_WAIT) && round_result_valid && (~flag_round_failure) && (cnt_channel == 2'd1))begin
			reg_feature_beta <= post_saturated_data; // 暂存乙通道INT8特征
		end else begin
			reg_feature_beta <= reg_feature_beta;   // 提交前保持乙临时特征
		end
	end

	//丙通道后量化结果暂存
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_feature_gamma <= 8'sd0;             // 复位清除丙临时特征
		end else if((state_current == ST_POST_WAIT) && round_result_valid && (~flag_round_failure) && (cnt_channel == 2'd2))begin
			reg_feature_gamma <= post_saturated_data; // 暂存丙通道INT8特征
		end else begin
			reg_feature_gamma <= reg_feature_gamma; // 提交前保持丙临时特征
		end
	end

	//缓存实体仅在三路均成功后依次写入
	always@(posedge i_clk)begin
		if(state_current == ST_COMMIT_ALPHA)begin
			reg_feature_cache[reg_write_base] <= reg_feature_alpha; // 提交当前位置甲特征
		end else if(state_current == ST_COMMIT_BETA)begin
			reg_feature_cache[reg_write_base + 4'd1] <= reg_feature_beta; // 提交当前位置乙特征
		end else if(state_current == ST_COMMIT_GAMMA)begin
			reg_feature_cache[reg_write_base + 4'd2] <= reg_feature_gamma; // 提交当前位置丙特征
		end
	end

	//缓存有效位在新位置首拍先失效，提交后逐项生效
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_cache_valid <= 12'd0;               // 复位使全部缓存项不可读
		end else if(flag_mac_input_transfer && i_first)begin
			case(reg_write_base)
				//位置零有效位失效
				4'd0:begin
					reg_cache_valid <= reg_cache_valid & 12'hff8; // 清除地址零到二有效位
				end
				//位置一有效位失效
				4'd3:begin
					reg_cache_valid <= reg_cache_valid & 12'hfc7; // 清除地址三到五有效位
				end
				//位置二有效位失效
				4'd6:begin
					reg_cache_valid <= reg_cache_valid & 12'he3f; // 清除地址六到八有效位
				end
				//位置三有效位失效
				default:begin
					reg_cache_valid <= reg_cache_valid & 12'h1ff; // 清除地址九到十一有效位
				end
			endcase
		end else if(state_current == ST_COMMIT_GAMMA)begin
			case(reg_write_base)
				//位置零三通道同时发布
				4'd0:begin
					reg_cache_valid <= reg_cache_valid | 12'h007; // 地址零到二完整可见
				end
				//位置一三通道同时发布
				4'd3:begin
					reg_cache_valid <= reg_cache_valid | 12'h038; // 地址三到五完整可见
				end
				//位置二三通道同时发布
				4'd6:begin
					reg_cache_valid <= reg_cache_valid | 12'h1c0; // 地址六到八完整可见
				end
				//位置三三通道同时发布
				default:begin
					reg_cache_valid <= reg_cache_valid | 12'he00; // 地址九到十一完整可见
				end
			endcase
		end else begin
			reg_cache_valid <= reg_cache_valid;     // 无事务事件时保持有效位
		end
	end

	//连续三个缓存地址基址随位置完成或取消推进
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_write_base <= 4'd0;                 // 复位从缓存地址零开始
		end else if((state_current == ST_COMMIT_GAMMA) || (state_current == ST_FAULT))begin
			case(reg_write_base)
				//位置零转位置一
				4'd0:begin
					reg_write_base <= 4'd3;          // 下一位置基址为三
				end
				//位置一转位置二
				4'd3:begin
					reg_write_base <= 4'd6;          // 下一位置基址为六
				end
				//位置二转位置三
				4'd6:begin
					reg_write_base <= 4'd9;          // 下一位置基址为九
				end
				//位置三回绕位置零
				default:begin
					reg_write_base <= 4'd0;          // 四位置结束后回绕缓存首址
				end
			endcase
		end else begin
			reg_write_base <= reg_write_base;       // 当前位置处理期间保持基址
		end
	end

	//--------------模块实例化区域--------------//
	//三输出八lane有符号MAC候选核
	road_mac_probe road_mac_probe_Inst_chain(
		.i_clk(i_clk),                           // 共享百兆工作时钟
		.i_rstn(i_rstn),                         // 共享异步低有效复位
		.i_input_valid(flag_mac_input_valid),    // 门控后的MAC输入有效标志
		.i_first(i_first),                       // 透传当前位置首组属性
		.i_last(i_last),                         // 透传当前位置末组属性
		.i_lane_mask(i_lane_mask),               // 透传八lane有效掩码
		.i_activation_data(i_activation_data),   // 透传八个有符号激活值
		.i_weight_data(i_weight_data),           // 透传三组有符号权重
		.i_bias_data(i_bias_data),               // 透传三通道首组偏置
		.i_result_ready(flag_mac_result_ready),  // 串行控制器终态接收许可
		.o_input_ready(mac_input_ready),         // MAC自身单在途输入许可
		.o_result_valid(mac_result_valid),       // MAC终态保持有效标志
		.o_result_data(mac_result_data),         // 三通道完整INT32累加值
		.o_fault(mac_fault)                      // 三通道原子越界故障
	);

	//前后重定标共同复用九级最近偶数舍入核
	road_round_shift road_round_shift_Inst_chain(
		.i_clk(i_clk),                           // 共享百兆工作时钟
		.i_rstn(i_rstn),                         // 共享异步低有效复位
		.i_advance(1'b1),                        // 串行单令牌始终共同推进
		.i_input_valid(flag_round_input_valid),  // 前后乘积发送拍有效标志
		.i_product(scaled_product),              // 唯一有符号六十四位乘积
		.i_shift(reg_round_shift),               // 当前前后阶段右移指数
		.i_tag(reg_round_tag),                   // 真实舍入tag携带外层身份
		.o_result_valid(round_result_valid),     // 舍入结果有效标志
		.o_result_data(round_result_data),       // 饱和INT16舍入结果
		.o_result_tag(round_result_tag),         // 返回位置通道阶段身份
		.o_fault(round_fault)                    // 非法移位或最小乘积故障
	);

	//官方PH1P模型承载真实一千零二十四项SiLU表
	silu_shared_unit silu_shared_unit_Inst_chain(
		.i_clk(i_clk),                           // 共享百兆工作时钟
		.i_rstn(i_rstn),                         // 共享异步低有效复位
		.i_table_valid(flag_table_valid),        // 空闲阶段门控表项有效标志
		.i_table_addr(i_table_addr),             // 透传严格递增表地址
		.i_table_data(i_table_data),             // 透传真实有符号Q7.8表项
		.i_input_valid(flag_silu_input_valid),   // 当前通道Q7.8输入有效标志
		.i_input_data(reg_silu_input),           // 前量化饱和INT16输入
		.i_output_ready(flag_silu_output_ready), // 外层单上下文结果许可
		.o_table_ready(silu_table_ready),        // SiLU装载协议接收许可
		.o_input_ready(silu_input_ready),        // SiLU推理协议接收许可
		.o_output_valid(silu_output_valid),      // SiLU结果保持有效标志
		.o_output_data(silu_output_data),        // 真实表或尾部旁路结果
		.o_table_loaded(silu_table_loaded),      // 完整真实表激活状态
		.o_table_fault(silu_table_fault)         // 装载地址顺序故障
	);

endmodule
