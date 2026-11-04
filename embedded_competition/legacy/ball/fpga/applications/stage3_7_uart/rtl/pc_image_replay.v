// Native 1080P remains in DDR. Existing 720P graph receives x/y samples
// 0,1,3,4,... (nearest-neighbour 3:2 reduction), no host-side algorithm.
// The processing clock remains the existing CSI clock; camera clock required.
module pc_image_replay #(parameter IN_W=1920,IN_H=1080,OUT_W=1280,OUT_H=720,
 parameter BASE0=25165824,BASE1=27239424,FRAME_GAP=10000000)(
 input clk,rst_n,input selected,runtime_busy,input publish,publish_bank,
 output reg publish_ack,output reg image_valid,output reg in_frame,
 output reg mem_start,output reg [24:0] mem_address,input mem_busy,mem_done,input [127:0] mem_result,
 output reg [95:0] rgb,output reg valid,early,last);
 (* ASYNC_REG="TRUE" *) reg pm,ps;
 reg bank;reg [3:0] state;reg [31:0] gap;
 reg [11:0] x,y,ox,oy;reg [1:0] xm,ym,lane;reg [2:0] pixel;
 reg [127:0] word_data;reg [95:0] pack;reg [7:0] prefix;
 wire [15:0] value=word_data[15:0];
 wire [23:0] expanded={value[15:11],value[15:13],value[10:5],value[10:9],value[4:0],value[4:2]};
 wire keep=IN_W==OUT_W||xm!=2;
 always @(posedge clk or negedge rst_n)begin
 if(!rst_n)begin pm<=0;ps<=0;publish_ack<=0;image_valid<=0;bank<=0;in_frame<=0;
 state<=0;gap<=0;x<=0;y<=0;ox<=0;oy<=0;xm<=0;ym<=0;lane<=0;pixel<=0;word_data<=0;pack<=0;prefix<=0;
 mem_start<=0;mem_address<=0;rgb<=0;valid<=0;early<=0;last<=0;end
 else begin
 pm<=publish;ps<=pm;valid<=0;early<=0;last<=0;mem_start<=0;
 case(state)
 0:begin
 if(ps!=publish_ack&&!runtime_busy)begin bank<=publish_bank;publish_ack<=ps;image_valid<=1;gap<=0;end
 else if(selected&&image_valid&&!runtime_busy)begin
 if(gap!=0)gap<=gap-1'b1;
 else begin in_frame<=1;early<=1;prefix<=64;x<=0;y<=0;ox<=0;oy<=0;xm<=0;ym<=0;lane<=0;pack<=0;
 mem_address<=bank?BASE1:BASE0;state<=1;end
 end end
 1:if(prefix!=0)prefix<=prefix-1'b1;else state<=2;
 2:if(!mem_busy)begin mem_start<=1;state<=3;end
 3:if(mem_done)begin word_data<=mem_result;pixel<=0;state<=4;end
 4:begin
 word_data<=word_data>>16;pixel<=pixel+1'b1;x<=x+1'b1;xm<=xm==2?0:xm+1'b1;
 if(keep)begin
 pack<={pack[71:0],expanded};lane<=lane+1'b1;ox<=ox+1'b1;
 if(lane==3)begin rgb<={pack[71:0],expanded};valid<=1;last<=ox==OUT_W-1;end
 end
 if(pixel==7)begin
 mem_address<=mem_address+8;state<=2;
 if(x==IN_W-1)begin
 x<=0;xm<=0;ox<=0;oy<=oy+1'b1;y<=y+1'b1;ym<=ym==2?0:ym+1'b1;
 // Skip every third input row when reducing 1080 to720.
 if(IN_H!=OUT_H&&ym==1)begin mem_address<=mem_address+8+IN_W; y<=y+2;ym<=0;end
 if(oy==OUT_H-1)state<=5;
 end
 end end
 5:if(!runtime_busy)begin in_frame<=0;gap<=FRAME_GAP;state<=0;end
 default:state<=0;
 endcase
 end end
endmodule

// Source switches only between complete processed frames. Camera is re-armed
// at its next early marker so returning from PC never starts halfway in a frame.
module image_source_mux(
 input clk,rst_n,input target,runtime_busy,pc_in_frame,
 input [95:0] camera_rgb,pc_rgb,input camera_valid,camera_early,camera_last,pc_valid,pc_early,pc_last,
 output reg source,output [95:0] rgb,output valid,early,last);
 reg camera_armed;
 always @(posedge clk or negedge rst_n)begin
 if(!rst_n)begin source<=0;camera_armed<=0;end else begin
 if(target!=source&&!runtime_busy&&!pc_in_frame)begin source<=target;camera_armed<=0;end
 else if(!source&&camera_early&&!runtime_busy)camera_armed<=1;
 end end
 wire switching=target!=source&&!runtime_busy&&!pc_in_frame;
 assign rgb=source?pc_rgb:camera_rgb;
 assign early=!switching&&(source?pc_early:camera_early&&!runtime_busy);
 assign valid=!switching&&(source?pc_valid:camera_valid&&(camera_armed||(camera_early&&!runtime_busy)));
 assign last=source?pc_last:camera_last;
endmodule
