// One outstanding bundled-data transaction. Only frame commit produces ROI ACK.
module vision_video_control #(parameter W=1280,H=720,IMAGE_FEATURES=0)(
 input clk,rst_n,input request,input [7:0] command,input [95:0] data,
 output reg ack,output reg [7:0] reply_code,reply_length,output reg [495:0] reply,
 input early,runtime_busy,input [3:0] active_mode,input source_actual,image_valid,input [31:0] uploaded,
 output reg [3:0] mode,output reg mode_valid,output reg source_target,
 output reg [95:0] roi_config,output reg [95:0] roi_applied,output reg [15:0] roi_revision,
 input [31:0] roi_frame,red_count,yellow_count,green_count,blue_count,input [2:0] roi_result,input roi_warm);
 (* ASYNC_REG="TRUE" *) reg req_meta,req_sync;
 reg [2:0] state;reg target_request;reg [7:0] held_command;
 localparam [95:0] DEFAULT_ROI={16'd540,16'd800,16'd180,16'd480,8'd1,8'd0,8'd1,8'd0};
 // enabled, traffic, strict, HDMI border; default disabled to preserve the old picture.
 localparam [31:0] CAPS=32'd3 | (IMAGE_FEATURES ? 32'd28 : 32'd0);
 always @(posedge clk or negedge rst_n)begin
 if(!rst_n)begin req_meta<=0;req_sync<=0;end else begin req_meta<=request;req_sync<=req_meta;end end
 task snapshot_roi;
 begin
 reply<=0;reply[7:0]<=1;reply[103:8]<=roi_applied;reply[119:104]<=roi_revision;
 reply[151:120]<=roi_frame;reply[159:152]<={5'b0,roi_result};reply[167:160]<={7'b0,roi_warm};
 reply[199:168]<=red_count;reply[231:200]<=yellow_count;reply[263:232]<=green_count;reply[295:264]<=blue_count;
 reply_length<=37;
 end endtask
 always @(posedge clk or negedge rst_n)begin
 if(!rst_n)begin ack<=0;state<=0;target_request<=0;held_command<=0;mode<=0;mode_valid<=0;source_target<=0;
 roi_config<=DEFAULT_ROI;roi_applied<=DEFAULT_ROI;roi_revision<=0;reply<=0;reply_code<=0;reply_length<=0;end
 else begin
 mode_valid<=0;
 case(state)
 0:if(req_sync!=ack)begin
 target_request<=req_sync;held_command<=command;reply<=0;reply_code<=0;reply_length<=0;
 case(command)
 8'h01:begin mode<=data[3:0];mode_valid<=1;state<=1;end
 8'h10:begin roi_config<=data;state<=2;end
 8'h11:begin snapshot_roi();ack<=req_sync;end
 8'h03:begin
 reply[7:0]<=1;reply[23:8]<=W;reply[39:24]<=H;reply[71:40]<=CAPS;
 reply[79:72]<={4'b0,active_mode};reply[87:80]<={7'b0,source_actual};reply[95:88]<={7'b0,image_valid};
 reply[127:96]<=uploaded;reply[143:128]<=roi_revision;reply_length<=18;ack<=req_sync;
 end
 8'h20:if(data[0]&&!image_valid)begin reply_code<=5;ack<=req_sync;end
 else begin source_target<=data[0];state<=3;end
 default:begin reply_code<=1;ack<=req_sync;end
 endcase
 end
 1:if(active_mode==mode)begin reply[7:0]<={4'b0,active_mode};reply_length<=1;ack<=target_request;state<=0;end
 2:if(early&&!runtime_busy)begin roi_applied<=roi_config;roi_revision<=roi_revision+1'b1;state<=4;end
 3:if(source_actual==source_target)begin reply[7:0]<={7'b0,source_actual};reply_length<=1;ack<=target_request;state<=0;end
 4:begin reply[95:0]<=roi_applied;reply_length<=12;ack<=target_request;state<=0;end
 default:state<=0;
 endcase
 end end
endmodule
