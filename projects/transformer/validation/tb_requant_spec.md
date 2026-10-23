# requant 独立回归契约

对象为 `requant_shift_sat.sv` 和 `ffn_relu_requant.sv`；使用现有 SV 接口，不修改功能 RTL。
两模块共享输入，时钟周期 10 ns，低有效异步复位。

- 每个上升沿采样 `in_valid`；NBA 后输出有效位等于该输入有效位。
- `requant_shift_sat` 输出为 `clamp(floor(raw / 2**shift), -128, 127)`；
  `saturated` 仅在截断前整数小于 -128 或大于 127 时置位。
- `ffn_relu_requant` 输出为 `clamp(floor(raw / 2**shift), 0, 127)`。
- valid 时 raw、phase、addr 和 FFN row/col 与本拍采样输入一致；无 ready，接收端逐拍接收。
- invalid 时输出 valid 为零，其余输出寄存器保持。输入改变不得在上升沿前改变输出。
- 异步复位在非时钟沿立即清除全部输出；复位期间 valid 输入不能泄漏到复位后的输出。

顶层投影和 Attention 使用前者，FFN hidden 使用后者。这里验证模块标签流水；
实际 Q/Key/V/Hidden bank 组合写回仍由顶层回归验证。

`gen_requant_vectors.py` 使用 Python 无界整数 `//` 独立计算 floor，覆盖 shift 0..31、
INT32_MIN/MAX、-1/0/1、正负量化边界及相邻值、可表示的正负饱和边界及相邻值，
每个 shift 另有固定种子随机输入。shift 24..31 不存在可表示的 INT32 饱和输入；
shift 31 结果只能为 -1 或 0。标签覆盖 18 位地址高位、四个 phase、9 位 row/col 边界。

TB 每个向量同时检查两个模块：下降沿驱动，1 ns 后验证输出仍为旧值，
上升沿后 1 ns 对拍全部输出。连续有效输入之间按确定规则插入改变 payload 的气泡，
在有效输出期间再次异步复位，然后继续未处理向量。结束前补三拍无效输入，禁止额外有效输出。
文件头声明向量数量，TB 拒绝缺少文件、缺失字段、未知值、越界、截断和尾部额外数据，
并确认精确输出数量、32 个 shift、气泡、连续 valid 及两次复位均执行。全局 watchdog 1 ms。

```powershell
python projects/transformer/validation/gen_requant_vectors.py
iverilog -g2012 -s tb_requant -o projects/transformer/reports/requant_unit.vvp projects/transformer/lesson14_transformer_full/rtl/requant_shift_sat.sv projects/transformer/lesson14_transformer_full/rtl/ffn_relu_requant.sv projects/transformer/validation/tb_requant.sv
vvp projects/transformer/reports/requant_unit.vvp +VECTORS=projects/transformer/reports/requant_unit_vectors/cases.txt
```

可用 `--out-dir` 指定向量目录；TB 的 `+VECTORS` 为文件路径。成功标记为
`PASS REQUANT_VECTORS` 和 `PASS REQUANT_UNIT`。`.sv` 不适用仅扫描 `.v` 的样式门禁。

以下 WaveJSON 是协议示意，不是实测波形：

```json
{"signal":[{"name":"clk","wave":"p...."},{"name":"in_valid","wave":"01101"},{"name":"in_payload","wave":"x====","data":["A","B","bubble changes","C"]},{"name":"out_valid_after_edge","wave":"01101"},{"name":"out_payload_after_edge","wave":"0==.=","data":["A","B","C"]}]}
```
