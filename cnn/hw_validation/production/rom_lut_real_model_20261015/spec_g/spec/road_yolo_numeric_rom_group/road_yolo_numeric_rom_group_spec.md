# road_yolo_numeric_rom_group 模块规范

> RTL: `rtl/road_yolo_numeric_rom_group.v`

## 1. 模块目的

未提供模块目的。

## 2. 参数

| 参数 | 默认值 | 说明 |
| --- | --- | --- |
| C_LANE_ALPHA_FILE | NONE |  |
| C_LANE_BETA_FILE | NONE |  |
| C_LANE_GAMMA_FILE | NONE |  |
| C_LANE_DELTA_FILE | NONE |  |

## 3. 时钟与复位

- 时钟：`{"name": "i_clk", "frequency_hz": 100000000}`
- 复位：`{"name": "i_rstn", "assert": "async_low", "release": "Existing asynchronous pair-register reset; vendor ERAM contents are initialization data, not array-reset"}`

## 4. 接口信号规范

| 信号 | 方向 | 位宽 | 时钟域 | 语义角色 | 描述 |
| --- | --- | --- | --- | --- | --- |
| `i_clk` | input | 1 | i_clk | clk | 统一100MHz上升沿时钟 |
| `i_rstn` | input | 1 | i_clk | rstn | 共同低有效异步复位，本地两级同步释放 |
| `i_word_addr` | input | 9 | i_clk | word_addr | word_addr：按requirements中对应事务/计数合同使用 |
| `o_word_data` | output | 160 | i_clk | word_data | word_data：按requirements中对应事务/计数合同使用 |

## 5. 周期行为与延迟

- 原R1四个PH1P_LOGIC_ERAM输出40位lane；低/高各80位寄存拼接后直接连160位输出。
- 不恢复已删除的第二级160位寄存器，不推进R2；初始化参数由reader固定14组路径选择。
- 实测由真实PH1P厂商模型执行；文档不证明实际Slice、ERAM映射或时序。

## 6. WaveDrom 时序图

### 请求所有权与停顿

协议示意：省略内部变长计算，用空白间隔表示；不是固定总时延。仅valid与ready同拍消费。

![请求所有权与停顿](waveforms/road_yolo_numeric_rom_group_request-hold-response.svg)

- WaveJSON：[road_yolo_numeric_rom_group_request-hold-response.json5](waveforms/road_yolo_numeric_rom_group_request-hold-response.json5)

## 7. 边界、反压与错误

- 复位、取消、背压、非法身份和边界地址；取消不能当成无标签外设已排空

## 8. CDC 与综合约束

- Verilog-2001；一个未决事务；ready/valid握手；无TD/物理时序签核
- 不改变冻结算术核/数值，不复制公共存储

## 9. 验证与验收

- 11数值向量、protocol、phase_reset，逐项DECODED160对拍

## 10. 可追溯性

- 规格模块：`road_yolo_numeric_rom_group`
- RTL 路径：`rtl/road_yolo_numeric_rom_group.v`
- 交付要求：本文档、WaveJSON 和 SVG 必须与同一版本规格一同发布。
