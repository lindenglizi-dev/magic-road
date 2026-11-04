`timescale 1ns / 1ps
module tb_ball_rotation_faults;
reg clk=0;always #5 clk=!clk;
reg rstn=0,clear=0,enable=1,external_fault=0,submit=0;
reg [31:0] frame=0;
reg [15:0] epoch=1,job_epoch=1;
reg [63:0] tick=0;
wire done,angle_valid,rpm_valid,fault;
wire [3:0] reason;
wire [31:0] result_frame;
wire [1:0] banks;
ball_rotation dut(.i_clk(clk),.i_rstn(rstn),.i_clear(clear),.i_fault(external_fault),.i_enable(enable),
 .i_rgb(96'd0),.i_valid(1'b0),.i_sof(1'b0),.i_x(12'd0),.i_y(12'd0),.i_frame(frame),.i_tick(tick),.i_epoch(epoch),
 .i_observation_done(submit),.i_observation_valid(1'b1),.i_observation_new(1'b0),
 .i_observation_frame(frame),.i_observation_tick(tick),.i_observation_epoch(job_epoch),
 .i_left(12'd100),.i_right(12'd219),.i_top(12'd200),.i_bottom(12'd319),
 .i_predict_valid(1'b0),.i_predict_x(12'd0),.i_predict_y(12'd0),
 .o_done(done),.o_frame(result_frame),.o_epoch(),.o_angle_valid(angle_valid),.o_phase(),.o_rpm_valid(rpm_valid),
 .o_rpm(),.o_status(),.o_net(),.o_cw(),.o_ccw(),.o_partial(),.o_saturated(),.o_reason(reason),.o_fault(fault),
 .o_bank_busy(banks),.o_median(),.o_threshold());
integer cycles,index;
task send;
 input [31:0] source;
 begin frame=source;tick=source*1000000;submit=1;@(negedge clk);submit=0;end
endtask
task result;
 input [3:0] expected;
 begin cycles=0;while(!done && cycles<3000)begin @(negedge clk);cycles=cycles+1;end
  if(cycles==3000 || reason!==expected || angle_valid || rpm_valid || fault)$fatal(1,"bad rejected job reason=%d",reason);
  @(negedge clk);
 end
endtask
initial begin
repeat(4)@(negedge clk);rstn=1;
send(1);result(2); // 没有对应灰度帧时不能使用上一帧。
job_epoch=0;send(2);result(4); // 旧配置的框不能进入新会话。
job_epoch=1;
for(index=0;index<9;index=index+1)begin send(3+index);end
repeat(8)@(negedge clk);
if(!fault || reason!==11 || banks!==0)$fatal(1,"FIFO overflow did not fail closed");
clear=1;@(negedge clk);clear=0;repeat(4)@(negedge clk);
if(fault || banks!==0)$fatal(1,"clear failed");
send(20);result(2);
external_fault=1;@(negedge clk);external_fault=0;repeat(4)@(negedge clk);
if(!fault)$fatal(1,"source fault was ignored");
enable=0;repeat(4)@(negedge clk);if(fault || banks!==0)$fatal(1,"disable did not release ownership");
$display("PASS ROTATION FAULTS: missing bank, stale epoch, FIFO overflow, clear, source fault, disable");$finish;
end
endmodule
