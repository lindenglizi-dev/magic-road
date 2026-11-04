# ball_stream_front 模块规范

> RTL: `rtl/ball_stream_front.v`

## 1. 模块目的

两拍RGB前端：强弱颜色判定及水平四像素支持；只在valid推进坐标。

## 2. 参数

| 参数 | 默认值 | 说明 |
| --- | --- | --- |
| C_WIDTH | 1280 | 原图像尺寸及ROI/计数门范围；端点使用原有半开区间语义。 |
| C_HEIGHT | 720 | 原图像尺寸及ROI/计数门范围；端点使用原有半开区间语义。 |
| C_X_MIN | 64 | 原图像尺寸及ROI/计数门范围；端点使用原有半开区间语义。 |
| C_Y_MIN | 160 | 原图像尺寸及ROI/计数门范围；端点使用原有半开区间语义。 |
| C_X_END | 1216 | 原图像尺寸及ROI/计数门范围；端点使用原有半开区间语义。 |
| C_Y_END | 640 | 原图像尺寸及ROI/计数门范围；端点使用原有半开区间语义。 |
| C_GATE_MIN | 544 | 原图像尺寸及ROI/计数门范围；端点使用原有半开区间语义。 |
| C_GATE_END | 736 | 原图像尺寸及ROI/计数门范围；端点使用原有半开区间语义。 |

## 3. 时钟与复位

- 时钟：`{"name": "i_clk", "edge": "posedge"}`
- 复位：`{"name": "i_rstn", "active": "low", "synchronous": false}`

## 4. 接口信号规范

| 信号 | 方向 | 位宽 | 时钟域 | 语义角色 | 描述 |
| --- | --- | --- | --- | --- | --- |
| `i_clk` | input | 1 | i_clk | clock | AWB pixel-group clock, same S_csi_rx_clk domain |
| `i_rstn` | input | 1 | i_clk | reset | asynchronous active-low reset |
| `i_rgb` | input | (95)-(0)+1 | i_clk | native | four gamma-corrected RGB888 pixels; leftmost pixel in bits95:72 |
| `i_valid` | input | 1 | i_clk | native | valid pixel group or candidate pulse; no video backpressure |
| `i_early` | input | 1 | i_clk | native | early frame notification independent of pixel valid |
| `i_strict` | input | 1 | i_clk | native | strict: brightness150 and channel gap50; normal: gamma-domain brightness64, gap12 and 5:4 relative channel dominance |
| `i_epoch` | input | (15)-(0)+1 | i_clk | native | configuration generation captured with frame statistics |
| `o_rgb` | output | (95)-(0)+1 | i_clk | native | four gamma-corrected RGB888 pixels; leftmost pixel in bits95:72 |
| `o_valid` | output | 1 | i_clk | native | valid pixel group or candidate pulse; no video backpressure |
| `o_sof` | output | 1 | i_clk | native | first valid group of a frame |
| `o_eol` | output | 1 | i_clk | native | last valid group of a line |
| `o_eof` | output | 1 | i_clk | native | last valid group of a frame |
| `o_x` | output | (11)-(0)+1 | i_clk | native | Native application interface field o_x; see module behavior and source connections |
| `o_y` | output | (11)-(0)+1 | i_clk | native | Native application interface field o_y; see module behavior and source connections |
| `o_labels` | output | (7)-(0)+1 | i_clk | native | four exclusive two-bit labels, lane zero in bits 1:0; 0 unknown,1 red,2 yellow,3 green |
| `o_gate_hits` | output | (2)-(0)+1 | i_clk | native | Native application interface field o_gate_hits; see module behavior and source connections |
| `o_epoch` | output | (15)-(0)+1 | i_clk | native | configuration generation captured with frame statistics |
| `o_error` | output | 1 | i_clk | native | sticky video/statistics protocol diagnostic |

## 5. 周期行为与延迟

- At first edge capture original RGB, coordinates, strong and weak labels, strict flag and epoch. Strong normal classification remains floor64,difference12,5:4dominance. Weak candidates use floor32,difference6,9:8dominance; yellow red/green balance remains5:4.
- At second edge, in normal mode preserve a strong-color pixel only if at least2of4lanes share that strong color; otherwise preserve a weak-color pixel if at least3of4lanes share that weak color. Strong label takes priority. Strict mode bypasses support and retains old strict classifier.
- RGB,valid,SOF,EOL,EOF,coordinates,epoch and recomputed gate occupancy share the same2registered cycles. Input early still resets input position; actual SOF remains pixel-aligned. No clock or external port changes.

## 6. WaveDrom 时序图

### Color classification and support pipeline

Cycle markers and RGB are delayed with labels. Runtime advance early remains independent and unchanged.

![Color classification and support pipeline](waveforms/ball_stream_front_two-stage-front.svg)

- WaveJSON：[ball_stream_front_two-stage-front.json5](waveforms/ball_stream_front_two-stage-front.json5)

## 7. 边界、反压与错误

- Reset or configuration change has priority over old results.
- Video invalid cycles must not advance pixel coordinates or packer phase.
- Conveyor V1 requires disjoint X projections, one ball per gate and three clear gate frames.
- Isolated strong foreground pixel in a neutral group must not contaminate bounds; three dark same-color lanes may pass; strict bypass supports isolated strict pixels.

## 8. CDC 与综合约束

- Synthesizable Verilog-2001; Anlogic PH1P35MDG324/-3.
- W is a multiple of16; projection Y coordinates are10bit, so H<=1023. Default1280x720.
- No video ready/backpressure or frame-dropping substitution; detector faults do not alter video byte count.
- Horizontal support is limited to original four-pixel aligned groups; it does not provide vertical connected components or separate dense same-X background.
- Filtered circle tips or a lone group-edge pixel can be removed; tested geometry center shift at most1pixel on legacy reference scenes. Very thin fragments may disappear.

## 9. 验证与验收

- sim/tb_ball_core.v:147-plus frames with split/hold100/dropout2/last column/BCD and byte ordering.
- sim/tb_ball_runtime.v:28 frames with boundary commits and late-result rejection.
- sim/tb_ball_hdmi.v:four complete720P frames and actual DDR capture.
- sim/tb_ball_lowlight.v: object-geometry ground truth verifies low-light labels including shaded ball interiors, highlight exclusion and textured cyan rejection.
- tb_ball_color_support compares2048independent Python group vectors and2clock metadata latency.
- tb_ball_dark_noise sends9RGB frames covering3bright balls and3colors x2dark/noise cases into actual front+projection.
- Updated28frame runtime,9frame shaded-color regression,4frame720P capture.

## 10. 可追溯性

- 规格模块：`ball_stream_front`
- RTL 路径：`rtl/ball_stream_front.v`
- 交付要求：本文档、WaveJSON 和 SVG 必须与同一版本规格一同发布。
