# road_pw_tile_scheduler 模块规范

> RTL: `road_pw_tile_scheduler.v`

## 1. 模块目的

冻结三种形状：PROFILE0=48→48兼容，1=96→24，2=192→12输出分片；同一算术核和窄口协议。

## 2. 参数

| 参数 | 默认值 | 说明 |
| --- | --- | --- |
| PROFILE | 0 | 只支持0/1/2三个冻结编译形状；不是运行时任意卷积配置。 |

## 3. 时钟与复位

- 时钟：`{"name": "i_clk", "edge": "posedge", "frequency_hz": 100000000}`
- 复位：`{"name": "i_rstn", "active": "low", "synchronous": false, "values": "立即取消旧事务；同步释放后重新完整装载1024项表及全部参数/halo。"}`

## 4. 接口信号规范

| 信号 | 方向 | 位宽 | 时钟域 | 语义角色 | 描述 |
| --- | --- | --- | --- | --- | --- |
| `i_clk` | input | 1 | i_clk | i_clk | 沿用冻结PW48接口；valid保持到ready，复位立即取消。 |
| `i_rstn` | input | 1 | i_clk | i_rstn | 沿用冻结PW48接口；valid保持到ready，复位立即取消。 |
| `i_table_loaded` | input | 1 | i_clk | i_table_loaded | 沿用冻结PW48接口；valid保持到ready，复位立即取消。 |
| `i_load_valid` | input | 1 | i_clk | i_load_valid | 沿用冻结PW48接口；valid保持到ready，复位立即取消。 |
| `i_load_kind` | input | 3 | i_clk | i_load_kind | 0 signed输入、2权重、3bias、4premul、5shift、6post；1/7非法。 |
| `i_load_addr` | input | 12 | i_clk | i_load_addr | 12位地址不变；输入0..16Cin-1、权重0..2303、通道参数0..Cout-1。 |
| `i_load_data` | input | 32 | i_clk | i_load_data | signed INT8以32位符号扩展承载；bias为signed32，其余范围见执行契约。 |
| `o_load_ready` | output | 1 | i_clk | o_load_ready | 沿用冻结PW48接口；valid保持到ready，复位立即取消。 |
| `i_start` | input | 1 | i_clk | i_start | 沿用冻结PW48接口；valid保持到ready，复位立即取消。 |
| `o_busy` | output | 1 | i_clk | o_busy | 沿用冻结PW48接口；valid保持到ready，复位立即取消。 |
| `o_done` | output | 1 | i_clk | o_done | 沿用冻结PW48接口；valid保持到ready，复位立即取消。 |
| `o_fault` | output | 1 | i_clk | o_fault | 沿用冻结PW48接口；valid保持到ready，复位立即取消。 |
| `o_core_cycles` | output | 32 | i_clk | o_core_cycles | 沿用冻结PW48接口；valid保持到ready，复位立即取消。 |
| `o_mac_valid` | output | 1 | i_clk | o_mac_valid | 沿用冻结PW48接口；valid保持到ready，复位立即取消。 |
| `i_mac_ready` | input | 1 | i_clk | i_mac_ready | 沿用冻结PW48接口；valid保持到ready，复位立即取消。 |
| `o_mac_first` | output | 1 | i_clk | o_mac_first | 沿用冻结PW48接口；valid保持到ready，复位立即取消。 |
| `o_mac_last` | output | 1 | i_clk | o_mac_last | 当前归约组5；六组共48个有效乘积。 |
| `o_mac_mask` | output | 8 | i_clk | o_mac_mask | 固定8'hff，48输入没有尾lane。 |
| `o_mac_activation` | output | 64 | i_clk | o_mac_activation | 沿用冻结PW48接口；valid保持到ready，复位立即取消。 |
| `o_mac_weight` | output | 192 | i_clk | o_mac_weight | 沿用冻结PW48接口；valid保持到ready，复位立即取消。 |
| `o_mac_bias` | output | 96 | i_clk | o_mac_bias | 沿用冻结PW48接口；valid保持到ready，复位立即取消。 |
| `i_mac_result_valid` | input | 1 | i_clk | i_mac_result_valid | 沿用冻结PW48接口；valid保持到ready，复位立即取消。 |
| `o_mac_result_ready` | output | 1 | i_clk | o_mac_result_ready | 沿用冻结PW48接口；valid保持到ready，复位立即取消。 |
| `i_mac_result` | input | 96 | i_clk | i_mac_result | 沿用冻结PW48接口；valid保持到ready，复位立即取消。 |
| `i_mac_fault` | input | 1 | i_clk | i_mac_fault | 沿用冻结PW48接口；valid保持到ready，复位立即取消。 |
| `o_pp_valid` | output | 1 | i_clk | o_pp_valid | 沿用冻结PW48接口；valid保持到ready，复位立即取消。 |
| `i_pp_ready` | input | 1 | i_clk | i_pp_ready | 沿用冻结PW48接口；valid保持到ready，复位立即取消。 |
| `o_pp_acc` | output | 96 | i_clk | o_pp_acc | 沿用冻结PW48接口；valid保持到ready，复位立即取消。 |
| `o_pp_multipliers` | output | 96 | i_clk | o_pp_multipliers | 沿用冻结PW48接口；valid保持到ready，复位立即取消。 |
| `o_pp_shifts` | output | 18 | i_clk | o_pp_shifts | 沿用冻结PW48接口；valid保持到ready，复位立即取消。 |
| `o_pp_post_multiplier` | output | 32 | i_clk | o_pp_post_multiplier | 沿用冻结PW48接口；valid保持到ready，复位立即取消。 |
| `o_pp_post_shift` | output | 6 | i_clk | o_pp_post_shift | 沿用冻结PW48接口；valid保持到ready，复位立即取消。 |
| `o_pp_mask` | output | 3 | i_clk | o_pp_mask | 固定3'b111，48输出没有尾通道。 |
| `o_pp_tags` | output | 48 | i_clk | o_pp_tags | 三路完整tag=position×48+channel，范围0..767。 |
| `i_pp_valid` | input | 1 | i_clk | i_pp_valid | 沿用冻结PW48接口；valid保持到ready，复位立即取消。 |
| `o_pp_ready` | output | 1 | i_clk | o_pp_ready | 沿用冻结PW48接口；valid保持到ready，复位立即取消。 |
| `i_pp_data` | input | 16 | i_clk | i_pp_data | 沿用冻结PW48接口；valid保持到ready，复位立即取消。 |
| `i_pp_tag` | input | 16 | i_clk | i_pp_tag | 沿用冻结PW48接口；valid保持到ready，复位立即取消。 |
| `i_pp_int16` | input | 1 | i_clk | i_pp_int16 | 沿用冻结PW48接口；valid保持到ready，复位立即取消。 |
| `i_pp_fault` | input | 1 | i_clk | i_pp_fault | 沿用冻结PW48接口；valid保持到ready，复位立即取消。 |
| `i_commit_ready` | input | 1 | i_clk | i_commit_ready | 沿用冻结PW48接口；valid保持到ready，复位立即取消。 |
| `i_export_start` | input | 1 | i_clk | i_export_start | 沿用冻结PW48接口；valid保持到ready，复位立即取消。 |
| `o_output_valid` | output | 1 | i_clk | o_output_valid | 沿用冻结PW48接口；valid保持到ready，复位立即取消。 |
| `i_output_ready` | input | 1 | i_clk | i_output_ready | 沿用冻结PW48接口；valid保持到ready，复位立即取消。 |
| `o_output_data` | output | 8 | i_clk | o_output_data | 沿用冻结PW48接口；valid保持到ready，复位立即取消。 |
| `o_output_index` | output | 10 | i_clk | o_output_index | 片内HWC索引0..16Cout-1，握手推进；不冒充整图全局写地址。 |
| `o_export_done` | output | 1 | i_clk | o_export_done | 沿用冻结PW48接口；valid保持到ready，复位立即取消。 |

## 5. 周期行为与延迟

- PROFILE0保留原回归；PROFILE1/2分别12/24组×8输入，未超过192有效乘积。
- 输入bank=ic%8,row=position*(Cin/8)+ic//8；权重bank=(local_oc%3)*8+ic%8,row=(local_oc//3)*(Cin/8)+ic//8。
- bias/pre三浅bank不变；装载地址0重启，完整性与合法性检查按冻结片形状展开。
- 每片输出local tag=position*Cout+local_oc；局部输出真实缓存逐项导出。全局OC合并由参考检查，不声称图执行器已实现。
- 表1024项重装、first/last、长反压、故障禁止发布、复位即时取消与既有接口保持。

## 6. WaveDrom 时序图

### 输出分片逐段归约

装载→PREPARE→12或24组接受→MAC等待→下一任务，所有输出提交才done，再导出。

![输出分片逐段归约](waveforms/road_pw_tile_scheduler_slab.svg)

- WaveJSON：[road_pw_tile_scheduler_slab.json5](waveforms/road_pw_tile_scheduler_slab.json5)

## 7. 边界、反压与错误

- 输入1535/1536、3071/3072，权重2303/2304，24/12参数边界，末24组及输出分片拼接。

## 8. CDC 与综合约束

- 12位逻辑装载地址不变；每片权重2304，输入768/1536/3072，输出768/384/192。
- 192→96按8个12输出通道分片；当前外部图级遍历和全局写址尚未实现。
- 算术核signed33末组INT32、RNE、SiLU、II、反压和复位行为不变。

## 9. 验证与验收

- PROFILE0同CSV回归；96及192八片真实参数逐级黄金值、随机/长反压、复位取消。

## 10. 可追溯性

- 规格模块：`road_pw_tile_scheduler`
- RTL 路径：`road_pw_tile_scheduler.v`
- 交付要求：本文档、WaveJSON 和 SVG 必须与同一版本规格一同发布。
