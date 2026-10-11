# V5-04 / V5-05 剩余审查报告

日期：2026-10-05  
角色：`review`（只读）  
结论：**V5 物理准入仍阻塞。** 候选 RTL 的严格门禁仍失败；VG145 有 9 条源锥超限，VG146 有 15 条已知操作下界超限（其中 7 条结构闭合，8 条同时受 PH1P 外部接口 unknown 污染）。这些是真实的**静态规则阻塞**，但不是 STA 关键路径、slack 或布线延迟证据。`drive_table_word` 的 `#1` 在 1 ns/1 ps 时基和 10 ns 时钟下不跨越上升沿，且每次 task 最多形成一次 ready/valid 握手。

## 1. 边界与冻结证据

- 本审查没有修改 RTL、testbench、checker、规则配置或 latency，没有运行 ModelSim/TD/训练/写 Flash。
- v3 候选与 v4 回归候选副本 SHA-256 均为 `5f357b493c7b3f941d9fa954a0ce5ec09091e466b641474360d2f64d0e42c938`，文件匹配。
- v5 manifest 记录的 fresh old-checker 两组为 original `174 errors / 173 issues`、candidate `242 errors / 241 issues`，均 exit 1；报告哈希与 v4 对应报告相同。新 checker 的 original/candidate 两组尚未形成，所以 V5-04 四组比较尚未完成。
- v4 的 65,536 全域日志与 seed 42 随机日志仅作**复用证据**，不是本审查新跑。

## 2. VG145 源锥超限：9 条

规则上限均为 3 个源信号。下表展开连续赋值别名；数量与位置来自 candidate gate，表达式来自同哈希 RTL。

| # | 位置 | target | 展开 expression | count / limit | 结论 |
|---:|---|---|---|---:|---|
| 1 | 139 | `table_ready_o` | `(cnt_pending == 3'd0) && ((i_table_addr == 10'd0) || ((~table_loaded_o) && (~table_fault_o)))` | 4 / 3 | confirmed |
| 2 | 140 | `input_ready_o` | `((~output_valid_o) \| i_output_ready) && table_loaded_o && (~i_table_valid)` | 4 / 3 | confirmed |
| 3 | 141 | `flag_input_transfer` | `i_input_valid && (((~output_valid_o) \| i_output_ready) && table_loaded_o && (~i_table_valid))` | 5 / 3 | confirmed |
| 4 | 143 | `flag_table_transfer` | `i_table_valid && ((cnt_pending == 3'd0) && ((i_table_addr == 10'd0) || ((~table_loaded_o) && (~table_fault_o))))` | 5 / 3 | confirmed |
| 5 | 144 | `flag_table_restart` | `[expanded flag_table_transfer] && (i_table_addr == 10'd0)` | 5 / 3 | confirmed |
| 6 | 145 | `flag_table_write_enable` | `[expanded flag_table_transfer] && ((i_table_addr == 10'd0) || (i_table_addr == cnt_table_expected[9:0]))` | 6 / 3 | confirmed |
| 7 | 146 | `wire_table_address` | `[expanded flag_table_transfer] ? i_table_addr : reg_lookup_address[9:0]` | 6 / 3 | confirmed |
| 8 | 154 | `o_table_ready` | 精确输出桥接，展开后同 `table_ready_o` | 4 / 3 | confirmed；与 #1 同根但是独立 report identity |
| 9 | 155 | `o_input_ready` | 精确输出桥接，展开后同 `input_ready_o` | 4 / 3 | confirmed；与 #2 同根但是独立 report identity |

## 3. VG146 操作下界超限：15 条

规则上限均为 3 个操作。candidate gate 的 VG146 总数是 51，必须分成：

- 7 条 `inconclusive_reason=none` 且 `count>3`：confirmed over-budget。
- 8 条有 PH1P `external interface has no implementation` 且已知下界 `count>3`：仍是强阻塞，但不把 unknown 扩展部分当成已知完整锥。
- 36 条 unknown 且 `count<=3`：是证据不闭合阻塞，**不是已知超预算项**。

对 `$enable` / `$D` 目标，gate 仅给出粗粒度 module-root 行 47；表中同时给出人工反查到的真实控制行。`[T]` 代表上表已完整展开的 `table_ready_o`，`[HT] = i_table_valid && [T]`，`[RT] = [HT] && (i_table_addr == 10'd0)`，`[P] = (~output_valid_o) | i_output_ready`。这些符号只为控制锥可读性，不是新 RTL 别名建议。

| # | gate 位置 / 真实行 | target | 展开的控制表达式或选择树 | count / limit | 证据分类 |
|---:|---|---|---|---:|---|
| 1 | 47 / 291-299 | `cnt_pending$enable` | `case({ i_input_valid && ([P] && table_loaded_o && ~i_table_valid), output_valid_o && i_output_ready })` | 7 / 3 | unknown closure + known lower bound over |
| 2 | 47 / 272-288 | `cnt_table_expected$enable` | `if ([RT]) 1; else if ([HT]) { mismatch -> 0; last -> 0; else -> cnt+1; }` | 14 / 3 | confirmed |
| 3 | 47 / 333-340 | `flag_input_valid$D` | `i_input_valid && ([P] && table_loaded_o && ~i_table_valid)`；外层推进使能为 `[P]` | 6 / 3 | unknown closure + known lower bound over |
| 4 | 47 / 173-190 | `output_data_o$enable` | `if ([P] == 1)`, 再依次选择 `!flag_ram_valid`, `flag_ram_lower`, `flag_ram_upper`, `reg_ram_address==1024` | 7 / 3 | unknown closure + known lower bound over |
| 5 | 47 / 213-223 | `table_fault_o$enable` | `[RT] || ([HT] && (i_table_addr != cnt_table_expected[9:0]))` | 14 / 3 | confirmed |
| 6 | 47 / 194-210 | `table_loaded_o$enable` | `[RT] || ([HT] && ((i_table_addr != cnt_table_expected[9:0]) || (i_table_addr == TABLE_LAST_ADDR)))` | 14 / 3 | confirmed |
| 7 | 139 | `table_ready_o` | `[T]` | 7 / 3 | confirmed |
| 8 | 140 | `input_ready_o` | `[P] && table_loaded_o && (~i_table_valid)` | 5 / 3 | unknown closure + known lower bound over |
| 9 | 141 | `flag_input_transfer` | `i_input_valid && ([P] && table_loaded_o && (~i_table_valid))` | 6 / 3 | unknown closure + known lower bound over |
| 10 | 143 | `flag_table_transfer` | `[HT] = i_table_valid && [T]` | 8 / 3 | confirmed |
| 11 | 144 | `flag_table_restart` | `[RT] = [HT] && (i_table_addr == 10'd0)` | 10 / 3 | confirmed |
| 12 | 145 | `flag_table_write_enable` | `[HT] && ((i_table_addr == 10'd0) || (i_table_addr == cnt_table_expected[9:0]))` | 12 / 3 | unknown closure + known lower bound over |
| 13 | 146 | `wire_table_address` | `[HT] ? i_table_addr : reg_lookup_address[9:0]` | 9 / 3 | unknown closure + known lower bound over |
| 14 | 154 | `o_table_ready` | 输出桥接展开后为 `[T]` | 7 / 3 | confirmed；与 #7 同根、独立 identity |
| 15 | 155 | `o_input_ready` | 输出桥接展开后为 `[P] && table_loaded_o && (~i_table_valid)` | 5 / 3 | unknown closure + known lower bound over |

审查结论：不应通过无寄存器别名拆分来隐藏上述锥；也不应仅因 PH1P unknown 就删除已知下界超限。如果协议 latency 必须保持 5，涉及寄存分割的修正必须先做架构评审；本报告不提交这类 RTL 改动。

## 4. VG122 四条 signed / width 风险复核

| 位置 | 表达式 | 宽度与 signed 结论 | 真实剩余风险 | 最小可验证建议（本轮不改 RTL/checker） |
|---|---|---|---|---|
| 283 | `cnt_table_expected <= cnt_table_expected + 11'd1;` | 两个操作数与目标都是 11-bit unsigned；`+` 结果不比 11-bit 目标更宽，VG122 的“结果超目标宽度”与源码语义不符。 | 同宽加法在 2047+1 时会模 2048 回绕；当前控制只在期望地址 1..1022 的中间项加 1，可达上界是 1023。 | 断言“执行该分支时 `cnt_table_expected <= 1022`”与“下一值 `<=1023`”；用 12-bit 黄金加法仅在 testbench 对比。 |
| 296 | `cnt_pending <= cnt_pending + 3'd1;` | 两个操作数与目标都是 3-bit unsigned，没有 signed 混用，也不存在“表达式宽于目标”的截断。 | 若协议错误允许 `cnt_pending==7` 时只输入握手，则 3-bit 计数器回绕到 0。现有回归不是这个不变式的穷尽证明。 | 断言 `flag_input_transfer && !flag_output_transfer -> cnt_pending != 3'd7`，并以 4-bit 黄金计数器对比。 |
| 297 | `cnt_pending <= cnt_pending - 3'd1;` | 两个操作数与目标都是 3-bit unsigned，没有 signed 混用或超宽截断。 | 若 `cnt_pending==0` 时出现只输出握手，结果会下溢为 7。 | 断言 `!flag_input_transfer && flag_output_transfer -> cnt_pending != 3'd0`，并与同一 4-bit 黄金计数器对比。 |
| 484 | `reg_lookup_address <= reg_rounded_value + 16'sd512;` | 两个操作数和目标均为 16-bit signed，类型一致。对所有 INT16 输入，附近偶数除 4 的 `reg_rounded_value` 范围为 `[-8192, 8192]`，加 512 后为 `[-7680, 8704]`，不超出 signed16。 | 当前算术范围内没有溢出或 signed 误解风险；风险只在上游舍入契约未来改变时重新出现。 | 在 testbench 用 17-bit signed 参考和断言 `[-7680,8704]`，覆盖 `16'h8000`、`16'h7fff`、舍入 tie 与 above-half 边界。 |

因此，四条都不支持立即改 RTL 位宽。但 VG122 的 rule key 是 `op_no_arith_overflow`：“操作数与目标同宽”只能排除目标更窄的截断解释，**不能单独清除溢出策略门**。在可达范围与计数不变式证据进入可重复门禁前，四条仍保留 blocking，不称为四条已证明误报。行 296/297 应以协议不变式闭环，行 283/484 应以显式范围黄金值闭环；如果这些证明通过，再评审 VG122 的宽度/范围建模并保留真实溢出负例，而不是机械加宽数据通路。

## 5. V5-05 `drive_table_word #1` 边沿审查

源码事实：

- `tb_silu_shared_unit.v:1` 为 `` `timescale 1ns / 1ps ``，所以 `#1` 是 1 ns。
- `tb_silu_shared_unit.v:50` 为 `always #5 i_clk = ~i_clk;`，时钟周期 10 ns，半周期 5 ns。
- task 在行 74 等待下降沿，行 75-77 用 blocking assignment 设置 valid/address/data，行 78 等待 1 ns，行 82 才等待上升沿，行 83 再等待 1 ns，行 84 撤销 valid。

时序证明：

1. 在任一下降沿 `t=N` 改变激励后，`#1` 到 `N+1 ns`；下一上升沿是 `N+5 ns`，因此 ready 检查与握手采样沿之间仍有 4 ns，不跨越 DUT 采样沿。
2. 若 ready 在 `N+1 ns` 为真，valid 在 `N+5 ns` 上升沿被采样，到 `N+6 ns` 才撤销；下一上升沿是 `N+15 ns`，所以不会二次握手。
3. 若 ready 为假，task 保持 valid/address/data，只在下降沿重新检查；ready 为假期间经过的上升沿不构成握手。对本 DUT，`table_ready_o` 只依赖 task 期间保持稳定的地址和同步寄存状态，等待期间 ready 的有效变化来自上升沿后的 NBA/组合收敛；在这个前提下，离开 while 后的第一个 ready-high 上升沿是唯一握手沿。这一证明不推广到可在两个轮询边沿之间异步变化的任意 ready/valid 接口。
4. 该 `#1` 的用途是跨过同一仿真时刻的 delta-cycle 组合更新，避免地址刚改变时读到上一地址的 stale ready；它没有改变 DUT latency，也没有将激励推过上升沿。

边界：这是行为仿真的调度证明，不是 SDF 或硅上 setup/hold 证明。本审查仅复用 v4 日志：全域日志显示 `65536 / latency=5 / II=1 / legal_writes=3072`，seed 42 日志显示 `4096 accepted / 4096 received / stall_cycles=1353 / max_stall=7`；本轮未新跑。

## 6. 八项公共门与物理准入

| 公共门 | 冻结候选状态 | 审查边界 |
|---|---|---|
| compile | passed | 只是本地静态解析 |
| ast | failed | formatter 1 条 run-level error |
| readability | failed | 包含本报告列出的预算阻塞 |
| comment | failed | 13 条 |
| naming | failed | 6 条 |
| profile | passed | 不代表交付通过 |
| testbench | not requested | gate 未用外部仿真替代该状态 |
| toolchain | not requested | 本轮没有新仿真、综合、TD 或板测 |

物理准入阻塞理由：

1. V5-04 四组比较只有 fresh old-checker 的 original/candidate 两组，缺 new-checker 两组及真实负例闭环。
2. candidate 仍非 delivery-ready，VG145/VG146 已知超预算项未处置；PH1P 所有权 unknown 也使 36 条 `count<=3` 不能放行。
3. 没有本候选的新物理证据：没有 ERAM 映射、CEA 实际连接、setup/hold/recovery/removal、未约束路径或多角 STA。静态 RTL 计数不能替代这些证据。

最小下一步：先完成项目级 PH1P input-sink 所有权/切片/测试台解析适配的正负例，再以同一输入和规则跑 new-checker 的 original/candidate 两组，完成四组差异。随后对上述 24 条 VG145/VG146 原始 finding 分“重复桥接 identity”和“独立控制根”建立不改 latency 的架构处置决策。只有阶段准入与运行授权都满足后，才进入 SiLU 可观测物理实现；本报告不放行 TD。

## 7. 证据索引

- `production/reports/v5_execution_20261005/manifest.json`
- `production/reports/v5_execution_20261005/old_candidate/gate.json`
- `production/reports/v4_execution_20261005/candidate_gate.json`
- `production/reports/v4_gate_diagnosis_20261005/finding_classification.json`
- `production/reports/v4_gate_diagnosis_20261005/T02_gate_diagnosis_report.md`
- `production/reports/v3_silu_stall_candidate_20261005/silu_shared_unit.v`
- `production/reports/v4_silu_regression_20261005/candidate/silu_shared_unit.v`
- `production/reports/v4_silu_regression_20261005/tb_silu_shared_unit.v`
- `production/reports/v4_silu_regression_20261005/candidate_full_domain_fixed.log`（复用）
- `production/reports/v4_silu_regression_20261005/candidate_random_seed42.log`（复用）
