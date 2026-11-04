`timescale 1ns / 1ps
// Serial Haar evaluator / 单窗口全级联求值；等于节点阈值取右叶，等于级阈值通过。
module face_haar_core #(
    parameter C_STUMPS="../rtl/face_rom/stumps.mem",C_STAGES="../rtl/face_rom/stages.mem"
)(
    input i_clk,
    input i_rstn,
    input i_clear,
    input i_start,
    input [5:0] i_x,
    input [5:0] i_y,
    input [16:0] i_root,
    output o_read,
    output [11:0] o_address,
    input [19:0] i_data,
    output o_done,
    output o_positive,
    output o_fault,
    output o_trace,
    output [11:0] o_weak_index,
    output signed [21:0] o_feature,
    output o_take_right,
    output signed [25:0] o_score,
    output [4:0] o_reject_stage
);
    localparam ST_IDLE=0,ST_ROM=1,ST_DECODE=2,ST_RECT_COORD=3,ST_RECT_START=4,
        ST_RECT_WAIT=5,ST_RECT_ACCUMULATE=6,ST_COMPARE=7,ST_LEAF=8,ST_TRACE=9,
        ST_STAGE=10,ST_NEXT=11,ST_DONE=12;
    reg [3:0] state_current,state_next;
    reg [5:0] reg_x,reg_y;
    reg [16:0] reg_root;
    reg [11:0] cnt_weak;
    reg [4:0] cnt_stage;
    reg [7:0] cnt_stage_weak,reg_stage_count;
    reg [1:0] cnt_rectangle,reg_mode;
    reg [59:0] reg_rectangles;
    reg signed [15:0] reg_node;
    reg signed [17:0] reg_left_leaf,reg_right_leaf,reg_stage_threshold;
    reg signed [21:0] reg_feature;
    reg signed [25:0] reg_score;
    reg signed [35:0] reg_feature_scaled,reg_node_scaled;
    reg flag_positive,flag_fault,flag_right;
    reg [6:0] reg_left,reg_top,reg_right,reg_bottom;
    wire [119:0] wire_weak;
    wire [39:0] wire_stage;
    wire [19:0] wire_rectangle=reg_rectangles[cnt_rectangle*20 +:20];
    wire rectangle_done;
    wire [19:0] rectangle_sum;
    wire signed [21:0] wire_sum=$signed({2'b0,rectangle_sum});
    wire flag_last_rectangle=cnt_rectangle == (reg_mode == 2 ? 2 : 1);
    assign o_done=state_current == ST_DONE;
    assign o_positive=flag_positive;
    assign o_fault=flag_fault;
    assign o_trace=state_current == ST_TRACE;
    assign o_weak_index=cnt_weak;
    assign o_feature=reg_feature;
    assign o_take_right=flag_right;
    assign o_score=reg_score;
    assign o_reject_stage=cnt_stage;
    face_model_rom #(.C_STUMPS(C_STUMPS),.C_STAGES(C_STAGES)) model_Inst(
        .i_clk(i_clk),.i_read(state_current == ST_ROM),.i_weak_address(cnt_weak),.i_stage_address(cnt_stage),
        .o_weak(wire_weak),.o_stage(wire_stage));
    face_rectangle_sum rectangle_Inst(
        .i_clk(i_clk),.i_rstn(i_rstn),.i_clear(i_clear),.i_start(state_current == ST_RECT_START),
        .i_left(reg_left),.i_top(reg_top),.i_right(reg_right),.i_bottom(reg_bottom),
        .o_read(o_read),.o_address(o_address),.i_data(i_data),.o_done(rectangle_done),.o_sum(rectangle_sum));
    always @(posedge i_clk or negedge i_rstn)begin
        if(!i_rstn)state_current<=ST_IDLE;
        else if(i_clear)state_current<=ST_IDLE;
        else state_current<=state_next;
    end
    always @(*)begin
        state_next=state_current;
        case(state_current)
            ST_IDLE:if(i_start)state_next=ST_ROM;
            ST_ROM:state_next=ST_DECODE;
            ST_DECODE:state_next=wire_weak[119:114] != 0 || wire_weak[61:60] == 3 || wire_stage[7:0] == 0 ? ST_DONE : ST_RECT_COORD;
            ST_RECT_COORD:state_next=ST_RECT_START;
            ST_RECT_START:state_next=ST_RECT_WAIT;
            ST_RECT_WAIT:if(rectangle_done)state_next=ST_RECT_ACCUMULATE;
            ST_RECT_ACCUMULATE:state_next=flag_last_rectangle ? ST_COMPARE : ST_RECT_COORD;
            ST_COMPARE:state_next=ST_LEAF;
            ST_LEAF:state_next=ST_TRACE;
            ST_TRACE:state_next=cnt_stage_weak+1'b1 == reg_stage_count ? ST_STAGE : ST_NEXT;
            ST_STAGE:state_next=reg_score < reg_stage_threshold || cnt_stage == 24 ? ST_DONE : ST_NEXT;
            ST_NEXT:state_next=ST_ROM;
            ST_DONE:state_next=ST_IDLE;
            default:state_next=ST_IDLE;
        endcase
    end
    always @(posedge i_clk or negedge i_rstn)begin
        if(!i_rstn)begin
            reg_x<=0;reg_y<=0;reg_root<=0;cnt_weak<=0;cnt_stage<=0;cnt_stage_weak<=0;
            reg_stage_count<=0;cnt_rectangle<=0;reg_mode<=0;reg_rectangles<=0;reg_node<=0;
            reg_left_leaf<=0;reg_right_leaf<=0;reg_stage_threshold<=0;reg_feature<=0;reg_score<=0;
            reg_feature_scaled<=0;reg_node_scaled<=0;flag_positive<=0;flag_fault<=0;flag_right<=0;
            reg_left<=0;reg_top<=0;reg_right<=0;reg_bottom<=0;
        end else if(!i_clear)begin
            case(state_current)
                ST_IDLE:if(i_start)begin
                    reg_x<=i_x;reg_y<=i_y;reg_root<=i_root;cnt_weak<=0;cnt_stage<=0;
                    cnt_stage_weak<=0;reg_score<=0;flag_positive<=0;flag_fault<=0;
                end
                ST_DECODE:begin
                    reg_rectangles<=wire_weak[59:0];reg_mode<=wire_weak[61:60];reg_node<=wire_weak[77:62];
                    reg_left_leaf<=wire_weak[95:78];reg_right_leaf<=wire_weak[113:96];
                    reg_stage_count<=wire_stage[7:0];reg_stage_threshold<=wire_stage[25:8];
                    cnt_rectangle<=0;reg_feature<=0;
                    flag_fault<=wire_weak[119:114] != 0 || wire_weak[61:60] == 3 || wire_stage[7:0] == 0;
                end
                ST_RECT_COORD:begin
                    reg_left<={1'b0,reg_x}+wire_rectangle[4:0];
                    reg_top<={1'b0,reg_y}+wire_rectangle[9:5];
                    reg_right<={1'b0,reg_x}+wire_rectangle[4:0]+wire_rectangle[14:10];
                    reg_bottom<={1'b0,reg_y}+wire_rectangle[9:5]+wire_rectangle[19:15];
                end
                ST_RECT_ACCUMULATE:begin
                    if(cnt_rectangle == 0)reg_feature<=-wire_sum;
                    else if(reg_mode == 1)reg_feature<=reg_feature+(wire_sum <<< 1)+wire_sum;
                    else reg_feature<=reg_feature+(wire_sum <<< 1);
                    cnt_rectangle<=cnt_rectangle+1'b1;
                end
                ST_COMPARE:begin
                    reg_feature_scaled<=$signed({reg_feature,14'd0});
                    reg_node_scaled<=reg_node*$signed({1'b0,reg_root});
                end
                ST_LEAF:begin
                    flag_right<=!(reg_feature_scaled < reg_node_scaled);
                    reg_score<=reg_score+(reg_feature_scaled < reg_node_scaled ? reg_left_leaf : reg_right_leaf);
                end
                ST_STAGE:if(reg_score >= reg_stage_threshold && cnt_stage == 24)flag_positive<=1;
                ST_NEXT:begin
                    cnt_weak<=cnt_weak+1'b1;
                    if(cnt_stage_weak+1'b1 == reg_stage_count)begin
                        cnt_stage<=cnt_stage+1'b1;cnt_stage_weak<=0;reg_score<=0;
                    end else cnt_stage_weak<=cnt_stage_weak+1'b1;
                end
                default:begin end
            endcase
        end
    end
endmodule
