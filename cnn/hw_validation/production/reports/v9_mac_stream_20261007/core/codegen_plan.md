# road_mac_probe II=1 代码生成计划

1. 复用参考核的显式 24 路 signed8 乘法和 16 -> 17 -> 18 -> 19 位寄存归约树。
2. 删除“输入接受时快照历史累加值”的依赖；将 `first/last/valid/bias` 随点积逐级对齐。
3. 在 A5 用当拍 signed33 累加器或对齐 bias 加点积，形成真实 signed34 候选并写回 signed33。
4. 对末组锁存三路候选和 INT32 越界，增加纯对齐寄存器，使外部 valid 仍在 A9 出现。
5. `last` 接受后置占用，终态握手后释放；不加入 FIFO、job id 或旁路接口。
6. 先运行 Python 自检，再做 RTL 编译/仿真、strict gate 和语义风险分类。

