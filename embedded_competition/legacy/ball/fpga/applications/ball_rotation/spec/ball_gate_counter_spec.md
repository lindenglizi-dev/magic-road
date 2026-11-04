# ball_gate_counter 模块规范

> RTL: `rtl/ball_gate_counter.v`

## 1. 模块目的

未提供模块目的。

## 2. 参数

| 参数 | 默认值 | 说明 |
| --- | --- | --- |
| C_GATE_MIN | 544 | 计数门左边界，包含；运行层传给占用检测 |
| C_GATE_END | 736 | 计数门右边界，不包含；运行层传给占用检测 |
| C_GATE_TOP | 160 | 计数门上边界，包含 |
| C_GATE_BOTTOM | 640 | 计数门下边界，不包含 |
| C_LINE | 640 | 从左向右的计数中心线X |
| C_HYST | 16 | 中心线两侧确认迟滞像素数 |
| C_MIN_GATE_PIXELS | 8 | 经区域确认的门内有效像素阈值，低于此值才可能空门 |

## 3. 时钟与复位

- 时钟：`{"name": "i_clk", "edge": "posedge"}`
- 复位：`{"name": "i_rstn", "active": "low", "synchronous": false}`

## 4. 接口信号规范

| 信号 | 方向 | 位宽 | 时钟域 | 语义角色 | 描述 |
| --- | --- | --- | --- | --- | --- |
| `i_clk` | input | 1 | i_clk | clock | AWB pixel-group clock, same S_csi_rx_clk domain |
| `i_rstn` | input | 1 | i_clk | reset | asynchronous active-low reset |
| `i_clear` | input | 1 | i_clk | native | discard track/gate history; old frame work must not change new state |
| `i_clear_counts` | input | 1 | i_clk | native | clear color totals only when clear is also asserted |
| `i_fault` | input | 1 | i_clk | native | dropped or overlapping statistics event; must not count as empty gate |
| `i_frame_start` | input | 1 | i_clk | native | start collecting metadata for a completed capture frame scan |
| `i_candidate_valid` | input | 1 | i_clk | native | one candidate on this clock; frame_done follows all candidates |
| `i_color` | input | (1)-(0)+1 | i_clk | native | 0 unknown,1 red,2 yellow,3 green |
| `i_x_min` | input | (11)-(0)+1 | i_clk | native | inclusive left edge of candidate |
| `i_x_max` | input | (11)-(0)+1 | i_clk | native | inclusive right edge of candidate |
| `i_y_min` | input | (11)-(0)+1 | i_clk | native | inclusive top edge of candidate |
| `i_y_max` | input | (11)-(0)+1 | i_clk | native | inclusive bottom edge of candidate |
| `i_frame_done` | input | 1 | i_clk | native | complete statistics pulse, including frames with no candidates |
| `i_overflow` | input | 1 | i_clk | native | more than eight accepted segments in this frame |
| `i_gate_pixels` | input | (19)-(0)+1 | i_clk | native | Effective gate color pixel count: runtime passes original raw count only if a connected region >= C_MIN_AREA overlaps gate, else zero. Other direct callers may still supply raw occupancy. Valid only with complete frame_done. |
| `o_red` | output | (31)-(0)+1 | i_clk | native | saturating red-ball pass count |
| `o_yellow` | output | (31)-(0)+1 | i_clk | native | saturating yellow-ball pass count |
| `o_green` | output | (31)-(0)+1 | i_clk | native | saturating green-ball pass count |
| `o_total` | output | (33)-(0)+1 | i_clk | native | 34-bit zero-extended sum of three color counts |
| `o_state` | output | (2)-(0)+1 | i_clk | native | gate FSM:0 wait-clear,1 ready,2 armed,3 hold,4 blocked |
| `o_empty` | output | (1)-(0)+1 | i_clk | native | consecutive completed empty gate frames, saturated at three |
| `o_event` | output | (1)-(0)+1 | i_clk | native | one-clock color of a newly accepted pass, zero if no event |
| `o_reason` | output | (2)-(0)+1 | i_clk | native | 0 normal,1 overflow,2 multi-ball,3 no upstream,4 short gap/reverse,5 frame fault,6 saturated,7 video error |
| `o_center_x` | output | (11)-(0)+1 | i_clk | native | floor((xmin+xmax)/2), not pixel-weighted centroid |
| `o_center_y` | output | (11)-(0)+1 | i_clk | native | floor((ymin+ymax)/2), not pixel-weighted centroid |

## 5. 周期行为与延迟

- Require three empty completed frames, then two consistent upstream observations before arming. A confirmed center reaching downstream emits exactly one count.
- HOLD never expires by elapsed time. One/two missing frames preserve identity; three empty gate frames rearm. Multi-ball, overflow, reverse or downstream-first observations block.
- Three color counters saturate at 32 bits. Total is a zero-extended 34-bit sum. Clear has priority over simultaneous old frame completion.
- Runtime qualifies i_gate_pixels with detector connected-region occupancy; no substantial region means effective count zero even if raw sparse pixels>=8. Any accepted gate candidate still prevents empty. Fault/overflow/multiple candidates retain blocking priority. Three complete empty frames still required for release.
- In ARMED/HOLD, one candidate centered inside gate with color != locked color blocks with reason4; never increment on that frame. Status/ports/reset/counter saturation semantics unchanged. Fast balls still require two upstream observations inside the existing gate.

## 6. WaveDrom 时序图

### ball_gate_counter interface event order

Compressed logical frame events only, not measured clock timing. Multicandidate frame blocks; three subsequent sparse-only complete frames release; two upstream matches then downstream count once. Rejected substantial regions hold occupied.

![ball_gate_counter interface event order](waveforms/ball_gate_counter_compressed-event-sequence.svg)

- WaveJSON：[ball_gate_counter_compressed-event-sequence.json5](waveforms/ball_gate_counter_compressed-event-sequence.json5)

## 7. 边界、反压与错误

- Reset or configuration change has priority over old results.
- Video invalid cycles must not advance pixel coordinates or packer phase.
- Conveyor V1 requires disjoint X projections, one ball per gate and three clear gate frames.

## 8. CDC 与综合约束

- Synthesizable Verilog-2001; Anlogic PH1P35MDG324/-3.
- W is a multiple of16; projection Y coordinates are10bit, so H<=1023. Default1280x720.
- No video ready/backpressure or frame-dropping substitution; detector faults do not alter video byte count.

## 9. 验证与验收

- sim/test_gate_recovery.py + tb_ball_gate_recovery.v:45frames; old frame6 staysGATE4/ERR2, new releases after3sparse128pxframes; rejected192pxregion holds, dropout/dedup/samecolor nextball, wrongcolor/overflow block.
- Existing 16component masks, partialROI/queue/collision, 6frameoverflow,206framemotion,28frameruntime and720P60 budget rerun.
- tb_ball_count_hdmi.v + check_count_hdmi.py:7full720Pframes, persistent sparse noise, yellow upstream/downstream counts1; actual capture and COUNT2 glyph.

## 10. 可追溯性

- 规格模块：`ball_gate_counter`
- RTL 路径：`rtl/ball_gate_counter.v`
- 交付要求：本文档、WaveJSON 和 SVG 必须与同一版本规格一同发布。
