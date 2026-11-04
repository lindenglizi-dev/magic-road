# ball_key_control 模块规范

> RTL: `rtl/ball_key_control.v`

## 1. 模块目的

板载四键消抖、互斥短长按及帧边界应用配置。

## 2. 参数

| 参数 | 默认值 | 说明 |
| --- | --- | --- |
| C_DEBOUNCE | 2100000 | 双向消抖时钟数，名义约20ms。 |
| C_COUNT_BITS | $clog2(C_DEBOUNCE+1) | 消抖计数位宽。 |
| C_LONG_PRESS | 103520000 | 消抖后的有效持续按下门限，名义约1秒。 |
| C_HOLD_BITS | $clog2(C_LONG_PRESS+1) | 长按计数位宽。 |

## 3. 时钟与复位

- 时钟：`{"name": "i_clk", "edge": "posedge"}`
- 复位：`{"name": "i_rstn", "active": "low", "synchronous": false}`

## 4. 接口信号规范

| 信号 | 方向 | 位宽 | 时钟域 | 语义角色 | 描述 |
| --- | --- | --- | --- | --- | --- |
| `i_clk` | input | 1 | i_clk | clock | AWB pixel-group clock, same S_csi_rx_clk domain |
| `i_rstn` | input | 1 | i_clk | reset | asynchronous active-low reset |
| `i_keys_n` | input | (3)-(0)+1 | i_clk | native | four original active-low board keys |
| `i_early` | input | 1 | i_clk | native | early frame notification independent of pixel valid |
| `o_count_mode` | output | 1 | i_clk | native | zero single-track, one conveyor-count |
| `o_strict` | output | 1 | i_clk | native | strict: brightness150 and channel gap50; normal: gamma-domain brightness64, gap12 and 5:4 relative channel dominance |
| `o_mask` | output | 1 | i_clk | native | display segmented mask without feeding graphics into detection |
| `o_epoch` | output | (15)-(0)+1 | i_clk | native | configuration generation captured with frame statistics |
| `o_clear` | output | 1 | i_clk | native | discard track/gate history; old frame work must not change new state |
| `o_clear_counts` | output | 1 | i_clk | native | clear color totals only when clear is also asserted |
| `o_camera_step` | output | 2 | i_clk | native | One retained toggle per long press:bit0=D5 exposure,bit1=A9 gain; receiver uses two synchronizers and edge detection. |

## 5. 周期行为与延迟

- Two flip-flop synchronization and bidirectional C_DEBOUNCE. D5/A9 short request fires on debounced release; a stable hold of C_LONG_PRESS=103520000 cycles toggles camera bit once and suppresses short release. B9/C7 retain press-edge behavior.
- Commit mode/mask/threshold requests at early only. Mode/threshold/clear increment the configuration epoch; mask-only changes preserve tracking/count history.

## 6. WaveDrom 时序图

### Short release and long toggle

Logical order; debounce and hold intervals compressed. Video/early latency unchanged.

![Short release and long toggle](waveforms/ball_key_control_compressed-key-sequence.svg)

- WaveJSON：[ball_key_control_compressed-key-sequence.json5](waveforms/ball_key_control_compressed-key-sequence.json5)

## 7. 边界、反压与错误

- Reset or configuration change has priority over old results.
- Video invalid cycles must not advance pixel coordinates or packer phase.
- Conveyor V1 requires disjoint X projections, one ball per gate and three clear gate frames.

## 8. CDC 与综合约束

- Synthesizable Verilog-2001; Anlogic PH1P35MDG324/-3.
- W is a multiple of16; projection Y coordinates are10bit, so H<=1023. Default1280x720.
- No video ready/backpressure or frame-dropping substitution; detector faults do not alter video byte count.
- C_LONG_PRESS>=1; C_HOLD_BITS must represent C_LONG_PRESS-1; nominal103.520MHz gives about1second after debounced press. Source video clock must be running.
- Release bounce shorter than debounce does not rearm the long event; both camera bits reset0 with the receiving domain.

## 9. 验证与验收

- sim/tb_ball_core.v:147-plus frames with split/hold100/dropout2/last column/BCD and byte ordering.
- sim/tb_ball_runtime.v:28 frames with boundary commits and late-result rejection.
- sim/tb_ball_hdmi.v:four complete720P frames and actual DDR capture.
- tb_ball_board_keys: press/release bounce, release-only short, long across early boundaries, all profiles, asynchronous receiver, busy queue, simultaneous hold, reset.

## 10. 可追溯性

- 规格模块：`ball_key_control`
- RTL 路径：`rtl/ball_key_control.v`
- 交付要求：本文档、WaveJSON 和 SVG 必须与同一版本规格一同发布。
