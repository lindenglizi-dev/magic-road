# tb_csp_tile_integrated 模块规范

> RTL: `tests/tb_csp_tile_integrated.v`

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
| `o_test_complete` | output | 1 | clk | native | 所有当前场景检查通过 |

## 5. 周期行为与延迟

- 只供应源、表和外部背压，不驱动内部任务、操作数或完成
- 真实核心各阶段与同包整数golden对拍，重复tile改变源以捕获旧缓存

## 6. WaveDrom 时序图

### 固定tile边界与完成

省略实际算术延迟；done严格来自最后实际写

![固定tile边界与完成](waveforms/tb_csp_tile_integrated_sequence.svg)

- WaveJSON：[tb_csp_tile_integrated_sequence.json5](waveforms/tb_csp_tile_integrated_sequence.json5)

## 7. 边界、反压与错误

- 完整源与表之前禁止启动
- 源重复和越界写粘滞错误
- 复位取消全部在途有效位
- 输出反压保持

## 8. CDC 与综合约束

- 仅首残差tile，不代表完整CSP2、整网、真实DDR或物理实现
- 保留冻结算术端口、II和数值

## 9. 验证与验收

- 320组、160任务、384输出和各中间值逐项一致
- 192实际DW写驱动128次PW缓存读
- 随机与长反压
- 三阶段复位
- 两次不同输入tile不复位核心或重装表
- 外部取消阻止同拍写

## 10. 可追溯性

- 规格模块：`tb_csp_tile_integrated`
- RTL 路径：`tests/tb_csp_tile_integrated.v`
- 交付要求：本文档、WaveJSON 和 SVG 必须与同一版本规格一同发布。
