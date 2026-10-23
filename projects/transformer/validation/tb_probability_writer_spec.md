# tb_probability_writer 验证契约

对象为 `lesson14_transformer_full/rtl/probability_writer.sv`，保持 DUT 不变。
TB 无外部端口，内部 10 ns 时钟、低有效异步复位，输入在下降沿驱动。

## 组合写回与完成

- `in_ready` 恒为 1，无反压；`wr_en` 组合等于 `in_valid`。
- `wr_bank = row_idx % 4`，`wr_addr = (row_idx / 4) * seq_len + in_index`。
  验证合法形状 L=1/2/5/64 的全部位置，共 4126 个，其中 L=64 为 4096 个。
- 数据 oracle 使用整数 `(data + 1) / 2` 后限制最大值为 127，与 DUT 的移位和低位相加写法独立。
  单独穷举全部 256 个 U8 值，包含 253/254/255；255 的舍入结果 128 必须饱和为 127。
- `row_done` 在上升沿采样 `in_valid && in_last`，边沿后输出该值。
  连续有效末项允许 `row_done` 连续为 1；无效拍即使 `in_last=1` 也必须清零。
  下降沿改输入后 1 ns 检查旧 `row_done`，上升沿后 1 ns 检查新值，防止组合或额外延迟实现假通过。
- 数值、bank 和地址是组合输出，在 valid 气泡内也检查它们随输入变化；所有比较使用 `!==`。

## 复位与边界

异步复位只清除 `row_done`，不屏蔽组合 `wr_en`。TB 在已有完成输出时于非时钟边沿拉低复位，
检查完成立即清除，同时刻意保留 `in_valid=1`，确认组合写使能仍为 1。
实际系统若要求复位期间不写存储，必须由上游降低 `in_valid`。
之后降低 valid、解除复位并完成新输入，检查无陈旧完成输出。

测试包含连续有效输入、连续三个 L=1 行、行首和行内气泡、无效末项，以及复位后重启。
全局 watchdog 为 1 ms。该单元结论不覆盖真实 SRAM、综合、时序或 top 调度；
目前 top 使用 Softmax 的 `sm_done` 推进行，未消费 `p_row_done`。

## 完成信号时序示意

图中 `row_done_after_edge` 表示对应采样沿之后的值；此 WaveJSON 是说明，不是实测波形。

```json
{
  "signal": [
    {"name": "clk", "wave": "p....."},
    {"name": "in_valid", "wave": "011010"},
    {"name": "in_last", "wave": "01..0."},
    {"name": "wr_en", "wave": "011010"},
    {"name": "row_done_after_edge", "wave": "0110.."}
  ]
}
```

## 独立复现

在 `projects/transformer/lesson14_transformer_full` 中运行：

```powershell
iverilog -g2012 -s tb_probability_writer -o ../reports/tb_probability_writer.out rtl/probability_writer.sv ../validation/tb_probability_writer.sv
vvp ../reports/tb_probability_writer.out
```

成功标志为 `PASS PROBABILITY_WRITER`。运行同一二进制加 `+CORRUPT_EXPECTED`，
会有意改错首个数据期望并必须非零退出，用于验证数值断言确实生效。
