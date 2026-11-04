# ball_overlay 模块规范

> RTL: `rtl/ball_overlay.v`

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
| `i_rgb` | input | (95)-(0)+1 | i_clk | native | four RGB888 pixels, leftmost pixel in bits 95:72 |
| `i_valid` | input | 1 | i_clk | native | valid pixel group or candidate pulse; no video backpressure |
| `i_sof` | input | 1 | i_clk | native | first valid group of a frame |
| `i_eol` | input | 1 | i_clk | native | last valid group of a line |
| `i_eof` | input | 1 | i_clk | native | last valid group of a frame |
| `i_x` | input | (11)-(0)+1 | i_clk | native | Native application interface field i_x; see module behavior and source connections |
| `i_y` | input | (11)-(0)+1 | i_clk | native | Native application interface field i_y; see module behavior and source connections |
| `i_labels` | input | (7)-(0)+1 | i_clk | native | four exclusive two-bit labels, lane zero in bits 1:0; 0 unknown,1 red,2 yellow,3 green |
| `i_mask` | input | 1 | i_clk | native | display segmented mask without feeding graphics into detection |
| `i_count_mode` | input | 1 | i_clk | native | zero single-track, one conveyor-count |
| `i_box_valid` | input | (7)-(0)+1 | i_clk | native | Eight packed box descriptors, slot zero in the least-significant slice: box_valid |
| `i_box_color` | input | (15)-(0)+1 | i_clk | native | Eight packed box descriptors, slot zero in the least-significant slice: box_color |
| `i_box_left` | input | (95)-(0)+1 | i_clk | native | Eight packed box descriptors, slot zero in the least-significant slice: box_left |
| `i_box_right` | input | (95)-(0)+1 | i_clk | native | Eight packed box descriptors, slot zero in the least-significant slice: box_right |
| `i_box_top` | input | (95)-(0)+1 | i_clk | native | Eight packed box descriptors, slot zero in the least-significant slice: box_top |
| `i_box_bottom` | input | (95)-(0)+1 | i_clk | native | Eight packed box descriptors, slot zero in the least-significant slice: box_bottom |
| `o_rgb` | output | (95)-(0)+1 | i_clk | native | four RGB888 pixels, leftmost pixel in bits 95:72 |
| `o_valid` | output | 1 | i_clk | native | valid pixel group or candidate pulse; no video backpressure |
| `o_sof` | output | 1 | i_clk | native | first valid group of a frame |
| `o_eol` | output | 1 | i_clk | native | last valid group of a line |
| `o_eof` | output | 1 | i_clk | native | last valid group of a frame |
| `o_x` | output | (11)-(0)+1 | i_clk | native | Native application interface field o_x; see module behavior and source connections |
| `o_y` | output | (11)-(0)+1 | i_clk | native | Native application interface field o_y; see module behavior and source connections |

## 5. 周期行为与延迟

- Register each of four pixel lanes against all eight frozen boxes, ROI and gate lines, then compose colors in a second registered stage.
- RGB, coordinates and all valid/SOF/EOL/EOF markers have exactly two cycles latency. Labels are observed before any graphics are applied.

## 6. WaveDrom 时序图

### ball_overlay interface event order

Logical event order only. Internal multi-cycle/frame intervals are compressed; exact latency is specified in behavior, not inferred from this sketch.

![ball_overlay interface event order](waveforms/ball_overlay_compressed-event-sequence.svg)

- WaveJSON：[ball_overlay_compressed-event-sequence.json5](waveforms/ball_overlay_compressed-event-sequence.json5)

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

- 规格模块：`ball_overlay`
- RTL 路径：`rtl/ball_overlay.v`
- 交付要求：本文档、WaveJSON 和 SVG 必须与同一版本规格一同发布。
