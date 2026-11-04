"""Regenerate the 2026-10 algorithm graph and project-local assets.

Only writes inside this project. Source algorithm kernels and board IP stay local.
"""
from pathlib import Path
import json,re,shutil
ROOT=Path(__file__).resolve().parent
def write(name,text):
    (ROOT/name).write_text(text,encoding='utf-8')

catalog=[('original','原图','ORIGINAL'),('white_balance','白平衡','WHITE BAL'),
 ('binary','灰度二值化','BINARY'),('median','中值滤波','MEDIAN'),
 ('edge','边缘检测','SOBEL'),('sharpen','锐化','SHARPEN'),
 ('gamma','伽马矫正','GAMMA'),('contrast','对比度调节','CONTRAST'),
 ('brightness','亮度调节','BRIGHTNESS'),('saturation','饱和度调节','SATURATION'),
 ('erode_dilate','腐蚀-膨胀','ERODE-DILATE'),('dilate_erode','膨胀-腐蚀','DILATE-ERODE')]
config={'schema_version':1,'profile':'image_algorithms_v2','protocol_version':2,
 'baudrates':[115200],'modes':[dict(id=key,name=(f'{i}. ' if i else '0. ')+cn,english=en,command=i) for i,(key,cn,en) in enumerate(catalog)]}
descriptions=['官方 ISP 原图（已包含 AWB 校正）；保留安路 logo 和模式说明',
 '已有自动白平衡 AWB；官方原图同样包含此校正，当前两者颜色一致',
 '灰度 Y=(77R+150G+29B)/256；Y≥128 输出白色，否则黑色',
 '3×3 灰度中值；精确取九个邻域像素的中间值',
 'Sobel 边缘；|Gx|+|Gy|≥128 输出白色',
 '灰度锐化：5×中心−上−下−左−右，饱和到0～255',
 'RGB Gamma=0.7，256项查表，提升暗部',
 'RGB 对比度1.25倍，以128为中心，饱和到0～255',
 'RGB 亮度加32，饱和到0～255',
 '饱和度1.5倍：Y+1.5×(RGB−Y)，饱和到0～255',
 '灰度二值图，3×3全1结构元素，先腐蚀后膨胀',
 '灰度二值图，3×3全1结构元素，先膨胀后腐蚀']
for item,description in zip(config['modes'],descriptions):
 item['description']=description
 item['role']='source' if item['command']==0 else 'algorithm'
config['modes'][0]['description_pc']='上传图片RGB565展开/FPGA适配输出；保留安路logo和模式说明'
config['modes'][1]['description_pc']='PC Image使用上传RGB565展开值，与原图相同；传感器AWB仅用于Camera'
write('pc_upper/config/algorithms.json',json.dumps(config,ensure_ascii=False,indent=2)+'\n')

# Preserve the vendor AWB's gain calculation and buffering, but expose its
# pre-gain pixels at exactly the same latency as the corrected RGB.
p=ROOT/'user_source/hdl_source/awb.v';s=p.read_text(encoding='utf-8')
if 'O_uncorrected' not in s:
 s=s.replace('output [95:0]           O_tdata  ,','output [95:0]           O_tdata  ,\n    output reg [95:0]       O_uncorrected,')
 at='    assign  O_tdata ='
 s=s.replace(at,"    // Pre-gain bypass: same edge and valid as the channel gain multipliers.\n    always @(posedge I_clk or negedge I_rst_n)\n      if(!I_rst_n) O_uncorrected<=0;\n      else if(valid_d1) O_uncorrected<=data_d1;\n\n"+at)
 p.write_text(s,encoding='utf-8')
p=ROOT/'user_source/hdl_source/isp/isp_top.v';s=p.read_text(encoding='utf-8')
if '.O_uncorrected' not in s:
 s=s.replace('wire app_last,','wire [95:0] awb_uncorrected;\nwire app_last,')
 s=s.replace('.O_tdata (awb_O_tdata ),','.O_tdata (awb_O_tdata ),\n    .O_uncorrected(awb_uncorrected),')
 s=s.replace('.I_rgb(awb_O_tdata),','.I_rgb(awb_O_tdata),.I_wb_rgb(awb_O_tdata),')
 p.write_text(s,encoding='utf-8')
# Keep the official AWB-corrected original even when upgrading an older copy.
s=p.read_text(encoding='utf-8').replace('.I_rgb(awb_uncorrected)', '.I_rgb(awb_O_tdata)')
p.write_text(s,encoding='utf-8')

# Explicitly remove retired modules and the old static wrappers that referenced them.
retired=['binary_open_4px','binary_close_4px','binary_denoise_4px','binary_fill_holes_4px',
 'binary_cleanup_4px','binary_cleanup_stream_4px','binary_morph_top',
 'gray_filter_stream_4px','gaussian_filter_4px','image_algorithm_stage7_96']
for name in retired:
 p=ROOT/'rtl'/f'{name}.v'
 if p.exists():p.unlink()

s='''// Configured graph: original 0, algorithms 1..11. All streams carry their own markers.
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
'''
for i in (2,6,7,8,9):s+=f'assign valid[{i}]=pv;assign user_mark[{i}]=pu;assign last_mark[{i}]=pl;assign done[{i}]=pd;\n'
def window(prefix,px,v,u,l,error):
 global s
 names=[f'{prefix}p{a}{b}' for a in range(1,4) for b in range(1,4)]
 s+='wire [31:0] '+','.join(names)+';\n'
 s+=f'wire {prefix}v,{prefix}u,{prefix}l,{prefix}d;wire [11:0] {prefix}x,{prefix}y;wire [3:0] {prefix}m;\n'
 ports=['.I_clk(I_clk)','.I_rst_n(I_rst_n)',f'.I_gray_data({px})',f'.I_tvalid({v})',f'.I_tuser({u})',f'.I_tlast({l})']
 ports += [f'.O_p{a}{b}({prefix}p{a}{b})' for a in range(1,4) for b in range(1,4)]
 ports += [f'.O_{a}({prefix}{b})' for a,b in [('tvalid','v'),('tuser','u'),('tlast','l'),('frame_done','d'),('x','x'),('y','y'),('window_valid','m')]]+[f'.O_protocol_error(errors[{error}])','.O_busy()']
 s+=f'line_buffer_3x3_4px #(.IMG_WIDTH(IMG_WIDTH),.IMG_HEIGHT(IMG_HEIGHT)) u_{prefix}window('+','.join(ports)+');\n'
def kernel(module,prefix,tag,rgbout,pxout,v,u,l,d,kind='pixel_data'):
 global s
 ports=['.I_clk(I_clk)','.I_rst_n(I_rst_n)']+[f'.I_p{a}{b}({prefix}p{a}{b})' for a in range(1,4) for b in range(1,4)]
 ports += [f'.I_{a}({prefix}{b})' for a,b in [('tvalid','v'),('tuser','u'),('tlast','l'),('frame_done','d'),('x','x'),('y','y'),('window_valid','m')]]
 ports += [f'.O_{kind}({pxout})',f'.O_tdata({rgbout})',f'.O_tvalid({v})',f'.O_tuser({u})',f'.O_tlast({l})',f'.O_frame_done({d})','.O_x()','.O_y()','.O_window_valid()']
 if module=='sobel_edge_4px':ports+=['.O_gx()','.O_gy()','.O_magnitude()']
 s+=f'{module} u_{tag}('+','.join(ports)+');\n'
window('w','gray','gv','guser','glast',0)
for i,mod,kind in [(3,'gray_median_4px','pixel_data'),(4,'sobel_edge_4px','edge_data'),(5,'gray_sharpen_4px','pixel_data')]:
 kernel(mod,'w',f'mode{i}',f'rgb[{i}]',f'pixel[{i}]',f'valid[{i}]',f'user_mark[{i}]',f'last_mark[{i}]',f'done[{i}]',kind)
window('b','pixel[2]','pv','pu','pl',1)
s+='wire [31:0] eroded,dilated;wire ev,eu,el,ed,dv,du,dl,dd;\n'
kernel('binary_erosion_4px','b','erode_first','','eroded','ev','eu','el','ed','binary_data')
kernel('binary_dilation_4px','b','dilate_first','','dilated','dv','du','dl','dd','binary_data')
window('ew','eroded','ev','eu','el',2)
window('dw','dilated','dv','du','dl',3)
kernel('binary_dilation_4px','ew','erode_then_dilate','rgb[10]','pixel[10]','valid[10]','user_mark[10]','last_mark[10]','done[10]','binary_data')
kernel('binary_erosion_4px','dw','dilate_then_erode','rgb[11]','pixel[11]','valid[11]','user_mark[11]','last_mark[11]','done[11]','binary_data')
s+='''reg [95:0] selected_rgb;reg sv,su,sl,sd;
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
'''
write('rtl/stage3_7_runtime.v',s)

for p in [ROOT/'td_project/camera_to_dsi_display.al',*ROOT.glob('td_project/*_Runs/*/*.prj')]:
 s=p.read_text(encoding='utf-8')
 for name in retired:s=re.sub(r'\s*<File Path="[^"]*/'+name+r'\.v">.*?</File>','',s,flags=re.S)
 prefix='../' if p.suffix=='.al' else '../../../'
 for name in ('gray_median_4px','rgb_point_adjust_4px'):
  if f'/{name}.v' not in s:s=s.replace('</Verilog>',f'<File Path="{prefix}rtl/{name}.v"><FileInfo><Attr Name="UsedInSyn" Val="true"/><Attr Name="UsedInP&amp;R" Val="true"/><Attr Name="BelongTo" Val="design_1"/><Attr Name="CompileOrder" Val="1"/></FileInfo></File>\n</Verilog>')
 p.write_text(s,encoding='utf-8')
print('Updated 0+11 algorithm graph, configuration and source lists')
