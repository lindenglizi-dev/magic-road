# FPGA Vision Control System：阶段1现状审查（2026-10-15）

## 当前上位机

入口pc_upper/main.py，PySide6；main_window.py包含串口行、配置驱动算法区和1500行日志。communication/serial_manager.py是唯一pyserial访问点，QThread+Queue负责收发，Signal回GUI；services/fpga_controller.py将配置ID映射为模式命令。算法配置为config/algorithms.json，没有用户会话设置持久化。

现有协议：AA55 / VERSION=02 / SEQ:u8 / CMD:u8 / LEN:u8 / DATA / CRC16小端 / 0D0A；CRC16/CCITT-FALSE覆盖VERSION至DATA。MODE=01保留，02参数、03状态、80结果、81 ACK已预留。Python通用解析器最多64字节，RTL实际只接受MODE、LEN=1、0～11；TX固定高电平，无硬件确认。图像上传需扩展完整命令解析与TX，不能把发送成功标作已应用。

## 实际有效视频链

摄像头配置uicfgcs520实例的uics520reg_720p60写3208/3209=0500、320A/320B=02D0，输出1280×720 RAW10；两Lane，RAW每拍40bit=四个10bit像素。CSI诊断检查每行800个16bit Lane word（1600字节）和720行。

uial2axis实际实例1280×720 → RAW10解包 → demosaic（实际1280×720、BGGR） → RGB128/96转换（每32位取24位并排列为四个{R,G,B}，最高24位为最左像素） → AWB → 四像素/拍RGB888算法及OSD → 96/128无填充打包 → video_in → DDR → video_out → hdmi_mixer → HDMI。

HDMI实际uivtc H_ACTIVE=1280、H_TOTAL=1650，V_ACTIVE=720、V_TOTAL=750；mixer有效窗口1280×720、无裁剪偏移。ISP中IN_HEIGHT=1080的axis_crop_rgb96未实例化，不能据此认定1080P。采集卡即便返回1920×1080，也不证明FPGA源为1080P，必须分别显示采集尺寸和FPGA源尺寸。

每帧921600像素，RGB888为2764800字节，230400个96bit组，172800个128bit字；每行240个DDR字。AWB提前帧通知保留供video_in FIFO复位，不能用算法首像素替代。0号原图使用官方AWB校正流，保留此前偏绿修复。

## ROI现状

ROI只在applications/color_traffic/rtl/color_traffic_core.v（及motion_mask派生副本），未实例化于stage3_7_uart。属于“综合前固定参数”：X0=480,Y0=180,X1=800,Y1=540，左闭右开[x0,x1)×[y0,y1)，单像素坐标，四像素逐个判断，不要求X按4对齐。已有运行输入traffic/strict/mask，但没有坐标、enable配置总线。

颜色编码0未知、1红、2黄、3绿、4蓝；黄先于红/绿/蓝匹配。普通阈值floor=100,delta=30；严格floor=150,delta=50；黄需R/G差不超过60。计数胜出需MIN_PIXELS=128、DOM_MARGIN=32，交通灯模式忽略蓝；最近三帧多数投票，未知也参与，前两帧预热未知。result为投票结果，frame_result为单帧结果，red/yellow/green/blue_count已有32bit输出；当前runtime将计数悬空。模式或strict变化会清投票。

最小接入：复制现有核心到当前工程并只将坐标、使能增加为输入寄存器，阈值与投票公式不改；在帧边界整体提交。输出作旁路检测/可选ROI边框，在算法选择后接入；UART使用握手mailbox传配置/快照，提交后才能ACK。

## DDR现状与后续输入源接入

video_in和video_out的四槽基址为0/7000000/14000000/21000000，地址每128bit请求加8；必须结合DDR16bit物理配置确认单位（见后续内存图），不能当作字节地址。当前只仲裁VI写和VO读，读返回未带tag直接进显示FIFO，不能直接新增图片读请求，否则会污染HDMI。mc_to_user_interface有512深命令FIFO，ready低后仍可容纳8条，读命令要求MC的app_rdy和wdf_rdy。

图片上传需要独立保留DDR区域、写入适配器、第三/第四请求方仲裁、读返回owner队列及FIFO水位管理；完整CRC通过才发布新图片，Camera/PC源在算法安全帧边界切换。1920×1080 RGB565=4147200字节，不能用剩余片上BRAM保存。当前完整闭环不存在。

## 分阶段实施与验收

A在原GUI增加采集线程/设备枚举、真实frame.shape和测量FPS、等比显示与原帧截图。B增加可测试ROI映射及保存/读取状态。RTL接口完成前必须显示“未确认/固件不支持”。C/D以统一调度器扩展原协议，只有FPGA ACK才能推进上传；缺少完整DDR接入时必须拒绝能力，不得伪造上传成功。保留MODE=01、V2帧布局及原算法编号。
