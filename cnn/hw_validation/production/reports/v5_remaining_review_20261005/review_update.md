# V5 剩余审查更新

日期：2026-10-05  
角色：`review`（只读）  
证据时点：ownership 四组 checker 与 fixed-path vendor 回归完成后。

## 1. 对旧报告的定位

`review_report.md` / `review_report.json` 是**旧 checker 的阶段快照**，保留用于追溯，不覆写。其中“ownership 四组未完成”和候选 VG146 `51 = 7 confirmed over + 8 unknown lower-bound over + 36 unknown at-or-under`的状态已被本更新取代。

`v5_execution_20261005/manifest.json` 现已列出四个 fresh run：

1. `old_original`
2. `old_candidate`
3. `new_original_ownership`
4. `new_candidate_ownership`

四组都有冻结 source SHA-256、gate 路径与 exit code，因此 ownership 四组比较已完成。四组 exit 仍为 1；“矩阵完成”不等于交付通过。

## 2. new candidate ownership 剩余门禁

直接读取 `v5_execution_20261005/new_candidate_ownership/gate.json`：

- `delivery_ready=false`，`171 errors / 170 issues`。
- VG145 = 9：与旧快照相同的 9 条源锥超限，上限仍为 3。
- VG146 = 20：15 条 `inconclusive_reason=none` 且 `operation_count>3`，均为 confirmed 操作预算超限；另 5 条为 `operation_count=0 / limit=3` 的 unknown，不当作超预算。
- VG147 = 2：两条都是外部输出实现未知导致的 inconclusive，不是已知超预算。

### VG145：9 条

| target | 位置 | source count / limit |
|---|---:|---:|
| `flag_input_transfer` | 141 | 5 / 3 |
| `flag_table_restart` | 144 | 5 / 3 |
| `flag_table_transfer` | 143 | 5 / 3 |
| `flag_table_write_enable` | 145 | 6 / 3 |
| `input_ready_o` | 140 | 4 / 3 |
| `o_input_ready` | 155 | 4 / 3 |
| `o_table_ready` | 154 | 4 / 3 |
| `table_ready_o` | 139 | 4 / 3 |
| `wire_table_address` | 146 | 6 / 3 |

### VG146：15 条 confirmed 超预算

| target | operation count / limit | 状态 |
|---|---:|---|
| `cnt_pending$enable` | 7 / 3 | confirmed |
| `cnt_table_expected$enable` | 14 / 3 | confirmed |
| `flag_input_valid$D` | 6 / 3 | confirmed |
| `output_data_o$enable` | 7 / 3 | confirmed |
| `table_fault_o$enable` | 14 / 3 | confirmed |
| `table_loaded_o$enable` | 14 / 3 | confirmed |
| `table_ready_o` | 7 / 3 | confirmed |
| `input_ready_o` | 5 / 3 | confirmed |
| `flag_input_transfer` | 6 / 3 | confirmed |
| `flag_table_transfer` | 8 / 3 | confirmed |
| `flag_table_restart` | 10 / 3 | confirmed |
| `flag_table_write_enable` | 12 / 3 | confirmed |
| `wire_table_address` | 9 / 3 | confirmed |
| `o_table_ready` | 7 / 3 | confirmed |
| `o_input_ready` | 5 / 3 | confirmed |

旧快照中这 15 条曾被分成 7 条 confirmed 和 8 条受 PH1P input-sink unknown 污染但已知下界超限。ownership 适配后，8 条的 `inconclusive_reason` 均已清除，所以当前统一记为 15 条 confirmed。

### VG146：5 条 unknown，不超已知下界

| target | count / limit | inconclusive reason |
|---|---:|---|
| `output_data_o$D` | 0 / 3 | external output implementation is unknown |
| `reg_input_quotient$D` | 0 / 3 | missing storage data expression |
| `reg_rounded_value$D` | 0 / 3 | missing storage data expression |
| `wire_table_read_data` | 0 / 3 | external output implementation is unknown |
| `wire_table_write_data` | 0 / 3 | concatenation parser error: expected `}`, got `{` |

### VG147：2 条

| target | count / limit | 原因 |
|---|---:|---|
| `output_data_o$D` | 0 / 3 | external output implementation is unknown; `loop_presence=unknown` |
| `wire_table_read_data` | 0 / 3 | external output implementation is unknown; `loop_presence=unknown` |

分类结论：ownership 修正已消除 PH1P input-sink 的反向 unknown 污染，但不会使真实预算超限自动消失。15 条 confirmed VG146 和 9 条 VG145 仍是静态严格门禁阻塞；它们仍不是 STA 关键路径证据。

## 3. fixed-path vendor 回归：8 项均为新跑

`v5_vendor_regression_fixed_paths_20261005/results.json` 标记 `new_run=true`，8 个 case 均有新日志哈希，所有编译/仿真命令退出码均为 0。运行结果符合各自预期：

| case | 对象 | 预期/结果 |
|---|---|---|
| `case_00` | 原版，无停顿 | `TB_PASS stall=0 accepted=9 received=9 errors=0` |
| `case_01` | 原版，1 拍停顿负例 | 预期失败；`TB_FAIL_CONTRACT ... accepted=1033 received=1033 freeze_checks=1 errors=2` |
| `case_02` | 候选，1 拍停顿 | PASS；1033/1033，freeze 1，load/read 各 1024，errors 0 |
| `case_03` | 候选，16 拍停顿 | PASS；1033/1033，freeze 16，load/read 各 1024，errors 0 |
| `case_04` | 候选，32 拍停顿 | PASS；1033/1033，freeze 32，load/read 各 1024，errors 0 |
| `case_05` | 候选，64 拍停顿 | PASS；1033/1033，freeze 64，load/read 各 1024，errors 0 |
| `case_06` | 候选，INT16 全域 | PASS；65536，latency 5，II 1，legal writes 3072，stale-output errors 0 |
| `case_07` | 候选，seed 42 中央区随机 | PASS；4096/4096，stall cycles 1353，max stall 7 |

边界：`case_01` 的 simulator 进程 exit 0 但 testbench marker 为预期 `TB_FAIL_CONTRACT`；它是有效负例，不能因进程 exit 0 就称原版通过。全域与 seed 42 仍是两个不同覆盖集，不合并声称“全域随机反压”。

## 4. `drive_table_word #1` 结论不变

新回归的 input closure 中 `tb_silu_shared_unit.v` SHA-256 仍为 `b69f982848165d4e87295988f70f990384a003b2c8723d04379357e4b157e7bf`，与旧审查对象相同。因此原结论不变：

- 1 ns/1 ps timescale 下 `#1` 是 1 ns；10 ns 时钟的下降沿到下一上升沿是 5 ns。
- 下降沿改变地址/valid 后等待 1 ns，到下一上升沿仍有 4 ns，不跨采样沿。
- 握手上升沿后再等待 1 ns 撤销 valid，下一上升沿前已低 9 ns，每次 task 只产生一次握手。
- 该证明限定于本 DUT：`table_ready` 只依赖 task 期间稳定的地址和同步寄存状态，等待期间的变化在上升沿后 NBA/组合收敛；不推广到任意异步 ready/valid 接口。

新 `case_06` 以相同 testbench 得到恰好 3072 次合法写入，是本轮新跑旁证；仍只证明行为仿真调度，不是 SDF 或物理 setup/hold 签核。

## 5. 当前准入结论

ownership 四组比较和 8 项 fixed-path vendor 回归已完成，候选功能证据增强；但新候选仍 `delivery_ready=false`，剩余 9 条 VG145、15 条 confirmed VG146、5 条 VG146 unknown 和 2 条 VG147 inconclusive。

**物理准入仍阻塞。** 下一步是对 confirmed 预算项做不改 latency 的架构处置评审，并闭合 5+2 条剩余 unknown/inconclusive；不能用功能回归代替严格门禁，也不能用静态操作计数推断物理关键路径。本轮 `td_executed=false`、`production_modified=false`。

## 6. 新增证据

- `production/reports/v5_execution_20261005/manifest.json`
- `production/reports/v5_execution_20261005/new_candidate_ownership/gate.json`  
  SHA-256: `6e122cb746a72dade93e729c11331a74ff4b9adb2f01fb2aed7378868d6be7d2`
- `production/reports/v5_vendor_regression_fixed_paths_20261005/results.json`  
  SHA-256: `0815d319843aae502549e3a8c1a45ab28196244a654fcbf06d9d296a214a1f1c`
