# 摄像头采集组件 TB 规格

## 证据边界

本验证只覆盖 `road_area_resize` 和 `road_capture_slots` 两个同控制时钟组件。`write_visible` 与 `last_read_consumed` 是 testbench 驱动的受控外部合同事件，不代表真实 PAXI 写可见、读响应退休、跨域同步或实板 DDR 屏障。未验证 TD、布局布线、资源、时序、位流、板卡、Flash、训练或真实 2 FPS 连续运行。

## `road_area_resize`

输入为 1280×720 RGB，每拍 AWB96 的像素先后顺序为 `[95:72]`、`[71:48]`、`[47:24]`、`[23:0]`，每 lane 内 `R/G/B = [23:16]/[15:8]/[7:0]`。正常流量每行 320 个连续 valid 拍，随后 480 个空拍；SOF 在首 valid 前独立出现，EOL 只在第320个有效拍。

输出必须是 512×288 RGB，共 147,456 像素、442,368 bytes。合法 mask 仅 `00/01/11`，mask01 使用 `o_pixels[23:0]`，mask11 的第二像素使用 `[47:24]`；每像素均按低字节 R/G/B。SOF、EOL、EOF 必须分别严格落在第一个像素、每行最后一个像素和全帧最后一个像素，不能在 mask00 时出现。

完整帧逐像素与冻结 CPU golden 比较：编号彩条验证 lane/字节/四边和行边界，seed `20261015` 随机帧验证一般数值，全255验证13-bit最大二维和6375及最终255。CPU golden 只在二维权重累加后做一次 `(sum+12)/25`，禁止中途除5。

有界调度合同为128条、每条67-bit的变长 record 队列。独立队列证明给出普通320+480及最短320+192调度的 record 峰值120，保留8条余量；无行间空闲时峰值触及128并在证明 cycle342 溢出。过载 TB 不硬套旧192像素 FIFO 的故障拍，只要求在有限时间明确 `o_frame_error` 且不得完整发布或无错丢像素。

异常 case 依次覆盖短行、321-beat 长行、重入 SOF、半帧复位；每段错误后清状态，最后完整重跑全255帧并逐像素核对，证明无旧输出泄漏。RTL 内两个 `PH1P_LOGIC_ERAM` 实例使用安路真实仿真模型编译和执行，不以行为假 RAM 代替。

## `road_capture_slots`

复位后两槽均 FREE。SOF 只能使用边沿前已 FREE 的槽；无 FREE 时整帧跳过，不允许同拍 release 旁路分配。CAPTURING、READY、READING、QUARANTINE 与 FREE 掩码必须互斥，捕获或读取槽不得被覆盖。

`i_capture_end` 只有在 byte count 精确为442,368且无帧错时进入 WAIT_VISIBLE；它本身不得使槽 READY。身份匹配的 `write_visible(slot,epoch,frame_id)` 才能发布 READY，同拍合法 capture_end+visible 允许直接发布。早、旧、重复 visible 必须报协议错且不污染新代。

claim 只在 READY 且 slot/epoch/frame_id 全匹配时 ready/接受。READING 只由身份匹配的 `last_read_consumed` 释放；它表示受控外部合同声称最后实际响应已消费且无在途/未来读取，不是 CNN done。非法 claim、旧/重复 release 不得改变状态。

重入 SOF 必须隔离正在 CAPTURING 的半帧并跳过新帧。专门覆盖同拍事件：slot1 正在 CAPTURING、slot0 正在 READING 时，新 SOF 隔离 slot1/跳帧，同时匹配末读释放 slot0。短帧、溢出、显式 frame error 进入 QUARANTINE；复位清除所有槽身份和状态，不得残留 READY/READING/输出脉冲。

## Case

| Runner case | 内容 |
|---:|---|
| 0 | 编号彩条完整帧逐像素。 |
| 1 | 固定 seed 随机完整帧逐像素。 |
| 2 | 全255完整帧逐像素。 |
| 3 | 短行、长行、重入SOF、半帧复位及完整全255恢复。 |
| 4 | 320拍行连续无空闲过载，必须显式报错且不发布。 |
| 10 | 双槽正常捕获、visible、claim、末读释放；含同拍结束+visible。 |
| 11 | 无空槽、捕获/读取保护、重入SOF和并发release。 |
| 12 | 早/旧/重复visible、非法claim、旧/重复release。 |
| 13 | 短帧、溢出、显式frame error、无空槽及复位清除。 |

## 通过定义

ModelSim SE-64 2020.4 必须重新编译两份冻结 RTL、对应 TB、`PH1P_PHY_GSR` 和 `PH1P_LOGIC_ERAM`。每个正式 case 在独立新目录保存命令、日志、源码/向量/厂商模型哈希和 `receipt.json`；失败目录不得覆盖。只有对应 `TB_PASS_AREA_RESIZE` 或 `TB_PASS_CAPTURE_SLOTS` marker 才算通过。
