# road_feature_blocks_client 模块规范

> RTL: `rtl/road_feature_blocks_client.v`

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
| `i_clk` | input | 1 | 未声明 | native | 与算术owner同域100MHz |
| `i_rstn` | input | 1 | 未声明 | native | 共同异步复位，服务同时撤销旧响应 |
| `i_block_id` | input | 4 | 未声明 | native | 仅start握手锁存的固定块编号 |
| `o_block_id` | output | 4 | 未声明 | native | 当前任务身份直到下一次start保持 |
| `i_start` | input | 1 | 未声明 | native | ready时启动一次完整固定图任务 |
| `i_cancel` | input | 1 | 未声明 | native | 取消后故障占有至共同复位 |
| `i_table_loaded` | input | 1 | 未声明 | native | 外部owner已装入同包SiLU表 |
| `o_start_ready` | output | 1 | 未声明 | native | 空闲、无故障且表有效 |
| `o_busy` | output | 1 | 未声明 | native | 包含完成拍和故障占有 |
| `o_done` | output | 1 | 未声明 | native | 末阶段可见性确认后单拍完成 |
| `o_fault` | output | 1 | 未声明 | native | 信任边界错误粘滞指示 |
| `o_layer` | output | 3 | 未声明 | native | 当前块内阶段编号 |
| `o_tile_y` | output | 7 | 未声明 | native | 当前四行块起点诊断 |
| `o_tile_x` | output | 8 | 未声明 | native | 当前四列块起点诊断 |
| `o_parameter_valid` | output | 1 | 未声明 | native | 当前参数分片请求有效 |
| `o_parameter_channel` | output | 7 | 未声明 | native | DW通道或PW输出三通道起点 |
| `o_parameter_group` | output | 5 | 未声明 | native | 八输入归约组编号 |
| `o_parameter_window` | output | 3 | 未声明 | native | DW窗口并集宽度，PW为零 |
| `i_parameter_ready` | input | 1 | 未声明 | native | 参数请求被服务接受 |
| `i_parameter_response_valid` | input | 1 | 未声明 | native | 参数响应保持至ready |
| `o_parameter_response_ready` | output | 1 | 未声明 | native | 只消费当前未完成请求 |
| `i_parameter_response_block_id` | input | 4 | 未声明 | native | 响应必须属于当前锁存块 |
| `i_parameter_response_layer` | input | 3 | 未声明 | native | 参数响应阶段身份 |
| `i_parameter_response_channel` | input | 7 | 未声明 | native | 参数响应输出通道身份 |
| `i_parameter_response_group` | input | 5 | 未声明 | native | 参数响应归约组身份 |
| `i_parameter_response_window` | input | 3 | 未声明 | native | 参数响应DW窗口形态 |
| `i_parameter_weight` | input | 192 | 未声明 | native | 三路八输入权重 |
| `i_parameter_data` | input | 248 | 未声明 | native | bias及动态量化字段 |
| `i_parameter_error` | input | 1 | 未声明 | native | 参数服务显式错误 |
| `o_read_valid` | output | 1 | 未声明 | native | 单个16字节行请求有效 |
| `o_read_address` | output | 32 | 未声明 | native | 十六字节对齐逻辑地址 |
| `i_read_ready` | input | 1 | 未声明 | native | 行请求被内存服务接受 |
| `i_read_response_valid` | input | 1 | 未声明 | native | 行响应保持至ready |
| `o_read_response_ready` | output | 1 | 未声明 | native | 只消费当前未完成行请求 |
| `i_read_response_address` | input | 32 | 未声明 | native | 必须匹配请求的对齐地址 |
| `i_read_response_data` | input | 128 | 未声明 | native | 低字节对应地址偏移零 |
| `i_read_error` | input | 1 | 未声明 | native | 内存服务显式读错误 |
| `o_write_valid` | output | 1 | 未声明 | native | 合法核结果写请求 |
| `o_write_address` | output | 32 | 未声明 | native | 完整冻结图字节地址 |
| `o_write_data` | output | 8 | 未声明 | native | 最终饱和INT8结果 |
| `o_write_sum` | output | 9 | 未声明 | native | 饱和前signed9残差和 |
| `i_write_ready` | input | 1 | 未声明 | native | 外部写服务接受 |
| `o_barrier_valid` | output | 1 | 未声明 | native | 当前整层全部写接受后的屏障 |
| `i_barrier_ready` | input | 1 | 未声明 | native | 此层此前写已经可读 |
| `i_barrier_block_id` | input | 4 | 未声明 | native | 屏障必须属于当前锁存块 |
| `i_barrier_layer` | input | 3 | 未声明 | native | 屏障确认所属阶段 |
| `o_core_valid` | output | 1 | 未声明 | native | 原算术核输入组有效 |
| `i_core_ready` | input | 1 | 未声明 | native | 原算术核输入组接受 |
| `o_core_first` | output | 1 | 未声明 | native | 当前任务首归约组 |
| `o_core_last` | output | 1 | 未声明 | native | 当前任务末归约组 |
| `o_core_input_mask` | output | 8 | 未声明 | native | 当前八输入有效掩码 |
| `o_core_activation` | output | 64 | 未声明 | native | 串行拼装的八个INT8输入 |
| `o_core_weight` | output | 192 | 未声明 | native | 当前归约组驻留参数 |
| `o_core_bias` | output | 96 | 未声明 | native | 三路首组偏置 |
| `o_core_output_mask` | output | 3 | 未声明 | native | DW行尾任务只启用lane零 |
| `o_core_tags` | output | 48 | 未声明 | native | 固定三路任务身份 |
| `o_core_addresses` | output | 96 | 未声明 | native | 三路完整写地址 |
| `o_core_pre_multiplier` | output | 96 | 未声明 | native | 三路动态前乘数 |
| `o_core_pre_shift` | output | 18 | 未声明 | native | 三路六位前移位 |
| `o_core_post_multiplier` | output | 32 | 未声明 | native | 当前层共享后乘数 |
| `o_core_post_shift` | output | 6 | 未声明 | native | 当前层共享后移位 |
| `o_core_residual` | output | 1 | 未声明 | native | PW残差阶段使能 |
| `o_core_bypass` | output | 24 | 未声明 | native | 三路真实旁路值 |
| `i_core_output_valid` | input | 1 | 未声明 | native | 原五级写回结果有效 |
| `o_core_output_ready` | output | 1 | 未声明 | native | 核结果和外部写原子接受 |
| `i_core_output_tag` | input | 16 | 未声明 | native | 原核返回任务lane |
| `i_core_output_address` | input | 32 | 未声明 | native | 原核返回完整地址 |
| `i_core_output_data` | input | 8 | 未声明 | native | 原核返回sat8数据 |
| `i_core_output_sum` | input | 9 | 未声明 | native | 原核返回signed9和 |
| `i_core_fault` | input | 1 | 未声明 | native | 原核错误保持原语义 |

## 5. 周期行为与延迟

- start握手锁存固定块2/3/4，busy期间不得切换，非法选择故障拒绝
- 一个FSM、3072B工作缓存、24项权重bank，复用唯一外部算术owner
- CSP2五阶段、CSP3/4七阶段，全幅整层可见性后推进
- 参数响应和屏障必须匹配锁存block_id，读返回匹配单在途地址
- 开始块清行缓存valid，工作缓存不reset但每个使用项先完整覆盖
- 共同复位清控制且重新装SiLU；不证明独立取消排空

## 6. WaveDrom 时序图

### 固定块只在启动握手锁存

中间省略全幅计算；done仍busy，返回idle后才接受下一块

![固定块只在启动握手锁存](waveforms/road_feature_blocks_client_selection.svg)

- WaveJSON：[road_feature_blocks_client_selection.json5](waveforms/road_feature_blocks_client_selection.json5)

## 7. 边界、反压与错误

- 忙时block/start扰动，跨块缓存完全覆盖，随机背压保持payload
- 非法块、错误参数block、错误屏障block与真实acc负例
- 共同复位、SiLU重装、CSP4尾行与CSP2尾通道

## 8. CDC 与综合约束

- 固定图非任意引擎，核心端口/II/数值/复位不改
- CSP2 Cin12尾mask0f，CSP4物理尾tile仅两行有效，禁止y18/y19写
- 同实例顺序运行不等于down3/down4已接入或连续CNN
- 4ERAM为容量组织目标，未实际映射/综合/物理时序
- 100M是整机1FPS目标，不是本组件已证明整机帧率

## 9. 验证与验收

- 同实例2->3->4全幅数值及地址逐项一致
- 正常/随机/复位完整序列和归属拒绝
- 阶段/状态/端点周期互斥核验，CPU来源与RTL计算分开

## 10. 可追溯性

- 规格模块：`road_feature_blocks_client`
- RTL 路径：`rtl/road_feature_blocks_client.v`
- 交付要求：本文档、WaveJSON 和 SVG 必须与同一版本规格一同发布。
