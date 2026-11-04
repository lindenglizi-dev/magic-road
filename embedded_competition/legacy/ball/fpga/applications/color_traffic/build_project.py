from pathlib import Path
import shutil,re
ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
BASE=ROOT/'lab_ex1_mipi_hdmi_SC520 (2)/lab_ex1_mipi_hdmi_SC520/lab_ex1_mipi_hdmi'
def write(p,s):
 p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s,encoding='utf-8')
shutil.copytree(BASE/'user_source',OUT/'user_source',dirs_exist_ok=True)
for d in ['rtl','sim','reports','td_project','td_project/run_settings']:(OUT/d).mkdir(exist_ok=True)
for name in ['al_ip','chip_debugger']:
 shutil.copytree(BASE/'td_project'/name,OUT/'td_project'/name,dirs_exist_ok=True)
shutil.copy2(ROOT/'TD_insert/rtl/rgb96_pack128_valid.v',OUT/'rtl/rgb96_pack128_valid.v')
p=OUT/'user_source/hdl_source/isp/isp_top.v';s=p.read_text(encoding='utf-8')
s=s.replace('module isp_top (','module isp_top (\n    input wire [3:0] I_keys_n,')
s=s.replace(');',');\nwire app_last, app_done, app_error; wire [2:0] app_result;',1)
s=s.replace('assign O_tlast  = awb_O_tlast','assign O_tlast  = app_last')
insert='''color_traffic_runtime u_application(.I_clk(axi4s_video_aclk),.I_rst_n(I_rst_n),.I_keys_n(I_keys_n),
 .I_rgb(awb_O_tdata),.I_valid(awb_O_tvalid),.I_user(awb_O_tuser),.I_last(awb_O_tlast),
 .O_data(awb_O_tdata_128),.O_valid(awb_O_tvalid_128),.O_early(awb_O_tuser_128),
 .O_last(app_last),.O_done(app_done),.O_error(app_error),.result(app_result));'''
s,n=re.subn(r'data_96bit_to_128bit u_data_96bit_to_128bit\(.*?\);',lambda m:insert,s,flags=re.S);assert n==1;write(p,s)
p=OUT/'user_source/hdl_source/design_top_wrapper.v';s=p.read_text(encoding='utf-8');s=s.replace('module design_top_wrapper (','module design_top_wrapper (\n    input wire [3:0] I_keys_n,').replace('isp_top u_isp_top (','isp_top u_isp_top (\n.I_keys_n(I_keys_n),');write(p,s)
p=OUT/'user_source/constraints_source/pin.adc';s=p.read_text(encoding='utf-8')
for i,pin in enumerate(['D5','A9','B9','C7']):
 assert not re.search(r'LOCATION\s*=\s*'+pin+r'\s*;',s)
 s+=f'\nset_pin_assignment {{ I_keys_n[{i}] }} {{ LOCATION = {pin}; IOSTANDARD = LVCMOS33; PULLTYPE = PULLUP; }}\n'
write(p,s)
shutil.copy2(BASE/'td_project/camera_to_dsi_display.sdc',OUT/'td_project/camera_to_dsi_display.sdc')
# Preserve original project options, IP and timing constraints; only append new RTL.
extra=list((OUT/'rtl').glob('*.v'))
for rel in ['camera_to_dsi_display.al','camera_to_dsi_display_Runs/syn_1/camera_to_dsi_display.prj','camera_to_dsi_display_Runs/phy_1/camera_to_dsi_display.prj']:
 src=BASE/'td_project'/rel;dst=OUT/'td_project'/rel;s=src.read_text(encoding='utf-8')
 if rel.endswith('.al'):
  s=re.sub(r'(<Project[^>]* Path=")[^"]*',lambda m:m[1]+str(OUT/'td_project').replace('\\','/'),s)
 entries=''
 for order,f in enumerate(extra,200):
  import os
  path=os.path.relpath(f,dst.parent).replace('\\','/')
  entries+=f'<File Path="{path}"><FileInfo><Attr Name="UsedInSyn" Val="true"/><Attr Name="UsedInP&amp;R" Val="true"/><Attr Name="BelongTo" Val="design_1"/><Attr Name="CompileOrder" Val="{order}"/></FileInfo></File>\n'
 # Original TD XML uses literal ampersand in attribute values too.
 entries=entries.replace('P&amp;R','P&R')
 s=s.replace('</Verilog>',entries+'</Verilog>');write(dst,s)
for stage in ['syn_1','phy_1']:
 for name in ['settings.cfg','camera_to_dsi_display.tcl']:
  shutil.copy2(BASE/'td_project/camera_to_dsi_display_Runs'/stage/name,OUT/'td_project/camera_to_dsi_display_Runs'/stage/name)
print('Created self-contained application from specified SC520 baseline')

for stage in ['syn_1','phy_1']:
 shutil.copy2(OUT/'td_project/camera_to_dsi_display_Runs'/stage/'settings.cfg',OUT/'td_project/run_settings'/f'{stage}.cfg')
