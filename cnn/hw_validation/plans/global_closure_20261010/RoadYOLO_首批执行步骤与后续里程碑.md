# RoadYOLO 首批执行步骤与后续里程碑

日期：2026年10月10日。工程：E:/project/qiansai/anlogic_topic2_work/lab1_sc500_road_vision。器件PH1P35MDG324，速度等级−3，目标100 MHz。工程不是Git仓库，采用独立目录和哈希，不安排提交或推送。

## 一 先执行哪一批

第一批只回答三个问题：两端点参考能否用最小物理分发修改闭合内部时序；现有tile调度的整网任务账究竟是多少；剩余存储和控制逻辑是否有容纳空间。第一批不写完67层、不训练、不上板，也不把缩网和新增MAC结构混进来。

执行顺序固定为：输入冻结和脚本绑定 → 修正预算 → 必要语义核查 → 单变量MAC CE候选 → 原向量回归 → 实际TD和结果分类。预算、缓存统计和DDR资料核查可以并行；候选RTL及其构建由一个执行者串行维护。

本文将[全局整改计划](E:/project/qiansai/anlogic_topic2_work/lab1_sc500_road_vision/cnn/hw_validation/plans/global_closure_20261010/RoadYOLO_全局整改与分区执行计划.md)细化为任务单。以下步骤均为待实施，不表示本轮已运行仿真或TD。对原计划补充三点：部分tile必须区分逻辑任务和实际发射策略；ROM接入使用schema2字段，不混用旧schema1；第二次物理尝试由第一次的实际失败路径决定，不机械地切到另一失败版本。

## 二 固定输入和当前失败

| 用途 | 唯一输入 | 当前结论 |
|---|---|---|
| 首选物理修改参考 | production/reports/control_operand_hold_20261009 | 2个内部setup失败端点，最差−0.222 ns；7,994 Slice、30 DSP、1 ERAM，均含壳 |
| 最新失败对照 | production/reports/scheduler_predecode_20261010 | 59个唯一内部setup失败端点、109条负路径，最差−0.565 ns；7,983 Slice、30 DSP、1 ERAM，含壳 |
| 网络和数值 | production/graph_artifacts/graph.json及deployment_contract.json | 106节点、67卷积；schema2，尚非训练完成的整数模型 |
| 运行参数读取目标 | production/numeric_artifacts/manifest.json | schema2 TEST包，140,522字节；不是E7或QAT权重 |
| 固定回归 | runtime_layer_integration_20261009/vectors和mac_task_stream_20261009/tests/vectors | 原四套小块向量、119任务/849组MAC向量 |

上述production目录均位于cnn/hw_validation/下。当前核心窗口DW为1,095拍、PW为592拍，总1,687拍；只证明down2的4×4小块。

最新59端点中，58个属于PRE round推进许可，1个属于halo RAM写使能。首选参考的两条失败则是MAC mult12/mult13的CE。两者不能用同一修改位置或同一个失败数量来描述。

最新源码静态门保持：compile通过；ast、readability、comment、naming、profile失败；testbench、toolchain字段为not_requested。实际ModelSim与TD证据另列。源码5049错误/37严格警告、TB1663错误/2严格警告不删除，也不解释成同等数量的独立功能错误。

## 三 步骤1 建立正确的新候选入口

建议新目录为production/reports/mac_ce_fanout_local_20261010/。如果已存在，使用新的唯一目录，不覆盖。本批只需要一个候选专用run.py和少量检查结果，不另建通用构建平台。

### 具体动作

1. 从control_operand_hold_20261009/rtl复制完整八文件到新目录baseline/和rtl/：down2_dynamic_tile_runner.v、road_down2_dynamic_adapter.v、road_dynamic_overlap_low_io_top.v、road_dynamic_postprocess.v、road_dynamic_requant.v、road_mac_probe.v、road_round_shift.v、silu_shared_unit.v。
2. 复制三个TB及对应spec、PH1P完整接口事实文件、inspect_undriven.tcl、dw_task_overlap.wave.json和已有模块spec。旧TB、厂商库、向量仍按哈希追溯。
3. 不复制旧physical、仿真库、gate结果、status、frozen或任何_current.json。physical目录由实际构建阶段创建，不能预建空目录冒充已有构建。
4. 对所有可能写文件的导入助手绑定新ROOT；只读依赖保持原绝对路径，使用现有工作目录归属断言。
5. 新prepare、scope和finish必须适配本候选，不能原样调用旧版本对应函数。

### 必须修正的脚本细节

| 对象 | 旧入口的实际行为 | 新入口的要求 |
|---|---|---|
| prepare | 经多层导入复制更早版本，不保证来自两端点参考 | 明确从control_operand_hold的八文件闭包准备 |
| ROOT | app、old、build、tools分别持有可写根 | 任何阶段开始前全部重定向，输出只能落新目录 |
| compare的BASE | 读取BASE/simulation_current.json | 指向本次直接比较参考control_operand_hold |
| collect的BASE | 用BASE/collect.py加载解析器 | 临时指向dw_task_overlap，解析完成恢复；不能与compare共用一次全局改值 |
| tools.BASE | 用于寻找retirement_lane_banks中的工程模板 | 保留只读模板来源及哈希，不盲目改成没有模板的新目录 |
| scope | 旧版限定其他两个RTL变化 | 新版只允许runner声明处的一个综合属性差异 |
| review | 旧分支重点审MAC或旧后处理 | 本次审实际变化的runner及新构建入口 |
| finish | 旧版写死evaluated_internal_timing_failed，且断言门禁未通过 | 根据本次实际检查分类；仍保留delivery_ready=false，不能把诊断闭合改写成生产通过 |

真正TD入口是dw_task_overlap_20261009/run.py的physical函数；scheduler_predecode/analyze.py中的physical只是事后分析。构建约束来自mac_task_stream_20261009/physical_opt中的build.tcl、shell.sdc、shell.adc，内容保持不变。

交付：input_manifest.json、frozen_check.json、path_bindings.json、候选专用run.py。通过条件：八文件准备正确，旧文件hash不变，新工作/日志/报告路径归属正确；不得引用旧_current指针作为本次结果。任一不满足，不改RTL、不启动TD。

## 四 步骤2 修正任务和周期预算

新增一个放在新验证目录的窄用途预算脚本和current_tile_budget.json；只读冻结graph及当前调度证据，不导入并直接运行旧budget.py，后者会写回它所属目录。无需新的网络编译器。

### 每层必须记录的字段

| 字段组 | 内容 |
|---|---|
| 身份和结构 | graph/node/hash、算子、H/W/Cin/Cout、kernel/stride/padding、输出类型 |
| 布局 | tile数、最后tile有效宽高、逻辑有效字节、tile存储字节、对齐分配字节 |
| 任务 | logical_required_tasks、planned_issued_tasks、每任务输入组、输出有效路、尾lane |
| 边界策略 | partial_tile_policy；没有实现依据时为UNKNOWN，不能默认跳过无效行 |
| 周期证据 | 数学下界、调度模型、RTL实测、完整层/DDR实测分别标记 |
| 额外成本 | ROM/DDR字节和等待、参数装载、写回屏障、非卷积/层切换成本 |

不要将graph的storage.raw_bytes直接当成逻辑有效字节。当前graph.py中的该值已经包含4×4 tile填充；逻辑有效字节须用H×W×C×元素字节数另算。

### 计算和自检步骤

1. 逐tile、逐有效输出行计算DW三空间点包，不能使用整行ceil(W/3)跨越tile边界。当前4列是3点包加1点包，尾包仍执行原组数。
2. DW stride2并集21槽，当前每包3组；stride1并集15槽、2组只作为已有参考/目标模型，不能标成当前RTL支持。
3. PW/Stem逻辑任务分别为H×W×ceil(Cout/3)，输入组分别为ceil(Cin/8)、ceil(9×Cin/8)。另列执行完整物理tile时的任务模型。
4. 只有down2两行绑定现有实测tile周期。其他65卷积保留UNMEASURED，不用统一系数制造“实测整网”。
5. 单独给出完整帧尚未知的成本清单；未知成本不填0，不用总预算减去已知项宣布剩余预算充足。

强制断言：

- down2为576个tile；单tile DW128任务/384输入组；完整层投影73,728任务/221,184组。
- down2 PW每tile128任务/256组；完整层投影73,728任务/147,456组。
- 两个tile端点1,095和592拍；全层投影630,720和340,992拍，仍标外推。
- DW完整4×4 tile有效乘法2,304，物理槽9,216，平均利用率25%，不能用满三点包37.5%替代。
- 图中卷积67、DW23、PW43、Stem1，六个原始预测层dtype为INT16。

部分tile的具体例子：down4.pw输出18×32×96。若跳过无效两行，逻辑PW任务18,432；若每个4×4槽都执行，模型任务20,480。逻辑有效数据55,296字节，tile存储61,440字节。填0规定不证明跳行策略已实现；planned_issued_tasks在适配器验证前保持UNKNOWN。DW同样区分有效行模型和满槽模型。

交付：67行任务表、23个DW旧新差异、部分tile策略清单，以及不含未知项的分项账。通过条件：上述断言全通过，旧预算文件不变；本阶段没有“5 FPS通过”出口。

## 五 步骤3 在花物理机时前排除真实语义错误

只读分组检查当前位宽、计数、默认状态、驱动、RAM地址/数据/使能。优先处理VG122、VG109、多驱动/缺驱动及SYN-5025；注释、命名和格式单列，不在本次物理补丁中顺手重写。

每条风险只需一行：规则/实例/信号 → 合法范围或反例 → 源码保护条件 → 结论/下一动作。已有二值范围证明可以复用，但不能覆盖X/Z、厂商时序或未知接口。

对SYN-5025，已有6个state_next对象PINS=0/DRIVER=0不等于所有置零端口都安全。有效激活、权重、bias、RAM地址/数据/使能逐项关联真实来源；有负载而无驱动则停止P1，先提交最小修复，不以补常量或过滤告警通过。

时钟异常从同一pr.db追到具体clock、pin和master。保留generated-clock异常、DSP dummy、未约束/忽略对象，不新增false path或伪造I/O延迟。模型查询若必须启动新的TD诊断，放在获批的新目录，不在旧数据库目录写输出。

交付：semantic_findings.json和clock_zeroing_questions.md。出口分为已证明合法、真实缺陷、待证；真实缺陷阻断物理优化。不能为了让统计好看把所有静态锥诊断归为格式项。

## 六 步骤4 只做一个MAC CE分发候选

准确修改位置是两端点参考runner第165行flag_mac_input_accept的wire声明；第296行接受方程不改。首试仅添加安路max_fanout=16综合属性，不加寄存器、preserve属性或预解码，不改策略/seed，不改另外七个RTL。

这个位置并非只凭信号名猜测：原coverage_100000_violations.timing第1059行附近的失败路径经过该网的复制网，实测扇出38。其作用是否真正传到DSP CE，仍须以新网表及新路径确认，不能认为属性写入即生效。

接受判据：

- 唯一RTL差异是该声明属性；移除这一条新增属性后与baseline逐字节相同。
- 接口、算术、II、反压、故障、复位、计数和约束不变，七个其余RTL哈希一致。
- 记录工具是否识别属性、有无复制、每份副本负载，以及最后网络/完整路径延迟。
- 同版本重新生成或绑定runner spec和周期图；行为没有变更时说明原图继续适用，不能拿无关新图替代接口证明。

交付：rtl_change.diff、scope_check.json、相关原/候选严格门报告和语义审查。严格门仍失败时，只有明确批准的隔离物理诊断可进入步骤6；不自动越过交付门。

## 七 步骤5 先完成同向量回归

| 检查 | 真实入口stage | 必须比较的内容 |
|---|---|---|
| 源码范围和原门对照 | scope、review、gates | 唯一属性差异；按规则/对象比较诊断，不能只比错误总数 |
| 四套小块回归 | simulate | fixed_original、fixed_stress、dynamic_original、dynamic_stress，各16案例；合计64行完整计数一致 |
| MAC任务协议 | mac_sim | 119任务、849组、1,211周期；预期故障、队列和复位检查保持 |
| 最后装载与立即启动 | boundary | 四套向量均出现DW_LOAD_BOUNDARY_PASS |
| 与直接参考比较 | compare | 64行逐字段一致；DW1,095、PW592、总1,687，不只检查最后输出 |
| 窄口真实数据流 | shell_rtl | 6 tile、2,304字节逐项一致，无丢失/重复 |
| 置零对象查询 | 受控步骤6的undriven及必要补充 | 会启动TD elaboration，不放入功能自动循环；保留原6死对象结论，不能外推为全原语端口证明 |

当前prepare/review/scope/finish不能原样复用，须先完成步骤1的入口适配。其他stage复用现函数，不重写仿真平台。新入口遇到compile真实失败或新增位宽/驱动/状态语义阻断须非零返回，不能因旧gate允许退出码1就继续后继。历史严格格式项保持真实failed；获批的隔离功能/物理诊断与生产交付分开。SiLU表和算术源码未变时复用其原数值全域证据，不再次开展SiLU优化。

第一处不一致即停止后继TD，并报告案例号、首次不同的周期/地址/tag、期望/实际值。定位按acc→pre→SiLU→post/raw→写地址顺序，不只截一段“TB失败”日志。故障案例提前结束不计作加速。

交付：本次receipt、输入哈希和cycle_comparison.json。scope、compile/语义安全或功能回归失败时，不进入步骤6。

## 八 步骤6 跑实际顶层并作一次明确决定

顶层仍为road_dynamic_overlap_low_io_top，38 I/O、PH1P35MDG324/−3、100 MHz。使用相同build.tcl/SDC/ADC和物理策略，不生成位流。

门禁和隔离TD授权核实后，先单独运行undriven及必要补充，再按physical → 校验本次manifest与pr.db → collect → 候选路径分析 → shell_routed → 新finish推进。undriven会实际调用TD进行elaboration，不能放在授权检查之前的功能循环。physical命令退出、日志无错误且本次pr.db和报告存在后，才能发布physical_current.json。无当前指针、工具失败、超时或报告缺失均停止依赖步骤，不能改读旧数据库。

完整导出setup、hold、recovery、removal、DSP/ERAM端点、复位入口/级间/功能分发、时钟异常/例外和覆盖对象。分别统计内部/外部、唯一端点/负路径记录。工具按路径选择的最差角不写成已经逐角独立签核。shell_routed无SDF，只证明网表功能。

### 第一轮之后如何分支

| 实际结果 | 下一步 |
|---|---|
| 内部四类检查均无负值，功能保持 | 冻结为内部闭合候选；进入代表层/资源验证，外部和严格门仍未签核 |
| 属性未识别，或目标驱动没有复制/负载未分流 | 标为映射无效；不反复扫描阈值，查真实展开网后提出一个明确替代点 |
| 仍只有MAC CE族失败 | 只研究该实际族；必要时评估核内flag_input_accept分发属性，但触及冻结核必须集中批准 |
| 新增PRE推进族失败 | 重新归因、比较两端点参考与当前候选；原PRE备选是独立诊断，不直接混入本补丁 |
| 主族消失且仅余halo WE | 才考虑一次独立halo局部分发候选；写入条件和可见性不能改变 |
| 出现功能变化、hold/removal退化或新的语义风险 | 不晋升、不叠补丁；回到较优冻结输入，提交具体结构决定 |

建议物理预算仍为主分发最多两次，纯halo残项最多一次；不是预先把三次全部用完。第二次变量由第一轮全量STA决定，不机械地从2端点版本跳去59端点版本。

交付一张比较表：基线/候选hash、总资源、内部四类WNS/违例、外部未决项、目标网实际负载/延迟、64案例/端点周期、严格门状态。单个CE转正不算整体通过。

## 九 第一批并行做的存储与资源核查

这条分支先做只读资料和已有网表统计，不等待时序补丁完成。

1. 从shell_route_ram.rpt及层级资源把halo、权重、DW输出、参数/元数据、诊断壳分开，列容量、读写口、读延迟、冲突和映射方式。先找一份确有收益且端口可满足的缓存，不同时迁移全部数组。
2. 保留视频模板12,358 Slice/8 DSP/40 ERAM的证据范围。与最新计算壳相加仅余875 Slice，与首选参考相加余864；都不是实际合并实现。
3. ROM的14×512×160物理结构可以复用，但当前参数消费者使用schema2字段。旧schema1和schema2虽然同为140,522字节，不能共用字段含义或CRC。
4. DDR的字节地址换算、AW/W时限、写可见性、无RREADY返回和复位晚返五项分别列出匹配IP证据；没有的项写具体缺项，不写笼统“缺数据”。

### ROM包必须做的版本核对

| 项目 | 旧ROM历史包 | 当前字段接入目标 |
|---|---|---|
| manifest | rom/artifacts/manifest.json，schema1 | production/numeric_artifacts/manifest.json，schema2 |
| 每通道量化字段 | output requant | acc→Q7.8 pre |
| 每SiLU层单对字段 | pre-SiLU | SiLU→INT8 post |
| payload SHA256 | c02f7c959a329161dcf7adcf599fc7e97f0a4ef799d83c40708e6c1f570cfd45 | 66284020976ae8a6decd841403a27c09b04ce5bbf4c8c6e3073368d8832abd43 |
| padded CRC32，清单记录 | 60c88426 | 1bbd0dce |

schema2已有56份lane文件和7,168词，无需为同一包重新造生成器。先校验文件hash及字段offset/length/count，再适配真实ROM读参数路径。两个包均为TEST，不是训练权重；旧包CRC通过不证明schema2已通过ROM RTL或厂商初始化。

ROM原427条严格阻断及修复预算已耗尽，新的修复/TD诊断须取得单独授权；此前只做字段、资源和资料核查。DDR原42条严格阻断和integration_release=false也保持。不得把mock中的byte_addr>>1、i_commit_confirmed或固定等N拍当成实际控制器保证。

交付：memory_resource_breakdown.json、package_schema_check.json、paxi_evidence_questions.md；不是本批就宣布ROM/DDR已经放行。

## 十 第二批做哪些真实层

内部时序候选形成后，复用算术核，用薄调度/存储适配扩展当前固定网络形状，不给MAC增加通用端口，不把无参数的down2 runner说成已覆盖67层。

| 顺序 | 固定图层 | 首先验证的风险 | 逻辑4×4满tile任务及组数 |
|---|---|---|---|
| 1 | stem.conv，3→16，3×3/s2 | pixel−128、9×9 halo、padding、Cin尾lane/Cout尾路 | 96任务，每任务4组 |
| 2 | csp2.blocks.0.dw.conv，12通道，3×3/s1 | 3×5并集、尾包、同通道参数复制 | 三点tile模型96任务，每任务2组；当前RTL尚未支持 |
| 3 | csp2.blocks.0.pw.conv，12→12 | 12通道两组、尾输入lane | 64任务，每任务2组 |
| 4 | down4.pw.conv，48→96 | 6组归约、H18底部部分tile | 满tile512任务，每任务6组 |
| 5 | csp4.out.conv，96→96 | 深通道累加/参数和地址 | 满tile512任务，每任务12组 |
| 6 | fuse4_bu.reduce.conv，192→96 | 最大24组、concat视图通道来源 | 满tile512任务，每任务24组 |
| 7 | head2.cls_out与head2.reg_out，48→2/5 | 无SiLU、INT16，两例末组均2路有效；1路尾由Stem覆盖 | 16/32任务，每任务6组 |

每一形状先在Python导出输入/权重/参数/acc/pre/post或raw/目标地址，再接RTL；明确TEST_NOT_QAT。Cin16的down2沿原向量作回归。PW Cin24和其他形状随后按固定图覆盖，不因这张代表表通过就宣布全部形状通过。

这批后立即补两个明确缺口：down3.pw.conv的Cin24→48、3组归约；down4.dw.conv的H18/W32/C48、stride2底部部分tile。前者逻辑全层36,864任务/110,592输入组；后者有效行模型13,824任务/41,472组，满槽模型15,360任务/46,080组。没有完成这些案例时，不写“全部PW组数或DW部分tile已经覆盖”。

空间位置至少覆盖内部、左上、右下、最后部分tile和真实图中的单点尾包。当前冻结图宽度均为4的倍数，每个tile行是3+1；两点尾包仅列为合成边界测试，不冒充冻结图的实际形状。部分tile的跳行或满槽策略在薄适配器中明确、计入周期并对拍；无效物理槽保持0，不能产生逻辑图外的有效写回。

第二批首个性能实验只做DW下一输入组准备与本组执行重叠。先用现trace细分capacity wait，再画当前payload保持/下一组预取/接受边沿逐拍表。不得在ready低时覆盖当前操作数，不新增通用FIFO、更多MAC或归约context。原384拍存储准备是优化目标，不承诺端点省383拍；若等待转移导致总周期不降，就停止该支线。

计时固定为接受start到完整输出提交，预装载、核心、导出分开。互斥统计存储准备、成功发射、容量等待、排空/完成；pre/SiLU/post忙周期只作活动率，不能求和。只在同向量/窗口/功能相同条件下比较端点。预取候选必须重新输出逐拍trace，补充预取请求/填充/有效/tag/消费/取消观察，不再因输出计数相同就复用旧活动轨迹。保留无停顿128个DW任务、384组接受、128个结果及256次标量提交/写回；若DW端点未低于1,095拍、存储等待只是转移而总端点不降，停止该支线。

## 十一 后续里程碑和完成出口

| 里程碑 | 具体执行顺序 | 必须留下的结果 |
|---|---|---|
| M2 存储与代表层 | TEST schema2 ROM读回/真实映射 → 一层参数读取 → 代表tile → 完整单层 | 实际56 ERAM或差异解释、字段逐项一致、层周期/字节/等待；先综合资源筛查，再决定是否布局 |
| M3 固定图 | DW/PW块 → CSP残差 → SPPF三次pool → PAN视图 → 106节点 | conv越界0、pool越界−128、尺度对齐残差signed9/sat8、concat/nearest地址正确；逐节点完整张量一致 |
| M4 真DDR | 语义前置闭合 → ROM取参/DDR读tile/计算/写回/屏障/读回 → 单层/块/全图 | 请求owner、返回容量、取消晚返、写可见性及输入槽释放均有真实模型证据 |
| M5 纯FPGA后处理 | INT16头 → decode → 两类Top128 → 同类NMS → 每类32/共64框 | 与integer golden一致；tie顺序、IoU严格大于0.5、最坏输入周期和资源纳入整网 |
| M6 视频整机 | 官方模板旁路缩放 → 两槽采集 → 图推理 → 完整表CDC → HDMI SOF切表 | 资源/内部与真实接口STA、每帧442,368字节、有效新结果间隔及500ms年龄；随后另行批准板测 |

模型分支独立接续已有训练工作：先冻结完整道路GT和开发基线，再短FP32对照，补完整部署QAT，最后真实模型包与整数/RTL合流。硬件分支不自行启动GPU，也不把随机TEST参数解释成模型精度通过。

在代表层和第一条DDR微循环具备后立即更新20M周期预算，不等到整机末尾。若可实现预算明显超20M，比较唯一H24或提出一个有具体收益依据的核级周转决定；H24不自动减少当前24 MAC的DSP，也不自动解决Slice/控制布线。若只有乐观值低于20M，继续补等待证据，不能宣称达标。

最终5FPS看稳态完整新结果间隔，不看HDMI重复刷新旧框。READY排队、服务时间、结果间隔、源SOF到显示年龄分别记录；500ms预算包含采集、排队、计算、显示及CDC误差，不能只比较READY到result。

## 十二 实施入口和失败处理

### 新runner完成路径验收后使用的阶段顺序

以下是未来执行命令，不是当前可直接运行的已交付脚本。新目录/run.py尚未创建；禁止将路径改成旧目录去“先跑起来”。prepare只能在正确输入绑定完成后执行一次；每阶段失败就停止依赖阶段。

~~~powershell
$roadPython = 'E:/project/qiansai/.tools/road_yolo_venv/Scripts/python.exe'
$roadCandidate = 'E:/project/qiansai/anlogic_topic2_work/lab1_sc500_road_vision/cnn/hw_validation/production/reports/mac_ce_fanout_local_20261010'
if (-not (Test-Path -LiteralPath (Join-Path $roadCandidate 'run.py'))) {
    throw '先完成候选专用入口和路径核查，不运行旧入口'
}
# prepare完成后，实施唯一属性修改。先只生成范围、审阅和门禁报告。
foreach ($roadStage in @('scope','review','gates')) {
    & $roadPython -B -X utf8 (Join-Path $roadCandidate 'run.py') $roadStage
    if ($LASTEXITCODE -ne 0) { throw ('阶段失败，停止：' + $roadStage) }
}
# 到此停止。退出码0不代表gate通过，不自动启动simulate或任何TD步骤。
~~~

读取本次candidate及baseline的gate JSON，确认compile/parse状态、实际新增诊断身份及步骤3的语义阻断清单；源码安全且隔离功能验证范围已获批，才继续simulate → mac_sim → boundary → compare → shell_rtl。gates的退出码不是此判断的替代物。

undriven、physical、collect、shell_routed、finish必须按步骤6分别经过状态判断，不放在无条件连续循环里。历史TD一次约22分钟、路由网表单套回归约4分钟，仅作机时参考，不承诺按这个时间必然修好。先便宜的范围和功能检查，再消耗物理机时。

### 按错误类型最短定位

| 失败类型 | 先取什么最少信息 | 禁止的处理 |
|---|---|---|
| 输入版本不对 | 八文件manifest、ROOT/BASE表、current指针 | 直接复制旧报告或重新冻结错误版本 |
| 功能不一致 | 第一个失败案例/地址/tag及首个不同中间值 | 只比较最终输出、checksum或只打印PASS数量 |
| 周期变化 | 同案例start/done事件和首次状态/握手分歧 | 故障提前退出、换窗口后报加速 |
| 属性无效 | 识别告警、实际驱动/复制/负载 | 连续扫描阈值或加无效wire副本 |
| setup/hold/复位失败 | 全量路径族、实际网延迟/扇出和角点 | 只取最差一条、忽略新端点或新增全局false path |
| ROM参数错误 | schema、字段offset/count、首个错误字节 | 用包长度相同或旧CRC相同代替字段验证 |
| DDR无法发布READY | IP匹配证据和缺失完成/排序事件 | 伪造commit、等固定N拍、超时释放owner |

每次报告固定回答：本轮实际改了哪些文件；仍失败的对象/数量；已证明原因和待证假设；全局到哪个里程碑；下一步具体动作。没有新物理结果时就写尚无新结果，不重复旧数值当新进展。

## 十三 授权与本批结束标准

本轮仅制定步骤并保存文档。下一次实施可集中批准“步骤1至6的P1A独立候选、相关测试/构建文件和隔离TD诊断”，范围内连续完成，不每一步重新询问。主分发的第二次尝试若触及冻结核，须给出实际目标和映射理由后再确认；ROM旧预算耗尽后的新轮修复/诊断、真实DDR协议、数值/II/接口/复位改变仍分别决定。

第一批结束时应有四份实际成果：修正后的逐层任务预算；单变量候选及完整物理比较；存储/参数包/DDR缺项清单；一份明确进入下一里程碑或停止该物理支线的结论。只完成计划、只过仿真或只修两条CE都不算该批实际完成。

本批不改生产、不训练、不生成部署位流、不上板、不写Flash、不改变严格检查或时序例外。原失败证据和旧全局计划保留。

## 证据入口

- [两端点参考源码修改位置](E:/project/qiansai/anlogic_topic2_work/lab1_sc500_road_vision/cnn/hw_validation/production/reports/control_operand_hold_20261009/rtl/down2_dynamic_tile_runner.v:165)
- [两端点实际失败路径](E:/project/qiansai/anlogic_topic2_work/lab1_sc500_road_vision/cnn/hw_validation/production/reports/control_operand_hold_20261009/physical/coverage_100000_violations.timing:1059)
- [真实TD构建函数](E:/project/qiansai/anlogic_topic2_work/lab1_sc500_road_vision/cnn/hw_validation/production/reports/dw_task_overlap_20261009/run.py:116)
- [工作目录及工程模板助手](E:/project/qiansai/anlogic_topic2_work/lab1_sc500_road_vision/cnn/hw_validation/production/reports/runtime_layer_integration_20261009/run_candidate.py:31)
- [旧compare与collect入口](E:/project/qiansai/anlogic_topic2_work/lab1_sc500_road_vision/cnn/hw_validation/production/reports/dw_weight_load_timing_20261009/run.py:40)
- [旧硬编码finish状态](E:/project/qiansai/anlogic_topic2_work/lab1_sc500_road_vision/cnn/hw_validation/production/reports/control_operand_hold_20261009/run.py:162)
- [旧整行DW预算公式](E:/project/qiansai/anlogic_topic2_work/lab1_sc500_road_vision/cnn/hw_validation/production/reports/mac_task_stream_20261009/budget.py:49)
- [固定图](E:/project/qiansai/anlogic_topic2_work/lab1_sc500_road_vision/cnn/hw_validation/production/graph_artifacts/graph.json)
- [布局字节计算](E:/project/qiansai/anlogic_topic2_work/lab1_sc500_road_vision/cnn/hw_validation/production/graph.py:99)
- [schema2数值契约](E:/project/qiansai/anlogic_topic2_work/lab1_sc500_road_vision/cnn/hw_validation/production/deployment_contract.json:45)
- [schema2已有TEST包清单](E:/project/qiansai/anlogic_topic2_work/lab1_sc500_road_vision/cnn/hw_validation/production/numeric_artifacts/manifest.json)
- [schema2包生成器及字段定义](E:/project/qiansai/anlogic_topic2_work/lab1_sc500_road_vision/cnn/hw_validation/production/numeric_package.py:43)
- [旧schema1包清单](E:/project/qiansai/anlogic_topic2_work/lab1_sc500_road_vision/cnn/hw_validation/rom/artifacts/manifest.json)
- [ROM原门禁与禁止TD记录](E:/project/qiansai/anlogic_topic2_work/lab1_sc500_road_vision/cnn/hw_validation/rom/report.md)
- [DDR真实未决项及门禁](E:/project/qiansai/anlogic_topic2_work/lab1_sc500_road_vision/cnn/hw_validation/ddr/reports/H1B_VALIDATION_RECEIPT.json)
- [批准的整体技术框架](E:/project/qiansai/anlogic_topic2_work/lab1_sc500_road_vision/cnn/hw_validation/plans/competition_framework_20261008/RoadYOLO_训练与RTL整体技术框架.md)

## 简要总结

先把输入版本、构建入口、任务口径和参数字段固定正确，然后只做一个MAC CE物理实验；结果决定是否需要第二变量。紧接着验证代表层和真实存储，不围绕一个验证壳无限微调。第一批优先取得能改变整体决策的四份证据，不新增与当前固定网络无关的硬件功能。
