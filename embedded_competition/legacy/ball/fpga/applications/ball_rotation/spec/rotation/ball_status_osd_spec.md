# ball_status_osd 模块规范

> RTL: `rtl/ball_status_osd.v`

## 1. 模块目的

保留两拍像素合成；旋转开启时在144至157行显示角度、转速、圈数及诊断。

## 2. 参数

| 参数 | 默认值 | 说明 |
| --- | --- | --- |
| C_ROTATION | 0 | 是否合成旋转状态行，生产runtime传入有效开关 |

## 3. 时钟与复位

- 时钟：`{"name": "i_clk", "edge": "posedge"}`
- 复位：`{"name": "i_rstn", "active": "low", "synchronous": false}`

## 4. 接口信号规范

| 信号 | 方向 | 位宽 | 时钟域 | 语义角色 | 描述 |
| --- | --- | --- | --- | --- | --- |
| `i_clk` | input | 1 | i_clk | clock | i_clk |
| `i_rstn` | input | 1 | i_clk | reset | i_rstn |
| `i_rgb` | input | 96 | i_clk | signal | i_rgb |
| `i_valid` | input | 1 | i_clk | status | i_valid |
| `i_sof` | input | 1 | i_clk | signal | i_sof |
| `i_eol` | input | 1 | i_clk | signal | i_eol |
| `i_eof` | input | 1 | i_clk | signal | i_eof |
| `i_x` | input | 12 | i_clk | signal | i_x |
| `i_y` | input | 12 | i_clk | signal | i_y |
| `i_count_mode` | input | 1 | i_clk | control | i_count_mode |
| `i_strict` | input | 1 | i_clk | signal | i_strict |
| `i_face_unlocked` | input | 1 | i_clk | signal | i_face_unlocked |
| `i_face_busy` | input | 1 | i_clk | signal | i_face_busy |
| `i_face_fault` | input | 1 | i_clk | signal | i_face_fault |
| `i_face_confirmed` | input | 2 | i_clk | signal | i_face_confirmed |
| `i_camera_status` | input | 48 | i_clk | status | i_camera_status |
| `i_diag_count` | input | 4 | i_clk | signal | i_diag_count |
| `i_diag_reject` | input | 4 | i_clk | signal | i_diag_reject |
| `i_diag_width_bcd` | input | 16 | i_clk | signal | i_diag_width_bcd |
| `i_diag_height_bcd` | input | 16 | i_clk | signal | i_diag_height_bcd |
| `i_diag_area_bcd` | input | 28 | i_clk | signal | i_diag_area_bcd |
| `i_diag_fill_bcd` | input | 12 | i_clk | signal | i_diag_fill_bcd |
| `i_red_bcd` | input | 40 | i_clk | signal | i_red_bcd |
| `i_green_bcd` | input | 40 | i_clk | signal | i_green_bcd |
| `i_yellow_bcd` | input | 40 | i_clk | signal | i_yellow_bcd |
| `i_total_bcd` | input | 44 | i_clk | signal | i_total_bcd |
| `i_x_bcd` | input | 16 | i_clk | signal | i_x_bcd |
| `i_y_bcd` | input | 16 | i_clk | signal | i_y_bcd |
| `i_gate_state` | input | 3 | i_clk | signal | i_gate_state |
| `i_track_status` | input | 2 | i_clk | status | i_track_status |
| `i_reason` | input | 3 | i_clk | signal | i_reason |
| `o_rgb` | output | 96 | i_clk | signal | o_rgb |
| `o_valid` | output | 1 | i_clk | status | o_valid |
| `o_sof` | output | 1 | i_clk | signal | o_sof |
| `o_eol` | output | 1 | i_clk | signal | o_eol |
| `o_eof` | output | 1 | i_clk | signal | o_eof |
| `i_rotation_enable` | input | 1 | i_clk | native | i_rotation_enable |
| `i_rotation_angle_valid` | input | 1 | i_clk | native | i_rotation_angle_valid |
| `i_rotation_rpm_valid` | input | 1 | i_clk | native | i_rotation_rpm_valid |
| `i_rotation_negative` | input | 1 | i_clk | native | i_rotation_negative |
| `i_rotation_partial` | input | 1 | i_clk | native | i_rotation_partial |
| `i_rotation_status` | input | 3 | i_clk | native | i_rotation_status |
| `i_rotation_reason` | input | 4 | i_clk | native | i_rotation_reason |
| `i_rotation_rpm_bcd` | input | 32 | i_clk | native | i_rotation_rpm_bcd |
| `i_rotation_angle_bcd` | input | 16 | i_clk | native | i_rotation_angle_bcd |
| `i_rotation_net_bcd` | input | 20 | i_clk | native | i_rotation_net_bcd |
| `i_rotation_cw_bcd` | input | 40 | i_clk | native | i_rotation_cw_bcd |
| `i_rotation_ccw_bcd` | input | 40 | i_clk | native | i_rotation_ccw_bcd |

## 5. 周期行为与延迟

- 保留两拍像素合成；旋转开启时在144至157行显示角度、转速、圈数及诊断。

## 6. WaveDrom 时序图

### 事务与有效标记

示意图中的长事务已压缩；实际周期数以状态机及仿真报告为准，像素支路保持原延迟。

![事务与有效标记](waveforms/ball_status_osd_transaction.svg)

- WaveJSON：[ball_status_osd_transaction.json5](waveforms/ball_status_osd_transaction.json5)

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

- 规格模块：`ball_status_osd`
- RTL 路径：`rtl/ball_status_osd.v`
- 交付要求：本文档、WaveJSON 和 SVG 必须与同一版本规格一同发布。
