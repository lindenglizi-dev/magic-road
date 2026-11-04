`timescale 1ns / 1ps
// 有方向计数门；颜色锁存与门占用保持不依赖全画面目标ID。
module ball_gate_counter #(
    parameter C_GATE_MIN = 544,
    parameter C_GATE_END = 736,
    parameter C_GATE_TOP = 160,
    parameter C_GATE_BOTTOM = 640,
    parameter C_LINE = 640,
    parameter C_HYST = 16,
    parameter C_MIN_GATE_PIXELS = 8
)(
    input i_clk,
    input i_rstn,
    input i_clear,
    input i_clear_counts,
    input i_fault,
    input i_frame_start,
    input i_candidate_valid,
    input [1:0] i_color,
    input [11:0] i_x_min,
    input [11:0] i_x_max,
    input [11:0] i_y_min,
    input [11:0] i_y_max,
    input i_frame_done,
    input i_overflow,
    input [19:0] i_gate_pixels,
    output [31:0] o_red,
    output [31:0] o_yellow,
    output [31:0] o_green,
    output [33:0] o_total,
    output [2:0] o_state,
    output [1:0] o_empty,
    output [1:0] o_event,
    output [2:0] o_reason,
    output [11:0] o_center_x,
    output [11:0] o_center_y
);
    localparam ST_WAIT_CLEAR=0, ST_READY=1, ST_ARMED=2, ST_HOLD=3, ST_BLOCKED=4;
    reg [2:0] state_current, state_next;
    reg [1:0] cnt_candidates, cnt_empty, cnt_confirm, cnt_back;
    reg [1:0] reg_pending_color, reg_locked_color, reg_candidate_color;
    reg [11:0] reg_candidate_x, reg_candidate_y;
    reg [31:0] reg_red_o, reg_yellow_o, reg_green_o;
    reg [1:0] reg_event_o;
    reg [2:0] reg_reason_o;
    reg [11:0] reg_center_x_o, reg_center_y_o;
    wire [12:0] wire_sum_x={1'b0,i_x_min}+{1'b0,i_x_max};
    wire [12:0] wire_sum_y={1'b0,i_y_min}+{1'b0,i_y_max};
    wire flag_intersects=i_x_min < C_GATE_END && i_x_max >= C_GATE_MIN &&
                         i_y_min < C_GATE_BOTTOM && i_y_max >= C_GATE_TOP;
    wire flag_empty=i_gate_pixels < C_MIN_GATE_PIXELS && cnt_candidates == 0;
    wire flag_center_inside=reg_candidate_x >= C_GATE_MIN && reg_candidate_x < C_GATE_END &&
                            reg_candidate_y >= C_GATE_TOP && reg_candidate_y < C_GATE_BOTTOM;
    wire flag_upstream=reg_candidate_x <= C_LINE-C_HYST;
    wire flag_downstream=reg_candidate_x >= C_LINE+C_HYST;
    wire flag_confirmed=reg_pending_color == reg_candidate_color && cnt_confirm >= 1;
    wire flag_color_mismatch=(state_current == ST_ARMED || state_current == ST_HOLD) &&
                             reg_candidate_color != reg_locked_color;
    wire flag_saturated=(reg_locked_color == 1 && reg_red_o == 32'hffffffff) ||
                         (reg_locked_color == 2 && reg_yellow_o == 32'hffffffff) ||
                         (reg_locked_color == 3 && reg_green_o == 32'hffffffff);

    // 门内目标列表按完整检测帧积累，原始占用另由前端保留。
    always @(posedge i_clk or negedge i_rstn)begin
        if(!i_rstn)begin
            cnt_candidates<=0; reg_candidate_color<=0; reg_candidate_x<=0; reg_candidate_y<=0;
        end else if(i_clear || i_frame_start)begin
            cnt_candidates<=0;
        end else if(i_candidate_valid && flag_intersects)begin
            if(cnt_candidates < 2)begin cnt_candidates<=cnt_candidates+1'b1; end
            reg_candidate_color<=i_color; reg_candidate_x<=wire_sum_x[12:1]; reg_candidate_y<=wire_sum_y[12:1];
        end
    end
    // 状态寄存过程与输出任务分开，clear优先于同拍旧帧完成。
    always @(posedge i_clk or negedge i_rstn)begin
        if(!i_rstn)begin state_current<=ST_WAIT_CLEAR; end
        else if(i_clear)begin state_current<=ST_WAIT_CLEAR; end
        else begin state_current<=state_next; end
    end
    always @(*)begin
        state_next=state_current;
        if(i_fault)begin state_next=ST_BLOCKED; end
        else if(i_frame_done)begin
            if(i_overflow)begin state_next=ST_BLOCKED; end
            else if(flag_empty)begin
                if(cnt_empty >= 2)begin state_next=ST_READY; end
            end else if(cnt_candidates > 1)begin state_next=ST_BLOCKED; end
            else if(cnt_candidates == 1 && flag_center_inside)begin
                if(flag_color_mismatch)begin state_next=ST_BLOCKED;end
                else case(state_current)
                    ST_READY:begin
                        if(!flag_upstream)begin state_next=ST_BLOCKED; end
                        else if(flag_confirmed)begin state_next=ST_ARMED; end
                    end
                    ST_ARMED:begin
                        if(flag_downstream)begin state_next=ST_HOLD; end
                    end
                    ST_HOLD:begin
                        if(flag_upstream && cnt_back >= 1)begin state_next=ST_BLOCKED; end
                    end
                    default:begin end
                endcase
            end
        end
    end

    // 已计数状态无超时释放；仅三个完整空门帧可以重新武装。
    always @(posedge i_clk or negedge i_rstn)begin
        if(!i_rstn)begin
            cnt_empty<=0; cnt_confirm<=0; cnt_back<=0; reg_pending_color<=0; reg_locked_color<=0;
            reg_red_o<=0; reg_yellow_o<=0; reg_green_o<=0; reg_event_o<=0; reg_reason_o<=0;
            reg_center_x_o<=0; reg_center_y_o<=0;
        end else begin
            reg_event_o<=0;
            if(i_clear)begin
                cnt_empty<=0; cnt_confirm<=0; cnt_back<=0; reg_pending_color<=0; reg_locked_color<=0;
                reg_reason_o<=0; reg_center_x_o<=0; reg_center_y_o<=0;
                if(i_clear_counts)begin reg_red_o<=0; reg_yellow_o<=0; reg_green_o<=0; end
            end else if(i_fault)begin
                cnt_empty<=0; cnt_confirm<=0; cnt_back<=0; reg_reason_o<=5;
            end else if(i_frame_done)begin
                if(i_overflow)begin
                    cnt_empty<=0; cnt_confirm<=0; cnt_back<=0; reg_reason_o<=1;
                end else if(flag_empty)begin
                    if(cnt_empty < 3)begin cnt_empty<=cnt_empty+1'b1; end
                    cnt_confirm<=0; cnt_back<=0;
                    if(cnt_empty >= 2)begin
                        reg_pending_color<=0; reg_locked_color<=0; reg_reason_o<=0;
                    end
                end else begin
                    cnt_empty<=0;
                    if(cnt_candidates > 1)begin
                        cnt_confirm<=0; cnt_back<=0; reg_reason_o<=2;
                    end else if(cnt_candidates == 1 && flag_center_inside)begin
                        reg_center_x_o<=reg_candidate_x; reg_center_y_o<=reg_candidate_y;
                        if(flag_color_mismatch)begin cnt_confirm<=0;cnt_back<=0;reg_reason_o<=4;end
                        else case(state_current)
                            ST_READY:begin
                                if(flag_upstream)begin
                                    reg_pending_color<=reg_candidate_color;
                                    if(flag_confirmed)begin cnt_confirm<=2; reg_locked_color<=reg_candidate_color; end
                                    else begin cnt_confirm<=1; end
                                end else begin reg_reason_o<=3; cnt_confirm<=0; end
                            end
                            ST_ARMED:begin
                                if(flag_downstream)begin
                                    if(flag_saturated)begin reg_reason_o<=6; end
                                    else begin
                                        reg_event_o<=reg_locked_color;
                                        case(reg_locked_color)
                                            1:begin reg_red_o<=reg_red_o+1'b1; end
                                            2:begin reg_yellow_o<=reg_yellow_o+1'b1; end
                                            3:begin reg_green_o<=reg_green_o+1'b1; end
                                            default:begin end
                                        endcase
                                    end
                                end
                            end
                            ST_HOLD:begin
                                if(flag_upstream)begin
                                    if(cnt_back >= 1)begin reg_reason_o<=4; end
                                    else begin cnt_back<=cnt_back+1'b1; end
                                end else begin cnt_back<=0; end
                            end
                            default:begin end
                        endcase
                    end else begin cnt_confirm<=0; cnt_back<=0; end
                end
            end
        end
    end
    assign o_red=reg_red_o;
    assign o_yellow=reg_yellow_o;
    assign o_green=reg_green_o;
    assign o_total={2'b0,reg_red_o}+{2'b0,reg_yellow_o}+{2'b0,reg_green_o};
    assign o_state=state_current;
    assign o_empty=cnt_empty;
    assign o_event=reg_event_o;
    assign o_reason=reg_reason_o;
    assign o_center_x=reg_center_x_o;
    assign o_center_y=reg_center_y_o;
endmodule
