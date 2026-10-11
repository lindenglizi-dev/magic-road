# DW 四 credit 任务重叠测试说明

日期：2026-10-09。DUT 为同目录上级 `rtl/` 的八份候选源码；本文件只定义
`tb_down2_dynamic_overlap.v` 的验证契约，不改变 DUT 外部端口、算术、II、量化、
复位或故障语义。

## 成功条件

- 原 case 0..9 不改编号和内容。每个完整场景继续逐项检查 MAC、pre、SiLU、post、
  commit 各 640 个值，要求 DW 384 组、DW 256 标量、PW 256 组、PW 128 batch，
  最后导出 384 字节；随机气泡、PW 长提交反压、复位与 PW 原子故障继续回归。
- case 10..14 分别在 DW issuer first、issuer last、active、active 后处理阻塞、
  四 credit 满时异步复位。每次复位后重新装满 1024 项 SiLU 表和全部输入/参数，
  再运行一个完整块；原全量数值、唯一 tag 和导出 scoreboard 同时证明无旧结果泄漏。
- case 15 对 DW 提交端施加 256 拍长反压并完整排空。所有完整场景均要求 128 次
  descriptor first/last/result 对齐、256 次 active 标量接受，descriptor 高水位为 4，
  覆盖满环 first/result-pop 同拍和 active 末标量/新 result-pop 同拍替换。
- 两个独立 DW 故障场景分别令首任务和较晚任务末组发生 INT32 溢出，并要求故障
  到达前至少一个年轻任务已接受。第二场景保持 `commit_ready=1`，使 fault pop 与旧
  active、已有 PP valid 同拍；该拍必须同时禁止 PP accept、commit accept 和 DW cache
  写使能，且跨边沿核对 DW 写计数不增。故障结果必须三路
  原子清零；故障任务和年轻任务不得进入后处理或发布。

## 层级可观察接口

shared descriptor ring 使用 `cnt_pw_meta`、`reg_pw_task_meta[0:3]` 和原读写指针；
其 push/pop 分别必须等于 `flag_dw_first_accept`/`flag_dw_result_accept`，并逐拍等于
MAC 核 `cnt_reserved`。`flag_result_reserved` 仅表示 DW active-valid，
`reg_dw_active_meta={position[3:0],channel[4:0]}` 保存退休身份。active 未接受时，
身份、96 位结果和 lane 不变；后处理 valid 等 ready 时，结果、mask、位置、通道和
参数基址不变。active 最后一标量与新结果同拍时，新结果覆盖 active，valid 不降拍。

TRACE 原 42 列及顺序保持不变，只在尾部增加 `active_valid` 和
`task_meta_count`。周期只作候选实测，不要求等于冻结基线 DW 2015、PW 592、总 2607。

## 复位与边界

复位异步清除 busy、输出 valid、active、descriptor ring、MAC reserved/result；释放后
仍须按原顺序重装表和全部运行参数。DW 转 PW 前要求 256 次 DW 最终提交，且 active、
descriptor、MAC 结果/预留和后处理队列均排空。DONE 同样不得留下任何所有权。
故障只清 active/busy/tile-valid，不软复用已接受的年轻 descriptor/MAC credit；TB 要求
这些所有权在 fault 状态保持，且只有公共复位将其归零。

```json
{signal:[
  {name:'clk',wave:'p...........'},
  {name:'dw_first_accept',wave:'010.........'},
  {name:'task_meta_count',wave:'x3.4...3....',data:'0 1 2 1'},
  {name:'dw_result_accept',wave:'0.....10....'},
  {name:'active_valid',wave:'0.....1..0..'},
  {name:'dw_post_accept',wave:'0.......10..'},
  {name:'rstn',wave:'1..........0'}
]}
```

通过边界仅限冻结小块的数值、所有权、握手、取消和导出一致性；不证明真实模型参数、
DDR 整网、物理时序、板级视频或 5 FPS。ModelSim 与 TD 由协调代理单独执行并留证。
