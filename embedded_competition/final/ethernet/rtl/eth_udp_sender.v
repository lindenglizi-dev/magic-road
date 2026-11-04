                                                                                     
module eth_udp_sender(
 input clk,rst_n,enabled,link_ready,input udp_busy,gmii_valid,
 output udp_req,udp_valid,output [7:0] udp_data,output [15:0] udp_length,
 input video_available,output video_pop,output [10:0] video_index,input [7:0] video_data,
 input reply_available,output reply_pop,input [7:0] reply_command,reply_seq,reply_length,
 output [5:0] reply_index,input [7:0] reply_data);
 reg [2:0] state;reg response;reg [10:0] index;reg [15:0] crc;
 wire [15:0] length=response?{8'd0,reply_length}+16'd10:16'd1304;
 reg [7:0] rb;
                                                                                
 reg [10:0] video_position;
 function [15:0] crc_add;input [15:0] old;input [7:0] b;reg [15:0] c;integer k;
 begin c=old^{b,8'd0};for(k=0;k<8;k=k+1)c=c[15]?(c<<1)^16'h1021:c<<1;crc_add=c;end endfunction
 always @*begin
 rb=0;
 case(index)
 0:rb=8'haa;1:rb=8'h55;2:rb=2;3:rb=reply_seq;4:rb=reply_command;5:rb=reply_length;
 default:if(index<6+reply_length)rb=reply_data;
 else if(index==6+reply_length)rb=crc[7:0];else if(index==7+reply_length)rb=crc[15:8];
 else if(index==8+reply_length)rb=13;else rb=10;
 endcase
 end
 assign udp_req=state==1;assign udp_valid=state==2;
 assign udp_data=response?rb:video_data;assign udp_length=length;
 assign video_index=video_position;
                                                                             
 assign reply_index=index[5:0]-6'd5;
 assign video_pop=(state==3&&!udp_busy&&!response)||(state==0&&video_available&&!enabled);
 assign reply_pop=state==3&&!udp_busy&&response;
 always @(posedge clk or negedge rst_n)begin
 if(!rst_n)begin state<=0;response<=0;index<=0;video_position<=0;crc<=16'hffff;end
 else case(state)
 0:if(link_ready&&!udp_busy&&(reply_available||(enabled&&video_available)))begin
 response<=reply_available;index<=0;video_position<=0;crc<=16'hffff;state<=1;end
 1:if(udp_busy)state<=2;
 2:begin
 if(response&&index>=2&&index<6+reply_length)crc<=crc_add(crc,rb);
 if(response)begin
  if(index==length-1)begin state<=3;index<=0;end else index<=index+1'b1;
 end else begin
  if(video_position==11'd1303)begin state<=3;video_position<=0;end
  else video_position<=video_position+1'b1;
 end
 end
                                                                           
                                                                               
 3:if(!udp_busy)state<=0;
 default:state<=0;
 endcase end
endmodule
