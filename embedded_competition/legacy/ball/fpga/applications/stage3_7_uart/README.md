# FPGA Vision Control System（现有工程集成版）

2026-10-15新增HDMI采集预览/原始帧截图、动态ROI及硬件确认、1080P RGB565 UART分包上传、双DDR图片缓冲/重放、Camera/PC Image帧间切换。**有效视频链仍是1280×720**；上传1920×1080由FPGA适配至720P复用原算法，不冒充1080P输出。完整文件说明、操作和限制见[集成说明](docs/VISION_INTEGRATION.md)，字节协议见[PROTOCOL.md](PROTOCOL.md)，本次结果与硬件待验项见[验证报告](reports/vision_verification.md)。

当前工程实际位于 `fpga/applications/stage3_7_uart`（相对仓库根目录）；本说明其余路径除特别注明外均相对当前应用目录。器件 PH1P35MDG324（-3），SC520、1280×720、四像素/拍、DDR 和 HDMI 链路保持使用。算法预先综合进 bitstream；上位机经 USB-UART 请求切换模式，按键同样可用。

## 打开、下载和启动上位机

1. TD 6.2.1 打开 `td_project/camera_to_dsi_display.al`，顶层 `design_top_wrapper`。
2. 下载本目录生成的 `td_project/camera_to_dsi_display_Runs/phy_1/camera_to_dsi_display.bit`。V2 与旧 mode 映射不兼容，必须同时使用本目录的 FPGA bit 和更新后的上位机。
3. 连接摄像头、HDMI、开发板 USB，启动后 mode=0，显示官方 ISP 原图（已包含 AWB 校正）。
4. PowerShell 执行：

   ```powershell
   python pc_upper/main.py
   ```

   或运行 `./pc_upper/run.ps1`；可通过 `-Python` 指定解释器。其他电脑先执行 `python -m pip install -r pc_upper/requirements.txt`。本机 pyserial 放在 `pc_upper/deps`，PySide6 使用已有安装。
5. 选择开发板实际 COM 口，115200，点击连接，再选择算法。COM 编号由系统分配，不能固定为某一号码。
6. 等待FPGA状态/能力确认，再枚举HDMI采集卡并开始预览。新版TX返回实际MODE、ROI和源切换确认；旧bit无应答时保留模式请求路径，新功能禁用。串口打开/写入成功本身不代表FPGA确认。

## 编号和处理定义

编号在按键、UART、图像 MUX、上位机和 OSD 中一致。0号原图单独显示在基础输出区；算法区从左到右、逐行按1～11排列。

| mode | 中文 | OSD 英文 | 当前实现 |
|---:|---|---|---|
| 0 | 原图 | ORIGINAL | 官方 ISP 的 AWB 校正输出，与官方原图链路一致 |
| 1 | 白平衡 | WHITE BAL | 已有自动白平衡 AWB，以绿色通道参考调整 R/B 增益 |
| 2 | 灰度二值化 | BINARY | Y=(77R+150G+29B)>>8，Y≥128为255，否则0 |
| 3 | 中值滤波 | MEDIAN | 精确3×3灰度中值；九级比较交换网络 |
| 4 | 边缘检测 | SOBEL | 3×3 Sobel，\|Gx\|+\|Gy\|≥128为白色 |
| 5 | 锐化 | SHARPEN | 灰度：5×中心−上−下−左−右，饱和到0～255 |
| 6 | 伽马矫正 | GAMMA | RGB逐通道，round(255×(C/255)^0.7)，256项查表 |
| 7 | 对比度调节 | CONTRAST | RGB逐通道，floor((5C−128)/4)，即中心128、1.25倍 |
| 8 | 亮度调节 | BRIGHTNESS | RGB逐通道加32，饱和到0～255 |
| 9 | 饱和度调节 | SATURATION | floor((3C−Y)/2)，即Y+1.5×(C−Y)，饱和到0～255 |
| 10 | 腐蚀-膨胀 | ERODE-DILATE | 灰度二值化结果，3×3全1结构元素，先腐蚀后膨胀 |
| 11 | 膨胀-腐蚀 | DILATE-ERODE | 灰度二值化结果，3×3全1结构元素，先膨胀后腐蚀 |

0号原图及其他算法均使用官方 AWB 校正流；1号仍表示该 AWB 输出，因此0/1两模式当前除OSD名称外颜色相同。3/4/5号输出灰度或黑白，不是RGB彩色中值/彩色锐化。邻域不完整处置黑；两次形态学操作各自重新建立窗口，第二次操作沿用边界置黑规则。

参数目前为固件默认预设，未加入 UART 参数写入或 GUI 滑块。`rgb_point_adjust_4px.v` 的二值阈值、亮度为编译参数；对比度、饱和度使用移位加法；Gamma 修改 `generate_point_adjust.py` 后重新生成 LUT。修改硬件参数后需重新生成 bitstream。

腐蚀→膨胀和膨胀→腐蚀在数学上分别等价于开运算、闭运算。本工程删除了旧包装模块、旧编号和名称，按用户指定名称接入新的独立两级链路；没有保留重复菜单。

## 已删除的旧文件

从当前工程 `rtl` 和 `.al/.prj` 清单删除：

- `binary_open_4px.v`、`binary_close_4px.v`；
- `binary_denoise_4px.v`、`binary_fill_holes_4px.v`；
- 依赖旧算法的 `binary_cleanup_4px.v`、`binary_cleanup_stream_4px.v`、`binary_morph_top.v`、`image_algorithm_stage7_96.v`；
- 本菜单不再使用的 `gaussian_filter_4px.v`、`gray_filter_stream_4px.v`。

只保留基本腐蚀/膨胀核，供10/11号链路复用。早期历史/参考工程仍保留在其他目录；它们不参加当前工程编译。

## OSD 与按键

左上角安路 logo 保持128×80、距边缘16像素；右上角416×80面板显示编号、中文名称和英文名称。所有输出包括原图都经过同一个 OSD。`generate_osd.py` 从上位机配置读取标签，字模和 logo ROM 嵌入 RTL，不依赖运行时 mem 文件。

| 按键 | 引脚 | 功能 |
|---|---|---|
| KEY0 | D5 | 1～11循环中的上一个算法 |
| KEY1 | A9 | 1～11循环中的下一个算法 |
| KEY2 | B9 | 返回1号白平衡 |
| KEY3 | C7 | 原图0 ↔ 白平衡1，回原图时锁定KEY0～2 |

同步、消抖和长按单次触发保留。有效按键事件与UART同拍时按键优先；不同拍按到达顺序处理。UART可从原图直接进入任意算法，无需先按KEY3。所有来源共用一个 requested_mode，避免按键跳回旧状态。

模式请求在 AWB 提前帧通知到来且上一帧所有算法支路排空后才提交 active_mode。逐支路记录完成事件，再等待8拍让MUX、OSD和打包排空。当前帧内 mode 不变，像素/有效/行末/帧末同步选择。

## UART 与软件分层

RX=J1，TX=H1，LVCMOS33。UART使用50MHz I_sys_clk，115200/8N1，无流控。接收模块双触发器同步；协议校验后通过握手mailbox进入S_csi_rx_clk域。共享复位断言、各域同步释放。相机时钟停止时保持在途数据和最后一个待处理请求，恢复后收敛到最新请求。无帧通知时只保存请求。

V2帧格式和CRC示例见 `PROTOCOL.md`。当前RTL已实现模式、状态、ROI、输入源、静态图片上传及ACK/NACK；SET_PARAM、RESULT和ROI主动推送仍未实现，当前使用ROI查询。V1帧被拒绝，防止旧mode=10原图命令被解释成新10号算法。

`pc_upper/config/algorithms.json` 定义编号、名称、英文、说明及source/algorithm分区，GUI动态创建控件并展示工具提示。串口操作集中在 `communication/serial_manager.py` 的工作线程；协议层是纯Python；`services/fpga_controller.py`负责ID到命令的转换；GUI不直接操作pyserial。

## 生成与验证

在本目录执行：

```powershell
& E:/anaconda3/python.exe generate_point_adjust.py
& E:/anaconda3/python.exe update_algorithms.py
& E:/anaconda3/python.exe generate_osd.py
& E:/anaconda3/python.exe audit_uart_project.py
& E:/anaconda3/python.exe pc_upper/tests/test_upper.py
./sim/run_verify.ps1
./sim/run_unit_verify.ps1
./sim/run_original_verify.ps1
./sim/run_uart_verify.ps1
./sim/run_uart_verify.ps1 -Full
./run_td.ps1
```

`update_algorithms.py` 生成当前固定硬件目录映射和默认配置，会覆盖手工配置；日常只增删GUI入口时直接修改JSON并重启即可，不要运行该生成器。新硬件算法仍需修改该生成器中的支路映射和RTL、OSD、合法mode范围及测试，再重新综合。

不要并行生成不同尺寸的仿真向量，脚本共用 `input.hex/input_wb.hex/expected.hex`。默认测试640×112，`-Full`为1280×720。UART集成仿真为了减少空拍运行时间，将解析器超时缩短为0.2ms；独立协议测试验证实际20ms超时。白平衡旁路测试使用厂商IP接口的行为模型，说明其验证边界；厂商原始IP参与真实综合布线。

最新验证见 `reports/vision_verification.md`，新增界面预览为 `reports/vision_roi_gui.png` / `vision_upload_gui.png`（无硬件确认的真实GUI空画面）。`reports/verification.md`、`pc_upper_preview.png`及`rtl_algorithms_preview_20261005.png`是历史结果，不能代表本次硬件联调。历史拼图的白平衡支路是MUX测试流，不是相机实拍。

## 上板验收

下载V2 bit并启动V2上位机后，逐一检查0～11的图像与OSD；每次间隔约0.2秒循环至少100次，检查缺行、花屏、撕裂和模式错位。UART选算法后测试KEY2/KEY3；测试拔插、重连及错误CRC帧。上位机重连不会自动重发旧模式。

当前已执行的软件、RTL和TD验证不替代摄像头与HDMI实测。实板下载和画面检查尚需完成。

## 2026-10-10 原图偏绿修复

上一版将原图输入误接为awb_uncorrected。官方原图在awb后输出，绕过该校正会把传感器的偏绿带入HDMI；本次恢复为awb_O_tdata，所有算法使用同一官方颜色基线。没有额外调红/绿/蓝增益，也没有修改摄像头寄存器、Bayer排列或HDMI通道。生成脚本同步修复，避免重建后再次退回未校正旁路。

新增run_original_verify.ps1测试实际isp_top接线：普通偏绿RGB输入经过现有AWB，逐字节检查0→1→0输出与AWB基准相等，核对通道顺序、行/帧标记、像素数量和流水排空。摄像头前端及厂商IP接口使用行为模型，测试不代表实板拍摄；新bit下载后需对照官方原图实拍复核。该测试暴露了原有runtime单模块测试未覆盖的ISP接线问题。

## 2026-10-16 仓库整理说明

本次仅修正文档中的入口路径和过时协议描述，未改变RTL、Python业务或工程配置。详细入口见[FPGA模块说明](../../README.md)，PC维护入口见[PC说明](../../../pc-software/README.md)。迁移后的绝对路径、历史基线缺失及生成脚本风险见[整理报告](../../../docs/repository_preparation_report.md)；不要按历史命令直接运行生成器。
