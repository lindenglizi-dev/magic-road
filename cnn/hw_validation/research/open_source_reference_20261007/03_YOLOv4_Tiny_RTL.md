# YOLOv4-Tiny 手写 RTL：可借鉴点与证据边界

核查日期：2026-10-07。对象为 `gauravanand10/YOLOV4-TINY-FPGA-ACCELERATOR`，固定到提交 [`6978bc64811ba530b7f2372a6e05d1852aeb9cab`](https://github.com/gauravanand10/YOLOV4-TINY-FPGA-ACCELERATOR/tree/6978bc64811ba530b7f2372a6e05d1852aeb9cab)。本轮只读网页与原始文件，**未下载、未运行仿真/综合、未上板**。根目录未见 `LICENSE`，GitHub 也未识别许可证；公开可读不等于可直接复制，复用代码前必须先取得授权或确认许可证。

## 我能核实什么

作者 README 声称 416×416、21 个卷积描述符、3.40 GMAC，xsim 全网 7,481,892 拍，187.5 MHz 换算约 25.1 FPS；[原始日志](https://github.com/gauravanand10/YOLOV4-TINY-FPGA-ACCELERATOR/blob/6978bc64811ba530b7f2372a6e05d1852aeb9cab/logs/xsim_yolo.log)确有 `layers=21`、948,224 个 128-bit 字逐字相等、AXI protocol error=0、`stall_rows=136188`、`stall_out=0`、`wload=376860`。周期起点是加速器 `start`，终点是 21 层和写响应完成；不含 PS 端 RGB 预处理、head 解码、NMS、TCP、摄像与画框。3.40G/512≈6.64M 拍，与作者“理想 6.97M、实测 7.48M”量级一致，差额可由通道分组、装载和填充解释；这是内部一致性检查，不是本地复现。

[实现报告](https://github.com/gauravanand10/YOLOV4-TINY-FPGA-ACCELERATOR/blob/6978bc64811ba530b7f2372a6e05d1852aeb9cab/06_vivado/reports/utilization_impl.rpt)为 96.5 BRAM、37 DSP，[时序报告](https://github.com/gauravanand10/YOLOV4-TINY-FPGA-ACCELERATOR/blob/6978bc64811ba530b7f2372a6e05d1852aeb9cab/06_vivado/reports/timing_impl.rpt)为 WNS +0.099 ns/WHS +0.010 ns。关键纠错：37 DSP 不是 37 个卷积 MAC；[RTL 说明](https://github.com/gauravanand10/YOLOV4-TINY-FPGA-ACCELERATOR/blob/6978bc64811ba530b7f2372a6e05d1852aeb9cab/04_rtl/README.md)显示 32×16=512 个 INT8 乘法映射 LUT，`pe_array` 单独占 26,176 LUT/11,136 FF/0 DSP，32 路 requant epilogue 占 32 DSP，整核为 54,653 LUT/21,279 FF/96 RAMB36+1 RAMB18/37 DSP。ZCU104 的这组资源和频率不能外推到仅 40 DSP/108 ERAM/21,216 Slice 的 PH1P35；当前 8 输入×3 输出=24 MAC 小块也不是它的缩小同构体。

## 真实文件与职责

| 文件/目录 | 源码可核实职责 |
|---|---|
| [`04_rtl/`](https://github.com/gauravanand10/YOLOV4-TINY-FPGA-ACCELERATOR/tree/6978bc64811ba530b7f2372a6e05d1852aeb9cab/04_rtl) | 13 个可综合文件：`yolo_pkg`/`yolo_accel(_wrap)`/`axil_regs`/`burst_gen`、权重和行装载器、`conv_engine`/`pe_array`/`epilogue`/`writer`、RAM/FIFO。每 32 输出通道组先装参数和权重，再让行装载、MAC、16 像素 credit FIFO、DDR writer 并行；层末等待全部 B response。 |
| [`02_golden_model/`](https://github.com/gauravanand10/YOLOV4-TINY-FPGA-ACCELERATOR/tree/6978bc64811ba530b7f2372a6e05d1852aeb9cab/02_golden_model) | Darknet 解析、浮点/INT8/DDR 描述符模拟、cycle model、decode/NMS；route/concat/group split 用地址偏移，maxpool 在 loader，upsample/双目的写在 writer。 |
| [`03_quant_export/`](https://github.com/gauravanand10/YOLOV4-TINY-FPGA-ACCELERATOR/blob/6978bc64811ba530b7f2372a6e05d1852aeb9cab/03_quant_export/README.md) | 导出 21×64 B descriptor、5.96 MB 权重、测试 DDR 镜像；参数 beat 是 `bias int32/Mpos/Mneg/sh`。 |
| [`07_sw/`](https://github.com/gauravanand10/YOLOV4-TINY-FPGA-ACCELERATOR/tree/6978bc64811ba530b7f2372a6e05d1852aeb9cab/07_sw) | ARM/Linux 负责装载、启动、双 input slot、解码和 NMS；作者明确尚未完成板上 selftest，因此不是已证明的整机检测系统。 |

数值契约与 RoadYOLO 不同：该工程是 `pixel>>1`，INT8×INT8→INT32，`acc+bias` 先饱和 27 位，再选 Leaky-ReLU 的 `Mpos/Mneg`，加 `2^(sh-1)` 后算术右移并夹紧 INT8；当前工程输入先做 `pixel−128`，权重与层间激活 zero-point 为 0，并使用 INT32 边界检查、RNE、SiLU-1024 LUT。不能直接搬 `epilogue` 或其导出二进制。

## 对当前工程的分级结论

- **直接复用：无。** 许可证、器件、总线与数值契约均不闭合。
- **需移植：** 只移植“descriptor 字段与导出器同源生成、权重/偏置/requant 打包后立即生成 DDR 级黄金镜像”的方法；字段改成现有 DW/PW、SiLU、RNE、PAXI 和双 DDR slot，不另造通用编译器。
- **理念复用：** 保留“行已就绪 + 输出 reservation 才发射”的固定流水思想；当前 stream 已有 2-group 结果队列、`flag_result_reserved` 与 `wire_capacity_used<=2`，先核查既有 reservation 是否真实覆盖所有背压路径，不原抄外部 16 像素 FIFO。写层结束仍须以真实 PAXI 写完成可见性为门槛。8 行缓冲和固定 4 拍覆盖期也只能参考，必须按 PH1P ERAM/PAXI 实测延迟重算。
- **不适合替代：** 其 416×416 anchor-based YOLOv4、PS NMS 与 512-LUT-MAC 大核不能替代 512×288 anchor-free、24 MAC、纯 FPGA 后处理的 RoadYOLO。

优先提案：先对现有 9×9 halo→DW s2→PW 小块做 reservation 记账审计，分出真正的 row wait、result-capacity wait 与写完成 wait；只有预算证明队列深度是瓶颈，才调整深度。跨任务连续发射或改变 II 会扩大控制语义，需另行批准，本文不实施。最小验证是同一冻结向量下：(1) 保持 5,433 拍基线并解释可减少项；(2) 每次覆盖前最后 RAM read 已完成；(3) PAXI 随机背压下逐元素相等且无队列溢出；(4) 再跑 PH1P35 100 MHz 实现。当前含壳候选 8,733 Slice/26 DSP/1 ERAM，仍有 5 个新 setup 失败、最差 −0.943 ns；未闭合前不把 63,662,586 条件预算改写成整网 FPS。

## 简短总结

最值钱的是 credit 驱动的连续流水、描述符与黄金 DDR 镜像同源；最危险的是把“37 DSP、25 FPS、全网在 PL”误读为本板纯 FPGA 已可用方案。
