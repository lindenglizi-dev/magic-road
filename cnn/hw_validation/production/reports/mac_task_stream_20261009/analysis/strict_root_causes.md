# 严格门禁长期未闭合根因审计

> **本轮最终状态（2026-10-09 后续复核，优先于下文历史快照）：** 下文保留的
> `5230/5249`、bare testbench 语法与“未执行 A-C”等表述只描述最初 raw gate
> 快照，不再代表当前状态。最终同一原/改闭包为 `gates_attempt3`：raw baseline
> `5249`、candidate `5416`；项目 overlay 与 PH1P registered external-interface 的
> 实际 A/C replay 为 baseline `4808`、candidate `4975`，两侧均较 raw 减少 `441`，
> 但仍未达到 strict delivery ready。A 与 C 已执行，B/F 尚未执行；未修改 global
> skill 或项目 checker overlay。三个新 testbench source 均使用合法 `()` 实例语法，
> 最终 gold 输出已经逐项通过，不能再按旧 bare 语法报告解释，也不能把功能通过解释为
> warn-free。最终 replay 证据见 `../checker_replay_final/report.{md,json}`；下文根因、
> 代表性分类与历史计数继续保留用于追溯，引用数字时应以本段和最新独立 warning 摘要为准。

日期：2026-10-09  
角色：review（只读 RTL、报告与 checker）  
范围：`pw_turnover_20261009/gates_attempt2`、`status.json`、项目 `checker_overlay`，并用 2026-10-05 的 `v4_gate_diagnosis_20261005/T02_gate_diagnosis_report.md` 判断问题是否早于本轮 PW 改动。  
边界：未运行冻结目录 `run.py`/runner，未运行 TD、训练、综合、布局布线或板卡；未修改 RTL、testbench、checker、全局 skill 或约束。本次只新增本报告。

## 1. 结论

严格门禁确实至少从 2026-10-05 到 2026-10-09 持续未闭合，但 **5249 条不是 5249 个独立 RTL 缺陷**。当前 candidate 相比 baseline 只增加 19 条：`VG040 +4`、`VG125 +4`、`VG067 +1`、`VG062 +4`、`VG147 +2`、`COMMENT_COMMENT_PLACEMENT +4`。也就是说，本轮 PW 候选没有新引入数千类问题，绝大多数是共享旧资产、层次展开、同一根因的逐目标复制，以及严格格式/注释规则。

当前公开状态为：`compile=passed`；`ast/readability/comment/naming/profile=failed`；`testbench/toolchain=not_requested`。独立 testbench 严格报告为 906 errors，但其两个源首先都触发同一个 formatter 前端错误，随后大量规则 fail-closed，不能把 906 当作 DUT 功能失败。

必须保留的真实阻塞有两类：

1. 已知、可确定的组合控制/数据操作锥超过 checker 的每目标 3 操作强预算；这与当前调度器的单周期接口判定和嵌套空间循环结构直接冲突。
2. `down2_dynamic_tile_runner` 是一进程 FSM，而严格 profile 要求当前状态、组合 next-state、独立输出三个过程。改成三段式不是注释修复，可能改变握手与可见延迟。

其余大头主要是：格式/注释欠账、checker 对数组/实例输出/循环归纳变量的误判或不确定、以及“严格规则要求”与已证明安全的定宽写法之间的策略冲突。

## 2. 本次实际检查

- 读取工程 `AGENTS.md`、已批准 RoadYOLO 框架及证据索引。
- 按 readable-verilog-generator `analyze` 路由检查八项公开状态；未把 `compile` 通过解释为整体门禁通过。
- 读取 `gates_attempt2/{baseline,candidate,testbench}.{md,json/command}` 的摘要、规则分布、代表 finding 和命令来源。
- 逐行核对 candidate 的 9 个门禁输入 RTL；重点核对位宽、驱动、状态、计数、组合反馈与组合操作预算。
- 读取项目 `checker_overlay` 的 11 个 Python 覆盖文件和 16 个正负回归测试，比较其覆盖范围与本轮 raw gate 的实际导入路径。
- 读取 2026-10-05 T02 根因报告。相同的 PH1P ownership、part-select/位宽、testbench delay/parser、格式和操作预算类别当时已经存在，因此可确认不是 10 月 9 日才出现。

## 3. 计数口径与共同根因

candidate 原报告为 5249 errors、24 strict warnings；可见 4605 个 VG finding 标题，并另有 comment-placement 明细。它们会对同一源码行重复给出质量、注释、命名和层次化语义诊断，不能简单相加为独立缺陷。

主要规则分布如下：

| 规则 | candidate 条数 | 共同根因解释 |
| --- | ---: | --- |
| VG146 | 921 | 442 条“超预算”、479 条 formatter 不确定；按 definition root、instance path、target 重复展开 |
| VG147 | 643 | 461 条“含 loop 的超预算”、182 条 formatter 不确定；其中 unknown output driver 会在 VG146/VG147 双报 |
| VG062 | 693 | 过程赋值缺同排语义注释 |
| VG040 | 664 | 声明/结构注释覆盖或语言规则 |
| VG004 | 408 | 空格缩进而非 Tab |
| VG015 | 183 | profile 要求内部 reg 声明时 `= 0`，即使时序复位块已经赋值 |
| VG064 | 135 | 实例端口映射缺同排注释 |
| VG153 | 126 | 数组动态索引写入、子模块输出和 primitive/interface 输出驱动未被 raw checker 确认 |
| VG125 | 110 | checker 要求字面量宽度等于数值最小位数，误把上下文定宽字面量当阻塞 |
| VG138 | 87 | 无显式位宽/进制的常数，主要是循环/临时整数的 `0`、`1` |
| VG145 | 64 | 完整组合源锥超过 3 个源；是真实规则/架构冲突，但不等价于已观察到功能错误 |
| VG122 | 48 | 算术结果宽度风险；需结合终止条件和允许回卷逐项证明，不能按条机械加宽 |

VG146/VG147 还需要再拆一层：

- VG146：432 条 `inconclusive_reason=none` 的确定超预算；其余 479 条由 unknown output、缺 storage D 表达式、`$signed` 未识别或表达式 parser 失败派生。
- VG147：301 条 `inconclusive_reason=none` 的确定超预算；140 条虽然计数超限但同时带 unknown output；其余由 unknown output、动态 lvalue/selection、缺 storage D 或 `$signed` 未识别派生。
- “确定超预算”也不是逐条独立设计错误。VG146 的 432 个层次身份折叠为 294 个 definition-target；VG147 的 301 个层次身份折叠为 290 个 definition-target。更高层 top/root 会再次包含相同 child 锥。

## 4. 分类审计

### 4.1 位宽：少量需人工证明，大量不是语义错误

代表位置：

- `down2_dynamic_tile_runner.v:225` 的 `cnt_output == 5'd7` 被 VG125 报“5 位但值只需 3 位”。这里 5 位是与 `cnt_output[4:0]` 对齐的上下文定宽，不是截断或溢出。
- `down2_dynamic_tile_runner.v:868` 实例处的 `reg_post_multiplier[flag_layer_pw]`、`reg_post_shift[flag_layer_pw]` 分别应为 unpacked array 的 32 位和 6 位元素；raw VG097 把两者都当成 1 位。这是具体可复核的 checker 前端误判，不应改 RTL 端口来迎合报告。
- `down2_dynamic_tile_runner.v:289` 的 `i_load_addr == cnt_expected_dw_cache` 是 11 位地址与 9 位有界计数比较。Verilog 会扩展窄操作数；逻辑意图是大地址不能等于计数。它是显式扩展/契约清晰度问题，不是当前已证明功能错误。
- `down2_dynamic_tile_runner.v:489/491/527/571/593/596/602/638/662` 等 VG122 主要是计数器加法。例：`cnt_position` 仅在终止条件内增加，`cnt_export` 的上限由 384 项导出控制。需要按每个 counter 的最大值、终止分支、允许回卷做一次表格证明，不能把 48 条统一改宽。

最小闭合路径：

1. checker 先保留 unpacked array element、part-select 和参数化宽度事实，并以真实 mismatch 负例回归。
2. 对地址/窄计数比较，仅在行为不变时显式零扩展窄计数；对算术计数先给出范围证明，再决定扩大临时 RHS、饱和或明确允许回卷。
3. VG125 应由规则维护者决定是否把“上下文定宽但非最小表示”降为 style；不要把 `5'd7` 机械改成 `3'd7` 来制造宽度混排。

授权：checker 局部修复需要单独实现任务；任何计数器位宽、端口或数值协议改变均需用户明确授权。仅添加显式扩展也应先跑原向量等价检查。

### 4.2 驱动：VG153 主要是 checker 未识别，不可补假驱动

126 条 VG153 有直接反例：

- `down2_dynamic_tile_runner.v:71` 的 `reg_dw_weight` 被报无驱动，但 `:710` 明确有 `reg_dw_weight[i_load_addr] <= i_load_data[7:0]`。
- `down2_dynamic_tile_runner.v:68-79` 的 11 组数组都有动态索引写入；raw liveness 只看根名字时漏掉 element lvalue。
- `down2_dynamic_tile_runner.v:150` 的 `mac_input_ready` 被报无驱动，但 `:862` 由 `road_mac_probe.o_input_ready` 命名连接驱动；同类还包括 `mac_result_*`、`pp_*` 以及 top 的 `runner_*`。
- `ph1p_eram_interface_complete.v:50-53` 是纯 primitive interface 的四个 output。当前 raw gate 把该接口文件和设计 RTL 一起作为普通 source root 扫描，于是按“源码模块自身未驱动 output”报错；正确处理应是受治理 external-interface/primitive 边界，而不是给接口文件添加伪行为。

最小闭合路径：扩展 project overlay 的 liveness，使动态数组 lvalue 归一到声明根，并从唯一、完整、同宽、同符号的命名 child output 建立驱动；PH1P 用受治理 external interface 入口，保留未知实现边界和真实多驱动/宽度冲突负例。

授权：需要 checker/runner 输入闭包的专项修改与原/fixed 全门对比。不要修改 RTL 增加假 assign，也不要把 unknown 静默改成 pass。

### 4.3 状态：一进程 FSM 与 strict 三段式规则冲突

`down2_dynamic_tile_runner.v:85` 只有 `state_current`；主状态转移位于 `:443-647` 的时序过程。VG144 在 `:57` 报“缺 current/next roles”。这不是 checker 找到错误状态跳转，而是当前一进程 FSM 不满足 skill 的强制三段式编码合同。

最小闭合路径：先冻结每个状态的输入握手、计数更新、输出可见周期和 fault 优先级，再把 next-state 与状态输出分离；用现有 original/stress 向量逐周期比较。不能只新增一个未使用的 `state_next` 名字骗过规则。

授权：需要，因为三段式重构可能改变 ready/valid、结果 reservation、fault 时序和可见延迟。

### 4.4 计数：报告把“有界控制”和“可能回卷”混在一起

代表信号：

- `cnt_position`：`down2_dynamic_tile_runner.v:94`，更新点 `:571/:593/:596`；受 tile 位置终止条件约束。
- `cnt_output`：`:95`，清零/加一判定来自 `:396-424`，VG145 对 `flag_cnt_output_clear` 报 26 个源、对 increment 报 12 个源。
- `cnt_expected_*`：如 `cnt_expected_control :81`，更新点 `:765`；其 enable 经 load-kind、地址连续性和 fault 条件形成长锥。
- `cnt_core_cycles` 等 32 位性能计数是观测量；如果任务时长允许超过 `2^32-1` 周期，需要明确“回卷允许”或改为饱和。当前严格 finding 本身没有给出运行时越界反例。

最小闭合路径：建立一张 counter contract（位宽、复位值、最大合法值、更新握手、终止/回卷语义），只修无证明项。对有界 counter 可用显式比较和同宽加数；对性能计数由系统合同决定回卷或饱和。

授权：纯文档/断言可单独做；位宽、饱和或外部观测格式变化需数值/接口授权。

### 4.5 “组合环”：两条是 for 归纳变量误判

VG136 只有两条：

- `down2_dynamic_tile_runner.v:212` 的 `lane_index`，实际在 `:352` 的 `for(lane_index = 0; lane_index < 8; lane_index = lane_index + 1)` 中使用。
- `road_dynamic_postprocess.v:129` 的 `check_lane`，实际在 `:132` 的三次静态 `for` 中使用。

两者都是 elaboration/过程循环的归纳变量自增，不是硬件组合反馈网。真实组合反馈负例仍必须保留。

最小闭合路径：VG136 依赖图构建时识别静态 `for` induction variable，不把 loop step 的自引用当数据通路反馈；新增真实 `assign a = ... a ...` 或互相依赖的负例，证明没有放松真正组合环。

授权：需要 project overlay 专项；不应为这两条修改 RTL。

### 4.6 组合操作预算：真实规则冲突，不是 1500 个独立 bug

最强代表证据：

- `down2_dynamic_tile_runner.v:343` 的 `weight_index`：VG147 `operation_count=418`，同一目标又因 top/root 路径出现一次。
- `down2_dynamic_tile_runner.v:358` 的 `next_mac_weight[...]`：`operation_count=266`。
- `down2_dynamic_tile_runner.v:342` 的 `halo_index`：`operation_count=136`。
- `down2_dynamic_tile_runner.v:396` 的 `flag_cnt_output_clear`：VG145 展开到 26 个源。
- `down2_dynamic_tile_runner.v:271-276` 的 `flag_start_accept` 同时组合 table、fault、多个 loaded 和模式条件，天然超过三源控制预算。

这里有真实的大组合表达式和嵌套 loop 展开，但“超过 checker 的 3 操作预算”不等于已观察到时序失败。当前 status 的内部 reg-to-reg setup 最小 slack 为 `+0.581 ns`，DSP/ERAM 内部也无负 slack；外部 reset entry 的负 slack 是另一类问题，已由同目录 `external_timing_causes.md` 负责，不能混成严格门禁的组合预算反例。

最小闭合路径分两级：

1. 先去除 unknown-output、缺 storage D、`$signed`、动态 lvalue 等 checker 派生污染，再以唯一 definition-target 重新看确定超预算集合。
2. 仅对仍有真实关键路径/资源证据的目标做 registered predecode、流水寄存器或多周期 FSM 分解。若保持固定 latency 是接口要求，则该门禁保持 blocking，交由人工架构评审，不应只挪到另一个 `always` 语法。

授权：必须有。任何流水、多周期、ready/valid 或 visible latency 变化都超出本次 review 权限。

### 4.7 格式与注释：数量大但机械，不是功能缺陷

VG004 408 条、VG040 664 条、VG062 693 条、VG064 135 条，以及 header/region/naming/default-init 等，说明这 9 个输入文件大多不是按当前 Erie strict profile 生成或归一化。candidate 比 baseline 只多 4 条过程注释、4 条实体注释和 4 条 comment placement，进一步证明大头是共享旧欠账。

特别注意 VG015：直接给所有 internal reg 加声明初始化可能改变 FPGA power-up/综合语义，且与现有异步复位重复。应先确认该规则是否真的适用于已有 RTL；不能把“格式修复”扩大成硬件初始化行为变更。

最小闭合路径：在语义 blocker 和 checker 误判清理后，单独做 formatter/comment 批次；注释批次必须用 immutable baseline 做 token 等价，格式批次单独验证，避免与 PW 功能差异混在一起。

授权：注释/格式实现仍需新任务授权；若触及声明初始化、信号重命名或 always 拆分，则按 RTL 行为修改处理。

## 5. raw gate 与 checker_overlay 的范围差异

本轮 `baseline.command.json` 和 `candidate.command.json` 都只把
`C:\Users\lenovo\.codex\skills\readable-verilog-generator`
插入 `sys.path`，没有加载项目 `checker_overlay`。因此当前 5230/5249 是 **全局 raw checker** 的结果，不是项目 overlay 修复后的结果。

项目 overlay 已覆盖：

- bare zero-port `module tb_name;` 前端形状；
- testbench `always #5` 周期 always 的解析，同时保留生产 RTL delay 失败；
- signed/数值 part-select、参数化静态 slice、真实 mismatch 负例；
- typed opaque interface 的 input sink ownership、output/inout 未知边界、多输出多驱动和宽度冲突；
- 极保守的简单 child-output liveness 驱动确认；
- 区域 banner 必须是真 banner，不能只靠正文关键词命中。

overlay **尚不能替代**：

- 动态 unpacked array element 的 VG097 宽度事实；
- 动态索引数组写入到声明根的 VG153 驱动归一；
- `for` induction variable 的 VG136 排除；
- `$signed`、dynamic lvalue、missing storage D 等 VG146/VG147 全部前端事实；
- VG144 三段式合同、VG145/146/147 强预算本身；
- 9 个 RTL 和 2 个 testbench 的格式/注释欠账。

所以最小正确顺序不是先改几千行 RTL，而是：**让同一冻结输入先经过已有 overlay，补齐仅有具体反例的 checker 缺口，保留真实负例，再对剩余确定 blocker 做 RTL/架构决策。**

## 6. testbench 906 条的独立解释

两个 testbench 都是合法的 bare zero-port module：

- `tests/tb_down2_dynamic_overlap.v:3`：`module tb_down2_dynamic_overlap;`
- `tests/tb_runtime_layer_shell.v:4`：`module tb_runtime_layer_shell;`

raw formatter 对两者都报 `only single module sources are currently supported`。每个 parse 根因随后使大量语义规则各产生一条 fail-closed finding。另有 533 条空格缩进和 102 条 begin/end 规范项，它们是真实 strict-profile 风格欠账，但不代表 DUT 功能错误。项目 overlay 已有 bare-zero-port 和 periodic-always 正负测试，而本次 raw testbench gate 没有加载 overlay。

最小闭合路径：先用 overlay/合并后的 checker 恢复 AST，再重算派生规则；最后独立做 testbench 风格归一。不得通过拆掉 testbench 自检逻辑来减数。

## 7. 建议的最小闭合序列与授权

| 顺序 | 动作 | 目的 | 额外授权 |
| --- | --- | --- | --- |
| A | 固定 strict gate 的 checker 来源，加载 project overlay；保持同一冻结输入与原始报告 | 消除“raw 与已修 checker 不同源” | 需要 checker/runner 实现授权；不改全局 skill |
| B | 补 VG097/VG153 数组事实与 VG136 induction-variable 识别；保留真实 mismatch、多驱动、真实反馈负例 | 只修有具体反例的误判 | 需要 project overlay + negative regression 授权 |
| C | 重跑原/fixed 全门并重新归并唯一 definition-target | 得到可行动的剩余 blocker，不运行 TD/训练 | 需要执行门禁授权；本报告未执行 |
| D | 建 counter/width/state/handshake 周期合同 | 把真实语义风险和 strict 编码偏好分开 | 文档可授权后独立完成 |
| E | 对确定组合预算和一进程 FSM 做架构决策 | 决定是否注册预译码、流水或多周期 | 必须明确授权 latency/握手/状态修改 |
| F | 最后分批做格式、命名和注释 | 清理机械欠账，保持因果清楚 | 需独立修改任务；comment-only 要 token 等价 |

当前没有权限批准或实施 A-F，也没有权限修改全局 skill。就本轮 review 而言，不需要新增训练、TD、时序例外、板卡或 Flash 授权；这些动作对关闭严格门禁没有帮助。

## 8. 八项门禁交接

| 门禁 | 当前状态 | 本次判断 |
| --- | --- | --- |
| compile | passed | 静态 compile 通过，不替代 AST/语义/外部工具证据 |
| ast | failed | raw checker 前端和 strict formatter 模板均有阻塞；testbench 还有 bare-zero-port 误判 |
| readability | failed | 混合真实强预算、FSM/profile 冲突、checker 派生与大量机械风格项 |
| comment | failed | 共享旧资产的注释覆盖/放置欠账为主 |
| naming | failed | strict Erie 命名/profile 欠账，不是 PW 功能回归 |
| profile | failed | 文件整体未按当前 strict profile 归一 |
| testbench | not_requested（设计门）；独立 TB static passed | 独立 deliverable 仍因 parser/style 906 errors，不能宣称 TB 严格通过 |
| toolchain | not_requested | 本次未补跑仿真、综合、TD 或远程工具 |

最终判断：长期未闭合是真，但正确的工作量单位是约 7 个共同根因族，而不是 5000 个独立缺陷。先闭 checker 来源和具体误判，再决定是否接受强组合预算/三段式 FSM 所要求的可见时序改变，才是最小且可验证的路径。
