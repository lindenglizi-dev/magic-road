# tb_feature_blocks_client 模块规范

> RTL: `tests/tb_feature_blocks_client.v`

## 1. 模块目的

未提供模块目的。

## 2. 参数

| 参数 | 默认值 | 说明 |
| --- | --- | --- |
| — | — | 本模块没有可配置参数。 |

## 3. 时钟与复位

- 时钟：`{"name": "clk", "edge": "posedge", "frequency_mhz": 100}`
- 复位：`{"name": "rstn", "active": "low", "synchronous": false}`

## 4. 接口信号规范

| 信号 | 方向 | 位宽 | 时钟域 | 语义角色 | 描述 |
| --- | --- | --- | --- | --- | --- |
| `o_test_complete` | output | 1 | 未声明 | verification_completion | 所有当前场景检查完成 |

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

![固定块只在启动握手锁存](waveforms/tb_feature_blocks_client_selection.svg)

- WaveJSON：[tb_feature_blocks_client_selection.json5](waveforms/tb_feature_blocks_client_selection.json5)

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

- 规格模块：`tb_feature_blocks_client`
- RTL 路径：`tests/tb_feature_blocks_client.v`
- 交付要求：本文档、WaveJSON 和 SVG 必须与同一版本规格一同发布。
