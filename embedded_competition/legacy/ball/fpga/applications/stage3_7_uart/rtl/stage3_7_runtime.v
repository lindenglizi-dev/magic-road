// Configured graph: original 0, algorithms 1..11. All streams carry their own markers.
module stage3_7_runtime #(parameter IMG_WIDTH=1280,IMG_HEIGHT=720,DEBOUNCE_CYCLES=2100000)(
 input wire [95:0] I_roi_config,
 output wire O_busy,
 input wire I_uart_valid,input wire [3:0] I_uart_mode,
 input wire I_clk,I_rst_n,input wire [3:0] I_keys_n,
 input wire [95:0] I_rgb,I_wb_rgb,input wire I_valid,I_user,I_last,
 output wire [127:0] O_data,output wire O_valid,O_last,O_done,
 output reg O_early,output wire O_error,output reg [3:0] active_mode);
 wire [3:0] requested_mode;
 key_mode_control #(.DEBOUNCE_CYCLES(DEBOUNCE_CYCLES)) u_keys(
 .uart_valid(I_uart_valid),.uart_mode(I_uart_mode),.clk(I_clk),.rst_n(I_rst_n),
 .unlocked(active_mode!=0),.keys_n(I_keys_n),.mode(requested_mode));
 wire [95:0] rgb[0:11];wire [31:0] pixel[0:11];
 wire [11:0] valid,user_mark,last_mark,done;wire [3:0] errors;
 reg pending,busy,overlap_error;reg [11:0] gx,gy,finished;reg [3:0] drain;
 wire gv,gu;wire [31:0] gray;
 rgb2gray_96 u_gray(.I_clk(I_clk),.I_rst_n(I_rst_n),.I_tdata(I_rgb),.I_tvalid(I_valid),.I_tuser(I_user),.I_tlast(I_last),
 .O_gray_data(gray),.O_tdata(),.O_tvalid(gv),.O_tuser(gu),.O_tlast());
 always @(posedge I_clk or negedge I_rst_n)begin
 if(!I_rst_n)begin pending<=0;gx<=0;gy<=0;end else begin
 if(gu)begin pending<=1;gx<=0;gy<=0;end
 if(gv)begin pending<=0;
 if((gu?12'd0:gx)==IMG_WIDTH/4-1)begin gx<=0;gy<=gy==IMG_HEIGHT-1?0:gy+1'b1;end
 else gx<=(gu?12'd0:gx)+1'b1;
 end end end
 wire guser=gv&&(pending||gu),glast=gv&&(gx==IMG_WIDTH/4-1);
 wire gdone=glast&&(gy==IMG_HEIGHT-1);
 reg [95:0] raw0,raw1,raw2,wb0,wb1,wb2;
 always @(posedge I_clk or negedge I_rst_n)begin
 if(!I_rst_n)begin raw0<=0;raw1<=0;raw2<=0;wb0<=0;wb1<=0;wb2<=0;end
 else begin raw0<=I_rgb;raw1<=raw0;raw2<=raw1;wb0<=I_wb_rgb;wb1<=wb0;wb2<=wb1;end end
 assign rgb[0]=raw2;assign rgb[1]=wb2;
 assign valid[0]=gv;assign valid[1]=gv;
 assign user_mark[0]=guser;assign user_mark[1]=guser;
 assign last_mark[0]=glast;assign last_mark[1]=glast;
 assign done[0]=gdone;assign done[1]=gdone;
 // Every branch must finish; then drain MUX, OSD and pack before accepting a new frame.
 always @(posedge I_clk or negedge I_rst_n)begin
 if(!I_rst_n)begin active_mode<=0;O_early<=0;busy<=0;overlap_error<=0;finished<=0;drain<=0;end
 else begin
 O_early<=I_user;
 if(busy)begin
 finished<=finished|done;
 if(drain!=0)begin drain<=drain-1'b1;if(drain==1)busy<=0;end
 else if(&(finished|done))drain<=8;
 end
 if(I_user)begin
 if(busy)overlap_error<=1;
 else begin active_mode<=requested_mode;busy<=1;finished<=0;drain<=0;end
 end end end
 wire pv,pu,pl,pd;
 rgb_point_adjust_4px u_point(.clk(I_clk),.rst_n(I_rst_n),.rgb(raw2),.gray(gray),
 .valid(gv),.user_mark(guser),.last_mark(glast),.done(gdone),
 .binary_rgb(rgb[2]),.binary_gray(pixel[2]),.gamma_rgb(rgb[6]),.contrast_rgb(rgb[7]),
 .brightness_rgb(rgb[8]),.saturation_rgb(rgb[9]),.ov(pv),.ou(pu),.ol(pl),.od(pd));
assign valid[2]=pv;assign user_mark[2]=pu;assign last_mark[2]=pl;assign done[2]=pd;
assign valid[6]=pv;assign user_mark[6]=pu;assign last_mark[6]=pl;assign done[6]=pd;
assign valid[7]=pv;assign user_mark[7]=pu;assign last_mark[7]=pl;assign done[7]=pd;
assign valid[8]=pv;assign user_mark[8]=pu;assign last_mark[8]=pl;assign done[8]=pd;
assign valid[9]=pv;assign user_mark[9]=pu;assign last_mark[9]=pl;assign done[9]=pd;
wire [31:0] wp11,wp12,wp13,wp21,wp22,wp23,wp31,wp32,wp33;
wire wv,wu,wl,wd;wire [11:0] wx,wy;wire [3:0] wm;
line_buffer_3x3_4px #(.IMG_WIDTH(IMG_WIDTH),.IMG_HEIGHT(IMG_HEIGHT)) u_wwindow(.I_clk(I_clk),.I_rst_n(I_rst_n),.I_gray_data(gray),.I_tvalid(gv),.I_tuser(guser),.I_tlast(glast),.O_p11(wp11),.O_p12(wp12),.O_p13(wp13),.O_p21(wp21),.O_p22(wp22),.O_p23(wp23),.O_p31(wp31),.O_p32(wp32),.O_p33(wp33),.O_tvalid(wv),.O_tuser(wu),.O_tlast(wl),.O_frame_done(wd),.O_x(wx),.O_y(wy),.O_window_valid(wm),.O_protocol_error(errors[0]),.O_busy());
gray_median_4px u_mode3(.I_clk(I_clk),.I_rst_n(I_rst_n),.I_p11(wp11),.I_p12(wp12),.I_p13(wp13),.I_p21(wp21),.I_p22(wp22),.I_p23(wp23),.I_p31(wp31),.I_p32(wp32),.I_p33(wp33),.I_tvalid(wv),.I_tuser(wu),.I_tlast(wl),.I_frame_done(wd),.I_x(wx),.I_y(wy),.I_window_valid(wm),.O_pixel_data(pixel[3]),.O_tdata(rgb[3]),.O_tvalid(valid[3]),.O_tuser(user_mark[3]),.O_tlast(last_mark[3]),.O_frame_done(done[3]),.O_x(),.O_y(),.O_window_valid());
sobel_edge_4px u_mode4(.I_clk(I_clk),.I_rst_n(I_rst_n),.I_p11(wp11),.I_p12(wp12),.I_p13(wp13),.I_p21(wp21),.I_p22(wp22),.I_p23(wp23),.I_p31(wp31),.I_p32(wp32),.I_p33(wp33),.I_tvalid(wv),.I_tuser(wu),.I_tlast(wl),.I_frame_done(wd),.I_x(wx),.I_y(wy),.I_window_valid(wm),.O_edge_data(pixel[4]),.O_tdata(rgb[4]),.O_tvalid(valid[4]),.O_tuser(user_mark[4]),.O_tlast(last_mark[4]),.O_frame_done(done[4]),.O_x(),.O_y(),.O_window_valid(),.O_gx(),.O_gy(),.O_magnitude());
gray_sharpen_4px u_mode5(.I_clk(I_clk),.I_rst_n(I_rst_n),.I_p11(wp11),.I_p12(wp12),.I_p13(wp13),.I_p21(wp21),.I_p22(wp22),.I_p23(wp23),.I_p31(wp31),.I_p32(wp32),.I_p33(wp33),.I_tvalid(wv),.I_tuser(wu),.I_tlast(wl),.I_frame_done(wd),.I_x(wx),.I_y(wy),.I_window_valid(wm),.O_pixel_data(pixel[5]),.O_tdata(rgb[5]),.O_tvalid(valid[5]),.O_tuser(user_mark[5]),.O_tlast(last_mark[5]),.O_frame_done(done[5]),.O_x(),.O_y(),.O_window_valid());
wire [31:0] bp11,bp12,bp13,bp21,bp22,bp23,bp31,bp32,bp33;
wire bv,bu,bl,bd;wire [11:0] bx,by;wire [3:0] bm;
line_buffer_3x3_4px #(.IMG_WIDTH(IMG_WIDTH),.IMG_HEIGHT(IMG_HEIGHT)) u_bwindow(.I_clk(I_clk),.I_rst_n(I_rst_n),.I_gray_data(pixel[2]),.I_tvalid(pv),.I_tuser(pu),.I_tlast(pl),.O_p11(bp11),.O_p12(bp12),.O_p13(bp13),.O_p21(bp21),.O_p22(bp22),.O_p23(bp23),.O_p31(bp31),.O_p32(bp32),.O_p33(bp33),.O_tvalid(bv),.O_tuser(bu),.O_tlast(bl),.O_frame_done(bd),.O_x(bx),.O_y(by),.O_window_valid(bm),.O_protocol_error(errors[1]),.O_busy());
wire [31:0] eroded,dilated;wire ev,eu,el,ed,dv,du,dl,dd;
binary_erosion_4px u_erode_first(.I_clk(I_clk),.I_rst_n(I_rst_n),.I_p11(bp11),.I_p12(bp12),.I_p13(bp13),.I_p21(bp21),.I_p22(bp22),.I_p23(bp23),.I_p31(bp31),.I_p32(bp32),.I_p33(bp33),.I_tvalid(bv),.I_tuser(bu),.I_tlast(bl),.I_frame_done(bd),.I_x(bx),.I_y(by),.I_window_valid(bm),.O_binary_data(eroded),.O_tdata(),.O_tvalid(ev),.O_tuser(eu),.O_tlast(el),.O_frame_done(ed),.O_x(),.O_y(),.O_window_valid());
binary_dilation_4px u_dilate_first(.I_clk(I_clk),.I_rst_n(I_rst_n),.I_p11(bp11),.I_p12(bp12),.I_p13(bp13),.I_p21(bp21),.I_p22(bp22),.I_p23(bp23),.I_p31(bp31),.I_p32(bp32),.I_p33(bp33),.I_tvalid(bv),.I_tuser(bu),.I_tlast(bl),.I_frame_done(bd),.I_x(bx),.I_y(by),.I_window_valid(bm),.O_binary_data(dilated),.O_tdata(),.O_tvalid(dv),.O_tuser(du),.O_tlast(dl),.O_frame_done(dd),.O_x(),.O_y(),.O_window_valid());
wire [31:0] ewp11,ewp12,ewp13,ewp21,ewp22,ewp23,ewp31,ewp32,ewp33;
wire ewv,ewu,ewl,ewd;wire [11:0] ewx,ewy;wire [3:0] ewm;
line_buffer_3x3_4px #(.IMG_WIDTH(IMG_WIDTH),.IMG_HEIGHT(IMG_HEIGHT)) u_ewwindow(.I_clk(I_clk),.I_rst_n(I_rst_n),.I_gray_data(eroded),.I_tvalid(ev),.I_tuser(eu),.I_tlast(el),.O_p11(ewp11),.O_p12(ewp12),.O_p13(ewp13),.O_p21(ewp21),.O_p22(ewp22),.O_p23(ewp23),.O_p31(ewp31),.O_p32(ewp32),.O_p33(ewp33),.O_tvalid(ewv),.O_tuser(ewu),.O_tlast(ewl),.O_frame_done(ewd),.O_x(ewx),.O_y(ewy),.O_window_valid(ewm),.O_protocol_error(errors[2]),.O_busy());
wire [31:0] dwp11,dwp12,dwp13,dwp21,dwp22,dwp23,dwp31,dwp32,dwp33;
wire dwv,dwu,dwl,dwd;wire [11:0] dwx,dwy;wire [3:0] dwm;
line_buffer_3x3_4px #(.IMG_WIDTH(IMG_WIDTH),.IMG_HEIGHT(IMG_HEIGHT)) u_dwwindow(.I_clk(I_clk),.I_rst_n(I_rst_n),.I_gray_data(dilated),.I_tvalid(dv),.I_tuser(du),.I_tlast(dl),.O_p11(dwp11),.O_p12(dwp12),.O_p13(dwp13),.O_p21(dwp21),.O_p22(dwp22),.O_p23(dwp23),.O_p31(dwp31),.O_p32(dwp32),.O_p33(dwp33),.O_tvalid(dwv),.O_tuser(dwu),.O_tlast(dwl),.O_frame_done(dwd),.O_x(dwx),.O_y(dwy),.O_window_valid(dwm),.O_protocol_error(errors[3]),.O_busy());
binary_dilation_4px u_erode_then_dilate(.I_clk(I_clk),.I_rst_n(I_rst_n),.I_p11(ewp11),.I_p12(ewp12),.I_p13(ewp13),.I_p21(ewp21),.I_p22(ewp22),.I_p23(ewp23),.I_p31(ewp31),.I_p32(ewp32),.I_p33(ewp33),.I_tvalid(ewv),.I_tuser(ewu),.I_tlast(ewl),.I_frame_done(ewd),.I_x(ewx),.I_y(ewy),.I_window_valid(ewm),.O_binary_data(pixel[10]),.O_tdata(rgb[10]),.O_tvalid(valid[10]),.O_tuser(user_mark[10]),.O_tlast(last_mark[10]),.O_frame_done(done[10]),.O_x(),.O_y(),.O_window_valid());
binary_erosion_4px u_dilate_then_erode(.I_clk(I_clk),.I_rst_n(I_rst_n),.I_p11(dwp11),.I_p12(dwp12),.I_p13(dwp13),.I_p21(dwp21),.I_p22(dwp22),.I_p23(dwp23),.I_p31(dwp31),.I_p32(dwp32),.I_p33(dwp33),.I_tvalid(dwv),.I_tuser(dwu),.I_tlast(dwl),.I_frame_done(dwd),.I_x(dwx),.I_y(dwy),.I_window_valid(dwm),.O_binary_data(pixel[11]),.O_tdata(rgb[11]),.O_tvalid(valid[11]),.O_tuser(user_mark[11]),.O_tlast(last_mark[11]),.O_frame_done(done[11]),.O_x(),.O_y(),.O_window_valid());
reg [95:0] selected_rgb;reg sv,su,sl,sd;
 always @(posedge I_clk or negedge I_rst_n)begin
 if(!I_rst_n)begin selected_rgb<=0;sv<=0;su<=0;sl<=0;sd<=0;end
 else begin selected_rgb<=rgb[active_mode];sv<=valid[active_mode];su<=user_mark[active_mode];sl<=last_mark[active_mode];sd<=done[active_mode];end end
 assign O_busy=busy;
 wire [95:0] roi_rgb;wire rv,ru,rl,rd;
 roi_border_overlay #(.W(IMG_WIDTH),.H(IMG_HEIGHT)) u_roi_border(.clk(I_clk),.rst_n(I_rst_n),.rgb(selected_rgb),
 .valid(sv),.user_mark(su),.last_mark(sl),.done(sd),.roi_cfg(I_roi_config),.out_rgb(roi_rgb),.ov(rv),.ou(ru),.ol(rl),.od(rd));
 wire pack_error;wire [95:0] osd_rgb;wire osd_v,osd_u,osd_l,osd_d;
 algorithm_label_osd #(.IMG_WIDTH(IMG_WIDTH),.IMG_HEIGHT(IMG_HEIGHT)) u_label(
 .clk(I_clk),.rst_n(I_rst_n),.I_rgb(roi_rgb),.I_valid(rv),.I_user(ru),.I_last(rl),.I_done(rd),.I_mode(active_mode),
 .O_rgb(osd_rgb),.O_valid(osd_v),.O_user(osd_u),.O_last(osd_l),.O_done(osd_d));
 rgb96_pack128_valid u_pack(.I_clk(I_clk),.I_rst_n(I_rst_n),.I_rgb(osd_rgb),.I_valid(osd_v),.I_user(osd_u),.I_last(osd_l),.I_done(osd_d),
 .O_data(O_data),.O_valid(O_valid),.O_last(O_last),.O_done(O_done),.O_error(pack_error));
 assign O_error=pack_error|overlap_error|(|errors);
endmodule
