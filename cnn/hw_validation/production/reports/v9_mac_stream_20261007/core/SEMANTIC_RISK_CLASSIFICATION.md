# road_mac_probe 候选语义风险分类

## 当前证据

- Python 周期/数值参考自检：PASS。
- ModelSim `vlog`：0 error，0 warning；仅证明候选可编译。
- readable-verilog strict 原始门禁：`delivery_ready=false`，431 errors，0 strict warnings。完整未删减输出保存在 `strict_gate.json` 与 `strict_gate.md`。
- 公开八门：compile passed；comment passed；profile passed；testbench/toolchain 在该次 strict 调用中 not requested；AST、readability、naming failed。

## A. 必须阻断“生产就绪”声明的门禁风险

1. `VG145` 10 项、`VG146` 44 项：组合源锥/操作预算对 A5 候选加法、fault 汇总、ready/valid 控制及部分乘法表达式报阻断或无法静态确定。外部 9 周期延迟已冻结，不能通过随意加级规避；需要物理结果和人工架构审查，不作放宽。
2. `VG088` 1 项 inconclusive：存在工具无法静态确定宽度的分支条件。保留为未闭合证据，不解释为通过。
3. 独立功能回归和物理 Fmax 尚未在本报告生成时完成；编译成功不能代替执行、综合或布局布线。

## B. 不应误判为已证实功能错误的规范阻断

- `VG015` 93 项：内部 reg 缺少声明初始化。所有状态均有异步复位，但不满足 Erie 声明初始化规范。
- `VG020` 10 项：一个时序块写多个目标，不满足 one-reg-per-always 规范。
- `VG061` 32 项、`VG070` 3 项：region/group 归属不满足 formatter 规范。
- `VG062` 190 项、`VG066` 20 项、`VG060` 1 项、`VG068` 1 项：行内语义注释、重复注释、对齐和固定文件头路径规范不满足。
- `VG156` 12 项：`stage0..stage3` 的数字 token 不在命名白名单。
- `VG138` 3 项：组合表达式中的常量未满足显式位宽格式。

这些问题仍是 strict 交付阻断，不因 ModelSim 编译通过而豁免；为避免在功能回归进行中制造大面积纯格式重写，本候选保留原始报告并明确不声明 production-ready。

## C. 合同边界风险

- 单上下文：接受 last 后才能等待结果并在握手后重开输入，不支持多个独立 job 交错。
- signed33 范围由上层冻结的 24 组/192 项数值证明约束；first0 历史继续不代表无限安全。
- 仅末组产生现有 INT32 fault。非末组超出 INT32 但仍处于 signed33 合法范围时继续累加，这是冻结语义。
- A5 的反馈相关路径是 II=1 的关键路径；功能正确不证明 100 MHz 物理收敛。
- 内部观测寄存器可能在综合中被裁剪；这不影响接口行为，但门级调试可见性不能据此保证。

