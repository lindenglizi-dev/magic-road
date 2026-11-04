`timescale 1ns / 1ps
// 两键同步消抖；稳定按下沿切换计数暂停/掩膜，保持和松开不重复。
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
    input i_session_restart, // 外部会话在early边界提交，保留epoch兼容接口。
    output o_count_mode,
    output o_count_enable,
    output o_strict,
    output o_mask,
    output [15:0] o_epoch,
    output [15:0] o_active_epoch, // 已提交epoch，与本帧组合前视epoch分离。
    output o_clear,
    output o_key_clear, // KEY3/4已裁掉，旧清零接口固定无请求。
    output o_clear_counts,
    output o_face_relock, // KEY4已裁掉，旧重锁接口固定无请求。
    output o_white_calibrate,
    output [1:0] o_camera_step // 保留旧接口，曝光/增益按键切换已移除。
);
    reg [1:0] reg_sync_first, reg_sync_second, reg_stable, reg_pressed;
    reg [C_COUNT_BITS-1:0] cnt_debounce[0:1];
    reg flag_request_mode, flag_request_mask;
    reg flag_active_mode, flag_active_mask;
    reg [15:0] cnt_epoch;
                                                                                 
    wire flag_change=i_early && i_session_restart;
    integer key_index;
    always @(posedge i_clk or negedge i_rstn)begin
        if(!i_rstn)begin
            reg_sync_first<=3; reg_sync_second<=3; reg_stable<=3; reg_pressed<=0;
            for(key_index=0;key_index<2;key_index=key_index+1)begin cnt_debounce[key_index]<=0; end
        end else begin
            reg_sync_first<=i_keys_n[1:0]; reg_sync_second<=reg_sync_first; reg_pressed<=0;
            for(key_index=0;key_index<2;key_index=key_index+1)begin
                if(reg_sync_second[key_index] == reg_stable[key_index])begin cnt_debounce[key_index]<=0; end
                else if(cnt_debounce[key_index] == C_DEBOUNCE-1)begin
                    cnt_debounce[key_index]<=0; reg_stable[key_index]<=reg_sync_second[key_index];
                    if(!reg_sync_second[key_index])begin reg_pressed[key_index]<=1; end
                end else begin cnt_debounce[key_index]<=cnt_debounce[key_index]+1'b1; end
            end
        end
    end
    always @(posedge i_clk or negedge i_rstn)begin
        if(!i_rstn)begin
            flag_request_mode<=1; flag_request_mask<=0;
            flag_active_mode<=1; flag_active_mask<=0; cnt_epoch<=0;
        end else begin
            if(i_early)begin
                flag_active_mode<=flag_request_mode;
                flag_active_mask<=flag_request_mask;
                if(flag_change)begin cnt_epoch<=cnt_epoch+1'b1; end
            end
            // KEY3/4已移除；参数/清零由面板统一提交，epoch保留接口。
            if(reg_pressed[0])begin flag_request_mode<=!flag_request_mode; end
            if(reg_pressed[1])begin flag_request_mask<=!flag_request_mask; end
        end
    end
    assign o_count_mode=1'b1;
    assign o_count_enable=i_early ? flag_request_mode : flag_active_mode;
    assign o_strict=1'b0;
    assign o_mask=i_early ? flag_request_mask : flag_active_mask;
    assign o_epoch=flag_change ? cnt_epoch+1'b1 : cnt_epoch;
    assign o_active_epoch=cnt_epoch;
    assign o_clear=flag_change;
    assign o_key_clear=1'b0;
    assign o_clear_counts=1'b0;
    assign o_face_relock=1'b0;
    assign o_camera_step=2'b00;
    assign o_white_calibrate=1'b0;
endmodule
