`timescale 1ns / 1ps
// COUNT专用四轨迹：逐对关联、逐轨迹越线锁存，整帧提交计数。
module reference_ball_multi_counter #(
    parameter C_PANEL_CONFIG=0,
    parameter C_MAX_MOVE=64,C_LINE=640,C_HYST=16,C_MAX_MISSES=8,
    parameter C_X_MIN=0,C_Y_MIN=0,C_X_END=4096,C_Y_END=4096,C_PREDICT_FRAMES=2
)(
    input i_clk,input i_rstn,input i_clear,input i_clear_counts,input i_fault,
    input i_frame_start,input i_candidate_valid,input [1:0] i_color,
    input [11:0] i_x_min,input [11:0] i_x_max,input [11:0] i_y_min,input [11:0] i_y_max,
    input i_frame_done,input i_overflow,input i_count_enable,
    input [191:0] i_settings,input i_good,input i_considered,input [19:0] i_area,
    input [7:0] i_reject_reason,
    input [11:0] i_line_low,input [11:0] i_line_high,
    output [31:0] o_good,output [31:0] o_bad,output [3:0] o_box_good,
    output [3:0] o_box_quality_pending,output [31:0] o_box_reject_reason,output [3:0] o_box_raw_good,
    output o_done,output o_busy,output [31:0] o_red,output [31:0] o_green,output [31:0] o_yellow,
    output [33:0] o_total,output [2:0] o_state,output [2:0] o_reason,
    output [11:0] o_center_x,output [11:0] o_center_y,output [2:0] o_active_count,
    output [3:0] o_box_valid,output [7:0] o_box_color,
    output [3:0] o_box_predicted,output [7:0] o_identity_color,
    output [47:0] o_box_left,output [47:0] o_box_right,output [47:0] o_box_top,output [47:0] o_box_bottom
);
    wire [7:0] read_cand_reject_reason;
    wire [1:0] read_cand_color;
    wire [11:0] read_cand_x;
    wire [11:0] read_cand_y;
    wire [12:0] read_cand_width;
    wire [12:0] read_cand_height;
    wire [11:0] read_cand_left;
    wire [11:0] read_cand_right;
    wire [11:0] read_cand_top;
    wire [11:0] read_cand_bottom;
    localparam ST_IDLE=0,ST_COLLECT=1,ST_SEARCH_INIT=2,ST_SEARCH=3,ST_BIND=4,
        ST_MISS=5,ST_CAPACITY=6,ST_ALLOCATE=7,ST_UPDATE=8,ST_SUM=9,
        ST_COMMIT=10,ST_REJECT=11,ST_REJECT_AGE=12,ST_REJECT_COMMIT=13,ST_PREDICT_CLAMP=14,ST_PREDICT_APPLY=15,
        ST_SEARCH_SELECT=16,ST_SEARCH_RESIDUAL=17,ST_SEARCH_ABS=18,ST_SEARCH_DISTANCE=19,ST_SEARCH_DRAIN=20,
        ST_QUALITY=21,ST_COLLECT_DONE=22;
    reg [4:0] state_current,state_next;
                                                                                      
    reg signed [14:0] reg_predict_left,reg_predict_top,reg_predict_max_left,reg_predict_max_top;
    reg [12:0] reg_predict_width_minus_one,reg_predict_height_minus_one;
    reg [11:0] reg_predict_clamp_left,reg_predict_clamp_top;
    reg reg_predict_reject;
    reg [3:0] cnt_candidates;
    reg flag_bad,flag_truncated;
    reg flag_fault_seen,flag_frame_count,flag_count_previous;
    reg [2:0] reg_frame_reason;

    reg [19:0] cand_area[0:3]; // 面板按真实着色面积保留四个候选，非面板路径不使用。
    reg [1:0] cand_order[0:3]; // 四槽当前候选的相对到达顺序，0最早、3最晚。
    reg [4:0] cand_good,cand_considered;
    reg [7:0] live_reject_reason[0:3],work_reject_reason[0:3];
    reg [3:0] live_good,work_good;
    reg [3:0] live_sampled,work_sampled,live_sample_good,work_sample_good;
    reg [3:0] live_quality_ready,work_quality_ready;
    reg [2:0] cnt_delta_good,cnt_delta_bad;
    reg [32:0] reg_sum_good,reg_sum_bad;
    reg [31:0] reg_good_o,reg_bad_o;
                                                                                       
    reg signed [14:0] reg_search_x,reg_search_y;
    reg [16:0] reg_search_distance;
    reg flag_search_eligible,flag_search_pair;
    wire signed [14:0] wire_roi_left=C_PANEL_CONFIG ? $signed({3'd0,i_settings[43:32]}) : C_X_MIN;
    wire signed [14:0] wire_roi_top=C_PANEL_CONFIG ? $signed({3'd0,i_settings[59:48]}) : C_Y_MIN;
    wire signed [14:0] wire_roi_end_x=C_PANEL_CONFIG ? $signed({3'd0,i_settings[75:64]}) : C_X_END;
    wire signed [14:0] wire_roi_end_y=C_PANEL_CONFIG ? $signed({3'd0,i_settings[91:80]}) : C_Y_END;
    wire [11:0] wire_line_low=C_PANEL_CONFIG ? i_line_low : C_LINE-C_HYST;
    wire [11:0] wire_line_high=C_PANEL_CONFIG ? i_line_high : C_LINE+C_HYST;
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
    reg [16:0] reg_best_distance;
    reg [2:0] cnt_delta_red,cnt_delta_green,cnt_delta_yellow;
    reg [32:0] reg_sum_red,reg_sum_green,reg_sum_yellow;
    reg [31:0] reg_red_o,reg_green_o,reg_yellow_o;
    reg reg_done_o;
    reg [2:0] reg_state_o,reg_reason_o;
    reg [11:0] reg_center_x_o,reg_center_y_o;
    wire [12:0] wire_input_x={1'b0,i_x_min}+{1'b0,i_x_max};
    wire [12:0] wire_input_y={1'b0,i_y_min}+{1'b0,i_y_max};
    // 两层比较树选面积最小槽；同面积优先替换较晚槽，保留先到的光栅候选。
    wire flag_area_01=cand_area[0]<cand_area[1],flag_area_23=cand_area[2]<cand_area[3];
    wire flag_min_01=flag_area_01 || (cand_area[0]==cand_area[1] && cand_order[0]>cand_order[1]);
    wire flag_min_23=flag_area_23 || (cand_area[2]==cand_area[3] && cand_order[2]>cand_order[3]);
    wire [19:0] wire_min_01=flag_area_01 ? cand_area[0] : cand_area[1];
    wire [19:0] wire_min_23=flag_area_23 ? cand_area[2] : cand_area[3];
    wire [1:0] wire_order_01=flag_min_01 ? cand_order[0] : cand_order[1];
    wire [1:0] wire_order_23=flag_min_23 ? cand_order[2] : cand_order[3];
    wire flag_area_pair=wire_min_01<wire_min_23;
    wire flag_min_pair=flag_area_pair || (wire_min_01==wire_min_23 && wire_order_01>wire_order_23);
    // 与严格大于最小面积等价，四个比较并行；最小槽位仍按原树及到达顺序选择。
    wire flag_replace_larger=i_area>cand_area[0] || i_area>cand_area[1] ||
        i_area>cand_area[2] || i_area>cand_area[3];
    wire [1:0] wire_min_slot=flag_min_pair ? (flag_min_01 ? 2'd0 : 2'd1) : (flag_min_23 ? 2'd2 : 2'd3);
    wire [1:0] wire_collect_slot=cnt_candidates<4 ? cnt_candidates[1:0] : wire_min_slot;
    wire [1:0] wire_allocate_slot,wire_first;
    wire [2:0] wire_match;
                                                                                     
    wire [1:0] wire_work_write_slot=state_current==ST_ALLOCATE ? wire_allocate_slot :
        state_current==ST_BIND ? reg_best_track : cnt_slot;
    reg [1:0] wire_work_read_slot;
    reg [2:0] wire_candidate_read_slot;
    wire [1:0] wire_next_track=state_current==ST_SEARCH_INIT ? 2'd0 :
        (state_current==ST_SEARCH && cnt_candidate==7) ? cnt_track+1'b1 : cnt_track;
    wire [1:0] wire_next_slot=(state_current==ST_SEARCH_DRAIN && !flag_best) ||
        (state_current==ST_BIND && cnt_pairs==3) || state_current==ST_ALLOCATE || state_current==ST_REJECT ? 2'd0 :
        (state_current==ST_PREDICT_APPLY || state_current==ST_UPDATE) ? cnt_slot+1'b1 : cnt_slot;
    wire [2:0] wire_next_candidate=state_current==ST_SEARCH_INIT || state_current==ST_CAPACITY ? 3'd0 :
        state_current==ST_SEARCH ? (cnt_candidate==7 ? 3'd0 : cnt_candidate+1'b1) :
        state_current==ST_ALLOCATE ? cnt_candidate+1'b1 : cnt_candidate;
    wire flag_next_search=state_next==ST_SEARCH_SELECT || state_next==ST_SEARCH_RESIDUAL ||
        state_next==ST_SEARCH_ABS || state_next==ST_SEARCH_DISTANCE || state_next==ST_SEARCH;
                                                                              
                                                                                
    always @(posedge i_clk or negedge i_rstn)begin
        if(!i_rstn)begin wire_work_read_slot<=0;wire_candidate_read_slot<=0;end
        else begin
            wire_work_read_slot<=flag_next_search ? wire_next_track :
                (state_next==ST_COMMIT || state_next==ST_REJECT_COMMIT) ? wire_first : wire_next_slot;
            wire_candidate_read_slot<=(state_next==ST_UPDATE || state_next==ST_QUALITY) ?
                work_match[wire_next_slot][2:0] : wire_next_candidate;
        end
    end
    wire signed [14:0] wire_predict_x=$signed({3'd0,work_x[wire_work_read_slot]})+$signed({{2{work_vx[wire_work_read_slot][12]}},work_vx[wire_work_read_slot]});
    wire signed [14:0] wire_predict_y=$signed({3'd0,work_y[wire_work_read_slot]})+$signed({{2{work_vy[wire_work_read_slot][12]}},work_vy[wire_work_read_slot]});
    wire [14:0] wire_limit=work_misses[wire_work_read_slot]!=0 ? C_MAX_MOVE*2 : C_MAX_MOVE;
    wire flag_size=read_cand_width<=({1'b0,work_width[wire_work_read_slot]}<<1) &&
        work_width[cnt_track]<=({1'b0,read_cand_width}<<1) &&
        read_cand_height<=({1'b0,work_height[wire_work_read_slot]}<<1) &&
        work_height[cnt_track]<=({1'b0,read_cand_height}<<1);
    // PANEL输送方向固定从左到右：下游丢失且已有资格锁的旧件不接管上游新件。
    // 同类目标在线附近反向运动存在身份歧义，双向识别需补充观测信息。
    wire flag_candidate_upstream=C_PANEL_CONFIG && read_cand_x<=wire_line_low;
    wire flag_upstream_birth=flag_candidate_upstream &&
        (work_counted[wire_work_read_slot] || work_blocked[wire_work_read_slot]) && work_x[wire_work_read_slot]>=wire_line_high;
    wire flag_pair_eligible=cnt_candidate<cnt_candidates && work_active[wire_work_read_slot] && !work_used[wire_work_read_slot] &&
        !cand_used[wire_candidate_read_slot] && read_cand_color==work_color[wire_work_read_slot] && flag_size && !flag_upstream_birth;
    // 已计数/blocked的失踪身份最后关联，不能在新件过线时凭距离较近抢走持续观测的新身份。
    wire flag_dormant_locked=C_PANEL_CONFIG && work_misses[wire_work_read_slot]!=0 && (work_counted[wire_work_read_slot] || work_blocked[wire_work_read_slot]);
    wire [15:0] wire_pair_distance={1'b0,reg_search_x}+{1'b0,reg_search_y};
    wire flag_last_pair=cnt_track==3 && cnt_candidate==7;
    wire [2:0] wire_free_count=(!work_active[0])+(!work_active[1])+(!work_active[2])+(!work_active[3]);
    wire [3:0] wire_used_count=cand_used[0]+cand_used[1]+cand_used[2]+cand_used[3]+cand_used[4]+cand_used[5]+cand_used[6]+cand_used[7];
    wire flag_capacity=wire_free_count>=cnt_candidates-wire_used_count;
    reg flag_free,flag_reclaim;
    reg [1:0] dec_free_slot,dec_reclaim_slot;
    integer free_index,slot,entry;
    always @(*)begin
        flag_free=0;dec_free_slot=0;flag_reclaim=0;dec_reclaim_slot=0;
        for(free_index=0;free_index<4;free_index=free_index+1)begin
            if(!work_active[free_index] && !flag_free)begin flag_free=1;dec_free_slot=free_index;end
        end
        // 匹配已结束才使用本选择：仅无空槽且明确上游新生，回收未匹配下游的旧锁身份。
        for(free_index=0;free_index<4;free_index=free_index+1)begin
            if(C_PANEL_CONFIG && !flag_free && !flag_reclaim && flag_candidate_upstream &&
                work_active[free_index] && !work_used[free_index] && work_match[free_index]==15 &&
                work_misses[free_index]!=0 && (work_counted[free_index] || work_blocked[free_index]) &&
                work_color[free_index]==read_cand_color && work_x[free_index]>=wire_line_high)begin
                flag_reclaim=1;dec_reclaim_slot=free_index;
            end
        end
    end
    assign wire_allocate_slot=flag_free ? dec_free_slot : dec_reclaim_slot;
    assign wire_match=work_match[cnt_slot][2:0];
    wire signed [12:0] wire_step_x=$signed({1'b0,read_cand_x})-$signed({1'b0,work_x[wire_work_read_slot]});
    wire signed [12:0] wire_step_y=$signed({1'b0,read_cand_y})-$signed({1'b0,work_y[wire_work_read_slot]});
    localparam signed [12:0] C_VELOCITY_LIMIT=C_MAX_MOVE*2;
    wire signed [12:0] wire_vx=wire_step_x>C_VELOCITY_LIMIT ? C_VELOCITY_LIMIT : wire_step_x < -C_VELOCITY_LIMIT ? -C_VELOCITY_LIMIT : wire_step_x;
    wire signed [12:0] wire_vy=wire_step_y>C_VELOCITY_LIMIT ? C_VELOCITY_LIMIT : wire_step_y < -C_VELOCITY_LIMIT ? -C_VELOCITY_LIMIT : wire_step_y;
    assign wire_first=work_active[0] ? 0 : work_active[1] ? 1 : work_active[2] ? 2 : 3;
                                                                               
    wire signed [14:0] wire_miss_left=$signed({3'd0,work_left[wire_work_read_slot]})+$signed({{2{work_vx[wire_work_read_slot][12]}},work_vx[wire_work_read_slot]});
    wire signed [14:0] wire_miss_top=$signed({3'd0,work_top[wire_work_read_slot]})+$signed({{2{work_vy[wire_work_read_slot][12]}},work_vy[wire_work_read_slot]});
    wire signed [14:0] wire_max_left=wire_roi_end_x-$signed({2'd0,work_width[wire_work_read_slot]});
    wire signed [14:0] wire_max_top=wire_roi_end_y-$signed({2'd0,work_height[wire_work_read_slot]});
    wire count_allowed=flag_frame_count && i_count_enable;

                                                                                   
                                                                                
    wire flag_candidate_payload_write=i_rstn && !i_clear && !i_frame_start && !(i_fault && !flag_fault_seen && state_current!=ST_IDLE && state_current!=ST_REJECT) && state_current==ST_COLLECT && i_candidate_valid &&
        (C_PANEL_CONFIG ? (cnt_candidates<4 || flag_replace_larger) : cnt_candidates<5);
    wire [2:0] wire_candidate_write_slot=C_PANEL_CONFIG ? {1'b0,wire_collect_slot} : cnt_candidates[2:0];

    wire [107:0] wire_candidate_payload;
    wire [2:0] wire_candidate_prefetch=(state_next==ST_UPDATE || state_next==ST_QUALITY) ?
        work_match[wire_next_slot][2:0] : wire_next_candidate;
    assign {read_cand_reject_reason,read_cand_color,read_cand_x,read_cand_y,read_cand_width,read_cand_height,read_cand_left,read_cand_right,read_cand_top,read_cand_bottom}=wire_candidate_payload;
                                                                              
                                                                             
    ball_component_store #(.C_DEPTH(512),.C_ADDR_BITS(9),.C_DATA_BITS(108)) candidate_payload_store(
        .i_clk(i_clk),.i_read_enable(1'b1),.i_read_address({6'd0,wire_candidate_prefetch}),
        .i_write_enable(flag_candidate_payload_write),.i_write_address({6'd0,wire_candidate_write_slot}),
        .i_write_data({(C_PANEL_CONFIG ? i_reject_reason : 8'd0),i_color,wire_input_x[12:1],wire_input_y[12:1],({1'b0,i_x_max}-{1'b0,i_x_min}+13'd1),({1'b0,i_y_max}-{1'b0,i_y_min}+13'd1),i_x_min,i_x_max,i_y_min,i_y_max}),.o_read_data(wire_candidate_payload));
    always @(posedge i_clk or negedge i_rstn)begin
        if(!i_rstn)begin state_current<=ST_IDLE;end
        else if(i_clear)begin state_current<=ST_IDLE;end
        else if(i_frame_start)begin state_current<=ST_COLLECT;end
        else begin state_current<=state_next;end
    end
    always @(*)begin
        state_next=state_current;
        if(i_fault && !flag_fault_seen && state_current!=ST_IDLE && state_current!=ST_REJECT)begin state_next=ST_REJECT;end
        else case(state_current)
            ST_IDLE:begin end
            ST_COLLECT:if(i_frame_done)begin
                state_next=C_PANEL_CONFIG ? ST_COLLECT_DONE : (flag_bad || i_overflow || cnt_candidates>4) ? ST_REJECT : ST_SEARCH_INIT;
            end
            ST_COLLECT_DONE:state_next=flag_bad ? ST_REJECT : ST_SEARCH_INIT;
            ST_SEARCH_INIT:state_next=ST_SEARCH_SELECT;
            ST_SEARCH_SELECT:state_next=ST_SEARCH_RESIDUAL;
            ST_SEARCH_RESIDUAL:state_next=ST_SEARCH_ABS;
            ST_SEARCH_ABS:state_next=ST_SEARCH_DISTANCE;
            ST_SEARCH_DISTANCE:state_next=ST_SEARCH;
            ST_SEARCH:state_next=flag_last_pair ? ST_SEARCH_DRAIN : ST_SEARCH_SELECT;
            ST_SEARCH_DRAIN:state_next=flag_best ? ST_BIND : ST_MISS;
            ST_BIND:state_next=cnt_pairs==3 ? ST_MISS : ST_SEARCH_INIT;
            ST_MISS,ST_REJECT_AGE:state_next=ST_PREDICT_CLAMP;
            ST_PREDICT_CLAMP:state_next=ST_PREDICT_APPLY;
            ST_PREDICT_APPLY:begin
                if(cnt_slot==3)state_next=reg_predict_reject ? ST_REJECT_COMMIT : ST_CAPACITY;
                else state_next=reg_predict_reject ? ST_REJECT_AGE : ST_MISS;
            end
            ST_CAPACITY:state_next=(C_PANEL_CONFIG || flag_capacity) ? ST_ALLOCATE : ST_REJECT;
            ST_ALLOCATE:if(cnt_candidate>=cnt_candidates)begin state_next=C_PANEL_CONFIG ? ST_QUALITY : ST_UPDATE;end
            ST_QUALITY:state_next=ST_UPDATE;
            ST_UPDATE:begin
                if(cnt_slot==3)begin state_next=ST_SUM;end
                else if(C_PANEL_CONFIG)begin state_next=ST_QUALITY;end
            end
            ST_SUM:state_next=ST_COMMIT;
            ST_COMMIT,ST_REJECT_COMMIT:state_next=ST_IDLE;
            ST_REJECT:state_next=ST_REJECT_AGE;
            default:state_next=ST_IDLE;
        endcase
    end
    // live仅在整帧提交时更新；故障不会留下半帧计数或被消耗的计数锁。
    always @(posedge i_clk or negedge i_rstn)begin
        if(!i_rstn)begin
            live_active<=0;work_active<=0;live_armed<=0;work_armed<=0;live_counted<=0;work_counted<=0;
            live_blocked<=0;work_blocked<=0;work_used<=0;work_new<=0;cand_used<=0;
            cnt_candidates<=0;flag_bad<=0;flag_truncated<=0;reg_frame_reason<=0;cnt_track<=0;cnt_slot<=0;cnt_candidate<=0;
            flag_fault_seen<=0;flag_frame_count<=1;flag_count_previous<=1;
            cand_good<=0;cand_considered<=0;live_good<=0;work_good<=0;
            live_sampled<=0;work_sampled<=0;live_sample_good<=0;work_sample_good<=0;
            live_quality_ready<=0;work_quality_ready<=0;
            cnt_delta_good<=0;cnt_delta_bad<=0;reg_sum_good<=0;reg_sum_bad<=0;reg_good_o<=0;reg_bad_o<=0;
            reg_search_x<=0;reg_search_y<=0;reg_search_distance<=0;flag_search_eligible<=0;flag_search_pair<=0;
            cnt_pairs<=0;flag_best<=0;reg_best_distance<=0;reg_best_track<=0;reg_best_candidate<=0;
            cnt_delta_red<=0;cnt_delta_green<=0;cnt_delta_yellow<=0;reg_sum_red<=0;reg_sum_green<=0;reg_sum_yellow<=0;
            reg_red_o<=0;reg_green_o<=0;reg_yellow_o<=0;reg_done_o<=0;reg_state_o<=0;reg_reason_o<=0;
            reg_center_x_o<=0;reg_center_y_o<=0;
            reg_predict_left<=0;reg_predict_top<=0;reg_predict_max_left<=0;reg_predict_max_top<=0;
            reg_predict_width_minus_one<=0;reg_predict_height_minus_one<=0;
            reg_predict_clamp_left<=0;reg_predict_clamp_top<=0;reg_predict_reject<=0;
            for(slot=0;slot<4;slot=slot+1)begin
                cand_area[slot]<=0;cand_order[slot]<=0;
                live_reject_reason[slot]<=0;work_reject_reason[slot]<=0;
                live_color[slot]<=0;work_color[slot]<=0;live_up[slot]<=0;work_up[slot]<=0;
                live_misses[slot]<=0;work_misses[slot]<=0;work_match[slot]<=15;
                live_x[slot]<=0;live_y[slot]<=0;
                live_left[slot]<=0;live_right[slot]<=0;live_top[slot]<=0;live_bottom[slot]<=0;
                
                live_width[slot]<=0;live_height[slot]<=0;
                live_vx[slot]<=0;live_vy[slot]<=0;
            end
        end else begin
            reg_done_o<=0;
            flag_count_previous<=i_count_enable;
            if(!i_count_enable)flag_frame_count<=0;
            if(i_clear)begin
                live_good<=0;work_good<=0;
                live_sampled<=0;work_sampled<=0;live_sample_good<=0;work_sample_good<=0;
                live_quality_ready<=0;work_quality_ready<=0;
                live_active<=0;work_active<=0;live_armed<=0;work_armed<=0;live_counted<=0;work_counted<=0;
                live_blocked<=0;work_blocked<=0;reg_state_o<=0;reg_reason_o<=0;
                flag_fault_seen<=0;
                reg_center_x_o<=0;reg_center_y_o<=0;
                for(slot=0;slot<4;slot=slot+1)begin live_reject_reason[slot]<=0;work_reject_reason[slot]<=0;end
                if(i_clear_counts)begin reg_red_o<=0;reg_green_o<=0;reg_yellow_o<=0;reg_good_o<=0;reg_bad_o<=0;end
            end else if(i_frame_start)begin
                cnt_candidates<=0;flag_bad<=state_current!=ST_IDLE;reg_frame_reason<=state_current!=ST_IDLE ? 5 : 0;
                flag_truncated<=0;
                flag_fault_seen<=0;flag_frame_count<=i_count_enable;
                work_good<=live_good;cnt_delta_good<=0;cnt_delta_bad<=0;
                work_sampled<=live_sampled;work_sample_good<=live_sample_good;work_quality_ready<=live_quality_ready;
                work_active<=live_active;work_armed<=live_armed;work_counted<=live_counted;work_blocked<=live_blocked;
                work_used<=0;work_new<=0;cand_used<=0;cnt_pairs<=0;
                cnt_delta_red<=0;cnt_delta_green<=0;cnt_delta_yellow<=0;
                for(slot=0;slot<4;slot=slot+1)begin
                    work_reject_reason[slot]<=live_reject_reason[slot];
                    work_color[slot]<=live_color[slot];work_up[slot]<=live_up[slot];work_misses[slot]<=live_misses[slot];work_match[slot]<=15;
                    
                    
                    
                end
            end else if(i_fault && !flag_fault_seen && state_current!=ST_IDLE && state_current!=ST_REJECT)begin reg_frame_reason<=5;flag_fault_seen<=1;end
            else case(state_current)
                ST_COLLECT:begin
                    if(i_candidate_valid)begin
                        if(C_PANEL_CONFIG)begin
                            // 每拍均可接收；容量满后只用严格更大的面积替换，质量不参与排名。
                            if(cnt_candidates<4 || flag_replace_larger)begin
                                cand_area[wire_collect_slot]<=i_area;
                                if(cnt_candidates<4)cand_order[wire_collect_slot]<=cnt_candidates[1:0];
                                else for(entry=0;entry<4;entry=entry+1)begin
                                    if(entry==wire_min_slot)cand_order[entry]<=3;
                                    else if(cand_order[entry]>cand_order[wire_min_slot])cand_order[entry]<=cand_order[entry]-1'b1;
                                end
                                cand_good[wire_collect_slot]<=i_good;cand_considered[wire_collect_slot]<=i_considered;
                                
                                
                                
                                
                                
                                
                                
                            end
                            if(cnt_candidates<4)cnt_candidates<=cnt_candidates+1'b1;
                            else flag_truncated<=1;
                            if(i_color==0 || i_x_max<i_x_min || i_y_max<i_y_min)begin flag_bad<=1;reg_frame_reason<=5;end
                        end else if(cnt_candidates<8)begin
                            if(cnt_candidates<5)begin
                            cand_good[cnt_candidates]<=C_PANEL_CONFIG ? i_good : 1'b0;
                            cand_considered[cnt_candidates]<=C_PANEL_CONFIG ? i_considered : 1'b0;
                            
                            
                            
                            
                            
                            
                            end
                            cnt_candidates<=cnt_candidates+1'b1;
                            if(i_color==0 || i_x_max<i_x_min || i_y_max<i_y_min)begin flag_bad<=1;reg_frame_reason<=5;end
                        end else begin flag_bad<=1;reg_frame_reason<=1;end
                    end
                    if(i_frame_done)begin
                        if(i_overflow)begin reg_frame_reason<=1;if(C_PANEL_CONFIG)flag_bad<=1;end
                        else if(!C_PANEL_CONFIG && cnt_candidates>4)begin reg_frame_reason<=2;end
                    end
                end
                ST_SEARCH_INIT:begin flag_best<=0;reg_best_distance<=16'hffff;cnt_track<=0;cnt_candidate<=0;end
                ST_SEARCH_SELECT:begin
                    reg_search_x<=wire_predict_x;reg_search_y<=wire_predict_y;flag_search_eligible<=flag_pair_eligible;
                end
                ST_SEARCH_RESIDUAL:begin
                    reg_search_x<=$signed({3'd0,read_cand_x})-reg_search_x;
                    reg_search_y<=$signed({3'd0,read_cand_y})-reg_search_y;
                end
                ST_SEARCH_ABS:begin
                    reg_search_x<=reg_search_x[14] ? -reg_search_x : reg_search_x;
                    reg_search_y<=reg_search_y[14] ? -reg_search_y : reg_search_y;
                end
                ST_SEARCH_DISTANCE:begin
                    reg_search_distance<={flag_dormant_locked,wire_pair_distance};
                    flag_search_pair<=flag_search_eligible && $unsigned(reg_search_x)<=wire_limit && $unsigned(reg_search_y)<=wire_limit;
                end
                ST_SEARCH:begin
                    if(flag_search_pair && (!flag_best || reg_search_distance<reg_best_distance))begin
                        flag_best<=1;reg_best_distance<=reg_search_distance;reg_best_track<=cnt_track;reg_best_candidate<=cnt_candidate;
                    end
                    if(cnt_candidate==7)begin cnt_candidate<=0;cnt_track<=cnt_track+1'b1;end
                    else begin cnt_candidate<=cnt_candidate+1'b1;end
                end
                ST_SEARCH_DRAIN:begin if(!flag_best)cnt_slot<=0;end
                ST_BIND:begin
                    work_used[wire_work_write_slot]<=1;cand_used[reg_best_candidate]<=1;work_match[wire_work_write_slot]<={1'b0,reg_best_candidate};
                    cnt_pairs<=cnt_pairs+1'b1;if(cnt_pairs==3)begin cnt_slot<=0;end
                end
                ST_MISS,ST_REJECT_AGE:begin
                    reg_predict_left<=wire_miss_left;reg_predict_top<=wire_miss_top;
                    reg_predict_max_left<=wire_max_left;reg_predict_max_top<=wire_max_top;
                    reg_predict_width_minus_one<=work_width[wire_work_read_slot]-13'd1;
                    reg_predict_height_minus_one<=work_height[wire_work_read_slot]-13'd1;
                    reg_predict_reject<=state_current==ST_REJECT_AGE;
                end
                ST_PREDICT_CLAMP:begin
                    reg_predict_clamp_left<=reg_predict_left<wire_roi_left ? wire_roi_left[11:0] :
                        reg_predict_left>reg_predict_max_left ? reg_predict_max_left[11:0] : reg_predict_left[11:0];
                    reg_predict_clamp_top<=reg_predict_top<wire_roi_top ? wire_roi_top[11:0] :
                        reg_predict_top>reg_predict_max_top ? reg_predict_max_top[11:0] : reg_predict_top[11:0];
                end
                ST_PREDICT_APPLY:begin
                    if(work_active[wire_work_read_slot] && (!work_used[wire_work_read_slot] || reg_predict_reject))begin
                        work_sampled[wire_work_write_slot]<=0;
                        work_misses[wire_work_write_slot]<=work_misses[wire_work_read_slot]+1'b1;
                        
                        
                        
                        
                        if(!work_armed[wire_work_write_slot])begin work_up[wire_work_write_slot]<=0;end
                        if(work_misses[wire_work_write_slot]>=C_MAX_MISSES-1)begin work_active[wire_work_write_slot]<=0;end
                    end
                    cnt_slot<=cnt_slot+1'b1;
                end
                ST_CAPACITY:begin
                    cnt_candidate<=0;
                    if(!C_PANEL_CONFIG && !flag_capacity)begin reg_frame_reason<=2;end
                end
                ST_ALLOCATE:begin
                    if(cnt_candidate<cnt_candidates && !cand_used[wire_candidate_read_slot])begin
                        if(flag_free || flag_reclaim)begin
                            work_active[wire_work_write_slot]<=1;work_new[wire_work_write_slot]<=1;
                            work_good[wire_work_write_slot]<=0;work_sampled[wire_work_write_slot]<=0;
                            work_sample_good[wire_work_write_slot]<=0;work_quality_ready[wire_work_write_slot]<=0;
                            work_reject_reason[wire_work_write_slot]<=0;
                            work_color[wire_work_write_slot]<=read_cand_color;work_match[wire_work_write_slot]<={1'b0,cnt_candidate};
                            work_up[wire_work_write_slot]<=0;work_armed[wire_work_write_slot]<=0;work_counted[wire_work_write_slot]<=0;work_blocked[wire_work_write_slot]<=0;
                            work_misses[wire_work_write_slot]<=0;
                            cand_used[wire_candidate_read_slot]<=1;
                        end else if(C_PANEL_CONFIG)begin reg_frame_reason<=2;flag_truncated<=1;end
                    end
                    cnt_candidate<=cnt_candidate+1'b1;cnt_slot<=0;
                end
                ST_QUALITY:begin
                    if(work_active[wire_work_read_slot] && work_match[wire_work_read_slot]!=15)begin
                                                                                   
                        if(work_sampled[wire_work_read_slot] && work_sample_good[wire_work_read_slot]==cand_good[wire_candidate_read_slot])begin
                            work_good[wire_work_write_slot]<=cand_good[wire_candidate_read_slot];work_quality_ready[wire_work_write_slot]<=1;
                        end
                        work_sample_good[wire_work_write_slot]<=cand_good[wire_candidate_read_slot];work_sampled[wire_work_write_slot]<=1;
                        work_reject_reason[wire_work_write_slot]<=read_cand_reject_reason;
                    end
                end
                ST_UPDATE:begin
                    if(work_active[wire_work_read_slot] && work_match[wire_work_read_slot]!=15)begin
                        if(!work_new[wire_work_read_slot] && work_misses[wire_work_read_slot]==0)begin end
                        
                        
                        
                        work_misses[wire_work_write_slot]<=0;
                        if(!work_counted[wire_work_read_slot] && !work_blocked[wire_work_read_slot])begin
                            if(!count_allowed)begin
                                work_up[wire_work_write_slot]<=0;work_armed[wire_work_write_slot]<=0;
                                if(read_cand_x>wire_line_low)work_blocked[wire_work_write_slot]<=1;
                            end else if(read_cand_x<=wire_line_low)begin
                                if(work_up[wire_work_read_slot]>=1)begin work_up[wire_work_write_slot]<=2;work_armed[wire_work_write_slot]<=1;end
                                else begin work_up[wire_work_write_slot]<=1;end
                            end else if(!work_armed[wire_work_read_slot])begin work_blocked[wire_work_write_slot]<=1;reg_frame_reason<=3;end
                            else if(read_cand_x>=wire_line_high && (!C_PANEL_CONFIG || work_quality_ready[wire_work_read_slot]))begin
                                work_counted[wire_work_write_slot]<=1;
                                if(C_PANEL_CONFIG && cand_considered[wire_candidate_read_slot])begin
                                    if(work_good[wire_work_write_slot])cnt_delta_good<=cnt_delta_good+1'b1;
                                    else cnt_delta_bad<=cnt_delta_bad+1'b1;
                                end
                                case(work_color[wire_work_read_slot])
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
                    reg_sum_good<={1'b0,reg_good_o}+cnt_delta_good;
                    reg_sum_bad<={1'b0,reg_bad_o}+cnt_delta_bad;
                    reg_sum_red<={1'b0,reg_red_o}+cnt_delta_red;
                    reg_sum_green<={1'b0,reg_green_o}+cnt_delta_green;
                    reg_sum_yellow<={1'b0,reg_yellow_o}+cnt_delta_yellow;
                end
                ST_COMMIT,ST_REJECT_COMMIT:begin
                    live_good<=work_good;
                    live_sampled<=work_sampled;live_sample_good<=work_sample_good;live_quality_ready<=work_quality_ready;
                    live_active<=work_active;live_armed<=work_armed;live_counted<=work_counted;live_blocked<=work_blocked;
                    for(slot=0;slot<4;slot=slot+1)begin
                        live_reject_reason[slot]<=work_reject_reason[slot];
                        live_color[slot]<=work_color[slot];live_up[slot]<=work_up[slot];live_misses[slot]<=work_misses[slot];
                        live_x[slot]<=work_x[slot];live_y[slot]<=work_y[slot];live_width[slot]<=work_width[slot];live_height[slot]<=work_height[slot];
                        live_left[slot]<=work_left[slot];live_right[slot]<=work_right[slot];live_top[slot]<=work_top[slot];live_bottom[slot]<=work_bottom[slot];
                        live_vx[slot]<=work_vx[slot];live_vy[slot]<=work_vy[slot];
                    end
                    reg_done_o<=1;reg_center_x_o<=work_active!=0 ? work_x[wire_work_read_slot] : 12'd0;
                    reg_center_y_o<=work_active!=0 ? work_y[wire_work_read_slot] : 12'd0;
                    if(state_current==ST_REJECT_COMMIT)begin reg_reason_o<=reg_frame_reason;reg_state_o<=4;end
                    else begin
                        if(count_allowed)begin
                            reg_good_o<=reg_sum_good[32] ? 32'hffffffff : reg_sum_good[31:0];
                            reg_bad_o<=reg_sum_bad[32] ? 32'hffffffff : reg_sum_bad[31:0];
                            reg_red_o<=reg_sum_red[32] ? 32'hffffffff : reg_sum_red[31:0];
                            reg_green_o<=reg_sum_green[32] ? 32'hffffffff : reg_sum_green[31:0];
                            reg_yellow_o<=reg_sum_yellow[32] ? 32'hffffffff : reg_sum_yellow[31:0];
                        end
                        reg_reason_o<=(reg_sum_red[32] || reg_sum_green[32] || reg_sum_yellow[32] || (C_PANEL_CONFIG && (reg_sum_good[32] || reg_sum_bad[32]))) ? 6 :
                            (C_PANEL_CONFIG && flag_truncated) ? 2 : reg_frame_reason;
                        reg_state_o<=|(work_active & work_armed & ~work_counted) ? 2 : |(work_active & work_counted) ? 3 : 1;
                    end
                end
                ST_REJECT:begin
                                                                                          
                    work_good<=live_good;cnt_delta_good<=0;cnt_delta_bad<=0;
                    work_sampled<=live_sampled;work_sample_good<=live_sample_good;work_quality_ready<=live_quality_ready;
                work_active<=live_active;work_armed<=live_armed;work_counted<=live_counted;work_blocked<=live_blocked;cnt_slot<=0;
                    for(slot=0;slot<4;slot=slot+1)begin
                        work_reject_reason[slot]<=live_reject_reason[slot];
                        work_color[slot]<=live_color[slot];work_up[slot]<=live_up[slot];work_misses[slot]<=live_misses[slot];
                        
                        
                        
                    end
                end
                default:begin end
            endcase
                                                                                     
            if(flag_count_previous && !i_count_enable)begin
                live_armed<=0;work_armed<=0;
                for(slot=0;slot<4;slot=slot+1)begin live_up[slot]<=0;work_up[slot]<=0;end
            end
        end
    end
                                                                                 
                                                                               
                                                                                           
    integer payload_slot;
    always @(posedge i_clk or negedge i_rstn)begin
        if(!i_rstn)begin
            for(payload_slot=0;payload_slot<4;payload_slot=payload_slot+1)begin
                work_x[payload_slot]<=0;work_y[payload_slot]<=0;
                work_left[payload_slot]<=0;work_right[payload_slot]<=0;
                work_top[payload_slot]<=0;work_bottom[payload_slot]<=0;
                work_width[payload_slot]<=0;work_height[payload_slot]<=0;
                work_vx[payload_slot]<=0;work_vy[payload_slot]<=0;
            end
        end else if(i_frame_start || state_current==ST_REJECT)begin
            for(payload_slot=0;payload_slot<4;payload_slot=payload_slot+1)begin
                work_x[payload_slot]<=live_x[payload_slot];work_y[payload_slot]<=live_y[payload_slot];
                work_left[payload_slot]<=live_left[payload_slot];work_right[payload_slot]<=live_right[payload_slot];
                work_top[payload_slot]<=live_top[payload_slot];work_bottom[payload_slot]<=live_bottom[payload_slot];
                work_width[payload_slot]<=live_width[payload_slot];work_height[payload_slot]<=live_height[payload_slot];
                work_vx[payload_slot]<=live_vx[payload_slot];work_vy[payload_slot]<=live_vy[payload_slot];
            end
        end else begin
            case(state_current)
                ST_ALLOCATE:begin
                    if(cnt_candidate<cnt_candidates && !cand_used[wire_candidate_read_slot] && (flag_free || flag_reclaim))begin
                        work_width[wire_work_write_slot]<=0;work_height[wire_work_write_slot]<=0;
                        work_vx[wire_work_write_slot]<=0;work_vy[wire_work_write_slot]<=0;
                    end
                end
                ST_PREDICT_APPLY:begin
                    if(work_active[wire_work_read_slot] && (!work_used[wire_work_read_slot] || reg_predict_reject))begin
                        work_left[wire_work_write_slot]<=reg_predict_clamp_left;work_right[wire_work_write_slot]<=reg_predict_clamp_left+reg_predict_width_minus_one;
                        work_top[wire_work_write_slot]<=reg_predict_clamp_top;work_bottom[wire_work_write_slot]<=reg_predict_clamp_top+reg_predict_height_minus_one;
                        work_x[wire_work_write_slot]<=reg_predict_clamp_left+((reg_predict_width_minus_one)>>1);
                        work_y[wire_work_write_slot]<=reg_predict_clamp_top+((reg_predict_height_minus_one)>>1);
                    end
                end
                ST_UPDATE:begin
                    if(work_active[wire_work_read_slot] && work_match[wire_work_read_slot]!=15)begin
                        if(!work_new[wire_work_read_slot] && work_misses[wire_work_read_slot]==0)begin work_vx[wire_work_write_slot]<=wire_vx;work_vy[wire_work_write_slot]<=wire_vy;end
                        work_x[wire_work_write_slot]<=read_cand_x;work_y[wire_work_write_slot]<=read_cand_y;
                        work_width[wire_work_write_slot]<=read_cand_width;work_height[wire_work_write_slot]<=read_cand_height;
                        work_left[wire_work_write_slot]<=read_cand_left;work_right[wire_work_write_slot]<=read_cand_right;
                        work_top[wire_work_write_slot]<=read_cand_top;work_bottom[wire_work_write_slot]<=read_cand_bottom;
                    end
                end
                default:begin end
            endcase
        end
    end
    genvar box;
    generate for(box=0;box<4;box=box+1)begin:gen_box
        assign o_box_left[box*12 +:12]=live_left[box];assign o_box_right[box*12 +:12]=live_right[box];
        assign o_box_top[box*12 +:12]=live_top[box];assign o_box_bottom[box*12 +:12]=live_bottom[box];
        assign o_box_color[box*2 +:2]=live_misses[box]!=0 || (C_PANEL_CONFIG && !live_quality_ready[box]) ? 2'd0 : live_color[box];
        assign o_identity_color[box*2 +:2]=live_color[box];
        assign o_box_good[box]=C_PANEL_CONFIG && o_box_valid[box] && live_quality_ready[box] && live_good[box];
        assign o_box_quality_pending[box]=C_PANEL_CONFIG && o_box_valid[box] && !live_quality_ready[box];
        assign o_box_reject_reason[box*8 +:8]=C_PANEL_CONFIG && live_active[box] ? live_reject_reason[box] : 8'd0;
        assign o_box_raw_good[box]=C_PANEL_CONFIG && live_active[box] && live_sample_good[box];
        assign o_box_valid[box]=live_active[box] && live_misses[box]<=C_PREDICT_FRAMES;
        assign o_box_predicted[box]=o_box_valid[box] && live_misses[box]!=0;
    end endgenerate
    assign o_active_count=live_active[0]+live_active[1]+live_active[2]+live_active[3];
    assign o_done=reg_done_o;assign o_busy=state_current!=ST_IDLE;
    assign o_good=C_PANEL_CONFIG ? reg_good_o : 32'd0;assign o_bad=C_PANEL_CONFIG ? reg_bad_o : 32'd0;
    assign o_red=reg_red_o;assign o_green=reg_green_o;assign o_yellow=reg_yellow_o;
    assign o_total={2'd0,reg_red_o}+{2'd0,reg_green_o}+{2'd0,reg_yellow_o};
    assign o_state=reg_state_o;assign o_reason=reg_reason_o;
    assign o_center_x=reg_center_x_o;assign o_center_y=reg_center_y_o;
endmodule
