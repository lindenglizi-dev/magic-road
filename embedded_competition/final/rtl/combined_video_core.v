                                                                                  
                                                                  
                                                                         
module combined_video_core #(parameter IMG_WIDTH=1280,IMG_HEIGHT=720,C_SHARED_INSPECTION_GAMMA=0,
 parameter BINARY_THRESHOLD=64,SOBEL_THRESHOLD=48,SHARPEN_DETAIL_SHIFT=2)(
 input wire [9:0] I_editor_saturation,input wire I_editor_we,I_editor_commit,
 input wire [7:0] I_editor_address,I_editor_value,
 input wire [9:0] I_tone_contrast,input wire signed [8:0] I_tone_brightness,
 input wire I_gamma_we,input wire [7:0] I_gamma_address,I_gamma_value,input wire I_gamma_commit,
 output wire O_busy,
 input wire I_uart_valid,input wire [3:0] I_uart_mode,
 input wire I_clk,I_rst_n,
 input wire [95:0] I_rgb,I_wb_rgb,input wire I_valid,I_user,I_last,
 output wire [95:0] O_rgb,output wire O_valid,O_user,O_last,O_done,
 output reg O_early,output wire O_error,output reg [3:0] active_mode);
                                                                           
                                                                              
                                                                        
 wire [95:0] rgb[0:9];wire [31:0] pixel[0:9];
 wire [9:0] valid,user_mark,last_mark,done;
 reg busy,overlap_error,input_first;
 reg [11:0] input_x,input_y;
 reg [10:0] finished;
 reg [5:0] drain;
 wire input_user=I_valid && (input_first || I_user);
 wire input_last=I_valid && (I_user?12'd0:input_x)==IMG_WIDTH/4-1;
 wire input_done=input_last && (I_user?12'd0:input_y)==IMG_HEIGHT-1;
 wire [95:0] base_rgb=(active_mode==1 || active_mode==10)?I_wb_rgb:I_rgb;
 always @(posedge I_clk or negedge I_rst_n)begin
  if(!I_rst_n)begin input_x<=0;input_y<=0;input_first<=1;end
  else begin
   if(I_user)begin input_x<=0;input_y<=0;input_first<=1;end
   if(I_valid)begin
    input_first<=0;
    if(input_last)begin input_x<=0;input_y<=input_y==IMG_HEIGHT-1?0:input_y+1'b1;end
    else input_x<=(I_user?12'd0:input_x)+1'b1;
   end
  end
 end
 wire [95:0] ball_rgb;wire ball_valid,ball_user,ball_last;
 reg ball_done;
 generate if(C_SHARED_INSPECTION_GAMMA)begin:gen_scalar_inspection_curve
                                                                            
  assign ball_rgb=(I_valid && active_mode==10)?I_wb_rgb:96'd0;
  assign ball_valid=I_valid && active_mode==10;
  assign ball_user=input_user && active_mode==10;
  assign ball_last=input_last && active_mode==10;
 end else begin:gen_parallel_inspection_curve
 axis_gamma_rgb96 u_inspection_gamma(.I_clk(I_clk),.I_rst_n(I_rst_n),
  .I_tdata(I_wb_rgb),.I_tvalid(I_valid && active_mode==10),
  .I_tuser(input_user && active_mode==10),.I_tlast(input_last && active_mode==10),
  .O_tdata(ball_rgb),.O_tvalid(ball_valid),.O_tuser(ball_user),.O_tlast(ball_last));
 end endgenerate
 always @(posedge I_clk or negedge I_rst_n)
  if(!I_rst_n)ball_done<=0;else ball_done<=input_done && active_mode==10;

 wire [95:0] input_group;wire [1:0] input_lane;
 wire scalar_valid,scalar_user,scalar_last,scalar_done,input_busy,input_error;
 quad_group_serializer #(.C_DATA_BITS(96)) u_input_fifo(
  .clk(I_clk),.rst_n(I_rst_n),.data(base_rgb),.valid(I_valid && active_mode!=10),
  .user_mark(input_user),.last_mark(input_last),.done(input_done),
  .group_data(input_group),.lane(input_lane),.ov(scalar_valid),.ou(scalar_user),.ol(scalar_last),.od(scalar_done),
  .busy(input_busy),.error(input_error),.level());
 wire [23:0] scalar_rgb=input_group[95-input_lane*24-:24];
 wire [31:0] gray;wire gv,gu,gl;
 rgb2gray_96 u_gray(.I_clk(I_clk),.I_rst_n(I_rst_n),.I_tdata({72'd0,scalar_rgb}),
  .I_tvalid(scalar_valid),.I_tuser(scalar_user),.I_tlast(scalar_last),
  .O_gray_data(gray),.O_tdata(),.O_tvalid(gv),.O_tuser(gu),.O_tlast(gl));
 reg [23:0] raw0,raw1,raw2;
 reg [2:0] done_delay;
 always @(posedge I_clk or negedge I_rst_n)begin
  if(!I_rst_n)begin raw0<=0;raw1<=0;raw2<=0;done_delay<=0;end
  else begin raw0<=scalar_rgb;raw1<=raw0;raw2<=raw1;done_delay<={done_delay[1:0],scalar_done};end
 end
 wire gd=done_delay[2];
 assign rgb[0]={72'd0,raw2};assign rgb[1]={72'd0,raw2};
 assign valid[0]=gv;assign valid[1]=gv;assign user_mark[0]=gu;assign user_mark[1]=gu;
 assign last_mark[0]=gl;assign last_mark[1]=gl;assign done[0]=gd;assign done[1]=gd;
 wire pv,pu,pl,pd;
 rgb_point_adjust_4px #(.BINARY_THRESHOLD(BINARY_THRESHOLD)) u_point(
  .clk(I_clk),.rst_n(I_rst_n),.rgb({72'd0,raw2}),.gray(gray),.valid(gv),.user_mark(gu),.last_mark(gl),.done(gd),
  .binary_rgb(rgb[2]),.binary_gray(pixel[2]),.gamma_rgb(),.contrast_rgb(),.brightness_rgb(),.saturation_rgb(),
  .ov(pv),.ou(pu),.ol(pl),.od(pd));
 assign valid[2]=pv;assign user_mark[2]=pu;assign last_mark[2]=pl;assign done[2]=pd;
                                                                          
 wire [7:0] window_pixels[0:8];
 wire window_valid,window_user,window_last,window_done,window_busy,window_error;
 wire scalar_window;wire queue_error=1'b0;
 wire [31:0] sp11,sp12,sp13,sp21,sp22,sp23,sp31,sp32,sp33;
 line_buffer_3x3_scalar #(.IMG_WIDTH(IMG_WIDTH),.IMG_HEIGHT(IMG_HEIGHT)) u_window(
 .I_clk(I_clk),.I_rst_n(I_rst_n),.I_gray_data(gray[7:0]),.I_tvalid(gv),.I_tuser(gu),.I_tlast(gl),
 .O_p11(window_pixels[0]),.O_p12(window_pixels[1]),.O_p13(window_pixels[2]),
 .O_p21(window_pixels[3]),.O_p22(window_pixels[4]),.O_p23(window_pixels[5]),
 .O_p31(window_pixels[6]),.O_p32(window_pixels[7]),.O_p33(window_pixels[8]),
 .O_window_valid(scalar_window),.O_tvalid(window_valid),.O_tuser(window_user),.O_tlast(window_last),
 .O_frame_done(window_done),.O_x(),.O_y(),.O_protocol_error(window_error),.O_busy(window_busy));
 assign sp11={24'd0,window_pixels[0]};
 assign sp12={24'd0,window_pixels[1]};
 assign sp13={24'd0,window_pixels[2]};
 assign sp21={24'd0,window_pixels[3]};
 assign sp22={24'd0,window_pixels[4]};
 assign sp23={24'd0,window_pixels[5]};
 assign sp31={24'd0,window_pixels[6]};
 assign sp32={24'd0,window_pixels[7]};
 assign sp33={24'd0,window_pixels[8]};
 wire [3:0] scalar_mask={3'd0,scalar_window};

gray_median_4px u_mode3(.I_clk(I_clk),.I_rst_n(I_rst_n),.I_p11(sp11),.I_p12(sp12),.I_p13(sp13),.I_p21(sp21),.I_p22(sp22),.I_p23(sp23),.I_p31(sp31),.I_p32(sp32),.I_p33(sp33),.I_tvalid(window_valid),.I_tuser(window_user),.I_tlast(window_last),.I_frame_done(window_done),.I_x(12'd0),.I_y(12'd0),.I_window_valid(scalar_mask),.O_pixel_data(pixel[3]),.O_tdata(rgb[3]),.O_tvalid(valid[3]),.O_tuser(user_mark[3]),.O_tlast(last_mark[3]),.O_frame_done(done[3]),.O_x(),.O_y(),.O_window_valid());
sobel_edge_4px #(.THRESHOLD(SOBEL_THRESHOLD)) u_mode4(.I_clk(I_clk),.I_rst_n(I_rst_n),.I_p11(sp11),.I_p12(sp12),.I_p13(sp13),.I_p21(sp21),.I_p22(sp22),.I_p23(sp23),.I_p31(sp31),.I_p32(sp32),.I_p33(sp33),.I_tvalid(window_valid),.I_tuser(window_user),.I_tlast(window_last),.I_frame_done(window_done),.I_x(12'd0),.I_y(12'd0),.I_window_valid(scalar_mask),.O_edge_data(pixel[4]),.O_tdata(rgb[4]),.O_tvalid(valid[4]),.O_tuser(user_mark[4]),.O_tlast(last_mark[4]),.O_frame_done(done[4]),.O_x(),.O_y(),.O_window_valid(),.O_gx(),.O_gy(),.O_magnitude());
gray_sharpen_4px #(.DETAIL_SHIFT(SHARPEN_DETAIL_SHIFT)) u_mode5(.I_clk(I_clk),.I_rst_n(I_rst_n),.I_p11(sp11),.I_p12(sp12),.I_p13(sp13),.I_p21(sp21),.I_p22(sp22),.I_p23(sp23),.I_p31(sp31),.I_p32(sp32),.I_p33(sp33),.I_tvalid(window_valid),.I_tuser(window_user),.I_tlast(window_last),.I_frame_done(window_done),.I_x(12'd0),.I_y(12'd0),.I_window_valid(scalar_mask),.O_pixel_data(pixel[5]),.O_tdata(rgb[5]),.O_tvalid(valid[5]),.O_tuser(user_mark[5]),.O_tlast(last_mark[5]),.O_frame_done(done[5]),.O_x(),.O_y(),.O_window_valid());
 wire tv,tu,tl,td;
 combined_tone_4px u_tone(.clk(I_clk),.rst_n(I_rst_n),.rgb({72'd0,raw2}),
 .valid(gv),.user_mark(gu),.last_mark(gl),.done(gd),.mode(active_mode),.gray(gray),.edit_saturation(I_editor_saturation),
 .editor_we(I_editor_we),.editor_commit(I_editor_commit),
 .curve_address(I_gamma_we?I_gamma_address:I_editor_address),.curve_value(I_gamma_we?I_gamma_value:I_editor_value),
 .gamma_we(I_gamma_we),.gamma_commit(I_gamma_commit),.contrast_q8(I_tone_contrast),.brightness(I_tone_brightness),
 .editor_rgb(rgb[9]),.ev(valid[9]),.eu(user_mark[9]),.el(last_mark[9]),.ed(done[9]),
 .gamma_rgb(rgb[6]),.contrast_rgb(rgb[7]),.brightness_rgb(rgb[8]),.ov(tv),.ou(tu),.ol(tl),.od(td));
 assign valid[6]=tv;assign valid[7]=tv;assign valid[8]=tv;
 assign user_mark[6]=tu;assign user_mark[7]=tu;assign user_mark[8]=tu;
 assign last_mark[6]=tl;assign last_mark[7]=tl;assign last_mark[8]=tl;
 assign done[6]=td;assign done[7]=td;assign done[8]=td;
 reg [23:0] selected_rgb;
 reg sv,su,sl,sd;
 always @(posedge I_clk or negedge I_rst_n)begin
  if(!I_rst_n)begin selected_rgb<=0;sv<=0;su<=0;sl<=0;sd<=0;end
  else begin
   selected_rgb<=rgb[active_mode<=9?active_mode:0][23:0];
   sv<=active_mode<=9 && valid[active_mode];su<=active_mode<=9 && user_mark[active_mode];
   sl<=active_mode<=9 && last_mark[active_mode];sd<=active_mode<=9 && done[active_mode];
  end
 end
 reg [71:0] output_shift;
 reg [1:0] output_lane;
 reg output_first;
 reg [95:0] demo_rgb;
 reg demo_valid,demo_user,demo_last,demo_done;
 always @(posedge I_clk or negedge I_rst_n)begin
  if(!I_rst_n)begin
   output_shift<=0;output_lane<=0;output_first<=0;demo_rgb<=0;
   demo_valid<=0;demo_user<=0;demo_last<=0;demo_done<=0;
  end else begin
   demo_valid<=0;demo_user<=0;demo_last<=0;demo_done<=0;
   if(sv)begin
    output_shift<={output_shift[47:0],selected_rgb};
    if(output_lane==0)output_first<=su;
    if(output_lane==3)begin
     demo_rgb<={output_shift,selected_rgb};demo_valid<=1;demo_user<=output_first;
     demo_last<=sl;demo_done<=sd;output_lane<=0;
    end else output_lane<=output_lane+1'b1;
   end
  end
 end
 wire [10:0] completed={ball_done,done};
 always @(posedge I_clk or negedge I_rst_n)begin
  if(!I_rst_n)begin active_mode<=10;O_early<=0;busy<=0;overlap_error<=0;finished<=0;drain<=0;end
  else begin
   O_early<=I_user;
   if(busy)begin
    finished<=finished|completed;
    if(drain!=0)begin drain<=drain-1'b1;if(drain==1)busy<=0;end
    else if(active_mode==10 ? (finished[10]||ball_done) : (&(finished[9:0]|done)))drain<=40;
   end
   if(I_user)begin
    if(busy)overlap_error<=1;
    else begin active_mode<=I_uart_mode;busy<=1;finished<=0;drain<=0;end
   end
  end
 end
 assign O_rgb=active_mode==10?ball_rgb:demo_rgb;
 assign O_valid=active_mode==10?ball_valid:demo_valid;
 assign O_user=active_mode==10?ball_user:demo_user;
 assign O_last=active_mode==10?ball_last:demo_last;
 assign O_done=active_mode==10?ball_done:demo_done;
 assign O_busy=busy;
 assign O_error=overlap_error || input_error || queue_error || window_error;
endmodule
