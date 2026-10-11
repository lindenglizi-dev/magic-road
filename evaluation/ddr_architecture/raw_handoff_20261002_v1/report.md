# 原始 run 银行同拍交接验证

- A 释放、B 完成与 B 释放、A 完成两种同拍交换均通过。
- 10 次同步读取逐项匹配独立的 y、run 数量、坐标和顺序。
- 双银行 full 后的额外 run 置位 raw_overrun/protocol_error，未破坏已提交银行；释放和 frame_clear 后恢复。
- run_valid 与 row_end 同拍被判非法；该暂存行未计入正常交接并由 frame_clear 丢弃。
- Icarus 检查 50 项，编译警告 1 条。
- 隔离 raw 表源码与生产保护文件在试验前后哈希一致。

证据边界：

- Isolated ccl_raw_run_table with MAX_RUN=64; no functional RTL edit.
- Single clock and synthetic run coordinates; no DDR or CDC model.
- run_valid plus row_end is flagged but temporarily stored by existing RTL; supervisory error discard is required.
- No synthesis, RAM inference, timing, complete CCL throughput or production integration evidence.
