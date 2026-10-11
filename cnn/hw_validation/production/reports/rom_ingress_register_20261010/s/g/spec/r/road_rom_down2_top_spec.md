# road_rom_down2_top 模块规范

> RTL: `rtl/road_rom_down2_top.v`

## 1. 模块目的

独立schema2 TEST参数接入，不是训练模型部署或整网性能证明。

## 2. 参数

| 参数 | 默认值 | 说明 |
| --- | --- | --- |
| — | — | 本模块没有可配置参数。 |

## 3. 时钟与复位

- 时钟：`{"name": "i_clk", "edge": "posedge", "frequency_hz": 100000000}`
- 复位：`{"name": "i_rstn", "active": "low", "synchronous": false, "values": "取消全部旧事务和装载有效状态；top同步释放后重装1024表项。"}`

## 4. 接口信号规范

| 信号 | 方向 | 位宽 | 时钟域 | 语义角色 | 描述 |
| --- | --- | --- | --- | --- | --- |
| `i_clk` | input | 1 | i_clk | i_clk | i_clk |
| `i_rstn` | input | 1 | i_clk | i_rstn | i_rstn |
| `i_load_valid` | input | 1 | i_clk | i_load_valid | i_load_valid |
| `i_load_addr` | input | 11 | i_clk | i_load_addr | i_load_addr |
| `i_load_data` | input | 8 | i_clk | i_load_data | i_load_data |
| `o_load_ready` | output | 1 | i_clk | o_load_ready | o_load_ready |
| `i_start` | input | 1 | i_clk | i_start | i_start |
| `i_commit_ready` | input | 1 | i_clk | i_commit_ready | i_commit_ready |
| `i_export_start` | input | 1 | i_clk | i_export_start | i_export_start |
| `i_output_ready` | input | 1 | i_clk | i_output_ready | i_output_ready |
| `o_parameters_ready` | output | 1 | i_clk | o_parameters_ready | o_parameters_ready |
| `o_busy` | output | 1 | i_clk | o_busy | o_busy |
| `o_done` | output | 1 | i_clk | o_done | o_done |
| `o_fault` | output | 1 | i_clk | o_fault | o_fault |
| `o_output_valid` | output | 1 | i_clk | o_output_valid | o_output_valid |
| `o_output_data` | output | 8 | i_clk | o_output_data | o_output_data |
| `o_output_index` | output | 9 | i_clk | o_output_index | o_output_index |
| `o_export_done` | output | 1 | i_clk | o_export_done | o_export_done |

## 5. 周期行为与延迟

- 50位外部端口不变；两级同步释放后自动从冻结TEST ROM装参数及1024项SiLU表。
- 仅参数流增加pending1/kind3/address11/data32单笔寄存，空时接收，不支持同拍排出补入。
- 预取器ready只确认进入缓冲；runner valid&&ready才确认参数提交，反压时payload保持。
- pref_done、table_loaded、沿前pending=0且无fault才登记external_owner，末笔消费同拍不移交。
- halo和表保持原直通接口；最后halo握手后的下一拍允许start。
- 故障当拍禁止runner参数有效，下一沿清pending/owner；复位立即取消、重新完整预取。
- 保持MAC/动态重定标/RNE/SiLU/缓存及II；启动周期单列，小块核心应仍1687周期。

## 6. WaveDrom 时序图

### 单笔参数保持与提交

在capture沿锁存，受阻保持，consume沿释放；owner另在已空的后续沿登记。

![单笔参数保持与提交](waveforms/road_rom_down2_top_entry.svg)

- WaveJSON：[road_rom_down2_top_entry.json5](waveforms/road_rom_down2_top_entry.json5)

## 7. 边界、反压与错误

- 跨20字节词、物理bank边界、未对齐层尾、非法地址。
- 装载和计算受阻时复位，不泄漏旧输出。

## 8. CDC 与综合约束

- 不改原核接口、II、数值、复位合同；不增时序例外。
- 不训练、不改生产、不生成位流、不上板。

## 9. 验证与验收

- 厂商PH1P模型、1676笔字段逐项比较、MAC/pre/SiLU/post/写回/导出对拍。
- 原64项同向量回归；TD资源和时序单列。

## 10. 可追溯性

- 规格模块：`road_rom_down2_top`
- RTL 路径：`rtl/road_rom_down2_top.v`
- 交付要求：本文档、WaveJSON 和 SVG 必须与同一版本规格一同发布。
