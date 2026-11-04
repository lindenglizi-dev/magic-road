# rgb96_pack128_valid 模块规范

> RTL: `rtl/rgb96_pack128_valid.v`

## 1. 模块目的

未提供模块目的。

## 2. 参数

| 参数 | 默认值 | 说明 |
| --- | --- | --- |
| — | — | 本模块没有可配置参数。 |

## 3. 时钟与复位

- 时钟：`{"name": "I_clk", "edge": "posedge"}`
- 复位：`{"name": "no memory reset", "active": "none", "synchronous": false}`

## 4. 接口信号规范

| 信号 | 方向 | 位宽 | 时钟域 | 语义角色 | 描述 |
| --- | --- | --- | --- | --- | --- |
| `I_clk` | input | 1 | I_clk | clock | AWB group clock |
| `I_rst_n` | input | 1 | I_clk | reset | Asynchronous active-low reset |
| `I_rgb` | input | 96 | I_clk | native | Four RGB888 pixels in left-to-right MSB order |
| `I_valid` | input | 1 | I_clk | native | Accepted four-pixel group |
| `I_user` | input | 1 | I_clk | native | Pixel-aligned SOF, not the independent early pulse |
| `I_last` | input | 1 | I_clk | native | Valid line-end group |
| `I_done` | input | 1 | I_clk | native | Valid frame-end group |
| `O_data` | output | 128 | I_clk | native | Ordered sixteen-byte DDR word |
| `O_valid` | output | 1 | I_clk | native | Valid packed word |
| `O_last` | output | 1 | I_clk | native | Last packed word of line |
| `O_done` | output | 1 | I_clk | native | Last packed word of frame |
| `O_error` | output | 1 | I_clk | native | Sticky packing alignment error |

## 5. 周期行为与延迟

- Reuse the original Anlogic application packer without semantic changes. Four valid 12-byte groups produce three ordered 16-byte words.
- Invalid cycles retain byte remainder and packing phase. EOL/EOF must coincide with phase three.

## 6. WaveDrom 时序图

### rgb96_pack128_valid interface event order

Logical event order only. Internal multi-cycle/frame intervals are compressed; exact latency is specified in behavior, not inferred from this sketch.

![rgb96_pack128_valid interface event order](waveforms/rgb96_pack128_valid_compressed-event-sequence.svg)

- WaveJSON：[rgb96_pack128_valid_compressed-event-sequence.json5](waveforms/rgb96_pack128_valid_compressed-event-sequence.json5)

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

- 规格模块：`rgb96_pack128_valid`
- RTL 路径：`rtl/rgb96_pack128_valid.v`
- 交付要求：本文档、WaveJSON 和 SVG 必须与同一版本规格一同发布。
