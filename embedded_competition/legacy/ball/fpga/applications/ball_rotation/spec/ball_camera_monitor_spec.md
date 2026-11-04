# ball_camera_monitor 模块规范

> RTL: `rtl/ball_camera_monitor.v`

## 1. 模块目的

未提供模块目的。

## 2. 参数

| 参数 | 默认值 | 说明 |
| --- | --- | --- |
| — | — | 本模块没有可配置参数。 |

## 3. 时钟与复位

- 时钟：`{"name": "i_ref_clk", "edge": "posedge"}`
- 复位：`{"name": "i_rstn", "active": "low", "synchronous": false}`

## 4. 接口信号规范

| 信号 | 方向 | 位宽 | 时钟域 | 语义角色 | 描述 |
| --- | --- | --- | --- | --- | --- |
| `i_ref_clk` | input | 1 | i_ref_clk | clock | 23.809524MHz nominal reference |
| `i_video_clk` | input | 1 | i_ref_clk | clock | CSI byte clock |
| `i_rstn` | input | 1 | i_ref_clk | reset | Common asynchronous reset |
| `i_frame` | input | 1 | i_video_clk | native | One CSI/raw frame-start pulse per actual input frame |
| `i_cfg_done` | input | 1 | i_ref_clk | native | Sensor initialization complete |
| `i_read_valid` | input | 1 | i_ref_clk | native | Completed six-register readback batch |
| `i_read_match` | input | 1 | i_ref_clk | native | Readback matched accepted AE/AG snapshot |
| `i_bus_error` | input | 1 | i_ref_clk | native | Sticky I2C bus error |
| `i_read_exposure` | input | 16 | i_ref_clk | native | Read exposure half-line count |
| `i_read_gain` | input | 24 | i_ref_clk | native | Read3e09/3e06/3e07 register bytes |
| `o_status` | output | 48 | i_video_clk | native | Coherent video-domain status snapshot |

## 5. 周期行为与延迟

- A video-domain toggle crosses2 reference synchronizers. Count real frame events over C_REF_CYCLES=23809524 reference cycles; report3-digit BCD fps, including an event on the window boundary.
- Convert read exposure to4-digit BCD using existing16-cycle decimal formatter. Do not report RB1/2 until its conversion completes. Gain display recognizes exact4x/8x/16x/32x known register presets.
- RB0=pending,1=read match,2=read mismatch,3=bus error. FPS is an input measurement against nominal reference, not HDMI refresh or exposure measurement.
- Hold a48-bit source bus stable until a request/ack toggle round trip. Destination waits2 synchronizers plus1 settle cycle before sampling and acknowledging; source cannot overwrite unacknowledged data.
- Status bits11:0 FPS,27:12 EXP,35:28 gain,37:36 RB,38 cfg. ISP supplies WB-ready at39. Runtime freezes the coherent bus at frame boundary.

## 6. WaveDrom 时序图

### ball_camera_monitor calibration event order

Logical sequence only; frame intervals and96 division cycles are compressed. Not a measured timing waveform.

![ball_camera_monitor calibration event order](waveforms/ball_camera_monitor_compressed-event-order.svg)

- WaveJSON：[ball_camera_monitor_compressed-event-order.json5](waveforms/ball_camera_monitor_compressed-event-order.json5)

## 7. 边界、反压与错误

- Reset clears pending work and diagnostics; no fabricated readback success.
- No new video backpressure or external pins; count/tracking rules unchanged in this milestone.

## 8. CDC 与综合约束

- Source/destination share reset; source data is a held bundled-data handshake, not independent bit synchronizers.
- Input frame-event spacing must exceed the reference synchronizer sampling interval.

## 9. 验证与验收

- sim/tb_ball_camera_monitor.v:unrelated clocks,7/0 frame events,read formatting,CDC and mismatch/error states.

## 10. 可追溯性

- 规格模块：`ball_camera_monitor`
- RTL 路径：`rtl/ball_camera_monitor.v`
- 交付要求：本文档、WaveJSON 和 SVG 必须与同一版本规格一同发布。
