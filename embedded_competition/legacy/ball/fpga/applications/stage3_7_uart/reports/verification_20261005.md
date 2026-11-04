# 算法菜单 V2 验证报告

> 仓库范围说明（2026-10-16）：本文是原始技术/验证记录，正文保留。其引用的原始日志、历史bit、第三方PDF或个人DOCX仅保留在本地，不随源仓库提交；这些本地附件不能视为GitHub中的可下载文件。历史结果不替代当前版本的实板验收。

验证日期：2026-10-05。当前工程已覆盖升级，mode=0原图，1～11按用户指定顺序。旧四项算法包装/去噪/补孔文件及其编译引用已删除。

| 检查 | 结果 | 证据 |
|---|---|---|
| UART 640×112，13帧、所有模式、错误帧/CDC/复位 | PASS | `reports/uart_v2_console.log` |
| UART 1280×720，13帧、所有模式、逐像素与行帧标记 | PASS | `reports/uart_v2_full_console.log` |
| 按键640×112，原图+11算法+返回原图共13帧 | PASS | `reports/keys_v2_console.log` |
| FIFO reset/recovery边界 | PASS | `sim/fifo_boundary.log` |
| 协议V2/旧V1拒绝、非法mode/CMD/CRC/帧尾、实际20ms超时 | PASS | `sim/tb_protocol_v2.log` |
| 白平衡未校正旁路、像素顺序、有效及增益对齐、饱和 | PASS | `sim/tb_awb_bypass.log` |
| Python配置增删、动态Qt控件、协议及pyserial回环 | PASS | `reports/python_v2_tests.log` |
| TD6.2.1综合、布局布线、bitstream | PASS | `td_project/camera_to_dsi_display_Runs/phy_1/console.log` |
| 最终 setup/hold | SWNS **+0.114ns**，HWNS **+0.020ns**；STNS/HTNS均0 | `camera_to_dsi_display_pr.timing` |
| 工程清单、删除项、OSD/config编号、引脚 | PASS | `audit_uart_project.py` |
| GUI中英文按钮、RTL logo及编号标签 | 已渲染检查 | `reports/pc_upper_preview.png`、`reports/rtl_algorithms_preview.png` |
| 实板下载、摄像头/HDMI画面与重复切换 | **尚未执行** | 按README上板验收 |

bit路径：`td_project/camera_to_dsi_display_Runs/phy_1/camera_to_dsi_display.bit`，1789539字节。

SHA256：`0780946fdd34db858ea685fff5f3fb78d9fec0bd3b16cf5cd989e6488ed442f5`。

资源：LUT6 13934/21216（65.68%），寄存器18897/42432（44.53%），slice16347/21216（77.05%），ERAM66/108，DSP20/40。源文件和bit指纹见 `reports/build_manifest.json`。后续改RTL或参数必须重新构建。

像素测试使用独立NumPy模型，包含彩色梯度、黑白端点、实心前景、小孔与孤立噪声。逐字比较包括OSD在内的完整输出；同时检查有效像素总数、行末、帧末、帧内模式不变和所有支路排空。中值为真实九输入中值，二次形态学处理重新建窗口。

UART输入为实际115200/8N1位波形、独立50MHz与约103.52MHz时钟。集成仿真的字节间超时缩短为0.2ms以降低空拍开销；单独协议仿真验证固件实际20ms超时。覆盖接收时钟暂停期间多次请求、恢复后最后请求、UART后按键操作、长按/回绕/锁定/复位和V1帧拒绝。

全模式图像测试向runtime提供一条刻意不同的白平衡测试流，证明1号确实选择校正支路，0号保留原图。AWB旁路测试另执行现有awb.v、signal_delay.v，使用厂商除法器/BRAM接口的行为模型，验证变动像素顺序、校正增益与未校正像素同拍对齐、通道顺序及饱和。这不是厂商IP门级时序仿真；原厂IP参与真实综合布线。RTL拼图是640×112测试输出，不是相机实拍。

继承工程的PHY-5060相机I2C/相机时钟混合扇出告警及PHY-5079局部时钟布线告警仍存在，在历史基线构建中也存在。最终STA通过，无UART约束失配告警。setup正裕量较小（0.114ns），改动后必须重新检查布局布线时序。

当前调节算法使用固定默认预设：二值阈值128、Gamma0.7、对比度1.25倍、亮度+32、饱和度1.5倍。没有实现UART参数修改。TX固定空闲，无ACK/状态回传；界面显示模式请求，无法自行确认HDMI实际效果。
