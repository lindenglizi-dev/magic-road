# transformer_block_top：控制与错误恢复契约

接口保持现有 `transformer_block_top.sv`：单时钟、低有效异步复位；
配置输入为 `cfg_*`，存储采用固定一周期 data/valid 读响应、无背压写回。
七个 GEMM 阶段依次为 Q、Key、V、Score、PV、FFN1、FFN2。

- 空闲且 start 为高时采样配置。合法配置锁存后进入 busy；运行期间的短 start 脉冲不排队。
- 非法配置保持空闲、产生一拍 done 并置 sticky error，不发存储请求。
- 合法任务结束时产生一拍 done；error 表示本次运行失败，故障任务的输出不能当作正确数值使用。
- GEMM 的 bad_dim/mem_protocol_error 在下一次子模块 start 时清除。顶层只在
  WAIT_GEMM/DRAIN 捕获它们，避免 IDLE/ISSUE 的旧标志污染新任务；Softmax error 处理保持原语义。
- 下一合法 start 清除顶层 error；当新任务产生真实错误时仍重新置位。
- 异步复位取消在途任务，清除控制/流水状态与输出有效位；不承诺清除外部 SRAM 内容。
  复位解除后须重新启动完整任务，旧任务不再补发 done。
- start 是空闲电平采样；若一直保持到下一次空闲，会被视为另一请求。

本轮修复的触发场景：第一项 Q 投影缺少一个必需读响应，顶层错误完成；
随后不复位直接合法启动。旧实现会在 ISSUE 重新采入 g_memerr，导致新任务提前失败。
修复只限制错误标志的采集阶段，没有新增状态、寄存器或改变存储延迟。

```json
{"signal":[{"name":"clk","wave":"p....."},{"name":"state","wave":"======","data":["IDLE","ISSUE","WAIT_GEMM","WAIT_GEMM","DRAIN","FINISH"]},{"name":"start","wave":"10...."},{"name":"g_start","wave":"010..."},{"name":"old_g_memerr","wave":"1.0..."},{"name":"new_job_error","wave":"0....."}]}
```

图为状态采样示意，非实测波形。验证入口为 `python run_checks.py`：四组正常整链向量
以及 `tb_transformer_block +CASE=vectors/demo +CONTROL`。控制回归同时检查非法配置、
busy start、关键阶段复位和运行时错误后的无复位恢复；仅为本地 RTL 功能证据。
