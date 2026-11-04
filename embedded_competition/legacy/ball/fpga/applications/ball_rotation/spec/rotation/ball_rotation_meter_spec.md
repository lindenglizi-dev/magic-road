# ball_rotation_meter 模块规范

> RTL: `rtl/ball_rotation_meter.v`

## 1. 模块目的

Frame-timestamped integer least-squares RPM and directional turns

## 2. 参数

| 参数 | 默认值 | 说明 |
| --- | --- | --- |
| C_CLOCK_HZ | 103520000 | 源帧时间戳时钟，支持实际时钟标定 |
| C_MAX_RPM | 120 | 先验最大转速，防止跨帧角度混叠 |

## 3. 时钟与复位

- 时钟：`{"name": "i_clk", "edge": "posedge"}`
- 复位：`{"name": "i_rstn", "active": "low", "synchronous": false, "soft_clear": "i_clear"}`

## 4. 接口信号规范

| 信号 | 方向 | 位宽 | 时钟域 | 语义角色 | 描述 |
| --- | --- | --- | --- | --- | --- |
| `i_clk` | input | 1 | i_clk | clock | 串行统计时钟 |
| `i_rstn` | input | 1 | i_clk | reset | 异步低有效复位 |
| `i_clear` | input | 1 | i_clk | native | 清除旋转参考及圈数 |
| `i_fault` | input | 1 | i_clk | native | 失效闭锁并冻结已有圈数 |
| `i_start` | input | 1 | i_clk | native | 空闲时提交一帧观测 |
| `i_valid` | input | 1 | i_clk | native | 本帧相位有效 |
| `i_new_target` | input | 1 | i_clk | native | 该事务建立新的目标参考 |
| `i_phase` | input | 16 | i_clk | native | 图像内顺时针圈相位 |
| `i_tick` | input | 64 | i_clk | native | 源帧SOF时间戳 |
| `o_busy` | output | 1 | i_clk | native | 统计事务尚未完成 |
| `o_done` | output | 1 | i_clk | native | 整包统计结果完成 |
| `o_angle_valid` | output | 1 | i_clk | native | 本帧角度有效 |
| `o_phase` | output | 16 | i_clk | native | 本帧冻结相位 |
| `o_rpm_valid` | output | 1 | i_clk | native | 历史窗口足以测量转速 |
| `o_rpm` | output | 24 | i_clk | native | 有符号转速，单位零点一RPM |
| `o_status` | output | 3 | i_clk | native | 等待采集预热顺转逆转停止丢失故障 |
| `o_net` | output | 48 | i_clk | native | 有符号累计相位 |
| `o_cw` | output | 32 | i_clk | native | 连续顺转段完成整圈数 |
| `o_ccw` | output | 32 | i_clk | native | 连续逆转段完成整圈数 |
| `o_partial` | output | 1 | i_clk | native | 观测曾经不连续 |
| `o_saturated` | output | 1 | i_clk | native | 整圈计数达到上限 |
| `o_fault` | output | 1 | i_clk | native | 时间或数值合同失效 |

## 5. 周期行为与延迟

- Frame-timestamped integer least-squares RPM and directional turns

## 6. WaveDrom 时序图

### 事务与有效标记

示意图中的长事务已压缩；实际周期数以状态机及仿真报告为准，像素支路保持原延迟。

![事务与有效标记](waveforms/ball_rotation_meter_transaction.svg)

- WaveJSON：[ball_rotation_meter_transaction.json5](waveforms/ball_rotation_meter_transaction.json5)

## 7. 边界、反压与错误

- clear aborts work
- missing sample invalidates RPM
- overflow fails closed

## 8. CDC 与综合约束

- Verilog-2001
- single pixel-group clock domain
- no array reset

## 9. 验证与验收

- Python integer vectors
- source-frame matching
- reset and invalid input

## 10. 可追溯性

- 规格模块：`ball_rotation_meter`
- RTL 路径：`rtl/ball_rotation_meter.v`
- 交付要求：本文档、WaveJSON 和 SVG 必须与同一版本规格一同发布。
