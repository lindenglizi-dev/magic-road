`timescale 1ns / 1ps
module tb_ball_rotation_numeric;
reg clk=0; always #5 clk=!clk;
reg rstn=0,clear=0,start=0,valid=0,new_target=0;
reg [15:0] phase=0,dx=0,dy=0;
reg [63:0] tick=0;
wire meter_done,meter_rpm_valid,meter_angle_valid,meter_partial,meter_fault;
wire [23:0] rpm;
wire [2:0] status;
wire [47:0] net;
wire [31:0] cw,ccw;
ball_rotation_meter meter_Inst(.i_clk(clk),.i_rstn(rstn),.i_clear(clear),.i_fault(1'b0),
 .i_start(start),.i_valid(valid),.i_new_target(new_target),.i_phase(phase),.i_tick(tick),
 .o_busy(),.o_done(meter_done),.o_angle_valid(meter_angle_valid),.o_phase(),.o_rpm_valid(meter_rpm_valid),
 .o_rpm(rpm),.o_status(status),.o_net(net),.o_cw(cw),.o_ccw(ccw),.o_partial(meter_partial),.o_saturated(),.o_fault(meter_fault));
reg angle_start=0;
wire angle_done,angle_valid;
wire [15:0] angle_phase;
ball_rotation_angle angle_Inst(.i_clk(clk),.i_rstn(rstn),.i_clear(clear),.i_start(angle_start),
 .i_dx(dx),.i_dy(dy),.o_busy(),.o_done(angle_done),.o_valid(angle_valid),.o_phase(angle_phase));
reg math_start=0,divide=0,rounded=0;
reg [95:0] left=0,right=0;
wire math_done,math_error;
wire [95:0] product;
ball_rotation_arithmetic arithmetic_Inst(.i_clk(clk),.i_rstn(rstn),.i_clear(clear),.i_start(math_start),
 .i_divide(divide),.i_round(rounded),.i_left(left),.i_right(right),.o_busy(),.o_done(math_done),.o_error(math_error),.o_result(product));
integer handle,rc,count,timeout;
reg expected_valid,expected_partial,expected_error;
reg [15:0] expected_angle;
reg [95:0] expected_product;
reg expected_rpm_valid;
reg [23:0] expected_rpm;
reg [2:0] expected_status;
reg [47:0] expected_net;
reg [31:0] expected_cw,expected_ccw;
initial begin
repeat(4)@(negedge clk);rstn=1;
handle=$fopen("sim/angle_vectors.txt","r");count=0;
while(!$feof(handle))begin
 rc=$fscanf(handle,"%h %h %h %h\n",dx,dy,expected_angle,expected_valid);
 if(rc==4)begin
  angle_start=1;@(negedge clk);angle_start=0;timeout=0;
  while(!angle_done && timeout<100)begin @(negedge clk);timeout=timeout+1;end
  if(timeout==100 || angle_valid!==expected_valid || (angle_valid && angle_phase!==expected_angle))
   $fatal(1,"angle vector %0d got %h expected %h",count,angle_phase,expected_angle);
  count=count+1;@(negedge clk);
 end
end
$fclose(handle);$display("PASS CORDIC %0d",count);
handle=$fopen("sim/arithmetic_vectors.txt","r");count=0;
while(!$feof(handle))begin
 rc=$fscanf(handle,"%h %h %h %h %h %h\n",divide,rounded,left,right,expected_product,expected_error);
 if(rc==6)begin
  math_start=1;@(negedge clk);math_start=0;timeout=0;
  while(!math_done && timeout<110)begin @(negedge clk);timeout=timeout+1;end
  if(timeout==110 || math_error!==expected_error || product!==expected_product)
   $fatal(1,"arithmetic vector %0d got %h expected %h",count,product,expected_product);
  count=count+1;@(negedge clk);
 end
end
$fclose(handle);$display("PASS ARITHMETIC %0d",count);
handle=$fopen("sim/meter_vectors.txt","r");count=0;
while(!$feof(handle))begin
 rc=$fscanf(handle,"%h %h %h %h %h %h %h %h %h %h %h\n",new_target,valid,phase,tick,expected_rpm_valid,expected_rpm,
             expected_status,expected_net,expected_cw,expected_ccw,expected_partial);
 if(rc==11)begin
  start=1;@(negedge clk);start=0;timeout=0;
  while(!meter_done && timeout<15000)begin @(negedge clk);timeout=timeout+1;end
  if(timeout==15000 || meter_fault || meter_angle_valid!==valid || meter_rpm_valid!==expected_rpm_valid ||
    (meter_rpm_valid && rpm!==expected_rpm) || status!==expected_status || net!==expected_net ||
    cw!==expected_cw || ccw!==expected_ccw || meter_partial!==expected_partial)
   $fatal(1,"meter vector %0d got rpm=%h/%b state=%d net=%h cw=%d ccw=%d part=%b expected rpm=%h/%b state=%d net=%h cw=%d ccw=%d part=%b",
      count,rpm,meter_rpm_valid,status,net,cw,ccw,meter_partial,expected_rpm,expected_rpm_valid,expected_status,expected_net,expected_cw,expected_ccw,expected_partial);
  count=count+1;@(negedge clk);
 end
end
$fclose(handle);$display("PASS METER %0d",count);$finish;
end
endmodule
