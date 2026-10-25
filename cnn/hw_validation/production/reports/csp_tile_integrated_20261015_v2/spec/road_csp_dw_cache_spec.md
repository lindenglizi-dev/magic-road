# road_csp_dw_cache 模块规范

> RTL: `rtl/road_csp_dw_cache.v`

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
| `i_clk` | input | 1 | i_clk | clock | 同域时钟 |
| `i_rstn` | input | 1 | i_clk | reset | 共同异步复位 |
| `i_clear` | input | 1 | i_clk | native | 启动新tile时同步清有效位 |
| `i_write_valid` | input | 1 | i_clk | native | 真实DW写请求 |
| `i_write_index` | input | 8 | i_clk | native | 0至191逻辑索引 |
| `i_write_data` | input | 8 | i_clk | native | 真实DW字节 |
| `i_read_valid` | input | 1 | i_clk | native | PW八输入组请求 |
| `i_read_pixel` | input | 4 | i_clk | native | 4x4像素位置 |
| `i_read_group` | input | 1 | i_clk | native | 八加四输入分组 |
| `i_output_ready` | input | 1 | i_clk | native | 响应消费许可 |
| `o_write_ready` | output | 1 | i_clk | native | 采集阶段写许可 |
| `o_write_legal` | output | 1 | i_clk | native | 当前DW索引合法且未写 |
| `o_loaded` | output | 1 | i_clk | native | 192个不同结果已齐全 |
| `o_write_count` | output | 8 | i_clk | native | 唯一实际写数量 |
| `o_fault` | output | 1 | i_clk | native | 非法写粘滞错误 |
| `o_read_ready` | output | 1 | i_clk | native | 完整屏障及响应空间许可 |
| `o_output_valid` | output | 1 | i_clk | native | 注册缓存响应valid |
| `o_output_data` | output | 64 | i_clk | native | 八字节实际缓存值 |
| `o_output_mask` | output | 8 | i_clk | native | 末组只低四lane有效 |
| `o_output_pixel` | output | 4 | i_clk | native | 响应像素身份 |
| `o_output_group` | output | 1 | i_clk | native | 响应分组身份 |

## 5. 周期行为与延迟

- i_clear同步撤销位图、计数及响应valid，不复位RAM，不清除粘滞故障
- 192不同有效写之后允许PW请求，响应一槽并保持至真实接受

## 6. WaveDrom 时序图

### 固定tile边界与完成

省略实际算术延迟；done严格来自最后实际写

![固定tile边界与完成](waveforms/road_csp_dw_cache_sequence.svg)

- WaveJSON：[road_csp_dw_cache_sequence.json5](waveforms/road_csp_dw_cache_sequence.json5)

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

- 规格模块：`road_csp_dw_cache`
- RTL 路径：`rtl/road_csp_dw_cache.v`
- 交付要求：本文档、WaveJSON 和 SVG 必须与同一版本规格一同发布。
