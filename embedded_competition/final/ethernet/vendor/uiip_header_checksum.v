/*******************************MILIANKE*******************************
*Company : MiLianKe Electronic Technology Co., Ltd.
*WebSite:https://www.milianke.com
*TechWeb:https://www.uisrc.com
*tmall-shop:https://milianke.tmall.com
*jd-shop:https://milianke.jd.com
*taobao-shop1: https://milianke.taobao.com
*Create Date: 2022/12/23
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

/*******************************uiip_header_checksum模块*********************
--以下是米联客设计的uiip_header_checksum
 uiip_header_checksum 对 IP 数据报包头的校验和迚行计算，判断包头正确性。
*********************************************************************/

`timescale 1ns / 1ps

module uiip_header_checksum(
 input wire I_clk,I_reset,I_ip_rdata_valid,input wire [7:0] I_ip_rdata,
 output wire O_checksum_rerror);
 reg [4:0] index;
 reg [7:0] high_byte;
 reg [15:0] sum;
 reg correct;
 wire [16:0] added={1'b0,sum}+{1'b0,high_byte,I_ip_rdata};
 wire [15:0] folded=added[15:0]+added[16];
 assign O_checksum_rerror=!correct;
                                                                       
                                                                    
 always @(posedge I_clk or posedge I_reset)begin
 if(I_reset)begin index<=0;high_byte<=0;sum<=0;correct<=1;end
 else if(!I_ip_rdata_valid)begin index<=0;high_byte<=0;sum<=0;correct<=1;end
 else if(index<20)begin
   index<=index+1'b1;
   if(!index[0])high_byte<=I_ip_rdata;
   else begin
     sum<=folded;
     if(index==19)correct<=folded==16'hffff;
   end
 end
 end
endmodule
