# tb_tiled_gemm：GEMM 独立回归契约

本测试平台保持工程现有 SystemVerilog 方言。被测模块为 `tiled_gemm_4x4_banked_compact`，配合真实 `mac_array_4x4`，不改 RTL、端口或时序。`clk` 周期 10 ns，`rst_n` 低有效异步复位；整个测试只复位一次，随后连续启动 10 个任务。

## 输入、布局与独立 oracle

`gen_gemm_unit_vectors.py --out-dir <目录>` 使用 Python 标准库生成 `cases.txt`、分 Bank 的 INT8 `a.hex/b.hex`、INT32 `expected.hex` 和 `summary.json`。期望值通过数学 A/B 上的三重循环整数点积计算，不调用 RTL 或已有 GEMM Python 实现。B 转置源仅改变物理布局，数学运算始终为 A[M,K]×B[K,N]。测试以 `+VECTORS=<目录>` 读取全部任务。

| 组 | 覆盖 |
|---|---|
| single/tile | 1×1×1、4×4×4；负乘积、完整 Tile |
| edge/edge_transposed | 5×7×6；M/N/K 均非整 Tile，B 两种物理布局 |
| long_k/long_k_transposed | 5×7×256；±INT8 极值，正负结果超 INT16 范围，最大 4194304、最小 -4161536 |
| missing_a/missing_b | 分别丢掉第一个有效 A/B bank 0 响应；另外一侧照常响应 |
| recover_a/recover_b | 注错任务结束后不复位，下一合法 start 清除错误标志并通过数值核对 |

一次仿真完成 8 个合法数值任务（174 个逐项结果）和 2 个协议注错任务。固定一周期存储按请求上升沿 NBA 更新 data/valid，DUT 下一沿捕获。注错结果明确为 `numeric=NOT_CHECKED`；只验证错误在预期捕获后置位、直到下次 start 保持，并检查最终完成和写回结构，不将错误任务认定数值通过，不增加 abort/retry 行为。

## 检查点与结束条件

- 根据独立读拍计数重建逻辑 Tile 和 K 次序，核对每个物理 Bank 的 en/address；无效行列不读、K 尾部不额外读，总 A/B 读次数必须精确匹配。
- 每个输出检查 row/col 范围、线性地址、只写一次、总次数 M×N；正常任务逐项比较 signed INT32。
- 任务期间 busy 保持；正常任务 bad_dim 和 mem_protocol_error 为零；done 单拍且在最后写入后、所有结果完成后才出现；完成后无额外读写。
- 每任务 watchdog 20000 拍；所有 case 与期望数量都核对，成功最终打印 `PASS GEMM_UNIT`，失败 `$fatal(1, ...)`。
- 每个任务载入前将数据和 oracle 清为 X，检查实际读取数据与全部期望值均已知；每个非复位沿拒绝未知控制信号，避免缺失向量或 X 同比造成假通过。

```json
{"signal":[{"name":"clk","wave":"p......"},{"name":"start","wave":"010...."},{"name":"busy","wave":"0.1..0."},{"name":"rd_en","wave":"0.10..."},{"name":"rd_valid_after_edge","wave":"0.10..."},{"name":"capture_at_edge","wave":"0..10.."},{"name":"c_wr_en","wave":"0...10."},{"name":"done","wave":"0....10"}]}
```

本回归只证明上述有界样例和固定一周期读接口；不覆盖最大 M/N、所有维度组合、可变延迟接口、综合/时序或实际 SRAM 宏。
