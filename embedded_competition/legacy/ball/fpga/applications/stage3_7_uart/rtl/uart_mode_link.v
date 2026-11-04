// Shared asynchronous reset assertion; independently synchronized release.
// One outstanding bundled-data mailbox plus a latest-request pending slot.
// The held bus remains stable until the synchronized acknowledgement arrives.
module uart_mode_link #(parameter integer CLK_HZ=50000000,BAUD=115200)(
 input wire sys_clk,video_clk,rst_n,rx,
 output reg [3:0] video_mode,output reg video_valid);
 (* ASYNC_REG="TRUE" *) reg [1:0] sys_reset,video_reset;
 always @(posedge sys_clk or negedge rst_n)
 if(!rst_n)sys_reset<=0;else sys_reset<={sys_reset[0],1'b1};
 always @(posedge video_clk or negedge rst_n)
 if(!rst_n)video_reset<=0;else video_reset<={video_reset[0],1'b1};
 wire [7:0] byte_data;wire byte_valid,frame_error;
 wire [3:0] parsed_mode;wire parsed_valid;
 uart_rx #(.CLK_HZ(CLK_HZ),.BAUD(BAUD)) u_rx(
 .clk(sys_clk),.rst_n(sys_reset[1]),.rx(rx),.data(byte_data),.valid(byte_valid),.framing_error(frame_error));
 uart_mode_protocol #(.TIMEOUT_CYCLES(CLK_HZ/50)) u_protocol(
 .clk(sys_clk),.rst_n(sys_reset[1]),.data(byte_data),.valid(byte_valid),.framing_error(frame_error),
 .mode(parsed_mode),.mode_valid(parsed_valid));
 reg request,ack,pending;reg [3:0] held_mode,pending_mode;
 (* ASYNC_REG="TRUE" *) reg ack_meta,ack_sync,request_meta,request_sync;
 always @(posedge sys_clk or negedge rst_n)begin
 if(!rst_n)begin request<=0;ack_meta<=0;ack_sync<=0;held_mode<=0;pending<=0;pending_mode<=0;end
 else if(!sys_reset[1])begin request<=0;ack_meta<=0;ack_sync<=0;held_mode<=0;pending<=0;pending_mode<=0;end
 else begin
 ack_meta<=ack;ack_sync<=ack_meta;
 if(parsed_valid)begin pending<=1;pending_mode<=parsed_mode;end
 if(request==ack_sync && (pending||parsed_valid))begin
 held_mode<=parsed_valid?parsed_mode:pending_mode;request<=~request;pending<=0;
 end end end
 always @(posedge video_clk or negedge rst_n)begin
 if(!rst_n)begin request_meta<=0;request_sync<=0;ack<=0;video_mode<=0;video_valid<=0;end
 else if(!video_reset[1])begin request_meta<=0;request_sync<=0;ack<=0;video_mode<=0;video_valid<=0;end
 else begin
 request_meta<=request;request_sync<=request_meta;video_valid<=0;
 if(request_sync!=ack)begin video_mode<=held_mode;video_valid<=1;ack<=request_sync;end
 end end
endmodule
