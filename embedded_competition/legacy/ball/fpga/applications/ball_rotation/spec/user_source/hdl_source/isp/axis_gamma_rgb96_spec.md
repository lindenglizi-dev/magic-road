# axis_gamma_rgb96 模块规范

> RTL: `user_source/hdl_source/isp/isp_top.v`

## 1. 模块目的

在AWB与小球应用之间对四像素RGB888流作统一gamma亮度曲线处理，提升暗部，并保持像素、有效及提前帧通知的一拍对应关系。

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
| `I_clk` | input | 1 | I_clk | clock | same pixel-group clock as the AWB and application stream |
| `I_rst_n` | input | 1 | I_clk | reset | asynchronous active-low reset clears all output registers |
| `I_tlast` | input | 1 | I_clk | native | upstream line-end notification; delayed by one clock |
| `I_tuser` | input | 1 | I_clk | native | advance frame notification independent of valid; delayed by one clock |
| `I_tdata` | input | 96 | I_clk | native | four RGB888 pixels, twelve independent8-bit channels; leftmost pixel in95:72 |
| `I_tvalid` | input | 1 | I_clk | native | valid four-pixel group; no ready/backpressure input |
| `O_tlast` | output | 1 | I_clk | native | one-clock-delayed I_tlast |
| `O_tuser` | output | 1 | I_clk | native | one-clock-delayed advance I_tuser; retains lead over valid pixels |
| `O_tdata` | output | 96 | I_clk | native | four gamma-corrected RGB888 pixels in the unchanged lane/channel order; zero for invalid cycles |
| `O_tvalid` | output | 1 | I_clk | native | one-clock-delayed I_tvalid |

## 5. 周期行为与延迟

- For each valid input group transform all twelve8-bit channels independently with the existing16-segment piecewise-linear approximation to255*(x/255)^0.7.
- The upper nibble selects base and delta; output is base+((delta*lower_nibble+8)>>4), with explicit255 endpoint. The curve is monotonic, preserves0/255, and lifts shadows/midtones (16->37,64->97,128->157).
- Every clock delays valid, early and last by one registered cycle. Data is transformed when input valid is high and set to zero otherwise. Asynchronous reset clears data and all marker registers.
- The module does not add or remove groups and does not reinterpret early as pixel SOF; isp_top places this stage before both detection and display.

## 6. WaveDrom 时序图

### axis_gamma_rgb96 registered stream event order

Logical RTL register relationship only; not a measured waveform. Early is independent of valid. The drawing illustrates one gamma register stage and intentionally omits the sensor/demosaic/AWB lead interval.

![axis_gamma_rgb96 registered stream event order](waveforms/axis_gamma_rgb96_logical-one-stage.svg)

- WaveJSON：[axis_gamma_rgb96_logical-one-stage.json5](waveforms/axis_gamma_rgb96_logical-one-stage.json5)

## 7. 边界、反压与错误

- Invalid cycles carry zero output data while markers continue with one-clock delay.
- An advance early pulse may occur while valid is low; it must retain its original lead relative to delayed pixel data.
- All8-bit inputs including0,15/16 segment boundaries,254 and255 retain the same channel and pixel lane.

## 8. CDC 与综合约束

- Synthesizable Verilog-2001; existing module shares isp_top.v; no additional source-file reference is required.
- Synchronous pixel-group domain; twelve parallel channel transforms sustain four RGB888 pixels per clock. No ready/backpressure interface.
- One registered stage is RTL latency, not measured routing delay. Perceived image brightness and real camera exposure still require board verification.

## 9. 验证与验收

- sim/tb_ball_lowlight.v: sweep all256 input levels through actual gamma RTL, check endpoints/monotonicity/shadow lift, mixed channel lanes and independently delayed early/last/valid.
- sim/tb_ball_lowlight.v: actual gamma plus full runtime with shadedradius85-pixel (171-pixel bounding extent) red/yellow/green balls, cyan background and bright highlights.
- sim/tb_ball_hdmi_lowlight.v: four full720P frames and actual packed display capture; this is simulation evidence, not physical sensor/DDR/HDMI evidence.

## 10. 可追溯性

- 规格模块：`axis_gamma_rgb96`
- RTL 路径：`user_source/hdl_source/isp/isp_top.v`
- 交付要求：本文档、WaveJSON 和 SVG 必须与同一版本规格一同发布。
