# DW 两槽利用：周转优化与后续决定

## 阶段位置

本轮承接v15内部时序基线，属于批准框架B的固定DW/PW小块调度优化。仅修改runner DW valid门限1→2，复用后级两个槽；post、MAC、round、SiLU、壳、SDC、接口、II、数值和复位均保持。没有跨任务MAC重叠、首组预取或增加通用FIFO。

v16原回归及增强回归通过，实际TD布局布线完成，报告内部分区四项时序均无负路径。外部窄口与严格门禁未通过，不把速度改进当成部署通过。

## 根因与最小改动

旧ACK后7拍：c1送lane0；c2等queue=0；c3送lane1；c4再等空；c5送lane2并释放raw reservation；c6装载下一任务；c7接受下一首组。

post本来支持2槽，其ready已要求`queue<2`。runner另加`queue<1`让三标量隔拍发送。新门限只允许利用已存在的第二槽：无反压c1/c2/c3连续发送，c4装载、c5接受首组。先完成旧任务ACK和所有scalar提交，再启动下一MAC，不改变累加上下文或core II。

raw triplet是独立96位保持区；post是两个记录槽，不能把`queue+reserved`不同单位的和拿来当容量证明。真正要求是queue≤2、queue满不接收；raw的数据/通道/位置在各scalar握手前保持，last scalar后才释放；DW→PW仍等待256次真实cache提交。

## 同向量周期

| 测量 | v15 | v16 |
|---|---:|---:|
| 无反压完整DW+PW核心 | 4281 | 4153 |
| DW端点 / PW端点 | 2460 / 1821 | 2332 / 1821 |
| 相同seed随机commit反压完整核心 | 4281 | 4154 |
| 纯PW核心 | 1822 | 1822 |
| DW ACK→下一首组 | 7 | 5 |
| DW任务 / MAC beats / scalars / tail scalars | 128 / 384 / 256 / 64 | 不变 |
| DW队列空等 | 128 | 0 |
| DW_POST周期 | 384 | 256 |

无阻塞省128拍，完整小块减少2.99%，DW减少5.20%；这是周期减少率，不是FPS或识别准确率。随机反压case2为4154，PW排空多1拍，不能硬改成4153。反压由同一case启动后LFSR seed=5eed推进；总运行窗口变短，停顿总数随窗口改变，比较的是端点总周期，不是故障提前退出。

互斥核心分类：storage640 + send640 + wait2560 + DW_POST256 + drain56 + done1 = 4153；case2 drain57，总4154。MAC/pre/SiLU/post活动计数有重叠，只用于活动率，不相加。预装载2894周期（1024表写、1864缓存写）；逐项导出384个值，448/449周期，均单列，不能用窄口速度代替core吞吐。

原完整回归保留：三套DW/PW黄金向量逐级和最终数据、唯一写地址、PW-only、原counter16896组及24个X/Z边界、容量预留1024四态组合、halo地址与复位、长反压、三路原子溢出/合法边界。初次12条schedule断言失败是旧期望7拍/384post/128wait未更新，数据功能一致；原日志保留，按明确新契约更正期望后重跑，不隐藏实际数据错误。

新增增强回归已由root独立compile=0/vvp=0：两槽定向填满后保持64拍、ready=0且不接受新数据；raw triplet、lane、tag/meta及reservation稳定；满载复位清空；三条lane各保持64拍且分别复位，无旧结果泄漏；64组四态队列控制覆盖48组未知count；同时push/pop实测384次。自包含Python两槽参考已PASS；它仅验证占用/顺序/取消，不替代RTL或厂商RAM证据。

## 物理与门禁

v16实际TD自10:42:56开始，10:45:54生成Routed报告，TD exit=0。器件PH1P35MDG324、速度等级−3、100MHz，原SDC不变。内部统计排除顶层输入起点/输出终点，保留DSP/RAM和复位端点；行数不是唯一寄存器数。

| 项目 | v15 | v16实际 |
|---|---:|---:|
| Slice / LUT6 / register | 6499 / 5808 / 4484 | 6452 / 5811 / 4474 |
| DSP / ERAM / I/O | 26 / 1 / 38 | 26 / 1 / 38 |
| 内部setup WNS | +0.072 ns | +0.247 ns |
| 内部hold WNS | +0.023 ns | +0.022 ns |
| 内部recovery / removal WNS | +4.913 / +0.062 ns | +2.234 / +0.068 ns |
| 内部四类失败行 | 0 | 0 |
| 外部setup / hold / removal失败行 | 16 / 311 / 4 | 15 / 348 / 1 |

资源包含窄口验证壳、当前DW/PW调度器及片上缓存，不包含完整权重ROM、DDR、视频或整网。仅固定测试系数，不能代表动态通道重定标成本。

最差内部setup是post的`reg_pre_cut_tag[14]`→MAC DSP `mult22.xa[11]`（slow_m40c）；最差hold是壳`reg_load_addr[4]`→缓存`ramread0.byteaddr`（fast_m40c）。DSP复位recovery最差+2.234ns，runner bias寄存器removal最差+0.068ns。原始全量报告保留，不只抽查正余量路径。

全局仍失败：setup WNS−1.584ns、min WNS−1.364ns。外部hold失败行311→348须明确保留，不用内部通过掩盖。窄口零I/O延迟仅为诊断，不代表真实外设时序。工具STA覆盖100%、Slow/Fast Max/Min已启用，但仍有local/generated clock与DSP dummy-node警告，SYN-5025未全部归因；`shell_route_status.rpt`未生成，不能宣称辅助报告完整或生产签核。所有绑定见`physical/physical_status.json`。

完整6源严格门：4001项诊断，compile通过；ast/readability/comment/naming/profile未闭合；该静态门未请求testbench/toolchain，独立Icarus/TD实际证据分别保存。缺少readable-python-generator不能宣称Python技能严格门通过；脚本只做本地小参考和条件预算，不修改检查器或部署数值。

生产、训练、板卡、位流、Flash、时序例外未修改；所有运行和输出在v16。旧v15源码、SDC、数据库、全量/失败报告及status的7项哈希在前后检查，旧核不覆盖。

## 更新逐层预算与抓手

`verification/layer_cycle_budget.json`列出67卷积，冻结graph hash核对通过，使用原预算清单复用PW/Stem的`2G+10`条件拟合，只更新DW三点/尾点的入队成本。

条件账本：v15 **51,912,186**→v16 **50,815,482**周期，省1,096,704；100 MHz/5 FPS目标20,000,000周期，仍差30,815,482。这些不是整帧实测或上下界：stride1三点尚未在当前stride2 probe验证；G>2 PW/Stem、INT16预测旁路、动态参数、逐tile排空/传输、DDR、非卷积、NMS均没有完整成本。本预算不能宣布约1.97 FPS实测。

此前63,662,586属于未空间打包的旧条件账本；本表先用三点DW重算v15，再和v16同口径比较，不能把全部约12.85M变化归功于这次单常量修复。

下一项最有价值的单变量是**PW组内装载/发射周转**，不是继续细改DW或SiLU：当前wait2560占完整小块61.6%，send与storage各640，保持单context时可先评估PW连续组发射的预取路径和真实RAM端口成本。只准备一个候选，若必须修改核端口/II/故障语义则先申请。得到这项证据后立即比较唯一H24结构预算，不继续无期限优化通用加速器；H24不会自动补齐5FPS，训练选择仍依精度分支证据，当前不训练或改网络。

## 成果入口

- 代码：`rtl/down2_overlap_tile_runner.v:240`，仅一个门限常量改变。
- 回归：`verification/regression_candidate/root_dw_capacity.log`；增强回归另存，不覆盖初轮。
- 参考：`reference/queue_contract.py`；条件预算生成：`reference/generate_layer_budget.py`。
- 新工程：`physical/road_postprocess_low_io_top.al`；不请求位流的`physical/build.tcl`。
- 最终以本目录`physical/physical_status.json`、`pr.db`、全量路径、面积和TD日志为准。
