`timescale 1ns / 1ps

// Company: RoadYOLO project
// Engineer: Codex
// Create Date: 2026/10/15
// Design Name: Complete frontend DDR traversal
// Module Name: road_stem_ddr_sequence
// Description: Fixed 512x288 Stem DW PW tensor traversal
// Simulations: tests/tb_frontend_ddr_tensor.v
// Referrences: reference/contract.json
// Dependencies: Frozen frontend core and fixed layer program
// Version: V1.0
// Revision Date: 2026/10/15
// History: 2026/10/15 V1.0 Codex Create file
// 版权归属: RoadYOLO project
// 开发人员: Codex
// 创建日期: 2026年10月15日
// 设计名称: 完整前三层存储遍历
// 模块名称: road_stem_ddr_sequence
// 模块说明: 小型循环与单字读缓存连接完整RGB、Stem及PW张量
// 仿真工程: tests/tb_frontend_ddr_tensor.v
// 参考资料: reference/contract.json
// 依赖文件: 原算术核及新固定层加载器
// 当前版本: V1.0
// 修订日期: 2026年10月15日
// 修订历史: 2026年10月15日 V1.0 Codex 创建文件
module road_stem_ddr_sequence
#(
	parameter [26:0] C_TIMEOUT = 27'h7ffffff // 无进展看门狗
)
(
	input i_clk, // 100MHz计算时钟
	input i_rstn, // 与DDR共同复位
	input i_phy_ready, // 已同步的DDR初始化许可
	input i_ddr_fault, // 邮箱粘滞故障
	input i_req_ready, // 唯一请求接受
	input i_rsp_valid, // 完整冻结返回
	input [127:0]i_rsp_data, // DDR真实返回
	input [3:0]i_rsp_error, // 原请求错误
	output o_req_valid, // 请求保持到接受
	output o_req_write, // 读写分型
	output [24:0]o_req_addr, // 原生半字地址
	output [127:0]o_req_data, // 当前完整写字
	output o_rsp_ready, // 仅消费所属响应
	output [1:0]o_status, // 等待、通过、失败
	output [3:0]o_error, // 首个错误编号
	output [4:0]o_phase, // 当前外层状态
	output [31:0]o_writes, // 真实写接受回执总数
	output [31:0]o_reads, // 真实已消费读返回总数
	output [31:0]o_output_bytes, // 完整PW导出字节数
	output [31:0]o_cycles, // 含初始化与图像装载总周期
	output [319:0]o_cycle_bins, // 十项互斥周期
	output [24:0]o_address, // 当前读写原生地址
	output [127:0]o_expected, // 最近输出核对期望
	output [127:0]o_actual // 最近输出核对实际
);
	//-------------状态参数区域-------------//
	localparam [4:0] ST_PHY=5'd0;
	localparam [4:0] ST_PATTERN=5'd1;
	localparam [4:0] ST_WRITE=5'd2;
	localparam [4:0] ST_WRITE_RESPONSE=5'd3;
	localparam [4:0] ST_FETCH=5'd4;
	localparam [4:0] ST_DECODE=5'd5;
	localparam [4:0] ST_TABLE=5'd6;
	localparam [4:0] ST_LOAD=5'd7;
	localparam [4:0] ST_START=5'd8;
	localparam [4:0] ST_RUN=5'd9;
	localparam [4:0] ST_EXPORT=5'd10;
	localparam [4:0] ST_EXPORT_BYTE=5'd11;
	localparam [4:0] ST_EXPORT_CHECK=5'd12;
	localparam [4:0] ST_SELECT=5'd13;
	localparam [4:0] ST_MAP=5'd14;
	localparam [4:0] ST_ROW=5'd15;
	localparam [4:0] ST_ADDRESS=5'd16;
	localparam [4:0] ST_CACHE=5'd17;
	localparam [4:0] ST_READ=5'd18;
	localparam [4:0] ST_READ_RESPONSE=5'd19;
	localparam [4:0] ST_HALO_BYTE=5'd20;
	localparam [4:0] ST_ADVANCE=5'd21;
	localparam [4:0] ST_PASS=5'd22;
	localparam [4:0] ST_FAIL=5'd23;

	//---------------计数信号---------------//
	reg [14:0]cnt_input_word=0; // 27648个RGB输入字
	reg [6:0]cnt_input_column=0; // 每行96个128位字
	reg [1:0]cnt_pattern_column=0; // 周期图案每行三个字
	reg [5:0]cnt_pattern_row=0; // 十六个周期行的ROM基址
	reg [11:0]cnt_stem_tile=0; // 完整2304块完成数
	reg [5:0]cnt_stem_x=0; // Stem每行64块
	reg [5:0]cnt_stem_y=0; // Stem共有36块行
	reg [9:0]cnt_down_tile=0; // 完整576块完成数
	reg [4:0]cnt_down_x=0; // 下采样每行32块
	reg [4:0]cnt_down_y=0; // 下采样共有18块行
	reg [3:0]cnt_halo_x=0; // 当前九列窗口
	reg [3:0]cnt_halo_y=0; // 当前九行窗口
	reg [3:0]cnt_channel=0; // RGB三通道或特征十六通道
	reg [10:0]cnt_halo_address=0; // 原核局部装载地址
	reg [8:0]cnt_export=0; // 当前256或384字节导出位置
	reg [3:0]cnt_byte=0; // 当前输出字内位置
	reg [13:0]cnt_program=0; // 固定10800个宏命令
	reg [31:0]cnt_writes_o=0;
	reg [31:0]cnt_reads_o=0;
	reg [31:0]cnt_output_bytes_o=0;
	reg [31:0]cnt_cycles_o=0;
	reg [31:0]cnt_bins[0:9];
	reg [26:0]cnt_watchdog=0;
	integer bin;

	//--------------状态机信号--------------//
	reg [4:0]state_current=0;
	reg [4:0]state_next=0;

	//--------------寄存器信号--------------//
	reg [127:0]reg_pattern[0:47]; // 只保存周期图案，不保存完整输入帧
	reg [127:0]reg_golden[0:255]; // 240个有效分类黄金字
	reg [127:0]reg_expected=0;
	reg [127:0]reg_word=0;
	reg [127:0]reg_cache=0; // 唯一16字节输入缓存
	reg [24:0]reg_cache_address=0;
	reg [24:0]reg_address=0;
	reg [24:0]reg_input_address=25'h1a00000;
	reg [24:0]reg_stem_address=25'h1a80000;
	reg [24:0]reg_pw_address=25'h1b00000;
	reg [9:0]reg_source_x=0;
	reg [9:0]reg_source_y=0;
	reg [24:0]reg_row_offset=0;
	reg [10:0]reg_column_offset=0;
	reg [24:0]reg_feature_offset=0;
	reg [3:0]reg_byte_lane=0;
	reg [7:0]reg_golden_index=0;
	reg [1:0]reg_write_owner=0; // 零RGB、一Stem、二PW
	reg [3:0]reg_category=0;
	reg [3:0]reg_error_o=0;
	reg [127:0]reg_expected_o=0;
	reg [127:0]reg_actual_o=0;

	//---------------标志信号---------------//
	reg flag_fault=0;
	reg flag_cache_valid=0;
	reg flag_halo_rgb=0;
	reg flag_padding=0;
	wire flag_request_accept,flag_response_accept;
	wire flag_table_accept,flag_load_accept,flag_output_accept;
	wire flag_halo_last,flag_word_last,flag_final_counts,flag_progress;
	wire flag_rgb_reuse; // 当前像素的下一通道仍在已命中的16字节缓存内
	wire core_select_ready,core_selected,core_table_ready,core_table_loaded,core_table_fault;
	wire core_load_ready,core_busy,core_done,core_fault,core_output_valid,core_export_done;
	wire [7:0]core_output_data;
	wire [8:0]core_output_index;
	wire [31:0]core_cycles;
	wire [63:0]reg_command;
	wire [7:0]wire_halo_byte;
	wire [2:0]wire_load_kind;
	wire [10:0]wire_load_address;
	wire signed [31:0]wire_load_data;

	//-------------其他信号连线-------------//
	assign flag_request_accept=o_req_valid && i_req_ready;
	assign flag_response_accept=i_rsp_valid && o_rsp_ready;
	assign flag_table_accept=i_rstn && !flag_fault && state_current==ST_TABLE && core_table_ready;
	assign flag_load_accept=i_rstn && !flag_fault && (state_current==ST_LOAD || state_current==ST_HALO_BYTE) && core_load_ready;
	assign flag_output_accept=i_rstn && !flag_fault && state_current==ST_EXPORT_BYTE && core_output_valid;
	assign flag_halo_last=flag_halo_rgb ? cnt_halo_address==11'd242 : cnt_halo_address==11'd1295;
	assign flag_word_last=core_selected ? cnt_export==9'd384 : cnt_export==9'd256;
	assign flag_final_counts=cnt_input_word==15'd27648 && cnt_stem_tile==12'd2304 && cnt_down_tile==10'd576 &&
		cnt_writes_o==32'd78336 && cnt_reads_o==32'd97564 && cnt_output_bytes_o==32'd221184 && cnt_program==14'd10799;
	assign flag_progress=flag_request_accept || flag_response_accept || flag_table_accept || flag_load_accept || flag_output_accept || core_done;
	assign flag_rgb_reuse=flag_halo_rgb && !flag_padding && cnt_channel<4'd2 &&
		flag_cache_valid && reg_address==reg_cache_address && reg_byte_lane<4'd15;
	assign wire_halo_byte=flag_halo_rgb ? reg_cache[reg_byte_lane*8+:8] : reg_cache[cnt_channel*8+:8];
	assign wire_load_kind=state_current==ST_HALO_BYTE ? (flag_halo_rgb && flag_padding ? 3'd1 : 3'd0) : reg_command[48:46];
	assign wire_load_address=state_current==ST_HALO_BYTE ? cnt_halo_address : reg_command[59:49];
	assign wire_load_data=state_current!=ST_HALO_BYTE ? reg_command[31:0] :
		(flag_padding ? 32'd0 : (flag_halo_rgb ? {24'd0,wire_halo_byte} : {{24{wire_halo_byte[7]}},wire_halo_byte}));

	//-------------输出信号连线-------------//
	assign o_req_valid=i_rstn && !flag_fault && (state_current==ST_WRITE || state_current==ST_READ);
	assign o_req_write=state_current==ST_WRITE;
	assign o_req_addr=reg_address;
	assign o_req_data=reg_word;
	assign o_rsp_ready=i_rstn && !flag_fault && (state_current==ST_WRITE_RESPONSE || state_current==ST_READ_RESPONSE);
	assign o_status=flag_fault || state_current==ST_FAIL ? 2'd2 : (state_current==ST_PASS ? 2'd1 : 2'd0);
	assign o_error=reg_error_o;
	assign o_phase=state_current;
	assign o_writes=cnt_writes_o;
	assign o_reads=cnt_reads_o;
	assign o_output_bytes=cnt_output_bytes_o;
	assign o_cycles=cnt_cycles_o;
	assign o_cycle_bins={cnt_bins[9],cnt_bins[8],cnt_bins[7],cnt_bins[6],cnt_bins[5],cnt_bins[4],cnt_bins[3],cnt_bins[2],cnt_bins[1],cnt_bins[0]};
	assign o_address=reg_address;
	assign o_expected=reg_expected_o;
	assign o_actual=reg_actual_o;

	//--------------状态机区域--------------//
	always@(posedge i_clk or negedge i_rstn)begin
		if(!i_rstn)begin state_current<=ST_PHY; end
		else begin state_current<=state_next; end
	end

	// 所有外部传输等待真实接受/返回，写字不能靠固定等待发布。
	always@(*)begin
		state_next=state_current;
		case(state_current)
			ST_PHY:begin if(i_phy_ready)begin state_next=ST_PATTERN; end end
			ST_PATTERN:begin state_next=ST_WRITE; end
			ST_WRITE:begin if(flag_request_accept)begin state_next=ST_WRITE_RESPONSE; end end
			ST_WRITE_RESPONSE:begin
				if(flag_response_accept)begin
					if(reg_write_owner==2'd0)begin state_next=cnt_input_word==15'd27647 ? ST_FETCH : ST_PATTERN; end
					else begin state_next=flag_word_last ? ST_ADVANCE : ST_EXPORT_BYTE; end
				end
			end
			ST_FETCH:begin state_next=ST_DECODE; end
			ST_DECODE:begin
				case(reg_command[63:60])
					4'd0:begin state_next=ST_TABLE; end
					4'd1:begin state_next=ST_LOAD; end
					4'd2:begin state_next=ST_START; end
					4'd3,4'd6:begin state_next=ST_EXPORT; end
					4'd4:begin state_next=ST_SELECT; end
					4'd5,4'd8:begin state_next=ST_MAP; end
					4'd7:begin state_next=flag_final_counts ? ST_PASS : ST_FAIL; end
					default:begin state_next=ST_FAIL; end
				endcase
			end
			ST_TABLE:begin if(flag_table_accept)begin state_next=ST_ADVANCE; end end
			ST_LOAD:begin if(flag_load_accept)begin state_next=ST_ADVANCE; end end
			ST_START:begin state_next=ST_RUN; end
			ST_RUN:begin if(core_done)begin state_next=ST_ADVANCE; end end
			ST_EXPORT:begin state_next=ST_EXPORT_BYTE; end
			ST_EXPORT_BYTE:begin if(flag_output_accept && cnt_byte==4'd15)begin state_next=ST_EXPORT_CHECK; end end
			ST_EXPORT_CHECK:begin state_next=reg_word==reg_expected ? ST_WRITE : ST_FAIL; end
			ST_SELECT:begin if(core_select_ready)begin state_next=ST_ADVANCE; end end
			ST_MAP:begin state_next=ST_ROW; end
			ST_ROW:begin state_next=ST_ADDRESS; end
			ST_ADDRESS:begin state_next=ST_CACHE; end
			ST_CACHE:begin state_next=flag_padding || (flag_cache_valid && reg_address==reg_cache_address) ? ST_HALO_BYTE : ST_READ; end
			ST_READ:begin if(flag_request_accept)begin state_next=ST_READ_RESPONSE; end end
			ST_READ_RESPONSE:begin if(flag_response_accept)begin state_next=ST_HALO_BYTE; end end
			ST_HALO_BYTE:begin
				if(flag_load_accept)begin
					if(flag_halo_last)begin state_next=ST_ADVANCE; end
					else if(flag_rgb_reuse)begin state_next=ST_HALO_BYTE; end
					else if(flag_halo_rgb || cnt_channel==4'd15)begin state_next=ST_MAP; end
				end
			end
			ST_ADVANCE:begin state_next=ST_FETCH; end
			ST_PASS:begin state_next=ST_PASS; end
			ST_FAIL:begin state_next=ST_FAIL; end
			default:begin state_next=ST_FAIL; end
		endcase
		if(flag_fault)begin state_next=ST_FAIL; end
	end

	//-----------状态任务处理区域-----------//
	// 地址预计算隔开坐标、行偏移及最终原生地址加法。
	always@(posedge i_clk or negedge i_rstn)begin
		if(!i_rstn)begin
			reg_source_x<=10'd0; reg_source_y<=10'd0;
			reg_row_offset<=25'd0; reg_column_offset<=11'd0; reg_feature_offset<=25'd0;
			reg_byte_lane<=4'd0; flag_padding<=1'b0;
		end else begin
			if(state_current==ST_MAP)begin
				reg_source_x<=(flag_halo_rgb ? {1'b0,cnt_stem_x,3'd0} : {2'd0,cnt_down_x,3'd0})+{6'd0,cnt_halo_x}-10'd1;
				reg_source_y<=(flag_halo_rgb ? {1'b0,cnt_stem_y,3'd0} : {2'd0,cnt_down_y,3'd0})+{6'd0,cnt_halo_y}-10'd1;
			end
			if(state_current==ST_ROW)begin
				flag_padding<=reg_source_x[9] || reg_source_y[9];
				reg_row_offset<=({15'd0,reg_source_y}<<9)+({15'd0,reg_source_y}<<8);
				reg_column_offset<={1'b0,reg_source_x}+{reg_source_x,1'b0}+{7'd0,cnt_channel};
				reg_feature_offset<={6'd0,reg_source_y[7:2],reg_source_x[7:2],7'd0}+{18'd0,reg_source_y[1:0],reg_source_x[1:0],3'd0};
			end
			if(state_current==ST_ADDRESS)begin reg_byte_lane<=reg_column_offset[3:0]; end
			// 仅真实装载接受才推进lane；跨词、padding及缓存无效回原地址流水。
			if(state_current==ST_HALO_BYTE && flag_load_accept && flag_rgb_reuse)begin
				reg_byte_lane<=reg_byte_lane+4'd1;
			end
		end
	end

	// 只有输入读完整返回才更新缓存；每个新tile使缓存失效。
	always@(posedge i_clk or negedge i_rstn)begin
		if(!i_rstn)begin
			flag_cache_valid<=1'b0; reg_cache<=128'd0; reg_cache_address<=25'd0;
		end else begin
			if(state_current==ST_DECODE && (reg_command[63:60]==4'd5 || reg_command[63:60]==4'd8))begin flag_cache_valid<=1'b0; end
			if(state_current==ST_READ_RESPONSE && flag_response_accept)begin
				reg_cache<=i_rsp_data; reg_cache_address<=reg_address; flag_cache_valid<=1'b1;
			end
		end
	end

	// 固定图案写入全部输入区；Stem/PW导出逐字比较后写各自完整张量。
	always@(posedge i_clk or negedge i_rstn)begin
		if(!i_rstn)begin
			cnt_input_word<=0; cnt_input_column<=0; cnt_pattern_column<=0; cnt_pattern_row<=0;
			reg_input_address<=25'h1a00000; reg_stem_address<=25'h1a80000; reg_pw_address<=25'h1b00000;
			reg_write_owner<=0; reg_address<=0; reg_word<=0; cnt_export<=0; cnt_byte<=0;
			reg_golden_index<=0; reg_expected_o<=0; reg_actual_o<=0;
			cnt_writes_o<=0; cnt_reads_o<=0; cnt_output_bytes_o<=0;
		end else if(!flag_fault)begin
			case(state_current)
				ST_PATTERN:begin
					reg_word<=reg_pattern[cnt_pattern_row+{4'd0,cnt_pattern_column}];
					reg_address<=reg_input_address; reg_write_owner<=2'd0;
				end
				ST_DECODE:begin
					if(reg_command[63:60]==4'd3)begin
						reg_write_owner<=2'd1;
						reg_golden_index<=((cnt_stem_y==0 ? 8'd0 : (cnt_stem_y[0] ? 8'd6 : 8'd3))+
							(cnt_stem_x==0 ? 8'd0 : (cnt_stem_x[0] ? 8'd2 : 8'd1)))<<4;
					end
					if(reg_command[63:60]==4'd6)begin
						reg_write_owner<=2'd2;
						reg_golden_index<=8'd144+(cnt_down_y==0 ? 8'd0 : 8'd48)+(cnt_down_x==0 ? 8'd0 : 8'd24);
					end
				end
				ST_EXPORT:begin cnt_export<=0; cnt_byte<=0; reg_word<=0; end
				ST_EXPORT_BYTE:begin
					if(flag_output_accept)begin
						reg_word<={core_output_data,reg_word[127:8]}; cnt_export<=cnt_export+9'd1; cnt_byte<=cnt_byte+4'd1;
						if(core_selected)begin cnt_output_bytes_o<=cnt_output_bytes_o+32'd1; end
					end
				end
				ST_EXPORT_CHECK:begin
					reg_expected_o<=reg_expected; reg_actual_o<=reg_word;
					reg_address<=core_selected ? reg_pw_address : reg_stem_address;
				end
				ST_ADDRESS:begin
					reg_address<=flag_halo_rgb ? 25'h1a00000+reg_row_offset+{15'd0,reg_column_offset[10:4],3'd0} : 25'h1a80000+reg_feature_offset;
				end
				ST_READ_RESPONSE:begin if(flag_response_accept)begin cnt_reads_o<=cnt_reads_o+32'd1; end end
				ST_WRITE_RESPONSE:begin
					if(flag_response_accept)begin
						cnt_writes_o<=cnt_writes_o+32'd1;
						if(reg_write_owner==2'd0)begin
							cnt_input_word<=cnt_input_word+15'd1; reg_input_address<=reg_input_address+25'd8;
							cnt_pattern_column<=cnt_pattern_column==2'd2 ? 2'd0 : cnt_pattern_column+2'd1;
							if(cnt_input_column==7'd95)begin
								cnt_input_column<=0; cnt_pattern_row<=cnt_pattern_row==6'd45 ? 6'd0 : cnt_pattern_row+6'd3;
							end else begin cnt_input_column<=cnt_input_column+7'd1; end
						end else begin
							reg_golden_index<=reg_golden_index+8'd1;
							if(reg_write_owner==2'd1)begin reg_stem_address<=reg_stem_address+25'd8; end
							else begin reg_pw_address<=reg_pw_address+25'd8; end
						end
					end
				end
				default:begin end
			endcase
		end
	end

	// 所有局部窗口计数由真实装载接受推进，末通道才换空间位置。
	always@(posedge i_clk or negedge i_rstn)begin
		if(!i_rstn)begin
			flag_halo_rgb<=0; cnt_halo_x<=0; cnt_halo_y<=0; cnt_channel<=0; cnt_halo_address<=0;
			cnt_stem_tile<=0; cnt_stem_x<=0; cnt_stem_y<=0; cnt_down_tile<=0; cnt_down_x<=0; cnt_down_y<=0; cnt_program<=0;
		end else if(!flag_fault)begin
			if(state_current==ST_DECODE && (reg_command[63:60]==4'd5 || reg_command[63:60]==4'd8))begin
				flag_halo_rgb<=reg_command[63:60]==4'd8;
				cnt_halo_x<=0; cnt_halo_y<=0; cnt_channel<=0; cnt_halo_address<=0;
			end
			if(state_current==ST_HALO_BYTE && flag_load_accept)begin
				cnt_halo_address<=cnt_halo_address+11'd1;
				if((flag_halo_rgb && cnt_channel==4'd2) || (!flag_halo_rgb && cnt_channel==4'd15))begin
					cnt_channel<=0;
					if(cnt_halo_x==4'd8)begin cnt_halo_x<=0; cnt_halo_y<=cnt_halo_y+4'd1; end
					else begin cnt_halo_x<=cnt_halo_x+4'd1; end
				end else begin cnt_channel<=cnt_channel+4'd1; end
			end
			if(state_current==ST_ADVANCE)begin
				cnt_program<=cnt_program+14'd1;
				if(reg_command[63:60]==4'd3)begin
					cnt_stem_tile<=cnt_stem_tile+12'd1;
					if(cnt_stem_x==6'd63)begin cnt_stem_x<=0; cnt_stem_y<=cnt_stem_y+6'd1; end
					else begin cnt_stem_x<=cnt_stem_x+6'd1; end
				end
				if(reg_command[63:60]==4'd6)begin
					cnt_down_tile<=cnt_down_tile+10'd1;
					if(cnt_down_x==5'd31)begin cnt_down_x<=0; cnt_down_y<=cnt_down_y+5'd1; end
					else begin cnt_down_x<=cnt_down_x+5'd1; end
				end
			end
		end
	end

	// 分类互斥：活动流水的忙时间不重复加进端点总周期。
	always@(*)begin
		reg_category=4'd9;
		case(state_current)
			ST_PHY:begin reg_category=4'd0; end
			ST_PATTERN:begin reg_category=4'd1; end
			ST_TABLE,ST_LOAD:begin reg_category=4'd2; end
			ST_RUN:begin reg_category=core_selected ? 4'd7 : 4'd4; end
			ST_EXPORT,ST_EXPORT_BYTE,ST_EXPORT_CHECK:begin reg_category=core_selected ? 4'd8 : 4'd5; end
			ST_MAP,ST_ROW,ST_ADDRESS,ST_CACHE,ST_READ,ST_READ_RESPONSE,ST_HALO_BYTE:begin reg_category=flag_halo_rgb ? 4'd3 : 4'd6; end
			ST_WRITE,ST_WRITE_RESPONSE:begin reg_category=reg_write_owner==2'd0 ? 4'd1 : (reg_write_owner==2'd1 ? 4'd5 : 4'd8); end
			default:begin end
		endcase
	end

	// 首错闭锁，PASS后的外部DDR故障仍撤销成功状态。
	always@(posedge i_clk or negedge i_rstn)begin
		if(!i_rstn)begin
			flag_fault<=0; reg_error_o<=0; cnt_watchdog<=0; cnt_cycles_o<=0;
			for(bin=0;bin<10;bin=bin+1)begin cnt_bins[bin]<=0; end
		end else begin
			if(state_current!=ST_PASS && state_current!=ST_FAIL)begin
				cnt_cycles_o<=cnt_cycles_o+32'd1; cnt_bins[reg_category]<=cnt_bins[reg_category]+32'd1;
			end
			if(state_current!=state_next || flag_progress)begin cnt_watchdog<=0; end
			else if(state_current!=ST_PASS && state_current!=ST_FAIL)begin cnt_watchdog<=cnt_watchdog+27'd1; end
			if(!flag_fault)begin
				if(i_ddr_fault)begin flag_fault<=1; reg_error_o<=4'd1; end
				else if(core_fault || core_table_fault)begin flag_fault<=1; reg_error_o<=4'd2; end
				else if(flag_output_accept && core_output_index!=cnt_export)begin flag_fault<=1; reg_error_o<=4'd3; end
				else if(state_current==ST_EXPORT_CHECK && reg_word!=reg_expected)begin flag_fault<=1; reg_error_o<=4'd4; end
				else if(flag_response_accept && i_rsp_error!=0)begin flag_fault<=1; reg_error_o<=4'd7; end
				else if(state_current==ST_DECODE && ((reg_command[63:60]==4'd7 && !flag_final_counts) || reg_command[63:60]>4'd8))begin
					flag_fault<=1; reg_error_o<=4'd8;
				end else if(state_current==ST_ADVANCE && cnt_program>=14'd10799)begin flag_fault<=1; reg_error_o<=4'd8; end
				else if(cnt_watchdog==C_TIMEOUT && state_current!=ST_PASS && state_current!=ST_FAIL)begin flag_fault<=1; reg_error_o<=4'd9; end
			end
		end
	end

	//--------------主要任务处理区域--------------//
	always@(posedge i_clk)begin reg_expected<=reg_golden[reg_golden_index]; end

	//--------------初始化区域--------------//
	initial begin
		$readmemh("rgb_pattern_words.hex",reg_pattern);
		$readmemh("combined_golden.hex",reg_golden);
	end

	//------------模块实例化区域------------//
	road_frontend_layer_sequence u_layer_sequence(
		.i_clk(i_clk),.i_rstn(i_rstn),.i_fetch(state_current==ST_FETCH),
		.i_advance(state_current==ST_ADVANCE && !flag_fault),.o_command(reg_command)
	);
	road_frontend_shared_core u_core(
		.i_clk(i_clk),.i_rstn(i_rstn),
		.i_select_valid(!flag_fault && state_current==ST_SELECT),.i_select_down2(reg_command[0]),
		.o_select_ready(core_select_ready),.o_selected_down2(core_selected),
		.i_table_valid(!flag_fault && state_current==ST_TABLE),.i_table_addr(reg_command[58:49]),.i_table_data(reg_command[15:0]),
		.o_table_ready(core_table_ready),.o_table_loaded(core_table_loaded),.o_table_fault(core_table_fault),
		.i_load_valid(!flag_fault && (state_current==ST_LOAD || state_current==ST_HALO_BYTE)),
		.i_load_kind(wire_load_kind),.i_load_addr(wire_load_address),.i_load_data(wire_load_data),.o_load_ready(core_load_ready),
		.i_start(!flag_fault && state_current==ST_START),.i_commit_ready(1'b1),
		.o_busy(core_busy),.o_done(core_done),.o_fault(core_fault),.o_core_cycles(core_cycles),
		.i_export_start(!flag_fault && state_current==ST_EXPORT),.i_output_ready(!flag_fault && state_current==ST_EXPORT_BYTE),
		.o_output_valid(core_output_valid),.o_output_data(core_output_data),.o_output_index(core_output_index),.o_export_done(core_export_done)
	);
endmodule
