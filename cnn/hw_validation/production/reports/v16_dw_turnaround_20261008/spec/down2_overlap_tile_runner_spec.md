# down2_overlap_tile_runner DW 三空间点与控制时序规格

## 契约

本候选只改变 DW 调度和内部 metadata 适配。`road_mac_probe`、
`road_postprocess_stream`、round、SiLU 的公开接口、定点位宽、舍入、饱和、复位和
fault 协议保持 v12 冻结版本。PW 调度和 v12 单 cache 写口保持不变。

## 端口

| 分组 | 输入 | 输出 |
|---|---|---|
| 时钟复位 | `i_clk`、低有效异步复位 `i_rstn` | - |
| SiLU 表 | `i_table_valid[0:0]`、`i_table_addr[9:0]`、`i_table_data[15:0]` | `o_table_ready`、`o_table_loaded`、`o_table_fault` |
| 预装载 | `i_load_valid`、`i_load_kind[2:0]`、`i_load_addr[10:0]`、`i_load_data[31:0]` | `o_load_ready` |
| 作业控制 | `i_start`、`i_pw_only`、`i_commit_ready` | `o_busy`、`o_done`、`o_fault` |
| 导出 | `i_export_start`、`i_output_ready` | `o_output_valid`、`o_output_data[7:0]`、`o_output_index[8:0]`、`o_export_done` |
| debug | - | `o_debug_valid`、`o_debug_phase[1:0]`、`o_debug_layer`、`o_debug_position[3:0]`、`o_debug_channel[4:0]`、`o_debug_value[31:0]` |
| 周期计数 | - | `o_preload_writes`、`o_core_cycles`、`o_mac_cycles`、`o_pre_cycles`、`o_silu_cycles`、`o_post_cycles`、`o_writeback_cycles`、`o_storage_wait_cycles`、`o_scheduler_idle_cycles`、`o_export_cycles`，均为 32 位 |
| 流水观察 | - | `o_result_queue_count[1:0]`、`o_result_reserved`、`o_meta_count[3:0]`、`o_mac_result_count`、`o_pre_accept_count`、`o_silu_accept_count`、`o_post_accept_count`、`o_writeback_count` |

所有数据端口沿用原 signed 声明；表地址、load 地址、tag 和计数保持 unsigned。

## DW 三空间点调度

- 输出位置按 anchor `0,3,4,7,8,11,12,15` 调度。每行 `x=0` 是三点组，
  `x=3` 是尾一点组；每个 anchor 依次处理逻辑通道 `0..15`，共 128 个 DW task。
- 每个 task 固定发送三拍 MAC：union21 分成 `8/8/5`，末拍 lane mask 为
  `8'h1f`。尾一点组也保持三拍，不使用另一套 G2 优化。
- 三个 MAC 输出 lane 表示同一逻辑通道的 `x、x+1、x+2`。尾一点组只有 lane0
  有效；lane1/2 的 weight 和 bias 必须为零。
- halo 行列先分别计算。尾一点 anchor 的物理列 `9..12` 必须显式填零，不能把
  线性地址绕到下一行；输入 mask 仍按 union21 的 `8/8/5` 发送。
- 三个 lane 共用 `reg_dw_bias[channel]`，偏置只由 MAC 的 first 拍加入一次。

## post metadata 适配

MAC 的 96 位结果先整体捕获。任一路 MAC INT32 越界时不向 post 发送任何 scalar，
并取消整个 triplet。正常结果在 `ST_DW_POST` 中逐路送入冻结 post 接口：

- `logical_lane = channel mod 3`，使用原枚举逻辑，不引入通用除法器；
- 被选空间结果搬到 post 的 `logical_lane` 数据槽；
- `lane_mask = 3'b001 << logical_lane`；
- `channel_base = channel - logical_lane`；
- `position = anchor + spatial_lane`。

因此 pre 系数由逻辑通道 `channel mod 3` 选择，而不是由 MAC 的空间 lane 选择。
只有最后一个有效 scalar 与 post 握手后，调度器才推进 channel/anchor。ready 拉低时
结果、position、channel base、mask、reservation 和空间 lane 必须保持。

PW 继续每 task 两拍 MAC、一次三通道 post 输入，行为不变。

## 计数与完成

- full tile：DW 为 128 个 MAC result、384 个 accepted MAC beat、256 个 post scalar；
  PW 为 128 个 MAC result、256 个 accepted MAC beat、384 个 post scalar。
- `o_mac_result_count` 按 MAC triplet 计数，不按 DW scalar 计数。
- `ST_STORAGE`、`ST_MAC_SEND`、`ST_MAC_WAIT` 和 `ST_DW_POST` 都计入
  `o_mac_cycles`；总 core 周期仍由 busy 逐拍计数。
- 256 个 DW cache commit 完成后才能进入 PW；384 个 PW commit 完成后 done。

## reset、背压与 fault

- 异步复位清除已捕获 triplet、空间 lane、reservation 和所有可见 valid；复位后
  不得出现 ghost post/debug/export 事件。
- `i_commit_ready` 继续反压 commit；post 输入 ready 反压时 `ST_DW_POST` 不推进。
- load/table/post fault 继续进入整块 fault；MAC 任一空间 lane 的正/负 INT32 越界
  必须使整个 triplet 零 post、零 commit、不可 export。
- 不对不可达的任意 X/Z metadata 声称等价；回归证明所有可达 DW tag 已知、
  channel `0..15`、完整 cache 地址 `0..255`。

## 验证义务

1. 三套冻结 4x4/s2/9x9 halo 向量逐项比较 accumulator、pre、SiLU、post 和最终 384 个输出。
2. 每套必须观察 128/384/256 的 DW task/beat/scalar 计数、末 mask `8'h1f` 和 256 个唯一写地址。
3. 尾一点所有越界 halo 读取为零，失效 lane weight/bias 为零。
4. DW post 的 lane0/1/2 分别承受至少 64 拍 ready 背压并保持 payload/metadata；在该状态复位后检查 ghost 窗口。
5. 用真实激活、权重和偏置制造仅空间 lane1 或 lane2 的正/负 INT32 越界，检查整组三路原子取消；合法极值不得误报。
6. PW-only、随机 commit 背压、cache 单写口、table-valid、X/Z directional 与 export 背压回归保持通过。

周期图：`waveforms/down2_overlap_tile_runner_triplet.json5`；渲染图：
`waveforms/down2_overlap_tile_runner_triplet.svg`。图中省略 MAC 固定流水延迟，只表达三拍输入、
原子捕获和逐 scalar post 握手的顺序。

## v14 控制时序重构

本候选仅重写两个组合/写口表达，不增加状态、寄存 fault 或改变可见周期：

1. `flag_can_reserve` 在二值合法状态下直接使用 `result_reserved` 和
   `pp_result_queue_count`，不再先计算二位加法 `capacity_used`。条件表达仍在同一拍直接包含
   `pp_fault`；fault 拉高时首组 `mac_valid`/`mac_accept` 立即取消。ternary 的未知分支保留
   v13 对 `reserved=X/Z` 的四态传播，不能把 queue 满时的未知静默变成零。
2. halo load 的合法条件形成唯一 `flag_halo_load_write`。`reg_halo` 只有一个独立时序写块；
   reset 分支不写、不复位数组。原 metadata 块仍对合法地址更新 expected/loaded，对非法顺序、
   X 地址或未知条件置 load fault，且不得写 RAM。

两个变化均保持 load ready、MAC 接口、II、即时 fault、复位、数值和固定系数不变。
独立写块是 `reg_halo` 的唯一 driver；其余 cache、weight、bias 和 metadata driver 不移动。

## v14 验证结果

- 四态穷举：`reserved`、queue 两位、fault 和 ready 各取 `0/1/X/Z`，共 1024 组；
  首组/后续组的 `can_reserve`、`mac_valid`、`mac_accept` 共 2048 条路径与 v13 表达一致。
- halo 写控制：合法地址单次写；非法顺序、X 地址、reset 均不写，前两者保持 fault。
- 原三套 full case 均保持 core 4281 周期，PW-only 保持 1822 周期；DW 128 task、
  384 MAC beat、256 scalar、64 tail scalar 和状态互斥计数不变。
- 原 X/Z directional、64 拍三 lane 背压、DW_POST reset、单空间 lane 正负溢出原子取消、
  合法边界、table-valid 和随机 commit 背压继续通过。

控制周期图：`waveforms/down2_overlap_tile_runner_control_timing.json5`；其 SVG 为
`waveforms/down2_overlap_tile_runner_control_timing.svg`。图中 fault 路径没有新增寄存级，
halo RAM 只在 `load_accept && kind0 && address_valid` 的采样沿写一次。

## v15 输出计数器时序重构

`cnt_output[4:0]` 保持五位宽度，只由一个异步低有效复位时序块驱动。原状态机中的
clear/increment 条件按原 `case`、嵌套 `if/else` 顺序提取为组合事件：

- IDLE 接受 start 时 clear；
- PW 的 `ST_MAC_WAIT` 在无 MAC fault 的 accepted result 上按原输出/位置边界
  increment 或 clear；
- DW 的 `ST_DW_POST` 只在最后一个有效 scalar 握手时按原输出/位置边界推进；
- `ST_DW_DRAIN` 在第 256 次写完成时 clear。

计数时序块最外层继续使用原 `if (pp_fault || flag_load_fault)` 空分支，因此已知 fault
同拍保持计数；fault 为 X/Z 时仍遵循 Verilog procedural-if 的原四态规则，不把未知改写为
已知 hold。事件优先级固定为 fault hold、clear、increment、hold。未移除 shared fault guard，
未缩窄计数器，也未改变 post、MAC、接口、II、即时 fault、reset 或数值行为。

## v15 验证结果

- 冻结 RTL 哈希：`0bb56663084965708befaa2f69d282e6e445b075d81d86623e4c1f086d4856a3`；
  `rtl/` 与回归副本一致。
- 计数转移检查覆盖 16 个 state、32 个五位计数值、16 个 position 及各状态相关二值控制，
  共 16896 组；另覆盖 24 个 X/Z 边界，包括 DRAIN 的 256 写同拍 clear 与
  `pp_fault`/`load_fault=1/X/Z`，全部与 v14 原 procedural hierarchy 一致。
- root 独立 `iverilog -g2001` compile exit 0、`vvp` exit 0；原 4 cases 保持通过，
  full DW core 4281 周期、PW-only 1822 周期，三 lane 64 拍背压、DW_POST reset、
  single-lane 正负溢出原子取消及 X/Z directional 检查保持通过。

计数周期图：`waveforms/down2_overlap_tile_runner_counter_timing.json5`；渲染图：
`waveforms/down2_overlap_tile_runner_counter_timing.svg`。图中 `clear`/`increment` 是同拍组合事件，
`fault=1` 的拍即使产生 increment 事件，时序块仍按原优先级保持计数。

## v16 DW 周转优化

本候选只把 runner 的 DW `flag_pp_input_valid` 队列门限从
`pp_result_queue_count < 1` 放宽到 `< 2`。`road_postprocess_stream` 原生两槽队列、
`o_input_ready`、算术、post 源码、状态、接口、II、数值、即时 fault、reset 和约束均不变。
PW 分支不使用该门限，行为保持 v15。

G3 triplet 的三个 scalar 在 post 无阻塞时连续三拍握手：

1. MAC result ACK 后第 1 拍，lane0 入空队列；
2. 第 2 拍，post 同时弹出 lane0 并压入 lane1，队列占用仍为 1；
3. 第 3 拍，同样弹出 lane1并压入 lane2，最后 scalar 握手后推进任务；
4. 第 4 拍 `ST_STORAGE` 锁存下一任务首组；
5. 第 5 拍下一任务 G0 握手。

因此代表性 G3 的 ACK→下一首组由 7 拍变为 5 拍，`ST_DW_POST` 由每任务
5 拍变为 3 拍。64 个 G3 task 共消除 128 个 queue wait；G1 task、三组 MAC、
固定 MAC 等待和 PW 周转不变。无阻塞 full case 的 core 从 4281 降到 4153；
随机 commit 背压 case 实测 4154，不能统一声称所有 case 都是 4153。

## 两槽与原子性不变量

- post queue 自身容量为 2；占用为 2 时 `o_input_ready=0`，runner 不产生 accept。
- `flag_result_reserved` 表示独立的 raw triplet buffer，不是第三个 post queue slot。
  raw result、spatial lane、position、channel base 和 mask 保持到对应 scalar accept；
  最后 scalar accept 后才释放 reservation。
- queue 为 1 时允许 post 同拍 pop 与 runner push；已有 queue `2'b11` 分支保存新 head，
  不覆盖未消费 tail。若下游阻塞，第二次 push 可使 queue 达到 2，随后停住。
- MAC fault 仍在进入 `ST_DW_POST` 前整组取消；post fault 清空 queue/inflight 并以 fatal
  抑制输出。任何单 lane fault 不得产生 scalar commit 或 export。
- DW→PW 仍由 `ST_DW_DRAIN` 等待 256 次 DW cache commit；本优化不提前读取未写完 cache，
  也不预装载下一任务或引入跨任务 MAC 重叠。
- 未知 queue count 或 ready 只能产生 0/X 的 accept 表达；procedural `if` 不得把 X/Z
  当作一次消费。reset 在任一 DW spatial lane 或 queue 满时都清空 queue/raw reservation，
  复位后不得出现 ghost debug/output/done。

## v16 验证义务与结果

- `reference/queue_contract.py` 的最小队列模型覆盖连续三 scalar、64 拍停顿、交替 ready
  和 10 个取消场景；这是调度参考，不替代 RTL 仿真。
- RTL 四态门限检查覆盖 queue 两位与 ready 的 64 组组合，其中 48 组含未知 queue bit，
  未观察到 unknown procedural consume。
- 定向填满两个 post slot 后，64 拍 commit 背压期间 queue 保持 2、无新 accept，raw triplet
  与 lane/tag/mask/reservation 保持；queue 满复位后无 ghost。
- lane0/1/2 分别进行 64 拍 payload 保持并在该 lane 独立 reset；正常流观察到 384 次
  simultaneous push/pop。DW_POST 的 accept、queue-full 和 ready-wait 三类逐拍互斥且覆盖状态总数。
- 三套 full case 保持 384 DW MAC beat、128 result、256 scalar、64 tail scalar、256 个唯一
  cache 写地址以及 accumulator/pre/SiLU/post/final 逐项黄金一致；PW-only 保持 1822 周期。
- v15 的 16896 个 counter 已知转移、24 个 X/Z 边界、halo/cache/table/X/Z、随机 commit、
  三 lane 背压、真实 single-lane 正负溢出原子取消和合法极值测试均保留。

周转周期图：`waveforms/down2_overlap_tile_runner_dw_turnaround.json5`；渲染图：
`waveforms/down2_overlap_tile_runner_dw_turnaround.svg`。图中 queue 值表示采样沿后的占用；
lane1/lane2 的 accept 与上一 scalar 的 pop 同拍，所以占用保持为 1。
