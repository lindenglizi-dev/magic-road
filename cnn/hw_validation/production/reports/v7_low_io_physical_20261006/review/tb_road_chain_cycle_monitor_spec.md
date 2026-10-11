# `tb_road_chain_cycle_monitor` 规格

## 目的

该只读仿真监视器与冻结的 `tb_road_onchip_chain` 同时加载，通过层级观察冻结 DUT，不驱动任何 DUT 信号。它记录第一组基础用例从首个 MAC 输入握手到第十二个缓存响应消费的逐周期状态。

## 接口和边界

- 模块没有端口；时钟来自 `tb_road_onchip_chain.i_clk` 的层级观察。
- 起点是第一笔 `i_input_valid && o_input_ready`。
- 终点是第十二笔 `o_cache_result_valid && i_cache_result_ready`。
- CSV 包含状态、位置、通道、各阶段事件、提交阶段、缓存握手、缓存有效位和表装载状态。
- 监视器不修改冻结 RTL、原测试平台、数值、握手、复位或 II。

## 周期行为

见 `waveforms/tb_road_chain_cycle_monitor_base_window.json5`。窗口采用端点差；周期分解使用半开区间 `[start,end)`，避免起止端重复计数。

## 验证

- 仿真日志必须出现 `endpoint_difference=482 responses=12`。
- 原测试平台仍必须输出唯一的 `TB_PASS_CHAIN ... errors=0`。
- 监视器 CSV 只作为周期归因证据，不替代数值逐项对拍。
