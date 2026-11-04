# ball_runtime 模块规范

> RTL: `rtl/ball_runtime.v`

## 1. 模块目的

既有视频检测与叠加流水线；将两位长按事件传出供相机调参。

## 2. 参数

| 参数 | 默认值 | 说明 |
| --- | --- | --- |
| C_WIDTH | 1280 | 每行像素数，必须为16的倍数 |
| C_HEIGHT | 720 | 帧有效像素行数 |
| C_X_MIN | 64 | ROI左边界，包含 |
| C_Y_MIN | 160 | ROI上边界，包含 |
| C_X_END | 1216 | ROI右边界，不包含 |
| C_Y_END | 640 | ROI下边界，不包含 |
| C_GATE_MIN | 544 | 计数门左边界，包含；运行层传给占用检测 |
| C_GATE_END | 736 | 计数门右边界，不包含；运行层传给占用检测 |
| C_LINE | 640 | 从左向右的计数中心线X |
| C_HYST | 16 | 中心线两侧确认迟滞像素数 |
| C_MIN_AREA | 128 | 连通区域有效同色像素最小面积，也用于疑似门占用 |
| C_MIN_SIZE | 12 | 候选框宽高最小像素数 |
| C_MAX_SIZE | 384 | 候选框宽高最大像素数 |
| C_MAX_MOVE | 64 | 原预测跟踪的单轴关联残差窗，计数修复不改此值 |
| C_DEBOUNCE | 2100000 | 板载键消抖稳定时钟数 |
| C_LONG_PRESS | 103520000 | 板载键长按判定时钟数 |

## 3. 时钟与复位

- 时钟：`{"name": "I_clk", "edge": "posedge"}`
- 复位：`{"name": "I_rst_n", "active": "low", "synchronous": false}`

## 4. 接口信号规范

| 信号 | 方向 | 位宽 | 时钟域 | 语义角色 | 描述 |
| --- | --- | --- | --- | --- | --- |
| `I_clk` | input | 1 | I_clk | clock | AWB pixel-group clock, same S_csi_rx_clk domain |
| `I_rst_n` | input | 1 | I_clk | reset | Native application interface field I_rst_n; see module behavior and source connections |
| `I_keys_n` | input | (3)-(0)+1 | I_clk | native | four original active-low board keys |
| `I_rgb` | input | (95)-(0)+1 | I_clk | native | four gamma-corrected RGB888 pixels, leftmost pixel in bits95:72 |
| `I_valid` | input | 1 | I_clk | native | valid pixel group or candidate pulse; no video backpressure |
| `I_user` | input | 1 | I_clk | native | early frame notification from the registered gamma path; independent of pixel-aligned SOF |
| `I_last` | input | 1 | I_clk | native | Native application interface field I_last; see module behavior and source connections |
| `O_data` | output | (127)-(0)+1 | I_clk | native | Native application interface field O_data; see module behavior and source connections |
| `O_valid` | output | 1 | I_clk | native | valid pixel group or candidate pulse; no video backpressure |
| `O_last` | output | 1 | I_clk | native | Native application interface field O_last; see module behavior and source connections |
| `O_done` | output | 1 | I_clk | native | complete word/frame event |
| `O_early` | output | 1 | I_clk | native | early frame notification independent of pixel valid |
| `O_error` | output | 1 | I_clk | native | sticky video/statistics protocol diagnostic |
| `O_red` | output | (31)-(0)+1 | I_clk | native | saturating red-ball pass count |
| `O_green` | output | (31)-(0)+1 | I_clk | native | saturating green-ball pass count |
| `O_yellow` | output | (31)-(0)+1 | I_clk | native | saturating yellow-ball pass count |
| `O_total` | output | (33)-(0)+1 | I_clk | native | 34-bit zero-extended sum of three color counts |
| `O_count_mode` | output | 1 | I_clk | native | zero single-track, one conveyor-count |
| `O_gate_state` | output | (2)-(0)+1 | I_clk | native | Native application interface field O_gate_state; see module behavior and source connections |
| `O_track_status` | output | (1)-(0)+1 | I_clk | native | Native application interface field O_track_status; see module behavior and source connections |
| `I_camera_status` | input | 48 | I_clk | native | Coherent camera diagnostics: FPS BCD[11:0], exposure BCD[27:12], gain BCD[35:28], readback state[37:36], cfg[38], WB-ready[39] |
| `O_camera_step` | output | 2 | I_clk | native | One retained toggle per long press:bit0=D5 exposure,bit1=A9 gain; receiver uses two synchronizers and edge detection. |

## 5. 周期行为与延迟

- Consume the gamma-corrected four-pixel RGB96 stream from isp_top; connect color front, bounded2Dcomponents, track/count, graphics, BCD, OSD and the unchanged RGB128 packer.
- Forward early by one clock independently of pixel SOF. The runtime pixel path remains seven registered cycles: two front, two overlay, two OSD and one packer. The upstream gamma adds one cycle outside this module.
- Reject old-epoch results. Tag decimal work by both epoch and job sequence; only a fully formatted snapshot can commit at a later early boundary.
- Camera status is coherent across domains; runtime freezes it at advance frame boundary before OSD. A fourth text row shows FPS/EXP/G/RB/WB/CAL without any extra video register stage.
- Expose board-key long-press toggles without adding any video/early register stage. D5/A9 short requests commit on early after debounced release.
- Color-support repair adds1pixel register in front only; runtime now7pixel stages and1independent advance-early stage.
- Replace the retired column detector with ball_components; tracker/counter implementations and raw gate semantics unchanged. At done, capture diagnostics before decimal conversion; commit all diagnostic BCD and N/R atomically with existing epoch/job snapshot.
- TRACK bbox and X/Y are one-frame forecasts from ball_target_tracker, clipped to configured ROI. COUNT metadata uses the original measured gate path. Tracker ports are unchanged; only ROI parameters are propagated.
- Pass C_GATE_MIN/END to detector. Gate counter receives scan_gate only when scan_gate_occupied, else zero. Raw detector gate count and display candidates preserved; fault/overflow and epoch guards unchanged. TRACK prediction path unchanged.

## 6. WaveDrom 时序图

### ball_runtime interface event order

Compressed logical frame events only, not measured clock timing. Multicandidate frame blocks; three subsequent sparse-only complete frames release; two upstream matches then downstream count once. Rejected substantial regions hold occupied.

![ball_runtime interface event order](waveforms/ball_runtime_compressed-event-sequence.svg)

- WaveJSON：[ball_runtime_compressed-event-sequence.json5](waveforms/ball_runtime_compressed-event-sequence.json5)

## 7. 边界、反压与错误

- Reset or configuration change has priority over old results.
- Video invalid cycles must not advance pixel coordinates or packer phase.
- Disconnected same-X regions can be extracted; count mode still requires at most one ball per gate and three clear raw-gate frames.

## 8. CDC 与综合约束

- Synthesizable Verilog-2001; Anlogic PH1P35MDG324/-3.
- W is a multiple of16, coordinates are12bit; configured ROI cell count<=65536 and pixel area<2^20. Default1280x720.
- No video ready/backpressure or frame-dropping substitution; detector faults do not alter video byte count.
- Default candidate width and height limits are inclusive12..384 pixels, minimum classified area128. Normal classification operates on gamma-corrected RGB; strict thresholds remain150/50.

## 9. 验证与验收

- sim/test_gate_recovery.py + tb_ball_gate_recovery.v:45frames; old frame6 staysGATE4/ERR2, new releases after3sparse128pxframes; rejected192pxregion holds, dropout/dedup/samecolor nextball, wrongcolor/overflow block.
- Existing 16component masks, partialROI/queue/collision, 6frameoverflow,206framemotion,28frameruntime and720P60 budget rerun.
- tb_ball_count_hdmi.v + check_count_hdmi.py:7full720Pframes, persistent sparse noise, yellow upstream/downstream counts1; actual capture and COUNT2 glyph.

## 10. 可追溯性

- 规格模块：`ball_runtime`
- RTL 路径：`rtl/ball_runtime.v`
- 交付要求：本文档、WaveJSON 和 SVG 必须与同一版本规格一同发布。
