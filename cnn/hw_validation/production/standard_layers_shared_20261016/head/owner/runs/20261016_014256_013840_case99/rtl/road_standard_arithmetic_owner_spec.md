# road_standard_arithmetic_owner 模块规范

> RTL: `rtl/road_standard_arithmetic_owner.v`

## 1. 模块目的

未提供模块目的。

## 2. 参数

| 参数 | 默认值 | 说明 |
| --- | --- | --- |
| — | — | 本模块没有可配置参数。 |

## 3. 时钟与复位

- 时钟：`{"name": "i_clk", "edge": "posedge", "frequency_mhz": 100}`
- 复位：`{"name": "i_rstn", "active": "low", "synchronous": false}`

## 4. 接口信号规范

| 信号 | 方向 | 位宽 | 时钟域 | 语义角色 | 描述 |
| --- | --- | --- | --- | --- | --- |
| `i_clk` | input | 1 | 未声明 | native | 同域100MHz时钟 |
| `i_rstn` | input | 1 | 未声明 | native | 所有原核共同低有效异步复位 |
| `i_table_valid` | input | 1 | 未声明 | native | 空闲表项保持有效 |
| `i_table_addr` | input | 10 | 未声明 | native | 原表严格递增装载地址 |
| `i_table_data` | input | 16 | 未声明 | native | 原模型有符号Q7.8表项 |
| `i_input_valid` | input | 1 | 未声明 | native | 八输入组保持到真实握手 |
| `i_first` | input | 1 | 未声明 | native | 仅首组开启归约并锁存元数据 |
| `i_last` | input | 1 | 未声明 | native | 当前组关闭归约 |
| `i_lane_mask` | input | 8 | 未声明 | native | 八输入槽使能 |
| `i_activation_data` | input | 64 | 未声明 | native | 低字节优先八个INT8 |
| `i_weight_data` | input | 192 | 未声明 | native | 三路各八个INT8权重 |
| `i_bias_data` | input | 96 | 未声明 | native | 原MAC只在first使用三路INT32偏置 |
| `i_output_mask` | input | 3 | 未声明 | native | 首组锁存三路输出有效位 |
| `i_tags` | input | 48 | 未声明 | native | 首组锁存不透明输出身份 |
| `i_addresses` | input | 96 | 未声明 | native | 首组锁存三路写地址 |
| `i_pre_multipliers` | input | 96 | 未声明 | native | 首组锁存三路前乘数 |
| `i_pre_shifts` | input | 18 | 未声明 | native | 首组锁存三路前移位 |
| `i_post_multiplier` | input | 32 | 未声明 | native | 首组锁存共享后乘数 |
| `i_post_shift` | input | 6 | 未声明 | native | 首组锁存共享后移位 |
| `i_activate` | input | 1 | 未声明 | native | 首组选择SiLU INT8或raw INT16 |
| `i_input_fault` | input | 1 | 未声明 | native | 任务错误转为保持故障 |
| `i_output_ready` | input | 1 | 未声明 | native | 唯一写端实际退休许可 |
| `o_table_ready` | output | 1 | 未声明 | native | 空闲且原DPP接受表项 |
| `o_table_loaded` | output | 1 | 未声明 | native | 原核完整表装载状态 |
| `o_input_ready` | output | 1 | 未声明 | native | 归约输入组接纳许可 |
| `o_output_valid` | output | 1 | 未声明 | native | 匹配身份和类型的完整输出有效 |
| `o_output_data` | output | 16 | 未声明 | native | 激活符号扩展INT8或raw INT16 |
| `o_output_int16` | output | 1 | 未声明 | native | 等于首组activate反值 |
| `o_output_tag` | output | 16 | 未声明 | native | 与数据同生存期身份 |
| `o_output_address` | output | 32 | 未声明 | native | 身份所选锁存写地址 |
| `o_fault` | output | 1 | 未声明 | native | 元数据或核故障粘滞 |
| `o_busy` | output | 1 | 未声明 | native | 首组到末输出退休或故障保持 |

## 5. 周期行为与延迟

- 单任务IDLE/GROUP/ACC/OUTPUT/FAULT三段状态机
- 首组锁存mask/tags/address/pre/post/activate，后续元数据变化忽略
- ACC只向原DPP提交一次完整MAC结果
- 最后有效lane真实输出握手后才能解除busy；故障必须共同复位
- 输出直接采用原DPP保持槽，owner没有结果array或residual

## 6. WaveDrom 时序图

### 仅最后真实输出退休释放

省略原核计算拍，输出反压保持身份，MAC交接不释放owner

![仅最后真实输出退休释放](waveforms/road_standard_arithmetic_owner_retirement.svg)

- WaveJSON：[road_standard_arithmetic_owner_retirement.json5](waveforms/road_standard_arithmetic_owner_retirement.json5)

## 7. 边界、反压与错误

- mask1/3/7、opaque唯一tags、错误/重复身份与错误类型
- 激活输出必须INT8符号扩展；raw保留完整INT16
- 末输出背压不释放，table只在idle接受
- reset取消原核和元数据，SiLU必须重新装满

## 8. CDC 与综合约束

- 原五核端口、II、复位、算术均不改
- 所有核同域共同reset；两拍owner准入释放，最早第三沿接收
- 每路最多192乘积/24组由现固定客户端保证
- 接口无帧号；外部调度负责完整任务身份与DDR可见性

## 9. 验证与验收

- 整数参考逐MAC/pre/SiLU/post/final值
- 真实ModelSim原核和原SiLU1024表
- 多组bias一次、尾mask、首组锁存扰动
- GROUP/ACC/OUTPUT共同复位和故障保持

## 10. 可追溯性

- 规格模块：`road_standard_arithmetic_owner`
- RTL 路径：`rtl/road_standard_arithmetic_owner.v`
- 交付要求：本文档、WaveJSON 和 SVG 必须与同一版本规格一同发布。
