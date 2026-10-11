# RoadYOLO v5 执行范围与阶段条件

日期为 2026-10-05，任务为用户要求的 v5 全部七项。当前工程不是 Git 仓库，没有可提交或推送的分支。本批使用独立目录及文件所有权隔离。

## 实施与成功条件

V5-01 核对五套诊断、源码、工具和配置，保存 manifest；所有未知证据单列，不从报告数量推测独立缺陷数量。V5-02/03 只在已有工程 checker_overlay 内修正端口事实、切片、测试台和规格表达能力；原生 formatter 仍是唯一语法来源，正例与真实负例都需验证。

V5-04 固定规格、外部接口和两份 RTL，运行已安装旧 checker 与项目新 checker 的四组完整严格门，逐条保留变化和剩余阻塞。真实控制预算不能靠别名隐藏，涉及行为的改动必须另立候选，不能混进原版和最小 CEA 候选的因果对照。

V5-05 当前 DUT 与测试台均未改动时允许复用哈希匹配的 v4 官方功能模型结果；复用与新跑分别标识。核对 1 ns 刺激等待、10 ns 时钟、采样沿，以及 3073 次失败和最终 3072 次记录。

V5-06 只有严格准入通过才启动独立 SiLU TD 实现；用户要求执行全部任务不意味着放宽文件规定的准入条件。未获单独批准的带阻塞诊断实现不执行。V5-07 依赖本次 SiLU 实际 STA，不能拿旧 round 裕量做优化依据。若这些依赖不满足，明确报告未执行和需要关闭的具体问题。

## 文件所有权与工具

协调者负责本目录的证据核查、四组门和最终报告。verify 代理独占 checker_overlay 修正及 v5_checker_adapter_20261005 报告；review 代理只读审查控制、位宽和刺激时序，在 v5_remaining_review_20261005 写报告。两代理按工程指定 gpt-5.6-sol/high，不改生产 DUT。

任务分类为 analyze、validate 及项目检查器 repair。公开门仍为 compile、ast、readability、comment、naming、profile、testbench、toolchain；无外部工具执行时不声称物理通过。按 readable-verilog-generator 保留阻塞语义，使用 ponytail 最小修正；本地工程文档按 write-page 写作要求沿用既有 Markdown 交付，不创建云 Page。

静态依赖预检已新跑，未配置远程、未找到 Vivado/xsim；PH1P 验证沿用已批准的本地官方 ModelSim 路线。Python/script 专用 readable 技能不可用，因此机械证据脚本用标准库及断言，不宣称它们的专用严格门通过。全局技能、生产 RTL、训练和 Flash 均保持不变。
