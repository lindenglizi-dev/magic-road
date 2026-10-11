`timescale 1ns / 1ps

////////////////////////////////////English///////////////////////////////////////
// Company:         Erie
// Engineer:        Erie
//
// Create Date:     2026/10/04 00:00:00
// Design Name:     silu_shared_unit
// Module Name:     silu_shared_unit
// Description:     description/silu_shared_unit_Design.pdf
// Simulations:     testbench/vivado/2021.1/silu_shared_unit
//
// Referrences:
// File Format      File Name
// 1.Book           cnn/integer.py
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
// 设计名称:        silu_shared_unit
// 模块名称:        silu_shared_unit
// 模块说明:        Description/silu_shared_unit_Design.pdf
// 仿真工程:        TestBench/Vivado/2021.1/silu_shared_unit
//
// 参考资料:
// 文件格式         文件名称
// 1.Book           cnn/integer.py
//
// 依赖文件:
// 模块名称         版本
//
// 当前版本:        V1.0
// 修订日期:        2026年10月04日
// 修订历史:
// 时间             版本        修订人            修订内容
// 2026年10月04日   V1.0        Erie              创建文件

module silu_shared_unit
(
	//-----------------全局信号-----------------//
	input i_clk,                                // 单一工作时钟
	input i_rstn,                               // 低有效异步复位

	//-----------------用户接口-----------------//

	//TABLE接口
	input i_table_valid,                        // 运行时表项有效
	input [9:0]i_table_addr,                    // 严格递增装载地址
	input signed [15:0]i_table_data,            // 有符号Q7.8表项
	input i_input_valid,                        // 推理输入有效
	input signed [15:0]i_input_data,            // 有符号Q7.8输入
	input i_output_ready,                       // 下游结果接收能力
	output o_table_ready,                       // 当前表项接收许可
	output o_input_ready,                       // 当前输入接收许可
	output o_output_valid,                      // SiLU结果有效
	output signed [15:0]o_output_data,          // 有符号Q7.8结果
	output o_table_loaded,                      // 完整表已激活
	output o_table_fault                        // 装载顺序故障
);

	//---------------配置参数区域---------------//
	localparam signed [15:0]LOWER_LIMIT = -16'sd2048; // 负尾硬连线边界
	localparam signed [15:0]UPPER_LIMIT = 16'sd2048; // 正尾恒等边界
	localparam signed [15:0]UPPER_VALUE = 16'sd2047; // 地址上端点常量
	localparam [9:0]TABLE_LAST_ADDR = 10'd1023; // 完整表最后地址

	//--------------模块实例化信号--------------//
	//PH1P_LOGIC_ERAM--用户接口
	wire [19:0]wire_table_read_data;            // PH1P二十位物理读数据

	//-----------------计数信号-----------------//
	reg [10:0]cnt_table_expected = 0;           // 下一合法装载地址
	reg [2:0]cnt_pending = 0;                   // 已接收但未返回样本数

	//----------------寄存器信号----------------//
	reg signed [15:0]reg_input_raw = 0;         // 输入级原始样本
	reg signed [15:0]reg_input_quotient = 0;    // 向负无穷取整商
	reg [1:0]reg_input_remainder = 0;           // 除四非负余数
	reg signed [15:0]reg_round_raw = 0;         // 舍入判定级原始样本
	reg signed [15:0]reg_round_quotient = 0;    // 舍入判定级商
	reg signed [15:0]reg_value_raw = 0;         // 舍入结果级原始样本
	reg signed [15:0]reg_rounded_value = 0;     // 最近偶数有符号商
	reg signed [15:0]reg_address_raw = 0;       // 查找地址级原始样本
	reg signed [15:0]reg_lookup_address = 0;    // 完整黄金查找地址
	reg signed [15:0]reg_ram_raw = 0;           // PH1P读返回级原始样本
	reg signed [15:0]reg_ram_address = 0;       // PH1P读返回级完整地址

	//-----------------标志信号-----------------//
	reg flag_input_valid = 0;                   // 输入算术级令牌
	reg flag_input_lower = 0;                   // 输入命中负尾
	reg flag_input_upper = 0;                   // 输入命中正尾
	reg flag_round_valid = 0;                   // 舍入判定级令牌
	reg flag_round_lower = 0;                   // 舍入级负尾标志
	reg flag_round_upper = 0;                   // 舍入级正尾标志
	reg flag_round_above = 0;                   // 余数超过半数
	reg flag_round_tie = 0;                     // 余数等于半数
	reg flag_round_odd = 0;                     // 商最低位为奇数
	reg flag_value_valid = 0;                   // 舍入结果级令牌
	reg flag_value_lower = 0;                   // 结果级负尾标志
	reg flag_value_upper = 0;                   // 结果级正尾标志
	reg flag_address_valid = 0;                 // 地址级令牌
	reg flag_address_lower = 0;                 // 地址级负尾标志
	reg flag_address_upper = 0;                 // 地址级正尾标志
	reg flag_ram_valid = 0;                     // PH1P读返回级令牌
	reg flag_ram_lower = 0;                     // PH1P读返回级负尾标志
	reg flag_ram_upper = 0;                     // PH1P读返回级正尾标志
	wire flag_pipeline_enable;                  // 全流水统一时钟使能
	wire flag_input_transfer;                   // 输入握手事件
	wire flag_output_transfer;                  // 输出握手事件
	wire flag_table_transfer;                   // 表项握手事件
	wire flag_table_restart;                    // 地址零整表重启事件
	wire flag_table_write_enable;               // 合法表项物理写使能

	//-----------------其他信号-----------------//
	wire [9:0]wire_table_address;               // PH1P复用装载与查表地址
	wire [19:0]wire_table_write_data;           // PH1P二十位物理写数据

	//-----------------输出信号-----------------//
	//用户接口
	wire table_ready_o;                         // 表装载ready内部连线
	wire input_ready_o;                         // 推理输入ready内部连线
	reg output_valid_o = 0;                     // 结果valid输出缓存
	reg signed [15:0]output_data_o = 0;         // SiLU结果输出缓存
	reg table_loaded_o = 0;                     // 完整表状态缓存
	reg table_fault_o = 0;                      // 装载故障状态缓存

	//---------------其他信号连线---------------//
	//其他信号连线
	assign table_ready_o = (cnt_pending == 3'd0) && ((i_table_addr == 10'd0) || ((~table_loaded_o) && (~table_fault_o))); // 空流水中接收重启或健康续载
	assign input_ready_o = flag_pipeline_enable && table_loaded_o && (~i_table_valid); // 已装表且无装载请求时接收样本
	assign flag_input_transfer = i_input_valid && input_ready_o; // 输入valid与ready共同确认接收
	assign flag_output_transfer = output_valid_o && i_output_ready; // 结果valid与ready共同确认发送
	assign flag_table_transfer = i_table_valid && table_ready_o; // 表valid与ready共同确认写入
	assign flag_table_restart = flag_table_transfer && (i_table_addr == 10'd0); // 地址零握手重建完整映像
	assign flag_table_write_enable = flag_table_transfer && ((i_table_addr == 10'd0) || (i_table_addr == cnt_table_expected[9:0])); // 错序握手不污染物理表
	assign wire_table_address = flag_table_transfer ? i_table_addr : reg_lookup_address[9:0]; // 装载握手优先占用单端口地址
	assign wire_table_write_data = {{4{i_table_data[15]}}, i_table_data}; // 表项符号扩展到二十位物理宽度

	//其他信号连线
	assign flag_pipeline_enable = (~output_valid_o) | i_output_ready; // 下游阻塞冻结全流水

	//---------------输出信号连线---------------//
	//用户接口
	assign o_table_ready = table_ready_o;       // 表装载接收许可
	assign o_input_ready = input_ready_o;       // 推理样本接收许可
	assign o_output_valid = output_valid_o;     // 结果有效桥接
	assign o_output_data = output_data_o;       // 结果数据桥接
	assign o_table_loaded = table_loaded_o;     // 完整表状态桥接
	assign o_table_fault = table_fault_o;       // 装载故障状态桥接

	//-------------输出信号处理区域-------------//
	//用户接口
	//全局使能开放时推进结果有效令牌
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			output_valid_o <= 1'b0;             // 复位撤销结果有效
		end else begin
			output_valid_o <= flag_pipeline_enable ? flag_ram_valid : output_valid_o; // 使能时推进结果令牌
		end
	end

	//时钟读表并在同级选择两个硬连线尾部
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			output_data_o <= 16'sd0;
		end else if(flag_pipeline_enable == 1'b1)begin
			if(flag_ram_valid == 1'b0)begin
				output_data_o <= 16'sd0;
			end else if(flag_ram_lower == 1'b1)begin
				output_data_o <= 16'sd0;
			end else if(flag_ram_upper == 1'b1)begin
				output_data_o <= reg_ram_raw;
			end else if(reg_ram_address == 16'sd1024)begin
				output_data_o <= UPPER_VALUE;
			end else begin
				output_data_o <= wire_table_read_data[15:0];
			end
		end else begin
			output_data_o <= output_data_o;
		end
	end

	//完整表状态仅由复位、重启、故障或最后合法表项改变
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			table_loaded_o <= 1'b0;                // 复位要求重新装载整表
		end else if(flag_table_restart == 1'b1)begin
			table_loaded_o <= 1'b0;                // 地址零握手立即撤销旧表状态
		end else if(flag_table_transfer == 1'b1)begin
			if(i_table_addr != cnt_table_expected[9:0])begin
				table_loaded_o <= 1'b0;            // 错序地址保持失效
			end else if(i_table_addr == TABLE_LAST_ADDR)begin
				table_loaded_o <= 1'b1;            // 最后合法表项完成整表
			end else begin
				table_loaded_o <= table_loaded_o;  // 中间合法表项保持状态
			end
		end else begin
			table_loaded_o <= table_loaded_o;      // 无表握手时保持状态
		end
	end

	//装载错误保持到下一次地址零重启
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			table_fault_o <= 1'b0;                 // 复位清除装载故障状态
		end else if(flag_table_restart == 1'b1)begin
			table_fault_o <= 1'b0;                 // 地址零握手恢复装载器
		end else if((flag_table_transfer == 1'b1) && (i_table_addr != cnt_table_expected[9:0]))begin
			table_fault_o <= 1'b1;                 // 已接收错序地址后保持故障
		end else begin
			table_fault_o <= table_fault_o;        // 其他周期保持故障状态
		end
	end

	//-------------主要任务处理区域-------------//
	//PH1P同步读出拍保留原样本供正尾恒等旁路
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_ram_raw <= 16'sd0;              // 复位撤销读返回原样本
		end else begin
			reg_ram_raw <= flag_pipeline_enable ? reg_address_raw : reg_ram_raw; // 使能时延迟原样本
		end
	end

	//PH1P同步读出拍保留完整地址供上端点常量选择
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_ram_address <= 16'sd0;             // 复位撤销读返回地址
		end else begin
			reg_ram_address <= flag_pipeline_enable ? reg_lookup_address : reg_ram_address; // 使能时延迟查表地址
		end
	end

	//PH1P同步读出拍延迟有效令牌
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			flag_ram_valid <= 1'b0;             // 复位撤销读返回令牌
		end else begin
			flag_ram_valid <= flag_pipeline_enable ? flag_address_valid : flag_ram_valid; // 使能时延迟有效令牌
		end
	end

	//PH1P同步读出拍延迟负尾旁路标志
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			flag_ram_lower <= 1'b0;             // 复位撤销读返回负尾标志
		end else begin
			flag_ram_lower <= flag_pipeline_enable ? flag_address_lower : flag_ram_lower; // 使能时延迟负尾标志
		end
	end

	//PH1P同步读出拍延迟正尾旁路标志
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			flag_ram_upper <= 1'b0;             // 复位撤销读返回正尾标志
		end else begin
			flag_ram_upper <= flag_pipeline_enable ? flag_address_upper : flag_ram_upper; // 使能时延迟正尾标志
		end
	end

	//跟踪下一严格递增地址
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			cnt_table_expected <= 11'd0;           // 复位期待地址零
		end else if(flag_table_restart == 1'b1)begin
			cnt_table_expected <= 11'd1;           // 地址零后期待地址一
		end else if(flag_table_transfer == 1'b1)begin
			if(i_table_addr != cnt_table_expected[9:0])begin
				cnt_table_expected <= 11'd0;       // 故障后只允许地址零重启
			end else if(i_table_addr == TABLE_LAST_ADDR)begin
				cnt_table_expected <= 11'd0;       // 完整表后只允许地址零重启
			end else begin
				cnt_table_expected <= cnt_table_expected + 11'd1; // 合法中间项推进地址
			end
		end else begin
			cnt_table_expected <= cnt_table_expected; // 无表握手时保持地址
		end
	end

	//守恒计数确保重载只在所有已接收样本返回后开放
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			cnt_pending <= 3'd0;                   // 复位取消所有在途样本
		end else begin
			case({flag_input_transfer, flag_output_transfer})
				2'b10: cnt_pending <= cnt_pending + 3'd1; // 仅输入握手增加在途数
				2'b01: cnt_pending <= cnt_pending - 3'd1; // 仅输出握手减少在途数
				default: cnt_pending <= cnt_pending;      // 同进同出或无传输保持计数
			endcase
		end
	end

	//输入级记录原始样本
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_input_raw <= 16'sd0;            // 复位撤销输入原样本
		end else begin
			reg_input_raw <= flag_pipeline_enable ? i_input_data : reg_input_raw; // 使能时接收输入原样本
		end
	end

	//算术右移形成向负无穷取整商
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_input_quotient <= 16'sd0;
		end else if(flag_pipeline_enable == 1'b1)begin
			reg_input_quotient <= {{2{i_input_data[15]}}, i_input_data[15:2]};
		end else begin
			reg_input_quotient <= reg_input_quotient;
		end
	end

	//低两位是对应非负除四余数
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_input_remainder <= 2'd0;        // 复位撤销输入余数
		end else begin
			reg_input_remainder <= flag_pipeline_enable ? i_input_data[1:0] : reg_input_remainder; // 使能时保存低两位余数
		end
	end

	//输入握手生成首级有效令牌
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			flag_input_valid <= 1'b0;
		end else if(flag_pipeline_enable == 1'b1)begin
			flag_input_valid <= flag_input_transfer;
		end else begin
			flag_input_valid <= flag_input_valid;
		end
	end

	//首级标记负尾绕过
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			flag_input_lower <= 1'b0;
		end else if(flag_pipeline_enable == 1'b1)begin
			flag_input_lower <= (i_input_data <= LOWER_LIMIT);
		end else begin
			flag_input_lower <= flag_input_lower;
		end
	end

	//首级标记正尾恒等
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			flag_input_upper <= 1'b0;
		end else if(flag_pipeline_enable == 1'b1)begin
			flag_input_upper <= (i_input_data >= UPPER_LIMIT);
		end else begin
			flag_input_upper <= flag_input_upper;
		end
	end

	//以下寄存器共享同一使能并逐级传递原始值和尾部标志
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_round_raw <= 16'sd0;            // 复位撤销舍入级原样本
		end else begin
			reg_round_raw <= flag_pipeline_enable ? reg_input_raw : reg_round_raw; // 使能时推进舍入级原样本
		end
	end

	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_round_quotient <= 16'sd0;       // 复位撤销舍入级商
		end else begin
			reg_round_quotient <= flag_pipeline_enable ? reg_input_quotient : reg_round_quotient; // 使能时推进舍入级商
		end
	end

	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			flag_round_valid <= 1'b0;           // 复位撤销舍入级令牌
		end else begin
			flag_round_valid <= flag_pipeline_enable ? flag_input_valid : flag_round_valid; // 使能时推进舍入级令牌
		end
	end

	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			flag_round_lower <= 1'b0;           // 复位撤销舍入级负尾标志
		end else begin
			flag_round_lower <= flag_pipeline_enable ? flag_input_lower : flag_round_lower; // 使能时推进负尾标志
		end
	end

	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			flag_round_upper <= 1'b0;           // 复位撤销舍入级正尾标志
		end else begin
			flag_round_upper <= flag_pipeline_enable ? flag_input_upper : flag_round_upper; // 使能时推进正尾标志
		end
	end

	//独立预译码使舍入加法保持三操作预算
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			flag_round_above <= 1'b0;
		end else if(flag_pipeline_enable == 1'b1)begin
			flag_round_above <= (reg_input_remainder == 2'd3);
		end else begin
			flag_round_above <= flag_round_above;
		end
	end

	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			flag_round_tie <= 1'b0;
		end else if(flag_pipeline_enable == 1'b1)begin
			flag_round_tie <= (reg_input_remainder == 2'd2);
		end else begin
			flag_round_tie <= flag_round_tie;
		end
	end

	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			flag_round_odd <= 1'b0;             // 复位撤销商奇偶标志
		end else begin
			flag_round_odd <= flag_pipeline_enable ? reg_input_quotient[0] : flag_round_odd; // 使能时推进商奇偶标志
		end
	end

	//最近偶数商只在超过半数或奇数平局时加一
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_rounded_value <= 16'sd0;
		end else if(flag_pipeline_enable == 1'b1)begin
			reg_rounded_value <= reg_round_quotient + {{15{1'b0}}, (flag_round_above | (flag_round_tie & flag_round_odd))};
		end else begin
			reg_rounded_value <= reg_rounded_value;
		end
	end

	//舍入结果级传递原始值与控制
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_value_raw <= 16'sd0;            // 复位撤销结果级原样本
		end else begin
			reg_value_raw <= flag_pipeline_enable ? reg_round_raw : reg_value_raw; // 使能时推进结果级原样本
		end
	end

	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			flag_value_valid <= 1'b0;           // 复位撤销结果级令牌
		end else begin
			flag_value_valid <= flag_pipeline_enable ? flag_round_valid : flag_value_valid; // 使能时推进结果级令牌
		end
	end

	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			flag_value_lower <= 1'b0;           // 复位撤销结果级负尾标志
		end else begin
			flag_value_lower <= flag_pipeline_enable ? flag_round_lower : flag_value_lower; // 使能时推进结果级负尾标志
		end
	end

	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			flag_value_upper <= 1'b0;           // 复位撤销结果级正尾标志
		end else begin
			flag_value_upper <= flag_pipeline_enable ? flag_round_upper : flag_value_upper; // 使能时推进结果级正尾标志
		end
	end

	//黄金地址在独立寄存级增加512偏移
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_lookup_address <= 16'sd0;
		end else if(flag_pipeline_enable == 1'b1)begin
			reg_lookup_address <= reg_rounded_value + 16'sd512;
		end else begin
			reg_lookup_address <= reg_lookup_address;
		end
	end

	//地址级传递最终选择所需信息
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_address_raw <= 16'sd0;          // 复位撤销地址级原样本
		end else begin
			reg_address_raw <= flag_pipeline_enable ? reg_value_raw : reg_address_raw; // 使能时推进地址级原样本
		end
	end

	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			flag_address_valid <= 1'b0;         // 复位撤销地址级令牌
		end else begin
			flag_address_valid <= flag_pipeline_enable ? flag_value_valid : flag_address_valid; // 使能时推进地址级令牌
		end
	end

	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			flag_address_lower <= 1'b0;         // 复位撤销地址级负尾标志
		end else begin
			flag_address_lower <= flag_pipeline_enable ? flag_value_lower : flag_address_lower; // 使能时推进地址级负尾标志
		end
	end

	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			flag_address_upper <= 1'b0;         // 复位撤销地址级正尾标志
		end else begin
			flag_address_upper <= flag_pipeline_enable ? flag_value_upper : flag_address_upper; // 使能时推进地址级正尾标志
		end
	end

	//--------------模块实例化区域--------------//
	//单个二十千比特PH1P存储承载一千零二十四个有符号表项
	PH1P_LOGIC_ERAM #(
		.DATA_WIDTH_A(20),                      // DATA_WIDTH_A参数映射为20
		.DATA_WIDTH_B(20),                      // DATA_WIDTH_B参数映射为20
		.ADDR_WIDTH_A(10),                      // ADDR_WIDTH_A参数映射为10
		.ADDR_WIDTH_B(10),                      // ADDR_WIDTH_B参数映射为10
		.DATA_DEPTH_A(1024),                    // DATA_DEPTH_A参数映射为1024
		.DATA_DEPTH_B(1024),                    // DATA_DEPTH_B参数映射为1024
		.BYTE_ENABLE(0),                        // BYTE_ENABLE参数映射为0
		.BYTE_A(1),                             // BYTE_A参数映射为1
		.BYTE_B(1),                             // BYTE_B参数映射为1
		.MODE("SP"),                            // MODE参数映射为"SP"
		.REGMODE_A("NOREG"),                    // REGMODE_A参数映射为"NOREG"
		.REGMODE_B("NOREG"),                    // REGMODE_B参数映射为"NOREG"
		.WRITEMODE_A("NORMAL"),                 // WRITEMODE_A参数映射为"NORMAL"
		.WRITEMODE_B("NORMAL"),                 // WRITEMODE_B参数映射为"NORMAL"
		.RESETMODE_A("ASYNC"),                  // RESETMODE_A参数映射为"ASYNC"
		.RESETMODE_B("ASYNC"),                  // RESETMODE_B参数映射为"ASYNC"
		.OREGSET_A("RESET"),                    // OREGSET_A参数映射为"RESET"
		.OREGSET_B("RESET"),                    // OREGSET_B参数映射为"RESET"
		.SSROVERCE("DISABLE"),                  // SSROVERCE参数映射为"DISABLE"
		.ECC_DECODE("DISABLE"),                 // ECC_DECODE参数映射为"DISABLE"
		.ECC_ENCODE("DISABLE"),                 // ECC_ENCODE参数映射为"DISABLE"
		.ASYNC_RESET_RELEASE_A("ASYNC"),        // ASYNC_RESET_RELEASE_A参数映射为"ASYNC"
		.ASYNC_RESET_RELEASE_B("ASYNC"),        // ASYNC_RESET_RELEASE_B参数映射为"ASYNC"
		.CLKMODE("ASYNC"),                      // CLKMODE参数映射为"ASYNC"
		.DEBUGGABLE("NO"),                      // DEBUGGABLE参数映射为"NO"
		.PACKABLE("NO"),                        // PACKABLE参数映射为"NO"
		.FORCE_KEEP("ON"),                      // FORCE_KEEP参数映射为"ON"
		.INIT_FILE("NONE"),                     // INIT_FILE参数映射为"NONE"
		.FILL_ALL("NONE"),                      // FILL_ALL参数映射为"NONE"
		.IMPLEMENT("20K")                       // IMPLEMENT参数映射为"20K"
	)PH1P_LOGIC_ERAM_Inst_silu_table(
		.dia(wire_table_write_data),            // A口接收符号扩展表项
		.addra(wire_table_address),             // A口复用装载与查找地址
		.cea(flag_pipeline_enable),             // 与响应控制同步冻结；空流水合法装载时使能为一
		.ocea(1'b0),                            // A口不使用额外输出寄存器
		.clka(i_clk),                           // A口使用模块工作时钟
		.wea(flag_table_write_enable),          // 仅顺序合法表握手写入
		.rsta(1'b0),                            // RAM内容不参与模块复位
		.bea(1'b0),                             // 禁用字节写使能
		.dib(20'd0),                            // B口写数据固定为零
		.addrb(10'd0),                          // B口地址固定为零
		.ceb(1'b0),                             // B口完全关闭
		.oceb(1'b0),                            // B口输出时钟关闭
		.clkb(i_clk),                           // B口连接同一时钟
		.web(1'b0),                             // B口禁止写入
		.rstb(1'b0),                            // B口复位保持无效
		.beb(1'b0),                             // B口字节使能关闭
		.ecc_sbiterrinj(1'b0),                  // 关闭单比特错误注入
		.ecc_dbiterrinj(1'b0),                  // 关闭双比特错误注入
		.doa(wire_table_read_data),             // A口同步读出表项
		.dob(),                                 // B口读数据未使用
		.ecc_sbiterr(),                         // 本原型不使用ECC状态
		.ecc_dbiterr()                          // 本原型不使用ECC状态
	);

endmodule
