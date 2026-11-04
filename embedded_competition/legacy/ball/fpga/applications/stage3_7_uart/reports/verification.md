# 原图偏绿修复验证

> 仓库范围说明（2026-10-16）：本文是原始技术/验证记录，正文保留。其引用的原始日志、历史bit、第三方PDF或个人DOCX仅保留在本地，不随源仓库提交；这些本地附件不能视为GitHub中的可下载文件。历史结果不替代当前版本的实板验收。

验证日期：2026-10-10。已直接覆盖当前 applications/stage3_7_uart 工程。

## 原因与修复

官方工程把awb_O_tdata送入96/128打包器，所谓官方原图包含AWB。上一版当前工程把runtime.I_rgb误接为awb_uncorrected，导致0号原图和其他算法使用未校正的传感器RGB，表现为偏绿。

本次恢复runtime.I_rgb=awb_O_tdata，保留现有AWB及其有效/提前帧通知信号；所有算法使用官方颜色基线。没有通过任意红蓝增益补偿照片，也没有修改Bayer模式、摄像头寄存器、RGB排列或HDMI通道。生成脚本已同步修复，并增加接线审计。ISP宽高参数默认仍1280×720，新增参数仅用于正常场景的小尺寸集成测试。

官方原图已有AWB，因此0号原图与1号白平衡当前除OSD名称外颜色相同，上位机说明已明确标注；编号0～11和UART V2协议保持使用。

## 本次验证

| 检查 | 结果 | 证据 |
|---|---|---|
| 实际ISP原图/AWB接线、RGB顺序、0→1→0三帧及行帧标记 | PASS | `reports/original_color_fix_console.log` |
| 上位机配置/GUI/协议及串口回环 | PASS | `reports/python_color_fix_tests.log` |
| 接线/清单/引脚/原始参考文件审计 | PASS | `audit_uart_project.py` |
| TD6.2.1综合、布局布线及bitstream | PASS | `reports/td_color_fix_console.log` |
| 最终setup/hold | SWNS **+0.678ns**，HWNS **+0.020ns**，STNS/HTNS均0 | `td_project/camera_to_dsi_display_Runs/phy_1/camera_to_dsi_display_pr.timing` |
| 实板摄像头/HDMI修复后颜色复核 | 尚未执行 | 需下载本次新bit后对比官方原图 |

集成测试执行实际isp_top、awb、signal_delay、runtime、OSD及打包器，普通偏绿RGB测试输入，经既有AWB后以官方输出逐字节作为基准。0→1→0共3帧，每帧9216字节、768个四像素组；全部输出等于AWB基准且每帧768组确实经过颜色校正，核对通道顺序、像素数量、行/帧标记及排空。测试尺寸256×12，OSD按原有规则关闭以比较全部颜色字节。摄像头前端和厂商除法器/BRAM接口使用行为模型，不属于实板/厂商IP门级仿真。

本次针对接线缺陷执行正常功能回归，没有新增随机故障注入、协议压力或强对抗测试。算法内核、UART及OSD实现未修改；2026-10-05的全算法640×112/1280×720记录属于历史验证，见verification_20261005.md，本次没有把历史记录冒充为修复后的全分辨率复测。

新的bit路径：`td_project/camera_to_dsi_display_Runs/phy_1/camera_to_dsi_display.bit`，1789539字节。

SHA256：`91f0c661a61b8d735bf3f40075994584d410dac06556d62e28011b7f5b7947b5`。源文件指纹见build_manifest.json。后续修改RTL需重新生成bit。完整资源统计见本次phy_1/camera_to_dsi_display_phy.area。

继承的相机I2C/相机时钟混合扇出、局部时钟布线告警在基线中也存在，最终STA通过。实际图像仍需要用户在同样场景与显示器条件下检查；本报告只确认已修复官方原图链路及完成上述工具验证。
