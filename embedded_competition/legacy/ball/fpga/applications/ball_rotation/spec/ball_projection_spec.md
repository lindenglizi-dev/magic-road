# ball_projection 模块规范

> RTL: `rtl/ball_projection.v`

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
| `i_valid` | input | 1 | i_clk | native | valid pixel group or candidate pulse; no video backpressure |
| `i_sof` | input | 1 | i_clk | native | first valid group of a frame |
| `i_eof` | input | 1 | i_clk | native | last valid group of a frame |
| `i_x` | input | (11)-(0)+1 | i_clk | native | Native application interface field i_x; see module behavior and source connections |
| `i_y` | input | (11)-(0)+1 | i_clk | native | Native application interface field i_y; see module behavior and source connections |
| `i_labels` | input | (7)-(0)+1 | i_clk | native | four exclusive two-bit labels, lane zero in bits 1:0; 0 unknown,1 red,2 yellow,3 green |
| `i_gate_hits` | input | (2)-(0)+1 | i_clk | native | Native application interface field i_gate_hits; see module behavior and source connections |
| `i_epoch` | input | (15)-(0)+1 | i_clk | native | configuration generation captured with frame statistics |
| `o_frame_start` | output | 1 | i_clk | native | start collecting metadata for a completed capture frame scan |
| `o_candidate_valid` | output | 1 | i_clk | native | one candidate on this clock; frame_done follows all candidates |
| `o_color` | output | (1)-(0)+1 | i_clk | native | 0 unknown,1 red,2 yellow,3 green |
| `o_area` | output | (19)-(0)+1 | i_clk | native | number of classified pixels in the candidate |
| `o_x_min` | output | (11)-(0)+1 | i_clk | native | inclusive left edge of candidate |
| `o_x_max` | output | (11)-(0)+1 | i_clk | native | inclusive right edge of candidate |
| `o_y_min` | output | (11)-(0)+1 | i_clk | native | inclusive top edge of candidate |
| `o_y_max` | output | (11)-(0)+1 | i_clk | native | inclusive bottom edge of candidate |
| `o_frame_done` | output | 1 | i_clk | native | complete statistics pulse, including frames with no candidates |
| `o_gate_pixels` | output | (19)-(0)+1 | i_clk | native | classified raw pixel count in the full rectangular counting gate |
| `o_epoch` | output | (15)-(0)+1 | i_clk | native | configuration generation captured with frame statistics |
| `o_overflow` | output | 1 | i_clk | native | more than eight accepted segments in this frame |
| `o_fault` | output | 1 | i_clk | native | dropped or overlapping statistics event; must not count as empty gate |
| `o_error` | output | 1 | i_clk | native | sticky video/statistics protocol diagnostic |

## 5. 周期行为与延迟

- Four pixel lanes update separate column RAMs with a one-cycle read/modify/write path. Two frame banks separate capture and scan.
- After the final RAM write, scan columns in READ/LOAD/ACC/ADVANCE phases. Merge at most two internal empty columns, then filter each segment.
- Emit at most eight candidates followed by frame_done. Flush the final column segment. Overflow blocks counting; incomplete/dropped frames never provide empty-gate evidence.

## 6. WaveDrom 时序图

### ball_projection interface event order

Logical event order only. Internal multi-cycle/frame intervals are compressed; exact latency is specified in behavior, not inferred from this sketch.

![ball_projection interface event order](waveforms/ball_projection_compressed-event-sequence.svg)

- WaveJSON：[ball_projection_compressed-event-sequence.json5](waveforms/ball_projection_compressed-event-sequence.json5)

## 7. 边界、反压与错误

- Reset or configuration change has priority over old results.
- Video invalid cycles must not advance pixel coordinates or packer phase.
- Conveyor V1 requires disjoint X projections, one ball per gate and three clear gate frames.

## 8. CDC 与综合约束

- Synthesizable Verilog-2001; Anlogic PH1P35MDG324/-3.
- W is a multiple of16; projection Y coordinates are10bit, so H<=1023. Default1280x720.
- No video ready/backpressure or frame-dropping substitution; detector faults do not alter video byte count.
- C_MAX_SIZE defaults to384; both accepted bounding-box dimensions must lie inclusively between C_MIN_SIZE=12 and C_MAX_SIZE. The previous160-pixel maximum is no longer the default.

## 9. 验证与验收

- sim/tb_ball_core.v:147-plus frames with split/hold100/dropout2/last column/BCD and byte ordering.
- sim/tb_ball_runtime.v:28 frames with boundary commits and late-result rejection.
- sim/tb_ball_hdmi.v:four complete720P frames and actual DDR capture.
- sim/tb_ball_lowlight.v: default projection admitsradius85-pixel (171-pixel bounding extent) shaded R/Y/G balls and rejects cyan background; exact object-derived labels and boxes are checked.

## 10. 可追溯性

- 规格模块：`ball_projection`
- RTL 路径：`rtl/ball_projection.v`
- 交付要求：本文档、WaveJSON 和 SVG 必须与同一版本规格一同发布。
