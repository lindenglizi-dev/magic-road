# ball_rotation_arithmetic 模块规范

> RTL: `rtl/ball_rotation_arithmetic.v`

## 1. 模块目的

Unsigned serial multiply and rounded restoring divide

## 2. 参数

| 参数 | 默认值 | 说明 |
| --- | --- | --- |
| C_BITS | 96 | 无符号运算宽度；质心实例为32 |

## 3. 时钟与复位

- 时钟：`{"name": "i_clk", "edge": "posedge"}`
- 复位：`{"name": "i_rstn", "active": "low", "synchronous": false, "soft_clear": "i_clear"}`

## 4. 接口信号规范

| 信号 | 方向 | 位宽 | 时钟域 | 语义角色 | 描述 |
| --- | --- | --- | --- | --- | --- |
| `i_clk` | input | 1 | i_clk | clock | 统计运算时钟 |
| `i_rstn` | input | 1 | i_clk | reset | 异步低有效复位 |
| `i_clear` | input | 1 | i_clk | native | 撤销正在执行的运算 |
| `i_start` | input | 1 | i_clk | native | 空闲时提交运算 |
| `i_divide` | input | 1 | i_clk | native | 为高执行除法，为低执行截断乘法 |
| `i_round` | input | 1 | i_clk | native | 除法按最近整数舍入 |
| `i_left` | input | C_BITS | i_clk | native | 被除数或第一乘数 |
| `i_right` | input | C_BITS | i_clk | native | 除数或第二乘数 |
| `o_busy` | output | 1 | i_clk | native | 正在占用串行运算器 |
| `o_done` | output | 1 | i_clk | native | 结果完成脉冲 |
| `o_error` | output | 1 | i_clk | native | 本次除数为零 |
| `o_result` | output | C_BITS | i_clk | native | 无符号结果或低位乘积 |

## 5. 周期行为与延迟

- Unsigned serial multiply and rounded restoring divide

## 6. WaveDrom 时序图

### 事务与有效标记

示意图中的长事务已压缩；实际周期数以状态机及仿真报告为准，像素支路保持原延迟。

![事务与有效标记](waveforms/ball_rotation_arithmetic_transaction.svg)

- WaveJSON：[ball_rotation_arithmetic_transaction.json5](waveforms/ball_rotation_arithmetic_transaction.json5)

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

- 规格模块：`ball_rotation_arithmetic`
- RTL 路径：`rtl/ball_rotation_arithmetic.v`
- 交付要求：本文档、WaveJSON 和 SVG 必须与同一版本规格一同发布。
