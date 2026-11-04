`timescale 1ns / 1ps
module tb_ball_rotation_runtime;
reg clk=0;always #20 clk=!clk;
reg rstn=0,user=0,valid=0;
reg [3:0] keys=15;
reg [95:0] rgb=0;
wire [127:0] data;
wire out_valid,last,done,early,error,mode;
wire [31:0] red,green,yellow;
wire [33:0] total;
ball_runtime #(.C_FACE_GATE(0),.C_ROTATION_ENABLE(1),.C_ROTATION_CLOCK_HZ(25000000),.C_WIDTH(320),.C_HEIGHT(288),
 .C_X_MIN(0),.C_Y_MIN(0),.C_X_END(320),.C_Y_END(288),.C_GATE_MIN(128),.C_GATE_END(192),.C_LINE(160),.C_HYST(8),
 .C_MAX_SIZE(192),.C_DEBOUNCE(3)) dut(
 .I_clk(clk),.I_rst_n(rstn),.I_keys_n(keys),.I_camera_status(48'd0),.I_rgb(rgb),.I_valid(valid),.I_user(user),.I_last(1'b0),
 .O_data(data),.O_valid(out_valid),.O_last(last),.O_done(done),.O_early(early),.O_error(error),
 .O_red(red),.O_green(green),.O_yellow(yellow),.O_total(total),.O_count_mode(mode),.O_gate_state(),.O_track_status(),.O_camera_step());
reg [95:0] pixels[0:184319];
integer frame,row,col,index,cycle=0,start_cycle,words=0,lines=0,frames=0,starts=0,nbytes=0,rotations=0,log;
reg [255:0] queue=0;
reg [127:0] expected_data;
reg [159:0] previous_snapshot=0;
reg expected_early,allow_change;
wire [159:0] display_snapshot={dut.reg_rotation_display_rpm_bcd,dut.reg_rotation_display_angle_bcd,
 dut.reg_rotation_display_net_bcd,dut.reg_rotation_display_cw_bcd,dut.reg_rotation_display_ccw_bcd,
 dut.reg_rotation_display_status,dut.reg_rotation_display_reason,dut.flag_rotation_display_angle,dut.flag_rotation_display_rpm,
 dut.flag_rotation_display_partial,dut.flag_rotation_display_negative};
always @(posedge clk)begin
 cycle=cycle+1;expected_early=user;
 allow_change=user || dut.clear_history || !dut.ball_enabled || mode;
 if(dut.osd_valid)begin
  queue=(queue<<96)|dut.osd_rgb;nbytes=nbytes+12;if(dut.osd_sof)starts=starts+1;
 end
 if(dut.rotation_done)begin
  rotations=rotations+1;
  $fwrite(log,"%0d %0d %0d %0d %h %0d %h %0d %h %0d %0d %0d %0d %0d\n",dut.rotation_frame,dut.rotation_epoch,
    dut.gen_rotation.rotation_Inst.meter_Inst.reg_input_tick,dut.rotation_angle_valid,dut.rotation_phase,dut.rotation_rpm_valid,dut.rotation_rpm,
    dut.rotation_status,dut.rotation_net,dut.rotation_cw,dut.rotation_ccw,dut.rotation_partial,dut.rotation_reason,
    dut.gen_rotation.rotation_Inst.flag_job_new);
 end
 #1;
 if(rstn && early!==expected_early)$fatal(1,"early latency changed");
 if(rstn && !allow_change && display_snapshot!==previous_snapshot)$fatal(1,"rotation OSD changed inside source frame");
 previous_snapshot=display_snapshot;
 if(out_valid)begin
  expected_data=queue >> ((nbytes-16)*8);
  if(nbytes<16 || data!==expected_data)$fatal(1,"video packing changed");
  nbytes=nbytes-16;queue=queue&((256'b1<<(nbytes*8))-1);words=words+1;
  if(last)lines=lines+1;if(done)frames=frames+1;
 end
 if(rstn && (error || dut.rotation_fault))$fatal(1,"runtime fault");
end
task tap;
 input integer key;
 begin keys[key]=0;repeat(12)@(negedge clk);keys=15;repeat(12)@(negedge clk);end
endtask
initial begin
$readmemh("sim/runtime_rotation_rgb.mem",pixels);log=$fopen("reports/runtime_rotation_trace.txt","w");
repeat(4)@(negedge clk);rstn=1;
for(frame=0;frame<8;frame=frame+1)begin
 if(frame==5)tap(3);
 if(frame==7)tap(0);
 start_cycle=cycle;user=1;@(negedge clk);user=0;repeat(8)@(negedge clk);
 for(row=0;row<288;row=row+1)begin
  for(col=0;col<80;col=col+1)begin
   rgb=pixels[frame*23040+row*80+col];valid=1;@(negedge clk);
   if(col==13)begin valid=0;repeat(2)@(negedge clk);end
  end
  valid=0;repeat(3)@(negedge clk);
 end
 valid=0;
 if(frame<7)begin
  while(rotations<frame+1)@(negedge clk);
 end
 repeat(200)@(negedge clk);
 $display("FRAME %0d completed at cycle %0d",frame,cycle);$fflush();$fflush(log);
 if(frame==2 && !dut.flag_rotation_display_angle)$fatal(1,"angle not published");
 if(frame==7 && (!mode || dut.gen_rotation.rotation_Inst.o_bank_busy!==0 || dut.reg_rotation_display_rpm_bcd!==0))$fatal(1,"count mode did not disable rotation");
end
$fclose(log);
if(rotations!=7 || words!=8*17280 || lines!=8*288 || frames!=8 || starts!=8 || nbytes!=0)
 $fatal(1,"totals rotation%0d words%0d lines%0d frames%0d starts%0d",rotations,words,lines,frames,starts);
$display("PASS ROTATION RUNTIME: 8 RGB frames, 7 ordered measurements, clear, mode change, frozen OSD and packed bytes");$finish;
end
initial begin #600000000;$fatal(1,"runtime rotation timeout");end
endmodule
