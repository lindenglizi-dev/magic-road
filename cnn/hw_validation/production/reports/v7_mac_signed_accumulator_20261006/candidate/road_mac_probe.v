`timescale 1ns / 1ps

////////////////////////////////////English///////////////////////////////////////
// Company:         Erie
// Engineer:        Erie
//
// Create Date:     2026/10/04 00:00:00
// Design Name:     road_mac_probe
// Module Name:     road_mac_probe
// Description:     description/road_mac_probe_Design.pdf
// Simulations:     testbench/vivado/2021.1/road_mac_probe
//
// Referrences:
// File Format      File Name
// 1.Book           cnn/hw_validation/mac/road_mac_probe_spec.md
//
// Dependencies:
// Module Name      Version
//
// Version:         V1.0
// Revision Date:   2026/10/04 00:00:00
// History:
// Time             Version     Revised by        Contents
// 2026/10/04       V1.0        Erie              Create file.
///////////////////////////////////Chinese////////////////////////////////////////
// 版权归属:        Erie
// 开发人员:        Erie
//
// 创建日期:        2026年10月04日
// 设计名称:        road_mac_probe
// 模块名称:        road_mac_probe
// 模块说明:        Description/road_mac_probe_Design.pdf
// 仿真工程:        TestBench/Vivado/2021.1/road_mac_probe
//
// 参考资料:
// 文件格式         文件名称
// 1.Book           cnn/hw_validation/mac/road_mac_probe_spec.md
//
// 依赖文件:
// 模块名称         版本
//
// 当前版本:        V1.0
// 修订日期:        2026年10月04日
// 修订历史:
// 时间             版本        修订人            修订内容
// 2026年10月04日   V1.0        Erie              创建文件

module road_mac_probe
(
	//-----------------全局信号-----------------//
	input i_clk,                                // 百兆工作时钟
	input i_rstn,                               // 异步低有效复位

	//-----------------用户接口-----------------//
	input i_input_valid,                        // 输入负载保持有效标志
	input i_first,                              // 当前拍选择偏置初值
	input i_last,                               // 当前拍完成本次归约
	input [7:0]i_lane_mask,                     // 八条输入通道共享使能掩码
	input [63:0]i_activation_data,              // 八个低字节优先的有符号激活值
	input [191:0]i_weight_data,                 // 三组八通道低字节优先权重
	input [95:0]i_bias_data,                    // 三个低字优先的有符号偏置
	input i_result_ready,                       // 下游接受结果或故障终态
	output o_input_ready,                       // 探针允许接受一个新输入拍
	output o_result_valid,                      // 结果负载保持有效标志
	output [95:0]o_result_data,                 // 三个低字优先的累加结果
	output o_fault                              // 任一路有符号累加越界标志
);

	//----------------寄存器信号----------------//
	//乘法与分级归约数据
	reg signed [15:0]reg_product_alpha_first = 16'sd0; // 甲输出首通道乘积
	reg signed [15:0]reg_product_alpha_second = 16'sd0; // 甲输出次通道乘积
	reg signed [15:0]reg_product_alpha_third = 16'sd0; // 甲输出第三通道乘积
	reg signed [15:0]reg_product_alpha_fourth = 16'sd0; // 甲输出第四通道乘积
	reg signed [15:0]reg_product_alpha_fifth = 16'sd0; // 甲输出第五通道乘积
	reg signed [15:0]reg_product_alpha_sixth = 16'sd0; // 甲输出第六通道乘积
	reg signed [15:0]reg_product_alpha_seventh = 16'sd0; // 甲输出第七通道乘积
	reg signed [15:0]reg_product_alpha_eighth = 16'sd0; // 甲输出末通道乘积
	reg signed [15:0]reg_product_beta_first = 16'sd0; // 乙输出首通道乘积
	reg signed [15:0]reg_product_beta_second = 16'sd0; // 乙输出次通道乘积
	reg signed [15:0]reg_product_beta_third = 16'sd0; // 乙输出第三通道乘积
	reg signed [15:0]reg_product_beta_fourth = 16'sd0; // 乙输出第四通道乘积
	reg signed [15:0]reg_product_beta_fifth = 16'sd0; // 乙输出第五通道乘积
	reg signed [15:0]reg_product_beta_sixth = 16'sd0; // 乙输出第六通道乘积
	reg signed [15:0]reg_product_beta_seventh = 16'sd0; // 乙输出第七通道乘积
	reg signed [15:0]reg_product_beta_eighth = 16'sd0; // 乙输出末通道乘积
	reg signed [15:0]reg_product_gamma_first = 16'sd0; // 丙输出首通道乘积
	reg signed [15:0]reg_product_gamma_second = 16'sd0; // 丙输出次通道乘积
	reg signed [15:0]reg_product_gamma_third = 16'sd0; // 丙输出第三通道乘积
	reg signed [15:0]reg_product_gamma_fourth = 16'sd0; // 丙输出第四通道乘积
	reg signed [15:0]reg_product_gamma_fifth = 16'sd0; // 丙输出第五通道乘积
	reg signed [15:0]reg_product_gamma_sixth = 16'sd0; // 丙输出第六通道乘积
	reg signed [15:0]reg_product_gamma_seventh = 16'sd0; // 丙输出第七通道乘积
	reg signed [15:0]reg_product_gamma_eighth = 16'sd0; // 丙输出末通道乘积
	reg signed [16:0]reg_pair_alpha_first = 17'sd0; // 甲输出首对和
	reg signed [16:0]reg_pair_alpha_second = 17'sd0; // 甲输出次对和
	reg signed [16:0]reg_pair_alpha_third = 17'sd0; // 甲输出第三对和
	reg signed [16:0]reg_pair_alpha_fourth = 17'sd0; // 甲输出末对和
	reg signed [16:0]reg_pair_beta_first = 17'sd0; // 乙输出首对和
	reg signed [16:0]reg_pair_beta_second = 17'sd0; // 乙输出次对和
	reg signed [16:0]reg_pair_beta_third = 17'sd0; // 乙输出第三对和
	reg signed [16:0]reg_pair_beta_fourth = 17'sd0; // 乙输出末对和
	reg signed [16:0]reg_pair_gamma_first = 17'sd0; // 丙输出首对和
	reg signed [16:0]reg_pair_gamma_second = 17'sd0; // 丙输出次对和
	reg signed [16:0]reg_pair_gamma_third = 17'sd0; // 丙输出第三对和
	reg signed [16:0]reg_pair_gamma_fourth = 17'sd0; // 丙输出末对和
	reg signed [17:0]reg_quad_alpha_first = 18'sd0; // 甲输出前四输入和
	reg signed [17:0]reg_quad_alpha_second = 18'sd0; // 甲输出后四输入和
	reg signed [17:0]reg_quad_beta_first = 18'sd0; // 乙输出前四输入和
	reg signed [17:0]reg_quad_beta_second = 18'sd0; // 乙输出后四输入和
	reg signed [17:0]reg_quad_gamma_first = 18'sd0; // 丙输出前四输入和
	reg signed [17:0]reg_quad_gamma_second = 18'sd0; // 丙输出后四输入和
	reg signed [18:0]reg_dot_alpha = 19'sd0;    // 甲输出八输入点积
	reg signed [18:0]reg_dot_beta = 19'sd0;     // 乙输出八输入点积
	reg signed [18:0]reg_dot_gamma = 19'sd0;    // 丙输出八输入点积

	//累加基值与候选数据
	reg [63:0]reg_activation_front = 64'd0;     // 握手拥有的八通道激活负载
	reg [191:0]reg_weight_front = 192'd0;       // 握手拥有的二十四权重负载
	reg [95:0]reg_bias_front = 96'd0;           // 握手拥有的三路偏置负载
	reg [7:0]reg_mask_front = 8'd0;             // 握手拥有的通道使能掩码
	reg [98:0]reg_base_product = 99'd0;         // 三路三十三位偏置或历史累加值
	reg [98:0]reg_base_pair = 99'd0;            // 与相邻对和对齐的累加基值
	reg [98:0]reg_base_quad = 99'd0;            // 与四输入和对齐的累加基值
	reg [98:0]reg_base_dot = 99'd0;             // 与八输入点积对齐的累加基值
	reg signed [33:0]reg_candidate_alpha = 34'sd0; // 甲输出完整精度候选
	reg signed [33:0]reg_candidate_beta = 34'sd0; // 乙输出完整精度候选
	reg signed [33:0]reg_candidate_gamma = 34'sd0; // 丙输出完整精度候选
	reg signed [33:0]reg_candidate_alpha_hold = 34'sd0; // 甲候选保持级
	reg signed [33:0]reg_candidate_beta_hold = 34'sd0; // 乙候选保持级
	reg signed [33:0]reg_candidate_gamma_hold = 34'sd0; // 丙候选保持级
	reg signed [33:0]reg_candidate_alpha_final = 34'sd0; // 甲候选判定级
	reg signed [33:0]reg_candidate_beta_final = 34'sd0; // 乙候选判定级
	reg signed [33:0]reg_candidate_gamma_final = 34'sd0; // 丙候选判定级
	reg [98:0]reg_publish_data = 99'd0;         // 候选写回使用的三路三十三位数据
	reg [31:0]reg_fault_safe_alpha = 32'd0;     // 甲输出故障安全数据
	reg [31:0]reg_fault_safe_beta = 32'd0;      // 乙输出故障安全数据
	reg [31:0]reg_fault_safe_gamma = 32'd0;     // 丙输出故障安全数据
	reg [98:0]reg_accumulator = 99'd0;          // 三路跨输入拍保留三十三位累加器
	reg [5:0]reg_last_pipe = 6'd0;              // 末拍属性到判定级的延迟链

	//-----------------标志信号-----------------//
	//控制流水数据
	reg [5:0]flag_stage_valid = 6'd0;           // 归约到判定各级有效移位标志
	reg flag_front_valid = 1'b0;                // 前端握手负载有效脉冲
	reg flag_first_front = 1'b0;                // 握手拥有的首拍属性
	reg flag_last_front = 1'b0;                 // 握手拥有的末拍属性
	reg flag_product_valid = 1'b0;              // 乘法寄存器内负载有效标志
	reg flag_overflow_alpha = 1'b0;             // 甲候选有符号越界
	reg flag_overflow_beta = 1'b0;              // 乙候选有符号越界
	reg flag_overflow_gamma = 1'b0;             // 丙候选有符号越界
	reg flag_overflow_any = 1'b0;               // 任一路候选发生有符号越界
	reg flag_last = 1'b0;                       // 判定级负载属于序列末拍
	reg flag_publish_event = 1'b0;              // 产生正常结果或故障终态脉冲
	reg flag_commit_event = 1'b0;               // 候选允许写回累加器脉冲
	reg flag_release_no_output = 1'b0;          // 非末拍正常完成释放脉冲
	reg flag_output_accept = 1'b0;              // 下游接受终态负载脉冲
	reg flag_release = 1'b0;                    // 当前在途输入允许结束标志
	reg flag_publish_fault = 1'b0;              // 与发布数据对齐的故障属性

	//输入通道有符号解释
	wire flag_input_accept;                     // 同时满足有效与就绪的输入事件
	wire flag_result_accept;                    // 下游接受保持终态的握手事件

	//-----------------其他信号-----------------//
	//输入通道有符号解释
	wire signed [7:0]activation_first;          // 首输入通道有符号激活
	wire signed [7:0]activation_second;         // 次输入通道有符号激活
	wire signed [7:0]activation_third;          // 第三输入通道有符号激活
	wire signed [7:0]activation_fourth;         // 第四输入通道有符号激活
	wire signed [7:0]activation_fifth;          // 第五输入通道有符号激活
	wire signed [7:0]activation_sixth;          // 第六输入通道有符号激活
	wire signed [7:0]activation_seventh;        // 第七输入通道有符号激活
	wire signed [7:0]activation_eighth;         // 末输入通道有符号激活

	//甲输出通道权重
	wire signed [7:0]weight_alpha_first;        // 甲输出首通道有符号权重
	wire signed [7:0]weight_alpha_second;       // 甲输出次通道有符号权重
	wire signed [7:0]weight_alpha_third;        // 甲输出第三通道有符号权重
	wire signed [7:0]weight_alpha_fourth;       // 甲输出第四通道有符号权重
	wire signed [7:0]weight_alpha_fifth;        // 甲输出第五通道有符号权重
	wire signed [7:0]weight_alpha_sixth;        // 甲输出第六通道有符号权重
	wire signed [7:0]weight_alpha_seventh;      // 甲输出第七通道有符号权重
	wire signed [7:0]weight_alpha_eighth;       // 甲输出末通道有符号权重

	//乙输出通道权重
	wire signed [7:0]weight_beta_first;         // 乙输出首通道有符号权重
	wire signed [7:0]weight_beta_second;        // 乙输出次通道有符号权重
	wire signed [7:0]weight_beta_third;         // 乙输出第三通道有符号权重
	wire signed [7:0]weight_beta_fourth;        // 乙输出第四通道有符号权重
	wire signed [7:0]weight_beta_fifth;         // 乙输出第五通道有符号权重
	wire signed [7:0]weight_beta_sixth;         // 乙输出第六通道有符号权重
	wire signed [7:0]weight_beta_seventh;       // 乙输出第七通道有符号权重
	wire signed [7:0]weight_beta_eighth;        // 乙输出末通道有符号权重

	//丙输出通道权重
	wire signed [7:0]weight_gamma_first;        // 丙输出首通道有符号权重
	wire signed [7:0]weight_gamma_second;       // 丙输出次通道有符号权重
	wire signed [7:0]weight_gamma_third;        // 丙输出第三通道有符号权重
	wire signed [7:0]weight_gamma_fourth;       // 丙输出第四通道有符号权重
	wire signed [7:0]weight_gamma_fifth;        // 丙输出第五通道有符号权重
	wire signed [7:0]weight_gamma_sixth;        // 丙输出第六通道有符号权重
	wire signed [7:0]weight_gamma_seventh;      // 丙输出第七通道有符号权重
	wire signed [7:0]weight_gamma_eighth;       // 丙输出末通道有符号权重

	//候选加法显式符号扩展
	wire signed [32:0]base_alpha;               // 甲输出三十三位累加基值
	wire signed [32:0]base_beta;                // 乙输出三十三位累加基值
	wire signed [32:0]base_gamma;               // 丙输出三十三位累加基值
	wire signed [32:0]dot_alpha_wide;           // 甲输出三十三位扩展点积
	wire signed [32:0]dot_beta_wide;            // 乙输出三十三位扩展点积
	wire signed [32:0]dot_gamma_wide;           // 丙输出三十三位扩展点积
	wire signed [33:0]candidate_alpha_sum;      // 甲输出两组三十三位操作数完整和
	wire signed [33:0]candidate_beta_sum;       // 乙输出两组三十三位操作数完整和
	wire signed [33:0]candidate_gamma_sum;      // 丙输出两组三十三位操作数完整和

	//-----------------输出信号-----------------//
	//用户接口
	reg input_ready_o = 1'b1;                   // 单事务通路的输入就绪输出
	reg result_valid_o = 1'b0;                  // 背压期间保持的结果有效输出
	reg [95:0]result_data_o = 96'd0;            // 背压期间保持的三路结果输出
	reg fault_o = 1'b0;                         // 背压期间保持的故障终态输出

	//---------------其他信号连线---------------//
	//其他信号连线
	assign flag_input_accept = i_input_valid & input_ready_o; // 输入负载真实转移事件
	assign flag_result_accept = result_valid_o & i_result_ready; // 输出负载真实转移事件
	assign activation_first = reg_activation_front[7:0]; // 解释首激活字节符号
	assign activation_second = reg_activation_front[15:8]; // 解释次激活字节符号
	assign activation_third = reg_activation_front[23:16]; // 解释第三激活字节符号
	assign activation_fourth = reg_activation_front[31:24]; // 解释第四激活字节符号
	assign activation_fifth = reg_activation_front[39:32]; // 解释第五激活字节符号
	assign activation_sixth = reg_activation_front[47:40]; // 解释第六激活字节符号
	assign activation_seventh = reg_activation_front[55:48]; // 解释第七激活字节符号
	assign activation_eighth = reg_activation_front[63:56]; // 解释末激活字节符号
	assign weight_alpha_first = reg_weight_front[7:0]; // 解释甲组首权重字节符号
	assign weight_alpha_second = reg_weight_front[15:8]; // 解释甲组次权重字节符号
	assign weight_alpha_third = reg_weight_front[23:16]; // 解释甲组第三权重字节符号
	assign weight_alpha_fourth = reg_weight_front[31:24]; // 解释甲组第四权重字节符号
	assign weight_alpha_fifth = reg_weight_front[39:32]; // 解释甲组第五权重字节符号
	assign weight_alpha_sixth = reg_weight_front[47:40]; // 解释甲组第六权重字节符号
	assign weight_alpha_seventh = reg_weight_front[55:48]; // 解释甲组第七权重字节符号
	assign weight_alpha_eighth = reg_weight_front[63:56]; // 解释甲组末权重字节符号
	assign weight_beta_first = reg_weight_front[71:64]; // 解释乙组首权重字节符号
	assign weight_beta_second = reg_weight_front[79:72]; // 解释乙组次权重字节符号
	assign weight_beta_third = reg_weight_front[87:80]; // 解释乙组第三权重字节符号
	assign weight_beta_fourth = reg_weight_front[95:88]; // 解释乙组第四权重字节符号
	assign weight_beta_fifth = reg_weight_front[103:96]; // 解释乙组第五权重字节符号
	assign weight_beta_sixth = reg_weight_front[111:104]; // 解释乙组第六权重字节符号
	assign weight_beta_seventh = reg_weight_front[119:112]; // 解释乙组第七权重字节符号
	assign weight_beta_eighth = reg_weight_front[127:120]; // 解释乙组末权重字节符号
	assign weight_gamma_first = reg_weight_front[135:128]; // 解释丙组首权重字节符号
	assign weight_gamma_second = reg_weight_front[143:136]; // 解释丙组次权重字节符号
	assign weight_gamma_third = reg_weight_front[151:144]; // 解释丙组第三权重字节符号
	assign weight_gamma_fourth = reg_weight_front[159:152]; // 解释丙组第四权重字节符号
	assign weight_gamma_fifth = reg_weight_front[167:160]; // 解释丙组第五权重字节符号
	assign weight_gamma_sixth = reg_weight_front[175:168]; // 解释丙组第六权重字节符号
	assign weight_gamma_seventh = reg_weight_front[183:176]; // 解释丙组第七权重字节符号
	assign weight_gamma_eighth = reg_weight_front[191:184]; // 解释丙组末权重字节符号
	assign base_alpha = reg_base_dot[32:0];     // 解释甲输出累加基值符号
	assign base_beta = reg_base_dot[65:33];     // 解释乙输出累加基值符号
	assign base_gamma = reg_base_dot[98:66];    // 解释丙输出累加基值符号
	assign dot_alpha_wide = {reg_dot_alpha[18], reg_dot_alpha[18], reg_dot_alpha[18], reg_dot_alpha[18], reg_dot_alpha[18], reg_dot_alpha[18], reg_dot_alpha[18], reg_dot_alpha[18], reg_dot_alpha[18], reg_dot_alpha[18], reg_dot_alpha[18], reg_dot_alpha[18], reg_dot_alpha[18], reg_dot_alpha[18], reg_dot_alpha}; // 符号扩展甲输出点积
	assign dot_beta_wide = {reg_dot_beta[18], reg_dot_beta[18], reg_dot_beta[18], reg_dot_beta[18], reg_dot_beta[18], reg_dot_beta[18], reg_dot_beta[18], reg_dot_beta[18], reg_dot_beta[18], reg_dot_beta[18], reg_dot_beta[18], reg_dot_beta[18], reg_dot_beta[18], reg_dot_beta[18], reg_dot_beta}; // 符号扩展乙输出点积
	assign dot_gamma_wide = {reg_dot_gamma[18], reg_dot_gamma[18], reg_dot_gamma[18], reg_dot_gamma[18], reg_dot_gamma[18], reg_dot_gamma[18], reg_dot_gamma[18], reg_dot_gamma[18], reg_dot_gamma[18], reg_dot_gamma[18], reg_dot_gamma[18], reg_dot_gamma[18], reg_dot_gamma[18], reg_dot_gamma[18], reg_dot_gamma}; // 符号扩展丙输出点积
	assign candidate_alpha_sum = base_alpha + dot_alpha_wide; // 保留甲输出加法进位
	assign candidate_beta_sum = base_beta + dot_beta_wide; // 保留乙输出加法进位
	assign candidate_gamma_sum = base_gamma + dot_gamma_wide; // 保留丙输出加法进位

	//---------------输出信号连线---------------//
	//用户接口
	assign o_input_ready = input_ready_o;       // 输入就绪寄存器桥接
	assign o_result_valid = result_valid_o;     // 输出有效标志桥接
	assign o_result_data = result_data_o;       // 三路累加结果桥接
	assign o_fault = fault_o;                   // 累加越界终态桥接

	//-------------输出信号处理区域-------------//
	//用户接口
	//输入就绪占用更新
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			input_ready_o <= 1'b1;              // 复位后允许接收首个输入拍
		end else begin
			input_ready_o <= (~i_input_valid & input_ready_o) | flag_release; // 三操作更新单在途就绪状态
		end
	end

	//结果有效背压保持
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			result_valid_o <= 1'b0;             // 复位撤销所有待收终态
		end else begin
			result_valid_o <= (result_valid_o & ~i_result_ready) | flag_publish_event; // 三操作保持或发布终态
		end
	end

	//结果负载终态发布
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			result_data_o <= 96'd0;             // 复位清空可见结果数据
		end else if(flag_publish_event == 1'b1)begin
			result_data_o <= {reg_fault_safe_gamma, reg_fault_safe_beta, reg_fault_safe_alpha}; // 锁存正常数值或故障零值
		end else begin
			result_data_o <= result_data_o;     // 下游停顿时保持结果不变
		end
	end

	//故障属性终态发布
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			fault_o <= 1'b0;                    // 复位清除外部故障指示
		end else if(flag_publish_event == 1'b1)begin
			fault_o <= flag_publish_fault;      // 锁存当前终态的越界属性
		end else begin
			fault_o <= fault_o;                 // 结果背压期间保持故障属性
		end
	end

	//-------------主要任务处理区域-------------//
	//前端握手脉冲登记
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			flag_front_valid <= 1'b0;           // 复位清除前端握手脉冲
		end else begin
			flag_front_valid <= flag_input_accept; // 只传播真实输入转移事件
		end
	end

	//首拍属性握手锁存
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			flag_first_front <= 1'b0;           // 复位清除首拍属性
		end else if(flag_input_accept == 1'b1)begin
			flag_first_front <= i_first;        // 接受首拍属性
		end else begin
			flag_first_front <= 1'b0;           // 非转移周期清除首拍属性
		end
	end

	//末拍属性握手锁存
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			flag_last_front <= 1'b0;            // 复位清除末拍属性
		end else if(flag_input_accept == 1'b1)begin
			flag_last_front <= i_last;          // 接受末拍属性
		end else begin
			flag_last_front <= 1'b0;            // 非转移周期清除末拍属性
		end
	end

	//激活负载握手锁存
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_activation_front <= 64'd0;      // 复位清空激活负载
		end else if(flag_input_accept == 1'b1)begin
			reg_activation_front <= i_activation_data; // 接受八通道激活负载
		end else begin
			reg_activation_front <= 64'd0;      // 非转移周期不采样外部激活
		end
	end

	//偏置负载握手锁存
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_bias_front <= 96'd0;            // 复位清空偏置负载
		end else if(flag_input_accept == 1'b1)begin
			reg_bias_front <= i_bias_data;      // 接受三路累加偏置
		end else begin
			reg_bias_front <= 96'd0;            // 非转移周期不采样外部偏置
		end
	end

	//通道掩码握手锁存
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_mask_front <= 8'd0;             // 复位清空通道掩码
		end else if(flag_input_accept == 1'b1)begin
			reg_mask_front <= i_lane_mask;      // 接受共享通道掩码
		end else begin
			reg_mask_front <= 8'd0;             // 非转移周期不采样外部掩码
		end
	end

	//权重负载握手锁存
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_weight_front <= 192'd0;         // 复位清空权重负载
		end else if(flag_input_accept == 1'b1)begin
			reg_weight_front <= i_weight_data;  // 接受三组八通道权重
		end else begin
			reg_weight_front <= 192'd0;         // 非转移周期不采样外部权重
		end
	end

	//乘法流水有效传递
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			flag_product_valid <= 1'b0;         // 复位取消乘法级有效负载
		end else begin
			flag_product_valid <= flag_front_valid; // 前端负载进入乘法寄存级
		end
	end

	//甲末通道乘积寄存
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_product_alpha_eighth <= 16'sd0; // 复位清空甲组末乘积
		end else begin
			reg_product_alpha_eighth <= reg_mask_front[7] ? activation_eighth * weight_alpha_eighth : 16'sd0; // 甲组末通道乘积
		end
	end

	//甲五通道乘积寄存
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_product_alpha_fifth <= 16'sd0;  // 复位清空甲组第五乘积
		end else begin
			reg_product_alpha_fifth <= reg_mask_front[4] ? activation_fifth * weight_alpha_fifth : 16'sd0; // 甲组第五通道乘积
		end
	end

	//甲首通道乘积寄存
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_product_alpha_first <= 16'sd0;  // 复位清空甲组首乘积
		end else begin
			reg_product_alpha_first <= reg_mask_front[0] ? activation_first * weight_alpha_first : 16'sd0; // 甲组首通道乘积
		end
	end

	//甲四通道乘积寄存
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_product_alpha_fourth <= 16'sd0; // 复位清空甲组第四乘积
		end else begin
			reg_product_alpha_fourth <= reg_mask_front[3] ? activation_fourth * weight_alpha_fourth : 16'sd0; // 甲组第四通道乘积
		end
	end

	//甲次通道乘积寄存
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_product_alpha_second <= 16'sd0; // 复位清空甲组次乘积
		end else begin
			reg_product_alpha_second <= reg_mask_front[1] ? activation_second * weight_alpha_second : 16'sd0; // 甲组次通道乘积
		end
	end

	//甲七通道乘积寄存
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_product_alpha_seventh <= 16'sd0; // 复位清空甲组第七乘积
		end else begin
			reg_product_alpha_seventh <= reg_mask_front[6] ? activation_seventh * weight_alpha_seventh : 16'sd0; // 甲组第七通道乘积
		end
	end

	//甲六通道乘积寄存
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_product_alpha_sixth <= 16'sd0;  // 复位清空甲组第六乘积
		end else begin
			reg_product_alpha_sixth <= reg_mask_front[5] ? activation_sixth * weight_alpha_sixth : 16'sd0; // 甲组第六通道乘积
		end
	end

	//甲三通道乘积寄存
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_product_alpha_third <= 16'sd0;  // 复位清空甲组第三乘积
		end else begin
			reg_product_alpha_third <= reg_mask_front[2] ? activation_third * weight_alpha_third : 16'sd0; // 甲组第三通道乘积
		end
	end

	//乙末通道乘积寄存
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_product_beta_eighth <= 16'sd0;  // 复位清空乙组末乘积
		end else begin
			reg_product_beta_eighth <= reg_mask_front[7] ? activation_eighth * weight_beta_eighth : 16'sd0; // 乙组末通道乘积
		end
	end

	//乙五通道乘积寄存
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_product_beta_fifth <= 16'sd0;   // 复位清空乙组第五乘积
		end else begin
			reg_product_beta_fifth <= reg_mask_front[4] ? activation_fifth * weight_beta_fifth : 16'sd0; // 乙组第五通道乘积
		end
	end

	//乙首通道乘积寄存
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_product_beta_first <= 16'sd0;   // 复位清空乙组首乘积
		end else begin
			reg_product_beta_first <= reg_mask_front[0] ? activation_first * weight_beta_first : 16'sd0; // 乙组首通道乘积
		end
	end

	//乙四通道乘积寄存
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_product_beta_fourth <= 16'sd0;  // 复位清空乙组第四乘积
		end else begin
			reg_product_beta_fourth <= reg_mask_front[3] ? activation_fourth * weight_beta_fourth : 16'sd0; // 乙组第四通道乘积
		end
	end

	//乙次通道乘积寄存
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_product_beta_second <= 16'sd0;  // 复位清空乙组次乘积
		end else begin
			reg_product_beta_second <= reg_mask_front[1] ? activation_second * weight_beta_second : 16'sd0; // 乙组次通道乘积
		end
	end

	//乙七通道乘积寄存
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_product_beta_seventh <= 16'sd0; // 复位清空乙组第七乘积
		end else begin
			reg_product_beta_seventh <= reg_mask_front[6] ? activation_seventh * weight_beta_seventh : 16'sd0; // 乙组第七通道乘积
		end
	end

	//乙六通道乘积寄存
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_product_beta_sixth <= 16'sd0;   // 复位清空乙组第六乘积
		end else begin
			reg_product_beta_sixth <= reg_mask_front[5] ? activation_sixth * weight_beta_sixth : 16'sd0; // 乙组第六通道乘积
		end
	end

	//乙三通道乘积寄存
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_product_beta_third <= 16'sd0;   // 复位清空乙组第三乘积
		end else begin
			reg_product_beta_third <= reg_mask_front[2] ? activation_third * weight_beta_third : 16'sd0; // 乙组第三通道乘积
		end
	end

	//丙末通道乘积寄存
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_product_gamma_eighth <= 16'sd0; // 复位清空丙组末乘积
		end else begin
			reg_product_gamma_eighth <= reg_mask_front[7] ? activation_eighth * weight_gamma_eighth : 16'sd0; // 丙组末通道乘积
		end
	end

	//丙五通道乘积寄存
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_product_gamma_fifth <= 16'sd0;  // 复位清空丙组第五乘积
		end else begin
			reg_product_gamma_fifth <= reg_mask_front[4] ? activation_fifth * weight_gamma_fifth : 16'sd0; // 丙组第五通道乘积
		end
	end

	//丙首通道乘积寄存
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_product_gamma_first <= 16'sd0;  // 复位清空丙组首乘积
		end else begin
			reg_product_gamma_first <= reg_mask_front[0] ? activation_first * weight_gamma_first : 16'sd0; // 丙组首通道乘积
		end
	end

	//丙四通道乘积寄存
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_product_gamma_fourth <= 16'sd0; // 复位清空丙组第四乘积
		end else begin
			reg_product_gamma_fourth <= reg_mask_front[3] ? activation_fourth * weight_gamma_fourth : 16'sd0; // 丙组第四通道乘积
		end
	end

	//丙次通道乘积寄存
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_product_gamma_second <= 16'sd0; // 复位清空丙组次乘积
		end else begin
			reg_product_gamma_second <= reg_mask_front[1] ? activation_second * weight_gamma_second : 16'sd0; // 丙组次通道乘积
		end
	end

	//丙七通道乘积寄存
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_product_gamma_seventh <= 16'sd0; // 复位清空丙组第七乘积
		end else begin
			reg_product_gamma_seventh <= reg_mask_front[6] ? activation_seventh * weight_gamma_seventh : 16'sd0; // 丙组第七通道乘积
		end
	end

	//丙六通道乘积寄存
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_product_gamma_sixth <= 16'sd0;  // 复位清空丙组第六乘积
		end else begin
			reg_product_gamma_sixth <= reg_mask_front[5] ? activation_sixth * weight_gamma_sixth : 16'sd0; // 丙组第六通道乘积
		end
	end

	//丙三通道乘积寄存
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_product_gamma_third <= 16'sd0;  // 复位清空丙组第三乘积
		end else begin
			reg_product_gamma_third <= reg_mask_front[2] ? activation_third * weight_gamma_third : 16'sd0; // 丙组第三通道乘积
		end
	end

	//甲首对部分和寄存
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_pair_alpha_first <= 17'sd0;     // 复位清空甲组首对和
		end else begin
			reg_pair_alpha_first <= {reg_product_alpha_first[15], reg_product_alpha_first} + {reg_product_alpha_second[15], reg_product_alpha_second}; // 甲组首对归约
		end
	end

	//甲四对部分和寄存
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_pair_alpha_fourth <= 17'sd0;    // 复位清空甲组末对和
		end else begin
			reg_pair_alpha_fourth <= {reg_product_alpha_seventh[15], reg_product_alpha_seventh} + {reg_product_alpha_eighth[15], reg_product_alpha_eighth}; // 甲组末对归约
		end
	end

	//甲次对部分和寄存
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_pair_alpha_second <= 17'sd0;    // 复位清空甲组次对和
		end else begin
			reg_pair_alpha_second <= {reg_product_alpha_third[15], reg_product_alpha_third} + {reg_product_alpha_fourth[15], reg_product_alpha_fourth}; // 甲组次对归约
		end
	end

	//甲三对部分和寄存
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_pair_alpha_third <= 17'sd0;     // 复位清空甲组第三对和
		end else begin
			reg_pair_alpha_third <= {reg_product_alpha_fifth[15], reg_product_alpha_fifth} + {reg_product_alpha_sixth[15], reg_product_alpha_sixth}; // 甲组第三对归约
		end
	end

	//乙首对部分和寄存
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_pair_beta_first <= 17'sd0;      // 复位清空乙组首对和
		end else begin
			reg_pair_beta_first <= {reg_product_beta_first[15], reg_product_beta_first} + {reg_product_beta_second[15], reg_product_beta_second}; // 乙组首对归约
		end
	end

	//乙四对部分和寄存
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_pair_beta_fourth <= 17'sd0;     // 复位清空乙组末对和
		end else begin
			reg_pair_beta_fourth <= {reg_product_beta_seventh[15], reg_product_beta_seventh} + {reg_product_beta_eighth[15], reg_product_beta_eighth}; // 乙组末对归约
		end
	end

	//乙次对部分和寄存
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_pair_beta_second <= 17'sd0;     // 复位清空乙组次对和
		end else begin
			reg_pair_beta_second <= {reg_product_beta_third[15], reg_product_beta_third} + {reg_product_beta_fourth[15], reg_product_beta_fourth}; // 乙组次对归约
		end
	end

	//乙三对部分和寄存
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_pair_beta_third <= 17'sd0;      // 复位清空乙组第三对和
		end else begin
			reg_pair_beta_third <= {reg_product_beta_fifth[15], reg_product_beta_fifth} + {reg_product_beta_sixth[15], reg_product_beta_sixth}; // 乙组第三对归约
		end
	end

	//丙首对部分和寄存
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_pair_gamma_first <= 17'sd0;     // 复位清空丙组首对和
		end else begin
			reg_pair_gamma_first <= {reg_product_gamma_first[15], reg_product_gamma_first} + {reg_product_gamma_second[15], reg_product_gamma_second}; // 丙组首对归约
		end
	end

	//丙四对部分和寄存
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_pair_gamma_fourth <= 17'sd0;    // 复位清空丙组末对和
		end else begin
			reg_pair_gamma_fourth <= {reg_product_gamma_seventh[15], reg_product_gamma_seventh} + {reg_product_gamma_eighth[15], reg_product_gamma_eighth}; // 丙组末对归约
		end
	end

	//丙次对部分和寄存
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_pair_gamma_second <= 17'sd0;    // 复位清空丙组次对和
		end else begin
			reg_pair_gamma_second <= {reg_product_gamma_third[15], reg_product_gamma_third} + {reg_product_gamma_fourth[15], reg_product_gamma_fourth}; // 丙组次对归约
		end
	end

	//丙三对部分和寄存
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_pair_gamma_third <= 17'sd0;     // 复位清空丙组第三对和
		end else begin
			reg_pair_gamma_third <= {reg_product_gamma_fifth[15], reg_product_gamma_fifth} + {reg_product_gamma_sixth[15], reg_product_gamma_sixth}; // 丙组第三对归约
		end
	end

	//甲前半归约和寄存
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_quad_alpha_first <= 18'sd0;     // 复位清空甲组前四输入和
		end else begin
			reg_quad_alpha_first <= {reg_pair_alpha_first[16], reg_pair_alpha_first} + {reg_pair_alpha_second[16], reg_pair_alpha_second}; // 甲组前四输入和
		end
	end

	//甲后半归约和寄存
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_quad_alpha_second <= 18'sd0;    // 复位清空甲组后四输入和
		end else begin
			reg_quad_alpha_second <= {reg_pair_alpha_third[16], reg_pair_alpha_third} + {reg_pair_alpha_fourth[16], reg_pair_alpha_fourth}; // 甲组后四输入和
		end
	end

	//乙前半归约和寄存
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_quad_beta_first <= 18'sd0;      // 复位清空乙组前四输入和
		end else begin
			reg_quad_beta_first <= {reg_pair_beta_first[16], reg_pair_beta_first} + {reg_pair_beta_second[16], reg_pair_beta_second}; // 乙组前四输入和
		end
	end

	//乙后半归约和寄存
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_quad_beta_second <= 18'sd0;     // 复位清空乙组后四输入和
		end else begin
			reg_quad_beta_second <= {reg_pair_beta_third[16], reg_pair_beta_third} + {reg_pair_beta_fourth[16], reg_pair_beta_fourth}; // 乙组后四输入和
		end
	end

	//丙前半归约和寄存
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_quad_gamma_first <= 18'sd0;     // 复位清空丙组前四输入和
		end else begin
			reg_quad_gamma_first <= {reg_pair_gamma_first[16], reg_pair_gamma_first} + {reg_pair_gamma_second[16], reg_pair_gamma_second}; // 丙组前四输入和
		end
	end

	//丙后半归约和寄存
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_quad_gamma_second <= 18'sd0;    // 复位清空丙组后四输入和
		end else begin
			reg_quad_gamma_second <= {reg_pair_gamma_third[16], reg_pair_gamma_third} + {reg_pair_gamma_fourth[16], reg_pair_gamma_fourth}; // 丙组后四输入和
		end
	end

	//甲八通道点积寄存
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_dot_alpha <= 19'sd0;            // 复位清空甲输出点积
		end else begin
			reg_dot_alpha <= {reg_quad_alpha_first[17], reg_quad_alpha_first} + {reg_quad_alpha_second[17], reg_quad_alpha_second}; // 合并甲输出前后四输入部分和
		end
	end

	//乙八通道点积寄存
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_dot_beta <= 19'sd0;             // 复位清空乙输出点积
		end else begin
			reg_dot_beta <= {reg_quad_beta_first[17], reg_quad_beta_first} + {reg_quad_beta_second[17], reg_quad_beta_second}; // 合并乙输出前后四输入部分和
		end
	end

	//丙八通道点积寄存
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_dot_gamma <= 19'sd0;            // 复位清空丙输出点积
		end else begin
			reg_dot_gamma <= {reg_quad_gamma_first[17], reg_quad_gamma_first} + {reg_quad_gamma_second[17], reg_quad_gamma_second}; // 合并丙输出前后四输入部分和
		end
	end

	//偏置历史基值选择
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_base_product <= 99'd0;          // 复位清空输入拍累加基值
		end else begin
			reg_base_product <= flag_first_front ? {reg_bias_front[95], reg_bias_front[95:64], reg_bias_front[63], reg_bias_front[63:32], reg_bias_front[31], reg_bias_front[31:0]} : reg_accumulator; // 三路偏置各自符号扩展后只在首拍进入
		end
	end

	//相邻对基值延迟
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_base_pair <= 99'd0;             // 复位清空相邻对级基值
		end else begin
			reg_base_pair <= reg_base_product;  // 对齐相邻对和流水级
		end
	end

	//四输入基值延迟
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_base_quad <= 99'd0;             // 复位清空四输入级基值
		end else begin
			reg_base_quad <= reg_base_pair;     // 对齐四输入和流水级
		end
	end

	//点积基值延迟
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_base_dot <= 99'd0;              // 复位清空点积级基值
		end else begin
			reg_base_dot <= reg_base_quad;      // 对齐八输入点积流水级
		end
	end

	//甲完整候选求和
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_candidate_alpha <= 34'sd0;      // 复位清空甲扩展候选
		end else begin
			reg_candidate_alpha <= candidate_alpha_sum; // 甲输出扩展累加候选
		end
	end

	//乙完整候选求和
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_candidate_beta <= 34'sd0;       // 复位清空乙扩展候选
		end else begin
			reg_candidate_beta <= candidate_beta_sum; // 乙输出扩展累加候选
		end
	end

	//丙完整候选求和
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_candidate_gamma <= 34'sd0;      // 复位清空丙扩展候选
		end else begin
			reg_candidate_gamma <= candidate_gamma_sum; // 丙输出扩展累加候选
		end
	end

	//甲候选越界对齐
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_candidate_alpha_hold <= 34'sd0; // 复位清空甲候选保持级
		end else begin
			reg_candidate_alpha_hold <= reg_candidate_alpha; // 延迟甲候选供汇总使用
		end
	end

	//乙候选越界对齐
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_candidate_beta_hold <= 34'sd0;  // 复位清空乙候选保持级
		end else begin
			reg_candidate_beta_hold <= reg_candidate_beta; // 延迟乙候选供汇总使用
		end
	end

	//丙候选越界对齐
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_candidate_gamma_hold <= 34'sd0; // 复位清空丙候选保持级
		end else begin
			reg_candidate_gamma_hold <= reg_candidate_gamma; // 延迟丙候选供汇总使用
		end
	end

	//甲候选终态对齐
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_candidate_alpha_final <= 34'sd0; // 复位清空甲候选判定级
		end else begin
			reg_candidate_alpha_final <= reg_candidate_alpha_hold; // 延迟甲候选到判定级
		end
	end

	//乙候选终态对齐
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_candidate_beta_final <= 34'sd0; // 复位清空乙候选判定级
		end else begin
			reg_candidate_beta_final <= reg_candidate_beta_hold; // 延迟乙候选到判定级
		end
	end

	//丙候选终态对齐
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_candidate_gamma_final <= 34'sd0; // 复位清空丙候选判定级
		end else begin
			reg_candidate_gamma_final <= reg_candidate_gamma_hold; // 延迟丙候选到判定级
		end
	end

	//候选三十三位写回缓存
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_publish_data <= 99'd0;          // 复位清空写回数据缓冲
		end else begin
			reg_publish_data <= {reg_candidate_gamma_final[32:0], reg_candidate_beta_final[32:0], reg_candidate_alpha_final[32:0]}; // 保留三路跨组累加符号位
		end
	end

	//甲候选符号检查
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			flag_overflow_alpha <= 1'b0;        // 复位清空甲输出越界结果
		end else begin
			flag_overflow_alpha <= (reg_candidate_alpha[33] ^ reg_candidate_alpha[31]) | (reg_candidate_alpha[32] ^ reg_candidate_alpha[31]); // 甲输出符号扩展不一致
		end
	end

	//乙候选符号检查
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			flag_overflow_beta <= 1'b0;         // 复位清空乙输出越界结果
		end else begin
			flag_overflow_beta <= (reg_candidate_beta[33] ^ reg_candidate_beta[31]) | (reg_candidate_beta[32] ^ reg_candidate_beta[31]); // 乙输出符号扩展不一致
		end
	end

	//丙候选符号检查
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			flag_overflow_gamma <= 1'b0;        // 复位清空丙输出越界结果
		end else begin
			flag_overflow_gamma <= (reg_candidate_gamma[33] ^ reg_candidate_gamma[31]) | (reg_candidate_gamma[32] ^ reg_candidate_gamma[31]); // 丙输出符号扩展不一致
		end
	end

	//甲故障结果选通
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_fault_safe_alpha <= 32'd0;      // 复位清空甲故障安全数据
		end else begin
			reg_fault_safe_alpha <= flag_overflow_any ? 32'd0 : reg_candidate_alpha_final[31:0]; // 甲输出故障时禁止回绕可见
		end
	end

	//乙故障结果选通
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_fault_safe_beta <= 32'd0;       // 复位清空乙故障安全数据
		end else begin
			reg_fault_safe_beta <= flag_overflow_any ? 32'd0 : reg_candidate_beta_final[31:0]; // 乙输出故障时返回确定零值
		end
	end

	//丙故障结果选通
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_fault_safe_gamma <= 32'd0;      // 复位清空丙故障安全数据
		end else begin
			reg_fault_safe_gamma <= flag_overflow_any ? 32'd0 : reg_candidate_gamma_final[31:0]; // 丙输出故障时保持终态一致
		end
	end

	//三路越界汇总登记
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			flag_overflow_any <= 1'b0;          // 复位清空汇总溢出标志
		end else begin
			flag_overflow_any <= reg_last_pipe[5] & (flag_overflow_alpha | flag_overflow_beta | flag_overflow_gamma); // 仅末组把任一路INT32越界发布为故障
		end
	end

	//归约有效链移位
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			flag_stage_valid <= 6'd0;           // 复位清空全部流水有效位
		end else begin
			flag_stage_valid <= {flag_stage_valid[4:0], flag_product_valid}; // 移入真实输入握手结果
		end
	end

	//末拍属性流水移位
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_last_pipe <= 6'd0;              // 复位清空末拍属性延迟链
		end else begin
			reg_last_pipe <= {reg_last_pipe[4:0], flag_last_front}; // 保持与前端负载相同采样相位
		end
	end

	//终态末拍属性登记
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			flag_last <= 1'b0;                  // 复位清空判定级末拍属性
		end else begin
			flag_last <= reg_last_pipe[5];      // 对齐汇总溢出和候选数据
		end
	end

	//终态发布事件形成
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			flag_publish_event <= 1'b0;         // 复位清除终态发布脉冲
		end else begin
			flag_publish_event <= flag_stage_valid[5] & (flag_overflow_any | flag_last); // 正常末拍和故障共享出口
		end
	end

	//无错累加提交形成
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			flag_commit_event <= 1'b0;          // 复位清除累加写回脉冲
		end else begin
			flag_commit_event <= flag_stage_valid[5] & ~flag_overflow_any; // 故障候选禁止写回
		end
	end

	//续拍内部释放形成
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			flag_release_no_output <= 1'b0;     // 复位清除内部释放脉冲
		end else begin
			flag_release_no_output <= flag_stage_valid[5] & ~(flag_overflow_any | flag_last); // 继续序列但不发布结果
		end
	end

	//发布故障属性对齐
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			flag_publish_fault <= 1'b0;         // 复位清空发布故障属性
		end else begin
			flag_publish_fault <= flag_overflow_any; // 传递判定级汇总越界结果
		end
	end

	//历史累加结果提交
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_accumulator <= 99'd0;           // 复位清空跨拍累加历史
		end else if(flag_commit_event == 1'b1)begin
			reg_accumulator <= reg_publish_data; // 写回无溢出的三路候选
		end else begin
			reg_accumulator <= reg_accumulator; // 无提交事件时保留历史值
		end
	end

	//结果握手事件登记
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			flag_output_accept <= 1'b0;         // 复位清除下游接受脉冲
		end else begin
			flag_output_accept <= flag_result_accept; // 有效与就绪同时成立才接受
		end
	end

	//两类释放事件合并
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			flag_release <= 1'b0;               // 复位清除统一释放标志
		end else begin
			flag_release <= flag_release_no_output | flag_output_accept; // 合并两类合法完成路径
		end
	end

endmodule
