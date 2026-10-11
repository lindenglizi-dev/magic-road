# Verilog deliverable gate

Root: `E:\project\qiansai\anlogic_topic2_work\lab1_sc500_road_vision\cnn\hw_validation\production\reports\runtime_layer_integration_20261009\physical\layer_shell`
Delivery ready: `False`
Summary: **782 error(s)**, **0 strict warning(s)**

## Actionable VG findings

<a id="vg-finding-1"></a>
### VG068: English References/Dependencies section must match exact `none_mode` or `table_mode` layout.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:1`
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
- Location: `road_dynamic_overlap_low_io_top.v:1`
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
- Location: `road_dynamic_overlap_low_io_top.v:1`
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
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 49.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:93`
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
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 49.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:94`
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
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 49.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:102`
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
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 49.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:103`
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
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 49.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:104`
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
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 49.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:105`
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
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 49.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:106`
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
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 49.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:115`
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
### VG025: Control statements must use explicit begin/end blocks.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:240`
- Evidence:
- node_kind: `verilog_rtl`
- detail: control.begin_end
- source_excerpt: `control.begin_end`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
control.begin_end
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-13"></a>
### VG025: Control statements must use explicit begin/end blocks.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:241`
- Evidence:
- node_kind: `verilog_rtl`
- detail: control.begin_end
- source_excerpt: `control.begin_end`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
control.begin_end
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-14"></a>
### VG025: Control statements must use explicit begin/end blocks.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:242`
- Evidence:
- node_kind: `verilog_rtl`
- detail: control.begin_end
- source_excerpt: `control.begin_end`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
control.begin_end
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-15"></a>
### VG025: Control statements must use explicit begin/end blocks.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:243`
- Evidence:
- node_kind: `verilog_rtl`
- detail: control.begin_end
- source_excerpt: `control.begin_end`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
control.begin_end
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-16"></a>
### VG025: Control statements must use explicit begin/end blocks.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:244`
- Evidence:
- node_kind: `verilog_rtl`
- detail: control.begin_end
- source_excerpt: `control.begin_end`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
control.begin_end
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-17"></a>
### VG025: Control statements must use explicit begin/end blocks.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:245`
- Evidence:
- node_kind: `verilog_rtl`
- detail: control.begin_end
- source_excerpt: `control.begin_end`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
control.begin_end
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-18"></a>
### VG025: Control statements must use explicit begin/end blocks.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:246`
- Evidence:
- node_kind: `verilog_rtl`
- detail: control.begin_end
- source_excerpt: `control.begin_end`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
control.begin_end
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-19"></a>
### VG025: Control statements must use explicit begin/end blocks.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:247`
- Evidence:
- node_kind: `verilog_rtl`
- detail: control.begin_end
- source_excerpt: `control.begin_end`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
control.begin_end
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-20"></a>
### VG025: Control statements must use explicit begin/end blocks.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:356`
- Evidence:
- node_kind: `verilog_rtl`
- detail: control.begin_end
- source_excerpt: `control.begin_end`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
control.begin_end
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-21"></a>
### VG025: Control statements must use explicit begin/end blocks.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:357`
- Evidence:
- node_kind: `verilog_rtl`
- detail: control.begin_end
- source_excerpt: `control.begin_end`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
control.begin_end
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-22"></a>
### VG025: Control statements must use explicit begin/end blocks.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:358`
- Evidence:
- node_kind: `verilog_rtl`
- detail: control.begin_end
- source_excerpt: `control.begin_end`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
control.begin_end
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-23"></a>
### VG025: Control statements must use explicit begin/end blocks.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:359`
- Evidence:
- node_kind: `verilog_rtl`
- detail: control.begin_end
- source_excerpt: `control.begin_end`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
control.begin_end
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-24"></a>
### VG025: Control statements must use explicit begin/end blocks.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:360`
- Evidence:
- node_kind: `verilog_rtl`
- detail: control.begin_end
- source_excerpt: `control.begin_end`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
control.begin_end
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-25"></a>
### VG025: Control statements must use explicit begin/end blocks.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:427`
- Evidence:
- node_kind: `verilog_rtl`
- detail: control.begin_end
- source_excerpt: `control.begin_end`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
control.begin_end
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-26"></a>
### VG025: Control statements must use explicit begin/end blocks.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:471`
- Evidence:
- node_kind: `verilog_rtl`
- detail: control.begin_end
- source_excerpt: `control.begin_end`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
control.begin_end
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-27"></a>
### VG025: Control statements must use explicit begin/end blocks.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:472`
- Evidence:
- node_kind: `verilog_rtl`
- detail: control.begin_end
- source_excerpt: `control.begin_end`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
control.begin_end
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-28"></a>
### VG013: Flag-like signal `reg_release_done` should use `flag_` prefix unless it is an output bridge.
- Status: `failed`
- Severity: `error`
- Location: `file:road_dynamic_overlap_low_io_top.v:unknown`
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

<a id="vg-finding-29"></a>
### VG013: Flag-like signal `reg_load_pending` should use `flag_` prefix unless it is an output bridge.
- Status: `failed`
- Severity: `error`
- Location: `file:road_dynamic_overlap_low_io_top.v:unknown`
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

<a id="vg-finding-30"></a>
### VG013: Flag-like signal `reg_export_done_seen` should use `flag_` prefix unless it is an output bridge.
- Status: `failed`
- Severity: `error`
- Location: `file:road_dynamic_overlap_low_io_top.v:unknown`
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

<a id="vg-finding-31"></a>
### VG013: Flag-like signal `reg_runner_done_seen` should use `flag_` prefix unless it is an output bridge.
- Status: `failed`
- Severity: `error`
- Location: `file:road_dynamic_overlap_low_io_top.v:unknown`
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

<a id="vg-finding-32"></a>
### VG013: Flag-like signal `reg_commit_ready` should use `flag_` prefix unless it is an output bridge.
- Status: `failed`
- Severity: `error`
- Location: `file:road_dynamic_overlap_low_io_top.v:unknown`
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

<a id="vg-finding-33"></a>
### VG013: Flag-like signal `reg_snapshot_flags` should use `flag_` prefix unless it is an output bridge.
- Status: `failed`
- Severity: `error`
- Location: `file:road_dynamic_overlap_low_io_top.v:unknown`
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

<a id="vg-finding-34"></a>
### VG013: Flag-like signal `reg_snapshot_writeback_cycles` should use `flag_` prefix unless it is an output bridge.
- Status: `failed`
- Severity: `error`
- Location: `file:road_dynamic_overlap_low_io_top.v:unknown`
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

<a id="vg-finding-35"></a>
### VG013: Flag-like signal `reg_snapshot_writebacks` should use `flag_` prefix unless it is an output bridge.
- Status: `failed`
- Severity: `error`
- Location: `file:road_dynamic_overlap_low_io_top.v:unknown`
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

<a id="vg-finding-36"></a>
### VG013: Flag-like signal `runner_table_ready` should use `flag_` prefix unless it is an output bridge.
- Status: `failed`
- Severity: `error`
- Location: `file:road_dynamic_overlap_low_io_top.v:unknown`
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

<a id="vg-finding-37"></a>
### VG013: Flag-like signal `runner_load_ready` should use `flag_` prefix unless it is an output bridge.
- Status: `failed`
- Severity: `error`
- Location: `file:road_dynamic_overlap_low_io_top.v:unknown`
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

<a id="vg-finding-38"></a>
### VG013: Flag-like signal `runner_done` should use `flag_` prefix unless it is an output bridge.
- Status: `failed`
- Severity: `error`
- Location: `file:road_dynamic_overlap_low_io_top.v:unknown`
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

<a id="vg-finding-39"></a>
### VG013: Flag-like signal `runner_output_valid` should use `flag_` prefix unless it is an output bridge.
- Status: `failed`
- Severity: `error`
- Location: `file:road_dynamic_overlap_low_io_top.v:unknown`
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

<a id="vg-finding-40"></a>
### VG013: Flag-like signal `runner_export_done` should use `flag_` prefix unless it is an output bridge.
- Status: `failed`
- Severity: `error`
- Location: `file:road_dynamic_overlap_low_io_top.v:unknown`
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

<a id="vg-finding-41"></a>
### VG013: Flag-like signal `runner_debug_valid` should use `flag_` prefix unless it is an output bridge.
- Status: `failed`
- Severity: `error`
- Location: `file:road_dynamic_overlap_low_io_top.v:unknown`
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

<a id="vg-finding-42"></a>
### VG013: Flag-like signal `runner_writeback_cycles` should use `flag_` prefix unless it is an output bridge.
- Status: `failed`
- Severity: `error`
- Location: `file:road_dynamic_overlap_low_io_top.v:unknown`
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

<a id="vg-finding-43"></a>
### VG013: Counter-like signal `runner_result_queue_count` should use `cnt_` prefix.
- Status: `failed`
- Severity: `error`
- Location: `file:road_dynamic_overlap_low_io_top.v:unknown`
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

<a id="vg-finding-44"></a>
### VG013: Counter-like signal `runner_meta_count` should use `cnt_` prefix.
- Status: `failed`
- Severity: `error`
- Location: `file:road_dynamic_overlap_low_io_top.v:unknown`
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

<a id="vg-finding-45"></a>
### VG013: Counter-like signal `runner_mac_result_count` should use `cnt_` prefix.
- Status: `failed`
- Severity: `error`
- Location: `file:road_dynamic_overlap_low_io_top.v:unknown`
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

<a id="vg-finding-46"></a>
### VG013: Counter-like signal `runner_pre_accept_count` should use `cnt_` prefix.
- Status: `failed`
- Severity: `error`
- Location: `file:road_dynamic_overlap_low_io_top.v:unknown`
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

<a id="vg-finding-47"></a>
### VG013: Counter-like signal `runner_silu_accept_count` should use `cnt_` prefix.
- Status: `failed`
- Severity: `error`
- Location: `file:road_dynamic_overlap_low_io_top.v:unknown`
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

<a id="vg-finding-48"></a>
### VG013: Counter-like signal `runner_post_accept_count` should use `cnt_` prefix.
- Status: `failed`
- Severity: `error`
- Location: `file:road_dynamic_overlap_low_io_top.v:unknown`
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

<a id="vg-finding-49"></a>
### VG013: Counter-like signal `runner_writeback_count` should use `cnt_` prefix.
- Status: `failed`
- Severity: `error`
- Location: `file:road_dynamic_overlap_low_io_top.v:unknown`
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

<a id="vg-finding-50"></a>
### VG013: Flag-like signal `runner_writeback_count` should use `flag_` prefix unless it is an output bridge.
- Status: `failed`
- Severity: `error`
- Location: `file:road_dynamic_overlap_low_io_top.v:unknown`
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

<a id="vg-finding-51"></a>
### VG013: Flag-like signal `runner_table_valid` should use `flag_` prefix unless it is an output bridge.
- Status: `failed`
- Severity: `error`
- Location: `file:road_dynamic_overlap_low_io_top.v:unknown`
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

<a id="vg-finding-52"></a>
### VG013: Flag-like signal `runner_load_valid` should use `flag_` prefix unless it is an output bridge.
- Status: `failed`
- Severity: `error`
- Location: `file:road_dynamic_overlap_low_io_top.v:unknown`
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

<a id="vg-finding-53"></a>
### VG013: Flag-like signal `runner_output_ready` should use `flag_` prefix unless it is an output bridge.
- Status: `failed`
- Severity: `error`
- Location: `file:road_dynamic_overlap_low_io_top.v:unknown`
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

<a id="vg-finding-54"></a>
### VG021: Sequential always `always@(posedge i_clk or negedge reg_release_done)` should use negedge active-low reset naming such as i_rstn/i_axis_arstn.
- Status: `failed`
- Severity: `error`
- Location: `file:road_dynamic_overlap_low_io_top.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: always.reset
- source_excerpt: `always.reset`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
always.reset
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-55"></a>
### VG020: Always block `always@(*)` assigns multiple targets ['rx_ready_o', 'tx_data_o', 'tx_valid_o']; split to one target per always.
- Status: `failed`
- Severity: `error`
- Location: `file:road_dynamic_overlap_low_io_top.v:unknown`
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

<a id="vg-finding-56"></a>
### VG020: Always block `always@(posedge i_clk or negedge reg_release_done)` assigns multiple targets ['cnt_status_index', 'reg_commit_ready', 'reg_export_done_seen', 'reg_export_start', 'reg_load_addr', 'reg_load_data', 'reg_load_kind', 'reg_load_low', 'reg_load_pending', 'reg_pw_only', 'reg_runner_done_seen', 'reg_shell_fault', 'reg_snapshot_core', 'reg_snapshot_export_cycles', 'reg_snapshot_flags', 'reg_snapshot_mac_cycles', 'reg_snapshot_mac_results', 'reg_snapshot_post_accepts', 'reg_snapshot_post_cycles', 'reg_snapshot_pre_accepts', 'reg_snapshot_pre_cycles', 'reg_snapshot_preload', 'reg_snapshot_scheduler_idle', 'reg_snapshot_silu_accepts', 'reg_snapshot_silu_cycles', 'reg_snapshot_storage_wait', 'reg_snapshot_writeback_cycles', 'reg_snapshot_writebacks', 'reg_start', 'reg_table_addr']; split to one target per always.
- Status: `failed`
- Severity: `error`
- Location: `file:road_dynamic_overlap_low_io_top.v:unknown`
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

<a id="vg-finding-57"></a>
### VG021: Sequential always `always@(posedge i_clk or negedge reg_release_done)` should use negedge active-low reset naming such as i_rstn/i_axis_arstn.
- Status: `failed`
- Severity: `error`
- Location: `file:road_dynamic_overlap_low_io_top.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: always.reset
- source_excerpt: `always.reset`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
always.reset
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-58"></a>
### VG054: FSM next-state if / else if chain must end with an explicit else branch.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:237`
- Evidence:
- node_kind: `verilog_rtl`
- detail: fsm.next_state_branch_closure
- source_excerpt: `fsm.next_state_branch_closure`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
fsm.next_state_branch_closure
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-59"></a>
### VG054: FSM next-state if / else if chain must end with an explicit else branch.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:252`
- Evidence:
- node_kind: `verilog_rtl`
- detail: fsm.next_state_branch_closure
- source_excerpt: `fsm.next_state_branch_closure`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
fsm.next_state_branch_closure
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-60"></a>
### VG054: FSM next-state if / else if chain must end with an explicit else branch.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:257`
- Evidence:
- node_kind: `verilog_rtl`
- detail: fsm.next_state_branch_closure
- source_excerpt: `fsm.next_state_branch_closure`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
fsm.next_state_branch_closure
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-61"></a>
### VG054: FSM next-state if / else if chain must end with an explicit else branch.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:262`
- Evidence:
- node_kind: `verilog_rtl`
- detail: fsm.next_state_branch_closure
- source_excerpt: `fsm.next_state_branch_closure`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
fsm.next_state_branch_closure
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-62"></a>
### VG054: FSM next-state if / else if chain must end with an explicit else branch.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:267`
- Evidence:
- node_kind: `verilog_rtl`
- detail: fsm.next_state_branch_closure
- source_excerpt: `fsm.next_state_branch_closure`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
fsm.next_state_branch_closure
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-63"></a>
### VG054: FSM next-state if / else if chain must end with an explicit else branch.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:272`
- Evidence:
- node_kind: `verilog_rtl`
- detail: fsm.next_state_branch_closure
- source_excerpt: `fsm.next_state_branch_closure`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
fsm.next_state_branch_closure
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-64"></a>
### VG054: FSM next-state if / else if chain must end with an explicit else branch.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:277`
- Evidence:
- node_kind: `verilog_rtl`
- detail: fsm.next_state_branch_closure
- source_excerpt: `fsm.next_state_branch_closure`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
fsm.next_state_branch_closure
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-65"></a>
### VG054: FSM next-state if / else if chain must end with an explicit else branch.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:284`
- Evidence:
- node_kind: `verilog_rtl`
- detail: fsm.next_state_branch_closure
- source_excerpt: `fsm.next_state_branch_closure`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
fsm.next_state_branch_closure
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-66"></a>
### VG054: FSM next-state if / else if chain must end with an explicit else branch.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:289`
- Evidence:
- node_kind: `verilog_rtl`
- detail: fsm.next_state_branch_closure
- source_excerpt: `fsm.next_state_branch_closure`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
fsm.next_state_branch_closure
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-67"></a>
### VG054: FSM next-state if / else if chain must end with an explicit else branch.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:294`
- Evidence:
- node_kind: `verilog_rtl`
- detail: fsm.next_state_branch_closure
- source_excerpt: `fsm.next_state_branch_closure`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
fsm.next_state_branch_closure
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-68"></a>
### VG054: FSM next-state if / else if chain must end with an explicit else branch.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:299`
- Evidence:
- node_kind: `verilog_rtl`
- detail: fsm.next_state_branch_closure
- source_excerpt: `fsm.next_state_branch_closure`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
fsm.next_state_branch_closure
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-69"></a>
### VG054: FSM next-state if / else if chain must end with an explicit else branch.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:304`
- Evidence:
- node_kind: `verilog_rtl`
- detail: fsm.next_state_branch_closure
- source_excerpt: `fsm.next_state_branch_closure`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
fsm.next_state_branch_closure
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-70"></a>
### VG063: Case branch leading comment must be the pure comment line immediately above the block.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:237`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.case_branch_leading_comment
- source_excerpt: `comments.case_branch_leading_comment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.case_branch_leading_comment
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-71"></a>
### VG063: Case branch leading comment must be the pure comment line immediately above the block.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:252`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.case_branch_leading_comment
- source_excerpt: `comments.case_branch_leading_comment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.case_branch_leading_comment
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-72"></a>
### VG063: Case branch leading comment must be the pure comment line immediately above the block.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:257`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.case_branch_leading_comment
- source_excerpt: `comments.case_branch_leading_comment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.case_branch_leading_comment
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-73"></a>
### VG063: Case branch leading comment must be the pure comment line immediately above the block.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:262`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.case_branch_leading_comment
- source_excerpt: `comments.case_branch_leading_comment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.case_branch_leading_comment
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-74"></a>
### VG063: Case branch leading comment must be the pure comment line immediately above the block.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:267`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.case_branch_leading_comment
- source_excerpt: `comments.case_branch_leading_comment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.case_branch_leading_comment
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-75"></a>
### VG063: Case branch leading comment must be the pure comment line immediately above the block.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:272`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.case_branch_leading_comment
- source_excerpt: `comments.case_branch_leading_comment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.case_branch_leading_comment
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-76"></a>
### VG063: Case branch leading comment must be the pure comment line immediately above the block.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:277`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.case_branch_leading_comment
- source_excerpt: `comments.case_branch_leading_comment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.case_branch_leading_comment
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-77"></a>
### VG063: Case branch leading comment must be the pure comment line immediately above the block.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:284`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.case_branch_leading_comment
- source_excerpt: `comments.case_branch_leading_comment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.case_branch_leading_comment
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-78"></a>
### VG063: Case branch leading comment must be the pure comment line immediately above the block.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:289`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.case_branch_leading_comment
- source_excerpt: `comments.case_branch_leading_comment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.case_branch_leading_comment
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-79"></a>
### VG063: Case branch leading comment must be the pure comment line immediately above the block.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:294`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.case_branch_leading_comment
- source_excerpt: `comments.case_branch_leading_comment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.case_branch_leading_comment
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-80"></a>
### VG063: Case branch leading comment must be the pure comment line immediately above the block.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:299`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.case_branch_leading_comment
- source_excerpt: `comments.case_branch_leading_comment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.case_branch_leading_comment
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-81"></a>
### VG063: Case branch leading comment must be the pure comment line immediately above the block.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:304`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.case_branch_leading_comment
- source_excerpt: `comments.case_branch_leading_comment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.case_branch_leading_comment
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-82"></a>
### VG031: Region banners appear out of the required order.
- Status: `failed`
- Severity: `error`
- Location: `file:road_dynamic_overlap_low_io_top.v:unknown`
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

<a id="vg-finding-83"></a>
### VG031: Module instances must stay inside the 模块实例化区域 banner.
- Status: `failed`
- Severity: `error`
- Location: `file:road_dynamic_overlap_low_io_top.v:unknown`
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

<a id="vg-finding-84"></a>
### VG061: Item `CMD_TABLE_BEGIN` must be placed in 配置参数区域, not `状态参数区域`.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:83`
- Evidence:
- node_kind: `verilog_rtl`
- detail: regions.localparam
- source_excerpt: `regions.localparam`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
regions.localparam
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-85"></a>
### VG061: Item `CMD_LOAD_BEGIN` must be placed in 配置参数区域, not `状态参数区域`.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:84`
- Evidence:
- node_kind: `verilog_rtl`
- detail: regions.localparam
- source_excerpt: `regions.localparam`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
regions.localparam
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-86"></a>
### VG061: Item `CMD_START_DW_PW` must be placed in 配置参数区域, not `状态参数区域`.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:85`
- Evidence:
- node_kind: `verilog_rtl`
- detail: regions.localparam
- source_excerpt: `regions.localparam`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
regions.localparam
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-87"></a>
### VG061: Item `CMD_START_PW_ONLY` must be placed in 配置参数区域, not `状态参数区域`.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:86`
- Evidence:
- node_kind: `verilog_rtl`
- detail: regions.localparam
- source_excerpt: `regions.localparam`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
regions.localparam
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-88"></a>
### VG061: Item `CMD_EXPORT` must be placed in 配置参数区域, not `状态参数区域`.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:87`
- Evidence:
- node_kind: `verilog_rtl`
- detail: regions.localparam
- source_excerpt: `regions.localparam`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
regions.localparam
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-89"></a>
### VG061: Item `CMD_STATUS` must be placed in 配置参数区域, not `状态参数区域`.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:88`
- Evidence:
- node_kind: `verilog_rtl`
- detail: regions.localparam
- source_excerpt: `regions.localparam`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
regions.localparam
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-90"></a>
### VG061: Item `CMD_COMMIT_BLOCK` must be placed in 配置参数区域, not `状态参数区域`.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:89`
- Evidence:
- node_kind: `verilog_rtl`
- detail: regions.localparam
- source_excerpt: `regions.localparam`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
regions.localparam
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-91"></a>
### VG061: Item `CMD_COMMIT_ALLOW` must be placed in 配置参数区域, not `状态参数区域`.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:90`
- Evidence:
- node_kind: `verilog_rtl`
- detail: regions.localparam
- source_excerpt: `regions.localparam`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
regions.localparam
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-92"></a>
### VG061: Item `cnt_status_index` must be placed in 计数信号, not `寄存器信号`.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:115`
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

<a id="vg-finding-93"></a>
### VG061: Item `rx_ready_o` must be placed in 输出信号, not `其他信号`.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:183`
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

<a id="vg-finding-94"></a>
### VG061: Item `tx_valid_o` must be placed in 输出信号, not `其他信号`.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:184`
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

<a id="vg-finding-95"></a>
### VG061: Item `tx_data_o` must be placed in 输出信号, not `其他信号`.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:185`
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

<a id="vg-finding-96"></a>
### VG061: Item `dec_status_word` must be placed in 译码信号, not `其他信号`.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:186`
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

<a id="vg-finding-97"></a>
### VG061: Item `runner_table_valid` must be placed in 模块实例化信号, not `其他信号`.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:187`
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

<a id="vg-finding-98"></a>
### VG061: Item `runner_load_valid` must be placed in 模块实例化信号, not `其他信号`.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:188`
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

<a id="vg-finding-99"></a>
### VG061: Item `runner_output_ready` must be placed in 模块实例化信号, not `其他信号`.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:189`
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

<a id="vg-finding-100"></a>
### VG061: Item `always@(posedge i_clk or negedge reg_release_done)` must be placed in 状态机区域, not `主要任务处理区域`.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:225`
- Evidence:
- node_kind: `verilog_rtl`
- detail: regions.always
- source_excerpt: `regions.always`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
regions.always
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-101"></a>
### VG061: Item `always@(*)` must be placed in 状态机区域, not `主要任务处理区域`.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:234`
- Evidence:
- node_kind: `verilog_rtl`
- detail: regions.always
- source_excerpt: `regions.always`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
regions.always
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-102"></a>
### VG061: Item `always@(*)` must be placed in 输出信号处理区域, not `主要任务处理区域`.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:351`
- Evidence:
- node_kind: `verilog_rtl`
- detail: regions.always
- source_excerpt: `regions.always`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
regions.always
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-103"></a>
### VG061: Item `always@(posedge i_clk or negedge reg_release_done)` must be placed in 状态任务处理区域, not `主要任务处理区域`.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:390`
- Evidence:
- node_kind: `verilog_rtl`
- detail: regions.always
- source_excerpt: `regions.always`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
regions.always
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-104"></a>
### VG061: Item `down2_dynamic_tile_runner_Inst_shell` must be placed in 模块实例化区域, not `主要任务处理区域`.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:517`
- Evidence:
- node_kind: `verilog_rtl`
- detail: regions.instance
- source_excerpt: `regions.instance`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `architecture`; human review required: `True`
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

<a id="vg-finding-105"></a>
### VG070: `输出信号连线` item `o_rx_ready` must use group label `RX接口`, not `unknown`.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:202`
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

<a id="vg-finding-106"></a>
### VG040: localparam `ST_IDLE` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:69`
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

<a id="vg-finding-107"></a>
### VG040: localparam `ST_TABLE` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:70`
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

<a id="vg-finding-108"></a>
### VG040: localparam `ST_LOAD_DESCRIPTOR` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:71`
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

<a id="vg-finding-109"></a>
### VG040: localparam `ST_LOAD_LOW` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:72`
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

<a id="vg-finding-110"></a>
### VG040: localparam `ST_LOAD_HIGH` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:73`
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

<a id="vg-finding-111"></a>
### VG040: localparam `ST_LOAD_WAIT` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:74`
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

<a id="vg-finding-112"></a>
### VG040: localparam `ST_EXPORT_WAIT` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:75`
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

<a id="vg-finding-113"></a>
### VG040: localparam `ST_EXPORT_META` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:76`
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

<a id="vg-finding-114"></a>
### VG040: localparam `ST_EXPORT_DATA` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:77`
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

<a id="vg-finding-115"></a>
### VG040: localparam `ST_EXPORT_REPORT` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:78`
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

<a id="vg-finding-116"></a>
### VG040: localparam `ST_ERROR_REPORT` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:79`
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

<a id="vg-finding-117"></a>
### VG040: localparam `ST_STATUS_SEND` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:80`
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

<a id="vg-finding-118"></a>
### VG040: localparam `CMD_TABLE_BEGIN` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:83`
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

<a id="vg-finding-119"></a>
### VG040: localparam `CMD_LOAD_BEGIN` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:84`
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

<a id="vg-finding-120"></a>
### VG040: localparam `CMD_START_DW_PW` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:85`
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

<a id="vg-finding-121"></a>
### VG040: localparam `CMD_START_PW_ONLY` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:86`
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

<a id="vg-finding-122"></a>
### VG040: localparam `CMD_EXPORT` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:87`
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

<a id="vg-finding-123"></a>
### VG040: localparam `CMD_STATUS` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:88`
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

<a id="vg-finding-124"></a>
### VG040: localparam `CMD_COMMIT_BLOCK` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:89`
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

<a id="vg-finding-125"></a>
### VG040: localparam `CMD_COMMIT_ALLOW` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:90`
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

<a id="vg-finding-126"></a>
### VG040: signal `reg_snapshot_flags` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:118`
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

<a id="vg-finding-127"></a>
### VG040: signal `reg_snapshot_preload` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:119`
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

<a id="vg-finding-128"></a>
### VG040: signal `reg_snapshot_core` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:120`
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

<a id="vg-finding-129"></a>
### VG040: signal `reg_snapshot_mac_cycles` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:121`
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

<a id="vg-finding-130"></a>
### VG040: signal `reg_snapshot_pre_cycles` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:122`
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

<a id="vg-finding-131"></a>
### VG040: signal `reg_snapshot_silu_cycles` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:123`
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

<a id="vg-finding-132"></a>
### VG040: signal `reg_snapshot_post_cycles` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:124`
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

<a id="vg-finding-133"></a>
### VG040: signal `reg_snapshot_writeback_cycles` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:125`
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

<a id="vg-finding-134"></a>
### VG040: signal `reg_snapshot_storage_wait` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:126`
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

<a id="vg-finding-135"></a>
### VG040: signal `reg_snapshot_scheduler_idle` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:127`
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

<a id="vg-finding-136"></a>
### VG040: signal `reg_snapshot_export_cycles` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:128`
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

<a id="vg-finding-137"></a>
### VG040: signal `reg_snapshot_mac_results` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:129`
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

<a id="vg-finding-138"></a>
### VG040: signal `reg_snapshot_pre_accepts` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:130`
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

<a id="vg-finding-139"></a>
### VG040: signal `reg_snapshot_silu_accepts` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:131`
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

<a id="vg-finding-140"></a>
### VG040: signal `reg_snapshot_post_accepts` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:132`
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

<a id="vg-finding-141"></a>
### VG040: signal `reg_snapshot_writebacks` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:133`
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

<a id="vg-finding-142"></a>
### VG040: signal `runner_table_ready` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:137`
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

<a id="vg-finding-143"></a>
### VG040: signal `runner_table_loaded` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:138`
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

<a id="vg-finding-144"></a>
### VG040: signal `runner_table_fault` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:139`
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

<a id="vg-finding-145"></a>
### VG040: signal `runner_load_ready` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:140`
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

<a id="vg-finding-146"></a>
### VG040: signal `runner_busy` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:141`
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

<a id="vg-finding-147"></a>
### VG040: signal `runner_done` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:142`
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

<a id="vg-finding-148"></a>
### VG040: signal `runner_fault` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:143`
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

<a id="vg-finding-149"></a>
### VG040: signal `runner_output_valid` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:144`
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

<a id="vg-finding-150"></a>
### VG040: signal `runner_output_data` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:145`
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

<a id="vg-finding-151"></a>
### VG040: signal `runner_output_index` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:146`
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

<a id="vg-finding-152"></a>
### VG040: signal `runner_export_done` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:147`
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

<a id="vg-finding-153"></a>
### VG040: signal `runner_debug_valid` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:150`
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

<a id="vg-finding-154"></a>
### VG040: signal `runner_debug_phase` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:151`
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

<a id="vg-finding-155"></a>
### VG040: signal `runner_debug_layer` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:152`
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

<a id="vg-finding-156"></a>
### VG040: signal `runner_debug_position` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:153`
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

<a id="vg-finding-157"></a>
### VG040: signal `runner_debug_channel` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:154`
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

<a id="vg-finding-158"></a>
### VG040: signal `runner_debug_value` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:155`
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

<a id="vg-finding-159"></a>
### VG040: signal `runner_preload_writes` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:156`
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

<a id="vg-finding-160"></a>
### VG040: signal `runner_core_cycles` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:157`
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

<a id="vg-finding-161"></a>
### VG040: signal `runner_mac_cycles` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:158`
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

<a id="vg-finding-162"></a>
### VG040: signal `runner_pre_cycles` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:159`
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

<a id="vg-finding-163"></a>
### VG040: signal `runner_silu_cycles` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:160`
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

<a id="vg-finding-164"></a>
### VG040: signal `runner_post_cycles` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:161`
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

<a id="vg-finding-165"></a>
### VG040: signal `runner_writeback_cycles` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:162`
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

<a id="vg-finding-166"></a>
### VG040: signal `runner_storage_wait_cycles` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:163`
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

<a id="vg-finding-167"></a>
### VG040: signal `runner_scheduler_idle_cycles` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:164`
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

<a id="vg-finding-168"></a>
### VG040: signal `runner_export_cycles` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:165`
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

<a id="vg-finding-169"></a>
### VG040: signal `runner_result_queue_count` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:166`
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

<a id="vg-finding-170"></a>
### VG040: signal `runner_result_reserved` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:167`
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

<a id="vg-finding-171"></a>
### VG040: signal `runner_meta_count` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:168`
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

<a id="vg-finding-172"></a>
### VG040: signal `runner_mac_result_count` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:169`
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

<a id="vg-finding-173"></a>
### VG040: signal `runner_pre_accept_count` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:170`
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

<a id="vg-finding-174"></a>
### VG040: signal `runner_silu_accept_count` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:171`
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

<a id="vg-finding-175"></a>
### VG040: signal `runner_post_accept_count` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:172`
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

<a id="vg-finding-176"></a>
### VG040: signal `runner_writeback_count` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:173`
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

<a id="vg-finding-177"></a>
### VG040: signal `runner_table_valid` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:187`
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

<a id="vg-finding-178"></a>
### VG040: signal `runner_load_valid` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:188`
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

<a id="vg-finding-179"></a>
### VG040: signal `runner_output_ready` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:189`
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

<a id="vg-finding-180"></a>
### VG040: assign `flag_interface_open` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:192`
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

<a id="vg-finding-181"></a>
### VG040: assign `flag_rx_transfer` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:193`
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

<a id="vg-finding-182"></a>
### VG040: assign `flag_tx_transfer` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:194`
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

<a id="vg-finding-183"></a>
### VG040: assign `runner_table_valid` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:195`
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

<a id="vg-finding-184"></a>
### VG040: assign `flag_table_transfer` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:196`
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

<a id="vg-finding-185"></a>
### VG040: assign `runner_load_valid` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:197`
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

<a id="vg-finding-186"></a>
### VG040: assign `flag_load_transfer` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:198`
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

<a id="vg-finding-187"></a>
### VG040: assign `runner_output_ready` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:199`
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

<a id="vg-finding-188"></a>
### VG040: assign `o_rx_ready` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:202`
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

<a id="vg-finding-189"></a>
### VG040: assign `o_tx_valid` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:203`
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

<a id="vg-finding-190"></a>
### VG040: assign `o_tx_data` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:204`
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

<a id="vg-finding-191"></a>
### VG040: Always block `always@(posedge i_clk or negedge i_rstn)` should have a nearby leading comment explaining behavior.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:216`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.always
- source_excerpt: `comments.always`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.always
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-192"></a>
### VG040: Instance `down2_dynamic_tile_runner_Inst_shell` should have a leading function/connection comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:517`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.instance
- source_excerpt: `comments.instance`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `structure`
- Bad example:
```text
comments.instance
```
- Good example:
```text
调整结构关系后重新检查组合锥、实例连接和相关下游节点。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-193"></a>
### VG062: process assignment `reg_release_meta` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:210`
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

<a id="vg-finding-194"></a>
### VG062: process assignment `reg_release_meta` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:212`
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

<a id="vg-finding-195"></a>
### VG062: process assignment `reg_release_done` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:218`
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

<a id="vg-finding-196"></a>
### VG062: process assignment `reg_release_done` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:220`
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

<a id="vg-finding-197"></a>
### VG062: process assignment `state_current` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:227`
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

<a id="vg-finding-198"></a>
### VG062: process assignment `state_current` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:229`
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

<a id="vg-finding-199"></a>
### VG062: process assignment `state_next` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:235`
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

<a id="vg-finding-200"></a>
### VG062: process assignment `CMD_TABLE_BEGIN: state_next` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:240`
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

<a id="vg-finding-201"></a>
### VG062: process assignment `CMD_LOAD_BEGIN: state_next` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:241`
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

<a id="vg-finding-202"></a>
### VG062: process assignment `CMD_START_DW_PW: state_next` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:242`
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

<a id="vg-finding-203"></a>
### VG062: process assignment `CMD_START_PW_ONLY: state_next` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:243`
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

<a id="vg-finding-204"></a>
### VG062: process assignment `CMD_EXPORT: state_next` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:244`
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

<a id="vg-finding-205"></a>
### VG062: process assignment `CMD_STATUS: state_next` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:245`
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

<a id="vg-finding-206"></a>
### VG062: process assignment `CMD_COMMIT_BLOCK: state_next` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:246`
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

<a id="vg-finding-207"></a>
### VG062: process assignment `CMD_COMMIT_ALLOW: state_next` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:247`
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

<a id="vg-finding-208"></a>
### VG062: process assignment `default: state_next` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:248`
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

<a id="vg-finding-209"></a>
### VG062: process assignment `state_next` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:254`
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

<a id="vg-finding-210"></a>
### VG062: process assignment `state_next` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:259`
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

<a id="vg-finding-211"></a>
### VG062: process assignment `state_next` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:264`
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

<a id="vg-finding-212"></a>
### VG062: process assignment `state_next` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:269`
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

<a id="vg-finding-213"></a>
### VG062: process assignment `state_next` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:274`
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

<a id="vg-finding-214"></a>
### VG062: process assignment `state_next` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:279`
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

<a id="vg-finding-215"></a>
### VG062: process assignment `state_next` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:281`
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

<a id="vg-finding-216"></a>
### VG062: process assignment `state_next` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:286`
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

<a id="vg-finding-217"></a>
### VG062: process assignment `state_next` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:291`
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

<a id="vg-finding-218"></a>
### VG062: process assignment `state_next` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:296`
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

<a id="vg-finding-219"></a>
### VG062: process assignment `state_next` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:301`
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

<a id="vg-finding-220"></a>
### VG062: process assignment `state_next` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:306`
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

<a id="vg-finding-221"></a>
### VG062: process assignment `default: state_next` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:309`
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

<a id="vg-finding-222"></a>
### VG062: process assignment `5'd0: dec_status_word` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:316`
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

<a id="vg-finding-223"></a>
### VG062: process assignment `5'd1: dec_status_word` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:317`
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

<a id="vg-finding-224"></a>
### VG062: process assignment `5'd2: dec_status_word` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:318`
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

<a id="vg-finding-225"></a>
### VG062: process assignment `5'd3: dec_status_word` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:319`
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

<a id="vg-finding-226"></a>
### VG062: process assignment `5'd4: dec_status_word` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:320`
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

<a id="vg-finding-227"></a>
### VG062: process assignment `5'd5: dec_status_word` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:321`
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

<a id="vg-finding-228"></a>
### VG062: process assignment `5'd6: dec_status_word` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:322`
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

<a id="vg-finding-229"></a>
### VG062: process assignment `5'd7: dec_status_word` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:323`
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

<a id="vg-finding-230"></a>
### VG062: process assignment `5'd8: dec_status_word` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:324`
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

<a id="vg-finding-231"></a>
### VG062: process assignment `5'd9: dec_status_word` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:325`
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

<a id="vg-finding-232"></a>
### VG062: process assignment `5'd10: dec_status_word` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:326`
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

<a id="vg-finding-233"></a>
### VG062: process assignment `5'd11: dec_status_word` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:327`
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

<a id="vg-finding-234"></a>
### VG062: process assignment `5'd12: dec_status_word` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:328`
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

<a id="vg-finding-235"></a>
### VG062: process assignment `5'd13: dec_status_word` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:329`
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

<a id="vg-finding-236"></a>
### VG062: process assignment `5'd14: dec_status_word` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:330`
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

<a id="vg-finding-237"></a>
### VG062: process assignment `5'd15: dec_status_word` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:331`
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

<a id="vg-finding-238"></a>
### VG062: process assignment `5'd16: dec_status_word` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:332`
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

<a id="vg-finding-239"></a>
### VG062: process assignment `5'd17: dec_status_word` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:333`
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

<a id="vg-finding-240"></a>
### VG062: process assignment `5'd18: dec_status_word` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:334`
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

<a id="vg-finding-241"></a>
### VG062: process assignment `5'd19: dec_status_word` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:335`
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

<a id="vg-finding-242"></a>
### VG062: process assignment `5'd20: dec_status_word` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:336`
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

<a id="vg-finding-243"></a>
### VG062: process assignment `5'd21: dec_status_word` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:337`
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

<a id="vg-finding-244"></a>
### VG062: process assignment `5'd22: dec_status_word` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:338`
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

<a id="vg-finding-245"></a>
### VG062: process assignment `5'd23: dec_status_word` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:339`
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

<a id="vg-finding-246"></a>
### VG062: process assignment `5'd24: dec_status_word` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:340`
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

<a id="vg-finding-247"></a>
### VG062: process assignment `5'd25: dec_status_word` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:341`
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

<a id="vg-finding-248"></a>
### VG062: process assignment `5'd26: dec_status_word` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:342`
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

<a id="vg-finding-249"></a>
### VG062: process assignment `5'd27: dec_status_word` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:343`
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

<a id="vg-finding-250"></a>
### VG062: process assignment `5'd28: dec_status_word` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:344`
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

<a id="vg-finding-251"></a>
### VG062: process assignment `5'd29: dec_status_word` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:345`
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

<a id="vg-finding-252"></a>
### VG062: process assignment `default: dec_status_word` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:346`
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

<a id="vg-finding-253"></a>
### VG062: process assignment `rx_ready_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:352`
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

<a id="vg-finding-254"></a>
### VG062: process assignment `tx_valid_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:353`
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

<a id="vg-finding-255"></a>
### VG062: process assignment `tx_data_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:354`
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

<a id="vg-finding-256"></a>
### VG062: process assignment `ST_IDLE: rx_ready_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:356`
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

<a id="vg-finding-257"></a>
### VG062: process assignment `ST_TABLE: rx_ready_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:357`
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

<a id="vg-finding-258"></a>
### VG062: process assignment `ST_LOAD_DESCRIPTOR: rx_ready_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:358`
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

<a id="vg-finding-259"></a>
### VG062: process assignment `ST_LOAD_LOW: rx_ready_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:359`
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

<a id="vg-finding-260"></a>
### VG062: process assignment `ST_LOAD_HIGH: rx_ready_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:360`
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

<a id="vg-finding-261"></a>
### VG062: process assignment `tx_valid_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:362`
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

<a id="vg-finding-262"></a>
### VG062: process assignment `tx_data_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:363`
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

<a id="vg-finding-263"></a>
### VG062: process assignment `tx_valid_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:366`
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

<a id="vg-finding-264"></a>
### VG062: process assignment `tx_data_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:367`
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

<a id="vg-finding-265"></a>
### VG062: process assignment `tx_valid_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:370`
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

<a id="vg-finding-266"></a>
### VG062: process assignment `tx_data_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:371`
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

<a id="vg-finding-267"></a>
### VG062: process assignment `tx_valid_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:374`
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

<a id="vg-finding-268"></a>
### VG062: process assignment `tx_data_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:375`
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

<a id="vg-finding-269"></a>
### VG062: process assignment `tx_valid_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:378`
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

<a id="vg-finding-270"></a>
### VG062: process assignment `tx_data_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:379`
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

<a id="vg-finding-271"></a>
### VG062: process assignment `rx_ready_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:382`
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

<a id="vg-finding-272"></a>
### VG062: process assignment `tx_valid_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:383`
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

<a id="vg-finding-273"></a>
### VG062: process assignment `tx_data_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:384`
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

<a id="vg-finding-274"></a>
### VG062: process assignment `reg_table_addr` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:392`
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

<a id="vg-finding-275"></a>
### VG062: process assignment `reg_load_kind` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:393`
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

<a id="vg-finding-276"></a>
### VG062: process assignment `reg_load_addr` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:394`
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

<a id="vg-finding-277"></a>
### VG062: process assignment `reg_load_low` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:395`
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

<a id="vg-finding-278"></a>
### VG062: process assignment `reg_load_data` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:396`
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

<a id="vg-finding-279"></a>
### VG062: process assignment `reg_load_pending` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:397`
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

<a id="vg-finding-280"></a>
### VG062: process assignment `reg_start` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:398`
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

<a id="vg-finding-281"></a>
### VG062: process assignment `reg_pw_only` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:399`
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

<a id="vg-finding-282"></a>
### VG062: process assignment `reg_export_start` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:400`
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

<a id="vg-finding-283"></a>
### VG062: process assignment `reg_export_done_seen` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:401`
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

<a id="vg-finding-284"></a>
### VG062: process assignment `reg_runner_done_seen` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:402`
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

<a id="vg-finding-285"></a>
### VG062: process assignment `reg_commit_ready` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:403`
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

<a id="vg-finding-286"></a>
### VG062: process assignment `reg_shell_fault` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:404`
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

<a id="vg-finding-287"></a>
### VG062: process assignment `cnt_status_index` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:405`
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

<a id="vg-finding-288"></a>
### VG062: process assignment `reg_snapshot_flags` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:406`
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

<a id="vg-finding-289"></a>
### VG062: process assignment `reg_snapshot_preload` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:407`
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

<a id="vg-finding-290"></a>
### VG062: process assignment `reg_snapshot_core` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:408`
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

<a id="vg-finding-291"></a>
### VG062: process assignment `reg_snapshot_mac_cycles` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:409`
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

<a id="vg-finding-292"></a>
### VG062: process assignment `reg_snapshot_pre_cycles` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:410`
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

<a id="vg-finding-293"></a>
### VG062: process assignment `reg_snapshot_silu_cycles` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:411`
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

<a id="vg-finding-294"></a>
### VG062: process assignment `reg_snapshot_post_cycles` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:412`
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

<a id="vg-finding-295"></a>
### VG062: process assignment `reg_snapshot_writeback_cycles` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:413`
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

<a id="vg-finding-296"></a>
### VG062: process assignment `reg_snapshot_storage_wait` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:414`
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

<a id="vg-finding-297"></a>
### VG062: process assignment `reg_snapshot_scheduler_idle` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:415`
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

<a id="vg-finding-298"></a>
### VG062: process assignment `reg_snapshot_export_cycles` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:416`
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

<a id="vg-finding-299"></a>
### VG062: process assignment `reg_snapshot_mac_results` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:417`
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

<a id="vg-finding-300"></a>
### VG062: process assignment `reg_snapshot_pre_accepts` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:418`
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

<a id="vg-finding-301"></a>
### VG062: process assignment `reg_snapshot_silu_accepts` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:419`
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

<a id="vg-finding-302"></a>
### VG062: process assignment `reg_snapshot_post_accepts` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:420`
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

<a id="vg-finding-303"></a>
### VG062: process assignment `reg_snapshot_writebacks` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:421`
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

<a id="vg-finding-304"></a>
### VG062: process assignment `reg_start` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:423`
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

<a id="vg-finding-305"></a>
### VG062: process assignment `reg_export_start` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:424`
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

<a id="vg-finding-306"></a>
### VG062: process assignment `reg_start` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:430`
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

<a id="vg-finding-307"></a>
### VG062: process assignment `reg_pw_only` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:431`
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

<a id="vg-finding-308"></a>
### VG062: process assignment `reg_runner_done_seen` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:432`
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

<a id="vg-finding-309"></a>
### VG062: process assignment `reg_start` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:437`
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

<a id="vg-finding-310"></a>
### VG062: process assignment `reg_pw_only` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:438`
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

<a id="vg-finding-311"></a>
### VG062: process assignment `reg_runner_done_seen` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:439`
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

<a id="vg-finding-312"></a>
### VG062: process assignment `reg_export_start` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:444`
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

<a id="vg-finding-313"></a>
### VG062: process assignment `reg_export_done_seen` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:445`
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

<a id="vg-finding-314"></a>
### VG062: process assignment `cnt_status_index` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:449`
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

<a id="vg-finding-315"></a>
### VG062: process assignment `reg_snapshot_preload` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:455`
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

<a id="vg-finding-316"></a>
### VG062: process assignment `reg_snapshot_core` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:456`
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

<a id="vg-finding-317"></a>
### VG062: process assignment `reg_snapshot_mac_cycles` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:457`
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

<a id="vg-finding-318"></a>
### VG062: process assignment `reg_snapshot_pre_cycles` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:458`
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

<a id="vg-finding-319"></a>
### VG062: process assignment `reg_snapshot_silu_cycles` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:459`
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

<a id="vg-finding-320"></a>
### VG062: process assignment `reg_snapshot_post_cycles` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:460`
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

<a id="vg-finding-321"></a>
### VG062: process assignment `reg_snapshot_writeback_cycles` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:461`
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

<a id="vg-finding-322"></a>
### VG062: process assignment `reg_snapshot_storage_wait` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:462`
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

<a id="vg-finding-323"></a>
### VG062: process assignment `reg_snapshot_scheduler_idle` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:463`
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

<a id="vg-finding-324"></a>
### VG062: process assignment `reg_snapshot_export_cycles` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:464`
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

<a id="vg-finding-325"></a>
### VG062: process assignment `reg_snapshot_mac_results` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:465`
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

<a id="vg-finding-326"></a>
### VG062: process assignment `reg_snapshot_pre_accepts` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:466`
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

<a id="vg-finding-327"></a>
### VG062: process assignment `reg_snapshot_silu_accepts` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:467`
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

<a id="vg-finding-328"></a>
### VG062: process assignment `reg_snapshot_post_accepts` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:468`
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

<a id="vg-finding-329"></a>
### VG062: process assignment `reg_snapshot_writebacks` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:469`
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

<a id="vg-finding-330"></a>
### VG062: process assignment `reg_shell_fault` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:475`
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

<a id="vg-finding-331"></a>
### VG062: process assignment `reg_table_addr` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:481`
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

<a id="vg-finding-332"></a>
### VG062: process assignment `reg_load_kind` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:484`
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

<a id="vg-finding-333"></a>
### VG062: process assignment `reg_load_addr` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:485`
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

<a id="vg-finding-334"></a>
### VG062: process assignment `reg_shell_fault` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:487`
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

<a id="vg-finding-335"></a>
### VG062: process assignment `reg_load_low` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:491`
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

<a id="vg-finding-336"></a>
### VG062: process assignment `reg_load_data` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:494`
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

<a id="vg-finding-337"></a>
### VG062: process assignment `reg_load_pending` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:495`
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

<a id="vg-finding-338"></a>
### VG062: process assignment `reg_load_pending` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:497`
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

<a id="vg-finding-339"></a>
### VG062: process assignment `reg_export_done_seen` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:500`
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

<a id="vg-finding-340"></a>
### VG062: process assignment `reg_export_done_seen` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:502`
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

<a id="vg-finding-341"></a>
### VG062: process assignment `reg_shell_fault` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:505`
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

<a id="vg-finding-342"></a>
### VG062: process assignment `reg_runner_done_seen` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:508`
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

<a id="vg-finding-343"></a>
### VG062: process assignment `cnt_status_index` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:511`
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

<a id="vg-finding-344"></a>
### VG064: instance mapping `.i_clk` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:518`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.instance_mapping
- source_excerpt: `comments.instance_mapping`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `structure`
- Bad example:
```text
comments.instance_mapping
```
- Good example:
```text
调整结构关系后重新检查组合锥、实例连接和相关下游节点。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-345"></a>
### VG064: instance mapping `.i_rstn` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:519`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.instance_mapping
- source_excerpt: `comments.instance_mapping`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `structure`
- Bad example:
```text
comments.instance_mapping
```
- Good example:
```text
调整结构关系后重新检查组合锥、实例连接和相关下游节点。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-346"></a>
### VG064: instance mapping `.i_table_valid` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:520`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.instance_mapping
- source_excerpt: `comments.instance_mapping`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `structure`
- Bad example:
```text
comments.instance_mapping
```
- Good example:
```text
调整结构关系后重新检查组合锥、实例连接和相关下游节点。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-347"></a>
### VG064: instance mapping `.i_table_addr` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:521`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.instance_mapping
- source_excerpt: `comments.instance_mapping`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `structure`
- Bad example:
```text
comments.instance_mapping
```
- Good example:
```text
调整结构关系后重新检查组合锥、实例连接和相关下游节点。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-348"></a>
### VG064: instance mapping `.i_table_data` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:522`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.instance_mapping
- source_excerpt: `comments.instance_mapping`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `structure`
- Bad example:
```text
comments.instance_mapping
```
- Good example:
```text
调整结构关系后重新检查组合锥、实例连接和相关下游节点。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-349"></a>
### VG064: instance mapping `.o_table_ready` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:523`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.instance_mapping
- source_excerpt: `comments.instance_mapping`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `structure`
- Bad example:
```text
comments.instance_mapping
```
- Good example:
```text
调整结构关系后重新检查组合锥、实例连接和相关下游节点。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-350"></a>
### VG064: instance mapping `.o_table_loaded` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:524`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.instance_mapping
- source_excerpt: `comments.instance_mapping`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `structure`
- Bad example:
```text
comments.instance_mapping
```
- Good example:
```text
调整结构关系后重新检查组合锥、实例连接和相关下游节点。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-351"></a>
### VG064: instance mapping `.o_table_fault` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:525`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.instance_mapping
- source_excerpt: `comments.instance_mapping`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `structure`
- Bad example:
```text
comments.instance_mapping
```
- Good example:
```text
调整结构关系后重新检查组合锥、实例连接和相关下游节点。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-352"></a>
### VG064: instance mapping `.i_load_valid` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:526`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.instance_mapping
- source_excerpt: `comments.instance_mapping`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `structure`
- Bad example:
```text
comments.instance_mapping
```
- Good example:
```text
调整结构关系后重新检查组合锥、实例连接和相关下游节点。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-353"></a>
### VG064: instance mapping `.i_load_kind` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:527`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.instance_mapping
- source_excerpt: `comments.instance_mapping`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `structure`
- Bad example:
```text
comments.instance_mapping
```
- Good example:
```text
调整结构关系后重新检查组合锥、实例连接和相关下游节点。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-354"></a>
### VG064: instance mapping `.i_load_addr` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:528`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.instance_mapping
- source_excerpt: `comments.instance_mapping`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `structure`
- Bad example:
```text
comments.instance_mapping
```
- Good example:
```text
调整结构关系后重新检查组合锥、实例连接和相关下游节点。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-355"></a>
### VG064: instance mapping `.i_load_data` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:529`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.instance_mapping
- source_excerpt: `comments.instance_mapping`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `structure`
- Bad example:
```text
comments.instance_mapping
```
- Good example:
```text
调整结构关系后重新检查组合锥、实例连接和相关下游节点。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-356"></a>
### VG064: instance mapping `.o_load_ready` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:530`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.instance_mapping
- source_excerpt: `comments.instance_mapping`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `structure`
- Bad example:
```text
comments.instance_mapping
```
- Good example:
```text
调整结构关系后重新检查组合锥、实例连接和相关下游节点。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-357"></a>
### VG064: instance mapping `.i_start` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:531`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.instance_mapping
- source_excerpt: `comments.instance_mapping`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `structure`
- Bad example:
```text
comments.instance_mapping
```
- Good example:
```text
调整结构关系后重新检查组合锥、实例连接和相关下游节点。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-358"></a>
### VG064: instance mapping `.i_pw_only` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:532`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.instance_mapping
- source_excerpt: `comments.instance_mapping`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `structure`
- Bad example:
```text
comments.instance_mapping
```
- Good example:
```text
调整结构关系后重新检查组合锥、实例连接和相关下游节点。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-359"></a>
### VG064: instance mapping `.i_commit_ready` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:533`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.instance_mapping
- source_excerpt: `comments.instance_mapping`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `structure`
- Bad example:
```text
comments.instance_mapping
```
- Good example:
```text
调整结构关系后重新检查组合锥、实例连接和相关下游节点。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-360"></a>
### VG064: instance mapping `.o_busy` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:534`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.instance_mapping
- source_excerpt: `comments.instance_mapping`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `structure`
- Bad example:
```text
comments.instance_mapping
```
- Good example:
```text
调整结构关系后重新检查组合锥、实例连接和相关下游节点。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-361"></a>
### VG064: instance mapping `.o_done` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:535`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.instance_mapping
- source_excerpt: `comments.instance_mapping`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `structure`
- Bad example:
```text
comments.instance_mapping
```
- Good example:
```text
调整结构关系后重新检查组合锥、实例连接和相关下游节点。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-362"></a>
### VG064: instance mapping `.o_fault` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:536`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.instance_mapping
- source_excerpt: `comments.instance_mapping`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `structure`
- Bad example:
```text
comments.instance_mapping
```
- Good example:
```text
调整结构关系后重新检查组合锥、实例连接和相关下游节点。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-363"></a>
### VG064: instance mapping `.i_export_start` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:537`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.instance_mapping
- source_excerpt: `comments.instance_mapping`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `structure`
- Bad example:
```text
comments.instance_mapping
```
- Good example:
```text
调整结构关系后重新检查组合锥、实例连接和相关下游节点。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-364"></a>
### VG064: instance mapping `.i_output_ready` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:538`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.instance_mapping
- source_excerpt: `comments.instance_mapping`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `structure`
- Bad example:
```text
comments.instance_mapping
```
- Good example:
```text
调整结构关系后重新检查组合锥、实例连接和相关下游节点。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-365"></a>
### VG064: instance mapping `.o_output_valid` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:539`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.instance_mapping
- source_excerpt: `comments.instance_mapping`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `structure`
- Bad example:
```text
comments.instance_mapping
```
- Good example:
```text
调整结构关系后重新检查组合锥、实例连接和相关下游节点。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-366"></a>
### VG064: instance mapping `.o_output_data` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:540`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.instance_mapping
- source_excerpt: `comments.instance_mapping`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `structure`
- Bad example:
```text
comments.instance_mapping
```
- Good example:
```text
调整结构关系后重新检查组合锥、实例连接和相关下游节点。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-367"></a>
### VG064: instance mapping `.o_output_index` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:541`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.instance_mapping
- source_excerpt: `comments.instance_mapping`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `structure`
- Bad example:
```text
comments.instance_mapping
```
- Good example:
```text
调整结构关系后重新检查组合锥、实例连接和相关下游节点。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-368"></a>
### VG064: instance mapping `.o_export_done` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:542`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.instance_mapping
- source_excerpt: `comments.instance_mapping`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `structure`
- Bad example:
```text
comments.instance_mapping
```
- Good example:
```text
调整结构关系后重新检查组合锥、实例连接和相关下游节点。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-369"></a>
### VG064: instance mapping `.o_debug_valid` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:543`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.instance_mapping
- source_excerpt: `comments.instance_mapping`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `structure`
- Bad example:
```text
comments.instance_mapping
```
- Good example:
```text
调整结构关系后重新检查组合锥、实例连接和相关下游节点。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-370"></a>
### VG064: instance mapping `.o_debug_phase` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:544`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.instance_mapping
- source_excerpt: `comments.instance_mapping`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `structure`
- Bad example:
```text
comments.instance_mapping
```
- Good example:
```text
调整结构关系后重新检查组合锥、实例连接和相关下游节点。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-371"></a>
### VG064: instance mapping `.o_debug_layer` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:545`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.instance_mapping
- source_excerpt: `comments.instance_mapping`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `structure`
- Bad example:
```text
comments.instance_mapping
```
- Good example:
```text
调整结构关系后重新检查组合锥、实例连接和相关下游节点。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-372"></a>
### VG064: instance mapping `.o_debug_position` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:546`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.instance_mapping
- source_excerpt: `comments.instance_mapping`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `structure`
- Bad example:
```text
comments.instance_mapping
```
- Good example:
```text
调整结构关系后重新检查组合锥、实例连接和相关下游节点。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-373"></a>
### VG064: instance mapping `.o_debug_channel` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:547`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.instance_mapping
- source_excerpt: `comments.instance_mapping`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `structure`
- Bad example:
```text
comments.instance_mapping
```
- Good example:
```text
调整结构关系后重新检查组合锥、实例连接和相关下游节点。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-374"></a>
### VG064: instance mapping `.o_debug_value` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:548`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.instance_mapping
- source_excerpt: `comments.instance_mapping`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `structure`
- Bad example:
```text
comments.instance_mapping
```
- Good example:
```text
调整结构关系后重新检查组合锥、实例连接和相关下游节点。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-375"></a>
### VG064: instance mapping `.o_preload_writes` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:549`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.instance_mapping
- source_excerpt: `comments.instance_mapping`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `structure`
- Bad example:
```text
comments.instance_mapping
```
- Good example:
```text
调整结构关系后重新检查组合锥、实例连接和相关下游节点。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-376"></a>
### VG064: instance mapping `.o_core_cycles` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:550`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.instance_mapping
- source_excerpt: `comments.instance_mapping`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `structure`
- Bad example:
```text
comments.instance_mapping
```
- Good example:
```text
调整结构关系后重新检查组合锥、实例连接和相关下游节点。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-377"></a>
### VG064: instance mapping `.o_mac_cycles` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:551`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.instance_mapping
- source_excerpt: `comments.instance_mapping`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `structure`
- Bad example:
```text
comments.instance_mapping
```
- Good example:
```text
调整结构关系后重新检查组合锥、实例连接和相关下游节点。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-378"></a>
### VG064: instance mapping `.o_pre_cycles` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:552`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.instance_mapping
- source_excerpt: `comments.instance_mapping`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `structure`
- Bad example:
```text
comments.instance_mapping
```
- Good example:
```text
调整结构关系后重新检查组合锥、实例连接和相关下游节点。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-379"></a>
### VG064: instance mapping `.o_silu_cycles` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:553`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.instance_mapping
- source_excerpt: `comments.instance_mapping`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `structure`
- Bad example:
```text
comments.instance_mapping
```
- Good example:
```text
调整结构关系后重新检查组合锥、实例连接和相关下游节点。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-380"></a>
### VG064: instance mapping `.o_post_cycles` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:554`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.instance_mapping
- source_excerpt: `comments.instance_mapping`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `structure`
- Bad example:
```text
comments.instance_mapping
```
- Good example:
```text
调整结构关系后重新检查组合锥、实例连接和相关下游节点。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-381"></a>
### VG064: instance mapping `.o_writeback_cycles` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:555`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.instance_mapping
- source_excerpt: `comments.instance_mapping`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `structure`
- Bad example:
```text
comments.instance_mapping
```
- Good example:
```text
调整结构关系后重新检查组合锥、实例连接和相关下游节点。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-382"></a>
### VG064: instance mapping `.o_storage_wait_cycles` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:556`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.instance_mapping
- source_excerpt: `comments.instance_mapping`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `structure`
- Bad example:
```text
comments.instance_mapping
```
- Good example:
```text
调整结构关系后重新检查组合锥、实例连接和相关下游节点。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-383"></a>
### VG064: instance mapping `.o_scheduler_idle_cycles` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:557`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.instance_mapping
- source_excerpt: `comments.instance_mapping`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `structure`
- Bad example:
```text
comments.instance_mapping
```
- Good example:
```text
调整结构关系后重新检查组合锥、实例连接和相关下游节点。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-384"></a>
### VG064: instance mapping `.o_export_cycles` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:558`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.instance_mapping
- source_excerpt: `comments.instance_mapping`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `structure`
- Bad example:
```text
comments.instance_mapping
```
- Good example:
```text
调整结构关系后重新检查组合锥、实例连接和相关下游节点。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-385"></a>
### VG064: instance mapping `.o_result_queue_count` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:559`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.instance_mapping
- source_excerpt: `comments.instance_mapping`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `structure`
- Bad example:
```text
comments.instance_mapping
```
- Good example:
```text
调整结构关系后重新检查组合锥、实例连接和相关下游节点。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-386"></a>
### VG064: instance mapping `.o_result_reserved` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:560`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.instance_mapping
- source_excerpt: `comments.instance_mapping`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `structure`
- Bad example:
```text
comments.instance_mapping
```
- Good example:
```text
调整结构关系后重新检查组合锥、实例连接和相关下游节点。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-387"></a>
### VG064: instance mapping `.o_meta_count` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:561`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.instance_mapping
- source_excerpt: `comments.instance_mapping`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `structure`
- Bad example:
```text
comments.instance_mapping
```
- Good example:
```text
调整结构关系后重新检查组合锥、实例连接和相关下游节点。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-388"></a>
### VG064: instance mapping `.o_mac_result_count` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:562`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.instance_mapping
- source_excerpt: `comments.instance_mapping`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `structure`
- Bad example:
```text
comments.instance_mapping
```
- Good example:
```text
调整结构关系后重新检查组合锥、实例连接和相关下游节点。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-389"></a>
### VG064: instance mapping `.o_pre_accept_count` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:563`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.instance_mapping
- source_excerpt: `comments.instance_mapping`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `structure`
- Bad example:
```text
comments.instance_mapping
```
- Good example:
```text
调整结构关系后重新检查组合锥、实例连接和相关下游节点。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-390"></a>
### VG064: instance mapping `.o_silu_accept_count` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:564`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.instance_mapping
- source_excerpt: `comments.instance_mapping`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `structure`
- Bad example:
```text
comments.instance_mapping
```
- Good example:
```text
调整结构关系后重新检查组合锥、实例连接和相关下游节点。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-391"></a>
### VG064: instance mapping `.o_post_accept_count` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:565`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.instance_mapping
- source_excerpt: `comments.instance_mapping`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `structure`
- Bad example:
```text
comments.instance_mapping
```
- Good example:
```text
调整结构关系后重新检查组合锥、实例连接和相关下游节点。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-392"></a>
### VG064: instance mapping `.o_writeback_count` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:566`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.instance_mapping
- source_excerpt: `comments.instance_mapping`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `structure`
- Bad example:
```text
comments.instance_mapping
```
- Good example:
```text
调整结构关系后重新检查组合锥、实例连接和相关下游节点。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-393"></a>
### VG065: signal `rx_ready_o` must be introduced by a group comment in `其他信号`.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_overlap_low_io_top.v:183`
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

<a id="vg-finding-394"></a>
### VG042: Comment coverage is too low for generated RTL (7.42%); add semantic comments near declarations, assigns, always blocks, FSM, and instances.
- Status: `failed`
- Severity: `error`
- Location: `file:road_dynamic_overlap_low_io_top.v:unknown`
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

<a id="vg-finding-395"></a>
### VG086: FSM 状态寄存器必须在复位路径进入已声明的常量初态。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:93`
- Evidence:
- node_kind: `verilog_rtl`
- detail: missing constant reset state
- source_excerpt: `missing constant reset state`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
missing constant reset state
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-396"></a>
### VG088: 存在无法静态确定宽度的分支条件。
- Status: `inconclusive`
- Severity: `WARNING`
- Location: `run:unknown`
- Evidence:
- node_kind: `verilog_project`
- detail: gate_id=VG088; rule_key=branch_cond_scalar; status=inconclusive; applicable=True; reason=存在无法静态确定宽度的分支条件。
- source_excerpt: `gate_id=VG088; rule_key=branch_cond_scalar; status=inconclusive; applicable=True; reason=存在无法静态确定宽度的分支条件。`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
gate_id=VG088; rule_key=branch_cond_scalar; status=inconclusive; applicable=True; reason=存在无法静态确定宽度的分支条件。
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-397"></a>
### VG093: 异步复位信号被连接到普通数据赋值右值。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:192`
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

<a id="vg-finding-398"></a>
### VG097: 缺少外部模块接口定义，无法静态比较端口位宽。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:517`
- Evidence:
- node_kind: `verilog_rtl`
- detail: down2_dynamic_tile_runner down2_dynamic_tile_runner_Inst_shell
- source_excerpt: `down2_dynamic_tile_runner down2_dynamic_tile_runner_Inst_shell`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
down2_dynamic_tile_runner down2_dynamic_tile_runner_Inst_shell
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-399"></a>
### VG098: FSM 缺少可信复位初态或 case(state_current) 转移图。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `run:unknown`
- Evidence:
- node_kind: `verilog_project`
- detail: gate_id=VG098; rule_key=fsm_no_dead_unreachable; status=inconclusive; applicable=True; reason=FSM 缺少可信复位初态或 case(state_current) 转移图。
- source_excerpt: `gate_id=VG098; rule_key=fsm_no_dead_unreachable; status=inconclusive; applicable=True; reason=FSM 缺少可信复位初态或 case(state_current) 转移图。`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
gate_id=VG098; rule_key=fsm_no_dead_unreachable; status=inconclusive; applicable=True; reason=FSM 缺少可信复位初态或 case(state_current) 转移图。
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-400"></a>
### VG109: 组合逻辑 if 链缺少终止 else。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_dynamic_overlap_low_io_top.v:238`
- Evidence:
- node_kind: `verilog_rtl`
- detail: if(flag_rx_transfer)
- source_excerpt: `if(flag_rx_transfer)`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
if(flag_rx_transfer)
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-401"></a>
### VG109: 组合逻辑 if 链缺少终止 else。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_dynamic_overlap_low_io_top.v:253`
- Evidence:
- node_kind: `verilog_rtl`
- detail: if(flag_table_transfer && (reg_table_addr == 10'd1023))
- source_excerpt: `if(flag_table_transfer && (reg_table_addr == 10'd1023))`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
if(flag_table_transfer && (reg_table_addr == 10'd1023))
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-402"></a>
### VG109: 组合逻辑 if 链缺少终止 else。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_dynamic_overlap_low_io_top.v:238`
- Evidence:
- node_kind: `verilog_rtl`
- detail: if(flag_rx_transfer)
- source_excerpt: `if(flag_rx_transfer)`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
if(flag_rx_transfer)
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-403"></a>
### VG109: 组合逻辑 if 链缺少终止 else。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_dynamic_overlap_low_io_top.v:238`
- Evidence:
- node_kind: `verilog_rtl`
- detail: if(flag_rx_transfer)
- source_excerpt: `if(flag_rx_transfer)`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
if(flag_rx_transfer)
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-404"></a>
### VG109: 组合逻辑 if 链缺少终止 else。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_dynamic_overlap_low_io_top.v:238`
- Evidence:
- node_kind: `verilog_rtl`
- detail: if(flag_rx_transfer)
- source_excerpt: `if(flag_rx_transfer)`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
if(flag_rx_transfer)
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-405"></a>
### VG109: 组合逻辑 if 链缺少终止 else。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_dynamic_overlap_low_io_top.v:273`
- Evidence:
- node_kind: `verilog_rtl`
- detail: if(flag_load_transfer)
- source_excerpt: `if(flag_load_transfer)`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
if(flag_load_transfer)
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-406"></a>
### VG109: 组合逻辑 if 链缺少终止 else。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_dynamic_overlap_low_io_top.v:280`
- Evidence:
- node_kind: `verilog_rtl`
- detail: if(reg_export_done_seen)
- source_excerpt: `if(reg_export_done_seen)`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
if(reg_export_done_seen)
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-407"></a>
### VG109: 组合逻辑 if 链缺少终止 else。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_dynamic_overlap_low_io_top.v:285`
- Evidence:
- node_kind: `verilog_rtl`
- detail: if(flag_tx_transfer)
- source_excerpt: `if(flag_tx_transfer)`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
if(flag_tx_transfer)
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-408"></a>
### VG109: 组合逻辑 if 链缺少终止 else。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_dynamic_overlap_low_io_top.v:285`
- Evidence:
- node_kind: `verilog_rtl`
- detail: if(flag_tx_transfer)
- source_excerpt: `if(flag_tx_transfer)`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
if(flag_tx_transfer)
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-409"></a>
### VG109: 组合逻辑 if 链缺少终止 else。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_dynamic_overlap_low_io_top.v:285`
- Evidence:
- node_kind: `verilog_rtl`
- detail: if(flag_tx_transfer)
- source_excerpt: `if(flag_tx_transfer)`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
if(flag_tx_transfer)
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-410"></a>
### VG109: 组合逻辑 if 链缺少终止 else。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_dynamic_overlap_low_io_top.v:285`
- Evidence:
- node_kind: `verilog_rtl`
- detail: if(flag_tx_transfer)
- source_excerpt: `if(flag_tx_transfer)`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
if(flag_tx_transfer)
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-411"></a>
### VG109: 组合逻辑 if 链缺少终止 else。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_dynamic_overlap_low_io_top.v:305`
- Evidence:
- node_kind: `verilog_rtl`
- detail: if(flag_tx_transfer && (cnt_status_index == 5'd30))
- source_excerpt: `if(flag_tx_transfer && (cnt_status_index == 5'd30))`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
if(flag_tx_transfer && (cnt_status_index == 5'd30))
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-412"></a>
### VG122: 算术结果位宽超过赋值目标位宽。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:481`
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

<a id="vg-finding-413"></a>
### VG122: 算术结果位宽超过赋值目标位宽。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:511`
- Evidence:
- node_kind: `verilog_rtl`
- detail: cnt_status_index <= cnt_status_index + 1'b1;
- source_excerpt: `cnt_status_index <= cnt_status_index + 1'b1;`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
cnt_status_index <= cnt_status_index + 1'b1;
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-414"></a>
### VG125: 字面量声明为 5 位，但实际值只需要 1 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:317`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 5'd1
- source_excerpt: `5'd1`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
5'd1
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-415"></a>
### VG125: 字面量声明为 5 位，但实际值只需要 2 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:318`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 5'd2
- source_excerpt: `5'd2`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
5'd2
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-416"></a>
### VG125: 字面量声明为 5 位，但实际值只需要 2 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:319`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 5'd3
- source_excerpt: `5'd3`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
5'd3
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-417"></a>
### VG125: 字面量声明为 5 位，但实际值只需要 3 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:320`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 5'd4
- source_excerpt: `5'd4`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
5'd4
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-418"></a>
### VG125: 字面量声明为 5 位，但实际值只需要 3 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:321`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 5'd5
- source_excerpt: `5'd5`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
5'd5
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-419"></a>
### VG125: 字面量声明为 5 位，但实际值只需要 3 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:322`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 5'd6
- source_excerpt: `5'd6`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
5'd6
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-420"></a>
### VG125: 字面量声明为 5 位，但实际值只需要 3 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:323`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 5'd7
- source_excerpt: `5'd7`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
5'd7
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-421"></a>
### VG125: 字面量声明为 5 位，但实际值只需要 4 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:324`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 5'd8
- source_excerpt: `5'd8`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
5'd8
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-422"></a>
### VG125: 字面量声明为 5 位，但实际值只需要 4 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:325`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 5'd9
- source_excerpt: `5'd9`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
5'd9
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-423"></a>
### VG125: 字面量声明为 5 位，但实际值只需要 4 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:326`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 5'd10
- source_excerpt: `5'd10`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
5'd10
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-424"></a>
### VG125: 字面量声明为 5 位，但实际值只需要 4 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:327`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 5'd11
- source_excerpt: `5'd11`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
5'd11
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-425"></a>
### VG125: 字面量声明为 5 位，但实际值只需要 4 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:328`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 5'd12
- source_excerpt: `5'd12`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
5'd12
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-426"></a>
### VG125: 字面量声明为 5 位，但实际值只需要 4 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:329`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 5'd13
- source_excerpt: `5'd13`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
5'd13
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-427"></a>
### VG125: 字面量声明为 5 位，但实际值只需要 4 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:330`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 5'd14
- source_excerpt: `5'd14`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
5'd14
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-428"></a>
### VG125: 字面量声明为 5 位，但实际值只需要 4 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:331`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 5'd15
- source_excerpt: `5'd15`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
5'd15
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-429"></a>
### VG125: 字面量声明为 10 位，但实际值只需要 1 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:481`
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

<a id="vg-finding-430"></a>
### VG132: 未登记原语或外部模块的时钟角色无法静态确定。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:517`
- Evidence:
- node_kind: `verilog_rtl`
- detail: down2_dynamic_tile_runner down2_dynamic_tile_runner_Inst_shell
- source_excerpt: `down2_dynamic_tile_runner down2_dynamic_tile_runner_Inst_shell`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
down2_dynamic_tile_runner down2_dynamic_tile_runner_Inst_shell
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-431"></a>
### VG145: 组合逻辑完整依赖锥最多允许三个源信号，超限逻辑必须由时序 reg 隔断。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:314`
- Evidence:
- node_kind: `verilog_rtl`
- detail: dec_status_word: 32 sources: cnt_status_index, reg_snapshot_core[15:0], reg_snapshot_core[31:16], reg_snapshot_export_cycles[15:0], reg_snapshot_export_cycles[31:16], reg_snapshot_flags, reg_snapshot_mac_cycles[15:0], reg_snapshot_mac_cycles[31:16], reg_snapshot_mac_results[15:0], reg_snapshot_mac_results[31:16], reg_snapshot_post_accepts[15:0], reg_snapshot_post_accepts[31:16], reg_snapshot_post_cycles[15:0], reg_snapshot_post_cycles[31:16], reg_snapshot_pre_accepts[15:0], reg_snapshot_pre_accepts[31:16], reg_snapshot_pre_cycles[15:0], reg_snapshot_pre_cycles[31:16], reg_snapshot_preload[15:0], reg_snapshot_preload[31:16], reg_snapshot_scheduler_idle[15:0], reg_snapshot_scheduler_idle[31:16], reg_snapshot_silu_accepts[15:0], reg_snapshot_silu_accepts[31:16], reg_snapshot_silu_cycles[15:0], reg_snapshot_silu_cycles[31:16], reg_snapshot_storage_wait[15:0], reg_snapshot_storage_wait[31:16], reg_snapshot_writeback_cycles[15:0], reg_snapshot_writeback_cycles[31:16], reg_snapshot_writebacks[15:0], reg_snapshot_writebacks[31:16]
- source_excerpt: `dec_status_word: 32 sources: cnt_status_index, reg_snapshot_core[15:0], reg_snapshot_core[31:16], reg_snapshot_export_cycles[15:0], reg_snapshot_export_cycles[31:16], reg_snapshot_flags, reg_snapshot_mac_cycles[15:0], reg_snapshot_mac_cycles[31:16], reg_snapshot_mac_results[15:0], reg_snapshot_mac_results[31:16], reg_snapshot_post_accepts[15:0], reg_snapshot_post_accepts[31:16], reg_snapshot_post_cycles[15:0], reg_snapshot_post_cycles[31:16], reg_snapshot_pre_accepts[15:0], reg_snapshot_pre_accepts[31:16], reg_snapshot_pre_cycles[15:0], reg_snapshot_pre_cycles[31:16], reg_snapshot_preload[15:0], reg_snapshot_preload[31:16], reg_snapshot_scheduler_idle[15:0], reg_snapshot_scheduler_idle[31:16], reg_snapshot_silu_accepts[15:0], reg_snapshot_silu_accepts[31:16], reg_snapshot_silu_cycles[15:0], reg_snapshot_silu_cycles[31:16], reg_snapshot_storage_wait[15:0], reg_snapshot_storage_wait[31:16], reg_snapshot_writeback_cycles[15:0], reg_snapshot_writeback_cycles[31:16], reg_snapshot_writebacks[15:0], reg_snapshot_writebacks[31:16]`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
dec_status_word: 32 sources: cnt_status_index, reg_snapshot_core[15:0], reg_snapshot_core[31:16], reg_snapshot_export_cycles[15:0], reg_snapshot_export_cycles[31:16], reg_snapshot_flags, reg_snapshot_mac_cycles[15:0], reg_snapshot_mac_cycles[31:16], reg_snapshot_mac_results[15:0], reg_snapshot_mac_results[31:16], reg_snapshot_post_accepts[15:0], reg_snapshot_post_accepts[31:16], reg_snapshot_post_cycles[15:0], reg_snapshot_post_cycles[31:16], reg_snapshot_pre_accepts[15:0], reg_snapshot_pre_accepts[31:16], reg_snapshot_pre_cycles[15:0], reg_snapshot_pre_cycles[31:16], reg_snapshot_preload[15:0], reg_snapshot_preload[31:16], reg_snapshot_scheduler_idle[15:0], reg_snapshot_scheduler_idle[31:16], reg_snapshot_silu_accepts[15:0], reg_snapshot_silu_accepts[31:16], reg_snapshot_silu_cycles[15:0], reg_snapshot_silu_cycles[31:16], reg_snapshot_storage_wait[15:0], reg_snapshot_storage_wait[31:16], reg_snapshot_writeback_cycles[15:0], reg_snapshot_writeback_cycles[31:16], reg_snapshot_writebacks[15:0], reg_snapshot_writebacks[31:16]
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-432"></a>
### VG145: 组合逻辑完整依赖锥最多允许三个源信号，超限逻辑必须由时序 reg 隔断。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:193`
- Evidence:
- node_kind: `verilog_rtl`
- detail: flag_rx_transfer: 5 sources: i_rstn, i_rx_valid, reg_release_done, runner_table_ready, state_current
- source_excerpt: `flag_rx_transfer: 5 sources: i_rstn, i_rx_valid, reg_release_done, runner_table_ready, state_current`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
flag_rx_transfer: 5 sources: i_rstn, i_rx_valid, reg_release_done, runner_table_ready, state_current
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-433"></a>
### VG145: 组合逻辑完整依赖锥最多允许三个源信号，超限逻辑必须由时序 reg 隔断。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:196`
- Evidence:
- node_kind: `verilog_rtl`
- detail: flag_table_transfer: 5 sources: i_rstn, i_rx_valid, reg_release_done, runner_table_ready, state_current
- source_excerpt: `flag_table_transfer: 5 sources: i_rstn, i_rx_valid, reg_release_done, runner_table_ready, state_current`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
flag_table_transfer: 5 sources: i_rstn, i_rx_valid, reg_release_done, runner_table_ready, state_current
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-434"></a>
### VG145: 组合逻辑完整依赖锥最多允许三个源信号，超限逻辑必须由时序 reg 隔断。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:194`
- Evidence:
- node_kind: `verilog_rtl`
- detail: flag_tx_transfer: 5 sources: i_rstn, i_tx_ready, reg_release_done, runner_output_valid, state_current
- source_excerpt: `flag_tx_transfer: 5 sources: i_rstn, i_tx_ready, reg_release_done, runner_output_valid, state_current`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
flag_tx_transfer: 5 sources: i_rstn, i_tx_ready, reg_release_done, runner_output_valid, state_current
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-435"></a>
### VG145: 组合逻辑完整依赖锥最多允许三个源信号，超限逻辑必须由时序 reg 隔断。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:202`
- Evidence:
- node_kind: `verilog_rtl`
- detail: o_rx_ready: 4 sources: i_rstn, reg_release_done, runner_table_ready, state_current
- source_excerpt: `o_rx_ready: 4 sources: i_rstn, reg_release_done, runner_table_ready, state_current`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
o_rx_ready: 4 sources: i_rstn, reg_release_done, runner_table_ready, state_current
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-436"></a>
### VG145: 组合逻辑完整依赖锥最多允许三个源信号，超限逻辑必须由时序 reg 隔断。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:204`
- Evidence:
- node_kind: `verilog_rtl`
- detail: o_tx_data: 37 sources: cnt_status_index, reg_shell_fault, reg_snapshot_core[15:0], reg_snapshot_core[31:16], reg_snapshot_export_cycles[15:0], reg_snapshot_export_cycles[31:16], reg_snapshot_flags, reg_snapshot_mac_cycles[15:0], reg_snapshot_mac_cycles[31:16], reg_snapshot_mac_results[15:0], reg_snapshot_mac_results[31:16], reg_snapshot_post_accepts[15:0], reg_snapshot_post_accepts[31:16], reg_snapshot_post_cycles[15:0], reg_snapshot_post_cycles[31:16], reg_snapshot_pre_accepts[15:0], reg_snapshot_pre_accepts[31:16], reg_snapshot_pre_cycles[15:0], reg_snapshot_pre_cycles[31:16], reg_snapshot_preload[15:0], reg_snapshot_preload[31:16], reg_snapshot_scheduler_idle[15:0], reg_snapshot_scheduler_idle[31:16], reg_snapshot_silu_accepts[15:0], reg_snapshot_silu_accepts[31:16], reg_snapshot_silu_cycles[15:0], reg_snapshot_silu_cycles[31:16], reg_snapshot_storage_wait[15:0], reg_snapshot_storage_wait[31:16], reg_snapshot_writeback_cycles[15:0], reg_snapshot_writeback_cycles[31:16], reg_snapshot_writebacks[15:0], reg_snapshot_writebacks[31:16], runner_fault, runner_output_data, runner_output_index, state_current
- source_excerpt: `o_tx_data: 37 sources: cnt_status_index, reg_shell_fault, reg_snapshot_core[15:0], reg_snapshot_core[31:16], reg_snapshot_export_cycles[15:0], reg_snapshot_export_cycles[31:16], reg_snapshot_flags, reg_snapshot_mac_cycles[15:0], reg_snapshot_mac_cycles[31:16], reg_snapshot_mac_results[15:0], reg_snapshot_mac_results[31:16], reg_snapshot_post_accepts[15:0], reg_snapshot_post_accepts[31:16], reg_snapshot_post_cycles[15:0], reg_snapshot_post_cycles[31:16], reg_snapshot_pre_accepts[15:0], reg_snapshot_pre_accepts[31:16], reg_snapshot_pre_cycles[15:0], reg_snapshot_pre_cycles[31:16], reg_snapshot_preload[15:0], reg_snapshot_preload[31:16], reg_snapshot_scheduler_idle[15:0], reg_snapshot_scheduler_idle[31:16], reg_snapshot_silu_accepts[15:0], reg_snapshot_silu_accepts[31:16], reg_snapshot_silu_cycles[15:0], reg_snapshot_silu_cycles[31:16], reg_snapshot_storage_wait[15:0], reg_snapshot_storage_wait[31:16], reg_snapshot_writeback_cycles[15:0], reg_snapshot_writeback_cycles[31:16], reg_snapshot_writebacks[15:0], reg_snapshot_writebacks[31:16], runner_fault, runner_output_data, runner_output_index, state_current`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
o_tx_data: 37 sources: cnt_status_index, reg_shell_fault, reg_snapshot_core[15:0], reg_snapshot_core[31:16], reg_snapshot_export_cycles[15:0], reg_snapshot_export_cycles[31:16], reg_snapshot_flags, reg_snapshot_mac_cycles[15:0], reg_snapshot_mac_cycles[31:16], reg_snapshot_mac_results[15:0], reg_snapshot_mac_results[31:16], reg_snapshot_post_accepts[15:0], reg_snapshot_post_accepts[31:16], reg_snapshot_post_cycles[15:0], reg_snapshot_post_cycles[31:16], reg_snapshot_pre_accepts[15:0], reg_snapshot_pre_accepts[31:16], reg_snapshot_pre_cycles[15:0], reg_snapshot_pre_cycles[31:16], reg_snapshot_preload[15:0], reg_snapshot_preload[31:16], reg_snapshot_scheduler_idle[15:0], reg_snapshot_scheduler_idle[31:16], reg_snapshot_silu_accepts[15:0], reg_snapshot_silu_accepts[31:16], reg_snapshot_silu_cycles[15:0], reg_snapshot_silu_cycles[31:16], reg_snapshot_storage_wait[15:0], reg_snapshot_storage_wait[31:16], reg_snapshot_writeback_cycles[15:0], reg_snapshot_writeback_cycles[31:16], reg_snapshot_writebacks[15:0], reg_snapshot_writebacks[31:16], runner_fault, runner_output_data, runner_output_index, state_current
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-437"></a>
### VG145: 组合逻辑完整依赖锥最多允许三个源信号，超限逻辑必须由时序 reg 隔断。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:203`
- Evidence:
- node_kind: `verilog_rtl`
- detail: o_tx_valid: 4 sources: i_rstn, reg_release_done, runner_output_valid, state_current
- source_excerpt: `o_tx_valid: 4 sources: i_rstn, reg_release_done, runner_output_valid, state_current`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
o_tx_valid: 4 sources: i_rstn, reg_release_done, runner_output_valid, state_current
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-438"></a>
### VG145: 组合逻辑完整依赖锥最多允许三个源信号，超限逻辑必须由时序 reg 隔断。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:199`
- Evidence:
- node_kind: `verilog_rtl`
- detail: runner_output_ready: 4 sources: i_rstn, i_tx_ready, reg_release_done, state_current
- source_excerpt: `runner_output_ready: 4 sources: i_rstn, i_tx_ready, reg_release_done, state_current`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
runner_output_ready: 4 sources: i_rstn, i_tx_ready, reg_release_done, state_current
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-439"></a>
### VG145: 组合逻辑完整依赖锥最多允许三个源信号，超限逻辑必须由时序 reg 隔断。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:195`
- Evidence:
- node_kind: `verilog_rtl`
- detail: runner_table_valid: 4 sources: i_rstn, i_rx_valid, reg_release_done, state_current
- source_excerpt: `runner_table_valid: 4 sources: i_rstn, i_rx_valid, reg_release_done, state_current`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
runner_table_valid: 4 sources: i_rstn, i_rx_valid, reg_release_done, state_current
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-440"></a>
### VG145: 组合逻辑完整依赖锥最多允许三个源信号，超限逻辑必须由时序 reg 隔断。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:234`
- Evidence:
- node_kind: `verilog_rtl`
- detail: state_next: 17 sources: cnt_status_index, i_rstn, i_rx_data, i_rx_data[12:11], i_rx_valid, i_tx_ready, reg_export_done_seen, reg_load_pending, reg_release_done, reg_runner_done_seen, reg_table_addr, runner_busy, runner_fault, runner_load_ready, runner_output_valid, runner_table_ready, state_current
- source_excerpt: `state_next: 17 sources: cnt_status_index, i_rstn, i_rx_data, i_rx_data[12:11], i_rx_valid, i_tx_ready, reg_export_done_seen, reg_load_pending, reg_release_done, reg_runner_done_seen, reg_table_addr, runner_busy, runner_fault, runner_load_ready, runner_output_valid, runner_table_ready, state_current`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
state_next: 17 sources: cnt_status_index, i_rstn, i_rx_data, i_rx_data[12:11], i_rx_valid, i_tx_ready, reg_export_done_seen, reg_load_pending, reg_release_done, reg_runner_done_seen, reg_table_addr, runner_busy, runner_fault, runner_load_ready, runner_output_valid, runner_table_ready, state_current
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-441"></a>
### VG145: 组合逻辑完整依赖锥最多允许三个源信号，超限逻辑必须由时序 reg 隔断。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:351`
- Evidence:
- node_kind: `verilog_rtl`
- detail: tx_data_o: 37 sources: cnt_status_index, reg_shell_fault, reg_snapshot_core[15:0], reg_snapshot_core[31:16], reg_snapshot_export_cycles[15:0], reg_snapshot_export_cycles[31:16], reg_snapshot_flags, reg_snapshot_mac_cycles[15:0], reg_snapshot_mac_cycles[31:16], reg_snapshot_mac_results[15:0], reg_snapshot_mac_results[31:16], reg_snapshot_post_accepts[15:0], reg_snapshot_post_accepts[31:16], reg_snapshot_post_cycles[15:0], reg_snapshot_post_cycles[31:16], reg_snapshot_pre_accepts[15:0], reg_snapshot_pre_accepts[31:16], reg_snapshot_pre_cycles[15:0], reg_snapshot_pre_cycles[31:16], reg_snapshot_preload[15:0], reg_snapshot_preload[31:16], reg_snapshot_scheduler_idle[15:0], reg_snapshot_scheduler_idle[31:16], reg_snapshot_silu_accepts[15:0], reg_snapshot_silu_accepts[31:16], reg_snapshot_silu_cycles[15:0], reg_snapshot_silu_cycles[31:16], reg_snapshot_storage_wait[15:0], reg_snapshot_storage_wait[31:16], reg_snapshot_writeback_cycles[15:0], reg_snapshot_writeback_cycles[31:16], reg_snapshot_writebacks[15:0], reg_snapshot_writebacks[31:16], runner_fault, runner_output_data, runner_output_index, state_current
- source_excerpt: `tx_data_o: 37 sources: cnt_status_index, reg_shell_fault, reg_snapshot_core[15:0], reg_snapshot_core[31:16], reg_snapshot_export_cycles[15:0], reg_snapshot_export_cycles[31:16], reg_snapshot_flags, reg_snapshot_mac_cycles[15:0], reg_snapshot_mac_cycles[31:16], reg_snapshot_mac_results[15:0], reg_snapshot_mac_results[31:16], reg_snapshot_post_accepts[15:0], reg_snapshot_post_accepts[31:16], reg_snapshot_post_cycles[15:0], reg_snapshot_post_cycles[31:16], reg_snapshot_pre_accepts[15:0], reg_snapshot_pre_accepts[31:16], reg_snapshot_pre_cycles[15:0], reg_snapshot_pre_cycles[31:16], reg_snapshot_preload[15:0], reg_snapshot_preload[31:16], reg_snapshot_scheduler_idle[15:0], reg_snapshot_scheduler_idle[31:16], reg_snapshot_silu_accepts[15:0], reg_snapshot_silu_accepts[31:16], reg_snapshot_silu_cycles[15:0], reg_snapshot_silu_cycles[31:16], reg_snapshot_storage_wait[15:0], reg_snapshot_storage_wait[31:16], reg_snapshot_writeback_cycles[15:0], reg_snapshot_writeback_cycles[31:16], reg_snapshot_writebacks[15:0], reg_snapshot_writebacks[31:16], runner_fault, runner_output_data, runner_output_index, state_current`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
tx_data_o: 37 sources: cnt_status_index, reg_shell_fault, reg_snapshot_core[15:0], reg_snapshot_core[31:16], reg_snapshot_export_cycles[15:0], reg_snapshot_export_cycles[31:16], reg_snapshot_flags, reg_snapshot_mac_cycles[15:0], reg_snapshot_mac_cycles[31:16], reg_snapshot_mac_results[15:0], reg_snapshot_mac_results[31:16], reg_snapshot_post_accepts[15:0], reg_snapshot_post_accepts[31:16], reg_snapshot_post_cycles[15:0], reg_snapshot_post_cycles[31:16], reg_snapshot_pre_accepts[15:0], reg_snapshot_pre_accepts[31:16], reg_snapshot_pre_cycles[15:0], reg_snapshot_pre_cycles[31:16], reg_snapshot_preload[15:0], reg_snapshot_preload[31:16], reg_snapshot_scheduler_idle[15:0], reg_snapshot_scheduler_idle[31:16], reg_snapshot_silu_accepts[15:0], reg_snapshot_silu_accepts[31:16], reg_snapshot_silu_cycles[15:0], reg_snapshot_silu_cycles[31:16], reg_snapshot_storage_wait[15:0], reg_snapshot_storage_wait[31:16], reg_snapshot_writeback_cycles[15:0], reg_snapshot_writeback_cycles[31:16], reg_snapshot_writebacks[15:0], reg_snapshot_writebacks[31:16], runner_fault, runner_output_data, runner_output_index, state_current
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-442"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=cnt_status_index$enable; child_output=road_dynamic_overlap_low_io_top.cnt_status_index$enable; operation_count=11; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=cnt_status_index$enable; child_output=road_dynamic_overlap_low_io_top.cnt_status_index$enable; operation_count=11; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=cnt_status_index$enable; child_output=road_dynamic_overlap_low_io_top.cnt_status_index$enable; operation_count=11; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-443"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_commit_ready$enable; child_output=road_dynamic_overlap_low_io_top.reg_commit_ready$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_commit_ready$enable; child_output=road_dynamic_overlap_low_io_top.reg_commit_ready$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_commit_ready$enable; child_output=road_dynamic_overlap_low_io_top.reg_commit_ready$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-444"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_export_done_seen$enable; child_output=road_dynamic_overlap_low_io_top.reg_export_done_seen$enable; operation_count=13; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_export_done_seen$enable; child_output=road_dynamic_overlap_low_io_top.reg_export_done_seen$enable; operation_count=13; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_export_done_seen$enable; child_output=road_dynamic_overlap_low_io_top.reg_export_done_seen$enable; operation_count=13; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-445"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_export_start$enable; child_output=road_dynamic_overlap_low_io_top.reg_export_start$enable; operation_count=9; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_export_start$enable; child_output=road_dynamic_overlap_low_io_top.reg_export_start$enable; operation_count=9; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_export_start$enable; child_output=road_dynamic_overlap_low_io_top.reg_export_start$enable; operation_count=9; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-446"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_load_addr$enable; child_output=road_dynamic_overlap_low_io_top.reg_load_addr$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_load_addr$enable; child_output=road_dynamic_overlap_low_io_top.reg_load_addr$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_load_addr$enable; child_output=road_dynamic_overlap_low_io_top.reg_load_addr$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-447"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_load_data$enable; child_output=road_dynamic_overlap_low_io_top.reg_load_data$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_load_data$enable; child_output=road_dynamic_overlap_low_io_top.reg_load_data$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_load_data$enable; child_output=road_dynamic_overlap_low_io_top.reg_load_data$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-448"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_load_kind$enable; child_output=road_dynamic_overlap_low_io_top.reg_load_kind$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_load_kind$enable; child_output=road_dynamic_overlap_low_io_top.reg_load_kind$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_load_kind$enable; child_output=road_dynamic_overlap_low_io_top.reg_load_kind$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-449"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_load_low$enable; child_output=road_dynamic_overlap_low_io_top.reg_load_low$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_load_low$enable; child_output=road_dynamic_overlap_low_io_top.reg_load_low$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_load_low$enable; child_output=road_dynamic_overlap_low_io_top.reg_load_low$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-450"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_load_pending$enable; child_output=road_dynamic_overlap_low_io_top.reg_load_pending$enable; operation_count=8; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_load_pending$enable; child_output=road_dynamic_overlap_low_io_top.reg_load_pending$enable; operation_count=8; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_load_pending$enable; child_output=road_dynamic_overlap_low_io_top.reg_load_pending$enable; operation_count=8; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-451"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_pw_only$enable; child_output=road_dynamic_overlap_low_io_top.reg_pw_only$enable; operation_count=7; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_pw_only$enable; child_output=road_dynamic_overlap_low_io_top.reg_pw_only$enable; operation_count=7; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_pw_only$enable; child_output=road_dynamic_overlap_low_io_top.reg_pw_only$enable; operation_count=7; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-452"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_runner_done_seen$enable; child_output=road_dynamic_overlap_low_io_top.reg_runner_done_seen$enable; operation_count=7; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_runner_done_seen$enable; child_output=road_dynamic_overlap_low_io_top.reg_runner_done_seen$enable; operation_count=7; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_runner_done_seen$enable; child_output=road_dynamic_overlap_low_io_top.reg_runner_done_seen$enable; operation_count=7; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-453"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_shell_fault$enable; child_output=road_dynamic_overlap_low_io_top.reg_shell_fault$enable; operation_count=15; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_shell_fault$enable; child_output=road_dynamic_overlap_low_io_top.reg_shell_fault$enable; operation_count=15; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_shell_fault$enable; child_output=road_dynamic_overlap_low_io_top.reg_shell_fault$enable; operation_count=15; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-454"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_core$D; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_core$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_core$D; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_core$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_core$D; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_core$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-455"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_core$enable; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_core$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_core$enable; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_core$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_core$enable; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_core$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-456"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_export_cycles$D; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_export_cycles$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_export_cycles$D; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_export_cycles$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_export_cycles$D; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_export_cycles$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-457"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_export_cycles$enable; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_export_cycles$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_export_cycles$enable; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_export_cycles$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_export_cycles$enable; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_export_cycles$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-458"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_flags$D; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_flags$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_flags$D; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_flags$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_flags$D; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_flags$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-459"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_flags$enable; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_flags$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_flags$enable; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_flags$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_flags$enable; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_flags$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-460"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_mac_cycles$D; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_mac_cycles$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_mac_cycles$D; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_mac_cycles$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_mac_cycles$D; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_mac_cycles$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-461"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_mac_cycles$enable; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_mac_cycles$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_mac_cycles$enable; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_mac_cycles$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_mac_cycles$enable; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_mac_cycles$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-462"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_mac_results$D; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_mac_results$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_mac_results$D; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_mac_results$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_mac_results$D; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_mac_results$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-463"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_mac_results$enable; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_mac_results$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_mac_results$enable; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_mac_results$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_mac_results$enable; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_mac_results$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-464"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_post_accepts$D; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_post_accepts$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_post_accepts$D; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_post_accepts$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_post_accepts$D; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_post_accepts$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-465"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_post_accepts$enable; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_post_accepts$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_post_accepts$enable; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_post_accepts$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_post_accepts$enable; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_post_accepts$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-466"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_post_cycles$D; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_post_cycles$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_post_cycles$D; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_post_cycles$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_post_cycles$D; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_post_cycles$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-467"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_post_cycles$enable; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_post_cycles$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_post_cycles$enable; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_post_cycles$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_post_cycles$enable; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_post_cycles$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-468"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_pre_accepts$D; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_pre_accepts$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_pre_accepts$D; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_pre_accepts$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_pre_accepts$D; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_pre_accepts$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-469"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_pre_accepts$enable; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_pre_accepts$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_pre_accepts$enable; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_pre_accepts$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_pre_accepts$enable; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_pre_accepts$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-470"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_pre_cycles$D; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_pre_cycles$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_pre_cycles$D; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_pre_cycles$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_pre_cycles$D; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_pre_cycles$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-471"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_pre_cycles$enable; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_pre_cycles$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_pre_cycles$enable; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_pre_cycles$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_pre_cycles$enable; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_pre_cycles$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-472"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_preload$D; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_preload$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_preload$D; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_preload$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_preload$D; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_preload$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-473"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_preload$enable; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_preload$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_preload$enable; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_preload$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_preload$enable; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_preload$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-474"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_scheduler_idle$D; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_scheduler_idle$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_scheduler_idle$D; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_scheduler_idle$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_scheduler_idle$D; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_scheduler_idle$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-475"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_scheduler_idle$enable; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_scheduler_idle$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_scheduler_idle$enable; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_scheduler_idle$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_scheduler_idle$enable; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_scheduler_idle$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-476"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_silu_accepts$D; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_silu_accepts$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_silu_accepts$D; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_silu_accepts$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_silu_accepts$D; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_silu_accepts$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-477"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_silu_accepts$enable; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_silu_accepts$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_silu_accepts$enable; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_silu_accepts$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_silu_accepts$enable; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_silu_accepts$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-478"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_silu_cycles$D; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_silu_cycles$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_silu_cycles$D; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_silu_cycles$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_silu_cycles$D; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_silu_cycles$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-479"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_silu_cycles$enable; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_silu_cycles$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_silu_cycles$enable; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_silu_cycles$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_silu_cycles$enable; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_silu_cycles$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-480"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_storage_wait$D; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_storage_wait$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_storage_wait$D; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_storage_wait$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_storage_wait$D; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_storage_wait$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-481"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_storage_wait$enable; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_storage_wait$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_storage_wait$enable; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_storage_wait$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_storage_wait$enable; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_storage_wait$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-482"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_writeback_cycles$D; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_writeback_cycles$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_writeback_cycles$D; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_writeback_cycles$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_writeback_cycles$D; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_writeback_cycles$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-483"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_writeback_cycles$enable; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_writeback_cycles$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_writeback_cycles$enable; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_writeback_cycles$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_writeback_cycles$enable; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_writeback_cycles$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-484"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_writebacks$D; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_writebacks$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_writebacks$D; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_writebacks$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_writebacks$D; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_writebacks$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-485"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_writebacks$enable; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_writebacks$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_writebacks$enable; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_writebacks$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_writebacks$enable; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_writebacks$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-486"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_start$enable; child_output=road_dynamic_overlap_low_io_top.reg_start$enable; operation_count=7; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_start$enable; child_output=road_dynamic_overlap_low_io_top.reg_start$enable; operation_count=7; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_start$enable; child_output=road_dynamic_overlap_low_io_top.reg_start$enable; operation_count=7; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-487"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_table_addr$D; child_output=road_dynamic_overlap_low_io_top.reg_table_addr$D; operation_count=1; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_table_addr$D; child_output=road_dynamic_overlap_low_io_top.reg_table_addr$D; operation_count=1; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_table_addr$D; child_output=road_dynamic_overlap_low_io_top.reg_table_addr$D; operation_count=1; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-488"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_table_addr$enable; child_output=road_dynamic_overlap_low_io_top.reg_table_addr$enable; operation_count=11; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_table_addr$enable; child_output=road_dynamic_overlap_low_io_top.reg_table_addr$enable; operation_count=11; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_table_addr$enable; child_output=road_dynamic_overlap_low_io_top.reg_table_addr$enable; operation_count=11; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-489"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_busy; child_output=road_dynamic_overlap_low_io_top.runner_busy; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_busy; child_output=road_dynamic_overlap_low_io_top.runner_busy; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_busy; child_output=road_dynamic_overlap_low_io_top.runner_busy; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-490"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_core_cycles; child_output=road_dynamic_overlap_low_io_top.runner_core_cycles; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_core_cycles; child_output=road_dynamic_overlap_low_io_top.runner_core_cycles; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_core_cycles; child_output=road_dynamic_overlap_low_io_top.runner_core_cycles; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-491"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_debug_channel; child_output=road_dynamic_overlap_low_io_top.runner_debug_channel; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_debug_channel; child_output=road_dynamic_overlap_low_io_top.runner_debug_channel; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_debug_channel; child_output=road_dynamic_overlap_low_io_top.runner_debug_channel; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-492"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_debug_layer; child_output=road_dynamic_overlap_low_io_top.runner_debug_layer; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_debug_layer; child_output=road_dynamic_overlap_low_io_top.runner_debug_layer; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_debug_layer; child_output=road_dynamic_overlap_low_io_top.runner_debug_layer; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-493"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_debug_phase; child_output=road_dynamic_overlap_low_io_top.runner_debug_phase; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_debug_phase; child_output=road_dynamic_overlap_low_io_top.runner_debug_phase; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_debug_phase; child_output=road_dynamic_overlap_low_io_top.runner_debug_phase; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-494"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_debug_position; child_output=road_dynamic_overlap_low_io_top.runner_debug_position; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_debug_position; child_output=road_dynamic_overlap_low_io_top.runner_debug_position; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_debug_position; child_output=road_dynamic_overlap_low_io_top.runner_debug_position; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-495"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_debug_valid; child_output=road_dynamic_overlap_low_io_top.runner_debug_valid; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_debug_valid; child_output=road_dynamic_overlap_low_io_top.runner_debug_valid; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_debug_valid; child_output=road_dynamic_overlap_low_io_top.runner_debug_valid; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-496"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_debug_value; child_output=road_dynamic_overlap_low_io_top.runner_debug_value; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_debug_value; child_output=road_dynamic_overlap_low_io_top.runner_debug_value; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_debug_value; child_output=road_dynamic_overlap_low_io_top.runner_debug_value; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-497"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_done; child_output=road_dynamic_overlap_low_io_top.runner_done; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_done; child_output=road_dynamic_overlap_low_io_top.runner_done; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_done; child_output=road_dynamic_overlap_low_io_top.runner_done; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-498"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_export_cycles; child_output=road_dynamic_overlap_low_io_top.runner_export_cycles; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_export_cycles; child_output=road_dynamic_overlap_low_io_top.runner_export_cycles; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_export_cycles; child_output=road_dynamic_overlap_low_io_top.runner_export_cycles; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-499"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_export_done; child_output=road_dynamic_overlap_low_io_top.runner_export_done; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_export_done; child_output=road_dynamic_overlap_low_io_top.runner_export_done; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_export_done; child_output=road_dynamic_overlap_low_io_top.runner_export_done; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-500"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_fault; child_output=road_dynamic_overlap_low_io_top.runner_fault; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_fault; child_output=road_dynamic_overlap_low_io_top.runner_fault; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_fault; child_output=road_dynamic_overlap_low_io_top.runner_fault; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-501"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_load_ready; child_output=road_dynamic_overlap_low_io_top.runner_load_ready; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_load_ready; child_output=road_dynamic_overlap_low_io_top.runner_load_ready; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_load_ready; child_output=road_dynamic_overlap_low_io_top.runner_load_ready; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-502"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_mac_cycles; child_output=road_dynamic_overlap_low_io_top.runner_mac_cycles; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_mac_cycles; child_output=road_dynamic_overlap_low_io_top.runner_mac_cycles; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_mac_cycles; child_output=road_dynamic_overlap_low_io_top.runner_mac_cycles; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-503"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_mac_result_count; child_output=road_dynamic_overlap_low_io_top.runner_mac_result_count; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_mac_result_count; child_output=road_dynamic_overlap_low_io_top.runner_mac_result_count; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_mac_result_count; child_output=road_dynamic_overlap_low_io_top.runner_mac_result_count; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-504"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_meta_count; child_output=road_dynamic_overlap_low_io_top.runner_meta_count; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_meta_count; child_output=road_dynamic_overlap_low_io_top.runner_meta_count; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_meta_count; child_output=road_dynamic_overlap_low_io_top.runner_meta_count; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-505"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_output_data; child_output=road_dynamic_overlap_low_io_top.runner_output_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_output_data; child_output=road_dynamic_overlap_low_io_top.runner_output_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_output_data; child_output=road_dynamic_overlap_low_io_top.runner_output_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-506"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_output_index; child_output=road_dynamic_overlap_low_io_top.runner_output_index; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_output_index; child_output=road_dynamic_overlap_low_io_top.runner_output_index; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_output_index; child_output=road_dynamic_overlap_low_io_top.runner_output_index; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-507"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_output_valid; child_output=road_dynamic_overlap_low_io_top.runner_output_valid; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_output_valid; child_output=road_dynamic_overlap_low_io_top.runner_output_valid; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_output_valid; child_output=road_dynamic_overlap_low_io_top.runner_output_valid; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-508"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_post_accept_count; child_output=road_dynamic_overlap_low_io_top.runner_post_accept_count; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_post_accept_count; child_output=road_dynamic_overlap_low_io_top.runner_post_accept_count; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_post_accept_count; child_output=road_dynamic_overlap_low_io_top.runner_post_accept_count; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-509"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_post_cycles; child_output=road_dynamic_overlap_low_io_top.runner_post_cycles; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_post_cycles; child_output=road_dynamic_overlap_low_io_top.runner_post_cycles; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_post_cycles; child_output=road_dynamic_overlap_low_io_top.runner_post_cycles; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-510"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_pre_accept_count; child_output=road_dynamic_overlap_low_io_top.runner_pre_accept_count; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_pre_accept_count; child_output=road_dynamic_overlap_low_io_top.runner_pre_accept_count; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_pre_accept_count; child_output=road_dynamic_overlap_low_io_top.runner_pre_accept_count; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-511"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_pre_cycles; child_output=road_dynamic_overlap_low_io_top.runner_pre_cycles; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_pre_cycles; child_output=road_dynamic_overlap_low_io_top.runner_pre_cycles; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_pre_cycles; child_output=road_dynamic_overlap_low_io_top.runner_pre_cycles; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-512"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_preload_writes; child_output=road_dynamic_overlap_low_io_top.runner_preload_writes; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_preload_writes; child_output=road_dynamic_overlap_low_io_top.runner_preload_writes; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_preload_writes; child_output=road_dynamic_overlap_low_io_top.runner_preload_writes; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-513"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_result_queue_count; child_output=road_dynamic_overlap_low_io_top.runner_result_queue_count; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_result_queue_count; child_output=road_dynamic_overlap_low_io_top.runner_result_queue_count; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_result_queue_count; child_output=road_dynamic_overlap_low_io_top.runner_result_queue_count; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-514"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_result_reserved; child_output=road_dynamic_overlap_low_io_top.runner_result_reserved; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_result_reserved; child_output=road_dynamic_overlap_low_io_top.runner_result_reserved; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_result_reserved; child_output=road_dynamic_overlap_low_io_top.runner_result_reserved; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-515"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_scheduler_idle_cycles; child_output=road_dynamic_overlap_low_io_top.runner_scheduler_idle_cycles; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_scheduler_idle_cycles; child_output=road_dynamic_overlap_low_io_top.runner_scheduler_idle_cycles; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_scheduler_idle_cycles; child_output=road_dynamic_overlap_low_io_top.runner_scheduler_idle_cycles; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-516"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_silu_accept_count; child_output=road_dynamic_overlap_low_io_top.runner_silu_accept_count; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_silu_accept_count; child_output=road_dynamic_overlap_low_io_top.runner_silu_accept_count; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_silu_accept_count; child_output=road_dynamic_overlap_low_io_top.runner_silu_accept_count; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-517"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_silu_cycles; child_output=road_dynamic_overlap_low_io_top.runner_silu_cycles; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_silu_cycles; child_output=road_dynamic_overlap_low_io_top.runner_silu_cycles; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_silu_cycles; child_output=road_dynamic_overlap_low_io_top.runner_silu_cycles; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-518"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_storage_wait_cycles; child_output=road_dynamic_overlap_low_io_top.runner_storage_wait_cycles; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_storage_wait_cycles; child_output=road_dynamic_overlap_low_io_top.runner_storage_wait_cycles; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_storage_wait_cycles; child_output=road_dynamic_overlap_low_io_top.runner_storage_wait_cycles; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-519"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_table_fault; child_output=road_dynamic_overlap_low_io_top.runner_table_fault; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_table_fault; child_output=road_dynamic_overlap_low_io_top.runner_table_fault; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_table_fault; child_output=road_dynamic_overlap_low_io_top.runner_table_fault; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-520"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_table_loaded; child_output=road_dynamic_overlap_low_io_top.runner_table_loaded; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_table_loaded; child_output=road_dynamic_overlap_low_io_top.runner_table_loaded; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_table_loaded; child_output=road_dynamic_overlap_low_io_top.runner_table_loaded; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-521"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_table_ready; child_output=road_dynamic_overlap_low_io_top.runner_table_ready; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_table_ready; child_output=road_dynamic_overlap_low_io_top.runner_table_ready; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_table_ready; child_output=road_dynamic_overlap_low_io_top.runner_table_ready; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-522"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_writeback_count; child_output=road_dynamic_overlap_low_io_top.runner_writeback_count; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_writeback_count; child_output=road_dynamic_overlap_low_io_top.runner_writeback_count; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_writeback_count; child_output=road_dynamic_overlap_low_io_top.runner_writeback_count; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-523"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_writeback_cycles; child_output=road_dynamic_overlap_low_io_top.runner_writeback_cycles; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_writeback_cycles; child_output=road_dynamic_overlap_low_io_top.runner_writeback_cycles; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_writeback_cycles; child_output=road_dynamic_overlap_low_io_top.runner_writeback_cycles; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-524"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=state_current$D; child_output=road_dynamic_overlap_low_io_top.state_current$D; operation_count=23; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=state_current$D; child_output=road_dynamic_overlap_low_io_top.state_current$D; operation_count=23; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=state_current$D; child_output=road_dynamic_overlap_low_io_top.state_current$D; operation_count=23; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-525"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:192`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=flag_interface_open; child_output=road_dynamic_overlap_low_io_top.flag_interface_open; operation_count=1; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=flag_interface_open; child_output=road_dynamic_overlap_low_io_top.flag_interface_open; operation_count=1; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=flag_interface_open; child_output=road_dynamic_overlap_low_io_top.flag_interface_open; operation_count=1; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-526"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:193`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=flag_rx_transfer; child_output=road_dynamic_overlap_low_io_top.flag_rx_transfer; operation_count=3; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=flag_rx_transfer; child_output=road_dynamic_overlap_low_io_top.flag_rx_transfer; operation_count=3; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=flag_rx_transfer; child_output=road_dynamic_overlap_low_io_top.flag_rx_transfer; operation_count=3; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-527"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:194`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=flag_tx_transfer; child_output=road_dynamic_overlap_low_io_top.flag_tx_transfer; operation_count=3; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=flag_tx_transfer; child_output=road_dynamic_overlap_low_io_top.flag_tx_transfer; operation_count=3; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=flag_tx_transfer; child_output=road_dynamic_overlap_low_io_top.flag_tx_transfer; operation_count=3; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-528"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:195`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_table_valid; child_output=road_dynamic_overlap_low_io_top.runner_table_valid; operation_count=4; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_table_valid; child_output=road_dynamic_overlap_low_io_top.runner_table_valid; operation_count=4; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_table_valid; child_output=road_dynamic_overlap_low_io_top.runner_table_valid; operation_count=4; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-529"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:196`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=flag_table_transfer; child_output=road_dynamic_overlap_low_io_top.flag_table_transfer; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=flag_table_transfer; child_output=road_dynamic_overlap_low_io_top.flag_table_transfer; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=flag_table_transfer; child_output=road_dynamic_overlap_low_io_top.flag_table_transfer; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-530"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:197`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_load_valid; child_output=road_dynamic_overlap_low_io_top.runner_load_valid; operation_count=2; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_load_valid; child_output=road_dynamic_overlap_low_io_top.runner_load_valid; operation_count=2; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_load_valid; child_output=road_dynamic_overlap_low_io_top.runner_load_valid; operation_count=2; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-531"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:198`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=flag_load_transfer; child_output=road_dynamic_overlap_low_io_top.flag_load_transfer; operation_count=3; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=flag_load_transfer; child_output=road_dynamic_overlap_low_io_top.flag_load_transfer; operation_count=3; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=flag_load_transfer; child_output=road_dynamic_overlap_low_io_top.flag_load_transfer; operation_count=3; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-532"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:199`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_output_ready; child_output=road_dynamic_overlap_low_io_top.runner_output_ready; operation_count=4; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_output_ready; child_output=road_dynamic_overlap_low_io_top.runner_output_ready; operation_count=4; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_output_ready; child_output=road_dynamic_overlap_low_io_top.runner_output_ready; operation_count=4; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-533"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:202`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=o_rx_ready; child_output=road_dynamic_overlap_low_io_top.o_rx_ready; operation_count=2; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=o_rx_ready; child_output=road_dynamic_overlap_low_io_top.o_rx_ready; operation_count=2; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=o_rx_ready; child_output=road_dynamic_overlap_low_io_top.o_rx_ready; operation_count=2; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-534"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:203`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=o_tx_valid; child_output=road_dynamic_overlap_low_io_top.o_tx_valid; operation_count=2; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=o_tx_valid; child_output=road_dynamic_overlap_low_io_top.o_tx_valid; operation_count=2; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=o_tx_valid; child_output=road_dynamic_overlap_low_io_top.o_tx_valid; operation_count=2; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-535"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:204`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=o_tx_data; child_output=road_dynamic_overlap_low_io_top.o_tx_data; operation_count=1; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=o_tx_data; child_output=road_dynamic_overlap_low_io_top.o_tx_data; operation_count=1; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=o_tx_data; child_output=road_dynamic_overlap_low_io_top.o_tx_data; operation_count=1; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-536"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:216`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_release_done; child_output=road_dynamic_overlap_low_io_top.reg_release_done; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_release_done; child_output=road_dynamic_overlap_low_io_top.reg_release_done; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_release_done; child_output=road_dynamic_overlap_low_io_top.reg_release_done; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-537"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:234`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=state_next; child_output=road_dynamic_overlap_low_io_top.state_next; operation_count=23; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=state_next; child_output=road_dynamic_overlap_low_io_top.state_next; operation_count=23; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=state_next; child_output=road_dynamic_overlap_low_io_top.state_next; operation_count=23; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-538"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:351`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=rx_ready_o; child_output=road_dynamic_overlap_low_io_top.rx_ready_o; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=rx_ready_o; child_output=road_dynamic_overlap_low_io_top.rx_ready_o; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=rx_ready_o; child_output=road_dynamic_overlap_low_io_top.rx_ready_o; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-539"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:352`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=tx_valid_o; child_output=road_dynamic_overlap_low_io_top.tx_valid_o; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=tx_valid_o; child_output=road_dynamic_overlap_low_io_top.tx_valid_o; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=tx_valid_o; child_output=road_dynamic_overlap_low_io_top.tx_valid_o; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-540"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:353`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=tx_data_o; child_output=road_dynamic_overlap_low_io_top.tx_data_o; operation_count=1; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=tx_data_o; child_output=road_dynamic_overlap_low_io_top.tx_data_o; operation_count=1; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=tx_data_o; child_output=road_dynamic_overlap_low_io_top.tx_data_o; operation_count=1; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-541"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:390`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_start; child_output=road_dynamic_overlap_low_io_top.reg_start; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_start; child_output=road_dynamic_overlap_low_io_top.reg_start; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_start; child_output=road_dynamic_overlap_low_io_top.reg_start; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-542"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:390`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_table_addr; child_output=road_dynamic_overlap_low_io_top.reg_table_addr; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_table_addr; child_output=road_dynamic_overlap_low_io_top.reg_table_addr; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_table_addr; child_output=road_dynamic_overlap_low_io_top.reg_table_addr; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-543"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:391`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_export_start; child_output=road_dynamic_overlap_low_io_top.reg_export_start; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_export_start; child_output=road_dynamic_overlap_low_io_top.reg_export_start; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_export_start; child_output=road_dynamic_overlap_low_io_top.reg_export_start; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-544"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:391`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_load_kind; child_output=road_dynamic_overlap_low_io_top.reg_load_kind; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_load_kind; child_output=road_dynamic_overlap_low_io_top.reg_load_kind; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_load_kind; child_output=road_dynamic_overlap_low_io_top.reg_load_kind; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-545"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:392`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_commit_ready; child_output=road_dynamic_overlap_low_io_top.reg_commit_ready; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_commit_ready; child_output=road_dynamic_overlap_low_io_top.reg_commit_ready; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_commit_ready; child_output=road_dynamic_overlap_low_io_top.reg_commit_ready; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-546"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:392`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_load_addr; child_output=road_dynamic_overlap_low_io_top.reg_load_addr; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_load_addr; child_output=road_dynamic_overlap_low_io_top.reg_load_addr; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_load_addr; child_output=road_dynamic_overlap_low_io_top.reg_load_addr; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-547"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:393`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_pw_only; child_output=road_dynamic_overlap_low_io_top.reg_pw_only; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_pw_only; child_output=road_dynamic_overlap_low_io_top.reg_pw_only; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_pw_only; child_output=road_dynamic_overlap_low_io_top.reg_pw_only; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-548"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:394`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_load_data; child_output=road_dynamic_overlap_low_io_top.reg_load_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_load_data; child_output=road_dynamic_overlap_low_io_top.reg_load_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_load_data; child_output=road_dynamic_overlap_low_io_top.reg_load_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-549"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=cnt_status_index$enable; child_output=road_dynamic_overlap_low_io_top.cnt_status_index$enable; operation_count=11; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=cnt_status_index$enable; child_output=road_dynamic_overlap_low_io_top.cnt_status_index$enable; operation_count=11; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=cnt_status_index$enable; child_output=road_dynamic_overlap_low_io_top.cnt_status_index$enable; operation_count=11; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-550"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_commit_ready$enable; child_output=road_dynamic_overlap_low_io_top.reg_commit_ready$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_commit_ready$enable; child_output=road_dynamic_overlap_low_io_top.reg_commit_ready$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_commit_ready$enable; child_output=road_dynamic_overlap_low_io_top.reg_commit_ready$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-551"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_export_done_seen$enable; child_output=road_dynamic_overlap_low_io_top.reg_export_done_seen$enable; operation_count=13; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_export_done_seen$enable; child_output=road_dynamic_overlap_low_io_top.reg_export_done_seen$enable; operation_count=13; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_export_done_seen$enable; child_output=road_dynamic_overlap_low_io_top.reg_export_done_seen$enable; operation_count=13; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-552"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_export_start$enable; child_output=road_dynamic_overlap_low_io_top.reg_export_start$enable; operation_count=9; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_export_start$enable; child_output=road_dynamic_overlap_low_io_top.reg_export_start$enable; operation_count=9; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_export_start$enable; child_output=road_dynamic_overlap_low_io_top.reg_export_start$enable; operation_count=9; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-553"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_load_addr$enable; child_output=road_dynamic_overlap_low_io_top.reg_load_addr$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_load_addr$enable; child_output=road_dynamic_overlap_low_io_top.reg_load_addr$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_load_addr$enable; child_output=road_dynamic_overlap_low_io_top.reg_load_addr$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-554"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_load_data$enable; child_output=road_dynamic_overlap_low_io_top.reg_load_data$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_load_data$enable; child_output=road_dynamic_overlap_low_io_top.reg_load_data$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_load_data$enable; child_output=road_dynamic_overlap_low_io_top.reg_load_data$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-555"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_load_kind$enable; child_output=road_dynamic_overlap_low_io_top.reg_load_kind$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_load_kind$enable; child_output=road_dynamic_overlap_low_io_top.reg_load_kind$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_load_kind$enable; child_output=road_dynamic_overlap_low_io_top.reg_load_kind$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-556"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_load_low$enable; child_output=road_dynamic_overlap_low_io_top.reg_load_low$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_load_low$enable; child_output=road_dynamic_overlap_low_io_top.reg_load_low$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_load_low$enable; child_output=road_dynamic_overlap_low_io_top.reg_load_low$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-557"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_load_pending$enable; child_output=road_dynamic_overlap_low_io_top.reg_load_pending$enable; operation_count=8; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_load_pending$enable; child_output=road_dynamic_overlap_low_io_top.reg_load_pending$enable; operation_count=8; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_load_pending$enable; child_output=road_dynamic_overlap_low_io_top.reg_load_pending$enable; operation_count=8; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-558"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_pw_only$enable; child_output=road_dynamic_overlap_low_io_top.reg_pw_only$enable; operation_count=7; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_pw_only$enable; child_output=road_dynamic_overlap_low_io_top.reg_pw_only$enable; operation_count=7; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_pw_only$enable; child_output=road_dynamic_overlap_low_io_top.reg_pw_only$enable; operation_count=7; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-559"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_runner_done_seen$enable; child_output=road_dynamic_overlap_low_io_top.reg_runner_done_seen$enable; operation_count=7; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_runner_done_seen$enable; child_output=road_dynamic_overlap_low_io_top.reg_runner_done_seen$enable; operation_count=7; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_runner_done_seen$enable; child_output=road_dynamic_overlap_low_io_top.reg_runner_done_seen$enable; operation_count=7; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-560"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_shell_fault$enable; child_output=road_dynamic_overlap_low_io_top.reg_shell_fault$enable; operation_count=15; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_shell_fault$enable; child_output=road_dynamic_overlap_low_io_top.reg_shell_fault$enable; operation_count=15; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_shell_fault$enable; child_output=road_dynamic_overlap_low_io_top.reg_shell_fault$enable; operation_count=15; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-561"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_core$D; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_core$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_core$D; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_core$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_core$D; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_core$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-562"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_core$enable; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_core$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_core$enable; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_core$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_core$enable; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_core$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-563"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_export_cycles$D; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_export_cycles$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_export_cycles$D; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_export_cycles$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_export_cycles$D; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_export_cycles$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-564"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_export_cycles$enable; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_export_cycles$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_export_cycles$enable; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_export_cycles$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_export_cycles$enable; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_export_cycles$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-565"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_flags$D; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_flags$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_flags$D; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_flags$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_flags$D; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_flags$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-566"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_flags$enable; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_flags$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_flags$enable; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_flags$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_flags$enable; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_flags$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-567"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_mac_cycles$D; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_mac_cycles$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_mac_cycles$D; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_mac_cycles$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_mac_cycles$D; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_mac_cycles$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-568"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_mac_cycles$enable; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_mac_cycles$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_mac_cycles$enable; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_mac_cycles$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_mac_cycles$enable; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_mac_cycles$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-569"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_mac_results$D; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_mac_results$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_mac_results$D; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_mac_results$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_mac_results$D; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_mac_results$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-570"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_mac_results$enable; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_mac_results$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_mac_results$enable; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_mac_results$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_mac_results$enable; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_mac_results$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-571"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_post_accepts$D; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_post_accepts$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_post_accepts$D; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_post_accepts$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_post_accepts$D; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_post_accepts$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-572"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_post_accepts$enable; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_post_accepts$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_post_accepts$enable; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_post_accepts$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_post_accepts$enable; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_post_accepts$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-573"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_post_cycles$D; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_post_cycles$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_post_cycles$D; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_post_cycles$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_post_cycles$D; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_post_cycles$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-574"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_post_cycles$enable; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_post_cycles$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_post_cycles$enable; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_post_cycles$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_post_cycles$enable; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_post_cycles$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-575"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_pre_accepts$D; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_pre_accepts$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_pre_accepts$D; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_pre_accepts$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_pre_accepts$D; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_pre_accepts$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-576"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_pre_accepts$enable; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_pre_accepts$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_pre_accepts$enable; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_pre_accepts$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_pre_accepts$enable; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_pre_accepts$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-577"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_pre_cycles$D; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_pre_cycles$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_pre_cycles$D; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_pre_cycles$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_pre_cycles$D; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_pre_cycles$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-578"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_pre_cycles$enable; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_pre_cycles$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_pre_cycles$enable; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_pre_cycles$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_pre_cycles$enable; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_pre_cycles$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-579"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_preload$D; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_preload$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_preload$D; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_preload$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_preload$D; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_preload$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-580"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_preload$enable; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_preload$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_preload$enable; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_preload$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_preload$enable; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_preload$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-581"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_scheduler_idle$D; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_scheduler_idle$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_scheduler_idle$D; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_scheduler_idle$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_scheduler_idle$D; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_scheduler_idle$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-582"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_scheduler_idle$enable; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_scheduler_idle$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_scheduler_idle$enable; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_scheduler_idle$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_scheduler_idle$enable; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_scheduler_idle$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-583"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_silu_accepts$D; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_silu_accepts$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_silu_accepts$D; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_silu_accepts$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_silu_accepts$D; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_silu_accepts$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-584"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_silu_accepts$enable; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_silu_accepts$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_silu_accepts$enable; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_silu_accepts$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_silu_accepts$enable; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_silu_accepts$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-585"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_silu_cycles$D; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_silu_cycles$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_silu_cycles$D; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_silu_cycles$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_silu_cycles$D; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_silu_cycles$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-586"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_silu_cycles$enable; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_silu_cycles$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_silu_cycles$enable; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_silu_cycles$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_silu_cycles$enable; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_silu_cycles$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-587"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_storage_wait$D; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_storage_wait$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_storage_wait$D; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_storage_wait$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_storage_wait$D; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_storage_wait$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-588"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_storage_wait$enable; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_storage_wait$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_storage_wait$enable; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_storage_wait$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_storage_wait$enable; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_storage_wait$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-589"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_writeback_cycles$D; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_writeback_cycles$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_writeback_cycles$D; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_writeback_cycles$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_writeback_cycles$D; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_writeback_cycles$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-590"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_writeback_cycles$enable; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_writeback_cycles$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_writeback_cycles$enable; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_writeback_cycles$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_writeback_cycles$enable; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_writeback_cycles$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-591"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_writebacks$D; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_writebacks$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_writebacks$D; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_writebacks$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_writebacks$D; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_writebacks$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-592"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_writebacks$enable; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_writebacks$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_writebacks$enable; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_writebacks$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_snapshot_writebacks$enable; child_output=road_dynamic_overlap_low_io_top.reg_snapshot_writebacks$enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-593"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_start$enable; child_output=road_dynamic_overlap_low_io_top.reg_start$enable; operation_count=7; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_start$enable; child_output=road_dynamic_overlap_low_io_top.reg_start$enable; operation_count=7; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_start$enable; child_output=road_dynamic_overlap_low_io_top.reg_start$enable; operation_count=7; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-594"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_table_addr$D; child_output=road_dynamic_overlap_low_io_top.reg_table_addr$D; operation_count=1; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_table_addr$D; child_output=road_dynamic_overlap_low_io_top.reg_table_addr$D; operation_count=1; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_table_addr$D; child_output=road_dynamic_overlap_low_io_top.reg_table_addr$D; operation_count=1; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-595"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_table_addr$enable; child_output=road_dynamic_overlap_low_io_top.reg_table_addr$enable; operation_count=11; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_table_addr$enable; child_output=road_dynamic_overlap_low_io_top.reg_table_addr$enable; operation_count=11; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_table_addr$enable; child_output=road_dynamic_overlap_low_io_top.reg_table_addr$enable; operation_count=11; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-596"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_busy; child_output=road_dynamic_overlap_low_io_top.runner_busy; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_busy; child_output=road_dynamic_overlap_low_io_top.runner_busy; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_busy; child_output=road_dynamic_overlap_low_io_top.runner_busy; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-597"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_core_cycles; child_output=road_dynamic_overlap_low_io_top.runner_core_cycles; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_core_cycles; child_output=road_dynamic_overlap_low_io_top.runner_core_cycles; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_core_cycles; child_output=road_dynamic_overlap_low_io_top.runner_core_cycles; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-598"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_debug_channel; child_output=road_dynamic_overlap_low_io_top.runner_debug_channel; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_debug_channel; child_output=road_dynamic_overlap_low_io_top.runner_debug_channel; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_debug_channel; child_output=road_dynamic_overlap_low_io_top.runner_debug_channel; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-599"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_debug_layer; child_output=road_dynamic_overlap_low_io_top.runner_debug_layer; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_debug_layer; child_output=road_dynamic_overlap_low_io_top.runner_debug_layer; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_debug_layer; child_output=road_dynamic_overlap_low_io_top.runner_debug_layer; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-600"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_debug_phase; child_output=road_dynamic_overlap_low_io_top.runner_debug_phase; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_debug_phase; child_output=road_dynamic_overlap_low_io_top.runner_debug_phase; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_debug_phase; child_output=road_dynamic_overlap_low_io_top.runner_debug_phase; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-601"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_debug_position; child_output=road_dynamic_overlap_low_io_top.runner_debug_position; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_debug_position; child_output=road_dynamic_overlap_low_io_top.runner_debug_position; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_debug_position; child_output=road_dynamic_overlap_low_io_top.runner_debug_position; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-602"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_debug_valid; child_output=road_dynamic_overlap_low_io_top.runner_debug_valid; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_debug_valid; child_output=road_dynamic_overlap_low_io_top.runner_debug_valid; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_debug_valid; child_output=road_dynamic_overlap_low_io_top.runner_debug_valid; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-603"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_debug_value; child_output=road_dynamic_overlap_low_io_top.runner_debug_value; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_debug_value; child_output=road_dynamic_overlap_low_io_top.runner_debug_value; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_debug_value; child_output=road_dynamic_overlap_low_io_top.runner_debug_value; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-604"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_done; child_output=road_dynamic_overlap_low_io_top.runner_done; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_done; child_output=road_dynamic_overlap_low_io_top.runner_done; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_done; child_output=road_dynamic_overlap_low_io_top.runner_done; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-605"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_export_cycles; child_output=road_dynamic_overlap_low_io_top.runner_export_cycles; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_export_cycles; child_output=road_dynamic_overlap_low_io_top.runner_export_cycles; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_export_cycles; child_output=road_dynamic_overlap_low_io_top.runner_export_cycles; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-606"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_export_done; child_output=road_dynamic_overlap_low_io_top.runner_export_done; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_export_done; child_output=road_dynamic_overlap_low_io_top.runner_export_done; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_export_done; child_output=road_dynamic_overlap_low_io_top.runner_export_done; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-607"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_fault; child_output=road_dynamic_overlap_low_io_top.runner_fault; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_fault; child_output=road_dynamic_overlap_low_io_top.runner_fault; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_fault; child_output=road_dynamic_overlap_low_io_top.runner_fault; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-608"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_load_ready; child_output=road_dynamic_overlap_low_io_top.runner_load_ready; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_load_ready; child_output=road_dynamic_overlap_low_io_top.runner_load_ready; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_load_ready; child_output=road_dynamic_overlap_low_io_top.runner_load_ready; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-609"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_mac_cycles; child_output=road_dynamic_overlap_low_io_top.runner_mac_cycles; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_mac_cycles; child_output=road_dynamic_overlap_low_io_top.runner_mac_cycles; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_mac_cycles; child_output=road_dynamic_overlap_low_io_top.runner_mac_cycles; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-610"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_mac_result_count; child_output=road_dynamic_overlap_low_io_top.runner_mac_result_count; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_mac_result_count; child_output=road_dynamic_overlap_low_io_top.runner_mac_result_count; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_mac_result_count; child_output=road_dynamic_overlap_low_io_top.runner_mac_result_count; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-611"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_meta_count; child_output=road_dynamic_overlap_low_io_top.runner_meta_count; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_meta_count; child_output=road_dynamic_overlap_low_io_top.runner_meta_count; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_meta_count; child_output=road_dynamic_overlap_low_io_top.runner_meta_count; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-612"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_output_data; child_output=road_dynamic_overlap_low_io_top.runner_output_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_output_data; child_output=road_dynamic_overlap_low_io_top.runner_output_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_output_data; child_output=road_dynamic_overlap_low_io_top.runner_output_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-613"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_output_index; child_output=road_dynamic_overlap_low_io_top.runner_output_index; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_output_index; child_output=road_dynamic_overlap_low_io_top.runner_output_index; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_output_index; child_output=road_dynamic_overlap_low_io_top.runner_output_index; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-614"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_output_valid; child_output=road_dynamic_overlap_low_io_top.runner_output_valid; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_output_valid; child_output=road_dynamic_overlap_low_io_top.runner_output_valid; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_output_valid; child_output=road_dynamic_overlap_low_io_top.runner_output_valid; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-615"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_post_accept_count; child_output=road_dynamic_overlap_low_io_top.runner_post_accept_count; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_post_accept_count; child_output=road_dynamic_overlap_low_io_top.runner_post_accept_count; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_post_accept_count; child_output=road_dynamic_overlap_low_io_top.runner_post_accept_count; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-616"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_post_cycles; child_output=road_dynamic_overlap_low_io_top.runner_post_cycles; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_post_cycles; child_output=road_dynamic_overlap_low_io_top.runner_post_cycles; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_post_cycles; child_output=road_dynamic_overlap_low_io_top.runner_post_cycles; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-617"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_pre_accept_count; child_output=road_dynamic_overlap_low_io_top.runner_pre_accept_count; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_pre_accept_count; child_output=road_dynamic_overlap_low_io_top.runner_pre_accept_count; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_pre_accept_count; child_output=road_dynamic_overlap_low_io_top.runner_pre_accept_count; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-618"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_pre_cycles; child_output=road_dynamic_overlap_low_io_top.runner_pre_cycles; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_pre_cycles; child_output=road_dynamic_overlap_low_io_top.runner_pre_cycles; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_pre_cycles; child_output=road_dynamic_overlap_low_io_top.runner_pre_cycles; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-619"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_preload_writes; child_output=road_dynamic_overlap_low_io_top.runner_preload_writes; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_preload_writes; child_output=road_dynamic_overlap_low_io_top.runner_preload_writes; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_preload_writes; child_output=road_dynamic_overlap_low_io_top.runner_preload_writes; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-620"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_result_queue_count; child_output=road_dynamic_overlap_low_io_top.runner_result_queue_count; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_result_queue_count; child_output=road_dynamic_overlap_low_io_top.runner_result_queue_count; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_result_queue_count; child_output=road_dynamic_overlap_low_io_top.runner_result_queue_count; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-621"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_result_reserved; child_output=road_dynamic_overlap_low_io_top.runner_result_reserved; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_result_reserved; child_output=road_dynamic_overlap_low_io_top.runner_result_reserved; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_result_reserved; child_output=road_dynamic_overlap_low_io_top.runner_result_reserved; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-622"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_scheduler_idle_cycles; child_output=road_dynamic_overlap_low_io_top.runner_scheduler_idle_cycles; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_scheduler_idle_cycles; child_output=road_dynamic_overlap_low_io_top.runner_scheduler_idle_cycles; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_scheduler_idle_cycles; child_output=road_dynamic_overlap_low_io_top.runner_scheduler_idle_cycles; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-623"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_silu_accept_count; child_output=road_dynamic_overlap_low_io_top.runner_silu_accept_count; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_silu_accept_count; child_output=road_dynamic_overlap_low_io_top.runner_silu_accept_count; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_silu_accept_count; child_output=road_dynamic_overlap_low_io_top.runner_silu_accept_count; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-624"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_silu_cycles; child_output=road_dynamic_overlap_low_io_top.runner_silu_cycles; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_silu_cycles; child_output=road_dynamic_overlap_low_io_top.runner_silu_cycles; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_silu_cycles; child_output=road_dynamic_overlap_low_io_top.runner_silu_cycles; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-625"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_storage_wait_cycles; child_output=road_dynamic_overlap_low_io_top.runner_storage_wait_cycles; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_storage_wait_cycles; child_output=road_dynamic_overlap_low_io_top.runner_storage_wait_cycles; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_storage_wait_cycles; child_output=road_dynamic_overlap_low_io_top.runner_storage_wait_cycles; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-626"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_table_fault; child_output=road_dynamic_overlap_low_io_top.runner_table_fault; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_table_fault; child_output=road_dynamic_overlap_low_io_top.runner_table_fault; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_table_fault; child_output=road_dynamic_overlap_low_io_top.runner_table_fault; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-627"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_table_loaded; child_output=road_dynamic_overlap_low_io_top.runner_table_loaded; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_table_loaded; child_output=road_dynamic_overlap_low_io_top.runner_table_loaded; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_table_loaded; child_output=road_dynamic_overlap_low_io_top.runner_table_loaded; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-628"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_table_ready; child_output=road_dynamic_overlap_low_io_top.runner_table_ready; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_table_ready; child_output=road_dynamic_overlap_low_io_top.runner_table_ready; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_table_ready; child_output=road_dynamic_overlap_low_io_top.runner_table_ready; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-629"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_writeback_count; child_output=road_dynamic_overlap_low_io_top.runner_writeback_count; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_writeback_count; child_output=road_dynamic_overlap_low_io_top.runner_writeback_count; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_writeback_count; child_output=road_dynamic_overlap_low_io_top.runner_writeback_count; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-630"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_writeback_cycles; child_output=road_dynamic_overlap_low_io_top.runner_writeback_cycles; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_writeback_cycles; child_output=road_dynamic_overlap_low_io_top.runner_writeback_cycles; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_writeback_cycles; child_output=road_dynamic_overlap_low_io_top.runner_writeback_cycles; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-631"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=state_current$D; child_output=road_dynamic_overlap_low_io_top.state_current$D; operation_count=23; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=state_current$D; child_output=road_dynamic_overlap_low_io_top.state_current$D; operation_count=23; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=state_current$D; child_output=road_dynamic_overlap_low_io_top.state_current$D; operation_count=23; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-632"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:192`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=flag_interface_open; child_output=road_dynamic_overlap_low_io_top.flag_interface_open; operation_count=1; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=flag_interface_open; child_output=road_dynamic_overlap_low_io_top.flag_interface_open; operation_count=1; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=flag_interface_open; child_output=road_dynamic_overlap_low_io_top.flag_interface_open; operation_count=1; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-633"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:193`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=flag_rx_transfer; child_output=road_dynamic_overlap_low_io_top.flag_rx_transfer; operation_count=3; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=flag_rx_transfer; child_output=road_dynamic_overlap_low_io_top.flag_rx_transfer; operation_count=3; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=flag_rx_transfer; child_output=road_dynamic_overlap_low_io_top.flag_rx_transfer; operation_count=3; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-634"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:194`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=flag_tx_transfer; child_output=road_dynamic_overlap_low_io_top.flag_tx_transfer; operation_count=3; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=flag_tx_transfer; child_output=road_dynamic_overlap_low_io_top.flag_tx_transfer; operation_count=3; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=flag_tx_transfer; child_output=road_dynamic_overlap_low_io_top.flag_tx_transfer; operation_count=3; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-635"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:195`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_table_valid; child_output=road_dynamic_overlap_low_io_top.runner_table_valid; operation_count=4; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_table_valid; child_output=road_dynamic_overlap_low_io_top.runner_table_valid; operation_count=4; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_table_valid; child_output=road_dynamic_overlap_low_io_top.runner_table_valid; operation_count=4; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-636"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:196`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=flag_table_transfer; child_output=road_dynamic_overlap_low_io_top.flag_table_transfer; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=flag_table_transfer; child_output=road_dynamic_overlap_low_io_top.flag_table_transfer; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=flag_table_transfer; child_output=road_dynamic_overlap_low_io_top.flag_table_transfer; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-637"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:197`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_load_valid; child_output=road_dynamic_overlap_low_io_top.runner_load_valid; operation_count=2; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_load_valid; child_output=road_dynamic_overlap_low_io_top.runner_load_valid; operation_count=2; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_load_valid; child_output=road_dynamic_overlap_low_io_top.runner_load_valid; operation_count=2; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-638"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:198`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=flag_load_transfer; child_output=road_dynamic_overlap_low_io_top.flag_load_transfer; operation_count=3; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=flag_load_transfer; child_output=road_dynamic_overlap_low_io_top.flag_load_transfer; operation_count=3; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=flag_load_transfer; child_output=road_dynamic_overlap_low_io_top.flag_load_transfer; operation_count=3; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-639"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:199`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_output_ready; child_output=road_dynamic_overlap_low_io_top.runner_output_ready; operation_count=4; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_output_ready; child_output=road_dynamic_overlap_low_io_top.runner_output_ready; operation_count=4; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=runner_output_ready; child_output=road_dynamic_overlap_low_io_top.runner_output_ready; operation_count=4; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-640"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:202`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=o_rx_ready; child_output=road_dynamic_overlap_low_io_top.o_rx_ready; operation_count=2; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=o_rx_ready; child_output=road_dynamic_overlap_low_io_top.o_rx_ready; operation_count=2; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=o_rx_ready; child_output=road_dynamic_overlap_low_io_top.o_rx_ready; operation_count=2; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-641"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:203`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=o_tx_valid; child_output=road_dynamic_overlap_low_io_top.o_tx_valid; operation_count=2; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=o_tx_valid; child_output=road_dynamic_overlap_low_io_top.o_tx_valid; operation_count=2; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=o_tx_valid; child_output=road_dynamic_overlap_low_io_top.o_tx_valid; operation_count=2; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-642"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:204`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=o_tx_data; child_output=road_dynamic_overlap_low_io_top.o_tx_data; operation_count=1; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=o_tx_data; child_output=road_dynamic_overlap_low_io_top.o_tx_data; operation_count=1; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=o_tx_data; child_output=road_dynamic_overlap_low_io_top.o_tx_data; operation_count=1; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-643"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:216`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_release_done; child_output=road_dynamic_overlap_low_io_top.reg_release_done; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_release_done; child_output=road_dynamic_overlap_low_io_top.reg_release_done; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_release_done; child_output=road_dynamic_overlap_low_io_top.reg_release_done; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-644"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:234`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=state_next; child_output=road_dynamic_overlap_low_io_top.state_next; operation_count=23; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=state_next; child_output=road_dynamic_overlap_low_io_top.state_next; operation_count=23; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=state_next; child_output=road_dynamic_overlap_low_io_top.state_next; operation_count=23; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-645"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:351`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=rx_ready_o; child_output=road_dynamic_overlap_low_io_top.rx_ready_o; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=rx_ready_o; child_output=road_dynamic_overlap_low_io_top.rx_ready_o; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=rx_ready_o; child_output=road_dynamic_overlap_low_io_top.rx_ready_o; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-646"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:352`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=tx_valid_o; child_output=road_dynamic_overlap_low_io_top.tx_valid_o; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=tx_valid_o; child_output=road_dynamic_overlap_low_io_top.tx_valid_o; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=tx_valid_o; child_output=road_dynamic_overlap_low_io_top.tx_valid_o; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-647"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:353`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=tx_data_o; child_output=road_dynamic_overlap_low_io_top.tx_data_o; operation_count=1; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=tx_data_o; child_output=road_dynamic_overlap_low_io_top.tx_data_o; operation_count=1; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=tx_data_o; child_output=road_dynamic_overlap_low_io_top.tx_data_o; operation_count=1; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-648"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:390`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_start; child_output=road_dynamic_overlap_low_io_top.reg_start; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_start; child_output=road_dynamic_overlap_low_io_top.reg_start; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_start; child_output=road_dynamic_overlap_low_io_top.reg_start; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-649"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:390`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_table_addr; child_output=road_dynamic_overlap_low_io_top.reg_table_addr; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_table_addr; child_output=road_dynamic_overlap_low_io_top.reg_table_addr; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_table_addr; child_output=road_dynamic_overlap_low_io_top.reg_table_addr; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-650"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:391`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_export_start; child_output=road_dynamic_overlap_low_io_top.reg_export_start; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_export_start; child_output=road_dynamic_overlap_low_io_top.reg_export_start; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_export_start; child_output=road_dynamic_overlap_low_io_top.reg_export_start; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-651"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:391`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_load_kind; child_output=road_dynamic_overlap_low_io_top.reg_load_kind; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_load_kind; child_output=road_dynamic_overlap_low_io_top.reg_load_kind; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_load_kind; child_output=road_dynamic_overlap_low_io_top.reg_load_kind; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-652"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:392`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_commit_ready; child_output=road_dynamic_overlap_low_io_top.reg_commit_ready; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_commit_ready; child_output=road_dynamic_overlap_low_io_top.reg_commit_ready; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_commit_ready; child_output=road_dynamic_overlap_low_io_top.reg_commit_ready; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-653"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:392`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_load_addr; child_output=road_dynamic_overlap_low_io_top.reg_load_addr; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_load_addr; child_output=road_dynamic_overlap_low_io_top.reg_load_addr; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_load_addr; child_output=road_dynamic_overlap_low_io_top.reg_load_addr; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-654"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:393`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_pw_only; child_output=road_dynamic_overlap_low_io_top.reg_pw_only; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_pw_only; child_output=road_dynamic_overlap_low_io_top.reg_pw_only; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_pw_only; child_output=road_dynamic_overlap_low_io_top.reg_pw_only; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-655"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:394`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_load_data; child_output=road_dynamic_overlap_low_io_top.reg_load_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_load_data; child_output=road_dynamic_overlap_low_io_top.reg_load_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_overlap_low_io_top.v:road_dynamic_overlap_low_io_top@49:1-569:1; instance_path=road_dynamic_overlap_low_io_top; specialization=e6ca50fd9a42a79f72afb41048bee008c4006e17674195b6c6ae478eca1eee3c; target=reg_load_data; child_output=road_dynamic_overlap_low_io_top.reg_load_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-656"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:137`
- Evidence:
- node_kind: `verilog_rtl`
- detail: runner_table_ready
- source_excerpt: `runner_table_ready`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
runner_table_ready
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-657"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:138`
- Evidence:
- node_kind: `verilog_rtl`
- detail: runner_table_loaded
- source_excerpt: `runner_table_loaded`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
runner_table_loaded
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-658"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:139`
- Evidence:
- node_kind: `verilog_rtl`
- detail: runner_table_fault
- source_excerpt: `runner_table_fault`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
runner_table_fault
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-659"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:140`
- Evidence:
- node_kind: `verilog_rtl`
- detail: runner_load_ready
- source_excerpt: `runner_load_ready`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
runner_load_ready
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-660"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:141`
- Evidence:
- node_kind: `verilog_rtl`
- detail: runner_busy
- source_excerpt: `runner_busy`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
runner_busy
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-661"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:142`
- Evidence:
- node_kind: `verilog_rtl`
- detail: runner_done
- source_excerpt: `runner_done`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
runner_done
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-662"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:143`
- Evidence:
- node_kind: `verilog_rtl`
- detail: runner_fault
- source_excerpt: `runner_fault`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
runner_fault
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-663"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:144`
- Evidence:
- node_kind: `verilog_rtl`
- detail: runner_output_valid
- source_excerpt: `runner_output_valid`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
runner_output_valid
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-664"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:145`
- Evidence:
- node_kind: `verilog_rtl`
- detail: runner_output_data
- source_excerpt: `runner_output_data`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
runner_output_data
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-665"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:146`
- Evidence:
- node_kind: `verilog_rtl`
- detail: runner_output_index
- source_excerpt: `runner_output_index`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
runner_output_index
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-666"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:147`
- Evidence:
- node_kind: `verilog_rtl`
- detail: runner_export_done
- source_excerpt: `runner_export_done`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
runner_export_done
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-667"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:150`
- Evidence:
- node_kind: `verilog_rtl`
- detail: runner_debug_valid
- source_excerpt: `runner_debug_valid`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
runner_debug_valid
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-668"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:151`
- Evidence:
- node_kind: `verilog_rtl`
- detail: runner_debug_phase
- source_excerpt: `runner_debug_phase`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
runner_debug_phase
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-669"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:152`
- Evidence:
- node_kind: `verilog_rtl`
- detail: runner_debug_layer
- source_excerpt: `runner_debug_layer`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
runner_debug_layer
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-670"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:153`
- Evidence:
- node_kind: `verilog_rtl`
- detail: runner_debug_position
- source_excerpt: `runner_debug_position`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
runner_debug_position
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-671"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:154`
- Evidence:
- node_kind: `verilog_rtl`
- detail: runner_debug_channel
- source_excerpt: `runner_debug_channel`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
runner_debug_channel
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-672"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:155`
- Evidence:
- node_kind: `verilog_rtl`
- detail: runner_debug_value
- source_excerpt: `runner_debug_value`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
runner_debug_value
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-673"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:156`
- Evidence:
- node_kind: `verilog_rtl`
- detail: runner_preload_writes
- source_excerpt: `runner_preload_writes`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
runner_preload_writes
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-674"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:157`
- Evidence:
- node_kind: `verilog_rtl`
- detail: runner_core_cycles
- source_excerpt: `runner_core_cycles`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
runner_core_cycles
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-675"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:158`
- Evidence:
- node_kind: `verilog_rtl`
- detail: runner_mac_cycles
- source_excerpt: `runner_mac_cycles`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
runner_mac_cycles
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-676"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:159`
- Evidence:
- node_kind: `verilog_rtl`
- detail: runner_pre_cycles
- source_excerpt: `runner_pre_cycles`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
runner_pre_cycles
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-677"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:160`
- Evidence:
- node_kind: `verilog_rtl`
- detail: runner_silu_cycles
- source_excerpt: `runner_silu_cycles`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
runner_silu_cycles
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-678"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:161`
- Evidence:
- node_kind: `verilog_rtl`
- detail: runner_post_cycles
- source_excerpt: `runner_post_cycles`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
runner_post_cycles
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-679"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:162`
- Evidence:
- node_kind: `verilog_rtl`
- detail: runner_writeback_cycles
- source_excerpt: `runner_writeback_cycles`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
runner_writeback_cycles
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-680"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:163`
- Evidence:
- node_kind: `verilog_rtl`
- detail: runner_storage_wait_cycles
- source_excerpt: `runner_storage_wait_cycles`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
runner_storage_wait_cycles
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-681"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:164`
- Evidence:
- node_kind: `verilog_rtl`
- detail: runner_scheduler_idle_cycles
- source_excerpt: `runner_scheduler_idle_cycles`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
runner_scheduler_idle_cycles
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-682"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:165`
- Evidence:
- node_kind: `verilog_rtl`
- detail: runner_export_cycles
- source_excerpt: `runner_export_cycles`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
runner_export_cycles
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-683"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:166`
- Evidence:
- node_kind: `verilog_rtl`
- detail: runner_result_queue_count
- source_excerpt: `runner_result_queue_count`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
runner_result_queue_count
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-684"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:167`
- Evidence:
- node_kind: `verilog_rtl`
- detail: runner_result_reserved
- source_excerpt: `runner_result_reserved`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
runner_result_reserved
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-685"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:168`
- Evidence:
- node_kind: `verilog_rtl`
- detail: runner_meta_count
- source_excerpt: `runner_meta_count`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
runner_meta_count
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-686"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:169`
- Evidence:
- node_kind: `verilog_rtl`
- detail: runner_mac_result_count
- source_excerpt: `runner_mac_result_count`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
runner_mac_result_count
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-687"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:170`
- Evidence:
- node_kind: `verilog_rtl`
- detail: runner_pre_accept_count
- source_excerpt: `runner_pre_accept_count`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
runner_pre_accept_count
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-688"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:171`
- Evidence:
- node_kind: `verilog_rtl`
- detail: runner_silu_accept_count
- source_excerpt: `runner_silu_accept_count`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
runner_silu_accept_count
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-689"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:172`
- Evidence:
- node_kind: `verilog_rtl`
- detail: runner_post_accept_count
- source_excerpt: `runner_post_accept_count`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
runner_post_accept_count
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-690"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:173`
- Evidence:
- node_kind: `verilog_rtl`
- detail: runner_writeback_count
- source_excerpt: `runner_writeback_count`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
runner_writeback_count
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-691"></a>
### VG157: 普通 RTL 注释不得携带版本字样；版本历史只能位于 formatter 固定文件头范围。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:19`
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

<a id="vg-finding-692"></a>
### VG157: 普通 RTL 注释不得携带版本字样；版本历史只能位于 formatter 固定文件头范围。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_overlap_low_io_top.v:42`
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
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_overlap_low_io_top.v:69` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_overlap_low_io_top.v:70` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_overlap_low_io_top.v:71` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_overlap_low_io_top.v:72` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_overlap_low_io_top.v:73` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_overlap_low_io_top.v:74` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_overlap_low_io_top.v:75` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_overlap_low_io_top.v:76` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_overlap_low_io_top.v:77` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_overlap_low_io_top.v:78` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_overlap_low_io_top.v:79` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_overlap_low_io_top.v:80` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_overlap_low_io_top.v:83` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_overlap_low_io_top.v:84` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_overlap_low_io_top.v:85` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_overlap_low_io_top.v:86` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_overlap_low_io_top.v:87` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_overlap_low_io_top.v:88` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_overlap_low_io_top.v:89` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_overlap_low_io_top.v:90` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_overlap_low_io_top.v:118` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_overlap_low_io_top.v:119` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_overlap_low_io_top.v:120` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_overlap_low_io_top.v:121` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_overlap_low_io_top.v:122` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_overlap_low_io_top.v:123` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_overlap_low_io_top.v:124` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_overlap_low_io_top.v:125` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_overlap_low_io_top.v:126` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_overlap_low_io_top.v:127` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_overlap_low_io_top.v:128` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_overlap_low_io_top.v:129` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_overlap_low_io_top.v:130` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_overlap_low_io_top.v:131` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_overlap_low_io_top.v:132` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_overlap_low_io_top.v:133` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_overlap_low_io_top.v:137` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_overlap_low_io_top.v:138` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_overlap_low_io_top.v:139` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_overlap_low_io_top.v:140` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_overlap_low_io_top.v:141` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_overlap_low_io_top.v:142` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_overlap_low_io_top.v:143` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_overlap_low_io_top.v:144` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_overlap_low_io_top.v:145` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_overlap_low_io_top.v:146` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_overlap_low_io_top.v:147` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_overlap_low_io_top.v:150` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_overlap_low_io_top.v:151` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_overlap_low_io_top.v:152` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_overlap_low_io_top.v:153` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_overlap_low_io_top.v:154` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_overlap_low_io_top.v:155` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_overlap_low_io_top.v:156` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_overlap_low_io_top.v:157` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_overlap_low_io_top.v:158` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_overlap_low_io_top.v:159` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_overlap_low_io_top.v:160` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_overlap_low_io_top.v:161` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_overlap_low_io_top.v:162` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_overlap_low_io_top.v:163` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_overlap_low_io_top.v:164` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_overlap_low_io_top.v:165` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_overlap_low_io_top.v:166` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_overlap_low_io_top.v:167` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_overlap_low_io_top.v:168` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_overlap_low_io_top.v:169` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_overlap_low_io_top.v:170` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_overlap_low_io_top.v:171` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_overlap_low_io_top.v:172` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_overlap_low_io_top.v:173` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_overlap_low_io_top.v:187` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_overlap_low_io_top.v:188` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_overlap_low_io_top.v:189` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_overlap_low_io_top.v:192` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_overlap_low_io_top.v:193` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_overlap_low_io_top.v:194` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_overlap_low_io_top.v:195` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_overlap_low_io_top.v:196` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_overlap_low_io_top.v:197` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_overlap_low_io_top.v:198` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_overlap_low_io_top.v:199` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_overlap_low_io_top.v:202` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_overlap_low_io_top.v:203` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_overlap_low_io_top.v:204` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_overlap_low_io_top.v:216` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_overlap_low_io_top.v:517` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
