# ball_target_tracker 模块规范

> RTL: `rtl/ball_target_tracker.v`

## 1. 模块目的

保留预测输出；新增当前选中实测框及其完成、有效、新目标脉冲。漏检保留不产生实测角度。

## 2. 参数

| 参数 | 默认值 | 说明 |
| --- | --- | --- |
| C_MAX_MOVE | 64 | 原有目标关联距离 |
| C_X_MIN | 0 | ROI左界 |
| C_Y_MIN | 0 | ROI上界 |
| C_X_END | 4096 | ROI右开界 |
| C_Y_END | 4096 | ROI下开界 |

## 3. 时钟与复位

- 时钟：`{"name": "i_clk", "edge": "posedge"}`
- 复位：`{"name": "i_rstn", "active": "low", "synchronous": false}`

## 4. 接口信号规范

| 信号 | 方向 | 位宽 | 时钟域 | 语义角色 | 描述 |
| --- | --- | --- | --- | --- | --- |
| `i_clk` | input | 1 | i_clk | clock | i_clk |
| `i_rstn` | input | 1 | i_clk | reset | i_rstn |
| `i_clear` | input | 1 | i_clk | signal | i_clear |
| `i_frame_start` | input | 1 | i_clk | signal | i_frame_start |
| `i_candidate_valid` | input | 1 | i_clk | status | i_candidate_valid |
| `i_color` | input | 2 | i_clk | signal | i_color |
| `i_area` | input | 20 | i_clk | signal | i_area |
| `i_x_min` | input | 12 | i_clk | signal | i_x_min |
| `i_x_max` | input | 12 | i_clk | signal | i_x_max |
| `i_y_min` | input | 12 | i_clk | signal | i_y_min |
| `i_y_max` | input | 12 | i_clk | signal | i_y_max |
| `i_frame_done` | input | 1 | i_clk | status | i_frame_done |
| `i_overflow` | input | 1 | i_clk | signal | i_overflow |
| `o_valid` | output | 1 | i_clk | status | o_valid |
| `o_status` | output | 2 | i_clk | status | o_status |
| `o_color` | output | 2 | i_clk | signal | o_color |
| `o_x_min` | output | 12 | i_clk | signal | o_x_min |
| `o_x_max` | output | 12 | i_clk | signal | o_x_max |
| `o_y_min` | output | 12 | i_clk | signal | o_y_min |
| `o_y_max` | output | 12 | i_clk | signal | o_y_max |
| `o_center_x` | output | 12 | i_clk | signal | o_center_x |
| `o_center_y` | output | 12 | i_clk | signal | o_center_y |
| `o_observation_done` | output | 1 | i_clk | native | o_observation_done |
| `o_observed_valid` | output | 1 | i_clk | native | o_observed_valid |
| `o_observed_new` | output | 1 | i_clk | native | o_observed_new |
| `o_observed_left` | output | 12 | i_clk | native | o_observed_left |
| `o_observed_right` | output | 12 | i_clk | native | o_observed_right |
| `o_observed_top` | output | 12 | i_clk | native | o_observed_top |
| `o_observed_bottom` | output | 12 | i_clk | native | o_observed_bottom |

## 5. 周期行为与延迟

- 保留预测输出；新增当前选中实测框及其完成、有效、新目标脉冲。漏检保留不产生实测角度。

## 6. WaveDrom 时序图

### 事务与有效标记

示意图中的长事务已压缩；实际周期数以状态机及仿真报告为准，像素支路保持原延迟。

![事务与有效标记](waveforms/ball_target_tracker_transaction.svg)

- WaveJSON：[ball_target_tracker_transaction.json5](waveforms/ball_target_tracker_transaction.json5)

## 7. 边界、反压与错误

- 清零撤销旧代次
- 漏检不使用预测框计算角度
- 错误时冻结累计圈数

## 8. CDC 与综合约束

- 保持原有像素延迟和视频端口
- C_ROTATION_ENABLE参数控制旋转综合
- RAM不做逐单元复位

## 9. 验证与验收

- RGB整链路与Python对比
- 原计数、会话清零及代次回归

## 10. 可追溯性

- 规格模块：`ball_target_tracker`
- RTL 路径：`rtl/ball_target_tracker.v`
- 交付要求：本文档、WaveJSON 和 SVG 必须与同一版本规格一同发布。
