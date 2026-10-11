# Verilog deliverable gate

Root: `E:\project\qiansai\anlogic_topic2_work\lab1_sc500_road_vision\cnn\hw_validation\mac\stream_gate_stage`
Delivery ready: `False`
Summary: **17 error(s)**, **0 strict warning(s)**

## Actionable VG findings

<a id="vg-finding-1"></a>
### VG031: Region banners appear out of the required order.
- Status: `failed`
- Severity: `error`
- Location: `file:road_mac_stream_probe.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: regions.order
- source_excerpt: `regions.order`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
regions.order
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-2"></a>
### VG061: Item `flag_core_input_ready` must be placed in 标志信号, not `模块实例化信号`.
- Status: `failed`
- Severity: `error`
- Location: `road_mac_stream_probe.v:91`
- Evidence:
- node_kind: `verilog_rtl`
- detail: regions.declaration
- source_excerpt: `regions.declaration`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `interface`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
regions.declaration
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-3"></a>
### VG061: Item `flag_core_input_ready` must be placed in 其他信号连线, not `模块实例化信号`.
- Status: `failed`
- Severity: `error`
- Location: `road_mac_stream_probe.v:116`
- Evidence:
- node_kind: `verilog_rtl`
- detail: regions.assign
- source_excerpt: `regions.assign`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `interface`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
regions.assign
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-4"></a>
### VG070: `输出信号` item `result_valid_o` must use group label `用户接口`, not `unknown`.
- Status: `failed`
- Severity: `error`
- Location: `road_mac_stream_probe.v:96`
- Evidence:
- node_kind: `verilog_rtl`
- detail: output.mirror.group_label
- source_excerpt: `output.mirror.group_label`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `interface`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
output.mirror.group_label
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-5"></a>
### VG070: `输出信号连线` item `o_command_ready` must use group label `用户接口`, not `unknown`.
- Status: `failed`
- Severity: `error`
- Location: `road_mac_stream_probe.v:126`
- Evidence:
- node_kind: `verilog_rtl`
- detail: output.mirror.group_label
- source_excerpt: `output.mirror.group_label`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `interface`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
output.mirror.group_label
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-6"></a>
### VG066: Comment for assign `result_valid_o` repeats or closely reuses comment from signal `result_valid_o`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_mac_stream_probe.v:103`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.repeated_semantic
- source_excerpt: `comments.repeated_semantic`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.repeated_semantic
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-7"></a>
### VG066: Comment for assign `result_data_o` repeats or closely reuses comment from signal `result_data_o`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_mac_stream_probe.v:106`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.repeated_semantic
- source_excerpt: `comments.repeated_semantic`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.repeated_semantic
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-8"></a>
### VG066: Comment for assign `fault_o` repeats or closely reuses comment from signal `fault_o`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_mac_stream_probe.v:107`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.repeated_semantic
- source_excerpt: `comments.repeated_semantic`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.repeated_semantic
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-9"></a>
### VG066: Comment for assign `flag_core_input_ready` repeats or closely reuses comment from signal `flag_core_input_ready`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_mac_stream_probe.v:116`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.repeated_semantic
- source_excerpt: `comments.repeated_semantic`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.repeated_semantic
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-10"></a>
### VG138: 常量未显式声明位宽和进制。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_mac_stream_probe.v:106`
- Evidence:
- node_kind: `verilog_rtl`
- detail: = {96
- source_excerpt: `= {96`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
= {96
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-11"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_mac_stream_probe.v:47`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_mac_stream_probe.v:road_mac_stream_probe@47:1-227:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_command_pending$enable; child_output=road_mac_stream_probe.flag_command_pending$enable; operation_count=6; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_mac_stream_probe.v:road_mac_stream_probe@47:1-227:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_command_pending$enable; child_output=road_mac_stream_probe.flag_command_pending$enable; operation_count=6; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_mac_stream_probe.v:road_mac_stream_probe@47:1-227:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_command_pending$enable; child_output=road_mac_stream_probe.flag_command_pending$enable; operation_count=6; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-12"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_mac_stream_probe.v:47`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_mac_stream_probe.v:road_mac_stream_probe@47:1-227:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_command_address$enable; child_output=road_mac_stream_probe.reg_command_address$enable; operation_count=5; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_mac_stream_probe.v:road_mac_stream_probe@47:1-227:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_command_address$enable; child_output=road_mac_stream_probe.reg_command_address$enable; operation_count=5; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_mac_stream_probe.v:road_mac_stream_probe@47:1-227:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_command_address$enable; child_output=road_mac_stream_probe.reg_command_address$enable; operation_count=5; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-13"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_mac_stream_probe.v:47`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_mac_stream_probe.v:road_mac_stream_probe@47:1-227:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_command_payload$enable; child_output=road_mac_stream_probe.reg_command_payload$enable; operation_count=5; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_mac_stream_probe.v:road_mac_stream_probe@47:1-227:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_command_payload$enable; child_output=road_mac_stream_probe.reg_command_payload$enable; operation_count=5; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_mac_stream_probe.v:road_mac_stream_probe@47:1-227:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_command_payload$enable; child_output=road_mac_stream_probe.reg_command_payload$enable; operation_count=5; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-14"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_mac_stream_probe.v:106`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_mac_stream_probe.v:road_mac_stream_probe@47:1-227:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=result_data_o; child_output=road_mac_stream_probe.result_data_o; operation_count=0; limit=3; inconclusive_reason=result_data_o: > ERR: [Python] expected '}', got '{'; loop_presence=absent
- source_excerpt: `definition_root=road_mac_stream_probe.v:road_mac_stream_probe@47:1-227:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=result_data_o; child_output=road_mac_stream_probe.result_data_o; operation_count=0; limit=3; inconclusive_reason=result_data_o: > ERR: [Python] expected '}', got '{'; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_mac_stream_probe.v:road_mac_stream_probe@47:1-227:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=result_data_o; child_output=road_mac_stream_probe.result_data_o; operation_count=0; limit=3; inconclusive_reason=result_data_o: > ERR: [Python] expected '}', got '{'; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-15"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_mac_stream_probe.v:121`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_mac_stream_probe.v:road_mac_stream_probe@47:1-227:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_command_accept; child_output=road_mac_stream_probe.flag_command_accept; operation_count=4; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_mac_stream_probe.v:road_mac_stream_probe@47:1-227:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_command_accept; child_output=road_mac_stream_probe.flag_command_accept; operation_count=4; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_mac_stream_probe.v:road_mac_stream_probe@47:1-227:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_command_accept; child_output=road_mac_stream_probe.flag_command_accept; operation_count=4; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-16"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_mac_stream_probe.v:128`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_mac_stream_probe.v:road_mac_stream_probe@47:1-227:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=o_result_data; child_output=road_mac_stream_probe.o_result_data; operation_count=0; limit=3; inconclusive_reason=result_data_o: > ERR: [Python] expected '}', got '{'; loop_presence=absent
- source_excerpt: `definition_root=road_mac_stream_probe.v:road_mac_stream_probe@47:1-227:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=o_result_data; child_output=road_mac_stream_probe.o_result_data; operation_count=0; limit=3; inconclusive_reason=result_data_o: > ERR: [Python] expected '}', got '{'; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_mac_stream_probe.v:road_mac_stream_probe@47:1-227:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=o_result_data; child_output=road_mac_stream_probe.o_result_data; operation_count=0; limit=3; inconclusive_reason=result_data_o: > ERR: [Python] expected '}', got '{'; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

## Other deliverable findings

| Severity | Code | Path | Line | Message |
|---|---|---|---:|---|
| error | COMMENT_COMMENT_PLACEMENT | `road_mac_stream_probe.v:210` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
