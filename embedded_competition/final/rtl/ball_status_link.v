`timescale 1ns/1ps
                                                                                
module ball_status_link #(parameter TIMEOUT=5000000, C_COMBINED=0, C_VIEW_SWITCH=0, C_REGISTERED_FRAME=0)(
 input wire video_pipeline_busy,
 output wire video_application_change,
 output wire video_application_mode_change,
 output wire video_view_target,
 input wire video_view_actual,video_view_commit,
 input wire [13:0] video_view_revision,
 output wire [191:0] video_application_config,
 output wire video_gamma_we,video_editor_we,video_gamma_commit,video_editor_commit,
 output wire [7:0] video_curve_address,video_curve_value,
 input wire sys_clk,
 input wire video_clk,
 input wire rst_n,
 input wire [1535:0] video_snapshot,
 input wire video_snapshot_valid,
 input wire video_early,
 input wire [31:0] video_good,
 input wire [31:0] video_bad,
 output wire [191:0] video_settings,
 output wire video_config_clear,
 output wire [15:0] video_revision,
 input wire [7:0] rx_data,
 input wire rx_valid,
 input wire tx_busy,
 output reg tx_start,
 output reg [7:0] tx_command,
 output reg [7:0] tx_seq,
 output reg [7:0] tx_length,
 input wire [5:0] tx_index,
 output reg [7:0] tx_data
);
 localparam ST_IDLE=0,ST_READ=1,ST_VALIDATE=2,ST_CAPTURE=3,
            ST_BUILD=4,ST_REPLY=5,ST_DRAIN=6,ST_CHECK=7,
            ST_CONTROL_START=8,ST_CONTROL_WAIT=9;
 localparam [191:0] DEFAULT_SETTINGS={16'd64,16'd640,16'd384,16'd24,16'd384,16'd24,
     16'd640,16'd1216,16'd160,16'd64,8'd2,8'd1,8'd1,8'd1};
 reg [3:0] state,next_state;
 (* ASYNC_REG="TRUE" *) reg [1:0] reset_sys,reset_video;
 always @(posedge sys_clk or negedge rst_n)
 if(!rst_n)reset_sys<=0;else reset_sys<={reset_sys[0],1'b1};
 always @(posedge video_clk or negedge rst_n)
 if(!rst_n)reset_video<=0;else reset_video<={reset_video[0],1'b1};

 reg request,acknowledge;
 (* ASYNC_REG="TRUE" *) reg request_meta,request_sync,ack_meta,ack_sync;
 reg [1535:0] source_hold;
 reg source_valid,bank_valid;
 reg [31:0] snapshot_id;
                                                                       
 always @(posedge video_clk or negedge reset_video[1])begin
 if(!reset_video[1])begin
  request_meta<=0;request_sync<=0;acknowledge<=0;source_hold<=0;source_valid<=0;
 end else begin
  request_meta<=request;request_sync<=request_meta;
  if(request_sync!=acknowledge && video_snapshot_valid)begin
   source_hold<=video_snapshot;source_valid<=video_snapshot_valid;acknowledge<=request_sync;
  end
 end end
 always @(posedge sys_clk or negedge reset_sys[1])begin
 if(!reset_sys[1])begin ack_meta<=0;ack_sync<=0;end
 else begin ack_meta<=acknowledge;ack_sync<=ack_meta;end end

 localparam CMD_SET_VIEW=8'h55,CMD_READ_VIEW=8'h56,ERR_VIEW_INACTIVE=8'd8;
 reg requested_view,view_waiting,reply_view_actual,reply_results_allowed;
 reg [13:0] reply_view_revision;
 reg ball_results_allowed,sys_application_inspection;
 reg control_request,control_ack,control_pending;
 reg [7:0] control_command;
 reg [239:0] control_data;
 (* ASYNC_REG="TRUE" *) reg control_meta,control_sync,control_ack_meta,control_ack_sync;
 wire video_pending=control_sync!=control_ack;
 localparam [191:0] DEFAULT_APPLICATION={112'd0,16'd100,16'd256,16'd0,16'd256,8'd0,8'd10};
 reg [191:0] active_application;

 reg [15:0] application_revision;
 reg [8:0] gamma_progress,editor_progress;
 reg curve_copy;
 reg [3:0] curve_index;
 reg flag_application_write,flag_application_read,flag_application_configure,flag_application_chunk;
 reg flag_application_revision_matches,flag_curves_complete,flag_curve_order_ok;
 reg [7:0] reg_application_mode;
 reg flag_application_mode_changed;
                                                                                 
                                                                                
 wire [191:0] canonical_application={112'd0,
     7'd0,control_data[120:112],6'd0,control_data[105:96],
     {7{control_data[88]}},control_data[88:80],6'd0,control_data[73:64],
     8'd0,4'd0,reg_application_mode[3:0]};
 always @(posedge video_clk or negedge reset_video[1])begin
 if(!reset_video[1])begin
  flag_application_write<=0;flag_application_read<=0;flag_application_configure<=0;flag_application_chunk<=0;
  flag_application_revision_matches<=0;flag_curves_complete<=0;flag_curve_order_ok<=0;reg_application_mode<=10;flag_application_mode_changed<=0;
 end else begin
  flag_application_write<=C_COMBINED && (control_command==8'h60 || control_command==8'h61);
  flag_application_read<=C_COMBINED && control_command==8'h62;
  flag_application_configure<=control_command==8'h60;flag_application_chunk<=control_command==8'h61;
  flag_application_revision_matches<=control_data[47:32]==application_revision;
  flag_curves_complete<=(!control_data[56] || gamma_progress==256) && (!control_data[57] || editor_progress==256);
  flag_curve_order_ok<=control_data[63:56]==0 || {1'b0,control_data[63:56]}==(control_data[48]?editor_progress:gamma_progress);
  reg_application_mode<=control_data[55:48];
                                                                           
  flag_application_mode_changed<=control_data[51:48]!=active_application[3:0];
 end end
 wire application_write=flag_application_write;
 wire application_read=flag_application_read;
 wire application_command=application_write || application_read;
 wire application_revision_matches=flag_application_revision_matches;
 wire application_commit=video_early && video_pending && application_write &&
     !video_pipeline_busy && !curve_copy && application_revision_matches;
 wire curve_kind=control_data[48];
 wire curve_order_ok=flag_curve_order_ok;
 wire curves_complete=flag_curves_complete;
 wire application_config_commit=application_commit && flag_application_configure && curves_complete;
 assign video_application_change=application_config_commit;
                                                                               
 assign video_application_mode_change=application_config_commit && flag_application_mode_changed;
 assign video_application_config=C_REGISTERED_FRAME ? active_application : application_config_commit?
     ({control_data[239:56],reg_application_mode} & ~(192'd3<<8)):active_application;
 assign video_gamma_commit=application_config_commit && control_data[56];
 assign video_editor_commit=application_config_commit && control_data[57];
 assign video_gamma_we=curve_copy && !curve_kind;
 assign video_editor_we=curve_copy && curve_kind;
 assign video_curve_address=control_data[63:56]+curve_index;
 assign video_curve_value=control_data[72+curve_index*8+:8];
 reg [191:0] active_settings;
 reg [15:0] revision;
 reg [7:0] control_error;
 reg [31:0] control_good,control_bad;
 wire control_complete=control_ack_sync==control_request;
                                                                              
                                                                            
 reg flag_configure,flag_clear,flag_revision_matches,flag_settings_differ;
 reg flag_incoming_value,flag_set_view,flag_read_view,flag_view_revision_matches;
 always @(posedge video_clk or negedge reset_video[1])begin
 if(!reset_video[1])begin
  flag_configure<=0;flag_clear<=0;flag_revision_matches<=0;flag_settings_differ<=0;
  flag_incoming_value<=0;flag_set_view<=0;flag_read_view<=0;flag_view_revision_matches<=0;
 end else begin
  flag_configure<=control_command==8'h52;flag_clear<=control_command==8'h53;
  flag_revision_matches<=control_data[47:32]==revision;
  flag_settings_differ<=control_data[239:48]!=active_settings;
  flag_incoming_value<=control_data[48];
  flag_set_view<=C_VIEW_SWITCH && control_command==CMD_SET_VIEW;
  flag_read_view<=C_VIEW_SWITCH && control_command==CMD_READ_VIEW;
  flag_view_revision_matches<=control_data[47:32]=={2'd0,video_view_revision};
 end end
 wire [3:0] view_application_mode=application_config_commit ? reg_application_mode[3:0] : active_application[3:0];
 wire application_is_inspection=!C_COMBINED || view_application_mode==10;
 wire view_revision_matches=flag_view_revision_matches;
 wire view_command=flag_set_view || flag_read_view;
                                                                           
                                                                           
 assign video_view_target=!C_VIEW_SWITCH || !application_is_inspection ? 1'b1 :
     (video_pending && flag_set_view && !view_waiting && view_revision_matches ?
      flag_incoming_value : requested_view);
 wire video_write=flag_configure || flag_clear;
 wire revision_matches=flag_revision_matches;
 wire commit_write=video_early && video_pending && video_write && revision_matches;
 wire settings_changed=flag_configure && flag_settings_differ;
 assign video_config_clear=commit_write && (flag_clear || settings_changed);
 assign video_settings=C_REGISTERED_FRAME ? active_settings : commit_write && flag_configure ? {control_data[239:49],flag_incoming_value} : active_settings;
 assign video_revision=revision;
                                                                            
                                                                                       
 always @(posedge video_clk or negedge reset_video[1])begin
 if(!reset_video[1])begin
  control_meta<=0;control_sync<=0;control_ack<=0;active_settings<=DEFAULT_SETTINGS;
  revision<=0;control_error<=0;control_good<=0;control_bad<=0;
  active_application<=DEFAULT_APPLICATION;application_revision<=0;
  gamma_progress<=0;editor_progress<=0;curve_copy<=0;curve_index<=0;
  requested_view<=0;view_waiting<=0;reply_view_actual<=0;reply_view_revision<=0;reply_results_allowed<=0;
 end else begin
  control_meta<=control_request;control_sync<=control_meta;
  if(view_waiting && video_view_commit)begin
   reply_view_actual<=video_view_actual;reply_view_revision<=video_view_revision;
   reply_results_allowed<=video_view_actual && application_is_inspection;
   control_error<=video_view_actual==requested_view ? 8'd0 : 8'd5;
   view_waiting<=0;control_ack<=control_sync;
  end else if(curve_copy)begin
   if(curve_index==15)begin
    curve_copy<=0;control_ack<=control_sync;application_revision<=application_revision+1'b1;
    if(curve_kind)editor_progress<={1'b0,control_data[63:56]}+9'd16;
    else gamma_progress<={1'b0,control_data[63:56]}+9'd16;
   end else curve_index<=curve_index+1'b1;
  end else if(video_early && video_pending && application_command && !video_pipeline_busy)begin
   control_good<=video_good;control_bad<=video_bad;
   control_error<=application_write && !application_revision_matches?8'd6:8'd0;
   if(application_commit && flag_application_chunk && curve_order_ok)begin
    curve_copy<=1;curve_index<=0;
   end else begin
    control_ack<=control_sync;
    if(application_commit && flag_application_chunk && !curve_order_ok)control_error<=8'd3;
    if(application_commit && flag_application_configure)begin
     if(!curves_complete)control_error<=8'd3;
     else begin
      active_application<=canonical_application;
      application_revision<=application_revision+1'b1;
      if(control_data[56])gamma_progress<=0;
      if(control_data[57])editor_progress<=0;
     end
    end
   end
  end else if(video_early && video_pending && view_command && !video_pipeline_busy)begin
   reply_view_actual<=video_view_actual;reply_view_revision<=video_view_revision;
   reply_results_allowed<=video_view_actual && application_is_inspection;
   if(flag_set_view)begin
    if(!view_revision_matches)begin control_error<=6;control_ack<=control_sync;end
    else if(!application_is_inspection && !flag_incoming_value)begin
     control_error<=ERR_VIEW_INACTIVE;control_ack<=control_sync;
    end else begin requested_view<=flag_incoming_value;view_waiting<=1;end
   end else begin control_error<=0;control_ack<=control_sync;end
  end else if(video_early && video_pending && !application_command && !view_command)begin
   control_error<=video_write && !revision_matches ? 8'd6 : 8'd0;
   if(commit_write && control_command==8'h52)active_settings<=control_data[239:48];
   if(video_config_clear)revision<=revision+1'b1;
   control_good<=video_config_clear ? 32'd0 : video_good;
   control_bad<=video_config_clear ? 32'd0 : video_bad;
   control_ack<=control_sync;
  end
 end end
 always @(posedge sys_clk or negedge reset_sys[1])begin
 if(!reset_sys[1])begin control_ack_meta<=0;control_ack_sync<=0;end
 else begin control_ack_meta<=control_ack;control_ack_sync<=control_ack_meta;end end
 wire [335:0] panel_control_reply={control_bad,control_good,
     (application_command?(application_read?active_application:control_data[239:48]):active_settings),
     control_data[31:0],(application_command?application_revision:revision),
     (application_command?{4'd0,active_application[3:0]}:8'd7),
     (application_command?8'd2:8'd1),control_error,control_command};

 wire [87:0] view_reply={control_data[31:0],2'd0,reply_view_revision,
     8'd3,7'd0,reply_view_actual,8'd1,control_error,control_command};
 wire [335:0] control_reply=C_VIEW_SWITCH &&
     (control_command==CMD_SET_VIEW || control_command==CMD_READ_VIEW) ? {248'd0,view_reply} : panel_control_reply;

 wire packet_valid;
 wire [7:0] packet_command,packet_seq,packet_length,payload_data;
 wire packet_is_ball=packet_command>=8'h50 && packet_command<=8'h54;
 wire reject_packet=C_VIEW_SWITCH && !ball_results_allowed && packet_is_ball;
 wire [15:0] packet_signature;
 reg take;reg [7:0] address;
 uart_frame_rx #(.TIMEOUT(TIMEOUT),.MAX_PAYLOAD(30)) u_receiver(
 .clk(sys_clk),.rst_n(reset_sys[1]),.data(rx_data),.valid(rx_valid),
 .framing_error(1'b0),.take(take),.payload_addr(address),.payload_data(payload_data),
 .frame_valid(packet_valid),.command(packet_command),.seq(packet_seq),
 .length(packet_length),.signature(packet_signature));
 reg [7:0] held_command,held_seq,held_length,error,page;
 reg [15:0] held_signature;
 reg [239:0] incoming;
                                                                            
                                                                                
 wire [191:0] canonical_config={
     incoming[239:224],                                                          
     5'd0,incoming[218:208],                                          
     7'd0,incoming[200:192],                                                
     7'd0,incoming[184:176],                                                
     5'd0,incoming[170:160],                                                 
     5'd0,incoming[154:144],                                                 
     6'd0,incoming[137:128],                                       
     5'd0,incoming[122:112],                                          
     6'd0,incoming[105:96],                                        
     5'd0,incoming[90:80],                                            
     6'd0,incoming[73:72],                                                    
     6'd0,incoming[65:64],                                        
     incoming[63:56],                                                            
     incoming[55:48]};                                                          
 reg [31:0] requested_id;
 reg [4:0] read_index;
 reg [3:0] check_index;
 reg [$clog2(TIMEOUT+1)-1:0] wait_count;
 reg cached;
 reg [7:0] cached_command,cached_seq,cached_length;
 reg [15:0] cached_signature;
                                                                                
 wire duplicate=(!C_VIEW_SWITCH || ball_results_allowed) && cached && packet_command==cached_command && packet_seq==cached_seq &&
     packet_length==cached_length && packet_signature==cached_signature &&
     (packet_command==8'h50 || packet_command==8'h51);
 reg write_cached;
 reg [7:0] last_write_command;
 reg [47:0] last_write_data;
 reg [335:0] last_write_reply;
 wire write_id_seen=write_cached && incoming[31:0]==last_write_data[31:0];
                                                                              
                                                                             
 wire write_key_matches=held_command==last_write_command && incoming[47:0]==last_write_data &&
     ((held_command!=8'h52 && held_command!=8'h60 && held_command!=8'h61) ||
      incoming[239:48]==last_write_reply[271:80]) &&
     (held_command!=CMD_SET_VIEW || incoming[55:48]==last_write_reply[31:24]);
 wire capture_complete=ack_sync==request;
 reg [71:0] reply_prefix;
 reg reply_panel,reply_write_cache;
 wire [1:0] reply_page=reply_prefix[25:24];
 wire [5:0] page_offset=tx_index-6'd9;
 wire [383:0] snapshot_first=source_hold[383:0],snapshot_second=source_hold[767:384];
 wire [383:0] snapshot_third=source_hold[1151:768],snapshot_fourth=source_hold[1535:1152];
 reg [7:0] page_byte;
 wire held_is_ball=held_command>=8'h50 && held_command<=8'h54;
 wire reject_held=C_VIEW_SWITCH && !ball_results_allowed && held_is_ball;
 wire [7:0] build_error=reject_held ? ERR_VIEW_INACTIVE : error;
 always @*begin
 case(reply_page)
 0:page_byte=snapshot_first[page_offset*8+:8];1:page_byte=snapshot_second[page_offset*8+:8];
 2:page_byte=snapshot_third[page_offset*8+:8];3:page_byte=snapshot_fourth[page_offset*8+:8];
 default:page_byte=0;
 endcase end
                                                                            
 always @*begin
 tx_data=0;
 if(reply_panel)begin
  if(tx_index<42)tx_data=reply_write_cache ? last_write_reply[tx_index*8+:8] : control_reply[tx_index*8+:8];
 end else if(tx_index<9)tx_data=reply_prefix[tx_index*8+:8];
 else if(tx_index<57 && tx_command==8'h81)tx_data=page_byte;
 end
 always @(posedge sys_clk or negedge reset_sys[1])begin
 if(!reset_sys[1])state<=ST_IDLE;else state<=next_state;
 end
 always @*begin
 next_state=state;
 case(state)
 ST_IDLE:if(packet_valid && !tx_busy)begin
  if(reject_packet)next_state=ST_BUILD;
  else if(duplicate)next_state=ST_REPLY;
  else if(packet_command==8'h50 && packet_length==0 && capture_complete)next_state=ST_CAPTURE;
  else if((packet_command==8'h51 && packet_length==5) ||
          (packet_command==8'h52 && packet_length==30) ||
          (packet_command==8'h53 && packet_length==6) ||
          (C_VIEW_SWITCH && packet_command==CMD_SET_VIEW && packet_length==7) ||
          (C_COMBINED && (packet_command==8'h60 || packet_command==8'h61) && packet_length==30))next_state=ST_READ;
  else if((packet_command==8'h54 || (C_VIEW_SWITCH && packet_command==CMD_READ_VIEW) || (C_COMBINED && packet_command==8'h62)) && packet_length==0 && !control_pending)next_state=ST_CONTROL_START;
  else next_state=ST_BUILD;
 end
 ST_READ:if(read_index==held_length-1)next_state=ST_VALIDATE;
 ST_VALIDATE:begin
  if(held_command==8'h51)next_state=ST_BUILD;
  else if(write_id_seen || control_pending)next_state=ST_BUILD;
  else if(held_command==8'h52 || held_command==8'h60 || held_command==8'h61)next_state=ST_CHECK;
  else if(C_VIEW_SWITCH && held_command==CMD_SET_VIEW && (incoming[55:48]>1 || incoming[47:46]!=0))next_state=ST_BUILD;
  else next_state=ST_CONTROL_START;
 end
 ST_CHECK:if(check_index==8)next_state=error==0 ? ST_CONTROL_START : ST_BUILD;
 ST_CAPTURE:if(capture_complete || wait_count==TIMEOUT-1)next_state=ST_BUILD;
 ST_CONTROL_START:next_state=ST_CONTROL_WAIT;
 ST_CONTROL_WAIT:if(control_complete || wait_count==TIMEOUT-1)next_state=ST_BUILD;
 ST_BUILD:next_state=ST_REPLY;
 ST_REPLY:if(reject_held && tx_command==8'h81)next_state=ST_BUILD;
          else if(!tx_busy)next_state=ST_DRAIN;
 ST_DRAIN:if(!tx_busy)next_state=ST_IDLE;
 default:next_state=ST_IDLE;
 endcase end
 always @(posedge sys_clk or negedge reset_sys[1])begin
 if(!reset_sys[1])begin
  request<=0;bank_valid<=0;snapshot_id<=0;ball_results_allowed<=!C_VIEW_SWITCH;sys_application_inspection<=1;
  control_request<=0;control_pending<=0;control_command<=0;control_data<=0;
  write_cached<=0;last_write_command<=0;last_write_data<=0;last_write_reply<=0;
  tx_start<=0;tx_command<=0;tx_seq<=0;tx_length<=0;reply_prefix<=0;reply_panel<=0;reply_write_cache<=0;
  held_command<=0;held_seq<=0;held_length<=0;held_signature<=0;
  incoming<=0;error<=0;page<=0;requested_id<=0;read_index<=0;check_index<=0;
  address<=0;take<=0;wait_count<=0;
  cached<=0;cached_command<=0;cached_seq<=0;cached_length<=0;cached_signature<=0;
 end else begin
  tx_start<=0;take<=0;
                                                                                 
  if(control_pending && control_complete)begin
   control_pending<=0;
   if(C_VIEW_SWITCH && control_error==0 && (control_command==CMD_SET_VIEW || control_command==CMD_READ_VIEW))begin
    ball_results_allowed<=reply_results_allowed;
    if(!reply_results_allowed)begin bank_valid<=0;cached<=0;end
   end
   if(C_COMBINED && control_error==0 && control_command==8'h60)begin
    sys_application_inspection<=active_application[3:0]==10;
    if(C_VIEW_SWITCH)begin ball_results_allowed<=0;bank_valid<=0;cached<=0;end
   end
   if(control_error==0 && (control_command==8'h52 || control_command==8'h53 || application_write || (C_VIEW_SWITCH && control_command==CMD_SET_VIEW)))begin
    write_cached<=1;last_write_command<=control_command;
    last_write_data<=control_data[47:0];last_write_reply<=control_reply;
   end
  end
  case(state)
  ST_IDLE:if(packet_valid && !tx_busy)begin
   held_command<=packet_command;held_seq<=packet_seq;
   held_length<=packet_length;held_signature<=packet_signature;
   error<=0;page<=0;address<=0;read_index<=0;requested_id<=0;wait_count<=0;
   check_index<=0;incoming<=0;
   if(C_VIEW_SWITCH && (packet_command==CMD_SET_VIEW || packet_command==8'h60))begin
    ball_results_allowed<=0;bank_valid<=0;cached<=0;
   end
   if(reject_packet)error<=ERR_VIEW_INACTIVE;
   else if(duplicate)begin end
   else if(packet_command==8'h50)begin
    if(packet_length!=0)error<=2;
    else if(!capture_complete)error<=4;
    else begin request<=!request;bank_valid<=0;end
   end else if(packet_command==8'h51)begin if(packet_length!=5)error<=2;end
   else if(packet_command==8'h52)begin if(packet_length!=30)error<=2;end
   else if(packet_command==8'h53)begin if(packet_length!=6)error<=2;end
   else if(C_VIEW_SWITCH && packet_command==CMD_SET_VIEW)begin if(packet_length!=7)error<=2;end
   else if(C_COMBINED && (packet_command==8'h60 || packet_command==8'h61))begin if(packet_length!=30)error<=2;end
   else if(packet_command==8'h54 || (C_VIEW_SWITCH && packet_command==CMD_READ_VIEW) || (C_COMBINED && packet_command==8'h62))begin
    if(packet_length!=0)error<=2;else if(control_pending)error<=4;
   end else error<=1;
  end
  ST_READ:begin
   incoming[read_index*8+:8]<=payload_data;
   read_index<=read_index+1'b1;address<=address+1'b1;
  end
  ST_VALIDATE:begin
   if(held_command==8'h51)begin
    requested_id<=incoming[31:0];page<=incoming[39:32];
    if(incoming[39:32]>3)error<=3;
    else if(!bank_valid)error<=5;
    else if(incoming[31:0]!=snapshot_id)error<=6;
   end else if(control_pending)error<=4;
   else if(write_id_seen && !write_key_matches)error<=7;
   else if(C_VIEW_SWITCH && write_id_seen && write_key_matches && held_command==CMD_SET_VIEW)
    ball_results_allowed<=last_write_reply[24] && sys_application_inspection;
   else if(C_VIEW_SWITCH && held_command==CMD_SET_VIEW && (incoming[55:48]>1 || incoming[47:46]!=0))error<=3;
  end
  ST_CHECK:begin
                                                                                  
   if(held_command==8'h60)begin
    case(check_index)
    0:if(incoming[55:48]>10 || incoming[63:56]>3)error<=3;
    1:if(incoming[79:64]>768 || incoming[111:96]>768)error<=3;
    2:if($signed(incoming[95:80]) < -128 || $signed(incoming[95:80]) > 128)error<=3;
    3:if(incoming[127:112]<20 || incoming[127:112]>300)error<=3;
    4:if(incoming[239:128]!=0)error<=3;
    default:begin end
    endcase
   end else if(held_command==8'h61)begin
    case(check_index)
    0:if(incoming[55:48]>1 || incoming[59:56]!=0 || incoming[71:64]!=16)error<=3;
    1:if(incoming[239:200]!=0)error<=3;
    default:begin end
    endcase
   end else case(check_index)
   0:if((incoming[55:49]!=0 && (incoming[55:49]<4 || incoming[55:49]>64)) ||
        incoming[71:64]>2 || incoming[79:72]>3)error<=3;
   1:if(incoming[95:80]<64 || incoming[95:80]>=incoming[127:112])error<=3;
   2:if(incoming[111:96]<160 || incoming[111:96]>=incoming[143:128])error<=3;
   3:if(incoming[127:112]>1216 || incoming[143:128]>640)error<=3;
   4:if(incoming[159:144]<4 || incoming[159:144]>incoming[175:160] || incoming[175:160]>1152)error<=3;
   5:if(incoming[191:176]<4 || incoming[191:176]>incoming[207:192] || incoming[207:192]>480)error<=3;
   6:if({1'b0,incoming[223:208]} < {1'b0,incoming[95:80]}+17'd16 ||
        {1'b0,incoming[223:208]}+17'd16 >= {1'b0,incoming[127:112]})error<=3;
   7:if(incoming[239:224]<16)error<=3;
   default:begin end
   endcase
   check_index<=check_index+1'b1;
  end
  ST_CAPTURE:begin
   if(capture_complete)begin
    bank_valid<=source_valid;snapshot_id<=snapshot_id==32'hffffffff ? 32'd1 : snapshot_id+1'b1;
    error<=source_valid?8'd0:8'd5;
   end else if(wait_count==TIMEOUT-1)error<=5;
   else wait_count<=wait_count+1'b1;
  end
  ST_CONTROL_START:begin
   control_data<=C_VIEW_SWITCH && held_command==CMD_SET_VIEW ? {184'd0,incoming[55:0]} :
      {(held_command==8'h52 ? canonical_config :
       ((held_command==8'h60 || held_command==8'h61)?incoming[239:48]:192'd0)),incoming[47:0]};
   control_command<=held_command;
   control_request<=!control_request;control_pending<=1;wait_count<=0;
  end
  ST_CONTROL_WAIT:begin
   if(control_complete)error<=control_error;
   else if(wait_count==TIMEOUT-1)error<=5;
   else wait_count<=wait_count+1'b1;
  end
  ST_BUILD:begin
   tx_seq<=held_seq;reply_prefix<=0;reply_panel<=0;reply_write_cache<=0;
   reply_prefix[7:0]<=held_command;reply_prefix[15:8]<=build_error;
   if(build_error!=0)begin tx_command<=8'h82;tx_length<=2;end
   else if(C_VIEW_SWITCH && (held_command==CMD_SET_VIEW || held_command==CMD_READ_VIEW))begin
    tx_command<=8'h81;tx_length<=11;reply_panel<=1;reply_write_cache<=held_command==CMD_SET_VIEW;
   end
   else if(held_command==8'h52 || held_command==8'h53 || held_command==8'h54 ||
       (C_COMBINED && (held_command==8'h60 || held_command==8'h61 || held_command==8'h62)))begin
    tx_command<=8'h81;tx_length<=42;reply_panel<=1;
    reply_write_cache<=held_command!=8'h54 && held_command!=8'h62;
   end else begin
    tx_command<=8'h81;tx_length<=57;
    reply_prefix[23:16]<=1;reply_prefix[31:24]<=page;reply_prefix[39:32]<=4;
    reply_prefix[71:40]<=snapshot_id;
   end
  end
  ST_REPLY:if(!tx_busy && !(reject_held && tx_command==8'h81))begin
   tx_start<=1;take<=1;
   cached<=1;cached_command<=held_command;cached_seq<=held_seq;
   cached_length<=held_length;cached_signature<=held_signature;
  end
  default:begin end
  endcase
 end end
endmodule
