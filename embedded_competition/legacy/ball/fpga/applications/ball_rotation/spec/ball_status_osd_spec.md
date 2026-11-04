# ball_status_osd 模块规范

> RTL: `rtl/ball_status_osd.v`

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
| `i_count_mode` | input | 1 | i_clk | native | zero single-track, one conveyor-count |
| `i_strict` | input | 1 | i_clk | native | strict: brightness150 and channel gap50; normal: gamma-domain brightness64, gap12 and 5:4 relative channel dominance |
| `i_red_bcd` | input | (39)-(0)+1 | i_clk | native | Frame-frozen packed BCD display field: red_bcd |
| `i_green_bcd` | input | (39)-(0)+1 | i_clk | native | Frame-frozen packed BCD display field: green_bcd |
| `i_yellow_bcd` | input | (39)-(0)+1 | i_clk | native | Frame-frozen packed BCD display field: yellow_bcd |
| `i_total_bcd` | input | (43)-(0)+1 | i_clk | native | Frame-frozen packed BCD display field: total_bcd |
| `i_x_bcd` | input | (15)-(0)+1 | i_clk | native | Frame-frozen packed BCD display field: x_bcd |
| `i_y_bcd` | input | (15)-(0)+1 | i_clk | native | Frame-frozen packed BCD display field: y_bcd |
| `i_gate_state` | input | (2)-(0)+1 | i_clk | native | Native application interface field i_gate_state; see module behavior and source connections |
| `i_track_status` | input | (1)-(0)+1 | i_clk | native | Native application interface field i_track_status; see module behavior and source connections |
| `i_reason` | input | (2)-(0)+1 | i_clk | native | 0 normal,1 overflow,2 multi-ball,3 no upstream,4 short gap/reverse,5 frame fault,6 saturated,7 video error |
| `o_rgb` | output | (95)-(0)+1 | i_clk | native | four RGB888 pixels, leftmost pixel in bits 95:72 |
| `o_valid` | output | 1 | i_clk | native | valid pixel group or candidate pulse; no video backpressure |
| `o_sof` | output | 1 | i_clk | native | first valid group of a frame |
| `o_eol` | output | 1 | i_clk | native | last valid group of a line |
| `o_eof` | output | 1 | i_clk | native | last valid group of a frame |
| `i_camera_status` | input | 48 | i_clk | native | Coherent camera diagnostics: FPS BCD[11:0], exposure BCD[27:12], gain BCD[35:28], readback state[37:36], cfg[38], WB-ready[39] |
| `i_diag_count` | input | 4 | i_clk | native | Accepted candidate count, <=8 |
| `i_diag_reject` | input | 4 | i_clk | native | Rejection bitmask:1 area,2 dimensions,4 aspect,8 fill |
| `i_diag_width_bcd` | input | 16 | i_clk | native | Four frozen decimal width digits |
| `i_diag_height_bcd` | input | 16 | i_clk | native | Four frozen decimal height digits |
| `i_diag_area_bcd` | input | 28 | i_clk | native | Seven frozen decimal area digits |
| `i_diag_fill_bcd` | input | 12 | i_clk | native | Three frozen decimal fill digits |

## 5. 周期行为与延迟

- One character/glyph lookup is shared by four aligned pixels; lookup and composition take two registered cycles.
- Use complete BCD snapshots for coordinates and counts. Five-by-seven glyphs are doubled; a dark panel occupies y<144 without changing stream length.
- The first title row includes the GAMMA marker in character columns24..28 retained from prior low-light builds; the fifth-row CCL4 marker identifies this milestone; marker text does not alter pixel/line/frame length.
- Camera status is coherent across domains; runtime freezes it at advance frame boundary before OSD. A fourth text row shows FPS/EXP/G/RB/WB/CAL without any extra video register stage.
- Add row128..141 with CCL4 N/W/H/A/F/R; panel extends to y143. Original lookup/composition remains two registered clocks. Rejection is hexadecimal bitmask; ERR meanings remain unchanged.
- TRACK mode top row columns32..35 display PRED. COUNT mode leaves these columns blank. Existing diagnostics CCL4 N/W/H/A/F/R unchanged.
- COUNT top row now shows COUNT2 at columns16..21; TRACK and PRED remain unchanged. This identifies gate recovery bit; all other glyph timing unchanged.

## 6. WaveDrom 时序图

### ball_status_osd interface event order

Compressed logical frame events only, not measured clock timing. Multicandidate frame blocks; three subsequent sparse-only complete frames release; two upstream matches then downstream count once. Rejected substantial regions hold occupied.

![ball_status_osd interface event order](waveforms/ball_status_osd_compressed-event-sequence.svg)

- WaveJSON：[ball_status_osd_compressed-event-sequence.json5](waveforms/ball_status_osd_compressed-event-sequence.json5)

## 7. 边界、反压与错误

- Reset or configuration change has priority over old results.
- Video invalid cycles must not advance pixel coordinates or packer phase.
- Disconnected same-X regions can be extracted; count mode still requires at most one ball per gate and three clear raw-gate frames.

## 8. CDC 与综合约束

- Synthesizable Verilog-2001; Anlogic PH1P35MDG324/-3.
- W is a multiple of16, coordinates are12bit; configured ROI cell count<=65536 and pixel area<2^20. Default1280x720.
- No video ready/backpressure or frame-dropping substitution; detector faults do not alter video byte count.

## 9. 验证与验收

- sim/test_gate_recovery.py + tb_ball_gate_recovery.v:45frames; old frame6 staysGATE4/ERR2, new releases after3sparse128pxframes; rejected192pxregion holds, dropout/dedup/samecolor nextball, wrongcolor/overflow block.
- Existing 16component masks, partialROI/queue/collision, 6frameoverflow,206framemotion,28frameruntime and720P60 budget rerun.
- tb_ball_count_hdmi.v + check_count_hdmi.py:7full720Pframes, persistent sparse noise, yellow upstream/downstream counts1; actual capture and COUNT2 glyph.

## 10. 可追溯性

- 规格模块：`ball_status_osd`
- RTL 路径：`rtl/ball_status_osd.v`
- 交付要求：本文档、WaveJSON 和 SVG 必须与同一版本规格一同发布。
