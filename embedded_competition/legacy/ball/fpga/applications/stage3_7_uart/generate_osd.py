"""Compile PNG and Chinese/English labels into synchronous ROMs."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageOps
import numpy as np
import json,hashlib,shutil
p=Path(__file__).resolve().parent
(p/'assets').mkdir(exist_ok=True)
src=p.parents[1]/'安路logo.png'
if src.exists():shutil.copy2(src,p/'assets/anlogic_source.png')
src=p/'assets/anlogic_source.png'
catalog=json.loads((p/'pc_upper/config/algorithms.json').read_text(encoding='utf-8'))
labels=[[item['name'].replace('. ','.'),item['english']] for item in catalog['modes']]
chars=sorted(set(' '+''.join(line for pair in labels for line in pair)))
font=ImageFont.truetype('C:/Windows/Fonts/simhei.ttf',24)
glyphs={}
for ch in chars:
 im=Image.new('L',(32,32));ImageDraw.Draw(im).text((16,16),ch,font=font,fill=255,anchor='mm')
 glyphs[ch]=[''.join('1' if im.getpixel((x,y))>=100 else '0' for x in range(32)) for y in range(32)]
im=Image.open(src).convert('RGB');a=np.asarray(im).astype(int)
mask=(a.max(2)-a.min(2)>80)&(a.min(2)<150)
yy,xx=np.where(mask);box=(int(xx.min()),int(yy.min()),int(xx.max()+1),int(yy.max()+1))
mark=ImageOps.contain(im.crop(box),(128,80),Image.Resampling.LANCZOS)
canvas=Image.new('RGB',(128,80),'white');canvas.paste(mark,((128-mark.width)//2,(80-mark.height)//2))
palette=np.array([[255,255,255],[3,23,91],[255,0,0],[185,193,210]],dtype=int)
arr=np.asarray(canvas).astype(int)
indices=((arr[:,:,None,:]-palette[None,None,:,:])**2).sum(3).argmin(2).astype(np.uint8)
Image.fromarray(palette[indices].astype(np.uint8)).save(p/'assets/logo_rom_preview.png')
assets={'labels':labels,'glyphs':glyphs,'palette':palette.tolist(),'logo':indices.tolist(),'logo_source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'crop_box':box,'font':'Windows SimHei 24px in 32x32 cells','panel':{'width':416,'height':80,'margin':16,'text_pad_x':8,'text_pad_y':8}}
(p/'sim/osd_font.json').write_text(json.dumps(assets,ensure_ascii=False),encoding='utf-8')
depth=1<<((len(chars)*32-1).bit_length());aw=(depth-1).bit_length()
rom=f'''`timescale 1ns/1ps
// Initialized synchronous ROMs: no external runtime .mem dependency.
module osd_assets_rom(input wire clk,input wire [{aw-1}:0] font_addr,
 input wire [11:0] logo_addr,output reg [31:0] font_row,output reg [7:0] logo_group);
 reg [31:0] font_rom[0:{depth-1}];
 reg [7:0] logo_rom[0:4095];
 initial begin
'''
rows=[int(row,2) for ch in chars for row in glyphs[ch]]
for i in range(depth):rom+=f"font_rom[{i}]=32'h{rows[i] if i<len(rows) else 0:08x};\n"
for i in range(4096):
 y=i//32;x=(i%32)*4
 value=sum(int(indices[y,x+k])<<(6-2*k) for k in range(4)) if y<80 else 0
 rom+=f"logo_rom[{i}]=8'h{value:02x};\n"
rom+='''end
 always @(posedge clk)begin font_row<=font_rom[font_addr];logo_group<=logo_rom[logo_addr];end
endmodule
'''
# Keep a harmless compatibility file for existing TD source lists. The ROM
# definition lives with its only consumer so older GUI projects also compile.
(p/'rtl/osd_assets_rom.v').write_text('// osd_assets_rom is defined in algorithm_label_osd.v.\n',encoding='utf-8')
s=f'''`timescale 1ns/1ps
// Four pixels share one glyph row and one logo ROM word.
// Pipeline: coordinates/addresses -> synchronous ROM -> compose RGB.
module algorithm_label_osd #(parameter IMG_WIDTH=1280,IMG_HEIGHT=720)(
 input wire clk,rst_n,input wire [95:0] I_rgb,
 input wire I_valid,I_user,I_last,I_done,input wire [3:0] I_mode,
 output reg [95:0] O_rgb,output reg O_valid,O_user,O_last,O_done);
 function [{aw-6}:0] char_id;
 input [3:0] mode;input line_sel;input [3:0] char_index;
 begin char_id={chars.index(' ')};case({{mode,line_sel,char_index}})
'''
for m,pair in enumerate(labels):
 for line,txt in enumerate(pair):
  for n,ch in enumerate(txt):s+=f"9'd{m*32+line*16+n}:char_id={chars.index(ch)};\n"
s+=f"default:char_id={chars.index(' ')};endcase end endfunction\n"
s+='function [23:0] logo_color;input [1:0] index;begin case(index)\n'
for n,color in enumerate(palette):s+=f"2'd{n}:logo_color=24'h{''.join(f'{v:02x}' for v in color)};\n"
s+='''endcase end endfunction
 reg [11:0] x,y;
 wire [11:0] base_x=I_user?12'd0:x,base_y=I_user?12'd0:y;
 wire [12:0] tx={1'b0,base_x}-(IMG_WIDTH-424);
 wire [11:0] ty=base_y-12'd24;
 wire [11:0] lx=base_x-12'd16,ly=base_y-12'd16;
 reg [95:0] data0,data1;reg [3:0] flags0,flags1;
 reg panel0,panel1,text0,text1,logo0,logo1;reg [2:0] group0,group1;
'''
s+=f'''reg [{aw-1}:0] font_addr0;reg [11:0] logo_addr0;
 wire [31:0] font_row;wire [7:0] logo_group;
 osd_assets_rom u_assets(.clk(clk),.font_addr(font_addr0),.logo_addr(logo_addr0),.font_row(font_row),.logo_group(logo_group));
'''
s+='''always @(posedge clk or negedge rst_n)begin
 if(!rst_n)begin x<=0;y<=0;data0<=0;data1<=0;flags0<=0;flags1<=0;
 panel0<=0;panel1<=0;text0<=0;text1<=0;logo0<=0;logo1<=0;group0<=0;group1<=0;
 font_addr0<=0;logo_addr0<=0;O_valid<=0;O_user<=0;O_last<=0;O_done<=0;end
 else begin
 if(I_user)begin x<=0;y<=0;end
 if(I_valid)begin
 if(base_x==IMG_WIDTH-4)begin x<=0;y<=base_y==IMG_HEIGHT-1?12'd0:base_y+1'b1;end
 else begin x<=base_x+12'd4;y<=base_y;end
 end
 data0<=I_rgb;data1<=data0;flags0<={I_valid,I_user,I_last,I_done};flags1<=flags0;
 {O_valid,O_user,O_last,O_done}<=flags1;
 panel0<=IMG_WIDTH>=608&&IMG_HEIGHT>=96&&base_x>=IMG_WIDTH-432&&base_x<IMG_WIDTH-16&&base_y>=16&&base_y<96;
 logo0<=IMG_WIDTH>=608&&IMG_HEIGHT>=96&&lx<128&&ly<80;
 text0<=tx<384&&ty<64;group0<=tx[4:2];
 font_addr0<={char_id(I_mode,ty[5],tx[8:5]),ty[4:0]};
 logo_addr0<={ly[6:0],lx[6:2]};
 panel1<=panel0;logo1<=logo0;text1<=text0;group1<=group0;
 end end
 genvar k;
 generate for(k=0;k<4;k=k+1)begin:lane
 wire ink=text1&&font_row[31-({group1,2'b00}+k)];
 always @(posedge clk or negedge rst_n)begin
 if(!rst_n)O_rgb[95-k*24-:24]<=0;
 else O_rgb[95-k*24-:24]<=logo1?logo_color(logo_group[7-k*2-:2]):
 panel1?(ink?24'hFFE066:24'h101820):data1[95-k*24-:24];
 end end endgenerate
endmodule
'''
(p/'rtl/algorithm_label_osd.v').write_text(s+'\n'+rom,encoding='utf-8')
print(f'Generated {len(chars)} bilingual glyphs, {depth} font rows and 128x80 logo')
