"""Generate point transforms with an exact 256-entry gamma=0.7 LUT."""
from pathlib import Path
ROOT=Path(__file__).resolve().parent
s='''// Two-cycle RGB transforms. Defaults are compile-time presets, not UART parameters.
module rgb_point_adjust_4px #(parameter integer BINARY_THRESHOLD=128,BRIGHTNESS=32)(
 input wire clk,rst_n,input wire [95:0] rgb,input wire [31:0] gray,
 input wire valid,user_mark,last_mark,done,
 output wire [95:0] binary_rgb,gamma_rgb,contrast_rgb,brightness_rgb,saturation_rgb,
 output wire [31:0] binary_gray,output wire ov,ou,ol,od);
 reg [3:0] flags0,flags1;
 always @(posedge clk or negedge rst_n)
 if(!rst_n)begin flags0<=0;flags1<=0;end
 else begin flags0<={valid,user_mark,last_mark,done};flags1<=flags0;end
 assign {ov,ou,ol,od}=flags1;
 function [7:0] clip;input signed [11:0] value;
 begin if(value<0)clip=0;else if(value>255)clip=255;else clip=value[7:0];end endfunction
 function [7:0] gamma_value;input [7:0] value;
 begin case(value)
'''
for i in range(256):s+=f"8'd{i}:gamma_value=8'd{int(255*(i/255)**0.7+0.5)};\n"
s+='''endcase end endfunction
 genvar lane,channel;
 generate for(lane=0;lane<4;lane=lane+1)begin:pixel
 reg bin0,bin1;
 always @(posedge clk or negedge rst_n)
 if(!rst_n)begin bin0<=0;bin1<=0;end else begin bin0<=gray[lane*8+:8]>=BINARY_THRESHOLD;bin1<=bin0;end
 assign binary_gray[lane*8+:8]={8{bin1}};
 assign binary_rgb[lane*24+:24]={24{bin1}};
 for(channel=0;channel<3;channel=channel+1)begin:component
 wire [7:0] c=rgb[lane*24+channel*8+:8];
 wire signed [11:0] cv=$signed({4'b0,c}),yv=$signed({4'b0,gray[lane*8+:8]});
 reg signed [11:0] contrast0,brightness0,saturation0;
 reg [7:0] gamma0,gamma1,contrast1,brightness1,saturation1;
 always @(posedge clk or negedge rst_n)begin
 if(!rst_n)begin contrast0<=0;brightness0<=0;saturation0<=0;gamma0<=0;gamma1<=0;contrast1<=0;brightness1<=0;saturation1<=0;end
 else begin
 gamma0<=gamma_value(c);gamma1<=gamma0;
 // contrast: 128 + 1.25*(C-128); saturation: Y + 1.5*(C-Y).
 contrast0<=((cv<<<2)+cv-12'sd128)>>>2;
 brightness0<=cv+BRIGHTNESS;
 saturation0<=((cv<<<1)+cv-yv)>>>1;
 contrast1<=clip(contrast0);brightness1<=clip(brightness0);saturation1<=clip(saturation0);
 end end
 assign gamma_rgb[lane*24+channel*8+:8]=gamma1;
 assign contrast_rgb[lane*24+channel*8+:8]=contrast1;
 assign brightness_rgb[lane*24+channel*8+:8]=brightness1;
 assign saturation_rgb[lane*24+channel*8+:8]=saturation1;
 end end endgenerate
endmodule
'''
(ROOT/'rtl/rgb_point_adjust_4px.v').write_text(s,encoding='utf-8')
print('Generated RGB point transforms: binary, gamma, contrast, brightness, saturation')
