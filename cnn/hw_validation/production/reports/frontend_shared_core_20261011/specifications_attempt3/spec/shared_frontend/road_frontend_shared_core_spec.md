# road_frontend_shared_core 模块规范

> RTL: `road_frontend_shared_core.v`

## 1. 模块目的

冻结Stem/down2调度对唯一MAC及动态后处理的互斥共享，不含DDR和整帧存储。

## 2. 参数

| 参数 | 默认值 | 说明 |
| --- | --- | --- |
| — | — | 本模块没有可配置参数。 |

## 3. 时钟与复位

- 时钟：`{"name": "i_clk", "edge": "posedge", "frequency_hz": 100000000}`
- 复位：`{"name": "i_rstn", "active": "low", "synchronous": false, "values": "立即取消在途及所有loaded状态；调用者同步释放；重新装满1024项表与参数。"}`

## 4. 接口信号规范

| 信号 | 方向 | 位宽 | 时钟域 | 语义角色 | 描述 |
| --- | --- | --- | --- | --- | --- |
| `i_clk` | input | 1 | i_clk | i_clk | 单时钟固定前端接口；有效负载保持到ready，完整表和参数后才能计算；复位立即取消。 |
| `i_rstn` | input | 1 | i_clk | i_rstn | 单时钟固定前端接口；有效负载保持到ready，完整表和参数后才能计算；复位立即取消。 |
| `i_select_valid` | input | 1 | i_clk | i_select_valid | 单时钟固定前端接口；有效负载保持到ready，完整表和参数后才能计算；复位立即取消。 |
| `i_select_down2` | input | 1 | i_clk | i_select_down2 | 单时钟固定前端接口；有效负载保持到ready，完整表和参数后才能计算；复位立即取消。 |
| `o_select_ready` | output | 1 | i_clk | o_select_ready | 单时钟固定前端接口；有效负载保持到ready，完整表和参数后才能计算；复位立即取消。 |
| `o_selected_down2` | output | 1 | i_clk | o_selected_down2 | 单时钟固定前端接口；有效负载保持到ready，完整表和参数后才能计算；复位立即取消。 |
| `i_table_valid` | input | 1 | i_clk | i_table_valid | 单时钟固定前端接口；有效负载保持到ready，完整表和参数后才能计算；复位立即取消。 |
| `i_table_addr` | input | 10 | i_clk | i_table_addr | 单时钟固定前端接口；有效负载保持到ready，完整表和参数后才能计算；复位立即取消。 |
| `i_table_data` | input | 16 | i_clk | i_table_data | 单时钟固定前端接口；有效负载保持到ready，完整表和参数后才能计算；复位立即取消。 |
| `o_table_ready` | output | 1 | i_clk | o_table_ready | 单时钟固定前端接口；有效负载保持到ready，完整表和参数后才能计算；复位立即取消。 |
| `o_table_loaded` | output | 1 | i_clk | o_table_loaded | 单时钟固定前端接口；有效负载保持到ready，完整表和参数后才能计算；复位立即取消。 |
| `o_table_fault` | output | 1 | i_clk | o_table_fault | 单时钟固定前端接口；有效负载保持到ready，完整表和参数后才能计算；复位立即取消。 |
| `i_load_valid` | input | 1 | i_clk | i_load_valid | 单时钟固定前端接口；有效负载保持到ready，完整表和参数后才能计算；复位立即取消。 |
| `i_load_kind` | input | 3 | i_clk | i_load_kind | 单时钟固定前端接口；有效负载保持到ready，完整表和参数后才能计算；复位立即取消。 |
| `i_load_addr` | input | 11 | i_clk | i_load_addr | 单时钟固定前端接口；有效负载保持到ready，完整表和参数后才能计算；复位立即取消。 |
| `i_load_data` | input | 32 | i_clk | i_load_data | 单时钟固定前端接口；有效负载保持到ready，完整表和参数后才能计算；复位立即取消。 |
| `o_load_ready` | output | 1 | i_clk | o_load_ready | 单时钟固定前端接口；有效负载保持到ready，完整表和参数后才能计算；复位立即取消。 |
| `i_start` | input | 1 | i_clk | i_start | 单时钟固定前端接口；有效负载保持到ready，完整表和参数后才能计算；复位立即取消。 |
| `i_commit_ready` | input | 1 | i_clk | i_commit_ready | 单时钟固定前端接口；有效负载保持到ready，完整表和参数后才能计算；复位立即取消。 |
| `o_busy` | output | 1 | i_clk | o_busy | 单时钟固定前端接口；有效负载保持到ready，完整表和参数后才能计算；复位立即取消。 |
| `o_done` | output | 1 | i_clk | o_done | 单时钟固定前端接口；有效负载保持到ready，完整表和参数后才能计算；复位立即取消。 |
| `o_fault` | output | 1 | i_clk | o_fault | 单时钟固定前端接口；有效负载保持到ready，完整表和参数后才能计算；复位立即取消。 |
| `o_core_cycles` | output | 32 | i_clk | o_core_cycles | 单时钟固定前端接口；有效负载保持到ready，完整表和参数后才能计算；复位立即取消。 |
| `i_export_start` | input | 1 | i_clk | i_export_start | 单时钟固定前端接口；有效负载保持到ready，完整表和参数后才能计算；复位立即取消。 |
| `i_output_ready` | input | 1 | i_clk | i_output_ready | 单时钟固定前端接口；有效负载保持到ready，完整表和参数后才能计算；复位立即取消。 |
| `o_output_valid` | output | 1 | i_clk | o_output_valid | 单时钟固定前端接口；有效负载保持到ready，完整表和参数后才能计算；复位立即取消。 |
| `o_output_data` | output | 8 | i_clk | o_output_data | 单时钟固定前端接口；有效负载保持到ready，完整表和参数后才能计算；复位立即取消。 |
| `o_output_index` | output | 9 | i_clk | o_output_index | 单时钟固定前端接口；有效负载保持到ready，完整表和参数后才能计算；复位立即取消。 |
| `o_export_done` | output | 1 | i_clk | o_export_done | 单时钟固定前端接口；有效负载保持到ready，完整表和参数后才能计算；复位立即取消。 |

## 5. 周期行为与延迟

- Stem4×4×16，down2 DW4×4×16再PW4×4×24，原数值、算术核和II不变。
- 共享顶层owner只在两个调度器空闲、算术排空且结果导出完成时切换；未导出结果禁止覆盖。
- 表只装一次后可切换算子；复位后不允许继续使用旧表。
- 顺序装载由各调度器按既有kind编码验证，数据必须保持直至ready；故障只可复位恢复。

## 6. WaveDrom 时序图

### 排空后切换

压缩示意；busy和未导出均阻止切换，导出完成后的空闲拍允许握手。

![排空后切换](waveforms/road_frontend_shared_core_handoff.svg)

- WaveJSON：[road_frontend_shared_core_handoff.json5](waveforms/road_frontend_shared_core_handoff.json5)

## 7. 边界、反压与错误

- 部分表和halo、尾lane、未导出交接、背压、复位取消、非法装载。

## 8. CDC 与综合约束

- 独立功能候选，TEST_ONLY动态系数；没有部署QAT或真实DDR完成语义。
- 不声称全网5FPS或生产时序通过；本次不增加任务重叠。

## 9. 验证与验收

- 同冻结2304Stem及576down2全量阶段/缓存读口比较；单算术链共享。

## 10. 可追溯性

- 规格模块：`road_frontend_shared_core`
- RTL 路径：`road_frontend_shared_core.v`
- 交付要求：本文档、WaveJSON 和 SVG 必须与同一版本规格一同发布。
