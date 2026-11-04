`timescale 1ns/1ps
// Control-boundary model only: vendor FIFO memory/DDR PHY are not modeled here.
module w128_d512_fifo(input rst,clkw,we,input [127:0] di,input clkr,re,
 output afull,full_flag,output [8:0] wrusedw,rdusedw,output [127:0] dout,
 output valid,empty_flag,aempty);
 integer recovery=99,writes=0,resets=0;
 assign afull=0;assign full_flag=0;assign wrusedw=0;assign rdusedw=0;
 assign dout=0;assign valid=0;assign empty_flag=1;assign aempty=1;
 always @(posedge rst)begin recovery=0;resets=resets+1;end
 always @(posedge clkw)begin
 if(rst)recovery=0;else if(recovery<99)recovery=recovery+1;
 if(we)begin
 if(rst!==0||recovery<3)$fatal(1,"FIFO reset overlaps processed write");
 writes=writes+1;
 end end
endmodule
module tb_fifo_boundary;
 reg clk=0,ddrclk=0;always #4.83 clk=~clk;always #7.5 ddrclk=~ddrclk;
 reg rst=0;reg [3:0] keys=15;reg v=0,u=0;wire [127:0] data;wire valid,early,err;
 stage3_7_runtime #(.IMG_WIDTH(32),.IMG_HEIGHT(12),.DEBOUNCE_CYCLES(4)) dut(
 .I_clk(clk),.I_rst_n(rst),.I_roi_config(96'd0),.I_keys_n(keys),.I_uart_valid(1'b0),.I_uart_mode(4'd10),.I_wb_rgb(96'h8899aa112233bbccdd445566),.I_rgb(96'h8899aa112233bbccdd445566),.I_valid(v),.I_user(u),.I_last(1'b0),
 .O_data(data),.O_valid(valid),.O_early(early),.O_error(err),.O_last(),.O_done(),.active_mode());
 video_in sink(.I_rst_n(rst),.I_camera_clk(clk),.I_camera_frame_start(early),.I_camera_valid(valid),.I_camera_data(data),
 .I_mipi_rx_error(1'b0),.I_ddr_clk(ddrclk),.I_display_pause(1'b0),.I_video_out_rd_busy(1'b0),.I_ddr_user_ready(1'b1),
 .O_video_in_wr_busy(),.O_video_out_rp(),.O_ddr_user_wr_en(),.O_ddr_user_addr(),.O_ddr_user_wr_data());
 integer m,i;
 task ticks(input integer n);repeat(n)@(negedge clk);endtask
 initial begin
 ticks(10);rst=1;ticks(10);
 for(m=0;m<12;m=m+1)begin
 u=1;ticks(1);u=0;
 // Conservative 20-cycle early lead, less than baseline AWB's 50-group delay.
 ticks(20);
 for(i=0;i<96;i=i+1)begin v=1;ticks(1);v=0;if(i%8==7)ticks(6);end
 ticks(300);
 if(err)$fatal(1,"runtime protocol error");
 if(m==0)begin keys[3]=0;ticks(15);keys[3]=1;ticks(15);end
 else begin keys[1]=0;ticks(15);keys[1]=1;ticks(15);end
 end
 if(sink.U_w128_d512_fifo.writes!=864)$fatal(1,"wrong write count");
 if(sink.U_w128_d512_fifo.resets!=12)$fatal(1,"wrong reset count");
 $display("PASS original video_in FIFO control: original+eleven modes, 103.52/66.67MHz, no write during reset/recovery");$finish;
 end
 initial begin #1000000;$fatal(1,"timeout");end
endmodule
