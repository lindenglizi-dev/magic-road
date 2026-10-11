# RoadYOLO v7 低 I/O 最小计算链物理验证报告

## 1. 结论先行

本轮已在安路 Tang Dynasty 6.2.168116 中，对冻结的 `road_low_io_physical_shell` 和最小计算链完成 PH1P35MDG324、速度等级 -3、100 MHz 的综合、布局布线和最终 STA。没有生成 bitstream，没有上板，没有修改生产工程、冻结 RTL、数值契约、接口、复位语义或 II。

阶段结论是：**布局布线完成，setup 通过；完整时序未通过。** 最终 setup WNS 为 **+0.208 ns**，0 个 setup 违例；全局最差 min slack 为 **-1.588 ns**，445 个违反检查。负余量主要是外部异步复位释放的 removal，以及诊断窄口在 0 ns 输入 min delay 假设下的 I/O hold，不是内部寄存器到寄存器、DSP 或 ERAM 数据路径 hold 失败。

原生 `route fix_hold=on` 候选没有改善结果。TD 6.2.168116 的实际参数数据库显示，PH1P 当前默认已是 `fix_hold=on`；官方手册列出的 `High` 只支持 PH2，因此本轮停止继续猜参数。若要闭合剩余 min 违例，需要决定真实板级输入/复位关系，或批准复位同步释放等契约变化，不能靠新增 false path、multicycle、任意 I/O 延迟或放宽门槛处理。

这份结果只证明当前低 I/O 壳与最小计算链的物理基线，**不证明完整 67 层 RoadYOLO、DDR 调度、5 FPS 或生产工程已经通过。**

## 2. 冻结范围与工具

| 项目 | 冻结值 |
|---|---|
| 顶层 | `road_low_io_physical_shell` |
| 顶层 I/O | 38 bits：`clk/rstn + RX16 valid/ready + TX16 valid/ready` |
| 器件 | PH1P35MDG324，speed 3（即 -3） |
| 时钟 | `probe_clk`，10.000 ns，100 MHz |
| 非时钟输入边界 | max=min=0.000 ns |
| 输出边界 | max=min=0.000 ns |
| 复位 | 外部异步低有效；未排除 recovery/removal |
| TD | 6.2.168116；可执行文件 SHA-256 `e2e04ada5e256dccd017240c0f4dcface7f96dca67cde0e56e606ac0e02f827a` |

关键冻结 SHA-256：

| 文件 | SHA-256 |
|---|---|
| shell RTL | `c7bd74ccf995f7f7a8527e7c6f8f661183bccd0a3f266922d4c0a026d019f5d5` |
| shell TB | `62424751aab4f8292a154531600cab2d630e1a7813238056700a8b44dcc86bc6` |
| chain | `6ec48c6ddda89ab91e66926c42e012b3d9c45cc93150823ffb50c1eb627f7132` |
| signed33 MAC | `f8bf6cace6eb99bd9b915be5e27e1d38af4b3a2485ffeb6e87675d8bfc3478e8` |
| round | `cb8f1e308e5832eecc9d5a0cebb86df221ea5f12abe97a5796dc49bea04b382d` |
| SiLU | `5f357b493c7b3f941d9fa954a0ce5ec09091e466b641474360d2f64d0e42c938` |
| SDC | `7ff9ccbef9990028a6473d5085799eab18d5c7edacc263b8b66e62840160acde` |
| baseline gate DB | `2ddbed3ba4f9f467a9b71acfa2e3ec7332eff2c41b3689757642d91ea72cc9b7` |
| baseline routed DB | `1e08334a4c5d175343bd35cccaa03dd8049c83783684c5e3cadec28e07033535` |

0/0 ns 是无板级数据时的同相理想诊断边界，不能作为开发板接口证据。自动引脚只用于隔离实现。物理目录中没有 `.bit`、`.bin` 或 `.mcs` 文件。

## 3. 功能前提与门禁状态

冻结 C7BD shell 的独立 ModelSim 结果为完整重编译 0 error/0 warning；14 个功能组全部通过、0 test error，另保留 2 条厂商 ERAM `INIT_FILE` warning。覆盖部分装载、反压、96 包、24 组/192 项、正负 signed33 暂时超界后恢复、最终溢出、三路原子故障、复位取消、真实缓存逐项导出等场景。

严格交付门仍未通过：shell 667 errors，显式包含 TB 时 219 errors；冻结计算链原 374 条诊断也继续保留。当前物理成功不能替代 `ast/readability/comment/naming/profile` 等失败，也没有把外部 ModelSim 结果冒充 public `toolchain` gate 通过。

## 4. 实际资源

以下数字来自 routed `shell_route.area`，全部包含验证壳：

| 资源 | 使用 | 器件总量 | 占比 |
|---|---:|---:|---:|
| Slice | 4,068 | 21,216 | 19.17% |
| LUT6 | 3,131 | 21,216 | 14.76% |
| Slice register | 3,782 | 42,432 | 8.91% |
| PLB | 841 | 2,652 | 31.71% |
| ERAM20K | 1 | 108 | 0.93% |
| DSP | 26 | 40 | 65.00% |
| I/O | 38 | 160 | 23.75% |
| GCLK/SCLK | 1 / 4 | 32 / 48 | 3.12% / 8.33% |

能可靠按层级分开的逻辑资源如下；Slice 因跨层级打包不能可靠相减，仍标记“含验证壳”。

| 范围 | logic LUT | ripple | seq | ERAM | DSP | DRAM LUT | shifter LUT |
|---|---:|---:|---:|---:|---:|---:|---:|
| 总体 | 1,525 | 854 | 3,782 | 1 | 26 | 744 | 8 |
| 计算链 | 1,061 | 622 | 2,681 | 1 | 26 | 8 | 8 |
| 壳差值 | 464 | 232 | 1,101 | 0 | 0 | 736 | 0 |

96×362-bit 包缓存主要被实现为分布式 RAM，导致壳本身使用 736 个 DRAM LUT。这是验证壳成本，不可外推为生产接口成本。

综合网表和 routed 网表保留了 24 个动态 8×8 MAC lane，以及一个共享 32×32 重定标乘法器；后者占 2 个 DSP site，总计 26 DSP。固定重定标系数仍是冻结内部契约，没有增加动态系数端口；本结果不能代表通用运行时系数乘法器成本。SiLU 的逻辑契约是 1,024 项 signed16 runtime 表；冻结 RAM 源的 `DATA_WIDTH=20` 使它在物理上配置为 1024×20，并实际映射为 1 个 ERAM20K，没有改变外部 signed16 数值契约。

## 5. 完整时序分类

最终报告覆盖 10,109 个端点、45,159 条分析路径，`STA coverage=100.00%`。重导时 `ep_num=20000`，没有沿用会截断端点的 10,000 上限。

| 类别 | 最差 slack | 违例 | 说明 |
|---|---:|---:|---|
| 全局 setup | +0.208 ns | 0 | 通过 |
| 内部 reg→reg setup | +1.382 ns | 0 | 通过 |
| 内部 reg→reg hold | +0.027 ns | 0 | 通过 |
| DSP operand setup / hold | +0.938 / +0.117 ns | 0 / 0 | 通过 |
| DSP result setup / hold | +3.113 / +0.465 ns | 0 / 0 | 通过 |
| ERAM input setup / hold | +4.182 / +0.027 ns | 0 / 0 | 通过 |
| ERAM output setup / hold | +6.614 / +0.871 ns | 0 / 0 | 通过 |
| 诊断输入 setup / hold | +3.285 / -0.531 ns | 0 / 36 | 0 ns min 输入边界 |
| 诊断输出 setup / hold | +0.554 / +2.630 ns | 0 / 0 | 通过 |
| reset recovery | +4.168 ns | 0 | 2,502 个适用寄存器端点 |
| reset removal | -1.588 ns | 393 register endpoints | 未通过 |

全局 `viol_only` 中共有 445 个违反检查：401 条 removal 和 44 条 hold。44 条 hold 又分为 36 条诊断输入 hold，以及 8 条 `i_rstn` 到 DSP reset pin 的 hold；这 8 个 DSP reset pin 同时还有 removal 检查。普通内部数据 hold 没有负余量。

最差 setup 是验证壳 `reg_packet_mask_reg[5]` 到分布式 RAM `ramread0_syn_3993.we`，数据路径 9.488 ns，其中 net 7.263 ns，占 77%；逻辑层级 6，扇出 46。它是壳包缓存写使能路径，不是 MAC、SiLU 或 ERAM 关键路径。

最差 min 路径是 `i_rstn` 到 MAC 内 `reg_base_quad_reg[26].asr` 的 removal，slack -1.588 ns。复位网扇出 2,529，路径到达 1.390 ns，而 capture clock 到达 2.978 ns。该失败是异步释放相对内部 SCLK 的关系，不能用“内部数据 hold 通过”掩盖。

## 6. RAM/DSP 端点证据

routed DB 中确认 26 个 `PH1P_PHY_DSPSIOU_V2` site 和 26 个配对 `PH1P_PHY_DSPMULT_V2` sub-cell；专项 STA 实际分析 1,128 个 DSP operand 端点和 421 个 DSP result 端点。动态 MAC 操作数没有被编译期常量替换。

SiLU 的逻辑 1024×signed16 runtime 表确认映射为一个物理 1024×20 `PH1P_PHY_ERAM_V2`：输入侧专项 STA 覆盖 32 个有效端点，输出侧覆盖 16 个有效端点。RAM 地址、写数据、写使能和读数据路径均存在于 routed timing，不是只依据 RTL 实例名判断映射。

## 7. DRC、覆盖率和未关闭告警

- `check_timing` 最终重导：0 invalid constraints、0 combinational loops、0 missing input/output delays、0 partial input/output delays、0 no-path constraints。
- timing exception 与 ignored 报告为空；没有 false path、multicycle 或新增例外。
- DRC：clock bound、force-route、sigmap、duplicated-self-driven、bound check 通过；没有 multi-drive；clock net 未使用 local routing。
- 保留 `PHY-1035/PHY-1039`：冗余属性，以及 8 个 MAC `flag_front_valid` 相关 MSLICE 无已用 reg/CE 属性。
- 保留 `PHY-5089`：437 条异常 min path 因 clock skew>1000 ps 或 hold slack<-1000 ps 被 router 跳过。它们主要对应高扇出异步复位，不能因 coverage=100% 而宣布关闭。
- 原构建阶段的 `check_timing_verbose.rpt` 曾显示 1 个 local clock 和 1 个 generated clock 未连 master；从最终 `pr.db` 重导的 `full_check_timing_verbose.rpt` 为 0/0，且 clock summary 只显示 primary `probe_clk`。两份原始记录均保留，按报告顺序差异处理，不删除早期记录。
- `check_timing` 仍列出 DSPSIOU `mul9_mode/mul9_signed` 和一个 SiLU slice `ofa` 的 dummy-node 告警；综合网表映射和功能回归未证明它们造成数值错误，但严格门未因此豁免。
- `report_route_status -drc -file` 在此 TD 版本没有生成独立 `shell_route_status.rpt`，实际 DRC 输出保存在 `td_20261006_185614.log`。这是报告导出限制，不能把缺文件写成 DRC 未运行。

## 8. 原生 hold-fix 候选

安装的 SWUG105 说明 `route fix_hold=on` 可用于全部器件，`High` 仅支持 PH2。对 baseline `gate.db` 的实际查询显示 TD 6.2.168116 在 PH1P 上的数据库默认已经是：

```text
fix_hold=on, hold_fix_iteration=5, post_route_opt=auto, timing=on
```

因此独立候选再次设置 `fix_hold=on` 是无实质参数变化的对照。候选完整 P&R 的资源和时序与 baseline 相同：4,068 Slice、26 DSP、1 ERAM、setup +0.208 ns、min -1.588 ns、445 个违反检查，仍跳过 437 条异常 min path。候选没有被采纳为“修复”。

较强的 `High` 不支持 PH1P，本轮不尝试；也没有增加 delay cell、修改 reset、添加 SDC 例外或调大外部 min delay 来制造绿色结果。

## 9. 周期与吞吐损失

低 I/O 壳仿真实测 base16：预装载 2,428 cycles，核心 436 cycles，结果导出 60 cycles。按 100 MHz 分别为 24.28 us、4.36 us、0.60 us。最大 96 包/四位置用例为预装载 6,564 cycles、核心 1,404 cycles、导出 60 cycles。窄口预装载和导出不计作计算核吞吐。

base16 核心 436 cycles 的互斥分解是：MAC 88、前重定标 132、SiLU 84、后重定标 120、提交 12。前后重定标共 252 cycles，占 57.8%；加上串行 SiLU 后为 336 cycles，占 77.1%。因此当前最小链的主要吞吐损失是单上下文的前重定标→SiLU→后重定标串行等待，不是 MAC 物理关键路径。

这只是代表性最小链周期，不能换算成完整 67 层网络 FPS。后续主线应按已批准计划转向真实逐点卷积层、深度卷积和小网络块，再做全层调度周期模型。

## 10. 需要集中决定的后续项

1. 提供真实板级 RX/TX 与 `probe_clk` 的 max/min delay 后，替换 0/0 ns 诊断假设；在此之前 36 个输入 hold 不能判作板级失败或通过。
2. 若外部 `i_rstn` 可能异步释放，需要批准“异步置位、同步释放”的复位入口方案或等价板级时序保证，再重新做 recovery/removal 和复位取消回归。当前不授权改变复位契约。
3. 严格门 667/219/374 条仍需独立关闭；物理结果不豁免它们。
4. 完整 CNN 尚需权重 ROM、真实 PW/DW 卷积、DMA/DDR 和全层调度实现后，才能回答 DSP≤40、ERAM≤108、整机时序及 ≥5 FPS。

## 11. 证据索引

- baseline DB/netlist：`gate.db`、`pr.db`、`gate_netlist.v`、`routed_netlist.v`
- 资源：`shell_route.area`、`shell_route_ram.rpt`
- 全端点 STA：`full_20000_all_paths.timing`、`full_20000_violations.timing`
- 分类 STA：`full_internal_reg_to_reg.timing`、`diagnostic_inputs_to_regs.timing`、`regs_to_diagnostic_outputs.timing`、`reset_recovery_removal.timing`
- hard-block STA：`dsp_operand_paths.timing`、`dsp_result_paths.timing`、`eram_input_paths.timing`、`eram_output_paths.timing`
- 覆盖与异常：`full_check_timing_verbose.rpt`、`full_timing_exceptions.rpt`、`full_timing_ignored.rpt`、`full_abnormal_targets.rpt`
- 原始 TD 日志：`td_20261006_185614.log/.logw`、`td_20261006_190550.log/.logw`
- hold-fix 对照：`hold_fix_candidate/`

