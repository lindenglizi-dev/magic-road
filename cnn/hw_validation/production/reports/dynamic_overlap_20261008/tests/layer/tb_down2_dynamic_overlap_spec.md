# tb_down2_dynamic_overlap 验证契约

本测试是无外部端口的 Verilog-2001 仿真顶层，仅验证独立 `dynamic_overlap_20261008` 候选中的完整 `MAC -> DW cache -> PW -> dynamic postprocess` 小层。它不修改生产 RTL，也不代表 DDR、整网、物理时序、精度或部署 QAT 通过。

## 固定输入和覆盖

- 复用 `diagnostic_repair_20261008/layer/vectors` 的原三位置向量，以及 `layer/stress_bias_contract_host/vectors` 的非零偏置压力向量；运行器验证两组 manifest 中已有文件的 SHA256。
- 每组向量执行三位置无停顿、三位置确定性随机反压，以及一次结果停顿中的异步复位、完整 SiLU 表和层数据重载后重跑，共七例。
- 每例逐项检查 640 个 MAC accumulator、640 个 pre、640 个 SiLU、640 个 post、640 个唯一有序提交和 384 个 PW 导出。
- 保留调度任务口径：DW 384 个 MAC group、256 个后处理 batch；PW 256 个 MAC group、128 个后处理 batch。

## 新重叠观察口径

中间值不读取旧串行后处理 FSM 状态。pre/post 取双 `u_pre`/`u_post` 重定标结果握手，SiLU 取 `u_silu` 输出握手；内部 `{slot,lane}` 只用于索引 `reg_retire_tags[slot]`，不解释为外部 layer/position/channel tag。

每个 busy 周期只计入一个端点原因，优先级为：写回反压、结果容量等待、提交、有效 MAC 发射、输入/存储准备、任务关闭等待、流水排空、其他。其总和必须等于端点窗口。DW 与 PW 端点按 runner 的当前层标志逐拍拆分，并断言两者之和等于总端点。pre/SiLU/post busy 和接受次数另行统计，因为这些活动可互相重叠，禁止与互斥端点原因相加。

记录入口队列、退休记录和 SiLU 身份队列实际高水位，以及入口或预约因容量阻塞的周期。装表 1024 次、层预载次数和导出端点独立记录，不混入核心端点。无停顿新端点只与冻结旧证据 `20633` 周期比较，不能把旧值写成新候选计数。

## 完成和复位断言

- 输出 valid 等待 ready 时 data/tag 保持。
- done 时 runner reservation、入口队列、退休记录和 SiLU 身份队列均为空。
- 结果被长时间停顿后异步复位，旧 valid、busy、table-loaded 和队列状态立即取消；完整重装后不得出现旧 tag 或旧数据。
- 通过标记为 `TB_PASS_DOWN2_DYNAMIC_OVERLAP`；任何 `$fatal`、ModelSim `Error` 或 `Fatal` 均使运行器失败。

