`timescale 1ns / 1ps

// 固定48→48 PW小块；复用现有MAC与PP，不包含通用图控制或DDR。
module road_pw_tile_scheduler(
    input i_clk,
    input i_rstn,
    input i_table_loaded,
    input i_load_valid,
    input [2:0]i_load_kind,
    input [11:0]i_load_addr,
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
    output [9:0]o_output_index,
    output o_export_done
);
    localparam [3:0] ST_IDLE=4'd0, ST_PREPARE=4'd1, ST_SEND=4'd2, ST_MAC_WAIT=4'd3;
    localparam [3:0] ST_DRAIN=4'd4, ST_ADVANCE=4'd5, ST_DONE=4'd6, ST_EXPORT=4'd7, ST_FAULT=4'd8;
    reg [3:0]state_current, state_next;
    reg flag_load_state_ready;
    reg [5:0]reg_loaded;
    reg flag_load_fault, flag_result_fault, flag_tile_valid, flag_export_done;
    reg [9:0]cnt_input_address;
    reg [11:0]cnt_weight_address;
    reg [5:0]cnt_bias_address, cnt_multiplier_address, cnt_shift_address;
    reg flag_post_address;
    // OIHW顺序装载的三个有界游标，不在计算地址上引入除48或除3。
    reg [2:0]cnt_weight_input_group;
    reg [1:0]cnt_weight_output_lane;
    reg [6:0]cnt_weight_output_base;
    reg flag_load_pending;
    reg flag_pending_weight;
    reg [4:0]reg_pending_bank;
    reg [6:0]reg_pending_address;
    reg signed [7:0]reg_pending_data;
    // 两类装载游标独立；地址0可重启，计算时不需要除3或多读口复制。
    reg [1:0]cnt_bias_lane, cnt_multiplier_lane;
    reg [3:0]cnt_bias_row, cnt_multiplier_row;
    reg [5:0]reg_shift[0:47];
    reg [31:0]reg_post_multiplier;
    reg [5:0]reg_post_shift;
    reg signed [7:0]reg_output[0:767];
    reg [3:0]cnt_position, cnt_output_group;
    reg [2:0]cnt_group;
    reg [9:0]cnt_written, cnt_export;
    reg [31:0]cnt_core_cycles;
    reg [63:0]reg_activation;
    reg [191:0]reg_mac_weight;
    reg [95:0]reg_mac_bias, reg_task_multiplier;
    reg [17:0]reg_task_shift;
    reg flag_load_legal;
    wire flag_load_accept, flag_start_accept, flag_mac_accept, flag_result_accept, flag_write_accept;
    wire flag_write_illegal;
    wire flag_prefetch = state_current==ST_SEND && cnt_group!=3'd5;
    wire [2:0]wire_read_group = flag_prefetch ? cnt_group+3'd1 : cnt_group;
    wire [6:0]wire_input_address = ({3'd0,cnt_position}<<2)+({3'd0,cnt_position}<<1)+{4'd0,wire_read_group};
    wire [6:0]wire_weight_address = ({3'd0,cnt_output_group}<<2)+({3'd0,cnt_output_group}<<1)+{4'd0,wire_read_group};
    wire [5:0]wire_channel_alpha = ({2'd0,cnt_output_group}<<1)+{2'd0,cnt_output_group};
    wire [5:0]wire_channel_beta = wire_channel_alpha+6'd1;
    wire [5:0]wire_channel_gamma = wire_channel_alpha+6'd2;
    wire [9:0]wire_tag_alpha = ({6'd0,cnt_position}<<5)+({6'd0,cnt_position}<<4)+{4'd0,wire_channel_alpha};
    wire [15:0]wire_tag_beta = {6'd0,wire_tag_alpha}+16'd1;
    wire [15:0]wire_tag_gamma = {6'd0,wire_tag_alpha}+16'd2;
    wire [63:0]wire_activation;
    wire [191:0]wire_weight;
    wire [95:0]wire_bias, wire_multiplier;
    wire [1:0]wire_bias_lane = i_load_addr==12'd0 ? 2'd0 : cnt_bias_lane;
    wire [1:0]wire_multiplier_lane = i_load_addr==12'd0 ? 2'd0 : cnt_multiplier_lane;
    wire [3:0]wire_bias_row = i_load_addr==12'd0 ? 4'd0 : cnt_bias_row;
    wire [3:0]wire_multiplier_row = i_load_addr==12'd0 ? 4'd0 : cnt_multiplier_row;
    genvar input_lane, weight_lane, parameter_lane;

    // 每bank单写单读；数组不复位，完整装载标志防止读取未初始化数据。
    generate
        for(parameter_lane=0;parameter_lane<3;parameter_lane=parameter_lane+1)begin: param_banks
            reg signed [31:0]reg_bias[0:15];
            reg [31:0]reg_multiplier[0:15];
            assign wire_bias[parameter_lane*32+:32]=reg_bias[cnt_output_group];
            assign wire_multiplier[parameter_lane*32+:32]=reg_multiplier[cnt_output_group];
            always @(posedge i_clk)begin
                if(i_rstn && flag_load_accept && flag_load_legal && i_load_kind==3'd3 && wire_bias_lane==parameter_lane)
                    reg_bias[wire_bias_row]<=i_load_data;
                if(i_rstn && flag_load_accept && flag_load_legal && i_load_kind==3'd4 && wire_multiplier_lane==parameter_lane)
                    reg_multiplier[wire_multiplier_row]<=i_load_data;
            end
        end
        for(input_lane=0;input_lane<8;input_lane=input_lane+1)begin: input_banks
            reg signed [7:0]reg_cache[0:95];
            assign wire_activation[input_lane*8+:8]=reg_cache[wire_input_address];
            always @(posedge i_clk)begin
                if(i_rstn && flag_load_pending && !flag_pending_weight && reg_pending_bank==input_lane)
                    reg_cache[reg_pending_address]<=reg_pending_data;
            end
        end
        for(weight_lane=0;weight_lane<24;weight_lane=weight_lane+1)begin: weight_banks
            reg signed [7:0]reg_cache[0:95];
            assign wire_weight[weight_lane*8+:8]=reg_cache[wire_weight_address];
            always @(posedge i_clk)begin
                if(i_rstn && flag_load_pending && flag_pending_weight && reg_pending_bank==weight_lane)
                    reg_cache[reg_pending_address]<=reg_pending_data;
            end
        end
    endgenerate

    assign o_fault=flag_load_fault || flag_result_fault || i_pp_fault || state_current==ST_FAULT;
    assign o_load_ready=i_rstn && flag_load_state_ready && !flag_tile_valid && !i_start && !i_export_start && !o_fault;
    assign flag_load_accept=i_load_valid && o_load_ready;
    assign flag_start_accept=i_rstn && state_current==ST_IDLE && i_start && !i_load_valid && !flag_tile_valid &&
                             i_table_loaded && (&reg_loaded) && !o_fault;
    assign o_busy=i_rstn && state_current>=ST_PREPARE && state_current<=ST_ADVANCE;
    assign o_done=i_rstn && state_current==ST_DONE;
    assign o_core_cycles=cnt_core_cycles;
    assign o_mac_valid=i_rstn && state_current==ST_SEND && !o_fault;
    assign o_mac_first=cnt_group==3'd0;
    assign o_mac_last=cnt_group==3'd5;
    assign o_mac_mask=8'hff;
    assign o_mac_activation=reg_activation;
    assign o_mac_weight=reg_mac_weight;
    assign o_mac_bias=reg_mac_bias;
    assign flag_mac_accept=o_mac_valid && i_mac_ready;
    assign o_pp_valid=i_rstn && state_current==ST_MAC_WAIT && i_mac_result_valid && !i_mac_fault && !o_fault;
    assign o_mac_result_ready=i_rstn && state_current==ST_MAC_WAIT && i_pp_ready && !i_mac_fault && !o_fault;
    assign flag_result_accept=i_mac_result_valid && o_mac_result_ready;
    assign o_pp_acc=i_mac_result;
    assign o_pp_multipliers=reg_task_multiplier;
    assign o_pp_shifts=reg_task_shift;
    assign o_pp_post_multiplier=reg_post_multiplier;
    assign o_pp_post_shift=reg_post_shift;
    assign o_pp_mask=3'b111;
    assign o_pp_tags={wire_tag_gamma,wire_tag_beta,{6'd0,wire_tag_alpha}};
    assign o_pp_ready=o_busy && i_commit_ready && !o_fault;
    assign flag_write_accept=i_pp_valid && o_pp_ready;
    assign flag_write_illegal=cnt_written>=10'd768 || i_pp_tag[15:10]!=6'd0 ||
        i_pp_tag[9:0]!=cnt_written || i_pp_int16 || i_pp_data[15:8]!={8{i_pp_data[7]}};
    assign o_output_valid=i_rstn && state_current==ST_EXPORT && flag_tile_valid && !o_fault;
    assign o_output_data=reg_output[cnt_export];
    assign o_output_index=cnt_export;
    assign o_export_done=i_rstn && flag_export_done;

    // 新PW入口接收有符号激活，不重复做RGB中心化。
    always @(*)begin
        flag_load_legal=1'b0;
        case(i_load_kind)
            3'd0:flag_load_legal=i_load_addr<12'd768 &&
                (i_load_addr=={2'd0,cnt_input_address} || i_load_addr==12'd0) &&
                i_load_data>=-32'sd128 && i_load_data<=32'sd127;
            3'd2:flag_load_legal=i_load_addr<12'd2304 &&
                (i_load_addr==cnt_weight_address || i_load_addr==12'd0) &&
                i_load_data>=-32'sd128 && i_load_data<=32'sd127;
            3'd3:flag_load_legal=i_load_addr<12'd48 &&
                (i_load_addr=={6'd0,cnt_bias_address} || i_load_addr==12'd0);
            3'd4:flag_load_legal=i_load_addr<12'd48 &&
                (i_load_addr=={6'd0,cnt_multiplier_address} || i_load_addr==12'd0) && !i_load_data[31];
            3'd5:flag_load_legal=i_load_addr<12'd48 &&
                (i_load_addr=={6'd0,cnt_shift_address} || i_load_addr==12'd0) &&
                i_load_data>=32'sd0 && i_load_data<=32'sd62;
            3'd6:flag_load_legal=i_load_addr<12'd2 &&
                (i_load_addr=={11'd0,flag_post_address} || i_load_addr==12'd0) &&
                (i_load_addr==12'd0 ? !i_load_data[31] : i_load_data>=32'sd0 && i_load_data<=32'sd62);
            default:flag_load_legal=1'b0;
        endcase
    end

    always @(posedge i_clk or negedge i_rstn)begin
        if(!i_rstn)begin state_current<=ST_IDLE; flag_load_state_ready<=1'b1; end
        else begin state_current<=state_next; flag_load_state_ready<=state_next==ST_IDLE; end
    end

    always @(*)begin
        state_next=state_current;
        case(state_current)
            ST_IDLE:begin
                if(flag_start_accept)state_next=ST_PREPARE;
                else if(i_export_start && flag_tile_valid)state_next=ST_EXPORT;
            end
            ST_PREPARE:state_next=ST_SEND;
            ST_SEND:if(flag_mac_accept && o_mac_last)state_next=ST_MAC_WAIT;
            ST_MAC_WAIT:if(flag_result_accept)state_next=ST_ADVANCE;
            ST_ADVANCE:state_next=cnt_output_group==4'd15 && cnt_position==4'd15 ? ST_DRAIN : ST_PREPARE;
            ST_DRAIN:if(cnt_written==10'd768)state_next=ST_DONE;
            ST_DONE:state_next=ST_IDLE;
            ST_EXPORT:if(o_output_valid && i_output_ready && cnt_export==10'd767)state_next=ST_IDLE;
            ST_FAULT:state_next=ST_FAULT;
            default:state_next=ST_FAULT;
        endcase
        if(o_fault || (state_current==ST_MAC_WAIT && i_mac_result_valid && i_mac_fault) ||
           (flag_write_accept && flag_write_illegal))state_next=ST_FAULT;
    end

    // 一拍注册装载bank/地址/数据，最后提交可与start同沿；复位取消pending。
    always @(posedge i_clk or negedge i_rstn)begin
        if(!i_rstn)begin
            flag_load_pending<=1'b0; flag_pending_weight<=1'b0;
            reg_pending_bank<=5'd0; reg_pending_address<=7'd0; reg_pending_data<=8'sd0;
            cnt_weight_input_group<=3'd0; cnt_weight_output_lane<=2'd0; cnt_weight_output_base<=7'd0;
        end else begin
            flag_load_pending<=flag_load_accept && flag_load_legal && (i_load_kind==3'd0 || i_load_kind==3'd2);
            if(flag_load_accept && flag_load_legal && i_load_kind==3'd0)begin
                flag_pending_weight<=1'b0; reg_pending_bank<={2'd0,i_load_addr[2:0]};
                reg_pending_address<=i_load_addr[9:3]; reg_pending_data<=i_load_data[7:0];
            end
            if(flag_load_accept && flag_load_legal && i_load_kind==3'd2)begin
                flag_pending_weight<=1'b1; reg_pending_data<=i_load_data[7:0];
                if(i_load_addr==12'd0)begin
                    reg_pending_bank<=5'd0; reg_pending_address<=7'd0;
                    cnt_weight_input_group<=3'd0; cnt_weight_output_lane<=2'd0; cnt_weight_output_base<=7'd0;
                end else begin
                    reg_pending_bank<={cnt_weight_output_lane,i_load_addr[2:0]};
                    reg_pending_address<=cnt_weight_output_base+{4'd0,cnt_weight_input_group};
                    if(i_load_addr[2:0]==3'd7)begin
                        if(cnt_weight_input_group==3'd5)begin
                            cnt_weight_input_group<=3'd0;
                            if(cnt_weight_output_lane==2'd2)begin
                                cnt_weight_output_lane<=2'd0; cnt_weight_output_base<=cnt_weight_output_base+7'd6;
                            end else cnt_weight_output_lane<=cnt_weight_output_lane+2'd1;
                        end else cnt_weight_input_group<=cnt_weight_input_group+3'd1;
                    end
                end
            end
        end
    end

    always @(posedge i_clk or negedge i_rstn)begin
        if(!i_rstn)begin
            reg_loaded<=6'd0; flag_load_fault<=1'b0; flag_result_fault<=1'b0; flag_tile_valid<=1'b0;
            flag_export_done<=1'b0; cnt_input_address<=10'd0; cnt_weight_address<=12'd0;
            cnt_bias_address<=6'd0; cnt_multiplier_address<=6'd0; cnt_shift_address<=6'd0; flag_post_address<=1'b0;
            cnt_bias_lane<=2'd0; cnt_multiplier_lane<=2'd0; cnt_bias_row<=4'd0; cnt_multiplier_row<=4'd0;
            cnt_position<=4'd0; cnt_output_group<=4'd0; cnt_group<=3'd0; cnt_written<=10'd0; cnt_export<=10'd0;
            cnt_core_cycles<=32'd0; reg_activation<=64'd0; reg_mac_weight<=192'd0; reg_mac_bias<=96'd0;
            reg_task_multiplier<=96'd0; reg_task_shift<=18'd0; reg_post_multiplier<=32'd0; reg_post_shift<=6'd0;
        end else begin
            flag_export_done<=1'b0;
            if(flag_load_accept)begin
                if(!flag_load_legal)flag_load_fault<=1'b1;
                else case(i_load_kind)
                    3'd0:begin reg_loaded[0]<=i_load_addr==12'd767;
                        cnt_input_address<=i_load_addr==12'd767 ? 10'd0 : i_load_addr[9:0]+10'd1; end
                    3'd2:begin reg_loaded[1]<=i_load_addr==12'd2303;
                        cnt_weight_address<=i_load_addr==12'd2303 ? 12'd0 : i_load_addr+12'd1; end
                    3'd3:begin reg_loaded[2]<=i_load_addr==12'd47;
                        cnt_bias_address<=i_load_addr==12'd47 ? 6'd0 : i_load_addr[5:0]+6'd1;
                        if(i_load_addr==12'd0)begin cnt_bias_lane<=2'd1; cnt_bias_row<=4'd0; end
                        else if(cnt_bias_lane==2'd2)begin cnt_bias_lane<=2'd0; cnt_bias_row<=cnt_bias_row+4'd1; end
                        else cnt_bias_lane<=cnt_bias_lane+2'd1;
                    end
                    3'd4:begin reg_loaded[3]<=i_load_addr==12'd47;
                        cnt_multiplier_address<=i_load_addr==12'd47 ? 6'd0 : i_load_addr[5:0]+6'd1;
                        if(i_load_addr==12'd0)begin cnt_multiplier_lane<=2'd1; cnt_multiplier_row<=4'd0; end
                        else if(cnt_multiplier_lane==2'd2)begin cnt_multiplier_lane<=2'd0; cnt_multiplier_row<=cnt_multiplier_row+4'd1; end
                        else cnt_multiplier_lane<=cnt_multiplier_lane+2'd1;
                    end
                    3'd5:begin reg_shift[i_load_addr[5:0]]<=i_load_data[5:0]; reg_loaded[4]<=i_load_addr==12'd47;
                        cnt_shift_address<=i_load_addr==12'd47 ? 6'd0 : i_load_addr[5:0]+6'd1; end
                    3'd6:begin
                        if(i_load_addr==12'd0)reg_post_multiplier<=i_load_data; else reg_post_shift<=i_load_data[5:0];
                        reg_loaded[5]<=i_load_addr==12'd1; flag_post_address<=i_load_addr==12'd0;
                    end
                    default:flag_load_fault<=1'b1;
                endcase
            end
            if(flag_start_accept)begin
                cnt_position<=4'd0; cnt_output_group<=4'd0; cnt_group<=3'd0; cnt_written<=10'd0; cnt_core_cycles<=32'd0;
            end else if(o_busy)cnt_core_cycles<=cnt_core_cycles+32'd1;
            if(state_current==ST_PREPARE || (flag_mac_accept && !o_mac_last))begin
                reg_activation<=wire_activation; reg_mac_weight<=wire_weight;
            end
            if(state_current==ST_PREPARE)begin
                reg_mac_bias<=wire_bias;
                reg_task_multiplier<=wire_multiplier;
                reg_task_shift<={reg_shift[wire_channel_gamma],reg_shift[wire_channel_beta],reg_shift[wire_channel_alpha]};
            end
            if(flag_mac_accept && !o_mac_last)cnt_group<=cnt_group+3'd1;
            if(flag_write_accept)begin
                if(flag_write_illegal)flag_result_fault<=1'b1;
                else begin reg_output[i_pp_tag[9:0]]<=i_pp_data[7:0]; cnt_written<=cnt_written+10'd1; end
            end
            if(state_current==ST_MAC_WAIT && i_mac_result_valid && i_mac_fault)flag_result_fault<=1'b1;
            if(state_current==ST_ADVANCE)begin
                cnt_group<=3'd0;
                if(cnt_output_group==4'd15)begin cnt_output_group<=4'd0; cnt_position<=cnt_position+4'd1; end
                else cnt_output_group<=cnt_output_group+4'd1;
            end
            if(state_current==ST_DRAIN && cnt_written==10'd768)flag_tile_valid<=1'b1;
            if(state_current==ST_IDLE && i_export_start && flag_tile_valid)cnt_export<=10'd0;
            if(o_output_valid && i_output_ready)begin
                if(cnt_export==10'd767)begin flag_export_done<=1'b1; flag_tile_valid<=1'b0; end
                else cnt_export<=cnt_export+10'd1;
            end
            if(o_fault)flag_tile_valid<=1'b0;
        end
    end
endmodule
