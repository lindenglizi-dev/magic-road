# FPGA Vision Control System：集成与阶段验收

2026-10-15，直接扩展现有`applications/stage3_7_uart`，没有创建独立上位机。初始扫描见[INTEGRATION_ANALYSIS.md](INTEGRATION_ANALYSIS.md)，字段/错误码/重试见[../PROTOCOL.md](../PROTOCOL.md)，测试和构建结果见[../reports/vision_verification.md](../reports/vision_verification.md)。

## 真实数据流和分辨率

```
SC520 1280×720 RAW10 → CSI → 四像素RAW10 → demosaic → 官方AWB ─────┐
                                                                ├→ 帧间源选择
PC图片 → RGB565编码 → UART → 备用DDR图片区 → CRC/尾字校验          │
 → 帧间发布 → 1920×1080逐行读取 → FPGA 3:2采样/四像素RGB888 ──────┘
 → 旁路ROI颜色统计 + 原0～11算法图 → 可选FPGA ROI边框 → 原OSD/logo
 → RGB888连续打包128bit → 原video_in → 原四槽DDR → 原video_out
 → 1280×720 HDMI → 分配器 → 显示器 / USB采集卡 → 预览/原始帧截图
```

有效RTL是720P，摄像头寄存器、CSI字节数、ISP、DDR行突发、HDMI VTC一致；1080常量位于未实例化模块。上传原生1920×1080 RGB565存DDR，FPGA按x/y=0,1,3,4…采样至1280×720进入原图像算法。**没有升级传感器/HDMI为1080P，也没有在PC放大图像冒充1080P**。实际采集卡帧尺寸另行测量显示；另有1080P工程时必须重新核查整条链。

Camera模式0/1保留偏绿修复，均使用官方AWB流。PC模式0/1均使用RGB565展开值，绕过传感器AWB，避免静态图干扰已验证的摄像头增益；后级二值、中值、Sobel、锐化、Gamma等仍由FPGA原算法执行。ROI观察源选择后的RGB，位置在算法图之前；Sobel显示黑白时ROI仍检测所选输入原色。

当前算法配置是原图和1～11，含灰度二值化及灰度邻域处理，没有独立纯Gray菜单；本次保留现有编号，没有擅自新增或重新编号算法。

## Python文件与架构

| 相对pc_upper路径 | 职责 |
|---|---|
| main.py | 保留原入口，实例化扩展窗口 |
| gui/main_window.py | 原串口、配置驱动算法、日志控件保留 |
| gui/vision_window.py | 组合原控件、预览、源选择、标签页及安全退出 |
| gui/roi_overlay.py / roi_panel.py | 鼠标框选、GUI叠加、ROI草稿/已应用状态、保存加载 |
| gui/upload_panel.py | 本地预览、图片信息、进度/速率/ETA/取消 |
| communication/serial_manager.py | 原有唯一pyserial拥有者，QThread+Queue |
| communication/protocol.py / image_protocol.py | 统一V2帧与类型、能力/错误码、ROI/图片字段 |
| communication/request_scheduler.py | 一条在途、匹配ACK、同包重试、上传独占 |
| services/fpga_controller.py / roi_controller.py | 模式/源/ROI业务及硬件确认 |
| services/video_capture.py | DirectShow枚举、独立采集线程、实际尺寸与FPS、最新不可变帧 |
| services/screenshot_manager.py | 复用最新有效帧，后台PNG/JPG/BMP、Unicode路径 |
| services/roi_geometry.py | 黑边/缩放/反向拖动/边界换算，独立测试 |
| services/image_converter.py | 后台解码、补边/裁剪、1920×1080 RGB565 LE、CRC32 |
| services/image_uploader.py | ACK/定时器驱动异步上传，不另开串口读写 |
| services/settings_store.py | config/session.json原子保存；截图目录/视频索引 |
| tests/ | 原测试及视频、ROI、截图、上传测试 |

视频、设备枚举、图片转换和截图分别用工作线程。上传状态机不循环等待ACK，所有串口事务由原SerialManager和调度器完成。窗口关闭先取消上传并等待工作线程，再关闭串口，不强杀QThread。极端DirectShow驱动永久阻塞open/read时，安全退出仍依赖系统驱动恢复/设备拔插。

## RTL/工程修改

新增`rtl/uart_frame_rx.v`、`uart_frame_tx.v`、`vision_uart_control.v`、`vision_video_control.v`：通用V2、CRC、回复缓存、CDC请求/状态握手。原uart_rx复用；旧uart_mode_link/protocol仍在工程作历史参考/旧测试，不再实例化于顶层。

新增`rtl/color_traffic_core.v`：复制既有color_traffic核心，只增加坐标/enable和帧状态；原classify、优先级、阈值和三帧投票逐段审计保留。新增`roi_border_overlay.v`可关闭两像素白边，默认ROI关闭。

新增`rtl/image_upload_engine.v`：会话/连续偏移、CRC32、16字节写请求、尾字读回、双缓冲发布。`image_ddr_bridge.v`：系统/视频到DDR的稳定数据mailbox、空闲插槽仲裁、读owner队列。`pc_image_replay.v`：1080P读取、RGB565展开、3:2取样、四像素打包、源选择。

修改`user_source/hdl_source/design_top_wrapper.v`接独立适配器/DDR分流；`isp/isp_top.v`在AWB后加源适配器和ROI旁路；`rtl/stage3_7_runtime.v`增加busy和算法后边框一拍；`update_algorithms.py`同步模板。`.al`和syn/phy项目纳入新RTL。**原图像内核、video_in/out、mc_to_user_interface、时钟频率和引脚未重写**。

## ROI接入与坐标

原ROI不在当前工程实例化，坐标为综合期参数，本次增加动态配置端口。系统域保持整包直到视频ACK；toggle两级同步，数据在握手期间稳定。视频域shadow在early且runtime空闲时提交applied/revision，算法只在early锁存；新帧数据到达前HDMI边框配置同步生效。

原点左上角0,0，终点不包含，width=x1−x0、height=y1−y0。鼠标通过QWidget等比例显示矩形（含黑边）→实际采集像素→FPGA源坐标，非固定乘2；反向拖动、窗口变化、末端夹紧、整数向外取整均支持。采集比例与源不符时拒绝框选，不猜未知裁剪；仍可手输RTL坐标。

默认采集帧完整对应HDMI有效画面，采集卡须关闭裁剪/缩放填充。RoiGeometry底层支持已知补边content矩形；GUI尚无任意采集裁剪校准面板，未知裁剪需先校准/关闭。比例相同不能证明没有裁剪，需检查完整OSD/logo/画面边缘。

草稿黄色，只有真实ROI返回且配置一致才转绿。保存/加载是草稿，必须应用；加载源尺寸不一致拒绝。清除操作框不关FPGA ROI，关闭须取消启用并应用。截图不含GUI叠加，但包含FPGA实际OSD/白边。状态每秒查询，上传期间暂停，所有检测结果来自FPGA。

## DDR容量、一致性与CDC

DDR16bit、25bit用户地址，单位16bit字，128bit请求步进8。按当前控制器13行+10列+2bank位配置，可寻址2^25×2=64MiB；尚未通过颗粒BOM/上板实测确认物理容量，高地址bank需作为上板首项检查。

| 区域 | 16bit字地址（左闭右开） | 有效字节 |
|---|---|---:|
| 原视频槽0 | [0,1382400) | 2764800 |
| 原视频槽1 | [7000000,8382400) | 2764800 |
| 原视频槽2 | [14000000,15382400) | 2764800 |
| 原视频槽3 | [21000000,22382400) | 2764800 |
| 图片bank0 | [25165824,27239424) | 4147200 |
| 图片bank1 | [27239424,29313024) | 4147200 |
| 物理地址上限 | 33554432 | 67108864总容量 |

不以BRAM存整帧，仅包RAM、mailbox和小owner队列。上传写非已提交bank，旧图片可继续播放。DATA ACK指请求已进入有序MC队列；END验证接收全帧CRC后，顺序读回最后128bit作写入栅栏，再等视频帧间发布ACK。尾字读回不是全DDR内容CRC。上传中断/CRC失败不发布备用bank；ABORT不撤销已完成提交。

Aux只在VI/VO突发均空闲、注册VI写尾拍结束时插入，保留原ready后8拍余量。每个入队读保存owner，包括MC FIFO内未执行请求；按序将DDR返回分给video/upload/replay，PC读不会进入显示FIFO。owner深1024，1000后视频背压，留流水尾拍余量；upload/replay各仅一个DDR在途。mailbox发送数据稳定至返回ack，控制toggle两级同步，无异步多位直接实时采样。

源切换等算法图排空及PC帧结束；回Camera再等摄像头early，避免半帧。PC仍使用原CSI处理时钟，**摄像头必须连接并持续供给CSI时钟**，本版不支持拔掉摄像头独立运行PC Image。

720P RGB888@60fps视频写/读各约165.9MB/s，合计331.8MB/s，未计DDR协议开销。PC适配每帧172800次128bit读=2.7648MB，帧间至少1000万处理时钟，处理帧率受mailbox/仲裁影响；HDMI按原时序刷新静态结果。115200上传约11.5kB/s，DDR带宽占用小。资源/时序最终值见验证报告；DDR长时稳定、FIFO余量和板级裕量仍需实测。

## 启动和操作

1. TD6.2.1打开`td_project/camera_to_dsi_display.al`，顶层design_top_wrapper，下载本次通过时序的最新bit。构建：`powershell -ExecutionPolicy Bypass -File run_td.ps1`。旧MODE-only bit不能验收新功能。
2. 接摄像头、开发板USB-UART、HDMI分配器；一路显示器，另一路UVC采集卡连PC，优先USB3。Windows允许桌面相机访问，关闭OBS/会议软件等设备占用。
3. 工程目录运行`./pc_upper/run.ps1`或`E:/anaconda3/python.exe ./pc_upper/main.py`。换电脑Python3.10+，`python -m pip install -r pc_upper/requirements.txt`；run.ps1可用-Python指定解释器。当前deps有pyserial/OpenCV，复用已有PySide6/NumPy。
4. 选开发板实际COM、115200连接，等GET_STATUS。驱动已连接与FPGA已确认分开显示，旧固件仅模式控制可发请求。
5. 枚举/选择HDMI设备索引，开始预览。1280×720与源一致；1920×1080仅向采集卡请求，以实际read尺寸/FPS为准。设备断开停止后可重连。
6. 原图和1～11算法仍按algorithms.json动态生成。ROI框选/输入→应用→确认→读数；保存/加载后需再应用。
7. 选PNG/JPG/BMP，按补边/裁剪方式转换，检查4147200字节和预览后上传。END确认后选PC Image，切换Sobel/锐化等，无须重传。上传中暂停普通控制，预览/截图继续。
8. 截图页默认pc_upper/screenshots和PNG，复用最新有效原始采集帧；可改格式/目录、打开目录，不重开设备、不截整个窗口。

## 验收边界

软件fixture、RTL仿真、TD实现和实机联调分别记录，不互相替代。开发板实际UART往返、ROI白边移动与回传、完整1080P上传时长/取消、DDR长时与显示器/采集卡同步显示需连接实际硬件后逐项验证；不得以软件图像或仿真结果代替。
