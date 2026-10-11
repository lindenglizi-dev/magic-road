# Verilog deliverable gate

Root: `E:\project\qiansai\anlogic_topic2_work\lab1_sc500_road_vision\cnn\hw_validation\production\reports\v8_reset_layer_tiles_20261007\reset\road_low_io_reset_shell.v`
Delivery ready: `False`
Summary: **54 error(s)**, **0 strict warning(s)**

## Actionable VG findings

<a id="vg-finding-1"></a>
### VG068: English References/Dependencies section must match exact `none_mode` or `table_mode` layout.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_reset_shell.v:1`
- Evidence:
- node_kind: `verilog_rtl`
- detail: header.reference_dependency_shape
- source_excerpt: `header.reference_dependency_shape`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
header.reference_dependency_shape
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-2"></a>
### VG068: Chinese References/Dependencies section must match exact `none_mode` or `table_mode` layout.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_reset_shell.v:1`
- Evidence:
- node_kind: `verilog_rtl`
- detail: header.reference_dependency_shape
- source_excerpt: `header.reference_dependency_shape`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
header.reference_dependency_shape
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-3"></a>
### VG068: Header Description/Simulations fields must use the fixed bilingual path contract (`description/testbench` in English and `Description/TestBench` in Chinese).
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_reset_shell.v:1`
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

<a id="vg-finding-4"></a>
### VG060: Inline comment must start at display column 46, aligned from region anchor column 46; got 47.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_reset_shell.v:69`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.region_anchor
- source_excerpt: `comments.region_anchor`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.region_anchor
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-5"></a>
### VG060: Inline comment must start at display column 46, aligned from region anchor column 46; got 47.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_reset_shell.v:70`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.region_anchor
- source_excerpt: `comments.region_anchor`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.region_anchor
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-6"></a>
### VG060: Inline comment must start at display column 44, aligned from region anchor column 44; got 47.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_reset_shell.v:74`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.region_anchor
- source_excerpt: `comments.region_anchor`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.region_anchor
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-7"></a>
### VG060: Inline comment must start at display column 44, aligned from region anchor column 44; got 47.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_reset_shell.v:75`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.region_anchor
- source_excerpt: `comments.region_anchor`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.region_anchor
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-8"></a>
### VG060: Inline comment must start at display column 44, aligned from region anchor column 44; got 47.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_reset_shell.v:76`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.region_anchor
- source_excerpt: `comments.region_anchor`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.region_anchor
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-9"></a>
### VG060: Inline comment must start at display column 44, aligned from region anchor column 44; got 47.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_reset_shell.v:77`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.region_anchor
- source_excerpt: `comments.region_anchor`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.region_anchor
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-10"></a>
### VG060: Inline comment must start at display column 44, aligned from region anchor column 44; got 47.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_reset_shell.v:78`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.region_anchor
- source_excerpt: `comments.region_anchor`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.region_anchor
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-11"></a>
### VG060: Inline comment must start at display column 44, aligned from region anchor column 44; got 47.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_reset_shell.v:79`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.region_anchor
- source_excerpt: `comments.region_anchor`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.region_anchor
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-12"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 47.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_reset_shell.v:83`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.region_anchor
- source_excerpt: `comments.region_anchor`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.region_anchor
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-13"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 47.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_reset_shell.v:87`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.region_anchor
- source_excerpt: `comments.region_anchor`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.region_anchor
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-14"></a>
### VG060: Inline comment must start at display column 44, aligned from region anchor column 44; got 51.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_reset_shell.v:102`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.region_anchor
- source_excerpt: `comments.region_anchor`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.region_anchor
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-15"></a>
### VG060: Inline comment must start at display column 44, aligned from region anchor column 44; got 51.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_reset_shell.v:104`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.region_anchor
- source_excerpt: `comments.region_anchor`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.region_anchor
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-16"></a>
### VG060: Inline comment must start at display column 44, aligned from region anchor column 44; got 51.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_reset_shell.v:111`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.region_anchor
- source_excerpt: `comments.region_anchor`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.region_anchor
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-17"></a>
### VG013: Flag-like signal `reg_release_done` should use `flag_` prefix unless it is an output bridge.
- Status: `failed`
- Severity: `error`
- Location: `file:road_low_io_reset_shell.v:unknown`
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

<a id="vg-finding-18"></a>
### VG013: Flag-like signal `shell_rx_ready` should use `flag_` prefix unless it is an output bridge.
- Status: `failed`
- Severity: `error`
- Location: `file:road_low_io_reset_shell.v:unknown`
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

<a id="vg-finding-19"></a>
### VG013: Flag-like signal `shell_tx_valid` should use `flag_` prefix unless it is an output bridge.
- Status: `failed`
- Severity: `error`
- Location: `file:road_low_io_reset_shell.v:unknown`
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

<a id="vg-finding-20"></a>
### VG013: Flag-like signal `shell_rx_valid` should use `flag_` prefix unless it is an output bridge.
- Status: `failed`
- Severity: `error`
- Location: `file:road_low_io_reset_shell.v:unknown`
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

<a id="vg-finding-21"></a>
### VG013: Flag-like signal `shell_tx_ready` should use `flag_` prefix unless it is an output bridge.
- Status: `failed`
- Severity: `error`
- Location: `file:road_low_io_reset_shell.v:unknown`
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

<a id="vg-finding-22"></a>
### VG031: Region banners appear out of the required order.
- Status: `failed`
- Severity: `error`
- Location: `file:road_low_io_reset_shell.v:unknown`
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

<a id="vg-finding-23"></a>
### VG031: Module instances must stay inside the 模块实例化区域 banner.
- Status: `failed`
- Severity: `error`
- Location: `file:road_low_io_reset_shell.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: regions.instances_last
- source_excerpt: `regions.instances_last`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `architecture`; human review required: `True`
- Example 1 kind: `structure`
- Bad example:
```text
regions.instances_last
```
- Good example:
```text
调整结构关系后重新检查组合锥、实例连接和相关下游节点。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-24"></a>
### VG061: Item `road_low_io_physical_shell_Inst_reset` must be placed in 模块实例化区域, not `主要任务处理区域`.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_reset_shell.v:119`
- Evidence:
- node_kind: `verilog_rtl`
- detail: regions.instance
- source_excerpt: `regions.instance`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `interface`; human review required: `True`
- Example 1 kind: `structure`
- Bad example:
```text
regions.instance
```
- Good example:
```text
调整结构关系后重新检查组合锥、实例连接和相关下游节点。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-25"></a>
### VG070: `输出信号连线` item `o_rx_ready` must use group label `RX接口`, not `unknown`.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_reset_shell.v:94`
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

<a id="vg-finding-26"></a>
### VG066: Comment for assign `o_tx_valid` repeats or closely reuses comment from assign `o_rx_ready`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_reset_shell.v:95`
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

<a id="vg-finding-27"></a>
### VG066: Comment for process assignment `reg_release_done` repeats or closely reuses comment from process assignment `reg_release_meta`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_reset_shell.v:111`
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

<a id="vg-finding-28"></a>
### VG093: 异步复位信号被连接到普通数据赋值右值。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_reset_shell.v:88`
- Evidence:
- node_kind: `verilog_rtl`
- detail: flag_interface_open = i_rstn & reg_release_done
- source_excerpt: `flag_interface_open = i_rstn & reg_release_done`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
flag_interface_open = i_rstn & reg_release_done
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-29"></a>
### VG099: 复位产生逻辑内联在功能模块中，建议封装为独立复位模块。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_low_io_reset_shell.v:87`
- Evidence:
- node_kind: `verilog_rtl`
- detail: assign shell_rstn = reg_release_done;
- source_excerpt: `assign shell_rstn = reg_release_done;`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
assign shell_rstn = reg_release_done;
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-30"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_low_io_reset_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_reset_shell.v:road_low_io_reset_shell@49:1-130:1; instance_path=road_low_io_reset_shell; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=shell_rx_ready; child_output=road_low_io_reset_shell.shell_rx_ready; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_reset_shell.v:road_low_io_reset_shell@49:1-130:1; instance_path=road_low_io_reset_shell; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=shell_rx_ready; child_output=road_low_io_reset_shell.shell_rx_ready; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_reset_shell.v:road_low_io_reset_shell@49:1-130:1; instance_path=road_low_io_reset_shell; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=shell_rx_ready; child_output=road_low_io_reset_shell.shell_rx_ready; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-31"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_low_io_reset_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_reset_shell.v:road_low_io_reset_shell@49:1-130:1; instance_path=road_low_io_reset_shell; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=shell_tx_data; child_output=road_low_io_reset_shell.shell_tx_data; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_reset_shell.v:road_low_io_reset_shell@49:1-130:1; instance_path=road_low_io_reset_shell; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=shell_tx_data; child_output=road_low_io_reset_shell.shell_tx_data; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_reset_shell.v:road_low_io_reset_shell@49:1-130:1; instance_path=road_low_io_reset_shell; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=shell_tx_data; child_output=road_low_io_reset_shell.shell_tx_data; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-32"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_low_io_reset_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_reset_shell.v:road_low_io_reset_shell@49:1-130:1; instance_path=road_low_io_reset_shell; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=shell_tx_valid; child_output=road_low_io_reset_shell.shell_tx_valid; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_reset_shell.v:road_low_io_reset_shell@49:1-130:1; instance_path=road_low_io_reset_shell; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=shell_tx_valid; child_output=road_low_io_reset_shell.shell_tx_valid; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_reset_shell.v:road_low_io_reset_shell@49:1-130:1; instance_path=road_low_io_reset_shell; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=shell_tx_valid; child_output=road_low_io_reset_shell.shell_tx_valid; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-33"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_low_io_reset_shell.v:87`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_reset_shell.v:road_low_io_reset_shell@49:1-130:1; instance_path=road_low_io_reset_shell; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=shell_rstn; child_output=road_low_io_reset_shell.shell_rstn; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_reset_shell.v:road_low_io_reset_shell@49:1-130:1; instance_path=road_low_io_reset_shell; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=shell_rstn; child_output=road_low_io_reset_shell.shell_rstn; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_reset_shell.v:road_low_io_reset_shell@49:1-130:1; instance_path=road_low_io_reset_shell; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=shell_rstn; child_output=road_low_io_reset_shell.shell_rstn; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-34"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_low_io_reset_shell.v:89`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_reset_shell.v:road_low_io_reset_shell@49:1-130:1; instance_path=road_low_io_reset_shell; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=shell_rx_valid; child_output=road_low_io_reset_shell.shell_rx_valid; operation_count=2; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_reset_shell.v:road_low_io_reset_shell@49:1-130:1; instance_path=road_low_io_reset_shell; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=shell_rx_valid; child_output=road_low_io_reset_shell.shell_rx_valid; operation_count=2; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_reset_shell.v:road_low_io_reset_shell@49:1-130:1; instance_path=road_low_io_reset_shell; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=shell_rx_valid; child_output=road_low_io_reset_shell.shell_rx_valid; operation_count=2; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-35"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_low_io_reset_shell.v:90`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_reset_shell.v:road_low_io_reset_shell@49:1-130:1; instance_path=road_low_io_reset_shell; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=shell_tx_ready; child_output=road_low_io_reset_shell.shell_tx_ready; operation_count=2; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_reset_shell.v:road_low_io_reset_shell@49:1-130:1; instance_path=road_low_io_reset_shell; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=shell_tx_ready; child_output=road_low_io_reset_shell.shell_tx_ready; operation_count=2; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_reset_shell.v:road_low_io_reset_shell@49:1-130:1; instance_path=road_low_io_reset_shell; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=shell_tx_ready; child_output=road_low_io_reset_shell.shell_tx_ready; operation_count=2; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-36"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_low_io_reset_shell.v:94`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_reset_shell.v:road_low_io_reset_shell@49:1-130:1; instance_path=road_low_io_reset_shell; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=o_rx_ready; child_output=road_low_io_reset_shell.o_rx_ready; operation_count=2; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_reset_shell.v:road_low_io_reset_shell@49:1-130:1; instance_path=road_low_io_reset_shell; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=o_rx_ready; child_output=road_low_io_reset_shell.o_rx_ready; operation_count=2; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_reset_shell.v:road_low_io_reset_shell@49:1-130:1; instance_path=road_low_io_reset_shell; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=o_rx_ready; child_output=road_low_io_reset_shell.o_rx_ready; operation_count=2; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-37"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_low_io_reset_shell.v:95`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_reset_shell.v:road_low_io_reset_shell@49:1-130:1; instance_path=road_low_io_reset_shell; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=o_tx_valid; child_output=road_low_io_reset_shell.o_tx_valid; operation_count=2; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_reset_shell.v:road_low_io_reset_shell@49:1-130:1; instance_path=road_low_io_reset_shell; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=o_tx_valid; child_output=road_low_io_reset_shell.o_tx_valid; operation_count=2; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_reset_shell.v:road_low_io_reset_shell@49:1-130:1; instance_path=road_low_io_reset_shell; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=o_tx_valid; child_output=road_low_io_reset_shell.o_tx_valid; operation_count=2; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-38"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_low_io_reset_shell.v:96`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_reset_shell.v:road_low_io_reset_shell@49:1-130:1; instance_path=road_low_io_reset_shell; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=o_tx_data; child_output=road_low_io_reset_shell.o_tx_data; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_reset_shell.v:road_low_io_reset_shell@49:1-130:1; instance_path=road_low_io_reset_shell; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=o_tx_data; child_output=road_low_io_reset_shell.o_tx_data; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_reset_shell.v:road_low_io_reset_shell@49:1-130:1; instance_path=road_low_io_reset_shell; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=o_tx_data; child_output=road_low_io_reset_shell.o_tx_data; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-39"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_low_io_reset_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_reset_shell.v:road_low_io_reset_shell@49:1-130:1; instance_path=road_low_io_reset_shell; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=shell_rx_ready; child_output=road_low_io_reset_shell.shell_rx_ready; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_reset_shell.v:road_low_io_reset_shell@49:1-130:1; instance_path=road_low_io_reset_shell; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=shell_rx_ready; child_output=road_low_io_reset_shell.shell_rx_ready; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_reset_shell.v:road_low_io_reset_shell@49:1-130:1; instance_path=road_low_io_reset_shell; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=shell_rx_ready; child_output=road_low_io_reset_shell.shell_rx_ready; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-40"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_low_io_reset_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_reset_shell.v:road_low_io_reset_shell@49:1-130:1; instance_path=road_low_io_reset_shell; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=shell_tx_data; child_output=road_low_io_reset_shell.shell_tx_data; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_reset_shell.v:road_low_io_reset_shell@49:1-130:1; instance_path=road_low_io_reset_shell; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=shell_tx_data; child_output=road_low_io_reset_shell.shell_tx_data; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_reset_shell.v:road_low_io_reset_shell@49:1-130:1; instance_path=road_low_io_reset_shell; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=shell_tx_data; child_output=road_low_io_reset_shell.shell_tx_data; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-41"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_low_io_reset_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_reset_shell.v:road_low_io_reset_shell@49:1-130:1; instance_path=road_low_io_reset_shell; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=shell_tx_valid; child_output=road_low_io_reset_shell.shell_tx_valid; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_reset_shell.v:road_low_io_reset_shell@49:1-130:1; instance_path=road_low_io_reset_shell; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=shell_tx_valid; child_output=road_low_io_reset_shell.shell_tx_valid; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_reset_shell.v:road_low_io_reset_shell@49:1-130:1; instance_path=road_low_io_reset_shell; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=shell_tx_valid; child_output=road_low_io_reset_shell.shell_tx_valid; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-42"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_low_io_reset_shell.v:87`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_reset_shell.v:road_low_io_reset_shell@49:1-130:1; instance_path=road_low_io_reset_shell; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=shell_rstn; child_output=road_low_io_reset_shell.shell_rstn; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_reset_shell.v:road_low_io_reset_shell@49:1-130:1; instance_path=road_low_io_reset_shell; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=shell_rstn; child_output=road_low_io_reset_shell.shell_rstn; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_reset_shell.v:road_low_io_reset_shell@49:1-130:1; instance_path=road_low_io_reset_shell; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=shell_rstn; child_output=road_low_io_reset_shell.shell_rstn; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-43"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_low_io_reset_shell.v:89`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_reset_shell.v:road_low_io_reset_shell@49:1-130:1; instance_path=road_low_io_reset_shell; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=shell_rx_valid; child_output=road_low_io_reset_shell.shell_rx_valid; operation_count=2; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_reset_shell.v:road_low_io_reset_shell@49:1-130:1; instance_path=road_low_io_reset_shell; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=shell_rx_valid; child_output=road_low_io_reset_shell.shell_rx_valid; operation_count=2; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_reset_shell.v:road_low_io_reset_shell@49:1-130:1; instance_path=road_low_io_reset_shell; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=shell_rx_valid; child_output=road_low_io_reset_shell.shell_rx_valid; operation_count=2; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-44"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_low_io_reset_shell.v:90`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_reset_shell.v:road_low_io_reset_shell@49:1-130:1; instance_path=road_low_io_reset_shell; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=shell_tx_ready; child_output=road_low_io_reset_shell.shell_tx_ready; operation_count=2; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_reset_shell.v:road_low_io_reset_shell@49:1-130:1; instance_path=road_low_io_reset_shell; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=shell_tx_ready; child_output=road_low_io_reset_shell.shell_tx_ready; operation_count=2; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_reset_shell.v:road_low_io_reset_shell@49:1-130:1; instance_path=road_low_io_reset_shell; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=shell_tx_ready; child_output=road_low_io_reset_shell.shell_tx_ready; operation_count=2; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-45"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_low_io_reset_shell.v:94`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_reset_shell.v:road_low_io_reset_shell@49:1-130:1; instance_path=road_low_io_reset_shell; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=o_rx_ready; child_output=road_low_io_reset_shell.o_rx_ready; operation_count=2; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_reset_shell.v:road_low_io_reset_shell@49:1-130:1; instance_path=road_low_io_reset_shell; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=o_rx_ready; child_output=road_low_io_reset_shell.o_rx_ready; operation_count=2; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_reset_shell.v:road_low_io_reset_shell@49:1-130:1; instance_path=road_low_io_reset_shell; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=o_rx_ready; child_output=road_low_io_reset_shell.o_rx_ready; operation_count=2; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-46"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_low_io_reset_shell.v:95`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_reset_shell.v:road_low_io_reset_shell@49:1-130:1; instance_path=road_low_io_reset_shell; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=o_tx_valid; child_output=road_low_io_reset_shell.o_tx_valid; operation_count=2; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_reset_shell.v:road_low_io_reset_shell@49:1-130:1; instance_path=road_low_io_reset_shell; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=o_tx_valid; child_output=road_low_io_reset_shell.o_tx_valid; operation_count=2; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_reset_shell.v:road_low_io_reset_shell@49:1-130:1; instance_path=road_low_io_reset_shell; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=o_tx_valid; child_output=road_low_io_reset_shell.o_tx_valid; operation_count=2; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-47"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_low_io_reset_shell.v:96`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_reset_shell.v:road_low_io_reset_shell@49:1-130:1; instance_path=road_low_io_reset_shell; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=o_tx_data; child_output=road_low_io_reset_shell.o_tx_data; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_reset_shell.v:road_low_io_reset_shell@49:1-130:1; instance_path=road_low_io_reset_shell; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=o_tx_data; child_output=road_low_io_reset_shell.o_tx_data; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_reset_shell.v:road_low_io_reset_shell@49:1-130:1; instance_path=road_low_io_reset_shell; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=o_tx_data; child_output=road_low_io_reset_shell.o_tx_data; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-48"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_reset_shell.v:74`
- Evidence:
- node_kind: `verilog_rtl`
- detail: shell_rx_ready
- source_excerpt: `shell_rx_ready`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
shell_rx_ready
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-49"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_reset_shell.v:75`
- Evidence:
- node_kind: `verilog_rtl`
- detail: shell_tx_valid
- source_excerpt: `shell_tx_valid`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
shell_tx_valid
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-50"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_reset_shell.v:76`
- Evidence:
- node_kind: `verilog_rtl`
- detail: shell_tx_data
- source_excerpt: `shell_tx_data`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
shell_tx_data
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-51"></a>
### VG157: 普通 RTL 注释不得携带版本字样；版本历史只能位于 formatter 固定文件头范围。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_reset_shell.v:19`
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

<a id="vg-finding-52"></a>
### VG157: 普通 RTL 注释不得携带版本字样；版本历史只能位于 formatter 固定文件头范围。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_reset_shell.v:42`
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
| error | COMMENT_COMMENT_PLACEMENT | `road_low_io_reset_shell.v:119` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
