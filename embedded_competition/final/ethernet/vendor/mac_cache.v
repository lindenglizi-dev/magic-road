/*******************************MILIANKE*******************************
*Company : MiLianKe Electronic Technology Co., Ltd.
*WebSite:https://www.milianke.com
*TechWeb:https://www.uisrc.com
*tmall-shop:https://milianke.tmall.com
*jd-shop:https://milianke.jd.com
*taobao-shop1: https://milianke.taobao.com
*Create Date: 2024-06-24
*Module Name:
*File Name:
*Description: 
*The reference demo provided by Milianke is only used for learning. 
*We cannot ensure that the demo itself is free of bugs, so users 
*should be responsible for the technical problems and consequences
*caused by the use of their own products.
*Copyright: Copyright (c) MiLianKe
*All rights reserved.
*Revision: 1.1
*Signal description
*1) I_ input
*2) O_ output
*3) IO_ input output
*4) S_ system internal signal
*5) _n activ low
*6) _dg debug signal 
*7) _r delay or register
*8) _s state mechine
*********************************************************************/

/*******************************xxxx模块*********************
--以下是米联客设计的xxxxx模块
1.
2.
3.
4.
*********************************************************************/
                                                                         
`timescale 1ns/1ps
module mac_cache(
 input I_wclk,I_reset,I_wen,input [31:0] I_wip_addr,input [47:0] I_wmac_addr,
 input I_rclk,I_ren,input [31:0] I_rip_addr,output reg [47:0] O_rmac_addr,output reg O_rmac_done);
 reg present;reg [31:0] ip;reg [47:0] mac;
 always @(posedge I_wclk or posedge I_reset)
 if(I_reset)begin present<=0;ip<=0;mac<=0;end
 else if(I_wen)begin present<=1;ip<=I_wip_addr;mac<=I_wmac_addr;end
 always @(posedge I_rclk or posedge I_reset)
 if(I_reset)begin O_rmac_addr<=0;O_rmac_done<=0;end
 else begin O_rmac_done<=I_ren;if(I_ren)O_rmac_addr<=present&&ip==I_rip_addr?mac:48'd0;end
endmodule
