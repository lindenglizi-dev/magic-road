`timescale 1ns / 1ps
// 参考时钟计数真实帧事件；读回值完成转换后通过保持总线握手跨域。
module ball_camera_monitor #(parameter C_REF_CYCLES=23809524)(
    input i_ref_clk,input i_video_clk,input i_rstn,input i_frame,
    input i_cfg_done,input i_read_valid,input i_read_match,input i_bus_error,
    input [15:0] i_read_exposure,input [23:0] i_read_gain,
    output [47:0] o_status
);
    reg flag_frame_toggle;
    reg frame_sync_first,frame_sync_second,frame_seen;
    wire frame_event=frame_sync_second != frame_seen;
    reg [31:0] cnt_reference;
    reg [11:0] cnt_frames_bcd,reg_fps;
    reg [11:0] dec_increment;
    always @(*)begin
        dec_increment=cnt_frames_bcd;
        if(cnt_frames_bcd != 12'h999)begin
            if(cnt_frames_bcd[3:0] != 9)begin dec_increment[3:0]=cnt_frames_bcd[3:0]+1'b1;end
            else begin
                dec_increment[3:0]=0;
                if(cnt_frames_bcd[7:4] != 9)begin dec_increment[7:4]=cnt_frames_bcd[7:4]+1'b1;end
                else begin dec_increment[7:4]=0;dec_increment[11:8]=cnt_frames_bcd[11:8]+1'b1;end
            end
        end
    end
    always @(posedge i_video_clk or negedge i_rstn)begin
        if(!i_rstn)begin flag_frame_toggle<=0;end
        else if(i_frame)begin flag_frame_toggle<=!flag_frame_toggle;end
    end
    always @(posedge i_ref_clk or negedge i_rstn)begin
        if(!i_rstn)begin
            frame_sync_first<=0;frame_sync_second<=0;frame_seen<=0;
            cnt_reference<=0;cnt_frames_bcd<=0;reg_fps<=0;
        end else begin
            frame_sync_first<=flag_frame_toggle;frame_sync_second<=frame_sync_first;frame_seen<=frame_sync_second;
            if(cnt_reference == C_REF_CYCLES-1)begin
                cnt_reference<=0;reg_fps<=frame_event ? dec_increment : cnt_frames_bcd;cnt_frames_bcd<=0;
            end else begin
                cnt_reference<=cnt_reference+1'b1;
                if(frame_event)begin cnt_frames_bcd<=dec_increment;end
            end
        end
    end
    reg flag_read_previous,flag_load,flag_format_ready;
    wire [15:0] exposure_bcd;
    wire exposure_done;
    reg [15:0] reg_exposure_bcd;
    reg [7:0] reg_gain_bcd;
    always @(posedge i_ref_clk or negedge i_rstn)begin
        if(!i_rstn)begin flag_read_previous<=0;flag_load<=0;flag_format_ready<=0;reg_exposure_bcd<=0;reg_gain_bcd<=0;end
        else begin
            flag_read_previous<=i_read_valid;flag_load<=i_read_valid && !flag_read_previous;
            if(!i_read_valid)begin flag_format_ready<=0;end
            else if(exposure_done)begin reg_exposure_bcd<=exposure_bcd;flag_format_ready<=1;end
            if(i_read_valid)begin
                case(i_read_gain)
                    24'h090080:reg_gain_bcd<=8'h04;
                    24'h0b0080:reg_gain_bcd<=8'h08;
                    24'h0f0080:reg_gain_bcd<=8'h16;
                    24'h1f0080:reg_gain_bcd<=8'h32;
                    default:reg_gain_bcd<=0;
                endcase
            end
        end
    end
    ball_decimal_format #(.C_BITS(16),.C_DIGITS(4)) format_Inst(
        .i_clk(i_ref_clk),.i_rstn(i_rstn),.i_load(flag_load),.i_binary(i_read_exposure),
        .o_bcd(exposure_bcd),.o_done(exposure_done),.o_busy());
    wire [1:0] read_state=i_bus_error ? 2'd3 : !i_read_valid || !flag_format_ready ? 2'd0 : i_read_match ? 2'd1 : 2'd2;
    wire [47:0] status_source={9'd0,i_cfg_done,read_state,reg_gain_bcd,reg_exposure_bcd,reg_fps};
    reg [47:0] reg_hold,reg_status;
    reg request_toggle,ack_toggle;
    reg ack_sync_first,ack_sync_second,request_sync_first,request_sync_second;
    reg flag_settle;
    always @(posedge i_ref_clk or negedge i_rstn)begin
        if(!i_rstn)begin reg_hold<=0;request_toggle<=0;ack_sync_first<=0;ack_sync_second<=0;end
        else begin
            ack_sync_first<=ack_toggle;ack_sync_second<=ack_sync_first;
            if(ack_sync_second == request_toggle && status_source != reg_hold)begin
                reg_hold<=status_source;request_toggle<=!request_toggle;
            end
        end
    end
    always @(posedge i_video_clk or negedge i_rstn)begin
        if(!i_rstn)begin
            request_sync_first<=0;request_sync_second<=0;ack_toggle<=0;flag_settle<=0;reg_status<=0;
        end else begin
            request_sync_first<=request_toggle;request_sync_second<=request_sync_first;
            if(flag_settle)begin reg_status<=reg_hold;ack_toggle<=request_sync_second;flag_settle<=0;end
            else if(request_sync_second != ack_toggle)begin flag_settle<=1;end
        end
    end
    assign o_status=reg_status;
endmodule
