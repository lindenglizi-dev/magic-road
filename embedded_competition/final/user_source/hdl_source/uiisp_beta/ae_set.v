`timescale 1ns / 1ps
// 保留启动曝光/增益请求与完成握手；I_step兼容保留但不再选择档位。
module ae_set (
    input I_clk,input I_rst,input [1:0] I_step,input I_ae_cfg_done,input I_cam_cfg_done,
    output O_ae_req,output [15:0] O_ae,output [15:0] O_ag
);
    reg [15:0] reg_exposure,reg_gain;
    reg flag_request;
    always @(posedge I_clk or posedge I_rst)begin
        if(I_rst)begin
            reg_exposure<=1990;reg_gain<=17;flag_request<=0;
        end else begin
            flag_request<=0;
            if(!flag_request && I_cam_cfg_done && I_ae_cfg_done && (reg_exposure != 16'd1991 || reg_gain != 16'd144))begin
                reg_exposure<=1991;reg_gain<=144;flag_request<=1;
            end
        end
    end
    assign O_ae_req=flag_request;
    assign O_ae=reg_exposure;
    assign O_ag=reg_gain;
endmodule
