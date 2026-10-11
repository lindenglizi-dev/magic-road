# Verilog deliverable gate

Root: `E:\project\qiansai\anlogic_topic2_work\lab1_sc500_road_vision\cnn\hw_validation\production\reports\v7_low_io_physical_20261006\shell\road_low_io_physical_shell.v`
Delivery ready: `False`
Summary: **667 error(s)**, **0 strict warning(s)**

## Actionable VG findings

<a id="vg-finding-1"></a>
### VG068: Header Description/Simulations fields must use the fixed bilingual path contract (`description/testbench` in English and `Description/TestBench` in Chinese).
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:1`
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
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 49.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:92`
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

<a id="vg-finding-3"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 49.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:93`
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

<a id="vg-finding-4"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 49.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:94`
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
- Location: `road_low_io_physical_shell.v:95`
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
- Location: `road_low_io_physical_shell.v:96`
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
- Location: `road_low_io_physical_shell.v:97`
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
- Location: `road_low_io_physical_shell.v:100`
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
- Location: `road_low_io_physical_shell.v:101`
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
- Location: `road_low_io_physical_shell.v:104`
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
- Location: `road_low_io_physical_shell.v:105`
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
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 49.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:106`
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
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 49.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:107`
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
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 49.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:118`
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
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 49.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:123`
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
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 49.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:124`
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
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 49.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:125`
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

<a id="vg-finding-18"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 49.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:126`
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

<a id="vg-finding-19"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 49.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:127`
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

<a id="vg-finding-20"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 49.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:128`
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

<a id="vg-finding-21"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 49.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:129`
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

<a id="vg-finding-22"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 49.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:130`
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

<a id="vg-finding-23"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 49.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:131`
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

<a id="vg-finding-24"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 49.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:134`
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

<a id="vg-finding-25"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 49.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:135`
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

<a id="vg-finding-26"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 49.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:136`
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

<a id="vg-finding-27"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 49.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:137`
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

<a id="vg-finding-28"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 49.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:138`
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

<a id="vg-finding-29"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 49.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:139`
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

<a id="vg-finding-30"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 49.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:140`
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

<a id="vg-finding-31"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 49.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:144`
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

<a id="vg-finding-32"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 49.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:145`
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

<a id="vg-finding-33"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 49.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:149`
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

<a id="vg-finding-34"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 49.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:150`
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

<a id="vg-finding-35"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 49.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:151`
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

<a id="vg-finding-36"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 50.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:152`
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

<a id="vg-finding-37"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 50.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:153`
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

<a id="vg-finding-38"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 50.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:154`
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

<a id="vg-finding-39"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 49.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:155`
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

<a id="vg-finding-40"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 49.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:158`
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

<a id="vg-finding-41"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 49.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:159`
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

<a id="vg-finding-42"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 49.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:160`
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

<a id="vg-finding-43"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 50.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:161`
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

<a id="vg-finding-44"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 50.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:162`
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

<a id="vg-finding-45"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 50.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:163`
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

<a id="vg-finding-46"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 49.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:166`
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

<a id="vg-finding-47"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 49.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:168`
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

<a id="vg-finding-48"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 50.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:169`
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

<a id="vg-finding-49"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 50.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:170`
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

<a id="vg-finding-50"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 49.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:173`
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

<a id="vg-finding-51"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 49.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:174`
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

<a id="vg-finding-52"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 50.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:175`
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

<a id="vg-finding-53"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 50.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:176`
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

<a id="vg-finding-54"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 50.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:177`
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

<a id="vg-finding-55"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 50.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:178`
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

<a id="vg-finding-56"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 50.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:179`
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

<a id="vg-finding-57"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 50.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:180`
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

<a id="vg-finding-58"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 50.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:181`
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

<a id="vg-finding-59"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 50.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:182`
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

<a id="vg-finding-60"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 49.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:186`
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

<a id="vg-finding-61"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 49.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:187`
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

<a id="vg-finding-62"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 49.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:188`
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

<a id="vg-finding-63"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 49.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:189`
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

<a id="vg-finding-64"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 49.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:190`
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

<a id="vg-finding-65"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 49.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:191`
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

<a id="vg-finding-66"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 49.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:192`
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

<a id="vg-finding-67"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 49.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:193`
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

<a id="vg-finding-68"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 49.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:194`
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

<a id="vg-finding-69"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 50.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:195`
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

<a id="vg-finding-70"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 49.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:198`
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

<a id="vg-finding-71"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 49.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:199`
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

<a id="vg-finding-72"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 49.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:200`
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

<a id="vg-finding-73"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 49.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:201`
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

<a id="vg-finding-74"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 49.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:202`
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

<a id="vg-finding-75"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 49.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:203`
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

<a id="vg-finding-76"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 49.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:204`
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

<a id="vg-finding-77"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 49.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:205`
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

<a id="vg-finding-78"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 49.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:206`
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

<a id="vg-finding-79"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 49.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:207`
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

<a id="vg-finding-80"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 50.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:208`
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

<a id="vg-finding-81"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 50.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:209`
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

<a id="vg-finding-82"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 50.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:213`
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

<a id="vg-finding-83"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 50.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:214`
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

<a id="vg-finding-84"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 50.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:215`
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

<a id="vg-finding-85"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 50.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:216`
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

<a id="vg-finding-86"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 49.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:220`
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

<a id="vg-finding-87"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 49.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:263`
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

<a id="vg-finding-88"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 49.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:264`
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

<a id="vg-finding-89"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 49.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:265`
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

<a id="vg-finding-90"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 50.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:270`
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

<a id="vg-finding-91"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 52.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:272`
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

<a id="vg-finding-92"></a>
### VG060: Inline comment must start at display column 51, aligned from region anchor column 48; got 52.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:274`
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

<a id="vg-finding-93"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 51.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:276`
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

<a id="vg-finding-94"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 51.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:278`
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

<a id="vg-finding-95"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 52.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:310`
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

<a id="vg-finding-96"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 51.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:312`
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

<a id="vg-finding-97"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 49.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:318`
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

<a id="vg-finding-98"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 54.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:335`
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

<a id="vg-finding-99"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 54.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:340`
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

<a id="vg-finding-100"></a>
### VG060: Inline comment must start at display column 51, aligned from region anchor column 48; got 54.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:345`
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

<a id="vg-finding-101"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 50.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:349`
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

<a id="vg-finding-102"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 54.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:353`
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

<a id="vg-finding-103"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 54.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:358`
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

<a id="vg-finding-104"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 54.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:363`
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

<a id="vg-finding-105"></a>
### VG060: Inline comment must start at display column 49, aligned from region anchor column 48; got 54.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:368`
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

<a id="vg-finding-106"></a>
### VG060: Inline comment must start at display column 49, aligned from region anchor column 48; got 54.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:373`
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

<a id="vg-finding-107"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 54.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:383`
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

<a id="vg-finding-108"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 54.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:388`
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

<a id="vg-finding-109"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 54.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:393`
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

<a id="vg-finding-110"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 54.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:398`
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

<a id="vg-finding-111"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 54.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:403`
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

<a id="vg-finding-112"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 50.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:407`
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

<a id="vg-finding-113"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 51.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:416`
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

<a id="vg-finding-114"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 51.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:417`
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

<a id="vg-finding-115"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 51.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:431`
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

<a id="vg-finding-116"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 51.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:432`
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

<a id="vg-finding-117"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 51.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:433`
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

<a id="vg-finding-118"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 51.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:434`
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

<a id="vg-finding-119"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 53.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:437`
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

<a id="vg-finding-120"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 53.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:438`
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

<a id="vg-finding-121"></a>
### VG060: Inline comment must start at display column 49, aligned from region anchor column 48; got 53.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:441`
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

<a id="vg-finding-122"></a>
### VG060: Inline comment must start at display column 49, aligned from region anchor column 48; got 53.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:444`
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

<a id="vg-finding-123"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 53.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:448`
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

<a id="vg-finding-124"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 51.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:456`
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

<a id="vg-finding-125"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 51.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:457`
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

<a id="vg-finding-126"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 51.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:458`
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

<a id="vg-finding-127"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 51.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:459`
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

<a id="vg-finding-128"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 51.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:460`
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

<a id="vg-finding-129"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 51.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:462`
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

<a id="vg-finding-130"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 51.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:463`
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

<a id="vg-finding-131"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 51.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:464`
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

<a id="vg-finding-132"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 51.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:466`
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

<a id="vg-finding-133"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 51.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:475`
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

<a id="vg-finding-134"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 51.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:476`
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

<a id="vg-finding-135"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 51.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:477`
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

<a id="vg-finding-136"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 51.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:479`
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

<a id="vg-finding-137"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 51.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:480`
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

<a id="vg-finding-138"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 51.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:481`
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

<a id="vg-finding-139"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 51.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:496`
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

<a id="vg-finding-140"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 51.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:497`
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

<a id="vg-finding-141"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 51.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:498`
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

<a id="vg-finding-142"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 51.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:499`
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

<a id="vg-finding-143"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 51.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:500`
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

<a id="vg-finding-144"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 51.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:511`
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

<a id="vg-finding-145"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 51.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:512`
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

<a id="vg-finding-146"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 51.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:513`
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

<a id="vg-finding-147"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 51.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:517`
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

<a id="vg-finding-148"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 51.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:525`
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

<a id="vg-finding-149"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 51.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:526`
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

<a id="vg-finding-150"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 51.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:527`
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

<a id="vg-finding-151"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 51.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:528`
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

<a id="vg-finding-152"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 51.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:529`
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

<a id="vg-finding-153"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 51.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:530`
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

<a id="vg-finding-154"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 53.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:534`
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

<a id="vg-finding-155"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 52.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:535`
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

<a id="vg-finding-156"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 52.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:536`
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

<a id="vg-finding-157"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 52.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:537`
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

<a id="vg-finding-158"></a>
### VG060: Inline comment must start at display column 49, aligned from region anchor column 48; got 52.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:538`
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

<a id="vg-finding-159"></a>
### VG060: Inline comment must start at display column 49, aligned from region anchor column 48; got 52.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:544`
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

<a id="vg-finding-160"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 52.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:547`
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

<a id="vg-finding-161"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 51.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:555`
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

<a id="vg-finding-162"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 51.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:556`
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

<a id="vg-finding-163"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 51.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:557`
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

<a id="vg-finding-164"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 51.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:558`
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

<a id="vg-finding-165"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 51.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:559`
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

<a id="vg-finding-166"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 51.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:560`
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

<a id="vg-finding-167"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 53.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:563`
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

<a id="vg-finding-168"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 52.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:564`
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

<a id="vg-finding-169"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 53.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:566`
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

<a id="vg-finding-170"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 52.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:568`
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

<a id="vg-finding-171"></a>
### VG060: Inline comment must start at display column 49, aligned from region anchor column 48; got 53.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:573`
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

<a id="vg-finding-172"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 53.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:574`
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

<a id="vg-finding-173"></a>
### VG060: Inline comment must start at display column 49, aligned from region anchor column 48; got 53.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:579`
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

<a id="vg-finding-174"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 52.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:582`
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

<a id="vg-finding-175"></a>
### VG060: Inline comment must start at display column 51, aligned from region anchor column 48; got 53.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:588`
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

<a id="vg-finding-176"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 51.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:596`
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

<a id="vg-finding-177"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 51.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:597`
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

<a id="vg-finding-178"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 51.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:598`
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

<a id="vg-finding-179"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 51.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:599`
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

<a id="vg-finding-180"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 51.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:600`
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

<a id="vg-finding-181"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 53.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:603`
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

<a id="vg-finding-182"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 53.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:605`
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

<a id="vg-finding-183"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 53.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:606`
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

<a id="vg-finding-184"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 51.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:623`
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

<a id="vg-finding-185"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 51.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:624`
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

<a id="vg-finding-186"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 53.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:627`
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

<a id="vg-finding-187"></a>
### VG060: Inline comment must start at display column 51, aligned from region anchor column 48; got 53.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:628`
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

<a id="vg-finding-188"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 53.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:630`
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

<a id="vg-finding-189"></a>
### VG060: Inline comment must start at display column 54, aligned from region anchor column 48; got 61.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:636`
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

<a id="vg-finding-190"></a>
### VG060: Inline comment must start at display column 54, aligned from region anchor column 48; got 61.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:642`
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

<a id="vg-finding-191"></a>
### VG060: Inline comment must start at display column 54, aligned from region anchor column 48; got 61.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:648`
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

<a id="vg-finding-192"></a>
### VG060: Inline comment must start at display column 54, aligned from region anchor column 48; got 61.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:654`
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

<a id="vg-finding-193"></a>
### VG060: Inline comment must start at display column 54, aligned from region anchor column 48; got 61.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:660`
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

<a id="vg-finding-194"></a>
### VG060: Inline comment must start at display column 60, aligned from region anchor column 48; got 61.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:661`
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

<a id="vg-finding-195"></a>
### VG060: Inline comment must start at display column 54, aligned from region anchor column 48; got 61.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:666`
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

<a id="vg-finding-196"></a>
### VG060: Inline comment must start at display column 50, aligned from region anchor column 48; got 57.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:671`
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

<a id="vg-finding-197"></a>
### VG060: Inline comment must start at display column 56, aligned from region anchor column 48; got 57.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:672`
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

<a id="vg-finding-198"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 51.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:682`
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

<a id="vg-finding-199"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 51.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:683`
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

<a id="vg-finding-200"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 51.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:684`
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

<a id="vg-finding-201"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 51.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:685`
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

<a id="vg-finding-202"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 51.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:686`
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

<a id="vg-finding-203"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 51.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:687`
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

<a id="vg-finding-204"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 51.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:688`
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

<a id="vg-finding-205"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 51.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:689`
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

<a id="vg-finding-206"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 51.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:698`
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

<a id="vg-finding-207"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 51.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:707`
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

<a id="vg-finding-208"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 51.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:708`
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

<a id="vg-finding-209"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 53.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:711`
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

<a id="vg-finding-210"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 53.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:714`
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

<a id="vg-finding-211"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 53.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:716`
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

<a id="vg-finding-212"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 53.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:722`
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

<a id="vg-finding-213"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 53.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:724`
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

<a id="vg-finding-214"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 55.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:728`
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

<a id="vg-finding-215"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 55.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:730`
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

<a id="vg-finding-216"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 53.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:752`
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

<a id="vg-finding-217"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 53.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:755`
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

<a id="vg-finding-218"></a>
### VG025: Control statements must use explicit begin/end blocks.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:323`
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

<a id="vg-finding-219"></a>
### VG025: Control statements must use explicit begin/end blocks.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:324`
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

<a id="vg-finding-220"></a>
### VG025: Control statements must use explicit begin/end blocks.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:325`
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

<a id="vg-finding-221"></a>
### VG025: Control statements must use explicit begin/end blocks.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:326`
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

<a id="vg-finding-222"></a>
### VG025: Control statements must use explicit begin/end blocks.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:327`
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

<a id="vg-finding-223"></a>
### VG025: Control statements must use explicit begin/end blocks.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:328`
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

<a id="vg-finding-224"></a>
### VG013: Flag-like signal `chain_input_ready` should use `flag_` prefix unless it is an output bridge.
- Status: `failed`
- Severity: `error`
- Location: `file:road_low_io_physical_shell.v:unknown`
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

<a id="vg-finding-225"></a>
### VG013: Flag-like signal `chain_table_ready` should use `flag_` prefix unless it is an output bridge.
- Status: `failed`
- Severity: `error`
- Location: `file:road_low_io_physical_shell.v:unknown`
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

<a id="vg-finding-226"></a>
### VG013: Flag-like signal `chain_cache_read_ready` should use `flag_` prefix unless it is an output bridge.
- Status: `failed`
- Severity: `error`
- Location: `file:road_low_io_physical_shell.v:unknown`
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

<a id="vg-finding-227"></a>
### VG013: Flag-like signal `chain_cache_result_valid` should use `flag_` prefix unless it is an output bridge.
- Status: `failed`
- Severity: `error`
- Location: `file:road_low_io_physical_shell.v:unknown`
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

<a id="vg-finding-228"></a>
### VG013: Flag-like signal `cnt_packet_loaded` should use `flag_` prefix unless it is an output bridge.
- Status: `failed`
- Severity: `error`
- Location: `file:road_low_io_physical_shell.v:unknown`
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

<a id="vg-finding-229"></a>
### VG013: Flag-like signal `reg_packet_first` should use `flag_` prefix unless it is an output bridge.
- Status: `failed`
- Severity: `error`
- Location: `file:road_low_io_physical_shell.v:unknown`
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

<a id="vg-finding-230"></a>
### VG013: Flag-like signal `reg_packet_last` should use `flag_` prefix unless it is an output bridge.
- Status: `failed`
- Severity: `error`
- Location: `file:road_low_io_physical_shell.v:unknown`
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

<a id="vg-finding-231"></a>
### VG013: Flag-like signal `reg_packet_mask` should use `flag_` prefix unless it is an output bridge.
- Status: `failed`
- Severity: `error`
- Location: `file:road_low_io_physical_shell.v:unknown`
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

<a id="vg-finding-232"></a>
### VG013: Flag-like signal `reg_packet_activation` should use `flag_` prefix unless it is an output bridge.
- Status: `failed`
- Severity: `error`
- Location: `file:road_low_io_physical_shell.v:unknown`
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

<a id="vg-finding-233"></a>
### VG013: Flag-like signal `reg_packet_weight` should use `flag_` prefix unless it is an output bridge.
- Status: `failed`
- Severity: `error`
- Location: `file:road_low_io_physical_shell.v:unknown`
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

<a id="vg-finding-234"></a>
### VG013: Flag-like signal `reg_packet_bias` should use `flag_` prefix unless it is an output bridge.
- Status: `failed`
- Severity: `error`
- Location: `file:road_low_io_physical_shell.v:unknown`
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

<a id="vg-finding-235"></a>
### VG013: Flag-like signal `reg_packet_header_legal` should use `flag_` prefix unless it is an output bridge.
- Status: `failed`
- Severity: `error`
- Location: `file:road_low_io_physical_shell.v:unknown`
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

<a id="vg-finding-236"></a>
### VG013: Flag-like signal `reg_table_pending_valid` should use `flag_` prefix unless it is an output bridge.
- Status: `failed`
- Severity: `error`
- Location: `file:road_low_io_physical_shell.v:unknown`
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

<a id="vg-finding-237"></a>
### VG013: Flag-like signal `reg_table_pending_data` should use `flag_` prefix unless it is an output bridge.
- Status: `failed`
- Severity: `error`
- Location: `file:road_low_io_physical_shell.v:unknown`
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

<a id="vg-finding-238"></a>
### VG013: Counter-like signal `reg_run_packet_count` should use `cnt_` prefix.
- Status: `failed`
- Severity: `error`
- Location: `file:road_low_io_physical_shell.v:unknown`
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

<a id="vg-finding-239"></a>
### VG013: Flag-like signal `reg_run_packet_count` should use `flag_` prefix unless it is an output bridge.
- Status: `failed`
- Severity: `error`
- Location: `file:road_low_io_physical_shell.v:unknown`
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

<a id="vg-finding-240"></a>
### VG013: Counter-like signal `reg_export_count` should use `cnt_` prefix.
- Status: `failed`
- Severity: `error`
- Location: `file:road_low_io_physical_shell.v:unknown`
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

<a id="vg-finding-241"></a>
### VG013: Flag-like signal `enc_packet_terms` should use `flag_` prefix unless it is an output bridge.
- Status: `failed`
- Severity: `error`
- Location: `file:road_low_io_physical_shell.v:unknown`
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

<a id="vg-finding-242"></a>
### VG013: Counter-like signal `next_group_count` should use `cnt_` prefix.
- Status: `failed`
- Severity: `error`
- Location: `file:road_low_io_physical_shell.v:unknown`
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

<a id="vg-finding-243"></a>
### VG013: Counter-like signal `next_term_count` should use `cnt_` prefix.
- Status: `failed`
- Severity: `error`
- Location: `file:road_low_io_physical_shell.v:unknown`
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

<a id="vg-finding-244"></a>
### VG013: Flag-like signal `chain_input_valid` should use `flag_` prefix unless it is an output bridge.
- Status: `failed`
- Severity: `error`
- Location: `file:road_low_io_physical_shell.v:unknown`
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

<a id="vg-finding-245"></a>
### VG013: Flag-like signal `chain_table_valid` should use `flag_` prefix unless it is an output bridge.
- Status: `failed`
- Severity: `error`
- Location: `file:road_low_io_physical_shell.v:unknown`
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

<a id="vg-finding-246"></a>
### VG013: Flag-like signal `chain_cache_read_valid` should use `flag_` prefix unless it is an output bridge.
- Status: `failed`
- Severity: `error`
- Location: `file:road_low_io_physical_shell.v:unknown`
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

<a id="vg-finding-247"></a>
### VG013: Flag-like signal `chain_cache_result_ready` should use `flag_` prefix unless it is an output bridge.
- Status: `failed`
- Severity: `error`
- Location: `file:road_low_io_physical_shell.v:unknown`
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

<a id="vg-finding-248"></a>
### VG030: Inline wire initialization is forbidden; declare wire and use a separate assign.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:247`
- Evidence:
- node_kind: `verilog_rtl`
- detail: assign.inline_wire
- source_excerpt: `assign.inline_wire`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
assign.inline_wire
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-249"></a>
### VG030: Inline wire initialization is forbidden; declare wire and use a separate assign.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:248`
- Evidence:
- node_kind: `verilog_rtl`
- detail: assign.inline_wire
- source_excerpt: `assign.inline_wire`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
assign.inline_wire
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-250"></a>
### VG030: Inline wire initialization is forbidden; declare wire and use a separate assign.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:249`
- Evidence:
- node_kind: `verilog_rtl`
- detail: assign.inline_wire
- source_excerpt: `assign.inline_wire`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
assign.inline_wire
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-251"></a>
### VG030: Inline wire initialization is forbidden; declare wire and use a separate assign.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:250`
- Evidence:
- node_kind: `verilog_rtl`
- detail: assign.inline_wire
- source_excerpt: `assign.inline_wire`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
assign.inline_wire
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-252"></a>
### VG030: Inline wire initialization is forbidden; declare wire and use a separate assign.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:251`
- Evidence:
- node_kind: `verilog_rtl`
- detail: assign.inline_wire
- source_excerpt: `assign.inline_wire`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
assign.inline_wire
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-253"></a>
### VG030: Inline wire initialization is forbidden; declare wire and use a separate assign.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:252`
- Evidence:
- node_kind: `verilog_rtl`
- detail: assign.inline_wire
- source_excerpt: `assign.inline_wire`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
assign.inline_wire
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-254"></a>
### VG030: Inline wire initialization is forbidden; declare wire and use a separate assign.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:253`
- Evidence:
- node_kind: `verilog_rtl`
- detail: assign.inline_wire
- source_excerpt: `assign.inline_wire`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
assign.inline_wire
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-255"></a>
### VG030: Inline wire initialization is forbidden; declare wire and use a separate assign.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:254`
- Evidence:
- node_kind: `verilog_rtl`
- detail: assign.inline_wire
- source_excerpt: `assign.inline_wire`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
assign.inline_wire
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-256"></a>
### VG030: Inline wire initialization is forbidden; declare wire and use a separate assign.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:255`
- Evidence:
- node_kind: `verilog_rtl`
- detail: assign.inline_wire
- source_excerpt: `assign.inline_wire`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
assign.inline_wire
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-257"></a>
### VG030: Inline wire initialization is forbidden; declare wire and use a separate assign.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:256`
- Evidence:
- node_kind: `verilog_rtl`
- detail: assign.inline_wire
- source_excerpt: `assign.inline_wire`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
assign.inline_wire
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-258"></a>
### VG030: Inline wire initialization is forbidden; declare wire and use a separate assign.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:257`
- Evidence:
- node_kind: `verilog_rtl`
- detail: assign.inline_wire
- source_excerpt: `assign.inline_wire`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
assign.inline_wire
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-259"></a>
### VG030: Inline wire initialization is forbidden; declare wire and use a separate assign.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:258`
- Evidence:
- node_kind: `verilog_rtl`
- detail: assign.inline_wire
- source_excerpt: `assign.inline_wire`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
assign.inline_wire
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-260"></a>
### VG030: Inline wire initialization is forbidden; declare wire and use a separate assign.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:259`
- Evidence:
- node_kind: `verilog_rtl`
- detail: assign.inline_wire
- source_excerpt: `assign.inline_wire`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
assign.inline_wire
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-261"></a>
### VG020: Always block `always@(posedge i_clk or negedge i_rstn)` assigns multiple targets ['cnt_rx_words', 'cnt_tx_words']; split to one target per always.
- Status: `failed`
- Severity: `error`
- Location: `file:road_low_io_physical_shell.v:unknown`
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

<a id="vg-finding-262"></a>
### VG020: Always block `always@(posedge i_clk or negedge i_rstn)` assigns multiple targets ['cnt_table_entry', 'flag_table_complete', 'reg_table_pending_data', 'reg_table_pending_valid']; split to one target per always.
- Status: `failed`
- Severity: `error`
- Location: `file:road_low_io_physical_shell.v:unknown`
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

<a id="vg-finding-263"></a>
### VG020: Always block `always@(posedge i_clk or negedge i_rstn)` assigns multiple targets ['cnt_payload_word', 'reg_packet_first', 'reg_packet_header_legal', 'reg_packet_last', 'reg_packet_mask']; split to one target per always.
- Status: `failed`
- Severity: `error`
- Location: `file:road_low_io_physical_shell.v:unknown`
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

<a id="vg-finding-264"></a>
### VG020: Always block `always@(posedge i_clk or negedge i_rstn)` assigns multiple targets ['reg_packet_activation', 'reg_packet_bias', 'reg_packet_weight']; split to one target per always.
- Status: `failed`
- Severity: `error`
- Location: `file:road_low_io_physical_shell.v:unknown`
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

<a id="vg-finding-265"></a>
### VG020: Always block `always@(posedge i_clk or negedge i_rstn)` has complex lvalues and multiple targets; formatter must not guess a split.
- Status: `failed`
- Severity: `error`
- Location: `file:road_low_io_physical_shell.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: always.complex_lvalue
- source_excerpt: `always.complex_lvalue`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
always.complex_lvalue
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-266"></a>
### VG020: Always block `always@(posedge i_clk or negedge i_rstn)` assigns multiple targets ['cnt_group_position', 'cnt_packet_loaded', 'cnt_position_loaded', 'cnt_term_position', 'flag_position_open', 'reg_activation_memory', 'reg_bias_memory', 'reg_first_memory', 'reg_last_memory', 'reg_mask_memory', 'reg_weight_memory']; split to one target per always.
- Status: `failed`
- Severity: `error`
- Location: `file:road_low_io_physical_shell.v:unknown`
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

<a id="vg-finding-267"></a>
### VG020: Always block `always@(posedge i_clk or negedge i_rstn)` has complex lvalues and multiple targets; formatter must not guess a split.
- Status: `failed`
- Severity: `error`
- Location: `file:road_low_io_physical_shell.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: always.complex_lvalue
- source_excerpt: `always.complex_lvalue`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
always.complex_lvalue
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-268"></a>
### VG020: Always block `always@(posedge i_clk or negedge i_rstn)` assigns multiple targets ['cnt_core_inputs', 'cnt_run_index', 'flag_core_busy_observed', 'flag_run_complete', 'flag_run_issued', 'reg_run_packet_count']; split to one target per always.
- Status: `failed`
- Severity: `error`
- Location: `file:road_low_io_physical_shell.v:unknown`
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

<a id="vg-finding-269"></a>
### VG020: Always block `always@(posedge i_clk or negedge i_rstn)` assigns multiple targets ['cnt_core_cycles', 'cnt_export_cycles', 'cnt_preload_cycles', 'flag_core_timing_active', 'flag_export_timing_active', 'flag_preload_active']; split to one target per always.
- Status: `failed`
- Severity: `error`
- Location: `file:road_low_io_physical_shell.v:unknown`
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

<a id="vg-finding-270"></a>
### VG020: Always block `always@(posedge i_clk or negedge i_rstn)` assigns multiple targets ['cnt_export_addr', 'cnt_result_outputs', 'reg_diagnostic_addr', 'reg_export_count', 'reg_result_checksum']; split to one target per always.
- Status: `failed`
- Severity: `error`
- Location: `file:road_low_io_physical_shell.v:unknown`
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

<a id="vg-finding-271"></a>
### VG020: Always block `always@(posedge i_clk or negedge i_rstn)` assigns multiple targets ['flag_shell_fault', 'reg_shell_error']; split to one target per always.
- Status: `failed`
- Severity: `error`
- Location: `file:road_low_io_physical_shell.v:unknown`
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

<a id="vg-finding-272"></a>
### VG020: Always block `always@(posedge i_clk or negedge i_rstn)` assigns multiple targets ['cnt_status_index', 'reg_snapshot_core', 'reg_snapshot_core_inputs', 'reg_snapshot_export', 'reg_snapshot_preload', 'reg_snapshot_results', 'reg_snapshot_rx_words', 'reg_snapshot_tx_words']; split to one target per always.
- Status: `failed`
- Severity: `error`
- Location: `file:road_low_io_physical_shell.v:unknown`
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

<a id="vg-finding-273"></a>
### VG020: Always block `always@(posedge i_clk or negedge i_rstn)` assigns multiple targets ['tx_data_o', 'tx_valid_o']; split to one target per always.
- Status: `failed`
- Severity: `error`
- Location: `file:road_low_io_physical_shell.v:unknown`
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

<a id="vg-finding-274"></a>
### VG054: FSM next-state if / else if chain must end with an explicit else branch.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:320`
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

<a id="vg-finding-275"></a>
### VG054: FSM next-state if / else if chain must end with an explicit else branch.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:333`
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

<a id="vg-finding-276"></a>
### VG054: FSM next-state if / else if chain must end with an explicit else branch.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:338`
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

<a id="vg-finding-277"></a>
### VG054: FSM next-state if / else if chain must end with an explicit else branch.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:343`
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

<a id="vg-finding-278"></a>
### VG054: FSM next-state if / else if chain must end with an explicit else branch.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:351`
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

<a id="vg-finding-279"></a>
### VG054: FSM next-state if / else if chain must end with an explicit else branch.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:356`
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

<a id="vg-finding-280"></a>
### VG054: FSM next-state if / else if chain must end with an explicit else branch.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:361`
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

<a id="vg-finding-281"></a>
### VG054: FSM next-state if / else if chain must end with an explicit else branch.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:366`
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

<a id="vg-finding-282"></a>
### VG054: FSM next-state if / else if chain must end with an explicit else branch.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:371`
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

<a id="vg-finding-283"></a>
### VG054: FSM next-state if / else if chain must end with an explicit else branch.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:376`
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

<a id="vg-finding-284"></a>
### VG054: FSM next-state if / else if chain must end with an explicit else branch.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:381`
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

<a id="vg-finding-285"></a>
### VG054: FSM next-state if / else if chain must end with an explicit else branch.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:386`
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

<a id="vg-finding-286"></a>
### VG054: FSM next-state if / else if chain must end with an explicit else branch.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:391`
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

<a id="vg-finding-287"></a>
### VG054: FSM next-state if / else if chain must end with an explicit else branch.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:396`
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

<a id="vg-finding-288"></a>
### VG054: FSM next-state if / else if chain must end with an explicit else branch.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:401`
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

<a id="vg-finding-289"></a>
### VG063: Case branch leading comment must be the pure comment line immediately above the block.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:320`
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

<a id="vg-finding-290"></a>
### VG063: Case branch leading comment must be the pure comment line immediately above the block.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:333`
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

<a id="vg-finding-291"></a>
### VG063: Case branch leading comment must be the pure comment line immediately above the block.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:338`
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

<a id="vg-finding-292"></a>
### VG063: Case branch leading comment must be the pure comment line immediately above the block.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:343`
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

<a id="vg-finding-293"></a>
### VG063: Case branch leading comment must be the pure comment line immediately above the block.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:348`
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

<a id="vg-finding-294"></a>
### VG063: Case branch leading comment must be the pure comment line immediately above the block.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:351`
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

<a id="vg-finding-295"></a>
### VG063: Case branch leading comment must be the pure comment line immediately above the block.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:356`
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

<a id="vg-finding-296"></a>
### VG063: Case branch leading comment must be the pure comment line immediately above the block.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:361`
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

<a id="vg-finding-297"></a>
### VG063: Case branch leading comment must be the pure comment line immediately above the block.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:366`
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

<a id="vg-finding-298"></a>
### VG063: Case branch leading comment must be the pure comment line immediately above the block.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:371`
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

<a id="vg-finding-299"></a>
### VG063: Case branch leading comment must be the pure comment line immediately above the block.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:376`
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

<a id="vg-finding-300"></a>
### VG063: Case branch leading comment must be the pure comment line immediately above the block.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:381`
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

<a id="vg-finding-301"></a>
### VG063: Case branch leading comment must be the pure comment line immediately above the block.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:386`
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

<a id="vg-finding-302"></a>
### VG063: Case branch leading comment must be the pure comment line immediately above the block.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:391`
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

<a id="vg-finding-303"></a>
### VG063: Case branch leading comment must be the pure comment line immediately above the block.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:396`
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

<a id="vg-finding-304"></a>
### VG063: Case branch leading comment must be the pure comment line immediately above the block.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:401`
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

<a id="vg-finding-305"></a>
### VG063: Case branch leading comment must be the pure comment line immediately above the block.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:406`
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

<a id="vg-finding-306"></a>
### VG031: Module instances must stay inside the 模块实例化区域 banner.
- Status: `failed`
- Severity: `error`
- Location: `file:road_low_io_physical_shell.v:unknown`
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

<a id="vg-finding-307"></a>
### VG061: Item `CMD_TABLE_BEGIN` must be placed in 配置参数区域, not `状态参数区域`.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:92`
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

<a id="vg-finding-308"></a>
### VG061: Item `CMD_PACKET_BEGIN` must be placed in 配置参数区域, not `状态参数区域`.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:93`
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

<a id="vg-finding-309"></a>
### VG061: Item `CMD_RUN` must be placed in 配置参数区域, not `状态参数区域`.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:94`
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

<a id="vg-finding-310"></a>
### VG061: Item `CMD_EXPORT` must be placed in 配置参数区域, not `状态参数区域`.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:95`
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

<a id="vg-finding-311"></a>
### VG061: Item `CMD_STATUS` must be placed in 配置参数区域, not `状态参数区域`.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:96`
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

<a id="vg-finding-312"></a>
### VG061: Item `CMD_DIAGNOSTIC_READ` must be placed in 配置参数区域, not `状态参数区域`.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:97`
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

<a id="vg-finding-313"></a>
### VG061: Item `ERR_COMMAND` must be placed in 配置参数区域, not `状态参数区域`.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:100`
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

<a id="vg-finding-314"></a>
### VG061: Item `ERR_TABLE_SEQUENCE` must be placed in 配置参数区域, not `状态参数区域`.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:101`
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

<a id="vg-finding-315"></a>
### VG061: Item `ERR_PACKET_SEQUENCE` must be placed in 配置参数区域, not `状态参数区域`.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:102`
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

<a id="vg-finding-316"></a>
### VG061: Item `ERR_REDUCTION_RANGE` must be placed in 配置参数区域, not `状态参数区域`.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:103`
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

<a id="vg-finding-317"></a>
### VG061: Item `ERR_RUN_GUARD` must be placed in 配置参数区域, not `状态参数区域`.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:104`
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

<a id="vg-finding-318"></a>
### VG061: Item `ERR_EXPORT_GUARD` must be placed in 配置参数区域, not `状态参数区域`.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:105`
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

<a id="vg-finding-319"></a>
### VG061: Item `ERR_DIAGNOSTIC` must be placed in 配置参数区域, not `状态参数区域`.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:106`
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

<a id="vg-finding-320"></a>
### VG061: Item `ERR_TABLE_CORE` must be placed in 配置参数区域, not `状态参数区域`.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:107`
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

<a id="vg-finding-321"></a>
### VG061: Item `tx_valid_o` must be placed in 输出信号, not `寄存器信号`.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:173`
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

<a id="vg-finding-322"></a>
### VG061: Item `tx_data_o` must be placed in 输出信号, not `寄存器信号`.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:174`
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

<a id="vg-finding-323"></a>
### VG061: Item `reg_shell_error` must be placed in 寄存器信号, not `标志信号`.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:195`
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

<a id="vg-finding-324"></a>
### VG061: Item `enc_packet_terms` must be placed in 编码信号, not `其他信号`.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:213`
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

<a id="vg-finding-325"></a>
### VG061: Item `dec_status_word` must be placed in 译码信号, not `其他信号`.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:216`
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

<a id="vg-finding-326"></a>
### VG061: Item `chain_input_valid` must be placed in 模块实例化信号, not `其他信号连线`.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:247`
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

<a id="vg-finding-327"></a>
### VG061: Item `chain_first` must be placed in 模块实例化信号, not `其他信号连线`.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:248`
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

<a id="vg-finding-328"></a>
### VG061: Item `chain_last` must be placed in 模块实例化信号, not `其他信号连线`.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:249`
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

<a id="vg-finding-329"></a>
### VG061: Item `chain_lane_mask` must be placed in 模块实例化信号, not `其他信号连线`.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:250`
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

<a id="vg-finding-330"></a>
### VG061: Item `chain_activation_data` must be placed in 模块实例化信号, not `其他信号连线`.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:251`
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

<a id="vg-finding-331"></a>
### VG061: Item `chain_weight_data` must be placed in 模块实例化信号, not `其他信号连线`.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:252`
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

<a id="vg-finding-332"></a>
### VG061: Item `chain_bias_data` must be placed in 模块实例化信号, not `其他信号连线`.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:253`
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

<a id="vg-finding-333"></a>
### VG061: Item `chain_table_valid` must be placed in 模块实例化信号, not `其他信号连线`.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:254`
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

<a id="vg-finding-334"></a>
### VG061: Item `chain_table_addr` must be placed in 模块实例化信号, not `其他信号连线`.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:255`
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

<a id="vg-finding-335"></a>
### VG061: Item `chain_table_data` must be placed in 模块实例化信号, not `其他信号连线`.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:256`
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

<a id="vg-finding-336"></a>
### VG061: Item `chain_cache_read_valid` must be placed in 模块实例化信号, not `其他信号连线`.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:257`
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

<a id="vg-finding-337"></a>
### VG061: Item `chain_cache_read_addr` must be placed in 模块实例化信号, not `其他信号连线`.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:258`
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

<a id="vg-finding-338"></a>
### VG061: Item `chain_cache_result_ready` must be placed in 模块实例化信号, not `其他信号连线`.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:259`
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

<a id="vg-finding-339"></a>
### VG061: Item `always@(*)` must be placed in 主要任务处理区域, not `输出信号处理区域`.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:283`
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

<a id="vg-finding-340"></a>
### VG061: Item `always@(posedge i_clk or negedge i_rstn)` must be placed in 状态任务处理区域, not `主要任务处理区域`.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:429`
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

<a id="vg-finding-341"></a>
### VG061: Item `always@(posedge i_clk or negedge i_rstn)` must be placed in 状态任务处理区域, not `主要任务处理区域`.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:454`
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

<a id="vg-finding-342"></a>
### VG061: Item `always@(posedge i_clk or negedge i_rstn)` must be placed in 状态任务处理区域, not `主要任务处理区域`.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:473`
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

<a id="vg-finding-343"></a>
### VG061: Item `always@(posedge i_clk or negedge i_rstn)` must be placed in 状态任务处理区域, not `主要任务处理区域`.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:494`
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

<a id="vg-finding-344"></a>
### VG061: Item `always@(posedge i_clk or negedge i_rstn)` must be placed in 状态任务处理区域, not `主要任务处理区域`.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:523`
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

<a id="vg-finding-345"></a>
### VG061: Item `always@(posedge i_clk or negedge i_rstn)` must be placed in 状态任务处理区域, not `主要任务处理区域`.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:553`
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

<a id="vg-finding-346"></a>
### VG061: Item `always@(posedge i_clk or negedge i_rstn)` must be placed in 状态任务处理区域, not `主要任务处理区域`.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:594`
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

<a id="vg-finding-347"></a>
### VG061: Item `always@(posedge i_clk or negedge i_rstn)` must be placed in 状态任务处理区域, not `主要任务处理区域`.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:621`
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

<a id="vg-finding-348"></a>
### VG061: Item `always@(posedge i_clk or negedge i_rstn)` must be placed in 状态任务处理区域, not `主要任务处理区域`.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:680`
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

<a id="vg-finding-349"></a>
### VG061: Item `always@(posedge i_clk or negedge i_rstn)` must be placed in 输出信号处理区域, not `主要任务处理区域`.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:705`
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

<a id="vg-finding-350"></a>
### VG061: Item `road_onchip_chain_Inst_shell` must be placed in 模块实例化区域, not `主要任务处理区域`.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:762`
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

<a id="vg-finding-351"></a>
### VG070: `输出信号` item `rx_ready_o` must use group label `RX接口`, not `unknown`.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:220`
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

<a id="vg-finding-352"></a>
### VG070: `输出信号连线` item `o_rx_ready` must use group label `RX接口`, not `unknown`.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:263`
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

<a id="vg-finding-353"></a>
### VG070: `输出信号处理区域` item `rx_ready_o` must use group label `RX接口`, not `unknown`.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:269`
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

<a id="vg-finding-354"></a>
### VG066: Comment for process assignment `reg_packet_last` repeats or closely reuses comment from process assignment `reg_packet_first`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:463`
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

<a id="vg-finding-355"></a>
### VG066: Comment for process assignment `reg_last_memory[cnt_packet_loaded]` repeats or closely reuses comment from process assignment `reg_first_memory[cnt_packet_loaded]`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_low_io_physical_shell.v:503`
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

<a id="vg-finding-356"></a>
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

<a id="vg-finding-357"></a>
### VG097: 缺少外部模块接口定义，无法静态比较端口位宽。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:762`
- Evidence:
- node_kind: `verilog_rtl`
- detail: road_onchip_chain road_onchip_chain_Inst_shell
- source_excerpt: `road_onchip_chain road_onchip_chain_Inst_shell`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
road_onchip_chain road_onchip_chain_Inst_shell
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-358"></a>
### VG098: FSM 状态必须能从复位初态到达且具有可证明的后继转移。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:87`
- Evidence:
- node_kind: `verilog_rtl`
- detail: ST_DIAG_REQUEST
- source_excerpt: `ST_DIAG_REQUEST`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
ST_DIAG_REQUEST
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-359"></a>
### VG098: FSM 状态必须能从复位初态到达且具有可证明的后继转移。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:89`
- Evidence:
- node_kind: `verilog_rtl`
- detail: ST_DIAG_SEND
- source_excerpt: `ST_DIAG_SEND`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
ST_DIAG_SEND
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-360"></a>
### VG098: FSM 状态必须能从复位初态到达且具有可证明的后继转移。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:88`
- Evidence:
- node_kind: `verilog_rtl`
- detail: ST_DIAG_WAIT
- source_excerpt: `ST_DIAG_WAIT`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
ST_DIAG_WAIT
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-361"></a>
### VG098: FSM 状态必须能从复位初态到达且具有可证明的后继转移。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:85`
- Evidence:
- node_kind: `verilog_rtl`
- detail: ST_EXPORT_REPORT
- source_excerpt: `ST_EXPORT_REPORT`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
ST_EXPORT_REPORT
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-362"></a>
### VG098: FSM 状态必须能从复位初态到达且具有可证明的后继转移。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:82`
- Evidence:
- node_kind: `verilog_rtl`
- detail: ST_EXPORT_REQUEST
- source_excerpt: `ST_EXPORT_REQUEST`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
ST_EXPORT_REQUEST
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-363"></a>
### VG098: FSM 状态必须能从复位初态到达且具有可证明的后继转移。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:84`
- Evidence:
- node_kind: `verilog_rtl`
- detail: ST_EXPORT_SEND
- source_excerpt: `ST_EXPORT_SEND`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
ST_EXPORT_SEND
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-364"></a>
### VG098: FSM 状态必须能从复位初态到达且具有可证明的后继转移。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:83`
- Evidence:
- node_kind: `verilog_rtl`
- detail: ST_EXPORT_WAIT
- source_excerpt: `ST_EXPORT_WAIT`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
ST_EXPORT_WAIT
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-365"></a>
### VG098: FSM 状态必须能从复位初态到达且具有可证明的后继转移。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:74`
- Evidence:
- node_kind: `verilog_rtl`
- detail: ST_IDLE
- source_excerpt: `ST_IDLE`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
ST_IDLE
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-366"></a>
### VG098: FSM 状态必须能从复位初态到达且具有可证明的后继转移。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:78`
- Evidence:
- node_kind: `verilog_rtl`
- detail: ST_PACKET_COMMIT
- source_excerpt: `ST_PACKET_COMMIT`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
ST_PACKET_COMMIT
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-367"></a>
### VG098: FSM 状态必须能从复位初态到达且具有可证明的后继转移。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:77`
- Evidence:
- node_kind: `verilog_rtl`
- detail: ST_PACKET_PAYLOAD
- source_excerpt: `ST_PACKET_PAYLOAD`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
ST_PACKET_PAYLOAD
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-368"></a>
### VG098: FSM 状态必须能从复位初态到达且具有可证明的后继转移。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:80`
- Evidence:
- node_kind: `verilog_rtl`
- detail: ST_RUN_DRAIN
- source_excerpt: `ST_RUN_DRAIN`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
ST_RUN_DRAIN
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-369"></a>
### VG098: FSM 状态必须能从复位初态到达且具有可证明的后继转移。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:81`
- Evidence:
- node_kind: `verilog_rtl`
- detail: ST_RUN_REPORT
- source_excerpt: `ST_RUN_REPORT`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
ST_RUN_REPORT
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-370"></a>
### VG098: FSM 状态必须能从复位初态到达且具有可证明的后继转移。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:79`
- Evidence:
- node_kind: `verilog_rtl`
- detail: ST_RUN_SEND
- source_excerpt: `ST_RUN_SEND`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
ST_RUN_SEND
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-371"></a>
### VG098: FSM 状态必须能从复位初态到达且具有可证明的后继转移。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:86`
- Evidence:
- node_kind: `verilog_rtl`
- detail: ST_STATUS_SEND
- source_excerpt: `ST_STATUS_SEND`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
ST_STATUS_SEND
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-372"></a>
### VG098: FSM 状态必须能从复位初态到达且具有可证明的后继转移。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:75`
- Evidence:
- node_kind: `verilog_rtl`
- detail: ST_TABLE_DATA
- source_excerpt: `ST_TABLE_DATA`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
ST_TABLE_DATA
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-373"></a>
### VG098: FSM 状态必须能从复位初态到达且具有可证明的后继转移。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:76`
- Evidence:
- node_kind: `verilog_rtl`
- detail: ST_TABLE_WAIT
- source_excerpt: `ST_TABLE_WAIT`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
ST_TABLE_WAIT
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-374"></a>
### VG109: 组合逻辑 if 链缺少终止 else。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_low_io_physical_shell.v:321`
- Evidence:
- node_kind: `verilog_rtl`
- detail: if(flag_rx_transfer == 1'b1)
- source_excerpt: `if(flag_rx_transfer == 1'b1)`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
if(flag_rx_transfer == 1'b1)
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-375"></a>
### VG109: 组合逻辑 if 链缺少终止 else。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_low_io_physical_shell.v:334`
- Evidence:
- node_kind: `verilog_rtl`
- detail: if(flag_table_last_transfer == 1'b1)
- source_excerpt: `if(flag_table_last_transfer == 1'b1)`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
if(flag_table_last_transfer == 1'b1)
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-376"></a>
### VG109: 组合逻辑 if 链缺少终止 else。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_low_io_physical_shell.v:339`
- Evidence:
- node_kind: `verilog_rtl`
- detail: if(chain_table_loaded || chain_table_fault)
- source_excerpt: `if(chain_table_loaded || chain_table_fault)`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
if(chain_table_loaded || chain_table_fault)
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-377"></a>
### VG109: 组合逻辑 if 链缺少终止 else。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_low_io_physical_shell.v:344`
- Evidence:
- node_kind: `verilog_rtl`
- detail: if(flag_rx_transfer && (cnt_payload_word == 5'd21))
- source_excerpt: `if(flag_rx_transfer && (cnt_payload_word == 5'd21))`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
if(flag_rx_transfer && (cnt_payload_word == 5'd21))
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-378"></a>
### VG109: 组合逻辑 if 链缺少终止 else。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_low_io_physical_shell.v:352`
- Evidence:
- node_kind: `verilog_rtl`
- detail: if(flag_core_last_transfer == 1'b1)
- source_excerpt: `if(flag_core_last_transfer == 1'b1)`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
if(flag_core_last_transfer == 1'b1)
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-379"></a>
### VG109: 组合逻辑 if 链缺少终止 else。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_low_io_physical_shell.v:357`
- Evidence:
- node_kind: `verilog_rtl`
- detail: if(flag_core_busy_observed && chain_input_ready)
- source_excerpt: `if(flag_core_busy_observed && chain_input_ready)`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
if(flag_core_busy_observed && chain_input_ready)
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-380"></a>
### VG109: 组合逻辑 if 链缺少终止 else。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_low_io_physical_shell.v:362`
- Evidence:
- node_kind: `verilog_rtl`
- detail: if(flag_tx_transfer == 1'b1)
- source_excerpt: `if(flag_tx_transfer == 1'b1)`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
if(flag_tx_transfer == 1'b1)
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-381"></a>
### VG109: 组合逻辑 if 链缺少终止 else。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_low_io_physical_shell.v:367`
- Evidence:
- node_kind: `verilog_rtl`
- detail: if(flag_cache_request_transfer == 1'b1)
- source_excerpt: `if(flag_cache_request_transfer == 1'b1)`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
if(flag_cache_request_transfer == 1'b1)
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-382"></a>
### VG109: 组合逻辑 if 链缺少终止 else。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_low_io_physical_shell.v:372`
- Evidence:
- node_kind: `verilog_rtl`
- detail: if(flag_cache_result_transfer == 1'b1)
- source_excerpt: `if(flag_cache_result_transfer == 1'b1)`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
if(flag_cache_result_transfer == 1'b1)
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-383"></a>
### VG109: 组合逻辑 if 链缺少终止 else。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_low_io_physical_shell.v:362`
- Evidence:
- node_kind: `verilog_rtl`
- detail: if(flag_tx_transfer == 1'b1)
- source_excerpt: `if(flag_tx_transfer == 1'b1)`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
if(flag_tx_transfer == 1'b1)
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-384"></a>
### VG109: 组合逻辑 if 链缺少终止 else。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_low_io_physical_shell.v:362`
- Evidence:
- node_kind: `verilog_rtl`
- detail: if(flag_tx_transfer == 1'b1)
- source_excerpt: `if(flag_tx_transfer == 1'b1)`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
if(flag_tx_transfer == 1'b1)
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-385"></a>
### VG109: 组合逻辑 if 链缺少终止 else。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_low_io_physical_shell.v:387`
- Evidence:
- node_kind: `verilog_rtl`
- detail: if(flag_tx_transfer && (cnt_status_index == STATUS_LAST_INDEX))
- source_excerpt: `if(flag_tx_transfer && (cnt_status_index == STATUS_LAST_INDEX))`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
if(flag_tx_transfer && (cnt_status_index == STATUS_LAST_INDEX))
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-386"></a>
### VG109: 组合逻辑 if 链缺少终止 else。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_low_io_physical_shell.v:367`
- Evidence:
- node_kind: `verilog_rtl`
- detail: if(flag_cache_request_transfer == 1'b1)
- source_excerpt: `if(flag_cache_request_transfer == 1'b1)`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
if(flag_cache_request_transfer == 1'b1)
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-387"></a>
### VG109: 组合逻辑 if 链缺少终止 else。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_low_io_physical_shell.v:372`
- Evidence:
- node_kind: `verilog_rtl`
- detail: if(flag_cache_result_transfer == 1'b1)
- source_excerpt: `if(flag_cache_result_transfer == 1'b1)`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
if(flag_cache_result_transfer == 1'b1)
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-388"></a>
### VG109: 组合逻辑 if 链缺少终止 else。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_low_io_physical_shell.v:362`
- Evidence:
- node_kind: `verilog_rtl`
- detail: if(flag_tx_transfer == 1'b1)
- source_excerpt: `if(flag_tx_transfer == 1'b1)`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
if(flag_tx_transfer == 1'b1)
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-389"></a>
### VG110: 同一时序块中存在未统一复位的触发器目标。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:494`
- Evidence:
- node_kind: `verilog_rtl`
- detail: reg_activation_memory, reg_bias_memory, reg_first_memory, reg_last_memory, reg_mask_memory, reg_weight_memory
- source_excerpt: `reg_activation_memory, reg_bias_memory, reg_first_memory, reg_last_memory, reg_mask_memory, reg_weight_memory`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
reg_activation_memory, reg_bias_memory, reg_first_memory, reg_last_memory, reg_mask_memory, reg_weight_memory
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-390"></a>
### VG113: 同一时序块中存在未统一复位的触发器目标。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:494`
- Evidence:
- node_kind: `verilog_rtl`
- detail: reg_activation_memory, reg_bias_memory, reg_first_memory, reg_last_memory, reg_mask_memory, reg_weight_memory
- source_excerpt: `reg_activation_memory, reg_bias_memory, reg_first_memory, reg_last_memory, reg_mask_memory, reg_weight_memory`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
reg_activation_memory, reg_bias_memory, reg_first_memory, reg_last_memory, reg_mask_memory, reg_weight_memory
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-391"></a>
### VG122: 算术结果位宽超过赋值目标位宽。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:420`
- Evidence:
- node_kind: `verilog_rtl`
- detail: cnt_rx_words <= cnt_rx_words + 32'd1;
- source_excerpt: `cnt_rx_words <= cnt_rx_words + 32'd1;`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
cnt_rx_words <= cnt_rx_words + 32'd1;
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-392"></a>
### VG122: 算术结果位宽超过赋值目标位宽。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:423`
- Evidence:
- node_kind: `verilog_rtl`
- detail: cnt_tx_words <= cnt_tx_words + 32'd1;
- source_excerpt: `cnt_tx_words <= cnt_tx_words + 32'd1;`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
cnt_tx_words <= cnt_tx_words + 32'd1;
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-393"></a>
### VG122: 算术结果位宽超过赋值目标位宽。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:445`
- Evidence:
- node_kind: `verilog_rtl`
- detail: cnt_table_entry <= cnt_table_entry + 10'd1;
- source_excerpt: `cnt_table_entry <= cnt_table_entry + 10'd1;`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
cnt_table_entry <= cnt_table_entry + 10'd1;
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-394"></a>
### VG122: 算术结果位宽超过赋值目标位宽。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:468`
- Evidence:
- node_kind: `verilog_rtl`
- detail: cnt_payload_word <= cnt_payload_word + 5'd1;
- source_excerpt: `cnt_payload_word <= cnt_payload_word + 5'd1;`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
cnt_payload_word <= cnt_payload_word + 5'd1;
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-395"></a>
### VG122: 算术结果位宽超过赋值目标位宽。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:508`
- Evidence:
- node_kind: `verilog_rtl`
- detail: cnt_packet_loaded <= cnt_packet_loaded + 7'd1;
- source_excerpt: `cnt_packet_loaded <= cnt_packet_loaded + 7'd1;`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
cnt_packet_loaded <= cnt_packet_loaded + 7'd1;
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-396"></a>
### VG122: 算术结果位宽超过赋值目标位宽。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:510`
- Evidence:
- node_kind: `verilog_rtl`
- detail: cnt_position_loaded <= cnt_position_loaded + 3'd1;
- source_excerpt: `cnt_position_loaded <= cnt_position_loaded + 3'd1;`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
cnt_position_loaded <= cnt_position_loaded + 3'd1;
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-397"></a>
### VG122: 算术结果位宽超过赋值目标位宽。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:540`
- Evidence:
- node_kind: `verilog_rtl`
- detail: cnt_run_index <= cnt_run_index + 7'd1;
- source_excerpt: `cnt_run_index <= cnt_run_index + 7'd1;`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
cnt_run_index <= cnt_run_index + 7'd1;
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-398"></a>
### VG122: 算术结果位宽超过赋值目标位宽。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:541`
- Evidence:
- node_kind: `verilog_rtl`
- detail: cnt_core_inputs <= cnt_core_inputs + 32'd1;
- source_excerpt: `cnt_core_inputs <= cnt_core_inputs + 32'd1;`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
cnt_core_inputs <= cnt_core_inputs + 32'd1;
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-399"></a>
### VG122: 算术结果位宽超过赋值目标位宽。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:567`
- Evidence:
- node_kind: `verilog_rtl`
- detail: cnt_preload_cycles <= cnt_preload_cycles + 32'd1;
- source_excerpt: `cnt_preload_cycles <= cnt_preload_cycles + 32'd1;`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
cnt_preload_cycles <= cnt_preload_cycles + 32'd1;
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-400"></a>
### VG122: 算术结果位宽超过赋值目标位宽。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:570`
- Evidence:
- node_kind: `verilog_rtl`
- detail: cnt_preload_cycles <= cnt_preload_cycles + 32'd1;
- source_excerpt: `cnt_preload_cycles <= cnt_preload_cycles + 32'd1;`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
cnt_preload_cycles <= cnt_preload_cycles + 32'd1;
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-401"></a>
### VG122: 算术结果位宽超过赋值目标位宽。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:576`
- Evidence:
- node_kind: `verilog_rtl`
- detail: cnt_core_cycles <= cnt_core_cycles + 32'd1;
- source_excerpt: `cnt_core_cycles <= cnt_core_cycles + 32'd1;`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
cnt_core_cycles <= cnt_core_cycles + 32'd1;
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-402"></a>
### VG122: 算术结果位宽超过赋值目标位宽。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:585`
- Evidence:
- node_kind: `verilog_rtl`
- detail: cnt_export_cycles <= cnt_export_cycles + 32'd1;
- source_excerpt: `cnt_export_cycles <= cnt_export_cycles + 32'd1;`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
cnt_export_cycles <= cnt_export_cycles + 32'd1;
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-403"></a>
### VG122: 算术结果位宽超过赋值目标位宽。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:608`
- Evidence:
- node_kind: `verilog_rtl`
- detail: cnt_export_addr <= cnt_export_addr + 4'd1;
- source_excerpt: `cnt_export_addr <= cnt_export_addr + 4'd1;`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
cnt_export_addr <= cnt_export_addr + 4'd1;
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-404"></a>
### VG122: 算术结果位宽超过赋值目标位宽。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:614`
- Evidence:
- node_kind: `verilog_rtl`
- detail: cnt_result_outputs <= cnt_result_outputs + 32'd1;
- source_excerpt: `cnt_result_outputs <= cnt_result_outputs + 32'd1;`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
cnt_result_outputs <= cnt_result_outputs + 32'd1;
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-405"></a>
### VG122: 算术结果位宽超过赋值目标位宽。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:700`
- Evidence:
- node_kind: `verilog_rtl`
- detail: cnt_status_index <= cnt_status_index + 5'd1;
- source_excerpt: `cnt_status_index <= cnt_status_index + 5'd1;`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
cnt_status_index <= cnt_status_index + 5'd1;
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-406"></a>
### VG125: 字面量声明为 6 位，但实际值只需要 1 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:227`
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

<a id="vg-finding-407"></a>
### VG125: 字面量声明为 8 位，但实际值只需要 1 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:234`
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

<a id="vg-finding-408"></a>
### VG125: 字面量声明为 6 位，但实际值只需要 5 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:242`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 6'd24
- source_excerpt: `6'd24`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
6'd24
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-409"></a>
### VG125: 字面量声明为 9 位，但实际值只需要 8 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:242`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 9'd192
- source_excerpt: `9'd192`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
9'd192
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-410"></a>
### VG125: 字面量声明为 5 位，但实际值只需要 1 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:286`
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

<a id="vg-finding-411"></a>
### VG125: 字面量声明为 5 位，但实际值只需要 2 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:287`
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

<a id="vg-finding-412"></a>
### VG125: 字面量声明为 5 位，但实际值只需要 2 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:288`
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

<a id="vg-finding-413"></a>
### VG125: 字面量声明为 5 位，但实际值只需要 3 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:289`
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

<a id="vg-finding-414"></a>
### VG125: 字面量声明为 5 位，但实际值只需要 3 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:290`
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

<a id="vg-finding-415"></a>
### VG125: 字面量声明为 5 位，但实际值只需要 3 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:291`
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

<a id="vg-finding-416"></a>
### VG125: 字面量声明为 5 位，但实际值只需要 3 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:292`
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

<a id="vg-finding-417"></a>
### VG125: 字面量声明为 5 位，但实际值只需要 4 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:293`
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

<a id="vg-finding-418"></a>
### VG125: 字面量声明为 5 位，但实际值只需要 4 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:294`
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

<a id="vg-finding-419"></a>
### VG125: 字面量声明为 5 位，但实际值只需要 4 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:295`
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

<a id="vg-finding-420"></a>
### VG125: 字面量声明为 5 位，但实际值只需要 4 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:296`
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

<a id="vg-finding-421"></a>
### VG125: 字面量声明为 5 位，但实际值只需要 4 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:297`
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

<a id="vg-finding-422"></a>
### VG125: 字面量声明为 5 位，但实际值只需要 4 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:298`
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

<a id="vg-finding-423"></a>
### VG125: 字面量声明为 5 位，但实际值只需要 4 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:299`
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

<a id="vg-finding-424"></a>
### VG125: 字面量声明为 5 位，但实际值只需要 4 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:300`
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

<a id="vg-finding-425"></a>
### VG125: 字面量声明为 5 位，但实际值只需要 1 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:378`
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

<a id="vg-finding-426"></a>
### VG125: 字面量声明为 32 位，但实际值只需要 1 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:420`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 32'd1
- source_excerpt: `32'd1`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
32'd1
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-427"></a>
### VG125: 字面量声明为 32 位，但实际值只需要 1 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:423`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 32'd1
- source_excerpt: `32'd1`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
32'd1
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-428"></a>
### VG125: 字面量声明为 10 位，但实际值只需要 1 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:445`
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

<a id="vg-finding-429"></a>
### VG125: 字面量声明为 5 位，但实际值只需要 1 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:468`
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

<a id="vg-finding-430"></a>
### VG125: 字面量声明为 5 位，但实际值只需要 3 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:483`
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

<a id="vg-finding-431"></a>
### VG125: 字面量声明为 5 位，但实际值只需要 3 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:486`
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

<a id="vg-finding-432"></a>
### VG125: 字面量声明为 7 位，但实际值只需要 1 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:508`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 7'd1
- source_excerpt: `7'd1`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
7'd1
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-433"></a>
### VG125: 字面量声明为 3 位，但实际值只需要 1 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:510`
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

<a id="vg-finding-434"></a>
### VG125: 字面量声明为 7 位，但实际值只需要 1 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:540`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 7'd1
- source_excerpt: `7'd1`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
7'd1
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-435"></a>
### VG125: 字面量声明为 32 位，但实际值只需要 1 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:541`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 32'd1
- source_excerpt: `32'd1`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
32'd1
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-436"></a>
### VG125: 字面量声明为 32 位，但实际值只需要 1 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:567`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 32'd1
- source_excerpt: `32'd1`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
32'd1
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-437"></a>
### VG125: 字面量声明为 32 位，但实际值只需要 1 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:570`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 32'd1
- source_excerpt: `32'd1`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
32'd1
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-438"></a>
### VG125: 字面量声明为 32 位，但实际值只需要 1 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:576`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 32'd1
- source_excerpt: `32'd1`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
32'd1
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-439"></a>
### VG125: 字面量声明为 32 位，但实际值只需要 1 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:585`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 32'd1
- source_excerpt: `32'd1`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
32'd1
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-440"></a>
### VG125: 字面量声明为 5 位，但实际值只需要 1 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:587`
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

<a id="vg-finding-441"></a>
### VG125: 字面量声明为 4 位，但实际值只需要 1 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:608`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 4'd1
- source_excerpt: `4'd1`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
4'd1
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-442"></a>
### VG125: 字面量声明为 32 位，但实际值只需要 1 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:614`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 32'd1
- source_excerpt: `32'd1`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
32'd1
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-443"></a>
### VG125: 字面量声明为 6 位，但实际值只需要 5 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:631`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 6'd24
- source_excerpt: `6'd24`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
6'd24
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-444"></a>
### VG125: 字面量声明为 9 位，但实际值只需要 8 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:631`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 9'd192
- source_excerpt: `9'd192`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
9'd192
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-445"></a>
### VG125: 字面量声明为 5 位，但实际值只需要 1 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:700`
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

<a id="vg-finding-446"></a>
### VG125: 字面量声明为 5 位，但实际值只需要 1 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:719`
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

<a id="vg-finding-447"></a>
### VG125: 字面量声明为 5 位，但实际值只需要 1 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:733`
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

<a id="vg-finding-448"></a>
### VG125: 字面量声明为 5 位，但实际值只需要 2 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:734`
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

<a id="vg-finding-449"></a>
### VG125: 字面量声明为 5 位，但实际值只需要 2 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:735`
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

<a id="vg-finding-450"></a>
### VG125: 字面量声明为 5 位，但实际值只需要 3 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:736`
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

<a id="vg-finding-451"></a>
### VG125: 字面量声明为 5 位，但实际值只需要 3 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:737`
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

<a id="vg-finding-452"></a>
### VG125: 字面量声明为 5 位，但实际值只需要 3 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:738`
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

<a id="vg-finding-453"></a>
### VG125: 字面量声明为 5 位，但实际值只需要 3 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:739`
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

<a id="vg-finding-454"></a>
### VG125: 字面量声明为 5 位，但实际值只需要 4 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:740`
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

<a id="vg-finding-455"></a>
### VG125: 字面量声明为 5 位，但实际值只需要 4 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:741`
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

<a id="vg-finding-456"></a>
### VG125: 字面量声明为 5 位，但实际值只需要 4 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:742`
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

<a id="vg-finding-457"></a>
### VG125: 字面量声明为 5 位，但实际值只需要 4 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:743`
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

<a id="vg-finding-458"></a>
### VG125: 字面量声明为 5 位，但实际值只需要 4 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:744`
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

<a id="vg-finding-459"></a>
### VG125: 字面量声明为 5 位，但实际值只需要 4 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:745`
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

<a id="vg-finding-460"></a>
### VG125: 字面量声明为 5 位，但实际值只需要 4 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:746`
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

<a id="vg-finding-461"></a>
### VG125: 字面量声明为 5 位，但实际值只需要 4 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:747`
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

<a id="vg-finding-462"></a>
### VG132: 未登记原语或外部模块的时钟角色无法静态确定。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:762`
- Evidence:
- node_kind: `verilog_rtl`
- detail: road_onchip_chain road_onchip_chain_Inst_shell
- source_excerpt: `road_onchip_chain road_onchip_chain_Inst_shell`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
road_onchip_chain road_onchip_chain_Inst_shell
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-463"></a>
### VG142: wire 声明包含内联初始化赋值。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:247`
- Evidence:
- node_kind: `verilog_rtl`
- detail: chain_input_valid
- source_excerpt: `chain_input_valid`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
chain_input_valid
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-464"></a>
### VG142: wire 声明包含内联初始化赋值。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:248`
- Evidence:
- node_kind: `verilog_rtl`
- detail: chain_first
- source_excerpt: `chain_first`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
chain_first
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-465"></a>
### VG142: wire 声明包含内联初始化赋值。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:249`
- Evidence:
- node_kind: `verilog_rtl`
- detail: chain_last
- source_excerpt: `chain_last`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
chain_last
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-466"></a>
### VG142: wire 声明包含内联初始化赋值。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:250`
- Evidence:
- node_kind: `verilog_rtl`
- detail: chain_lane_mask
- source_excerpt: `chain_lane_mask`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
chain_lane_mask
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-467"></a>
### VG142: wire 声明包含内联初始化赋值。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:251`
- Evidence:
- node_kind: `verilog_rtl`
- detail: chain_activation_data
- source_excerpt: `chain_activation_data`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
chain_activation_data
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-468"></a>
### VG142: wire 声明包含内联初始化赋值。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:252`
- Evidence:
- node_kind: `verilog_rtl`
- detail: chain_weight_data
- source_excerpt: `chain_weight_data`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
chain_weight_data
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-469"></a>
### VG142: wire 声明包含内联初始化赋值。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:253`
- Evidence:
- node_kind: `verilog_rtl`
- detail: chain_bias_data
- source_excerpt: `chain_bias_data`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
chain_bias_data
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-470"></a>
### VG142: wire 声明包含内联初始化赋值。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:254`
- Evidence:
- node_kind: `verilog_rtl`
- detail: chain_table_valid
- source_excerpt: `chain_table_valid`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
chain_table_valid
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-471"></a>
### VG142: wire 声明包含内联初始化赋值。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:255`
- Evidence:
- node_kind: `verilog_rtl`
- detail: chain_table_addr
- source_excerpt: `chain_table_addr`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
chain_table_addr
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-472"></a>
### VG142: wire 声明包含内联初始化赋值。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:256`
- Evidence:
- node_kind: `verilog_rtl`
- detail: chain_table_data
- source_excerpt: `chain_table_data`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
chain_table_data
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-473"></a>
### VG142: wire 声明包含内联初始化赋值。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:257`
- Evidence:
- node_kind: `verilog_rtl`
- detail: chain_cache_read_valid
- source_excerpt: `chain_cache_read_valid`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
chain_cache_read_valid
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-474"></a>
### VG142: wire 声明包含内联初始化赋值。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:258`
- Evidence:
- node_kind: `verilog_rtl`
- detail: chain_cache_read_addr
- source_excerpt: `chain_cache_read_addr`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
chain_cache_read_addr
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-475"></a>
### VG142: wire 声明包含内联初始化赋值。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:259`
- Evidence:
- node_kind: `verilog_rtl`
- detail: chain_cache_result_ready
- source_excerpt: `chain_cache_result_ready`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
chain_cache_result_ready
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-476"></a>
### VG145: 组合逻辑完整依赖锥最多允许三个源信号，超限逻辑必须由时序 reg 隔断。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:283`
- Evidence:
- node_kind: `verilog_rtl`
- detail: dec_status_word: 26 sources: chain_fault, chain_table_fault, cnt_packet_loaded, cnt_position_loaded, cnt_status_index, cnt_table_entry, flag_run_complete, flag_run_issued, flag_shell_fault, flag_table_complete, reg_result_checksum, reg_shell_error, reg_snapshot_core[15:0], reg_snapshot_core[31:16], reg_snapshot_core_inputs[15:0], reg_snapshot_core_inputs[31:16], reg_snapshot_export[15:0], reg_snapshot_export[31:16], reg_snapshot_preload[15:0], reg_snapshot_preload[31:16], reg_snapshot_results[15:0], reg_snapshot_results[31:16], reg_snapshot_rx_words[15:0], reg_snapshot_rx_words[31:16], reg_snapshot_tx_words[15:0], reg_snapshot_tx_words[31:16]
- source_excerpt: `dec_status_word: 26 sources: chain_fault, chain_table_fault, cnt_packet_loaded, cnt_position_loaded, cnt_status_index, cnt_table_entry, flag_run_complete, flag_run_issued, flag_shell_fault, flag_table_complete, reg_result_checksum, reg_shell_error, reg_snapshot_core[15:0], reg_snapshot_core[31:16], reg_snapshot_core_inputs[15:0], reg_snapshot_core_inputs[31:16], reg_snapshot_export[15:0], reg_snapshot_export[31:16], reg_snapshot_preload[15:0], reg_snapshot_preload[31:16], reg_snapshot_results[15:0], reg_snapshot_results[31:16], reg_snapshot_rx_words[15:0], reg_snapshot_rx_words[31:16], reg_snapshot_tx_words[15:0], reg_snapshot_tx_words[31:16]`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
dec_status_word: 26 sources: chain_fault, chain_table_fault, cnt_packet_loaded, cnt_position_loaded, cnt_status_index, cnt_table_entry, flag_run_complete, flag_run_issued, flag_shell_fault, flag_table_complete, reg_result_checksum, reg_shell_error, reg_snapshot_core[15:0], reg_snapshot_core[31:16], reg_snapshot_core_inputs[15:0], reg_snapshot_core_inputs[31:16], reg_snapshot_export[15:0], reg_snapshot_export[31:16], reg_snapshot_preload[15:0], reg_snapshot_preload[31:16], reg_snapshot_results[15:0], reg_snapshot_results[31:16], reg_snapshot_rx_words[15:0], reg_snapshot_rx_words[31:16], reg_snapshot_tx_words[15:0], reg_snapshot_tx_words[31:16]
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-477"></a>
### VG145: 组合逻辑完整依赖锥最多允许三个源信号，超限逻辑必须由时序 reg 隔断。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:226`
- Evidence:
- node_kind: `verilog_rtl`
- detail: enc_packet_terms: 8 sources: reg_packet_mask[0], reg_packet_mask[1], reg_packet_mask[2], reg_packet_mask[3], reg_packet_mask[4], reg_packet_mask[5], reg_packet_mask[6], reg_packet_mask[7]
- source_excerpt: `enc_packet_terms: 8 sources: reg_packet_mask[0], reg_packet_mask[1], reg_packet_mask[2], reg_packet_mask[3], reg_packet_mask[4], reg_packet_mask[5], reg_packet_mask[6], reg_packet_mask[7]`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
enc_packet_terms: 8 sources: reg_packet_mask[0], reg_packet_mask[1], reg_packet_mask[2], reg_packet_mask[3], reg_packet_mask[4], reg_packet_mask[5], reg_packet_mask[6], reg_packet_mask[7]
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-478"></a>
### VG145: 组合逻辑完整依赖锥最多允许三个源信号，超限逻辑必须由时序 reg 隔断。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:234`
- Evidence:
- node_kind: `verilog_rtl`
- detail: flag_core_last_transfer: 4 sources: chain_input_ready, cnt_run_index, reg_run_packet_count, state_current
- source_excerpt: `flag_core_last_transfer: 4 sources: chain_input_ready, cnt_run_index, reg_run_packet_count, state_current`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
flag_core_last_transfer: 4 sources: chain_input_ready, cnt_run_index, reg_run_packet_count, state_current
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-479"></a>
### VG145: 组合逻辑完整依赖锥最多允许三个源信号，超限逻辑必须由时序 reg 隔断。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:242`
- Evidence:
- node_kind: `verilog_rtl`
- detail: flag_packet_commit_legal: 15 sources: cnt_group_position, cnt_packet_loaded, cnt_position_loaded, cnt_term_position, flag_position_open, reg_packet_first, reg_packet_header_legal, reg_packet_mask[0], reg_packet_mask[1], reg_packet_mask[2], reg_packet_mask[3], reg_packet_mask[4], reg_packet_mask[5], reg_packet_mask[6], reg_packet_mask[7]
- source_excerpt: `flag_packet_commit_legal: 15 sources: cnt_group_position, cnt_packet_loaded, cnt_position_loaded, cnt_term_position, flag_position_open, reg_packet_first, reg_packet_header_legal, reg_packet_mask[0], reg_packet_mask[1], reg_packet_mask[2], reg_packet_mask[3], reg_packet_mask[4], reg_packet_mask[5], reg_packet_mask[6], reg_packet_mask[7]`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
flag_packet_commit_legal: 15 sources: cnt_group_position, cnt_packet_loaded, cnt_position_loaded, cnt_term_position, flag_position_open, reg_packet_first, reg_packet_header_legal, reg_packet_mask[0], reg_packet_mask[1], reg_packet_mask[2], reg_packet_mask[3], reg_packet_mask[4], reg_packet_mask[5], reg_packet_mask[6], reg_packet_mask[7]
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-480"></a>
### VG145: 组合逻辑完整依赖锥最多允许三个源信号，超限逻辑必须由时序 reg 隔断。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:241`
- Evidence:
- node_kind: `verilog_rtl`
- detail: flag_run_command_legal: 8 sources: cnt_packet_loaded, cnt_position_loaded, flag_position_open, flag_run_issued, flag_shell_fault, flag_table_complete, i_rx_data[11:7], i_rx_data[6:0]
- source_excerpt: `flag_run_command_legal: 8 sources: cnt_packet_loaded, cnt_position_loaded, flag_position_open, flag_run_issued, flag_shell_fault, flag_table_complete, i_rx_data[11:7], i_rx_data[6:0]`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
flag_run_command_legal: 8 sources: cnt_packet_loaded, cnt_position_loaded, flag_position_open, flag_run_issued, flag_shell_fault, flag_table_complete, i_rx_data[11:7], i_rx_data[6:0]
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-481"></a>
### VG145: 组合逻辑完整依赖锥最多允许三个源信号，超限逻辑必须由时序 reg 隔断。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:224`
- Evidence:
- node_kind: `verilog_rtl`
- detail: flag_rx_transfer: 4 sources: i_rx_valid, reg_table_pending_valid, state_current, tx_valid_o
- source_excerpt: `flag_rx_transfer: 4 sources: i_rx_valid, reg_table_pending_valid, state_current, tx_valid_o`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
flag_rx_transfer: 4 sources: i_rx_valid, reg_table_pending_valid, state_current, tx_valid_o
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-482"></a>
### VG145: 组合逻辑完整依赖锥最多允许三个源信号，超限逻辑必须由时序 reg 隔断。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:228`
- Evidence:
- node_kind: `verilog_rtl`
- detail: next_term_count: 9 sources: cnt_term_position, reg_packet_mask[0], reg_packet_mask[1], reg_packet_mask[2], reg_packet_mask[3], reg_packet_mask[4], reg_packet_mask[5], reg_packet_mask[6], reg_packet_mask[7]
- source_excerpt: `next_term_count: 9 sources: cnt_term_position, reg_packet_mask[0], reg_packet_mask[1], reg_packet_mask[2], reg_packet_mask[3], reg_packet_mask[4], reg_packet_mask[5], reg_packet_mask[6], reg_packet_mask[7]`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
next_term_count: 9 sources: cnt_term_position, reg_packet_mask[0], reg_packet_mask[1], reg_packet_mask[2], reg_packet_mask[3], reg_packet_mask[4], reg_packet_mask[5], reg_packet_mask[6], reg_packet_mask[7]
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-483"></a>
### VG145: 组合逻辑完整依赖锥最多允许三个源信号，超限逻辑必须由时序 reg 隔断。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:317`
- Evidence:
- node_kind: `verilog_rtl`
- detail: state_next: 31 sources: chain_cache_read_ready, chain_cache_result_valid, chain_input_ready, chain_table_fault, chain_table_loaded, chain_table_ready, cnt_export_addr, cnt_packet_loaded, cnt_payload_word, cnt_position_loaded, cnt_run_index, cnt_status_index, cnt_table_entry, flag_core_busy_observed, flag_position_open, flag_run_complete, flag_run_issued, flag_shell_fault, flag_table_complete, i_rx_data[11:0], i_rx_data[11:4], i_rx_data[11:7], i_rx_data[15:12], i_rx_data[6:0], i_rx_valid, i_tx_ready, reg_export_count, reg_run_packet_count, reg_table_pending_valid, state_current, tx_valid_o
- source_excerpt: `state_next: 31 sources: chain_cache_read_ready, chain_cache_result_valid, chain_input_ready, chain_table_fault, chain_table_loaded, chain_table_ready, cnt_export_addr, cnt_packet_loaded, cnt_payload_word, cnt_position_loaded, cnt_run_index, cnt_status_index, cnt_table_entry, flag_core_busy_observed, flag_position_open, flag_run_complete, flag_run_issued, flag_shell_fault, flag_table_complete, i_rx_data[11:0], i_rx_data[11:4], i_rx_data[11:7], i_rx_data[15:12], i_rx_data[6:0], i_rx_valid, i_tx_ready, reg_export_count, reg_run_packet_count, reg_table_pending_valid, state_current, tx_valid_o`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
state_next: 31 sources: chain_cache_read_ready, chain_cache_result_valid, chain_input_ready, chain_table_fault, chain_table_loaded, chain_table_ready, cnt_export_addr, cnt_packet_loaded, cnt_payload_word, cnt_position_loaded, cnt_run_index, cnt_status_index, cnt_table_entry, flag_core_busy_observed, flag_position_open, flag_run_complete, flag_run_issued, flag_shell_fault, flag_table_complete, i_rx_data[11:0], i_rx_data[11:4], i_rx_data[11:7], i_rx_data[15:12], i_rx_data[6:0], i_rx_valid, i_tx_ready, reg_export_count, reg_run_packet_count, reg_table_pending_valid, state_current, tx_valid_o
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
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_activation_data; child_output=road_low_io_physical_shell.chain_activation_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_activation_data; child_output=road_low_io_physical_shell.chain_activation_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_activation_data; child_output=road_low_io_physical_shell.chain_activation_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-485"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_bias_data; child_output=road_low_io_physical_shell.chain_bias_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_bias_data; child_output=road_low_io_physical_shell.chain_bias_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_bias_data; child_output=road_low_io_physical_shell.chain_bias_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-486"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_cache_read_addr; child_output=road_low_io_physical_shell.chain_cache_read_addr; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_cache_read_addr; child_output=road_low_io_physical_shell.chain_cache_read_addr; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_cache_read_addr; child_output=road_low_io_physical_shell.chain_cache_read_addr; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
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
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_cache_read_ready; child_output=road_low_io_physical_shell.chain_cache_read_ready; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_cache_read_ready; child_output=road_low_io_physical_shell.chain_cache_read_ready; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_cache_read_ready; child_output=road_low_io_physical_shell.chain_cache_read_ready; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-488"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_cache_read_valid; child_output=road_low_io_physical_shell.chain_cache_read_valid; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_cache_read_valid; child_output=road_low_io_physical_shell.chain_cache_read_valid; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_cache_read_valid; child_output=road_low_io_physical_shell.chain_cache_read_valid; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
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
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_cache_result_data; child_output=road_low_io_physical_shell.chain_cache_result_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_cache_result_data; child_output=road_low_io_physical_shell.chain_cache_result_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_cache_result_data; child_output=road_low_io_physical_shell.chain_cache_result_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
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
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_cache_result_fault; child_output=road_low_io_physical_shell.chain_cache_result_fault; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_cache_result_fault; child_output=road_low_io_physical_shell.chain_cache_result_fault; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_cache_result_fault; child_output=road_low_io_physical_shell.chain_cache_result_fault; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
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
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_cache_result_ready; child_output=road_low_io_physical_shell.chain_cache_result_ready; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_cache_result_ready; child_output=road_low_io_physical_shell.chain_cache_result_ready; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_cache_result_ready; child_output=road_low_io_physical_shell.chain_cache_result_ready; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
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
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_cache_result_valid; child_output=road_low_io_physical_shell.chain_cache_result_valid; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_cache_result_valid; child_output=road_low_io_physical_shell.chain_cache_result_valid; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_cache_result_valid; child_output=road_low_io_physical_shell.chain_cache_result_valid; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
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
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_fault; child_output=road_low_io_physical_shell.chain_fault; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_fault; child_output=road_low_io_physical_shell.chain_fault; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_fault; child_output=road_low_io_physical_shell.chain_fault; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
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
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_first; child_output=road_low_io_physical_shell.chain_first; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_first; child_output=road_low_io_physical_shell.chain_first; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_first; child_output=road_low_io_physical_shell.chain_first; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
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
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_input_ready; child_output=road_low_io_physical_shell.chain_input_ready; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_input_ready; child_output=road_low_io_physical_shell.chain_input_ready; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_input_ready; child_output=road_low_io_physical_shell.chain_input_ready; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
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
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_input_valid; child_output=road_low_io_physical_shell.chain_input_valid; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_input_valid; child_output=road_low_io_physical_shell.chain_input_valid; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_input_valid; child_output=road_low_io_physical_shell.chain_input_valid; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
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
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_lane_mask; child_output=road_low_io_physical_shell.chain_lane_mask; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_lane_mask; child_output=road_low_io_physical_shell.chain_lane_mask; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_lane_mask; child_output=road_low_io_physical_shell.chain_lane_mask; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
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
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_last; child_output=road_low_io_physical_shell.chain_last; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_last; child_output=road_low_io_physical_shell.chain_last; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_last; child_output=road_low_io_physical_shell.chain_last; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
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
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_table_addr; child_output=road_low_io_physical_shell.chain_table_addr; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_table_addr; child_output=road_low_io_physical_shell.chain_table_addr; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_table_addr; child_output=road_low_io_physical_shell.chain_table_addr; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
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
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_table_data; child_output=road_low_io_physical_shell.chain_table_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_table_data; child_output=road_low_io_physical_shell.chain_table_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_table_data; child_output=road_low_io_physical_shell.chain_table_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
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
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_table_fault; child_output=road_low_io_physical_shell.chain_table_fault; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_table_fault; child_output=road_low_io_physical_shell.chain_table_fault; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_table_fault; child_output=road_low_io_physical_shell.chain_table_fault; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
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
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_table_loaded; child_output=road_low_io_physical_shell.chain_table_loaded; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_table_loaded; child_output=road_low_io_physical_shell.chain_table_loaded; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_table_loaded; child_output=road_low_io_physical_shell.chain_table_loaded; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
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
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_table_ready; child_output=road_low_io_physical_shell.chain_table_ready; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_table_ready; child_output=road_low_io_physical_shell.chain_table_ready; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_table_ready; child_output=road_low_io_physical_shell.chain_table_ready; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
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
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_table_valid; child_output=road_low_io_physical_shell.chain_table_valid; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_table_valid; child_output=road_low_io_physical_shell.chain_table_valid; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_table_valid; child_output=road_low_io_physical_shell.chain_table_valid; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
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
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_weight_data; child_output=road_low_io_physical_shell.chain_weight_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_weight_data; child_output=road_low_io_physical_shell.chain_weight_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_weight_data; child_output=road_low_io_physical_shell.chain_weight_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-506"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=cnt_core_cycles$enable; child_output=road_low_io_physical_shell.cnt_core_cycles$enable; operation_count=38; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=cnt_core_cycles$enable; child_output=road_low_io_physical_shell.cnt_core_cycles$enable; operation_count=38; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=cnt_core_cycles$enable; child_output=road_low_io_physical_shell.cnt_core_cycles$enable; operation_count=38; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-507"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=cnt_core_inputs$enable; child_output=road_low_io_physical_shell.cnt_core_inputs$enable; operation_count=26; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=cnt_core_inputs$enable; child_output=road_low_io_physical_shell.cnt_core_inputs$enable; operation_count=26; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=cnt_core_inputs$enable; child_output=road_low_io_physical_shell.cnt_core_inputs$enable; operation_count=26; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-508"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=cnt_export_addr$enable; child_output=road_low_io_physical_shell.cnt_export_addr$enable; operation_count=17; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=cnt_export_addr$enable; child_output=road_low_io_physical_shell.cnt_export_addr$enable; operation_count=17; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=cnt_export_addr$enable; child_output=road_low_io_physical_shell.cnt_export_addr$enable; operation_count=17; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-509"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=cnt_export_cycles$enable; child_output=road_low_io_physical_shell.cnt_export_cycles$enable; operation_count=14; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=cnt_export_cycles$enable; child_output=road_low_io_physical_shell.cnt_export_cycles$enable; operation_count=14; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=cnt_export_cycles$enable; child_output=road_low_io_physical_shell.cnt_export_cycles$enable; operation_count=14; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-510"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=cnt_group_position$enable; child_output=road_low_io_physical_shell.cnt_group_position$enable; operation_count=26; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=cnt_group_position$enable; child_output=road_low_io_physical_shell.cnt_group_position$enable; operation_count=26; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=cnt_group_position$enable; child_output=road_low_io_physical_shell.cnt_group_position$enable; operation_count=26; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-511"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=cnt_packet_loaded$enable; child_output=road_low_io_physical_shell.cnt_packet_loaded$enable; operation_count=26; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=cnt_packet_loaded$enable; child_output=road_low_io_physical_shell.cnt_packet_loaded$enable; operation_count=26; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=cnt_packet_loaded$enable; child_output=road_low_io_physical_shell.cnt_packet_loaded$enable; operation_count=26; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-512"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=cnt_payload_word$enable; child_output=road_low_io_physical_shell.cnt_payload_word$enable; operation_count=16; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=cnt_payload_word$enable; child_output=road_low_io_physical_shell.cnt_payload_word$enable; operation_count=16; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=cnt_payload_word$enable; child_output=road_low_io_physical_shell.cnt_payload_word$enable; operation_count=16; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-513"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=cnt_position_loaded$enable; child_output=road_low_io_physical_shell.cnt_position_loaded$enable; operation_count=26; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=cnt_position_loaded$enable; child_output=road_low_io_physical_shell.cnt_position_loaded$enable; operation_count=26; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=cnt_position_loaded$enable; child_output=road_low_io_physical_shell.cnt_position_loaded$enable; operation_count=26; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-514"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=cnt_preload_cycles$enable; child_output=road_low_io_physical_shell.cnt_preload_cycles$enable; operation_count=34; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=cnt_preload_cycles$enable; child_output=road_low_io_physical_shell.cnt_preload_cycles$enable; operation_count=34; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=cnt_preload_cycles$enable; child_output=road_low_io_physical_shell.cnt_preload_cycles$enable; operation_count=34; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-515"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=cnt_result_outputs$enable; child_output=road_low_io_physical_shell.cnt_result_outputs$enable; operation_count=22; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=cnt_result_outputs$enable; child_output=road_low_io_physical_shell.cnt_result_outputs$enable; operation_count=22; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=cnt_result_outputs$enable; child_output=road_low_io_physical_shell.cnt_result_outputs$enable; operation_count=22; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-516"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=cnt_run_index$enable; child_output=road_low_io_physical_shell.cnt_run_index$enable; operation_count=26; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=cnt_run_index$enable; child_output=road_low_io_physical_shell.cnt_run_index$enable; operation_count=26; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=cnt_run_index$enable; child_output=road_low_io_physical_shell.cnt_run_index$enable; operation_count=26; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-517"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=cnt_rx_words$enable; child_output=road_low_io_physical_shell.cnt_rx_words$enable; operation_count=5; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=cnt_rx_words$enable; child_output=road_low_io_physical_shell.cnt_rx_words$enable; operation_count=5; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=cnt_rx_words$enable; child_output=road_low_io_physical_shell.cnt_rx_words$enable; operation_count=5; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-518"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=cnt_status_index$enable; child_output=road_low_io_physical_shell.cnt_status_index$enable; operation_count=12; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=cnt_status_index$enable; child_output=road_low_io_physical_shell.cnt_status_index$enable; operation_count=12; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=cnt_status_index$enable; child_output=road_low_io_physical_shell.cnt_status_index$enable; operation_count=12; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-519"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=cnt_table_entry$enable; child_output=road_low_io_physical_shell.cnt_table_entry$enable; operation_count=12; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=cnt_table_entry$enable; child_output=road_low_io_physical_shell.cnt_table_entry$enable; operation_count=12; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=cnt_table_entry$enable; child_output=road_low_io_physical_shell.cnt_table_entry$enable; operation_count=12; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-520"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=cnt_term_position$enable; child_output=road_low_io_physical_shell.cnt_term_position$enable; operation_count=26; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=cnt_term_position$enable; child_output=road_low_io_physical_shell.cnt_term_position$enable; operation_count=26; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=cnt_term_position$enable; child_output=road_low_io_physical_shell.cnt_term_position$enable; operation_count=26; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-521"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=flag_core_busy_observed$enable; child_output=road_low_io_physical_shell.flag_core_busy_observed$enable; operation_count=27; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=flag_core_busy_observed$enable; child_output=road_low_io_physical_shell.flag_core_busy_observed$enable; operation_count=27; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=flag_core_busy_observed$enable; child_output=road_low_io_physical_shell.flag_core_busy_observed$enable; operation_count=27; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-522"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=flag_core_timing_active$enable; child_output=road_low_io_physical_shell.flag_core_timing_active$enable; operation_count=7; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=flag_core_timing_active$enable; child_output=road_low_io_physical_shell.flag_core_timing_active$enable; operation_count=7; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=flag_core_timing_active$enable; child_output=road_low_io_physical_shell.flag_core_timing_active$enable; operation_count=7; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-523"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=flag_export_timing_active$enable; child_output=road_low_io_physical_shell.flag_export_timing_active$enable; operation_count=20; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=flag_export_timing_active$enable; child_output=road_low_io_physical_shell.flag_export_timing_active$enable; operation_count=20; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=flag_export_timing_active$enable; child_output=road_low_io_physical_shell.flag_export_timing_active$enable; operation_count=20; limit=3; inconclusive_reason=none; loop_presence=absent
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
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=flag_position_open$enable; child_output=road_low_io_physical_shell.flag_position_open$enable; operation_count=26; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=flag_position_open$enable; child_output=road_low_io_physical_shell.flag_position_open$enable; operation_count=26; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=flag_position_open$enable; child_output=road_low_io_physical_shell.flag_position_open$enable; operation_count=26; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-525"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=flag_preload_active$enable; child_output=road_low_io_physical_shell.flag_preload_active$enable; operation_count=34; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=flag_preload_active$enable; child_output=road_low_io_physical_shell.flag_preload_active$enable; operation_count=34; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=flag_preload_active$enable; child_output=road_low_io_physical_shell.flag_preload_active$enable; operation_count=34; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-526"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=flag_run_complete$enable; child_output=road_low_io_physical_shell.flag_run_complete$enable; operation_count=27; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=flag_run_complete$enable; child_output=road_low_io_physical_shell.flag_run_complete$enable; operation_count=27; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=flag_run_complete$enable; child_output=road_low_io_physical_shell.flag_run_complete$enable; operation_count=27; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-527"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=flag_run_issued$enable; child_output=road_low_io_physical_shell.flag_run_issued$enable; operation_count=24; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=flag_run_issued$enable; child_output=road_low_io_physical_shell.flag_run_issued$enable; operation_count=24; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=flag_run_issued$enable; child_output=road_low_io_physical_shell.flag_run_issued$enable; operation_count=24; limit=3; inconclusive_reason=none; loop_presence=absent
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
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=flag_shell_fault$enable; child_output=road_low_io_physical_shell.flag_shell_fault$enable; operation_count=65; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=flag_shell_fault$enable; child_output=road_low_io_physical_shell.flag_shell_fault$enable; operation_count=65; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=flag_shell_fault$enable; child_output=road_low_io_physical_shell.flag_shell_fault$enable; operation_count=65; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
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
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=flag_table_complete$enable; child_output=road_low_io_physical_shell.flag_table_complete$enable; operation_count=13; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=flag_table_complete$enable; child_output=road_low_io_physical_shell.flag_table_complete$enable; operation_count=13; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=flag_table_complete$enable; child_output=road_low_io_physical_shell.flag_table_complete$enable; operation_count=13; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
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
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_activation_memory[cnt_packet_loaded]$D; child_output=road_low_io_physical_shell.reg_activation_memory[cnt_packet_loaded]$D; operation_count=0; limit=3; inconclusive_reason=reg_activation_memory[cnt_packet_loaded]$D: missing storage data expression; loop_presence=absent
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_activation_memory[cnt_packet_loaded]$D; child_output=road_low_io_physical_shell.reg_activation_memory[cnt_packet_loaded]$D; operation_count=0; limit=3; inconclusive_reason=reg_activation_memory[cnt_packet_loaded]$D: missing storage data expression; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_activation_memory[cnt_packet_loaded]$D; child_output=road_low_io_physical_shell.reg_activation_memory[cnt_packet_loaded]$D; operation_count=0; limit=3; inconclusive_reason=reg_activation_memory[cnt_packet_loaded]$D: missing storage data expression; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-531"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_activation_memory[cnt_packet_loaded]$enable; child_output=road_low_io_physical_shell.reg_activation_memory[cnt_packet_loaded]$enable; operation_count=26; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_activation_memory[cnt_packet_loaded]$enable; child_output=road_low_io_physical_shell.reg_activation_memory[cnt_packet_loaded]$enable; operation_count=26; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_activation_memory[cnt_packet_loaded]$enable; child_output=road_low_io_physical_shell.reg_activation_memory[cnt_packet_loaded]$enable; operation_count=26; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-532"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_bias_memory[cnt_packet_loaded]$D; child_output=road_low_io_physical_shell.reg_bias_memory[cnt_packet_loaded]$D; operation_count=0; limit=3; inconclusive_reason=reg_bias_memory[cnt_packet_loaded]$D: missing storage data expression; loop_presence=absent
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_bias_memory[cnt_packet_loaded]$D; child_output=road_low_io_physical_shell.reg_bias_memory[cnt_packet_loaded]$D; operation_count=0; limit=3; inconclusive_reason=reg_bias_memory[cnt_packet_loaded]$D: missing storage data expression; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_bias_memory[cnt_packet_loaded]$D; child_output=road_low_io_physical_shell.reg_bias_memory[cnt_packet_loaded]$D; operation_count=0; limit=3; inconclusive_reason=reg_bias_memory[cnt_packet_loaded]$D: missing storage data expression; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-533"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_bias_memory[cnt_packet_loaded]$enable; child_output=road_low_io_physical_shell.reg_bias_memory[cnt_packet_loaded]$enable; operation_count=26; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_bias_memory[cnt_packet_loaded]$enable; child_output=road_low_io_physical_shell.reg_bias_memory[cnt_packet_loaded]$enable; operation_count=26; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_bias_memory[cnt_packet_loaded]$enable; child_output=road_low_io_physical_shell.reg_bias_memory[cnt_packet_loaded]$enable; operation_count=26; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-534"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_diagnostic_addr$enable; child_output=road_low_io_physical_shell.reg_diagnostic_addr$enable; operation_count=11; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_diagnostic_addr$enable; child_output=road_low_io_physical_shell.reg_diagnostic_addr$enable; operation_count=11; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_diagnostic_addr$enable; child_output=road_low_io_physical_shell.reg_diagnostic_addr$enable; operation_count=11; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-535"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_export_count$enable; child_output=road_low_io_physical_shell.reg_export_count$enable; operation_count=14; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_export_count$enable; child_output=road_low_io_physical_shell.reg_export_count$enable; operation_count=14; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_export_count$enable; child_output=road_low_io_physical_shell.reg_export_count$enable; operation_count=14; limit=3; inconclusive_reason=none; loop_presence=absent
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
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_first_memory[cnt_packet_loaded]$D; child_output=road_low_io_physical_shell.reg_first_memory[cnt_packet_loaded]$D; operation_count=0; limit=3; inconclusive_reason=reg_first_memory[cnt_packet_loaded]$D: missing storage data expression; loop_presence=absent
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_first_memory[cnt_packet_loaded]$D; child_output=road_low_io_physical_shell.reg_first_memory[cnt_packet_loaded]$D; operation_count=0; limit=3; inconclusive_reason=reg_first_memory[cnt_packet_loaded]$D: missing storage data expression; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_first_memory[cnt_packet_loaded]$D; child_output=road_low_io_physical_shell.reg_first_memory[cnt_packet_loaded]$D; operation_count=0; limit=3; inconclusive_reason=reg_first_memory[cnt_packet_loaded]$D: missing storage data expression; loop_presence=absent
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
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_first_memory[cnt_packet_loaded]$enable; child_output=road_low_io_physical_shell.reg_first_memory[cnt_packet_loaded]$enable; operation_count=26; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_first_memory[cnt_packet_loaded]$enable; child_output=road_low_io_physical_shell.reg_first_memory[cnt_packet_loaded]$enable; operation_count=26; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_first_memory[cnt_packet_loaded]$enable; child_output=road_low_io_physical_shell.reg_first_memory[cnt_packet_loaded]$enable; operation_count=26; limit=3; inconclusive_reason=none; loop_presence=absent
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
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_last_memory[cnt_packet_loaded]$D; child_output=road_low_io_physical_shell.reg_last_memory[cnt_packet_loaded]$D; operation_count=0; limit=3; inconclusive_reason=reg_last_memory[cnt_packet_loaded]$D: missing storage data expression; loop_presence=absent
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_last_memory[cnt_packet_loaded]$D; child_output=road_low_io_physical_shell.reg_last_memory[cnt_packet_loaded]$D; operation_count=0; limit=3; inconclusive_reason=reg_last_memory[cnt_packet_loaded]$D: missing storage data expression; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_last_memory[cnt_packet_loaded]$D; child_output=road_low_io_physical_shell.reg_last_memory[cnt_packet_loaded]$D; operation_count=0; limit=3; inconclusive_reason=reg_last_memory[cnt_packet_loaded]$D: missing storage data expression; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-539"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_last_memory[cnt_packet_loaded]$enable; child_output=road_low_io_physical_shell.reg_last_memory[cnt_packet_loaded]$enable; operation_count=26; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_last_memory[cnt_packet_loaded]$enable; child_output=road_low_io_physical_shell.reg_last_memory[cnt_packet_loaded]$enable; operation_count=26; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_last_memory[cnt_packet_loaded]$enable; child_output=road_low_io_physical_shell.reg_last_memory[cnt_packet_loaded]$enable; operation_count=26; limit=3; inconclusive_reason=none; loop_presence=absent
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
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_mask_memory[cnt_packet_loaded]$D; child_output=road_low_io_physical_shell.reg_mask_memory[cnt_packet_loaded]$D; operation_count=0; limit=3; inconclusive_reason=reg_mask_memory[cnt_packet_loaded]$D: missing storage data expression; loop_presence=absent
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_mask_memory[cnt_packet_loaded]$D; child_output=road_low_io_physical_shell.reg_mask_memory[cnt_packet_loaded]$D; operation_count=0; limit=3; inconclusive_reason=reg_mask_memory[cnt_packet_loaded]$D: missing storage data expression; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_mask_memory[cnt_packet_loaded]$D; child_output=road_low_io_physical_shell.reg_mask_memory[cnt_packet_loaded]$D; operation_count=0; limit=3; inconclusive_reason=reg_mask_memory[cnt_packet_loaded]$D: missing storage data expression; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-541"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_mask_memory[cnt_packet_loaded]$enable; child_output=road_low_io_physical_shell.reg_mask_memory[cnt_packet_loaded]$enable; operation_count=26; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_mask_memory[cnt_packet_loaded]$enable; child_output=road_low_io_physical_shell.reg_mask_memory[cnt_packet_loaded]$enable; operation_count=26; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_mask_memory[cnt_packet_loaded]$enable; child_output=road_low_io_physical_shell.reg_mask_memory[cnt_packet_loaded]$enable; operation_count=26; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-542"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_packet_activation$enable; child_output=road_low_io_physical_shell.reg_packet_activation$enable; operation_count=9; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_packet_activation$enable; child_output=road_low_io_physical_shell.reg_packet_activation$enable; operation_count=9; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_packet_activation$enable; child_output=road_low_io_physical_shell.reg_packet_activation$enable; operation_count=9; limit=3; inconclusive_reason=none; loop_presence=absent
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
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_packet_activation[cnt_payload_word*16+:16]$D; child_output=road_low_io_physical_shell.reg_packet_activation[cnt_payload_word*16+:16]$D; operation_count=0; limit=3; inconclusive_reason=reg_packet_activation[cnt_payload_word*16+:16]$D: missing storage data expression; loop_presence=absent
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_packet_activation[cnt_payload_word*16+:16]$D; child_output=road_low_io_physical_shell.reg_packet_activation[cnt_payload_word*16+:16]$D; operation_count=0; limit=3; inconclusive_reason=reg_packet_activation[cnt_payload_word*16+:16]$D: missing storage data expression; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_packet_activation[cnt_payload_word*16+:16]$D; child_output=road_low_io_physical_shell.reg_packet_activation[cnt_payload_word*16+:16]$D; operation_count=0; limit=3; inconclusive_reason=reg_packet_activation[cnt_payload_word*16+:16]$D: missing storage data expression; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-544"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_packet_activation[cnt_payload_word*16+:16]$enable; child_output=road_low_io_physical_shell.reg_packet_activation[cnt_payload_word*16+:16]$enable; operation_count=12; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_packet_activation[cnt_payload_word*16+:16]$enable; child_output=road_low_io_physical_shell.reg_packet_activation[cnt_payload_word*16+:16]$enable; operation_count=12; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_packet_activation[cnt_payload_word*16+:16]$enable; child_output=road_low_io_physical_shell.reg_packet_activation[cnt_payload_word*16+:16]$enable; operation_count=12; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-545"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_packet_bias$enable; child_output=road_low_io_physical_shell.reg_packet_bias$enable; operation_count=9; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_packet_bias$enable; child_output=road_low_io_physical_shell.reg_packet_bias$enable; operation_count=9; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_packet_bias$enable; child_output=road_low_io_physical_shell.reg_packet_bias$enable; operation_count=9; limit=3; inconclusive_reason=none; loop_presence=absent
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
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_packet_bias[(cnt_payload_word-5'd16)*16+:16]$D; child_output=road_low_io_physical_shell.reg_packet_bias[(cnt_payload_word-5'd16)*16+:16]$D; operation_count=0; limit=3; inconclusive_reason=reg_packet_bias[(cnt_payload_word-5'd16)*16+:16]$D: missing storage data expression; loop_presence=absent
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_packet_bias[(cnt_payload_word-5'd16)*16+:16]$D; child_output=road_low_io_physical_shell.reg_packet_bias[(cnt_payload_word-5'd16)*16+:16]$D; operation_count=0; limit=3; inconclusive_reason=reg_packet_bias[(cnt_payload_word-5'd16)*16+:16]$D: missing storage data expression; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_packet_bias[(cnt_payload_word-5'd16)*16+:16]$D; child_output=road_low_io_physical_shell.reg_packet_bias[(cnt_payload_word-5'd16)*16+:16]$D; operation_count=0; limit=3; inconclusive_reason=reg_packet_bias[(cnt_payload_word-5'd16)*16+:16]$D: missing storage data expression; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-547"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_packet_bias[(cnt_payload_word-5'd16)*16+:16]$enable; child_output=road_low_io_physical_shell.reg_packet_bias[(cnt_payload_word-5'd16)*16+:16]$enable; operation_count=13; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_packet_bias[(cnt_payload_word-5'd16)*16+:16]$enable; child_output=road_low_io_physical_shell.reg_packet_bias[(cnt_payload_word-5'd16)*16+:16]$enable; operation_count=13; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_packet_bias[(cnt_payload_word-5'd16)*16+:16]$enable; child_output=road_low_io_physical_shell.reg_packet_bias[(cnt_payload_word-5'd16)*16+:16]$enable; operation_count=13; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-548"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_packet_first$enable; child_output=road_low_io_physical_shell.reg_packet_first$enable; operation_count=14; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_packet_first$enable; child_output=road_low_io_physical_shell.reg_packet_first$enable; operation_count=14; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_packet_first$enable; child_output=road_low_io_physical_shell.reg_packet_first$enable; operation_count=14; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-549"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_packet_header_legal$enable; child_output=road_low_io_physical_shell.reg_packet_header_legal$enable; operation_count=14; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_packet_header_legal$enable; child_output=road_low_io_physical_shell.reg_packet_header_legal$enable; operation_count=14; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_packet_header_legal$enable; child_output=road_low_io_physical_shell.reg_packet_header_legal$enable; operation_count=14; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-550"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_packet_last$enable; child_output=road_low_io_physical_shell.reg_packet_last$enable; operation_count=14; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_packet_last$enable; child_output=road_low_io_physical_shell.reg_packet_last$enable; operation_count=14; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_packet_last$enable; child_output=road_low_io_physical_shell.reg_packet_last$enable; operation_count=14; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-551"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_packet_mask$enable; child_output=road_low_io_physical_shell.reg_packet_mask$enable; operation_count=14; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_packet_mask$enable; child_output=road_low_io_physical_shell.reg_packet_mask$enable; operation_count=14; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_packet_mask$enable; child_output=road_low_io_physical_shell.reg_packet_mask$enable; operation_count=14; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-552"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_packet_weight$enable; child_output=road_low_io_physical_shell.reg_packet_weight$enable; operation_count=9; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_packet_weight$enable; child_output=road_low_io_physical_shell.reg_packet_weight$enable; operation_count=9; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_packet_weight$enable; child_output=road_low_io_physical_shell.reg_packet_weight$enable; operation_count=9; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-553"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_packet_weight[(cnt_payload_word-5'd4)*16+:16]$D; child_output=road_low_io_physical_shell.reg_packet_weight[(cnt_payload_word-5'd4)*16+:16]$D; operation_count=0; limit=3; inconclusive_reason=reg_packet_weight[(cnt_payload_word-5'd4)*16+:16]$D: missing storage data expression; loop_presence=absent
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_packet_weight[(cnt_payload_word-5'd4)*16+:16]$D; child_output=road_low_io_physical_shell.reg_packet_weight[(cnt_payload_word-5'd4)*16+:16]$D; operation_count=0; limit=3; inconclusive_reason=reg_packet_weight[(cnt_payload_word-5'd4)*16+:16]$D: missing storage data expression; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_packet_weight[(cnt_payload_word-5'd4)*16+:16]$D; child_output=road_low_io_physical_shell.reg_packet_weight[(cnt_payload_word-5'd4)*16+:16]$D; operation_count=0; limit=3; inconclusive_reason=reg_packet_weight[(cnt_payload_word-5'd4)*16+:16]$D: missing storage data expression; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-554"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_packet_weight[(cnt_payload_word-5'd4)*16+:16]$enable; child_output=road_low_io_physical_shell.reg_packet_weight[(cnt_payload_word-5'd4)*16+:16]$enable; operation_count=13; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_packet_weight[(cnt_payload_word-5'd4)*16+:16]$enable; child_output=road_low_io_physical_shell.reg_packet_weight[(cnt_payload_word-5'd4)*16+:16]$enable; operation_count=13; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_packet_weight[(cnt_payload_word-5'd4)*16+:16]$enable; child_output=road_low_io_physical_shell.reg_packet_weight[(cnt_payload_word-5'd4)*16+:16]$enable; operation_count=13; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-555"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_result_checksum$D; child_output=road_low_io_physical_shell.reg_result_checksum$D; operation_count=1; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_result_checksum$D; child_output=road_low_io_physical_shell.reg_result_checksum$D; operation_count=1; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_result_checksum$D; child_output=road_low_io_physical_shell.reg_result_checksum$D; operation_count=1; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-556"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_result_checksum$enable; child_output=road_low_io_physical_shell.reg_result_checksum$enable; operation_count=22; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_result_checksum$enable; child_output=road_low_io_physical_shell.reg_result_checksum$enable; operation_count=22; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_result_checksum$enable; child_output=road_low_io_physical_shell.reg_result_checksum$enable; operation_count=22; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-557"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_run_packet_count$enable; child_output=road_low_io_physical_shell.reg_run_packet_count$enable; operation_count=24; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_run_packet_count$enable; child_output=road_low_io_physical_shell.reg_run_packet_count$enable; operation_count=24; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_run_packet_count$enable; child_output=road_low_io_physical_shell.reg_run_packet_count$enable; operation_count=24; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-558"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_shell_error$D; child_output=road_low_io_physical_shell.reg_shell_error$D; operation_count=13; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_shell_error$D; child_output=road_low_io_physical_shell.reg_shell_error$D; operation_count=13; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_shell_error$D; child_output=road_low_io_physical_shell.reg_shell_error$D; operation_count=13; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-559"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_shell_error$enable; child_output=road_low_io_physical_shell.reg_shell_error$enable; operation_count=65; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_shell_error$enable; child_output=road_low_io_physical_shell.reg_shell_error$enable; operation_count=65; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_shell_error$enable; child_output=road_low_io_physical_shell.reg_shell_error$enable; operation_count=65; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-560"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_snapshot_core$enable; child_output=road_low_io_physical_shell.reg_snapshot_core$enable; operation_count=9; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_snapshot_core$enable; child_output=road_low_io_physical_shell.reg_snapshot_core$enable; operation_count=9; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_snapshot_core$enable; child_output=road_low_io_physical_shell.reg_snapshot_core$enable; operation_count=9; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-561"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_snapshot_core_inputs$enable; child_output=road_low_io_physical_shell.reg_snapshot_core_inputs$enable; operation_count=9; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_snapshot_core_inputs$enable; child_output=road_low_io_physical_shell.reg_snapshot_core_inputs$enable; operation_count=9; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_snapshot_core_inputs$enable; child_output=road_low_io_physical_shell.reg_snapshot_core_inputs$enable; operation_count=9; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-562"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_snapshot_export$enable; child_output=road_low_io_physical_shell.reg_snapshot_export$enable; operation_count=9; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_snapshot_export$enable; child_output=road_low_io_physical_shell.reg_snapshot_export$enable; operation_count=9; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_snapshot_export$enable; child_output=road_low_io_physical_shell.reg_snapshot_export$enable; operation_count=9; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-563"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_snapshot_preload$enable; child_output=road_low_io_physical_shell.reg_snapshot_preload$enable; operation_count=9; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_snapshot_preload$enable; child_output=road_low_io_physical_shell.reg_snapshot_preload$enable; operation_count=9; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_snapshot_preload$enable; child_output=road_low_io_physical_shell.reg_snapshot_preload$enable; operation_count=9; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-564"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_snapshot_results$enable; child_output=road_low_io_physical_shell.reg_snapshot_results$enable; operation_count=9; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_snapshot_results$enable; child_output=road_low_io_physical_shell.reg_snapshot_results$enable; operation_count=9; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_snapshot_results$enable; child_output=road_low_io_physical_shell.reg_snapshot_results$enable; operation_count=9; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-565"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_snapshot_rx_words$enable; child_output=road_low_io_physical_shell.reg_snapshot_rx_words$enable; operation_count=9; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_snapshot_rx_words$enable; child_output=road_low_io_physical_shell.reg_snapshot_rx_words$enable; operation_count=9; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_snapshot_rx_words$enable; child_output=road_low_io_physical_shell.reg_snapshot_rx_words$enable; operation_count=9; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-566"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_snapshot_tx_words$enable; child_output=road_low_io_physical_shell.reg_snapshot_tx_words$enable; operation_count=9; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_snapshot_tx_words$enable; child_output=road_low_io_physical_shell.reg_snapshot_tx_words$enable; operation_count=9; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_snapshot_tx_words$enable; child_output=road_low_io_physical_shell.reg_snapshot_tx_words$enable; operation_count=9; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-567"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_table_pending_data$enable; child_output=road_low_io_physical_shell.reg_table_pending_data$enable; operation_count=7; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_table_pending_data$enable; child_output=road_low_io_physical_shell.reg_table_pending_data$enable; operation_count=7; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_table_pending_data$enable; child_output=road_low_io_physical_shell.reg_table_pending_data$enable; operation_count=7; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-568"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_table_pending_valid$enable; child_output=road_low_io_physical_shell.reg_table_pending_valid$enable; operation_count=8; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_table_pending_valid$enable; child_output=road_low_io_physical_shell.reg_table_pending_valid$enable; operation_count=8; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_table_pending_valid$enable; child_output=road_low_io_physical_shell.reg_table_pending_valid$enable; operation_count=8; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-569"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_weight_memory[cnt_packet_loaded]$D; child_output=road_low_io_physical_shell.reg_weight_memory[cnt_packet_loaded]$D; operation_count=0; limit=3; inconclusive_reason=reg_weight_memory[cnt_packet_loaded]$D: missing storage data expression; loop_presence=absent
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_weight_memory[cnt_packet_loaded]$D; child_output=road_low_io_physical_shell.reg_weight_memory[cnt_packet_loaded]$D; operation_count=0; limit=3; inconclusive_reason=reg_weight_memory[cnt_packet_loaded]$D: missing storage data expression; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_weight_memory[cnt_packet_loaded]$D; child_output=road_low_io_physical_shell.reg_weight_memory[cnt_packet_loaded]$D; operation_count=0; limit=3; inconclusive_reason=reg_weight_memory[cnt_packet_loaded]$D: missing storage data expression; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-570"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_weight_memory[cnt_packet_loaded]$enable; child_output=road_low_io_physical_shell.reg_weight_memory[cnt_packet_loaded]$enable; operation_count=26; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_weight_memory[cnt_packet_loaded]$enable; child_output=road_low_io_physical_shell.reg_weight_memory[cnt_packet_loaded]$enable; operation_count=26; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_weight_memory[cnt_packet_loaded]$enable; child_output=road_low_io_physical_shell.reg_weight_memory[cnt_packet_loaded]$enable; operation_count=26; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-571"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=state_current$D; child_output=road_low_io_physical_shell.state_current$D; operation_count=77; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=state_current$D; child_output=road_low_io_physical_shell.state_current$D; operation_count=77; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=state_current$D; child_output=road_low_io_physical_shell.state_current$D; operation_count=77; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-572"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=tx_data_o$D; child_output=road_low_io_physical_shell.tx_data_o$D; operation_count=1; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=tx_data_o$D; child_output=road_low_io_physical_shell.tx_data_o$D; operation_count=1; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=tx_data_o$D; child_output=road_low_io_physical_shell.tx_data_o$D; operation_count=1; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-573"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=tx_data_o$enable; child_output=road_low_io_physical_shell.tx_data_o$enable; operation_count=32; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=tx_data_o$enable; child_output=road_low_io_physical_shell.tx_data_o$enable; operation_count=32; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=tx_data_o$enable; child_output=road_low_io_physical_shell.tx_data_o$enable; operation_count=32; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-574"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=tx_valid_o$enable; child_output=road_low_io_physical_shell.tx_valid_o$enable; operation_count=34; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=tx_valid_o$enable; child_output=road_low_io_physical_shell.tx_valid_o$enable; operation_count=34; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=tx_valid_o$enable; child_output=road_low_io_physical_shell.tx_valid_o$enable; operation_count=34; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-575"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:224`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=flag_rx_transfer; child_output=road_low_io_physical_shell.flag_rx_transfer; operation_count=5; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=flag_rx_transfer; child_output=road_low_io_physical_shell.flag_rx_transfer; operation_count=5; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=flag_rx_transfer; child_output=road_low_io_physical_shell.flag_rx_transfer; operation_count=5; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-576"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:226`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=enc_packet_terms; child_output=road_low_io_physical_shell.enc_packet_terms; operation_count=7; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=enc_packet_terms; child_output=road_low_io_physical_shell.enc_packet_terms; operation_count=7; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=enc_packet_terms; child_output=road_low_io_physical_shell.enc_packet_terms; operation_count=7; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-577"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:228`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=next_term_count; child_output=road_low_io_physical_shell.next_term_count; operation_count=8; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=next_term_count; child_output=road_low_io_physical_shell.next_term_count; operation_count=8; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=next_term_count; child_output=road_low_io_physical_shell.next_term_count; operation_count=8; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-578"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:231`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=flag_table_transfer; child_output=road_low_io_physical_shell.flag_table_transfer; operation_count=1; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=flag_table_transfer; child_output=road_low_io_physical_shell.flag_table_transfer; operation_count=1; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=flag_table_transfer; child_output=road_low_io_physical_shell.flag_table_transfer; operation_count=1; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-579"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:232`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=flag_table_last_transfer; child_output=road_low_io_physical_shell.flag_table_last_transfer; operation_count=3; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=flag_table_last_transfer; child_output=road_low_io_physical_shell.flag_table_last_transfer; operation_count=3; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=flag_table_last_transfer; child_output=road_low_io_physical_shell.flag_table_last_transfer; operation_count=3; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-580"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:233`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=flag_core_input_transfer; child_output=road_low_io_physical_shell.flag_core_input_transfer; operation_count=2; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=flag_core_input_transfer; child_output=road_low_io_physical_shell.flag_core_input_transfer; operation_count=2; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=flag_core_input_transfer; child_output=road_low_io_physical_shell.flag_core_input_transfer; operation_count=2; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-581"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:234`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=flag_core_last_transfer; child_output=road_low_io_physical_shell.flag_core_last_transfer; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=flag_core_last_transfer; child_output=road_low_io_physical_shell.flag_core_last_transfer; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=flag_core_last_transfer; child_output=road_low_io_physical_shell.flag_core_last_transfer; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-582"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:237`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=flag_cache_request_transfer; child_output=road_low_io_physical_shell.flag_cache_request_transfer; operation_count=4; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=flag_cache_request_transfer; child_output=road_low_io_physical_shell.flag_cache_request_transfer; operation_count=4; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=flag_cache_request_transfer; child_output=road_low_io_physical_shell.flag_cache_request_transfer; operation_count=4; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-583"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:238`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=flag_cache_result_transfer; child_output=road_low_io_physical_shell.flag_cache_result_transfer; operation_count=6; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=flag_cache_result_transfer; child_output=road_low_io_physical_shell.flag_cache_result_transfer; operation_count=6; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=flag_cache_result_transfer; child_output=road_low_io_physical_shell.flag_cache_result_transfer; operation_count=6; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-584"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:241`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=flag_run_command_legal; child_output=road_low_io_physical_shell.flag_run_command_legal; operation_count=14; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=flag_run_command_legal; child_output=road_low_io_physical_shell.flag_run_command_legal; operation_count=14; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=flag_run_command_legal; child_output=road_low_io_physical_shell.flag_run_command_legal; operation_count=14; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-585"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:242`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=flag_packet_commit_legal; child_output=road_low_io_physical_shell.flag_packet_commit_legal; operation_count=24; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=flag_packet_commit_legal; child_output=road_low_io_physical_shell.flag_packet_commit_legal; operation_count=24; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=flag_packet_commit_legal; child_output=road_low_io_physical_shell.flag_packet_commit_legal; operation_count=24; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-586"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:263`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=o_rx_ready; child_output=road_low_io_physical_shell.o_rx_ready; operation_count=4; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=o_rx_ready; child_output=road_low_io_physical_shell.o_rx_ready; operation_count=4; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=o_rx_ready; child_output=road_low_io_physical_shell.o_rx_ready; operation_count=4; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-587"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:269`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=rx_ready_o; child_output=road_low_io_physical_shell.rx_ready_o; operation_count=4; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=rx_ready_o; child_output=road_low_io_physical_shell.rx_ready_o; operation_count=4; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=rx_ready_o; child_output=road_low_io_physical_shell.rx_ready_o; operation_count=4; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-588"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:283`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=dec_status_word; child_output=road_low_io_physical_shell.dec_status_word; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=dec_status_word; child_output=road_low_io_physical_shell.dec_status_word; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=dec_status_word; child_output=road_low_io_physical_shell.dec_status_word; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-589"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:317`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=state_next; child_output=road_low_io_physical_shell.state_next; operation_count=77; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=state_next; child_output=road_low_io_physical_shell.state_next; operation_count=77; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=state_next; child_output=road_low_io_physical_shell.state_next; operation_count=77; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-590"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_activation_data; child_output=road_low_io_physical_shell.chain_activation_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_activation_data; child_output=road_low_io_physical_shell.chain_activation_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_activation_data; child_output=road_low_io_physical_shell.chain_activation_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
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
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_bias_data; child_output=road_low_io_physical_shell.chain_bias_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_bias_data; child_output=road_low_io_physical_shell.chain_bias_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_bias_data; child_output=road_low_io_physical_shell.chain_bias_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-592"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_cache_read_addr; child_output=road_low_io_physical_shell.chain_cache_read_addr; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_cache_read_addr; child_output=road_low_io_physical_shell.chain_cache_read_addr; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_cache_read_addr; child_output=road_low_io_physical_shell.chain_cache_read_addr; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-593"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_cache_read_ready; child_output=road_low_io_physical_shell.chain_cache_read_ready; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_cache_read_ready; child_output=road_low_io_physical_shell.chain_cache_read_ready; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_cache_read_ready; child_output=road_low_io_physical_shell.chain_cache_read_ready; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
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
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_cache_read_valid; child_output=road_low_io_physical_shell.chain_cache_read_valid; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_cache_read_valid; child_output=road_low_io_physical_shell.chain_cache_read_valid; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_cache_read_valid; child_output=road_low_io_physical_shell.chain_cache_read_valid; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-595"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_cache_result_data; child_output=road_low_io_physical_shell.chain_cache_result_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_cache_result_data; child_output=road_low_io_physical_shell.chain_cache_result_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_cache_result_data; child_output=road_low_io_physical_shell.chain_cache_result_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
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
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_cache_result_fault; child_output=road_low_io_physical_shell.chain_cache_result_fault; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_cache_result_fault; child_output=road_low_io_physical_shell.chain_cache_result_fault; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_cache_result_fault; child_output=road_low_io_physical_shell.chain_cache_result_fault; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
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
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_cache_result_ready; child_output=road_low_io_physical_shell.chain_cache_result_ready; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_cache_result_ready; child_output=road_low_io_physical_shell.chain_cache_result_ready; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_cache_result_ready; child_output=road_low_io_physical_shell.chain_cache_result_ready; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
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
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_cache_result_valid; child_output=road_low_io_physical_shell.chain_cache_result_valid; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_cache_result_valid; child_output=road_low_io_physical_shell.chain_cache_result_valid; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_cache_result_valid; child_output=road_low_io_physical_shell.chain_cache_result_valid; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
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
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_fault; child_output=road_low_io_physical_shell.chain_fault; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_fault; child_output=road_low_io_physical_shell.chain_fault; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_fault; child_output=road_low_io_physical_shell.chain_fault; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
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
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_first; child_output=road_low_io_physical_shell.chain_first; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_first; child_output=road_low_io_physical_shell.chain_first; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_first; child_output=road_low_io_physical_shell.chain_first; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
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
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_input_ready; child_output=road_low_io_physical_shell.chain_input_ready; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_input_ready; child_output=road_low_io_physical_shell.chain_input_ready; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_input_ready; child_output=road_low_io_physical_shell.chain_input_ready; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
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
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_input_valid; child_output=road_low_io_physical_shell.chain_input_valid; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_input_valid; child_output=road_low_io_physical_shell.chain_input_valid; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_input_valid; child_output=road_low_io_physical_shell.chain_input_valid; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
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
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_lane_mask; child_output=road_low_io_physical_shell.chain_lane_mask; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_lane_mask; child_output=road_low_io_physical_shell.chain_lane_mask; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_lane_mask; child_output=road_low_io_physical_shell.chain_lane_mask; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
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
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_last; child_output=road_low_io_physical_shell.chain_last; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_last; child_output=road_low_io_physical_shell.chain_last; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_last; child_output=road_low_io_physical_shell.chain_last; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
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
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_table_addr; child_output=road_low_io_physical_shell.chain_table_addr; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_table_addr; child_output=road_low_io_physical_shell.chain_table_addr; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_table_addr; child_output=road_low_io_physical_shell.chain_table_addr; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
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
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_table_data; child_output=road_low_io_physical_shell.chain_table_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_table_data; child_output=road_low_io_physical_shell.chain_table_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_table_data; child_output=road_low_io_physical_shell.chain_table_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
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
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_table_fault; child_output=road_low_io_physical_shell.chain_table_fault; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_table_fault; child_output=road_low_io_physical_shell.chain_table_fault; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_table_fault; child_output=road_low_io_physical_shell.chain_table_fault; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
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
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_table_loaded; child_output=road_low_io_physical_shell.chain_table_loaded; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_table_loaded; child_output=road_low_io_physical_shell.chain_table_loaded; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_table_loaded; child_output=road_low_io_physical_shell.chain_table_loaded; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
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
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_table_ready; child_output=road_low_io_physical_shell.chain_table_ready; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_table_ready; child_output=road_low_io_physical_shell.chain_table_ready; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_table_ready; child_output=road_low_io_physical_shell.chain_table_ready; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
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
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_table_valid; child_output=road_low_io_physical_shell.chain_table_valid; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_table_valid; child_output=road_low_io_physical_shell.chain_table_valid; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_table_valid; child_output=road_low_io_physical_shell.chain_table_valid; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
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
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_weight_data; child_output=road_low_io_physical_shell.chain_weight_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_weight_data; child_output=road_low_io_physical_shell.chain_weight_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=chain_weight_data; child_output=road_low_io_physical_shell.chain_weight_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-612"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=cnt_core_cycles$enable; child_output=road_low_io_physical_shell.cnt_core_cycles$enable; operation_count=38; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=cnt_core_cycles$enable; child_output=road_low_io_physical_shell.cnt_core_cycles$enable; operation_count=38; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=cnt_core_cycles$enable; child_output=road_low_io_physical_shell.cnt_core_cycles$enable; operation_count=38; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-613"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=cnt_core_inputs$enable; child_output=road_low_io_physical_shell.cnt_core_inputs$enable; operation_count=26; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=cnt_core_inputs$enable; child_output=road_low_io_physical_shell.cnt_core_inputs$enable; operation_count=26; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=cnt_core_inputs$enable; child_output=road_low_io_physical_shell.cnt_core_inputs$enable; operation_count=26; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-614"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=cnt_result_outputs$enable; child_output=road_low_io_physical_shell.cnt_result_outputs$enable; operation_count=22; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=cnt_result_outputs$enable; child_output=road_low_io_physical_shell.cnt_result_outputs$enable; operation_count=22; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=cnt_result_outputs$enable; child_output=road_low_io_physical_shell.cnt_result_outputs$enable; operation_count=22; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-615"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=cnt_run_index$enable; child_output=road_low_io_physical_shell.cnt_run_index$enable; operation_count=26; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=cnt_run_index$enable; child_output=road_low_io_physical_shell.cnt_run_index$enable; operation_count=26; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=cnt_run_index$enable; child_output=road_low_io_physical_shell.cnt_run_index$enable; operation_count=26; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-616"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=cnt_table_entry$enable; child_output=road_low_io_physical_shell.cnt_table_entry$enable; operation_count=12; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=cnt_table_entry$enable; child_output=road_low_io_physical_shell.cnt_table_entry$enable; operation_count=12; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=cnt_table_entry$enable; child_output=road_low_io_physical_shell.cnt_table_entry$enable; operation_count=12; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-617"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=flag_core_busy_observed$enable; child_output=road_low_io_physical_shell.flag_core_busy_observed$enable; operation_count=27; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=flag_core_busy_observed$enable; child_output=road_low_io_physical_shell.flag_core_busy_observed$enable; operation_count=27; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=flag_core_busy_observed$enable; child_output=road_low_io_physical_shell.flag_core_busy_observed$enable; operation_count=27; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-618"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=flag_core_timing_active$enable; child_output=road_low_io_physical_shell.flag_core_timing_active$enable; operation_count=7; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=flag_core_timing_active$enable; child_output=road_low_io_physical_shell.flag_core_timing_active$enable; operation_count=7; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=flag_core_timing_active$enable; child_output=road_low_io_physical_shell.flag_core_timing_active$enable; operation_count=7; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-619"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=flag_run_complete$enable; child_output=road_low_io_physical_shell.flag_run_complete$enable; operation_count=27; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=flag_run_complete$enable; child_output=road_low_io_physical_shell.flag_run_complete$enable; operation_count=27; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=flag_run_complete$enable; child_output=road_low_io_physical_shell.flag_run_complete$enable; operation_count=27; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-620"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=flag_shell_fault$enable; child_output=road_low_io_physical_shell.flag_shell_fault$enable; operation_count=65; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=flag_shell_fault$enable; child_output=road_low_io_physical_shell.flag_shell_fault$enable; operation_count=65; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=flag_shell_fault$enable; child_output=road_low_io_physical_shell.flag_shell_fault$enable; operation_count=65; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-621"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=flag_table_complete$enable; child_output=road_low_io_physical_shell.flag_table_complete$enable; operation_count=13; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=flag_table_complete$enable; child_output=road_low_io_physical_shell.flag_table_complete$enable; operation_count=13; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=flag_table_complete$enable; child_output=road_low_io_physical_shell.flag_table_complete$enable; operation_count=13; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
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
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_result_checksum$D; child_output=road_low_io_physical_shell.reg_result_checksum$D; operation_count=1; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_result_checksum$D; child_output=road_low_io_physical_shell.reg_result_checksum$D; operation_count=1; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_result_checksum$D; child_output=road_low_io_physical_shell.reg_result_checksum$D; operation_count=1; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-623"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_result_checksum$enable; child_output=road_low_io_physical_shell.reg_result_checksum$enable; operation_count=22; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_result_checksum$enable; child_output=road_low_io_physical_shell.reg_result_checksum$enable; operation_count=22; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_result_checksum$enable; child_output=road_low_io_physical_shell.reg_result_checksum$enable; operation_count=22; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-624"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_shell_error$enable; child_output=road_low_io_physical_shell.reg_shell_error$enable; operation_count=65; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_shell_error$enable; child_output=road_low_io_physical_shell.reg_shell_error$enable; operation_count=65; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_shell_error$enable; child_output=road_low_io_physical_shell.reg_shell_error$enable; operation_count=65; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-625"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_table_pending_valid$enable; child_output=road_low_io_physical_shell.reg_table_pending_valid$enable; operation_count=8; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_table_pending_valid$enable; child_output=road_low_io_physical_shell.reg_table_pending_valid$enable; operation_count=8; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=reg_table_pending_valid$enable; child_output=road_low_io_physical_shell.reg_table_pending_valid$enable; operation_count=8; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-626"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=state_current$D; child_output=road_low_io_physical_shell.state_current$D; operation_count=77; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=state_current$D; child_output=road_low_io_physical_shell.state_current$D; operation_count=77; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=state_current$D; child_output=road_low_io_physical_shell.state_current$D; operation_count=77; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
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
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=tx_data_o$D; child_output=road_low_io_physical_shell.tx_data_o$D; operation_count=1; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=tx_data_o$D; child_output=road_low_io_physical_shell.tx_data_o$D; operation_count=1; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=tx_data_o$D; child_output=road_low_io_physical_shell.tx_data_o$D; operation_count=1; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-628"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=tx_data_o$enable; child_output=road_low_io_physical_shell.tx_data_o$enable; operation_count=32; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=tx_data_o$enable; child_output=road_low_io_physical_shell.tx_data_o$enable; operation_count=32; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=tx_data_o$enable; child_output=road_low_io_physical_shell.tx_data_o$enable; operation_count=32; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-629"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=tx_valid_o$enable; child_output=road_low_io_physical_shell.tx_valid_o$enable; operation_count=34; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=tx_valid_o$enable; child_output=road_low_io_physical_shell.tx_valid_o$enable; operation_count=34; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=tx_valid_o$enable; child_output=road_low_io_physical_shell.tx_valid_o$enable; operation_count=34; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
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
- Location: `road_low_io_physical_shell.v:231`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=flag_table_transfer; child_output=road_low_io_physical_shell.flag_table_transfer; operation_count=1; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=flag_table_transfer; child_output=road_low_io_physical_shell.flag_table_transfer; operation_count=1; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=flag_table_transfer; child_output=road_low_io_physical_shell.flag_table_transfer; operation_count=1; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-631"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:232`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=flag_table_last_transfer; child_output=road_low_io_physical_shell.flag_table_last_transfer; operation_count=3; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=flag_table_last_transfer; child_output=road_low_io_physical_shell.flag_table_last_transfer; operation_count=3; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=flag_table_last_transfer; child_output=road_low_io_physical_shell.flag_table_last_transfer; operation_count=3; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
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
- Location: `road_low_io_physical_shell.v:233`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=flag_core_input_transfer; child_output=road_low_io_physical_shell.flag_core_input_transfer; operation_count=2; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=flag_core_input_transfer; child_output=road_low_io_physical_shell.flag_core_input_transfer; operation_count=2; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=flag_core_input_transfer; child_output=road_low_io_physical_shell.flag_core_input_transfer; operation_count=2; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-633"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:234`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=flag_core_last_transfer; child_output=road_low_io_physical_shell.flag_core_last_transfer; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=flag_core_last_transfer; child_output=road_low_io_physical_shell.flag_core_last_transfer; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=flag_core_last_transfer; child_output=road_low_io_physical_shell.flag_core_last_transfer; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-634"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:237`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=flag_cache_request_transfer; child_output=road_low_io_physical_shell.flag_cache_request_transfer; operation_count=4; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=flag_cache_request_transfer; child_output=road_low_io_physical_shell.flag_cache_request_transfer; operation_count=4; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=flag_cache_request_transfer; child_output=road_low_io_physical_shell.flag_cache_request_transfer; operation_count=4; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
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
- Location: `road_low_io_physical_shell.v:238`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=flag_cache_result_transfer; child_output=road_low_io_physical_shell.flag_cache_result_transfer; operation_count=6; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=flag_cache_result_transfer; child_output=road_low_io_physical_shell.flag_cache_result_transfer; operation_count=6; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=flag_cache_result_transfer; child_output=road_low_io_physical_shell.flag_cache_result_transfer; operation_count=6; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-636"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:283`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=dec_status_word; child_output=road_low_io_physical_shell.dec_status_word; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=dec_status_word; child_output=road_low_io_physical_shell.dec_status_word; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=dec_status_word; child_output=road_low_io_physical_shell.dec_status_word; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-637"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:317`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=state_next; child_output=road_low_io_physical_shell.state_next; operation_count=77; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=state_next; child_output=road_low_io_physical_shell.state_next; operation_count=77; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_low_io_physical_shell.v:road_low_io_physical_shell@49:1-789:1; instance_path=road_low_io_physical_shell; specialization=66960d26b3a6162462a76b0898d681efe2fd1df72935c63d597a4a47de4b6fa3; target=state_next; child_output=road_low_io_physical_shell.state_next; operation_count=77; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-638"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:111`
- Evidence:
- node_kind: `verilog_rtl`
- detail: chain_input_ready
- source_excerpt: `chain_input_ready`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
chain_input_ready
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-639"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:112`
- Evidence:
- node_kind: `verilog_rtl`
- detail: chain_fault
- source_excerpt: `chain_fault`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
chain_fault
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-640"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:113`
- Evidence:
- node_kind: `verilog_rtl`
- detail: chain_table_ready
- source_excerpt: `chain_table_ready`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
chain_table_ready
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-641"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:114`
- Evidence:
- node_kind: `verilog_rtl`
- detail: chain_table_loaded
- source_excerpt: `chain_table_loaded`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
chain_table_loaded
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-642"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:115`
- Evidence:
- node_kind: `verilog_rtl`
- detail: chain_table_fault
- source_excerpt: `chain_table_fault`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
chain_table_fault
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-643"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:116`
- Evidence:
- node_kind: `verilog_rtl`
- detail: chain_cache_read_ready
- source_excerpt: `chain_cache_read_ready`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
chain_cache_read_ready
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-644"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:117`
- Evidence:
- node_kind: `verilog_rtl`
- detail: chain_cache_result_valid
- source_excerpt: `chain_cache_result_valid`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
chain_cache_result_valid
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-645"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:118`
- Evidence:
- node_kind: `verilog_rtl`
- detail: chain_cache_result_data
- source_excerpt: `chain_cache_result_data`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
chain_cache_result_data
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-646"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:119`
- Evidence:
- node_kind: `verilog_rtl`
- detail: chain_cache_result_fault
- source_excerpt: `chain_cache_result_fault`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
chain_cache_result_fault
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-647"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:158`
- Evidence:
- node_kind: `verilog_rtl`
- detail: reg_first_memory
- source_excerpt: `reg_first_memory`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
reg_first_memory
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-648"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:159`
- Evidence:
- node_kind: `verilog_rtl`
- detail: reg_last_memory
- source_excerpt: `reg_last_memory`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
reg_last_memory
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-649"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:160`
- Evidence:
- node_kind: `verilog_rtl`
- detail: reg_mask_memory
- source_excerpt: `reg_mask_memory`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
reg_mask_memory
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-650"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:161`
- Evidence:
- node_kind: `verilog_rtl`
- detail: reg_activation_memory
- source_excerpt: `reg_activation_memory`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
reg_activation_memory
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-651"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:162`
- Evidence:
- node_kind: `verilog_rtl`
- detail: reg_weight_memory
- source_excerpt: `reg_weight_memory`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
reg_weight_memory
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-652"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:163`
- Evidence:
- node_kind: `verilog_rtl`
- detail: reg_bias_memory
- source_excerpt: `reg_bias_memory`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
reg_bias_memory
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-653"></a>
### VG157: 普通 RTL 注释不得携带版本字样；版本历史只能位于 formatter 固定文件头范围。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:19`
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

<a id="vg-finding-654"></a>
### VG157: 普通 RTL 注释不得携带版本字样；版本历史只能位于 formatter 固定文件头范围。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_low_io_physical_shell.v:42`
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
| error | COMMENT_COMMENT_PLACEMENT | `road_low_io_physical_shell.v:762` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
