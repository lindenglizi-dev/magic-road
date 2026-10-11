# v7 signed33 累加器定向验证报告

日期：2026-10-06 Asia/Shanghai  
角色：verify  
结论：`FUNCTIONAL_PASS_TESTBENCH_STRICT_FAIL`，不声明 release passed。

## 1. 验证对象与边界

- 最终候选：`../candidate/road_mac_probe.v`
- 候选 SHA-256：`f8bf6cace6eb99bd9b915be5e27e1d38af4b3a2485ffeb6e87675d8bfc3478e8`
- 冻结旧核反证：`../../v7_minimal_chain_20261006/inputs/road_mac_probe.v`
- 范围证明：`../coordinator/range_proof.json`
- 合法调用边界：单个归约最多 192 个有效 INT8 乘积、最多 24 个 8-lane 接受拍，bias 仅在 `first` 一次进入。
- 未覆盖且不声称：无限违规 first/last 流、形式证明、TD、训练、Flash、物理时序。
- 工程目录不是 Git 仓库，因此没有 branch 或 checkpoint commit。

范围证明给出 INT8 乘积范围 `[-16256, 16384]`，含任意 INT32 bias 的全部合法前缀为
`[-2150604800, 2150629375]`，严格落在 signed33
`[-4294967296, 4294967295]` 内。因此合法调用不需要新增计数器、端口或流水级；仅末拍把
signed34 candidate 判为 INT32 成功或三路原子 fault。

## 2. Python 参考与确定向量

`signed33_reference.py` 使用 Python 标准库逐拍计算真实 product/pair/quad/dot bank、三路
signed33 base、signed34 candidate 和 signed33 writeback。专用 Python/script skill 未安装，故这里只声明
标准库参考自检通过，不声明专用 Python strict。

参考结果：12 cases、84 accepted beats、12 terminals、8 final faults。

关键算术点：

| 覆盖点 | 暂态/终态 |
|---|---|
| 三路正向暂超 INT32 后恢复 | partial `[2147483651, 2147483652, 2147483653]`；final `[2147483643, 2147483644, 2147483645]` |
| 三路负向暂超 INT32 后恢复 | partial `[-2147483652, -2147483653, -2147483654]`；final `[-2147483644, -2147483645, -2147483646]` |
| 192 项合法极值归约 | 24 beats；final `[-2144337920, 2144362495, -7]` |
| 最大正前缀证明端点 | `INT32_MAX + 192*16384 = 2150629375`，末拍 fault、三路输出全零 |
| 最大负前缀证明端点 | `INT32_MIN + 192*(-16256) = -2150604800`，末拍 fault、三路输出全零 |
| 尾 mask 与 bias once | 非法 lane 均填非零极值，mask `0x25`；第二拍 bias 改为极值但被忽略；final `[154, -258, 389]` |

六个独立用例分别让 alpha/beta/gamma 发生正、负最终溢出；另有正、负 192 项端点故障。
8 个 fault 终态均检查三路外部 payload 同时为零，且 full-width accumulator 禁止提交故障 candidate。

## 3. 独立 TB 与周期断言

新增模块 `tb_road_mac_signed_accumulator` 配套同名 spec 与 WaveDrom。它复用冻结旧 TB 的真实
bank 观察方式，没有改 checker、DUT 或接口，也没有仅修改 fault 期望来绕过截断。

逐拍白盒检查：

| 接受后周期 | 检查 |
|---:|---|
| +1 | 24 个 signed16 product 与 `flag_product_valid` |
| +2 | 12 个 signed17 pair 与 `flag_stage_valid[0]` |
| +3 | 6 个 signed18 quad 与 `flag_stage_valid[1]` |
| +4 | 3 个 signed19 dot、完整 `reg_base_dot[98:0]` |
| +5 | 三路 `reg_candidate_*[33:0]` |
| +6 | 三路 candidate hold 全位 |
| +7 | 三路 candidate final 全位 |
| +8 | commit/publish decision |
| +9 | 完整 `reg_accumulator[98:0]` 与可选终态 |

ModelSim CSV 机器审计结果：

- 84 次主向量接受，12 次 `result_valid`，12 次真实 `result_accept`。
- 所有终态固定 latency 9 cycles。
- 相邻接受间隔仅为 `[11, 16, 25]`，逐项与期望 `[11, 16, 25]` 相等：非末拍 11；3-cycle 输出停顿 16；12-cycle 输出停顿 25。
- 输入忙期间共观察 593 个 payload hold cycles，没有 payload 改变。
- 下游在恢复终态之前已置 `ready=1`：第二拍仍在 +9 产生正确恢复结果，下一 posedge 用边沿前旧值记录真实握手，之后有效清除且连续四拍无重复/ghost。
- 异步复位取消覆盖 offset `1,2,3,4,5,6,7,8,9,9`：product、pair、quad、dot、candidate、hold、final、decision、writeback、output hold。
- 每个复位点同时断言 base 四级、candidate/hold/final、`reg_publish_data[98:0]`、accumulator、valid/last 链及外部终态清零；释放后无 ghost。

## 4. 官方 ModelSim 2020.4 结果

候选：

- compile：`Errors: 0, Warnings: 0`
- run：`VERILOG-GEN-RESULT PASS vectors=84 errors=0 busy_hold=593 resets=10 ready_high=1 latency=9 ii_nonlast=11 ii_stall3=16`
- run footer：`Errors: 0, Warnings: 0`

冻结旧核负例：

- compile：`Errors: 0, Warnings: 0`
- run：`VERILOG-GEN-NEGATIVE PASS legacy_early_faults=2 errors=0`
- 正、负恢复序列的第一非末拍都在 accept+9 被旧 96-bit 核提前拒绝，fault=1、三路 payload=0；这证明旧截断行为没有被测试期望隐藏。

完整命令参数见 `commands.json`，原始日志和周期 CSV 分别为：

- `modelsim_candidate_compile.log`
- `modelsim_candidate.log`
- `modelsim_candidate_trace.csv`
- `modelsim_legacy_compile.log`
- `modelsim_legacy_negative.log`
- `modelsim_legacy_negative_trace.csv`

工具和全部输入/证据哈希见 `baseline_manifest.json`。Icarus 仅作辅助预检，最终判断以上述官方
ModelSim 实跑为准。

## 5. readable-verilog-generator 严格门

候选 RTL 自身的独立 strict 报告为 `delivery_ready=true`；本 verify 角色新增的 TB 另行运行
`generated_deliverable_gate.py --include-testbench`，必须单列：

| 公共门 | 状态 | errors | 说明 |
|---|---|---:|---|
| compile | failed | 1 | formatter AST 路径失败；不等同于 ModelSim 编译，后者 0 error |
| ast | failed | 2 | formatter 解析/归一化未闭合 |
| readability | failed | 140 | 包含 AST 级联及真实风格项 |
| comment | failed | 30 | 真实注释覆盖/放置项 |
| naming | failed | 126 | 包含 AST 级联及真实命名项 |
| profile | failed | 1 | 真实 header/profile 契约未闭合 |
| testbench | passed | 0 | 专用 testbench static gate 通过 |
| toolchain | not_requested | 0 | 官方 ModelSim 已在本报告独立实跑 |

这不是可以豁免的纯工具误报。冻结 TB 的首个 VG000 为
`only single module sources are currently supported`；临时副本仅把零端口声明从
`module name;` 改成 `module name();` 后，首个 VG000 变为
`always header normalization failed`，整体仍 `delivery_ready=false`。同时报告明确存在可局部修复的
header 路径/间距、`$display` 前缀、begin/end、命名、注释和 profile 违规。因此：

- 功能语义和官方仿真：通过。
- 新增 TB 的完整结构/风格 strict：未通过，原始 JSON/Markdown 和显式空端口 A/B 报告均保留。
- 不把 testbench static gate 通过或 ModelSim 0 error 扩大为完整八门通过。

初次失败证据也未删除：

- `legacy_negative_first_attempt.log`：旧负例跳号向量误套候选 interval，算术观察正确，harness 期望错误；修正后官方负例通过。
- `modelsim_vmap_first_attempt.log`：本地 `modelsim.ini` 尚未创建导致 vmap 失败；执行 `vmap -c` 后双库映射、编译和仿真通过。

## 6. 交付索引

- `signed33_reference.py` / `signed33_vectors.json` / `signed33_vectors.txt`
- `tb_road_mac_signed_accumulator.v`
- `tb_road_mac_signed_accumulator.spec.json`
- `tb_road_mac_signed_accumulator.wavedrom.json`
- `verification_results.json`
- `commands.json`
- `baseline_manifest.json`
- `tb_strict_gate.json` / `tb_strict_gate.md`
- `tb_strict_explicit_empty_probe.json` / `tb_strict_explicit_empty_probe.md`

机器汇总结论固定为 `FUNCTIONAL_PASS_TESTBENCH_STRICT_FAIL`，`release_claim=false`。
