`timescale 1ns / 1ps

// 动态乘积与最近偶数重定标，复用冻结舍入核，不包含 SiLU。
module road_dynamic_requant(
	input i_clk,
	input i_rstn,
	input i_input_valid,
	input signed [31:0]i_accumulator,
	input [30:0]i_multiplier,
	input [5:0]i_shift,
	input [15:0]i_tag,
	output o_input_ready,
	input i_output_ready,
	output o_output_valid,
	output signed [15:0]o_output_data,
	output [15:0]o_output_tag,
	output o_fault
);
	// 单级乘积和元数据共同冻结，防止系数切换错配。
	reg signed [63:0]reg_product;
	reg [5:0]reg_shift;
	reg [15:0]reg_tag;
	reg flag_product_valid;
	wire signed [31:0]wire_multiplier;
	wire flag_advance;
	wire flag_round_valid;
	wire [15:0]wire_round_data;
	wire [15:0]wire_round_tag;
	wire flag_round_fault;

	// 输出停顿时冻结整个算术流水；复位期间不接受传输。
	assign wire_multiplier = $signed({1'b0, i_multiplier});
	assign flag_advance = i_rstn && (!flag_round_valid || i_output_ready);
	assign o_input_ready = flag_advance;
	assign o_output_valid = i_rstn && flag_round_valid;
	assign o_output_data = wire_round_data;
	assign o_output_tag = wire_round_tag;
	assign o_fault = o_output_valid && flag_round_fault;

	// 完整有符号乘积不截断，不预先假定映射到几个 DSP。
	always @(posedge i_clk or negedge i_rstn) begin
		if (!i_rstn) begin
			reg_product <= 64'sd0;
			reg_shift <= 6'd0;
			reg_tag <= 16'd0;
			flag_product_valid <= 1'b0;
		end else if (flag_advance) begin
			flag_product_valid <= i_input_valid && o_input_ready;
			if (i_input_valid && o_input_ready) begin
				reg_product <= $signed(i_accumulator) * $signed(wire_multiplier);
				reg_shift <= i_shift;
				reg_tag <= i_tag;
			end
		end
	end

	// shift=63 沿冻结核发布故障，不将非法参数解释为合法数值。
	road_round_shift u_round(
		.i_clk(i_clk), .i_rstn(i_rstn), .i_advance(flag_advance),
		.i_input_valid(flag_product_valid), .i_product(reg_product),
		.i_shift(reg_shift), .i_tag(reg_tag),
		.o_result_valid(flag_round_valid), .o_result_data(wire_round_data),
		.o_result_tag(wire_round_tag), .o_fault(flag_round_fault)
	);
endmodule
