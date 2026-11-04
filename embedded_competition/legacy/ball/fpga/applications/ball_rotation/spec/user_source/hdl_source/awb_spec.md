# awb 模块规范

> RTL: `user_source/hdl_source/awb.v`

## 1. 模块目的

未提供模块目的。

## 2. 参数

| 参数 | 默认值 | 说明 |
| --- | --- | --- |
| — | — | 本模块没有可配置参数。 |

## 3. 时钟与复位

- 时钟：`{"name": "I_clk", "edge": "posedge"}`
- 复位：`{"name": "I_rst_n", "active": "low", "synchronous": false}`

## 4. 接口信号规范

| 信号 | 方向 | 位宽 | 时钟域 | 语义角色 | 描述 |
| --- | --- | --- | --- | --- | --- |
| `I_clk` | input | 1 | I_clk | clock | CSI clock |
| `I_rst_n` | input | 1 | I_clk | reset | Active-low reset |
| `I_tlast` | input | 1 | I_clk | native | Legacy input end-of-line |
| `I_tuser` | input | 1 | I_clk | native | Advance frame notification |
| `I_tdata` | input | 96 | I_clk | native | Four RGB888 pixels |
| `I_tvalid` | input | 1 | I_clk | native | Input group valid |
| `I_tready` | output | 1 | I_clk | native | Retained ready forwarding |
| `O_tlast` | output | 1 | I_clk | native | Original regenerated output line tail |
| `O_tuser` | output | 1 | I_clk | native | Direct original early notification |
| `O_tdata` | output | 96 | I_clk | native | Original Q16 saturated per-lane gain output |
| `O_tvalid` | output | 1 | I_clk | native | Original delayed group valid |
| `O_tready` | input | 1 | I_clk | native | Retained ready input |
| `O_wb_ready` | output | 1 | I_clk | native | Neutral WB estimate has been committed |

## 5. 周期行为与延迟

- Original input-register block,signal_delay instance with50-cycle setting,post-register/multiply/output section are retained as exact LF-normalized text; see reports/awb_preserved_sections.json.
- Replace prefix-gray-world streaming divider gains with ball_white_balance. Preserve all video byte ordering,original saturation,valid generation,line tail and direct early forwarding.
- All gains are constant between early boundaries. First neutral estimate takes up to two subsequent frame boundaries; no neutral samples preserves existing gains.

## 6. WaveDrom 时序图

### awb calibration event order

Logical sequence only; frame intervals and96 division cycles are compressed. Not a measured timing waveform.

![awb calibration event order](waveforms/awb_compressed-event-order.svg)

- WaveJSON：[awb_compressed-event-order.json5](waveforms/awb_compressed-event-order.json5)

## 7. 边界、反压与错误

- Reset clears pending work and diagnostics; no fabricated readback success.
- No new video backpressure or external pins; count/tracking rules unchanged in this milestone.

## 8. CDC 与综合约束

- Fullboard width1280,height720. Retain original signal_delay width/line blanking requirements.
- Do not replace early with pixel-aligned SOF.

## 9. 验证与验收

- sim/tb_ball_calibration.v verifies actual gain controller.
- sim/tb_ball_awb.v is provided for a vendor-compatible simulator; local Icarus cannot read encrypted PH1P_LOGIC_ERAM model. This test is NOT reported as passed.
- Native full-project Anlogic elaboration/synthesis verifies actual retained RAM binding.

## 10. 可追溯性

- 规格模块：`awb`
- RTL 路径：`user_source/hdl_source/awb.v`
- 交付要求：本文档、WaveJSON 和 SVG 必须与同一版本规格一同发布。
