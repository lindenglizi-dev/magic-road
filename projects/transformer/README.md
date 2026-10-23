# Lesson 15：Transformer RTL 真正的验证门禁

目标：确认 Lesson 14 的共享 GEMM + Attention + FFN 可以通过实际 HDL 编译、仿真。**2026-10-23 已完成 Icarus 编译、MAC 测试和四组顶层 RTL 对拍；ASIC 综合及布局布线仍未完成。** 实测命令、返回码和日志见 `reports/summary.json`。

## 来源与修改范围

- `lesson14_transformer_full/`：基于上一课 ZIP 的工作副本（含四组原始向量）；原始快照在工作区 `review_20261023/`。
- 本轮只将 GEMM 的双层 A/B ping-pong 数组展平，修复 Icarus 动态索引内部断言；端口、状态机、复位、算术和周期保持不变。当前哈希见 `reports/rtl_sha256.json`。
- 补齐顶层 TB 的 `q_wr_data/key_wr_data/v_wr_data` 声明，补 Q/Key 物理 Bank 逐点对拍；Python 参考从 X/W 重算 raw 和 QKV 后再检查 Attention/FFN，覆盖 573 个值。
- `static_contracts.py` 的端口名字出现检查仅作源文本检查；声明和位宽以真实 HDL elaboration 为准。
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

本轮四例周期数依次为 **244 / 1178 / 486 / 139**，均从 TB 释放复位起计数，包含发射前空拍，不能直接称为核延迟或推算物理频率。只覆盖表中小例；维度上界、非法配置、复位中断、多次任务、Softmax 输出反压尚未作为独立系统回归完成。

应通过 `scripts/validate.py --strict` 运行：它先解析并重算 Golden 文件，再编译和仿真。直接 `vvp` 不替代 Golden 文件预检。Windows 执行沙箱曾使该 Icarus 驱动返回 `3221225477` 或 `1`，完整 HDL 回归在获准的宿主执行上下文中通过；不要忽略非零返回码，也不要直接使用崩溃后遗留的 `.out`。

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
