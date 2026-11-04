# 小球旋转候选 bit 使用说明

状态：**2026-10-20 已完成本轮布局布线并生成候选 bit，待上板验证**。本说明对应独立 `ball_rotation` 工程，配置为 `C_FACE_GATE=0`、`C_ROTATION_ENABLE=1`，器件为安路 PH1P35MDG324、速度等级 3。

建议首次上板使用普通版：[ball_rotation.bit](ball_rotation.bit)，1,789,539 字节。压缩版：[ball_rotation_compress.bit](ball_rotation_compress.bit)，1,578,161 字节。两者来自同一最终数据库。

普通版 SHA256：`e0f41d741f2cb46f2893b62e2374da093f8265aabdde96aaa6d8f7e151ddc8bb`。

压缩版 SHA256：`d8a3cd1fc9268cfec0545331c5f6cea17883032139a7458b9a604ceb79e32a6c`。

完整文件清单、输入哈希和验证范围见 [manifest.json](manifest.json)；[SHA256SUMS.txt](SHA256SUMS.txt) 可用于文件核对。

本轮报告为实际布线后的 Slow/Fast 双角分析：建立裕量 **+0.103 ns**，保持裕量 **+0.020 ns**，STNS/HTNS 均为 0；STA覆盖率94.23%。Slice 18,521/21,216，ERAM 93/108，DSP 34/40（此前37/40）。[最终时序](route.timing)、[资源报告](route.area)、[bit生成日志](bitgen_console.log)。

bit生成前后207项工程输入哈希与route数据库哈希保持一致，生成步骤重新计算的时序/资源与最终route一致。route数据库 SHA256：`53e969f92e62593c2136975ff0368fa4f9b1658ddaf6eea7ec72a85b82406bbb`。

仍保留相机23.810 MHz输出时钟的混合负载本地布线告警（PHY-5079），以及非时钟负载/DDR PLL反馈时钟链告警（PHY-5088）；详见 [时钟分析](../reports/optimized_build/clock_detail_console.log)。相应内部时钟域已通过布线时序，不能因此称为零告警或量产放行。

## 上板与校准

1. 在安路 TD 中打开 [ball_rotation.al](../td_project/ball_rotation.al)。本轮交付以确认后的 bit 文件和 SHA256 为准。
2. 使用 JTAG 加载候选 bit 到 SRAM 做上板测试；本任务不自动操作板卡或写入 Flash。
3. 相机固定，先在追踪模式确认小球颜色和球框稳定，再测试旋转。首次发现目标后需要等待采集窗建立及后续帧，RPM还需要足够有效观测。
4. 曝光/增益仍可按键校准：D5 长按约1秒切换曝光，A9 长按约1秒切换增益。校准时停止运动，调整后清除应用历史。档位与按键细节见 [相机校准规范](../spec/user_source/hdl_source/uiisp_beta/ae_set_spec.md) 和 [按键说明](../spec/ball_key_control_spec.md)。

旋转条件沿用 [现有旋转场景说明](../python_sim/rotation_rtl_README.md#场景与无效条件)：单球、一个哑光偏心黑点、固定旋转轴大致朝向相机；建议球径80～192像素，黑点直径至少10～12像素，偏心约0.4～0.7倍球半径。球体须完整位于ROI和采集窗。该设计不保证任意倾斜轴或自由滚动的真实三维转速。默认120RPM是算法先验上界，不是已经实测的最高速度。标记不可见、多暗块、窗口丢失或长缺口会拒绝测量；PARTIAL表示只累计可观测部分，不补造缺失圈数。

## 本轮五处优化

- 旋转显示换算拆为绝对值冻结、26位缩位及BCD装载阶段，保留原数值公式、抢占/清零规则与像素延迟。
- DDR PLL修正参考频率标称并调整倍分频，在保持原输出频率的同时让VCO进入器件支持范围；模拟锁定仍待实板确认。
- 相机I²C的五个派生时钟过程改为主时钟加rise/fall使能；保持分频、采样与输出OFFSET，删除过期的生成时钟约束。
- HDMI帧同步进入DDR调试域前加两级同步，避免异步电平直接控制调试标志。
- 仅为已核实的两个FIFO跨域方向补四条数据路径延时预算，保留DDR IP灰码指针约束。

## 验证证据与范围

本轮物理实现、DRC、源码约束清单及最终日志见 [optimized_build](../reports/optimized_build/)。本说明与manifest记录本轮最终结果；此前失败的PLL标签实验和I²C保持时间实验已分别保存在诊断目录，不能用于本次交付。

- [显示换算与事务边界检查](../reports/optimized_build/format_summary.json)
- [I²C正常/复位等价核对](../reports/optimized_build/i2c_equivalence_summary.json)
- [PLL输出频率等价核对](../reports/optimized_build/pll_frequency_equivalence.json)
- [完整旋转RTL/Python核对日志](../reports/optimized_build/rotation_full_checks.log)
- [严格静态门禁状态](../reports/optimized_build/readable_status.json)
- [旋转显示流水契约与波形](../spec/rotation/ball_runtime_spec.md)

PLL模拟锁定、DDR初始化/读写和摄像头/HDMI连续工作仍需上板验证；现有输入输出的外部延时尚未完整建模。严格静态报告也未全部通过，不能将候选 bit 或已有仿真称为量产验收通过。
