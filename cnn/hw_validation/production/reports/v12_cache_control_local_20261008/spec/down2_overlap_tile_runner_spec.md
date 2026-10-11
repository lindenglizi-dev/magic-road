# down2_overlap_tile_runner v12 cache-control-local 规格

## 契约

runner 的公开端口、调度、存储、两组 MAC、结果预留和整块 fault/export 语义与冻结
v11 ack-local 候选相同。当前候选只把 `reg_dw_cache` 的 preload/commit 两个互斥写点
收敛成一个物理写口；不增加寄存级，不改 ready/fault、计算周期或 postprocess。

接口包括：时钟/复位；SiLU table ready/valid 组；load kind/address/data ready/valid 组；
`i_start`、`i_pw_only`、`i_commit_ready`；busy/done/fault；export start/ready/valid、
INT8 data/index/done；单 debug event；preload/core/MAC/pre/SiLU/post/writeback/storage-wait/
scheduler-idle/export 周期计数；结果 queue/reservation/meta 观察；MAC result、三个 stage
accept 与 writeback 端点计数。所有位宽和方向保持冻结 v10 声明。

## 调度与容量

- 首个 MAC group 接收时预留完整结果项：`R <= 1`、`Q + R <= 2`。
- 末个 MAC group 与 postprocess 原子输入握手时，reservation 转成 queued result。
- `ST_MAC_WAIT` 内 child table-valid 恒为 0；局部 ready 为
  `reserved && Q<2 && table_loaded && !fault`，MAC ready 与接受事件共用该项。
- `reg_dw_cache` 的 IDLE preload 与计算期 commit 保持原互斥协议，并收敛到单一写口；若异常同拍，commit 保持原来后赋值优先。
- preload 先在完整 11 位地址上检查 `0..255` 和原 expected/restart 条件；commit 先在完整 9 位地址上检查 `0..255`。只有检查通过才选择 8 位物理地址，无效 preload 只置 fault、不写缓存。
- 可达 DW commit 元数据必须为已知值，channel 为 `0..15`。旧 `if(tag[15]) ... else ...` 与新写使能不对任意 X/Z 内部 tag 声称等价；回归须证明所有实际 commit tag 已知。
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
7. 父级 table-valid 在 `ST_MAC_WAIT` 拉高时，结果仍仅接受一次；X/Z 差异单列诊断。
8. 每拍比较旧双写点和新单写口的 enable、完整 address 与 data；覆盖同拍 commit 优先、invalid/X 地址、reset 禁写和 IDLE table fault。

WaveJSON：`waveforms/down2_overlap_tile_runner_cache_write.json5`。
渲染图：`waveforms/down2_overlap_tile_runner_cache_write.svg`。竖线省略两段接口间的计算间隔，不表示装载下一拍即完成 DW；本轮不改变原握手延迟。
