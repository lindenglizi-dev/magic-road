`timescale 1ns / 1ps
module tb_ball_rotation_queue;
reg clk=0;always #5 clk=!clk;
reg rstn=0,clear=0,start=0;
reg [11:0] left=0,right=0,top=0,bottom=0;
wire read,done,valid;
wire [12:0] address;
reg [15:0] data=0;
wire [3:0] reason;
wire [15:0] center_x,center_y,marker_x,marker_y;
wire [7:0] median,threshold;
reg [15:0] memory[0:90112-1];
integer selected=0;
always @(posedge clk)begin if(read)data<=memory[selected*8192+address];end
ball_marker_extract #(.C_QUEUE_BITS(1),.C_X_MIN(0),.C_Y_MIN(0),.C_X_END(320),.C_Y_END(288)) dut(
 .i_clk(clk),.i_rstn(rstn),.i_clear(clear),.i_start(start),.i_origin_x(12'd32),.i_origin_y(12'd22),
 .i_left(left),.i_right(right),.i_top(top),.i_bottom(bottom),.i_read_data(data),.o_read(read),.o_read_address(address),
 .o_busy(),.o_done(done),.o_valid(valid),.o_reason(reason),.o_center_x(center_x),.o_center_y(center_y),
 .o_marker_x(marker_x),.o_marker_y(marker_y),.o_median(median),.o_threshold(threshold));
integer handle,rc,timeout,max_cycles=0;
reg expected_valid;
reg [3:0] expected_reason;
reg [15:0] expected_x,expected_y,expected_cx,expected_cy;
reg [7:0] expected_median,expected_threshold;
initial begin
$readmemh("sim/marker_gray.mem",memory);
repeat(4)@(negedge clk);rstn=1;
handle=$fopen("sim/marker_vectors.txt","r");
while(selected<1)begin
 rc=$fscanf(handle,"%h %h %h %h %h %h %h %h %h %h %h %h\n",left,top,right,bottom,expected_valid,expected_reason,
     expected_x,expected_y,expected_cx,expected_cy,expected_median,expected_threshold);
 if(rc==12)begin
  expected_valid=0;expected_reason=8;start=1;@(negedge clk);start=0;timeout=0;
  while(!done && timeout<1000000)begin @(negedge clk);timeout=timeout+1;end
  if(timeout>max_cycles)max_cycles=timeout;
  if(timeout==1000000 || valid!==expected_valid || reason!==expected_reason || center_x!==expected_cx || center_y!==expected_cy ||
     median!==expected_median || threshold!==expected_threshold || (valid && (marker_x!==expected_x || marker_y!==expected_y)))
    $fatal(1,"marker %d got v=%b r=%d m=%d,%d c=%d,%d median=%d th=%d expected v=%b r=%d m=%d,%d c=%d,%d median=%d th=%d state=%d",
       selected,valid,reason,marker_x,marker_y,center_x,center_y,median,threshold,expected_valid,expected_reason,expected_x,expected_y,
       expected_cx,expected_cy,expected_median,expected_threshold,dut.state_current);
  $display("PASS MARKER %d reason=%d cycles=%d",selected,reason,timeout);
  selected=selected+1;@(negedge clk);
 end
end
$display("PASS IMAGE %d max_cycles=%d",selected,max_cycles);$finish;
end
endmodule
