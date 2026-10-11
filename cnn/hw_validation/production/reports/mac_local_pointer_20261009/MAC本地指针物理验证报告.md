# RoadYOLO MAC 本地指针物理验证

本轮候选未通过全量内部时序，不替代上一版基线。只保留本地读指针确实解决了 MAC DSP 使能端点，但其他调度控制路径转为失败：内部 setup 从 2 条增加到 12 条，最差裕量由 −0.222 ns 变为 −0.374 ns。功能回归与核心周期保持，不能据此宣布 100 MHz 时序闭合。

## 修改与实际映射

比较基线为冻结的 `control_operand_hold_20261009`，当前结果仅在 `mac_local_pointer_20261009`。实际唯一 RTL 差异是 [road_mac_probe.v](rtl/road_mac_probe.v) 第 189 行增加 `(* preserve *)`。去掉这一属性后与基线逐字节一致；其他七个 RTL 文件不变，算术、端口、II、延迟、复位、故障原子性和同拍释放信用旁路均未改变。

安路安装目录的 SWUG106 第 4.2.14 节、印刷页 43–45 明确说明该属性用于防止寄存器合并和常量优化。[本地厂商手册](E:/Anlogic/TD_6.2.1_Engineer_6.2.168.116/doc/SWUG/SWUG106_HDL_Coding_Synthesis_User_Guide.pdf)

综合网表中，基线只有两位 runner `ptr_pw_meta_read`，MAC 本地 `ptr_result_read` 被合并；候选保留两套各两位寄存器。本地指针实际连接 MAC 结果队列读地址，不是悬空保留。相关证据见 [变更范围](scope_check.json)、[实际差异](rtl_change.diff)、[映射与端点核查](local_pointer_diagnosis.json)。

## 实际资源与全量时序

实际顶层为 `road_dynamic_overlap_low_io_top`，包含 DW/PW 调度、MAC、动态量化、SiLU、缓存和 38 位窄口壳。目标 PH1P35MDG324、速度等级 −3、100 MHz。原构建脚本、SDC 和 ADC 保持不变，没有新增时序例外或真实外设延迟。

| 项目 | 上一版冻结基线 | 本轮候选 |
|---|---:|---:|
| 全量内部 setup 失败端点 | 2 | 12 |
| 内部最差 setup | −0.222 ns | −0.374 ns |
| MAC DSP CE 最差 setup | −0.222 ns | +0.135 ns，24 个端点均无负值 |
| 内部最差 hold | +0.021 ns | +0.020 ns |
| 内部最差 recovery | +3.915 ns | +4.528 ns |
| 内部最差 removal | +0.048 ns | +0.077 ns |
| Slice，含壳 | 7,994 | 7,998 |
| 寄存器，含壳 | 5,371 | 5,360 |
| LUT6，含壳 | 7,096 | 7,133 |
| DSP，含壳 | 30 | 30 |
| ERAM，含壳 | 1 | 1 |
| 核心端点周期 | 1,687 | 1,687 |

寄存器总数受本轮整体映射和物理打包影响，不能把“本地保留两位”解释为整机寄存器数必然增加两位。资源无法可靠拆成壳与核，均标为含壳；不包括完整 ROM、DDR、视频链和整网后处理。

STA 工具报告覆盖率 100%，报告保留 DSP/ERAM 端点、复位入口、同步器级间、功能复位分发及原始数据库。覆盖率不代表全部约束检查和外部接口已签核。外部仍有 setup 16、hold 30、removal 4 条失败，最差分别 −0.916 ns、−1.015 ns、−0.718 ns。

证据：[物理汇总](physical_analysis.json)、[全部路径](physical/coverage_100000_all_paths.timing)、[全部违例](physical/coverage_100000_violations.timing)、[约束检查](physical/check_timing_verbose.rpt)。

## 十二条失败的实际原因

12 条失败均为 slow_m40c 的 setup，按端点分为四个 `cnt_output` 寄存器输入和四个权重寄存器的八个 CE 输入；后八条裕量都是 −0.033 ns。最差四个计数端点为 −0.374、−0.244、−0.171、−0.082 ns。

不能按物理单元名称判断语义。报告的起点叫 `u_post/u_round/fault_o_reg_syn_3.clk`，但路由网表显示该 LSLICE 同时装有两个独立寄存器：`oqa` 是重定标 fault，`oqb` 是 MAC 的 `ptr_result_read[0]`。实际失败路径由 `oqb` 发起；它不是新出现的重定标故障计算问题。本轮最初按起点名称归因的说法已更正。

最差实际链路是：

```text
MAC 本地 ptr_result_read[0]
  → 结果队列 DRAM 的 fault 位读取
  → 结果/输入接受资格逻辑
  → 末组与输出计数 clear/increment 控制
  → cnt_output 寄存器数据输入
```

数据延迟 10.113 ns，其中单元 1.747 ns、布线 8.366 ns，约 83% 来自布线；共有六级逻辑，最大扇出 58。保留本地指针只能改变发起位置及映射，不能消除异步队头读取、接受资格与计数选择之间的组合深度。因此“本地寄存器保留成功”不等于“整个控制链成功”。

下一项应收窄到调度控制，不改乘加或 SiLU：先验证 `cnt_output` 的后继值能否只依赖状态、通道、空间位置提前计算，再以真实握手提交，移除接受许可之后的 clear/increment 选择深度。同时单独追踪八个权重 CE 端点与同一接受许可的关系，不能仅假设它们会随计数修复消失。源码中权重装载分别出现在 ST_STORAGE、PW 非末归约组接受、PW 末归约组接受且不是最后空间/输出组；这些资格可在接受事件之前预解码，但最终更新仍必须保留原故障优先级和真实握手。

这是下一候选建议，不是已实施修改。修改前需做局部布尔对拍，覆盖 PW 末输出组、末空间点、DW 第 15 通道、DW 排空、复位和故障禁止接受。不能给故障晚一拍、删除信用旁路或改变接受事件；若需要这些变化，先请求决定。本轮不继续叠加补丁，也不晋升当前候选。

## 功能证据与剩余交付门

| 检查 | 结果 |
|---|---|
| 完整 DW/PW 小块 | 四套向量各 16 案例，共 64 案例通过；全部计数行与基线一致 |
| MAC 压力回归 | 119 任务、849 组、1,211 拍；两个预期故障、队列满、同拍收发、停顿和复位检查通过 |
| DW 写入边界 | 四套向量通过 |
| RTL 验证壳 | 两套向量，共六个 tile、2,304 导出字节逐项一致 |
| 路由网表验证壳 | 第二次运行通过，两套向量、六个 tile、2,304 导出字节逐项一致；首次未进入仿真，失败记录保留 |

对应收据：[完整小块](simulation/receipt.json)、[周期比较](cycle_comparison.json)、[MAC](mac_sim/receipt.json)、[DW 边界](load_boundary/receipt.json)、[RTL 壳](shell_rtl/receipt.json)、[路由网表壳](shell_routed_attempt2/receipt.json)。路由网表仿真未回注 SDF，不代替静态时序；厂商原语相关仿真警告保留，不能描述为零警告。DW 仍为 1,095 拍，PW 592 拍，共 1,687 拍；详细活动沿用已冻结 trace，依据为本轮 64 个完整计数行相同，不当作新采集 trace。MAC、激活和提交活动可能重叠，不能简单相加。固定/动态测试参数通过不代表真实 QAT 模型通过，也不代表全帧 5 FPS。

八项严格门禁状态：RTL `compile` 通过；`ast、readability、comment、naming、profile` 失败；静态 `testbench、toolchain` 未请求。TB 严格解析仍失败，静态 testbench 检查通过；实际 ModelSim 和 TD 执行另列证据，不覆盖严格结果。

当前 RTL 为 5,039 errors、37 strict warnings；同范围基线为 5,037/37。新增两条分别为属性行注释对齐列从 48 移到 63 的 VG060，以及下一声明分组注释的 VG065。未为这次属性候选改写周边格式或放宽门禁。TB 为 1,663 errors、2 strict warnings，与上版相同。详见 [RTL 门禁](gate_candidate/gate.json)、[TB 门禁](gate_testbench/gate.json)。

## 运行失败与保留范围

网表回归首次在 `physical_current.json` 发布之前读取索引而退出，未启动仿真；结果发布后在独立 attempt 目录重新运行，旧失败目录和 JSON 保留。收集器首次因包装脚本未导出原有 `MAC/frozen` 别名而失败，补齐别名后收集成功。这两项是运行编排问题，不是 RTL 功能错误，也没有重跑综合或删除失败记录。

展开网未驱动查询仍为六条 `state_next` 残留记录，均 PINS 0、DRIVER 0，没有加载用户；该查询不是全部映射原语端点证明，见 [查询收据](undriven/receipt.json)。

所有输出限定本候选目录。未训练、改生产、生成位流、上板或写 Flash。冻结输入复核 2,184 项，无变化。当前原始物理记录已保留，最终收据、冻结复核和哈希以 [status.json](status.json)、[evidence_hashes.json](evidence_hashes.json) 为准。上一版继续作为比较基线，但它自身仍有两条内部时序失败，不能描述成通过版本。
