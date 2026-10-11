# T02 严格诊断分类与根因报告

日期：2026-10-05  
角色：review（只读 RTL/规则）  
边界：未修改生产 RTL、testbench、checker、profile、阈值或时序约束；未运行 TD、训练、综合或布局布线。

## 1. 完整性与计数口径

| 输入报告 | 报告 `errors` | `issues` 逐项记录 | 额外 run-level AST/formatter 错误 | 分类状态 |
| --- | ---: | ---: | ---: | --- |
| SiLU original | 174 | 173 | 1 | 全覆盖 |
| SiLU candidate | 242 | 241 | 1 | 全覆盖 |
| round testbench | 413 | 412 | 1 | 全覆盖 |
| 合计 | 829 | 826 | 3 | 全覆盖 |

三条额外记录不是伪造 finding：original/candidate 各有一条 `Source does not match the enforced formatter template.`；round 的额外 formatter 错误与同文件 `always header normalization failed` 同源。`finding_classification.json` 保留 826 个原始 issue 对象和独立的 `additional_run_level_evidence`；CSV 用 `raw_index` 保留每个 issue 的原顺序。

## 2. 八项公开门禁状态

| 对象 | compile | ast | readability | comment | naming | profile | testbench | toolchain |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SiLU original/candidate | passed | failed | failed | failed | failed | passed | not_requested | not_requested |
| round DUT+TB | failed | failed | failed | failed | failed | failed | passed | not_requested |

所有原报告仍为严格门禁阻塞；同根因派生诊断没有被删除、忽略或改写为通过。

## 3. VG146 +31 / VG147 +37 的精确解释

候选唯一相关改变是 PH1P 实例 `cea` 的 actual 从常量变为 `flag_pipeline_enable`。该 PH1P 实例在报告中同时存在 VG097：参数/端口区无法静态解析。于是 checker 给 actual signal 注入 `external interface has no implementation`，并把 `loop_presence` 从可知的 `absent` 污染为 `unknown`。规则规定 `loop_presence=unknown` 时 VG146、VG147 同时适用。

- 新增 VG146 31 条：`flag_pipeline_enable` 自身 `operation_count=2, limit=3`，其余 30 个端点均为 `3/3`；全部未超预算，只因外部接口未知而阻塞。
- 新增 VG147 37 条：前述 31 个端点成对派生 VG147；另有 6 个既有 VG146 超预算端点（count 5/6/7）原先 `loop_presence=absent`，候选中变为 `unknown`，因此新增 VG147 镜像。
- 这 68 条不是 68 个独立硬件缺陷；但在规则输入未闭合前仍是 68 条真实 blocking 结果，不能静默豁免。

规则契约只允许已知 child **output** 向父层展开；child input `cea` 是 sink，不应反向成为父信号的驱动/loop 来源。最小建议是给该次门禁提供受治理的 PH1P 纯接口 source/manifest，或由规则维护者修正 input sink ownership 后同参数重跑。不要给 CEA 单独延迟一拍，这会破坏当前功能修复的控制/数据对齐。

## 4. SiLU 既有问题

- VG145 9 条与原始 VG146 中可确定的 13 个操作预算端点是真实组合控制复杂度；它们是严格规则阻塞，但不等价于已证明的功能错误。流水/预译码可能改变可见延迟，需架构评审后才可改。
- VG122 4 条是算术结果宽度风险，需逐式检查 signed、截断和固定点契约；本轮不据静态提示改数据通路。
- VG085 4 条是 checker part-select 丢失：源码四处均使用 `cnt_table_expected[9:0]`，报告 evidence 却变成 `i_table_addr ==/!= cnt_table_expected`。不要把 11 位计数器机械改成 10 位。
- VG097 1 条、VG132 2 条、VG153 1 条同属 PH1P 接口事实未闭合：实例无法解析后，`clka/clkb` 被误判为非时钟端口，`doa -> wire_table_read_data` 的输出驱动也未确认。
- VG084/VG137 各 1 条和两个 storage-expression 提取项保持 inconclusive；没有证据支持将其写成 pass。
- 其余是命名、字面量、注释与版式问题；可机械修复，但应与功能候选分批，避免污染一处 CEA 的因果对照。

## 5. round 413 条的规则适用性

412 个 issue 中，326 个是 testbench 文件上的明确 strict-profile 规范项：空格缩进 246、begin/end 15、显示前缀 18、header 5、注释覆盖/放置 42。测试台是明确识别的 Verilog-2001 testbench，当前 strict profile 没有给这些规则 testbench 豁免，因此它们仍阻塞门禁，但不代表 DUT 有 326 个功能故障。

另 86 条全部来自一个 parser 根因：合法测试台时钟发生器 `always #5 i_clk = ~i_clk;` 触发 `always header normalization failed`。其中 VG000 是原始 parse 错误，VG072..VG147、VG150..VG158 共 85 条是 fail-closed 派生；这些规则的具体适用性在 AST 恢复前无法判定。round 的 413 条都定位到 `tb_road_round_shift_stall.v`；当前报告没有产生 `road_round_shift.v` 的具体 finding。

最小复现只有一个 module、一个 reg 和一条周期 always；以 `--include-testbench` 运行原生 focused gate，稳定得到相同 parse 错误与 86 条 parser 派生记录。正确修复点是 formatter 对 testbench delay-control always 的识别，或由规则维护者明确哪些综合规则不适用于 testbench；不能写第二个 Verilog parser，也不能全局关闭规则。

## 6. 最小局部建议

1. 已实际向门禁传入 `ph1p_eram_interface_complete.v`，相关 unknown 仍未消失；规则维护者需检查 PH1P 参数块、空输出端口解析、input-sink 方向所有权及 `clka/clkb` clock-role，修复后再重跑 VG097/132/146/147/153，不能只重复传同一接口文件。
2. 规则维护者修复 VG085 对 part-select 的保留，并增加 `[9:0]` 回归；不改 RTL counter。
3. formatter 支持 `always #delay` testbench clock generator，并以本目录最小复现做回归；AST 成功后才评价 85 个派生规则。
4. 最后才分批处理真实 style 与组合复杂度；每批按原 strict 参数重跑，所有 blocker 清零前不宣称 T02 通过。

## 7. 验证边界

- 分类脚本自检：826 个原始 issue；三份报告分别 173/241/412；candidate-only VG146=31、VG147=37；另有 3 条 run-level formatter 记录，总计 829。
- 原生 focused quality gate 最小复现：93 个 issue，其中 parser 根因派生 86 个；结果不是 delivery PASS。
- readable-python/readable-script 专用技能在当前会话不可用；分类器为标准库机械分析 fallback，仅用断言验证计数，不宣称通过相应脚本质量门禁。
