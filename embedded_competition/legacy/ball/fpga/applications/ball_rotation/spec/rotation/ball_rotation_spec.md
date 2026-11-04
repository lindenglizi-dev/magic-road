# ball_rotation 模块规范

> RTL: `rtl/ball_rotation.v`

## 1. 模块目的

Frame-ordered dual-bank marker and rotation transaction controller

## 2. 参数

| 参数 | 默认值 | 说明 |
| --- | --- | --- |
| C_WIDTH | 1280 | 源图宽度 |
| C_HEIGHT | 720 | 源图高度 |
| C_X_MIN | 64 | ROI左界 |
| C_Y_MIN | 160 | ROI上界 |
| C_X_END | 1216 | ROI右开界 |
| C_Y_END | 640 | ROI下开界 |
| C_CLOCK_HZ | 103520000 | 实际源时钟标定 |
| C_MAX_RPM | 120 | 已知转速上界 |

## 3. 时钟与复位

- 时钟：`{"name": "i_clk", "edge": "posedge"}`
- 复位：`{"name": "i_rstn", "active": "low", "synchronous": false, "soft_clear": "i_clear"}`

## 4. 接口信号规范

| 信号 | 方向 | 位宽 | 时钟域 | 语义角色 | 描述 |
| --- | --- | --- | --- | --- | --- |
| `i_clk` | input | 1 | i_clk | clock | 像素组与统计共用时钟 |
| `i_rstn` | input | 1 | i_clk | reset | 异步低有效复位 |
| `i_clear` | input | 1 | i_clk | native | 清除旋转会话 |
| `i_fault` | input | 1 | i_clk | native | 颜色支路故障闭锁 |
| `i_enable` | input | 1 | i_clk | native | 追踪模式且门禁已解锁 |
| `i_rgb` | input | 96 | i_clk | native | 原始四像素RGB旁路 |
| `i_valid` | input | 1 | i_clk | native | 有效像素组 |
| `i_sof` | input | 1 | i_clk | native | 首个有效像素组 |
| `i_x` | input | 12 | i_clk | native | 当前横坐标 |
| `i_y` | input | 12 | i_clk | native | 当前纵坐标 |
| `i_frame` | input | 32 | i_clk | native | 源帧编号 |
| `i_tick` | input | 64 | i_clk | native | 该源帧采集时刻 |
| `i_epoch` | input | 16 | i_clk | native | 当前配置代次 |
| `i_observation_done` | input | 1 | i_clk | native | 当前组件帧已完成目标选择 |
| `i_observation_valid` | input | 1 | i_clk | native | 本帧有实测球而非漏检保留 |
| `i_observation_new` | input | 1 | i_clk | native | 新目标首帧 |
| `i_observation_frame` | input | 32 | i_clk | native | 实测球所属源帧 |
| `i_observation_tick` | input | 64 | i_clk | native | 实测源帧采集时间 |
| `i_observation_epoch` | input | 16 | i_clk | native | 实测帧配置代次 |
| `i_left` | input | 12 | i_clk | native | 实测左边界 |
| `i_right` | input | 12 | i_clk | native | 实测右边界 |
| `i_top` | input | 12 | i_clk | native | 实测上边界 |
| `i_bottom` | input | 12 | i_clk | native | 实测下边界 |
| `i_predict_valid` | input | 1 | i_clk | native | 预测框仍有效 |
| `i_predict_x` | input | 12 | i_clk | native | 用于未来采集窗的预测中心 |
| `i_predict_y` | input | 12 | i_clk | native | 用于未来采集窗的预测纵坐标 |
| `o_done` | output | 1 | i_clk | native | 带源帧号的结果完成脉冲 |
| `o_frame` | output | 32 | i_clk | native | 统计结果源帧号 |
| `o_epoch` | output | 16 | i_clk | native | 统计结果配置代次 |
| `o_angle_valid` | output | 1 | i_clk | native | 相位有效 |
| `o_phase` | output | 16 | i_clk | native | 65536一圈的冻结相位 |
| `o_rpm_valid` | output | 1 | i_clk | native | 转速窗口有效 |
| `o_rpm` | output | 24 | i_clk | native | 有符号零点一RPM |
| `o_status` | output | 3 | i_clk | native | 旋转统计状态 |
| `o_net` | output | 48 | i_clk | native | 有符号累计圈相位 |
| `o_cw` | output | 32 | i_clk | native | 顺转整圈累计 |
| `o_ccw` | output | 32 | i_clk | native | 逆转整圈累计 |
| `o_partial` | output | 1 | i_clk | native | 存在未能观测的时段 |
| `o_saturated` | output | 1 | i_clk | native | 整圈计数已饱和 |
| `o_reason` | output | 4 | i_clk | native | 本次测量拒绝原因 |
| `o_fault` | output | 1 | i_clk | native | 旋转支路失效闭锁 |
| `o_bank_busy` | output | 2 | i_clk | native | 缓存所有权诊断 |
| `o_median` | output | 8 | i_clk | native | 当前实测球内中位亮度 |
| `o_threshold` | output | 8 | i_clk | native | 当前黑点阈值 |

## 5. 周期行为与延迟

- Frame-ordered dual-bank marker and rotation transaction controller

## 6. WaveDrom 时序图

### 事务与有效标记

示意图中的长事务已压缩；实际周期数以状态机及仿真报告为准，像素支路保持原延迟。

![事务与有效标记](waveforms/ball_rotation_transaction.svg)

- WaveJSON：[ball_rotation_transaction.json5](waveforms/ball_rotation_transaction.json5)

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

- 规格模块：`ball_rotation`
- RTL 路径：`rtl/ball_rotation.v`
- 交付要求：本文档、WaveJSON 和 SVG 必须与同一版本规格一同发布。
