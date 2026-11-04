# 安路选题二：官方基线工程验证记录

验证日期：2026-09-07  
工作副本：`anlogic_topic2_work/baseline_lab1`  
原始工程：`安路/7_lab_ex_2026_nosoft/lab_hd_1_mipi_hdmi/lab_hd_1_mipi_hdmi`

## 1. 验证结论

官方 `lab_hd_1_mipi_hdmi` 工程已在本机使用与工程一致的 Tang Dynasty
`V6.2.168116` 完成全流程重建：综合、布局、布线、保持时间修复、最终静态时序分析和位流生成全部成功。

- 顶层：`design_top_wrapper`
- 器件：`PH1P35MDG324`，速度等级 `-3`
- 综合错误：0
- 最终建立时间：WNS `+0.629 ns`，TNS `0 ns`，违例端点 `0`
- 最终保持时间：WNS `+0.020 ns`，TNS `0 ns`，违例端点 `0`
- 报告中的关键时钟 Fmax：`121.080 MHz`
- 普通位流：`camera_to_dsi_display.bit`，1,789,539 字节
- 压缩位流：`camera_to_dsi_display_compress.bit`，1,312,497 字节

本次构建前后对原始工程与工作副本的 `user_source`、工程 `.al` 文件逐文件做了
SHA-256 对照，共比较 191 个文件，差异为 0。因此当前结果是未修改 RTL 的官方基线。

## 2. 最终资源占用

| 资源 | 使用量 | 总量 | 占用率 |
|---|---:|---:|---:|
| LUT6 | 9,830 | 21,216 | 46.33% |
| Slice | 12,187 | 21,216 | 57.44% |
| Slice Register | 13,318 | 42,432 | 31.39% |
| ERAM20K | 31 | 108 | 28.70% |
| DSP | 8 | 40 | 20.00% |
| MIPI RX | 1 | 2 | 50.00% |
| PLL | 3 | 6 | 50.00% |

这意味着后续增加算法时，最紧张的不是 DSP 或 ERAM，而是 Slice/LUT 和视频时钟域下的时序、布线压力。

## 3. 需要保留观察的告警

全流程没有 Error，但官方工程存在 3 条物理实现级 Critical Warning：

1. I2C 内部分频时钟 `scl_clk` 同时驱动时钟和数据/控制端。
2. 摄像头 24 MHz 时钟网 `O_cam_24m_syn_3` 同时驱动 102 个时钟端和 1 个数据/控制端。
3. 一条 24 MHz 摄像头时钟支路使用了局部布线资源。

这些告警在官方工程保持不变，且最终时序全部通过，暂不修改。后续若出现摄像头初始化不稳定、温度/电压变化下偶发问题，优先回查这三项。

综合阶段另有未使用 IP 端口、生成 IP 内未连接位、自动位宽截取等 Warning。它们不阻止基线构建，但在修改相邻模块时不可盲目忽略。

## 4. 位流哈希说明

新生成位流与资料包自带位流大小相同，但 SHA-256 不同。工程的 Bitgen 参数启用了
`time_info on`，位流包含构建时间信息，因此重新构建不要求二进制哈希完全一致；应以器件、资源、最终时序和上板功能为基准。

## 5. 下一步验证顺序

1. 连接开发板、JTAG、HDMI 显示器和 SC500CS 摄像头，先下载本次新生成位流。
2. 记录上电、DDR 校准、摄像头初始化、HDMI 锁定和画面稳定性。
3. 连续运行 10 分钟，检查黑屏、花屏、撕裂、颜色异常与帧停顿。
4. 基线通过后另建开发副本，先插入可旁路的 RGB 图像处理模块，再逐步实现比赛算法。
5. 每次修改都重复“仿真/小模块验证 → 综合 → 布局布线 → 时序 → 上板 A/B 对照”。

## 6. 关键生成物

- 工程入口：`baseline_lab1/td_project/camera_to_dsi_display.al`
- 最终时序：`baseline_lab1/td_project/camera_to_dsi_display_Runs/phy_1/final_timing.rpt`
- 资源报告：`baseline_lab1/td_project/camera_to_dsi_display_Runs/phy_1/camera_to_dsi_display_phy.area`
- 下载位流：`baseline_lab1/td_project/camera_to_dsi_display_Runs/phy_1/camera_to_dsi_display.bit`
- 压缩位流：`baseline_lab1/td_project/camera_to_dsi_display_Runs/phy_1/camera_to_dsi_display_compress.bit`
