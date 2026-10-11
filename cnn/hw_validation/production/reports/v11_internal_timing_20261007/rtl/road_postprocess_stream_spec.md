# road_postprocess_stream 时序切分规格

## 目标与边界

本模块在冻结 v10 数值链的第一颗 `road_round_shift` 前增加一个深度为 1 的
弹性切分，切断 `lane mux -> fixed multiply -> round abs` 的物理长路径。
两个 `road_round_shift`、`silu_shared_unit` 的源码、端口和数值行为均不改变。

## 接口

所有公开端口与 v10 相同：

- 时钟/复位：`i_clk`、异步低有效 `i_rstn`。
- SiLU 表：`i_table_valid[0:0]`、`i_table_addr[9:0]`、
  `i_table_data[15:0]`、`o_table_ready`、`o_table_loaded`、`o_table_fault`。
- 原子结果输入：`i_input_valid`、`i_result_data[95:0]`、`i_result_fault`、
  `i_layer`、`i_position[3:0]`、`i_channel_base[4:0]`、`i_lane_mask[2:0]`、
  `o_input_ready`。
- 标量输出：`i_output_ready`、`o_output_valid`、有符号 `o_output_data[7:0]`、
  `o_output_tag[15:0]`。
- 状态/观察：`o_fault`、`o_result_queue_count[1:0]`、`o_meta_count[3:0]`、
  `o_pre_busy`、`o_silu_busy`、`o_post_busy`、`o_pre_accept`、
  `o_silu_accept`、`o_post_accept`。

## 数值与元数据

- `i_result_data` 依次保存 alpha、beta、gamma 三个有符号 32 位结果。
- lane 0/1/2 的固定 pre 系数为 1/3/5，shift 为 0/2/4。
- post 系数为 1，shift 为 4；最终做 INT8 饱和。
- 16 位 tag 为 `{layer, position[3:0], channel[4:0], 6'b0}`。
- DW 只消费 one-hot mask 选中的 lane；PW 消费三 lane。channel base 必须按 3 对齐。
- 新寄存器保存完整的有符号 64 位乘积、6 位 shift 和 16 位 tag，不做截断或重算。

## 弹性握手

定义：

```text
cut_ready  = !cut_valid || pre_round_advance
pre_accept = scalar_valid && cut_ready
```

`o_pre_accept` 表示 scalar 已进入 cut，而不是已经进入 round。cut 为空时可以接收；
cut 满且 round 停顿时必须保持 product/shift/tag/valid；cut 满且 round 前进时，同一边沿
旧 token 进入 round，新 scalar 补入 cut，维持 II=1。组 mask 仅在 `pre_accept` 时清除。

`cnt_pre_inflight` 在 `pre_accept` 加一，在 pre-result 被 SiLU 接收时减一，因此同时覆盖
cut 与九级 pre round。`o_pre_busy` 与 table global-empty 由该计数得到，无需新增接口。

## 延迟、容量与 reload

- 无停顿时，scalar 在边沿 `t` 被 `o_pre_accept` 接收；输出在 `t+24` 的 NBA 后可见，
  首个 ready/valid 写回边沿为 `t+25`。
- scalar II 保持 1。
- pre 结构上限从 9 增为 10；meta 上限 6，post 上限 9，原子组 FIFO 深度 2。
- scalar obligation 的结构安全上限为 31；Python 定向压力模型观察到 empty-window 30、
  existing-tail 22，不能把 31 写成已观测值。
- held reload 只阻止新原子组 admission；已接收的 group/cut/round token 继续排空。
  `cnt_pre_inflight==0` 后 global-empty 才允许表写入。

## reset 与 fault

异步低复位清空 cut payload/valid、队列和计数。任一既有 sticky fault event 在同一边沿
清 cut valid/payload；公开输入与输出随后被阻断，直到外部 reset 并重新完整装表。
故障当拍之前已写入 runner cache 的数据仍属于未发布事务，整块不得导出。
本版不寄存、不延迟 `table_fault`，不改变 fatal 可见性和取消语义。

## 验证义务

1. lane 0/1/2 固定系数和 tag 对齐；完整数值与 v10/reference 一致。
2. cut 空接收、满停顿保持、消费补入、组 FIFO 同拍 push/pop。
3. 连续、气泡、随机 ready、empty/tail 长反压；检查 Q、pre、meta、post 上限。
4. 逐个实际 pipeline age reset，reset 后无旧 tag/value，重新装表前不 ready。
5. partial/held reload、末组 atomic fault、表 fault；故障后无可见输出。
6. 无停顿 `+24` visible、`+25` write，且连续 scalar II=1。

WaveJSON：`waveforms/road_postprocess_stream_elastic_cut.json5`。

