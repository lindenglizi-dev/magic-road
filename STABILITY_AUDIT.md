# 道路视觉RTL稳定性审计

## 已修复问题

### 1. 背景RAM地址累计漂移

原实现使用 `stream_addr + 1` 访问背景图。如果输入坐标重复、跳变或丢失，后续像素可能整体错位，而EOF像素总数检查无法覆盖“重复一次又丢失一次”这种情况。

当前实现：

- 256×144正式配置直接使用 `{in_y, in_x}`，等价于 `y*256+x`；
- 每个有效像素检查实际坐标和期望坐标；
- 每行检查256个像素和行号；
- EOF检查144行和总像素数；
- 出现错误后，本帧后续禁止修改背景RAM；
- 下一帧干净SOF可恢复，不需要全局复位。

`tb_background_address_guard.v` 会交换两个像素坐标，同时保持像素总数不变，验证错误能够检测且错误位置之后的背景RAM不会被修改。

### 2. 错误CCL帧泄漏部分目标

原结构即使CCL后半帧溢出，前半帧暂存的目标仍可能提交给跟踪器，形成假轨迹。

当前 `object_frame_store` 增加 `discard_frame`：背景、CCL或分类链报错时，提交一个明确的空对象表，不提交部分结果；跟踪器仍会收到帧提交并正常增加miss计数，旧轨迹可以自然消失。

`tb_object_discard.v` 验证错误帧不会泄漏目标，下一干净帧仍可正常提交。

### 3. 单像素水平噪声消耗CCL资源

`run_detector` 默认要求水平run长度至少为2，宽度为1的孤立前景不再分配run和label。正常目标仍需满足面积和几何条件。

### 4. 离线回放节奏过快

真实5倍纵向采样在分析行之间有约1280个摄像头时钟的处理窗口。视频回放Testbench现在默认插入相同空闲窗口，避免制造板上不存在的 `raw_overrun`。

### 5. 二值前景只有一维去噪

当前在背景差分和RLE-CCL之间加入 `binary_cleanup_3x3`：

- 使用完整3×3邻域，默认要求中心为前景且邻域至少3点；
- 按中心像素坐标输出，CCL框不会整体偏移；
- 边界零填充，同时保持完整256×144输出；
- 可用 `CLEANUP_ENABLE` 旁路，用 `CLEANUP_MIN_NEIGHBORS` 调节强度；
- 清理级协议错误并入 `core_error`，错误帧不会提交部分目标。

正式AWB降采样流的行/帧空白大于模块所需的两拍行空白和约260拍帧空白。`tb_binary_cleanup_3x3.v` 验证孤立点被删除、致密3×3前景保持且坐标连续。

### 6. 算法读帧与摄像头写帧互相覆盖

新增 `gray_frame_pingpong`，用两组256×144×8位原生ERAM帧缓存隔离摄像头域与100 MHz算法域：

- 完整写帧后才通过toggle握手发布bank和frame ID；
- 算法域持有bank期间，摄像头域禁止覆盖该bank；冲突帧明确丢弃并产生 `wr_frame_drop`；
- 坐标、行尾、帧尾或像素计数异常时，错误帧不发布，下一干净帧自动恢复；
- 越界读、无所有权读取和重复释放均产生协议错误；
- 使用36个显式 `PH1P_LOGIC_ERAM`，避免双时钟大数组被综合成MSLICE。

`tb_gray_frame_pingpong.v` 已覆盖正常读回、错误帧丢弃、读者超期、受保护bank拒绝覆盖以及释放后的恢复。

### 7. 候选框和灰度帧跨域错配

新增 `roi_object_snapshot_cdc` 和 `roi_frame_reader`：

- CCL候选框先在摄像头域冻结，再通过toggle事件送入100 MHz域；
- 帧缓存和候选框都携带源帧编号，编号一致才启动ROI读取；
- 旧帧/新框不一致时丢弃较旧一方，绝不把错误框用于另一帧；
- 每个有效框用定点DDA归一化为32×32，运行时不使用除法器或乘法器；
- ROI完成后才释放帧缓存bank；越界框、异常响应和所有权错误都会进入诊断状态。

`tb_roi_object_snapshot_cdc.v` 验证跨域负载和错误帧空表；`tb_roi_frame_reader.v` 验证16×8框到32×32像素流的地址、数据、数量以及帧号错配处理。

### 8. ROI/HOG输入顺序失步

`hog_sobel_gradient` 不使用自由递增地址来猜测ROI位置，而是核对输入的 `roi_x/roi_y` 必须按32×32光栅顺序出现，同时检查一幅ROI内对象编号保持一致。异常会锁存 `protocol_error` 并进入顶层红色诊断状态。

`hog_cell_histogram` 在每个ROI最后一个梯度后顺序输出64项并清零。下一ROI的前两行不会产生3×3有效梯度，提供超过64周期的自然空档；如果上游违反这一节奏，在直方图忙时送入梯度，模块会显式报错而不是静默覆盖特征。

`tb_hog_frontend.v` 使用水平灰度斜坡验证900个Sobel输出的幅值、方向以及全部64个cell直方图值。

## 仍存在但已显式处理的边界

- 每行最多保存64个run；极端交错噪声可能触发 `run_overflow`。
- 每帧最多32个并行label；全画面亮度突变或严重噪声可能触发 `label_overflow`。
- 这些情况会置位 `core_error`、点亮红色诊断块，并丢弃该帧对象结果，不会再静默生成部分轨迹。
- 是否提高容量必须根据真实道路视频统计决定；直接扩大到128个label仍无法解决全画面场景突变，并会显著增加资源。

后续应使用真实道路视频统计前景比例、每行run峰值、label峰值，再决定阈值、去噪和容量。全局场景变化应采用重新学习或整帧抑制，而不是无限增加label RAM。

## 验证结果

Icarus RTL回归：

```text
PASS: lab1 AWB tap to adapter/background/CCL/track/event
PASS: 3x3 cleanup removes isolated noise and preserves dense foreground
PASS: tracker snapshot CDC and HDMI box overlay
PASS: coordinate address guard detects and contains bad frame
PASS: invalid CCL frame commits empty object table
PASS: ping-pong ownership, invalid-frame discard and conflict containment
PASS: candidate table snapshot CDC and discard handling
PASS: CCL box is normalized into a 32x32 ROI stream
PASS: Sobel gradient and 4x4x4 HOG cell histogram
```

Tang Dynasty最终布局布线：

- LUT6：15,693 / 21,216（73.97%）
- Slice：18,003 / 21,216（84.86%）
- Register：19,323 / 42,432（45.54%）
- ERAM20K：94 / 108（87.04%）
- DSP：9 / 40（22.50%）
- Setup：SWNS +0.110 ns，STNS 0
- Hold：HWNS +0.020 ns，HTNS 0

最终实现无setup/hold违例。

ERAM只剩14块，Slice使用率已到84.86%，setup裕量只有0.110 ns，均属于明确的后续约束：分类器必须采用小容量权重存储、流水或串行复用结构，不能再新增完整帧副本或宽并行乘加网络。
