# V5 工程检查器适配验证

主端从最终冻结快照独立执行：16 项测试均通过；生产 RTL 和预算阈值未改。实际命令、测试文件哈希、stdout/stderr 保存于 `main_adapter_recheck.json/.log`。

## 最小污染复现

`cea_dependency_probe.v` 使用 `flag_enable = i_left | i_right` 接不透明 RAM 的 CEA 输入。`reproduce_cea_ownership.py` 分别在独立进程加载旧/新 checker。`cea_minimal_reproduction.json` 实际证明：旧 checker 为中间使能添加 unknown producer；新 checker 只保留本地驱动；RAM 输出两版都保持内部实现未知。这不是仅用父 input 端口正例推测根因。

## 16 项正式测试

| 类别 | 已测试结果与边界 |
|---|---|
| typed input/output | input sink 不污染，output 保持 opaque unknown |
| 真实反馈 | 保持 unknown；没有假称已证明无环 |
| 两个输出驱动同一 actual | 两个 producer 保留，不伪称单驱动 |
| 输出接父 input | 仍记录 unknown producer，方向冲突未被省略；未声称独立方向规则已全部闭包 |
| 位宽不符 | 8 位 output 接 4 位 actual，VG097 failed |
| inout | ownership unresolved，不放行 |
| 缺接口 | missing implementation unknown，不放行 |
| bare zero-port module | 原生 formatter 识别空端口模块，无假端口 |
| `always #5` | 原生 AST 保留周期延迟；生产 VG131 仍 failed |
| malformed delay | 仍有 error，不转成 pass |
| signed 10 位切片 | VG085 检查宽度通过；不据此推断 signed 算术完全正确 |
| 真 11 对 10 位切片 | VG085 failed，selector 没有丢失 |
| 参数 `WIDTH-1:0` 切片 | 已有 formatter 常量/位宽事实求值后通过 |
| 未知参数切片 | VG085 inconclusive |
| 参数端口绑定 | WIDTH=10 接 10 位通过，接 9 位失败 |
| 整向量及符号扩展 | 同宽整向量 ==/!= 通过；显式扩展通过原生 AST 解析。真宽度负例见切片/实例绑定行，不宣称扩展数值仿真已完成 |

另有 15 项零端口规格正负例，通过实际规格生成入口生成了 WaveDrom SVG。相关 fixture 仅供检查器测试，不是待发布 RTL，也不代表其注释/命名/物理门通过。

## 补丁与未闭合边界

`v5_only_adapter.patch` 是相对 pre-change overlay 的本轮差分；`project_adapter.patch` 是整个项目 overlay 对安装源的累计差分，两者不能混为本轮修改量。已有 liveness/structure 两模块本轮未改。`adapter_sources.json` 记录逐文件初始、安装源、最终哈希；当前活动 overlay 与冻结的 11 文件一致。

bare header 规范化委托安装 formatter；简单 periodic delay 的 header 拆分和渲染补充不改变生产禁止延迟规则。没有新增 Verilog parser。此处没有覆盖全部延迟控制语法、所有复杂参数或任意 signed 表达式；超出已有事实能力时不能声称通过。

最终两份 SiLU 静态门仍为 167 errors，真实控制预算、RAM output unknown、未解析存储/拼接、部分位宽与格式问题保持阻塞。上述适配不是物理准入豁免。

协作验证任务最后因通信流中断未交付其独立终稿；主端已接管并独立完成冻结、16 项测试、两操作数最小复现、四组完整门、补丁及来源核查。本文件不将通信中断当作 RTL 失败，也不假称取得不存在的代理报告。
