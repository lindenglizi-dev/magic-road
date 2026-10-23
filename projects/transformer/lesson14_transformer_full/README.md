# 第 14 课：统一单头 Attention + FFN 系统（教学 RTL）

本工程基于 Lesson 12 `full_attention_top.sv` 修改；复用 Lesson 13 的 `ffn_relu_requant.sv`。
**只有一个** `tiled_gemm_4x4_banked_compact` GEMM 实例。课设所需的完整端到端 **RTL 仿真尚需实际执行**；本环境完成的仅是 Python Golden Model、生成向量及结构级检查。

## 控制阶段

- Phase 0: Q=X·WQ, `L×D = (L×D)(D×D)`
- Phase 1: Key=X·WK
- Phase 2: V=X·WV
- Phase 3: Score=Q·Keyᵀ, `L×L`
- 独立 Softmax：Score 逐行 → `P`（按行四 Bank、UINT8→signed INT8）
- Phase 4: Oacc=P·V, `L×D` 的 INT32；附加 INT32→INT8 移位饱和输出到 Attention Activation Bank
- Phase 5: Hraw=O8·W1, `L×F`；ReLU + shift/saturation，写 Hidden Bank
- Phase 6: Y=H·W2, `L×D` INT32，写 final Y。

## 关键存储映射

- A / Q / P / O8 / H：`bank=row%4`, `addr=(row//4)*cols+col`
- WQ/WK/WV / W1/W2 / V：`bank=col%4`, `addr=row*ceil(cols/4)+col//4`
- Key 转置模式：读取 Key 的行优先物理 Bank，即 B 的逻辑列 `col` 对应原 Key 行 `col`。
- 同一权重存储器提供 QKV 和 FFN 两套权重；配置寄存器分别选择 `w1_base`、`w2_base`。
- `x_sparse.hex` 与 `weights_sparse.hex` 使用标准 Verilog `$readmemh` 的 `@address` 指令，直接对应测试平台 `bank*65536 + local_addr` 物理地址；修正旧教学用紧凑文件与 Testbench Bank 跨度不匹配的问题。

## 接口时序限定

- 每个读 Bank 在请求发出后的下一个时钟提供数据+valid；**不支持可变延迟**。
- 写存储器不提供反压；一个有效写入每拍都必须被接受。
- QKV、Attention 和 FFN1 的单级后处理寄存器保留地址、数据与任务标签；顶层等待 `DRAIN` 再切换 Phase。
- `cfg_hidden_dim` 取 `1..256`，`cfg_seq_len` `1..64`，`cfg_dim` `1..256`。

## 实际运行

```bash
bash scripts/run_python.sh
bash scripts/run_iverilog.sh
```

`run_iverilog.sh` 会对四组 case 编译一次 RTL、运行四遍 TB，并在任意结果错误时 `$fatal`；需要本机 `iverilog` 和 `vvp`。ModelSim 可执行：

```tcl
vsim -c -do scripts/run_modelsim.do
```

仿真测试包括：QKV/Score/P/PV/Attention量化/Hidden/FFN 最终结果，7 次 GEMM 发射计数、非整 Tile、写地址正确与重复写入检测，以及 1,000,000 周期 watchdog。

## 哪些还没有完成

- RTL 编译/仿真成功状态需以工具运行结果为准；当前仅参考模型通过。
- 不含训练模型 scale/zero point、LayerNorm、残差连接、偏置、Dropout。
- 不含 Croc OBI 接口、商业 SRAM 宏或完整的开源 ASIC 后端结果。
- 未进行功耗、面积、最大频率测量。
- 本版独立的外部 Bank SRAM 是 Testbench 仿真模型，不能直接称为可实现的完整 SoC 内存系统。

优先级建议：先在 ModelSim/Verilator/Icarus 跑通并保存波形、日志，然后检查 RAM 实现和综合面积；不要在验证缺口尚存时继续增加新模块。
