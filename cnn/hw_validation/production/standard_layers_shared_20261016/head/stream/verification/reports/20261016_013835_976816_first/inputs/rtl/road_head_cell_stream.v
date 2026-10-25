`timescale 1ns / 1ps
////////////////////////////////////English///////////////////////////////////////
// Company: RoadYOLO
// Engineer: Codex
// Create Date: 2026-10-16
// Design Name: Fixed INT16 prediction cell reader
// Module Name: road_head_cell_stream
// Description: description/road_head_cell_stream_Design.pdf
// Simulations: testbench/vivado/2021.1/road_head_cell_stream
// Referrences: Frozen graph and head HWC7 contract
// Dependencies: External logical128-bit read service
// Version: V1.0
// Revision Date: 2026-10-16
// History: 2026-10-16 V1.0 Codex Create file
///////////////////////////////////Chinese////////////////////////////////////////
// 版权归属: RoadYOLO
// 开发人员: Codex
// 创建日期: 2026-10-16
// 设计名称: 固定预测张量逐cell读取
// 模块名称: road_head_cell_stream
// 模块说明: Description/road_head_cell_stream_Design.pdf
// 仿真工程: TestBench/Vivado/2021.1/road_head_cell_stream
// 参考资料: 冻结图和HWC7顺序契约
// 依赖文件: 外部逻辑128位读服务
// 当前版本: V1.0
// 修订日期: 2026-10-16
// 修订历史: 2026-10-16 V1.0 Codex 创建文件

module road_head_cell_stream
(
	//-----------------全局信号-----------------//
	input i_clk, // 与唯一计算和后处理同域
	input i_rstn, // 与读服务共同低有效复位
	//-----------------用户接口-----------------//
	input i_cancel, // 取消后保持owner直到共同reset
	input i_start_valid, // 完整预测读取任务有效
	input [31:0]i_start_frame_token, // 当前任务身份首握手锁存
	input [31:0]i_start_model_id, // 当前参数包标识首握手锁存
	input i_predictions_committed, // 六张预测张量全部已可读
	input i_read_ready, // 接受唯一未决源行请求
	input i_read_rsp_valid, // 完整128位源行返回
	input [31:0]i_read_rsp_address, // 已接受源行的地址回显
	input [127:0]i_read_rsp_data, // 低字节对应低地址
	input i_read_error, // 源读服务拒绝结果
	input i_cell_ready, // 现有decoder接受完整cell
	output o_start_ready, // 空闲且预测写可见才准入
	output o_busy, // 含未退休读、输出与故障占有
	output o_done, // 最后cell实际消费后一拍
	output o_fault, // 故障或取消禁止发布成功
	output o_read_valid, // 对齐128位源行请求
	output [31:0]o_read_address, // 保持至read ready
	output o_read_rsp_ready, // 只消费当前未决源行
	output o_cell_valid, // 七个字段全部填入后发布
	output [111:0]o_cell_data, // 低位reg0到4再cls0到1
	output [13:0]o_cell_id, // S4/S8/S16共12096位置
	output [31:0]o_cell_frame_token, // 与cell数据整组保持
	output [31:0]o_cell_model_id // 与start绑定的模型身份
);
	//-------------状态参数区域-------------//
	localparam [2:0]ST_IDLE = 0; // 无任务且无未决读
	localparam [2:0]ST_FIELD = 1; // 从缓存取下一个INT16字段
	localparam [2:0]ST_READ = 2; // 等源行请求实际接受
	localparam [2:0]ST_WAIT = 3; // 等完整源行消费
	localparam [2:0]ST_SEND = 4; // 完整cell保持到decoder消费
	localparam [2:0]ST_FINISH = 5; // 末cell已消费的完成脉冲
	localparam [2:0]ST_FAULT = 6; // 不以故障当作排空

	//--------------状态机信号--------------//
	reg [2:0]state_current = ST_IDLE; // 当前读取阶段
	reg [2:0]state_next = ST_IDLE; // 组合下一读取阶段

	//--------------寄存器信号--------------//
	reg [1:0]reg_release = 0; // 异步断言两级释放
	reg [31:0]reg_token = 0; // 首握手冻结的任务标识
	reg [31:0]reg_model = 0; // 首握手冻结的参数包标识
	reg [1:0]reg_scale = 0; // 固定三个尺度的顺序编号
	reg [6:0]reg_y = 0; // 当前尺度真实输出行
	reg [6:0]reg_x = 0; // 当前尺度真实输出列
	reg [13:0]reg_cell_id = 0; // 全局从零递增至12095
	reg [2:0]reg_field = 0; // 当前cell填充字段0..6
	reg [111:0]reg_cell = 0; // 唯一待发cell非整幅预测RAM
	reg [31:0]reg_read_address = 0; // 唯一未决源行地址
	reg [31:0]reg_line_address = 0; // 当前16B缓存全地址标签
	reg [127:0]reg_line = 0; // 单个源行寄存器

	//---------------标志信号---------------//
	reg flag_line_valid = 0; // 已消费且匹配的源行有效
	reg flag_fault = 0; // 错读/取消保持至共同复位
	wire flag_active; // 释放且无取消故障
	wire flag_hit; // 当前INT16字段命中源行
	wire flag_bad_read; // 完整响应归属或服务错误

	//---------------译码信号---------------//
	reg [6:0]dec_height = 0; // 固定尺度高度72/36/18
	reg [7:0]dec_width = 0; // 固定尺度宽度128/64/32
	reg [31:0]dec_reg_base = 0; // 五通道INT16预测基址
	reg [31:0]dec_cls_base = 0; // 两通道INT16预测基址
	reg [31:0]dec_field_address = 0; // 当前字段完整字节位置
	integer dec_pixel; // tile4x4中的真实元素像素号
	integer dec_channels; // 当前预测平面的五或二通道
	integer dec_channel; // 当前平面中的真实通道

	//-------------其他信号连线-------------//
	assign flag_active = reg_release[1] && !o_fault; // 共同释放才传输
	assign flag_hit = flag_line_valid && reg_line_address == {dec_field_address[31:4],4'b0000}; // 完整行标签核验
	assign flag_bad_read = i_read_rsp_valid && o_read_rsp_ready && (i_read_error || i_read_rsp_address != reg_read_address); // 旧地址不得填缓存

	//-------------输出信号连线-------------//
	assign o_fault = flag_fault || i_cancel; // 取消立即撤成功许可
	assign o_start_ready = state_current == ST_IDLE && flag_active && i_predictions_committed; // 不读半幅预测
	assign o_busy = state_current != ST_IDLE; // fault不提前释放owner
	assign o_done = state_current == ST_FINISH && flag_active; // 最末输出消费之后
	assign o_read_valid = state_current == ST_READ && flag_active; // 单未决请求保持
	assign o_read_address = reg_read_address; // 请求地址由寄存器锁定
	assign o_read_rsp_ready = state_current == ST_WAIT && flag_active; // 只归属当前读
	assign o_cell_valid = state_current == ST_SEND && flag_active; // 完整七字段才有效
	assign o_cell_data = reg_cell; // 背压期间不改载荷
	assign o_cell_id = reg_cell_id; // 与cell载荷同拍冻结
	assign o_cell_frame_token = reg_token; // 任务全程源身份稳定
	assign o_cell_model_id = reg_model; // 模型全程身份稳定

	// 六个plane均来自冻结图；INT16逻辑地址总为偶数且不会跨16B行。
	always@(*)begin
		dec_height = 72;
		dec_width = 128;
		dec_reg_base = 61919232;
		dec_cls_base = 60997632;
		case(reg_scale)
			1:begin
				dec_height = 36;
				dec_width = 64;
				dec_reg_base = 62578688;
				dec_cls_base = 62345216;
			end
			2:begin
				dec_height = 18;
				dec_width = 32;
				dec_reg_base = 62771200;
				dec_cls_base = 62701568;
			end
			default:begin
				dec_height = 72;
			end
		endcase
		dec_channels = reg_field < 5 ? 5 : 2;
		dec_channel = reg_field < 5 ? reg_field : reg_field - 5;
		dec_pixel = ((reg_y / 4) * (dec_width / 4) + reg_x / 4) * 16 + (reg_y % 4) * 4 + reg_x % 4;
		dec_field_address = (reg_field < 5 ? dec_reg_base : dec_cls_base) + (dec_pixel * dec_channels + dec_channel) * 2;
	end

	//--------------状态机区域--------------//
	// 只门控新读取应用，不改变任何冻结算术模块的reset。
	always@(posedge i_clk or negedge i_rstn)begin
		if(!i_rstn)begin
			reg_release <= 0;
		end else begin
			reg_release <= {reg_release[0],1'b1};
		end
	end

	// 状态寄存器只在共同reset撤销本地未决控制。
	always@(posedge i_clk or negedge i_rstn)begin
		if(!i_rstn)begin
			state_current <= ST_IDLE;
		end else begin
			state_current <= state_next;
		end
	end

	// 字段填充、外部读和cell消费均以真实握手推进。
	always@(*)begin
		state_next = state_current;
		case(state_current)
			// start有效且全部预测已可见才能取得owner。
			ST_IDLE:begin
				if(i_start_valid && o_start_ready)begin
					state_next = ST_FIELD;
				end
			end
			// 缓存未命中只请求一个源行。
			ST_FIELD:begin
				if(!flag_hit)begin
					state_next = ST_READ;
				end else if(reg_field == 6)begin
					state_next = ST_SEND;
				end
			end
			// 请求接受后不再修改未决地址。
			ST_READ:begin
				if(o_read_valid && i_read_ready)begin
					state_next = ST_WAIT;
				end
			end
			// 响应消费后重新检查字段缓存命中。
			ST_WAIT:begin
				if(i_read_rsp_valid && o_read_rsp_ready)begin
					state_next = ST_FIELD;
				end
			end
			// 背压保持整个cell，不推进源位置。
			ST_SEND:begin
				if(o_cell_valid && i_cell_ready)begin
					if(reg_cell_id == 12095)begin
						state_next = ST_FINISH;
					end else begin
						state_next = ST_FIELD;
					end
				end
			end
			// done单拍结束后才准入下一个模型任务。
			ST_FINISH:begin
				state_next = ST_IDLE;
			end
			// 不能用取消当源服务已排空。
			ST_FAULT:begin
				state_next = ST_FAULT;
			end
			// 不合法状态保守保持owner。
			default:begin
				state_next = ST_FAULT;
			end
		endcase
		if(o_fault || flag_bad_read)begin
			state_next = ST_FAULT;
		end
	end

	//-----------状态任务处理区域-----------//
	// 数据只保存一行和一个cell，不清理或复制整张预测张量。
	always@(posedge i_clk or negedge i_rstn)begin
		if(!i_rstn)begin
			reg_token <= 0;
			reg_model <= 0;
			reg_scale <= 0;
			reg_y <= 0;
			reg_x <= 0;
			reg_cell_id <= 0;
			reg_field <= 0;
			reg_cell <= 0;
			reg_read_address <= 0;
			reg_line_address <= 0;
			reg_line <= 0;
			flag_line_valid <= 0;
			flag_fault <= 0;
		end else begin
			if(state_next == ST_FAULT)begin
				flag_fault <= 1; // 共同reset以外不解除故障
			end
			if(i_start_valid && o_start_ready)begin
				reg_token <= i_start_frame_token; // 首握手冻结源任务
				reg_model <= i_start_model_id; // 首握手冻结模型版本
				reg_scale <= 0; // 从stride4预测开始
				reg_y <= 0; // 从首行开始
				reg_x <= 0; // 从首列开始
				reg_cell_id <= 0; // 新任务从全局cell零开始
				reg_field <= 0; // 首字段为tx
				reg_cell <= 0; // 新cell全部字段需重新覆盖
				flag_line_valid <= 0; // 禁止跨帧继承预测数据
			end
			if(state_current == ST_FIELD)begin
				if(flag_hit)begin
					reg_cell[reg_field * 16 +: 16] <= reg_line[dec_field_address[3:0] * 8 +: 16]; // 偶数INT16原样复制
					if(reg_field != 6)begin
						reg_field <= reg_field + 1'b1; // tx至vehicle七字段逐一填入
					end
				end else begin
					reg_read_address <= {dec_field_address[31:4],4'b0000}; // 请求前锁定完整对齐行
				end
			end
			if(i_read_rsp_valid && o_read_rsp_ready && !flag_bad_read)begin
				reg_line <= i_read_rsp_data; // 仅接受正确返回的128位
				reg_line_address <= i_read_rsp_address; // 标签与载荷同拍登记
				flag_line_valid <= 1; // 下一字段阶段可用
			end
			if(o_cell_valid && i_cell_ready && reg_cell_id != 12095)begin
				reg_cell_id <= reg_cell_id + 1'b1; // 只有真实cell消费才递增
				reg_field <= 0; // 下一cell从tx开始
				reg_cell <= 0; // 不能发布未覆盖的旧字段
				if(reg_x == dec_width - 1)begin
					reg_x <= 0; // 每尺度行尾回到首列
					if(reg_y == dec_height - 1)begin
						reg_y <= 0; // 尺度结束回到首行
						reg_scale <= reg_scale + 1'b1; // S4再S8最后S16
					end else begin
						reg_y <= reg_y + 1'b1; // 仅真实有效行递增
					end
				end else begin
					reg_x <= reg_x + 1'b1; // 行内逐位置输出
				end
			end
		end
	end
endmodule
