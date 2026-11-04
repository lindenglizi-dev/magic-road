

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

/*******************************uiudp_rx模块*********************
--以下是米联客设计的uiudp_rx控制器模块
--1.完成对上层应用数据 udp 报文的接收
*********************************************************************/

`timescale 1ns / 1ps

module uiudp_rx(
 input wire I_reset,I_R_udp_clk,
 input wire [15:0] I_udp_local_port,
 output reg O_R_udp_valid,output reg [7:0] O_R_udp_data,
 output reg [15:0] O_R_udp_len,output wire [15:0] O_R_udp_src_port,
 input wire I_udp_ip_rvalid,input wire [7:0] I_udp_ip_rdata);
 reg [3:0] index;
 reg [15:0] source_port,dest_port,udp_length,remaining;
 assign O_R_udp_src_port=source_port;
                                                                         
                                                                        
 always @(posedge I_R_udp_clk or posedge I_reset)begin
 if(I_reset)begin
   index<=0;source_port<=0;dest_port<=0;udp_length<=0;remaining<=0;
   O_R_udp_valid<=0;O_R_udp_data<=0;O_R_udp_len<=0;
 end else begin
   O_R_udp_valid<=0;
   if(!I_udp_ip_rvalid)begin
     index<=0;source_port<=0;dest_port<=0;udp_length<=0;remaining<=0;
     O_R_udp_data<=0;O_R_udp_len<=0;
   end else begin
     case(index)
       0:begin source_port[15:8]<=I_udp_ip_rdata;index<=1;end
       1:begin source_port[7:0]<=I_udp_ip_rdata;index<=2;end
       2:begin dest_port[15:8]<=I_udp_ip_rdata;index<=3;end
       3:begin dest_port[7:0]<=I_udp_ip_rdata;index<=4;end
       4:begin udp_length[15:8]<=I_udp_ip_rdata;index<=5;end
       5:begin udp_length[7:0]<=I_udp_ip_rdata;index<=6;end
       6:index<=7;
       7:begin
         index<=8;
         if(udp_length>=8 && dest_port==I_udp_local_port)begin
           remaining<=udp_length-8;O_R_udp_len<=udp_length-8;
         end else remaining<=0;
       end
       8:if(remaining!=0)begin
         O_R_udp_valid<=1;O_R_udp_data<=I_udp_ip_rdata;remaining<=remaining-1'b1;
       end
       default:index<=0;
     endcase
   end
 end end
endmodule
