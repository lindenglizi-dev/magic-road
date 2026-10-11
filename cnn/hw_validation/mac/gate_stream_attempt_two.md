# Verilog deliverable gate

Root: `E:\project\qiansai\anlogic_topic2_work\lab1_sc500_road_vision\cnn\hw_validation\mac\stream_gate_stage`
Delivery ready: `False`
Summary: **173 error(s)**, **40 strict warning(s)**

## Actionable VG findings

<a id="vg-finding-1"></a>
### VG061: Item `core_activation_data` must be placed in 模块实例化信号, not `其他信号`.
- Status: `failed`
- Severity: `error`
- Location: `road_mac_stream_probe.v:128`
- Evidence:
- node_kind: `verilog_rtl`
- detail: regions.declaration
- source_excerpt: `regions.declaration`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
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

<a id="vg-finding-2"></a>
### VG061: Item `core_weight_data` must be placed in 模块实例化信号, not `其他信号`.
- Status: `failed`
- Severity: `error`
- Location: `road_mac_stream_probe.v:129`
- Evidence:
- node_kind: `verilog_rtl`
- detail: regions.declaration
- source_excerpt: `regions.declaration`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
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
### VG061: Item `core_bias_data` must be placed in 模块实例化信号, not `其他信号`.
- Status: `failed`
- Severity: `error`
- Location: `road_mac_stream_probe.v:130`
- Evidence:
- node_kind: `verilog_rtl`
- detail: regions.declaration
- source_excerpt: `regions.declaration`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
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

<a id="vg-finding-4"></a>
### VG070: `输出信号` item `result_valid_o` must use group label `用户接口`, not `unknown`.
- Status: `failed`
- Severity: `error`
- Location: `road_mac_stream_probe.v:135`
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
- Location: `road_mac_stream_probe.v:194`
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
### VG056: Comment for assign `flag_all_loaded` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_mac_stream_probe.v:142`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.no_fallback
- source_excerpt: `comments.no_fallback`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.no_fallback
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-7"></a>
### VG041: Comment for assign `flag_all_loaded` looks generic: `assign`.
- Status: `failed`
- Severity: `warning`
- Location: `road_mac_stream_probe.v:142`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.semantic
- source_excerpt: `comments.semantic`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.semantic
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-8"></a>
### VG056: Comment for assign `flag_core_accept` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_mac_stream_probe.v:143`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.no_fallback
- source_excerpt: `comments.no_fallback`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.no_fallback
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-9"></a>
### VG041: Comment for assign `flag_core_accept` looks generic: `assign`.
- Status: `failed`
- Severity: `warning`
- Location: `road_mac_stream_probe.v:143`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.semantic
- source_excerpt: `comments.semantic`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.semantic
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-10"></a>
### VG056: Comment for assign `core_activation_data` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_mac_stream_probe.v:146`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.no_fallback
- source_excerpt: `comments.no_fallback`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.no_fallback
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-11"></a>
### VG041: Comment for assign `core_activation_data` looks generic: `assign`.
- Status: `failed`
- Severity: `warning`
- Location: `road_mac_stream_probe.v:146`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.semantic
- source_excerpt: `comments.semantic`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.semantic
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-12"></a>
### VG056: Comment for assign `core_weight_data` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_mac_stream_probe.v:147`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.no_fallback
- source_excerpt: `comments.no_fallback`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.no_fallback
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-13"></a>
### VG041: Comment for assign `core_weight_data` looks generic: `assign`.
- Status: `failed`
- Severity: `warning`
- Location: `road_mac_stream_probe.v:147`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.semantic
- source_excerpt: `comments.semantic`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.semantic
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-14"></a>
### VG056: Comment for assign `core_bias_data` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_mac_stream_probe.v:148`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.no_fallback
- source_excerpt: `comments.no_fallback`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.no_fallback
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-15"></a>
### VG041: Comment for assign `core_bias_data` looks generic: `assign`.
- Status: `failed`
- Severity: `warning`
- Location: `road_mac_stream_probe.v:148`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.semantic
- source_excerpt: `comments.semantic`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.semantic
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-16"></a>
### VG056: Comment for assign `flag_command_accept` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_mac_stream_probe.v:151`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.no_fallback
- source_excerpt: `comments.no_fallback`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.no_fallback
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-17"></a>
### VG041: Comment for assign `flag_command_accept` looks generic: `assign`.
- Status: `failed`
- Severity: `warning`
- Location: `road_mac_stream_probe.v:151`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.semantic
- source_excerpt: `comments.semantic`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.semantic
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-18"></a>
### VG056: Comment for assign `flag_load_activation_lower` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_mac_stream_probe.v:154`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.no_fallback
- source_excerpt: `comments.no_fallback`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.no_fallback
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-19"></a>
### VG041: Comment for assign `flag_load_activation_lower` looks generic: `assign`.
- Status: `failed`
- Severity: `warning`
- Location: `road_mac_stream_probe.v:154`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.semantic
- source_excerpt: `comments.semantic`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.semantic
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-20"></a>
### VG056: Comment for assign `flag_load_activation_upper` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_mac_stream_probe.v:155`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.no_fallback
- source_excerpt: `comments.no_fallback`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.no_fallback
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-21"></a>
### VG041: Comment for assign `flag_load_activation_upper` looks generic: `assign`.
- Status: `failed`
- Severity: `warning`
- Location: `road_mac_stream_probe.v:155`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.semantic
- source_excerpt: `comments.semantic`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.semantic
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-22"></a>
### VG056: Comment for assign `flag_load_weight_first` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_mac_stream_probe.v:156`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.no_fallback
- source_excerpt: `comments.no_fallback`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.no_fallback
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-23"></a>
### VG041: Comment for assign `flag_load_weight_first` looks generic: `assign`.
- Status: `failed`
- Severity: `warning`
- Location: `road_mac_stream_probe.v:156`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.semantic
- source_excerpt: `comments.semantic`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.semantic
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-24"></a>
### VG056: Comment for assign `flag_load_weight_second` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_mac_stream_probe.v:157`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.no_fallback
- source_excerpt: `comments.no_fallback`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.no_fallback
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-25"></a>
### VG041: Comment for assign `flag_load_weight_second` looks generic: `assign`.
- Status: `failed`
- Severity: `warning`
- Location: `road_mac_stream_probe.v:157`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.semantic
- source_excerpt: `comments.semantic`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.semantic
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-26"></a>
### VG056: Comment for assign `flag_load_weight_third` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_mac_stream_probe.v:158`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.no_fallback
- source_excerpt: `comments.no_fallback`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.no_fallback
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-27"></a>
### VG041: Comment for assign `flag_load_weight_third` looks generic: `assign`.
- Status: `failed`
- Severity: `warning`
- Location: `road_mac_stream_probe.v:158`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.semantic
- source_excerpt: `comments.semantic`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.semantic
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-28"></a>
### VG056: Comment for assign `flag_load_weight_fourth` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_mac_stream_probe.v:159`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.no_fallback
- source_excerpt: `comments.no_fallback`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.no_fallback
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-29"></a>
### VG041: Comment for assign `flag_load_weight_fourth` looks generic: `assign`.
- Status: `failed`
- Severity: `warning`
- Location: `road_mac_stream_probe.v:159`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.semantic
- source_excerpt: `comments.semantic`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.semantic
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-30"></a>
### VG056: Comment for assign `flag_load_weight_fifth` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_mac_stream_probe.v:160`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.no_fallback
- source_excerpt: `comments.no_fallback`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.no_fallback
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-31"></a>
### VG041: Comment for assign `flag_load_weight_fifth` looks generic: `assign`.
- Status: `failed`
- Severity: `warning`
- Location: `road_mac_stream_probe.v:160`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.semantic
- source_excerpt: `comments.semantic`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.semantic
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-32"></a>
### VG056: Comment for assign `flag_load_weight_sixth` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_mac_stream_probe.v:161`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.no_fallback
- source_excerpt: `comments.no_fallback`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.no_fallback
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-33"></a>
### VG041: Comment for assign `flag_load_weight_sixth` looks generic: `assign`.
- Status: `failed`
- Severity: `warning`
- Location: `road_mac_stream_probe.v:161`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.semantic
- source_excerpt: `comments.semantic`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.semantic
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-34"></a>
### VG056: Comment for assign `flag_load_bias_first` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_mac_stream_probe.v:162`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.no_fallback
- source_excerpt: `comments.no_fallback`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.no_fallback
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-35"></a>
### VG041: Comment for assign `flag_load_bias_first` looks generic: `assign`.
- Status: `failed`
- Severity: `warning`
- Location: `road_mac_stream_probe.v:162`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.semantic
- source_excerpt: `comments.semantic`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.semantic
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-36"></a>
### VG056: Comment for assign `flag_load_bias_second` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_mac_stream_probe.v:163`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.no_fallback
- source_excerpt: `comments.no_fallback`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.no_fallback
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-37"></a>
### VG041: Comment for assign `flag_load_bias_second` looks generic: `assign`.
- Status: `failed`
- Severity: `warning`
- Location: `road_mac_stream_probe.v:163`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.semantic
- source_excerpt: `comments.semantic`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.semantic
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-38"></a>
### VG056: Comment for assign `flag_load_bias_third` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_mac_stream_probe.v:164`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.no_fallback
- source_excerpt: `comments.no_fallback`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.no_fallback
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-39"></a>
### VG041: Comment for assign `flag_load_bias_third` looks generic: `assign`.
- Status: `failed`
- Severity: `warning`
- Location: `road_mac_stream_probe.v:164`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.semantic
- source_excerpt: `comments.semantic`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.semantic
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-40"></a>
### VG056: Comment for assign `flag_load_control` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_mac_stream_probe.v:165`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.no_fallback
- source_excerpt: `comments.no_fallback`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.no_fallback
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-41"></a>
### VG041: Comment for assign `flag_load_control` looks generic: `assign`.
- Status: `failed`
- Severity: `warning`
- Location: `road_mac_stream_probe.v:165`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.semantic
- source_excerpt: `comments.semantic`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.semantic
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-42"></a>
### VG056: Comment for assign `load_event_mask` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_mac_stream_probe.v:166`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.no_fallback
- source_excerpt: `comments.no_fallback`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.no_fallback
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-43"></a>
### VG041: Comment for assign `load_event_mask` looks generic: `assign`.
- Status: `failed`
- Severity: `warning`
- Location: `road_mac_stream_probe.v:166`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.semantic
- source_excerpt: `comments.semantic`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.semantic
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-44"></a>
### VG056: Comment for assign `flag_opcode_activation` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_mac_stream_probe.v:169`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.no_fallback
- source_excerpt: `comments.no_fallback`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.no_fallback
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-45"></a>
### VG041: Comment for assign `flag_opcode_activation` looks generic: `assign`.
- Status: `failed`
- Severity: `warning`
- Location: `road_mac_stream_probe.v:169`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.semantic
- source_excerpt: `comments.semantic`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.semantic
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-46"></a>
### VG056: Comment for assign `flag_opcode_weight` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_mac_stream_probe.v:170`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.no_fallback
- source_excerpt: `comments.no_fallback`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.no_fallback
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-47"></a>
### VG041: Comment for assign `flag_opcode_weight` looks generic: `assign`.
- Status: `failed`
- Severity: `warning`
- Location: `road_mac_stream_probe.v:170`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.semantic
- source_excerpt: `comments.semantic`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.semantic
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-48"></a>
### VG056: Comment for assign `flag_opcode_bias` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_mac_stream_probe.v:171`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.no_fallback
- source_excerpt: `comments.no_fallback`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.no_fallback
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-49"></a>
### VG041: Comment for assign `flag_opcode_bias` looks generic: `assign`.
- Status: `failed`
- Severity: `warning`
- Location: `road_mac_stream_probe.v:171`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.semantic
- source_excerpt: `comments.semantic`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.semantic
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-50"></a>
### VG056: Comment for assign `flag_opcode_control` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_mac_stream_probe.v:172`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.no_fallback
- source_excerpt: `comments.no_fallback`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.no_fallback
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-51"></a>
### VG041: Comment for assign `flag_opcode_control` looks generic: `assign`.
- Status: `failed`
- Severity: `warning`
- Location: `road_mac_stream_probe.v:172`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.semantic
- source_excerpt: `comments.semantic`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.semantic
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-52"></a>
### VG056: Comment for assign `flag_activation_address` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_mac_stream_probe.v:175`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.no_fallback
- source_excerpt: `comments.no_fallback`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.no_fallback
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-53"></a>
### VG041: Comment for assign `flag_activation_address` looks generic: `assign`.
- Status: `failed`
- Severity: `warning`
- Location: `road_mac_stream_probe.v:175`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.semantic
- source_excerpt: `comments.semantic`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.semantic
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-54"></a>
### VG056: Comment for assign `flag_weight_address` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_mac_stream_probe.v:176`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.no_fallback
- source_excerpt: `comments.no_fallback`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.no_fallback
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-55"></a>
### VG041: Comment for assign `flag_weight_address` looks generic: `assign`.
- Status: `failed`
- Severity: `warning`
- Location: `road_mac_stream_probe.v:176`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.semantic
- source_excerpt: `comments.semantic`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.semantic
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-56"></a>
### VG056: Comment for assign `flag_bias_address` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_mac_stream_probe.v:177`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.no_fallback
- source_excerpt: `comments.no_fallback`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.no_fallback
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-57"></a>
### VG041: Comment for assign `flag_bias_address` looks generic: `assign`.
- Status: `failed`
- Severity: `warning`
- Location: `road_mac_stream_probe.v:177`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.semantic
- source_excerpt: `comments.semantic`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.semantic
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-58"></a>
### VG056: Comment for assign `flag_control_address` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_mac_stream_probe.v:178`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.no_fallback
- source_excerpt: `comments.no_fallback`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.no_fallback
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-59"></a>
### VG041: Comment for assign `flag_control_address` looks generic: `assign`.
- Status: `failed`
- Severity: `warning`
- Location: `road_mac_stream_probe.v:178`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.semantic
- source_excerpt: `comments.semantic`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.semantic
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-60"></a>
### VG056: Comment for assign `flag_address_lower` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_mac_stream_probe.v:179`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.no_fallback
- source_excerpt: `comments.no_fallback`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.no_fallback
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-61"></a>
### VG041: Comment for assign `flag_address_lower` looks generic: `assign`.
- Status: `failed`
- Severity: `warning`
- Location: `road_mac_stream_probe.v:179`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.semantic
- source_excerpt: `comments.semantic`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.semantic
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-62"></a>
### VG056: Comment for assign `flag_address_upper` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_mac_stream_probe.v:180`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.no_fallback
- source_excerpt: `comments.no_fallback`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.no_fallback
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-63"></a>
### VG041: Comment for assign `flag_address_upper` looks generic: `assign`.
- Status: `failed`
- Severity: `warning`
- Location: `road_mac_stream_probe.v:180`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.semantic
- source_excerpt: `comments.semantic`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.semantic
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-64"></a>
### VG056: Comment for assign `flag_command_address` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_mac_stream_probe.v:181`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.no_fallback
- source_excerpt: `comments.no_fallback`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.no_fallback
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-65"></a>
### VG041: Comment for assign `flag_command_address` looks generic: `assign`.
- Status: `failed`
- Severity: `warning`
- Location: `road_mac_stream_probe.v:181`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.semantic
- source_excerpt: `comments.semantic`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.semantic
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-66"></a>
### VG056: Comment for assign `flag_index_zero` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_mac_stream_probe.v:184`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.no_fallback
- source_excerpt: `comments.no_fallback`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.no_fallback
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-67"></a>
### VG041: Comment for assign `flag_index_zero` looks generic: `assign`.
- Status: `failed`
- Severity: `warning`
- Location: `road_mac_stream_probe.v:184`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.semantic
- source_excerpt: `comments.semantic`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.semantic
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-68"></a>
### VG056: Comment for assign `flag_index_one` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_mac_stream_probe.v:185`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.no_fallback
- source_excerpt: `comments.no_fallback`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.no_fallback
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-69"></a>
### VG041: Comment for assign `flag_index_one` looks generic: `assign`.
- Status: `failed`
- Severity: `warning`
- Location: `road_mac_stream_probe.v:185`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.semantic
- source_excerpt: `comments.semantic`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.semantic
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-70"></a>
### VG056: Comment for assign `flag_index_two` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_mac_stream_probe.v:186`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.no_fallback
- source_excerpt: `comments.no_fallback`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.no_fallback
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-71"></a>
### VG041: Comment for assign `flag_index_two` looks generic: `assign`.
- Status: `failed`
- Severity: `warning`
- Location: `road_mac_stream_probe.v:186`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.semantic
- source_excerpt: `comments.semantic`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.semantic
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-72"></a>
### VG056: Comment for assign `flag_index_three` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_mac_stream_probe.v:187`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.no_fallback
- source_excerpt: `comments.no_fallback`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.no_fallback
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-73"></a>
### VG041: Comment for assign `flag_index_three` looks generic: `assign`.
- Status: `failed`
- Severity: `warning`
- Location: `road_mac_stream_probe.v:187`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.semantic
- source_excerpt: `comments.semantic`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.semantic
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-74"></a>
### VG056: Comment for assign `flag_index_four` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_mac_stream_probe.v:188`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.no_fallback
- source_excerpt: `comments.no_fallback`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.no_fallback
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-75"></a>
### VG041: Comment for assign `flag_index_four` looks generic: `assign`.
- Status: `failed`
- Severity: `warning`
- Location: `road_mac_stream_probe.v:188`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.semantic
- source_excerpt: `comments.semantic`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.semantic
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-76"></a>
### VG056: Comment for assign `flag_index_five` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_mac_stream_probe.v:189`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.no_fallback
- source_excerpt: `comments.no_fallback`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.no_fallback
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-77"></a>
### VG041: Comment for assign `flag_index_five` looks generic: `assign`.
- Status: `failed`
- Severity: `warning`
- Location: `road_mac_stream_probe.v:189`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.semantic
- source_excerpt: `comments.semantic`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.semantic
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-78"></a>
### VG056: Comment for assign `o_command_ready` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_mac_stream_probe.v:194`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.no_fallback
- source_excerpt: `comments.no_fallback`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.no_fallback
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-79"></a>
### VG041: Comment for assign `o_command_ready` looks generic: `assign`.
- Status: `failed`
- Severity: `warning`
- Location: `road_mac_stream_probe.v:194`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.semantic
- source_excerpt: `comments.semantic`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.semantic
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-80"></a>
### VG056: Comment for assign `o_result_valid` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_mac_stream_probe.v:195`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.no_fallback
- source_excerpt: `comments.no_fallback`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.no_fallback
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-81"></a>
### VG041: Comment for assign `o_result_valid` looks generic: `assign`.
- Status: `failed`
- Severity: `warning`
- Location: `road_mac_stream_probe.v:195`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.semantic
- source_excerpt: `comments.semantic`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.semantic
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-82"></a>
### VG056: Comment for assign `o_result_data` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_mac_stream_probe.v:196`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.no_fallback
- source_excerpt: `comments.no_fallback`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.no_fallback
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-83"></a>
### VG041: Comment for assign `o_result_data` looks generic: `assign`.
- Status: `failed`
- Severity: `warning`
- Location: `road_mac_stream_probe.v:196`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.semantic
- source_excerpt: `comments.semantic`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.semantic
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-84"></a>
### VG056: Comment for assign `o_fault` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_mac_stream_probe.v:197`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.no_fallback
- source_excerpt: `comments.no_fallback`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.no_fallback
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-85"></a>
### VG041: Comment for assign `o_fault` looks generic: `assign`.
- Status: `failed`
- Severity: `warning`
- Location: `road_mac_stream_probe.v:197`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.semantic
- source_excerpt: `comments.semantic`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.semantic
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-86"></a>
### VG062: process assignment `reg_loaded` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_mac_stream_probe.v:203`
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

<a id="vg-finding-87"></a>
### VG062: process assignment `reg_loaded` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_mac_stream_probe.v:205`
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

<a id="vg-finding-88"></a>
### VG062: process assignment `reg_loaded` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_mac_stream_probe.v:207`
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

<a id="vg-finding-89"></a>
### VG062: process assignment `reg_activation_lower` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_mac_stream_probe.v:214`
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

<a id="vg-finding-90"></a>
### VG062: process assignment `reg_activation_lower` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_mac_stream_probe.v:216`
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

<a id="vg-finding-91"></a>
### VG062: process assignment `reg_activation_upper` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_mac_stream_probe.v:223`
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

<a id="vg-finding-92"></a>
### VG062: process assignment `reg_activation_upper` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_mac_stream_probe.v:225`
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

<a id="vg-finding-93"></a>
### VG062: process assignment `reg_weight_first` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_mac_stream_probe.v:232`
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

<a id="vg-finding-94"></a>
### VG062: process assignment `reg_weight_first` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_mac_stream_probe.v:234`
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

<a id="vg-finding-95"></a>
### VG062: process assignment `reg_weight_second` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_mac_stream_probe.v:241`
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

<a id="vg-finding-96"></a>
### VG062: process assignment `reg_weight_second` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_mac_stream_probe.v:243`
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

<a id="vg-finding-97"></a>
### VG062: process assignment `reg_weight_third` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_mac_stream_probe.v:250`
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

<a id="vg-finding-98"></a>
### VG062: process assignment `reg_weight_third` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_mac_stream_probe.v:252`
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

<a id="vg-finding-99"></a>
### VG062: process assignment `reg_weight_fourth` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_mac_stream_probe.v:259`
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

<a id="vg-finding-100"></a>
### VG062: process assignment `reg_weight_fourth` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_mac_stream_probe.v:261`
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

<a id="vg-finding-101"></a>
### VG062: process assignment `reg_weight_fifth` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_mac_stream_probe.v:268`
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

<a id="vg-finding-102"></a>
### VG062: process assignment `reg_weight_fifth` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_mac_stream_probe.v:270`
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

<a id="vg-finding-103"></a>
### VG062: process assignment `reg_weight_sixth` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_mac_stream_probe.v:277`
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

<a id="vg-finding-104"></a>
### VG062: process assignment `reg_weight_sixth` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_mac_stream_probe.v:279`
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

<a id="vg-finding-105"></a>
### VG062: process assignment `reg_bias_first` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_mac_stream_probe.v:286`
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

<a id="vg-finding-106"></a>
### VG062: process assignment `reg_bias_first` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_mac_stream_probe.v:288`
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

<a id="vg-finding-107"></a>
### VG062: process assignment `reg_bias_second` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_mac_stream_probe.v:295`
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

<a id="vg-finding-108"></a>
### VG062: process assignment `reg_bias_second` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_mac_stream_probe.v:297`
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

<a id="vg-finding-109"></a>
### VG062: process assignment `reg_bias_third` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_mac_stream_probe.v:304`
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

<a id="vg-finding-110"></a>
### VG062: process assignment `reg_bias_third` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_mac_stream_probe.v:306`
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

<a id="vg-finding-111"></a>
### VG062: process assignment `reg_control` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_mac_stream_probe.v:313`
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

<a id="vg-finding-112"></a>
### VG062: process assignment `reg_control` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_mac_stream_probe.v:315`
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

<a id="vg-finding-113"></a>
### VG065: signal `load_event_mask` must be introduced by a group comment in `其他信号`.
- Status: `failed`
- Severity: `error`
- Location: `road_mac_stream_probe.v:127`
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

<a id="vg-finding-114"></a>
### VG125: 字面量声明为 3 位，但实际值只需要 2 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_mac_stream_probe.v:177`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 3'd2
- source_excerpt: `3'd2`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
3'd2
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-115"></a>
### VG125: 字面量声明为 3 位，但实际值只需要 1 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_mac_stream_probe.v:185`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 3'd1
- source_excerpt: `3'd1`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
3'd1
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-116"></a>
### VG125: 字面量声明为 3 位，但实际值只需要 2 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_mac_stream_probe.v:186`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 3'd2
- source_excerpt: `3'd2`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
3'd2
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
- Location: `road_mac_stream_probe.v:187`
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
### VG145: 组合逻辑完整依赖锥最多允许三个源信号，超限逻辑必须由时序 reg 隔断。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_mac_stream_probe.v:147`
- Evidence:
- node_kind: `verilog_rtl`
- detail: core_weight_data: 6 sources: reg_weight_fifth, reg_weight_first, reg_weight_fourth, reg_weight_second, reg_weight_sixth, reg_weight_third
- source_excerpt: `core_weight_data: 6 sources: reg_weight_fifth, reg_weight_first, reg_weight_fourth, reg_weight_second, reg_weight_sixth, reg_weight_third`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
core_weight_data: 6 sources: reg_weight_fifth, reg_weight_first, reg_weight_fourth, reg_weight_second, reg_weight_sixth, reg_weight_third
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-119"></a>
### VG145: 组合逻辑完整依赖锥最多允许三个源信号，超限逻辑必须由时序 reg 隔断。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_mac_stream_probe.v:151`
- Evidence:
- node_kind: `verilog_rtl`
- detail: flag_command_accept: 4 sources: i_command_index, i_command_opcode, i_command_valid, reg_loaded
- source_excerpt: `flag_command_accept: 4 sources: i_command_index, i_command_opcode, i_command_valid, reg_loaded`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
flag_command_accept: 4 sources: i_command_index, i_command_opcode, i_command_valid, reg_loaded
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-120"></a>
### VG145: 组合逻辑完整依赖锥最多允许三个源信号，超限逻辑必须由时序 reg 隔断。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_mac_stream_probe.v:154`
- Evidence:
- node_kind: `verilog_rtl`
- detail: flag_load_activation_lower: 4 sources: i_command_index, i_command_opcode, i_command_valid, reg_loaded
- source_excerpt: `flag_load_activation_lower: 4 sources: i_command_index, i_command_opcode, i_command_valid, reg_loaded`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
flag_load_activation_lower: 4 sources: i_command_index, i_command_opcode, i_command_valid, reg_loaded
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-121"></a>
### VG145: 组合逻辑完整依赖锥最多允许三个源信号，超限逻辑必须由时序 reg 隔断。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_mac_stream_probe.v:155`
- Evidence:
- node_kind: `verilog_rtl`
- detail: flag_load_activation_upper: 4 sources: i_command_index, i_command_opcode, i_command_valid, reg_loaded
- source_excerpt: `flag_load_activation_upper: 4 sources: i_command_index, i_command_opcode, i_command_valid, reg_loaded`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
flag_load_activation_upper: 4 sources: i_command_index, i_command_opcode, i_command_valid, reg_loaded
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-122"></a>
### VG145: 组合逻辑完整依赖锥最多允许三个源信号，超限逻辑必须由时序 reg 隔断。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_mac_stream_probe.v:162`
- Evidence:
- node_kind: `verilog_rtl`
- detail: flag_load_bias_first: 4 sources: i_command_index, i_command_opcode, i_command_valid, reg_loaded
- source_excerpt: `flag_load_bias_first: 4 sources: i_command_index, i_command_opcode, i_command_valid, reg_loaded`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
flag_load_bias_first: 4 sources: i_command_index, i_command_opcode, i_command_valid, reg_loaded
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-123"></a>
### VG145: 组合逻辑完整依赖锥最多允许三个源信号，超限逻辑必须由时序 reg 隔断。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_mac_stream_probe.v:163`
- Evidence:
- node_kind: `verilog_rtl`
- detail: flag_load_bias_second: 4 sources: i_command_index, i_command_opcode, i_command_valid, reg_loaded
- source_excerpt: `flag_load_bias_second: 4 sources: i_command_index, i_command_opcode, i_command_valid, reg_loaded`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
flag_load_bias_second: 4 sources: i_command_index, i_command_opcode, i_command_valid, reg_loaded
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-124"></a>
### VG145: 组合逻辑完整依赖锥最多允许三个源信号，超限逻辑必须由时序 reg 隔断。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_mac_stream_probe.v:164`
- Evidence:
- node_kind: `verilog_rtl`
- detail: flag_load_bias_third: 4 sources: i_command_index, i_command_opcode, i_command_valid, reg_loaded
- source_excerpt: `flag_load_bias_third: 4 sources: i_command_index, i_command_opcode, i_command_valid, reg_loaded`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
flag_load_bias_third: 4 sources: i_command_index, i_command_opcode, i_command_valid, reg_loaded
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-125"></a>
### VG145: 组合逻辑完整依赖锥最多允许三个源信号，超限逻辑必须由时序 reg 隔断。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_mac_stream_probe.v:165`
- Evidence:
- node_kind: `verilog_rtl`
- detail: flag_load_control: 4 sources: i_command_index, i_command_opcode, i_command_valid, reg_loaded
- source_excerpt: `flag_load_control: 4 sources: i_command_index, i_command_opcode, i_command_valid, reg_loaded`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
flag_load_control: 4 sources: i_command_index, i_command_opcode, i_command_valid, reg_loaded
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-126"></a>
### VG145: 组合逻辑完整依赖锥最多允许三个源信号，超限逻辑必须由时序 reg 隔断。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_mac_stream_probe.v:160`
- Evidence:
- node_kind: `verilog_rtl`
- detail: flag_load_weight_fifth: 4 sources: i_command_index, i_command_opcode, i_command_valid, reg_loaded
- source_excerpt: `flag_load_weight_fifth: 4 sources: i_command_index, i_command_opcode, i_command_valid, reg_loaded`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
flag_load_weight_fifth: 4 sources: i_command_index, i_command_opcode, i_command_valid, reg_loaded
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-127"></a>
### VG145: 组合逻辑完整依赖锥最多允许三个源信号，超限逻辑必须由时序 reg 隔断。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_mac_stream_probe.v:156`
- Evidence:
- node_kind: `verilog_rtl`
- detail: flag_load_weight_first: 4 sources: i_command_index, i_command_opcode, i_command_valid, reg_loaded
- source_excerpt: `flag_load_weight_first: 4 sources: i_command_index, i_command_opcode, i_command_valid, reg_loaded`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
flag_load_weight_first: 4 sources: i_command_index, i_command_opcode, i_command_valid, reg_loaded
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-128"></a>
### VG145: 组合逻辑完整依赖锥最多允许三个源信号，超限逻辑必须由时序 reg 隔断。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_mac_stream_probe.v:159`
- Evidence:
- node_kind: `verilog_rtl`
- detail: flag_load_weight_fourth: 4 sources: i_command_index, i_command_opcode, i_command_valid, reg_loaded
- source_excerpt: `flag_load_weight_fourth: 4 sources: i_command_index, i_command_opcode, i_command_valid, reg_loaded`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
flag_load_weight_fourth: 4 sources: i_command_index, i_command_opcode, i_command_valid, reg_loaded
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-129"></a>
### VG145: 组合逻辑完整依赖锥最多允许三个源信号，超限逻辑必须由时序 reg 隔断。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_mac_stream_probe.v:157`
- Evidence:
- node_kind: `verilog_rtl`
- detail: flag_load_weight_second: 4 sources: i_command_index, i_command_opcode, i_command_valid, reg_loaded
- source_excerpt: `flag_load_weight_second: 4 sources: i_command_index, i_command_opcode, i_command_valid, reg_loaded`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
flag_load_weight_second: 4 sources: i_command_index, i_command_opcode, i_command_valid, reg_loaded
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-130"></a>
### VG145: 组合逻辑完整依赖锥最多允许三个源信号，超限逻辑必须由时序 reg 隔断。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_mac_stream_probe.v:161`
- Evidence:
- node_kind: `verilog_rtl`
- detail: flag_load_weight_sixth: 4 sources: i_command_index, i_command_opcode, i_command_valid, reg_loaded
- source_excerpt: `flag_load_weight_sixth: 4 sources: i_command_index, i_command_opcode, i_command_valid, reg_loaded`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
flag_load_weight_sixth: 4 sources: i_command_index, i_command_opcode, i_command_valid, reg_loaded
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-131"></a>
### VG145: 组合逻辑完整依赖锥最多允许三个源信号，超限逻辑必须由时序 reg 隔断。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_mac_stream_probe.v:158`
- Evidence:
- node_kind: `verilog_rtl`
- detail: flag_load_weight_third: 4 sources: i_command_index, i_command_opcode, i_command_valid, reg_loaded
- source_excerpt: `flag_load_weight_third: 4 sources: i_command_index, i_command_opcode, i_command_valid, reg_loaded`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
flag_load_weight_third: 4 sources: i_command_index, i_command_opcode, i_command_valid, reg_loaded
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-132"></a>
### VG145: 组合逻辑完整依赖锥最多允许三个源信号，超限逻辑必须由时序 reg 隔断。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_mac_stream_probe.v:166`
- Evidence:
- node_kind: `verilog_rtl`
- detail: load_event_mask: 4 sources: i_command_index, i_command_opcode, i_command_valid, reg_loaded
- source_excerpt: `load_event_mask: 4 sources: i_command_index, i_command_opcode, i_command_valid, reg_loaded`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
load_event_mask: 4 sources: i_command_index, i_command_opcode, i_command_valid, reg_loaded
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-133"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_mac_probe.v:47`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_mac_stream_probe.v:road_mac_stream_probe@49:1-338:1; instance_path=road_mac_stream_probe/road_mac_probe_Inst_core; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=input_ready_o$D; child_output=road_mac_stream_probe/road_mac_probe_Inst_core.input_ready_o$D; operation_count=4; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_mac_stream_probe.v:road_mac_stream_probe@49:1-338:1; instance_path=road_mac_stream_probe/road_mac_probe_Inst_core; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=input_ready_o$D; child_output=road_mac_stream_probe/road_mac_probe_Inst_core.input_ready_o$D; operation_count=4; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_mac_stream_probe.v:road_mac_stream_probe@49:1-338:1; instance_path=road_mac_stream_probe/road_mac_probe_Inst_core; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=input_ready_o$D; child_output=road_mac_stream_probe/road_mac_probe_Inst_core.input_ready_o$D; operation_count=4; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-134"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_mac_stream_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_mac_stream_probe.v:road_mac_stream_probe@49:1-338:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_activation_lower$enable; child_output=road_mac_stream_probe.reg_activation_lower$enable; operation_count=23; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_mac_stream_probe.v:road_mac_stream_probe@49:1-338:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_activation_lower$enable; child_output=road_mac_stream_probe.reg_activation_lower$enable; operation_count=23; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_mac_stream_probe.v:road_mac_stream_probe@49:1-338:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_activation_lower$enable; child_output=road_mac_stream_probe.reg_activation_lower$enable; operation_count=23; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-135"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_mac_stream_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_mac_stream_probe.v:road_mac_stream_probe@49:1-338:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_activation_upper$enable; child_output=road_mac_stream_probe.reg_activation_upper$enable; operation_count=23; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_mac_stream_probe.v:road_mac_stream_probe@49:1-338:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_activation_upper$enable; child_output=road_mac_stream_probe.reg_activation_upper$enable; operation_count=23; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_mac_stream_probe.v:road_mac_stream_probe@49:1-338:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_activation_upper$enable; child_output=road_mac_stream_probe.reg_activation_upper$enable; operation_count=23; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-136"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_mac_stream_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_mac_stream_probe.v:road_mac_stream_probe@49:1-338:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_bias_first$enable; child_output=road_mac_stream_probe.reg_bias_first$enable; operation_count=23; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_mac_stream_probe.v:road_mac_stream_probe@49:1-338:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_bias_first$enable; child_output=road_mac_stream_probe.reg_bias_first$enable; operation_count=23; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_mac_stream_probe.v:road_mac_stream_probe@49:1-338:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_bias_first$enable; child_output=road_mac_stream_probe.reg_bias_first$enable; operation_count=23; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-137"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_mac_stream_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_mac_stream_probe.v:road_mac_stream_probe@49:1-338:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_bias_second$enable; child_output=road_mac_stream_probe.reg_bias_second$enable; operation_count=23; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_mac_stream_probe.v:road_mac_stream_probe@49:1-338:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_bias_second$enable; child_output=road_mac_stream_probe.reg_bias_second$enable; operation_count=23; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_mac_stream_probe.v:road_mac_stream_probe@49:1-338:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_bias_second$enable; child_output=road_mac_stream_probe.reg_bias_second$enable; operation_count=23; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-138"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_mac_stream_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_mac_stream_probe.v:road_mac_stream_probe@49:1-338:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_bias_third$enable; child_output=road_mac_stream_probe.reg_bias_third$enable; operation_count=24; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_mac_stream_probe.v:road_mac_stream_probe@49:1-338:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_bias_third$enable; child_output=road_mac_stream_probe.reg_bias_third$enable; operation_count=24; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_mac_stream_probe.v:road_mac_stream_probe@49:1-338:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_bias_third$enable; child_output=road_mac_stream_probe.reg_bias_third$enable; operation_count=24; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-139"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_mac_stream_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_mac_stream_probe.v:road_mac_stream_probe@49:1-338:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_control$enable; child_output=road_mac_stream_probe.reg_control$enable; operation_count=23; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_mac_stream_probe.v:road_mac_stream_probe@49:1-338:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_control$enable; child_output=road_mac_stream_probe.reg_control$enable; operation_count=23; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_mac_stream_probe.v:road_mac_stream_probe@49:1-338:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_control$enable; child_output=road_mac_stream_probe.reg_control$enable; operation_count=23; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-140"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_mac_stream_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_mac_stream_probe.v:road_mac_stream_probe@49:1-338:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_loaded$D; child_output=road_mac_stream_probe.reg_loaded$D; operation_count=49; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_mac_stream_probe.v:road_mac_stream_probe@49:1-338:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_loaded$D; child_output=road_mac_stream_probe.reg_loaded$D; operation_count=49; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_mac_stream_probe.v:road_mac_stream_probe@49:1-338:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_loaded$D; child_output=road_mac_stream_probe.reg_loaded$D; operation_count=49; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-141"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_mac_stream_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_mac_stream_probe.v:road_mac_stream_probe@49:1-338:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_loaded$enable; child_output=road_mac_stream_probe.reg_loaded$enable; operation_count=23; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_mac_stream_probe.v:road_mac_stream_probe@49:1-338:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_loaded$enable; child_output=road_mac_stream_probe.reg_loaded$enable; operation_count=23; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_mac_stream_probe.v:road_mac_stream_probe@49:1-338:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_loaded$enable; child_output=road_mac_stream_probe.reg_loaded$enable; operation_count=23; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-142"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_mac_stream_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_mac_stream_probe.v:road_mac_stream_probe@49:1-338:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_weight_fifth$enable; child_output=road_mac_stream_probe.reg_weight_fifth$enable; operation_count=24; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_mac_stream_probe.v:road_mac_stream_probe@49:1-338:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_weight_fifth$enable; child_output=road_mac_stream_probe.reg_weight_fifth$enable; operation_count=24; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_mac_stream_probe.v:road_mac_stream_probe@49:1-338:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_weight_fifth$enable; child_output=road_mac_stream_probe.reg_weight_fifth$enable; operation_count=24; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-143"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_mac_stream_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_mac_stream_probe.v:road_mac_stream_probe@49:1-338:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_weight_first$enable; child_output=road_mac_stream_probe.reg_weight_first$enable; operation_count=23; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_mac_stream_probe.v:road_mac_stream_probe@49:1-338:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_weight_first$enable; child_output=road_mac_stream_probe.reg_weight_first$enable; operation_count=23; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_mac_stream_probe.v:road_mac_stream_probe@49:1-338:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_weight_first$enable; child_output=road_mac_stream_probe.reg_weight_first$enable; operation_count=23; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-144"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_mac_stream_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_mac_stream_probe.v:road_mac_stream_probe@49:1-338:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_weight_fourth$enable; child_output=road_mac_stream_probe.reg_weight_fourth$enable; operation_count=24; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_mac_stream_probe.v:road_mac_stream_probe@49:1-338:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_weight_fourth$enable; child_output=road_mac_stream_probe.reg_weight_fourth$enable; operation_count=24; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_mac_stream_probe.v:road_mac_stream_probe@49:1-338:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_weight_fourth$enable; child_output=road_mac_stream_probe.reg_weight_fourth$enable; operation_count=24; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-145"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_mac_stream_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_mac_stream_probe.v:road_mac_stream_probe@49:1-338:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_weight_second$enable; child_output=road_mac_stream_probe.reg_weight_second$enable; operation_count=23; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_mac_stream_probe.v:road_mac_stream_probe@49:1-338:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_weight_second$enable; child_output=road_mac_stream_probe.reg_weight_second$enable; operation_count=23; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_mac_stream_probe.v:road_mac_stream_probe@49:1-338:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_weight_second$enable; child_output=road_mac_stream_probe.reg_weight_second$enable; operation_count=23; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-146"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_mac_stream_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_mac_stream_probe.v:road_mac_stream_probe@49:1-338:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_weight_sixth$enable; child_output=road_mac_stream_probe.reg_weight_sixth$enable; operation_count=24; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_mac_stream_probe.v:road_mac_stream_probe@49:1-338:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_weight_sixth$enable; child_output=road_mac_stream_probe.reg_weight_sixth$enable; operation_count=24; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_mac_stream_probe.v:road_mac_stream_probe@49:1-338:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_weight_sixth$enable; child_output=road_mac_stream_probe.reg_weight_sixth$enable; operation_count=24; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-147"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_mac_stream_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_mac_stream_probe.v:road_mac_stream_probe@49:1-338:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_weight_third$enable; child_output=road_mac_stream_probe.reg_weight_third$enable; operation_count=24; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_mac_stream_probe.v:road_mac_stream_probe@49:1-338:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_weight_third$enable; child_output=road_mac_stream_probe.reg_weight_third$enable; operation_count=24; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_mac_stream_probe.v:road_mac_stream_probe@49:1-338:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_weight_third$enable; child_output=road_mac_stream_probe.reg_weight_third$enable; operation_count=24; limit=3; inconclusive_reason=none; loop_presence=absent
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
- Location: `road_mac_stream_probe.v:151`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_mac_stream_probe.v:road_mac_stream_probe@49:1-338:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_command_accept; child_output=road_mac_stream_probe.flag_command_accept; operation_count=20; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_mac_stream_probe.v:road_mac_stream_probe@49:1-338:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_command_accept; child_output=road_mac_stream_probe.flag_command_accept; operation_count=20; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_mac_stream_probe.v:road_mac_stream_probe@49:1-338:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_command_accept; child_output=road_mac_stream_probe.flag_command_accept; operation_count=20; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-149"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_mac_stream_probe.v:154`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_mac_stream_probe.v:road_mac_stream_probe@49:1-338:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_load_activation_lower; child_output=road_mac_stream_probe.flag_load_activation_lower; operation_count=22; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_mac_stream_probe.v:road_mac_stream_probe@49:1-338:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_load_activation_lower; child_output=road_mac_stream_probe.flag_load_activation_lower; operation_count=22; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_mac_stream_probe.v:road_mac_stream_probe@49:1-338:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_load_activation_lower; child_output=road_mac_stream_probe.flag_load_activation_lower; operation_count=22; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-150"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_mac_stream_probe.v:155`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_mac_stream_probe.v:road_mac_stream_probe@49:1-338:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_load_activation_upper; child_output=road_mac_stream_probe.flag_load_activation_upper; operation_count=22; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_mac_stream_probe.v:road_mac_stream_probe@49:1-338:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_load_activation_upper; child_output=road_mac_stream_probe.flag_load_activation_upper; operation_count=22; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_mac_stream_probe.v:road_mac_stream_probe@49:1-338:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_load_activation_upper; child_output=road_mac_stream_probe.flag_load_activation_upper; operation_count=22; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-151"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_mac_stream_probe.v:156`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_mac_stream_probe.v:road_mac_stream_probe@49:1-338:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_load_weight_first; child_output=road_mac_stream_probe.flag_load_weight_first; operation_count=22; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_mac_stream_probe.v:road_mac_stream_probe@49:1-338:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_load_weight_first; child_output=road_mac_stream_probe.flag_load_weight_first; operation_count=22; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_mac_stream_probe.v:road_mac_stream_probe@49:1-338:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_load_weight_first; child_output=road_mac_stream_probe.flag_load_weight_first; operation_count=22; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-152"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_mac_stream_probe.v:157`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_mac_stream_probe.v:road_mac_stream_probe@49:1-338:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_load_weight_second; child_output=road_mac_stream_probe.flag_load_weight_second; operation_count=22; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_mac_stream_probe.v:road_mac_stream_probe@49:1-338:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_load_weight_second; child_output=road_mac_stream_probe.flag_load_weight_second; operation_count=22; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_mac_stream_probe.v:road_mac_stream_probe@49:1-338:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_load_weight_second; child_output=road_mac_stream_probe.flag_load_weight_second; operation_count=22; limit=3; inconclusive_reason=none; loop_presence=absent
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
- Location: `road_mac_stream_probe.v:158`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_mac_stream_probe.v:road_mac_stream_probe@49:1-338:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_load_weight_third; child_output=road_mac_stream_probe.flag_load_weight_third; operation_count=23; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_mac_stream_probe.v:road_mac_stream_probe@49:1-338:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_load_weight_third; child_output=road_mac_stream_probe.flag_load_weight_third; operation_count=23; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_mac_stream_probe.v:road_mac_stream_probe@49:1-338:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_load_weight_third; child_output=road_mac_stream_probe.flag_load_weight_third; operation_count=23; limit=3; inconclusive_reason=none; loop_presence=absent
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
- Location: `road_mac_stream_probe.v:159`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_mac_stream_probe.v:road_mac_stream_probe@49:1-338:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_load_weight_fourth; child_output=road_mac_stream_probe.flag_load_weight_fourth; operation_count=23; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_mac_stream_probe.v:road_mac_stream_probe@49:1-338:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_load_weight_fourth; child_output=road_mac_stream_probe.flag_load_weight_fourth; operation_count=23; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_mac_stream_probe.v:road_mac_stream_probe@49:1-338:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_load_weight_fourth; child_output=road_mac_stream_probe.flag_load_weight_fourth; operation_count=23; limit=3; inconclusive_reason=none; loop_presence=absent
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
- Location: `road_mac_stream_probe.v:160`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_mac_stream_probe.v:road_mac_stream_probe@49:1-338:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_load_weight_fifth; child_output=road_mac_stream_probe.flag_load_weight_fifth; operation_count=23; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_mac_stream_probe.v:road_mac_stream_probe@49:1-338:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_load_weight_fifth; child_output=road_mac_stream_probe.flag_load_weight_fifth; operation_count=23; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_mac_stream_probe.v:road_mac_stream_probe@49:1-338:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_load_weight_fifth; child_output=road_mac_stream_probe.flag_load_weight_fifth; operation_count=23; limit=3; inconclusive_reason=none; loop_presence=absent
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
- Location: `road_mac_stream_probe.v:161`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_mac_stream_probe.v:road_mac_stream_probe@49:1-338:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_load_weight_sixth; child_output=road_mac_stream_probe.flag_load_weight_sixth; operation_count=23; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_mac_stream_probe.v:road_mac_stream_probe@49:1-338:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_load_weight_sixth; child_output=road_mac_stream_probe.flag_load_weight_sixth; operation_count=23; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_mac_stream_probe.v:road_mac_stream_probe@49:1-338:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_load_weight_sixth; child_output=road_mac_stream_probe.flag_load_weight_sixth; operation_count=23; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-157"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_mac_stream_probe.v:162`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_mac_stream_probe.v:road_mac_stream_probe@49:1-338:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_load_bias_first; child_output=road_mac_stream_probe.flag_load_bias_first; operation_count=22; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_mac_stream_probe.v:road_mac_stream_probe@49:1-338:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_load_bias_first; child_output=road_mac_stream_probe.flag_load_bias_first; operation_count=22; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_mac_stream_probe.v:road_mac_stream_probe@49:1-338:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_load_bias_first; child_output=road_mac_stream_probe.flag_load_bias_first; operation_count=22; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-158"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_mac_stream_probe.v:163`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_mac_stream_probe.v:road_mac_stream_probe@49:1-338:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_load_bias_second; child_output=road_mac_stream_probe.flag_load_bias_second; operation_count=22; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_mac_stream_probe.v:road_mac_stream_probe@49:1-338:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_load_bias_second; child_output=road_mac_stream_probe.flag_load_bias_second; operation_count=22; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_mac_stream_probe.v:road_mac_stream_probe@49:1-338:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_load_bias_second; child_output=road_mac_stream_probe.flag_load_bias_second; operation_count=22; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-159"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_mac_stream_probe.v:164`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_mac_stream_probe.v:road_mac_stream_probe@49:1-338:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_load_bias_third; child_output=road_mac_stream_probe.flag_load_bias_third; operation_count=23; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_mac_stream_probe.v:road_mac_stream_probe@49:1-338:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_load_bias_third; child_output=road_mac_stream_probe.flag_load_bias_third; operation_count=23; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_mac_stream_probe.v:road_mac_stream_probe@49:1-338:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_load_bias_third; child_output=road_mac_stream_probe.flag_load_bias_third; operation_count=23; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-160"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_mac_stream_probe.v:165`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_mac_stream_probe.v:road_mac_stream_probe@49:1-338:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_load_control; child_output=road_mac_stream_probe.flag_load_control; operation_count=22; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_mac_stream_probe.v:road_mac_stream_probe@49:1-338:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_load_control; child_output=road_mac_stream_probe.flag_load_control; operation_count=22; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_mac_stream_probe.v:road_mac_stream_probe@49:1-338:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_load_control; child_output=road_mac_stream_probe.flag_load_control; operation_count=22; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-161"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_mac_stream_probe.v:166`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_mac_stream_probe.v:road_mac_stream_probe@49:1-338:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=load_event_mask; child_output=road_mac_stream_probe.load_event_mask; operation_count=48; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_mac_stream_probe.v:road_mac_stream_probe@49:1-338:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=load_event_mask; child_output=road_mac_stream_probe.load_event_mask; operation_count=48; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_mac_stream_probe.v:road_mac_stream_probe@49:1-338:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=load_event_mask; child_output=road_mac_stream_probe.load_event_mask; operation_count=48; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-162"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_mac_stream_probe.v:175`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_mac_stream_probe.v:road_mac_stream_probe@49:1-338:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_activation_address; child_output=road_mac_stream_probe.flag_activation_address; operation_count=5; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_mac_stream_probe.v:road_mac_stream_probe@49:1-338:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_activation_address; child_output=road_mac_stream_probe.flag_activation_address; operation_count=5; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_mac_stream_probe.v:road_mac_stream_probe@49:1-338:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_activation_address; child_output=road_mac_stream_probe.flag_activation_address; operation_count=5; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-163"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_mac_stream_probe.v:179`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_mac_stream_probe.v:road_mac_stream_probe@49:1-338:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_address_lower; child_output=road_mac_stream_probe.flag_address_lower; operation_count=9; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_mac_stream_probe.v:road_mac_stream_probe@49:1-338:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_address_lower; child_output=road_mac_stream_probe.flag_address_lower; operation_count=9; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_mac_stream_probe.v:road_mac_stream_probe@49:1-338:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_address_lower; child_output=road_mac_stream_probe.flag_address_lower; operation_count=9; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-164"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_mac_stream_probe.v:180`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_mac_stream_probe.v:road_mac_stream_probe@49:1-338:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_address_upper; child_output=road_mac_stream_probe.flag_address_upper; operation_count=7; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_mac_stream_probe.v:road_mac_stream_probe@49:1-338:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_address_upper; child_output=road_mac_stream_probe.flag_address_upper; operation_count=7; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_mac_stream_probe.v:road_mac_stream_probe@49:1-338:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_address_upper; child_output=road_mac_stream_probe.flag_address_upper; operation_count=7; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-165"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_mac_stream_probe.v:181`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_mac_stream_probe.v:road_mac_stream_probe@49:1-338:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_command_address; child_output=road_mac_stream_probe.flag_command_address; operation_count=16; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_mac_stream_probe.v:road_mac_stream_probe@49:1-338:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_command_address; child_output=road_mac_stream_probe.flag_command_address; operation_count=16; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_mac_stream_probe.v:road_mac_stream_probe@49:1-338:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_command_address; child_output=road_mac_stream_probe.flag_command_address; operation_count=16; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-166"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_mac_stream_probe.v:194`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_mac_stream_probe.v:road_mac_stream_probe@49:1-338:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=o_command_ready; child_output=road_mac_stream_probe.o_command_ready; operation_count=19; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_mac_stream_probe.v:road_mac_stream_probe@49:1-338:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=o_command_ready; child_output=road_mac_stream_probe.o_command_ready; operation_count=19; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_mac_stream_probe.v:road_mac_stream_probe@49:1-338:1; instance_path=road_mac_stream_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=o_command_ready; child_output=road_mac_stream_probe.o_command_ready; operation_count=19; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-167"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_mac_stream_probe.v:124`
- Evidence:
- node_kind: `verilog_rtl`
- detail: flag_core_input_ready
- source_excerpt: `flag_core_input_ready`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
flag_core_input_ready
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-168"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_mac_stream_probe.v:135`
- Evidence:
- node_kind: `verilog_rtl`
- detail: result_valid_o
- source_excerpt: `result_valid_o`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
result_valid_o
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-169"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_mac_stream_probe.v:136`
- Evidence:
- node_kind: `verilog_rtl`
- detail: result_data_o
- source_excerpt: `result_data_o`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
result_data_o
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-170"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_mac_stream_probe.v:137`
- Evidence:
- node_kind: `verilog_rtl`
- detail: fault_o
- source_excerpt: `fault_o`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
fault_o
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-171"></a>
### VG157: 普通 RTL 注释不得携带版本字样；版本历史只能位于 formatter 固定文件头范围。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_mac_stream_probe.v:19`
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

<a id="vg-finding-172"></a>
### VG157: 普通 RTL 注释不得携带版本字样；版本历史只能位于 formatter 固定文件头范围。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_mac_stream_probe.v:42`
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
| error | COMMENT_COMMENT_PLACEMENT | `road_mac_stream_probe.v:142` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_mac_stream_probe.v:143` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_mac_stream_probe.v:146` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_mac_stream_probe.v:147` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_mac_stream_probe.v:148` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_mac_stream_probe.v:151` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_mac_stream_probe.v:154` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_mac_stream_probe.v:155` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_mac_stream_probe.v:156` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_mac_stream_probe.v:157` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_mac_stream_probe.v:158` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_mac_stream_probe.v:159` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_mac_stream_probe.v:160` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_mac_stream_probe.v:161` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_mac_stream_probe.v:162` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_mac_stream_probe.v:163` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_mac_stream_probe.v:164` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_mac_stream_probe.v:165` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_mac_stream_probe.v:166` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_mac_stream_probe.v:169` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_mac_stream_probe.v:170` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_mac_stream_probe.v:171` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_mac_stream_probe.v:172` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_mac_stream_probe.v:175` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_mac_stream_probe.v:176` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_mac_stream_probe.v:177` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_mac_stream_probe.v:178` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_mac_stream_probe.v:179` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_mac_stream_probe.v:180` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_mac_stream_probe.v:181` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_mac_stream_probe.v:184` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_mac_stream_probe.v:185` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_mac_stream_probe.v:186` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_mac_stream_probe.v:187` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_mac_stream_probe.v:188` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_mac_stream_probe.v:189` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_mac_stream_probe.v:194` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_mac_stream_probe.v:195` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_mac_stream_probe.v:196` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_mac_stream_probe.v:197` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_mac_stream_probe.v:321` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
