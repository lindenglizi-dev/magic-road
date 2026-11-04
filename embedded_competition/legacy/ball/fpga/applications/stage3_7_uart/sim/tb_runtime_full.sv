`timescale 1ns/1ps
module tb_runtime_full;
 parameter W=1280,H=720;
 localparam GROUPS=W*H/4,WORDS=W*H*3/16;
 reg clk=0;always #5 clk=~clk;
 reg rst=0;reg [3:0] keys=15;reg [95:0] rgb=0;reg v=0,u=0,l=0;
 wire [127:0] data;wire ov,ol,od,early,err;wire [3:0] mode;
 stage3_7_runtime #(.IMG_WIDTH(W),.IMG_HEIGHT(H),.DEBOUNCE_CYCLES(4)) dut
 (.I_clk(clk),.I_rst_n(rst),.I_roi_config(96'd0),.I_keys_n(keys),.I_uart_valid(1'b0),.I_uart_mode(4'd10),.I_rgb(rgb),.I_valid(v),.I_user(u),.I_last(l),
 .O_data(data),.O_valid(ov),.O_last(ol),.O_done(od),.O_early(early),.O_error(err),.active_mode(mode));
 reg [95:0] source[0:GROUPS-1];reg [127:0] expected[0:WORDS*11-1];
 integer m=10,count=0,frames=0,i,capture;reg checking=0;
 always @(posedge clk)begin
 #1;
 if(rst)begin
 if(early!==u)$fatal(1,"early frame notice mismatch");
 if(err)$fatal(1,"protocol or pack error");
 if(ov)begin
 if(!checking)$fatal(1,"unexpected output");
 if(data!==expected[m*WORDS+count])$fatal(1,"pixel mismatch mode=%0d word=%0d got=%h expected=%h",m,count,data,expected[m*WORDS+count]);
 if(ol!==((count%(W*3/16))==W*3/16-1))$fatal(1,"line marker");
 if(od!==(count==WORDS-1))$fatal(1,"done marker");
 if(W==640)$fdisplay(capture,"%032h",data);
 count=count+1;
 if(od)frames=frames+1;
 end end end
 task ticks(input integer n);repeat(n)@(negedge clk);endtask
 task press(input integer k);
 begin keys[k]=0;ticks(15);keys[k]=1;ticks(15);end endtask
 initial begin
 $readmemh("input.hex",source);$readmemh("expected.hex",expected);
 ticks(5);rst=1;ticks(5);
 if(W==640)capture=$fopen("captured.hex","w");
 if(mode!=10||dut.requested_mode!=10)$fatal(1,"startup must be original");
 press(0);press(1);press(2);
 if(dut.requested_mode!=10)$fatal(1,"locked keys changed mode");
 keys[3]=0;ticks(1);keys[3]=1;ticks(10);
 if(dut.requested_mode!=10)$fatal(1,"KEY3 bounce unlocked");
 // Original frame: locked keys stay disabled; KEY3 unlocks during frame.
 send_frame(10);
 if(dut.requested_mode!=0)$fatal(1,"KEY3 did not unlock into gray");
 press(0);press(1);press(2);
 if(dut.requested_mode!=0||mode!=10)$fatal(1,"keys unlocked before gray frame commit");
 for(m=0;m<10;m=m+1)send_frame(m);
 // Return from an algorithm to original; a long KEY3 hold toggles exactly once.
 keys[3]=0;ticks(50);keys[3]=1;ticks(15);
 if(dut.requested_mode!=10)$fatal(1,"KEY3 return/hold");
 press(0);press(1);press(2);
 if(dut.requested_mode!=10)$fatal(1,"pending color return was overridden");
 send_frame(10); // Its midframe KEY3 press must re-enter gray on the next frame.
 if(dut.requested_mode!=0)$fatal(1,"KEY3 reentry from original");
 send_frame(0);
 if(frames!=13)$fatal(1,"frame count");
 if(W==640)$fclose(capture);
 rst=0;ticks(3);rst=1;ticks(3);
 if(mode!=10||dut.requested_mode!=10)$fatal(1,"reset must relock original");
 $display("PASS runtime original+ten modes, KEY3 roundtrip/relock, bilingual labels+PNG logo, 13 golden frames and DDR packing %0dx%0d",W,H);$finish;
 end
 task send_frame(input integer selected_mode);
 begin
 m=selected_mode;
 count=0;checking=1;u=1;ticks(1);u=0;ticks(20);
 if(mode!=m)$fatal(1,"frame mode latch");
 for(i=0;i<GROUPS;i=i+1)begin
 rgb=source[i];v=1;ticks(1);v=0;
 // Request next mode during current frame; current frame must remain intact.
 if(i==GROUPS/3&&m==10)begin
 press(0);press(1);press(2);
 if(dut.requested_mode!=10)$fatal(1,"locked keys changed active frame request");end
 if(i==GROUPS/2)begin
 if(m==10)begin press(3);press(1);if(dut.requested_mode!=0)$fatal(1,"pending gray skipped");end
 else if(m==0)begin
 keys[1]=0;ticks(50);if(dut.requested_mode!=1)$fatal(1,"hold repeats");keys=15;ticks(10);
 press(2);if(dut.requested_mode!=0)$fatal(1,"gray home");
 press(0);if(dut.requested_mode!=9)$fatal(1,"wrap previous");
 press(1);if(dut.requested_mode!=0)$fatal(1,"wrap next");
 press(1);
 end else press(1);
 end
 if(i%(W/4)==W/4-1)begin l=1;ticks(6);l=0;end
 else if(i%7==2)ticks(2);
 if(mode!=m)$fatal(1,"midframe switch");
 end
 ticks(W*3+200);
 if(count!=WORDS)$fatal(1,"frame size mode=%0d got=%0d",m,count);
 if(dut.busy)$fatal(1,"branch drain incomplete");
 checking=0;
 end endtask
 initial begin #200000000;$fatal(1,"timeout");end
endmodule


