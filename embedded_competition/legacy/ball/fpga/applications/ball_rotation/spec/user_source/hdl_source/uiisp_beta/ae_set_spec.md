# ae_set 模块规范

> RTL: `user_source/hdl_source/uiisp_beta/ae_set.v`

## 1. 模块目的

接收长按事件并在I2C空闲时提交最新曝光和增益档位。

## 2. 参数

| 参数 | 默认值 | 说明 |
| --- | --- | --- |
| — | — | 本模块没有可配置参数。 |

## 3. 时钟与复位

- 时钟：`{"name": "I_clk", "edge": "posedge"}`
- 复位：`{"name": "I_rst", "active": "high", "synchronous": false}`

## 4. 接口信号规范

| 信号 | 方向 | 位宽 | 时钟域 | 语义角色 | 描述 |
| --- | --- | --- | --- | --- | --- |
| `I_clk` | input | 1 | I_clk | clock | 23.809524MHz reference |
| `I_rst` | input | 1 | I_clk | reset | Asynchronous high reset |
| `I_step` | input | 2 | I_clk | native | Asynchronous retained long-press toggles from board key controller;bit0 exposure,bit1 gain. |
| `I_ae_cfg_done` | input | 1 | I_clk | native | Previous AE write/read batch complete |
| `I_cam_cfg_done` | input | 1 | I_clk | native | Camera initialization complete |
| `O_ae_req` | output | 1 | I_clk | native | One-clock request; fields then held until complete |
| `O_ae` | output | 16 | I_clk | native | Requested exposure half-lines |
| `O_ag` | output | 16 | I_clk | native | Gain control for original SC520 table |

## 5. 周期行为与延迟

- Synchronize retained I_step through two I_clk registers, compare to consumed value, and step each profile once per changed bit. No physical N2/J14 button dependency.
- Exposure cycles1991,480,240,120; nominal60fps/VTS1000 correspond16.59,4,2,1ms. Display actual register ticks instead of claiming measured milliseconds.
- Gain control cycles144,176,80,112 corresponding16x,32x,4x,8x. Default remains1991/144. Reset output1990/17 intentionally triggers initial default application.
- Queue latest profiles while sensor is busy. Update AE/AG outputs and issue1-clock request only when initialization and prior transaction done; fields stay stable throughout transaction.

## 6. WaveDrom 时序图

### Long event into camera clock

Two synchronizers then consumed-event comparison; request follows decoded profile when camera idle.

![Long event into camera clock](waveforms/ae_set_toggle-cdc.svg)

- WaveJSON：[ae_set_toggle-cdc.json5](waveforms/ae_set_toggle-cdc.json5)

## 7. 边界、反压与错误

- Reset clears pending work and diagnostics; no fabricated readback success.
- No new video backpressure or external pins; count/tracking rules unchanged in this milestone.

## 8. CDC 与综合约束

- Only existing two camera pins are remapped; four application keys unchanged.
- Use calibration while conveyor is stopped; clear app history after changing camera settings.
- Same asynchronous reset asserted in source and receiver. Source toggles spaced about1second apart, far longer than synchronizer latency. I_step is an event toggle, not an active-low level.

## 9. 验证与验收

- sim/tb_ball_calibration.v:initial request,queued changes,long press,all exposure/gain wrap cases.
- tb_ball_board_keys with unrelated10ns video/14ns reference clocks; long release does not change app state.

## 10. 可追溯性

- 规格模块：`ae_set`
- RTL 路径：`user_source/hdl_source/uiisp_beta/ae_set.v`
- 交付要求：本文档、WaveJSON 和 SVG 必须与同一版本规格一同发布。
