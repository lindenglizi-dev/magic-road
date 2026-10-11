# v11 RTL semantic risk review

## 已改变

`road_postprocess_stream` 新增一个 1-entry elastic cut，payload 是完整
`{signed product[63:0], shift[5:0], tag[15:0]}`。`o_pre_accept` 从“直接送 round”改为
“进入 cut”。无停顿可见/写回端点由 `+23/+24` 变为 `+24/+25`。

## 未改变

- 所有公开端口、位宽、符号、固定系数、lane 规则和 tag 格式；
- 两个 round、SiLU、MAC 的源码与实例端口；
- 两项原子组 FIFO、reservation `R<=1` 与 `Q+R<=2`；
- metadata 仅在真实 SiLU input/output 握手 push/pop；
- sticky fatal、同拍 whole-tile 取消与 reset/full-reload 恢复；
- table fault 到 runner/MAC 的组合控制语义。

## 范围证明

- group FIFO 物理深度 2，计数只在 push/pop 不同拍时增减。
- pre inflight 新上限 10 = cut 1 + frozen pre round 9；4 位计数足够。
- SiLU metadata 实际上限 6；8-entry FIFO 与 3 位读写指针按模 8 自然回绕。
- post inflight 上限 9；4 位计数足够。
- reset/fault 分支把所有 occupancy 计数清零，优先于加减，因此不会回绕。
- metadata RAM 只以已写的 read pointer 读 tag：pop 需要 `cnt_meta != 0`，push 由真实
  SiLU input handshake 驱动；同拍 push/pop 在不同逻辑 token 上保持 FIFO 次序。
- frozen round 端口仍接收 64 位 product、6 位 shift、16 位 tag；没有隐式缩窄。

## parser 与静态门禁

六处紧凑 else 的非空白序列等价检查 PASS，原先的 `case_normalization_violation`
已消失。formatter 随后到达更深的既有 runner FSM 结构检查，并以
`state_machine_violation` 停止，因为冻结 runner 不是该工具要求的三进程 FSM。
本任务不把 runner 重写成三进程 FSM，也不放宽/豁免门禁；该失败与证据原样保留。

### v11 strict raw matrix

三个对象的 `compile` 均 PASS；`ast/readability/comment/naming/profile` 均 FAIL，
`testbench/toolchain` 在该静态命令中为 `not_requested`。raw error 数为：

| 对象 | v11 raw errors | v10 raw errors | v11 raw SHA-256 |
|---|---:|---:|---|
| stream | 720 | 669 | `d2cf49042766317b43d6fb2c818c46fa36be6bcd45b347fab0c048ac7829ff54` |
| runner | 1121 | 313 | `879b3caefdb32f864e71d4de2bff598299129a411352f6ef7712647570104e91` |
| full closure | 3773 | 1679 | `a593d3e08b5a9d7cf0b8682a2b4c5567198fed13ff4af1cc25e26ca4527c7111` |

v11 runner 已无 v10 的 `VG000 FORMATTER_AST_PARSE` 占位，因此新数目覆盖了更多真实节点；
不能用 raw 数量的增减推断功能质量，也不能与 v10 的占位数混算。
更早阶段的历史诊断标签“原计算链 374 / 原 38-bit 壳 667 / TB 219”继续保存在冻结
报告中；它们与 v11 扩展覆盖不可直接比较，本审查不据此宣称任何 gate PASS。

### priority 语义复核

- `VG122`：stream 的 queue/meta/pre/post 计数与 runner 的 endpoint/address 计数使用
  小宽度 `+/- 1'b1`。已证明运行上限分别为 Q2、pre10、meta6、post9；reset/fault
  优先清零。ModelSim 也观察到这些上限，无回绕。该规则仍是显式位宽 blocker，未豁免。
- `VG110/VG113/VG153`：metadata 和 runner data RAM 不逐项 reset。valid/count/load flag
  是读取屏障；metadata 只在真实 push 后可 pop，runner 数组只在完整 preload 后使用。
  未发现 read-before-write，但门禁仍 FAIL。
- `VG125/VG138`：显式较宽 literal 与 replication count/loop index 的 unsized 常量没有
  改变比较或索引值；这是保留的宽度/风格失败，不宣称 gate PASS。
- `VG097/VG132`：单文件检查缺冻结子模块/原语定义。完整 Icarus closure 和 ModelSim
  绑定均成功，但这些证据不把单文件诊断改成 PASS。
- `VG023/VG054/VG094/VG098/VG144`：runner 是冻结的一进程调度 FSM，不满足工具要求的
  三进程形态。四 case、reset/fault 回归证明当前状态轨迹，但本时序修复不承担 FSM 重构。
- `VG080/VG085/VG091/VG103/VG109/VG136/VG137`：runner 的循环临时变量、动态数组
  索引和多 lane 组合构造触发结构规则。它们与 v10 运算/寻址 token 相同；六处 runner
  编辑已由全文件非空白字符等价证明。没有从这些项发现新的 v11 语义 bug。
- `VG145/VG146/VG147`：这些是当前最重要的剩余实质风险。新增 cut 已把冻结 round
  从五条实测长锥后移，但 cut 的 D/enable、自身握手和 sticky-fault 控制仍超过静态
  三源/三操作预算，部分子模块锥还因外部实现或表达式解析而 inconclusive。这些项只能
  由后续架构拆分或真实物理证据关闭，本任务不以功能仿真豁免它们。
- header、comment、region、默认初始化、多 target always 与 formatter-template 项是明确的
  strict 交付失败；它们未被静默修复，因为全面格式/结构改写会超出本次独立 timing scope。

### 功能证据（与静态矩阵分开）

精确候选 hash 上的 ModelSim priority regression PASS：runner 四 case、640 个 MAC/pre/
SiLU/post/writeback 端点；stream 无停顿 `24/25`、reset age 1..25、partial/held reload、
fault、随机与长反压，并显式断言 cut 满停顿时 product/shift/tag/valid 全部保持。
观测最大值为 Q2/pre10/meta6/post9/obligations30。该 PASS 不改变上述 strict FAIL 状态。

## 尚待物理证明

单个 product cut 在结构上切断五条 mux/multiply/abs 路径，但只有新的布局布线报告
能证明 setup/hold 收敛。两条 `table_fault` 高 net-delay 路径未做逻辑修复；必须检查
首个候选的实际结果，再决定是否存在保持同拍 fatal 语义的最小等价修复。

