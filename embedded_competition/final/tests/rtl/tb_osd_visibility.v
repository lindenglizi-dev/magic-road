
`timescale 1ns/1ps
module osd_case #(parameter PRE=1,SCALAR=1,COMBINED=1)(output reg done=0);
reg clk=0; always #5 clk=~clk;
reg rstn=0,valid=0,sof=0,eol=0,eof=0,view=1;
reg [3:0] mode=0;
reg [11:0] x=0,y=0;
wire [95:0] dut_rgb,reference_rgb;
wire dut_valid,dut_sof,dut_eol,dut_eof,reference_valid,reference_sof,reference_eol,reference_eof;
ball_status_osd #(.C_COMBINED(COMBINED),.C_VIEW_SWITCH(1),.C_SCALAR_RENDER(SCALAR),.C_PREDECODE(PRE)) dut(.i_application_mode(mode),
.i_clk(clk),
.i_rstn(rstn),
.i_rgb({24'h397ab1,24'hc36924,24'h258769,24'h976abc}),
.i_view_ball(view),
.i_valid(valid),
.i_sof(sof),
.i_eol(eol),
.i_eof(eof),
.i_x(x),
.i_y(y),
.i_count_mode(0),
.i_count_enable(x[5]),
.i_strict(0),
.i_live_count(y[2:0]),
.i_display_white_busy(0),
.i_display_white_ready(0),
.i_display_white_error(0),
.i_face_unlocked(0),
.i_face_busy(0),
.i_face_fault(0),
.i_face_confirmed(0),
.i_camera_status(0),
.i_diag_count(0),
.i_diag_reject(0),
.i_diag_width_bcd(0),
.i_diag_height_bcd(0),
.i_diag_area_bcd(0),
.i_diag_fill_bcd(0),
.i_red_bcd(40'h1234567890),
.i_green_bcd(40'h1234567890),
.i_yellow_bcd(40'h1234567890),
.i_total_bcd(44'h01234567890),
.i_x_bcd(0),
.i_y_bcd(0),
.i_gate_state(0),
.i_track_status(0),
.i_reason(x[2:0]),.o_rgb(dut_rgb),.o_valid(dut_valid),.o_sof(dut_sof),.o_eol(dut_eol),.o_eof(dut_eof));
reference_osd #(.C_COMBINED(COMBINED),.C_VIEW_SWITCH(1),.C_SCALAR_RENDER(SCALAR),.C_PREDECODE(PRE)) reference(.i_application_mode(mode),
.i_clk(clk),
.i_rstn(rstn),
.i_rgb({24'h397ab1,24'hc36924,24'h258769,24'h976abc}),
.i_view_ball(view),
.i_valid(valid),
.i_sof(sof),
.i_eol(eol),
.i_eof(eof),
.i_x(x),
.i_y(y),
.i_count_mode(0),
.i_count_enable(x[5]),
.i_strict(0),
.i_live_count(y[2:0]),
.i_display_white_busy(0),
.i_display_white_ready(0),
.i_display_white_error(0),
.i_face_unlocked(0),
.i_face_busy(0),
.i_face_fault(0),
.i_face_confirmed(0),
.i_camera_status(0),
.i_diag_count(0),
.i_diag_reject(0),
.i_diag_width_bcd(0),
.i_diag_height_bcd(0),
.i_diag_area_bcd(0),
.i_diag_fill_bcd(0),
.i_red_bcd(40'h1234567890),
.i_green_bcd(40'h1234567890),
.i_yellow_bcd(40'h1234567890),
.i_total_bcd(44'h01234567890),
.i_x_bcd(0),
.i_y_bcd(0),
.i_gate_state(0),
.i_track_status(0),
.i_reason(x[2:0]),.o_rgb(reference_rgb),.o_valid(reference_valid),.o_sof(reference_sof),.o_eol(reference_eol),.o_eof(reference_eof));

reg [31:0] golden_font[0:4095];
reg [6:0] golden_ids[0:511];
initial begin $readmemh("old_font.hex",golden_font);$readmemh("old_ids.hex",golden_ids);end
function [23:0] expected_pixel;
input integer px,py,m,ln;
reg [6:0] ch;
reg [31:0] bits;
reg [7:0] logo;
begin
case(ln)0:expected_pixel=24'h397ab1;1:expected_pixel=24'hc36924;2:expected_pixel=24'h258769;3:expected_pixel=24'h976abc;endcase
if(px>=848 && px<1264 && py>=16 && py<96)begin
 expected_pixel=24'h101820;
 if(px>=856 && px<1240 && py>=24 && py<88)begin
  ch=golden_ids[m*32+((py-24)/32)*16+(px-856)/32];
  bits=golden_font[ch*32+(py-24)%32];
  if(bits[31-(px-856)%32])expected_pixel=24'hffe066;
 end
end
if(px>=16 && px<144 && py>=16 && py<96)begin
 logo=reference.rom_logo[(py-16)*32+(px-16)/4];
 expected_pixel=reference.logo_color((logo >> (6-((px-16)%4)*2)) & 3);
end
end endfunction
reg [95:0] expected[0:2];
reg [3:0] markers[0:2];
reg compare_reference[0:2];
integer j,l,checked=0,m,xx,yy;
always @(posedge clk)begin
 if(!rstn)begin for(j=0;j<3;j=j+1)begin markers[j]=0;expected[j]=0;compare_reference[j]=1;end end
 else begin
  for(j=2;j>0;j=j-1)begin expected[j]=expected[j-1];markers[j]=markers[j-1];compare_reference[j]=compare_reference[j-1];end
  expected[0]=0;markers[0]={valid,sof,eol,eof};compare_reference[0]=!COMBINED || mode==10;
  for(l=0;l<(SCALAR?1:4);l=l+1)expected[0][95-l*24 -:24]=expected_pixel(x+l,y,mode,l);
  #1;
  if({dut_valid,dut_sof,dut_eol,dut_eof}!==markers[PRE+1])$fatal(1,"marker latency PRE=%d SCALAR=%d",PRE,SCALAR);
  if(dut_valid)begin
   if(compare_reference[PRE+1])begin
    if(dut_rgb!==reference_rgb)$fatal(1,"ball/standalone changed PRE=%d SCALAR=%d",PRE,SCALAR);
   end else if(dut_rgb!==expected[PRE+1])$fatal(1,"algorithm pixels PRE=%d SCALAR=%d mode=%d x=%d y=%d actual=%h expected=%h",PRE,SCALAR,mode,x,y,dut_rgb,expected[PRE+1]);
   checked=checked+1;
  end
 end
end
initial begin
 repeat(4)@(negedge clk);rstn=1;
 for(m=0;m<27;m=m+1)begin
  for(yy=0;yy<148;yy=yy+1)begin
   for(xx=0;xx<1280;xx=xx+(SCALAR?1:4))begin
    @(negedge clk);mode=(m<22?m%11:((m==24 || m==26)?0:10));view=(m!=23 && m!=25);x=xx;y=yy;valid=1;sof=xx==0 && yy==0;eol=xx==(1280-(SCALAR?1:4));eof=eol && yy==147;
   end
  end
 end
 @(negedge clk);valid=0;sof=0;eol=0;eof=0;
 repeat(5)@(negedge clk);
 $display("PASS OSD PRE=%d SCALAR=%d COMBINED=%d checked=%d",PRE,SCALAR,COMBINED,checked);done=1;
end
endmodule
module tb_osd_visibility;
wire [4:0] done;
osd_case #(.PRE(1),.SCALAR(1)) a(done[0]);
osd_case #(.PRE(0),.SCALAR(1)) b(done[1]);
osd_case #(.PRE(1),.SCALAR(0)) c(done[2]);
osd_case #(.PRE(0),.SCALAR(0)) d(done[3]);
osd_case #(.PRE(1),.SCALAR(1),.COMBINED(0)) e(done[4]);
initial begin wait(&done);$display("PASS ALL OSD MODES AND ORIGINAL BALL/RAW");$finish;end
initial begin #60000000;$fatal(1,"timeout");end
endmodule
