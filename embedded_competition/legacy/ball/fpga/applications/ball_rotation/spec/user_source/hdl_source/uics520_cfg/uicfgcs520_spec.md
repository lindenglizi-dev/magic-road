# uicfgcs520 模块规范

> RTL: `user_source/hdl_source/uics520_cfg/uicfgcs520.v`

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
| `I_clk` | input | 1 | I_clk | clock | Reference clock |
| `I_rst_n` | input | 1 | I_clk | reset | Delayed camera power-up reset |
| `I_ae_req` | input | 1 | I_clk | native | Accept AE request only in idle |
| `I_ae` | input | 16 | I_clk | native | Requested exposure snapshot |
| `I_ag` | input | 16 | I_clk | native | Gain-table control snapshot |
| `O_cam_scl` | output | 1 | I_clk | native | Original I2C clock |
| `IO_cam_sda` | inout | 1 | I_clk | native | Original open-drain SDA |
| `O_cfg_done` | output | 1 | I_clk | native | Factory initialization complete |
| `O_ae_cfg_done` | output | 1 | I_clk | native | AE write and readback complete |
| `O_sensor_id` | output | 16 | I_clk | native | Read3107/3108 ID |
| `O_sensor_id_ok` | output | 1 | I_clk | native | Acceptedee4b/9e4b ID |
| `O_iic_error` | output | 1 | I_clk | native | Sticky bus ACK error |
| `O_read_exposure` | output | 16 | I_clk | native | Assembled3e00/01/02 exposure |
| `O_read_gain` | output | 24 | I_clk | native | Assembled3e09/06/07 gain |
| `O_read_valid` | output | 1 | I_clk | native | Readback batch completed |
| `O_read_match` | output | 1 | I_clk | native | Read values match snapshot without transaction fault |

## 5. 周期行为与延迟

- Original sensor ID,initialization table,5ms reset delay,group-hold write table and actual uii2c master are retained.
- At accepted AE request snapshot exposure and converted gain bytes; use snapshots for the full grouped write transaction.
- After group release wait READ_WAIT_CYCLES=952381 reference clocks, nominal40ms, before six-register readback. Test delays sensor read visibility and proves omitting wait falsely mismatches. This is a conservative settling interval for the fixed720p60 mode, not a claim about undocumented sensor internals.
- After8 AE table writes, read3e00,3e01,3e02,3e09,3e06,3e07 via actual repeated-start I2C reads. Assembled exposure uses only documented programmed bit fields.
- O_ae_cfg_done stays low until all6 reads complete. Compare the final newly received gain byte together with prior bytes; mismatch must not report match.
- A bus error is sticky and prevents this batch from matching; RB telemetry also reports bus error. No new sensor register addresses are written.

### I²C主时钟与接单契约

- uii2c的5个原派生时钟过程改为I_clk正沿加scl_rise_ce/scl_fall_ce；分频器和SCL输出OFFSET不变，scl_clk只作数据状态，不驱动寄存器时钟。所有触发器使用42ns的I_clk参考时钟。
- 实际实例CLK_DIV=237：SCL_DIV=118，每119个I_clk周期翻转一次，完整采样周期238拍；23.809524MHz/238约为100.040kHz，保持原采样与输出相位。既有异步低有效复位分支优先于时钟使能。
- 若请求恰好由同一参考时钟上升沿产生，非阻塞赋值使主机可在下一次rise使能才接单，相比旧派生时钟实现最多晚一个I²C周期，约9.996微秒；调用方应保持请求直到busy响应。写字节、ACK/NACK、读回及repeated-start协议保持原约定。

## 6. WaveDrom 时序图

### uicfgcs520 calibration event order

Logical sequence only; frame intervals and96 division cycles are compressed. Not a measured timing waveform.

![uicfgcs520 calibration event order](waveforms/uicfgcs520_compressed-event-order.svg)

- WaveJSON：[uicfgcs520_compressed-event-order.json5](waveforms/uicfgcs520_compressed-event-order.json5)

## 7. 边界、反压与错误

- Reset clears pending work and diagnostics; no fabricated readback success.
- No new video backpressure or external pins; count/tracking rules unchanged in this milestone.

## 8. CDC 与综合约束

- I_ae_req is a1-cycle pulse while done; no requests accepted while busy.
- RB match proves register read/write agreement, not actual optical exposure/brightness.
- READ_WAIT_CYCLES must be1..1048576 for its20-bit counter.

## 9. 验证与验收

- sim/tb_ball_camera_i2c.v:actual uii2c and open-drain byte BFM,ID/table,5 exposure/gain requests,read mismatch,recovery and injected address NACK.
- No-settle negative control compiles0 and sim exits1 at default readback check; positive wait passes.

## 10. 可追溯性

- 规格模块：`uicfgcs520`
- RTL 路径：`user_source/hdl_source/uics520_cfg/uicfgcs520.v`
- 交付要求：本文档、WaveJSON 和 SVG 必须与同一版本规格一同发布。
