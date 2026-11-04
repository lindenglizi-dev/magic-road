# ball_white_balance 模块规范

> RTL: `rtl/ball_white_balance.v`

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
| `i_clk` | input | 1 | i_clk | clock | CSI pixel-group clock |
| `i_rstn` | input | 1 | i_clk | reset | Asynchronous active-low reset |
| `i_rgb` | input | 96 | i_clk | native | Four uncorrected demosaic RGB888 pixels |
| `i_valid` | input | 1 | i_clk | native | Accepted four-pixel group |
| `i_early` | input | 1 | i_clk | native | Independent early frame boundary |
| `o_gain_red` | output | 20 | i_clk | native | Frame-frozen unsigned Q16 red gain |
| `o_gain_blue` | output | 20 | i_clk | native | Frame-frozen unsigned Q16 blue gain |
| `o_ready` | output | 1 | i_clk | native | At least one valid neutral estimate has been committed |

## 5. 周期行为与延迟

- Statistics-only pipeline: capture RGB/flags, register per-lane neutral masks, register balanced four-lane sums. Accumulate and process the frame boundary3 clocks after input early. Existing AWB pixel output has its original50-cycle delay, so active gains settle before pixels. No RGB/valid/early video latency added.
- All4 lanes contribute only if minRGB>=16, maxRGB<=224 and2*max<=3*min. At least64 neutral pixels are required.
- Frame boundary snapshots previous-frame sums and starts a shared48-bit restoring division:48 cycles red, then48 cycles blue. Division truncates toward zero; clamp Q16 to32768..131072.
- Completed red/blue estimates are committed together only at a subsequent three-cycle-delayed statistics early. Each gain advances by floor(abs(target-current)/4); no neutral samples holds previous gain. First frames use unity65536.
- A busy divider does not restart at another early; stats for that frame still restart. early+valid includes its4 pixels in the new frame.

## 6. WaveDrom 时序图

### ball_white_balance calibration event order

Logical sequence only; frame intervals and96 division cycles are compressed. Not a measured timing waveform.

![ball_white_balance calibration event order](waveforms/ball_white_balance_compressed-event-order.svg)

- WaveJSON：[ball_white_balance_compressed-event-order.json5](waveforms/ball_white_balance_compressed-event-order.json5)

## 7. 边界、反压与错误

- Reset clears pending work and diagnostics; no fabricated readback success.
- No new video backpressure or external pins; count/tracking rules unchanged in this milestone.

## 8. CDC 与综合约束

- Same CSI clock; no video data/marker latency changes.
- 32-bit sums support full1280x720 at8-bit channels;22-bit sample count.

## 9. 验证与验收

- sim/tb_ball_calibration.v:15 exact Python integer vectors, all4 lanes, frame freeze, neutral rejection,64-sample threshold and valid gaps.

## 10. 可追溯性

- 规格模块：`ball_white_balance`
- RTL 路径：`rtl/ball_white_balance.v`
- 交付要求：本文档、WaveJSON 和 SVG 必须与同一版本规格一同发布。
