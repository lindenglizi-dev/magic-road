`timescale 1ns / 1ps

////////////////////////////////////English///////////////////////////////////////
// Company:         Erie
// Engineer:        Erie
//
// Create Date:     2026/10/07 00:00:00
// Design Name:     road_mac_probe
// Module Name:     road_mac_probe
// Description:     Three-output signed INT8 streaming MAC candidate
// Simulations:     ModelSim 2020.4
//
// Referrences:
// File Format      File Name
// 1.Markdown       road_mac_probe_spec.md
//
// Dependencies:
// Module Name      Version
//
// Version:         V1.0
// Revision Date:   2026/10/07 00:00:00
// History:
// Time             Version     Revised by        Contents
// 2026/10/07       V1.0        Erie              Create streaming candidate.
///////////////////////////////////Chinese////////////////////////////////////////
// 版权归属:        Erie
// 开发人员:        Erie
//
// 创建日期:        2026年10月07日
// 设计名称:        road_mac_probe
// 模块名称:        road_mac_probe
// 模块说明:        三输出有符号INT8流式乘加候选
// 仿真工程:        ModelSim 2020.4
//
// 参考资料:
// 文件格式         文件名称
// 1.Markdown       road_mac_probe_spec.md
//
// 依赖文件:
// 模块名称         版本
//
// 当前版本:        V1.0
// 修订日期:        2026年10月07日
// 修订历史:
// 时间             版本        修订人            修订内容
// 2026年10月07日   V1.0        Erie              创建流式候选

module road_mac_probe
(
	//-----------------全局信号-----------------//
	input i_clk,                                // 百兆工作时钟
	input i_rstn,                               // 异步低有效复位

	//-----------------用户接口-----------------//
	input i_input_valid,                        // 输入负载保持有效标志
	input i_first,                              // 当前组以偏置替代历史累加值
	input i_last,                               // 当前组结束本次归约序列
	input [7:0]i_lane_mask,                     // 八条输入通道共享使能掩码
	input [63:0]i_activation_data,              // 八个低字节优先有符号激活值
	input [191:0]i_weight_data,                 // 三组八通道低字节优先权重
	input [95:0]i_bias_data,                    // 三个低字优先有符号偏置
	input i_result_ready,                       // 下游允许接受保持型终态
	output o_input_ready,                       // 当前序列允许接受输入组
	output o_result_valid,                      // 结果负载保持有效标志
	output [95:0]o_result_data,                 // 三个低字优先INT32结果
	output o_fault                              // 任一路末组INT32越界标志
);

	//----------------寄存器信号----------------//
	//输入握手拥有的负载与属性
	reg [63:0]reg_activation_front;             // A0锁存八通道激活负载
	reg [191:0]reg_weight_front;                // A0锁存三组八通道权重
	reg [95:0]reg_bias_front;                   // A0锁存三路偏置
	reg [7:0]reg_mask_front;                    // A0锁存共享lane掩码
	reg flag_front_valid;                       // A0负载有效标志
	reg flag_first_front;                       // A0首组替代属性
	reg flag_last_front;                        // A0末组属性

	//A1三输出二十四路乘积
	reg signed [15:0]reg_product_alpha_first;   // 甲输出首通道乘积
	reg signed [15:0]reg_product_alpha_second;  // 甲输出次通道乘积
	reg signed [15:0]reg_product_alpha_third;   // 甲输出第三通道乘积
	reg signed [15:0]reg_product_alpha_fourth;  // 甲输出第四通道乘积
	reg signed [15:0]reg_product_alpha_fifth;   // 甲输出第五通道乘积
	reg signed [15:0]reg_product_alpha_sixth;   // 甲输出第六通道乘积
	reg signed [15:0]reg_product_alpha_seventh; // 甲输出第七通道乘积
	reg signed [15:0]reg_product_alpha_eighth;  // 甲输出末通道乘积
	reg signed [15:0]reg_product_beta_first;    // 乙输出首通道乘积
	reg signed [15:0]reg_product_beta_second;   // 乙输出次通道乘积
	reg signed [15:0]reg_product_beta_third;    // 乙输出第三通道乘积
	reg signed [15:0]reg_product_beta_fourth;   // 乙输出第四通道乘积
	reg signed [15:0]reg_product_beta_fifth;    // 乙输出第五通道乘积
	reg signed [15:0]reg_product_beta_sixth;    // 乙输出第六通道乘积
	reg signed [15:0]reg_product_beta_seventh;  // 乙输出第七通道乘积
	reg signed [15:0]reg_product_beta_eighth;   // 乙输出末通道乘积
	reg signed [15:0]reg_product_gamma_first;   // 丙输出首通道乘积
	reg signed [15:0]reg_product_gamma_second;  // 丙输出次通道乘积
	reg signed [15:0]reg_product_gamma_third;   // 丙输出第三通道乘积
	reg signed [15:0]reg_product_gamma_fourth;  // 丙输出第四通道乘积
	reg signed [15:0]reg_product_gamma_fifth;   // 丙输出第五通道乘积
	reg signed [15:0]reg_product_gamma_sixth;   // 丙输出第六通道乘积
	reg signed [15:0]reg_product_gamma_seventh; // 丙输出第七通道乘积
	reg signed [15:0]reg_product_gamma_eighth;  // 丙输出末通道乘积
	reg [95:0]reg_bias_product;                 // A1对齐三路偏置
	reg flag_product_valid;                     // A1乘积有效标志
	reg flag_first_product;                     // A1首组替代属性
	reg flag_last_product;                      // A1末组属性

	//A2十二路相邻对和
	reg signed [16:0]reg_pair_alpha_first;      // 甲输出首对和
	reg signed [16:0]reg_pair_alpha_second;     // 甲输出次对和
	reg signed [16:0]reg_pair_alpha_third;      // 甲输出第三对和
	reg signed [16:0]reg_pair_alpha_fourth;     // 甲输出末对和
	reg signed [16:0]reg_pair_beta_first;       // 乙输出首对和
	reg signed [16:0]reg_pair_beta_second;      // 乙输出次对和
	reg signed [16:0]reg_pair_beta_third;       // 乙输出第三对和
	reg signed [16:0]reg_pair_beta_fourth;      // 乙输出末对和
	reg signed [16:0]reg_pair_gamma_first;      // 丙输出首对和
	reg signed [16:0]reg_pair_gamma_second;     // 丙输出次对和
	reg signed [16:0]reg_pair_gamma_third;      // 丙输出第三对和
	reg signed [16:0]reg_pair_gamma_fourth;     // 丙输出末对和
	reg [95:0]reg_bias_pair;                    // A2对齐三路偏置
	reg flag_pair_valid;                        // A2相邻对和有效标志
	reg flag_first_pair;                        // A2首组替代属性
	reg flag_last_pair;                         // A2末组属性

	//A3六路四项和
	reg signed [17:0]reg_quad_alpha_first;      // 甲输出前四项和
	reg signed [17:0]reg_quad_alpha_second;     // 甲输出后四项和
	reg signed [17:0]reg_quad_beta_first;       // 乙输出前四项和
	reg signed [17:0]reg_quad_beta_second;      // 乙输出后四项和
	reg signed [17:0]reg_quad_gamma_first;      // 丙输出前四项和
	reg signed [17:0]reg_quad_gamma_second;     // 丙输出后四项和
	reg [95:0]reg_bias_quad;                    // A3对齐三路偏置
	reg flag_quad_valid;                        // A3四项和有效标志
	reg flag_first_quad;                        // A3首组替代属性
	reg flag_last_quad;                         // A3末组属性

	//A4三路八项点积
	reg signed [18:0]reg_dot_alpha;             // A4甲输出八项点积
	reg signed [18:0]reg_dot_beta;              // A4乙输出八项点积
	reg signed [18:0]reg_dot_gamma;             // A4丙输出八项点积
	reg [95:0]reg_bias_dot;                     // A4对齐三路偏置
	reg flag_dot_valid;                         // A4点积有效标志
	reg flag_first_dot;                         // A4首组替代属性
	reg flag_last_dot;                          // A4末组属性

	//A5三路反馈累加与候选观测
	reg signed [32:0]reg_accumulator_alpha;     // 甲输出signed33历史累加值
	reg signed [32:0]reg_accumulator_beta;      // 乙输出signed33历史累加值
	reg signed [32:0]reg_accumulator_gamma;     // 丙输出signed33历史累加值
	reg signed [33:0]reg_candidate_alpha;       // A5甲输出signed34候选
	reg signed [33:0]reg_candidate_beta;        // A5乙输出signed34候选
	reg signed [33:0]reg_candidate_gamma;       // A5丙输出signed34候选
	reg flag_candidate_valid;                   // A5候选有效标志
	reg flag_candidate_last;                    // A5候选属于末组
	reg flag_candidate_fault;                   // A5末组任一路INT32越界

	//A5安全终态到A6保持输出
	reg flag_final_valid_stage0;                // A5末组终态有效
	reg [95:0]reg_final_data_stage0;            // A5故障安全终态负载
	reg flag_final_fault_stage0;                // A5终态故障属性

	//-----------------其他信号-----------------//
	//握手与候选加法组合量
	wire flag_input_accept;                     // 输入ready与valid同时成立事件
	wire flag_result_accept;                    // 输出ready与valid同时成立事件
	wire signed [32:0]base_alpha;               // 甲输出A5累加基值
	wire signed [32:0]base_beta;                // 乙输出A5累加基值
	wire signed [32:0]base_gamma;               // 丙输出A5累加基值
	wire signed [32:0]dot_alpha_wide;           // 甲输出点积符号扩展值
	wire signed [32:0]dot_beta_wide;            // 乙输出点积符号扩展值
	wire signed [32:0]dot_gamma_wide;           // 丙输出点积符号扩展值
	wire signed [33:0]candidate_alpha_sum;      // 甲输出完整候选加法结果
	wire signed [33:0]candidate_beta_sum;       // 乙输出完整候选加法结果
	wire signed [33:0]candidate_gamma_sum;      // 丙输出完整候选加法结果
	wire flag_overflow_alpha;                   // 甲末组候选超出INT32
	wire flag_overflow_beta;                    // 乙末组候选超出INT32
	wire flag_overflow_gamma;                   // 丙末组候选超出INT32
	wire flag_overflow_any;                     // 任一路末组候选超出INT32

	//-----------------输出信号-----------------//
	//保持型用户输出寄存器
	reg input_ready_o;                          // last后到结果握手前关闭输入
	reg result_valid_o;                         // 背压期间保持结果有效
	reg [95:0]result_data_o;                    // 背压期间保持三路结果
	reg fault_o;                                // 背压期间保持故障属性

	//---------------其他信号连线---------------//
	//握手事件与A5真实宽度加法
	assign flag_input_accept = i_input_valid & input_ready_o; // 只接受ready期间的输入负载
	assign flag_result_accept = result_valid_o & i_result_ready; // 只在双方许可时释放终态
	assign base_alpha = flag_first_dot ? {reg_bias_dot[31], reg_bias_dot[31:0]} : reg_accumulator_alpha; // first替代甲历史值
	assign base_beta = flag_first_dot ? {reg_bias_dot[63], reg_bias_dot[63:32]} : reg_accumulator_beta; // first替代乙历史值
	assign base_gamma = flag_first_dot ? {reg_bias_dot[95], reg_bias_dot[95:64]} : reg_accumulator_gamma; // first替代丙历史值
	assign dot_alpha_wide = {{14{reg_dot_alpha[18]}}, reg_dot_alpha}; // 甲点积扩展为signed33
	assign dot_beta_wide = {{14{reg_dot_beta[18]}}, reg_dot_beta}; // 乙点积扩展为signed33
	assign dot_gamma_wide = {{14{reg_dot_gamma[18]}}, reg_dot_gamma}; // 丙点积扩展为signed33
	assign candidate_alpha_sum = {base_alpha[32], base_alpha} + {dot_alpha_wide[32], dot_alpha_wide}; // 甲候选保留signed34进位
	assign candidate_beta_sum = {base_beta[32], base_beta} + {dot_beta_wide[32], dot_beta_wide}; // 乙候选保留signed34进位
	assign candidate_gamma_sum = {base_gamma[32], base_gamma} + {dot_gamma_wide[32], dot_gamma_wide}; // 丙候选保留signed34进位
	assign flag_overflow_alpha = (candidate_alpha_sum[33] ^ candidate_alpha_sum[31]) | (candidate_alpha_sum[32] ^ candidate_alpha_sum[31]); // 甲候选INT32符号扩展检查
	assign flag_overflow_beta = (candidate_beta_sum[33] ^ candidate_beta_sum[31]) | (candidate_beta_sum[32] ^ candidate_beta_sum[31]); // 乙候选INT32符号扩展检查
	assign flag_overflow_gamma = (candidate_gamma_sum[33] ^ candidate_gamma_sum[31]) | (candidate_gamma_sum[32] ^ candidate_gamma_sum[31]); // 丙候选INT32符号扩展检查
	assign flag_overflow_any = flag_overflow_alpha | flag_overflow_beta | flag_overflow_gamma; // 汇总末组原子故障条件

	//---------------输出信号连线---------------//
	//用户接口寄存器桥接
	assign o_input_ready = input_ready_o;       // 输出输入许可状态
	assign o_result_valid = result_valid_o;     // 输出保持型有效状态
	assign o_result_data = result_data_o;       // 输出三路故障安全结果
	assign o_fault = fault_o;                   // 输出原子越界属性

	//-------------输出信号处理区域-------------//
	//last接受后关闭输入，终态握手后重开
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			input_ready_o <= 1'b1;              // 保持参考核复位后ready为一
		end else if(flag_input_accept & i_last)begin
			input_ready_o <= 1'b0;              // last进入流水后禁止下一任务
		end else if(flag_result_accept)begin
			input_ready_o <= 1'b1;              // 终态被接受后恢复输入许可
		end else begin
			input_ready_o <= input_ready_o;      // 其余周期保持序列占用状态
		end
	end

	//A6发布并在背压期间保持valid
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			result_valid_o <= 1'b0;             // 异步复位取消待收终态
		end else begin
			result_valid_o <= (result_valid_o & ~i_result_ready) | flag_final_valid_stage0; // 发布或保持唯一终态
		end
	end

	//A6只在发布事件更新结果负载
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			result_data_o <= 96'd0;             // 异步复位清空可见结果
		end else if(flag_final_valid_stage0)begin
			result_data_o <= reg_final_data_stage0; // 锁存末组正常值或三路零值
		end else begin
			result_data_o <= result_data_o;     // 背压或空闲期间保持负载
		end
	end

	//A6只在发布事件更新故障属性
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			fault_o <= 1'b0;                    // 异步复位清除外部故障
		end else if(flag_final_valid_stage0)begin
			fault_o <= flag_final_fault_stage0; // 锁存与结果同拍的故障属性
		end else begin
			fault_o <= fault_o;                 // 背压期间保持故障属性
		end
	end

	//-------------主要任务处理区域-------------//
	//A0只锁存真实握手负载
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_activation_front <= 64'd0;
			reg_weight_front <= 192'd0;
			reg_bias_front <= 96'd0;
			reg_mask_front <= 8'd0;
			flag_front_valid <= 1'b0;
			flag_first_front <= 1'b0;
			flag_last_front <= 1'b0;
		end else if(flag_input_accept)begin
			reg_activation_front <= i_activation_data;
			reg_weight_front <= i_weight_data;
			reg_bias_front <= i_bias_data;
			reg_mask_front <= i_lane_mask;
			flag_front_valid <= 1'b1;
			flag_first_front <= i_first;
			flag_last_front <= i_last;
		end else begin
			reg_activation_front <= 64'd0;
			reg_weight_front <= 192'd0;
			reg_bias_front <= 96'd0;
			reg_mask_front <= 8'd0;
			flag_front_valid <= 1'b0;
			flag_first_front <= 1'b0;
			flag_last_front <= 1'b0;
		end
	end

	//A1计算三输出二十四路有符号乘积并传递属性
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_product_alpha_first <= 16'sd0;
			reg_product_alpha_second <= 16'sd0;
			reg_product_alpha_third <= 16'sd0;
			reg_product_alpha_fourth <= 16'sd0;
			reg_product_alpha_fifth <= 16'sd0;
			reg_product_alpha_sixth <= 16'sd0;
			reg_product_alpha_seventh <= 16'sd0;
			reg_product_alpha_eighth <= 16'sd0;
			reg_product_beta_first <= 16'sd0;
			reg_product_beta_second <= 16'sd0;
			reg_product_beta_third <= 16'sd0;
			reg_product_beta_fourth <= 16'sd0;
			reg_product_beta_fifth <= 16'sd0;
			reg_product_beta_sixth <= 16'sd0;
			reg_product_beta_seventh <= 16'sd0;
			reg_product_beta_eighth <= 16'sd0;
			reg_product_gamma_first <= 16'sd0;
			reg_product_gamma_second <= 16'sd0;
			reg_product_gamma_third <= 16'sd0;
			reg_product_gamma_fourth <= 16'sd0;
			reg_product_gamma_fifth <= 16'sd0;
			reg_product_gamma_sixth <= 16'sd0;
			reg_product_gamma_seventh <= 16'sd0;
			reg_product_gamma_eighth <= 16'sd0;
			reg_bias_product <= 96'd0;
			flag_product_valid <= 1'b0;
			flag_first_product <= 1'b0;
			flag_last_product <= 1'b0;
		end else begin
			reg_product_alpha_first <= reg_mask_front[0] ? $signed(reg_activation_front[7:0]) * $signed(reg_weight_front[7:0]) : 16'sd0;
			reg_product_alpha_second <= reg_mask_front[1] ? $signed(reg_activation_front[15:8]) * $signed(reg_weight_front[15:8]) : 16'sd0;
			reg_product_alpha_third <= reg_mask_front[2] ? $signed(reg_activation_front[23:16]) * $signed(reg_weight_front[23:16]) : 16'sd0;
			reg_product_alpha_fourth <= reg_mask_front[3] ? $signed(reg_activation_front[31:24]) * $signed(reg_weight_front[31:24]) : 16'sd0;
			reg_product_alpha_fifth <= reg_mask_front[4] ? $signed(reg_activation_front[39:32]) * $signed(reg_weight_front[39:32]) : 16'sd0;
			reg_product_alpha_sixth <= reg_mask_front[5] ? $signed(reg_activation_front[47:40]) * $signed(reg_weight_front[47:40]) : 16'sd0;
			reg_product_alpha_seventh <= reg_mask_front[6] ? $signed(reg_activation_front[55:48]) * $signed(reg_weight_front[55:48]) : 16'sd0;
			reg_product_alpha_eighth <= reg_mask_front[7] ? $signed(reg_activation_front[63:56]) * $signed(reg_weight_front[63:56]) : 16'sd0;
			reg_product_beta_first <= reg_mask_front[0] ? $signed(reg_activation_front[7:0]) * $signed(reg_weight_front[71:64]) : 16'sd0;
			reg_product_beta_second <= reg_mask_front[1] ? $signed(reg_activation_front[15:8]) * $signed(reg_weight_front[79:72]) : 16'sd0;
			reg_product_beta_third <= reg_mask_front[2] ? $signed(reg_activation_front[23:16]) * $signed(reg_weight_front[87:80]) : 16'sd0;
			reg_product_beta_fourth <= reg_mask_front[3] ? $signed(reg_activation_front[31:24]) * $signed(reg_weight_front[95:88]) : 16'sd0;
			reg_product_beta_fifth <= reg_mask_front[4] ? $signed(reg_activation_front[39:32]) * $signed(reg_weight_front[103:96]) : 16'sd0;
			reg_product_beta_sixth <= reg_mask_front[5] ? $signed(reg_activation_front[47:40]) * $signed(reg_weight_front[111:104]) : 16'sd0;
			reg_product_beta_seventh <= reg_mask_front[6] ? $signed(reg_activation_front[55:48]) * $signed(reg_weight_front[119:112]) : 16'sd0;
			reg_product_beta_eighth <= reg_mask_front[7] ? $signed(reg_activation_front[63:56]) * $signed(reg_weight_front[127:120]) : 16'sd0;
			reg_product_gamma_first <= reg_mask_front[0] ? $signed(reg_activation_front[7:0]) * $signed(reg_weight_front[135:128]) : 16'sd0;
			reg_product_gamma_second <= reg_mask_front[1] ? $signed(reg_activation_front[15:8]) * $signed(reg_weight_front[143:136]) : 16'sd0;
			reg_product_gamma_third <= reg_mask_front[2] ? $signed(reg_activation_front[23:16]) * $signed(reg_weight_front[151:144]) : 16'sd0;
			reg_product_gamma_fourth <= reg_mask_front[3] ? $signed(reg_activation_front[31:24]) * $signed(reg_weight_front[159:152]) : 16'sd0;
			reg_product_gamma_fifth <= reg_mask_front[4] ? $signed(reg_activation_front[39:32]) * $signed(reg_weight_front[167:160]) : 16'sd0;
			reg_product_gamma_sixth <= reg_mask_front[5] ? $signed(reg_activation_front[47:40]) * $signed(reg_weight_front[175:168]) : 16'sd0;
			reg_product_gamma_seventh <= reg_mask_front[6] ? $signed(reg_activation_front[55:48]) * $signed(reg_weight_front[183:176]) : 16'sd0;
			reg_product_gamma_eighth <= reg_mask_front[7] ? $signed(reg_activation_front[63:56]) * $signed(reg_weight_front[191:184]) : 16'sd0;
			reg_bias_product <= reg_bias_front;
			flag_product_valid <= flag_front_valid;
			flag_first_product <= flag_first_front;
			flag_last_product <= flag_last_front;
		end
	end

	//A2把每两个signed16乘积扩展为signed17相加
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_pair_alpha_first <= 17'sd0;
			reg_pair_alpha_second <= 17'sd0;
			reg_pair_alpha_third <= 17'sd0;
			reg_pair_alpha_fourth <= 17'sd0;
			reg_pair_beta_first <= 17'sd0;
			reg_pair_beta_second <= 17'sd0;
			reg_pair_beta_third <= 17'sd0;
			reg_pair_beta_fourth <= 17'sd0;
			reg_pair_gamma_first <= 17'sd0;
			reg_pair_gamma_second <= 17'sd0;
			reg_pair_gamma_third <= 17'sd0;
			reg_pair_gamma_fourth <= 17'sd0;
			reg_bias_pair <= 96'd0;
			flag_pair_valid <= 1'b0;
			flag_first_pair <= 1'b0;
			flag_last_pair <= 1'b0;
		end else begin
			reg_pair_alpha_first <= {reg_product_alpha_first[15], reg_product_alpha_first} + {reg_product_alpha_second[15], reg_product_alpha_second};
			reg_pair_alpha_second <= {reg_product_alpha_third[15], reg_product_alpha_third} + {reg_product_alpha_fourth[15], reg_product_alpha_fourth};
			reg_pair_alpha_third <= {reg_product_alpha_fifth[15], reg_product_alpha_fifth} + {reg_product_alpha_sixth[15], reg_product_alpha_sixth};
			reg_pair_alpha_fourth <= {reg_product_alpha_seventh[15], reg_product_alpha_seventh} + {reg_product_alpha_eighth[15], reg_product_alpha_eighth};
			reg_pair_beta_first <= {reg_product_beta_first[15], reg_product_beta_first} + {reg_product_beta_second[15], reg_product_beta_second};
			reg_pair_beta_second <= {reg_product_beta_third[15], reg_product_beta_third} + {reg_product_beta_fourth[15], reg_product_beta_fourth};
			reg_pair_beta_third <= {reg_product_beta_fifth[15], reg_product_beta_fifth} + {reg_product_beta_sixth[15], reg_product_beta_sixth};
			reg_pair_beta_fourth <= {reg_product_beta_seventh[15], reg_product_beta_seventh} + {reg_product_beta_eighth[15], reg_product_beta_eighth};
			reg_pair_gamma_first <= {reg_product_gamma_first[15], reg_product_gamma_first} + {reg_product_gamma_second[15], reg_product_gamma_second};
			reg_pair_gamma_second <= {reg_product_gamma_third[15], reg_product_gamma_third} + {reg_product_gamma_fourth[15], reg_product_gamma_fourth};
			reg_pair_gamma_third <= {reg_product_gamma_fifth[15], reg_product_gamma_fifth} + {reg_product_gamma_sixth[15], reg_product_gamma_sixth};
			reg_pair_gamma_fourth <= {reg_product_gamma_seventh[15], reg_product_gamma_seventh} + {reg_product_gamma_eighth[15], reg_product_gamma_eighth};
			reg_bias_pair <= reg_bias_product;
			flag_pair_valid <= flag_product_valid;
			flag_first_pair <= flag_first_product;
			flag_last_pair <= flag_last_product;
		end
	end

	//A3把相邻signed17对和扩展为signed18四项和
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_quad_alpha_first <= 18'sd0;
			reg_quad_alpha_second <= 18'sd0;
			reg_quad_beta_first <= 18'sd0;
			reg_quad_beta_second <= 18'sd0;
			reg_quad_gamma_first <= 18'sd0;
			reg_quad_gamma_second <= 18'sd0;
			reg_bias_quad <= 96'd0;
			flag_quad_valid <= 1'b0;
			flag_first_quad <= 1'b0;
			flag_last_quad <= 1'b0;
		end else begin
			reg_quad_alpha_first <= {reg_pair_alpha_first[16], reg_pair_alpha_first} + {reg_pair_alpha_second[16], reg_pair_alpha_second};
			reg_quad_alpha_second <= {reg_pair_alpha_third[16], reg_pair_alpha_third} + {reg_pair_alpha_fourth[16], reg_pair_alpha_fourth};
			reg_quad_beta_first <= {reg_pair_beta_first[16], reg_pair_beta_first} + {reg_pair_beta_second[16], reg_pair_beta_second};
			reg_quad_beta_second <= {reg_pair_beta_third[16], reg_pair_beta_third} + {reg_pair_beta_fourth[16], reg_pair_beta_fourth};
			reg_quad_gamma_first <= {reg_pair_gamma_first[16], reg_pair_gamma_first} + {reg_pair_gamma_second[16], reg_pair_gamma_second};
			reg_quad_gamma_second <= {reg_pair_gamma_third[16], reg_pair_gamma_third} + {reg_pair_gamma_fourth[16], reg_pair_gamma_fourth};
			reg_bias_quad <= reg_bias_pair;
			flag_quad_valid <= flag_pair_valid;
			flag_first_quad <= flag_first_pair;
			flag_last_quad <= flag_last_pair;
		end
	end

	//A4把两路signed18四项和扩展为signed19点积
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_dot_alpha <= 19'sd0;
			reg_dot_beta <= 19'sd0;
			reg_dot_gamma <= 19'sd0;
			reg_bias_dot <= 96'd0;
			flag_dot_valid <= 1'b0;
			flag_first_dot <= 1'b0;
			flag_last_dot <= 1'b0;
		end else begin
			reg_dot_alpha <= {reg_quad_alpha_first[17], reg_quad_alpha_first} + {reg_quad_alpha_second[17], reg_quad_alpha_second};
			reg_dot_beta <= {reg_quad_beta_first[17], reg_quad_beta_first} + {reg_quad_beta_second[17], reg_quad_beta_second};
			reg_dot_gamma <= {reg_quad_gamma_first[17], reg_quad_gamma_first} + {reg_quad_gamma_second[17], reg_quad_gamma_second};
			reg_bias_dot <= reg_bias_quad;
			flag_dot_valid <= flag_quad_valid;
			flag_first_dot <= flag_first_quad;
			flag_last_dot <= flag_last_quad;
		end
	end

	//A5在点积到达处读取当拍历史值并提交下一拍反馈
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_accumulator_alpha <= 33'sd0;
			reg_accumulator_beta <= 33'sd0;
			reg_accumulator_gamma <= 33'sd0;
			reg_candidate_alpha <= 34'sd0;
			reg_candidate_beta <= 34'sd0;
			reg_candidate_gamma <= 34'sd0;
			flag_candidate_valid <= 1'b0;
			flag_candidate_last <= 1'b0;
			flag_candidate_fault <= 1'b0;
		end else begin
			reg_candidate_alpha <= candidate_alpha_sum;
			reg_candidate_beta <= candidate_beta_sum;
			reg_candidate_gamma <= candidate_gamma_sum;
			flag_candidate_valid <= flag_dot_valid;
			flag_candidate_last <= flag_dot_valid & flag_last_dot;
			flag_candidate_fault <= flag_dot_valid & flag_last_dot & flag_overflow_any;
			if(flag_dot_valid & ~(flag_last_dot & flag_overflow_any))begin
				reg_accumulator_alpha <= candidate_alpha_sum[32:0];
				reg_accumulator_beta <= candidate_beta_sum[32:0];
				reg_accumulator_gamma <= candidate_gamma_sum[32:0];
			end else begin
				reg_accumulator_alpha <= reg_accumulator_alpha;
				reg_accumulator_beta <= reg_accumulator_beta;
				reg_accumulator_gamma <= reg_accumulator_gamma;
			end
		end
	end

	//A5锁存唯一末组的故障安全结果
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			flag_final_valid_stage0 <= 1'b0;
			reg_final_data_stage0 <= 96'd0;
			flag_final_fault_stage0 <= 1'b0;
		end else begin
			flag_final_valid_stage0 <= flag_dot_valid & flag_last_dot;
			if(flag_dot_valid & flag_last_dot)begin
				reg_final_data_stage0 <= flag_overflow_any ? 96'd0 : {candidate_gamma_sum[31:0], candidate_beta_sum[31:0], candidate_alpha_sum[31:0]};
				flag_final_fault_stage0 <= flag_overflow_any;
			end else begin
				reg_final_data_stage0 <= 96'd0;
				flag_final_fault_stage0 <= 1'b0;
			end
		end
	end

endmodule
