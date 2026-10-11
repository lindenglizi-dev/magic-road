`timescale 1ns / 1ps

////////////////////////////////////English///////////////////////////////////////
// Company:         Erie
// Engineer:        Erie
//
// Create Date:     2026/10/06 00:00:00
// Design Name:     silu_internal_probe
// Module Name:     silu_internal_probe
// Description:     spec/silu_internal_probe_spec.md
// Simulations:     tb/tb_silu_internal_probe.v
//
// Referrences:
// File Format      File Name
// 1.Document       spec/silu_internal_probe_spec.md
//
// Dependencies:
// Module Name      Version
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
// 设计名称:        silu_internal_probe
// 模块名称:        silu_internal_probe
// 模块说明:        spec/silu_internal_probe_spec.md
// 仿真工程:        tb/tb_silu_internal_probe.v
//
// 参考资料:
// 文件格式         文件名称
// 1.Document       spec/silu_internal_probe_spec.md
//
// 依赖文件:
// 模块名称         版本
// silu_shared_unit V1.0
//
// 当前版本:        V1.0
// 修订日期:        2026年10月06日
// 修订历史:
// 时间             版本        修订人            修订内容
// 2026年10月06日   V1.0        Erie              创建文件

module silu_internal_probe
(
	//-----------------全局信号-----------------//
	input i_clk,                                // 探针与SiLU共用工作时钟
	input i_rstn,                               // 外部低有效异步复位

	//----------------PROBE接口-----------------//
	output o_done,                              // 全部十八个结果已捕获
	output o_error,                             // 任一结果或装表状态异常
	output [2:0]o_phase,                        // 当前装表等待运行完成阶段
	output [5:0]o_result_count,                 // 已捕获结果数量
	output [31:0]o_checksum                     // 结果与序号动态异或摘要
);

	//---------------配置参数区域---------------//
	localparam [2:0]PHASE_LOAD = 3'd0;          // 顺序装载一千零二十四项
	localparam [2:0]PHASE_WAIT = 3'd1;          // 等待完整表状态生效
	localparam [2:0]PHASE_RUN = 3'd2;           // 连续发送并制造真实背压
	localparam [2:0]PHASE_DONE = 3'd3;          // 捕获十八项后停止

	//--------------模块实例化信号--------------//
	//silu_shared_unit--用户接口
	wire wire_table_ready;                      // DUT表项接收许可
	wire wire_input_ready;                      // DUT输入接收许可
	wire wire_output_valid;                     // DUT结果有效
	wire signed [15:0]wire_output_data;         // DUT结果数据
	wire wire_table_loaded;                     // DUT完整表状态
	wire wire_table_fault;                      // DUT装载顺序故障

	//-----------------计数信号-----------------//
	reg [10:0]cnt_table = 11'd0;                // 当前装载地址
	reg [5:0]cnt_input = 6'd0;                  // 已发送输入数量
	reg [5:0]cnt_result = 6'd0;                 // 已捕获输出数量
	reg [7:0]cnt_cycle = 8'd0;                  // 背压节拍生成计数

	//----------------寄存器信号----------------//
	reg [2:0]reg_phase = PHASE_LOAD;            // 探针阶段状态
	reg reg_table_valid = 1'b0;                 // 内部寄存表valid
	reg [9:0]reg_table_addr = 10'd0;            // 内部寄存表地址
	reg signed [15:0]reg_table_data = -16'sd512; // 内部寄存表数据
	reg reg_input_valid = 1'b0;                 // 内部寄存输入valid
	reg signed [15:0]reg_input_data = -16'sd4096; // 内部寄存输入样本
	reg reg_output_ready = 1'b0;                // 内部寄存输出ready
	reg [31:0]reg_checksum = 32'd0;             // 已捕获结果摘要
	reg reg_error = 1'b0;                       // 自检错误保持位

	//-----------------标志信号-----------------//
	wire flag_table_transfer;                   // 表项握手事件
	wire flag_input_transfer;                   // 输入握手事件
	wire flag_output_transfer;                  // 输出握手事件

	//-----------------输出信号-----------------//
	wire done_o;                                // 完成状态内部桥
	wire error_o;                               // 错误状态内部桥
	wire [2:0]phase_o;                          // 阶段状态内部桥
	wire [5:0]result_count_o;                   // 结果计数内部桥
	wire [31:0]checksum_o;                      // 摘要内部桥

	//---------------其他信号连线---------------//
	//握手事件
	assign flag_table_transfer = reg_table_valid && wire_table_ready;
	assign flag_input_transfer = reg_input_valid && wire_input_ready;
	assign flag_output_transfer = wire_output_valid && reg_output_ready;

	//---------------输出信号连线---------------//
	//PROBE接口
	assign done_o = (reg_phase == PHASE_DONE);
	assign error_o = reg_error;
	assign phase_o = reg_phase;
	assign result_count_o = cnt_result;
	assign checksum_o = reg_checksum;
	assign o_done = done_o;
	assign o_error = error_o;
	assign o_phase = phase_o;
	assign o_result_count = result_count_o;
	assign o_checksum = checksum_o;

	//-------------主要任务处理区域-------------//
	//阶段控制在完整装表后运行固定样本并等待全部结果。
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_phase <= PHASE_LOAD;
		end else begin
			case(reg_phase)
				PHASE_LOAD: begin
					if(flag_table_transfer && (reg_table_addr == 10'd1023))begin
						reg_phase <= PHASE_WAIT;
					end
				end
				PHASE_WAIT: begin
					if(wire_table_loaded)begin
						reg_phase <= PHASE_RUN;
					end
				end
				PHASE_RUN: begin
					if(flag_output_transfer && (cnt_result == 6'd17))begin
						reg_phase <= PHASE_DONE;
					end
				end
				default: reg_phase <= PHASE_DONE;
			endcase
		end
	end

	//装表接口由寄存器驱动，表值等于地址减去五百一十二。
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_table_valid <= 1'b0;
			reg_table_addr <= 10'd0;
			reg_table_data <= -16'sd512;
			cnt_table <= 11'd0;
		end else if(reg_phase == PHASE_LOAD)begin
			reg_table_valid <= 1'b1;
			if(flag_table_transfer)begin
				cnt_table <= cnt_table + 11'd1;
				if(reg_table_addr == 10'd1023)begin
					reg_table_valid <= 1'b0;
				end else begin
					reg_table_addr <= reg_table_addr + 10'd1;
					reg_table_data <= reg_table_data + 16'sd1;
				end
			end
		end else begin
			reg_table_valid <= 1'b0;
		end
	end

	//运行阶段保持valid，只有真实输入握手才切换下一个固定样本。
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_input_valid <= 1'b0;
			reg_input_data <= -16'sd4096;
			cnt_input <= 6'd0;
		end else if(reg_phase == PHASE_WAIT && wire_table_loaded)begin
			reg_input_valid <= 1'b1;
			reg_input_data <= -16'sd4096;
		end else if(reg_phase == PHASE_RUN && flag_input_transfer)begin
			cnt_input <= cnt_input + 6'd1;
			case(cnt_input)
				6'd0: reg_input_data <= -16'sd2048;
				6'd1: reg_input_data <= -16'sd2047;
				6'd2: reg_input_data <= -16'sd7;
				6'd3: reg_input_data <= -16'sd6;
				6'd4: reg_input_data <= -16'sd5;
				6'd5: reg_input_data <= -16'sd4;
				6'd6: reg_input_data <= -16'sd3;
				6'd7: reg_input_data <= -16'sd2;
				6'd8: reg_input_data <= -16'sd1;
				6'd9: reg_input_data <= 16'sd0;
				6'd10: reg_input_data <= 16'sd1;
				6'd11: reg_input_data <= 16'sd2;
				6'd12: reg_input_data <= 16'sd3;
				6'd13: reg_input_data <= 16'sd4;
				6'd14: reg_input_data <= 16'sd2047;
				6'd15: reg_input_data <= 16'sd2048;
				6'd16: reg_input_data <= 16'sd4096;
				default: begin
					reg_input_valid <= 1'b0;
					reg_input_data <= 16'sd0;
				end
			endcase
		end
	end

	//周期三插入真实输出背压，其余周期允许流水连续推进。
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			cnt_cycle <= 8'd0;
			reg_output_ready <= 1'b0;
		end else if(reg_phase == PHASE_RUN)begin
			cnt_cycle <= cnt_cycle + 8'd1;
			reg_output_ready <= (cnt_cycle[2:0] != 3'd3);
		end else begin
			cnt_cycle <= 8'd0;
			reg_output_ready <= 1'b0;
		end
	end

	//每个输出握手按Python合同核对，并将数据纳入可观测摘要。
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			cnt_result <= 6'd0;
			reg_checksum <= 32'd0;
			reg_error <= 1'b0;
		end else begin
			if(wire_table_fault)begin
				reg_error <= 1'b1;
			end
			if(flag_output_transfer)begin
				reg_checksum <= reg_checksum ^ {{16{wire_output_data[15]}}, wire_output_data} ^ {26'd0, cnt_result};
				cnt_result <= cnt_result + 6'd1;
				case(cnt_result)
					6'd0: if(wire_output_data != 16'sd0) reg_error <= 1'b1;
					6'd1: if(wire_output_data != 16'sd0) reg_error <= 1'b1;
					6'd2: if(wire_output_data != -16'sd512) reg_error <= 1'b1;
					6'd3: if(wire_output_data != -16'sd2) reg_error <= 1'b1;
					6'd4: if(wire_output_data != -16'sd2) reg_error <= 1'b1;
					6'd5: if(wire_output_data != -16'sd1) reg_error <= 1'b1;
					6'd6: if(wire_output_data != -16'sd1) reg_error <= 1'b1;
					6'd7: if(wire_output_data != -16'sd1) reg_error <= 1'b1;
					6'd8: if(wire_output_data != 16'sd0) reg_error <= 1'b1;
					6'd9: if(wire_output_data != 16'sd0) reg_error <= 1'b1;
					6'd10: if(wire_output_data != 16'sd0) reg_error <= 1'b1;
					6'd11: if(wire_output_data != 16'sd0) reg_error <= 1'b1;
					6'd12: if(wire_output_data != 16'sd0) reg_error <= 1'b1;
					6'd13: if(wire_output_data != 16'sd1) reg_error <= 1'b1;
					6'd14: if(wire_output_data != 16'sd1) reg_error <= 1'b1;
					6'd15: if(wire_output_data != 16'sd2047) reg_error <= 1'b1;
					6'd16: if(wire_output_data != 16'sd2048) reg_error <= 1'b1;
					6'd17: if(wire_output_data != 16'sd4096) reg_error <= 1'b1;
					default: reg_error <= 1'b1;
				endcase
			end
		end
	end

	//--------------模块实例化区域--------------//
	//冻结候选保持原接口和单个PH1P ERAM，不在探针内替换存储。
	silu_shared_unit silu_shared_unit_Inst_stage( // 实例化冻结SiLU候选
		.i_clk(i_clk),                          // 共用唯一工作时钟
		.i_rstn(i_rstn),                        // 共用外部低有效复位
		.i_table_valid(reg_table_valid),        // 内部寄存装表valid
		.i_table_addr(reg_table_addr),          // 内部寄存装表地址
		.i_table_data(reg_table_data),          // 内部寄存装表数据
		.i_input_valid(reg_input_valid),        // 内部寄存样本valid
		.i_input_data(reg_input_data),          // 内部寄存样本数据
		.i_output_ready(reg_output_ready),      // 内部寄存背压ready
		.o_table_ready(wire_table_ready),       // 观察装表接收许可
		.o_input_ready(wire_input_ready),       // 观察输入接收许可
		.o_output_valid(wire_output_valid),     // 捕获结果valid
		.o_output_data(wire_output_data),       // 捕获结果数据
		.o_table_loaded(wire_table_loaded),     // 观察完整表状态
		.o_table_fault(wire_table_fault)        // 观察装载错误状态
	);

endmodule
