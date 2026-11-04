# UART V2：算法、ROI、图片与输入源

2026-10-15扩展，原MODE=01编码不变。115200 baud、8N1、无流控；FPGA50MHz/434周期。J1=FPGA RX、H1=FPGA TX（本工程pin.adc）。不能只改Python波特率。

```
AA 55 | 02 | SEQ:u8 | CMD:u8 | LEN:u8 | DATA[LEN] | CRC16_LE | 0D 0A
```

整帧10+LEN字节，LEN最大240，图片DATA最大232。多字节参数均小端。CRC16/CCITT-FALSE：poly1021、initFFFF、无反射、xorout0，覆盖02至DATA；123456789→29B1。负载可含AA55/0D0A，按长度解析。错误CRC/版本/尾字节丢弃，由超时重传；RTL字节间20ms、PC解码器100ms清除半帧。

响应沿用SEQ。ACK=81，DATA=`请求CMD:u8,00,响应体`；NACK=82，DATA=`请求CMD:u8,错误码:u8`。错误码：0成功、1不支持、2长度错误、3越界、4忙/会话冲突、5无有效图片、6偏移/总长度错误、7整帧CRC/尾字读回错误、8DDR未就绪/会话不存在、9超时（保留）。02/80未实现；90预留ROI主动上报，本版使用查询。

## 命令

| CMD | 请求DATA | 成功响应体 |
|---|---|---|
| 01 MODE | mode:u8，0～11 | 实际mode:u8；实际更新后确认 |
| 03 GET_STATUS | 空 | 下述18字节 |
| 10 ROI_CONFIG | 下述12字节 | 已在帧边界应用的12字节 |
| 11 ROI_QUERY | 空 | 下述37字节 |
| 20 SOURCE_SELECT | source:u8，0Camera/1PC Image | 实际source:u8；帧间切换后确认 |
| 30 IMAGE_BEGIN | id:u32,W:u16,H:u16,format:u8,total:u32,crc32:u32（17字节） | id:u32 |
| 31 IMAGE_DATA | id:u32,offset:u32,像素数据（16～224字节、16的倍数） | id:u32,next_offset:u32 |
| 32 IMAGE_END | id:u32,crc32:u32 | id:u32,crc32:u32；校验、尾字读回、视频域发布完成后确认 |
| 33 IMAGE_ABORT | id:u32 | id:u32；丢弃未提交会话，保留上次完整图片 |

BEGIN仅接受1920×1080、format=1、total=4147200。RGB565位定义R[15:11]/G[10:5]/B[4:0]，左上角起、从左到右逐行、无填充，每像素低字节先发。PC解码PNG/JPEG/BMP后发送像素，不发送压缩文件。

整帧CRC32/ISO-HDLC：reflected polyEDB88320、initFFFFFFFF、xoroutFFFFFFFF，与`zlib.crc32(pixel_bytes)`相同；123456789→CBF43926。仅覆盖像素字节，不含id/offset；每包另有CRC16。

## 状态

GET_STATUS18字节，Python`<BHHIBBBIH`：schema:u8=1，源W:u16，源H:u16，caps:u32，mode:u8，source:u8，committed_image_valid:u8，committed_bytes:u32，roi_revision:u16。源尺寸本工程1280×720，不是采集卡或上传尺寸。caps位0 MODE_ACK、位1 ROI、位2 IMAGE_UPLOAD、位3 SOURCE_SWITCH、位4 NATIVE_1080_IMAGE，本版31。committed_bytes=0或4147200，不是实时上传进度。

ROI_CONFIG12字节，`<BBBBHHHH`：enable、traffic、strict、HDMI_border各u8（0/1），x0,y0,x1,y1各u16。左上角原点，左闭右开`[x0,x1)×[y0,y1)`；width=x1−x0、height=y1−y0。0≤x0<x1≤1280，0≤y0<y1≤720，不要求四像素对齐。默认关闭、traffic=1、strict=0、border=1、坐标480,180,800,540。border是FPGA两像素白边，不等同GUI框/原核心mask。

ROI_QUERY37字节：schema:u8=1 + 已应用配置12字节 + revision:u16 + completed_frame:u32 + result:u8 + warmed_up:u8 + red/yellow/green/blue_count各u32。视频域同一拍快照后握手回传。counts为最近完整帧，result为三帧多数投票；0UNKNOWN、1RED、2YELLOW、3GREEN、4BLUE。traffic模式忽略蓝；前两帧/配置变化后预热。GUI每秒查询，上传期间暂停，不做Python颜色识别。

保留阈值：普通最低100、优势30；严格150/50；黄色R/G差≤60；最小128像素、类别优势32。未开放任意数值阈值寄存器。ROI观察的是所选输入进入算法图前的RGB，Camera为官方AWB，PC为RGB565展开/缩放，不在Sobel/二值结果上判色。

## 调度与重试

SerialManager独占串口；RequestScheduler一次一条在途、队列≤32。普通超时1.5秒、额外重试3次；GET_STATUS0.8秒额外1次；SOURCE_SELECT3秒；上传2秒额外3次。重试保持CMD/SEQ/完整帧。缺少视频帧/时钟时MODE/ROI可能超时，不显示已应用。

FPGA缓存最近CMD/SEQ/帧CRC16及回复，丢ACK不重复提交。图片额外核对ID、连续偏移及上一包签名；每次新上传随机32bit ID。BEGIN同ID/同描述不重置进度。DATA ACK在全部128bit写请求被DDR有序命令队列接受后返回。END验证总长度及整帧CRC，再通过同队列读回最后128bit作栅栏，等待视频域帧间发布确认。CRC检查接收字节；尾字栅栏不是整帧DDR逐字读回CRC。

上传独占调度器，模式/ROI/源控制暂停，采集/截图继续。进度按DATA ACK增加，100%后仍等待END。取消等当前包边界再ABORT；未收到取消ACK显示未确认。END已发可能已提交，ABORT不撤销已完成图片，需查实际状态。

115200/8N1纯像素理论360秒；224字节分18515包，含帧/ACK理论约421秒，实际另加调度/DDR等待/重传。目标是单张静态图片，不是UART视频。

## 兼容性

原模式帧保持，例如mode0 `AA 55 02 00 01 01 00 8E 51 0D 0A`、mode4 `AA 55 02 00 01 01 04 0A 11 0D 0A`、mode5 `AA 55 02 00 01 01 05 2B 01 0D 0A`。

新PC查询实际能力。旧V2不回包时保留原模式发送路径并显示请求状态，新功能禁用。新功能须新bitstream；历史协议在docs/PROTOCOL_LEGACY_MODE_ONLY.md，仅供参考。V1不兼容本工程模式映射。
