`timescale 1ns / 1ps
// 四键同步消抖；前两键短按在松开时触发，长按只翻转一次相机请求。
module ball_key_control #(
    parameter C_DEBOUNCE=2100000,
    parameter C_COUNT_BITS=$clog2(C_DEBOUNCE+1),
    parameter C_LONG_PRESS=103520000,
    parameter C_HOLD_BITS=$clog2(C_LONG_PRESS+1)
)(
    input i_clk,
    input i_rstn,
    input [3:0] i_keys_n,
    input i_early,
    input i_session_restart, // 人脸门禁在early边界重开统计会话，复用唯一epoch。
    output o_count_mode,
    output o_strict,
    output o_mask,
    output [15:0] o_epoch,
    output [15:0] o_active_epoch, // 已提交epoch；门禁比较此值以避免restart组合反馈。
    output o_clear,
    output o_key_clear, // 仅按键会话清理，不依赖人脸提交，切断门禁反馈链。
    output o_clear_counts,
    output [1:0] o_camera_step // 保持到下一次长按的翻转事件，供相机时钟域同步。
);
    reg [3:0] reg_sync_first, reg_sync_second, reg_stable, reg_pressed;
    reg [C_COUNT_BITS-1:0] cnt_debounce[0:3];
    reg [C_HOLD_BITS-1:0] cnt_hold[0:1];
    reg [1:0] flag_long_sent,reg_camera_step;
    reg flag_request_mode, flag_request_strict, flag_request_mask, flag_clear_pending;
    reg flag_active_mode, flag_active_strict, flag_active_mask;
    reg [15:0] cnt_epoch;
    wire flag_key_change=flag_request_mode != flag_active_mode ||
                         flag_request_strict != flag_active_strict || flag_clear_pending;
    wire flag_change=i_early && (flag_key_change || i_session_restart);
    integer key_index;
    always @(posedge i_clk or negedge i_rstn)begin
        if(!i_rstn)begin
            reg_sync_first<=15; reg_sync_second<=15; reg_stable<=15; reg_pressed<=0;
            flag_long_sent<=0; reg_camera_step<=0;
            for(key_index=0;key_index<2;key_index=key_index+1)begin cnt_hold[key_index]<=0; end
            for(key_index=0;key_index<4;key_index=key_index+1)begin cnt_debounce[key_index]<=0; end
        end else begin
            reg_sync_first<=i_keys_n; reg_sync_second<=reg_sync_first; reg_pressed<=0;
            for(key_index=0;key_index<4;key_index=key_index+1)begin
                if(reg_sync_second[key_index] == reg_stable[key_index])begin cnt_debounce[key_index]<=0; end
                else if(cnt_debounce[key_index] == C_DEBOUNCE-1)begin
                    cnt_debounce[key_index]<=0; reg_stable[key_index]<=reg_sync_second[key_index];
                    if(key_index<2)begin
                        if(reg_sync_second[key_index] && !flag_long_sent[key_index])begin reg_pressed[key_index]<=1; end
                    end else if(!reg_sync_second[key_index])begin reg_pressed[key_index]<=1; end
                end else begin cnt_debounce[key_index]<=cnt_debounce[key_index]+1'b1; end
            end
            for(key_index=0;key_index<2;key_index=key_index+1)begin
                if(reg_stable[key_index])begin
                    cnt_hold[key_index]<=0; flag_long_sent[key_index]<=0;
                end else if(!reg_sync_second[key_index] && !flag_long_sent[key_index])begin
                    if(cnt_hold[key_index] == C_LONG_PRESS-1)begin
                        flag_long_sent[key_index]<=1;
                        reg_camera_step[key_index]<=!reg_camera_step[key_index];
                    end else begin cnt_hold[key_index]<=cnt_hold[key_index]+1'b1; end
                end
            end
        end
    end
    always @(posedge i_clk or negedge i_rstn)begin
        if(!i_rstn)begin
            flag_request_mode<=0; flag_request_strict<=0; flag_request_mask<=0; flag_clear_pending<=0;
            flag_active_mode<=0; flag_active_strict<=0; flag_active_mask<=0; cnt_epoch<=0;
        end else begin
            if(i_early)begin
                flag_active_mode<=flag_request_mode; flag_active_strict<=flag_request_strict;
                flag_active_mask<=flag_request_mask; flag_clear_pending<=0;
                if(flag_change)begin cnt_epoch<=cnt_epoch+1'b1; end
            end
            // 清零按键优先；同拍新请求留待下一个early，不丢失按键。
            if(reg_pressed[3])begin flag_clear_pending<=1; end
            else begin
                if(reg_pressed[0])begin flag_request_mode<=!flag_request_mode; end
                if(reg_pressed[1])begin flag_request_mask<=!flag_request_mask; end
                if(reg_pressed[2])begin flag_request_strict<=!flag_request_strict; end
            end
        end
    end
    assign o_count_mode=i_early ? flag_request_mode : flag_active_mode;
    assign o_strict=i_early ? flag_request_strict : flag_active_strict;
    assign o_mask=i_early ? flag_request_mask : flag_active_mask;
    assign o_epoch=flag_change ? cnt_epoch+1'b1 : cnt_epoch;
    assign o_active_epoch=cnt_epoch;
    assign o_clear=flag_change;
    assign o_key_clear=i_early && flag_key_change;
    assign o_clear_counts=i_early && flag_clear_pending;
    assign o_camera_step=reg_camera_step;
endmodule
