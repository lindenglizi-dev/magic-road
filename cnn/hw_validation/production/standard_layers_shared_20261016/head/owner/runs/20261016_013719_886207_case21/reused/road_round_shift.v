`timescale 1ns / 1ps

////////////////////////////////////English///////////////////////////////////////
// Company:         Erie
// Engineer:        Erie
//
// Create Date:     2026/10/04 00:00:00
// Design Name:     road_round_shift
// Module Name:     road_round_shift
// Description:     description/road_round_shift_Design.pdf
// Simulations:     testbench/vivado/2021.1/road_round_shift
//
// Referrences:
// File Format      File Name
// 1.Book           road_round_shift.contract.json
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
// 设计名称:        road_round_shift
// 模块名称:        road_round_shift
// 模块说明:        Description/road_round_shift_Design.pdf
// 仿真工程:        TestBench/Vivado/2021.1/road_round_shift
//
// 参考资料:
// 文件格式         文件名称
// 1.Book           road_round_shift.contract.json
//
// 依赖文件:
// 模块名称         版本
//
// 当前版本:        V1.0
// 修订日期:        2026年10月04日
// 修订历史:
// 时间             版本        修订人            修订内容
// 2026年10月04日   V1.0        Erie              创建文件

module road_round_shift
(
	//-----------------全局信号-----------------//
	input i_clk,                                // 算术流水工作时钟
	input i_rstn,                               // 异步低有效取消复位

	//-----------------用户接口-----------------//
	input i_advance,                            // 外层控制的共同推进许可
	input i_input_valid,                        // 本次推进携带有效乘积
	input signed [63:0]i_product,               // 上游完整有符号乘积
	input [5:0]i_shift,                         // 非负二进制除数指数
	input [15:0]i_tag,                          // 与乘积绑定的结果身份

	//----------------RESULT接口----------------//

	//RESULT接口
	output o_result_valid,                      // 完成舍入的结果有效标志
	output [15:0]o_result_data,                 // 饱和后的有符号整数位型
	output [15:0]o_result_tag,                  // 原输入身份随结果返回
	output o_fault                              // 非法移位或乘积最小值标志
);

	//----------------寄存器信号----------------//
	//乘积绝对值与第一拍非法标记
	reg [63:0]reg_absolute = 64'd0;             // 第一拍乘积绝对值
	reg [5:0]reg_shift = 6'd0;                  // 第一拍保留移位指数
	reg reg_bad_shift = 1'd0;                   // 第一拍非法指数检测
	reg reg_bad_product = 1'd0;                 // 第一拍最小负整数检测
	reg [5:0]reg_sign_pipe = 6'd0;              // 到符号恢复拍的负号流水

	//除法商和余数比较路径
	reg [63:0]reg_absolute_delay = 64'd0;       // 第二拍绝对值供掩码提取
	reg [63:0]reg_quotient = 64'd0;             // 第二拍截断的正数商
	reg [63:0]reg_mask = 64'd0;                 // 第二拍余数低位掩码
	reg [63:0]reg_half = 64'd0;                 // 第二拍除数半值
	reg [63:0]reg_remainder = 64'd0;            // 第三拍精确余数
	reg [63:0]reg_half_delay = 64'd0;           // 第三拍保留半值
	reg [63:0]reg_quotient_rem = 64'd0;         // 第三拍商与余数同步
	reg [63:0]reg_quotient_compare = 64'd0;     // 第四拍商与比较标志同步
	reg [63:0]reg_quotient_increment = 64'd0;   // 第五拍待进位商
	reg [2:0]reg_fraction_pipe = 3'd0;          // 到第五拍的非零指数标记
	reg reg_above = 1'd0;                       // 第四拍余数大于半值
	reg reg_tie_odd = 1'd0;                     // 第四拍中点且商为奇数
	reg reg_increment = 1'd0;                   // 第五拍最近偶数进位决定
	reg [63:0]reg_rounded_magnitude = 64'd0;    // 第六拍已舍入绝对值
	reg signed [63:0]reg_signed_value = 64'd0;  // 第七拍恢复原符号

	//范围比较与终端身份
	reg reg_below_minimum = 1'd0;               // 第八拍负端饱和标志
	reg reg_above_maximum = 1'd0;               // 第八拍正端饱和标志
	reg [15:0]reg_narrow_value = 16'd0;         // 第八拍保留范围内位型
	reg [127:0]reg_tag_pipe = 128'd0;           // 前八拍不透明身份
	reg [6:0]reg_fault_pipe = 7'd0;             // 第二到第八拍故障标记

	//-----------------标志信号-----------------//
	reg [7:0]flag_valid_pipe = 8'd0;            // 前八拍有效令牌

	//-----------------输出信号-----------------//
	//RESULT接口
	reg result_valid_o = 1'd0;                  // 第九拍输出有效代理
	reg [15:0]result_data_o = 16'd0;            // 第九拍输出数值代理
	reg [15:0]result_tag_o = 16'd0;             // 第九拍输出身份代理
	reg fault_o = 1'd0;                         // 第九拍输出故障代理

	//---------------输出信号连线---------------//
	//RESULT接口
	assign o_result_valid = result_valid_o;     // 发布寄存有效标志
	assign o_result_data = result_data_o;       // 发布寄存整数位型
	assign o_result_tag = result_tag_o;         // 发布寄存输入身份
	assign o_fault = fault_o;                   // 发布寄存异常状态

	//-------------输出信号处理区域-------------//
	//RESULT接口
	// 输出有效只由对应的第八拍令牌决定。
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			result_valid_o <= 1'd0;             // 取消第九拍输出有效代理
		end else begin
			result_valid_o <= i_advance ? (flag_valid_pipe[7]) : result_valid_o; // 推进第九拍输出有效代理
		end
	end

	// 第九拍饱和到两个端点，范围内不作额外舍入。
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			result_data_o <= 16'd0;             // 取消第九拍输出数值代理
		end else begin
			result_data_o <= i_advance ? (reg_below_minimum ? 16'h8000 : reg_above_maximum ? 16'h7fff : reg_narrow_value) : result_data_o; // 推进第九拍输出数值代理
		end
	end

	// 输出身份取对应的最早十六位段。
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			result_tag_o <= 16'd0;              // 取消第九拍输出身份代理
		end else begin
			result_tag_o <= i_advance ? (reg_tag_pipe[127:112]) : result_tag_o; // 推进第九拍输出身份代理
		end
	end

	//RESULT接口
	// 非法指数与最小负数的异常令牌在此交给调用方。
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			fault_o <= 1'd0;                    // 取消第九拍输出故障代理
		end else begin
			fault_o <= i_advance ? (reg_fault_pipe[6]) : fault_o; // 推进第九拍输出故障代理
		end
	end

	//-------------主要任务处理区域-------------//
	// 第一拍以无符号位型保存乘积幅值，最小负数另行报告故障。
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_absolute <= 64'd0;              // 取消第一拍乘积绝对值
		end else begin
			reg_absolute <= i_advance ? (i_product[63] ? -i_product : i_product) : reg_absolute; // 推进第一拍乘积绝对值
		end
	end

	// 指数只随共同推进更新。
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_shift <= 6'd0;                  // 取消第一拍保留移位指数
		end else begin
			reg_shift <= i_advance ? (i_shift) : reg_shift; // 推进第一拍保留移位指数
		end
	end

	// 全部合法指数不含六十三。
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_bad_shift <= 1'd0;              // 取消第一拍非法指数检测
		end else begin
			reg_bad_shift <= i_advance ? (i_shift == 6'd63) : reg_bad_shift; // 推进第一拍非法指数检测
		end
	end

	// 最小负数不能在完整宽度内取正幅值。
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_bad_product <= 1'd0;            // 取消第一拍最小负整数检测
		end else begin
			reg_bad_product <= i_advance ? (i_product == 64'h8000000000000000) : reg_bad_product; // 推进第一拍最小负整数检测
		end
	end

	// 保留原始负号直到第七拍恢复符号。
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_sign_pipe <= 6'd0;              // 取消到符号恢复拍的负号流水
		end else begin
			reg_sign_pipe <= i_advance ? ({reg_sign_pipe[4:0], i_product[63]}) : reg_sign_pipe; // 推进到符号恢复拍的负号流水
		end
	end

	// 第二拍保留绝对值供下一拍提取余数。
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_absolute_delay <= 64'd0;        // 取消第二拍绝对值供掩码提取
		end else begin
			reg_absolute_delay <= i_advance ? (reg_absolute) : reg_absolute_delay; // 推进第二拍绝对值供掩码提取
		end
	end

	// 正幅值右移不会引入算术符号填充。
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_quotient <= 64'd0;              // 取消第二拍截断的正数商
		end else begin
			reg_quotient <= i_advance ? (reg_absolute >> reg_shift) : reg_quotient; // 推进第二拍截断的正数商
		end
	end

	// 零指数自然得到零掩码而不执行负指数移位。
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_mask <= 64'd0;                  // 取消第二拍余数低位掩码
		end else begin
			reg_mask <= i_advance ? (~(64'hffffffffffffffff << reg_shift)) : reg_mask; // 推进第二拍余数低位掩码
		end
	end

	// 除数右移一位给出半值，零指数对应零半值。
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_half <= 64'd0;                  // 取消第二拍除数半值
		end else begin
			reg_half <= i_advance ? ((64'h0000000000000001 << reg_shift) >> 6'b000001) : reg_half; // 推进第二拍除数半值
		end
	end

	// 非零指数标记排除整数输入被误判中点。
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_fraction_pipe <= 3'd0;          // 取消到第五拍的非零指数标记
		end else begin
			reg_fraction_pipe <= i_advance ? ({reg_fraction_pipe[1:0], reg_shift != 6'd0}) : reg_fraction_pipe; // 推进到第五拍的非零指数标记
		end
	end

	// 第三拍只保留除法丢弃的低位。
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_remainder <= 64'd0;             // 取消第三拍精确余数
		end else begin
			reg_remainder <= i_advance ? (reg_absolute_delay & reg_mask) : reg_remainder; // 推进第三拍精确余数
		end
	end

	// 半值与余数同步进入比较拍。
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_half_delay <= 64'd0;            // 取消第三拍保留半值
		end else begin
			reg_half_delay <= i_advance ? (reg_half) : reg_half_delay; // 推进第三拍保留半值
		end
	end

	// 商经过余数提取拍保持不变。
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_quotient_rem <= 64'd0;          // 取消第三拍商与余数同步
		end else begin
			reg_quotient_rem <= i_advance ? (reg_quotient) : reg_quotient_rem; // 推进第三拍商与余数同步
		end
	end

	// 第四拍区分严格大于半值的舍入情形。
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_above <= 1'd0;                  // 取消第四拍余数大于半值
		end else begin
			reg_above <= i_advance ? (reg_remainder > reg_half_delay) : reg_above; // 推进第四拍余数大于半值
		end
	end

	// 中点只在截断商为奇数时需要进位。
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_tie_odd <= 1'd0;                // 取消第四拍中点且商为奇数
		end else begin
			reg_tie_odd <= i_advance ? ((reg_remainder == reg_half_delay) & reg_quotient_rem[0]) : reg_tie_odd; // 推进第四拍中点且商为奇数
		end
	end

	// 商跟随比较标志到第四拍。
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_quotient_compare <= 64'd0;      // 取消第四拍商与比较标志同步
		end else begin
			reg_quotient_compare <= i_advance ? (reg_quotient_rem) : reg_quotient_compare; // 推进第四拍商与比较标志同步
		end
	end

	// 第五拍形成唯一的最近偶数进位。
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_increment <= 1'd0;              // 取消第五拍最近偶数进位决定
		end else begin
			reg_increment <= i_advance ? ((reg_above | reg_tie_odd) & reg_fraction_pipe[2]) : reg_increment; // 推进第五拍最近偶数进位决定
		end
	end

	// 待进位商在第五拍保持同步。
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_quotient_increment <= 64'd0;    // 取消第五拍待进位商
		end else begin
			reg_quotient_increment <= i_advance ? (reg_quotient_compare) : reg_quotient_increment; // 推进第五拍待进位商
		end
	end

	// 第六拍幅值最多增加一个单位。
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_rounded_magnitude <= 64'd0;     // 取消第六拍已舍入绝对值
		end else begin
			reg_rounded_magnitude <= i_advance ? (reg_quotient_increment + {63'd0, reg_increment}) : reg_rounded_magnitude; // 推进第六拍已舍入绝对值
		end
	end

	// 第七拍恢复负数，正负中点遵守同一个偶数规则。
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_signed_value <= 64'd0;          // 取消第七拍恢复原符号
		end else begin
			reg_signed_value <= i_advance ? (reg_sign_pipe[5] ? -reg_rounded_magnitude : reg_rounded_magnitude) : reg_signed_value; // 推进第七拍恢复原符号
		end
	end

	// 第八拍检测有符号负端边界。
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_below_minimum <= 1'd0;          // 取消第八拍负端饱和标志
		end else begin
			reg_below_minimum <= i_advance ? (reg_signed_value < 64'shffffffffffff8000) : reg_below_minimum; // 推进第八拍负端饱和标志
		end
	end

	// 第八拍检测有符号正端边界。
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_above_maximum <= 1'd0;          // 取消第八拍正端饱和标志
		end else begin
			reg_above_maximum <= i_advance ? (reg_signed_value > 64'sh0000000000007fff) : reg_above_maximum; // 推进第八拍正端饱和标志
		end
	end

	// 范围内数值保留低位而不改变符号位型。
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_narrow_value <= 16'd0;          // 取消第八拍保留范围内位型
		end else begin
			reg_narrow_value <= i_advance ? (reg_signed_value[15:0]) : reg_narrow_value; // 推进第八拍保留范围内位型
		end
	end

	// 有效令牌包括空拍并随共同使能冻结。
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			flag_valid_pipe <= 8'd0;            // 取消前八拍有效令牌
		end else begin
			flag_valid_pipe <= i_advance ? ({flag_valid_pipe[6:0], i_input_valid}) : flag_valid_pipe; // 推进前八拍有效令牌
		end
	end

	// 身份按固定十六位段随每次推进移动。
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_tag_pipe <= 128'd0;             // 取消前八拍不透明身份
		end else begin
			reg_tag_pipe <= i_advance ? ({reg_tag_pipe[111:0], i_tag}) : reg_tag_pipe; // 推进前八拍不透明身份
		end
	end

	// 故障在第一拍独立比较后合并并保持七拍。
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_fault_pipe <= 7'd0;             // 取消第二到第八拍故障标记
		end else begin
			reg_fault_pipe <= i_advance ? ({reg_fault_pipe[5:0], reg_bad_shift | reg_bad_product}) : reg_fault_pipe; // 推进第二到第八拍故障标记
		end
	end

endmodule
