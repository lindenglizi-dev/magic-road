# tb_gemm_control：GEMM 启动与复位恢复回归

沿用工程 SystemVerilog 风格，使用真实 `tiled_gemm_4x4_banked_compact` 与 `mac_array_4x4`。时钟 10 ns，`rst_n` 低有效异步复位；无额外向量文件或依赖。固定一周期 SRAM 根据公开物理地址解码逻辑行列，返回 `A[r,k]=2r-k-5`、`B[k,c]=k+3c-6`。输出 oracle 用三重循环整数点积，与 DUT 的 Tile/缓冲索引无关。

- 六次非法启动分别覆盖 M/N/K=0 与 257。检查拒绝 busy/done/读写、计数器清零、`bad_dim` 保持，下一合法 start 清除标志。
- 基线 5×7×8 与三个同配置任务分别在待捕获读响应、首个 MAC 后和已接受首个输出的 STORE 阶段插入 busy start 脉冲。配置维度与布局全程保持稳定，检查所有数值、地址、唯一写入、总次数、单拍 done 与基线总周期一致；完成后继续观察，拒绝额外任务。
- 在以上三个阶段分别异步复位，检查复位期间立即静默、状态/计数清零以及释放后无旧读写/done。随后各运行一个 2×3×5 合法任务并核对全部数值，验证清除旧累加与在途响应后的恢复。
- 所有有效读写要求 busy，拒绝未知控制/输出和协议错误；每个阶段与完成等待都有 watchdog。共 6 个非法任务、7 个正常完成任务、3 个复位取消任务。

顶层 `tb_gemm_control`，无参数正例成功打印 `PASS GEMM_CONTROL`。加 `+CORRUPT_EXPECTED` 后仅损坏第一个输出的期望值，应以数值不匹配 `$fatal` 非零退出。被复位取消的任务只核对复位前已实际发出的写回，不要求取消后的完整矩阵或 done。

```json
{"signal":[{"name":"clk","wave":"p........"},{"name":"start","wave":"010.10..."},{"name":"busy","wave":"0.1....0."},{"name":"rd_en","wave":"0..10...."},{"name":"rd_valid","wave":"0...10..."},{"name":"rst_n","wave":"1.....01."},{"name":"done","wave":"0........"}]}
```

范围限定：busy 时 start 仅是稳定配置下的额外脉冲，不将端口维度可在 busy 中改变、start 持续跨越空闲边界、可变读延迟或 SRAM 宏行为视作保证。
