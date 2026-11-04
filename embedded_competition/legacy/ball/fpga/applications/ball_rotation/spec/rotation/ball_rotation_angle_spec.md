# ball_rotation_angle 模块规范

> RTL: `rtl/ball_rotation_angle.v`

## 1. 模块目的

Sixteen-iteration image-coordinate CORDIC phase

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
| `i_clk` | input | 1 | i_clk | clock | 向量计算时钟 |
| `i_rstn` | input | 1 | i_clk | reset | 异步低有效复位 |
| `i_clear` | input | 1 | i_clk | native | 撤销尚未完成的角度 |
| `i_start` | input | 1 | i_clk | native | 空闲时提交相对向量 |
| `i_dx` | input | 16 | i_clk | native | 有符号Q4水平位移 |
| `i_dy` | input | 16 | i_clk | native | 有符号Q4垂直位移 |
| `o_busy` | output | 1 | i_clk | native | CORDIC正在迭代 |
| `o_done` | output | 1 | i_clk | native | 本次向量处理结束 |
| `o_valid` | output | 1 | i_clk | native | 非零向量角度有效 |
| `o_phase` | output | 16 | i_clk | native | 65536表示一圈的相位 |

## 5. 周期行为与延迟

- Sixteen-iteration image-coordinate CORDIC phase

## 6. WaveDrom 时序图

### 事务与有效标记

示意图中的长事务已压缩；实际周期数以状态机及仿真报告为准，像素支路保持原延迟。

![事务与有效标记](waveforms/ball_rotation_angle_transaction.svg)

- WaveJSON：[ball_rotation_angle_transaction.json5](waveforms/ball_rotation_angle_transaction.json5)

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

- 规格模块：`ball_rotation_angle`
- RTL 路径：`rtl/ball_rotation_angle.v`
- 交付要求：本文档、WaveJSON 和 SVG 必须与同一版本规格一同发布。
