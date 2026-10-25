`timescale 1ns / 1ps

// 固定 Stem 的单 tile 调度器；算术算子外置，以便后续整图互斥复用。
module road_stem_tile_scheduler(
	input i_clk,
	input i_rstn,
	input i_table_loaded,
	input i_load_valid,
	input [2:0]i_load_kind,
	input [8:0]i_load_addr,
	input signed [31:0]i_load_data,
	output o_load_ready,
	input i_start,
	output o_busy,
	output o_done,
	output o_fault,
	output [31:0]o_core_cycles,
	output o_mac_valid,
	input i_mac_ready,
	output o_mac_first,
	output o_mac_last,
	output [7:0]o_mac_mask,
	output [63:0]o_mac_activation,
	output [191:0]o_mac_weight,
	output [95:0]o_mac_bias,
	input i_mac_result_valid,
	output o_mac_result_ready,
	input [95:0]i_mac_result,
	input i_mac_fault,
	output o_pp_valid,
	input i_pp_ready,
	output [95:0]o_pp_acc,
	output [95:0]o_pp_multipliers,
	output [17:0]o_pp_shifts,
	output [31:0]o_pp_post_multiplier,
	output [5:0]o_pp_post_shift,
	output [2:0]o_pp_mask,
	output [47:0]o_pp_tags,
	input i_pp_valid,
	output o_pp_ready,
	input signed [15:0]i_pp_data,
	input [15:0]i_pp_tag,
	input i_pp_int16,
	input i_pp_fault,
	input i_commit_ready,
	input i_export_start,
	output o_output_valid,
	input i_output_ready,
	output signed [7:0]o_output_data,
	output [7:0]o_output_index,
	output o_export_done
);
	localparam [3:0]ST_IDLE=4'd0, ST_PREPARE=4'd1, ST_SEND=4'd2, ST_MAC_WAIT=4'd3;
	localparam [3:0]ST_POST_WAIT=4'd4, ST_ADVANCE=4'd5, ST_DONE=4'd6, ST_EXPORT=4'd7, ST_FAULT=4'd8;
	reg [3:0]state_current, state_next; // 当前和下一调度状态。
	reg flag_load_state_ready; // 与当前IDLE严格等价，切断状态译码到多端口RAM写使能的长链。
	reg signed [7:0]reg_halo[0:242]; // 9×9×3，已中心化且 padding 为算子零。
	reg signed [7:0]reg_weight[0:431]; // 16×3×3×3 OIHW 驻留权重。
	reg flag_weight_write_pending; // 合法接收后下一沿写入，连续装载无气泡。
	reg [8:0]reg_weight_write_address; // 与写许可同沿保管的完整权重地址。
	reg signed [7:0]reg_weight_write_data; // 与写许可同沿保管的INT8权重。
	reg signed [31:0]reg_bias[0:15]; // first 仅加入一次的偏置。
	reg [31:0]reg_multiplier[0:15]; // 每逻辑输出通道的动态 pre 系数。
	reg [5:0]reg_shift[0:15]; // 每通道 pre 移位。
	reg [31:0]reg_post_multiplier; // 当前 Stem 的 post 系数。
	reg [5:0]reg_post_shift; // 当前 Stem 的 post 移位。
	reg signed [7:0]reg_output[0:255]; // 4×4×16 输出，仅完整 tile 可导出。
	reg [5:0]reg_loaded; // halo、weight、bias、multiplier、shift、post 六类完整性。
	reg [7:0]cnt_halo_address; // halo 顺序装载游标。
	reg [8:0]cnt_weight_address; // 权重顺序装载游标。
	reg [3:0]cnt_bias_address, cnt_multiplier_address, cnt_shift_address; // 逐通道参数游标。
	reg flag_post_address; // 两项 post 参数游标。
	reg flag_load_fault, flag_result_fault, flag_tile_valid, flag_export_done; // 有效性及粘滞故障。
	reg [3:0]cnt_position, cnt_channel; // tile 像素及输出组起始通道。
	reg [1:0]cnt_group; // 当前任务四组归约，独立于后处理的提交位置。
	reg [7:0]cnt_export; // 实际输出缓存读地址。
	reg [8:0]cnt_written; // 完整 tile 需要 256 次有效写回。
	reg [31:0]cnt_core_cycles; // 只计核心 busy 窗口，不含预装载和导出。
	reg [63:0]reg_activation; // 注册后的八个激活，反压时不变化。
	reg [191:0]reg_mac_weight; // 三路各八个注册权重。
	reg [95:0]reg_mac_bias; // 注册的三路偏置。
	reg [7:0]reg_mask; // 最后组仅三个输入有效。
	reg [63:0]next_activation; // 固定窗口展开的下一组激活。
	reg [191:0]next_weight; // 固定 OIHW 展开的下一组权重。
	reg [95:0]next_bias; // 无效输出尾路置零。
	reg [7:0]next_mask; // 对应当前归约组的输入掩码。
	reg [8:0]next_weight_base[0:2]; // 六组合法输出通道的OIHW基址，不使用地址乘法器。
	reg flag_load_legal; // 地址、范围及顺序校验结果。
	wire flag_start_accept, flag_load_accept, flag_mac_accept, flag_result_accept, flag_write_accept;
	wire flag_write_illegal; // 无效 tag、原始 INT16 或非 INT8 符号扩展禁止写入。
	wire [4:0]wire_channel_beta={1'b0,cnt_channel}+5'd1;
	wire [4:0]wire_channel_gamma={1'b0,cnt_channel}+5'd2;
	wire [15:0]wire_tag_alpha={8'd0,cnt_position,cnt_channel};
	wire [15:0]wire_tag_beta={8'd0,cnt_position,wire_channel_beta[3:0]};
	wire [15:0]wire_tag_gamma={8'd0,cnt_position,wire_channel_gamma[3:0]};
	integer lane, term, input_channel, kernel_y, kernel_x, address, output_lane;

	assign o_fault=flag_load_fault || flag_result_fault || i_pp_fault || (state_current==ST_FAULT);
	assign o_load_ready=i_rstn && flag_load_state_ready && !i_start && !i_export_start && !o_fault;
	assign flag_load_accept=i_load_valid && o_load_ready;
	assign flag_start_accept=i_rstn && state_current==ST_IDLE && i_start && !i_load_valid &&
	                         i_table_loaded && (&reg_loaded) && !o_fault;
	assign o_busy=i_rstn && state_current>=ST_PREPARE && state_current<=ST_ADVANCE;
	assign o_done=i_rstn && state_current==ST_DONE;
	assign o_core_cycles=cnt_core_cycles;
	assign o_mac_valid=i_rstn && state_current==ST_SEND && !o_fault;
	assign o_mac_first=cnt_group==2'd0;
	assign o_mac_last=cnt_group==2'd3;
	assign o_mac_mask=reg_mask;
	assign o_mac_activation=reg_activation;
	assign o_mac_weight=reg_mac_weight;
	assign o_mac_bias=reg_mac_bias;
	assign flag_mac_accept=o_mac_valid && i_mac_ready;
	assign o_pp_valid=i_rstn && state_current==ST_MAC_WAIT && i_mac_result_valid && !i_mac_fault && !o_fault;
	assign o_mac_result_ready=i_rstn && state_current==ST_MAC_WAIT && i_pp_ready && !i_mac_fault && !o_fault;
	assign flag_result_accept=i_mac_result_valid && o_mac_result_ready;
	assign o_pp_acc=i_mac_result;
	assign o_pp_multipliers={cnt_channel==4'd15 ? 32'd0 : reg_multiplier[wire_channel_gamma],
	                         cnt_channel==4'd15 ? 32'd0 : reg_multiplier[wire_channel_beta],reg_multiplier[cnt_channel]};
	assign o_pp_shifts={cnt_channel==4'd15 ? 6'd0 : reg_shift[wire_channel_gamma],
	                    cnt_channel==4'd15 ? 6'd0 : reg_shift[wire_channel_beta],reg_shift[cnt_channel]};
	assign o_pp_post_multiplier=reg_post_multiplier;
	assign o_pp_post_shift=reg_post_shift;
	assign o_pp_mask=cnt_channel==4'd15 ? 3'b001 : 3'b111;
	assign o_pp_tags={wire_tag_gamma,wire_tag_beta,wire_tag_alpha};
	assign o_pp_ready=o_busy && i_commit_ready && !o_fault;
	assign flag_write_accept=i_pp_valid && o_pp_ready;
	assign flag_write_illegal=cnt_written[8] || (i_pp_tag[15:8]!=8'd0) ||
	                          (i_pp_tag[7:0]!=cnt_written[7:0]) ||
	                          i_pp_int16 || (i_pp_data[15:8]!={8{i_pp_data[7]}});
	assign o_output_valid=i_rstn && state_current==ST_EXPORT && flag_tile_valid && !o_fault;
	assign o_output_data=reg_output[cnt_export];
	assign o_output_index=cnt_export;
	assign o_export_done=i_rstn && flag_export_done;

	// loader 仅支持当前 Stem 的七类记录；非法记录停止，不发布半个 tile。
	always @(*)begin
		flag_load_legal=1'b0;
		case(i_load_kind)
			3'd0,3'd1:flag_load_legal=(i_load_addr<9'd243) &&
				(i_load_addr==cnt_halo_address || i_load_addr==9'd0) &&
				(i_load_kind==3'd1 ? i_load_data==32'sd0 : i_load_data>=32'sd0 && i_load_data<=32'sd255);
			3'd2:flag_load_legal=(i_load_addr<9'd432) && (i_load_addr==cnt_weight_address || i_load_addr==9'd0) &&
				i_load_data>=-32'sd128 && i_load_data<=32'sd127;
			3'd3:flag_load_legal=(i_load_addr<9'd16) && (i_load_addr==cnt_bias_address || i_load_addr==9'd0);
			3'd4:flag_load_legal=(i_load_addr<9'd16) && (i_load_addr==cnt_multiplier_address || i_load_addr==9'd0) && !i_load_data[31];
			3'd5:flag_load_legal=(i_load_addr<9'd16) && (i_load_addr==cnt_shift_address || i_load_addr==9'd0) &&
				i_load_data>=32'sd0 && i_load_data<=32'sd62;
			3'd6:flag_load_legal=(i_load_addr<9'd2) && (i_load_addr=={8'd0,flag_post_address} || i_load_addr==9'd0) &&
				(i_load_addr==9'd0 ? !i_load_data[31] : i_load_data>=32'sd0 && i_load_data<=32'sd62);
			default:flag_load_legal=1'b0;
		endcase
	end

	// 每路基址是输出通道乘27；只译码现有六组，最大405，尾路不读权重。
	always @(*)begin
		next_weight_base[0]=9'd0; next_weight_base[1]=9'd0; next_weight_base[2]=9'd0;
		case(cnt_channel)
			4'd0:begin next_weight_base[0]=9'd0; next_weight_base[1]=9'd27; next_weight_base[2]=9'd54; end
			4'd3:begin next_weight_base[0]=9'd81; next_weight_base[1]=9'd108; next_weight_base[2]=9'd135; end
			4'd6:begin next_weight_base[0]=9'd162; next_weight_base[1]=9'd189; next_weight_base[2]=9'd216; end
			4'd9:begin next_weight_base[0]=9'd243; next_weight_base[1]=9'd270; next_weight_base[2]=9'd297; end
			4'd12:begin next_weight_base[0]=9'd324; next_weight_base[1]=9'd351; next_weight_base[2]=9'd378; end
			4'd15:next_weight_base[0]=9'd405;
			default:begin next_weight_base[0]=9'd0; next_weight_base[1]=9'd0; next_weight_base[2]=9'd0; end
		endcase
	end

	// 27 项按 OIHW 中 C、Y、X 顺序展平；每路最多四组，不改变算术归约契约。
	always @(*)begin
		next_activation=64'd0; next_weight=192'd0; next_bias=96'd0; next_mask=8'd0;
		term=0; input_channel=0; kernel_y=0; kernel_x=0; address=0;
		for(lane=0;lane<8;lane=lane+1)begin
			term=cnt_group*8+lane;
			if(term<27)begin
				input_channel=term/9; kernel_y=(term%9)/3; kernel_x=term%3;
				address=((cnt_position/4*2+kernel_y)*9+cnt_position%4*2+kernel_x)*3+input_channel;
				next_activation[lane*8+:8]=reg_halo[address];
				next_mask[lane]=1'b1;
				for(output_lane=0;output_lane<3;output_lane=output_lane+1)begin
					if(cnt_channel+output_lane<16) next_weight[(output_lane*8+lane)*8+:8]=reg_weight[next_weight_base[output_lane]+{4'd0,term[4:0]}];
				end
			end
		end
		for(output_lane=0;output_lane<3;output_lane=output_lane+1)begin
			if(cnt_channel+output_lane<16) next_bias[output_lane*32+:32]=reg_bias[cnt_channel+output_lane];
		end
	end

	// 状态寄存器独立于转移及数据路径。
	// 同沿登记下一状态资格；不登记旧state，也不延迟外部start/export/fault条件。
	always @(posedge i_clk or negedge i_rstn)begin
		if(!i_rstn) flag_load_state_ready<=1'b1;
		else flag_load_state_ready<=(state_next==ST_IDLE);
	end

	always @(posedge i_clk or negedge i_rstn)begin
		if(!i_rstn) state_current<=ST_IDLE;
		else state_current<=state_next;
	end

	// 现有PP队列接受任务后即可推进；MAC归约仍逐任务串行，末任务等完整提交。
	always @(*)begin
		state_next=state_current;
		case(state_current)
			ST_IDLE:begin
				if(flag_start_accept) state_next=ST_PREPARE;
				else if(i_export_start && flag_tile_valid) state_next=ST_EXPORT;
			end
			ST_PREPARE:state_next=ST_SEND;
			ST_SEND:if(flag_mac_accept) state_next=o_mac_last ? ST_MAC_WAIT : ST_PREPARE;
			ST_MAC_WAIT:if(flag_result_accept) state_next=ST_ADVANCE;
			ST_POST_WAIT:if(cnt_written==9'd256) state_next=ST_DONE;
			ST_ADVANCE:state_next=(cnt_channel==4'd15 && cnt_position==4'd15) ? ST_POST_WAIT : ST_PREPARE;
			ST_DONE:state_next=ST_IDLE;
			ST_EXPORT:if(o_output_valid && i_output_ready && cnt_export==8'd255) state_next=ST_IDLE;
			ST_FAULT:state_next=ST_FAULT;
			default:state_next=ST_FAULT;
		endcase
		if(o_fault || (state_current==ST_MAC_WAIT && i_mac_result_valid && i_mac_fault) ||
		   (flag_write_accept && flag_write_illegal)) state_next=ST_FAULT;
	end

	// 缓存不靠复位清零；有效标志、游标及发布状态在复位时全部作废。
	always @(posedge i_clk or negedge i_rstn)begin
		if(!i_rstn)begin
			reg_loaded<=6'd0; cnt_halo_address<=8'd0; cnt_weight_address<=9'd0;
			cnt_bias_address<=4'd0; cnt_multiplier_address<=4'd0; cnt_shift_address<=4'd0; flag_post_address<=1'b0;
			flag_load_fault<=1'b0; flag_result_fault<=1'b0; flag_tile_valid<=1'b0; flag_export_done<=1'b0;
			cnt_position<=4'd0; cnt_channel<=4'd0; cnt_group<=2'd0;
			cnt_export<=8'd0; cnt_written<=9'd0; cnt_core_cycles<=32'd0;
			reg_activation<=64'd0; reg_mac_weight<=192'd0; reg_mac_bias<=96'd0; reg_mask<=8'd0;
			reg_post_multiplier<=32'd0; reg_post_shift<=6'd0;
		end else begin
			flag_export_done<=1'b0;
			if(flag_load_accept)begin
				flag_tile_valid<=1'b0;
				if(!flag_load_legal) flag_load_fault<=1'b1;
				else case(i_load_kind)
					3'd0,3'd1:begin
						reg_halo[i_load_addr]<=i_load_kind==3'd1 ? 8'd0 : i_load_data[7:0]^8'h80;
						reg_loaded[0]<=i_load_addr==9'd242; cnt_halo_address<=i_load_addr==9'd242 ? 8'd0 : i_load_addr[7:0]+8'd1;
					end
					3'd2:begin reg_loaded[1]<=i_load_addr==9'd431;
						cnt_weight_address<=i_load_addr==9'd431 ? 9'd0 : i_load_addr+9'd1; end
					3'd3:begin reg_bias[i_load_addr]<=i_load_data; reg_loaded[2]<=i_load_addr==9'd15;
						cnt_bias_address<=i_load_addr==9'd15 ? 4'd0 : i_load_addr[3:0]+4'd1; end
					3'd4:begin reg_multiplier[i_load_addr]<=i_load_data; reg_loaded[3]<=i_load_addr==9'd15;
						cnt_multiplier_address<=i_load_addr==9'd15 ? 4'd0 : i_load_addr[3:0]+4'd1; end
					3'd5:begin reg_shift[i_load_addr]<=i_load_data[5:0]; reg_loaded[4]<=i_load_addr==9'd15;
						cnt_shift_address<=i_load_addr==9'd15 ? 4'd0 : i_load_addr[3:0]+4'd1; end
					3'd6:begin
						if(i_load_addr==9'd0) reg_post_multiplier<=i_load_data;
						else reg_post_shift<=i_load_data[5:0];
						reg_loaded[5]<=i_load_addr==9'd1; flag_post_address<=i_load_addr==9'd0;
					end
					default:flag_load_fault<=1'b1;
				endcase
			end
			if(flag_start_accept)begin
				cnt_position<=4'd0; cnt_channel<=4'd0; cnt_group<=2'd0;
				cnt_written<=9'd0; cnt_core_cycles<=32'd0; flag_tile_valid<=1'b0;
			end else if(o_busy) cnt_core_cycles<=cnt_core_cycles+32'd1;
			if(state_current==ST_PREPARE)begin
				reg_activation<=next_activation; reg_mac_weight<=next_weight; reg_mac_bias<=next_bias; reg_mask<=next_mask;
			end
			if(flag_mac_accept && !o_mac_last) cnt_group<=cnt_group+2'd1;
			if(flag_write_accept)begin
				if(flag_write_illegal) flag_result_fault<=1'b1;
				else begin
					reg_output[i_pp_tag[7:0]]<=i_pp_data[7:0];
					cnt_written<=cnt_written+9'd1;
				end
			end
			if(state_current==ST_MAC_WAIT && i_mac_result_valid && i_mac_fault) flag_result_fault<=1'b1;
			if(state_current==ST_ADVANCE)begin
				cnt_group<=2'd0;
				if(cnt_channel==4'd15)begin cnt_channel<=4'd0; cnt_position<=cnt_position+4'd1; end
				else cnt_channel<=cnt_channel+4'd3;
			end
			if(state_current==ST_POST_WAIT && cnt_written==9'd256) flag_tile_valid<=1'b1;
			if(state_current==ST_IDLE && i_export_start && flag_tile_valid) cnt_export<=8'd0;
			if(o_output_valid && i_output_ready)begin
				if(cnt_export==8'd255) flag_export_done<=1'b1;
				else cnt_export<=cnt_export+8'd1;
			end
			if(o_fault) flag_tile_valid<=1'b0;
		end
	end

	// 接收游标在原接受沿推进；此项与上一项提交重叠，不参与ready回压。
	always @(posedge i_clk or negedge i_rstn)begin
		if(!i_rstn)begin
			flag_weight_write_pending<=1'b0;
			reg_weight_write_address<=9'd0;
			reg_weight_write_data<=8'sd0;
		end else begin
			flag_weight_write_pending<=flag_load_accept && flag_load_legal && (i_load_kind==3'd2);
			if(flag_load_accept && flag_load_legal && (i_load_kind==3'd2))begin
				reg_weight_write_address<=i_load_addr;
				reg_weight_write_data<=i_load_data[7:0];
			end
		end
	end

	// 单一写入者；最后提交可与start同沿，实际读取发生在随后的PREPARE沿。
	always @(posedge i_clk or negedge i_rstn)begin
		if(!i_rstn)begin
		end else if(flag_weight_write_pending)begin
			reg_weight[reg_weight_write_address]<=reg_weight_write_data;
		end
	end
endmodule
