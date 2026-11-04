# ball_target_tracker 模块规范

> RTL: `rtl/ball_target_tracker.v`

## 1. 模块目的

未提供模块目的。

## 2. 参数

| 参数 | 默认值 | 说明 |
| --- | --- | --- |
| C_MAX_MOVE | 64 | 预测残差窗；1..1024，速度限幅为两倍此值 |
| C_X_MIN / C_Y_MIN / C_X_END / C_Y_END | 0 / 0 / 4096 / 4096 | 显示平移裁剪边界；runtime传入实际ROI |

## 3. 时钟与复位

- 时钟：`{"name": "i_clk", "edge": "posedge"}`
- 复位：`{"name": "i_rstn", "active": "low", "synchronous": false}`

## 4. 接口信号规范

| 信号 | 方向 | 位宽 | 时钟域 | 语义角色 | 描述 |
| --- | --- | --- | --- | --- | --- |
| `i_clk` | input | 1 | i_clk | clock | AWB pixel-group clock, same S_csi_rx_clk domain |
| `i_rstn` | input | 1 | i_clk | reset | asynchronous active-low reset |
| `i_clear` | input | 1 | i_clk | native | discard track/gate history; old frame work must not change new state |
| `i_frame_start` | input | 1 | i_clk | native | start collecting metadata for a completed capture frame scan |
| `i_candidate_valid` | input | 1 | i_clk | native | one candidate on this clock; frame_done follows all candidates |
| `i_color` | input | (1)-(0)+1 | i_clk | native | 0 unknown,1 red,2 yellow,3 green |
| `i_area` | input | (19)-(0)+1 | i_clk | native | number of classified pixels in the candidate |
| `i_x_min` | input | (11)-(0)+1 | i_clk | native | inclusive left edge of candidate |
| `i_x_max` | input | (11)-(0)+1 | i_clk | native | inclusive right edge of candidate |
| `i_y_min` | input | (11)-(0)+1 | i_clk | native | inclusive top edge of candidate |
| `i_y_max` | input | (11)-(0)+1 | i_clk | native | inclusive bottom edge of candidate |
| `i_frame_done` | input | 1 | i_clk | native | complete statistics pulse, including frames with no candidates |
| `i_overflow` | input | 1 | i_clk | native | more than eight accepted segments in this frame |
| `o_valid` | output | 1 | i_clk | native | valid pixel group or candidate pulse; no video backpressure |
| `o_status` | output | (1)-(0)+1 | i_clk | native | tracker:0 search,1 confirm,2 track,3 temporarily lost |
| `o_color` | output | (1)-(0)+1 | i_clk | native | 0 unknown,1 red,2 yellow,3 green |
| `o_x_min` | output | (11)-(0)+1 | i_clk | native | One-frame forecast coordinate on accepted measurement; clamped to ROI as a whole; held on misses. Not a raw measured coordinate. |
| `o_x_max` | output | (11)-(0)+1 | i_clk | native | One-frame forecast coordinate on accepted measurement; clamped to ROI as a whole; held on misses. Not a raw measured coordinate. |
| `o_y_min` | output | (11)-(0)+1 | i_clk | native | One-frame forecast coordinate on accepted measurement; clamped to ROI as a whole; held on misses. Not a raw measured coordinate. |
| `o_y_max` | output | (11)-(0)+1 | i_clk | native | One-frame forecast coordinate on accepted measurement; clamped to ROI as a whole; held on misses. Not a raw measured coordinate. |
| `o_center_x` | output | (11)-(0)+1 | i_clk | native | One-frame forecast coordinate on accepted measurement; clamped to ROI as a whole; held on misses. Not a raw measured coordinate. |
| `o_center_y` | output | (11)-(0)+1 | i_clk | native | One-frame forecast coordinate on accepted measurement; clamped to ROI as a whole; held on misses. Not a raw measured coordinate. |

## 5. 周期行为与延迟

- Search: choose the largest valid nonzero-color region. First match has zero velocity and status1.
- Associate only identical color and width/height each within [previous/2, previous*2]. Rank candidates in the predicted-position window before candidates in the observed-position fallback window; then minimum Manhattan prediction residual. Equal scores retain input order.
- Prediction reference is the last observed center plus velocity*(misses+1); status1 bootstrap window is 2*C_MAX_MOVE, otherwise residual window C_MAX_MOVE*(misses+1). Actual observed positions are stored separately from forecast output.
- Consecutive measurements update per-axis velocity to the observed delta, with <=4pixel deadband and +/-2*C_MAX_MOVE clamp. First recovery after missing frames retains previous velocity; next consecutive observation updates it.
- Commit at frame_done only. Output the measured bbox translated by one velocity step, clamped as a whole within the ROI; center is translated identically. Missing1/2 hold the last output with status3; missing3 clears valid. Two observations confirm status2.
- Clear/reset/overflow discard lock and velocity. Candidate stream can be consecutive; frame_start and frame_done must be separate from candidates. Frame_done follows last candidate by at least one clock. Video pipeline/early latency and counting remain unchanged.

## 6. WaveDrom 时序图

### ball_target_tracker interface event order

Compressed frame event order, not measured clock timing. Matching frame centers200,280,360 gives display centers199,359,439; empty frame freezes439 with LOST.

![ball_target_tracker interface event order](waveforms/ball_target_tracker_compressed-event-sequence.svg)

- WaveJSON：[ball_target_tracker_compressed-event-sequence.json5](waveforms/ball_target_tracker_compressed-event-sequence.json5)

## 7. 边界、反压与错误

- Sudden stop uses observed-position fallback. Predicted-window target wins over stationary background even if background has greater area.
- Forecast clipping preserves bbox size and cannot recreate the portion of a ball already outside the ROI.
- No new moving box is fabricated during misses; displayed coordinate is an estimate, not raw measured centroid.

## 8. CDC 与综合约束

- Verilog-2001, asynchronous active-low reset, S_csi_rx_clk domain; no CDC added.
- 1<=C_MAX_MOVE<=1024; 0<=ROI min<end<=4096. Candidate bbox inclusive, within ROI, nonzero color, valid dimensions. Runtime enforces epoch/mode.
- One forecast frame compensates nominal display lag only. Dense-region statistics can add an extra frame; sudden acceleration, same-color same-size interference, connected regions and optical blur remain limitations.

## 9. 验证与验收

- sim/test_motion.py and tb_ball_motion.v:206 frames/990 cycle snapshots,80px/frame vs original64,wrong color,size,dropout,stop,ROI,signed velocity,clear/overflow.
- tb_ball_runtime.v:28frames including count,epoch,clear,OSD/packing; tb_ball_dark_noise.v:9frames3colors with explicit clear between independent color cases.
- tb_ball_hdmi_lowlight.v and check_motion_hdmi.py: actual4frame720P capture; expected forecast center331,399 versus current synthetic ball332,400.

## 10. 可追溯性

- 规格模块：`ball_target_tracker`
- RTL 路径：`rtl/ball_target_tracker.v`
- 交付要求：本文档、WaveJSON 和 SVG 必须与同一版本规格一同发布。
