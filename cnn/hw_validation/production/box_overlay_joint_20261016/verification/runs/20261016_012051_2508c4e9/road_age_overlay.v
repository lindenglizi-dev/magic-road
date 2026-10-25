`timescale 1ns / 1ps

// Company: RoadYOLO
// Engineer: C8
// Create Date: 2026-10-15
// Design Name: Fixed result-age text
// Module Name: road_age_overlay
// Description: Eleven fixed glyph cells with frame-latched age and live draw permission.
// Simulations: ../tests/tb_age_overlay.v
// Referrences: ../interfaces.json
// Dependencies: Existing fixed-row diagnostic glyph mechanism
// Version: V1.0
// Revision Date: 2026-10-15
// History: Create file
// 版权归属: RoadYOLO
// 开发人员: C8
// 创建日期: 2026-10-15
// 设计名称: 固定结果年龄文字
// 模块名称: road_age_overlay
// 模块说明: 帧边界锁定十一字符，撤框许可不经文字寄存器
// 仿真工程: ../tests/tb_age_overlay.v
// 参考资料: ../interfaces.json
// 依赖文件: 既有固定行点阵机制
// 当前版本: V1.0
// 修订日期: 2026-10-15
// 修订历史: 创建文件
module road_age_overlay (
	input         i_clk,                  // HDMI像素时钟，标称75MHz
	input         i_rstn,                 // 已在像素域同步释放的共同复位
	input         i_sof,                  // 消隐内单拍边界，和表切换使用同一事件
	input         i_vsync,                // 与原图对齐的垂直同步
	input         i_hsync,                // 与原图对齐的水平同步
	input         i_de,                   // 当前原图有效像素
	input  [23:0] i_rgb,                  // 文字空点保留的原图颜色
	input  [63:0] i_age_upper_ms,         // 完整表保守年龄，未知为全一
	input         i_table_draw_valid,     // 实时安全许可，不能从显示文字推导
	output        o_vsync,                // 等延迟一拍的垂直同步
	output        o_hsync,                // 等延迟一拍的水平同步
	output        o_de,                   // 等延迟一拍的有效像素
	output [23:0] o_rgb,                  // 白色字形覆盖，其余原图透传
	output        o_draw_permit           // 立即反映许可撤销，不等下一SOF
);
	//---------------计数信号---------------//
	// 有效像素坐标只由原视频推进，不反压原链。
	reg [10:0] cnt_x = 0;                  // 首个有效像素使用横坐标零
	reg [9:0]  cnt_y = 0;                  // 有效行结束后才递增纵坐标

	//--------------寄存器信号--------------//
	// 帧内文字保持，数值与有效性一起切换。
	reg [15:0] reg_decimal_digits = 0;      // 千百十个位，合法范围各为零至九
	reg flag_age_known = 0;                // 未知/超四位时使用INVALID字符
	reg flag_latch_pending = 0;            // 延后一消隐拍观察同SOF的新活动表
	reg flag_de_previous = 0;              // 检测一行有效区的结束

	//---------------译码信号---------------//
	// 仅对四位范围作常数十进制转换，没有64位除法器。
	wire [13:0] dec_thousands;             // 已知年龄的千位商
	wire [13:0] dec_hundreds;              // 去掉更高位后的百位
	wire [13:0] dec_tens;                  // 去掉更高位后的十位
	wire [13:0] dec_units;                 // 个位余数
	wire [7:0] dec_local_x;                // 固定文字区的局部横向偏移
	wire [4:0] dec_cell;                   // 只使用前十一个固定字符单元
	wire [3:0] dec_cell_x;                 // 每单元十二像素含两像素字间距
	wire [3:0] dec_local_y;                // 十六像素高的两倍行点阵
	wire [2:0] dec_font_row;               // 顶部行零，最后一行为六
	wire [2:0] dec_font_column;            // 左列零，最后一列为四
	reg  [7:0] dec_character;              // 固定字符串位置或四个数字的ASCII
	reg [34:0] dec_bitmap;                 // 七行五列；顶行占位34至30
	wire [5:0] dec_bit_index;              // 仅在点阵范围内使用的打包位索引
	wire flag_text_pixel;                 // 真正有墨点的像素，不涂整块背景
	reg [23:0] dec_rgb;                    // 文字与原图合成的当前颜色

	//---------------输出信号---------------//
	// 颜色和视频同步共享一个寄存边界。
	reg [23:0] rgb_o = 0;                  // 本拍输出上一输入像素
	reg vsync_o = 0;                       // 对应输出像素的VS
	reg hsync_o = 0;                       // 对应输出像素的HS
	reg de_o = 0;                          // 对应输出像素的DE

	//-------------其他信号连线-------------//
	// 范围判断在锁存处完成；低十四位不足以把未知值伪装成有效年龄。
	assign dec_thousands = i_age_upper_ms[13:0] / 14'd1000;                  // 四位数最高位
	assign dec_hundreds = (i_age_upper_ms[13:0] / 14'd100) % 14'd10;         // 百位截余
	assign dec_tens = (i_age_upper_ms[13:0] / 14'd10) % 14'd10;              // 十位截余
	assign dec_units = i_age_upper_ms[13:0] % 14'd10;                       // 个位截余
	assign dec_local_x = cnt_x[7:0] - 8'd16;                              // 起点固定横坐标16
	assign dec_cell = dec_local_x / 8'd12;                                // 常数间距选字符
	assign dec_cell_x = dec_local_x % 8'd12;                              // 单元内横坐标
	assign dec_local_y = cnt_y[3:0];                                      // 区域16至31低四位正好为偏移
	assign dec_font_row = dec_local_y[3:1];                               // 垂直二倍放大
	assign dec_font_column = dec_cell_x[3:1];                             // 水平二倍放大
	assign dec_bit_index = 6'd34 - ({3'd0, dec_font_row} * 6'd5)
	                     - {3'd0, dec_font_column};                       // 点阵MSB位于左上角
	assign flag_text_pixel = i_de && (cnt_x >= 11'd16) && (cnt_x < 11'd148)
	                      && (cnt_y >= 10'd16) && (cnt_y < 10'd32)
	                      && (dec_cell_x < 4'd10) && (dec_local_y < 4'd14)
	                      && dec_bitmap[dec_bit_index];                   // 区域和行列同时合法才取墨点

	//-------------输出信号连线-------------//
	// 实时安全许可不经过帧内文本或视频流水。
	assign o_draw_permit = i_rstn && i_table_draw_valid;                    // 立即撤框；不产生新的许可
	assign o_rgb = rgb_o;                                                 // 注册颜色送原HDMI链
	assign o_vsync = vsync_o;                                             // VS和颜色对齐
	assign o_hsync = hsync_o;                                             // HS和颜色对齐
	assign o_de = de_o;                                                   // DE和颜色对齐

	//-----------主要任务处理区域-----------//
	// 第一消隐拍之后更新文本；活动区之前必须留出这个锁存边界。
	always @(posedge i_clk or negedge i_rstn) begin
		if (!i_rstn) begin
			flag_latch_pending <= 1'b0;
			flag_age_known <= 1'b0;
			reg_decimal_digits <= 16'd0;
		end else if (i_sof) begin
			flag_latch_pending <= 1'b1;
		end else if (flag_latch_pending && !i_de) begin
			flag_latch_pending <= 1'b0;
			flag_age_known <= i_age_upper_ms <= 64'd9999;
			reg_decimal_digits <= {dec_thousands[3:0], dec_hundreds[3:0],
			                       dec_tens[3:0], dec_units[3:0]};
		end
	end

	// 有效行首为零；空白时不推进横坐标，SOF取消旧行位置。
	always @(posedge i_clk or negedge i_rstn) begin
		if (!i_rstn) begin
			cnt_x <= 11'd0;
			cnt_y <= 10'd0;
			flag_de_previous <= 1'b0;
		end else begin
			flag_de_previous <= i_de;
			if (i_sof) begin
				cnt_x <= 11'd0;
				cnt_y <= 10'd0;
			end else if (i_de) begin
				cnt_x <= cnt_x + 11'd1;
			end else if (flag_de_previous) begin
				cnt_x <= 11'd0;
				cnt_y <= cnt_y + 10'd1;
			end
		end
	end

	// 仅选十一位置，不建立字符RAM或可编程排版接口。
	always @(*) begin
		dec_character = 8'h20;
		case (dec_cell)
			5'd0: begin dec_character = 8'h41; end
			5'd1: begin dec_character = 8'h47; end
			5'd2: begin dec_character = 8'h45; end
			5'd3: begin dec_character = flag_age_known ? 8'h20 : 8'h5f; end
			5'd4: begin dec_character = flag_age_known ? {4'h3, reg_decimal_digits[15:12]} : 8'h49; end
			5'd5: begin dec_character = flag_age_known ? {4'h3, reg_decimal_digits[11:8]} : 8'h4e; end
			5'd6: begin dec_character = flag_age_known ? {4'h3, reg_decimal_digits[7:4]} : 8'h56; end
			5'd7: begin dec_character = flag_age_known ? {4'h3, reg_decimal_digits[3:0]} : 8'h41; end
			5'd8: begin dec_character = flag_age_known ? 8'h20 : 8'h4c; end
			5'd9: begin dec_character = flag_age_known ? 8'h6d : 8'h49; end
			5'd10: begin dec_character = flag_age_known ? 8'h73 : 8'h44; end
			default: begin dec_character = 8'h20; end
		endcase
	end

	// 常量字形来自CPU冻结点阵；七行直接拼成35bit组合查表。
	always @(*) begin
		case (dec_character)
			8'h30: begin dec_bitmap = 35'h3a33ae62e; end
			8'h31: begin dec_bitmap = 35'h11842108e; end
			8'h32: begin dec_bitmap = 35'h3a211111f; end
			8'h33: begin dec_bitmap = 35'h78217043e; end
			8'h34: begin dec_bitmap = 35'h08ca97c42; end
			8'h35: begin dec_bitmap = 35'h7e10f043e; end
			8'h36: begin dec_bitmap = 35'h3a10f462e; end
			8'h37: begin dec_bitmap = 35'h7c2222108; end
			8'h38: begin dec_bitmap = 35'h3a317462e; end
			8'h39: begin dec_bitmap = 35'h3a317842e; end
			8'h41: begin dec_bitmap = 35'h3a31fc631; end
			8'h47: begin dec_bitmap = 35'h3a30bc62f; end
			8'h45: begin dec_bitmap = 35'h7e10f421f; end
			8'h5f: begin dec_bitmap = 35'h00000001f; end
			8'h49: begin dec_bitmap = 35'h38842108e; end
			8'h4e: begin dec_bitmap = 35'h4739ace71; end
			8'h56: begin dec_bitmap = 35'h46318c544; end
			8'h4c: begin dec_bitmap = 35'h42108421f; end
			8'h44: begin dec_bitmap = 35'h7a318c63e; end
			8'h6d: begin dec_bitmap = 35'h001aad6b5; end
			8'h73: begin dec_bitmap = 35'h000f8383e; end
			default: begin dec_bitmap = 35'd0; end
		endcase
	end

	// 点阵空点透明，不把未知年龄的零寄存内容显示为零毫秒。
	always @(*) begin
		dec_rgb = i_rgb;
		if (flag_text_pixel) begin
			dec_rgb = 24'hffffff;
		end
	end

	// 四条视频输出共同延迟一拍，不改变有效区长度。
	always @(posedge i_clk or negedge i_rstn) begin
		if (!i_rstn) begin
			rgb_o <= 24'd0;
			vsync_o <= 1'b0;
			hsync_o <= 1'b0;
			de_o <= 1'b0;
		end else begin
			rgb_o <= dec_rgb;
			vsync_o <= i_vsync;
			hsync_o <= i_hsync;
			de_o <= i_de;
		end
	end
endmodule
