# down2_overlap_tile_runner v11 规格

## 契约

runner 的公开端口、调度、存储、两组 MAC、结果预留和整块 fault/export 语义与冻结
v10 相同。v11 只包含两项局部变化：实例化带一个 pre-round 弹性切分的
`road_postprocess_stream`；把六处紧凑 load-error `else` 展开为多行以恢复 formatter
控制流解析。第二项已证明全部非空白字符顺序完全相同。

接口包括：时钟/复位；SiLU table ready/valid 组；load kind/address/data ready/valid 组；
`i_start`、`i_pw_only`、`i_commit_ready`；busy/done/fault；export start/ready/valid、
INT8 data/index/done；单 debug event；preload/core/MAC/pre/SiLU/post/writeback/storage-wait/
scheduler-idle/export 周期计数；结果 queue/reservation/meta 观察；MAC result、三个 stage
accept 与 writeback 端点计数。所有位宽和方向保持冻结 v10 声明。

## 调度与容量

- 首个 MAC group 接收时预留完整结果项：`R <= 1`、`Q + R <= 2`。
- 末个 MAC group 与 postprocess 原子输入握手时，reservation 转成 queued result。
- DW channel 使用 `base=floor(channel/3)*3` 与 `lane=channel mod 3`；PW 使用
  `base=group*3` 与 mask `3'b111`。
- 256 个 DW writeback 全部完成并排空后才进入 PW；384 个 PW writeback 完成后 done。
- `i_commit_ready` 只反压内部 cache 提交；export 继续由 `i_output_ready` 控制。
- pre 接受观察现在表示 scalar 进入新增 cut；计数仍保持每 scalar 恰好一次。

## fault 与计数

`table_fault` 到 runner 调度与 MAC 的控制组合路径不做逻辑修改。任何 load/table/MAC/
postprocess fault 都阻止 whole-tile valid/export；不能用延迟 fatal 的办法修 timing。

MAC/pre/SiLU/post/writeback busy 周期可以重叠，不得相加为总延迟。storage-wait 和
scheduler-idle 按优先级互斥。端点计数只在实际握手递增。新增 cut 使成功作业的绝对
endpoint 可能较 v10 增加，必须从回归日志实测，不能由忙周期求和或预先编造。

## 验证义务

1. 冻结四 case 的 accumulator、pre、SiLU、post、writeback 全值比较。
2. full queue、reservation fence、同拍 consume/refill、长 `i_commit_ready=0`。
3. reset 覆盖 MAC/cut/round/SiLU/post/drain/export 的所有实际年龄。
4. 末组 fault 不发布整块；held reload 能让旧 token 排空后才装表。
5. v9 MAC、v9 serial、原 14/reset6、round7042、SiLU65536 新鲜回归。
6. 首轮布局布线复核七条原始内部路径；功能 PASS 不能替代物理 timing 证据。

WaveJSON：`waveforms/down2_overlap_tile_runner_timing_cut.json5`。

