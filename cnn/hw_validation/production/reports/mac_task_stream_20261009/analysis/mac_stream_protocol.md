# 跨任务 MAC 最小协议审查

2026-10-09，arch_lead，只读 RTL 分析；未写 RTL、未运行综合/实现。按 readable-verilog-generator 的 analyze 路由和 Ponytail 最小改动原则，结论限独立候选。

## 结论

保留原 8×3 乘法、A0–A5 算术及顺序归约，只把 last 锁定换成 first 预留 credit，把 A6 单保持结果换成固定四项、每项 97 位的结果环，是可行的有界候选。每项为三路 INT32 加一个原子 fault。无需复制乘法器、无需多上下文累加器。PW 两组任务可以在上一 last 后下一拍投递 first；四项是原流水延迟下、输出随时接收、允许同拍 pop 复用 credit 时，连续 first-first 2 拍的最小容量。四项不保证任意单组任务 sustained II=1，也不保证后处理堵塞时无停顿。

只要 first 预留覆盖所有在途结果，四项对任意长输出停顿都安全：停发新任务，已开始任务继续完成。错误是用“已完成 FIFO 未满”代替“未释放预约未满”。

## 源证据

基准来自 production/reports 下：

| 源 | SHA256 |
|---|---|
| retirement_lane_banks_20261009/rtl/road_mac_probe.v | 89a6896fd5b85dbee08ac07fffc97864c9acb4e06444fa38f0123c64e2a7e449 |
| retirement_lane_banks_20261009/rtl/road_dynamic_postprocess.v | de8deeb625b80c96bae0757a831d4eb9f4be3b2a7174265079aca1a4f15439e9 |
| pw_turnover_20261009/rtl/down2_dynamic_tile_runner.v | 22f37a633c85d7140a5600e0aa33b167b26ba05171c8b781fe3e24c7ac5ca7c7 |

以上本次读取哈希均与 pw_turnover physical/input_manifest.json 一致。该 manifest 使用 runtime_layer_integration_20261009/rtl/road_down2_dynamic_adapter.v；不要误用 retirement_lane_banks 目录中的固定参数 adapter，它不具备当前 runner 连接的动态参数端口。

## 周期与容量

定义上升沿 t 为输入握手进入 A0；该组在 t+1 进入乘积、t+2 对和、t+3 四项和、t+4 点积、t+5 累加并产生安全终态、t+6 写结果 FIFO，最早 t+7 输出握手。不存在组合空队列直通。

L 组任务的 first 在 0，last 在 L−1，最早 pop 在 L+6。连续任务首组间隔 L 时，无泡预约下界为 ceil((L+6)/L)，前提为同拍 pop 释放 credit 可被新 first 使用。故 L=1 为 7，L=2 为 4，L=3 为 3。若禁止同拍复用，当整除时要多一槽才能维持同速；四槽 L=2 会在 first=8 的边沿停一拍，安全性不受影响。

两组任务例：A first/last=0/1，B=2/3，C=4/5，D=6/7；A 在7写FIFO、8消费；E 可在8接受 first。四预约包含活动归约、末组之后的流水和已完成FIFO，不是四项完成结果外再允许四个在途任务。

后处理既有两项 ingress 和八项 retirement。其三lane串行吞吐不是每两拍一组三lane；持续流最终反压是正常结果。MAC四项只隐藏流水周转并吸收有限停顿，不应扩容到无限缓存来掩盖平均速率差。未释放 PW 描述符至多四项；MAC与PP整体最多十二个未完全退休的批次（四个MAC预约加八个PP退休槽），PP ingress 是后八个的子集，不能再次相加。

## 预约、归约、结果守恒

- first_accept = input_valid && input_ready && first；result_pop = result_valid && result_ready。reset 外 reserved_next = reserved + first_accept − result_pop，0≤reserved≤4。
- active 表示已经接受 first 而未接受 last 的唯一输入归约。active 时续组不依赖剩余 credit；否则新 first 需要 reserved<4 或同拍 result_pop。first=last 单组直接占预约但不保留 active。
- completed_count_next = completed_count + final_push − result_pop，0≤completed_count≤reserved≤4。reserved−completed_count 包含活动归约和全部未入结果FIFO的已开始任务。三个计数不能用裸 valid 推进。
- final_push 对应每个已接受任务恰好一次 last 的 t+6 事件。此前已有预约，所以即使下游永久不收，也有空间。满 FIFO 时不能再有合法无预约 final_push；把这种情况列成断言错误。
- FIFO 使用独立读写指针；同拍 pop/push 数量不变，两指针各推进；同拍 first/pop 预约数量不变。输出 valid 且未ready时，队头data/fault和指针保持。不要在背压期间以新完成值覆盖队头。
- 三路共用同一预约和fault；不得拆成不同有效周期。输入必须是非交织、完整 first…last，每任务≤24组、每路≤192有效乘积。只接受规范流，不把本候选扩成错误格式自愈引擎；独立检查器覆盖违约输入。

## first、fault 和复位

first 位与对应 bias 沿现有 A0–A4 一起前进，A5 使用该组携带的 bias 替代旧 accumulator。新任务 first 不能用当前外部 bias 或 runner 当前计数器重读。上一 last 的 A5 终态和下一 first 的 A5 累加出现在相邻边沿，顺序固定；单累加器即可隔离。first=last 仍只加一次bias。

MAC末组任一候选超过INT32时，该任务输出三路零和fault=1；该末组不更新历史累加器。其后的合法first使用自己bias，不受前一fault污染；MAC本身不把fault升级为全局sticky，也不能吞掉后继已接受任务的结果。

runner保留已有整tile失败、只能外部reset恢复的语义：消费fault后停止发新组，清tile有效、禁止export及成功done。后继已经接受的工作属于失败tile，不得成为后续tile结果。最小实现是保留其预约/描述符和残留流水，停在FAULT直到共享外部reset；称为“逻辑放弃，reset物理取消”，不能声称立即清掉所有MAC任务。后继可能只接受first尚未last，因此不能仅靠继续pop排空，也不能单独清runner队列而让MAC保留旧结果。

同拍fault消费和新输入握手必须明确处理：允许该输入也计入失败tile并在reset取消，或者组合阻止该拍新发射。两种都必须有断言和占用记账；不可软件式假定先fault再发射。此前已经写入私有tile cache的数据允许残留，但tile_valid永远为0，不能导出。

复位异步断言取消全部预约、FIFO valid、流水valid、描述符及tile资格；释放沿既有系统规则，SiLU重新装表。无需为任务fault新增局部软reset。原MAC复位ready默认1属于既有端口可观察行为，候选若更改为复位ready0需显式列入接口差异，不能隐藏在credit改造中。

## PW 元数据与参数对齐

固定四项描述符保存 position[3:0] 和 output-group[2:0]（或channel-base[4:0]），仅在实际first_accept入队。发射游标可在last后前进，但结果侧完全改用描述符队头。正常结果的result_pop、descriptor_pop、PP input_accept必须同一事件。fault允许独立fault_pop：MAC与描述符同时消费、不给PP输入、runner当拍作废tile；不得只弹出其中一侧。PP正常入口当拍同时采样三路数据、lane mask、三路tag、pre参数、post参数和mode。

本固定PW24输出每组mask=111、channel_base=group×3，层标志可在PW阶段固定，不必扩大描述符。参数从冻结cache按队头channel取；整段未排空前禁止模型参数重装、层标志切换、位置/通道cache所有权复用。当前调度参数若仅依赖cnt_output，会把A数据配成正在发射的D参数和tag，这是首要风险。

因为PP自己在accept时复制参数和tag，描述符到该拍即可释放，不必等三个lane完全写回。四项描述符count应始终等于MAC reserved；如果不同则停机报告，不能继续用猜测tag。DW本轮仍串行，可保留其triplet暂存与空间拆分；切换DW→PW前确保DW写回屏障、MAC无预约和PP无旧任务，禁止跨阶段混用四项PW队列。

PW最后一次last只代表发射完成；必须等待MAC预约=0、描述符=0、后处理排空且384个PW元素实际写回，再允许tile完成。不能用最后一个发射游标直接进入成功态。

## 必测反例

1. 连续单组和两组任务，bias各不相同；最后一组A与firstB相邻；核对每次A5中间和与所有结果顺序。
2. 第四次first占满预约时仍有续组，ready不得关闭该续组；永久result_ready=0时最多接受四个first，全部末组最终无覆盖入FIFO。
3. 满队列同拍pop/push、满预约同拍first/pop，以及指针绕回；计数不加两次、不漏减。
4. A fault、B正常、C极值bias，MAC级仍返回A零/fault、B和C正确；runner级收到A后不导出tile，B未last也能在外部reset后清空。
5. 队头背压期间继续完成后继，data/fault/tag/参数稳定；输出ready反复切换时无重复和遗漏。
6. 发射跨position末尾、channel-group7→0时，先前结果使用旧描述符；PP停顿超过MAC四项容量，解除后顺序无误。
7. 在first、last、final_push、pop和fault边沿分别reset；无旧valid泄露，新表装载后首个任务从新bias开始。
8. PP故障pending先封输入但o_fault尚未抬起时，MAC有限缓冲正确反压，无覆写；runner最终进入故障且不发布tile。

以上是静态协议检查和待执行反例，尚非仿真PASS。八门状态本次均为 not_run：compile、ast、readability、comment、naming、profile、testbench、toolchain；不覆盖或改写历史门禁结果。

## 授权边界

已批准的独立跨任务周转研究足以实现和验证上述候选：端口位宽、8×3资源、数值、任务内II1、整tile故障封闭和外部reset恢复保持原意。无需就每个四项寄存器或描述符另求授权。若要继续使用fault后的后继任务、错误后无reset恢复、局部软reset、改变复位ready行为、任务交织、多累加上下文或整机集成，均是额外可观察契约，应先明确决定。本审查没有授权生产接入或实际部署。

## 最终候选只读复核（2026-10-09）

本次复核的修正前候选MAC哈希 `9a26e4edbcbdd9e56c50fcfc35d2a28e4fd8a8749eb19599fa3b787587be404f`、runner哈希 `c275fb0ef210b7abae4bed99fa9b7147fc8188854a12757e2bf0453d8a2b70d2`。MAC从“A0只锁存真实握手负载”起至endmodule与冻结源逐字相同。仅审查信用/元数据/故障/复位/阶段切换，不评判物理实现。以下发现的reset-ready差异要求修正，因此此MAC哈希不能作为最终交付版本。

这次限定语义审查未发现新增功能阻断缺陷。具体核对如下：

- MAC reserved和PW meta均由真实first/pop同拍加减，满时允许pop释放槽供新first复用；已开始归约不被满credit截断。满meta环的同地址读写在时钟沿前向PP提供旧队头，非阻塞赋值沿后写新描述符；读写指针同时推进，仍保持顺序。
- 当前fault使用独立fault_pop，不送PP。队头fault同时封锁输入发射、消费故障结果和元数据、禁止runner该拍写回，进入sticky FAULT。已接受后继的半任务和预约保留，直到共享外部reset清空；没有假称这些半任务自行排空。PP可能在同一边沿内部消费一个更早的正常结果，但runner不提交它且整tile不可导出，符合失败tile放弃规则。
- PW结果position/channel和pre参数索引均取描述符队头，不再取正在前进的issuer计数。背压时队头读指针不动，参数cache在非IDLE禁止改写；同时pop/first不覆盖沿前所采样的旧参数。
- DW仍串行，每次MAC结果已消费后才发送后处理空间点。DW256次实际提交完成后下一拍才切PW；PW完成要求384次真实写回且metadata=0。已完成写回数量是正常受限流程下排空的证据；不支持任意重复/缺失外设回包的自愈。
- reset同时清MAC计数/指针/流水valid、runner描述符和状态。结果/描述符数组不必逐项复位，因为清计数阻止旧项泄露。PW MAC debug事件重新获得与旧runner一致的高于同拍commit事件的选择优先级。

已定位并要求恢复的一项接口差异：上述修正前MAC的input_ready由i_rstn门控，reset期间为0；冻结MAC reset期间为1。原请求要求保留复位行为，故不接受ready0稿作为最终。协调代理负责移除该门控恢复ready=1，同时保持reset优先取消所有事务；本审查代理只在独立TB的两处复位取消检查增加ready必须等于1的断言，其余向量和检查未改。最终源码哈希与恢复后仿真/物理结果由协调代理的新报告绑定，旧attempt2/attempt3不能冒充恢复后证据。

已直接读取修正前正式ModelSim产物：`mac_sim_attempt2/receipt.json`及`simulation.log`确认119任务、849组、1211周期、两次fault、四槽/续组/同拍push-pop/first-pop/保持/两处reset覆盖PASS，Errors=0；`candidate_attempt3/receipt.json`确认fixed/dynamic与original/stress四组各10例PASS，并含reset_stall、4个PW reset位置、256拍长停顿、final_lane_fault和queue_empty_done。该证据补充前文静态审查not_run状态，不把物理失败或严格八门改写为通过。正式ModelSim验证已解除此前本子代理遇到的启动/审批超时证据限制，但ready恢复稿仍须新一轮回归。

## ready=1 最终恢复复核

已再次读取当前MAC，SHA256为 `ddd15b09196bc6d55fa31803ddc0f5f050a1af40938cfa947b951ebddf7822e2`。input_ready现已移除i_rstn门控，复位清预约后保持原ready=1；复位优先分支仍取消事务。从A0处理标记至endmodule与冻结MAC逐字一致，再次比对为True。

已读取 `mac_sim_attempt3/receipt.json`，绑定上述MAC和包含两处ready=1复位断言的TB（SHA256 `cf2daec04cb756b75ae879e6aa563ce5795149e5a31fa075de4a0895d854df8c`），119任务、849组、1211周期及全部已列覆盖PASS。已读取 `candidate_attempt4/receipt.json`，同样绑定上述MAC与runner `c275fb0ef210b7abae4bed99fa9b7147fc8188854a12757e2bf0453d8a2b70d2`，fixed/dynamic及original/stress四组各10例、共40例PASS。

因此此前“ready恢复稿须新回归”的待办现已闭合，当前复位兼容修复及其语义回归均通过。上文旧哈希、旧回执及发现过程保留为历史；本结论不将物理实现或严格检查的未通过项改写为通过。
