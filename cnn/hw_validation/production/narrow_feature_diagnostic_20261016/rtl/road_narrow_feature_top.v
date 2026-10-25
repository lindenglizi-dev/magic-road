`timescale 1ns / 1ps
// Company: RoadYOLO
// Engineer: Codex
// Create Date: 2026-10-16
// Design Name: Frozen feature narrow diagnostic
// Module Name: road_narrow_feature_top
// Description: Fixed 16-bit host transport around actual frozen feature top
// Simulations: tests/tb_narrow_feature_transport.v
// Referrences: interface_contract.json
// Dependencies: road_feature_workstore_top.v and frozen source closure
// Version: V1.0
// Revision Date: 2026-10-16
// History: Create file
// 版权归属: RoadYOLO
// 开发人员: Codex
// 创建日期: 2026-10-16
// 设计名称: 冻结特征窄口诊断
// 模块名称: road_narrow_feature_top
// 模块说明: 真实冻结计算链的固定16位主机链路
// 仿真工程: tests/tb_narrow_feature_transport.v
// 参考资料: interface_contract.json
// 依赖文件: road_feature_workstore_top.v及冻结闭包
// 当前版本: V1.0
// 修订日期: 2026-10-16
// 修订历史: 创建文件
module road_narrow_feature_top(
	input i_clk, // 单一主机与计算时钟
	input i_rstn, // 共同异步低有效复位
	input i_rx_valid, // 主机当前输入字有效
	input [15:0]i_rx_data, // 包头或低字优先载荷
	output o_rx_ready, // 当前输入字接受许可
	output o_tx_valid, // 导出字保持有效
	output [15:0]o_tx_data, // 请求或真实输出的当前字
	input i_tx_ready, // 主机当前导出字接收许可
	output o_busy, // 实际客户占用状态
	output o_done, // 实际末层屏障完成脉冲
	output o_fault, // 壳与全部实际所有者故障合并
	output o_table_loaded // 实际完整SiLU表有效
);
	localparam [2:0] ST_RX_IDLE = 3'd0; // 等待固定命令头
	localparam [2:0] ST_RX_PAYLOAD = 3'd1; // 收齐当前固定长度载荷
	localparam [2:0] ST_RX_APPLY = 3'd2; // 向实际响应口保持整包
	localparam [2:0] ST_RX_TABLE = 3'd3; // 逐项直写唯一查表存储
	localparam [2:0] ST_RX_FAULT = 3'd4; // 等待共同复位恢复
	localparam [1:0] ST_TX_IDLE = 2'd0; // 固定优先级选择一个源
	localparam [1:0] ST_TX_HEADER = 2'd1; // 保持当前导出包头
	localparam [1:0] ST_TX_PAYLOAD = 2'd2; // 低字优先导出载荷
	localparam [1:0] ST_TX_GAP = 2'd3; // 等源端退休后再选择
	reg [2:0] state_rx_current, state_rx_next; // 接收状态及独立下一状态
	reg [1:0] state_tx_current, state_tx_next; // 导出状态及独立下一状态
	reg [15:0] reg_rx_header; // 当前完整包类型
	reg [463:0] reg_rx_payload; // 最大参数响应的一份保持寄存器
	reg [4:0] cnt_rx_remaining; // 当前载荷尚余字数减一
	reg [9:0] cnt_table_address; // 从零递增的真实表地址
	reg [15:0] reg_tx_header; // 导出过程中固定的包头
	reg [63:0] reg_tx_payload; // 单个真实结果或请求的移位快照
	reg [2:0] cnt_tx_remaining; // 当前导出载荷余字数减一
	reg flag_read_pending; // 完整读请求已发送而响应未应用
	reg flag_parameter_pending; // 完整参数请求已发送而响应未应用
	reg flag_barrier_pending; // 完整屏障已发送而可见性未确认
	reg flag_shell_fault; // 非法包的粘滞故障
	reg flag_cancel; // 向冻结客户送一次取消事件
	reg flag_padding_valid; // 当前固定布局高填充位合法
	wire flag_rx_accept; // 共同握手才消耗输入字
	wire flag_tx_accept; // 共同握手才移动导出字
	wire flag_tx_finish; // 包末真实握手退休源请求
	wire flag_rx_apply; // 完整合法响应被实际客户接受
	wire flag_read_response; // 当前整包属于读响应
	wire flag_parameter_response; // 当前整包属于参数响应
	wire flag_barrier_response; // 当前整包属于屏障确认
	wire link_busy, link_done, link_fault; // 冻结客户状态
	wire link_start_ready, link_table_ready, link_table_loaded; // 实际启动和装表许可
	wire [3:0] link_block; // 当前锁存块身份
	wire [2:0] link_layer; // 当前层屏障身份
	wire [6:0] link_tile_y; // 实际客户行进度
	wire [7:0] link_tile_x; // 实际客户列进度
	wire link_parameter_valid, link_parameter_response_ready; // 参数请求与响应状态
	wire [6:0] link_parameter_channel; // 请求输出通道
	wire [4:0] link_parameter_group; // 请求输入通道组
	wire [2:0] link_parameter_window; // 请求卷积窗口
	wire link_read_valid, link_read_response_ready; // 外部特征行请求与响应许可
	wire [31:0] link_read_address; // 请求绝对字节地址
	wire link_write_valid; // 实际计算结果可接受
	wire [31:0] link_write_address; // 实际计算结果目标地址
	wire [7:0] link_write_data; // 实际定点输出逐项导出
	wire [8:0] link_write_sum; // 算术核原辅助和值
	wire link_barrier_valid; // 此前实际写必须可见的屏障
	wire flag_read_retire, flag_parameter_retire, flag_write_retire; // 各源末字退休许可
	wire flag_start; // 完整合法启动包的单拍触发

	assign o_busy = link_busy; // 保留实际客户忙语义
	assign o_done = link_done; // 保留实际完成事件
	assign o_fault = flag_shell_fault | link_fault; // 不屏蔽核心或工作仓故障
	assign o_table_loaded = link_table_loaded; // 不以壳内计数代替实际全表状态
	assign o_rx_ready = i_rstn && !o_fault && ((state_rx_current == ST_RX_IDLE) ||
		(state_rx_current == ST_RX_PAYLOAD) || (state_rx_current == ST_RX_TABLE && link_table_ready)); // 表项必须等真实ready
	assign o_tx_valid = i_rstn && !o_fault && ((state_tx_current == ST_TX_HEADER) ||
		(state_tx_current == ST_TX_PAYLOAD)); // 只有包头和载荷状态发送
	assign o_tx_data = state_tx_current == ST_TX_HEADER ? reg_tx_header : reg_tx_payload[15:0]; // 快照或当前移位字
	assign flag_rx_accept = i_rx_valid && o_rx_ready; // 输入流联合握手
	assign flag_tx_accept = o_tx_valid && i_tx_ready; // 输出流联合握手
	assign flag_tx_finish = flag_tx_accept && state_tx_current == ST_TX_PAYLOAD && cnt_tx_remaining == 3'd0; // 接受末字才完成包
	assign flag_read_retire = flag_tx_finish && reg_tx_header == 16'ha100; // 全地址已交付主机
	assign flag_parameter_retire = flag_tx_finish && reg_tx_header == 16'ha101; // 完整参数身份已交付
	assign flag_write_retire = flag_tx_finish && reg_tx_header == 16'ha102; // 地址数值和值全部导出一次
	assign flag_read_response = state_rx_current == ST_RX_APPLY && reg_rx_header == 16'h8100 && flag_padding_valid; // 保持完整读响应
	assign flag_parameter_response = state_rx_current == ST_RX_APPLY && reg_rx_header == 16'h8101 && flag_padding_valid; // 保持全部463位参数响应
	assign flag_barrier_response = state_rx_current == ST_RX_APPLY && reg_rx_header == 16'h8102 && flag_padding_valid; // 完整身份送实际屏障检查
	assign flag_start = state_rx_current == ST_RX_APPLY && reg_rx_header == 16'h8001 && flag_padding_valid && link_start_ready; // 部分表绝不启动
	assign flag_rx_apply = (flag_read_response && link_read_response_ready) ||
		(flag_parameter_response && link_parameter_response_ready) || (flag_barrier_response && link_barrier_valid); // 仅实际端口接受时清请求

	// 固定布局的高填充位必须全零；短包在移位寄存器高端对齐。
	always@(*)begin
		flag_padding_valid = 1'b0;
		case(reg_rx_header)
			16'h8001:begin flag_padding_valid = reg_rx_payload[463:452] == 12'd0; end
			16'h8100:begin flag_padding_valid = reg_rx_payload[463:449] == 15'd0; end
			16'h8101:begin flag_padding_valid = reg_rx_payload[463] == 1'b0; end
			16'h8102:begin flag_padding_valid = reg_rx_payload[463:455] == 9'd0; end
			default:begin flag_padding_valid = 1'b0; end
		endcase
	end
	// 接收状态寄存器只由共同复位及独立下一状态更新。
	always@(posedge i_clk or negedge i_rstn)begin
		if(!i_rstn)begin state_rx_current <= ST_RX_IDLE; end
		else begin state_rx_current <= state_rx_next; end
	end
	// 未期望的响应不进入实际客户；完整包才应用。
	always@(*)begin
		state_rx_next = state_rx_current;
		case(state_rx_current)
			ST_RX_IDLE:begin
				if(flag_rx_accept)begin
					case(i_rx_data)
						16'h8000:begin
							if(!link_busy)begin state_rx_next = ST_RX_TABLE; end
							else begin state_rx_next = ST_RX_FAULT; end
						end
						16'h8001:begin state_rx_next = ST_RX_PAYLOAD; end
						16'h8002:begin state_rx_next = ST_RX_IDLE; end
						16'h8100:begin
							if(flag_read_pending)begin state_rx_next = ST_RX_PAYLOAD; end
							else begin state_rx_next = ST_RX_FAULT; end
						end
						16'h8101:begin
							if(flag_parameter_pending)begin state_rx_next = ST_RX_PAYLOAD; end
							else begin state_rx_next = ST_RX_FAULT; end
						end
						16'h8102:begin
							if(flag_barrier_pending)begin state_rx_next = ST_RX_PAYLOAD; end
							else begin state_rx_next = ST_RX_FAULT; end
						end
						default:begin state_rx_next = ST_RX_FAULT; end
					endcase
				end
			end
			ST_RX_PAYLOAD:begin
				if(flag_rx_accept && cnt_rx_remaining == 5'd0)begin state_rx_next = ST_RX_APPLY; end
			end
			ST_RX_APPLY:begin
				if(!flag_padding_valid)begin state_rx_next = ST_RX_FAULT; end
				else if(reg_rx_header == 16'h8001)begin
					state_rx_next = ST_RX_IDLE;
				end else if(flag_rx_apply)begin state_rx_next = ST_RX_IDLE; end
			end
			ST_RX_TABLE:begin
				if(flag_rx_accept && cnt_table_address == 10'd1023)begin state_rx_next = ST_RX_IDLE; end
			end
			ST_RX_FAULT:begin state_rx_next = ST_RX_FAULT; end
			default:begin state_rx_next = ST_RX_FAULT; end
		endcase
	end
	// 接收任务只维护一份最大响应；不创建权重ROM或图像缓存。
	always@(posedge i_clk or negedge i_rstn)begin
		if(!i_rstn)begin
			reg_rx_header <= 16'd0;
			reg_rx_payload <= 464'd0;
			cnt_rx_remaining <= 5'd0;
			cnt_table_address <= 10'd0;
			flag_shell_fault <= 1'b0;
			flag_cancel <= 1'b0;
		end else begin
			flag_cancel <= 1'b0;
			if(state_rx_next == ST_RX_FAULT)begin flag_shell_fault <= 1'b1; end
			if(state_rx_current == ST_RX_IDLE && flag_rx_accept)begin
				reg_rx_header <= i_rx_data;
				reg_rx_payload <= 464'd0;
				case(i_rx_data)
					16'h8000:begin cnt_table_address <= 10'd0; end
					16'h8001, 16'h8102:begin cnt_rx_remaining <= 5'd0; end
					16'h8100:begin cnt_rx_remaining <= 5'd10; end
					16'h8101:begin cnt_rx_remaining <= 5'd28; end
					16'h8002:begin flag_cancel <= 1'b1; end
					default:begin flag_shell_fault <= 1'b1; end
				endcase
			end
			if(state_rx_current == ST_RX_PAYLOAD && flag_rx_accept)begin
				reg_rx_payload <= {i_rx_data, reg_rx_payload[463:16]};
				cnt_rx_remaining <= cnt_rx_remaining - 5'd1;
			end
			if(state_rx_current == ST_RX_TABLE && flag_rx_accept)begin cnt_table_address <= cnt_table_address + 10'd1; end
		end
	end
	// 每种服务至多一个完整已发送请求；屏障确认后才允许下一层请求。
	always@(posedge i_clk or negedge i_rstn)begin
		if(!i_rstn)begin
			flag_read_pending <= 1'b0;
			flag_parameter_pending <= 1'b0;
			flag_barrier_pending <= 1'b0;
		end else begin
			if(flag_read_retire)begin flag_read_pending <= 1'b1; end
			else if(flag_read_response && link_read_response_ready)begin flag_read_pending <= 1'b0; end
			if(flag_parameter_retire)begin flag_parameter_pending <= 1'b1; end
			else if(flag_parameter_response && link_parameter_response_ready)begin flag_parameter_pending <= 1'b0; end
			if(flag_tx_finish && reg_tx_header == 16'ha103)begin flag_barrier_pending <= 1'b1; end
			else if(flag_barrier_response && link_barrier_valid)begin flag_barrier_pending <= 1'b0; end
		end
	end
	// 导出状态寄存器与载荷存储独立，背压时全部保持。
	always@(posedge i_clk or negedge i_rstn)begin
		if(!i_rstn)begin state_tx_current <= ST_TX_IDLE; end
		else begin state_tx_current <= state_tx_next; end
	end
	// 请求末字与源握手同拍，随后隔一拍等待源撤销valid。
	always@(*)begin
		state_tx_next = state_tx_current;
		case(state_tx_current)
			ST_TX_IDLE:begin
				if(link_read_valid || link_parameter_valid || link_write_valid || (link_barrier_valid && !flag_barrier_pending))begin
					state_tx_next = ST_TX_HEADER;
				end
			end
			ST_TX_HEADER:begin
				if(flag_tx_accept)begin
					state_tx_next = ST_TX_PAYLOAD;
				end
			end
			ST_TX_PAYLOAD:begin
				if(flag_tx_finish)begin
					state_tx_next = ST_TX_GAP;
				end
			end
			ST_TX_GAP:begin state_tx_next = ST_TX_IDLE; end
			default:begin state_tx_next = ST_TX_IDLE; end
		endcase
	end
	// 固定优先级快照全部身份与实际结果，移位仅发生在接受边沿。
	always@(posedge i_clk or negedge i_rstn)begin
		if(!i_rstn)begin
			reg_tx_header <= 16'd0;
			reg_tx_payload <= 64'd0;
			cnt_tx_remaining <= 3'd0;
		end else begin
			if(state_tx_current == ST_TX_IDLE)begin
				if(link_read_valid)begin
					reg_tx_header <= 16'ha100;
					reg_tx_payload <= {32'd0, link_read_address};
					cnt_tx_remaining <= 3'd1;
				end else if(link_parameter_valid)begin
					reg_tx_header <= 16'ha101;
					reg_tx_payload <= {42'd0, link_parameter_window, link_parameter_group, link_parameter_channel, link_layer, link_block};
					cnt_tx_remaining <= 3'd1;
				end else if(link_write_valid)begin
					reg_tx_header <= 16'ha102;
					reg_tx_payload <= {15'd0, link_write_sum, link_write_data, link_write_address};
					cnt_tx_remaining <= 3'd3;
				end else if(link_barrier_valid && !flag_barrier_pending)begin
					reg_tx_header <= 16'ha103;
					reg_tx_payload <= {57'd0, link_layer, link_block};
					cnt_tx_remaining <= 3'd0;
				end
			end
			if(state_tx_current == ST_TX_PAYLOAD && flag_tx_accept)begin
				reg_tx_payload <= {16'd0, reg_tx_payload[63:16]};
				cnt_tx_remaining <= cnt_tx_remaining - 3'd1;
			end
		end
	end
	// 实际冻结顶层完整保留，主机仅替代原宽外部服务接口。
	road_feature_workstore_top core_Inst(
		.i_clk(i_clk), .i_rstn(i_rstn),
		.i_block_id(reg_rx_payload[451:448]), .o_block_id(link_block),
		.i_start(flag_start), .i_cancel(flag_cancel), .o_start_ready(link_start_ready),
		.o_busy(link_busy), .o_done(link_done), .o_fault(link_fault),
		.o_layer(link_layer), .o_tile_y(link_tile_y), .o_tile_x(link_tile_x),
		.o_parameter_valid(link_parameter_valid), .o_parameter_channel(link_parameter_channel),
		.o_parameter_group(link_parameter_group), .o_parameter_window(link_parameter_window),
		.i_parameter_ready(flag_parameter_retire), .i_parameter_response_valid(flag_parameter_response),
		.o_parameter_response_ready(link_parameter_response_ready),
		.i_parameter_response_block_id(reg_rx_payload[3:0]), .i_parameter_response_layer(reg_rx_payload[6:4]),
		.i_parameter_response_channel(reg_rx_payload[13:7]), .i_parameter_response_group(reg_rx_payload[18:14]),
		.i_parameter_response_window(reg_rx_payload[21:19]), .i_parameter_weight(reg_rx_payload[213:22]),
		.i_parameter_data(reg_rx_payload[461:214]), .i_parameter_error(reg_rx_payload[462]),
		.o_read_valid(link_read_valid), .o_read_address(link_read_address), .i_read_ready(flag_read_retire),
		.i_read_response_valid(flag_read_response), .o_read_response_ready(link_read_response_ready),
		.i_read_response_address(reg_rx_payload[319:288]), .i_read_response_data(reg_rx_payload[447:320]),
		.i_read_error(reg_rx_payload[448]), .o_write_valid(link_write_valid),
		.o_write_address(link_write_address), .o_write_data(link_write_data), .o_write_sum(link_write_sum),
		.i_write_ready(flag_write_retire), .o_barrier_valid(link_barrier_valid), .i_barrier_ready(flag_barrier_response),
		.i_barrier_block_id(reg_rx_payload[451:448]), .i_barrier_layer(reg_rx_payload[454:452]),
		.i_table_valid(state_rx_current == ST_RX_TABLE && i_rx_valid && !o_fault),
		.i_table_addr(cnt_table_address), .i_table_data(i_rx_data),
		.o_table_ready(link_table_ready), .o_table_loaded(link_table_loaded)
	);
endmodule
