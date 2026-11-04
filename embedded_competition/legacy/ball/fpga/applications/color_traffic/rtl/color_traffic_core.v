`timescale 1ns/1ps
// AWB RGB888: first pixel [95:72]. No backpressure; coordinates count valid only.
module color_traffic_core #(
 parameter integer W=1280,H=720,
 parameter integer X0=480,Y0=180,X1=800,Y1=540,
 parameter integer MIN_PIXELS=128, DOM_MARGIN=32
)(
 input wire clk,rst_n, input wire [95:0] rgb,
 input wire valid,early, input wire traffic,strict,mask,
 output reg [95:0] out_rgb, output reg out_valid,out_user,out_last,out_done,
 output reg [2:0] result,frame_result,
 // Frame snapshot shared by the existing status block and downstream text OSD.
 output wire [2:0] O_display_result,output wire O_display_traffic,
 output reg [31:0] red_count,yellow_count,green_count,blue_count,
 output reg error
);
 // IDs: 0 unknown, 1 red, 2 yellow, 3 green, 4 blue.
 reg [11:0] x,y;
 reg started,pending,finish;
 reg [31:0] cr,cy,cg,cb;
 reg [2:0] hist0,hist1,display_result;
 reg [1:0] history_size;
 reg active_traffic,active_strict,active_mask;
 assign O_display_result=display_result;
 assign O_display_traffic=active_traffic;
 wire [11:0] px=early?12'd0:x, py=early?12'd0:y;
 wire mt=early?traffic:active_traffic;
 wire st=early?strict:active_strict;
 wire mm=early?mask:active_mask;
 integer i,xx,nr,ny,ng,nb;
 reg inside_roi,border;
 reg [2:0] c,winner,voted;
 reg [23:0] p,q;
 reg [95:0] painted;
 function [2:0] classify;
 input [23:0] a; input tight;
 reg [8:0] r,g,b; reg [8:0] floor_v,delta;
 begin
 r={1'b0,a[23:16]};g={1'b0,a[15:8]};b={1'b0,a[7:0]};
 floor_v=tight?9'd150:9'd100;delta=tight?9'd50:9'd30;
 classify=0;
 if(r>=floor_v && g>=floor_v && r>b+delta && g>b+delta && r+60>=g && g+60>=r) classify=2;
 else if(r>=floor_v && r>g+delta && r>b+delta) classify=1;
 else if(g>=floor_v && g>r+delta && g>b+delta) classify=3;
 else if(b>=floor_v && b>r+delta && b>g+delta) classify=4;
 end endfunction
 function [23:0] palette;
 input [2:0] id;
 begin case(id)
 1:palette=24'hff3030;2:palette=24'hffff00;3:palette=24'h00ff40;
 4:palette=24'h3080ff;default:palette=24'h606060;
 endcase end endfunction
 always @* begin
 nr=0;ny=0;ng=0;nb=0;painted=rgb;c=0;p=0;q=0;xx=0;inside_roi=0;border=0;
 for(i=0;i<4;i=i+1)begin
 xx=px+i;p=rgb[95-i*24 -:24];c=classify(p,st);
 inside_roi=xx>=X0 && xx<X1 && py>=Y0 && py<Y1;
 if(inside_roi)case(c)
 1:nr=nr+1;2:ny=ny+1;3:ng=ng+1;4:nb=nb+1;default:begin end
 endcase
 q=p;
 if(mm) q=inside_roi && c!=0 ? palette(c):24'h000000;
 border=inside_roi && (xx<X0+2 || xx>=X1-2 || py<Y0+2 || py>=Y1-2);
 if(border)q=24'hffffff;
 // Top-left: voted result, mode (cyan=color/orange=traffic), threshold preset.
 if(xx>=16 && xx<80 && py>=16 && py<48)q=palette(display_result);
 if(xx>=88 && xx<112 && py>=16 && py<48)q=active_traffic?24'hff8000:24'h00ffff;
 if(xx>=120 && xx<144 && py>=16 && py<48)q=active_strict?24'hffffff:24'h404040;
 painted[95-i*24 -:24]=q;
 end
 winner=0;
 if(cr>=MIN_PIXELS && cr>cy+DOM_MARGIN && cr>cg+DOM_MARGIN && (active_traffic || cr>cb+DOM_MARGIN))winner=1;
 else if(cy>=MIN_PIXELS && cy>cr+DOM_MARGIN && cy>cg+DOM_MARGIN && (active_traffic || cy>cb+DOM_MARGIN))winner=2;
 else if(cg>=MIN_PIXELS && cg>cr+DOM_MARGIN && cg>cy+DOM_MARGIN && (active_traffic || cg>cb+DOM_MARGIN))winner=3;
 else if(!active_traffic && cb>=MIN_PIXELS && cb>cr+DOM_MARGIN && cb>cy+DOM_MARGIN && cb>cg+DOM_MARGIN)winner=4;
 voted=0;
 if(history_size==2)begin
 if(winner==hist0 || winner==hist1)voted=winner;
 else if(hist0==hist1)voted=hist0;
 end
 end
 always @(posedge clk or negedge rst_n)begin
 if(!rst_n)begin
 x<=0;y<=0;started<=0;pending<=0;finish<=0;cr<=0;cy<=0;cg<=0;cb<=0;
 hist0<=0;hist1<=0;history_size<=0;result<=0;frame_result<=0;display_result<=0;
 active_traffic<=1;active_strict<=0;active_mask<=0;
 out_rgb<=0;out_valid<=0;out_user<=0;out_last<=0;out_done<=0;
 red_count<=0;yellow_count<=0;green_count<=0;blue_count<=0;error<=0;
 end else begin
 out_valid<=0;out_user<=0;out_last<=0;out_done<=0;finish<=0;
 if(finish)begin
 frame_result<=winner;result<=voted;hist1<=hist0;hist0<=winner;
 if(history_size<2)history_size<=history_size+1'b1;
 red_count<=cr;yellow_count<=cy;green_count<=cg;blue_count<=cb;
 end
 if(early)begin
 if(started)error<=1;
 x<=0;y<=0;started<=1;pending<=1;cr<=0;cy<=0;cg<=0;cb<=0;
 active_traffic<=traffic;active_strict<=strict;active_mask<=mask;
 display_result<=result;
 if(traffic!=active_traffic || strict!=active_strict)begin
 hist0<=0;hist1<=0;history_size<=0;result<=0;display_result<=0;
 end
 end
 if(valid && (started || early))begin
 out_rgb<=painted;out_valid<=1;out_user<=pending || early;pending<=0;
 cr<=(early?0:cr)+nr;cy<=(early?0:cy)+ny;cg<=(early?0:cg)+ng;cb<=(early?0:cb)+nb;
 if(px==W-4)begin
 x<=0;out_last<=1;
 if(py==H-1)begin y<=0;out_done<=1;started<=0;finish<=1;end
 else y<=py+1'b1;
 end else x<=px+4;
 end
 end end
endmodule
