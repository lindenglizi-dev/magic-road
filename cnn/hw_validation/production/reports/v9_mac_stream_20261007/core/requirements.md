# road_mac_probe II=1 候选需求

## 冻结接口与数值合同

- 模块名与端口保持参考 `road_mac_probe` 完全一致，不增加参数、状态口或调试口。
- 每个输入组包含 8 个 signed INT8 激活、三组各 8 个 signed INT8 权重、共享 lane mask、三路 signed INT32 bias、`first` 与 `last`。
- 每组形成三路 8 项点积，共 24 个乘法；24 组的完整序列因此含 192 个有效乘积。
- 乘积与归约宽度固定为 signed16 -> signed17 -> signed18 -> signed19；跨组累加器固定为 signed33；候选加法固定为 signed34。
- `first=1` 时该组以对齐后的 bias 符号扩展值替代历史累加值；`first=0` 时继续当时的 signed33 历史值。复位历史值为零。
- 只有末组候选检查 signed INT32 范围。任一路越界时 `fault=1` 且三路结果全部为零；故障末组不写回历史值。正常末组和正常非末组均写回 signed33 值。
- 上层保证一次 bias/first 建立到最终归约的 signed33 有限累计范围；本候选不增加新协议 fault，也不把 first=0 的无限历史继续声明为安全。

## 周期与握手合同

- A0 接受输入；A1 乘法；A2 两两和；A3 四项和；A4 八项点积；A5 候选累加。
- 非末组允许每周期接受一个输入组，即稳态组间 II=1。
- 接受 `last` 后关闭输入，直到该终态被 `o_result_valid && i_result_ready` 接受；不增加 FIFO、结果队列或多上下文。
- 无停顿时，接受 `last` 的上升沿到 `o_result_valid=1` 的上升沿间隔保持 9 周期。
- `o_result_valid=1 && i_result_ready=0` 时结果数据与 fault 保持稳定。
- 异步低有效复位立即取消流水和输出有效，清零状态，并保持旧核行为 `o_input_ready=1`。

## 成功判据

1. Python 周期模型覆盖连续组、空泡、first 替代、first0 继续、末组越界、背压和异步复位。
2. RTL 与冻结端口一致，连续输入组可逐拍握手，末组到 valid 为 9 周期。
3. ModelSim 功能回归通过后才冻结源码哈希；strict 原始报告完整保留，任何失败不放宽。

