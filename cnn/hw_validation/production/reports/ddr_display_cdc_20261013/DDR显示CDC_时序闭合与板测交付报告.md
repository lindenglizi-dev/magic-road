# DDR 显示 CDC：时序闭合与临时板测交付

日期：2026-10-13。状态：**有界 CDC 诊断实现通过；真实 DDR 板测未执行；不是整机或 CNN 部署通过。**

## 1. 尚未通过的具体项目

- 外部接口时序未签核：23 个输入、49 个输出缺少输入/输出延迟；其中包含 DDR、复位和 HDMI 端口。不能编造板级时序来消除提示。
- STA 覆盖率为 92.69%，不是 100%。仍有 3 个本地时钟及其 master 连接提示、2 类 dummy node 提示，需要分别解释，不能用“已计时路径零违例”替代它们。
- 严格门禁：RTL 1039 errors / 18 strict warnings；TB 530 errors / 0 strict warnings。与前基线相同，未放宽检查、未隐藏旧失败。
- 当前只有受控端点仿真，不是完整 DDR 存储器模型仿真；开发板的真实写入、读回尚待用户执行。
- 当前测试仅覆盖 4 个地址、两套互补数据，**64 字节独立空间、128 字节累计比较量**。不证明容量、地址末端、52–64 MiB CNN 区域、掩码、视频并发、输入槽发布屏障或 CNN 5 FPS。

## 2. 本轮改动与冻结边界

工作目录：`E:/project/qiansai/anlogic_topic2_work/lab1_sc500_road_vision/cnn/hw_validation/production/reports/ddr_display_cdc_20261013/`。

只在此目录新增约束解析、构建/报告与测试产物。DDR requester、顶层及复用显示模块的 RTL 与冻结版本相同。旧基线及依赖共 891 个文件哈希检查无变化；原始 68 个 IP/HDMI 文件无变化。没有训练、生产修改、板卡访问或 Flash 写入。

| 文件 | 功能 |
|---|---|
| `build/display_cdc.tcl` | 从实际打包后的网表定位精确 CDC 引脚，生成平面 SDC 与映射表 |
| `build/build.tcl` | 独立综合、布局、读取打包后 CDC 约束、布线、报告与数据库导出 |
| `run_cdc.py` | 复用冻结回归、冻结检查、报告解析和临时诊断位流生成 |
| `bitgen.tcl` | 导入已验证数据库，复核时序及数据总线连接后生成文件；无下载命令 |
| `rtl/road_ddr_selftest.v` | 冻结请求器副本：独立 AW/W 接受、单读在途、逐项比较、超时与首错保持 |
| `rtl/road_ddr_selftest_top.v` | 冻结顶层副本：实际 DDR2 IP、时钟复位和 HDMI 显示；不含 CNN |

## 3. 实测结果

器件 PH1P35MDG324、速度等级 3；工具 TD 6.2.168.116。时钟包含 DDR 用户约 133.33 MHz、参考 100 MHz、像素 75 MHz、串行 375 MHz。结果来自重新布局布线的 `physical_attempt3`，不是仅修改旧报告。

| 项目 | 旧失败基线 | 当前实际结果 |
|---|---:|---:|
| 已计时负余量记录 | setup 183、hold 1 | setup/hold/recovery/removal 均 0 |
| setup 最小余量 | 失败 | +0.074 ns |
| hold 最小余量 | 失败 | +0.020 ns |
| recovery 最小余量 | 单独保留 | +1.481 ns |
| removal 最小余量 | 单独保留 | +0.030 ns |
| 无效约束 | 曾在失败尝试中出现 184 项 | 0 |
| Slice / ERAM / DSP / PLL | 见冻结报告 | 3922 / 5 / 0 / 3，含 DDR 与 HDMI，无 CNN |
| 逻辑 I/O / PAD | — | 51 / 10；不是将全部 DDR 引脚理解为 10 个普通 I/O |

检查记录数量：setup 6950、hold 9161、recovery 1445、removal 1445；这是报告记录数，不等同唯一端点数。包含工具适用的 Slow/Fast、Max/Min 检查；RAM 路径另见 `eram_inputs.timing`、`eram_outputs.timing`，本设计 DSP 数为 0。

当前最差 setup 是 DDR IP 内部 `mdl_tck_reg[3]` → `init_rdqsp_reg[11]`，133.33 MHz → 100 MHz，数据路径 1.282 ns；最差 hold 是 `init_rdqsn_reg[5]` → `init_rdqsp_r_reg[0]`。这些余量很小，仍需真实板测，不能把它们宣传为宽裕的整机裕量。最差 removal 是像素复位释放到显示 request_sync 异步复位端，仍保留检查。

### 3.1 CDC 处理为何成立，处理了什么

原协议不变：源域冻结 256 位 payload 后翻转 request；目标域经过两级同步，在帧边界接收完整 payload 并返回 ack；源域收到同步后的 ack 前不改变 payload。

1. 仅切除 request 和 ack **首级 D 输入**的异步跨域 setup/hold；精确指定源 clock pin、源 Q through pin、目标 D，避免同一 Slice 的其他寄存器被误切。
2. payload 只设置精确逐路径 **7.500 ns datapath-only 最大延迟**，含 C2Q、布线和目标 setup，不设置全局时钟组 false path。
3. TD 官方 SWUG200 §3.11.2–3.11.3 说明该模式会自动排除对应 payload 的 hold 检查。本报告明确保留这一事实，不声称 payload 仍按同步 hold 签核；稳定性依据冻结/确认协议及最大数据延迟，而非异步相位的同步 hold。
4. 两条同步器的首级到第二级继续完整计时：request setup/hold 为 12.418/0.142 ns；ack 为 7.019/0.058 ns。复位 recovery/removal 未切除。
5. 256 逻辑位中 57 位严格匹配预期常零；剩余 199 个逻辑非零位映射到 182 条唯一物理数据路径（常一标记位共享寄存器）。182 条路径全部满足界限，最差数据路径 1.378 ns 加 setup 0.064 ns，余量 6.058 ns。
6. 协议结构给目标采样留下至少两像素周期；仿真观察到最小 payload 年龄 33.803 ns。仿真不证明亚稳态 MTBF，也不覆盖任意独立时钟域复位组合。

纠正前报告：旧 **183 个 setup** 是 **182 条 payload + 1 条 request 首级**，不是 183 条 payload；另 1 个 hold 是 ack 首级。旧报告和失败产物保留，未覆盖。

### 3.2 已执行功能及约束有效性验证

- 请求器 17/17 用例通过，包括 AW/W 独立背压、同拍读返回、错误数据、RLAST、初始化/读写超时、异常返回、PHY 失效及复位恢复。故障用例中的非零 error 是预期检测结果，不是普通成功写读。
- 显示 CDC 60 次快照检查通过，含握手和公共复位；实际最小冻结年龄 33.803 ns。
- 负向约束实验仅将隔离探针的界限从 7.5 ns 改成 0.001 ns，正确产生 −0.689 ns setup 违例，证明约束真正进入引擎；没有把负向值带入交付实现。
- 导入最终数据库后再次得到 setup +0.074 ns、hold +0.020 ns，全部已计时记录无负余量。
- 导入数据库检查 128 位真实 DDR 读数据和 128 位写数据：256 个 retained 数据网均有驱动和消费者，读数据驱动来自 DDR 实例。控制信号可能被综合折叠，未以不存在的顶层别名冒充其独立物理证明；控制行为由冻结 RTL 和端点测试约束。

## 4. 失败原因与最小修复记录

| 失败表现 | 查明原因 | 本轮修复 / 保留限制 |
|---|---|---|
| 直接执行 Tcl 后负余量未变 | 约束未通过 TD 的 SDC 读取入口生效 | 生成平面 SDC，再 `read_sdc`；用负向探针证明有效 |
| 逻辑网名在物理阶段找不到 | TD 打包后寄存器引脚变为实际 Slice Q/D | 布局后通过实际网连接定位；空集合立即失败 |
| 重读约束仍有 184 个无效对象 | 同名 SDC 先在逻辑阶段读取，后覆盖文件，TD 仍缓存旧文本 | 正式流程只在打包完成后首次读取该 SDC，然后布线 |
| 解析器把末条路径误归类 | ignored 路径有端点但无 Slack，覆盖前一条已计时记录 | 在新 Begin Point 出现时结束前记录；核对 182/1/1 分类与原始报告 |
| 首次 bitgen 审计提前停止 | 综合删除顶层 awvalid 等别名，不代表 DDR 数据断开 | 从实际路由网表查询保留的完整读写总线；首次失败未生成位流并保留日志 |

`physical`、`physical_attempt2` 及 `probe*` 均保留。`physical_attempt2` 有无效约束，**不是通过版本**；只认 `physical_attempt3` 和其数据库导出的临时位流。

### 4.1 SYN-5025 的具体范围

日志可见的置零来源包括：CAL_EN=0 分支未驱动的校准 APB 读数据，以及只读初始化 ROM 未使用的写 DI 端。当前 APB 空闲，初始化 ROM 的 readmemh 有加载记录；没有为消除告警修改 IP。日志有同类告警抑制，因此这只能解释已定位类别，不能宣称厂商 IP 的所有未驱动对象均已闭合。真实数据总线连接另有 256 项检查。

### 4.2 严格门禁不与物理通过混为一谈

RTL 的 compile/profile 通过，但 AST 格式、readability、comment、naming 未闭合；TB 静态解析仍有 2 个 parse errors，具体为检查器报告 `only single module sources are currently supported`，不是 ModelSim 报告的 RTL 语法错误。该限制又引出多项依赖 AST 的诊断，因此不能把 530 条都理解为独立硬件错误，也不能删除这些失败。ModelSim 实际编译执行成功与静态解析失败分别保留。各门禁计数有交叉，不能把八项分项数再次相加。

本轮未对冻结 RTL 做无关格式重写。readable-script-generator / readable-python-generator 当前不可用，构建脚本仅做 Python AST、实际运行与断言验证，不声称通过不存在的脚本技能严格门禁。

## 5. 临时诊断位流与操作入口

文件：`diagnostic_bitgen_attempt2/HX1P35A_C7_DDR_DIAG.bit`。

- 大小：1,789,542 字节。
- SHA256：`9250eadc204e53da4bf4d211dc7d662c3937c251b49433875be869e2a0b3ffdc`。
- 路由数据库 SHA256：`b2a8c8c4628fcf45e0b9cc1a68503d14c8fe50915855d5a5cd015d6f15fac015`。
- 仅供 HX1P35A / PH1P35MDG324 的临时 SRAM/JTAG 诊断；**不是 CNN 模型位流，不写 Flash，不是板测通过证据**。

具体操作见同目录 `DDR临时板测操作.md`。必须选择这个新文件；旧计算自检同样会显示绿色 TEST，旧绿色画面不能证明 DDR 通过。

## 6. 证据索引及下一步

相对本目录：

- `comparison.json`、`status.json`：机器可读实测状态。
- `frozen.json`、`frozen_check.json`：冻结清单与 891 文件不变记录。
- `simulation/receipt.json`、`display_simulation/receipt.json`：本轮重新执行的功能结果。
- `gate/rtl.json`、`gate/tests.json`：严格门禁原始结果。
- `physical_attempt3/`：源文件哈希、实际 gate/pr 数据库、路由网表、面积、完整端点报告、RAM/复位/同步器分项报告、coverage 与工具日志。
- `physical_attempt3/display_cdc_mapping.tsv`、`resolved_display.sdc`：逐项映射和实际生效约束。
- `probe_attempt7/negative_receipt.json`：过紧界限必须失败的负向验证。
- `diagnostic_bitgen_attempt2/receipt.json`、`paxi_connectivity.tsv`、`imported.timing`、`td.log`：位流哈希、连接复核及生成证据。
- `artifact_hashes.json`：本次关键交付文件的哈希索引；不覆盖历史 manifest。

下一步先由用户加载临时位流，提交新版本的颜色、心跳、三次 K4 复位及 10 分钟稳定结果。四地址测试成功后才扩展地址边界、掩码、容量与写后读可见性，再进入保留视频区之外的 CNN DMA 验证。当前不需要 DDR 芯片内部电路资料，也不把缺少完整存储器仿真模型作为这次板测的阻点。
