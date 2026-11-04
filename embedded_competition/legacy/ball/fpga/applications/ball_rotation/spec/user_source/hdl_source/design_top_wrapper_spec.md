# design_top_wrapper 模块规范

> RTL: `user_source/hdl_source/design_top_wrapper.v`

## 1. 模块目的

保留实体接口和时钟，连接视频域按键事件与参考时钟域相机配置。

## 2. 参数

| 参数 | 默认值 | 说明 |
| --- | --- | --- |
| — | — | 本模块没有可配置参数。 |

## 3. 时钟与复位

- 时钟：`{"name": "I_sys_clk", "edge": "posedge"}`
- 复位：`{"name": "I_rst_n", "active": "low", "synchronous": false}`

## 4. 接口信号规范

| 信号 | 方向 | 位宽 | 时钟域 | 语义角色 | 描述 |
| --- | --- | --- | --- | --- | --- |
| `I_keys_n` | input | 4 | I_sys_clk | native | Retained board port; pin assignment unchanged |
| `I_sys_clk` | input | 1 | I_sys_clk | clock | Retained board port; pin assignment unchanged |
| `I_rst_n` | input | 1 | I_sys_clk | reset | Retained board port; pin assignment unchanged |
| `O_cam_scl` | output | 1 | I_sys_clk | native | Retained board port; pin assignment unchanged |
| `IO_cam_sda` | inout | 1 | I_sys_clk | native | Retained board port; pin assignment unchanged |
| `O_cam_24m` | output | 1 | I_sys_clk | native | Retained board port; pin assignment unchanged |
| `O_cam_rst` | output | 1 | I_sys_clk | native | Retained board port; pin assignment unchanged |
| `I_button` | inout | 2 | I_sys_clk | native | Retained board port; pin assignment unchanged |
| `O_screen_pwm` | output | 1 | I_sys_clk | native | Retained board port; pin assignment unchanged |
| `O_tmds_ch0_p` | output | 1 | I_sys_clk | native | Retained board port; pin assignment unchanged |
| `O_tmds_ch1_p` | output | 1 | I_sys_clk | native | Retained board port; pin assignment unchanged |
| `O_tmds_ch2_p` | output | 1 | I_sys_clk | native | Retained board port; pin assignment unchanged |
| `O_tmds_clk_p` | output | 1 | I_sys_clk | native | Retained board port; pin assignment unchanged |
| `IO_rx_clk_pad_n` | inout | 1 | I_sys_clk | native | Retained board port; pin assignment unchanged |
| `IO_rx_clk_pad_p` | inout | 1 | I_sys_clk | native | Retained board port; pin assignment unchanged |
| `IO_rx_data_pad_n` | inout | 4 | I_sys_clk | native | Retained board port; pin assignment unchanged |
| `IO_rx_data_pad_p` | inout | 4 | I_sys_clk | native | Retained board port; pin assignment unchanged |
| `ddr_addr` | output | 13 | I_sys_clk | native | Retained board port; pin assignment unchanged |
| `ddr_ba` | output | 2 | I_sys_clk | native | Retained board port; pin assignment unchanged |
| `ddr_cke` | output | 1 | I_sys_clk | native | Retained board port; pin assignment unchanged |
| `ddr_odt` | output | 1 | I_sys_clk | native | Retained board port; pin assignment unchanged |
| `ddr_cs_n` | output | 1 | I_sys_clk | native | Retained board port; pin assignment unchanged |
| `ddr_ras_n` | output | 1 | I_sys_clk | native | Retained board port; pin assignment unchanged |
| `ddr_cas_n` | output | 1 | I_sys_clk | native | Retained board port; pin assignment unchanged |
| `ddr_we_n` | output | 1 | I_sys_clk | native | Retained board port; pin assignment unchanged |
| `ddr_ck_p` | output | 1 | I_sys_clk | native | Retained board port; pin assignment unchanged |
| `ddr_ck_n` | output | 1 | I_sys_clk | native | Retained board port; pin assignment unchanged |
| `ddr_dm` | inout | 2 | I_sys_clk | native | Retained board port; pin assignment unchanged |
| `ddr_dq` | inout | 16 | I_sys_clk | native | Retained board port; pin assignment unchanged |
| `ddr_dqs_p` | inout | 2 | I_sys_clk | native | Retained board port; pin assignment unchanged |
| `ddr_dqs_n` | inout | 2 | I_sys_clk | native | Retained board port; pin assignment unchanged |

## 5. 周期行为与延迟

- All physical ports,pins,PLLs,DDR/MIPI/HDMI protocols unchanged.
- Connect six-register camera readback to reference-domain monitor and coherent video-domain status to ISP.
- Raw10 frame-start event,not HDMI vsync,feeds actual input-fps counting. Route board-key long event from runtime through ISP to ae_set camera-reference synchronizers. N2/J14 expansion GPIO remain unused; physical ports and constraints preserved.
- HDMI像素时钟域的S_video_out_vsync先经S_ddr_clk域两级寄存器S_dbg_frame_vsync_sync同步，再由第2级清理DDR读请求与读有效的调试粘滞标志；不再直接用异步HDMI电平控制DDR域调试寄存器。两级寄存器保持原S_video_out_rst_n异步低有效复位；只改变调试观测，视频/DDR传输接口不变。

## 6. WaveDrom 时序图

### design_top_wrapper calibration event order

Logical sequence only; frame intervals and96 division cycles are compressed. Not a measured timing waveform.

![design_top_wrapper calibration event order](waveforms/design_top_wrapper_compressed-event-order.svg)

- WaveJSON：[design_top_wrapper_compressed-event-order.json5](waveforms/design_top_wrapper_compressed-event-order.json5)

## 7. 边界、反压与错误

- Reset clears pending work and diagnostics; no fabricated readback success.
- No new video backpressure or external pins; count/tracking rules unchanged in this milestone.

## 8. CDC 与综合约束

- 原有ADC引脚约束保留。相机I²C主机改用pll_clk_24m正沿及rise/fall时钟使能，内部scl_clk仅为分频状态；SDC已删除cam_i2c_scl生成时钟，相关寄存器按42ns参考时钟检查。仅对两个已核实的FIFO时钟域对设置四条datapath-only最大延时预算，保留DDR IP灰码指针约束；实际约束覆盖与时序结论以本轮报告为准。
- Nominal23.809524MHz clock is the FPS time reference; actual oscillator tolerance is outside simulation.

## 9. 验证与验收

- Anlogic full-project synthesis/place-route and source/pin manifest.
- Component I2C,CDC,WB and complete720P application testbenches cover internal changes; no physical board programming performed by agent.

## 10. 可追溯性

- 规格模块：`design_top_wrapper`
- RTL 路径：`user_source/hdl_source/design_top_wrapper.v`
- 交付要求：本文档、WaveJSON 和 SVG 必须与同一版本规格一同发布。
