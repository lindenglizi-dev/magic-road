# tb_softmax_row 验证契约

对象为 `lesson14_transformer_full/rtl/softmax_row_int32.sv`，不修改 DUT 算法或端口。
本 TB 无端口，内部 10 ns 时钟，低有效异步复位。所有输入在下降沿驱动，
上升沿 NBA 前检查传输，NBA 后 1 ns 检查 `done/error/busy`。

## 输入、输出与完成

- `start=1` 且空闲时锁存 `seq_len` 和 `scale_q16`；合法长度 1..64、scale 1..65536。
- 输入仅在 `in_valid && in_ready` 时接收，整行收齐后才能输出。
- 输出按 index 0..L-1，每项与 Python 黄金逐元素比较，最后一项必须 `out_last=1`。
- 输出阻塞时 `out_valid/out_data/out_index/out_last` 保持稳定，包括最后一项。
- 最后一次 `out_valid && out_ready` 传输后，`done=1`、`busy=0`，下一拍 `done=0`。
- 非法启动只产生一拍 `error`，不进入 busy、不接收输入、不产生输出。
- 中途复位取消当前行，清除协议状态；随后新任务不能收到旧行输出。

## 数值和测试范围

`gen_softmax_vectors.py` 调用既有 `reference/softmax_fixed.py` 的
`softmax_fixed` 与 `approximate_exp_weights`。实际 ROM 的全部 129 项另与数学 LUT 比较。
输入以有符号 INT32 十进制存储，黄金为无符号 0..255；检查指数和 `dbg_exp_sum`。
不要求量化后概率和恒为 255，例如两项相等输出 128、128，和为 256。

| case | 长度 | scale | 重点 |
|---|---:|---:|---|
| single_min_scale | 1 | 1 | 单元素、INT32_MIN |
| extreme_pair_full_scale | 2 | 65536 | INT32_MIN 与 INT32_MAX 的 33 位差 |
| extreme_pair_min_scale | 2 | 1 | 极值反序、最小 scale |
| equal_pair | 2 | 65536 | 相等值、独立舍入 |
| equal_max_row | 64 | 65536 | 最大长度、指数和上界 |
| bounded_full_scale | 64 | 65536 | 固定种子随机有界 score |
| bounded_min_scale | 64 | 1 | 最小 scale、固定种子随机 score |
| lut_clamp_boundary | 64 | 4096 | LUT 索引 127/128/129 和低于 -8 截断 |
| mixed_extremes | 64 | 65536 | 极值、零、负一交错 |

九组无复位连续完成；每个输入前插入 1..3 拍 valid 气泡，每个输出至少阻塞三拍。
另测试长度 0/65 和 scale 0/65537 四次非法启动，在一个有效输出被阻塞时复位，
然后重新完成最后一组。共十行、391 个成功输出；所有关键比较使用 `!==` 避免 X 假通过。
每项等待最多 1000 拍，全局 watchdog 为 1 ms。

## 最后一个输出被阻塞的时序示意

图中数据在采样边沿前表示；`done` 是该边沿 NBA 后的结果。

```json
{
  "signal": [
    {"name": "clk", "wave": "p......"},
    {"name": "out_valid", "wave": "01...0."},
    {"name": "out_ready", "wave": "0...10."},
    {"name": "out_last", "wave": "01...0."},
    {"name": "out_data/index", "wave": "x=...x.", "data": ["last golden / L-1"]},
    {"name": "busy_after_edge", "wave": "1...0.."},
    {"name": "done_after_edge", "wave": "0...10."}
  ]
}
```

此 WaveJSON 为协议说明，非实测波形；通过结论以仿真日志为准。

## 独立复现

工程根目录运行生成器：

```powershell
python projects/transformer/validation/gen_softmax_vectors.py
```

在 `projects/transformer/lesson14_transformer_full` 中编译、运行：

```powershell
iverilog -g2012 -s tb_softmax_row -o ../reports/tb_softmax_row.out rtl/softmax_row_int32.sv ../validation/tb_softmax_row.sv
vvp ../reports/tb_softmax_row.out +VECTORS=../reports/softmax_unit_vectors/cases.txt
```

通过标志 `PASS SOFTMAX_ROW`。向量生成、编译和运行必须分别成功，不能用 Python 通过代替 RTL 仿真。
仿真边界：单时钟功能与协议验证，不证明综合、真实存储、时序收敛或物理实现。
