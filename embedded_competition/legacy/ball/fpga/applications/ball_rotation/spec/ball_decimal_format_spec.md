# ball_decimal_format 模块规范

> RTL: `rtl/ball_decimal_format.v`

## 1. 模块目的

未提供模块目的。

## 2. 参数

| 参数 | 默认值 | 说明 |
| --- | --- | --- |
| — | — | 本模块没有可配置参数。 |

## 3. 时钟与复位

- 时钟：`{"name": "i_clk", "edge": "posedge"}`
- 复位：`{"name": "i_rstn", "active": "low", "synchronous": false}`

## 4. 接口信号规范

| 信号 | 方向 | 位宽 | 时钟域 | 语义角色 | 描述 |
| --- | --- | --- | --- | --- | --- |
| `i_clk` | input | 1 | i_clk | clock | AWB pixel-group clock, same S_csi_rx_clk domain |
| `i_rstn` | input | 1 | i_clk | reset | asynchronous active-low reset |
| `i_load` | input | 1 | i_clk | native | start/restart decimal conversion |
| `i_binary` | input | (C_BITS-1)-(0)+1 | i_clk | native | unsigned input captured when load is high |
| `o_bcd` | output | (C_DIGITS*4-1)-(0)+1 | i_clk | native | stable packed BCD; least-significant digit is bits 3:0 |
| `o_done` | output | 1 | i_clk | native | complete word/frame event |
| `o_busy` | output | 1 | i_clk | native | module is processing a captured request |

## 5. 周期行为与延迟

- On load capture the binary value and clear working BCD; each following clock performs add-three and shifts one bit.
- After C_BITS clocks publish a complete stable BCD word and pulse done; a new load restarts conversion without partial publication.

## 6. WaveDrom 时序图

### ball_decimal_format interface event order

Logical event order only. Internal multi-cycle/frame intervals are compressed; exact latency is specified in behavior, not inferred from this sketch.

![ball_decimal_format interface event order](waveforms/ball_decimal_format_compressed-event-sequence.svg)

- WaveJSON：[ball_decimal_format_compressed-event-sequence.json5](waveforms/ball_decimal_format_compressed-event-sequence.json5)

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

- 规格模块：`ball_decimal_format`
- RTL 路径：`rtl/ball_decimal_format.v`
- 交付要求：本文档、WaveJSON 和 SVG 必须与同一版本规格一同发布。
