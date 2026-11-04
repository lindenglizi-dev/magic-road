# ball_column_store 模块规范

> RTL: `rtl/ball_column_store.v`

## 1. 模块目的

未提供模块目的。

## 2. 参数

| 参数 | 默认值 | 说明 |
| --- | --- | --- |
| — | — | 本模块没有可配置参数。 |

## 3. 时钟与复位

- 时钟：`{"name": "i_clk", "edge": "posedge"}`
- 复位：`{"name": "no memory reset", "active": "none", "synchronous": false}`

## 4. 接口信号规范

| 信号 | 方向 | 位宽 | 时钟域 | 语义角色 | 描述 |
| --- | --- | --- | --- | --- | --- |
| `i_clk` | input | 1 | i_clk | clock | AWB pixel-group clock, same S_csi_rx_clk domain |
| `i_read_enable` | input | 1 | i_clk | native | perform one synchronous column-memory read |
| `i_read_address` | input | (C_ADDR_BITS-1)-(0)+1 | i_clk | native | column group address selected within one lane/frame bank |
| `i_write_enable` | input | 1 | i_clk | native | perform one synchronous column-memory write |
| `i_write_address` | input | (C_ADDR_BITS-1)-(0)+1 | i_clk | native | address delayed from the accepted capture read |
| `i_write_data` | input | (49)-(0)+1 | i_clk | native | packed R,Y,G counts and ymin/ymax, each ten bits |
| `o_read_data` | output | (49)-(0)+1 | i_clk | native | registered packed column result |

## 5. 周期行为与延迟

- One enabled read is synchronous with one-cycle latency; a separate enabled write updates a 50-bit column word.
- No memory-array reset is used. Every complete capture frame initializes all columns on its first row.

## 6. WaveDrom 时序图

### ball_column_store interface event order

Logical event order only. Internal multi-cycle/frame intervals are compressed; exact latency is specified in behavior, not inferred from this sketch.

![ball_column_store interface event order](waveforms/ball_column_store_compressed-event-sequence.svg)

- WaveJSON：[ball_column_store_compressed-event-sequence.json5](waveforms/ball_column_store_compressed-event-sequence.json5)

## 7. 边界、反压与错误

- Reset or configuration change has priority over old results.
- Video invalid cycles must not advance pixel coordinates or packer phase.
- Conveyor V1 requires disjoint X projections, one ball per gate and three clear gate frames.

## 8. CDC 与综合约束

- Synthesizable Verilog-2001; Anlogic PH1P35MDG324/-3.
- W is a multiple of16; projection Y coordinates are10bit, so H<=1023. Default1280x720.
- No video ready/backpressure or frame-dropping substitution; detector faults do not alter video byte count.

## 9. 验证与验收

- sim/tb_ball_core.v:147-plus frames with split/hold100/dropout2/last column/BCD and byte ordering.
- sim/tb_ball_runtime.v:28 frames with boundary commits and late-result rejection.
- sim/tb_ball_hdmi.v:four complete720P frames and actual DDR capture.

## 10. 可追溯性

- 规格模块：`ball_column_store`
- RTL 路径：`rtl/ball_column_store.v`
- 交付要求：本文档、WaveJSON 和 SVG 必须与同一版本规格一同发布。
