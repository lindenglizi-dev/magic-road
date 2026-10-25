`timescale 1ns / 1ps

// 42位I/O；默认最大192输入分片，16位窄口命令与冻结基线相同。
module road_pw_validation_top #(
    parameter integer PROFILE=2
)(
    input i_clk,
    input i_rstn,
    input i_rx_valid,
    input [15:0]i_rx_data,
    output o_rx_ready,
    output o_tx_valid,
    output [15:0]o_tx_data,
    input i_tx_ready,
    output o_busy,
    output o_done,
    output o_fault,
    output o_parameters_ready
);
    localparam [11:0] INPUT_LAST=PROFILE==0 ? 12'd767 : PROFILE==1 ? 12'd1535 : 12'd3071;
    localparam [11:0] PARAMETER_LAST=PROFILE==0 ? 12'd47 : PROFILE==1 ? 12'd23 : 12'd11;
    localparam [9:0] OUTPUT_LAST=PROFILE==0 ? 10'd767 : PROFILE==1 ? 10'd383 : 10'd191;
    localparam [3:0] ST_IDLE=4'd0, ST_LOW=4'd1, ST_HIGH=4'd2, ST_LOAD=4'd3, ST_TABLE=4'd4;
    localparam [3:0] ST_EXPORT_WAIT=4'd5, ST_INDEX=4'd6, ST_DATA=4'd7, ST_COMPLETE=4'd8;
    localparam [3:0] ST_STATUS_LOW=4'd9, ST_STATUS_HIGH=4'd10, ST_ERROR=4'd11, ST_FAULT=4'd12;
    reg [3:0]state_current, state_next;
    reg reg_release_meta, reg_release_done;
    reg [2:0]reg_load_kind;
    reg [11:0]reg_load_address;
    reg [15:0]reg_load_low;
    reg signed [31:0]reg_load_data;
    reg [9:0]cnt_table_address;
    reg [5:0]reg_loaded;
    reg flag_start, flag_export_start, flag_commit_ready, flag_shell_fault, flag_unexported;
    reg [9:0]reg_output_index;
    reg signed [7:0]reg_output_data;
    reg [31:0]reg_status_cycles;
    wire domain_rstn=i_rstn && reg_release_done;
    wire s_load_ready, s_busy, s_done, s_fault, s_output_valid, s_export_done;
    wire signed [7:0]s_output_data;
    wire [9:0]s_output_index;
    wire [31:0]s_cycles;
    wire s_mac_valid, s_mac_ready, s_mac_first, s_mac_last, s_mac_result_valid, s_mac_result_ready, s_mac_fault;
    wire [7:0]s_mac_mask;
    wire [63:0]s_mac_activation;
    wire [191:0]s_mac_weight;
    wire [95:0]s_mac_bias, s_mac_result;
    wire s_pp_valid, s_pp_ready, s_pp_output_valid, s_pp_output_ready, pp_fault, pp_int16;
    wire [95:0]s_pp_acc, s_pp_multipliers;
    wire [17:0]s_pp_shifts;
    wire [31:0]s_pp_post_multiplier;
    wire [5:0]s_pp_post_shift;
    wire [2:0]s_pp_mask;
    wire [47:0]s_pp_tags;
    wire signed [15:0]pp_data;
    wire [15:0]pp_tag;
    wire pp_table_ready, pp_table_loaded;
    wire flag_rx_accept=i_rx_valid && o_rx_ready;
    wire flag_tx_accept=o_tx_valid && i_tx_ready;
    wire flag_load_accept=state_current==ST_LOAD && s_load_ready;
    wire flag_output_pending=flag_unexported || s_done;

    always @(posedge i_clk or negedge i_rstn)begin
        if(!i_rstn)begin reg_release_meta<=1'b0; reg_release_done<=1'b0; end
        else begin reg_release_meta<=1'b1; reg_release_done<=reg_release_meta; end
    end
    assign o_busy=domain_rstn && s_busy;
    assign o_done=domain_rstn && s_done;
    assign o_fault=domain_rstn && (flag_shell_fault || s_fault || pp_fault);
    assign o_parameters_ready=domain_rstn && (&reg_loaded) && pp_table_loaded && !o_fault;
    assign o_rx_ready=domain_rstn && !o_fault &&
        ((state_current==ST_IDLE && (i_rx_data[15] || s_load_ready) &&
          (i_rx_data!=16'h8000 || (!s_busy && !flag_output_pending))) ||
         state_current==ST_LOW || state_current==ST_HIGH ||
         (state_current==ST_TABLE && pp_table_ready));
    assign o_tx_valid=domain_rstn && (state_current==ST_INDEX || state_current==ST_DATA ||
        state_current==ST_COMPLETE || state_current==ST_STATUS_LOW || state_current==ST_STATUS_HIGH || state_current==ST_ERROR);
    assign o_tx_data=state_current==ST_INDEX ? (16'ha000 | {6'd0,reg_output_index}) :
        state_current==ST_DATA ? {{8{reg_output_data[7]}},reg_output_data} :
        state_current==ST_COMPLETE ? 16'hf000 :
        state_current==ST_STATUS_LOW ? reg_status_cycles[15:0] :
        state_current==ST_STATUS_HIGH ? reg_status_cycles[31:16] : 16'hf001;

    always @(posedge i_clk or negedge domain_rstn)begin
        if(!domain_rstn)state_current<=ST_IDLE;
        else state_current<=state_next;
    end
    always @(*)begin
        state_next=state_current;
        case(state_current)
            ST_IDLE:if(flag_rx_accept)begin
                if(!i_rx_data[15])state_next=ST_LOW;
                else case(i_rx_data)
                    16'h8000:state_next=ST_TABLE;
                    16'h8001,16'h8004,16'h8005:state_next=ST_IDLE;
                    16'h8002:state_next=flag_output_pending ? ST_EXPORT_WAIT : ST_IDLE;
                    16'h8003:state_next=ST_STATUS_LOW;
                    default:state_next=ST_ERROR;
                endcase
            end
            ST_LOW:if(flag_rx_accept)state_next=ST_HIGH;
            ST_HIGH:if(flag_rx_accept)state_next=ST_LOAD;
            ST_LOAD:if(flag_load_accept)state_next=ST_IDLE;
            ST_TABLE:if(flag_rx_accept && cnt_table_address==10'd1023)state_next=ST_IDLE;
            ST_EXPORT_WAIT:if(s_output_valid)state_next=ST_INDEX;
            ST_INDEX:if(flag_tx_accept)state_next=ST_DATA;
            ST_DATA:if(flag_tx_accept)state_next=reg_output_index==OUTPUT_LAST ? ST_COMPLETE : ST_EXPORT_WAIT;
            ST_COMPLETE:if(flag_tx_accept)state_next=ST_IDLE;
            ST_STATUS_LOW:if(flag_tx_accept)state_next=ST_STATUS_HIGH;
            ST_STATUS_HIGH:if(flag_tx_accept)state_next=ST_IDLE;
            ST_ERROR:if(flag_tx_accept)state_next=ST_FAULT;
            ST_FAULT:state_next=ST_FAULT;
            default:state_next=ST_ERROR;
        endcase
        if(o_fault && state_current!=ST_ERROR && state_current!=ST_FAULT)state_next=ST_ERROR;
    end
    always @(posedge i_clk or negedge domain_rstn)begin
        if(!domain_rstn)begin
            reg_load_kind<=3'd0; reg_load_address<=12'd0; reg_load_low<=16'd0; reg_load_data<=32'sd0;
            cnt_table_address<=10'd0; reg_loaded<=6'd0; flag_start<=1'b0; flag_export_start<=1'b0;
            flag_commit_ready<=1'b1; flag_shell_fault<=1'b0; flag_unexported<=1'b0;
            reg_output_index<=10'd0; reg_output_data<=8'sd0; reg_status_cycles<=32'd0;
        end else begin
            flag_start<=1'b0; flag_export_start<=1'b0;
            if(s_done)flag_unexported<=1'b1;
            if(s_export_done)flag_unexported<=1'b0;
            if(state_current==ST_IDLE && flag_rx_accept)begin
                if(!i_rx_data[15])begin reg_load_kind<=i_rx_data[14:12]; reg_load_address<=i_rx_data[11:0]; end
                else case(i_rx_data)
                    16'h8000:cnt_table_address<=10'd0;
                    16'h8001:flag_start<=1'b1;
                    16'h8002:flag_export_start<=flag_output_pending;
                    16'h8003:reg_status_cycles<=s_cycles;
                    16'h8004:flag_commit_ready<=1'b0;
                    16'h8005:flag_commit_ready<=1'b1;
                    default:flag_shell_fault<=1'b1;
                endcase
            end
            if(state_current==ST_LOW && flag_rx_accept)reg_load_low<=i_rx_data;
            if(state_current==ST_HIGH && flag_rx_accept)reg_load_data<={i_rx_data,reg_load_low};
            if(state_current==ST_TABLE && flag_rx_accept)cnt_table_address<=cnt_table_address+10'd1;
            if(flag_load_accept)begin
                case(reg_load_kind)
                    3'd0:reg_loaded[0]<=reg_load_address==INPUT_LAST;
                    3'd2:reg_loaded[1]<=reg_load_address==12'd2303;
                    3'd3:reg_loaded[2]<=reg_load_address==PARAMETER_LAST;
                    3'd4:reg_loaded[3]<=reg_load_address==PARAMETER_LAST;
                    3'd5:reg_loaded[4]<=reg_load_address==PARAMETER_LAST;
                    3'd6:reg_loaded[5]<=reg_load_address==12'd1;
                    default:flag_shell_fault<=1'b1;
                endcase
            end
            if(state_current==ST_EXPORT_WAIT && s_output_valid)begin
                reg_output_index<=s_output_index; reg_output_data<=s_output_data;
            end
        end
    end

    road_pw_tile_scheduler #(.PROFILE(PROFILE)) u_scheduler(
        .i_clk(i_clk),.i_rstn(domain_rstn),.i_table_loaded(pp_table_loaded),
        .i_load_valid(state_current==ST_LOAD),.i_load_kind(reg_load_kind),.i_load_addr(reg_load_address),
        .i_load_data(reg_load_data),.o_load_ready(s_load_ready),.i_start(flag_start),
        .o_busy(s_busy),.o_done(s_done),.o_fault(s_fault),.o_core_cycles(s_cycles),
        .o_mac_valid(s_mac_valid),.i_mac_ready(s_mac_ready),.o_mac_first(s_mac_first),.o_mac_last(s_mac_last),
        .o_mac_mask(s_mac_mask),.o_mac_activation(s_mac_activation),.o_mac_weight(s_mac_weight),.o_mac_bias(s_mac_bias),
        .i_mac_result_valid(s_mac_result_valid),.o_mac_result_ready(s_mac_result_ready),.i_mac_result(s_mac_result),.i_mac_fault(s_mac_fault),
        .o_pp_valid(s_pp_valid),.i_pp_ready(s_pp_ready),.o_pp_acc(s_pp_acc),.o_pp_multipliers(s_pp_multipliers),
        .o_pp_shifts(s_pp_shifts),.o_pp_post_multiplier(s_pp_post_multiplier),.o_pp_post_shift(s_pp_post_shift),
        .o_pp_mask(s_pp_mask),.o_pp_tags(s_pp_tags),.i_pp_valid(s_pp_output_valid),.o_pp_ready(s_pp_output_ready),
        .i_pp_data(pp_data),.i_pp_tag(pp_tag),.i_pp_int16(pp_int16),.i_pp_fault(pp_fault),
        .i_commit_ready(flag_commit_ready),.i_export_start(flag_export_start),
        .o_output_valid(s_output_valid),.i_output_ready(state_current==ST_DATA && i_tx_ready),
        .o_output_data(s_output_data),.o_output_index(s_output_index),.o_export_done(s_export_done)
    );
    road_mac_probe u_mac(
        .i_clk(i_clk),.i_rstn(domain_rstn),.i_input_valid(s_mac_valid),.o_input_ready(s_mac_ready),
        .i_first(s_mac_first),.i_last(s_mac_last),.i_lane_mask(s_mac_mask),.i_activation_data(s_mac_activation),
        .i_weight_data(s_mac_weight),.i_bias_data(s_mac_bias),.i_result_ready(s_mac_result_ready),
        .o_result_valid(s_mac_result_valid),.o_result_data(s_mac_result),.o_fault(s_mac_fault)
    );
    road_dynamic_postprocess u_pp(
        .i_clk(i_clk),.i_rstn(domain_rstn),.i_table_valid(state_current==ST_TABLE && i_rx_valid),
        .i_table_addr(cnt_table_address),.i_table_data(i_rx_data),.o_table_ready(pp_table_ready),.o_table_loaded(pp_table_loaded),
        .i_input_valid(s_pp_valid),.o_input_ready(s_pp_ready),.i_accumulators(s_pp_acc),
        .i_pre_multipliers(s_pp_multipliers),.i_pre_shifts(s_pp_shifts),.i_post_multiplier(s_pp_post_multiplier),
        .i_post_shift(s_pp_post_shift),.i_activate(1'b1),.i_lane_mask(s_pp_mask),.i_tags(s_pp_tags),.i_input_fault(1'b0),
        .i_output_ready(s_pp_output_ready),.o_output_valid(s_pp_output_valid),.o_output_data(pp_data),
        .o_output_tag(pp_tag),.o_output_int16(pp_int16),.o_fault(pp_fault),
        .o_queue_count(),.o_pending_count(),.o_meta_count(),.o_pre_busy(),.o_silu_busy(),.o_post_busy(),
        .o_pre_accept(),.o_silu_accept(),.o_post_accept()
    );
endmodule
