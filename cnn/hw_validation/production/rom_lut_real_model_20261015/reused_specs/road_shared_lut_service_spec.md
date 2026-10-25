# road_shared_lut_service 模块规范

> RTL: `rtl/road_shared_lut_service.v`

## 1. 模块目的

未提供模块目的。

## 2. 参数

| 参数 | 默认值 | 说明 |
| --- | --- | --- |
| C_SIGMOID_BYTE_OFFSET | 137962 |  |
| C_EXP_BYTE_OFFSET | 140010 |  |

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
| `i_rom_request_ready` | input | 1 | i_clk | rom_request_ready | 现有reader允许锁定一个13位物理词地址 |
| `i_rom_response_valid` | input | 1 | i_clk | rom_response_valid | reader完整160位响应有效，不携带标签 |
| `i_rom_response_data` | input | 160 | i_clk | rom_response_data | 低8位对应物理词第0字节的160位载荷 |
| `i_rom_fault` | input | 1 | i_clk | rom_fault | reader粘滞故障，只由共同复位清除 |
| `o_lut_req_ready` | output | 1 | i_clk | lut_req_ready | 空闲且无旧ROM在途时允许一次查表传输 |
| `o_lut_rsp_valid` | output | 1 | i_clk | lut_rsp_valid | 查表完整响应有效，等ready时身份与数据保持 |
| `o_lut_rsp_kind` | output | 1 | i_clk | lut_rsp_kind | 回显已接受请求的表类别 |
| `o_lut_rsp_address` | output | 10 | i_clk | lut_rsp_address | 回显已接受请求的原索引 |
| `o_lut_rsp_tag` | output | 16 | i_clk | lut_rsp_tag | 回显已接受请求的16位标签 |
| `o_lut_rsp_frame_token` | output | 32 | i_clk | lut_rsp_frame_token | 回显源帧标识，禁止旧响应串入新任务 |
| `o_lut_rsp_model_id` | output | 32 | i_clk | lut_rsp_model_id | 回显请求模型标识 |
| `o_lut_rsp_data` | output | 16 | i_clk | lut_rsp_data | 从冻结小端ROM字节提取的UINT16值 |
| `o_lut_rsp_error` | output | 1 | i_clk | lut_rsp_error | 范围/模型/ROM错误，错误数据为零 |
| `o_rom_request_valid` | output | 1 | i_clk | rom_request_valid | 唯一ROM读口请求有效，等待ready时词地址保持 |
| `o_rom_request_addr` | output | 13 | i_clk | rom_request_addr | 20字节物理词号，合法0至7167 |
| `o_rom_response_ready` | output | 1 | i_clk | rom_response_ready | 消费当前ROM读响应；取消排空也必须握手 |
| `o_fault` | output | 1 | i_clk | fault | 本组件故障状态，不得发布为成功表 |

## 5. 周期行为与延迟

- IDLE接收并锁定所有身份；模型/exp范围错误返回error且不读ROM。18拍除20，注册word和lane。
- 单个ROM请求等待ready；返回低字节在高lane19时请求相邻词并拼接第二字节，否则单读。
- LUT响应身份/数据/error保持至消费；不接第二条查询；ROM fault粘滞到共同复位。
- cancel立即屏蔽客户端，已接受的无标签ROM读进入DRAIN，握手丢弃旧返回后才ready；不复位reader。

## 6. WaveDrom 时序图

### 请求所有权与停顿

协议示意：省略内部变长计算，用空白间隔表示；不是固定总时延。仅valid与ready同拍消费。

![请求所有权与停顿](waveforms/road_shared_lut_service_request-hold-response.svg)

- WaveJSON：[road_shared_lut_service_request-hold-response.json5](waveforms/road_shared_lut_service_request-hold-response.json5)

## 7. 边界、反压与错误

- 复位、取消、背压、非法身份和边界地址；取消不能当成无标签外设已排空

## 8. CDC 与综合约束

- Verilog-2001；一个未决事务；ready/valid握手；无TD/物理时序签核
- 不改变冻结算术核/数值，不复制公共存储

## 9. 验证与验收

- all1024sigmoid
- all256exp
- dynamic identities
- byte/lane/word boundaries
- odd relocation crossword
- request bubbles
- ROM request stalls
- delayed responses
- LUT response long hold
- cancel before ROM acceptance
- cancel while ROM pending and late response then restart
- cancel between crossword reads
- common reset during wait/response
- wrong model
- exp index256 and1023
- ROM fault

## 10. 可追溯性

- 规格模块：`road_shared_lut_service`
- RTL 路径：`rtl/road_shared_lut_service.v`
- 交付要求：本文档、WaveJSON 和 SVG 必须与同一版本规格一同发布。
