"""Collect current software/simulation/build evidence; never assert board success."""
from pathlib import Path
import hashlib,json,re,runpy
ROOT=Path(__file__).resolve().parent
runpy.run_path(str(ROOT/'audit_uart_project.py'),run_name='__main__')
checks=[
 ('Python 13项：配置/串口回环/ROI/原始截图/1080P编码/18515包ACK/取消','reports/vision_software_tests.log','Ran 13 tests'),
 ('115200双向UART：ROI帧提交/红绿计数/重复ACK缓存/原MODE','reports/stage4_roi_sim.log','PASS vision ROI:'),
 ('实际UART图片命令：232字节/坏CRC/重发去重/DDR数据/异常NACK/ABORT','reports/stage4_roi_sim.log','PASS UART image commands:'),
 ('缩小尺寸DDR功能模型：CDC/背压/owner隔离/CRC失败/重放/旧图保留','reports/vision_image_sim.log','PASS image path:'),
 ('原生1080P跨度：172800次读、921600输出像素/720行逐一比对','reports/vision_image_sim.log','PASS native 1080 DDR replay:'),
 ('输入源：帧间切换/PC在途保护/返回摄像头拒收半帧','reports/vision_image_sim.log','PASS source select:'),
 ('全部原有算法：640×112、13黄金帧、OSD/logo/按键/DDR打包','reports/vision_algorithm_regression.log','PASS runtime'),
 ('原video_in FIFO：原图+11模式，103.52/66.67MHz复位边界','reports/vision_algorithm_regression.log','PASS original video_in'),
 ('原图色彩：实际ISP/AWB接线、0→1→0逐字节RGB与行帧标志','reports/vision_original_regression.log','PASS official-original colour regression'),
]
rows=[]
for label,name,marker in checks:
    s=(ROOT/name).read_text(encoding='utf-8',errors='replace')
    assert marker in s and not any(error in s for error in ('Fatal:','ERROR:','FAILED (','Traceback')),name
    if 'software' in name:assert '\nOK' in s,name
    rows.append(f'| {label} | PASS | `{name}` |')
phy=ROOT/'td_project/camera_to_dsi_display_Runs/phy_1'
bit=phy/'camera_to_dsi_display.bit';timing_file=phy/'camera_to_dsi_display_pr.timing'
text=timing_file.read_text(errors='replace')
slack={k:float(re.search(k+r':\s*([-\d.]+)ns',text)[1]) for k in ('SWNS','HWNS','STNS','HTNS')}
assert min(slack['SWNS'],slack['HWNS'])>=0 and slack['STNS']==slack['HTNS']==0,slack
al=ROOT/'td_project/camera_to_dsi_display.al'
compiled=[(al.parent/p).resolve() for p in re.findall(r'<File Path="([^"]+)"',al.read_text(encoding='utf-8'))]
assert bit.exists() and (phy/'.bitgen.end.f').exists()
assert all(bit.stat().st_mtime>p.stat().st_mtime for p in compiled if p.suffix.lower() in ('.v','.sv','.sdc','.adc')),'Stale bitstream'
sources=[p for p in compiled if p.is_file()]+[al,ROOT/'td_project/camera_to_dsi_display.sdc',bit]
sources += [p for p in ROOT.glob('pc_upper/**/*.py') if 'deps' not in p.parts]
sources += [ROOT/'pc_upper/config/algorithms.json',ROOT/'pc_upper/requirements.txt']
fingerprints={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}
(ROOT/'reports/vision_build_manifest.json').write_text(json.dumps(fingerprints,indent=2),encoding='utf-8')
report='''# FPGA Vision集成验证（2026-10-15）

现有工程直接修改，代码实现覆盖阶段1～7；阶段4和7的实机联调尚未完成。所有PASS均限定于下述软件、RTL功能模型或TD工具，不代表开发板实拍成功。

## 分阶段结果

| 阶段 | 已完成/可验证结果 | 硬件待验 |
|---|---|---|
| 1 分析 | 摄像头/CSI/ISP/DDR/HDMI均确认1280×720；ROI原为独立固定参数核心 | 用户若另有1080P工程需提供实际工程 |
| 2 预览/截图 | 原GUI扩展、后台采集、实际shape/FPS、复用原始帧截图；fixture逐像素相等 | 确认UVC设备实际连接FPGA HDMI，采集真实帧/FPS |
| 3 ROI GUI | 黑边/缩放/反向拖动坐标、手输/保存/加载、草稿与应用区分 | 实画面校准；禁止采集卡未知裁剪 |
| 4 ROI RTL | 统一UART、CDC、帧提交ACK、查询/颜色计数/原三帧投票仿真 | 真实UART往返，观察硬件白边及目标移动 |
| 5 图片上传 | 1920×1080 RGB565=4147200字节，18515包，CRC/ACK/重试/取消软件+UART仿真 | 完整实板上传时长、断线/取消及DDR异常 |
| 6 FPGA输入 | 双DDR区、末尾栅栏、完整提交、静态重放、720P适配、源选择仿真 | DDR真实控制器/板级容量及争用/长时显示 |
| 7 闭环 | 代码链路接通，原算法/原色回归和完整综合布线 | 上传→FPGA算法→显示器/采集卡→ROI→截图全流程实测 |

## 实际执行测试

| 项目 | 结果 | 日志 |
|---|---|---|
'''+ '\n'.join(rows)+f'''

实际脚本：`python -m unittest discover -s pc_upper/tests -v`、`sim/run_vision_roi_verify.ps1`、`sim/run_image_verify.ps1`、`sim/run_original_verify.ps1`、`sim/run_verify.ps1`及`audit_uart_project.py`。GUI在1240×740离屏渲染并人工检查，图在vision_roi_gui.png / vision_upload_gui.png；这些是未连接FPGA的GUI，不是HDMI实拍。

ROI/图片功能测试采用真实RTL和可控DDR响应模型，DDR厂商控制器参与真实综合，但未在仿真中模拟整颗DDR器件。ROI测试几何64×32，图片CRC/双缓冲测试48×6；原生地址/采样另以1920×1080模型完整验证。旧uart_mode_link独立测试不作为新版控制器通过的依据。

## TD最终实现

- 器件PH1P35MDG324，-3，TD6.2.168116。
- 已执行新综合（约4分51秒）和布局布线/bitgen（约15分15秒）。最终报告为2026-10-15 13:11:56，bit生成13:12:11；不是2026-10-10历史bit。
- 建立SWNS **{slack['SWNS']:+.3f}ns**，保持HWNS **{slack['HWNS']:+.3f}ns**，STNS/HTNS均0；慢/快角检查通过，STA覆盖94.44%。异步域按既有clock groups排除；数据稳定mailbox另以功能仿真检查，并非完成形式CDC签核。
- 物理Slice18391/21216=86.68%，LUT6 16510/21216=77.82%，寄存器22651/42432=53.38%，ERAM66/108=61.11%，DSP20/40=50%。最终报告`td_project/camera_to_dsi_display_Runs/phy_1/camera_to_dsi_display_phy.area`。
- bit：`{bit.relative_to(ROOT).as_posix()}`，{bit.stat().st_size}字节。
- SHA256：`{fingerprints[bit.relative_to(ROOT).as_posix()]}`；源码/配置/bit指纹见vision_build_manifest.json。校验器拒绝比RTL旧的bit。

## 风险与尚未执行项目

建立裕量仅3ps，虽通过本次工具约束，余量很薄；新增算法/重新布线需重验，不能据此宣称板级长期稳定。主要关键路径为源选择/early→ROI坐标比较/颜色计数。高Slice占用可能增加布局敏感性；后续可独立流水ROI，须保持阈值/计数/帧标志一致。

上传原生1080P，输出/ROI坐标仍为实际720P。PC输入不经过传感器AWB；模式0/1在PC源相同。ROI统计在算法前，投票连续使用最近三帧；切源后需等新帧稳定。PC重放依赖现有CSI时钟，摄像头必须保持连接供钟。

DDR按25bit的16bit字地址配置可寻址64MiB，尚未按颗粒BOM/实测确认物理容量，需先核验高地址bank；图片两bank共8294400字节，避开四个原视频槽。END用接收CRC和尾字读回栅栏，不是整DDR读回校验。视频@60fps原读写约331.8MB/s，PC重放另加读取，需实测仲裁/FIFO和稳定性。驱动永久阻塞read/open时，线程安全退出依赖驱动恢复。

设备枚举看到COM3/COM4（蓝牙标准串口）及视频索引0/1；未确认开发板USB-UART或哪路视频为FPGA采集卡，未向这些串口发送开发板命令。尚未下载本次bit到实板，未取得FPGA HDMI实拍，不宣称硬件闭环通过。

上板验收顺序：下载最新bit→115200读能力/尺寸→原0～11模式/按键→HDMI采集真实尺寸/FPS和原帧PNG→ROI移动/开关/红黄绿回传→完整1080P上传/CRC/取消→PC Image切源/各算法/同图ROI→显示器与采集卡同时核对→反复切源及长时DDR稳定。任何未确认命令保持未确认状态。
'''
(ROOT/'reports/vision_verification.md').write_text(report,encoding='utf-8')
print('PASS current evidence, fresh bitstream, timing and source manifest',slack)
