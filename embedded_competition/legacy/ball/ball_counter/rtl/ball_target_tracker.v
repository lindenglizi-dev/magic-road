`timescale 1ns / 1ps
// 单轨迹：同色同尺寸关联、匀速预测；漏检保留两帧后回搜索。
module ball_target_tracker #(
    parameter C_MAX_MOVE = 64,
    parameter C_X_MIN=0, C_Y_MIN=0, C_X_END=4096, C_Y_END=4096
)(
    input i_clk,
    input i_rstn,
    input i_clear,
    input i_frame_start,
    input i_candidate_valid,
    input [1:0] i_color,
    input [19:0] i_area,
    input [11:0] i_x_min,
    input [11:0] i_x_max,
    input [11:0] i_y_min,
    input [11:0] i_y_max,
    input i_frame_done,
    input i_overflow,
    output o_valid,
    output [1:0] o_status,
    output [1:0] o_color,
    output [11:0] o_x_min,
    output [11:0] o_x_max,
    output [11:0] o_y_min,
    output [11:0] o_y_max,
    output [11:0] o_center_x,
    output [11:0] o_center_y
);
    reg flag_valid_o;
    reg [1:0] reg_status_o, reg_color_o;
    reg [11:0] reg_left_o, reg_right_o, reg_top_o, reg_bottom_o, reg_center_x_o, reg_center_y_o;
    reg [1:0] cnt_misses, cnt_color_hits;
    reg flag_best;
    reg [19:0] reg_best_area;
    reg [15:0] reg_best_distance;
    reg [1:0] reg_best_color;
    reg [11:0] reg_best_left, reg_best_right, reg_best_top, reg_best_bottom;
    // 实测位置独立于显示预测框；关联不能把预测框误当成下一次观测。
    reg [11:0] reg_observed_x,reg_observed_y;
    reg [12:0] reg_observed_width,reg_observed_height;
    reg signed [12:0] reg_velocity_x,reg_velocity_y;
    localparam signed [12:0] C_VELOCITY_LIMIT=C_MAX_MOVE*2;
    wire flag_geometry=i_color != 0 && i_x_max >= i_x_min && i_y_max >= i_y_min;
    wire [12:0] wire_width={1'b0,i_x_max}-{1'b0,i_x_min}+13'd1;
    wire [12:0] wire_height={1'b0,i_y_max}-{1'b0,i_y_min}+13'd1;
    wire flag_size_x={1'b0,wire_width} <= ({1'b0,reg_observed_width} << 1) &&
                     {1'b0,reg_observed_width} <= ({1'b0,wire_width} << 1);
    wire flag_size_y={1'b0,wire_height} <= ({1'b0,reg_observed_height} << 1) &&
                     {1'b0,reg_observed_height} <= ({1'b0,wire_height} << 1);
    wire flag_identity=i_color == reg_color_o && flag_size_x && flag_size_y;
    wire [12:0] wire_center_sum_x={1'b0,i_x_min}+{1'b0,i_x_max};
    wire [12:0] wire_center_sum_y={1'b0,i_y_min}+{1'b0,i_y_max};
    wire [11:0] wire_center_x=wire_center_sum_x[12:1];
    wire [11:0] wire_center_y=wire_center_sum_y[12:1];
    wire signed [14:0] wire_velocity_x={{2{reg_velocity_x[12]}},reg_velocity_x};
    wire signed [14:0] wire_velocity_y={{2{reg_velocity_y[12]}},reg_velocity_y};
    wire signed [14:0] wire_travel_x=cnt_misses == 0 ? wire_velocity_x :
        (cnt_misses == 1 ? (wire_velocity_x <<< 1) : (wire_velocity_x <<< 1)+wire_velocity_x);
    wire signed [14:0] wire_travel_y=cnt_misses == 0 ? wire_velocity_y :
        (cnt_misses == 1 ? (wire_velocity_y <<< 1) : (wire_velocity_y <<< 1)+wire_velocity_y);
    wire signed [14:0] wire_predict_x=$signed({3'b0,reg_observed_x})+wire_travel_x;
    wire signed [14:0] wire_predict_y=$signed({3'b0,reg_observed_y})+wire_travel_y;
    wire signed [14:0] wire_residual_x=$signed({3'b0,wire_center_x})-wire_predict_x;
    wire signed [14:0] wire_residual_y=$signed({3'b0,wire_center_y})-wire_predict_y;
    wire [14:0] wire_distance_x=wire_residual_x < 0 ? -wire_residual_x : wire_residual_x;
    wire [14:0] wire_distance_y=wire_residual_y < 0 ? -wire_residual_y : wire_residual_y;
    wire [15:0] wire_residual_distance={1'b0,wire_distance_x}+{1'b0,wire_distance_y};
    wire [14:0] wire_limit=reg_status_o == 1 ? C_MAX_MOVE*2 : C_MAX_MOVE*(cnt_misses+3'd1);
    wire flag_near=wire_distance_x <= wire_limit && wire_distance_y <= wire_limit;
    wire [11:0] wire_observed_distance_x=wire_center_x >= reg_observed_x ? wire_center_x-reg_observed_x : reg_observed_x-wire_center_x;
    wire [11:0] wire_observed_distance_y=wire_center_y >= reg_observed_y ? wire_center_y-reg_observed_y : reg_observed_y-wire_center_y;
    wire flag_stop_near=wire_observed_distance_x <= wire_limit && wire_observed_distance_y <= wire_limit;
    // 急停候选可退回实测位置窗；预测窗内候选始终优先，防止旧位置背景抢占。
    wire [15:0] wire_distance=flag_near ? wire_residual_distance : 16'h4000+wire_residual_distance;
    wire flag_choose=flag_valid_o ? flag_identity && (flag_near || flag_stop_near) && (!flag_best || wire_distance < reg_best_distance) :
                                                   !flag_best || i_area > reg_best_area;

    wire [12:0] wire_best_sum_x={1'b0,reg_best_left}+{1'b0,reg_best_right};
    wire [12:0] wire_best_sum_y={1'b0,reg_best_top}+{1'b0,reg_best_bottom};
    wire [11:0] wire_best_x=wire_best_sum_x[12:1];
    wire [11:0] wire_best_y=wire_best_sum_y[12:1];
    wire signed [12:0] wire_delta_x=$signed({1'b0,wire_best_x})-$signed({1'b0,reg_observed_x});
    wire signed [12:0] wire_delta_y=$signed({1'b0,wire_best_y})-$signed({1'b0,reg_observed_y});
    wire signed [12:0] wire_step_x=wire_delta_x >= -13'sd4 && wire_delta_x <= 13'sd4 ? 13'sd0 :
        (wire_delta_x > C_VELOCITY_LIMIT ? C_VELOCITY_LIMIT :
        (wire_delta_x < -C_VELOCITY_LIMIT ? -C_VELOCITY_LIMIT : wire_delta_x));
    wire signed [12:0] wire_step_y=wire_delta_y >= -13'sd4 && wire_delta_y <= 13'sd4 ? 13'sd0 :
        (wire_delta_y > C_VELOCITY_LIMIT ? C_VELOCITY_LIMIT :
        (wire_delta_y < -C_VELOCITY_LIMIT ? -C_VELOCITY_LIMIT : wire_delta_y));
    // 连续观测才重估速度；缺帧后的首次恢复沿用旧速度，避免把多帧位移当一帧。
    wire signed [12:0] wire_next_velocity_x=!flag_valid_o ? 13'sd0 : (cnt_misses == 0 ? wire_step_x : reg_velocity_x);
    wire signed [12:0] wire_next_velocity_y=!flag_valid_o ? 13'sd0 : (cnt_misses == 0 ? wire_step_y : reg_velocity_y);
    wire signed [13:0] wire_margin_left=C_X_MIN-$signed({2'b0,reg_best_left});
    wire signed [13:0] wire_margin_right=C_X_END-1-$signed({2'b0,reg_best_right});
    wire signed [13:0] wire_margin_top=C_Y_MIN-$signed({2'b0,reg_best_top});
    wire signed [13:0] wire_margin_bottom=C_Y_END-1-$signed({2'b0,reg_best_bottom});
    wire signed [13:0] wire_shift_x=wire_next_velocity_x < wire_margin_left ? wire_margin_left :
        (wire_next_velocity_x > wire_margin_right ? wire_margin_right : wire_next_velocity_x);
    wire signed [13:0] wire_shift_y=wire_next_velocity_y < wire_margin_top ? wire_margin_top :
        (wire_next_velocity_y > wire_margin_bottom ? wire_margin_bottom : wire_next_velocity_y);

    // 帧内仅保存最佳候选；done与最后一个candidate之间由扫描器留出时钟。
    always @(posedge i_clk or negedge i_rstn)begin
        if(!i_rstn)begin
            flag_best<=0; reg_best_area<=0; reg_best_distance<=0; reg_best_color<=0;
            reg_best_left<=0; reg_best_right<=0; reg_best_top<=0; reg_best_bottom<=0;
        end else if(i_clear || i_frame_start)begin
            flag_best<=0; reg_best_area<=0; reg_best_distance<=16'hffff;
        end else if(i_candidate_valid && flag_geometry && flag_choose)begin
            flag_best<=1; reg_best_area<=i_area; reg_best_distance<=wire_distance;
            reg_best_color<=i_color; reg_best_left<=i_x_min; reg_best_right<=i_x_max;
            reg_best_top<=i_y_min; reg_best_bottom<=i_y_max;
        end
    end

    // 只补偿一帧匀速位移，急停会短暂超前；无观测期间冻结而不持续外推。
    always @(posedge i_clk or negedge i_rstn)begin
        if(!i_rstn)begin
            flag_valid_o<=0; reg_status_o<=0; reg_color_o<=0; cnt_misses<=0; cnt_color_hits<=0;
            reg_left_o<=0; reg_right_o<=0; reg_top_o<=0; reg_bottom_o<=0;
            reg_center_x_o<=0; reg_center_y_o<=0;
            reg_observed_x<=0;reg_observed_y<=0;reg_observed_width<=0;reg_observed_height<=0;
            reg_velocity_x<=0;reg_velocity_y<=0;
        end else if(i_clear)begin
            flag_valid_o<=0; reg_status_o<=0; reg_color_o<=0; cnt_misses<=0; cnt_color_hits<=0;
            reg_velocity_x<=0;reg_velocity_y<=0;
        end else if(i_frame_done)begin
            if(i_overflow)begin
                flag_valid_o<=0; reg_status_o<=0; cnt_misses<=0; cnt_color_hits<=0;
                reg_velocity_x<=0;reg_velocity_y<=0;
            end else if(flag_best)begin
                flag_valid_o<=1; cnt_misses<=0; reg_color_o<=reg_best_color;
                reg_observed_x<=wire_best_x;reg_observed_y<=wire_best_y;
                reg_observed_width<={1'b0,reg_best_right}-{1'b0,reg_best_left}+13'd1;
                reg_observed_height<={1'b0,reg_best_bottom}-{1'b0,reg_best_top}+13'd1;
                reg_velocity_x<=wire_next_velocity_x;reg_velocity_y<=wire_next_velocity_y;
                reg_left_o<=$signed({2'b0,reg_best_left})+wire_shift_x;
                reg_right_o<=$signed({2'b0,reg_best_right})+wire_shift_x;
                reg_top_o<=$signed({2'b0,reg_best_top})+wire_shift_y;
                reg_bottom_o<=$signed({2'b0,reg_best_bottom})+wire_shift_y;
                reg_center_x_o<=$signed({2'b0,wire_best_x})+wire_shift_x;
                reg_center_y_o<=$signed({2'b0,wire_best_y})+wire_shift_y;
                if(flag_valid_o && reg_color_o == reg_best_color && cnt_color_hits != 0)begin
                    cnt_color_hits<=2; reg_status_o<=2;
                end else begin cnt_color_hits<=1; reg_status_o<=1; end
            end else if(flag_valid_o && cnt_misses < 2)begin
                cnt_misses<=cnt_misses+1'b1; reg_status_o<=3;
            end else begin
                flag_valid_o<=0; reg_status_o<=0; cnt_misses<=0; cnt_color_hits<=0;
                reg_velocity_x<=0;reg_velocity_y<=0;
            end
        end
    end
    assign o_valid=flag_valid_o;
    assign o_status=reg_status_o;
    assign o_color=reg_color_o;
    assign o_x_min=reg_left_o;
    assign o_x_max=reg_right_o;
    assign o_y_min=reg_top_o;
    assign o_y_max=reg_bottom_o;
    assign o_center_x=reg_center_x_o;
    assign o_center_y=reg_center_y_o;
endmodule
