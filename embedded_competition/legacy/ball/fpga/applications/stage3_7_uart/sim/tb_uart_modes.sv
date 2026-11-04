`timescale 1ns/1ps
module tb_uart_modes;
 parameter W=640,H=112;
 localparam GROUPS=W*H/4,WORDS=W*H*3/16;
 reg sys=0;always #10 sys=~sys;
 reg clk=0;reg clock_enable=1;always #4.83 if(clock_enable)clk=~clk;
 reg rst=0,rx=1;reg [3:0] keys=15;reg [95:0] rgb=0,wb=0;reg v=0,u=0,l=0;
 wire [3:0] request,mode;wire request_valid;
 uart_mode_link link(.sys_clk(sys),.video_clk(clk),.rst_n(rst),.rx(rx),.video_mode(request),.video_valid(request_valid));
 // Use 0.2ms byte timeout here; tb_protocol_v2 separately verifies the real 20ms timer.
 defparam link.u_protocol.TIMEOUT_CYCLES=10000;
 wire [127:0] data;wire ov,ol,od,early,err;
 stage3_7_runtime #(.IMG_WIDTH(W),.IMG_HEIGHT(H),.DEBOUNCE_CYCLES(4)) dut(
 .I_clk(clk),.I_rst_n(rst),.I_roi_config(96'd0),.I_keys_n(keys),.I_uart_valid(request_valid),.I_uart_mode(request),
 .I_rgb(rgb),.I_wb_rgb(wb),.I_valid(v),.I_user(u),.I_last(l),.O_data(data),.O_valid(ov),.O_last(ol),.O_done(od),.O_early(early),.O_error(err),.active_mode(mode));
 reg [95:0] source[0:GROUPS-1],source_wb[0:GROUPS-1];reg [127:0] expected[0:WORDS*12-1];
 integer m=0,count=0,frames=0;reg checking=0;
 always @(posedge clk)begin
 #1;
 if(rst)begin
 if(err)$fatal(1,"runtime error");
 if(checking && mode!==m)$fatal(1,"midframe mode switch");
 if(ov)begin
 if(!checking || count>=WORDS)$fatal(1,"unexpected output");
 if(data!==expected[m*WORDS+count])$fatal(1,"pixel mismatch mode=%0d word=%0d got=%h expected=%h",m,count,data,expected[m*WORDS+count]);
 if(ol!==((count%(W*3/16))==W*3/16-1))$fatal(1,"line marker");
 if(od!==(count==WORDS-1))$fatal(1,"frame marker");
 count=count+1;
 end end end
 task ticks(input integer n);repeat(n)@(negedge clk);endtask
 task byte_send(input [7:0] b,input bit stop_ok=1);
 integer i;begin
 @(negedge sys);rx=0;repeat(434)@(negedge sys);
 for(i=0;i<8;i=i+1)begin rx=b[i];repeat(434)@(negedge sys);end
 rx=stop_ok;repeat(434)@(negedge sys);rx=1;
 end endtask
 function automatic [15:0] crc_add(input [15:0] old,input [7:0] b);
 reg [15:0] c;integer i;begin c=old^{b,8'b0};for(i=0;i<8;i=i+1)c=c[15]?(c<<1)^16'h1021:c<<1;return c;end endfunction
 task packet(input [7:0] value,input bit bad_crc=0,input [7:0] command=1);
 reg [15:0] c;begin
 c=16'hffff;c=crc_add(c,2);c=crc_add(c,8'haa);c=crc_add(c,command);c=crc_add(c,1);c=crc_add(c,value);
 byte_send(8'haa);byte_send(8'h55);byte_send(2);byte_send(8'haa);byte_send(command);byte_send(1);byte_send(value);
 byte_send(c[7:0]^{7'b0,bad_crc});byte_send(c[15:8]);byte_send(13);byte_send(10);ticks(30);
 end endtask
 task frame(input integer selected,input integer next_mode);
 integer i;begin
 m=selected;count=0;u=1;ticks(1);u=0;ticks(20);checking=1;
 if(mode!==selected)$fatal(1,"frame commit");
 fork
 begin
 for(i=0;i<GROUPS;i=i+1)begin
 rgb=source[i];wb=source_wb[i];v=1;ticks(1);v=0;
 if(i%(W/4)==W/4-1)begin l=1;ticks(6);l=0;end else if(i%7==2)ticks(2);
 end
 ticks(W*3+200);
 end
 begin ticks(100);packet(next_mode);end
 join
 if(count!=WORDS || dut.busy)$fatal(1,"frame size/drain");
 checking=0;frames=frames+1;
 if(dut.requested_mode!==next_mode)$fatal(1,"UART requested mode");
 end endtask
 initial begin
 $readmemh("input.hex",source);$readmemh("input_wb.hex",source_wb);$readmemh("expected.hex",expected);
 ticks(5);rst=1;ticks(10);
 // False start, invalid stop bit, bad CRC, invalid mode, unknown command and half-packet timeout.
 rx=0;repeat(20)@(negedge sys);rx=1;ticks(20);
 byte_send(8'haa,0);repeat(500)@(negedge sys);
 packet(5,1);packet(255);packet(5,0,2);
 byte_send(8'haa);byte_send(8'h55);byte_send(2);repeat(10100)@(negedge sys);
 if(dut.requested_mode!=0)$fatal(1,"invalid input changed mode");
 frame(0,1);
 for(integer n=1;n<=11;n=n+1)frame(n,n==11?0:n+1);
 frame(0,1);
 // Stopped destination clock: held payload must not be overwritten; latest queued mode wins.
 @(negedge clk);clock_enable=0;packet_without_video(1);packet_without_video(5);packet_without_video(10);
 clock_enable=1;ticks(100);
 if(dut.requested_mode!=10)$fatal(1,"mailbox recovery/latest request");
 // UART and local keys share one requested-mode state.
 packet(5);u=1;ticks(1);u=0;ticks(5);
 keys[2]=0;ticks(15);keys=15;ticks(15);
 if(dut.requested_mode!=1)$fatal(1,"key after UART used stale state");
 rst=0;ticks(5);rst=1;ticks(10);
 if(mode!=0||dut.requested_mode!=0)$fatal(1,"reset");
 $display("PASS UART actual 115200 8N1, CRC/errors/timeout, CDC clock stall, 13 golden frames (0..11 + original return), keys and reset");$finish;
 end
 task packet_without_video(input [7:0] value);
 reg [15:0] c;begin
 c=16'hffff;c=crc_add(c,2);c=crc_add(c,0);c=crc_add(c,1);c=crc_add(c,1);c=crc_add(c,value);
 byte_send(8'haa);byte_send(8'h55);byte_send(2);byte_send(0);byte_send(1);byte_send(1);byte_send(value);byte_send(c[7:0]);byte_send(c[15:8]);byte_send(13);byte_send(10);
 end endtask
 initial begin #200000000;$fatal(1,"timeout");end
endmodule
