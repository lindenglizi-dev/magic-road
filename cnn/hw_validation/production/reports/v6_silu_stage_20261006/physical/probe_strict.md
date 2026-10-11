# Verilog deliverable gate

Root: `E:\project\qiansai\anlogic_topic2_work\lab1_sc500_road_vision\cnn\hw_validation\production\reports\v6_silu_stage_20261006\physical\rtl\silu_internal_probe.v`
Delivery ready: `False`
Summary: **214 error(s)**, **0 strict warning(s)**

## Actionable VG findings

<a id="vg-finding-1"></a>
### VG068: Header Description/Simulations fields must use the fixed bilingual path contract (`description/testbench` in English and `Description/TestBench` in Chinese).
- Status: `failed`
- Severity: `error`
- Location: `silu_internal_probe.v:1`
- Evidence:
- node_kind: `verilog_rtl`
- detail: header.description_simulations_paths
- source_excerpt: `header.description_simulations_paths`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
header.description_simulations_paths
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-2"></a>
### VG013: Flag-like signal `wire_table_ready` should use `flag_` prefix unless it is an output bridge.
- Status: `failed`
- Severity: `error`
- Location: `file:silu_internal_probe.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: naming.flag
- source_excerpt: `naming.flag`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
naming.flag
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-3"></a>
### VG013: Flag-like signal `wire_input_ready` should use `flag_` prefix unless it is an output bridge.
- Status: `failed`
- Severity: `error`
- Location: `file:silu_internal_probe.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: naming.flag
- source_excerpt: `naming.flag`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
naming.flag
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-4"></a>
### VG013: Flag-like signal `wire_output_valid` should use `flag_` prefix unless it is an output bridge.
- Status: `failed`
- Severity: `error`
- Location: `file:silu_internal_probe.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: naming.flag
- source_excerpt: `naming.flag`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
naming.flag
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-5"></a>
### VG013: Flag-like signal `reg_table_valid` should use `flag_` prefix unless it is an output bridge.
- Status: `failed`
- Severity: `error`
- Location: `file:silu_internal_probe.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: naming.flag
- source_excerpt: `naming.flag`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
naming.flag
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-6"></a>
### VG013: Flag-like signal `reg_input_valid` should use `flag_` prefix unless it is an output bridge.
- Status: `failed`
- Severity: `error`
- Location: `file:silu_internal_probe.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: naming.flag
- source_excerpt: `naming.flag`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
naming.flag
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-7"></a>
### VG013: Flag-like signal `reg_output_ready` should use `flag_` prefix unless it is an output bridge.
- Status: `failed`
- Severity: `error`
- Location: `file:silu_internal_probe.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: naming.flag
- source_excerpt: `naming.flag`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
naming.flag
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-8"></a>
### VG013: Counter-like signal `result_count_o` should use `cnt_` prefix.
- Status: `failed`
- Severity: `error`
- Location: `file:silu_internal_probe.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: naming.counter
- source_excerpt: `naming.counter`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
naming.counter
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-9"></a>
### VG020: Always block `always@(posedge i_clk or negedge i_rstn)` assigns multiple targets ['cnt_table', 'reg_table_addr', 'reg_table_data', 'reg_table_valid']; split to one target per always.
- Status: `failed`
- Severity: `error`
- Location: `file:silu_internal_probe.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: always.single_target
- source_excerpt: `always.single_target`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `interface`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
always.single_target
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-10"></a>
### VG020: Always block `always@(posedge i_clk or negedge i_rstn)` assigns multiple targets ['cnt_input', 'reg_input_data', 'reg_input_valid']; split to one target per always.
- Status: `failed`
- Severity: `error`
- Location: `file:silu_internal_probe.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: always.single_target
- source_excerpt: `always.single_target`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `interface`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
always.single_target
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-11"></a>
### VG020: Always block `always@(posedge i_clk or negedge i_rstn)` assigns multiple targets ['cnt_cycle', 'reg_output_ready']; split to one target per always.
- Status: `failed`
- Severity: `error`
- Location: `file:silu_internal_probe.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: always.single_target
- source_excerpt: `always.single_target`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `interface`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
always.single_target
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-12"></a>
### VG020: Always block `always@(posedge i_clk or negedge i_rstn)` assigns multiple targets ['cnt_result', 'reg_checksum', 'reg_error']; split to one target per always.
- Status: `failed`
- Severity: `error`
- Location: `file:silu_internal_probe.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: always.single_target
- source_excerpt: `always.single_target`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
always.single_target
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-13"></a>
### VG061: Item `done_o` must be placed in 其他信号连线, not `输出信号连线`.
- Status: `failed`
- Severity: `error`
- Location: `silu_internal_probe.v:116`
- Evidence:
- node_kind: `verilog_rtl`
- detail: regions.assign
- source_excerpt: `regions.assign`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
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

<a id="vg-finding-14"></a>
### VG061: Item `error_o` must be placed in 其他信号连线, not `输出信号连线`.
- Status: `failed`
- Severity: `error`
- Location: `silu_internal_probe.v:117`
- Evidence:
- node_kind: `verilog_rtl`
- detail: regions.assign
- source_excerpt: `regions.assign`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
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

<a id="vg-finding-15"></a>
### VG061: Item `phase_o` must be placed in 其他信号连线, not `输出信号连线`.
- Status: `failed`
- Severity: `error`
- Location: `silu_internal_probe.v:118`
- Evidence:
- node_kind: `verilog_rtl`
- detail: regions.assign
- source_excerpt: `regions.assign`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
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

<a id="vg-finding-16"></a>
### VG061: Item `result_count_o` must be placed in 其他信号连线, not `输出信号连线`.
- Status: `failed`
- Severity: `error`
- Location: `silu_internal_probe.v:119`
- Evidence:
- node_kind: `verilog_rtl`
- detail: regions.assign
- source_excerpt: `regions.assign`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
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

<a id="vg-finding-17"></a>
### VG061: Item `checksum_o` must be placed in 其他信号连线, not `输出信号连线`.
- Status: `failed`
- Severity: `error`
- Location: `silu_internal_probe.v:120`
- Evidence:
- node_kind: `verilog_rtl`
- detail: regions.assign
- source_excerpt: `regions.assign`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
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

<a id="vg-finding-18"></a>
### VG070: `输出信号` item `done_o` must use group label `PROBE接口`, not `unknown`.
- Status: `failed`
- Severity: `error`
- Location: `silu_internal_probe.v:102`
- Evidence:
- node_kind: `verilog_rtl`
- detail: output.mirror.group_label
- source_excerpt: `output.mirror.group_label`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
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

<a id="vg-finding-19"></a>
### VG070: `输出信号连线` item `o_done` must use group label `PROBE接口`, not `unknown`.
- Status: `failed`
- Severity: `error`
- Location: `silu_internal_probe.v:121`
- Evidence:
- node_kind: `verilog_rtl`
- detail: output.mirror.group_label
- source_excerpt: `output.mirror.group_label`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
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

<a id="vg-finding-20"></a>
### VG040: assign `flag_table_transfer` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `silu_internal_probe.v:110`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.coverage
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-21"></a>
### VG040: assign `flag_input_transfer` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `silu_internal_probe.v:111`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.coverage
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-22"></a>
### VG040: assign `flag_output_transfer` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `silu_internal_probe.v:112`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.coverage
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-23"></a>
### VG040: assign `done_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `silu_internal_probe.v:116`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.coverage
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-24"></a>
### VG040: assign `error_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `silu_internal_probe.v:117`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.coverage
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-25"></a>
### VG040: assign `phase_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `silu_internal_probe.v:118`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.coverage
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-26"></a>
### VG040: assign `result_count_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `silu_internal_probe.v:119`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.coverage
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-27"></a>
### VG040: assign `checksum_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `silu_internal_probe.v:120`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.coverage
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-28"></a>
### VG040: assign `o_done` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `silu_internal_probe.v:121`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.coverage
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-29"></a>
### VG040: assign `o_error` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `silu_internal_probe.v:122`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.coverage
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-30"></a>
### VG040: assign `o_phase` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `silu_internal_probe.v:123`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.coverage
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-31"></a>
### VG040: assign `o_result_count` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `silu_internal_probe.v:124`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.coverage
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-32"></a>
### VG040: assign `o_checksum` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `silu_internal_probe.v:125`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.coverage
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-33"></a>
### VG062: process assignment `reg_phase` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `silu_internal_probe.v:131`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.procedural_assignment
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-34"></a>
### VG062: process assignment `reg_phase` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `silu_internal_probe.v:136`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.procedural_assignment
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-35"></a>
### VG062: process assignment `reg_phase` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `silu_internal_probe.v:141`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.procedural_assignment
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-36"></a>
### VG062: process assignment `reg_phase` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `silu_internal_probe.v:146`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.procedural_assignment
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-37"></a>
### VG062: process assignment `reg_table_valid` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `silu_internal_probe.v:157`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.procedural_assignment
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-38"></a>
### VG062: process assignment `reg_table_addr` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `silu_internal_probe.v:158`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.procedural_assignment
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-39"></a>
### VG062: process assignment `reg_table_data` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `silu_internal_probe.v:159`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.procedural_assignment
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-40"></a>
### VG062: process assignment `cnt_table` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `silu_internal_probe.v:160`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.procedural_assignment
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-41"></a>
### VG062: process assignment `reg_table_valid` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `silu_internal_probe.v:162`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.procedural_assignment
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-42"></a>
### VG062: process assignment `cnt_table` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `silu_internal_probe.v:164`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.procedural_assignment
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-43"></a>
### VG062: process assignment `reg_table_valid` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `silu_internal_probe.v:166`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.procedural_assignment
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-44"></a>
### VG062: process assignment `reg_table_addr` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `silu_internal_probe.v:168`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.procedural_assignment
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-45"></a>
### VG062: process assignment `reg_table_data` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `silu_internal_probe.v:169`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.procedural_assignment
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-46"></a>
### VG062: process assignment `reg_table_valid` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `silu_internal_probe.v:173`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.procedural_assignment
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-47"></a>
### VG062: process assignment `reg_input_valid` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `silu_internal_probe.v:180`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.procedural_assignment
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-48"></a>
### VG062: process assignment `reg_input_data` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `silu_internal_probe.v:181`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.procedural_assignment
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-49"></a>
### VG062: process assignment `cnt_input` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `silu_internal_probe.v:182`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.procedural_assignment
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-50"></a>
### VG062: process assignment `reg_input_valid` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `silu_internal_probe.v:184`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.procedural_assignment
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-51"></a>
### VG062: process assignment `reg_input_data` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `silu_internal_probe.v:185`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.procedural_assignment
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-52"></a>
### VG062: process assignment `cnt_input` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `silu_internal_probe.v:187`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.procedural_assignment
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-53"></a>
### VG062: process assignment `reg_input_valid` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `silu_internal_probe.v:207`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.procedural_assignment
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-54"></a>
### VG062: process assignment `reg_input_data` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `silu_internal_probe.v:208`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.procedural_assignment
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-55"></a>
### VG062: process assignment `cnt_cycle` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `silu_internal_probe.v:217`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.procedural_assignment
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-56"></a>
### VG062: process assignment `reg_output_ready` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `silu_internal_probe.v:218`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.procedural_assignment
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-57"></a>
### VG062: process assignment `cnt_cycle` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `silu_internal_probe.v:220`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.procedural_assignment
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-58"></a>
### VG062: process assignment `reg_output_ready` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `silu_internal_probe.v:221`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.procedural_assignment
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-59"></a>
### VG062: process assignment `cnt_cycle` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `silu_internal_probe.v:223`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.procedural_assignment
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-60"></a>
### VG062: process assignment `reg_output_ready` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `silu_internal_probe.v:224`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.procedural_assignment
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-61"></a>
### VG062: process assignment `cnt_result` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `silu_internal_probe.v:231`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.procedural_assignment
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-62"></a>
### VG062: process assignment `reg_checksum` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `silu_internal_probe.v:232`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.procedural_assignment
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-63"></a>
### VG062: process assignment `reg_error` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `silu_internal_probe.v:233`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.procedural_assignment
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-64"></a>
### VG062: process assignment `reg_error` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `silu_internal_probe.v:236`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.procedural_assignment
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-65"></a>
### VG062: process assignment `reg_checksum` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `silu_internal_probe.v:239`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.procedural_assignment
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-66"></a>
### VG062: process assignment `cnt_result` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `silu_internal_probe.v:240`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.procedural_assignment
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-67"></a>
### VG065: signal `done_o` must be introduced by a group comment in `输出信号`.
- Status: `failed`
- Severity: `error`
- Location: `silu_internal_probe.v:102`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.definition_group
- source_excerpt: `comments.definition_group`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.definition_group
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-68"></a>
### VG122: 算术结果位宽超过赋值目标位宽。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:164`
- Evidence:
- node_kind: `verilog_rtl`
- detail: cnt_table <= cnt_table + 11'd1;
- source_excerpt: `cnt_table <= cnt_table + 11'd1;`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
cnt_table <= cnt_table + 11'd1;
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-69"></a>
### VG122: 算术结果位宽超过赋值目标位宽。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:168`
- Evidence:
- node_kind: `verilog_rtl`
- detail: reg_table_addr <= reg_table_addr + 10'd1;
- source_excerpt: `reg_table_addr <= reg_table_addr + 10'd1;`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
reg_table_addr <= reg_table_addr + 10'd1;
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-70"></a>
### VG122: 算术结果位宽超过赋值目标位宽。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:169`
- Evidence:
- node_kind: `verilog_rtl`
- detail: reg_table_data <= reg_table_data + 16'sd1;
- source_excerpt: `reg_table_data <= reg_table_data + 16'sd1;`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
reg_table_data <= reg_table_data + 16'sd1;
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-71"></a>
### VG122: 算术结果位宽超过赋值目标位宽。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:187`
- Evidence:
- node_kind: `verilog_rtl`
- detail: cnt_input <= cnt_input + 6'd1;
- source_excerpt: `cnt_input <= cnt_input + 6'd1;`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
cnt_input <= cnt_input + 6'd1;
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-72"></a>
### VG122: 算术结果位宽超过赋值目标位宽。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:220`
- Evidence:
- node_kind: `verilog_rtl`
- detail: cnt_cycle <= cnt_cycle + 8'd1;
- source_excerpt: `cnt_cycle <= cnt_cycle + 8'd1;`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
cnt_cycle <= cnt_cycle + 8'd1;
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-73"></a>
### VG122: 算术结果位宽超过赋值目标位宽。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:240`
- Evidence:
- node_kind: `verilog_rtl`
- detail: cnt_result <= cnt_result + 6'd1;
- source_excerpt: `cnt_result <= cnt_result + 6'd1;`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
cnt_result <= cnt_result + 6'd1;
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-74"></a>
### VG125: 字面量声明为 16 位，但实际值只需要 10 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:89`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 16'sd512
- source_excerpt: `16'sd512`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
16'sd512
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-75"></a>
### VG125: 字面量声明为 16 位，但实际值只需要 13 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:91`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 16'sd4096
- source_excerpt: `16'sd4096`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
16'sd4096
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-76"></a>
### VG125: 字面量声明为 6 位，但实际值只需要 5 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:145`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 6'd17
- source_excerpt: `6'd17`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
6'd17
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-77"></a>
### VG125: 字面量声明为 16 位，但实际值只需要 10 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:159`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 16'sd512
- source_excerpt: `16'sd512`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
16'sd512
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-78"></a>
### VG125: 字面量声明为 11 位，但实际值只需要 1 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:164`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 11'd1
- source_excerpt: `11'd1`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
11'd1
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-79"></a>
### VG125: 字面量声明为 10 位，但实际值只需要 1 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:168`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 10'd1
- source_excerpt: `10'd1`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
10'd1
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-80"></a>
### VG125: 字面量声明为 16 位，但实际值只需要 1 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:169`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 16'sd1
- source_excerpt: `16'sd1`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
16'sd1
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-81"></a>
### VG125: 字面量声明为 16 位，但实际值只需要 13 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:181`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 16'sd4096
- source_excerpt: `16'sd4096`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
16'sd4096
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-82"></a>
### VG125: 字面量声明为 16 位，但实际值只需要 13 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:185`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 16'sd4096
- source_excerpt: `16'sd4096`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
16'sd4096
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-83"></a>
### VG125: 字面量声明为 6 位，但实际值只需要 1 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:187`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 6'd1
- source_excerpt: `6'd1`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
6'd1
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-84"></a>
### VG125: 字面量声明为 16 位，但实际值只需要 12 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:189`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 16'sd2048
- source_excerpt: `16'sd2048`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
16'sd2048
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-85"></a>
### VG125: 字面量声明为 6 位，但实际值只需要 1 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:190`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 6'd1
- source_excerpt: `6'd1`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
6'd1
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-86"></a>
### VG125: 字面量声明为 16 位，但实际值只需要 11 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:190`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 16'sd2047
- source_excerpt: `16'sd2047`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
16'sd2047
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-87"></a>
### VG125: 字面量声明为 6 位，但实际值只需要 2 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:191`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 6'd2
- source_excerpt: `6'd2`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
6'd2
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-88"></a>
### VG125: 字面量声明为 16 位，但实际值只需要 3 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:191`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 16'sd7
- source_excerpt: `16'sd7`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
16'sd7
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-89"></a>
### VG125: 字面量声明为 6 位，但实际值只需要 2 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:192`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 6'd3
- source_excerpt: `6'd3`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
6'd3
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-90"></a>
### VG125: 字面量声明为 16 位，但实际值只需要 3 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:192`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 16'sd6
- source_excerpt: `16'sd6`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
16'sd6
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-91"></a>
### VG125: 字面量声明为 6 位，但实际值只需要 3 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:193`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 6'd4
- source_excerpt: `6'd4`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
6'd4
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-92"></a>
### VG125: 字面量声明为 16 位，但实际值只需要 3 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:193`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 16'sd5
- source_excerpt: `16'sd5`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
16'sd5
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-93"></a>
### VG125: 字面量声明为 6 位，但实际值只需要 3 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:194`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 6'd5
- source_excerpt: `6'd5`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
6'd5
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-94"></a>
### VG125: 字面量声明为 16 位，但实际值只需要 3 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:194`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 16'sd4
- source_excerpt: `16'sd4`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
16'sd4
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-95"></a>
### VG125: 字面量声明为 6 位，但实际值只需要 3 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:195`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 6'd6
- source_excerpt: `6'd6`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
6'd6
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-96"></a>
### VG125: 字面量声明为 16 位，但实际值只需要 2 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:195`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 16'sd3
- source_excerpt: `16'sd3`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
16'sd3
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-97"></a>
### VG125: 字面量声明为 6 位，但实际值只需要 3 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:196`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 6'd7
- source_excerpt: `6'd7`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
6'd7
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-98"></a>
### VG125: 字面量声明为 16 位，但实际值只需要 2 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:196`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 16'sd2
- source_excerpt: `16'sd2`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
16'sd2
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-99"></a>
### VG125: 字面量声明为 6 位，但实际值只需要 4 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:197`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 6'd8
- source_excerpt: `6'd8`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
6'd8
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-100"></a>
### VG125: 字面量声明为 16 位，但实际值只需要 1 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:197`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 16'sd1
- source_excerpt: `16'sd1`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
16'sd1
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-101"></a>
### VG125: 字面量声明为 6 位，但实际值只需要 4 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:198`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 6'd9
- source_excerpt: `6'd9`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
6'd9
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-102"></a>
### VG125: 字面量声明为 6 位，但实际值只需要 4 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:199`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 6'd10
- source_excerpt: `6'd10`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
6'd10
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-103"></a>
### VG125: 字面量声明为 16 位，但实际值只需要 1 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:199`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 16'sd1
- source_excerpt: `16'sd1`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
16'sd1
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-104"></a>
### VG125: 字面量声明为 6 位，但实际值只需要 4 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:200`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 6'd11
- source_excerpt: `6'd11`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
6'd11
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-105"></a>
### VG125: 字面量声明为 16 位，但实际值只需要 2 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:200`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 16'sd2
- source_excerpt: `16'sd2`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
16'sd2
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-106"></a>
### VG125: 字面量声明为 6 位，但实际值只需要 4 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:201`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 6'd12
- source_excerpt: `6'd12`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
6'd12
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-107"></a>
### VG125: 字面量声明为 16 位，但实际值只需要 2 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:201`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 16'sd3
- source_excerpt: `16'sd3`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
16'sd3
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-108"></a>
### VG125: 字面量声明为 6 位，但实际值只需要 4 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:202`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 6'd13
- source_excerpt: `6'd13`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
6'd13
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-109"></a>
### VG125: 字面量声明为 16 位，但实际值只需要 3 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:202`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 16'sd4
- source_excerpt: `16'sd4`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
16'sd4
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-110"></a>
### VG125: 字面量声明为 6 位，但实际值只需要 4 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:203`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 6'd14
- source_excerpt: `6'd14`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
6'd14
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-111"></a>
### VG125: 字面量声明为 16 位，但实际值只需要 11 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:203`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 16'sd2047
- source_excerpt: `16'sd2047`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
16'sd2047
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-112"></a>
### VG125: 字面量声明为 6 位，但实际值只需要 4 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:204`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 6'd15
- source_excerpt: `6'd15`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
6'd15
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-113"></a>
### VG125: 字面量声明为 16 位，但实际值只需要 12 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:204`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 16'sd2048
- source_excerpt: `16'sd2048`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
16'sd2048
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-114"></a>
### VG125: 字面量声明为 6 位，但实际值只需要 5 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:205`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 6'd16
- source_excerpt: `6'd16`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
6'd16
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-115"></a>
### VG125: 字面量声明为 16 位，但实际值只需要 13 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:205`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 16'sd4096
- source_excerpt: `16'sd4096`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
16'sd4096
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-116"></a>
### VG125: 字面量声明为 8 位，但实际值只需要 1 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:220`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 8'd1
- source_excerpt: `8'd1`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
8'd1
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-117"></a>
### VG125: 字面量声明为 3 位，但实际值只需要 2 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:221`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 3'd3
- source_excerpt: `3'd3`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
3'd3
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-118"></a>
### VG125: 字面量声明为 6 位，但实际值只需要 1 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:240`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 6'd1
- source_excerpt: `6'd1`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
6'd1
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-119"></a>
### VG125: 字面量声明为 6 位，但实际值只需要 1 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:243`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 6'd1
- source_excerpt: `6'd1`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
6'd1
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-120"></a>
### VG125: 字面量声明为 6 位，但实际值只需要 2 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:244`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 6'd2
- source_excerpt: `6'd2`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
6'd2
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-121"></a>
### VG125: 字面量声明为 16 位，但实际值只需要 10 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:244`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 16'sd512
- source_excerpt: `16'sd512`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
16'sd512
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-122"></a>
### VG125: 字面量声明为 6 位，但实际值只需要 2 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:245`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 6'd3
- source_excerpt: `6'd3`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
6'd3
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-123"></a>
### VG125: 字面量声明为 16 位，但实际值只需要 2 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:245`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 16'sd2
- source_excerpt: `16'sd2`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
16'sd2
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-124"></a>
### VG125: 字面量声明为 6 位，但实际值只需要 3 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:246`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 6'd4
- source_excerpt: `6'd4`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
6'd4
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-125"></a>
### VG125: 字面量声明为 16 位，但实际值只需要 2 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:246`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 16'sd2
- source_excerpt: `16'sd2`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
16'sd2
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-126"></a>
### VG125: 字面量声明为 6 位，但实际值只需要 3 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:247`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 6'd5
- source_excerpt: `6'd5`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
6'd5
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-127"></a>
### VG125: 字面量声明为 16 位，但实际值只需要 1 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:247`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 16'sd1
- source_excerpt: `16'sd1`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
16'sd1
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-128"></a>
### VG125: 字面量声明为 6 位，但实际值只需要 3 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:248`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 6'd6
- source_excerpt: `6'd6`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
6'd6
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-129"></a>
### VG125: 字面量声明为 16 位，但实际值只需要 1 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:248`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 16'sd1
- source_excerpt: `16'sd1`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
16'sd1
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-130"></a>
### VG125: 字面量声明为 6 位，但实际值只需要 3 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:249`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 6'd7
- source_excerpt: `6'd7`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
6'd7
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-131"></a>
### VG125: 字面量声明为 16 位，但实际值只需要 1 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:249`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 16'sd1
- source_excerpt: `16'sd1`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
16'sd1
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-132"></a>
### VG125: 字面量声明为 6 位，但实际值只需要 4 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:250`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 6'd8
- source_excerpt: `6'd8`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
6'd8
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-133"></a>
### VG125: 字面量声明为 6 位，但实际值只需要 4 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:251`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 6'd9
- source_excerpt: `6'd9`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
6'd9
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-134"></a>
### VG125: 字面量声明为 6 位，但实际值只需要 4 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:252`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 6'd10
- source_excerpt: `6'd10`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
6'd10
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-135"></a>
### VG125: 字面量声明为 6 位，但实际值只需要 4 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:253`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 6'd11
- source_excerpt: `6'd11`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
6'd11
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-136"></a>
### VG125: 字面量声明为 6 位，但实际值只需要 4 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:254`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 6'd12
- source_excerpt: `6'd12`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
6'd12
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-137"></a>
### VG125: 字面量声明为 6 位，但实际值只需要 4 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:255`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 6'd13
- source_excerpt: `6'd13`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
6'd13
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-138"></a>
### VG125: 字面量声明为 16 位，但实际值只需要 1 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:255`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 16'sd1
- source_excerpt: `16'sd1`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
16'sd1
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-139"></a>
### VG125: 字面量声明为 6 位，但实际值只需要 4 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:256`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 6'd14
- source_excerpt: `6'd14`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
6'd14
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-140"></a>
### VG125: 字面量声明为 16 位，但实际值只需要 1 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:256`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 16'sd1
- source_excerpt: `16'sd1`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
16'sd1
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-141"></a>
### VG125: 字面量声明为 6 位，但实际值只需要 4 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:257`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 6'd15
- source_excerpt: `6'd15`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
6'd15
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-142"></a>
### VG125: 字面量声明为 16 位，但实际值只需要 11 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:257`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 16'sd2047
- source_excerpt: `16'sd2047`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
16'sd2047
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-143"></a>
### VG125: 字面量声明为 6 位，但实际值只需要 5 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:258`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 6'd16
- source_excerpt: `6'd16`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
6'd16
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-144"></a>
### VG125: 字面量声明为 16 位，但实际值只需要 12 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:258`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 16'sd2048
- source_excerpt: `16'sd2048`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
16'sd2048
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-145"></a>
### VG125: 字面量声明为 6 位，但实际值只需要 5 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:259`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 6'd17
- source_excerpt: `6'd17`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
6'd17
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-146"></a>
### VG125: 字面量声明为 16 位，但实际值只需要 13 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:259`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 16'sd4096
- source_excerpt: `16'sd4096`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
16'sd4096
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-147"></a>
### VG138: 常量未显式声明位宽和进制。
- Status: `failed`
- Severity: `WARNING`
- Location: `silu_internal_probe.v:239`
- Evidence:
- node_kind: `verilog_rtl`
- detail: = reg_checksum ^ {{16
- source_excerpt: `= reg_checksum ^ {{16`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
= reg_checksum ^ {{16
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-148"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=cnt_input$enable; child_output=silu_internal_probe.cnt_input$enable; operation_count=5; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=cnt_input$enable; child_output=silu_internal_probe.cnt_input$enable; operation_count=5; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=cnt_input$enable; child_output=silu_internal_probe.cnt_input$enable; operation_count=5; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-149"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=cnt_result$enable; child_output=silu_internal_probe.cnt_result$enable; operation_count=1; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=cnt_result$enable; child_output=silu_internal_probe.cnt_result$enable; operation_count=1; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=cnt_result$enable; child_output=silu_internal_probe.cnt_result$enable; operation_count=1; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-150"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=cnt_table$enable; child_output=silu_internal_probe.cnt_table$enable; operation_count=2; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=cnt_table$enable; child_output=silu_internal_probe.cnt_table$enable; operation_count=2; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=cnt_table$enable; child_output=silu_internal_probe.cnt_table$enable; operation_count=2; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-151"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=reg_checksum$D; child_output=silu_internal_probe.reg_checksum$D; operation_count=0; limit=3; inconclusive_reason=reg_checksum$D: missing storage data expression; loop_presence=absent
- source_excerpt: `definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=reg_checksum$D; child_output=silu_internal_probe.reg_checksum$D; operation_count=0; limit=3; inconclusive_reason=reg_checksum$D: missing storage data expression; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=reg_checksum$D; child_output=silu_internal_probe.reg_checksum$D; operation_count=0; limit=3; inconclusive_reason=reg_checksum$D: missing storage data expression; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-152"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=reg_checksum$enable; child_output=silu_internal_probe.reg_checksum$enable; operation_count=1; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=reg_checksum$enable; child_output=silu_internal_probe.reg_checksum$enable; operation_count=1; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=reg_checksum$enable; child_output=silu_internal_probe.reg_checksum$enable; operation_count=1; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-153"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=reg_error$enable; child_output=silu_internal_probe.reg_error$enable; operation_count=25; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=reg_error$enable; child_output=silu_internal_probe.reg_error$enable; operation_count=25; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=reg_error$enable; child_output=silu_internal_probe.reg_error$enable; operation_count=25; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-154"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=reg_input_data$enable; child_output=silu_internal_probe.reg_input_data$enable; operation_count=5; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=reg_input_data$enable; child_output=silu_internal_probe.reg_input_data$enable; operation_count=5; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=reg_input_data$enable; child_output=silu_internal_probe.reg_input_data$enable; operation_count=5; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-155"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=reg_input_valid$enable; child_output=silu_internal_probe.reg_input_valid$enable; operation_count=5; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=reg_input_valid$enable; child_output=silu_internal_probe.reg_input_valid$enable; operation_count=5; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=reg_input_valid$enable; child_output=silu_internal_probe.reg_input_valid$enable; operation_count=5; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-156"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=reg_phase$enable; child_output=silu_internal_probe.reg_phase$enable; operation_count=6; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=reg_phase$enable; child_output=silu_internal_probe.reg_phase$enable; operation_count=6; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=reg_phase$enable; child_output=silu_internal_probe.reg_phase$enable; operation_count=6; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-157"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=reg_table_addr$enable; child_output=silu_internal_probe.reg_table_addr$enable; operation_count=3; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=reg_table_addr$enable; child_output=silu_internal_probe.reg_table_addr$enable; operation_count=3; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=reg_table_addr$enable; child_output=silu_internal_probe.reg_table_addr$enable; operation_count=3; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-158"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=reg_table_data$enable; child_output=silu_internal_probe.reg_table_data$enable; operation_count=3; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=reg_table_data$enable; child_output=silu_internal_probe.reg_table_data$enable; operation_count=3; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=reg_table_data$enable; child_output=silu_internal_probe.reg_table_data$enable; operation_count=3; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-159"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=reg_table_valid$enable; child_output=silu_internal_probe.reg_table_valid$enable; operation_count=3; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=reg_table_valid$enable; child_output=silu_internal_probe.reg_table_valid$enable; operation_count=3; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=reg_table_valid$enable; child_output=silu_internal_probe.reg_table_valid$enable; operation_count=3; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-160"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=wire_input_ready; child_output=silu_internal_probe.wire_input_ready; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=wire_input_ready; child_output=silu_internal_probe.wire_input_ready; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=wire_input_ready; child_output=silu_internal_probe.wire_input_ready; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-161"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=wire_output_data; child_output=silu_internal_probe.wire_output_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=wire_output_data; child_output=silu_internal_probe.wire_output_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=wire_output_data; child_output=silu_internal_probe.wire_output_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-162"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=wire_output_valid; child_output=silu_internal_probe.wire_output_valid; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=wire_output_valid; child_output=silu_internal_probe.wire_output_valid; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=wire_output_valid; child_output=silu_internal_probe.wire_output_valid; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-163"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=wire_table_fault; child_output=silu_internal_probe.wire_table_fault; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=wire_table_fault; child_output=silu_internal_probe.wire_table_fault; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=wire_table_fault; child_output=silu_internal_probe.wire_table_fault; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-164"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=wire_table_loaded; child_output=silu_internal_probe.wire_table_loaded; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=wire_table_loaded; child_output=silu_internal_probe.wire_table_loaded; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=wire_table_loaded; child_output=silu_internal_probe.wire_table_loaded; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-165"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=wire_table_ready; child_output=silu_internal_probe.wire_table_ready; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=wire_table_ready; child_output=silu_internal_probe.wire_table_ready; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=wire_table_ready; child_output=silu_internal_probe.wire_table_ready; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-166"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:110`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=flag_table_transfer; child_output=silu_internal_probe.flag_table_transfer; operation_count=1; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=flag_table_transfer; child_output=silu_internal_probe.flag_table_transfer; operation_count=1; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=flag_table_transfer; child_output=silu_internal_probe.flag_table_transfer; operation_count=1; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-167"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:111`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=flag_input_transfer; child_output=silu_internal_probe.flag_input_transfer; operation_count=1; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=flag_input_transfer; child_output=silu_internal_probe.flag_input_transfer; operation_count=1; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=flag_input_transfer; child_output=silu_internal_probe.flag_input_transfer; operation_count=1; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-168"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:112`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=flag_output_transfer; child_output=silu_internal_probe.flag_output_transfer; operation_count=1; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=flag_output_transfer; child_output=silu_internal_probe.flag_output_transfer; operation_count=1; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=flag_output_transfer; child_output=silu_internal_probe.flag_output_transfer; operation_count=1; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-169"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=cnt_input$enable; child_output=silu_internal_probe.cnt_input$enable; operation_count=5; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=cnt_input$enable; child_output=silu_internal_probe.cnt_input$enable; operation_count=5; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=cnt_input$enable; child_output=silu_internal_probe.cnt_input$enable; operation_count=5; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-170"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=cnt_result$enable; child_output=silu_internal_probe.cnt_result$enable; operation_count=1; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=cnt_result$enable; child_output=silu_internal_probe.cnt_result$enable; operation_count=1; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=cnt_result$enable; child_output=silu_internal_probe.cnt_result$enable; operation_count=1; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-171"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=cnt_table$enable; child_output=silu_internal_probe.cnt_table$enable; operation_count=2; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=cnt_table$enable; child_output=silu_internal_probe.cnt_table$enable; operation_count=2; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=cnt_table$enable; child_output=silu_internal_probe.cnt_table$enable; operation_count=2; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-172"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=reg_checksum$enable; child_output=silu_internal_probe.reg_checksum$enable; operation_count=1; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=reg_checksum$enable; child_output=silu_internal_probe.reg_checksum$enable; operation_count=1; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=reg_checksum$enable; child_output=silu_internal_probe.reg_checksum$enable; operation_count=1; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-173"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=reg_error$enable; child_output=silu_internal_probe.reg_error$enable; operation_count=25; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=reg_error$enable; child_output=silu_internal_probe.reg_error$enable; operation_count=25; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=reg_error$enable; child_output=silu_internal_probe.reg_error$enable; operation_count=25; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-174"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=reg_input_data$enable; child_output=silu_internal_probe.reg_input_data$enable; operation_count=5; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=reg_input_data$enable; child_output=silu_internal_probe.reg_input_data$enable; operation_count=5; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=reg_input_data$enable; child_output=silu_internal_probe.reg_input_data$enable; operation_count=5; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-175"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=reg_input_valid$enable; child_output=silu_internal_probe.reg_input_valid$enable; operation_count=5; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=reg_input_valid$enable; child_output=silu_internal_probe.reg_input_valid$enable; operation_count=5; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=reg_input_valid$enable; child_output=silu_internal_probe.reg_input_valid$enable; operation_count=5; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-176"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=reg_phase$enable; child_output=silu_internal_probe.reg_phase$enable; operation_count=6; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=reg_phase$enable; child_output=silu_internal_probe.reg_phase$enable; operation_count=6; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=reg_phase$enable; child_output=silu_internal_probe.reg_phase$enable; operation_count=6; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-177"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=reg_table_addr$enable; child_output=silu_internal_probe.reg_table_addr$enable; operation_count=3; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=reg_table_addr$enable; child_output=silu_internal_probe.reg_table_addr$enable; operation_count=3; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=reg_table_addr$enable; child_output=silu_internal_probe.reg_table_addr$enable; operation_count=3; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-178"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=reg_table_data$enable; child_output=silu_internal_probe.reg_table_data$enable; operation_count=3; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=reg_table_data$enable; child_output=silu_internal_probe.reg_table_data$enable; operation_count=3; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=reg_table_data$enable; child_output=silu_internal_probe.reg_table_data$enable; operation_count=3; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-179"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=reg_table_valid$enable; child_output=silu_internal_probe.reg_table_valid$enable; operation_count=3; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=reg_table_valid$enable; child_output=silu_internal_probe.reg_table_valid$enable; operation_count=3; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=reg_table_valid$enable; child_output=silu_internal_probe.reg_table_valid$enable; operation_count=3; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-180"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=wire_input_ready; child_output=silu_internal_probe.wire_input_ready; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=wire_input_ready; child_output=silu_internal_probe.wire_input_ready; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=wire_input_ready; child_output=silu_internal_probe.wire_input_ready; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-181"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=wire_output_data; child_output=silu_internal_probe.wire_output_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=wire_output_data; child_output=silu_internal_probe.wire_output_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=wire_output_data; child_output=silu_internal_probe.wire_output_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-182"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=wire_output_valid; child_output=silu_internal_probe.wire_output_valid; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=wire_output_valid; child_output=silu_internal_probe.wire_output_valid; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=wire_output_valid; child_output=silu_internal_probe.wire_output_valid; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-183"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=wire_table_fault; child_output=silu_internal_probe.wire_table_fault; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=wire_table_fault; child_output=silu_internal_probe.wire_table_fault; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=wire_table_fault; child_output=silu_internal_probe.wire_table_fault; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-184"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=wire_table_loaded; child_output=silu_internal_probe.wire_table_loaded; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=wire_table_loaded; child_output=silu_internal_probe.wire_table_loaded; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=wire_table_loaded; child_output=silu_internal_probe.wire_table_loaded; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-185"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=wire_table_ready; child_output=silu_internal_probe.wire_table_ready; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=wire_table_ready; child_output=silu_internal_probe.wire_table_ready; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=wire_table_ready; child_output=silu_internal_probe.wire_table_ready; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-186"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:110`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=flag_table_transfer; child_output=silu_internal_probe.flag_table_transfer; operation_count=1; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=flag_table_transfer; child_output=silu_internal_probe.flag_table_transfer; operation_count=1; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=flag_table_transfer; child_output=silu_internal_probe.flag_table_transfer; operation_count=1; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-187"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:111`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=flag_input_transfer; child_output=silu_internal_probe.flag_input_transfer; operation_count=1; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=flag_input_transfer; child_output=silu_internal_probe.flag_input_transfer; operation_count=1; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=flag_input_transfer; child_output=silu_internal_probe.flag_input_transfer; operation_count=1; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-188"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:112`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=flag_output_transfer; child_output=silu_internal_probe.flag_output_transfer; operation_count=1; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=flag_output_transfer; child_output=silu_internal_probe.flag_output_transfer; operation_count=1; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=silu_internal_probe.v:silu_internal_probe@49:1-285:1; instance_path=silu_internal_probe; specialization=6266b244edded33c5572c7987420f70d39e512cc0dc7f882824529f46604114e; target=flag_output_transfer; child_output=silu_internal_probe.flag_output_transfer; operation_count=1; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-189"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:72`
- Evidence:
- node_kind: `verilog_rtl`
- detail: wire_table_ready
- source_excerpt: `wire_table_ready`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
wire_table_ready
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-190"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:73`
- Evidence:
- node_kind: `verilog_rtl`
- detail: wire_input_ready
- source_excerpt: `wire_input_ready`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
wire_input_ready
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-191"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:74`
- Evidence:
- node_kind: `verilog_rtl`
- detail: wire_output_valid
- source_excerpt: `wire_output_valid`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
wire_output_valid
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-192"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:75`
- Evidence:
- node_kind: `verilog_rtl`
- detail: wire_output_data
- source_excerpt: `wire_output_data`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
wire_output_data
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-193"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:76`
- Evidence:
- node_kind: `verilog_rtl`
- detail: wire_table_loaded
- source_excerpt: `wire_table_loaded`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
wire_table_loaded
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-194"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:77`
- Evidence:
- node_kind: `verilog_rtl`
- detail: wire_table_fault
- source_excerpt: `wire_table_fault`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
wire_table_fault
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-195"></a>
### VG157: 普通 RTL 注释不得携带版本字样；版本历史只能位于 formatter 固定文件头范围。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:19`
- Evidence:
- node_kind: `verilog_rtl`
- detail: markers=V1.0; kind=group_or_leading
- source_excerpt: `markers=V1.0; kind=group_or_leading`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
markers=V1.0; kind=group_or_leading
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-196"></a>
### VG157: 普通 RTL 注释不得携带版本字样；版本历史只能位于 formatter 固定文件头范围。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `silu_internal_probe.v:42`
- Evidence:
- node_kind: `verilog_rtl`
- detail: markers=V1.0; kind=group_or_leading
- source_excerpt: `markers=V1.0; kind=group_or_leading`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
markers=V1.0; kind=group_or_leading
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

## Other deliverable findings

| Severity | Code | Path | Line | Message |
|---|---|---|---:|---|
| error | COMMENT_COMMENT_PLACEMENT | `silu_internal_probe.v:110` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `silu_internal_probe.v:111` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `silu_internal_probe.v:112` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `silu_internal_probe.v:116` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `silu_internal_probe.v:117` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `silu_internal_probe.v:118` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `silu_internal_probe.v:119` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `silu_internal_probe.v:120` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `silu_internal_probe.v:121` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `silu_internal_probe.v:122` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `silu_internal_probe.v:123` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `silu_internal_probe.v:124` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `silu_internal_probe.v:125` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
