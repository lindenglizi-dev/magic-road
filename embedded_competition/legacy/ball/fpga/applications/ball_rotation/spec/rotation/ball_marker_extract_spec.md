# ball_marker_extract 模块规范

> RTL: `rtl/ball_marker_extract.v`

## 1. 模块目的

Same-frame median threshold and bounded four-connected dark marker extraction

## 2. 参数

| 参数 | 默认值 | 说明 |
| --- | --- | --- |
| C_X_MIN | 64 | 原图ROI左界 |
| C_Y_MIN | 160 | 原图ROI上界 |
| C_X_END | 1216 | 原图ROI右开区间 |
| C_Y_END | 640 | 原图ROI下开区间 |
| C_QUEUE_BITS | 9 | 默认512个待访问结点 |

## 3. 时钟与复位

- 时钟：`{"name": "i_clk", "edge": "posedge"}`
- 复位：`{"name": "i_rstn", "active": "low", "synchronous": false, "soft_clear": "i_clear"}`

## 4. 接口信号规范

| 信号 | 方向 | 位宽 | 时钟域 | 语义角色 | 描述 |
| --- | --- | --- | --- | --- | --- |
| `i_clk` | input | 1 | i_clk | clock | 灰度统计时钟 |
| `i_rstn` | input | 1 | i_clk | reset | 异步低有效复位 |
| `i_clear` | input | 1 | i_clk | native | 撤销当前黑点提取 |
| `i_start` | input | 1 | i_clk | native | 空闲时提交已冻结bank |
| `i_origin_x` | input | 12 | i_clk | native | 采集窗左边界 |
| `i_origin_y` | input | 12 | i_clk | native | 采集窗上边界 |
| `i_left` | input | 12 | i_clk | native | 同帧实测球框左边界 |
| `i_right` | input | 12 | i_clk | native | 同帧实测球框右边界 |
| `i_top` | input | 12 | i_clk | native | 同帧实测球框上边界 |
| `i_bottom` | input | 12 | i_clk | native | 同帧实测球框下边界 |
| `i_read_data` | input | 16 | i_clk | native | 同步灰度读返回值 |
| `o_read` | output | 1 | i_clk | native | 同步灰度读请求 |
| `o_read_address` | output | 13 | i_clk | native | 灰度双单元字地址 |
| `o_busy` | output | 1 | i_clk | native | 正在处理冻结bank |
| `o_done` | output | 1 | i_clk | native | 黑点提取结束 |
| `o_valid` | output | 1 | i_clk | native | 恰好识别出一个合格黑点 |
| `o_reason` | output | 4 | i_clk | native | 裁切几何窗口队列或标记错误 |
| `o_center_x` | output | 16 | i_clk | native | Q4实测球心横坐标 |
| `o_center_y` | output | 16 | i_clk | native | Q4实测球心纵坐标 |
| `o_marker_x` | output | 16 | i_clk | native | Q4黑点横坐标 |
| `o_marker_y` | output | 16 | i_clk | native | Q4黑点纵坐标 |
| `o_median` | output | 8 | i_clk | native | 本帧内圆低中位灰度 |
| `o_threshold` | output | 8 | i_clk | native | 本帧黑点阈值 |

## 5. 周期行为与延迟

- Same-frame median threshold and bounded four-connected dark marker extraction

## 6. WaveDrom 时序图

### 事务与有效标记

示意图中的长事务已压缩；实际周期数以状态机及仿真报告为准，像素支路保持原延迟。

![事务与有效标记](waveforms/ball_marker_extract_transaction.svg)

- WaveJSON：[ball_marker_extract_transaction.json5](waveforms/ball_marker_extract_transaction.json5)

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

- 规格模块：`ball_marker_extract`
- RTL 路径：`rtl/ball_marker_extract.v`
- 交付要求：本文档、WaveJSON 和 SVG 必须与同一版本规格一同发布。
