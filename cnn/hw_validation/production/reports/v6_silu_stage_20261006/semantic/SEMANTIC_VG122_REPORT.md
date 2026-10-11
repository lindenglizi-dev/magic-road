# SiLU 阶段二 VG122 语义闭合报告

日期：2026-10-06  
角色：`verify`  
状态：四项语义已闭合；官方 ModelSim 定向断言与固定回归通过预期；严格交付门仍失败。

## 1. 边界与冻结对象

- 只新增本目录中的 Python 参考、仿真 testbench、规格/WaveDrom、日志和报告。
- CEA DUT 只读：`../../v3_silu_stall_candidate_20261005/silu_shared_unit.v`，SHA256 `5f357b493c7b3f941d9fa954a0ce5ec09091e466b641474360d2f64d0e42c938`。
- 该 DUT 与 v4 `candidate/silu_shared_unit.v` 的 SHA256 相同。
- 原版负例 DUT：v4 `original/silu_shared_unit.v`，SHA256 `ee9beb80decb4f276b9ff81214c22f044a71ac1ffc8c72beb1378e6ddb07a7ed`。
- 未修改 DUT、checker、生产 RTL、TD/Flash、训练数据、约束或时序例外；未运行 TD、上板、训练或 Flash。
- 本工程不是 Git 仓库，无分支/提交可记录。
- 未使用形式工具。下文“闭合”表示源码不变式推导加官方模型断言仿真，不表示形式证明。

## 2. 四项 VG122 逐项结论

### 2.1 `cnt_table_expected + 11'd1`

源码：冻结 DUT 第 82、274-286 行；VG122 算术点在第 283 行。

状态转移：

1. 复位为 0。
2. 地址 0 握手是重启，下一状态为 1。
3. 仅当非零地址等于当前期望且不等于 1023 时加 1。
4. 地址 1023 合法提交后回到 0；任何错序握手也回到 0。

因此精确可达集合是 `0..1023`，`1024` 不可达。11 位加法的潜在进位在可达状态和更新条件下不会发生。Python 顺序遍历和逐拍 testbench 断言均覆盖全部 1024 个合法装载地址。

结论：语义闭合，保留冻结 11 位实现，不做位宽修改。

### 2.2 `cnt_pending + 3'd1`

源码：冻结 DUT 第 83、293-300 行；VG122 算术点在第 296 行。

真实容量不是 3 位编码上限 7，而是以下六个 valid 存储级：

1. `flag_input_valid`
2. `flag_round_valid`
3. `flag_value_valid`
4. `flag_address_valid`
5. `flag_ram_valid`
6. `output_valid_o`

复位时六级与 `cnt_pending` 都为 0。流水推进时，六级 valid 之和的下一值等于旧值加输入握手、减输出握手；停顿时六级和计数同时保持。输出级被阻塞后 `flag_pipeline_enable=0`，从而 `o_input_ready=0`，不能接收第七个事务。可达范围为 `0..6`。

结论：`+1` 只可能从 `0..5` 发生，结果最大 6，不发生 3 位溢出。

### 2.3 `cnt_pending - 3'd1`

源码：冻结 DUT 第 297 行。

输出握手要求 `output_valid_o=1`，而该位本身属于六级 valid 和，因此输出握手前 `cnt_pending >= 1`。仅输出握手使计数减 1；同拍输入/输出保持；停顿保持；异步复位将计数和六级 valid 一并清零。地址 0 重载只在 `cnt_pending=0` 时开放，不会取消在途事务；当前实现中只有复位执行取消。

结论：`-1` 只可能从 `1..6` 发生，结果最小 0，不发生下溢。

### 2.4 `reg_rounded_value + 16'sd512`

源码：冻结 DUT 第 94、482-486 行；VG122 算术点在第 484 行。

RTL 先对有符号 INT16 输入除以 4 向负无穷取整，再按低两位执行最近偶数舍入，最后加 512。穷举全部 65536 个输入得到：

- 完整有符号 lookup 范围：`-7680..8704`，在 signed 16 位内无溢出。
- 非旁路中央输入 `-2047..2047` 的 lookup 范围：`0..1024`。
- lookup 0 对应 raw `-2047/-2046`。
- lookup 1024 对应 raw `2046/2047`。
- raw `<= -2048` 走负尾输出 0；raw `>= 2048` 走正尾原值旁路。

lookup 1024 是读取路径的特殊端点，不是表写地址。物理 RAM 地址端口只有 10 位，特殊端点的低 10 位会读地址 0，但对齐的 `reg_ram_address==1024` 在输出级选择常量 2047，RAM 读值被丢弃。表写地址仍严格是 `0..1023`。

结论：语义闭合，16 位 signed 目标足够；不能把 lookup 1024 与合法表写地址混为一谈。

## 3. 定向断言覆盖

新增 `tb_silu_semantic_assertions.v`，只通过层次观察冻结 DUT，不修改其接口或行为。主要断言：

- 每拍 `cnt_pending ==` 六个真实 valid 位之和。
- `cnt_pending(next) = cnt_pending + accepted - consumed`。
- 满六级后反压冻结，不能接收第七个事务；恢复时同拍进出保持 6。
- 仅输出时递减，排空回 0；异步复位取消 3 个定向在途事务。
- `cnt_table_expected <= 1023`，并逐拍核对重启、顺序推进、末项提交和错序回零。
- 错序地址 2 产生 fault 且不触发物理写；日志保留 `TB_EXPECTED_NEGATIVE`。
- 定向 raw 覆盖 lookup `-7680、0、1024、8704`，并检查中央域范围。
- CEA 停顿期间全部控制/载荷寄存器及官方 RAM 输出保持。

官方 ModelSim 结果：

```text
TB_EXPECTED_NEGATIVE wrong_order_address=2 physical_write_suppressed=1
TB_PASS_SEMANTIC pending_capacity=6 table_expected_max=1023 legal_write_range=0..1023 lookup_full=-7680..8704 lookup_central=0..1024 endpoint1024_special=1
```

日志：`semantic_assertions_retry.log`。官方模型原始 `INIT_FILE` 越界告警保留，未屏蔽。首次 `-modelsimini .\modelsim.ini` 写法失败的 `semantic_assertions.log` 也保留。

## 4. v5 固定官方模型回归复跑

| 用例 | 对象 | 期望/实测标记 | DUT 状态 |
|---|---|---|---|
| 00 | 原版，STALL=0 | `TB_PASS stall=0 accepted=9 received=9 errors=0` | PASS |
| 01 | 原版，STALL=1 | `TB_FAIL_CONTRACT ... errors=2`，含 RAM freeze error 与 raw=4 mismatch | 预期负例复现 |
| 02 | CEA，STALL=1 | `TB_PASS_CONTRACT ... freeze_checks=1 ... errors=0` | PASS |
| 03 | CEA，STALL=16 | `TB_PASS_CONTRACT ... freeze_checks=16 ... errors=0` | PASS |
| 04 | CEA，STALL=32 | `TB_PASS_CONTRACT ... freeze_checks=32 ... errors=0` | PASS |
| 05 | CEA，STALL=64 | `TB_PASS_CONTRACT ... freeze_checks=64 ... errors=0` | PASS |
| 06 | CEA，INT16 全域 | `TB_PASS inputs=65536 latency=5 ii=1 ... legal_writes=3072` | PASS |
| 07 | CEA，seed=42 随机反压 | `TB_PASS_RANDOM ... accepted=4096 received=4096 stall_cycles=1353 max_stall=7` | PASS |

所有 `vsim` 进程退出码均为 0；用例 01 的 DUT 状态由 TB 标记判为预期失败，未把进程码冒充 DUT 通过。最终日志为 `fixed_final_case_00.log` 至 `fixed_final_case_07.log`，case 00-05 的 CSV 同目录保存。命令虽显式请求 `-wlf`，本次 ModelSim 批处理未实际生成 `.wlf` 文件，因此不声称保存了波形数据库。

首次使用反斜杠绝对 `modelsim.ini` 路径的四次 setup 失败日志 `fixed_case_00.log` 至 `fixed_case_03.log` 保留；绝对 TRACE 超过旧 TB 128 字符向量而失败的 `fixed_retry_case_00.log` 也保留。最终复跑改用短相对 TRACE 路径，不改测试台。

## 5. 实例、驱动和组合依赖检查

- 冻结 CEA DUT 与官方 `PH1P_LOGIC_ERAM`、`PH1P_PHY_GSR` 在 ModelSim 2020.4 编译为 0 error/0 warning。
- 四个 VG122 目标各自由单一时序 always 块驱动；未发现多驱动。
- 计数更新依赖握手 wire，lookup 更新依赖已寄存舍入值；相关依赖跨寄存器切断，未发现组合环。
- 官方模型仿真能正确展开并运行全域与反压用例，未触发“不能保证设计可正确展开则停止”的条件。
- 这不替代 TD 映射、布局布线、硅上初始化或时序证据。

## 6. 严格门与公开八项状态

冻结 DUT/checker 未变化，因此 v5 的 167 最终严格计数仍是生产交付依据，本工作不把它改成 PASS。

对新增 testbench 运行 strict generated-deliverable gate，结果 `delivery_ready=false`，工具摘要为 194 errors、0 strict warnings。其 formatter 对 testbench 的 `silu_shared_unit dut` 实例报 `unsupported_construct`，因此这是测试辅助门禁失败，不是 ModelSim 编译失败。报告保存在 `semantic_tb_strict_gate_retry.json/.md`。

| 公开检查 | 状态 |
|---|---|
| compile | failed（formatter parse） |
| ast | failed |
| readability | failed |
| comment | failed |
| naming | failed |
| profile | failed |
| testbench | passed |
| toolchain | not_requested（该门本身）；官方 ModelSim 外部证据另行实际运行并通过预期 |

`readable-python-generator` 与 `readable-script-generator` 未安装；Python 参考仅用标准库，未声称通过对应专用 strict gate。没有新增运行脚本。

## 7. 工具、输入与日志哈希

| 对象 | SHA256 |
|---|---|
| ModelSim `vlog.exe` | `39e7f5cbae66a5aa65a179f5ab8faee01a0c53dc838e5e2b76510ac6c77e80a6` |
| ModelSim `vsim.exe` | `011f110291dc69707d7118e8f8d712b91438e0c837f9bc10ce6bf53c1d048cfd` |
| 官方 `ph1p_logic_eram.v` | `70d89b70bdd51812ad86b91e88526b4604ebb117516efda5af976fcddb2e69af` |
| 官方 `ph1p_phy_gsr.v` | `787312a19b4007bef3b76986bce267966b2d04c1871290ce29905629e38f1524` |
| `silu_table.hex` | `05d6d7062a6b6d0c9178562168d7f8e1554182bb99878b85a0cb6faeb71a25a6` |
| `silu_expected.hex` | `4f6552528d4035f14203e9aafbf8142ad3de8cd5867a0cfdfdcacb5131b908e2` |
| `silu_semantic_reference.py` | `95b7a24023ba3ca812d81bade944cbf9a73428ac6dd1952a008b6ef9692c3398` |
| `semantic_reference_results.json` | `f6e29cc1d93b0c6e09a25ace6f11fb39615500205edbfee378020ee4d2e63f88` |
| `tb_silu_semantic_assertions.v` | `af8129b3aebb89edd03102cd7fc6a7e75fe15de97940cd142d871fe4d8f065d7` |
| spec Markdown | `79987d1b3ff0b8ca6517c2e10e46df9b1510e00357aac689b322cd3f70a3ba78` |
| WaveDrom JSON5 | `a3e32636808198fe967398aae8652788789e04fc1c18fd4fec14dfa07608c0b0` |
| WaveDrom SVG | `9a0bf61464571b6cb8ac2c929753af756612715231a218809e369f171b610a03` |
| semantic assertion log | `7ed358c5b9a41f3a5ae24d576454c3ed8a4b6db20463663e505bb30288c397ee` |
| strict gate JSON | `3d98911934f518e733f7ceb0cc7dbb5b19493853676ab27f3b298c22634ad2e9` |

固定最终日志 SHA256：

```text
case00 d91ef1fdc2341b54d42c4b10c0a3d5458985a5a4c1a7e1b5632832eb8ee02251
case01 245bf3c49d4660a7e9013366486704c717f1919929065d42df09f4131cbf5aca
case02 b2178ccadbeadea89c627a8d9be1b43e9f5cccd60ed7ef2812021d11dea74790
case03 86d8864ba87905766bfc360e177a323fb6650785ba65e2cd2fe29cc452e1959f
case04 d53d7004eea8beec9a9fc7901eb2ec96f80f6ed15ce7ef95376b97540d27f029
case05 21687ad3152923c794c2b98c21e37233ec81df827f96315cfed77f55d6da1200
case06 1dadfda9bcefab151f277a18728c60ffac8d9a6979a78ba67c692350e85107f6
case07 e71b955ab19729c28f242e7e1895558ad5cf1873a1e87d31fdc878fce57be78e
```

## 8. 复现命令边界

工作目录与 v4 固定测试台一致时，读取冻结黄金文件；所有请求的输出路径均指向本 `semantic/` 目录。核心命令形态：

```powershell
python .\silu_semantic_reference.py --json .\semantic_reference_results.json

vlog.exe -modelsimini modelsim.ini -work semantic_candidate_work -l compile_candidate.log `
  ..\..\v4_silu_regression_20261005\vendor_sources\ph1p_logic_eram.v `
  ..\..\v4_silu_regression_20261005\vendor_sources\ph1p_phy_gsr.v `
  ..\..\v3_silu_stall_candidate_20261005\silu_shared_unit.v `
  ..\..\v4_silu_regression_20261005\tb_silu_vendor_stall.v `
  ..\..\v4_silu_regression_20261005\tb_silu_vendor_contract.v `
  ..\..\v4_silu_regression_20261005\tb_silu_shared_unit.v `
  ..\..\v4_silu_regression_20261005\tb_silu_vendor_random.v `
  .\tb_silu_semantic_assertions.v

vsim.exe -c -modelsimini modelsim.ini -l semantic_assertions_retry.log `
  -wlf semantic_assertions_retry.wlf `
  semantic_candidate_work.PH1P_PHY_GSR `
  semantic_candidate_work.tb_silu_semantic_assertions `
  -do 'run 500 us; quit -f'
```

固定用例沿用 v5 的 top 与 plusargs：原版 `stall=0/contract stall=1`，CEA `contract stall=1/16/32/64`、`tb_silu_shared_unit`、`tb_silu_vendor_random`。完整实际命令已由每个 ModelSim 日志首部自动记录。

## 9. 给物理分支的结论

- 当前四项 VG122 没有发现功能性溢出/下溢或 1024 写地址混用，冻结 CEA DUT可继续隔离 TD 物理诊断。
- 物理分支应保持现有 3 位 pending、11 位 table expected 与 signed 16 位 lookup，不在本阶段据此缩位或改接口。
- 1024 只作为 lookup 特殊端点；ERAM 映射核对时，写口必须仍只有 0..1023，读地址 1024 的低位别名必须与输出级常量选择一起理解。
- 严格交付仍阻塞；语义闭合和 ModelSim PASS 不等于 release passed、TD passed 或硅上行为签核。
