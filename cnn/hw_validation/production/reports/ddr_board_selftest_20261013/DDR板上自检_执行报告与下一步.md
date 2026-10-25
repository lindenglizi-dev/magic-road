# DDR板上自检：执行报告与下一步

日期：2026-10-13。工程分支：`work/roadyolo`。独立目录：`cnn/hw_validation/production/reports/ddr_board_selftest_20261013/`。

## 先看结论

**请求器和显示握手功能测试通过，真实顶层已完成安路综合、布局布线；显示CDC时序未闭合，尚未生成位流，也尚未做真实DDR读回。**

这次不是等待DDR内部电路资料：已经将独立写读测试器直连原厂 `ddr2` IP，避开旧桥接器将AWREADY当成WREADY、读尾输出未连接的问题。旧桥接器、生产顶层、CNN算术核及已上板通过的C7自检位流均未覆盖。

本次只验证独占DDR，不运行摄像头或CNN。缺少兼容DDR2器件模型仅限制完整电脑存储器仿真，不阻止板测工程准备。

## 1. 已实现的最小实验

```text
50MHz板载时钟 → 原有PLL的100MHz输出 → 原厂DDR IP
                                    ↓ dhi_clk≈133.33MHz
                           独立PAXI写读比较器
                                    ↓ 冻结载荷请求/确认
                         原有75MHz HDMI TEST显示
```

主要代码和接口：

| 文件 | 功能及接口边界 |
|---|---|
| `rtl/road_ddr_selftest.v` | 25位原生地址、128位数据、16位屏蔽；AW/W独立记账，单读在途，比较全部128位及RLAST |
| `rtl/road_ddr_selftest_top.v` | 直连真实原厂DDR IP；各域异步断言/两拍释放；复用已验证HDMI源文件，未改原文件 |
| `tests/tb_ddr_selftest.v` | 可控端点17项测试；不是DDR器件模型 |
| `tests/tb_ddr_display_cdc.v` | 133.33MHz/约75MHz双时钟冻结载荷、帧边界和复位恢复测试 |
| `reference.py` | 独立Python字节模式和事务参考 |
| `run.py` | 构建/仿真/门禁/规范/汇总入口；工作目录和输出限定在本验证目录 |
| `rtl/spec/` | 两个RTL模块的生成式接口规范及WaveDrom周期图；示意图不表示真实DDR返回延迟 |

实验访问原生地址 `0、8、16、24`，先写四字，再逆序读回；第二轮写入逐位取反的数据再读回。共8次写入、8次读回比较，检查128字节读回数据；实际只覆盖64字节存储位置，不能代表全容量测试。

读写背压期间保持有效请求和数据，AW/W按各自ready退休。W与AW同时开始提供，不利用手册允许的“写数据最迟晚两拍”窗口来延后生成。超时/协议错误/比较错误锁存首错、不自动重试。发生部分接受后故障，恢复必须同时复位原厂IP和请求器，不能只重置计数继续发送。

### 手册确认与未确认边界

依据用户提供的 `IPUG035_1.4`：

- 印刷第30页：PAXI `wstrb` 是高有效数据屏蔽，因此全零为全字写入；不能套用AXI全一WSTRB写法。既有PH1P工程也使用全零。
- 印刷第41页表3-5：16-bit物理数据宽度对应 `byte_address = paxi_address × 2`。本次原生步长8对应16字节。
- 印刷第41–42页图3-15至3-19：写读握手和写数据生成窗口；已实际查看图，不只搜索关键词。
- `bvalid/bresp` 在该手册中是保留信号，当前生成IP也不对外提供写完成响应。**AW/W都接受只表示已交给控制器，不冒充DRAM写完成或CNN输入槽READY屏障。**

这份资料针对PH1A接口，当前PH1P生成源码可核对接口形状、掩码传递和地址宽度，但不是PH1P集成DDR2的完整保证。真实板测仍需确认该IP实例上的写后读行为、地址映射及字节顺序。52–64MiB区域、容量末端和视频并发均未验证。

## 2. 本轮实测

### 功能回归

`simulation_attempt3/receipt.json`：**17/17通过**。正常端点101周期；独立气泡140周期；同拍读返回61周期。它们仅是可控端点周期，不是DDR带宽或板上延迟。

覆盖正常、独立AW/W/AR背压、随机气泡、长停顿、同拍/延迟返回、翻转数据、缺RLAST、初始化及各通道超时、无请求返回、PHY ready丢失、部分写/在途读复位恢复、通过后额外返回。补充首错地址、完整期望/实际字及终态保持断言后再次全部通过。

`display_simulation/receipt.json`：**60次完整快照捕获通过**，无半表更新、非帧边界更新或复位旧结果泄漏；本次最短实测载荷年龄33.803ns。两级请求同步和确认前载荷保持提供协议依据，仿真不证明亚稳态可靠性或布局布线后的STA签核。

### 真实安路物理结果

`physical_attempt2/` 保存工程、IP副本、约束、`gate.db`、`pr.db`、网表和全量端点报告。TD 6.2.168116，PH1P35MDG324、速度等级3。

| 项目 | 结果 |
|---|---:|
| Slice | 3922 / 21216 |
| ERAM | 5 / 108 |
| DSP | 0 / 40 |
| PLL | 3 / 6 |
| 顶层逻辑端口展开 | 51位，含封装内DDR端口 |
| 实际PAD统计 | 10，含TMDS差分配对 |
| Setup WNS | **−0.825ns，183个失败端点** |
| Hold WNS | **−0.155ns，1个失败端点** |
| Recovery最差已报告余量 | +1.481ns |
| Removal最差已报告余量 | +0.030ns，余量较小 |
| STA覆盖率 | **92.69%，不是完整签核** |

上述资源含原厂DDR及HDMI，不含CNN计算。不能用0 DSP推导完整CNN资源，也没有将这个工程与原计算自检工程合并。Slow/Fast的Max/Min均启用。全部端点报告共提取7143条setup、9351条hold、1445条recovery及1445条removal记录；这是报告记录数，不当作独立目标数。

DDR用户域自域路径：setup +0.172ns、hold +0.054ns，未发现该自域的时序违例；这不等于实际DDR存取通过。恢复/移除的正余量也只限已检查路径，不能覆盖未约束外部入口。

## 3. 未通过项的具体原因

### A. 183个setup：冻结载荷跨域被按相邻边沿检查

方向为 `u_ddr2/usr_clk → PLL.clkc[4]`，即133.33MHz到75MHz显示域。最差路径：

```text
road_selftest_display_Inst/reg_hold_payload_reg[187]_syn_2
  → road_selftest_display_Inst/reg_active_payload_reg[186]_syn_2.ima
slack = −0.825ns
data delay = 0.626ns，logic level = 0，STA相邻边沿预算仅0.832ns
```

不是128位比较器过长，也不是DDR控制器的运算吞吐瓶颈。冻结载荷在同步请求到达、且VS边界满足时才采样；当前没有对这一多周期协议施加新的受限时序处理。由于两域从同一参考时钟派生，TD仍按其推导的相邻边沿关系检查。

### B. 1个hold：确认到源域同步器首级

方向为75MHz到DDR用户域，最差端点：

```text
road_selftest_display_Inst/cnt_y_reg[0]_syn_2
  → road_selftest_display_Inst/reg_request_reg_syn_3.imb
slack = −0.155ns，data delay = 0.410ns，skew = 0.501ns
```

已追踪路由网表：终点这个PH1P LSLICE的B寄存器实际是 `reg_ack_meta`，`.imb`接 `reg_acknowledge`；A寄存器才是 `reg_request`。**不能仅凭打包后cell名称把它误判成坐标计数器直接写请求状态。** 请求meta/sync、确认meta/sync均仍可在网表中找到。

同理，3条setup的打包cell名称含 `state_current` 或 `reg_actual`，但属于上述显示跨域路径组。后续选择约束必须按实际pin/net连接映射逻辑寄存器，不得按这些名称做通配豁免，更不能切掉请求器内部数据路径。

### C. 覆盖率及原厂警告

`check_timing.rpt`仍有23个缺输入延迟、49个缺输出延迟对象（含DDR专用物理端口）；无真实外部契约前不补虚构数值。报告还有原厂模块的未驱动/位宽/综合忽略延迟警告及SYN-5025；没有宣称全部无害。先保留原厂配置，不擅改加密核。下一轮只核对有效PAXI地址、数据、valid及读回捕获路径，避免将所有厂商保留端口警告扩展成无边界审计。

仅保留原厂DDR SDC中MCU域的异步分组；本轮**没有新增**false path、MCP或宽泛clock group。

### D. 严格门禁，不能当成功能失败次数

最终门禁目录见 `strict_summary.json` 的 `report_directory`。RTL **1039条错误/18条严格警告**，两份TB **530条错误**，均未交付闭合。规则检查存在重叠，不把八列数字相加。

| 门禁 | RTL | TB |
|---|---|---|
| compile | 静态解析通过；真实TD也展开成功 | 严格解析器不支持本次无端口TB；ModelSim真实编译/执行通过 |
| ast | 10条格式/AST约束失败 | 解析失败保留 |
| readability | 未通过，含缩进、区域锚点和表达式限制 | 未通过 |
| comment | 10条失败 | 15条失败 |
| naming | 未通过 | 未通过 |
| profile | 通过 | 未通过 |
| testbench | RTL入口未请求 | 静态TB门通过，另有真实执行日志 |
| toolchain | 此静态门未请求；另存ModelSim/TD证据 | 同左 |

语义相关诊断（位宽、驱动、FSM、复位、溢出）分别导出 `strict_rtl_semantic_review.json`、`strict_tests_semantic_review.json`。其中官方模块输出的驱动/端口分析也受该检查器接口建模限制；不能全部归为排版问题，亦不能把它们说成1039个真实硬件逻辑错误。官方HDMI接口文件导致严格格式器无法解析的历史执行失败也保留；未修改全局规则以获得绿色结果。

## 4. 下一步：只处理显示CDC签核，不改CNN或原厂DDR核

**需要确认的范围是限定CDC时序处理，而不是新硬件协议。尚未实施以下任何例外。**

建议在新的独立候选中：

1. 冻结本目录的两份RTL、已完成数据库和全部失败报告；不覆盖当前物理基线。
2. 按网表实际连接列出：`reg_request → reg_request_meta`、`reg_acknowledge → reg_ack_meta`的两个首级入口，以及冻结载荷到显示active寄存器的有效数据pin集合。对逻辑位与打包cell逐项映射，核对没有误选第二级或CNN/DDR客户数据路径。
3. 对两个控制同步器**首级入口**申请精确的CDC时序例外；继续检查meta→sync级间setup/hold和两级结构。不同步豁免整个时钟域。
4. 对冻结载荷申请受限多周期/物理最大延迟约束。候选物理上限7.5ns，低于结构上至少两个像素周期的采样等待；先核实TD支持的命令语义。保留载荷稳定、请求/确认顺序及帧边界断言，不能仅false-path掉数据而不保留物理延迟限制。必要hold调整必须列明对象和理由，不预先全局切除。
5. 不豁免任何复位recovery/removal、域内数据路径或同步器第二级；重新跑17项请求器和CDC回归、布局布线及全部端点报告。另核对未约束对象、原厂SYN-5025影响和有效数据路径。
6. 限定诊断验证通过后，再生成新的JTAG/SRAM DDR测试位流及单独加载说明。到时用户才需换位流并观察TEST状态和错误诊断带；当前无需操作板子或补芯片内部结构资料。
7. 真实板测8读比较通过后，再逐步扩展地址边界、掩码字节、52–64MiB区域和压力测试；最后再接CNN DMA及视频仲裁。**首轮四地址通过不能直接发布生产输入槽READY契约。**

如果不批准限定CDC约束，备选是另做无HDMI的DDR状态灯实验；那需要先核实板级LED引脚，不自动引入新接口或引脚假设。本轮不同时做这条备选。

## 5. 可复现入口与保护记录

使用 `D:/Python313/python.exe -B -X utf8 run.py <action>`，动作包括 `check`、`simulate`、`display`、`gate`、`specifications`、`physical`、`collect`。`prepare`仅首次冻结时运行，禁止覆盖已有冻结清单。每次验证使用新的attempt目录，不清除旧失败日志。ModelSim和TD在受限启动环境中曾遇到DLL/路径权限错误，获准的本地运行环境已实际执行成功；这些环境错误不伪装为RTL修复。

`frozen_check.json`：465个历史文件哈希不变。`physical_attempt2/original_ip_check.json`：68个原厂/HDMI源资产不变。IP在新目录副本中实现。`artifact_manifest.json`保存当前新模块、TB、脚本、规格和汇总的哈希。

未训练、未改生产、未加载板子、未生成位流、未写Flash。已通过的原C7计算自检仍可原样恢复；本轮尚无DDR板测PASS记录。
