# 首次分析器失败与局部修正

首版 analyze.py 对所有 CSV 列直接 int()，遇到 `commit_valid=0` 时未初始化的
`commit_tag=x` 而失败。原仿真四套均已通过；这是测量解析器把无效 payload
误当有效数据的问题，不是算术或有效输出 X。

第一次局部修正只处理 commit_tag，第二次运行又检查出 PW 未有结果时
`pp_valid=0` 的 `pp_position/pp_channel=x`。两次均停在分析阶段，没有生成通过结论。

最终仅允许 commit_tag 在 commit_valid=0，以及 pp_position/pp_channel 在
pp_valid=0 时保留为 None。任何其他未知数，包括 valid=1 的 payload，仍断言失败。
原始 CSV 不修改，未把 X 静默改成 0。
