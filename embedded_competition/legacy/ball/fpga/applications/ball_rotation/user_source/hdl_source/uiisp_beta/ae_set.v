`timescale 1ns / 1ps
// 接收CSI域保持的长按翻转事件，配置忙期间保留最新曝光/增益档位。
module ae_set (
    input I_clk,input I_rst,input [1:0] I_step,input I_ae_cfg_done,input I_cam_cfg_done,
    output O_ae_req,output [15:0] O_ae,output [15:0] O_ag
);
    reg [1:0] reg_sync_first,reg_sync_second,reg_seen;
    wire [1:0] step_event=reg_sync_second ^ reg_seen;
    reg [1:0] reg_exposure_profile,reg_gain_profile;
    reg [15:0] reg_exposure,reg_gain,dec_exposure,dec_gain;
    reg flag_request;
    always @(*)begin
        case(reg_exposure_profile)
            1:dec_exposure=480;2:dec_exposure=240;3:dec_exposure=120;default:dec_exposure=1991;
        endcase
        case(reg_gain_profile)
            1:dec_gain=176;2:dec_gain=80;3:dec_gain=112;default:dec_gain=144;
        endcase
    end
    always @(posedge I_clk or posedge I_rst)begin
        if(I_rst)begin
            reg_sync_first<=0;reg_sync_second<=0;reg_seen<=0;
        end else begin
            reg_sync_first<=I_step;reg_sync_second<=reg_sync_first;reg_seen<=reg_sync_second;
        end
    end
    always @(posedge I_clk or posedge I_rst)begin
        if(I_rst)begin
            reg_exposure_profile<=0;reg_gain_profile<=0;reg_exposure<=1990;reg_gain<=17;flag_request<=0;
        end else begin
            flag_request<=0;
            if(step_event[0])begin reg_exposure_profile<=reg_exposure_profile+1'b1;end
            if(step_event[1])begin reg_gain_profile<=reg_gain_profile+1'b1;end
            if(!flag_request && I_cam_cfg_done && I_ae_cfg_done && (reg_exposure != dec_exposure || reg_gain != dec_gain))begin
                reg_exposure<=dec_exposure;reg_gain<=dec_gain;flag_request<=1;
            end
        end
    end
    assign O_ae_req=flag_request;
    assign O_ae=reg_exposure;
    assign O_ag=reg_gain;
endmodule
