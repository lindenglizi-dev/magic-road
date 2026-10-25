# road_stem_ddr_sequence 模块规范

> RTL: `road_stem_ddr_sequence.v`

## 1. 模块目的

完整前三层RGB同像素缓存地址复用；核和DDR接口保持。

## 2. 参数

| 参数 | 默认值 | 说明 |
| --- | --- | --- |
| — | — | 本模块没有可配置参数。 |

## 3. 时钟与复位

- 时钟：`{"domains": "CNN100MHz; DDR133.33MHz; HDMI75/375MHz"}`
- 复位：`{"assertion": "Entire DDR and arithmetic jointly asserted asynchronously", "release": "Two-flop release in each domain, reload all 1024 SiLU entries before start"}`

## 4. 接口信号规范

| 信号 | 方向 | 位宽 | 时钟域 | 语义角色 | 描述 |
| --- | --- | --- | --- | --- | --- |
| `i_clk` | input | 1 | 未声明 | 100MHz计算时钟 | 100MHz计算时钟 |
| `i_rstn` | input | 1 | 未声明 | 与整个DDR共同断言并在本域同步释放 | 与整个DDR共同断言并在本域同步释放 |
| `i_phy_ready` | input | 1 | 未声明 | 已同步到本域的初始化许可 | 已同步到本域的初始化许可 |
| `i_ddr_fault` | input | 1 | 未声明 | 邮箱的本域粘滞故障 | 邮箱的本域粘滞故障 |
| `i_req_ready` | input | 1 | 未声明 | 邮箱可保管唯一请求 | 邮箱可保管唯一请求 |
| `i_rsp_valid` | input | 1 | 未声明 | 完整响应已跨域冻结 | 完整响应已跨域冻结 |
| `i_rsp_data` | input | 128 | 未声明 | 实际DDR返回字 | 实际DDR返回字 |
| `i_rsp_error` | input | 4 | 未声明 | 写接受或读请求错误 | 写接受或读请求错误 |
| `o_req_valid` | output | 1 | 未声明 | 载荷保持到本域接受 | 载荷保持到本域接受 |
| `o_req_write` | output | 1 | 未声明 | 写接受与读返回分型 | 写接受与读返回分型 |
| `o_req_addr` | output | 25 | 未声明 | 按冻结布局转换的native地址 | 按冻结布局转换的native地址 |
| `o_req_data` | output | 128 | 未声明 | 实际核导出打包的128位字 | 实际核导出打包的128位字 |
| `o_rsp_ready` | output | 1 | 未声明 | 完整响应只消费一次 | 完整响应只消费一次 |
| `o_status` | output | 2 | 未声明 | 零等待、一通过、二失败 | 零等待、一通过、二失败 |
| `o_error` | output | 4 | 未声明 | 首个失败类型 | 首个失败类型 |
| `o_phase` | output | 5 | 未声明 | 可观测调度状态 | 可观测调度状态 |
| `o_writes` | output | 32 | 未声明 | 已收到接受回执的唯一写字数 | 已收到接受回执的唯一写字数 |
| `o_reads` | output | 32 | 未声明 | 实际已消费的读响应数 | 实际已消费的读响应数 |
| `o_output_bytes` | output | 32 | 未声明 | 已核对的最终PW字节数 | 已核对的最终PW字节数 |
| `o_cycles` | output | 32 | 未声明 | 含初始化的端点总周期 | 含初始化的端点总周期 |
| `o_cycle_bins` | output | 320 | 未声明 | 十项互斥分类，低32位为初始化 | 十项互斥分类，低32位为初始化 |
| `o_address` | output | 25 | 未声明 | 当前读写的完整native地址 | 当前读写的完整native地址 |
| `o_expected` | output | 128 | 未声明 | 最近比较的完整期望字 | 最近比较的完整期望字 |
| `o_actual` | output | 128 | 未声明 | 最近比较的完整实读或导出字 | 最近比较的完整实读或导出字 |

## 5. 周期行为与延迟

- 10800个宏命令；2304 Stem块和576下采样块，真实输出写DDR再作为下一层输入。
- 图像从48词周期图案写满DDR；算术激活必须来自DDR实读或定义的padding。
- 单16B缓存每tile失效，命中省读；完整写/读/导出计数必须一致才PASS。
- 计算与DDR共同复位；所有旧计数、缓存和valid取消，重新写输入并装满1024表。
- RGB非padding、channel<2、cache有效且tag匹配、lane<15时，core_load握手后lane+1并留HALO_BYTE。
- lane15、padding或cache无效回原MAP→ROW→ADDRESS→CACHE；末B通道换像素仍回原路径。
- 反压不推进lane/channel/halo索引；整个DDR/CNN共同复位，重新装满1024项表。
- W响应只表示原mailbox接受AW/W，不是存储可见或提交保证。

## 6. WaveDrom 时序图

### R14/G15直达与B跨词回退

例示响应延迟仅为图示；真实READ_RESPONSE等待valid。

![R14/G15直达与B跨词回退](waveforms/road_stem_ddr_sequence_rgb-word-boundary.svg)

- WaveJSON：[road_stem_ddr_sequence_rgb-word-boundary.json5](waveforms/road_stem_ddr_sequence_rgb-word-boundary.json5)

### 装载反压保持游标

ready为零期间同一HALO字节保持，接受后才换下一通道。

![装载反压保持游标](waveforms/road_stem_ddr_sequence_rgb-load-stall.svg)

- WaveJSON：[road_stem_ddr_sequence_rgb-load-stall.json5](waveforms/road_stem_ddr_sequence_rgb-load-stall.json5)

## 7. 边界、反压与错误

- 顶左padding、右下末tile、行列进位、cache跨字节边界、请求背压、读延迟、复位与故障

## 8. CDC 与综合约束

- Read-only ROM initialization is checked separately from board readback.
- No new timing exceptions for mailbox; existing bounded display CDC retained.
- TEST_ONLY coefficients, no deployed-model precision or full CNN FPS claim.

## 9. 验证与验收

- 全帧逐项数值与地址、真实中间值、正常及随机背压、共同复位、实际TD资源时序
- 原八例同向量，lane14/15跨词，RGB通道编号，真实子核装载长反压

## 10. 可追溯性

- 规格模块：`road_stem_ddr_sequence`
- RTL 路径：`road_stem_ddr_sequence.v`
- 交付要求：本文档、WaveJSON 和 SVG 必须与同一版本规格一同发布。
