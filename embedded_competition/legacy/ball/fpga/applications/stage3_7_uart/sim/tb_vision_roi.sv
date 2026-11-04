`timescale 1ns/1ps
module tb_vision_roi;
 reg sys=0;always #10 sys=~sys;
 reg clk=0;always #4.83 clk=~clk;
 reg rst=0,rx=1,early=0,valid=0;reg [95:0] rgb=0;
 wire tx,mode_valid,source_target;wire [3:0] mode;reg [3:0] active_mode=0,pending_mode=0;
 wire [95:0] cfg,applied;wire [15:0] revision;wire [31:0] frame,cr,cy,cg,cb;wire [2:0] result;wire warm;
 wire ims,imw;wire [24:0] ima;wire [127:0] imd;reg imdone=0;integer writes=0,k;
 always @(posedge sys)begin
 imdone<=ims;
 if(ims&&imw)begin
 if(ima!=25165824+writes*8)$fatal(1,"UART IMAGE_DATA DDR offset");
 for(k=0;k<16;k=k+1)if(imd[k*8+:8]!==8'(writes*16+k+8))$fatal(1,"UART image payload byte order");
 writes=writes+1;
 end end
 vision_uart_control #(.W(64),.H(32),.IMAGE_FEATURES(1)) dut(.sys_clk(sys),.video_clk(clk),.rst_n(rst),.rx(rx),.tx(tx),
 .source_actual(1'b0),.image_valid(1'b0),.ddr_ready(1'b1),.image_publish(),.image_publish_bank(),.image_publish_ack(1'b0),
 .image_mem_start(ims),.image_mem_write(imw),.image_mem_address(ima),.image_mem_data(imd),
 .image_mem_busy(1'b0),.image_mem_done(imdone),.image_mem_result(128'd0),
 .video_early(early),.video_busy(1'b0),.active_mode(active_mode),.mode(mode),.mode_valid(mode_valid),.source_target(source_target),
 .roi_config(cfg),.roi_applied(applied),.roi_revision(revision),.roi_frame(frame),.red_count(cr),.yellow_count(cy),.green_count(cg),.blue_count(cb),.roi_result(result),.roi_warm(warm));
 color_traffic_core #(.W(64),.H(32)) core(.clk(clk),.rst_n(rst),.rgb(rgb),.valid(valid),.early(early),
 .traffic(cfg[8]),.strict(cfg[16]),.mask(1'b0),.roi_enable(cfg[0]),.roi_x0(cfg[43:32]),.roi_y0(cfg[59:48]),.roi_x1(cfg[75:64]),.roi_y1(cfg[91:80]),
 .out_rgb(),.out_valid(),.out_user(),.out_last(),.out_done(),.result(result),.frame_result(),.O_display_result(),.O_display_traffic(),
 .red_count(cr),.yellow_count(cy),.green_count(cg),.blue_count(cb),.O_frame_count(frame),.O_result_ready(warm),.O_frame_complete(),.error());
 always @(posedge clk)begin if(!rst)begin pending_mode<=0;active_mode<=0;end else begin if(mode_valid)pending_mode<=mode;if(early)active_mode<=pending_mode;end end
 wire [7:0] byte_data;wire byte_valid,frame_error;
 uart_rx receiver(.clk(sys),.rst_n(rst),.rx(tx),.data(byte_data),.valid(byte_valid),.framing_error(frame_error));
 reg take=0;reg [7:0] address=0;wire [7:0] value,reply_cmd,reply_seq,reply_len;wire reply_valid;
 uart_frame_rx replies(.clk(sys),.rst_n(rst),.data(byte_data),.valid(byte_valid),.framing_error(frame_error),.take(take),
 .payload_addr(address),.payload_data(value),.frame_valid(reply_valid),.command(reply_cmd),.seq(reply_seq),.length(reply_len),.signature());
 task ticks(input integer n);repeat(n)@(negedge clk);endtask
 task send_byte(input [7:0] b);integer i;begin
 @(negedge sys);rx=0;repeat(434)@(negedge sys);
 for(i=0;i<8;i=i+1)begin rx=b[i];repeat(434)@(negedge sys);end
 rx=1;repeat(434)@(negedge sys);
 end endtask
 function automatic [15:0] crc_add(input [15:0] old,input [7:0] b);
 reg [15:0] c;begin c=old^{b,8'b0};repeat(8)c=c[15]?(c<<1)^16'h1021:c<<1;return c;end endfunction
 reg corrupt=0;
 task packet(input [7:0] cmd,sn,len,input [1919:0] bytes);
 reg [15:0] c;integer i;begin
 c=crc_add(crc_add(crc_add(crc_add(16'hffff,2),sn),cmd),len);
 send_byte(8'haa);send_byte(8'h55);send_byte(2);send_byte(sn);send_byte(cmd);send_byte(len);
 for(i=0;i<len;i=i+1)begin send_byte(bytes[i*8+:8]);c=crc_add(c,bytes[i*8+:8]);end
 send_byte(c[7:0]^(corrupt?8'd1:8'd0));send_byte(c[15:8]);send_byte(13);send_byte(10);
 end endtask
 task expect_nack(input [7:0] cmd,sn,code);
 begin wait(reply_valid);if(reply_cmd!=8'h82||reply_seq!=sn||reply_len!=2)$fatal(1,"NACK header");
 address=0;repeat(2)@(negedge sys);if(value!=cmd)$fatal(1,"NACK command");
 address=1;repeat(2)@(negedge sys);if(value!=code)$fatal(1,"NACK code");consume();end endtask
 task expect_reply(input [7:0] cmd,sn,len);
 begin
 wait(reply_valid);if(reply_cmd!=8'h81||reply_seq!=sn||reply_len!=len)$fatal(1,"reply header");
 address=0;repeat(2)@(negedge sys);if(value!=cmd)$fatal(1,"ACK command");
 address=1;repeat(2)@(negedge sys);if(value!=0)$fatal(1,"ACK error");
 end endtask
 task consume;begin take=1;repeat(2)@(negedge sys);take=0;repeat(2)@(negedge sys);end endtask
 task video_frame;
 integer row,col;begin
 @(negedge clk);early=1;ticks(1);early=0;ticks(20);
 for(row=0;row<32;row=row+1)begin
 for(col=0;col<16;col=col+1)begin rgb=col<8 ? {4{24'hff0000}} : {4{24'h00ff00}};valid=1;ticks(1);end
 valid=0;ticks(4);
 end
 ticks(100);
 end endtask
 reg [95:0] left_roi,right_roi;reg [1919:0] image_packet;integer j;
 initial begin
 left_roi={16'd16,16'd32,16'd0,16'd0,8'd1,8'd0,8'd1,8'd1};
 right_roi={16'd16,16'd64,16'd0,16'd32,8'd1,8'd0,8'd1,8'd1};
 ticks(5);rst=1;ticks(10);
 packet(3,1,0,0);expect_reply(3,1,20);address=3;repeat(2)@(negedge sys);if(value!=64)$fatal(1,"source width");consume();
 packet(8'h10,2,12,left_roi);ticks(50);
 if(revision!=0||dut.request==dut.video_ack)$fatal(1,"ROI ACK before frame commit");
 video_frame();expect_reply(8'h10,2,14);consume();
 video_frame();video_frame();if(result!=1||!warm||cr!=512||cg!=0)$fatal(1,"red detection");
 packet(8'h11,3,0,0);expect_reply(8'h11,3,39);address=21;repeat(2)@(negedge sys);if(value!=1)$fatal(1,"ROI status red");consume();
 packet(8'h10,4,12,right_roi);ticks(50);if(revision!=1)$fatal(1,"midframe ROI changed");
 video_frame();expect_reply(8'h10,4,14);consume();video_frame();video_frame();
 if(result!=3||!warm||cr!=0||cg!=512)$fatal(1,"ROI moved to green");
 packet(8'h10,4,12,right_roi);expect_reply(8'h10,4,14);consume();if(revision!=2)$fatal(1,"duplicate reapplied");
 packet(1,5,1,96'd5);ticks(50);if(active_mode!=0)$fatal(1,"mode changed before frame");video_frame();
 expect_reply(1,5,3);consume();if(active_mode!=5)$fatal(1,"legacy MODE failed");
 image_packet=0;image_packet[31:0]=123;image_packet[47:32]=1920;image_packet[63:48]=1080;
 image_packet[71:64]=1;image_packet[103:72]=4147200;
 packet(8'h30,6,17,image_packet);expect_reply(8'h30,6,6);consume();
 image_packet=0;image_packet[31:0]=123;
 for(j=8;j<232;j=j+1)image_packet[j*8+:8]=j;
 corrupt=1;packet(8'h31,7,232,image_packet);ticks(100);if(writes!=0||reply_valid)$fatal(1,"bad CRC wrote image");
 corrupt=0;packet(8'h31,7,232,image_packet);expect_reply(8'h31,7,10);consume();if(writes!=14)$fatal(1,"image DATA count");
 packet(8'h31,7,232,image_packet);expect_reply(8'h31,7,10);consume();if(writes!=14)$fatal(1,"duplicate image packet wrote twice");
 packet(8'h32,8,8,1920'd123);expect_nack(8'h32,8,6);
 packet(8'h20,9,1,1920'd1);expect_nack(8'h20,9,5);
 packet(8'h33,10,4,1920'd123);expect_reply(8'h33,10,6);consume();
 $display("PASS UART image commands: native1080 BEGIN, full232-byte DATA/CRC drop/retry/cache, DDR payload/offset, incomplete END/source NACK and ABORT at115200");
 $display("PASS vision ROI: bidirectional UART CRC, actual frame commit ACK, red/green moved ROI, voting/counts, duplicate ACK cache and MODE compatibility");$finish;
 end
 initial begin #200000000;$fatal(1,"ROI integration timeout");end
endmodule
