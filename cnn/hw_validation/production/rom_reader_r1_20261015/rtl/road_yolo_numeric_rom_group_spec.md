# road_yolo_numeric_rom_group 模块规范

> RTL: `road_yolo_numeric_rom_group.v`

## 1. 模块目的

Four 40-bit physical ROM lanes are captured into two 80-bit pair registers and concatenated directly for the enclosing reader.

## 2. 参数

| 参数 | 默认值 | 说明 |
| --- | --- | --- |
| C_LANE_ALPHA_FILE | NONE | Initialization file for bytes zero through four. |
| C_LANE_BETA_FILE | NONE | Initialization file for bytes five through nine. |
| C_LANE_GAMMA_FILE | NONE | Initialization file for bytes ten through fourteen. |
| C_LANE_DELTA_FILE | NONE | Initialization file for bytes fifteen through nineteen. |

## 3. 时钟与复位

- 时钟：`{"name": "i_clk", "edge": "posedge", "frequency_hz": 100000000}`
- 复位：`{"name": "i_rstn", "active": "low", "synchronous": false, "values": "reg_lower_pair and reg_upper_pair clear to zero; o_word_data is therefore zero."}`

## 4. 接口信号规范

| 信号 | 方向 | 位宽 | 时钟域 | 语义角色 | 描述 |
| --- | --- | --- | --- | --- | --- |
| `i_clk` | input | 1 | i_clk | clock | Physical ROM and pair-register clock. |
| `i_rstn` | input | 1 | i_clk | reset | Active-low asynchronous reset for both pair registers. |
| `i_word_addr` | input | 9 | i_clk | address | Shared address for the four 512-word physical ROM lanes. |
| `o_word_data` | output | 160 | i_clk | data | Direct concatenation of the registered upper and lower ten-byte pairs. |

## 5. 周期行为与延迟

- Each rising edge captures lane beta/alpha into reg_lower_pair and lane delta/gamma into reg_upper_pair.
- o_word_data continuously concatenates reg_upper_pair above reg_lower_pair without a second 160-bit register stage.
- The group-visible data change is one clock earlier than the frozen baseline group; this candidate is valid only inside road_numeric_rom_reader, which still samples at cnt_wait equal to seven.

## 6. WaveDrom 时序图

### Single registered pair boundary

After the physical lane outputs are available, one rising edge updates both pair registers and the concatenated group output changes in the same cycle. The enclosing reader samples later at its unchanged cnt_wait value of seven.

![Single registered pair boundary](waveforms/road_yolo_numeric_rom_group_pair-capture.svg)

- WaveJSON：[road_yolo_numeric_rom_group_pair-capture.json5](waveforms/road_yolo_numeric_rom_group_pair-capture.json5)

## 7. 边界、反压与错误

- Reset during a read clears both pair registers and immediately drives the concatenated output to zero.
- The enclosing reader must retain enough fixed wait cycles to absorb the shorter group latency.
- Addresses outside the fourteen-group reader range remain rejected by the reader and never reach a fabricated group completion.

## 8. CDC 与综合约束

- The four PH1P_LOGIC_ERAM instances, initialization files, widths, addresses, ports and pair-register reset behavior are unchanged.
- No reader wait, request/response handshake, numeric content, arithmetic kernel, initiation interval or timing exception is changed.
- The structural declaration delta is 160 register bits per group and 2240 bits for fourteen instances; it is not a measured Slice result.

## 9. 验证与验收

- Baseline and ROM-R1 reader external traces match cycle by cycle for all 7168 legal words.
- All fourteen group first and last words, long response backpressure, WAIT reset, RESPONSE reset, address 7167 and invalid address 7168 are checked.
- Original tb_rom_reader, tb_parameter_prefetch and tb_rom_down2 regressions are rerun against the candidate closure.

## 10. 可追溯性

- 规格模块：`road_yolo_numeric_rom_group`
- RTL 路径：`road_yolo_numeric_rom_group.v`
- 交付要求：本文档、WaveJSON 和 SVG 必须与同一版本规格一同发布。
