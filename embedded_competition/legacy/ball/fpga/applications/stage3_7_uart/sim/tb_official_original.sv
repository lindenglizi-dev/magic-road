`timescale 1ns/1ps
// Model only the unchanged camera front end. Actual ISP wiring, AWB, algorithm
// graph, OSD and DDR packing are under test. Vendor IP interface models are
// provided by tb_awb_bypass.sv; this is a functional test, not board emulation.
module demosaic #(parameter IMG_HEIGHT=720,IMG_WIDTH=1280,data_complete_delay=50,
 parameter BAYER_MODE="BGGR")(
 input I_clk,I_rst_n,input [39:0] axi4s_video_tdata,input [9:0] axi4s_video_tdest,
 input axi4s_video_tlast,axi4s_video_tvalid,axi4s_video_tuser,
 output axi4s_video_tready,output [127:0] O_tdata,
 output O_tvalid,O_tuser,O_tlast,input O_tready);
 assign axi4s_video_tready=O_tready;
 assign O_tvalid=axi4s_video_tvalid;assign O_tuser=axi4s_video_tuser;assign O_tlast=axi4s_video_tlast;
 genvar k;
 generate for(k=0;k<4;k=k+1)begin:lane
 wire [7:0] r=8'd32+axi4s_video_tdata[3:0]+k;
 wire [7:0] g=8'd80+k;
 wire [7:0] b=8'd16+axi4s_video_tdata[7:4]+k;
 assign O_tdata[k*32+:32]={8'd0,r,g,b};
 end endgenerate
endmodule

module tb_official_original;
 localparam W=256,H=12,GROUPS=W*H/4,BYTES=W*H*3,WORDS=BYTES/16;
 reg clk=0;always #5 clk=~clk;
 reg rst=0,v=0,u=0,l=0,uart_valid=0;reg [3:0] requested=0;
 reg [39:0] sample=0;
 wire [127:0] out_data;wire ov,ol,early;
 isp_top #(.IMG_WIDTH(W),.IMG_HEIGHT(H)) dut(
 .I_source_target(1'b0),.I_pc_rgb(96'd0),.I_pc_valid(1'b0),.I_pc_early(1'b0),.I_pc_last(1'b0),.I_pc_in_frame(1'b0),.I_roi_config(96'd0),.I_roi_applied(96'd0),.I_uart_valid(uart_valid),.I_uart_mode(requested),.I_keys_n(4'hf),
 .axi4s_video_aclk(clk),.I_rst_n(rst),.I_tlast(l),.I_tuser(u),.I_tdata(sample),
 .I_tvalid(v),.I_tdest(10'd0),.O_tready(1'b1),.O_tdata(out_data),
 .O_tlast(ol),.O_tuser(early),.O_tvalid(ov),.I_tready());
 reg [7:0] reference_bytes[0:BYTES-1];
 integer write_count=0,read_count=0,words=0,corrected_groups=0,frames=0,j;
 reg checking=0;integer active=0;
 always @(posedge clk)begin
 #1;
 if(rst && checking)begin
 // This is the integration condition missed by the previous runtime-only tests.
 if(dut.u_application.I_rgb!==dut.awb_O_tdata)$fatal(1,"original tap bypasses official AWB");
 if(dut.app_error)$fatal(1,"runtime/packing error");
 if(dut.awb_O_tvalid)begin
 if(write_count+12>BYTES)$fatal(1,"extra AWB pixels");
 for(j=0;j<12;j=j+1)reference_bytes[write_count+j]=dut.awb_O_tdata[95-j*8-:8];
 write_count=write_count+12;
 if(dut.awb_O_tdata!==dut.awb_uncorrected)corrected_groups=corrected_groups+1;
 end
 if(ov)begin
 if(read_count+16>write_count)$fatal(1,"output before reference pixels");
 for(j=0;j<16;j=j+1)
 if(out_data[127-j*8-:8]!==reference_bytes[read_count+j])$fatal(1,"official RGB mismatch mode=%d byte=%d",active,read_count+j);
 if(ol!==((words%(W*3/16))==W*3/16-1))$fatal(1,"line marker");
 if(dut.app_done!==(words==WORDS-1))$fatal(1,"frame marker");
 read_count=read_count+16;words=words+1;
 end
 end end
 task ticks(input integer n);repeat(n)@(negedge clk);endtask
 task frame(input integer mode);
 integer row,col;
 begin
 requested=mode;uart_valid=1;ticks(1);uart_valid=0;ticks(4);
 write_count=0;read_count=0;words=0;corrected_groups=0;checking=1;active=mode;
 u=1;ticks(1);u=0;ticks(20);
 if(dut.app_mode!=mode)$fatal(1,"frame mode latch");
 for(row=0;row<H;row=row+1)begin
 for(col=0;col<W/4;col=col+1)begin sample=col+row;v=1;ticks(1);end
 v=0;l=1;ticks(1);l=0;ticks(100);
 end
 ticks(800);
 if(write_count!=BYTES||read_count!=BYTES||words!=WORDS)$fatal(1,"pixel count");
 if(corrected_groups<GROUPS/2)$fatal(1,"test did not exercise a green-biased sensor stream");
 if(dut.u_application.busy)$fatal(1,"branch drain");
 checking=0;frames=frames+1;
 $display("PASS official original frame mode=%0d: %0d bytes equal AWB reference; %0d corrected groups",mode,read_count,corrected_groups);
 end endtask
 initial begin
 ticks(5);rst=1;ticks(5);
 frame(0);frame(1);frame(0);
 if(frames!=3)$fatal(1,"frame count");
 $display("PASS official-original colour regression: actual ISP AWB tap, RGB ordering, 0/1/0 switching and frame markers");$finish;
 end
 initial begin #2000000;$fatal(1,"timeout");end
endmodule
