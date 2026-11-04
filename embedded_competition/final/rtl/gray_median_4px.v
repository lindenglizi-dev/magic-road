                                                                            
module gray_median_4px(
    input wire I_clk,I_rst_n, // 现有算法时钟、低有效异步复位。
    input wire [31:0] I_p11,I_p12,I_p13, // 上行左/中/右邻点，每根总线包含四个窗口的对应像素。
    input wire [31:0] I_p21,I_p22,I_p23, // 中行邻点；每根总线高字节对应最左窗口。
    input wire [31:0] I_p31,I_p32,I_p33, // 下行邻点，与Stage4保持相同接口。
    input wire [3:0] I_window_valid, // bit3对应最左窗口，0时强制输出黑色。
    input wire I_tvalid,I_tuser,I_tlast,I_frame_done, // 组有效/帧首/行末/帧末标记。
    input wire [11:0] I_x,I_y, // 本组最左中心坐标。
    output wire [31:0] O_pixel_data, // 四个8bit像素；二值算法只产生0/255。
    output wire [95:0] O_tdata, // 四份RGB888，分别把结果复制到R/G/B。
    output wire O_tvalid,O_tuser,O_tlast,O_frame_done, // 与结果严格对齐的标记。
    output wire [11:0] O_x,O_y, // 与结果对齐的中心坐标。
    output wire [3:0] O_window_valid // 各窗口是否完整，无效组清0。
);

 reg [8:0] v,u,l,d;reg [3:0] mask[0:8];reg [11:0] x[0:8],y[0:8];integer j;
 always @(posedge I_clk or negedge I_rst_n)begin
 if(!I_rst_n)begin v<=0;u<=0;l<=0;d<=0;for(j=0;j<9;j=j+1)begin mask[j]<=0;x[j]<=0;y[j]<=0;end end
 else begin
 v<={v[7:0],I_tvalid};u<={u[7:0],I_tuser};l<={l[7:0],I_tlast};d<={d[7:0],I_frame_done};
 mask[0]<=I_window_valid;x[0]<=I_x;y[0]<=I_y;
 for(j=1;j<9;j=j+1)begin mask[j]<=mask[j-1];x[j]<=x[j-1];y[j]<=y[j-1];end
 end end
 assign O_tvalid=v[8];assign O_tuser=u[8];assign O_tlast=l[8];assign O_frame_done=d[8];
 assign O_x=x[8];assign O_y=y[8];assign O_window_valid=mask[8]&{4{v[8]}};
                                                                               
                                                                                            
 function [23:0] sort3;
 input [7:0] a,b,c;
 reg [7:0] lo,hi,mid;
 begin
  lo=a<b?a:b;hi=a<b?b:a;
  mid=hi<c?hi:c;
  sort3={hi>c?hi:c,lo<mid?mid:lo,lo<mid?lo:mid};
 end
 endfunction
 genvar lane;
 generate for(lane=0;lane<4;lane=lane+1)begin:pixel
 reg [23:0] row0,row1,row2;
 wire [23:0] sorted_min=sort3(row0[7:0],row1[7:0],row2[7:0]);
 wire [23:0] sorted_mid=sort3(row0[15:8],row1[15:8],row2[15:8]);
 wire [23:0] sorted_max=sort3(row0[23:16],row1[23:16],row2[23:16]);
 reg [23:0] survivors;
 wire [23:0] sorted_final=sort3(survivors[7:0],survivors[15:8],survivors[23:16]);
 reg [7:0] delay[0:6];
 integer n;
 always @(posedge I_clk)begin
  row0<=sort3(I_p11[lane*8+:8],I_p12[lane*8+:8],I_p13[lane*8+:8]);
  row1<=sort3(I_p21[lane*8+:8],I_p22[lane*8+:8],I_p23[lane*8+:8]);
  row2<=sort3(I_p31[lane*8+:8],I_p32[lane*8+:8],I_p33[lane*8+:8]);
  survivors<={sorted_min[23:16],sorted_mid[15:8],sorted_max[7:0]};
  delay[0]<=sorted_final[15:8];
  for(n=1;n<7;n=n+1)delay[n]<=delay[n-1];
 end
                                                                                            
 wire [7:0] median_value=(v[8]&&mask[8][lane])?delay[6]:8'd0;
 assign O_pixel_data[lane*8+:8]=median_value;
 assign O_tdata[lane*24+:24]={median_value,median_value,median_value};
 end endgenerate
endmodule
