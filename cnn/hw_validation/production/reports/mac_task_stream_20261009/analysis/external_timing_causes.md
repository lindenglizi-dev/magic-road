# 外部窄口时序长期未签核原因

日期：2026-10-09。任务类别：`analyze`，只读审查。工程不是 Git 仓库；本次没有修改 RTL/SDC/ADC，没有启动仿真、综合或布局布线。

## 结论与批准边界

可以批准 `pw_turnover_20261009` 作为 **PW 预取功能与内部 100 MHz 时序里程碑**：`internal_reg_to_reg.timing` 的 23,710 条 setup/min 记录无负裕量，最小 setup `+0.581 ns`、hold `+0.021 ns`。不能批准外部 I/O、原始复位、板级接口或部署签核：全量 routed STA 仍有 **16 个 setup、33 个 hold、4 个 removal** 失败端点，状态文件也明确是 `PW_PREFETCH_FUNCTION_AND_INTERNAL_TIMING_PASS_NOT_DEPLOYMENT_RELEASE`、`release=false`。

这些外部问题不是本轮才出现。至少从 2026-10-07 的 v11，到 2026-10-09 的动态层集成，再到当前 PW 周转候选，连续三个实际 routed 候选都保留了同一类零延迟诊断窄口和未签核外部边界：

| 实际候选 | 全局 setup | 全局 min | 外部分类 |
|---|---:|---:|---|
| `v11_internal_timing_20261007/physical/final_timing.rpt` | WNS `-2.264 ns`，20 端点 | WNS `-1.449 ns`，411 端点 | 报告已明确外部 I/O 与复位未签核；其中还混有 5 个内部 setup |
| `runtime_layer_integration_20261009/physical_attempt2/final_timing.rpt` | WNS `-2.122 ns`，15 端点 | WNS `-1.181 ns`，51 端点 | 15 setup、48 hold、3 removal，均归为外部 |
| `pw_turnover_20261009/physical/final_timing.rpt` | WNS `-1.409 ns`，16 端点 | WNS `-1.266 ns`，37 端点 | 16 setup、33 hold、4 removal，均归为外部 |

因此“很久没通过”若按本项目保存证据理解，应准确表述为：**不是日历上无法判断的长期，而是从 10 月 7 日至当前连续多个候选都没有做外部签核；候选优化改变了数量和裕量，但没有改变未闭合边界的性质。**

## 当前失败端点和根因

证据基线为：

- `cnn/hw_validation/production/reports/pw_turnover_20261009/physical/coverage_100000_violations.timing`
- `cnn/hw_validation/production/reports/pw_turnover_20261009/physical/final_timing.rpt`
- `cnn/hw_validation/production/reports/pw_turnover_20261009/physical/shell.sdc`
- `cnn/hw_validation/production/reports/runtime_layer_integration_20261009/physical/layer_shell/road_dynamic_overlap_low_io_top.v`

### 1. 输出 setup：内部组合选择直接到自动放置 PAD

16 个 setup 失败全部终止于诊断输出 `o_tx_data[*]`、`o_tx_valid` 或 `o_rx_ready`。最差路径为：

```text
down2_dynamic_tile_runner_Inst_shell/cnt_export_reg[2]_syn_6.clk
  -> runner_output_data / shell 组合选择
  -> o_tx_data[0] PAD
slack = -1.409 ns, data path = 8.382 ns, clock skew = 2.977 ns
```

shell 的 `o_tx_data`、`o_tx_valid`、`o_rx_ready` 都是组合输出桥，见 `road_dynamic_overlap_low_io_top.v:201-204`；`tx_data_o`/`tx_valid_o`/`rx_ready_o` 又由 `road_dynamic_overlap_low_io_top.v:350-387` 的状态组合逻辑产生。这里没有最终输出寄存边界。零 `set_output_delay` 仍然失败，真实接收器若要求正的 setup 预算，只会进一步压缩 FPGA 可用时间，不能把当前结果外推成板级通过。

### 2. 输入 hold：`i_rx_data` 确实直达 SiLU ERAM 写数据口

最差 hold 的完整起终点是：

```text
i_rx_data[2]
  -> HDIO
  -> down2_dynamic_tile_runner_Inst_shell/
     road_postprocess_stream_Inst_tile/u_chain/u_silu/
     PH1P_LOGIC_ERAM_Inst_silu_table_syn_1.dia[2]
slack = -1.266 ns
data arrival = 2.128 ns
capture clock arrival = 3.067 ns
ERAM hold = 0.327 ns
```

所以报告中的 ERAM 入端口不是误分类，源头确实是顶层 `i_rx_data`。源码链路为：

```text
road_dynamic_overlap_low_io_top.v:58       i_rx_data[15:0]
road_dynamic_overlap_low_io_top.v:195-196  TABLE valid/handshake 直接使用外部 valid
road_dynamic_overlap_low_io_top.v:522      .i_table_data(i_rx_data)
```

当前 shell 没有先锁存完整的 `valid + data` 接收事务，再从内部寄存器驱动表写口。除了 ERAM，其他 hold 端点也落在 `reg_load_addr`、`reg_load_data`、`reg_load_kind`、`reg_load_low`、runner 的 `flag_layer_pw` 和 `reg_mac_weight`，与同一个“外部数据直接进入内部控制/存储”根因一致。

特别注意：`physical/eram_all.timing` 显示 ERAM hold 最小 `+1.039 ns`，并不与上述结果矛盾。`physical/build.tcl:59-62` 只把 ERAM **输出 pins** 放进 `$eram_q`，随后执行 `report_timing_path -from $eram_q`；它检查的是 45 个 ERAM 输出起点到下游的路径，不覆盖 `i_rx_data -> ERAM dia` 写入路径。全量 `coverage_100000_violations.timing` 才揭示了写数据入口失败。局部 ERAM 报告不能单独签核 ERAM 的全部端口。

### 3. 原始复位：内部同步级通过，不等于外部释放通过

shell 在 `road_dynamic_overlap_low_io_top.v:207-222` 实现两级异步断言、同步释放；`reset_sync_interstage.timing` 的 8 条 setup/min 记录均为正，最小 setup `+8.072 ns`、hold `+0.124 ns`。但全量外部入口仍有：

- `i_rstn -> reg_release_done_reg_syn_5.asr` removal `-0.542 ns`
- `i_rstn -> reg_release_done_reg_syn_3.asr` removal `-0.326 ns`
- `i_rstn -> reg_release_done_reg_syn_6.asr` removal `-0.079 ns`
- `i_rstn -> reg_release_done_reg_syn_4.asr` removal `-0.064 ns`
- `i_rstn -> state_current_reg[2]_syn_2.ic` hold `-0.025 ns`

后一条也说明原始 `i_rstn` 不只用于 synchronizer 的异步断言；`flag_interface_open = i_rstn & reg_release_done`（`road_dynamic_overlap_low_io_top.v:192`）把原始复位重新带入功能组合锥。内部释放链和后续 `reg_release_done` 分发通过，只证明同步级之后的内部路径，不证明引脚释放和原始复位组合使用已经签核。

## 为什么 STA coverage 100% 仍不能签核

`STA coverage = 100.00%` 的含义是：在当前网表、当前自动放置和当前约束模型下，工具对可识别时序端点完成了分析。它不表示裕量通过，也不表示约束真实。当前同一份报告紧接着给出 setup WNS `-1.409 ns`、hold WNS `-1.266 ns`。

更关键的是，`shell.sdc` 明写“no external device or board delay is modeled”，并对 19 个非时钟输入位和 18 个输出位统一使用 `-max 0.000/-min 0.000`。因此：

- `check_timing` 的 no/partial input/output delay 都是 0，只能说明每个端口被一个数值覆盖；不能说明数值来自真实外设。
- `timing_ignored.rpt` 和 `timing_exceptions.rpt` 都为空，说明没有用 false/multicycle/min/max-delay 例外遮掉失败；这是诊断证据完整，不是通过。
- `shell.adc` 刻意为空。`td_20261009_152048.logw` 明确报告 38/38 逻辑端口没有用户位置约束，并被随机分配；连 `i_clk` 也是自动分到 K5。当前 PAD 路由、clock skew 和 I/O 延迟都是一次自动位置的诊断结果，不能代表官方模板或比赛板。

## `check_timing` 未闭合对象及与上轮关系

当前 `check_timing_verbose.rpt` 仍有两个 HIGH 类别：

1. **clock definition(1)**
   - 明确列出的 local clock 是 `probe_clk`。
   - 同时报告“1 generated clock is not connected to its master clock”，但 TD 文本没有打印该 generated-clock 名称。
   - `clock_summary_debug.rpt` 只发布一个 `probe_clk` primary clock（100 MHz，5,439 endpoints）；实际路径和 clock debug 可见自动插入的 `i_clk_dup_1_created_gclkinst` 以及多个 `...auto_created_sclk...` 分支。可以据此判断问题位于当前自动生成的时钟网络附近，但不能把未打印名称的 generated clock 擅自等同为某一具体 SCLK 实例。
   - v11、动态层集成 attempt2 和当前 PW 三轮都原样报告 `probe_clk` local clock 和 1 个 master 未连接的 generated clock；这不是 PW 修改新引入的问题。

2. **dummy node(2)**
   - `PH1P_PHY_DSPSIOU_V2`：当前 30 个 DSP 映射实例的 `.mul9_mode` 与 `.mul9_signed`，共 60 个列出的悬空模型 pins。24 个在 `road_mac_probe`，其余是动态 pre/post 乘法映射。
   - `PH1P_PHY_LSLICE`：当前对象为 `down2_dynamic_tile_runner_Inst_shell/reg_mac_bias_reg[47]_syn_2.ofb`。
   - v11 已有同两类 dummy：当时是 26 个 DSP 的 52 个 control pins，LSLICE 对象为 `_al_n1_syn_556.ofb`；动态层集成增加到 30 个 DSP/60 pins，LSLICE 对象变为 `reg_final_data_stage0_reg[35]_syn_2.ofb`；当前 DSP 家族不变，LSLICE 映射对象又变为 `reg_mac_bias_reg[47]_syn_2.ofb`。这说明 dummy 类别长期存在，LSLICE 具体对象随综合映射漂移，不能仅凭对象换名宣称已修复。

`td_20261009_152048.logw` 另有 `SYN-5025 Using 0 for all undriven pins and nets`。现有报告不足以证明这些 dummy pins 对功能无影响，也不足以证明它们一定有害；干净签核前需要在真实绑定网表中核对 DSP mode/signed 配置和 LSLICE 输出是否为合法未用物理端，而不是降低 `check_timing` 严格度。

## 自动 I/O 与同步边界核对

当前窄口只能被解释为“假定与 `i_clk` 同步的诊断接口”，不能解释为已验证的真实外设：

- `i_rx_valid`、`i_rx_data`、`i_tx_ready` 都未经统一输入寄存边界直接参与状态、握手、存储和输出-ready 组合逻辑。
- ready-valid 本身不构成 CDC。若发送端不是同一个 `i_clk` 域，必须明确源保持规则、目的捕获规则、确认点、payload 稳定区间和复位行为，通常需要异步 FIFO 或等价的完整事务 CDC。
- 即使发送端同域，也仍需真实 clock relation、外设 tCO/setup/hold、PCB skew、I/O standard 和固定 pin location，才能给出真实 `set_input_delay`/`set_output_delay`。
- 输出端没有最终寄存边界；输入端尤其 TABLE 数据可直达 ERAM。自动随机 I/O placement 会让这些路径的结果随位置变化，不能靠换种子或提高 hold-fix 优先级替代接口设计。

## 最小可签核方案

按风险从小到大，建议用户先决定窄口的真实身份，再实施一个方案；本报告不修改接口或延迟数值。

### 方案 A：真实片内同步集成（最终系统优先）

若窄口只是独立探针壳，最终应在官方视频模板/同一 100 MHz 域内连接真实生产模块，把 `i_rx_*`/`o_tx_*` 从板级 PAD 变成片内寄存器到寄存器接口。保留 ready-valid 的稳定与反压语义，在真实顶层重新跑全量 setup/hold/removal。这个方案能消除“随机 PAD + 不存在的外设”模型，但需要用户确认生产侧实际时钟域、复位域和连接模块；跨域时不能按同域处理。

### 方案 B：增加内部注册 I/O 边界（最小 RTL 候选，需另行授权）

在 shell 内先原子锁存 `i_rx_valid + i_rx_data`，所有命令解析、load 和 TABLE/ERAM 写口只使用锁存后的事务；输出 `o_rx_ready/o_tx_valid/o_tx_data` 使用最终寄存边界并保持 ready-valid 停顿稳定。原始 `i_rstn` 只负责同步器的异步断言，功能开放与状态逻辑只使用同步释放后的信号。

这可以把深层 `i_rx_data -> ERAM` 和组合 `reg -> PAD` 切成局部路径，但会引入可见的 1 拍或更多延迟，可能改变 ready 的时序和测试期望；必须经端口/协议决定、更新周期图、功能回归和新 routed 报告。它仍不能代替真实板级 min/max delay 与固定管脚。

### 方案 C：保留真实外部同步外设，等待完整契约

若比赛系统确实需要这组 16 位外部窄口，必须由用户/板卡接口给出：驱动和采样时钟、相位关系、两端器件 tCO/setup/hold、板级 skew/jitter、I/O standard、电压、slew/drive 和固定 pin。之后用这些事实建立 SDC/ADC，再判断是否还需 I/O register、相位调整或板级协议改变。若外设异步，则改为 CDC 方案，不能给异步总线套一个虚构的同步 delay。

### 不可采用的“快速变绿”

- 不编造非零 input/output delay。
- 不为 `i_rx_data -> ERAM`、输出 PAD 或原始 reset 添加 false path/multicycle/min-delay/max-delay 例外。
- 不用随机 I/O seed、`bitgen unconstr_io` 或单纯提高 hold-fix 优先级冒充接口签核。
- 不因 `eram_all.timing` 或内部 reg-to-reg 通过而忽略全量报告中的外部端点。

## 需要用户决定

1. 最终窄口是片内同域接口、真实同步板级外设，还是异步外设？
2. 是否允许为注册边界增加接口可见延迟，并相应更新 ready-valid 测试契约？
3. 原始复位必须异步断言/同步释放，还是上游可以提供同步复位？无论选择哪种，是否同意把原始 `i_rstn` 从功能组合锥中移除？
4. 若保留板级外设，请提供/确认管脚表、电气标准和真实 min/max 时序参数；在此之前只能批准内部里程碑。

## 八项公开门禁状态

本任务只读，没有重跑门禁。当前 `pw_turnover_20261009/measured_evidence.json` 记录为：`compile=passed`；`ast/readability/comment/naming/profile=failed`；`testbench/toolchain=not_requested`。因此外部时序之外，严格交付门禁本身也未闭合；本分析不把已有功能/物理局部证据改写成八项通过。

## 追加：最终 `physical_attempt2` 的内部 setup 根因

> 当前结论以 `reports/mac_task_stream_20261009/physical_attempt2/`（2026-10-09 16:19 生成）为准。前一轮 `reports/mac_task_stream_20261009/physical/` 的 `-0.534 ns` 只保留为布局敏感性对照，不是当前候选结果；上文对 PW 外部窄口的结论没有被本节改写。

### 当前口径与签核状态

- `physical_attempt2/internal_reg_to_reg.timing`：setup WNS `-1.327 ns`、TNS `-48.237 ns`、57 个失败端点；hold WNS `+0.049 ns`、0 个失败端点。因此“内部 reg-to-reg 已通过”的里程碑在最终候选上不成立。
- `physical_attempt2/coverage_100000_violations.timing`：全量 setup 共 102 个失败端点，SWNS `-2.408 ns`；其中 15 个是原有外部输出端点，87 个是内部端点。内部 87 个又分成 57 个 reg-to-reg 和 30 个 reg-to-DSP 输入端点，不能只看 57 个 reg-to-reg。
- 全量 hold 仍有 46 个失败端点、HWNS `-0.832 ns`；`internal_reg_to_reg.timing` 的 `+0.049 ns` 只说明内部寄存器间 hold 已过，不推翻上文外部 hold/removal 未签核结论。

### 57 个 reg-to-reg setup 端点不是全部同一根因

| 分组 | 数量 | 最差路径 | 物理特征 | 判断 |
|---|---:|---|---|---|
| A | 56 | `u_pre/u_round/result_tag_o_reg[2]` -> `u_pre/u_round` 各流水寄存器 CE；代表端点包括 `reg_absolute_delay_reg[62].cea` 和 `reg_remainder_reg[1].cea` | WNS `-1.327 ns`；data `11.070 ns`，cell `1.257 ns`/11%，net `9.813 ns`/89%；4 级 LUT；最终 `u_pre/u_round/i_advance` fanout 844、单网延迟 `6.123 ns` | 同一条“结果 tag 判定 -> ready -> advance/CE”高扇出反馈锥 |
| B | 1 | `state_current_reg[2]` -> `cnt_output_reg[1]_syn_54.ima` | WNS `-0.238 ns`；data `9.978 ns`，cell `2.196 ns`/22%，net `7.782 ns`/78%；7 级 LUT；max fanout 33，末段网延迟 `3.506 ns` | 独立的状态解码/计数器更新长锥，不是 A 组的 fanout-844 根因 |

A 组的 RTL 语义链可由本轮实际输入源码直接闭合：

1. `reports/retirement_lane_banks_20261009/rtl/road_dynamic_postprocess.v:95-102` 用 `pre_result_tag` 解码 `wire_pre_slot/wire_pre_lane` 和 `flag_pre_identity`；
2. 同文件 `:111-117` 将身份、retire 状态、故障、SILU ready 和 post 状态组合成 `flag_pre_result_ready`；`:198` 把它接到 `u_pre.i_output_ready`；
3. `reports/retirement_lane_banks_20261009/rtl/road_dynamic_requant.v:33-34` 形成 `flag_advance = i_rstn && (!flag_round_valid || i_output_ready)`，`:59` 将其送入 `u_round.i_advance`；
4. `reports/retirement_lane_banks_20261009/rtl/road_round_shift.v:55` 的 `i_advance` 控制大量流水寄存器，映射后成为 fanout 844 的 CE 网。

因此这不是算术数据通路本身变长，而是已寄存的 pre 结果身份在同拍内经过 retirement/ready 判断后反向控制同一 pre 舍入流水的全局推进。恢复原 debug 事件优先级虽然没有改变结构算术或端口，却改变了网表规模/放置竞争，使主导关键路径从前轮的 `reg_release_done -> u_post/u_round/i_advance` 漂移到本轮的 `pre_result_tag -> u_pre/u_round/i_advance`。这说明当前设计在默认布局下缺少时序裕量，前轮 `-0.534 ns` 不能作为最终候选可重复通过的证据。

### 全量报告额外暴露 30 个 reg-to-DSP 输入 setup 端点

除上述 57 个寄存器端点外，全量报告还有 30 个内部 setup 违例，全部从 `down2_dynamic_tile_runner_Inst_shell/cnt_mac_group_reg[0]_syn_14` 发往 `road_mac_probe_Inst_tile/mult0_syn_57.xa[*]`。最差为 `-0.352 ns`，data `9.946 ns`（cell `1.417 ns`/14%，net `8.529 ns`/86%），4 级 LUT，路径经过 `wire_mac_prepare_group`、`cnt_output` 组合锥、fanout-78 的 `flag_mac_input_accept_dup_21`，再到 DSP 输入寄存端。

`physical_attempt2/dsp_all.timing` 的 setup WNS `+2.343 ns` 不与这 30 个违例矛盾：`physical_attempt2/build.tcl:61` 的报告命令是 `report_timing_path -from $dsp_q`，只覆盖 DSP **输出** 发出的路径，不覆盖寄存器到 DSP **输入** 的路径。这与上文 `eram_all.timing` 无法覆盖 `i_rx_data -> ERAM.dia` 是同一类报告方向盲区。全量签核必须以 `coverage_100000_violations.timing` 为准。

### TD 现有的无 RTL 语义变化优化能力

本机 TD 6.2.168116 帮助 `E:/Anlogic/TD_6.2.1_Engineer_6.2.168.116/doc/cmd/help_comment_opt.json` 明确列出：

- `phys_opt -force_replication_on_nets <net>`：对指定高扇出网做复制；
- `-fanout_threshold <num>`：设置 HFN 门槛；
- `-effort low|middle|high|ultra`；
- `-post_route`：布线后单元重定位；`-mode` 支持 relocation/reroute；
- 帮助描述中另有 `-post_place`，但该选项没有出现在同文件 `opt_list`，属于版本内文档不一致，执行前必须在对应 DB/命令解释器中验证，不能凭本文拼命令。

官方策略 `E:/Anlogic/TD_6.2.1_Engineer_6.2.168.116/doc/strategies/official_strategy_ph1.json` 还提供 `TimingUltra`：place effort/opt_timing/logic_level/critical-path/post-place 均加强，`hfn_opt_effort=high`，route `post_route_opt=high`，并有 4 轮额外 post-route 优化。当前工程 `physical_attempt2/road_dynamic_overlap_low_io_top.al` 仍是 `Default_PhysicalDesign_Strategy`，`build.tcl` 也只是普通 `optimize_rtl -> optimize_gate -> place -> route`。

但“工具支持”不等于“本轮已经做过且有效”：

- 当前默认流程其实已经进行多轮 HFN 处理，例如 pre-pack 处理 78 个 HFN/复制 511 个实例，post-pack 又处理 17 个/复制 66 个；布线阶段也多轮尝试 HFN 优化。fanout 844 的 `u_pre/u_round/i_advance` 仍留在最终网表，说明泛化的默认复制不足以闭合此网。
- 日志虽调用 `phys_opt -post_route -effort low`，但在 WNS `-2.408 ns`/102 FEP 起点直接报告 `Bail out post-route opt flow because bad initial timing`，relocation/reroute/DR 尝试数均为 0；不能把这条命令的存在算成有效 post-route 优化实验。
- 定向 HFN 复制最可能帮助 A 组，但不能保证修复 B 组的 7 级状态锥，也不能保证修复 30 个 reg-to-DSP 输入长锥，更不处理外部 I/O 违例。

### 最小可行的下一步及授权边界

1. **先做纯物理候选，已在本轮独立 P&R 范围内获准**：复制 `physical_attempt2` 的冻结输入和约束，保留当前结果，单独尝试官方 `TimingUltra`。这是不改 RTL/SDC 的最小整体验证；必须重新保存全量 setup/hold/removal、ignored/abnormal、clock、check_timing，并回归功能/网表等价性。它只是候选，不得预先承诺收敛；本报告没有执行它。
2. **若 TimingUltra 未解决 A 组，可在同一已批准纯工具范围内另存定向复制候选**：从与该候选严格匹配的已加载数据库查询 `.../u_pre/u_round/i_advance` 的真实 net object，再使用 TD 支持的 `force_replication_on_nets`/fanout threshold。不要按报告字符串猜 `get_nets` 语法，也不要盲目复制 `result_tag`、reset 或整棵控制树。该操作不改 RTL 源语义，但会改变物理网表，必须做等价、功能和全量 STA 验证，且不得无限换 seed。
3. **若纯物理方案后仍有 B 组或 reg-to-DSP 违例，必须另行取得 RTL/协议授权**：候选方向是把 retirement ready/advance 决策局部化或注册化，以及缩短 runner 到 probe DSP 输入的选择锥；这些会触及 backpressure、可见延迟、II 或 debug 事件优先级，不能在本只读任务中假定等价。
4. **不得用时序例外或虚构 delay 收口**：不为 A/B/DSP 路径添加 false path、multicycle 或 min/max 例外；不以换 seed 单次变绿、`-hold_fix` 或仅看 `internal_reg_to_reg.timing` 代替全量签核。`-hold_fix` 也不是内部 setup 的根因修复。

现有授权已覆盖保存基线后的 `TimingUltra` 纯物理候选，以及同一纯工具范围内、另存结果的已查询 `i_advance` net 定向复制候选；两者都不得改 RTL、数值、II、SDC 或时序例外，也不能无限试 seed。只有纯物理证据仍不足时，才需要用户另行决定是否接受 ready/advance 或 probe 输入边界的 RTL 延迟/II 变化。

### 已核实的 `TimingUltra` 设置入口（未执行）

本轮已经授权一个独立纯工具 P&R 候选，但本报告没有执行它。TD 工程 XML 的当前物理 run 为：

```xml
<Run Name="phy_1" Type="PhysicalDesign" ...>
    <Strategy Name="Default_PhysicalDesign_Strategy">
    </Strategy>
```

官方策略名对应的最小 XML 替换是把物理 run 的 `Strategy Name` 改为 `TimingUltra`；综合 run 仍保持 `Default_Synthesis_Strategy`。为避免当前自写 `build.tcl` 对 active-run 策略装载行为产生歧义，更可审计的做法是在 `open_project ... -single_run` 之后、`place` 之前显式加入下列由 `official_strategy_ph1.json` 原样转写的参数：

```tcl
set_param place effort high
set_param place opt_timing high
set_param place logic_level_opt on
set_param place aggressive_opt 21
set_param place aggr_neighbor_dist 5
set_param place enhanced_beeline_opt 3
set_param place timing_driven_mode on
set_param place shifter_opt on
set_param place crit_path_opt on
set_param place post_place_opt high
set_param place hfn_opt_effort high
set_param place split_data_from_clock on
set_param route post_route_opt high
set_param route postrt_opt_extra_round 4
report_param
```

`set_param <step> <param> <value>` 和无参数 `report_param` 的语法可在 TD 自己生成的 `td_project/camera_to_dsi_display_Runs/phy_1/camera_to_dsi_display.tcl:77` 及 `:79` 附近核对；上面 14 个参数名和值来自 PH1 的官方 `TimingUltra` 条目，不是推测值。`report_param` 应保留在日志中证明实际生效。

已观察到的基线是 `Default_PhysicalDesign_Strategy`，普通生成流打印 place `effort=medium`、`hfn_opt_effort=medium`、`logic_level_opt=off`、`opt_timing=medium`、`post_place_opt=auto`，route `post_route_opt=auto`；当前 attempt2 日志也明确使用 medium HFN，并最终调用 low-effort post-route。未在日志中打印的默认参数不作臆测。

`TimingUltra` 的官方条目 `is_syn="phy"`，14 项全部属于 `place` 或 `route`；没有 `read_sdc`、`set_false_path`、`set_multicycle_path`、clock/delay 或其他约束项。因此该设置本身不自动添加时序例外，也不改 RTL/数值/II；它会改变物理映射、复制、放置与布线。候选仍应对比 `shell.sdc` 哈希以及 `timing_exceptions.rpt`/`timing_ignored.rpt`，防止把路径名漂移误认成约束变化。

### 覆盖全部 DSP 输入的追加报告语法（未执行）

当前 `dsp_all.timing` 仅从 DSP 输出出发。沿用工程已验证可解析的 `get_cells/get_pins` 写法，追加以下目标端报告即可覆盖当前所有 `PH1P_PHY_DSPSIOU_V2` 实例的全部 input-direction pins；不再只看 `$dsp_q`：

```tcl
set dsp_cells [get_cells -hier -filter {REF_NAME == PH1P_PHY_DSPSIOU_V2} *]
set dsp_inputs [get_pins -of $dsp_cells -filter {DIRECTION == input} *]
report_timing_path -to $dsp_inputs -ep_num 100000 -path_num 1 -file dsp_inputs_all.timing
```

这里只使用 `-to $dsp_inputs`，不加 `-from $all_regs`，因此不会漏掉来自端口、LUT、寄存器或其他硬块的 DSP 输入路径；`DIRECTION == input` 也不按 `xa/xb` 名字裁剪，数据、使能、模式/控制和时钟类 input pins 均先进入集合，由 STA 报告有效 timing endpoints。现有 30 个 `...mult0_syn_57.xa[*]` setup 端点将落入此集合。若某些 dummy/unconnected control pin 没有合法 timing path，它们仍应由 `check_timing_verbose.rpt` 核对，而不是从 DSP 输入集合中预先排除。

## 追加：ready=1 最终源码的 `physical_attempt3` 与 `physical_opt`

> 本节以 `reports/mac_task_stream_20261009/physical_attempt3/` 为 ready=1 当前源码的默认物理基线，并以已完成的 `physical_opt/` 为同源码、同 SDC/ADC 的官方 `TimingUltra` 对照。它取代上一节 `physical_attempt2` 作为当前候选证据，但不改写该轮历史结果。

### `physical_attempt3`：51 个内部 setup 失败的精确分组

`coverage_100000_violations.timing` 为 Routed confidence、STA coverage `100.00%`，Slow/Fast 的 Max/Min 四项均检查，CRPR 开启。全量 setup 为 66 个失败端点、SWNS `-1.631 ns`；其中 15 个是外部输出，51 个是内部端点。51 个内部端点虽然都从 `state_current_reg[1]_syn_2` 发出并共享早段 state decode，但落入三个不同的下游控制锥：

| 类别 | 数量 | 最差端点与 slack | 路径构成 | 根因 |
|---|---:|---|---|---|
| 寄存器端点 | 4 | `cnt_output_reg[2]_syn_214.ima`, `-0.848 ns` | data `10.659 ns`；cell `1.902 ns`/17%，net `8.757 ns`/83%；7 级 LUT；max fanout 24；末段网 `3.090 ns` | `state_current` 参与 `flag_cnt_output_clear/increment` 后更新 `cnt_output`，属于深状态解码、计数器反馈与远距离路由 |
| DSP 输入端点 | 46 | `road_mac_probe_Inst_tile/mult4_syn_57.xa[23]`, `-0.689 ns` | data `10.299 ns`；cell `1.617 ns`/15%，net `8.682 ns`/85%；5 级 LUT；max fanout 70 | `state_current == ST_MAC_SEND` 经 `flag_mac_input_valid`/`flag_mac_input_accept`、probe 输入选择后到 DSPSIOU 输入寄存端，主要是控制/路由锥，不是 DSP 输出算术路径 |
| distributed RAM 写使能 | 1 | `ramread2_syn_9292.we`, `-0.334 ns` | data `9.992 ns`；cell `2.340 ns`/23%，net `7.652 ns`/77%；7 级 LUT；max fanout 36；终段为 `DRAM (reg)` | `state_current == ST_IDLE` 经 `o_load_ready -> flag_load_accept -> flag_halo_load_write` 控制 `reg_halo` 写入，属于分布式 RAM 的 WE 解码/路由 |

RTL 对应关系位于当前 `reports/mac_task_stream_20261009/rtl/down2_dynamic_tile_runner.v`：

- `:265-269`：`state_current` 进入 `flag_mac_input_valid`，再与 `mac_input_ready` 形成 `flag_mac_input_accept`；
- `:319-320`、`:285`、`:300-301`、`:817-821`：state/IDLE 生成 load ready，再形成 halo load write，最终写 `reg_halo`；
- `:412-452`、`:689-699`：状态解码产生 `flag_cnt_output_clear/increment` 并更新 `cnt_output`。

所以“51 个都同源”不等于“51 个都是一个可由 fanout replication 单点解决的根因”。共同上游是 state decode；寄存器、DSP 输入、distributed-RAM WE 三类下游各自还有不同的深逻辑和长网。尤其 `ramread2_syn_9292.we` 是 LUTRAM/DRAM 写使能，不是 SiLU 的 PH1P ERAM，不能归入前文 `i_rx_data -> ERAM.dia` 外部路径。

### `physical_opt`：官方 `TimingUltra` 的实际对照

`physical_opt/input_manifest.json` 与 `physical_attempt3/input_manifest.json` SHA-256 完全相同；`shell.sdc` 哈希均为 `9D7A4652CA51DAC7217F25DEA02E8D2019F0EC64B4A2BF84E2FF19FB9F681ADA`，`shell.adc` 哈希均为 `849F310976CAC0090E8432F50E39EE3AE8EB407FA7F8FAAC2669D92DB5ADF384`。日志逐项记录了上一节列出的 14 个 `set_param place/route` 及 `report_param`，`strategy.json` 指向官方 PH1 `TimingUltra`，没有 RTL、数值、II、SDC 或时序例外变化。两轮 `timing_exceptions.rpt` 和 `timing_ignored.rpt` 均为空；文件哈希不同仅来自生成时间和 Constraint File 路径文本。

该轮同样是 Routed confidence、100% STA coverage、Slow/Fast Max/Min 四项全查且 CRPR 开启。结果如下：

- 全量 setup：17 个失败端点，SWNS `-0.581 ns`，全部是 `o_rx_ready/o_tx_valid/o_tx_data[*]` 外部输出；内部负 setup 为 0。
- 全量 min：45 个外部 hold 失败，最差 `i_rx_data[7] -> SiLU ERAM.dia[6]` 为 `-0.798 ns`；5 个外部 reset removal 失败，最差 `i_rstn -> reg_release_done_reg_syn_3.asr` 为 `-1.246 ns`。内部负 hold/removal 为 0。
- 内部 reg-to-reg：setup WNS `+0.091 ns`，hold WNS `+0.021 ns`。
- 全 DSP 输入：内部 setup 最小 `+0.052 ns`，内部 hold 最小 `+0.114 ns`；没有 DSP 输入负路径。
- 全 distributed-RAM WE：setup 最小 `+0.089 ns`，hold 最小 `+0.246 ns`；`physical_attempt3` 的 WE 失败已消失。

当前最紧的三类内部 setup 正裕量是：

1. **DSP input `+0.052 ns`**：`reg_release_done_reg_syn_7 -> road_mac_probe_Inst_tile/mult15_syn_57.y[7]`，data `9.582 ns`，cell `1.445 ns`/15%，net `8.137 ns`/85%，5 级 LUT，max fanout 1826。路径由同步释放寄存器经 `u_chain/i_rstn`、`pp_fault`、runner 控制和 `flag_mac_input_accept` 到 probe DSP 输入；虽然已经通过，52 ps 裕量仍很薄，且功能控制继续使用同步 release/reset 派生网。
2. **distributed-RAM WE `+0.089 ns`**：当前映射中最紧为 `flag_multiplier_loaded_reg_syn_6 -> ramread0_syn_2037.we`。这说明 TimingUltra 对整个 DRAM-WE 类别闭合，而不是保证原 `ramread2_syn_9292` 实例名或布局保持不变。
3. **reg-to-reg `+0.091 ns`**：`state_current_reg[1] -> cnt_silu_cycles_reg[9].cea`，data `9.648 ns`，cell `1.313 ns`/13%，net `8.335 ns`/87%，4 级 LUT，max fanout 32；终段控制当前 debug/性能计数器的清零/使能（RTL `:841-862`）。

内部最紧 hold 是 `u_post/u_round/reg_quotient_rem_reg[33] -> reg_quotient_increment_reg[33]`，slack `+0.021 ns`、data `0.187 ns`、0 级逻辑；因此不能只看 setup 变正就宣称裕量充足。

### DSP/ERAM 输入按内部与外部来源拆分

`physical_opt/dsp_inputs_all.timing` 和 `eram_inputs_all.timing` 使用全 input-direction pin 集合；按报告实际列出的 Begin Point 拆分如下：

| 硬块输入 | 内部 setup 最小 | 内部 hold 最小 | 外部 setup 最小 | 外部 hold 最小 |
|---|---:|---:|---:|---:|
| DSP input | `+0.052 ns` | `+0.114 ns` | 合并报告未独立选出 | `+0.469 ns` |
| SiLU ERAM input | `+1.995 ns` | `+0.157 ns` | `+6.056 ns` | `-0.798 ns` |

DSP 报告采用“每 endpoint 每检查取 1 条最差路径”；1941 个 setup endpoint 的被选最差路径全部来自内部，因而报告没有给出独立的外部-source setup 最小值。可以确认外部 DSP setup 没有压过 `+0.052 ns` 的 endpoint 最差值，也没有全量负违例，但不能从现有合并报告编造一个精确的外部 DSP setup 数值。DSP reset pins 另有内部 recovery `+6.649 ns`、removal `+0.124 ns`，均通过。

ERAM 拆分是明确的：内部最差 setup 为 `state_current_reg[1] -> SiLU ERAM.addra[11]` (`+1.995 ns`)，内部最差 hold 为 `reg_table_addr_reg[2] -> addra[6]` (`+0.157 ns`)；外部 setup 最差是 `i_rx_data[3] -> dia[3]` (`+6.056 ns`)，外部 hold 最差是 `i_rx_data[7] -> dia[6]` (`-0.798 ns`)。这再次证明 ERAM 内部端已闭合，但外部 data-to-ERAM hold 仍未签核。

### 资源与可批准边界

`physical_opt/shell_route.area`：8029 slices、30 DSP、1 ERAM、5005 registers；相对默认 `physical_attempt3` 的 7990 slices/30 DSP/1 ERAM/5023 registers，属于纯物理/映射策略造成的小幅变化。

因此可以把 `physical_opt` 记录为“当前约束模型下，100 MHz routed 内部 setup/hold/removal 全部无负路径”的纯物理候选；不能把它写成整体时序签核或部署签核，因为 17 setup、45 hold、5 removal 外部端点仍失败，外部契约仍为零 I/O delay/自动 I/O 模型。

`reports/mac_task_stream_20261009/shell_routed_opt/receipt.json` 已记录 `physical_opt/routed_netlist.v` 的两套同向量回归：`fixed_stress` 与 `dynamic_stress` 均为 `TB_PASS_RUNTIME_LAYER_SHELL tiles=3 exported=1152 guards=3 core_cycles=2607`。两份仿真日志最终均为 Errors `0`；`fixed_stress` 保留 239490 条 warnings，`dynamic_stress` 保留 580 条 warnings，编译日志为 Errors `0`/Warnings `578`。receipt 明确 `sdf=false`，所以这是未标注 SDF 的 routed-netlist 功能回归 PASS，可与 STA 内部闭合证据并列；它不是 formal equivalence，也不是带延迟门级仿真，不能清除外部 STA、check_timing 或大量模型 warning 的签核边界。
