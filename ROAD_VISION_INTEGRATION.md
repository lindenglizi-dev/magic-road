# Lab1 道路视觉接入状态

本目录是新版官方 `lab_ex1_mipi_hdmi_SC500_720P` 的工作副本；官方模板未修改。
打开 `td_project/camera_to_dsi_display.al`，综合顶层仍为 `design_top_wrapper`。
本工作副本已经完成端到端 RTL 仿真，以及修改后设计的完整综合、布局布线。

## 数据链

- 官方链：SC500 → ISP → 128 位打包 → DDR → HDMI mixer → 状态叠加 → HDMI。
- 分析链：ISP 内 AWB 96 位 RGB888 旁路 → `awb96_analysis_adapter` → 256×144 灰度 → `foreground_ccl_top` → 四目标跟踪、事件。
- ROI/HOG支链：同一份256×144灰度流 → `gray_frame_pingpong` 双ERAM帧缓存；CCL候选框经 `roi_object_snapshot_cdc` 跨域后，与源帧编号配对，再由 `roi_frame_reader` 归一化输出32×32 ROI像素流，随后生成Sobel梯度和64维HOG cell特征。
- 分析核心运行于 `S_csi_rx_clk`，与 AWB 同域；每帧由 `track_snapshot_cdc` 读取四项跟踪表并冻结，再以翻转握手送到 HDMI 像素域。
- `road_box_overlay` 将 256×144 目标框坐标放大 5 倍叠加到 1280×720 画面：行人绿色、车辆青色、未知类别洋红色。
- HDMI 左上角保留四块16×16诊断状态：绿=曾检出目标，黄=曾发生事件，红=曾发生分析/ROI/HOG错误，蓝色变化块=HOG已经输出目标特征且校验值在变化。

## 功能测试

`tests/tb_lab1_road_chain.v` 用合成的四像素 RGB 数据测试 40×20 → 8×4 的同构缩放，并串联背景、CCL、分类、跟踪、警戒区事件；应检查像素数、坐标、行帧标志、对象与事件 ID。

实测结果：Icarus Verilog 编译成功，仿真输出：

```text
PASS: lab1 AWB tap to adapter/background/CCL/track/event
PASS: 3x3 cleanup removes isolated noise and preserves dense foreground
PASS: tracker snapshot CDC and HDMI box overlay
PASS: ping-pong ownership, invalid-frame discard and conflict containment
PASS: candidate table snapshot CDC and discard handling
PASS: CCL box is normalized into a 32x32 ROI stream
PASS: Sobel gradient and 4x4x4 HOG cell histogram
PASS: serial HOG linear SVM MAC and protocol guard
PASS: coordinate address guard detects and contains bad frame
PASS: invalid CCL frame commits empty object table
```

可在 PowerShell 中执行：

```powershell
.\tests\run_iverilog.ps1
```

## 综合与布局布线结果

`td_project/road_elaborate.tcl` 已对修改后的总顶层完成 optimize、legalize、place、route。最终报告为 `road_route.area` 和 `road_route.timing`：

- LUT6：15,693 / 21,216（73.97%）
- Slice：18,003 / 21,216（84.86%）
- Slice Register：19,323 / 42,432（45.54%）
- ERAM20K：94 / 108（87.04%）
- DSP：9 / 40（22.50%）
- Setup：SWNS +0.110 ns，STNS 0
- Hold：HWNS +0.020 ns，HTNS 0
- 结论：当前版本资源可容纳，布局布线后无 setup/hold 违例。

画框坐标缩放已明确写成移位加法 `x + (x << 2)`；若直接写四组乘 5，Tang 会额外推断 16 个 DSP。

这些结果只证明 RTL 链路、资源和静态时序成立；摄像头输入相位、真实画面阈值与 HDMI 显示仍需上板验收。

## 后续验收顺序

1. 上板核对真实 AWB 的 `tuser/tlast` 相位，确认红色错误块不亮。
2. 确认原 HDMI 画面不受影响，动态框及绿/黄状态块能随目标和事件变化。
3. 用真实道路视频调背景阈值、最小面积、分类阈值和警戒区坐标。
4. 使用已通过逐项对照的PC参考模型提取训练集特征并训练线性SVM。
5. 量化并生成权重ROM，将已有串行MAC接入总顶层，再回写最终类别。

当前仅剩14块ERAM20K，Slice使用率已到84.86%，100 MHz域setup裕量仅0.110 ns。后续分类器必须优先采用流式计算、串行MAC、复用现有帧缓存和小型权重ROM，不能再规划一组完整灰度帧缓存或大规模并行乘加阵列。
