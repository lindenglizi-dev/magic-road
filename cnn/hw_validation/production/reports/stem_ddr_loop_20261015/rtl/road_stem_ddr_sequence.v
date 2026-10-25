`timescale 1ns / 1ps

// Company: RoadYOLO project
// Engineer: Codex
// Create Date: 2026-10-14
// Design Name: Once-only Stem DDR downsample experiment
// Module Name: road_stem_ddr_sequence
// Description: Sixteen Stem tiles feed four down2 consumers through real DDR.
// Simulations: tests/tb_stem_ddr_sequence.v
// Referrences: requirements.txt, reference.py
// Dependencies: road_frontend_shared_core; frozen command and golden ROMs
// Version: V1.0
// Revision Date: 2026-10-14
// History: 2026-10-14 Codex Create file
// 版权归属: RoadYOLO project
// 开发人员: Codex
// 创建日期: 2026-10-14
// 设计名称: 一次性真实存储计算交接
// 模块名称: road_stem_ddr_sequence
// 模块说明: 实际核导出写DDR，实际读回装载下一层，逐项比对后锁存结果。
// 仿真工程: tests/tb_stem_ddr_sequence.v
// 参考资料: requirements.txt, reference.py
// 依赖文件: 冻结共享核和只读测试向量
// 当前版本: V1.0
// 修订日期: 2026-10-14
// 修订历史: 2026-10-14 Codex 创建文件
module road_stem_ddr_sequence
#(
	parameter [26:0] C_TIMEOUT = 27'h7ffffff // 无进展看门狗，不充当DDR屏障
)
(
	input i_clk, // 100MHz计算时钟
	input i_rstn, // 与整个DDR共同断言并在本域同步释放
	input i_phy_ready, // 已同步到本域的初始化许可
	input i_ddr_fault, // 邮箱的本域粘滞故障
	input i_req_ready, // 邮箱可保管唯一请求
	input i_rsp_valid, // 完整响应已跨域冻结
	input [127:0]i_rsp_data, // 实际DDR返回字
	input [3:0]i_rsp_error, // 写接受或读请求错误
	output o_req_valid, // 载荷保持到本域接受
	output o_req_write, // 写接受与读返回分型
	output [24:0]o_req_addr, // 按冻结布局转换的native地址
	output [127:0]o_req_data, // 实际核导出打包的128位字
	output o_rsp_ready, // 完整响应只消费一次
	output [1:0]o_status, // 零等待、一通过、二失败
	output [3:0]o_error, // 首个失败类型
	output [4:0]o_phase, // 可观测调度状态
	output [8:0]o_writes, // 已收到接受回执的唯一写字数
	output [8:0]o_reads, // 实际已消费的读响应数
	output [10:0]o_output_bytes, // 已核对的最终PW字节数
	output [31:0]o_cycles, // 含初始化的端点总周期
	output [319:0]o_cycle_bins, // 十项互斥分类，低32位为初始化
	output [24:0]o_address, // 当前读写的完整native地址
	output [127:0]o_expected, // 最近比较的完整期望字
	output [127:0]o_actual // 最近比较的完整实读或导出字
);
	//-----------------参数信号-----------------//
	`include "once_constants.vh"
	localparam [4:0] ST_PHY = 5'd0;
	localparam [4:0] ST_FETCH = 5'd1;
	localparam [4:0] ST_DECODE = 5'd2;
	localparam [4:0] ST_TABLE = 5'd3;
	localparam [4:0] ST_LOAD = 5'd4;
	localparam [4:0] ST_START = 5'd5;
	localparam [4:0] ST_RUN = 5'd6;
	localparam [4:0] ST_EXPORT = 5'd7;
	localparam [4:0] ST_STEM_BYTE = 5'd8;
	localparam [4:0] ST_STEM_CHECK = 5'd9;
	localparam [4:0] ST_WRITE = 5'd10;
	localparam [4:0] ST_WRITE_RESPONSE = 5'd11;
	localparam [4:0] ST_SELECT = 5'd12;
	localparam [4:0] ST_HALO_MAP = 5'd13;
	localparam [4:0] ST_HALO_DECODE = 5'd14;
	localparam [4:0] ST_READ_PREPARE = 5'd15;
	localparam [4:0] ST_READ = 5'd16;
	localparam [4:0] ST_READ_RESPONSE = 5'd17;
	localparam [4:0] ST_READ_CHECK = 5'd18;
	localparam [4:0] ST_HALO_BYTE = 5'd19;
	localparam [4:0] ST_OUTPUT_FETCH = 5'd20;
	localparam [4:0] ST_OUTPUT_BYTE = 5'd21;
	localparam [4:0] ST_ADVANCE = 5'd22;
	localparam [4:0] ST_PASS = 5'd23;
	localparam [4:0] ST_FAIL = 5'd24;

	//-----------------存储信号-----------------//
	reg [127:0]reg_stem_golden[0:255]; // 仅用于比较，不作为下层激活
	reg [31:0]reg_addresses[0:255]; // 十六个实际tile的256个字地址，保留层行跨度
	reg [15:0]reg_halo_map[0:511]; // 位八表示top/left补零，低八位为黄金字索引
	reg [7:0]reg_output_golden[0:2047]; // 1536项有效PW输出与零填充
	wire [63:0]reg_command; // 循环加载器同步返回，沿用原解码接口
	reg [127:0]reg_golden; // 同步读取的完整Stem比较字
	reg [24:0]reg_address; // 与黄金字同索引的真实DDR地址
	reg [15:0]reg_map; // 当前halo像素的映射记录
	reg [7:0]reg_output_expected; // 本次导出字节的同步黄金值
	reg [127:0]reg_word; // 唯一打包/读回寄存器，按字节移位消费
	reg [127:0]reg_expected_o; // 首错时停止更新的期望观察口
	reg [127:0]reg_actual_o; // 与期望同次比较的实际观察口

	//-----------------控制信号-----------------//
	reg [4:0]state_current;
	reg [4:0]state_next;
	reg [12:0]cnt_program; // 8192项ROM索引，仅有效程序范围执行
	reg [7:0]reg_golden_index; // Stem导出或halo映射指定的黄金索引
	reg [2:0]cnt_down2_tile; // 四个消费者，最终值四
	reg [8:0]cnt_tile_output; // 当前tile的384字节输出游标
	reg [8:0]cnt_export; // 当前Stem tile实际导出偏移，末尾为256
	reg [3:0]cnt_byte; // 一个128位字内的字节游标
	reg [6:0]cnt_halo_pixel; // 9×9 halo像素游标
	reg [10:0]cnt_halo_address; // 连续1296字节装载地址
	reg [8:0]cnt_writes_o;
	reg [8:0]cnt_reads_o;
	reg [10:0]cnt_output_bytes_o;
	reg [3:0]reg_error_o;
	reg flag_fault; // 本轮故障只由共同复位撤销
	reg [26:0]cnt_watchdog; // 无进展状态保持计数
	reg [31:0]cnt_cycles_o;
	reg [31:0]cnt_bins[0:9]; // 每拍只增加一项的端点分类
	reg [3:0]reg_category; // 当前拍对应的互斥分类
	integer bin; // 常量范围统计数组复位游标

	//-----------------模块连线-----------------//
	wire core_select_ready,core_selected;
	wire core_table_ready,core_table_loaded,core_table_fault;
	wire core_load_ready,core_busy,core_done,core_fault;
	wire core_output_valid,core_export_done;
	wire signed [7:0]core_output_data;
	wire [8:0]core_output_index;
	wire [31:0]core_cycles;
	wire flag_table_accept,flag_load_accept,flag_output_accept;
	wire flag_request_accept,flag_response_accept,flag_progress;
	wire flag_halo_load;
	wire [2:0]wire_load_kind;
	wire [10:0]wire_load_address;
	wire signed [31:0]wire_load_data;
	wire flag_output_ready;
	wire flag_final_counts;

	//-----------------输出连线-----------------//
	assign o_req_valid = i_rstn && !flag_fault && (state_current == ST_WRITE || state_current == ST_READ);
	assign o_req_write = state_current == ST_WRITE;
	assign o_req_addr = reg_address;
	assign o_req_data = reg_word;
	assign o_rsp_ready = i_rstn && !flag_fault && (state_current == ST_WRITE_RESPONSE || state_current == ST_READ_RESPONSE);
	assign o_status = flag_fault || state_current == ST_FAIL ? 2'd2 : (state_current == ST_PASS ? 2'd1 : 2'd0);
	assign o_error = reg_error_o;
	assign o_phase = state_current;
	assign o_writes = cnt_writes_o;
	assign o_reads = cnt_reads_o;
	assign o_output_bytes = cnt_output_bytes_o;
	assign o_cycles = cnt_cycles_o;
	assign o_address = reg_address;
	assign o_expected = reg_expected_o;
	assign o_actual = reg_actual_o;
	assign o_cycle_bins = {cnt_bins[9],cnt_bins[8],cnt_bins[7],cnt_bins[6],cnt_bins[5],
	                       cnt_bins[4],cnt_bins[3],cnt_bins[2],cnt_bins[1],cnt_bins[0]};

	//-----------------其他信号连线-----------------//
	assign flag_halo_load = state_current == ST_HALO_BYTE;
	assign wire_load_kind = flag_halo_load ? 3'd0 : reg_command[48:46];
	assign wire_load_address = flag_halo_load ? cnt_halo_address : reg_command[59:49];
	assign wire_load_data = flag_halo_load ? {{24{reg_word[7]}},reg_word[7:0]} : reg_command[31:0];
	assign flag_table_accept = state_current == ST_TABLE && core_table_ready;
	assign flag_load_accept = (state_current == ST_LOAD || flag_halo_load) && core_load_ready;
	assign flag_output_ready = !flag_fault && (state_current == ST_STEM_BYTE || state_current == ST_OUTPUT_BYTE);
	assign flag_output_accept = core_output_valid && flag_output_ready;
	assign flag_request_accept = o_req_valid && i_req_ready;
	assign flag_response_accept = i_rsp_valid && o_rsp_ready;
	assign flag_progress = flag_table_accept || flag_load_accept || flag_output_accept ||
	                       flag_request_accept || flag_response_accept || core_done ||
	                       (state_current == ST_SELECT && core_select_ready);
	assign flag_final_counts = cnt_writes_o == 9'd256 && cnt_reads_o == 9'd289 &&
	                           cnt_output_bytes_o == 11'd1536 && cnt_down2_tile == 3'd4 && cnt_halo_address == 11'd1296;

	// 固定ROM文件与参考生成器绑定；首轮核输入只来自加载程序。
	initial begin
		$readmemh("stem_golden.hex",reg_stem_golden);
		$readmemh("stem_addresses.hex",reg_addresses);
		$readmemh("halo_map.hex",reg_halo_map);
		$readmemh("pw_golden.hex",reg_output_golden);
	end

	// 同步ROM读边界无需清空数据；状态机只在取数后的状态使用它。
	always@(posedge i_clk)begin
		reg_golden <= reg_stem_golden[reg_golden_index];
		reg_address <= reg_addresses[reg_golden_index][24:0];
		if(state_current == ST_HALO_MAP)begin
			reg_map <= reg_halo_map[{cnt_down2_tile[1:0],cnt_halo_pixel}];
		end
		if(state_current == ST_OUTPUT_FETCH)begin
			reg_output_expected <= reg_output_golden[cnt_output_bytes_o];
		end
	end

	// 每个有效拍只进入一个端点分类，不把并行模块的忙拍相加。
	always@(*)begin
		reg_category = 4'd9;
		case(state_current)
			ST_PHY:begin reg_category = 4'd0; end
			ST_TABLE,ST_LOAD:begin reg_category = 4'd1; end
			ST_RUN:begin reg_category = core_selected ? 4'd6 : 4'd2; end
			ST_WRITE,ST_WRITE_RESPONSE:begin reg_category = 4'd3; end
			ST_READ_PREPARE,ST_READ,ST_READ_RESPONSE,ST_READ_CHECK:begin reg_category = 4'd4; end
			ST_HALO_MAP,ST_HALO_DECODE,ST_HALO_BYTE:begin reg_category = 4'd5; end
			ST_STEM_BYTE,ST_STEM_CHECK:begin reg_category = 4'd7; end
			ST_OUTPUT_FETCH,ST_OUTPUT_BYTE:begin reg_category = 4'd8; end
			default:begin reg_category = 4'd9; end
		endcase
	end

	// 状态寄存器只随组合决策推进，故障在任意阶段优先取消本地发射。
	always@(posedge i_clk or negedge i_rstn)begin
		if(!i_rstn)begin state_current <= ST_PHY; end
		else begin state_current <= state_next; end
	end

	// 无默认跳转、无自动重试；每次读取都等待完整真实响应。
	always@(*)begin
		state_next = state_current;
		case(state_current)
			ST_PHY:begin if(i_phy_ready)begin state_next = ST_FETCH; end end
			ST_FETCH:begin state_next = ST_DECODE; end
			ST_DECODE:begin
				case(reg_command[63:60])
					4'd0:begin state_next = ST_TABLE; end
					4'd1:begin state_next = ST_LOAD; end
					4'd2:begin state_next = ST_START; end
					4'd3,4'd6:begin state_next = ST_EXPORT; end
					4'd4:begin state_next = ST_SELECT; end
					4'd5:begin state_next = ST_HALO_MAP; end
					4'd7:begin state_next = flag_final_counts ? ST_PASS : ST_FAIL; end
					default:begin state_next = ST_FAIL; end
				endcase
			end
			ST_TABLE:begin if(flag_table_accept)begin state_next = ST_ADVANCE; end end
			ST_LOAD:begin if(flag_load_accept)begin state_next = ST_ADVANCE; end end
			ST_START:begin state_next = ST_RUN; end
			ST_RUN:begin if(core_done)begin state_next = ST_ADVANCE; end end
			ST_EXPORT:begin state_next = core_selected ? ST_OUTPUT_FETCH : ST_STEM_BYTE; end
			ST_STEM_BYTE:begin if(flag_output_accept && cnt_byte == 4'd15)begin state_next = ST_STEM_CHECK; end end
			ST_STEM_CHECK:begin state_next = reg_word == reg_golden ? ST_WRITE : ST_FAIL; end
			ST_WRITE:begin if(flag_request_accept)begin state_next = ST_WRITE_RESPONSE; end end
			ST_WRITE_RESPONSE:begin
				if(flag_response_accept)begin
					state_next = cnt_export == 9'd256 ? ST_ADVANCE : ST_STEM_BYTE;
				end
			end
			ST_SELECT:begin if(core_select_ready)begin state_next = ST_ADVANCE; end end
			ST_HALO_MAP:begin state_next = ST_HALO_DECODE; end
			ST_HALO_DECODE:begin state_next = reg_map[8] ? ST_HALO_BYTE : ST_READ_PREPARE; end
			ST_READ_PREPARE:begin state_next = ST_READ; end
			ST_READ:begin if(flag_request_accept)begin state_next = ST_READ_RESPONSE; end end
			ST_READ_RESPONSE:begin if(flag_response_accept)begin state_next = ST_READ_CHECK; end end
			ST_READ_CHECK:begin state_next = reg_word == reg_golden ? ST_HALO_BYTE : ST_FAIL; end
			ST_HALO_BYTE:begin
				if(flag_load_accept && cnt_byte == 4'd15)begin
					state_next = cnt_halo_pixel == 7'd80 ? ST_ADVANCE : ST_HALO_MAP;
				end
			end
			ST_OUTPUT_FETCH:begin state_next = ST_OUTPUT_BYTE; end
			ST_OUTPUT_BYTE:begin
				if(flag_output_accept)begin
					state_next = cnt_tile_output == 9'd383 ? ST_ADVANCE : ST_OUTPUT_FETCH;
				end
			end
			ST_ADVANCE:begin state_next = ST_FETCH; end
			ST_PASS:begin state_next = ST_PASS; end
			ST_FAIL:begin state_next = ST_FAIL; end
			default:begin state_next = ST_FAIL; end
		endcase
		if(flag_fault)begin state_next = ST_FAIL; end
	end

	// 数据与身份在对应的真实握手沿更新；整个实验不复用DDR地址。
	always@(posedge i_clk or negedge i_rstn)begin
		if(!i_rstn)begin
			cnt_program <= 13'd0;
			reg_golden_index <= 8'd0;
			cnt_export <= 9'd0;
			cnt_down2_tile <= 3'd0;
			cnt_tile_output <= 9'd0;
			cnt_byte <= 4'd0;
			cnt_halo_pixel <= 7'd0;
			cnt_halo_address <= 11'd0;
			cnt_writes_o <= 9'd0;
			cnt_reads_o <= 9'd0;
			cnt_output_bytes_o <= 11'd0;
			reg_word <= 128'd0;
			reg_expected_o <= 128'd0;
			reg_actual_o <= 128'd0;
			reg_error_o <= 4'd0;
			flag_fault <= 1'b0;
			cnt_watchdog <= 27'd0;
			cnt_cycles_o <= 32'd0;
			for(bin=0;bin<10;bin=bin+1)begin cnt_bins[bin] <= 32'd0; end
		end else begin
			if(state_current != ST_PASS && state_current != ST_FAIL)begin
				cnt_cycles_o <= cnt_cycles_o + 32'd1;
				cnt_bins[reg_category] <= cnt_bins[reg_category] + 32'd1;
			end
			if(state_current != state_next || flag_progress)begin cnt_watchdog <= 27'd0; end
			else if(state_current != ST_PASS && state_current != ST_FAIL)begin cnt_watchdog <= cnt_watchdog + 27'd1; end
			if(!flag_fault)begin
			case(state_current)
				ST_DECODE:begin
					if(reg_command[63:60] == 4'd3)begin cnt_export <= 9'd0; cnt_byte <= 4'd0; end
					if(reg_command[63:60] == 4'd6)begin cnt_tile_output <= 9'd0; end
					if(reg_command[63:60] == 4'd5)begin cnt_halo_pixel <= 7'd0; cnt_halo_address <= 11'd0; end
					if(reg_command[63:60] > 4'd7 || (reg_command[63:60] == 4'd7 && !flag_final_counts))begin
						flag_fault <= 1'b1; reg_error_o <= 4'd8;
					end
				end
				ST_STEM_BYTE:begin
					if(flag_output_accept)begin
						reg_word <= {core_output_data,reg_word[127:8]};
						cnt_export <= cnt_export + 9'd1;
						cnt_byte <= cnt_byte + 4'd1;
						if(core_output_index != cnt_export)begin flag_fault <= 1'b1; reg_error_o <= 4'd3; end
					end
				end
				ST_STEM_CHECK:begin
					reg_expected_o <= reg_golden; reg_actual_o <= reg_word;
					if(reg_word != reg_golden)begin flag_fault <= 1'b1; reg_error_o <= 4'd4; end
				end
				ST_WRITE_RESPONSE:begin
					if(flag_response_accept)begin
						cnt_writes_o <= cnt_writes_o + 9'd1;
						if(reg_golden_index != 8'd255)begin reg_golden_index <= reg_golden_index + 8'd1; end
					end
				end
				ST_HALO_DECODE:begin
					cnt_byte <= 4'd0;
					if(reg_map[8])begin reg_word <= 128'd0; end
					else begin reg_golden_index <= reg_map[7:0]; end
				end
				ST_READ_RESPONSE:begin
					if(flag_response_accept)begin reg_word <= i_rsp_data; cnt_reads_o <= cnt_reads_o + 9'd1; end
				end
				ST_READ_CHECK:begin
					reg_expected_o <= reg_golden; reg_actual_o <= reg_word;
					if(reg_word != reg_golden)begin flag_fault <= 1'b1; reg_error_o <= 4'd5; end
				end
				ST_HALO_BYTE:begin
					if(flag_load_accept)begin
						reg_word <= {8'd0,reg_word[127:8]};
						cnt_byte <= cnt_byte + 4'd1;
						cnt_halo_address <= cnt_halo_address + 11'd1;
						if(cnt_byte == 4'd15)begin cnt_halo_pixel <= cnt_halo_pixel + 7'd1; end
					end
				end
				ST_OUTPUT_BYTE:begin
					if(flag_output_accept)begin
						cnt_output_bytes_o <= cnt_output_bytes_o + 11'd1;
						cnt_tile_output <= cnt_tile_output + 9'd1;
						if(cnt_tile_output == 9'd383)begin cnt_down2_tile <= cnt_down2_tile + 3'd1; end
						if(core_output_index != cnt_tile_output || core_output_data != reg_output_expected)begin
							flag_fault <= 1'b1; reg_error_o <= 4'd6;
							reg_expected_o <= {120'd0,reg_output_expected}; reg_actual_o <= {120'd0,core_output_data};
						end
					end
				end
				ST_ADVANCE:begin
					cnt_program <= cnt_program + 13'd1;
					if({1'b0,cnt_program}+14'd1 >= PROGRAM_LENGTH)begin flag_fault <= 1'b1; reg_error_o <= 4'd8; end
				end
				default:begin end
			endcase
			end
			if(!flag_fault)begin
				if(i_ddr_fault)begin flag_fault <= 1'b1; reg_error_o <= 4'd1; end
				else if(core_fault || core_table_fault)begin flag_fault <= 1'b1; reg_error_o <= 4'd2; end
				else if(flag_response_accept && i_rsp_error != 4'd0)begin flag_fault <= 1'b1; reg_error_o <= 4'd7; end
				else if(cnt_watchdog == C_TIMEOUT && state_current != ST_PASS && state_current != ST_FAIL)begin
					flag_fault <= 1'b1; reg_error_o <= 4'd9;
				end
			end
		end
	end

	// 仅在原FETCH沿取指、ADVANCE沿推进，停顿不消耗命令。
	road_frontend_load_sequence u_load_sequence(
		.i_clk(i_clk),.i_rstn(i_rstn),
		.i_fetch(state_current == ST_FETCH),.i_advance(state_current == ST_ADVANCE && !flag_fault),
		.o_command(reg_command)
	);

	// 唯一共享核保留内部算术、表、first/last、尾lane及写回规则。
	road_frontend_shared_core u_core(
		.i_clk(i_clk),.i_rstn(i_rstn),
		.i_select_valid(!flag_fault && state_current == ST_SELECT),.i_select_down2(reg_command[0]),
		.o_select_ready(core_select_ready),.o_selected_down2(core_selected),
		.i_table_valid(!flag_fault && state_current == ST_TABLE),.i_table_addr(reg_command[58:49]),.i_table_data(reg_command[15:0]),
		.o_table_ready(core_table_ready),.o_table_loaded(core_table_loaded),.o_table_fault(core_table_fault),
		.i_load_valid(!flag_fault && (state_current == ST_LOAD || flag_halo_load)),.i_load_kind(wire_load_kind),
		.i_load_addr(wire_load_address),.i_load_data(wire_load_data),.o_load_ready(core_load_ready),
		.i_start(!flag_fault && state_current == ST_START),.i_commit_ready(1'b1),
		.o_busy(core_busy),.o_done(core_done),.o_fault(core_fault),.o_core_cycles(core_cycles),
		.i_export_start(!flag_fault && state_current == ST_EXPORT),.i_output_ready(flag_output_ready),
		.o_output_valid(core_output_valid),.o_output_data(core_output_data),.o_output_index(core_output_index),
		.o_export_done(core_export_done)
	);
endmodule
