`timescale 1ns / 1ps
// Candidate grouping / 容量128；确定性等价类合并，至少6个支持窗口。
// 启动检测采用两两候选比较；候选容量固定，溢出时丢弃本帧结果。
module face_candidate_merge(
    input i_clk,
    input i_rstn,
    input i_clear,
    input i_add,
    input [8:0] i_x,
    input [8:0] i_y,
    input [8:0] i_width,
    input [8:0] i_height,
    input i_start,
    output o_done,
    output o_positive,
    output o_overflow,
    output [7:0] o_raw_count,
    output o_box_valid,
    output [8:0] o_x,
    output [8:0] o_y,
    output [8:0] o_width,
    output [8:0] o_height,
    output [7:0] o_support
);
    localparam ST_IDLE=0,ST_INITIALIZE=1,ST_PAIR_LOAD=2,ST_PAIR_DELTA=3,ST_PAIR_TEST=4,
        ST_ROOT_FIRST=5,ST_ROOT_SECOND=6,ST_UNION=7,ST_PAIR_NEXT=8,
        ST_AGG_ROOT=9,ST_AGG_READ=10,ST_AGG_LOAD=11,ST_AGG_WRITE=12,ST_AGG_NEXT=13,
        ST_MEAN_READ=14,ST_MEAN_LOAD=15,ST_DIVIDE_START=16,ST_DIVIDE_WAIT=17,
        ST_MEAN_STORE=18,ST_MEAN_NEXT=19,ST_NEST_READ=20,ST_NEST_LOAD=21,
        ST_NEST_OTHER_READ=22,ST_NEST_OTHER_LOAD=23,ST_NEST_MARGIN=24,ST_NEST_TEST=25,
        ST_NEST_NEXT=26,ST_EMIT=27,ST_OUTPUT_NEXT=28,ST_DONE=29,ST_PAIR_DISTANCE=30;
    reg [4:0] state_current,state_next;
    reg [35:0] mem_boxes[0:127];
    reg [6:0] mem_parent[0:127];
    reg [7:0] cnt_boxes,cnt_first,cnt_second,cnt_initialize;
    reg [6:0] reg_root_first,reg_root_second;
    reg [35:0] reg_first,reg_second;
    reg [9:0] reg_delta;
    reg [10:0] reg_first_right,reg_first_bottom,reg_second_right,reg_second_bottom;
    reg [13:0] reg_distance_x,reg_distance_y,reg_distance_right,reg_distance_bottom;
    reg flag_overflow,flag_positive,flag_nested;
    reg [75:0] reg_aggregate;
    reg [1:0] cnt_field;
    reg [35:0] reg_mean;
    reg [7:0] reg_support;
    reg [8:0] reg_margin_x,reg_margin_y;
    reg [75:0] reg_nested_first,reg_nested_second;
    wire [75:0] wire_group;
    wire flag_group_read=state_current == ST_AGG_READ || state_current == ST_MEAN_READ ||
        state_current == ST_NEST_READ || state_current == ST_NEST_OTHER_READ;
    wire [6:0] wire_group_address=state_current == ST_AGG_READ ? reg_root_first :
        (state_current == ST_NEST_OTHER_READ ? cnt_second[6:0] : cnt_first[6:0]);
    wire flag_group_write=state_current == ST_INITIALIZE || state_current == ST_AGG_WRITE || state_current == ST_MEAN_STORE;
    wire [6:0] wire_group_write_address=state_current == ST_INITIALIZE ? cnt_initialize[6:0] :
        (state_current == ST_AGG_WRITE ? reg_root_first : cnt_first[6:0]);
    wire [16:0] wire_sum_x=reg_aggregate[16:0]+reg_first[8:0];
    wire [16:0] wire_sum_y=reg_aggregate[33:17]+reg_first[17:9];
    wire [16:0] wire_sum_width=reg_aggregate[50:34]+reg_first[26:18];
    wire [16:0] wire_sum_height=reg_aggregate[67:51]+reg_first[35:27];
    wire [7:0] wire_support=reg_aggregate[75:68]+1'b1;
    wire [75:0] wire_aggregate={wire_support,wire_sum_height,wire_sum_width,wire_sum_y,wire_sum_x};
    // 归一后的组记录复用同一同步RAM：低36位xywh，高8位support。
    wire [75:0] wire_group_write=state_current == ST_INITIALIZE ? 76'd0 :
        (state_current == ST_AGG_WRITE ? wire_aggregate : {reg_support,32'd0,reg_mean});
    wire [16:0] wire_mean_sum=reg_aggregate[cnt_field*17 +:17];
    wire [19:0] wire_numerator={3'd0,wire_mean_sum}+{13'd0,reg_support[7:1]};
    wire divide_done;
    wire [19:0] divide_quotient;
    wire [10:0] wire_difference_x=reg_first[8:0] >= reg_second[8:0] ? reg_first[8:0]-reg_second[8:0] : reg_second[8:0]-reg_first[8:0];
    wire [10:0] wire_difference_y=reg_first[17:9] >= reg_second[17:9] ? reg_first[17:9]-reg_second[17:9] : reg_second[17:9]-reg_first[17:9];
    wire [10:0] wire_difference_right=reg_first_right >= reg_second_right ? reg_first_right-reg_second_right : reg_second_right-reg_first_right;
    wire [10:0] wire_difference_bottom=reg_first_bottom >= reg_second_bottom ? reg_first_bottom-reg_second_bottom : reg_second_bottom-reg_first_bottom;
    wire flag_similar=reg_distance_x <= reg_delta && reg_distance_y <= reg_delta &&
        reg_distance_right <= reg_delta && reg_distance_bottom <= reg_delta;
    wire signed [11:0] wire_nested_left=$signed({3'd0,reg_nested_second[8:0]})-$signed({3'd0,reg_margin_x});
    wire signed [11:0] wire_nested_top=$signed({3'd0,reg_nested_second[17:9]})-$signed({3'd0,reg_margin_y});
    wire [11:0] wire_nested_right={3'd0,reg_nested_second[8:0]}+reg_nested_second[26:18]+reg_margin_x;
    wire [11:0] wire_nested_bottom={3'd0,reg_nested_second[17:9]}+reg_nested_second[35:27]+reg_margin_y;
    wire flag_same_box=reg_nested_first[35:0] == reg_nested_second[35:0];
    wire flag_inside=$signed({3'd0,reg_nested_first[8:0]}) >= wire_nested_left &&
        $signed({3'd0,reg_nested_first[17:9]}) >= wire_nested_top &&
        ({3'd0,reg_nested_first[8:0]}+reg_nested_first[26:18]) <= wire_nested_right &&
        ({3'd0,reg_nested_first[17:9]}+reg_nested_first[35:27]) <= wire_nested_bottom;
    assign o_done=state_current == ST_DONE;
    assign o_positive=flag_positive && !flag_overflow;
    assign o_overflow=flag_overflow;
    assign o_raw_count=cnt_boxes;
    assign o_box_valid=state_current == ST_EMIT && !flag_nested && !flag_overflow;
    assign o_x=reg_nested_first[8:0];assign o_y=reg_nested_first[17:9];
    assign o_width=reg_nested_first[26:18];assign o_height=reg_nested_first[35:27];
    assign o_support=reg_nested_first[75:68];
    ball_component_store #(.C_DEPTH(128),.C_ADDR_BITS(7),.C_DATA_BITS(76)) groups_Inst(
        .i_clk(i_clk),.i_read_enable(flag_group_read),.i_read_address(wire_group_address),
        .i_write_enable(flag_group_write && !i_clear),.i_write_address(wire_group_write_address),
        .i_write_data(wire_group_write),.o_read_data(wire_group));
    face_unsigned_divide divide_Inst(.i_clk(i_clk),.i_rstn(i_rstn),.i_clear(i_clear),
        .i_start(state_current == ST_DIVIDE_START),.i_numerator(wire_numerator),.i_denominator({1'b0,reg_support}),
        .o_done(divide_done),.o_quotient(divide_quotient));
    always @(posedge i_clk or negedge i_rstn)begin
        if(!i_rstn)state_current<=ST_IDLE;
        else if(i_clear)state_current<=ST_IDLE;
        else state_current<=state_next;
    end
    always @(*)begin
        state_next=state_current;
        case(state_current)
            ST_IDLE:if(i_start)state_next=flag_overflow || cnt_boxes == 0 ? ST_DONE : ST_INITIALIZE;
            ST_INITIALIZE:if(cnt_initialize == 127)state_next=cnt_boxes < 2 ? ST_AGG_ROOT : ST_PAIR_LOAD;
            ST_PAIR_LOAD:state_next=ST_PAIR_DELTA;
            ST_PAIR_DELTA:state_next=ST_PAIR_DISTANCE;
            ST_PAIR_DISTANCE:state_next=ST_PAIR_TEST;
            ST_PAIR_TEST:state_next=flag_similar ? ST_ROOT_FIRST : ST_PAIR_NEXT;
            ST_ROOT_FIRST:if(mem_parent[reg_root_first] == reg_root_first)state_next=ST_ROOT_SECOND;
            ST_ROOT_SECOND:if(mem_parent[reg_root_second] == reg_root_second)state_next=ST_UNION;
            ST_UNION:state_next=ST_PAIR_NEXT;
            ST_PAIR_NEXT:state_next=cnt_first+1'b1 == cnt_boxes && cnt_second+1'b1 == cnt_first ? ST_AGG_ROOT : ST_PAIR_LOAD;
            ST_AGG_ROOT:if(mem_parent[reg_root_first] == reg_root_first)state_next=ST_AGG_READ;
            ST_AGG_READ:state_next=ST_AGG_LOAD;
            ST_AGG_LOAD:state_next=ST_AGG_WRITE;
            ST_AGG_WRITE:state_next=ST_AGG_NEXT;
            ST_AGG_NEXT:state_next=cnt_first+1'b1 == cnt_boxes ? ST_MEAN_READ : ST_AGG_ROOT;
            ST_MEAN_READ:state_next=ST_MEAN_LOAD;
            ST_MEAN_LOAD:state_next=wire_group[75:68] == 0 ? ST_MEAN_NEXT : ST_DIVIDE_START;
            ST_DIVIDE_START:state_next=ST_DIVIDE_WAIT;
            ST_DIVIDE_WAIT:if(divide_done)state_next=cnt_field == 3 ? ST_MEAN_STORE : ST_DIVIDE_START;
            ST_MEAN_STORE:state_next=ST_MEAN_NEXT;
            ST_MEAN_NEXT:state_next=cnt_first+1'b1 == cnt_boxes ? ST_NEST_READ : ST_MEAN_READ;
            ST_NEST_READ:state_next=ST_NEST_LOAD;
            ST_NEST_LOAD:state_next=wire_group[75:68] > 5 ? ST_NEST_OTHER_READ : ST_OUTPUT_NEXT;
            ST_NEST_OTHER_READ:state_next=ST_NEST_OTHER_LOAD;
            ST_NEST_OTHER_LOAD:state_next=ST_NEST_MARGIN;
            ST_NEST_MARGIN:state_next=ST_NEST_TEST;
            ST_NEST_TEST:state_next=ST_NEST_NEXT;
            ST_NEST_NEXT:state_next=flag_nested || cnt_second+1'b1 == cnt_boxes ? ST_EMIT : ST_NEST_OTHER_READ;
            ST_EMIT:state_next=ST_OUTPUT_NEXT;
            ST_OUTPUT_NEXT:state_next=cnt_first+1'b1 == cnt_boxes ? ST_DONE : ST_NEST_READ;
            ST_DONE:state_next=ST_IDLE;
            default:state_next=ST_IDLE;
        endcase
    end
    always @(posedge i_clk or negedge i_rstn)begin
        if(!i_rstn)begin
            cnt_boxes<=0;cnt_first<=0;cnt_second<=0;cnt_initialize<=0;reg_root_first<=0;reg_root_second<=0;
            reg_first<=0;reg_second<=0;reg_delta<=0;reg_first_right<=0;reg_first_bottom<=0;reg_second_right<=0;reg_second_bottom<=0;
            reg_distance_x<=0;reg_distance_y<=0;reg_distance_right<=0;reg_distance_bottom<=0;
            flag_overflow<=0;flag_positive<=0;flag_nested<=0;reg_aggregate<=0;cnt_field<=0;reg_mean<=0;reg_support<=0;
            reg_margin_x<=0;reg_margin_y<=0;reg_nested_first<=0;reg_nested_second<=0;
        end else if(i_clear)begin cnt_boxes<=0;flag_overflow<=0;flag_positive<=0;end
        else begin
            if(state_current == ST_IDLE && i_add)begin
                if(cnt_boxes == 128)flag_overflow<=1;
                else begin mem_boxes[cnt_boxes[6:0]]<={i_height,i_width,i_y,i_x};cnt_boxes<=cnt_boxes+1'b1;end
            end
            case(state_current)
                ST_IDLE:if(i_start)begin cnt_initialize<=0;flag_positive<=0;end
                ST_INITIALIZE:begin
                    mem_parent[cnt_initialize[6:0]]<=cnt_initialize[6:0];cnt_initialize<=cnt_initialize+1'b1;
                    cnt_first<=cnt_boxes < 2 ? 0 : 1;cnt_second<=0;reg_root_first<=0;
                end
                ST_PAIR_LOAD:begin
                    reg_first<=mem_boxes[cnt_first[6:0]];reg_second<=mem_boxes[cnt_second[6:0]];
                    reg_root_first<=cnt_first[6:0];reg_root_second<=cnt_second[6:0];
                end
                ST_PAIR_DELTA:begin
                    reg_delta<=(reg_first[26:18] < reg_second[26:18] ? reg_first[26:18] : reg_second[26:18])+
                        {1'b0,(reg_first[35:27] < reg_second[35:27] ? reg_first[35:27] : reg_second[35:27])};
                    reg_first_right<={2'd0,reg_first[8:0]}+reg_first[26:18];
                    reg_first_bottom<={2'd0,reg_first[17:9]}+reg_first[35:27];
                    reg_second_right<={2'd0,reg_second[8:0]}+reg_second[26:18];
                    reg_second_bottom<={2'd0,reg_second[17:9]}+reg_second[35:27];
                end
                ST_ROOT_FIRST:reg_root_first<=mem_parent[reg_root_first];
                ST_PAIR_DISTANCE:begin
                    // 常数10显式拆为8+2，避免启动分组占用四个DSP。
                    reg_distance_x<={wire_difference_x,3'b0}+{2'b0,wire_difference_x,1'b0};
                    reg_distance_y<={wire_difference_y,3'b0}+{2'b0,wire_difference_y,1'b0};
                    reg_distance_right<={wire_difference_right,3'b0}+{2'b0,wire_difference_right,1'b0};
                    reg_distance_bottom<={wire_difference_bottom,3'b0}+{2'b0,wire_difference_bottom,1'b0};
                end
                ST_ROOT_SECOND:reg_root_second<=mem_parent[reg_root_second];
                ST_UNION:if(reg_root_first > reg_root_second)mem_parent[reg_root_first]<=reg_root_second;
                    else if(reg_root_second > reg_root_first)mem_parent[reg_root_second]<=reg_root_first;
                ST_PAIR_NEXT:begin
                    if(cnt_second+1'b1 == cnt_first)begin
                        cnt_second<=0;cnt_first<=cnt_first+1'b1;
                        if(cnt_first+1'b1 == cnt_boxes)begin cnt_first<=0;reg_root_first<=0;end
                    end else cnt_second<=cnt_second+1'b1;
                end
                ST_AGG_ROOT:begin reg_root_first<=mem_parent[reg_root_first];reg_first<=mem_boxes[cnt_first[6:0]];end
                ST_AGG_LOAD:reg_aggregate<=wire_group;
                ST_AGG_NEXT:begin
                    cnt_first<=cnt_first+1'b1;reg_root_first<=cnt_first+1'b1;
                    if(cnt_first+1'b1 == cnt_boxes)cnt_first<=0;
                end
                ST_MEAN_LOAD:begin reg_aggregate<=wire_group;reg_support<=wire_group[75:68];cnt_field<=0;reg_mean<=0;end
                ST_DIVIDE_WAIT:if(divide_done)begin reg_mean[cnt_field*9 +:9]<=divide_quotient[8:0];cnt_field<=cnt_field+1'b1;end
                ST_MEAN_NEXT:begin cnt_first<=cnt_first+1'b1;if(cnt_first+1'b1 == cnt_boxes)cnt_first<=0;end
                ST_NEST_LOAD:begin reg_nested_first<=wire_group;cnt_second<=0;flag_nested<=0;end
                ST_NEST_OTHER_LOAD:reg_nested_second<=wire_group;
                ST_NEST_MARGIN:begin
                    reg_margin_x<=({1'b0,reg_nested_second[26:18]}+10'd2)/5;
                    reg_margin_y<=({1'b0,reg_nested_second[35:27]}+10'd2)/5;
                end
                ST_NEST_TEST:if(!flag_same_box && reg_nested_second[75:68] > 5 &&
                    reg_nested_second[75:68] > reg_nested_first[75:68] && flag_inside)flag_nested<=1;
                ST_NEST_NEXT:cnt_second<=cnt_second+1'b1;
                ST_EMIT:if(!flag_nested && !flag_overflow)flag_positive<=1;
                ST_OUTPUT_NEXT:cnt_first<=cnt_first+1'b1;
                default:begin end
            endcase
        end
    end
endmodule
