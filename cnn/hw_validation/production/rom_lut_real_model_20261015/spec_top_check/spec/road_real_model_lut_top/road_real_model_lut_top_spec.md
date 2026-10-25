# road_real_model_lut_top 模块规范

> RTL: `rtl/road_real_model_lut_top.v`

## 1. 模块目的

未提供模块目的。

## 2. 参数

| 参数 | 默认值 | 说明 |
| --- | --- | --- |
| — | — | 本模块没有可配置参数。 |

## 3. 时钟与复位

- 时钟：`{"name": "i_clk", "frequency_hz": 100000000}`
- 复位：`{"name": "i_rstn", "assert": "async_low", "release": "local_sync_two_flops_or_owner_gating"}`

## 4. 接口信号规范

| 信号 | 方向 | 位宽 | 时钟域 | 语义角色 | 描述 |
| --- | --- | --- | --- | --- | --- |
| `i_clk` | input | 1 | i_clk | clk | 统一100MHz上升沿时钟 |
| `i_rstn` | input | 1 | i_clk | rstn | 共同低有效异步复位，本地两级同步释放 |
| `i_cancel` | input | 1 | i_clk | cancel | 取消当前查表，已接受的ROM读必须排空后再接新任务 |
| `i_lut_req_valid` | input | 1 | i_clk | lut_req_valid | 查表请求有效，等待ready时所有请求字段保持 |
| `i_lut_req_kind` | input | 1 | i_clk | lut_req_kind | 0为sigmoid，1为exp |
| `i_lut_req_address` | input | 10 | i_clk | lut_req_address | 表内索引；exp只允许0至255 |
| `i_lut_req_tag` | input | 16 | i_clk | lut_req_tag | 16位请求标签，响应原样回显 |
| `i_lut_req_frame_token` | input | 32 | i_clk | lut_req_frame_token | 请求源帧任务标识，响应回显 |
| `i_lut_req_model_id` | input | 32 | i_clk | lut_req_model_id | 绑定完整模型payload的32位模型标识 |
| `i_lut_rsp_ready` | input | 1 | i_clk | lut_rsp_ready | 本拍允许消费一次完整查表响应 |
| `o_lut_req_ready` | output | 1 | i_clk | lut_req_ready | 空闲且无旧ROM在途时允许一次查表传输 |
| `o_lut_rsp_valid` | output | 1 | i_clk | lut_rsp_valid | 查表完整响应有效，等ready时身份与数据保持 |
| `o_lut_rsp_kind` | output | 1 | i_clk | lut_rsp_kind | 回显已接受请求的表类别 |
| `o_lut_rsp_address` | output | 10 | i_clk | lut_rsp_address | 回显已接受请求的原索引 |
| `o_lut_rsp_tag` | output | 16 | i_clk | lut_rsp_tag | 回显已接受请求的16位标签 |
| `o_lut_rsp_frame_token` | output | 32 | i_clk | lut_rsp_frame_token | 回显源帧标识，禁止旧响应串入新任务 |
| `o_lut_rsp_model_id` | output | 32 | i_clk | lut_rsp_model_id | 回显请求模型标识 |
| `o_lut_rsp_data` | output | 16 | i_clk | lut_rsp_data | 从冻结小端ROM字节提取的UINT16值 |
| `o_lut_rsp_error` | output | 1 | i_clk | lut_rsp_error | 范围/模型/ROM错误，错误数据为零 |
| `o_fault` | output | 1 | i_clk | fault | 本组件故障状态，不得发布为成功表 |

## 5. 周期行为与延迟

- 一个冻结ROM-R1 reader连接一个冻结共享LUT服务；无额外缓存、时钟、参数变换或流水。
- reader的14组/56lane只加载G10初始化；i_cancel只进入服务，绝不当作reader复位。
- 真实reader接受后等待原cnt_wait7；服务保持动态身份、跨词聚合和取消排空合同。

## 6. WaveDrom 时序图

### 请求所有权与停顿

动态请求握手示意，省略18步地址定位和reader固定等待；不是按图格数换算实际总时延。反压时身份/数值保持。

![请求所有权与停顿](waveforms/road_real_model_lut_top_request-hold-response.svg)

- WaveJSON：[road_real_model_lut_top_request-hold-response.json5](waveforms/road_real_model_lut_top_request-hold-response.json5)

## 7. 边界、反压与错误

- 复位、取消、背压、非法身份和边界地址；取消不能当成无标签外设已排空

## 8. CDC 与综合约束

- Verilog-2001；一个未决事务；ready/valid握手；无TD/物理时序签核
- 不改变冻结算术核/数值，不复制公共存储

## 9. 验证与验收

- 7168 complete160bitword matches
- 143360 physicalbytes
- 14group edges
- last payload byte140521
- zero padding2838
- full sigmoid1024/exp256
- backpressure hold
- cancel old response drain/restart
- common reset
- bad model/exp range no ROM read

## 10. 可追溯性

- 规格模块：`road_real_model_lut_top`
- RTL 路径：`rtl/road_real_model_lut_top.v`
- 交付要求：本文档、WaveJSON 和 SVG 必须与同一版本规格一同发布。
