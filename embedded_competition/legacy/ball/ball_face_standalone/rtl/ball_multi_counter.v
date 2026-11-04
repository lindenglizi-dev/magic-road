`timescale 1ns / 1ps
// COUNT专用四轨迹：逐对关联、逐轨迹越线锁存，整帧提交计数。
module ball_multi_counter #(
    parameter C_MAX_MOVE=64,C_LINE=640,C_HYST=16,C_MAX_MISSES=8
)(
    input i_clk,input i_rstn,input i_clear,input i_clear_counts,input i_fault,
    input i_frame_start,input i_candidate_valid,input [1:0] i_color,
    input [11:0] i_x_min,input [11:0] i_x_max,input [11:0] i_y_min,input [11:0] i_y_max,
    input i_frame_done,input i_overflow,
    output o_done,output o_busy,output [31:0] o_red,output [31:0] o_green,output [31:0] o_yellow,
    output [33:0] o_total,output [2:0] o_state,output [2:0] o_reason,
    output [11:0] o_center_x,output [11:0] o_center_y,output [2:0] o_active_count,
    output [3:0] o_box_valid,output [7:0] o_box_color,
    output [47:0] o_box_left,output [47:0] o_box_right,output [47:0] o_box_top,output [47:0] o_box_bottom
);
    localparam ST_IDLE=0,ST_COLLECT=1,ST_SEARCH_INIT=2,ST_SEARCH=3,ST_BIND=4,
        ST_MISS=5,ST_CAPACITY=6,ST_ALLOCATE=7,ST_UPDATE=8,ST_SUM=9,
        ST_COMMIT=10,ST_REJECT=11,ST_CAPACITY_FAIL=12;
    reg [3:0] state_current,state_next;
    reg [3:0] cnt_candidates;
    reg flag_bad;
    reg [2:0] reg_frame_reason;
    reg [1:0] cand_color[0:7];
    reg [11:0] cand_x[0:7],cand_y[0:7],cand_left[0:7],cand_right[0:7],cand_top[0:7],cand_bottom[0:7];
    reg [12:0] cand_width[0:7],cand_height[0:7];
    reg [3:0] live_active,work_active,work_used,work_new,live_armed,work_armed,live_counted,work_counted,live_blocked,work_blocked;
    reg [7:0] cand_used;
    reg [1:0] live_color[0:3],work_color[0:3],live_up[0:3],work_up[0:3];
    reg [3:0] live_misses[0:3],work_misses[0:3],work_match[0:3];
    reg [11:0] live_x[0:3],live_y[0:3],work_x[0:3],work_y[0:3];
    reg [11:0] live_left[0:3],live_right[0:3],live_top[0:3],live_bottom[0:3];
    reg [11:0] work_left[0:3],work_right[0:3],work_top[0:3],work_bottom[0:3];
    reg [12:0] live_width[0:3],live_height[0:3],work_width[0:3],work_height[0:3];
    reg signed [12:0] live_vx[0:3],live_vy[0:3],work_vx[0:3],work_vy[0:3];
    reg [1:0] cnt_track,cnt_slot,reg_best_track;
    reg [2:0] cnt_candidate,reg_best_candidate;
    reg [1:0] cnt_pairs;
    reg flag_best;
    reg [15:0] reg_best_distance;
    reg [2:0] cnt_delta_red,cnt_delta_green,cnt_delta_yellow;
    reg [32:0] reg_sum_red,reg_sum_green,reg_sum_yellow;
    reg [31:0] reg_red_o,reg_green_o,reg_yellow_o;
    reg reg_done_o;
    reg [2:0] reg_state_o,reg_reason_o;
    reg [11:0] reg_center_x_o,reg_center_y_o;
    wire [12:0] wire_input_x={1'b0,i_x_min}+{1'b0,i_x_max};
    wire [12:0] wire_input_y={1'b0,i_y_min}+{1'b0,i_y_max};
    wire signed [14:0] wire_predict_x=$signed({3'd0,work_x[cnt_track]})+$signed({{2{work_vx[cnt_track][12]}},work_vx[cnt_track]});
    wire signed [14:0] wire_predict_y=$signed({3'd0,work_y[cnt_track]})+$signed({{2{work_vy[cnt_track][12]}},work_vy[cnt_track]});
    wire signed [14:0] wire_residual_x=$signed({3'd0,cand_x[cnt_candidate]})-wire_predict_x;
    wire signed [14:0] wire_residual_y=$signed({3'd0,cand_y[cnt_candidate]})-wire_predict_y;
    wire [14:0] wire_dx=wire_residual_x<0 ? -wire_residual_x : wire_residual_x;
    wire [14:0] wire_dy=wire_residual_y<0 ? -wire_residual_y : wire_residual_y;
    wire [15:0] wire_distance={1'b0,wire_dx}+{1'b0,wire_dy};
    wire [14:0] wire_limit=work_misses[cnt_track]!=0 ? C_MAX_MOVE*2 : C_MAX_MOVE;
    wire flag_size=cand_width[cnt_candidate]<=({1'b0,work_width[cnt_track]}<<1) &&
        work_width[cnt_track]<=({1'b0,cand_width[cnt_candidate]}<<1) &&
        cand_height[cnt_candidate]<=({1'b0,work_height[cnt_track]}<<1) &&
        work_height[cnt_track]<=({1'b0,cand_height[cnt_candidate]}<<1);
    wire flag_pair=cnt_candidate<cnt_candidates && work_active[cnt_track] && !work_used[cnt_track] &&
        !cand_used[cnt_candidate] && cand_color[cnt_candidate]==work_color[cnt_track] && flag_size && wire_dx<=wire_limit && wire_dy<=wire_limit;
    wire flag_last_pair=cnt_track==3 && cnt_candidate==7;
    wire [2:0] wire_free_count=(!work_active[0])+(!work_active[1])+(!work_active[2])+(!work_active[3]);
    wire [3:0] wire_used_count=cand_used[0]+cand_used[1]+cand_used[2]+cand_used[3]+cand_used[4]+cand_used[5]+cand_used[6]+cand_used[7];
    wire flag_capacity=wire_free_count>=cnt_candidates-wire_used_count;
    reg flag_free;
    reg [1:0] dec_free_slot;
    integer free_index,slot,entry;
    always @(*)begin
        flag_free=0;dec_free_slot=0;
        for(free_index=0;free_index<4;free_index=free_index+1)begin
            if(!work_active[free_index] && !flag_free)begin flag_free=1;dec_free_slot=free_index;end
        end
    end
    wire [2:0] wire_match=work_match[cnt_slot][2:0];
    wire signed [12:0] wire_step_x=$signed({1'b0,cand_x[wire_match]})-$signed({1'b0,work_x[cnt_slot]});
    wire signed [12:0] wire_step_y=$signed({1'b0,cand_y[wire_match]})-$signed({1'b0,work_y[cnt_slot]});
    localparam signed [12:0] C_VELOCITY_LIMIT=C_MAX_MOVE*2;
    wire signed [12:0] wire_vx=wire_step_x>C_VELOCITY_LIMIT ? C_VELOCITY_LIMIT : wire_step_x < -C_VELOCITY_LIMIT ? -C_VELOCITY_LIMIT : wire_step_x;
    wire signed [12:0] wire_vy=wire_step_y>C_VELOCITY_LIMIT ? C_VELOCITY_LIMIT : wire_step_y < -C_VELOCITY_LIMIT ? -C_VELOCITY_LIMIT : wire_step_y;
    wire [1:0] wire_first=work_active[0] ? 0 : work_active[1] ? 1 : work_active[2] ? 2 : 3;

    always @(posedge i_clk or negedge i_rstn)begin
        if(!i_rstn)begin state_current<=ST_IDLE;end
        else if(i_clear)begin state_current<=ST_IDLE;end
        else if(i_frame_start)begin state_current<=ST_COLLECT;end
        else begin state_current<=state_next;end
    end
    always @(*)begin
        state_next=state_current;
        if(i_fault)begin state_next=ST_REJECT;end
        else case(state_current)
            ST_IDLE:begin end
            ST_COLLECT:if(i_frame_done)begin state_next=(flag_bad || i_overflow || cnt_candidates>4) ? ST_REJECT : ST_SEARCH_INIT;end
            ST_SEARCH_INIT:state_next=ST_SEARCH;
            ST_SEARCH:if(flag_last_pair)begin state_next=flag_best ? ST_BIND : ST_MISS;end
            ST_BIND:state_next=cnt_pairs==3 ? ST_MISS : ST_SEARCH_INIT;
            ST_MISS:if(cnt_slot==3)begin state_next=ST_CAPACITY;end
            ST_CAPACITY:state_next=flag_capacity ? ST_ALLOCATE : ST_CAPACITY_FAIL;
            ST_ALLOCATE:if(cnt_candidate>=cnt_candidates)begin state_next=ST_UPDATE;end
            ST_UPDATE:if(cnt_slot==3)begin state_next=ST_SUM;end
            ST_SUM:state_next=ST_COMMIT;
            ST_COMMIT,ST_REJECT,ST_CAPACITY_FAIL:state_next=ST_IDLE;
            default:state_next=ST_IDLE;
        endcase
    end
    // live仅在整帧提交时更新；故障不会留下半帧计数或被消耗的计数锁。
    always @(posedge i_clk or negedge i_rstn)begin
        if(!i_rstn)begin
            live_active<=0;work_active<=0;live_armed<=0;work_armed<=0;live_counted<=0;work_counted<=0;
            live_blocked<=0;work_blocked<=0;work_used<=0;work_new<=0;cand_used<=0;
            cnt_candidates<=0;flag_bad<=0;reg_frame_reason<=0;cnt_track<=0;cnt_slot<=0;cnt_candidate<=0;
            cnt_pairs<=0;flag_best<=0;reg_best_distance<=0;reg_best_track<=0;reg_best_candidate<=0;
            cnt_delta_red<=0;cnt_delta_green<=0;cnt_delta_yellow<=0;reg_sum_red<=0;reg_sum_green<=0;reg_sum_yellow<=0;
            reg_red_o<=0;reg_green_o<=0;reg_yellow_o<=0;reg_done_o<=0;reg_state_o<=0;reg_reason_o<=0;
            reg_center_x_o<=0;reg_center_y_o<=0;
            for(slot=0;slot<4;slot=slot+1)begin
                live_color[slot]<=0;work_color[slot]<=0;live_up[slot]<=0;work_up[slot]<=0;
                live_misses[slot]<=0;work_misses[slot]<=0;work_match[slot]<=15;
                live_x[slot]<=0;live_y[slot]<=0;work_x[slot]<=0;work_y[slot]<=0;
                live_left[slot]<=0;live_right[slot]<=0;live_top[slot]<=0;live_bottom[slot]<=0;
                work_left[slot]<=0;work_right[slot]<=0;work_top[slot]<=0;work_bottom[slot]<=0;
                live_width[slot]<=0;live_height[slot]<=0;work_width[slot]<=0;work_height[slot]<=0;
                live_vx[slot]<=0;live_vy[slot]<=0;work_vx[slot]<=0;work_vy[slot]<=0;
            end
            for(entry=0;entry<8;entry=entry+1)begin
                cand_color[entry]<=0;cand_x[entry]<=0;cand_y[entry]<=0;cand_width[entry]<=0;cand_height[entry]<=0;
                cand_left[entry]<=0;cand_right[entry]<=0;cand_top[entry]<=0;cand_bottom[entry]<=0;
            end
        end else begin
            reg_done_o<=0;
            if(i_clear)begin
                live_active<=0;work_active<=0;live_armed<=0;work_armed<=0;live_counted<=0;work_counted<=0;
                live_blocked<=0;work_blocked<=0;reg_state_o<=0;reg_reason_o<=0;
                reg_center_x_o<=0;reg_center_y_o<=0;
                if(i_clear_counts)begin reg_red_o<=0;reg_green_o<=0;reg_yellow_o<=0;end
            end else if(i_frame_start)begin
                cnt_candidates<=0;flag_bad<=state_current!=ST_IDLE;reg_frame_reason<=state_current!=ST_IDLE ? 5 : 0;
                work_active<=live_active;work_armed<=live_armed;work_counted<=live_counted;work_blocked<=live_blocked;
                work_used<=0;work_new<=0;cand_used<=0;cnt_pairs<=0;
                cnt_delta_red<=0;cnt_delta_green<=0;cnt_delta_yellow<=0;
                for(slot=0;slot<4;slot=slot+1)begin
                    work_color[slot]<=live_color[slot];work_up[slot]<=live_up[slot];work_misses[slot]<=live_misses[slot];work_match[slot]<=15;
                    work_x[slot]<=live_x[slot];work_y[slot]<=live_y[slot];work_width[slot]<=live_width[slot];work_height[slot]<=live_height[slot];
                    work_left[slot]<=live_left[slot];work_right[slot]<=live_right[slot];work_top[slot]<=live_top[slot];work_bottom[slot]<=live_bottom[slot];
                    work_vx[slot]<=live_vx[slot];work_vy[slot]<=live_vy[slot];
                end
            end else if(i_fault)begin reg_frame_reason<=5;end
            else case(state_current)
                ST_COLLECT:begin
                    if(i_candidate_valid)begin
                        if(cnt_candidates<8)begin
                            cand_color[cnt_candidates]<=i_color;cand_x[cnt_candidates]<=wire_input_x[12:1];cand_y[cnt_candidates]<=wire_input_y[12:1];
                            cand_width[cnt_candidates]<={1'b0,i_x_max}-{1'b0,i_x_min}+13'd1;
                            cand_height[cnt_candidates]<={1'b0,i_y_max}-{1'b0,i_y_min}+13'd1;
                            cand_left[cnt_candidates]<=i_x_min;cand_right[cnt_candidates]<=i_x_max;
                            cand_top[cnt_candidates]<=i_y_min;cand_bottom[cnt_candidates]<=i_y_max;cnt_candidates<=cnt_candidates+1'b1;
                            if(i_color==0 || i_x_max<i_x_min || i_y_max<i_y_min)begin flag_bad<=1;reg_frame_reason<=5;end
                        end else begin flag_bad<=1;reg_frame_reason<=1;end
                    end
                    if(i_frame_done)begin
                        if(i_overflow)begin reg_frame_reason<=1;end
                        else if(cnt_candidates>4)begin reg_frame_reason<=2;end
                    end
                end
                ST_SEARCH_INIT:begin flag_best<=0;reg_best_distance<=16'hffff;cnt_track<=0;cnt_candidate<=0;end
                ST_SEARCH:begin
                    if(flag_pair && (!flag_best || wire_distance<reg_best_distance))begin
                        flag_best<=1;reg_best_distance<=wire_distance;reg_best_track<=cnt_track;reg_best_candidate<=cnt_candidate;
                    end
                    if(cnt_candidate==7)begin cnt_candidate<=0;cnt_track<=cnt_track+1'b1;end
                    else begin cnt_candidate<=cnt_candidate+1'b1;end
                    if(flag_last_pair && !flag_best)begin cnt_slot<=0;end
                end
                ST_BIND:begin
                    work_used[reg_best_track]<=1;cand_used[reg_best_candidate]<=1;work_match[reg_best_track]<={1'b0,reg_best_candidate};
                    cnt_pairs<=cnt_pairs+1'b1;if(cnt_pairs==3)begin cnt_slot<=0;end
                end
                ST_MISS:begin
                    if(work_active[cnt_slot] && !work_used[cnt_slot])begin
                        work_misses[cnt_slot]<=work_misses[cnt_slot]+1'b1;
                        if(!work_armed[cnt_slot])begin work_up[cnt_slot]<=0;end
                        if(work_misses[cnt_slot]>=C_MAX_MISSES-1)begin work_active[cnt_slot]<=0;end
                    end
                    cnt_slot<=cnt_slot+1'b1;
                end
                ST_CAPACITY:begin cnt_candidate<=0;end
                ST_ALLOCATE:begin
                    if(cnt_candidate<cnt_candidates && !cand_used[cnt_candidate] && flag_free)begin
                        work_active[dec_free_slot]<=1;work_new[dec_free_slot]<=1;
                        work_color[dec_free_slot]<=cand_color[cnt_candidate];work_match[dec_free_slot]<={1'b0,cnt_candidate};
                        work_up[dec_free_slot]<=0;work_armed[dec_free_slot]<=0;work_counted[dec_free_slot]<=0;work_blocked[dec_free_slot]<=0;
                        work_misses[dec_free_slot]<=0;work_width[dec_free_slot]<=0;work_height[dec_free_slot]<=0;
                        work_vx[dec_free_slot]<=0;work_vy[dec_free_slot]<=0;cand_used[cnt_candidate]<=1;
                    end
                    cnt_candidate<=cnt_candidate+1'b1;cnt_slot<=0;
                end
                ST_UPDATE:begin
                    if(work_active[cnt_slot] && work_match[cnt_slot]!=15)begin
                        if(!work_new[cnt_slot] && work_misses[cnt_slot]==0)begin work_vx[cnt_slot]<=wire_vx;work_vy[cnt_slot]<=wire_vy;end
                        work_x[cnt_slot]<=cand_x[wire_match];work_y[cnt_slot]<=cand_y[wire_match];
                        work_width[cnt_slot]<=cand_width[wire_match];work_height[cnt_slot]<=cand_height[wire_match];
                        work_left[cnt_slot]<=cand_left[wire_match];work_right[cnt_slot]<=cand_right[wire_match];
                        work_top[cnt_slot]<=cand_top[wire_match];work_bottom[cnt_slot]<=cand_bottom[wire_match];work_misses[cnt_slot]<=0;
                        if(!work_counted[cnt_slot] && !work_blocked[cnt_slot])begin
                            if(cand_x[wire_match]<=C_LINE-C_HYST)begin
                                if(work_up[cnt_slot]>=1)begin work_up[cnt_slot]<=2;work_armed[cnt_slot]<=1;end
                                else begin work_up[cnt_slot]<=1;end
                            end else if(!work_armed[cnt_slot])begin work_blocked[cnt_slot]<=1;reg_frame_reason<=3;end
                            else if(cand_x[wire_match]>=C_LINE+C_HYST)begin
                                work_counted[cnt_slot]<=1;
                                case(work_color[cnt_slot])
                                    1:cnt_delta_red<=cnt_delta_red+1'b1;
                                    2:cnt_delta_yellow<=cnt_delta_yellow+1'b1;
                                    3:cnt_delta_green<=cnt_delta_green+1'b1;
                                    default:begin end
                                endcase
                            end
                        end
                    end
                    cnt_slot<=cnt_slot+1'b1;
                end
                ST_SUM:begin
                    reg_sum_red<={1'b0,reg_red_o}+cnt_delta_red;
                    reg_sum_green<={1'b0,reg_green_o}+cnt_delta_green;
                    reg_sum_yellow<={1'b0,reg_yellow_o}+cnt_delta_yellow;
                end
                ST_COMMIT,ST_CAPACITY_FAIL:begin
                    live_active<=work_active;live_armed<=work_armed;live_counted<=work_counted;live_blocked<=work_blocked;
                    for(slot=0;slot<4;slot=slot+1)begin
                        live_color[slot]<=work_color[slot];live_up[slot]<=work_up[slot];live_misses[slot]<=work_misses[slot];
                        live_x[slot]<=work_x[slot];live_y[slot]<=work_y[slot];live_width[slot]<=work_width[slot];live_height[slot]<=work_height[slot];
                        live_left[slot]<=work_left[slot];live_right[slot]<=work_right[slot];live_top[slot]<=work_top[slot];live_bottom[slot]<=work_bottom[slot];
                        live_vx[slot]<=work_vx[slot];live_vy[slot]<=work_vy[slot];
                    end
                    reg_done_o<=1;reg_center_x_o<=work_active!=0 ? work_x[wire_first] : 12'd0;
                    reg_center_y_o<=work_active!=0 ? work_y[wire_first] : 12'd0;
                    if(state_current==ST_CAPACITY_FAIL)begin reg_reason_o<=2;reg_state_o<=4;end
                    else begin
                        reg_red_o<=reg_sum_red[32] ? 32'hffffffff : reg_sum_red[31:0];
                        reg_green_o<=reg_sum_green[32] ? 32'hffffffff : reg_sum_green[31:0];
                        reg_yellow_o<=reg_sum_yellow[32] ? 32'hffffffff : reg_sum_yellow[31:0];
                        reg_reason_o<=(reg_sum_red[32] || reg_sum_green[32] || reg_sum_yellow[32]) ? 6 : reg_frame_reason;
                        reg_state_o<=|(work_active & work_armed & ~work_counted) ? 2 : |(work_active & work_counted) ? 3 : 1;
                    end
                end
                ST_REJECT:begin reg_done_o<=1;reg_reason_o<=reg_frame_reason;reg_state_o<=4;end
                default:begin end
            endcase
        end
    end
    genvar box;
    generate for(box=0;box<4;box=box+1)begin:gen_box
        assign o_box_left[box*12 +:12]=live_left[box];assign o_box_right[box*12 +:12]=live_right[box];
        assign o_box_top[box*12 +:12]=live_top[box];assign o_box_bottom[box*12 +:12]=live_bottom[box];
        assign o_box_color[box*2 +:2]=live_misses[box]!=0 ? 2'd0 : live_color[box];
    end endgenerate
    assign o_box_valid=live_active;
    assign o_active_count=live_active[0]+live_active[1]+live_active[2]+live_active[3];
    assign o_done=reg_done_o;assign o_busy=state_current!=ST_IDLE;
    assign o_red=reg_red_o;assign o_green=reg_green_o;assign o_yellow=reg_yellow_o;
    assign o_total={2'd0,reg_red_o}+{2'd0,reg_green_o}+{2'd0,reg_yellow_o};
    assign o_state=reg_state_o;assign o_reason=reg_reason_o;
    assign o_center_x=reg_center_x_o;assign o_center_y=reg_center_y_o;
endmodule
