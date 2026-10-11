# PW组内预取：执行与吞吐决定

## 本次位置和边界

承接v16，执行冻结框架B中的PW组内装载/发送重叠。只改固定down2的Cin16两组PW调度；MAC、round、SiLU、post、外部接口、核II、数值、即时故障、复位、DW以及SDC不变。不是跨任务MAC重叠，不改网络、训练或生产工程，不生成位流、上板或写Flash。旧v16七项冻结输入运行前核验PASS，运行后再次核验。

候选RTL SHA256：`689cf1ff06d422d7d9db04722e6c55d8acf8763343d2bd0396b01022b34a93ca`。原核和post不覆盖。

## 根因、具体改动及逐拍契约

旧PW每个任务两组归约：STORAGE0锁存G0 → SEND0接受 → STORAGE1锁存G1 → SEND1接受。虽然MAC同一归约内II=1，runner主动插入了一个装载空拍。

新增`wire_mac_prepare_group`只在PW SEND/G0指向G1。当前MAC引脚仍来自原reg_mac保持寄存器，不直接使用next组合读数据。G0被真实接受的沿才将预读G1锁存到原reg_mac四组字段，并留在SEND；G1下一沿可接受。未接受时不锁存、不递增，G1被反压时已锁存数据保持。PW任务关闭和ACK后下一任务两拍不变。

每个PW任务的无阻塞序列：锁存G0、接受G0并锁存G1、接受G1、等待原结果、ACK。first/last仍只对应G0/G1，偏置first一次。G1末组故障仍按原三路原子协议取消结果；metadata/post参数选择不按新预取索引变化。DW继续原STORAGE和发送路径，DW→PW仍等待256项缓存提交。片上PW读取路径新增加了组地址选择，物理成本以新实际顶层为准，不用旧资源替代。

Python `reference/pw_prefetch_contract.py`先于RTL，覆盖16位置×8输出组、连续/停顿、G0前/G1前复位及末组取消。只证明调度与地址，不代替整数或RAM硬件验证；readable-python-generator未提供，不宣称其严格技能门通过。

## 同向量实测周期

| 测量 | v16 | v17 |
|---|---:|---:|
| 无阻塞完整DW/PW核心 | 4153 | 4025 |
| 固定seed随机commit反压完整核心 | 4154 | 4025 |
| DW端点 | 2332 | 2332 |
| PW端点 | 1821（随机1822） | 1693 |
| PW-only核心 | 1822 | 1694 |
| PW首组→末组间隔 | 2 | 1 |
| PW末组→ACK / ACK→下一首组 | 10 / 2 | 10 / 2 |
| DW ACK→下一首组 | 5 | 5 |

无阻塞完整小块省128拍，减少3.08%；PW端点减少7.03%。随机案例额外1拍排空减少是窗口变化，不把129拍都归为128次结构空泡消除。相同随机seed=5eed，运行长度改变，停顿次数1004→982；不是固定停顿输入逐拍完全相同的实验。核心运行、预装载和导出保持分开：预装载2894拍（1024表、1864缓存），导出384项/449拍，不能算为每帧CNN吞吐。

互斥完整核心：storage512 + send640 + wait2560 + DW_POST256 + drain56 + done1 = 4025。PW-only：storage128 + send256 + wait1280 + drain29 + done1 = 1694。原MAC/pre/SiLU/post/writeback活动周期有重叠，不相加。DW128任务/384 beats/256 scalars/64 tail、PW128任务/256 beats/384 scalars不变，640次真实cache写回。

root原回归和增强回归均独立compile=0/vvp=0；原4cases PASS，新增case4 PW随机MAC-ready seed1d0f观察284拍停顿（G0/G1各142），核心1978=1694+284，384项黄金输出仍一致。原最终日志`cases=4`是历史显示字段，实际case0..4均已运行，不能据此隐去新增案例。

三套完整小块acc/pre/SiLU/post/最终384项及tag/地址逐项一致。增强测试每次PW接受都核对激活、权重、偏置、mask和first/last；G0接受前复位、G1预取后64拍hold复位无ghost；真实G1末组溢出只产生1组故障结果，pre/writeback为0且不能export。原队列满64拍、三lane复位、16896计数转移/24XZ、halo/cache、故障边界继续通过。

初次旧周期期望产生5条失败，数据对拍无误，原失败日志保留，按新逐拍契约更新期望。增强TB的force/release-ready激励死锁也保留为测试平台失败：在SEND期间逐拍明确驱动0/1、同一信号控制MAC与runner两端握手，离开SEND才释放；不是改DUT或把失败屏蔽。child compiler曾Windows C0000005；root独立编译exit0和仿真exit0为最终实证，不用异常编译产物代替正常编译证据。

## 实际实现、门禁和未通过项

TD于2026-10-08 11:36:10启动，11:43:12生成Routed报告，exit=0；PH1P35MDG324/−3/100MHz，原壳/SDC/ADC不变。包含固定DW/PW调度、片上缓存、MAC和固定后处理及38位窄口壳；不包含完整权重ROM、DDR、视频链或完整CNN。

| 实际物理项 | v16 | v17 |
|---|---:|---:|
| Slice / LUT6 / reg | 6452 / 5811 / 4474 | 6494 / 5822 / 4457 |
| DSP / ERAM / I/O | 26 / 1 / 38 | 26 / 1 / 38 |
| 内部setup / hold WNS | +0.247 / +0.022 ns | +0.316 / +0.025 ns |
| 内部recovery / removal WNS | +2.234 / +0.068 ns | +3.515 / +0.051 ns |
| 内部四项失败行 | 0 | 0 |
| 外部setup / hold / removal失败行 | 15 / 348 / 1 | 41 / 279 / 2 |

内部分区仍排除顶层i_*起点及o_*终点，包含DSP/RAM；setup最差壳`reg_load_low[2]`→runner RAM写使能，hold最差runner写回计数→壳快照寄存器；removal最差release_done→MAC结果寄存器。全部路径和端点原文保留，行数不是唯一寄存器数量。

全局setup WNS−1.443ns、min−1.281ns仍失败；外部setup15→41、removal1→2增加，不能因hold减少或内部通过忽略。没有新增例外、编造外设延迟。STA报告100%并启用Slow/Fast Max/Min，仍保留local/generated clock、DSP dummy-node警告和未全部归因SYN-5025；`shell_route_status.rpt`未生成，不宣称所有辅助报告完整。仿真RAM是Icarus行为模型，本轮没有新厂商模型仿真或板测。完整绑定见`physical/physical_status.json`。

六源严格检查实际4021项诊断，v16为4001。增加20项分别为VG147组合操作预算10、VG062注释5、VG040实体注释2、COMMENT_COMMENT_PLACEMENT2、VG125状态结构1。不能将组合/状态项全部归为格式。compile通过；ast/readability/comment/naming/profile未闭合；静态门未请求testbench/toolchain，实际Icarus与TD证据另存。既有SYN-5025与外部接口警告不删除，不新增false path或伪造输入延迟。周期图运行时Node24.21/npm11.19/WaveDrom3.6.1冒烟通过；首次沙箱临时目录权限失败不是RTL失败，权限复跑成功。

## 逐层条件预算及不再拖延的决定

`verification/layer_cycle_budget.json`给出67层明细，与冻结graph哈希一致。仅Cin16 PW按已测试的两组任务省1拍重算：v16 **50,815,482→v17 50,741,754**，省73,728。其他Cin/Cout、stride1DW、完整层末排空、DDR、动态量化、预测INT16、非卷积及NMS未实测，本表不是上下界或整帧FPS。

同时完成框架唯一H24的**形状算术对照**，没有改model.py/权重/RTL：156,114,432 MAC、96,900权重、2,141偏置；沿同一未验证调度假设的条件预算38,718,330拍，仍超过20M目标18,718,330拍。H24没有精度结果，不能凭这个数字切换网络或保证5FPS。

结论：这次组内优化可以保留，但不足以解决吞吐。wait2560占4025的63.6%，原单归约结果关闭10拍仍是主因。冻结账本有条件DW1,096,704任务、PW1,386,432任务、Stem221,184任务；`2G+10`中的10拍周转项合计27,043,200拍，单这一条件项已超过20M。这不是整帧实际等待测量，但明确指出下一项应瞄准任务关闭，而不是继续追加DW门限/SiLU微调；当前Cin16实验也不能推广成所有PW已完成。

下一段必须选择有限路径：先以当前真实图的较深PW形状（48/96/192输入、最多24组）检验组内连续预取及端口成本，同时准备框架C所需真实动态参数成本；若要改变算术核任务关闭、跨任务重叠或增加动态系数端口，则集中提交接口/故障/资源决定，不擅自实施。H24只作为同数据、同训练预算的一次精度对照，不替代核周转/DDR证据；本轮没有启动该训练。目标是在下一批证据后选择一条主线，不继续无限扩展通用加速器。

## 成果入口

- 改动代码：`rtl/down2_overlap_tile_runner.v`，组预取选择和G0 accept锁存G1。
- 模块规格与周期图：`spec/down2_overlap_tile_runner_spec.md`及其waveforms目录。
- 原回归：`verification/regression_candidate/root_pw_prefetch_baseline.log`。
- 增强回归：`verification/regression_candidate/root_pw_prefetch_enhanced.log`，原轮不覆盖。
- 条件预算生成器：`reference/generate_layer_budget.py`；小调度参考：`reference/pw_prefetch_contract.py`。
- 新物理工程：`physical/road_postprocess_low_io_top.al`；build.tcl不含位流生成。
- 最终实现以新`physical/physical_status.json`、pr.db、全量时序、资源及日志绑定为准。
- 算术/仿真/黄金向量闭包：`source_manifest.json`；工具版本、入口/执行文件哈希与工作目录：`toolchain_receipt.json`。
