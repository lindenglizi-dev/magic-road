# ball_rotation_capture 模块规范

> RTL: `rtl/ball_rotation_capture.v`

## 1. 模块目的

Four-pixel grayscale capture with frame-tagged dual banks

## 2. 参数

| 参数 | 默认值 | 说明 |
| --- | --- | --- |
| — | — | 本模块没有可配置参数。 |

## 3. 时钟与复位

- 时钟：`{"name": "i_clk", "edge": "posedge"}`
- 复位：`{"name": "i_rstn", "active": "low", "synchronous": false, "soft_clear": "i_clear"}`

## 4. 接口信号规范

| 信号 | 方向 | 位宽 | 时钟域 | 语义角色 | 描述 |
| --- | --- | --- | --- | --- | --- |
| `i_clk` | input | 1 | i_clk | clock | 像素组时钟 |
| `i_rstn` | input | 1 | i_clk | reset | 异步低有效复位 |
| `i_clear` | input | 1 | i_clk | native | 撤销采集并释放bank |
| `i_enable` | input | 1 | i_clk | native | 允许本次采集 |
| `i_rgb` | input | 96 | i_clk | native | 四个连续RGB像素 |
| `i_valid` | input | 1 | i_clk | native | 当前像素组有效 |
| `i_sof` | input | 1 | i_clk | native | 源帧首个有效像素组 |
| `i_x` | input | 12 | i_clk | native | 左侧像素横坐标 |
| `i_y` | input | 12 | i_clk | native | 当前行号 |
| `i_frame` | input | 32 | i_clk | native | 采集源帧编号 |
| `i_tick` | input | 64 | i_clk | native | 该源帧SOF时间 |
| `i_epoch` | input | 16 | i_clk | native | 该源帧配置代次 |
| `i_window_valid` | input | 1 | i_clk | native | 窗口来自已完成追踪结果 |
| `i_window_x` | input | 12 | i_clk | native | 四像素对齐的采集左边界 |
| `i_window_y` | input | 12 | i_clk | native | 两行对齐的采集上边界 |
| `i_release` | input | 2 | i_clk | native | 每一位释放对应bank |
| `i_read` | input | 1 | i_clk | native | 处理支路请求同步读 |
| `i_read_bank` | input | 1 | i_clk | native | 处理bank选择 |
| `i_read_address` | input | 13 | i_clk | native | 两个灰度单元组成一字的地址 |
| `o_read_data` | output | 16 | i_clk | native | 请求后一个时钟返回两个灰度 |
| `o_busy` | output | 2 | i_clk | native | bank从采集到释放一直占用 |
| `o_ready` | output | 2 | i_clk | native | 完整采集的bank |
| `o_frames` | output | 64 | i_clk | native | 两个bank的源帧编号 |
| `o_ticks` | output | 128 | i_clk | native | 两个bank的采集时刻 |
| `o_epochs` | output | 32 | i_clk | native | 两个bank的代次 |
| `o_origins_x` | output | 24 | i_clk | native | 两个bank的窗口左边界 |
| `o_origins_y` | output | 24 | i_clk | native | 两个bank的窗口上边界 |
| `o_overrun` | output | 1 | i_clk | native | SOF请求的bank仍被占用 |

## 5. 周期行为与延迟

- Four-pixel grayscale capture with frame-tagged dual banks

## 6. WaveDrom 时序图

### 事务与有效标记

示意图中的长事务已压缩；实际周期数以状态机及仿真报告为准，像素支路保持原延迟。

![事务与有效标记](waveforms/ball_rotation_capture_transaction.svg)

- WaveJSON：[ball_rotation_capture_transaction.json5](waveforms/ball_rotation_capture_transaction.json5)

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

- 规格模块：`ball_rotation_capture`
- RTL 路径：`rtl/ball_rotation_capture.v`
- 交付要求：本文档、WaveJSON 和 SVG 必须与同一版本规格一同发布。
