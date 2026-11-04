"""Collect the 2026-10-10 official-original colour correction evidence."""
from pathlib import Path
import hashlib,json,re,runpy
ROOT=Path(__file__).resolve().parent
runpy.run_path(str(ROOT/'audit_uart_project.py'),run_name='__main__')
checks=[('实际ISP原图/AWB接线、RGB顺序、0→1→0三帧及行帧标记','reports/original_color_fix_console.log','PASS official-original colour regression'),
        ('上位机配置/GUI/协议及串口回环','reports/python_color_fix_tests.log','\nOK')]
rows=[]
for label,name,marker in checks:
 text=(ROOT/name).read_text(encoding='utf-8',errors='replace')
 assert marker in text and not any(e in text for e in ['Fatal:','ERROR:','FAILED (']),name
 rows.append(f'| {label} | PASS | `{name}` |')
phy=ROOT/'td_project/camera_to_dsi_display_Runs/phy_1'
bit=phy/'camera_to_dsi_display.bit'
assert bit.is_file() and (phy/'.bitgen.end.f').is_file()
assert bit.stat().st_mtime>(ROOT/'user_source/hdl_source/isp/isp_top.v').stat().st_mtime,'Stale bitstream'
timing=(phy/'camera_to_dsi_display_pr.timing').read_text(errors='replace')
slack={name:float(re.search(name+r':\s*([-\d.]+)ns',timing)[1]) for name in ['SWNS','HWNS','STNS','HTNS']}
assert slack['SWNS']>=0 and slack['HWNS']>=0 and slack['STNS']==0 and slack['HTNS']==0,slack
assert 'PASS fresh TD run' in (ROOT/'reports/td_color_fix_console.log').read_text(errors='replace')
sources=[*ROOT.glob('rtl/*.v'),*ROOT.glob('user_source/**/*.v'),*ROOT.glob('user_source/**/*.sv'),
 *ROOT.glob('user_source/**/*.adc'),ROOT/'td_project/camera_to_dsi_display.sdc',ROOT/'td_project/camera_to_dsi_display.al',
 ROOT/'pc_upper/config/algorithms.json',bit]
sources += [p for p in ROOT.glob('pc_upper/**/*.py') if 'deps' not in p.parts]
fingerprints={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}
(ROOT/'reports/build_manifest.json').write_text(json.dumps(fingerprints,indent=2),encoding='utf-8')
s='''# 原图偏绿修复验证

验证日期：2026-10-10。已直接覆盖当前 applications/stage3_7_uart 工程。

## 原因与修复

官方工程把awb_O_tdata送入96/128打包器，所谓官方原图包含AWB。上一版当前工程把runtime.I_rgb误接为awb_uncorrected，导致0号原图和其他算法使用未校正的传感器RGB，表现为偏绿。

本次恢复runtime.I_rgb=awb_O_tdata，保留现有AWB及其有效/提前帧通知信号；所有算法使用官方颜色基线。没有通过任意红蓝增益补偿照片，也没有修改Bayer模式、摄像头寄存器、RGB排列或HDMI通道。生成脚本已同步修复，并增加接线审计。ISP宽高参数默认仍1280×720，新增参数仅用于正常场景的小尺寸集成测试。

官方原图已有AWB，因此0号原图与1号白平衡当前除OSD名称外颜色相同，上位机说明已明确标注；编号0～11和UART V2协议保持使用。

## 本次验证

| 检查 | 结果 | 证据 |
|---|---|---|
'''+ '\n'.join(rows)+f'''
| 接线/清单/引脚/原始参考文件审计 | PASS | `audit_uart_project.py` |
| TD6.2.1综合、布局布线及bitstream | PASS | `reports/td_color_fix_console.log` |
| 最终setup/hold | SWNS **+{slack['SWNS']:.3f}ns**，HWNS **+{slack['HWNS']:.3f}ns**，STNS/HTNS均0 | `td_project/camera_to_dsi_display_Runs/phy_1/camera_to_dsi_display_pr.timing` |
| 实板摄像头/HDMI修复后颜色复核 | 尚未执行 | 需下载本次新bit后对比官方原图 |

集成测试执行实际isp_top、awb、signal_delay、runtime、OSD及打包器，普通偏绿RGB测试输入，经既有AWB后以官方输出逐字节作为基准。0→1→0共3帧，每帧9216字节、768个四像素组；全部输出等于AWB基准且每帧768组确实经过颜色校正，核对通道顺序、像素数量、行/帧标记及排空。测试尺寸256×12，OSD按原有规则关闭以比较全部颜色字节。摄像头前端和厂商除法器/BRAM接口使用行为模型，不属于实板/厂商IP门级仿真。

本次针对接线缺陷执行正常功能回归，没有新增随机故障注入、协议压力或强对抗测试。算法内核、UART及OSD实现未修改；2026-10-05的全算法640×112/1280×720记录属于历史验证，见verification_20261005.md，本次没有把历史记录冒充为修复后的全分辨率复测。

新的bit路径：`td_project/camera_to_dsi_display_Runs/phy_1/camera_to_dsi_display.bit`，{bit.stat().st_size}字节。

SHA256：`{fingerprints[bit.relative_to(ROOT).as_posix()]}`。源文件指纹见build_manifest.json。后续修改RTL需重新生成bit。完整资源统计见本次phy_1/camera_to_dsi_display_phy.area。

继承的相机I2C/相机时钟混合扇出、局部时钟布线告警在基线中也存在，最终STA通过。实际图像仍需要用户在同样场景与显示器条件下检查；本报告只确认已修复官方原图链路及完成上述工具验证。
'''
(ROOT/'reports/verification.md').write_text(s,encoding='utf-8')
print('PASS current colour-fix evidence, fresh bitstream and timing; reports saved')
