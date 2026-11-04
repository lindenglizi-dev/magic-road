`timescale 1ns / 1ps
                                                                                    
module ball_color_group_serial #(
 parameter C_WIDTH=1280,C_HEIGHT=720,C_X_MIN=64,C_Y_MIN=160,C_X_END=1216,C_Y_END=640,
 parameter C_PANEL_CONFIG=0,C_CHECK_LAST=0,C_SHARED_GAMMA=0
)(
 input i_apply_gamma,i_display_source_gamma,
 input i_clk,i_rstn,input [95:0] i_rgb,i_display_rgb,input i_valid,i_early,i_last,i_strict,
 input [15:0] i_epoch,input [191:0] i_settings,
 output reg [95:0] o_display_rgb,output reg o_valid,o_sof,o_eol,o_eof,
 output reg [15:0] o_epoch,output reg [51:0] o_control,
 output reg [7:0] o_strong,o_weak,output reg [3:0] o_inside,o_highlight,
 output o_error,o_capture_fault,o_busy,output [9:0] o_level
);
    function [1:0] classify;
        input [23:0] pixel;
        input tight;
        reg [8:0] red, green, blue, floor_value, margin;
        reg [10:0] red_four, green_four, blue_five, red_five, green_five;
        begin
            red = {1'b0,pixel[23:16]};
            green = {1'b0,pixel[15:8]};
            blue = {1'b0,pixel[7:0]};
            floor_value = tight ? 9'd150 : 9'd100;
            margin = tight ? 9'd50 : 9'd30;
            red_four = {2'd0,red} << 2;
            green_four = {2'd0,green} << 2;
            blue_five = ({2'd0,blue} << 2)+blue;
            red_five = red_four+red;
            green_five = green_four+green;
            classify = 0;
            if(!tight)begin
                // 五比四的颜色优势及12级色差拒绝灰白与青色背景。
                // 黄与红绿使用互补边界，避免暗红被黄优先规则吞掉。
                if(red >= 64 && green >= 64 && red > blue+9'd12 && green > blue+9'd12 &&
                   red_four > blue_five && green_four > blue_five &&
                   red_four <= green_five && green_four <= red_five)begin
                    classify = 2;
                end else if(red >= 64 && red > green+9'd12 && red > blue+9'd12 &&
                            red_four > green_five && red_four > blue_five)begin
                    classify = 1;
                end else if(green >= 64 && green > red+9'd12 && green > blue+9'd12 &&
                            green_four > red_five && green_four > blue_five)begin
                    classify = 3;
                end
            end else if(red >= floor_value && green >= floor_value && red > blue+margin &&
               green > blue+margin && red+9'd60 >= green && green+9'd60 >= red)begin
                classify = 2;
            end else if(red >= floor_value && red > green+margin && red > blue+margin)begin
                classify = 1;
            end else if(green >= floor_value && green > red+margin && green > blue+margin)begin
                classify = 3;
            end
        end
    endfunction
    function [1:0] classify_weak;
        input [23:0] pixel;
        reg [8:0] red,green,blue;
        reg [11:0] red_eight,green_eight,red_nine,green_nine,blue_nine;
        reg [10:0] red_four,green_four,red_five,green_five;
        begin
            red={1'b0,pixel[23:16]};green={1'b0,pixel[15:8]};blue={1'b0,pixel[7:0]};
            red_eight={3'd0,red} << 3;green_eight={3'd0,green} << 3;
            red_nine=red_eight+red;green_nine=green_eight+green;
            blue_nine=({3'd0,blue} << 3)+blue;
            red_four={2'd0,red} << 2;green_four={2'd0,green} << 2;
            red_five=red_four+red;green_five=green_four+green;
            classify_weak=0;
            if(red>=32 && green>=32 && red>blue+9'd6 && green>blue+9'd6 &&
               red_eight>blue_nine && green_eight>blue_nine &&
               red_four<=green_five && green_four<=red_five)begin classify_weak=2;end
            else if(red>=32 && red>green+9'd6 && red>blue+9'd6 &&
                    red_eight>green_nine && red_eight>blue_nine)begin classify_weak=1;end
            else if(green>=32 && green>red+9'd6 && green>blue+9'd6 &&
                    green_eight>red_nine && green_eight>blue_nine)begin classify_weak=3;end
        end
    endfunction
    function [15:0] highlight_bounds;
        input [23:0] pixel;
        reg [7:0] minimum,maximum;
        begin
            minimum=pixel[23:16];maximum=minimum;
            if(pixel[15:8]<minimum)minimum=pixel[15:8];
            if(pixel[7:0]<minimum)minimum=pixel[7:0];
            if(pixel[15:8]>maximum)maximum=pixel[15:8];
            if(pixel[7:0]>maximum)maximum=pixel[7:0];
            highlight_bounds={maximum,minimum};
        end
    endfunction
 reg [11:0] capture_x,capture_y;
 reg capture_active,capture_pending,capture_bad,source_error,fault_first,fault_second;
 wire [11:0] input_x=i_early?12'd0:capture_x,input_y=i_early?12'd0:capture_y;
 wire accept=i_valid && (capture_active || i_early) && !i_early;
 wire end_line=input_x==C_WIDTH-4;
 wire end_frame=end_line && input_y==C_HEIGHT-1;
 wire line_fault=C_CHECK_LAST && i_valid && (capture_active || i_early) && i_last!=end_line;
 wire [51:0] control={i_settings[91:80],i_settings[75:64],i_settings[59:48],i_settings[43:32],
                      i_settings[9:8],(C_PANEL_CONFIG?i_settings[24]:i_strict),i_settings[0]};
 wire [261:0] payload;
 wire [1:0] queue_lane;
 wire queue_valid,queue_sof,queue_eol,queue_eof,queue_busy,queue_error;
 quad_group_serializer #(.C_DATA_BITS(262),.C_SYNCHRONOUS_FLUSH(1)) queue(
  .clk(i_clk),.rst_n(i_rstn),.clear(i_early),.data({(C_SHARED_GAMMA && i_apply_gamma),(C_SHARED_GAMMA && i_display_source_gamma),i_rgb,i_display_rgb,i_epoch,control}),
  .valid(accept),.user_mark(capture_pending),.last_mark(i_last),.done(end_frame),
  .group_data(payload),.lane(queue_lane),.ov(queue_valid),.ou(queue_sof),.ol(queue_eol),.od(queue_eof),
  .busy(queue_busy),.error(queue_error),.level(o_level));
 wire [23:0] queued_pixel=payload[259-queue_lane*24-:24];
 wire [23:0] queued_display=payload[163-queue_lane*24-:24];
 wire [23:0] pixel,display_pixel;
 wire [51:0] pixel_control;
 wire [15:0] pixel_epoch;
 wire [1:0] lane;
 wire valid,sof,eol,eof;
 generate if(C_SHARED_GAMMA)begin:gen_shared_gamma
                                                                          
  (* ram_style="block" *) reg [7:0] curve_red_green[0:511];
  (* ram_style="block" *) reg [7:0] curve_blue[0:511];
  reg [7:0] reg_red,reg_green,reg_blue;
  reg [23:0] reg_source,reg_display;
  reg [51:0] reg_control;
  reg [15:0] reg_epoch;
  reg [1:0] reg_lane;
  reg [3:0] reg_markers;
  reg flag_apply,flag_display_source;
  initial begin
   $readmemh("../rtl/gamma_fixed.mem",curve_red_green);
   $readmemh("../rtl/gamma_fixed.mem",curve_blue);
  end
  always @(posedge i_clk)begin
   reg_red<=curve_red_green[{1'b0,queued_pixel[23:16]}];
   reg_green<=curve_red_green[{1'b0,queued_pixel[15:8]}];
   reg_blue<=curve_blue[{1'b0,queued_pixel[7:0]}];
   reg_source<=queued_pixel;reg_display<=queued_display;
   reg_control<=payload[51:0];reg_epoch<=payload[67:52];reg_lane<=queue_lane;
  end
  always @(posedge i_clk or negedge i_rstn)begin
   if(!i_rstn)begin reg_markers<=0;flag_apply<=0;flag_display_source<=0;end
   else if(i_early)begin reg_markers<=0;flag_apply<=0;flag_display_source<=0;end
   else begin
    reg_markers<={queue_valid,queue_sof,queue_eol,queue_eof};
    flag_apply<=payload[261];flag_display_source<=payload[260];
   end
  end
  assign pixel=flag_apply?{reg_red,reg_green,reg_blue}:reg_source;
                                                                         
  assign display_pixel=flag_display_source?pixel:reg_display;
  assign pixel_control=reg_control;assign pixel_epoch=reg_epoch;assign lane=reg_lane;
  assign {valid,sof,eol,eof}=reg_markers;
 end else begin:gen_original_curve_input
  assign pixel=queued_pixel;assign display_pixel=queued_display;
  assign pixel_control=payload[51:0];assign pixel_epoch=payload[67:52];assign lane=queue_lane;
  assign {valid,sof,eol,eof}={queue_valid,queue_sof,queue_eol,queue_eof};
 end endgenerate
 reg [11:0] group_x,group_y;
 wire [11:0] current_x=sof?12'd0:group_x,current_y=sof?12'd0:group_y;
 wire [12:0] pixel_x={1'b0,current_x}+{11'd0,lane};
 wire inside=pixel_x>=C_X_MIN && pixel_x<C_X_END && current_y>=C_Y_MIN && current_y<C_Y_END &&
     (!C_PANEL_CONFIG || (pixel_control[0] && pixel_x>={1'b0,pixel_control[15:4]} &&
      pixel_x<{1'b0,pixel_control[39:28]} && current_y>=pixel_control[27:16] && current_y<pixel_control[51:40]));
 wire [15:0] bounds=highlight_bounds(pixel);
 wire highlighted=bounds[7:0]>=160 && {1'b0,bounds[15:8]}<={1'b0,bounds[7:0]}+9'd24;
 reg scalar_valid,scalar_sof,scalar_eol,scalar_eof,scalar_inside,scalar_highlight;
 reg [1:0] scalar_lane,scalar_strong,scalar_weak;
 reg [23:0] scalar_display;
 reg [15:0] scalar_epoch;
 reg [51:0] scalar_control;
 reg [71:0] gather_rgb;
 reg [7:0] gather_strong,gather_weak;
 reg [3:0] gather_inside,gather_highlight;
 reg gather_sof,gather_pending;
 wire busy=queue_busy || valid || scalar_valid || gather_pending || o_valid;
 assign o_busy=busy;
 assign o_error=source_error;
 assign o_capture_fault=fault_second;
                                                                           
                                                                                  
 always @(posedge i_clk or negedge i_rstn)begin
  if(!i_rstn)begin
   capture_x<=0;capture_y<=0;capture_active<=0;capture_pending<=0;capture_bad<=0;
   source_error<=0;fault_first<=0;fault_second<=0;
  end else begin
   fault_first<=0;fault_second<=fault_first;
   if(i_early)begin
    capture_x<=0;capture_y<=0;capture_active<=1;capture_pending<=1;capture_bad<=0;
    source_error<=0;
    if((capture_active && !capture_bad) || busy || i_valid)begin
     source_error<=1;fault_first<=1;
    end
   end
   if(line_fault && (i_early || !capture_bad))begin source_error<=1;capture_bad<=1;fault_first<=1;end
   if(queue_error && !capture_bad)begin source_error<=1;capture_bad<=1;fault_first<=1;end
   if(accept)begin
    capture_pending<=0;
    if(end_line)begin
     capture_x<=0;
     if(end_frame)begin capture_y<=0;capture_active<=0;end
     else capture_y<=input_y+1'b1;
    end else capture_x<=input_x+12'd4;
   end
  end
 end
                                                                               
                                                                              
 always @(posedge i_clk or negedge i_rstn)begin
  if(!i_rstn)begin
   group_x<=0;group_y<=0;scalar_valid<=0;scalar_sof<=0;scalar_eol<=0;scalar_eof<=0;
   scalar_lane<=0;scalar_strong<=0;scalar_weak<=0;scalar_inside<=0;scalar_highlight<=0;
   scalar_display<=0;scalar_epoch<=0;scalar_control<=0;
  end else if(i_early)begin
   group_x<=0;group_y<=0;scalar_valid<=0;scalar_sof<=0;scalar_eol<=0;scalar_eof<=0;
  end else begin
   scalar_valid<=valid;scalar_sof<=sof;scalar_eol<=eol;scalar_eof<=eof;scalar_lane<=lane;
   scalar_strong<=inside?classify(pixel,pixel_control[1]):2'd0;
   scalar_weak<=inside?classify_weak(pixel):2'd0;
   scalar_inside<=C_PANEL_CONFIG?inside:1'b1;scalar_highlight<=highlighted;
   scalar_display<=display_pixel;scalar_epoch<=pixel_epoch;scalar_control<=pixel_control;
   if(sof)begin group_x<=0;group_y<=0;end
   if(valid && lane==3)begin
    if(current_x==C_WIDTH-4)begin group_x<=0;group_y<=current_y==C_HEIGHT-1?0:current_y+1'b1;end
    else group_x<=current_x+12'd4;
   end
  end
 end
 always @(posedge i_clk or negedge i_rstn)begin
  if(!i_rstn)begin
   gather_rgb<=0;gather_strong<=0;gather_weak<=0;gather_inside<=0;gather_highlight<=0;gather_sof<=0;gather_pending<=0;
   o_display_rgb<=0;o_valid<=0;o_sof<=0;o_eol<=0;o_eof<=0;o_epoch<=0;o_control<=0;
   o_strong<=0;o_weak<=0;o_inside<=0;o_highlight<=0;
  end else if(i_early)begin
   gather_pending<=0;o_valid<=0;o_sof<=0;o_eol<=0;o_eof<=0;
  end else begin
   o_valid<=0;o_sof<=0;o_eol<=0;o_eof<=0;
   if(scalar_valid)begin
    gather_rgb<={gather_rgb[47:0],scalar_display};
    gather_strong[scalar_lane*2+:2]<=scalar_strong;gather_weak[scalar_lane*2+:2]<=scalar_weak;
    gather_inside[scalar_lane]<=scalar_inside;gather_highlight[scalar_lane]<=scalar_highlight;
    if(scalar_lane==0)begin gather_sof<=scalar_sof;gather_pending<=1;end
    if(scalar_lane==3)begin
     gather_pending<=0;o_valid<=1;o_sof<=gather_sof;o_eol<=scalar_eol;o_eof<=scalar_eof;
     o_display_rgb<={gather_rgb,scalar_display};o_epoch<=scalar_epoch;o_control<=scalar_control;
     o_strong<={scalar_strong,gather_strong[5:0]};o_weak<={scalar_weak,gather_weak[5:0]};
     o_inside<={scalar_inside,gather_inside[2:0]};o_highlight<={scalar_highlight,gather_highlight[2:0]};
    end
   end
  end
 end
endmodule
