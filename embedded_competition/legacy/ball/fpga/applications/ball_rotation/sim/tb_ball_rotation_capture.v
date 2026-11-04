`timescale 1ns / 1ps
module tb_ball_rotation_capture;
reg clk=0;always #5 clk=!clk;
reg rstn=0,clear=0,valid=0,sof=0,read=0,bank=0;
reg [95:0] rgb=0;
reg [11:0] x=0,y=0;
reg [31:0] frame=0;
reg [1:0] release_bank=0;
reg [12:0] address=0;
wire [15:0] data;
wire [1:0] busy,ready;
wire overrun;
reg [95:0] pixels[0:23039];
reg [15:0] expected[0:8191];
integer row,col,index,overruns=0;
always @(posedge clk)begin if(overrun)overruns=overruns+1;end
ball_rotation_capture dut(.i_clk(clk),.i_rstn(rstn),.i_clear(clear),.i_enable(1'b1),.i_rgb(rgb),.i_valid(valid),.i_sof(sof),
 .i_x(x),.i_y(y),.i_frame(frame),.i_tick(64'd100),.i_epoch(16'd3),.i_window_valid(1'b1),.i_window_x(12'd32),.i_window_y(12'd22),
 .i_release(release_bank),.i_read(read),.i_read_bank(bank),.i_read_address(address),.o_read_data(data),.o_busy(busy),.o_ready(ready),
 .o_frames(),.o_ticks(),.o_epochs(),.o_origins_x(),.o_origins_y(),.o_overrun(overrun));
task send_frame;
 input [31:0] source;
 begin
 frame=source;
 for(row=0;row<288;row=row+1)begin
  for(col=0;col<80;col=col+1)begin
   x=col*4;y=row;rgb=pixels[row*80+col];valid=1;sof=row==0 && col==0;
   @(negedge clk);sof=0;
   if(col==13)begin valid=0;repeat(3)@(negedge clk);end
  end
  valid=0;repeat(2)@(negedge clk);
 end
 valid=0;sof=0;repeat(8)@(negedge clk);
 end
endtask
task check_bank;
 input selected;
 begin
 bank=selected;
 for(index=0;index<8192;index=index+1)begin
  address=index;read=1;@(negedge clk);
  if(data!==expected[index])$fatal(1,"capture bank%d addr%d got%h expected%h",bank,index,data,expected[index]);
 end
 read=0;
 end
endtask
initial begin
$readmemh("sim/capture_rgb.mem",pixels);$readmemh("sim/capture_expected.mem",expected);
repeat(4)@(negedge clk);rstn=1;send_frame(0);
if(busy!==1 || ready!==1)$fatal(1,"first capture ownership");check_bank(0);
send_frame(1);if(busy!==3 || ready!==3)$fatal(1,"second capture ownership");check_bank(1);
send_frame(2);if(overruns!=1)$fatal(1,"busy overwrite not rejected");check_bank(0);
release_bank=1;@(negedge clk);release_bank=0;send_frame(4);check_bank(0);
clear=1;@(negedge clk);clear=0;if(busy!==0 || ready!==0)$fatal(1,"clear ownership");
$display("PASS CAPTURE 32768 compared words, overrun rejected, clear released");$finish;
end
endmodule
