# schema2 ROM 验证结果与下一步

2026年10月10日。本轮目标是确认140,522字节参数测试包能否按160位布局装入56块ERAM，并取得真实读回、资源和100MHz时序证据。结论：**内容、56块映射和内部数据时序取得正向证据；外部复位、时钟分类诊断及严格交付门禁仍未闭合。** 不是完整CNN通过。

## 未通过项先看这里

| 项目 | 本轮具体结果 | 原因和后续处理 |
|---|---|---|
| 外部复位 removal | 1,000个负裕量端点，最差−1.196ns | 全部起于顶层`i_rstn`，到异步复位脚；裸入口直接驱动复位分发。最终接入既定的异步断言、同步释放边界后重新测量，不改输入延迟或加false path。当前没有修改复位合同。 |
| 时钟分类诊断 | `check_timing`仍报definition(1) | 连续综合及恢复数据库均复现。XML标为单一primary 100MHz，默认查询返回1个10ns时钟；`-include_generated_clocks`查询却返回0。分类矛盾保留，不能宣布时钟检查全面通过。 |
| 严格门禁 | DUT441 errors / 0 warnings；两份TB462 / 3 | DUT与同范围基线完全相同；存在格式、注释及保守驱动分析等未闭合项。动态验证与TD诊断不替代严格交付。 |
| 完整综合网表控制链回归 | 未完成，已主动取消慢速尝试 | 串行CRC要运行约236万拍，7千余寄存器的门级仿真成本过高。替代证据只覆盖真实物理ERAM全地址内容，不冒称完整控制链门级通过。 |
| 部署参数消费者、整网及精度 | 未完成 | 当前是TEST包；没有QAT权重、参数缓存至计算链闭环、完整DDR调度或整网5FPS证据。 |

以上1,000项是复位端点，不是1,000个不同功能错误；但外部复位失败仍是真实未签核状态。内部hold最小仅+0.024ns，后续联合布局必须重测，不能把当前局部正裕量继承为整机通过。

## 本轮实际完成

| 检查 | 结果与证据 |
|---|---|
| schema2文件布局 | 14组×4 lane×512词；有效140,522B，物理143,360B，padding2,838B。全部lane重构一致。见[包核查](package_check.json)。 |
| 厂商模型整链RTL读回 | 7,168个160位词、143,360字节及393字段逐项一致；CRC32=`1bbd0dce`；扫描中复位后从头重启通过。见[仿真收据](vendor_simulation/receipt.json)。 |
| TD真实物理ERAM读回 | 从真实综合网表提取56个`PH1P_PHY_ERAM_V2`，保留全部初始化参数和数据位拼接，核对每块512地址。143,360字节一致，仿真执行约4秒。见[读回收据](mapped_readback/receipt.json)、[提取绑定](mapped_readback/extraction.json)。 |
| 布线后初始化保留 | 56块×80个INIT/INITP，共4,480组参数，在原综合网表、连续流程综合网表、布线网表之间完全一致。见[result.json](result.json)。这是参数保持核查，不是SDF或上板验证。 |
| SYN-5025归因 | 置零优化前，probe仅22根`state_next_b/state_next_b1`临时网，全部PIN_COUNT=0、DRIVER_COUNT=0；group定义为0。综合网表查询无无驱动网。见[置零前收据](prezero_query/receipt.json)。查询不替代所有物理模式脚证明。 |
| 源码保留 | 两份DUT与旧ROM字节一致；629个冻结依赖未变。见[范围核查](scope_check.json)、[冻结核查](frozen_check.json)。 |

真实逻辑40位ROM映射成物理DP20K时使用A/B数据及额外位共同形成40位输出，因此不能把物理B口读路径当作多余连接直接剪掉。本轮物理读回保留了TD原样连接及参数。

## 实际资源和时序

器件PH1P35MDG324，速度等级−3，TD6.2.168116，100MHz。最终取[连续综合到布线流程](continuous_physical/build.tcl)，不是0%覆盖率的首次无效报告。

| 资源 | 实测 |
|---|---:|
| ERAM20K | 56 / 108 |
| DSP | 0 / 40 |
| Slice | 3,799 / 21,216 |
| 寄存器 | 7,130 |
| LUT6 | 1,348 |
| 顶层I/O | 35＝时钟1＋复位1＋done1＋checksum32 |

这是**完整CRC验证探针**的资源，包含14组拼接寄存器、选择流水和CRC扫描控制；不是最终参数读取器的资源。不能与独立计算壳资源简单相加，称为整机资源。

| 路径范围 | setup / recovery最差 | hold / removal最差 | 负端点 |
|---|---:|---:|---:|
| 内部寄存器到寄存器 | +3.253ns | +0.024ns | 0 / 0 |
| ERAM读数据到寄存器 | +6.458ns | +0.559ns | 0 / 0 |
| 寄存器到ERAM地址 | +6.172ns | +0.025ns | 0 / 0 |
| 寄存器到诊断输出 | +1.232ns | +2.506ns | 0 / 0 |
| 外部复位入口 | recovery +2.981ns | removal −1.196ns | 0 / 1,000 |

内部最差setup：`state_current_reg[0]_syn_3.clk → cnt_word_addr_reg[2]_syn_13.ima`，slow_m40c；数据延迟6.488ns，其中布线4.928ns。内部最差hold：mu组upper_pair至word_data，fast_m40c。各类完整起终点和角点见[result.json](result.json)。

TD报告coverage=100%，Slow/Fast的Max/Min均启用；无缺时钟、无无效约束、无组合环、无缺输入/输出延迟。但这不消除上表复位失败，也不消除时钟分类警告。[原始时序](continuous_physical/final_timing.rpt)、[覆盖报告](continuous_physical/coverage_100000_all_paths.timing)、[检查报告](continuous_physical/check_timing_verbose.rpt)、[时钟XML](continuous_physical/clock_summary_debug.rpt)。

输出零延迟及自动引脚仅用于隔离诊断，不能据此上板或签核真实外设。`report_route_status -drc -file`本版本未生成独立文件，实际DRC结果保存在[TD日志](continuous_physical/td.log)，不得引用不存在的文件。

## 修复了什么和保留了哪些失败

1. 测试平台旧`forever`时钟被检查器误判成`for`循环。只改成等效`always #5`，解析错误降至0；没改DUT。
2. 首次综合工程名与文件名不一致，随后修正构建器，仅替换顶层LABEL/MODULE。
3. 第二次综合找不到初始化文件：ModelSim按工作目录解析，TD按RTL目录解析。新增同哈希`rtl/artifacts`副本，不改RTL中的参数路径。
4. 首次物理尝试重复加载数据库已携带的SDC，导致时钟被删除、coverage=0%。该报告无效，完整保留。恢复流程不重复加载后为100%；另外执行连续综合→布局布线复核，资源与关键裕量相同。
5. 完整门级CRC扫描因成本取消；准确PID/父子关系核对后只停止本轮ModelSim进程。改用真实物理ERAM全地址读回，保留取消记录及未完成状态。

原427项失败报告未删除；本轮同范围baseline/candidate均441项，差异来自当前检查闭包，不是“修成了441个硬件错误”。TB351项是单个整链测试范围；最终462项是新增物理读回TB后的两文件范围，不能直接作为同一对象恶化比较。[语义归因](semantic_review/ROM风险与门禁归因.md)。

厂商模型警告也未屏蔽：RTL仿真112项为模型`INIT_FILE`位选范围警告；物理ERAM仿真1,344项主要为TD输出网表省略未用模式/探针端口的连接警告。全量读回只支持当前固定只读配置，不推广成所有模式安全。

## 八项门禁与工具边界

| 范围 | compile | ast | readability | comment | naming | profile | testbench | toolchain |
|---|---|---|---|---|---|---|---|---|
| 两份DUT严格门禁 | passed | failed | failed | failed | failed | passed | not_requested | not_requested |

门禁JSON中的`toolchain=not_requested`没有自动改成通过；本轮真实ModelSim和TD独立证据另列于上文。两份TB本地compile/parse通过，但总体严格交付仍失败。Python/Tcl辅助技能不在当前可用目录中，不宣称其严格门禁通过；使用既有工具助手、限定输出目录和可运行断言收集证据。

测试规范和WaveDrom已通过`workflow.write-spec`生成，见[测试规格目录](spec_current/spec/tests/tb_road_yolo_numeric_rom_probe_spec.md)。本报告沿项目本地Markdown格式保存，没有创建云端文档。

## 下一步及需要决定的边界

主线从“包能否存入和读出”转到“参数是否正确送给真实DW/PW计算”，不要继续扩展CRC探针。

1. 复用这56块ROM和现有动态计算链，先完成固定`down2.dw.conv/down2.pw.conv`的活动组参数预取；权重、偏置、pre/post参数与manifest同源。只缓存当前输出组，不复制整套参数RAM。
2. 与同一批4×4向量逐项比较：参数字段、通道编号、MAC输入、中间重定标及最终输出。覆盖跨20字节词边界、层尾、停顿、复位取消及错误禁止发布。
3. ROM接入既有同步释放域后，重做联合顶层资源与时序；保留时钟分类问题和原始复位失败，不用单独探针资源替代联合结果。
4. 再推进固定67层调度和DDR闭环。真实QAT参数未就绪时仍明确TEST；不以ROM扫描速度或小块周期宣称5FPS。

若接入必须改内部核端口、II、数值或复位合同，或需要新增时序例外/真实DDR协议选择，停止该分支并集中提交具体决定。本轮没有训练、修改生产、生成位流、上板或写Flash。

简要总结：56块ROM容量布局得到实测支持，内容、初始化保持和内部数据路径已取证；完整系统仍有明确缺口。下一项最有价值的工作是参数消费者闭环，不是继续优化诊断CRC速度。
