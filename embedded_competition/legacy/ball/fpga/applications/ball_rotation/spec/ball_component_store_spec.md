# ball_component_store 模块规范

> RTL: `rtl/ball_component_store.v`

## 1. 模块目的

按使能同步读写的参数化ERAM推断存储，复用于单元、行统计和队列。

## 2. 参数

| 参数 | 默认值 | 说明 |
| --- | --- | --- |
| — | — | 本模块没有可配置参数。 |

## 3. 时钟与复位

- 时钟：`{"name": "i_clk", "edge": "posedge"}`
- 复位：`{"name": "no memory reset", "active": "none", "synchronous": false}`

## 4. 接口信号规范

| 信号 | 方向 | 位宽 | 时钟域 | 语义角色 | 描述 |
| --- | --- | --- | --- | --- | --- |
| `i_clk` | input | 1 | i_clk | clock | AWB pixel-group clock, same S_csi_rx_clk domain |
| `i_read_enable` | input | 1 | i_clk | native | perform one synchronous column-memory read |
| `i_read_address` | input | (C_ADDR_BITS-1)-(0)+1 | i_clk | native | column group address selected within one lane/frame bank |
| `i_write_enable` | input | 1 | i_clk | native | perform one synchronous column-memory write |
| `i_write_address` | input | (C_ADDR_BITS-1)-(0)+1 | i_clk | native | address delayed from the accepted capture read |
| `i_write_data` | input | C_DATA_BITS | i_clk | native | Parameterized stored word |
| `o_read_data` | output | C_DATA_BITS | i_clk | native | Parameterized stored word |

## 5. 周期行为与延迟

- One enabled synchronous read and independent enabled write; read output is registered. No memory-array reset.
- Caller establishes initialized entries by capture overwrite or queue push before read. Same-address read/write is not used as write-through evidence.

## 6. WaveDrom 时序图

### Synchronous memory event order

Logical event order only. Internal multi-cycle/frame intervals are compressed; exact latency is specified in behavior, not inferred from this sketch.

![Synchronous memory event order](waveforms/ball_component_store_compressed-event-sequence.svg)

- WaveJSON：[ball_component_store_compressed-event-sequence.json5](waveforms/ball_component_store_compressed-event-sequence.json5)

## 7. 边界、反压与错误

- Disabled read holds prior output. Contents/read output are unspecified until initialized; callers must not consume them early.

## 8. CDC 与综合约束

- C_DEPTH>=1, C_DATA_BITS>=1, C_DEPTH<=2^C_ADDR_BITS. Native Anlogic inference must be checked in actual synthesis reports.

## 9. 验证与验收

- Actual detector tests exercise all RAM roles, valid bubbles, frame reuse and queue wrap/overflow.

## 10. 可追溯性

- 规格模块：`ball_component_store`
- RTL 路径：`rtl/ball_component_store.v`
- 交付要求：本文档、WaveJSON 和 SVG 必须与同一版本规格一同发布。
