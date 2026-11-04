// GUI overlays are separate. This optional two-pixel border is real HDMI output.
module roi_border_overlay #(parameter W=1280,H=720)(
 input clk,rst_n,input [95:0] rgb,input valid,user_mark,last_mark,done,
 input [95:0] roi_cfg,
 output reg [95:0] out_rgb,output reg ov,ou,ol,od);
 reg [11:0] x,y;wire [11:0] px=user_mark?12'd0:x,py=user_mark?12'd0:y;
 wire enabled=roi_cfg[0]&&roi_cfg[24];
 wire [15:0] x0=roi_cfg[47:32],y0=roi_cfg[63:48],x1=roi_cfg[79:64],y1=roi_cfg[95:80];
 integer i,xx;reg inside,border;reg [95:0] painted;
 always @*begin
 painted=rgb;xx=0;inside=0;border=0;
 for(i=0;i<4;i=i+1)begin
 xx=px+i;inside=enabled&&xx>=x0&&xx<x1&&py>=y0&&py<y1;
 border=inside&&(xx<x0+2||xx>=x1-2||py<y0+2||py>=y1-2);
 if(border)painted[95-i*24-:24]=24'hffffff;
 end end
 always @(posedge clk or negedge rst_n)begin
 if(!rst_n)begin x<=0;y<=0;out_rgb<=0;ov<=0;ou<=0;ol<=0;od<=0;end
 else begin
 out_rgb<=painted;ov<=valid;ou<=user_mark;ol<=last_mark;od<=done;
 if(user_mark)begin x<=0;y<=0;end
 if(valid)begin if(px==W-4)begin x<=0;y<=py==H-1?0:py+1'b1;end else begin x<=px+4;y<=py;end end
 end end
endmodule
