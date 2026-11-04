# ball_components 模块规范

> RTL: `rtl/ball_components.v`

## 1. 模块目的

为颜色组件扫描冻结源帧号与SOF时间；不改变颜色连通区域计算。

## 2. 参数

| 参数 | 默认值 | 说明 |
| --- | --- | --- |
| C_WIDTH | 1280 | 保持原有尺寸或筛选参数 |
| C_HEIGHT | 720 | 保持原有尺寸或筛选参数 |
| C_X_MIN | 64 | 保持原有尺寸或筛选参数 |
| C_Y_MIN | 160 | 保持原有尺寸或筛选参数 |
| C_X_END | 1216 | 保持原有尺寸或筛选参数 |
| C_Y_END | 640 | 保持原有尺寸或筛选参数 |
| C_GATE_MIN | 544 | 保持原有尺寸或筛选参数 |
| C_GATE_END | 736 | 保持原有尺寸或筛选参数 |
| C_MIN_AREA | 128 | 保持原有尺寸或筛选参数 |
| C_MIN_SIZE | 12 | 保持原有尺寸或筛选参数 |
| C_MAX_SIZE | 384 | 保持原有尺寸或筛选参数 |
| C_MAX_CANDIDATES | 8 | 保持原有尺寸或筛选参数 |
| C_QUEUE_BITS | 12 | 保持原有尺寸或筛选参数 |

## 3. 时钟与复位

- 时钟：`{"name": "i_clk", "edge": "posedge"}`
- 复位：`{"name": "i_rstn", "active": "low", "synchronous": false}`

## 4. 接口信号规范

| 信号 | 方向 | 位宽 | 时钟域 | 语义角色 | 描述 |
| --- | --- | --- | --- | --- | --- |
| `i_clk` | input | 1 | i_clk | clock | i_clk |
| `i_rstn` | input | 1 | i_clk | reset | i_rstn |
| `i_session_clear` | input | 1 | i_clk | signal | i_session_clear |
| `i_valid` | input | 1 | i_clk | status | i_valid |
| `i_sof` | input | 1 | i_clk | signal | i_sof |
| `i_eof` | input | 1 | i_clk | signal | i_eof |
| `i_x` | input | 12 | i_clk | signal | i_x |
| `i_y` | input | 12 | i_clk | signal | i_y |
| `i_labels` | input | 8 | i_clk | signal | i_labels |
| `i_gate_hits` | input | 3 | i_clk | signal | i_gate_hits |
| `i_epoch` | input | 16 | i_clk | signal | i_epoch |
| `o_frame_start` | output | 1 | i_clk | signal | o_frame_start |
| `o_candidate_valid` | output | 1 | i_clk | status | o_candidate_valid |
| `o_color` | output | 2 | i_clk | signal | o_color |
| `o_area` | output | 20 | i_clk | signal | o_area |
| `o_x_min` | output | 12 | i_clk | signal | o_x_min |
| `o_x_max` | output | 12 | i_clk | signal | o_x_max |
| `o_y_min` | output | 12 | i_clk | signal | o_y_min |
| `o_y_max` | output | 12 | i_clk | signal | o_y_max |
| `o_frame_done` | output | 1 | i_clk | status | o_frame_done |
| `o_gate_pixels` | output | 20 | i_clk | signal | o_gate_pixels |
| `o_gate_occupied` | output | 1 | i_clk | signal | o_gate_occupied |
| `o_epoch` | output | 16 | i_clk | signal | o_epoch |
| `o_overflow` | output | 1 | i_clk | signal | o_overflow |
| `o_fault` | output | 1 | i_clk | signal | o_fault |
| `o_error` | output | 1 | i_clk | signal | o_error |
| `o_diag_count` | output | 4 | i_clk | signal | o_diag_count |
| `o_diag_width` | output | 12 | i_clk | signal | o_diag_width |
| `o_diag_height` | output | 12 | i_clk | signal | o_diag_height |
| `o_diag_area` | output | 20 | i_clk | signal | o_diag_area |
| `o_diag_fill` | output | 7 | i_clk | signal | o_diag_fill |
| `o_diag_reject` | output | 4 | i_clk | signal | o_diag_reject |
| `i_frame_id` | input | 32 | i_clk | native | i_frame_id |
| `i_stamp` | input | 64 | i_clk | native | i_stamp |
| `o_frame_id` | output | 32 | i_clk | native | o_frame_id |
| `o_stamp` | output | 64 | i_clk | native | o_stamp |

## 5. 周期行为与延迟

- 为颜色组件扫描冻结源帧号与SOF时间；不改变颜色连通区域计算。

## 6. WaveDrom 时序图

### 事务与有效标记

示意图中的长事务已压缩；实际周期数以状态机及仿真报告为准，像素支路保持原延迟。

![事务与有效标记](waveforms/ball_components_transaction.svg)

- WaveJSON：[ball_components_transaction.json5](waveforms/ball_components_transaction.json5)

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

- 规格模块：`ball_components`
- RTL 路径：`rtl/ball_components.v`
- 交付要求：本文档、WaveJSON 和 SVG 必须与同一版本规格一同发布。
