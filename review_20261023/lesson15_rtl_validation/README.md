# Lesson 15：Transformer RTL 真正的验证门禁

目标：停止增加新模块，确认 Lesson 14 的共享 GEMM + Attention + FFN 可以通过实际 HDL 编译、仿真。**这个包不声称已经完成 HDL 仿真或 ASIC 布局布线。**

## 来源与修改范围

- `lesson14_transformer_full/`：从上一课 ZIP 原样解压的全部工程（含四组向量）。
- **所有 `rtl/*.sv` 保持不变**；`reports/rtl_sha256.json` 保存源码哈希。
- 修复 `reference/check_contracts.py`：从遗留 `full_attention_top.sv` / `u_requant` 改为当前实际 `transformer_block_top.sv`、`u_attn_requant`、`u_ffn_requant`。这是测试脚本修复，不是设计功能修复。
- 新增 `validation/tb_mac_smoke.sv`，覆盖 INT8 符号乘法、clear 优先级、停顿保持、120 拍随机输入。
- 新增一键执行入口 `scripts/validate.py`，对检查明确区分 PASS、FAIL、SKIP。

## 最短路径（在本目录）

```
python3 scripts/validate.py
```

如果有 `iverilog` 和 `vvp`，上述脚本会依次执行：Python Golden Model、静态接口与 Bank 布局检查、MAC 定向 + 随机 RTL Testbench、Transformer 顶层四组 RTL 用例。

如果没有仿真器，返回 `gate=RTL_UNVERIFIED`；并不意味着 RTL 通过。要让 CI 因未跑过 RTL 而失败：

```
python3 scripts/validate.py --strict
```

Windows/ModelSim：在 `lesson14_transformer_full/` 目录打开命令行执行：

```
vsim -c -do ../validation/run_modelsim_all.do
```

可选：在装有 Yosys + slang 插件时运行 `bash validation/run_yosys_mac.sh`，只对计算核做不映射工艺库的综合检查；**不是**课设要求的 IHP 130nm 真实 PPA，更不是 GDSII。

## 四组测试及验收

| case | 规模 | 目的 |
|---|---|---|
| demo | L=2 D=4 F=6 | 完整 Attention + FFN 数据流 |
| edge_5x7 | L=5 D=7 F=9 | 非整 4x4 Tile、Bank 边界 |
| random_00 | L=1 D=9 F=5 | 长 K、短序列、随机权重 |
| sat_1x1 | L=1 D=1 F=3 | 极小维度与量化边界 |

完整顶层通过标准：Testbench 的 `PASS TRANSFORMER BLOCK ...`，7 次 GEMM 发射、全部有效地址/写回次数、所有数据与 Golden Model 相等，仿真无 `$fatal`、无超时。

## 调试顺序

1. 先看 `reports/mac_compile.log`，解决 SV 语法/工具兼容。
2. 再看 `reports/mac_rtl.log`，排除符号位、clear、valid 控制错误。
3. 再看 `reports/top_compile.log`，核对 top 所有端口。
4. 单独分析 `reports/rtl_demo.log` 的第一处 `$fatal`。不要同时改多个状态机。
5. demo 通过后检查 edge、random、sat。所有用例通过后再进入 Yosys/IHP 工艺综合。

## 工艺验证尚需什么

- Yosys + `yosys-slang`、IHP 130 nm 开源 PDK、合理时序约束。
- OpenROAD 布局/CTS/布线/时序报告，DRC、LVS、GDSII。
- 物理 SRAM macro 或经过实际综合的存储实现。当前 Testbench 数组不是已映射 ASIC SRAM。
