                                                               
                                                                                       
module combined_tone_4px #(
 parameter CURVE_FILE="../rtl/combined_curves.mem"
)(
 input clk,rst_n,input [3:0] mode,
 input [95:0] rgb,input [31:0] gray,input valid,user_mark,last_mark,done,
 input [9:0] contrast_q8,edit_saturation,input signed [8:0] brightness,
 input gamma_we,editor_we,input [7:0] curve_address,curve_value,
 input gamma_commit,editor_commit,
 output [95:0] gamma_rgb,contrast_rgb,brightness_rgb,editor_rgb,
 output ov,ou,ol,od,ev,eu,el,ed
);
 reg gamma_bank,editor_bank,gamma_ready,editor_ready;
 reg [3:0] marks0,marks1,marks2,marks3;
 always @(posedge clk or negedge rst_n)begin
  if(!rst_n)begin
   gamma_bank<=0;editor_bank<=0;gamma_ready<=0;editor_ready<=0;
   marks0<=0;marks1<=0;marks2<=0;marks3<=0;
  end else begin
   if(gamma_commit)begin gamma_bank<=~gamma_bank;gamma_ready<=1;end
   if(editor_commit)begin editor_bank<=~editor_bank;editor_ready<=1;end
   marks0<={valid,user_mark,last_mark,done};marks1<=marks0;
   marks2<=marks1;marks3<=marks2;
  end
 end
 assign {ov,ou,ol,od}=marks1;
 assign {ev,eu,el,ed}=marks3;
                                                                       
                                                                               
 wire [2:0] read_page=mode==10?3'd0:(mode==9?(editor_bank?3'd4:3'd3):(gamma_bank?3'd2:3'd1));
 wire [2:0] write_page=editor_we?(editor_bank?3'd3:3'd4):(gamma_bank?3'd1:3'd2);
 genvar ch;
 generate for(ch=0;ch<12;ch=ch+1)begin:component
  reg [7:0] lut[0:2047];
  initial $readmemh(CURVE_FILE,lut);
  reg [7:0] lookup,raw0,gamma1,contrast1,brightness1,editor1,edit_raw;
  reg signed [19:0] product0;
  reg signed [10:0] bright0;
  wire [7:0] y=gray[(ch/3)*8+:8];
  wire signed [9:0] centered=mode==9?
   ($signed({2'b0,rgb[ch*8+:8]})-$signed({2'b0,y})):
   ($signed({2'b0,rgb[ch*8+:8]})-10'sd128);
  wire signed [10:0] coefficient=$signed({1'b0,(mode==9?edit_saturation:contrast_q8)});
  wire signed [19:0] base=mode==9?$signed({4'd0,y,8'd0}):20'sd32768;
  wire [7:0] read_byte=mode==9?contrast1:rgb[ch*8+:8];
  function [7:0] clip;
   input signed [19:0] value;
   begin if(value<0)clip=0;else if(value>255)clip=255;else clip=value[7:0];end
  endfunction
                                                                        
  always @(posedge clk)begin
   if(gamma_we || editor_we)lut[{write_page,curve_address}]<=curve_value;
   lookup<=lut[{read_page,read_byte}];
   edit_raw<=contrast1;
  end
  always @(posedge clk or negedge rst_n)begin
   if(!rst_n)begin
    raw0<=0;product0<=0;bright0<=0;gamma1<=0;contrast1<=0;brightness1<=0;editor1<=0;
   end else begin
    raw0<=rgb[ch*8+:8];
    product0<=centered*coefficient+base;
    bright0<=$signed({3'b0,rgb[ch*8+:8]})+brightness;
    gamma1<=(mode==10 || gamma_ready)?lookup:raw0;
    contrast1<=clip(product0>>>8);
    brightness1<=clip({{9{bright0[10]}},bright0});
    editor1<=editor_ready?lookup:edit_raw;
   end
  end
  assign gamma_rgb[ch*8+:8]=gamma1;
  assign contrast_rgb[ch*8+:8]=contrast1;
  assign brightness_rgb[ch*8+:8]=brightness1;
  assign editor_rgb[ch*8+:8]=editor1;
 end endgenerate
endmodule
