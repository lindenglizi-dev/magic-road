`timescale 1ns/1ps
module tb_counter_generic;
reg [0:0] i_clk=0;
reg [0:0] i_rstn=0;
reg [0:0] i_clear=0;
reg [0:0] i_clear_counts=0;
reg [0:0] i_fault=0;
reg [0:0] i_frame_start=0;
reg [0:0] i_candidate_valid=0;
reg [1:0] i_color=0;
reg [11:0] i_x_min=0;
reg [11:0] i_x_max=0;
reg [11:0] i_y_min=0;
reg [11:0] i_y_max=0;
reg [0:0] i_frame_done=0;
reg [0:0] i_overflow=0;
reg [0:0] i_count_enable=0;
reg [191:0] i_settings=0;
reg [0:0] i_good=0;
reg [0:0] i_considered=0;
reg [19:0] i_area=0;
reg [7:0] i_reject_reason=0;
reg [11:0] i_line_low=0;
reg [11:0] i_line_high=0;
wire [31:0] a_o_good,b_o_good;
wire [31:0] a_o_bad,b_o_bad;
wire [3:0] a_o_box_good,b_o_box_good;
wire [3:0] a_o_box_quality_pending,b_o_box_quality_pending;
wire [31:0] a_o_box_reject_reason,b_o_box_reject_reason;
wire [3:0] a_o_box_raw_good,b_o_box_raw_good;
wire [0:0] a_o_done,b_o_done;
wire [0:0] a_o_busy,b_o_busy;
wire [31:0] a_o_red,b_o_red;
wire [31:0] a_o_green,b_o_green;
wire [31:0] a_o_yellow,b_o_yellow;
wire [33:0] a_o_total,b_o_total;
wire [2:0] a_o_state,b_o_state;
wire [2:0] a_o_reason,b_o_reason;
wire [11:0] a_o_center_x,b_o_center_x;
wire [11:0] a_o_center_y,b_o_center_y;
wire [2:0] a_o_active_count,b_o_active_count;
wire [3:0] a_o_box_valid,b_o_box_valid;
wire [7:0] a_o_box_color,b_o_box_color;
wire [3:0] a_o_box_predicted,b_o_box_predicted;
wire [7:0] a_o_identity_color,b_o_identity_color;
wire [47:0] a_o_box_left,b_o_box_left;
wire [47:0] a_o_box_right,b_o_box_right;
wire [47:0] a_o_box_top,b_o_box_top;
wire [47:0] a_o_box_bottom,b_o_box_bottom;
ball_multi_counter #(.C_PANEL_CONFIG(0)) dut_a(.i_clk(i_clk),.i_rstn(i_rstn),.i_clear(i_clear),.i_clear_counts(i_clear_counts),.i_fault(i_fault),.i_frame_start(i_frame_start),.i_candidate_valid(i_candidate_valid),.i_color(i_color),.i_x_min(i_x_min),.i_x_max(i_x_max),.i_y_min(i_y_min),.i_y_max(i_y_max),.i_frame_done(i_frame_done),.i_overflow(i_overflow),.i_count_enable(i_count_enable),.i_settings(i_settings),.i_good(i_good),.i_considered(i_considered),.i_area(i_area),.i_reject_reason(i_reject_reason),.i_line_low(i_line_low),.i_line_high(i_line_high),.o_good(a_o_good),.o_bad(a_o_bad),.o_box_good(a_o_box_good),.o_box_quality_pending(a_o_box_quality_pending),.o_box_reject_reason(a_o_box_reject_reason),.o_box_raw_good(a_o_box_raw_good),.o_done(a_o_done),.o_busy(a_o_busy),.o_red(a_o_red),.o_green(a_o_green),.o_yellow(a_o_yellow),.o_total(a_o_total),.o_state(a_o_state),.o_reason(a_o_reason),.o_center_x(a_o_center_x),.o_center_y(a_o_center_y),.o_active_count(a_o_active_count),.o_box_valid(a_o_box_valid),.o_box_color(a_o_box_color),.o_box_predicted(a_o_box_predicted),.o_identity_color(a_o_identity_color),.o_box_left(a_o_box_left),.o_box_right(a_o_box_right),.o_box_top(a_o_box_top),.o_box_bottom(a_o_box_bottom));
reference_ball_multi_counter #(.C_PANEL_CONFIG(0)) dut_b(.i_clk(i_clk),.i_rstn(i_rstn),.i_clear(i_clear),.i_clear_counts(i_clear_counts),.i_fault(i_fault),.i_frame_start(i_frame_start),.i_candidate_valid(i_candidate_valid),.i_color(i_color),.i_x_min(i_x_min),.i_x_max(i_x_max),.i_y_min(i_y_min),.i_y_max(i_y_max),.i_frame_done(i_frame_done),.i_overflow(i_overflow),.i_count_enable(i_count_enable),.i_settings(i_settings),.i_good(i_good),.i_considered(i_considered),.i_area(i_area),.i_reject_reason(i_reject_reason),.i_line_low(i_line_low),.i_line_high(i_line_high),.o_good(b_o_good),.o_bad(b_o_bad),.o_box_good(b_o_box_good),.o_box_quality_pending(b_o_box_quality_pending),.o_box_reject_reason(b_o_box_reject_reason),.o_box_raw_good(b_o_box_raw_good),.o_done(b_o_done),.o_busy(b_o_busy),.o_red(b_o_red),.o_green(b_o_green),.o_yellow(b_o_yellow),.o_total(b_o_total),.o_state(b_o_state),.o_reason(b_o_reason),.o_center_x(b_o_center_x),.o_center_y(b_o_center_y),.o_active_count(b_o_active_count),.o_box_valid(b_o_box_valid),.o_box_color(b_o_box_color),.o_box_predicted(b_o_box_predicted),.o_identity_color(b_o_identity_color),.o_box_left(b_o_box_left),.o_box_right(b_o_box_right),.o_box_top(b_o_box_top),.o_box_bottom(b_o_box_bottom));
always #5 i_clk=~i_clk;
integer frame,k,clocks=0,checks=0,seed=261026,random_value,center,n,guard;
always @(posedge i_clk)begin
 #1;
 if(i_rstn)begin
  checks=checks+1;
  if(dut_a.wire_collect_slot!==dut_b.wire_collect_slot)$fatal(1,"candidate slot differs");
  if(dut_a.flag_replace_larger!==dut_b.flag_replace_larger)$fatal(1,"strict minimum-area replacement differs");
  if({a_o_good,a_o_bad,a_o_box_good,a_o_box_quality_pending,a_o_box_reject_reason,a_o_box_raw_good,a_o_done,a_o_busy,a_o_red,a_o_green,a_o_yellow,a_o_total,a_o_state,a_o_reason,a_o_center_x,a_o_center_y,a_o_active_count,a_o_box_valid,a_o_box_color,a_o_box_predicted,a_o_identity_color,a_o_box_left,a_o_box_right,a_o_box_top,a_o_box_bottom} !== {b_o_good,b_o_bad,b_o_box_good,b_o_box_quality_pending,b_o_box_reject_reason,b_o_box_raw_good,b_o_done,b_o_busy,b_o_red,b_o_green,b_o_yellow,b_o_total,b_o_state,b_o_reason,b_o_center_x,b_o_center_y,b_o_active_count,b_o_box_valid,b_o_box_color,b_o_box_predicted,b_o_identity_color,b_o_box_left,b_o_box_right,b_o_box_top,b_o_box_bottom})$fatal(1,"counter port mismatch frame=%0d cycle=%0d state=%0d",frame,clocks,dut_a.state_current);
 end
 clocks=clocks+1;
end
initial begin
 i_settings[47:32]=64;i_settings[63:48]=160;i_settings[79:64]=1216;i_settings[95:80]=640;
 i_line_low=624;i_line_high=656;i_count_enable=1;i_area=8000;
 repeat(5)@(negedge i_clk);i_rstn=1;
 for(frame=0;frame<1600;frame=frame+1)begin
  if(frame%53==0)begin i_clear=1;i_clear_counts=frame%106==0;@(negedge i_clk);i_clear=0;i_clear_counts=0;end
  if(frame%17==0)i_count_enable=!i_count_enable;
  i_frame_start=1;@(negedge i_clk);i_frame_start=0;
  center=250+(frame%35)*22;n=frame%11==0?0:(frame%13==0?8:4);
  for(k=0;k<n;k=k+1)begin
   random_value=$random(seed);i_color=1+(k%3);
   i_x_min=center+(k%2)*6;i_x_max=i_x_min+48+(k%3)*4;
   i_y_min=180+(k%4)*100;i_y_max=i_y_min+60;
   i_good=(random_value&7)!=0;i_considered=(random_value&15)!=0;
   i_reject_reason=i_good?0:8'h28;i_area=frame%7==0 ? 2000 : frame%7==1 ? (1<<20)-1 : 2000+(random_value&8191);
   i_candidate_valid=1;@(negedge i_clk);i_candidate_valid=0;
   if(frame%3!=0)repeat(k%3)@(negedge i_clk);
  end
  i_overflow=frame%41==0;i_frame_done=1;@(negedge i_clk);i_frame_done=0;i_overflow=0;
  guard=0;
  while(!a_o_done && guard<2500)begin
   @(negedge i_clk);guard=guard+1;
   i_fault=frame%37==0 && guard==5;
   if(frame%29==0 && guard==9)i_count_enable=0;
  end
  i_fault=0;
  if(!a_o_done)$fatal(1,"counter timeout");
  repeat(3)@(negedge i_clk);
 end
 $display("PASS_COUNTER_EQUIVALENCE frames=%0d all_outputs_cycles=%0d; ties, capacity, qualities, faults, clear, pause, predictions",frame,checks);$finish;
end
initial begin #100000000;$fatal(1,"watchdog");end
endmodule
