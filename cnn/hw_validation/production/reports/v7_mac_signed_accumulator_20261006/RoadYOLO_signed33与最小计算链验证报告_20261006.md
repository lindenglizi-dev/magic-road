# RoadYOLO signed33 累加与最小计算链验证报告

## 当前未通过或未完成事项

MAC 候选的数值与协议回归、源码严格检查已通过。测试台专用静态门通过，但完整八门未通过：初次检查保留了 171 条诊断，包含真实的文件头、display、begin/end、命名、注释和 profile 问题，也有 formatter AST 解析限制；显式空端口的隔离 A/B 尝试未消除失败。不能将 MAC 源码的零错误扩展为全部交付物通过。最小计算链数值与实际缓存写读已通过；其首轮源码严格门有 374 条错误，包含注释对齐、宽度、状态逻辑依赖锥、时序赋值结构及模板问题，不将这些记录一概归为误报。新链布局布线被 414 位并行测试 I/O 超出器件 160 个用户 I/O 的问题阻塞。尚无新链时序或整网 5 FPS 的通过结论。

本阶段只修改独立候选，不覆盖旧核，不改部署契约、MAC 外部接口或接收间隔，也不训练、不写 Flash、不上板。

## 最大合法长度与范围证明

冻结的 67 层图按每层卷积核形状、输入通道和 groups 计算归约长度，并核对权重数量及 MAC 数。全部图生成源文件的哈希与现有文件一致。最大合法长度为 192 个有效 INT8 乘积，即最多 24 个八通道组，出现在 `fuse4_bu.reduce.conv` 的 192 输入通道 1×1 卷积。图合计 214,465,536 MAC。

signed INT8 乘积最小值为 −16,256，最大值为 16,384。偏置允许覆盖完整 signed INT32 范围，且只在 first 组加入一次。对每个前缀长度 n＝0…192，部分和下界为 −2³¹−16,256n，上界为 2³¹−1＋16,384n。所有前缀统一落在：

```text
−2,150,604,800 ≤ 部分和 ≤ 2,150,629,375
signed33 范围：−4,294,967,296 … 4,294,967,295
```

因此所有合法中间部分和都能放入 signed33。这不是对无限长非法输入组流的保证；调度方必须遵守同一归约最多 24 组、192 个有效乘积的冻结图约束。没有增加长度端口，也没有宣称完成整网调度验证。

证明脚本与机器结果：[prove_accumulator_range.py](coordinator/prove_accumulator_range.py)、[range_proof.json](coordinator/range_proof.json)。

## 候选数据通路

| 环节 | 每路位宽 | 处理方式 |
|---|---:|---|
| 外部激活和权重 | signed8 | 原 24 路乘法与 mask 不变 |
| 外部偏置 | signed32 | first 时三路分别符号扩展至 33 位 |
| 跨组 accumulator | signed33 | 三路合计 99 位，保留 bit32 |
| base product pair quad dot | signed33 | 四级均为 99 位，无提前截断 |
| 点积操作数 | signed33 | signed19 点积符号扩展 |
| 加法及 candidate hold final | signed34 | 两个 signed33 操作数形成完整 signed34 和 |
| publish 写回中继 | signed33 | 三路分别取 candidate 的 33 位，合计 99 位 |
| 对外最终结果 | signed32 | 仅 last 组检查 INT32；正常后分别窄化 |

非末组允许暂时越过 INT32 边界，不发布结果或故障。末组三路任一路最终越界，三路对外结果全部清零，且三路历史累加均不提交。正常末组仍保留旧核的成功提交语义。ready、first/last、输出保持及异步复位取消的控制赋值保持原样。

源码检查入口：[audit_candidate.py](coordinator/audit_candidate.py)，结果：[source_audit.json](coordinator/source_audit.json)。这是位宽与接线审计，不替代 RTL 仿真或物理实现。

## 已执行验证

原 1031 项冻结 MAC 回归通过，错误数为 0。最小链原基础 16 通道与尾组 13 通道的旧测试各 8 组，也均通过。原向量及旧核未覆盖。

新增定向参考和 RTL 测试含 12 个用例、84 个输入组，覆盖三路正负暂时越过 INT32 后恢复、每路正负最终溢出、192 项极值归约、最大正负范围端点、非零无效 lane 的 mask、续组不同 bias、不重复加入 bias、忙时保持下一请求、短长输出反压、预先 ready 以及 10 个阶段复位取消点。

Icarus 与 ModelSim 均通过；主任务又独立编译并复跑 Icarus，结果为 0 错误。独立周期收据匹配全部 84 次接收、12 个终态，其中 8 个最终故障均为三路原子清零并禁止提交。

| 周期事件 | 实测周期 |
|---|---:|
| last 输入接收到终态有效 | 9 |
| 非末组到下一组接收 | 11 |
| 末组施加 3 拍反压后到下一次接收 | 16 |
| 末组施加 12 拍反压后到下一次接收 | 25 |

这里的 16、25 拍包含该测试台的消费和释放安排，不能称为优化后的通用 II。没有改变 MAC 性能控制。

参考与测试：[signed33_reference.py](verification/signed33_reference.py)、[tb_road_mac_signed_accumulator.v](verification/tb_road_mac_signed_accumulator.v)。主任务独立收据：[independent_receipt.json](coordinator/independent_receipt.json)、[independent_trace.csv](coordinator/independent_trace.csv)、[check_trace.py](coordinator/check_trace.py)。

旧核对正负恢复序列第一组提前报错的行为也保留为反证，不能把旧行为复现通过解释为新部署契约正确。

## 严格检查与历史失败

候选源码最终严格检查为 0 错误、0 strict warning，`delivery_ready=true`：[strict_candidate_pass.json](candidate/strict_candidate_pass.json)。范围仅为 MAC 源码及其绑定规范，不包含新测试台、SiLU、整个计算链或物理签核。该源码检查的 compile、ast、readability、comment、naming、profile 为 passed；testbench 和 toolchain 在该调用中为 not_requested，不能写成八门全部通过。实际 Icarus、ModelSim 编译与运行证据另列。

首份三条 VG122 诊断与中间注释对齐失败均保留。首个失败版本另有精确重建并匹配 SHA256 的源码快照，重建性质已在候选报告注明。VG122 的修复是将加法明确为 signed33＋signed33→signed34，而不是删除规则或仅修改溢出判断；没有新增流水级。测试台的最终验证状态为 `FUNCTIONAL_PASS_TESTBENCH_STRICT_FAIL`，`release_claim=false`：[verification_results.json](verification/verification_results.json)、[verification_report.md](verification/verification_report.md)。这与 ModelSim 的编译及功能通过是不同结论。

必要依赖检查 `required_ok=true`，WaveDrom 3.6.1 可用；推荐的 context-engineering 组件缺失，导致依赖汇总返回非零，不能写成全部可选依赖通过。独立 Python 审计只运行实际脚本，不冒称未安装的专用 Python 技能门禁通过。

## 源码与契约不变性

| 对象 | SHA256 |
|---|---|
| 旧 MAC 原文件与冻结快照 | `5df97da6910c5673f35807207cc06260fc6ed6edc7d9313aa2fac9ec7b3016be` |
| signed33 候选 | `f8bf6cace6eb99bd9b915be5e27e1d38af4b3a2485ffeb6e87675d8bfc3478e8` |
| 未修改的部署契约 | `5cff8d5a406dc235a0d5d35cbf72903c0d6b48477e99a0cabf58251331f3a681` |

候选代码：[road_mac_probe.v](candidate/road_mac_probe.v)。旧核继续位于 `cnn/hw_validation/mac/road_mac_probe.v`，没有替换。

## 最小计算链推进边界

新链目录为 `../v7_onchip_chain_20261006/`。采用单上下文串行适配，连接 MAC 最终三路 INT32、实际重定标乘法、既有最近偶数舍入核、冻结真实 SiLU 表、输出重定标与 INT8 缓存写读。位置及通道身份由外层保持，SiLU 不增加虚构 tag 端口。

本版只使用冻结测试系数：pre M＝1、3、5，post M＝1，以及对应移位参数。给新 top 增加运行时系数端口的尝试因扩大接口范围被安全审查拒绝，未实施；既有核接口不变。固定系数可能被 TD 综合为移位或加法，所以该链的资源结果不能代表任意合法 31 位部署 M 的乘法器预算。通用系数硬件的资源验证仍需另行确定接口与授权。

基础用例为 2×2、16 输入通道、3 输出通道，共 192 有效 MAC 和 12 输出；另有 13 通道尾组，共 156 有效 MAC。真实训练量化参数尚未冻结，测试参数不支持准确率声明。

最终 ModelSim 官方 PH1P 模型对拍已匹配 MAC、pre 乘积及 round、真实 SiLU、post 乘积及 round 和最终 INT8。两案各 12 项缓存输出，加一组 3 项定向边界输出，共 27 项，全部通过真实写口和读口匹配。三路数值齐备后分三拍写实体缓存，前两拍不公开有效位，末拍才同时发布该位置三项；已观察 18 次前两拍隐藏状态。最终日志为 `TB_PASS_CHAIN mac=9 pre=27 silu=27 post=27 read=27 atomic_hidden=18 reset=6 directed=1 errors=0`。

主任务另用 [check_chain_trace.py](coordinator/check_chain_trace.py) 独立比较最终 CSV 与冻结黄金文件，27 个实际缓存读响应、81 个 pre／SiLU／post 事件及 9 个 MAC 终态均一致：[chain_trace_receipt.json](coordinator/chain_trace_receipt.json)。此项为独立数值日志审计，不冒称第二次独立 RTL 运行。

最小链源码：[road_onchip_chain.v](../v7_onchip_chain_20261006/road_onchip_chain.v)。完整功能报告：[validation_report.md](../v7_onchip_chain_20261006/validation_report.md)，机器收据：[validation_receipt.json](../v7_onchip_chain_20261006/validation_receipt.json)，可复跑命令：[verification_commands.md](../v7_onchip_chain_20261006/verification_commands.md)。主任务已核对 [final_manifest.json](../v7_onchip_chain_20261006/final_manifest.json) 的 30 项哈希全部一致；本节结论绑定该冻结版本。

新增边界用例偏置为 100000、−100000、8，零乘积：前级分别饱和至 32767、−32768，第三路最近偶数舍入将 2.5 舍入为 2；真实 SiLU 后的最终读回为 127、0、0，验证正端 INT8 饱和。固定 SiLU 与 post 比例下无法构造最终 −128 饱和，故不宣称该链覆盖最终 INT8 负端饱和。

复位取消覆盖 MAC 在途、pre round 等待、SiLU 等待、post round 等待及两处提交中途，共六个计算阶段；另有缓存读响应保持时复位取消。检查核有效位、身份、缓存提交位和 table_loaded 清零，以及复位后无幽灵结果。MAC 故障后的三个缓存地址均读到零和 fault。功能用例有明确 PASS 标记；失败日志与历史版本均保留。

源码严格报告：[strict_gate.json](../v7_onchip_chain_20261006/strict_gate.json)。其中 131 条为 VG060 注释对齐，2 条 VG122 涉及位置／通道计数递增，7 条 VG145 为组合依赖锥限制；另有时序结构、声明、注释及模板问题。此状态为功能候选通过、严格交付未通过，不使用编译通过代替八门通过。

基础 16 通道用例从首个输入握手至最后一个缓存读响应被消费为 482 个周期；13 通道尾组含读回 3／20 拍反压为 503 个周期。1024 项表的预装载在起点之前，不计入上述周期。这是串行测试链的真实墙钟时间，不是整网帧率。

运行保留两条官方加密 ERAM 模型的 `vopt-2697` 警告：`INIT_FILE` 位选 MSB 172095、LSB 172024 越界，原日志指向模型第 165 行。运行无错误，但不能写成无警告。数值用例先通过协议写入完整 1024 项真实表，不依赖该初始化路径；这不证明 bitstream 初始化正确。

物理预检确认 top 共 24 个端口声明，展开为 398 位输入和 16 位输出，共 414 位；即使封装全部 324 球均作为用户 I/O 也不够。同器件既有 TD 原报告 `v6_silu_stage_20261006/physical/td/probe_route.area` 第 2 行绑定 PH1P35MDG324，第 5 行为 `#IO 45 out of 160`，SHA256 为 `59c907d9992bad9ad2b1345fa07fbe940667cc9c7ce58ec6bfbd91dc7d10f24e`。

完整布局布线需要独立低 I/O 物理壳；这会改变物理工程的外部接口，虽然三个内部核接口可以不变。本阶段未创建该壳、未修改接口、未运行 place／route 或 bitgen。无壳时最多只能做独立综合及 I/O 数量预检，不能给出真实布局布线资源或时序通过结论。探针若获准，含探针资源必须单列，不把自动管脚分配解释为板级可用。

本阶段保持 II＝11。按 24 路满有效、100 MHz 及冻结全网 MAC 数计算，纯 MAC 的理想上限约 1.017 FPS，尚不能达到 5 FPS；这只是当前结构的上界估算，不是整网实测速度。II 优化不与本次 signed33 契约修复同时实施。
