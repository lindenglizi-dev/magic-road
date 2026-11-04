`timescale 1ns / 1ps
// 四键同步消抖；前三键短按松开触发，长按分别调整曝光、增益及白纸校准。
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
    output o_count_mode,
    output o_strict,
    output o_mask,
    output [15:0] o_epoch,
    output o_clear,
    output o_clear_counts,
    output [1:0] o_camera_step, // 保持到下一次长按的翻转事件，供相机时钟域同步。
    output o_white_calibrate // 第三键长按单拍，仅供同域显示校准。
);
    reg [3:0] reg_sync_first, reg_sync_second, reg_stable, reg_pressed;
    reg [C_COUNT_BITS-1:0] cnt_debounce[0:3];
    reg [C_HOLD_BITS-1:0] cnt_hold[0:2];
    reg [2:0] flag_long_sent;
    reg [1:0] reg_camera_step;
    reg flag_white_calibrate;
    reg flag_request_mode, flag_request_strict, flag_request_mask, flag_clear_pending;
    reg flag_active_mode, flag_active_strict, flag_active_mask;
    reg [15:0] cnt_epoch;
    wire flag_change=i_early && (flag_request_mode != flag_active_mode ||
                                 flag_request_strict != flag_active_strict || flag_clear_pending);
    integer key_index;
    always @(posedge i_clk or negedge i_rstn)begin
        if(!i_rstn)begin
            reg_sync_first<=15; reg_sync_second<=15; reg_stable<=15; reg_pressed<=0;
            flag_long_sent<=0; reg_camera_step<=0;flag_white_calibrate<=0;
            for(key_index=0;key_index<3;key_index=key_index+1)begin cnt_hold[key_index]<=0; end
            for(key_index=0;key_index<4;key_index=key_index+1)begin cnt_debounce[key_index]<=0; end
        end else begin
            reg_sync_first<=i_keys_n; reg_sync_second<=reg_sync_first; reg_pressed<=0;flag_white_calibrate<=0;
            for(key_index=0;key_index<4;key_index=key_index+1)begin
                if(reg_sync_second[key_index] == reg_stable[key_index])begin cnt_debounce[key_index]<=0; end
                else if(cnt_debounce[key_index] == C_DEBOUNCE-1)begin
                    cnt_debounce[key_index]<=0; reg_stable[key_index]<=reg_sync_second[key_index];
                    if(key_index<3)begin
                        if(reg_sync_second[key_index] && !flag_long_sent[key_index])begin reg_pressed[key_index]<=1; end
                    end else if(!reg_sync_second[key_index])begin reg_pressed[key_index]<=1; end
                end else begin cnt_debounce[key_index]<=cnt_debounce[key_index]+1'b1; end
            end
            for(key_index=0;key_index<3;key_index=key_index+1)begin
                if(reg_stable[key_index])begin
                    cnt_hold[key_index]<=0; flag_long_sent[key_index]<=0;
                end else if(!reg_sync_second[key_index] && !flag_long_sent[key_index])begin
                    if(cnt_hold[key_index] == C_LONG_PRESS-1)begin
                        flag_long_sent[key_index]<=1;
                        if(key_index<2)begin reg_camera_step[key_index]<=!reg_camera_step[key_index];end
                        else begin flag_white_calibrate<=1;end
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
    assign o_clear=flag_change;
    assign o_clear_counts=i_early && flag_clear_pending;
    assign o_camera_step=reg_camera_step;
    assign o_white_calibrate=flag_white_calibrate;
endmodule
