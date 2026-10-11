# 双银行像素行缓存本地验证

- Python 周期模型自检通过。
- Icarus 共 80 项检查通过：背压、银行交替、双满停供、取消、错误和 tag 保留。
- 编译警告：0。
- 生产 RTL、冻结配置和架构文档在试验前后哈希一致。

证据边界：

- Single clock and two 129-pixel banks; testbench uses WIDTH=5.
- One-cycle synchronous read request plus held output register.
- No DDR controller, CDC, production top, CCL result, synthesis or timing evidence.
- Cancel is sampled as a level and new-task ownership remains a top-level duty.
