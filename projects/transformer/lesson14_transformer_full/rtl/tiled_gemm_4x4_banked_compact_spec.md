# tiled_gemm_4x4_banked_compact：本轮修复规格

模块接口见同名 `.sv`：`clk` 上升沿；`rst_n` 低有效异步复位。`start` 在空闲时采样，任务期间调用方须保持维度和源布局配置稳定。维度均为 1..MAX_DIM（当前顶层 MAX_DIM=256）。不改变任何端口或时序。

| 接口组 | 契约 |
|---|---|
| start / m_dim / n_dim / k_dim / b_src_transposed | 启动 M×K 乘 K×N；B 可使用转置源布局 |
| a/b_rd_en、a/b_rd_addr、a/b_rd_data、a/b_rd_valid | 四个独立 INT8 读 Bank，每个有效请求固定一周期响应；缺失响应置 mem_protocol_error |
| c_wr_en / c_wr_row / c_wr_col / c_wr_addr / c_wr_data | INT32 C 写回，接收方每个有效周期均接受，无 ready |
| busy / done / bad_dim / mem_protocol_error | 忙、单拍完成、非法维度和读响应错误 |
| cycles_* / dbg_* | 原周期计数和 tile/loader/MAC 状态输出；语义不变 |

算术为 16 路 signed INT8×INT8，累加到 signed INT32。A/B 双缓冲仍各为 2×16 字节；本轮由 `[bank][offset]` 改为 `[16*bank+offset]`，全量复位、响应捕获、补零、MAC 读取一致替换。对 bank∈{0,1}、offset∈[0,15]，映射为 [0,31] 的双射；两 bank 不混叠。未改变 MAC 次序、补零、缓冲释放、状态机、复位值或延迟。

## 固定读响应示意

```text
上升沿                 t                 t+1                 t+2
读请求                 req0              req1                req2
存储模型 NBA 后        data0/valid0      data1/valid1        data2/valid2
GEMM 本沿采样          上一响应          data0/valid0        data1/valid1
```

```json
{"signal":[{"name":"clk","wave":"p...."},{"name":"rd_en","wave":"01..0"},{"name":"rd_addr","wave":"x345x","data":["req0","req1","req2"]},{"name":"rd_valid_after_edge","wave":"01..0"},{"name":"capture_at_edge","wave":"001.."}]}
```

现有 TB 的 SRAM 在请求边沿以 NBA 更新响应，GEMM 在下一边沿捕获；本轮没有引入竞态修复。因原源码是 SystemVerilog，本轮按项目方言保留 `.sv` 与 `always_ff`，不进行 Verilog-2001 风格重写。

## 验证与限制

运行 `python projects/transformer/scripts/validate.py --strict`：MAC smoke、demo、edge_5x7、random_00、sat_1x1 均实测 PASS。四组顶层分别经过 Q/K/V、Score、PV、FFN1、FFN2 七次 GEMM，核对原始值及中间张量和 Bank 布局。当前只证明这些尺寸与固定一周期接口；不等同形式等价证明、上界回归、综合或实际 SRAM 映射。外部仿真日志与严格风格检查为独立证据。
