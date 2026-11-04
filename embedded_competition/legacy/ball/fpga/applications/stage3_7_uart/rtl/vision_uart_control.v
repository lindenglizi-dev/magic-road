// V2 superset: original MODE command 01 is unchanged. Shared RX/TX + reply cache.
module vision_uart_control #(parameter CLK_HZ=50000000,BAUD=115200,W=1280,H=720,IMAGE_FEATURES=0)(
 input sys_clk,video_clk,rst_n,rx,output tx,
 input video_early,video_busy,input [3:0] active_mode,
 input source_actual,image_valid,ddr_ready,
 output image_publish,image_publish_bank,input image_publish_ack,
 output image_mem_start,image_mem_write,output [24:0] image_mem_address,output [127:0] image_mem_data,
 input image_mem_busy,image_mem_done,input [127:0] image_mem_result,
 output [3:0] mode,output mode_valid,output source_target,
 output [95:0] roi_config,roi_applied,output [15:0] roi_revision,
 input [31:0] roi_frame,red_count,yellow_count,green_count,blue_count,input [2:0] roi_result,input roi_warm);
 (* ASYNC_REG="TRUE" *) reg [1:0] sr,vr;
 always @(posedge sys_clk or negedge rst_n)if(!rst_n)sr<=0;else sr<={sr[0],1'b1};
 always @(posedge video_clk or negedge rst_n)if(!rst_n)vr<=0;else vr<={vr[0],1'b1};
 wire [7:0] rx_data;wire rx_valid,rx_error;
 uart_rx #(.CLK_HZ(CLK_HZ),.BAUD(BAUD)) u_rx(.clk(sys_clk),.rst_n(sr[1]),.rx(rx),.data(rx_data),.valid(rx_valid),.framing_error(rx_error));
 reg [3:0] state;
 reg take;reg [7:0] address;wire [7:0] value,command,sn,length;wire packet;wire [15:0] signature;
 wire [7:0] image_address;wire [7:0] read_address=state==7?image_address:address;
 uart_frame_rx #(.TIMEOUT(CLK_HZ/50)) u_frames(.clk(sys_clk),.rst_n(sr[1]),.data(rx_data),.valid(rx_valid),.framing_error(rx_error),
 .take(take),.payload_addr(read_address),.payload_data(value),.frame_valid(packet),.command(command),.seq(sn),.length(length),.signature(signature));
 reg tx_start;wire tx_busy;reg [7:0] tx_command,tx_seq,tx_length;reg [511:0] tx_payload;
 uart_frame_tx #(.CLK_HZ(CLK_HZ),.BAUD(BAUD)) u_tx(.clk(sys_clk),.rst_n(sr[1]),.start(tx_start),.command(tx_command),.seq(tx_seq),.length(tx_length),.payload(tx_payload),.busy(tx_busy),.tx(tx));
 reg request;wire video_ack;reg [7:0] vcommand;reg [95:0] vdata;
 wire [7:0] vcode,vlength;wire [495:0] vreply;
 (* ASYNC_REG="TRUE" *) reg ack_meta,ack_sync;
 always @(posedge sys_clk or negedge rst_n)if(!rst_n)begin ack_meta<=0;ack_sync<=0;end else begin ack_meta<=video_ack;ack_sync<=ack_meta;end
 vision_video_control #(.W(W),.H(H),.IMAGE_FEATURES(IMAGE_FEATURES)) u_video(.clk(video_clk),.rst_n(vr[1]),.request(request),.command(vcommand),.data(vdata),
 .ack(video_ack),.reply_code(vcode),.reply_length(vlength),.reply(vreply),.early(video_early),.runtime_busy(video_busy),.active_mode(active_mode),
 .source_actual(IMAGE_FEATURES?source_actual:1'b0),.image_valid(IMAGE_FEATURES?image_valid:1'b0),.uploaded(IMAGE_FEATURES&&image_valid?32'd4147200:32'd0),.mode(mode),.mode_valid(mode_valid),.source_target(source_target),
 .roi_config(roi_config),.roi_applied(roi_applied),.roi_revision(roi_revision),.roi_frame(roi_frame),
 .red_count(red_count),.yellow_count(yellow_count),.green_count(green_count),.blue_count(blue_count),.roi_result(roi_result),.roi_warm(roi_warm));
 reg [255:0] header;reg [7:0] held_cmd,held_seq,held_len,code;
 reg [15:0] held_sig,last_sig;reg [7:0] last_cmd,last_seq,last_length,last_txcmd;reg [511:0] last_reply;reg cached;
 reg image_start;wire image_done;wire [7:0] image_code,image_length;wire [63:0] image_reply;
 wire image_valid_sys;wire [31:0] image_uploaded;
 (* ASYNC_REG="TRUE" *) reg ready_meta,ready_sync;
 always @(posedge sys_clk or negedge rst_n)if(!rst_n)begin ready_meta<=0;ready_sync<=0;end else begin ready_meta<=ddr_ready;ready_sync<=ready_meta;end
 image_upload_engine u_upload(.clk(sys_clk),.rst_n(sr[1]),.ready(ready_sync),.start(image_start),.command(held_cmd),.length(held_len),.header(header),.signature(held_sig),
 .payload_addr(image_address),.payload_data(value),.done(image_done),.error(image_code),.reply_length(image_length),.reply(image_reply),
 .mem_start(image_mem_start),.mem_write(image_mem_write),.mem_address(image_mem_address),.mem_data(image_mem_data),.mem_busy(image_mem_busy),.mem_done(image_mem_done),.mem_result(image_mem_result),
 .publish(image_publish),.publish_bank(image_publish_bank),.publish_ack(image_publish_ack),.valid_image(image_valid_sys),.uploaded(image_uploaded));

 always @(posedge sys_clk or negedge rst_n)begin
 if(!rst_n)begin state<=0;take<=0;address<=0;header<=0;held_cmd<=0;held_seq<=0;held_len<=0;held_sig<=0;request<=0;vcommand<=0;vdata<=0;
 tx_start<=0;image_start<=0;tx_command<=0;tx_seq<=0;tx_length<=0;tx_payload<=0;code<=0;last_sig<=0;last_cmd<=0;last_seq<=0;last_reply<=0;last_length<=0;last_txcmd<=0;cached<=0;end
 else if(sr[1])begin
 take<=0;tx_start<=0;image_start<=0;
 case(state)
 0:if(packet&&!tx_busy&&!tx_start)begin
 held_cmd<=command;held_seq<=sn;held_len<=length;held_sig<=signature;header<=0;address<=0;code<=0;
 if(cached&&command==last_cmd&&sn==last_seq&&signature==last_sig)begin
 tx_command<=last_txcmd;tx_seq<=sn;tx_length<=last_length;tx_payload<=last_reply;tx_start<=1;take<=1;state<=5;
 end else if(length==0)state<=2;else state<=1;
 end
 1:begin header[address*8+:8]<=value;if(address==held_len-1||address==31)state<=2;else address<=address+1'b1;end
 2:begin
 vcommand<=held_cmd;vdata<=header[95:0];
 case(held_cmd)
 8'h01:if(held_len!=1)begin code<=2;state<=4;end else if(header[7:0]>11)begin code<=3;state<=4;end else begin request<=~request;state<=3;end
 8'h03,8'h11:if(held_len!=0)begin code<=2;state<=4;end else begin request<=~request;state<=3;end
 8'h10:if(held_len!=12)begin code<=2;state<=4;end
 else if(header[7:0]>1||header[15:8]>1||header[23:16]>1||header[31:24]>1||
 header[47:32]>=header[79:64]||header[63:48]>=header[95:80]||header[79:64]>W||header[95:80]>H)begin code<=3;state<=4;end
 else begin request<=~request;state<=3;end
 8'h20:if(!IMAGE_FEATURES)begin code<=1;state<=4;end
 else if(held_len!=1)begin code<=2;state<=4;end
 else if(header[7:0]>1)begin code<=3;state<=4;end
 else begin request<=~request;state<=3;end
 8'h30,8'h31,8'h32,8'h33:if(!IMAGE_FEATURES)begin code<=1;state<=4;end
 else begin image_start<=1;state<=7;end
 default:begin code<=1;state<=4;end
 endcase
 end
 3:if(ack_sync==request)begin
 tx_payload<={vreply,vcode,held_cmd};tx_length<=vlength+2;tx_command<=vcode==0 ? 8'h81 : 8'h82;tx_seq<=held_seq;state<=6;
 end
 4:begin tx_payload<={496'd0,code,held_cmd};tx_length<=2;tx_command<=8'h82;tx_seq<=held_seq;state<=6;end
 7:if(image_done)begin tx_payload<={432'd0,image_reply,image_code,held_cmd};tx_length<=image_length+2;
 tx_command<=image_code==0?8'h81:8'h82;tx_seq<=held_seq;state<=6;end
 6:if(!tx_busy)begin
 tx_start<=1;take<=1;cached<=1;last_cmd<=held_cmd;last_seq<=held_seq;last_sig<=held_sig;
 last_reply<=tx_payload;last_length<=tx_length;last_txcmd<=tx_command;state<=5;
 end
 5:if(!packet)state<=0;
 default:state<=0;
 endcase
 end end
endmodule
