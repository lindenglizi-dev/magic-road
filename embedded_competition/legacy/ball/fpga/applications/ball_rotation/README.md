# 小球旋转独立工程

安路 TD 打开 `E:/project/ball/fpga/applications/ball_rotation/td_project/ball_rotation.al`；顶层为 `design_top_wrapper`。
默认配置：C_FACE_GATE=0，旋转=开启。
本目录包含独立 RTL、user_source/IP、SDC、ROM、sim、spec 与 Python 模型；不依赖另一功能工程的源码。
在本目录运行 `python sim/run_rotation_checks.py`；Icarus 需位于 PATH（旋转脚本也支持已有工具路径）。
Python 模型位于本目录 python_sim；人脸模型如适用位于 python_face、python_face_fixed。

来源：旋转集成后的当前源码，门禁关闭、旋转开启。
隔离仅修改工程路径、功能默认值和仿真导入路径；算法、引脚、时钟约束保持原来源版本。
TD 综合使用新目录的默认脚本，未携带旧运行缓存、bit 或历史时序报告。
当前没有此独立工程的新 bit。现有约束下已完成布局布线，仍需核查约束覆盖和时序余量，尚未上板放行。
隔离证据见 reports/isolation，独立工程时序复测见 reports/timing_baseline；原 ball_detection 保留回退，后续不在那里继续写功能。

已知旧测试：tb_ball_core 使用 ball_projection，在 exact pixel area 断言失败；原共享源码也复现同一失败，非此次隔离新增。现用 ball_components_limits 及追踪检查通过，详见 reports/isolation/verification.json。

## 独立旋转工程时序复测（2026-10-20）

在 RTL、IP、引脚和时钟约束均未修改的情况下，安路完整综合、布局布线已完成。
综合 SWNS=-0.733 ns；布线后 SWNS=+0.005 ns、HWNS=+0.020 ns，STNS/HTNS=0。
物理资源：Slice 18670/21216，ERAM 93/108，DSP 37/40；STA coverage 94.11%。
现有完整旋转检查（包括 8 帧 RGB 到转速、7 次有序测量）及 Python 定点逐项核对通过。
实际最差路径为旋转累计相位到 OSD 数值换算，后续余量优化应以布线报告为依据。

这些结果仅证明现有约束下本次物理实现没有负裕量，不是上板放行：余量只有 5 ps；
I2C 分频时钟缺约束、DDR PLL 标称频率不一致、I/O 延迟及 FIFO 例外覆盖仍需核查。
既有严格 RTL 风格门禁也未通过。本轮没有生成 bit、没有操作板卡。
证据：reports/timing_baseline/summary.json、route.timing、route_constraint_check.txt、routed_audit_console.log。
