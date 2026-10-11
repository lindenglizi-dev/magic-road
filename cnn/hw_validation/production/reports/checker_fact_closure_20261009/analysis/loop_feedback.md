# VG136 for 归纳变量事实修正

## 原始复现

旧 `vg_structure_rules.py::_comb_no_feedback` 从 formatter 已确认的 module 文本再次用正则扫描 `always @(*)`。扫描把 `for` header 的更新子句当成普通阻塞赋值，因此形成两条伪自边：

- `road_dynamic_postprocess.v`：`check_lane = check_lane + 1`，VG136 evidence 为 `check_lane`。
- `down2_dynamic_tile_runner.v`：`lane_index = lane_index + 1`，VG136 evidence 为 `lane_index`。

同一旧规则对普通 `integer i; i = i + 1;`、普通信号自反馈及两节点环均失败，证明不能按声明类型或变量名整体豁免。

## 最小修正

新 overlay 只接管 VG136，VG104/VG130/VG145 继续逐次委托已安装的原模块。VG136 保留原依赖图和原环检测，仅用 formatter 控制树确认 `kind == "loop"` 的静态规范归纳变量，然后删除该 `for` 更新产生的单条自边。

自边只有同时满足以下条件才删除：

1. formatter 声明事实明确为 `integer`；初始化、比较界限和步长都是可解析的十进制常数，且位于 signed32 范围；
2. 比较只接受 `i < N`、`i <= N`、`i > N` 或 `i >= N`，更新只接受 `i = i + K` 或 `i = i - K`；
3. `K` 必须为正，更新方向必须匹配比较方向，并且数学计算证明退出更新不会发生 signed32 溢出；
4. 同名变量的全部 loop 都满足上述形态；
5. formatter `always.targets` 未把该变量列为任意形态的过程左值，变量也未在自身 loop 范围外被任何组合或顺序 `always` 引用；
6. 连续赋值和实例端口实参均不引用该变量。

因此普通整数反馈、循环体自反馈、循环体多节点环、变量外逃、顺序过程/实例端口逃逸、窄位宽 `reg` 归纳变量、运行时步长、零步长、`i=i`、错误方向和 `i=i*2` 均仍由原图失败。实现没有增加第二套 Verilog parser，也没有修改全局 skill、旧 overlay 或 RTL。

## 验证

执行：

```text
python -B -X utf8 tests/check_loop_feedback.py --overlay checker_overlay --output analysis/loop_feedback_test_v3.json
```

结果：进程退出码 0，`all_passed=true`。

- 两份真实 RTL：旧规则均失败且分别定位 `check_lane`/`lane_index`；新规则均通过 VG136。
- 十六组 VG136 formatter fixture：只有规范 `integer` 归纳循环由 failed→passed；普通自反馈、两节点环、同名普通整数反馈、循环体反馈/多节点环/拼接左值写归纳变量、组合/顺序/实例逃逸、窄 `reg`、运行时/零/恒等/错误方向/乘法更新均保持 failed。
- 非目标规则 VG130 的 overlay 返回值与 upstream 完全相等，证明 wrapper 委托未改变该规则。
- fixture 持久化在 `analysis/loop_feedback_fixtures/`；每个 fixture 的相对路径和 SHA256 均记录在 fresh JSON 的 `fixture_cases` 中。
- 运行只做 Python/formatter 静态事实验证；未运行 TD、仿真、训练、位流或板卡操作，也未声称完整八门禁通过。

最终 fresh 测试 JSON：`analysis/loop_feedback_test_v3.json`，SHA256 `cc1b655a72d6499f8b5fc5451e440df27d37d19538f0bfead9f542cba5887287`。
