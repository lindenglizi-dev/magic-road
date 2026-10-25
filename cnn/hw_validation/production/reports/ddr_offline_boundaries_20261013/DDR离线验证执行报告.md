# DDR 离线验证执行报告

日期：2026 年 10 月 13 日。状态：**离线条件端点通过，真实 DDR 闭环待板测，严格交付门未通过。**

仍未通过的具体问题：实际 DDR 顶层没有可直接接入旧桥 `i_commit_confirmed` 的已证明写完成事件；旧桥与板测 requester 的 AW/W 呈现方式和最早读返回支持不同。这些接口缺口不能靠模型通过消除。本轮没有修改实际硬件，不产生新的时序或资源通过结论。

## 执行结果

已按“地址和写掩码 → 背压及取消 → CNN 接入方案”的顺序完成离线部分。保持分支 `work/roadyolo`，只在本目录新增验证和报告；没有改生产、计算核、旧桥、约束、训练或位流，没有连接板卡或写 Flash。

| 项目 | 实际结果 |
|---|---|
| 旧基线和生产源码 | 1205 个冻结文件 SHA256 前后完全一致 |
| Python 参考 | 地址和 mask 自检通过，原协议 Python 自检通过 |
| ModelSim 编译 | 0 error、0 warning |
| 原桥回归 | PASS，使用原 testbench，不覆盖旧记录 |
| 新向量 | 每模式 1102 条，三种模式共 3306 条，全部比较错误为 0 |
| 长等待取消 | 每模式 6 类，共 18 次；每类相关等待 1024 拍，每次排空后新 owner 读回通过 |
| 接入方案 | 已完成 [CNN张量搬运接入方案.md](CNN张量搬运接入方案.md) |

最终证据是 `simulation_attempt3/receipt.json`，不是中途旧快照。新 TB SHA256 为 `7c05df57cce244ee4d921f517920da30f044ab171f10bb0d5eba79a6774c220c`；原桥 SHA256 为 `364920d2e1d2c006c62f07a91cb8cda95033b9f17cdfeb7cbaac4cb293b4bd5f`。源文件、输入向量和仿真工具哈希分别保存在该目录的 `source_hashes.json` 与 `tool_hashes.json`。

## 地址与掩码覆盖

共 217 个地址槽：194 个合法地址、23 个非法地址。覆盖预留区起止、两个输入槽、冻结图中 70 个实际存储分配的首末 16 字节及合法邻块、逻辑地址进位边界。

每模式包含：

- 两轮“所有合法地址先写完，再逆序全部读回”，第二轮数据逐位互补，共 388 写、388 读。
- 四处关键地址的全屏蔽、奇偶交错、逐 lane 单开和单屏蔽，共 140 个写读对。16 个 byte lane 均覆盖；每一步新旧字节都不同，避免写错被相同数值掩盖。
- 23 个非法地址分别发读和写，共 46 次拒绝。包括所有非零低 4 位、上下界外地址，以及 `0x07400000`、`0x83400000`；后两者截断后会别名到合法起点，专门检验高位必须先检查。

端点内存只按 **实际 PAXI 地址、实际 WDATA、实际 mask 和真实握手** 更新。Python expected 只参与比较，不反向写入模拟内存。读返回取自该内存。mask 位 1 保留对应 little-endian byte lane。

这能抓桥内的地址截断、byte lane 和 mask 传递错误；不等于真实 DRAM 地址线无别名，也不证明实物容量或 bank/row 映射。

## 背压和取消覆盖

新增测试覆盖 AW、W、AR、写提交等待、读返回等待、结果消费背压。请求接受后，立即毒化上游地址、数据、mask、epoch 和 owner，确认桥使用缓存；结果和接受遥测的 owner/epoch 均比较。

取消后已呈现的请求仍保持 VALID 和载荷直到接受；终结事件到达前 req_ready 与 drain_done 保持为 0；不泄漏旧结果。六种取消位置都随后完成新 owner 的读操作。原回归额外保留缺 RLAST、意外返回、提前 commit、同拍边界与守恒检查；本轮新 TB 没有新增对 late_discard/cancelled_drain 遥测数值的独立断言，不扩大宣称。

| 模式 | 主向量流停顿 | 全测试周期 | 错误 |
|---|---|---:|---:|
| 0 | 无注入停顿 | 13622 | 0 |
| 1 | 固定种子、各阶段独立 0–7 拍停顿 | 26773 | 0 |
| 2 | 周期性 1024 拍长停顿，其余 0–3 拍 | 77596 | 0 |

所有模式最后都附加六种长取消测试，因此六类最大等待均为 1024 拍，并非随机 DDR 的自然峰值。周期包含向量、非法请求复位、取消、排空和新 owner 探测；不是每帧周期、计算核吞吐或真实 DDR 带宽，不能换算成 CNN FPS。

## 严格检查的真实状态

最终检查为 `gate_attempt2/tests.json`：**1075 条 errors，0 strict warnings，delivery_ready=false**。对象仅是新增的非综合 testbench，不是新增 1075 个 FPGA 硬件错误；旧硬件检查记录没有变更。

| 公开门 | 当前状态 | 说明 |
|---|---|---|
| compile | failed | 技能静态解析失败；与 ModelSim 的 0 error 编译分开 |
| ast | failed | formatter 未成功展开 TB，报 `only single module sources are currently supported` |
| readability | failed | 格式、规则条目未闭合 |
| comment | failed | 实体同行注释规则未满足 |
| naming | failed | 命名规则未满足 |
| profile | failed | 严格 profile 未通过 |
| testbench | passed | 静态 testbench 门通过，不替代执行 |
| toolchain | not_requested | 该检查器未内联 ModelSim；外部 ModelSim 执行证据另存，已通过 |

这些门的计数有交叉，不能逐栏相加。静态 AST 未展开意味着不能宣称完整语义静态检查通过。当前按已批准的隔离诊断范围执行，不为变绿去改全局检查器，也不批量重写无关格式。

规范工具另因真实 TB 无端口报 `ports must be non-empty`，完整规范生成未通过；没有伪造端口。已有同名人工接口规范与配置的 WaveDrom 3.6.1 渲染出的 [写时序示意](specification_attempt3/write.svg)、[读时序示意](specification_attempt3/read.svg)。它们不是实测波形，不能代替断言结果。

## 中途问题及最小处理

| 记录 | 具体原因 | 处理和最终状态 |
|---|---|---|
| `simulation/` | Windows 沙箱导致 ModelSim 启动 WinError 623，未进入 HDL 编译 | 通过允许的本地工具执行重跑；未改 HDL 规避 |
| `simulation_attempt2/` | 仿真快照通过，但运行期间 TB 增加断言，结束时源哈希不一致 | 不签核当前源码，保留快照；冻结 TB 后 attempt3 完整重跑，通过且无运行期变化 |
| `specification/` | 沙箱拒绝规范工具读取 contract | 保留日志，允许本地执行后继续 |
| `specification_attempt2/` | 工具将过深 cwd 视为工作区，拒绝引用兄弟 tests 目录 | cwd 改为本验证根目录，不放宽路径检查 |
| `specification_attempt3/` | 无端口 schema 限制 | 原样保留 canonical 失败；两个周期图用正式 renderer 单独生成 |

## 文件和复跑

所有新代码位于当前 `ddr_offline_boundaries_20261013` 目录：

- `reference.py`：地址/byte mask 参考与确定性向量。
- `tests/tb_paxi_boundary_mask.v`：驱动冻结桥并逐项检查。
- `run.py`：复用上一轮工具封装，冻结、检查、仿真和汇总。
- `render_spec.py`：规范限制记录与周期图。

在当前目录执行以下命令可复跑；`prepare` 仅首次执行，已有冻结文件时不重复。每次 gate、simulation、specification 生成新 attempt，不覆盖旧失败。

```powershell
& 'D:/Python313/python.exe' -B -X utf8 run.py check
& 'D:/Python313/python.exe' -B -X utf8 run.py reference
& 'D:/Python313/python.exe' -B -X utf8 run.py gate
& 'D:/Python313/python.exe' -B -X utf8 run.py simulate
& 'D:/Python313/python.exe' -B -X utf8 render_spec.py
& 'D:/Python313/python.exe' -B -X utf8 run.py finish
```

ModelSim 路径为 `D:/modeltech64_2020.4/win64`。Python 沙箱启动器会打印路径警告，需以实际退出码和断言判断；本轮参考和最终汇总退出码为 0。

## 下一步

离线三项已完成，暂无需要用户立即操作的事项。后续先完成已交付独占 DDR 诊断的真实写读回，再依接入方案补写可见性及控制器时序的具体接口证据，接通 Stem → DDR → down2；随后才扩展视频并发。没有新板测结果时不冒充实板通过，但可继续软件侧调度准备，不再扩大 CRC 或通用 DMA 探针。
