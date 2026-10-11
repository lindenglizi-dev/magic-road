# VG097 unpacked array element 位宽事实闭合

日期：2026-10-09。任务类别：`modify + validate`，只修改本目录的 checker overlay，不修改生产 RTL、计算 RTL、全局 skill 或旧 overlay。

## 根因与补丁边界

调用链为：

```text
vg_control_rules.VG097
  -> vg_instance_rules._connection_port_width_match
  -> _evaluate_instance_widths
  -> _evaluate_named_connections
  -> vg_value_facts.expression_width
```

上游 `expression_width` 对所有单层 `identifier[index]` 固定返回 1，未消费 formatter AST 声明项已经提供的 `unpacked` 字段。因此：

```verilog
reg [31:0] reg_post_multiplier [0:1];
.i_post_multiplier(reg_post_multiplier[flag_layer_pw])
```

被误报成 `port_width=32 signal_width=1`；同类 6 位 `reg_post_shift` 也被误报为 1 位。

补丁只新增 `checker_overlay/scripts/python/quality/vg_instance_rules.py` 私有 wrapper。它加载安装版 `vg_instance_rules` 的独立副本，在该副本中：

1. 复用现有 `vg_value_facts.module_widths`，同时保留 formatter AST 的 `unpacked` 声明事实；
2. 仅当表达式是单层简单下标、基声明确有且只有一维 unpacked 维度时，返回该元素的 packed 宽度；
3. packed bit-select、packed part-select 和其他既有表达式继续委托上游；
4. 多维 unpacked 单次选择、unpacked array slice、嵌套选择及未知表达式保持 `inconclusive`。

没有修改共享 `vg_value_facts.expression_width`，因此 VG085 等共享规则不受该补丁影响；没有信号名白名单，也没有新增第二套 Verilog parser。

## 定向回归

命令：

```text
python -B -X utf8 tests/check_array_width.py --overlay checker_overlay --output analysis/array_width_results_v2.json
```

结果：10/10 通过。JSON 同时记录原检查器和 overlay 的 expected、actual、实际导入路径、导入文件标准 SHA256 与每个 formatter fixture 目录 fingerprint。普通文件摘要严格为 `sha256(file_bytes)`；fixture 目录 fingerprint 为按相对 POSIX 路径排序后重复输入 `relative_path + NUL + file_bytes + NUL` 的 SHA256，不把目录 fingerprint 冒充单文件 SHA256。

| 用例 | 原检查器 | overlay | 约束 |
|---|---|---|---|
| unpacked 32 位元素接 32 位端口 | failed | passed | 修复目标 |
| unpacked 32 位元素接 6 位端口 | failed | failed | 保留真实 mismatch |
| packed bit-select 接 1 位端口 | passed | passed | 不把 packed 位选当数组元素 |
| packed bit-select 接 6 位端口 | failed | failed | 保留真实 mismatch |
| packed `[9:4]` part-select | passed | passed | 保留既有 part-select |
| 参数化 6 位 unpacked 元素 | failed | passed | 保留参数求值 |
| 未支持算术表达式 | inconclusive | inconclusive | 未知不冒充通过 |
| unpacked 元素后的嵌套选择 | inconclusive | inconclusive | 保守处理 |
| 多维 unpacked 的单次选择 | failed | inconclusive | 单次选择仍是数组 |
| unpacked array slice | passed | inconclusive | 不套用 packed part-select 语义 |

主要证据：

- `analysis/array_width_results_v2.json`，标准文件 SHA256 `712df7127c3707aff62ed706f1f4128398ae997701fa184eea4850b639b1c997`
- wrapper SHA256 `79e2404b610e53d9a4213669c9e388c2c07893cf3b508ded0cc52c6c9b9c5dd0`
- 测试脚本 SHA256 `aebbbcf3ea8c63259a5410f8d4a4cfe0aa6f86622806f8791ef8b83871614d32`

本轮没有可用的 `readable-python-generator` skill，因此只报告上述可执行回归，不宣称 Python strict gate 通过。

## 真实 8 源候选

输入：`../mac_task_stream_20261009/checker_replay_final/inputs/candidate`，目录 fingerprint SHA256 `994e01c803447765eb3815401b4b4b997a42fdb250ce30ebfa385b30315f8d3e`，使用上述路径与 NUL framing 合同。

VG097 单规则结果：

- 原检查器：`failed`，2 条 finding；正是 `reg_post_multiplier[flag_layer_pw]` 的 32→1 假 mismatch 和 `reg_post_shift[flag_layer_pw]` 的 6→1 假 mismatch。
- overlay：上述 2 条假 mismatch 均消失；结果为 `inconclusive`，暴露 7 条原先被 failed 优先级遮蔽的既有未知事实，包括复杂条件/拼接表达式、空输出连接及外部 ERAM 接口。
- 证据：`analysis/real_vg097_original_v2.json`、`analysis/real_vg097_overlay_v2.json`；其中普通导入文件摘要均已与标准 SHA256 工具交叉核对。

这不是 VG097 全通过，也没有把复杂表达式猜成确定宽度。

## 完整门禁差异

使用同 8 个源、同外部接口、严格默认和本目录完整 overlay 重跑。新报告为 `analysis/candidate_gate.json` / `analysis/candidate_gate.md`。

与既有 `checker_replay_final/candidate/gate.json` 比较，规则计数只有以下变化：

| 规则 | 旧 | 新 | 说明 |
|---|---:|---:|---|
| VG097 | 2 | 7 | 2 条假 mismatch 移除，7 条既有未知事实显现 |
| VG136 | 2 | 0 | 本目录另一独立事实补丁的结果，不归因于本 wrapper |
| VG153 | 35 | 5 | 本目录另一独立事实补丁的结果，不归因于本 wrapper |

其余规则计数完全一致，包括 VG085 仍为 11。总计从 4975 errors / 20 strict warnings 变为 4948 errors / 20 strict warnings；仍非交付通过。

进一步以完整 issue JSON（稳定键排序后的多重集合）比较，排除本轮并行拥有者负责的 `VG097/VG136/VG153` 后，旧、新均为 4937 条，`removed=0`、`added=0`。

八项公开状态：`compile=passed`；`ast/readability/comment/naming/profile=failed`；`testbench/toolchain=not_requested`。本轮没有训练、TD、仿真、综合、位流或板卡证据。

## 剩余风险

wrapper 依赖 formatter AST 当前稳定提供声明的 `width` 与 `unpacked` 字段；未知或更复杂选择会保持 `inconclusive`。若未来需要支持多维数组的完整索引链，应先扩展 formatter 的结构事实合同，而不是在 VG097 中新增文本 parser。
