# Verilog deliverable gate

Root: `E:\project\qiansai\anlogic_topic2_work\lab1_sc500_road_vision\cnn\hw_validation\production\reports\v11_internal_timing_ack_local_20261007\rtl\down2_overlap_tile_runner.v`
Delivery ready: `False`
Summary: **1127 error(s)**, **0 strict warning(s)**

## Actionable VG findings

<a id="vg-finding-1"></a>
### VG007: Standard bilingual header with English/Chinese sections is required.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:1`
- Evidence:
- node_kind: `verilog_rtl`
- detail: header.bilingual
- source_excerpt: `header.bilingual`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
header.bilingual
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-2"></a>
### VG007: English header is missing required field(s): Company, Engineer, Create Date, Design Name, Module Name, Description, Simulations, Referrences, Dependencies, Version, Revision Date, History
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:1`
- Evidence:
- node_kind: `verilog_rtl`
- detail: header.english_fields
- source_excerpt: `header.english_fields`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
header.english_fields
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-3"></a>
### VG007: Chinese header is missing required field(s): 版权归属, 开发人员, 创建日期, 设计名称, 模块名称, 模块说明, 仿真工程, 参考资料, 依赖文件, 当前版本, 修订日期, 修订历史
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:1`
- Evidence:
- node_kind: `verilog_rtl`
- detail: header.chinese_fields
- source_excerpt: `header.chinese_fields`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
header.chinese_fields
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-4"></a>
### VG068: Header Description/Simulations fields must use the fixed bilingual path contract (`description/testbench` in English and `Description/TestBench` in Chinese).
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:1`
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

<a id="vg-finding-5"></a>
### VG007: Header history must contain at least one dated record with a Vx.y version.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:1`
- Evidence:
- node_kind: `verilog_rtl`
- detail: header.history_records
- source_excerpt: `header.history_records`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
header.history_records
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-6"></a>
### VG025: Control statements must use explicit begin/end blocks.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:586`
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

<a id="vg-finding-7"></a>
### VG025: Control statements must use explicit begin/end blocks.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:594`
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

<a id="vg-finding-8"></a>
### VG040: Generated explanatory comments should be Chinese-first.
- Status: `failed`
- Severity: `error`
- Location: `file:down2_overlap_tile_runner.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.language
- source_excerpt: `comments.language`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.language
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-9"></a>
### VG009: Module `down2_overlap_tile_runner` port list should use Chinese group comments such as 全局信号, 用户接口, or protocol 接口 groups.
- Status: `failed`
- Severity: `error`
- Location: `file:down2_overlap_tile_runner.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: ports.group_comments
- source_excerpt: `ports.group_comments`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
ports.group_comments
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-10"></a>
### VG015: Internal non-array reg declaration `state_current` must be explicitly initialized inside the module; when backfilling a missing initializer, use exact ` = 0;`.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:75`
- Evidence:
- node_kind: `verilog_rtl`
- detail: declaration.internal_reg_default_init
- source_excerpt: `declaration.internal_reg_default_init`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
declaration.internal_reg_default_init
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-11"></a>
### VG015: Internal non-array reg declaration `flag_layer_pw` must be explicitly initialized inside the module; when backfilling a missing initializer, use exact ` = 0;`.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:76`
- Evidence:
- node_kind: `verilog_rtl`
- detail: declaration.internal_reg_default_init
- source_excerpt: `declaration.internal_reg_default_init`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
declaration.internal_reg_default_init
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-12"></a>
### VG015: Internal non-array reg declaration `flag_busy_o` must be explicitly initialized inside the module; when backfilling a missing initializer, use exact ` = 0;`.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:77`
- Evidence:
- node_kind: `verilog_rtl`
- detail: declaration.internal_reg_default_init
- source_excerpt: `declaration.internal_reg_default_init`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
declaration.internal_reg_default_init
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-13"></a>
### VG015: Internal non-array reg declaration `flag_done_o` must be explicitly initialized inside the module; when backfilling a missing initializer, use exact ` = 0;`.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:78`
- Evidence:
- node_kind: `verilog_rtl`
- detail: declaration.internal_reg_default_init
- source_excerpt: `declaration.internal_reg_default_init`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
declaration.internal_reg_default_init
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-14"></a>
### VG015: Internal non-array reg declaration `flag_fault_o` must be explicitly initialized inside the module; when backfilling a missing initializer, use exact ` = 0;`.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:79`
- Evidence:
- node_kind: `verilog_rtl`
- detail: declaration.internal_reg_default_init
- source_excerpt: `declaration.internal_reg_default_init`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
declaration.internal_reg_default_init
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-15"></a>
### VG015: Internal non-array reg declaration `flag_load_fault` must be explicitly initialized inside the module; when backfilling a missing initializer, use exact ` = 0;`.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:80`
- Evidence:
- node_kind: `verilog_rtl`
- detail: declaration.internal_reg_default_init
- source_excerpt: `declaration.internal_reg_default_init`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
declaration.internal_reg_default_init
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-16"></a>
### VG015: Internal non-array reg declaration `flag_tile_valid` must be explicitly initialized inside the module; when backfilling a missing initializer, use exact ` = 0;`.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:81`
- Evidence:
- node_kind: `verilog_rtl`
- detail: declaration.internal_reg_default_init
- source_excerpt: `declaration.internal_reg_default_init`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `interface`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
declaration.internal_reg_default_init
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-17"></a>
### VG015: Internal non-array reg declaration `flag_export_done_o` must be explicitly initialized inside the module; when backfilling a missing initializer, use exact ` = 0;`.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:82`
- Evidence:
- node_kind: `verilog_rtl`
- detail: declaration.internal_reg_default_init
- source_excerpt: `declaration.internal_reg_default_init`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
declaration.internal_reg_default_init
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-18"></a>
### VG015: Internal non-array reg declaration `flag_result_reserved` must be explicitly initialized inside the module; when backfilling a missing initializer, use exact ` = 0;`.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:83`
- Evidence:
- node_kind: `verilog_rtl`
- detail: declaration.internal_reg_default_init
- source_excerpt: `declaration.internal_reg_default_init`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
declaration.internal_reg_default_init
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-19"></a>
### VG015: Internal non-array reg declaration `cnt_position` must be explicitly initialized inside the module; when backfilling a missing initializer, use exact ` = 0;`.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:84`
- Evidence:
- node_kind: `verilog_rtl`
- detail: declaration.internal_reg_default_init
- source_excerpt: `declaration.internal_reg_default_init`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
declaration.internal_reg_default_init
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-20"></a>
### VG015: Internal non-array reg declaration `cnt_output` must be explicitly initialized inside the module; when backfilling a missing initializer, use exact ` = 0;`.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:85`
- Evidence:
- node_kind: `verilog_rtl`
- detail: declaration.internal_reg_default_init
- source_excerpt: `declaration.internal_reg_default_init`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
declaration.internal_reg_default_init
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-21"></a>
### VG015: Internal non-array reg declaration `cnt_mac_group` must be explicitly initialized inside the module; when backfilling a missing initializer, use exact ` = 0;`.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:86`
- Evidence:
- node_kind: `verilog_rtl`
- detail: declaration.internal_reg_default_init
- source_excerpt: `declaration.internal_reg_default_init`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
declaration.internal_reg_default_init
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-22"></a>
### VG015: Internal non-array reg declaration `cnt_export` must be explicitly initialized inside the module; when backfilling a missing initializer, use exact ` = 0;`.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:87`
- Evidence:
- node_kind: `verilog_rtl`
- detail: declaration.internal_reg_default_init
- source_excerpt: `declaration.internal_reg_default_init`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
declaration.internal_reg_default_init
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-23"></a>
### VG015: Internal non-array reg declaration `cnt_dw_writes` must be explicitly initialized inside the module; when backfilling a missing initializer, use exact ` = 0;`.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:88`
- Evidence:
- node_kind: `verilog_rtl`
- detail: declaration.internal_reg_default_init
- source_excerpt: `declaration.internal_reg_default_init`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
declaration.internal_reg_default_init
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-24"></a>
### VG015: Internal non-array reg declaration `cnt_pw_writes` must be explicitly initialized inside the module; when backfilling a missing initializer, use exact ` = 0;`.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:89`
- Evidence:
- node_kind: `verilog_rtl`
- detail: declaration.internal_reg_default_init
- source_excerpt: `declaration.internal_reg_default_init`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
declaration.internal_reg_default_init
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-25"></a>
### VG015: Internal non-array reg declaration `reg_mac_activation` must be explicitly initialized inside the module; when backfilling a missing initializer, use exact ` = 0;`.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:91`
- Evidence:
- node_kind: `verilog_rtl`
- detail: declaration.internal_reg_default_init
- source_excerpt: `declaration.internal_reg_default_init`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
declaration.internal_reg_default_init
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-26"></a>
### VG015: Internal non-array reg declaration `reg_mac_weight` must be explicitly initialized inside the module; when backfilling a missing initializer, use exact ` = 0;`.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:92`
- Evidence:
- node_kind: `verilog_rtl`
- detail: declaration.internal_reg_default_init
- source_excerpt: `declaration.internal_reg_default_init`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
declaration.internal_reg_default_init
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-27"></a>
### VG015: Internal non-array reg declaration `reg_mac_bias` must be explicitly initialized inside the module; when backfilling a missing initializer, use exact ` = 0;`.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:93`
- Evidence:
- node_kind: `verilog_rtl`
- detail: declaration.internal_reg_default_init
- source_excerpt: `declaration.internal_reg_default_init`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
declaration.internal_reg_default_init
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-28"></a>
### VG015: Internal non-array reg declaration `reg_mac_mask` must be explicitly initialized inside the module; when backfilling a missing initializer, use exact ` = 0;`.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:94`
- Evidence:
- node_kind: `verilog_rtl`
- detail: declaration.internal_reg_default_init
- source_excerpt: `declaration.internal_reg_default_init`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
declaration.internal_reg_default_init
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-29"></a>
### VG013: Register `next_mac_activation` should use reg_/cnt_/state_/flag_/enc_/dec_ prefix or `_o` output suffix.
- Status: `failed`
- Severity: `error`
- Location: `file:down2_overlap_tile_runner.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: naming.register_signal
- source_excerpt: `naming.register_signal`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
naming.register_signal
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-30"></a>
### VG015: Internal non-array reg declaration `next_mac_activation` must be explicitly initialized inside the module; when backfilling a missing initializer, use exact ` = 0;`.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:95`
- Evidence:
- node_kind: `verilog_rtl`
- detail: declaration.internal_reg_default_init
- source_excerpt: `declaration.internal_reg_default_init`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
declaration.internal_reg_default_init
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-31"></a>
### VG013: Register `next_mac_weight` should use reg_/cnt_/state_/flag_/enc_/dec_ prefix or `_o` output suffix.
- Status: `failed`
- Severity: `error`
- Location: `file:down2_overlap_tile_runner.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: naming.register_signal
- source_excerpt: `naming.register_signal`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
naming.register_signal
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-32"></a>
### VG015: Internal non-array reg declaration `next_mac_weight` must be explicitly initialized inside the module; when backfilling a missing initializer, use exact ` = 0;`.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:96`
- Evidence:
- node_kind: `verilog_rtl`
- detail: declaration.internal_reg_default_init
- source_excerpt: `declaration.internal_reg_default_init`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
declaration.internal_reg_default_init
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-33"></a>
### VG013: Register `next_mac_bias` should use reg_/cnt_/state_/flag_/enc_/dec_ prefix or `_o` output suffix.
- Status: `failed`
- Severity: `error`
- Location: `file:down2_overlap_tile_runner.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: naming.register_signal
- source_excerpt: `naming.register_signal`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
naming.register_signal
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-34"></a>
### VG015: Internal non-array reg declaration `next_mac_bias` must be explicitly initialized inside the module; when backfilling a missing initializer, use exact ` = 0;`.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:97`
- Evidence:
- node_kind: `verilog_rtl`
- detail: declaration.internal_reg_default_init
- source_excerpt: `declaration.internal_reg_default_init`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
declaration.internal_reg_default_init
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-35"></a>
### VG013: Register `next_mac_mask` should use reg_/cnt_/state_/flag_/enc_/dec_ prefix or `_o` output suffix.
- Status: `failed`
- Severity: `error`
- Location: `file:down2_overlap_tile_runner.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: naming.register_signal
- source_excerpt: `naming.register_signal`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
naming.register_signal
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-36"></a>
### VG015: Internal non-array reg declaration `next_mac_mask` must be explicitly initialized inside the module; when backfilling a missing initializer, use exact ` = 0;`.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:98`
- Evidence:
- node_kind: `verilog_rtl`
- detail: declaration.internal_reg_default_init
- source_excerpt: `declaration.internal_reg_default_init`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
declaration.internal_reg_default_init
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-37"></a>
### VG015: Internal non-array reg declaration `flag_debug_valid_o` must be explicitly initialized inside the module; when backfilling a missing initializer, use exact ` = 0;`.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:100`
- Evidence:
- node_kind: `verilog_rtl`
- detail: declaration.internal_reg_default_init
- source_excerpt: `declaration.internal_reg_default_init`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `interface`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
declaration.internal_reg_default_init
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-38"></a>
### VG015: Internal non-array reg declaration `reg_debug_phase_o` must be explicitly initialized inside the module; when backfilling a missing initializer, use exact ` = 0;`.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:101`
- Evidence:
- node_kind: `verilog_rtl`
- detail: declaration.internal_reg_default_init
- source_excerpt: `declaration.internal_reg_default_init`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
declaration.internal_reg_default_init
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-39"></a>
### VG015: Internal non-array reg declaration `flag_debug_layer_o` must be explicitly initialized inside the module; when backfilling a missing initializer, use exact ` = 0;`.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:102`
- Evidence:
- node_kind: `verilog_rtl`
- detail: declaration.internal_reg_default_init
- source_excerpt: `declaration.internal_reg_default_init`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
declaration.internal_reg_default_init
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-40"></a>
### VG015: Internal non-array reg declaration `reg_debug_position_o` must be explicitly initialized inside the module; when backfilling a missing initializer, use exact ` = 0;`.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:103`
- Evidence:
- node_kind: `verilog_rtl`
- detail: declaration.internal_reg_default_init
- source_excerpt: `declaration.internal_reg_default_init`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
declaration.internal_reg_default_init
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-41"></a>
### VG015: Internal non-array reg declaration `reg_debug_channel_o` must be explicitly initialized inside the module; when backfilling a missing initializer, use exact ` = 0;`.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:104`
- Evidence:
- node_kind: `verilog_rtl`
- detail: declaration.internal_reg_default_init
- source_excerpt: `declaration.internal_reg_default_init`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
declaration.internal_reg_default_init
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-42"></a>
### VG015: Internal non-array reg declaration `reg_debug_value_o` must be explicitly initialized inside the module; when backfilling a missing initializer, use exact ` = 0;`.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:105`
- Evidence:
- node_kind: `verilog_rtl`
- detail: declaration.internal_reg_default_init
- source_excerpt: `declaration.internal_reg_default_init`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
declaration.internal_reg_default_init
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-43"></a>
### VG015: Internal non-array reg declaration `cnt_preload_writes` must be explicitly initialized inside the module; when backfilling a missing initializer, use exact ` = 0;`.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:107`
- Evidence:
- node_kind: `verilog_rtl`
- detail: declaration.internal_reg_default_init
- source_excerpt: `declaration.internal_reg_default_init`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
declaration.internal_reg_default_init
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-44"></a>
### VG015: Internal non-array reg declaration `cnt_core_cycles` must be explicitly initialized inside the module; when backfilling a missing initializer, use exact ` = 0;`.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:108`
- Evidence:
- node_kind: `verilog_rtl`
- detail: declaration.internal_reg_default_init
- source_excerpt: `declaration.internal_reg_default_init`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
declaration.internal_reg_default_init
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-45"></a>
### VG015: Internal non-array reg declaration `cnt_mac_cycles` must be explicitly initialized inside the module; when backfilling a missing initializer, use exact ` = 0;`.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:109`
- Evidence:
- node_kind: `verilog_rtl`
- detail: declaration.internal_reg_default_init
- source_excerpt: `declaration.internal_reg_default_init`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
declaration.internal_reg_default_init
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-46"></a>
### VG015: Internal non-array reg declaration `cnt_pre_cycles` must be explicitly initialized inside the module; when backfilling a missing initializer, use exact ` = 0;`.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:110`
- Evidence:
- node_kind: `verilog_rtl`
- detail: declaration.internal_reg_default_init
- source_excerpt: `declaration.internal_reg_default_init`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
declaration.internal_reg_default_init
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-47"></a>
### VG015: Internal non-array reg declaration `cnt_silu_cycles` must be explicitly initialized inside the module; when backfilling a missing initializer, use exact ` = 0;`.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:111`
- Evidence:
- node_kind: `verilog_rtl`
- detail: declaration.internal_reg_default_init
- source_excerpt: `declaration.internal_reg_default_init`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
declaration.internal_reg_default_init
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-48"></a>
### VG015: Internal non-array reg declaration `cnt_post_cycles` must be explicitly initialized inside the module; when backfilling a missing initializer, use exact ` = 0;`.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:112`
- Evidence:
- node_kind: `verilog_rtl`
- detail: declaration.internal_reg_default_init
- source_excerpt: `declaration.internal_reg_default_init`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
declaration.internal_reg_default_init
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-49"></a>
### VG015: Internal non-array reg declaration `cnt_writeback_cycles` must be explicitly initialized inside the module; when backfilling a missing initializer, use exact ` = 0;`.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:113`
- Evidence:
- node_kind: `verilog_rtl`
- detail: declaration.internal_reg_default_init
- source_excerpt: `declaration.internal_reg_default_init`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
declaration.internal_reg_default_init
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-50"></a>
### VG013: Flag-like signal `cnt_writeback_cycles` should use `flag_` prefix unless it is an output bridge.
- Status: `failed`
- Severity: `error`
- Location: `file:down2_overlap_tile_runner.v:unknown`
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
### VG015: Internal non-array reg declaration `cnt_storage_wait_cycles` must be explicitly initialized inside the module; when backfilling a missing initializer, use exact ` = 0;`.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:114`
- Evidence:
- node_kind: `verilog_rtl`
- detail: declaration.internal_reg_default_init
- source_excerpt: `declaration.internal_reg_default_init`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
declaration.internal_reg_default_init
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-52"></a>
### VG015: Internal non-array reg declaration `cnt_scheduler_idle_cycles` must be explicitly initialized inside the module; when backfilling a missing initializer, use exact ` = 0;`.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:115`
- Evidence:
- node_kind: `verilog_rtl`
- detail: declaration.internal_reg_default_init
- source_excerpt: `declaration.internal_reg_default_init`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
declaration.internal_reg_default_init
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-53"></a>
### VG015: Internal non-array reg declaration `cnt_export_cycles` must be explicitly initialized inside the module; when backfilling a missing initializer, use exact ` = 0;`.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:116`
- Evidence:
- node_kind: `verilog_rtl`
- detail: declaration.internal_reg_default_init
- source_excerpt: `declaration.internal_reg_default_init`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
declaration.internal_reg_default_init
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-54"></a>
### VG015: Internal non-array reg declaration `cnt_mac_results` must be explicitly initialized inside the module; when backfilling a missing initializer, use exact ` = 0;`.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:117`
- Evidence:
- node_kind: `verilog_rtl`
- detail: declaration.internal_reg_default_init
- source_excerpt: `declaration.internal_reg_default_init`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
declaration.internal_reg_default_init
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-55"></a>
### VG015: Internal non-array reg declaration `cnt_pre_accepts` must be explicitly initialized inside the module; when backfilling a missing initializer, use exact ` = 0;`.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:118`
- Evidence:
- node_kind: `verilog_rtl`
- detail: declaration.internal_reg_default_init
- source_excerpt: `declaration.internal_reg_default_init`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
declaration.internal_reg_default_init
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-56"></a>
### VG015: Internal non-array reg declaration `cnt_silu_accepts` must be explicitly initialized inside the module; when backfilling a missing initializer, use exact ` = 0;`.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:119`
- Evidence:
- node_kind: `verilog_rtl`
- detail: declaration.internal_reg_default_init
- source_excerpt: `declaration.internal_reg_default_init`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
declaration.internal_reg_default_init
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-57"></a>
### VG015: Internal non-array reg declaration `cnt_post_accepts` must be explicitly initialized inside the module; when backfilling a missing initializer, use exact ` = 0;`.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:120`
- Evidence:
- node_kind: `verilog_rtl`
- detail: declaration.internal_reg_default_init
- source_excerpt: `declaration.internal_reg_default_init`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
declaration.internal_reg_default_init
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-58"></a>
### VG015: Internal non-array reg declaration `cnt_writebacks` must be explicitly initialized inside the module; when backfilling a missing initializer, use exact ` = 0;`.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:121`
- Evidence:
- node_kind: `verilog_rtl`
- detail: declaration.internal_reg_default_init
- source_excerpt: `declaration.internal_reg_default_init`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
declaration.internal_reg_default_init
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-59"></a>
### VG013: Flag-like signal `cnt_writebacks` should use `flag_` prefix unless it is an output bridge.
- Status: `failed`
- Severity: `error`
- Location: `file:down2_overlap_tile_runner.v:unknown`
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

<a id="vg-finding-60"></a>
### VG015: Internal non-array reg declaration `cnt_expected_halo` must be explicitly initialized inside the module; when backfilling a missing initializer, use exact ` = 0;`.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:123`
- Evidence:
- node_kind: `verilog_rtl`
- detail: declaration.internal_reg_default_init
- source_excerpt: `declaration.internal_reg_default_init`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
declaration.internal_reg_default_init
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-61"></a>
### VG015: Internal non-array reg declaration `cnt_expected_dw_cache` must be explicitly initialized inside the module; when backfilling a missing initializer, use exact ` = 0;`.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:124`
- Evidence:
- node_kind: `verilog_rtl`
- detail: declaration.internal_reg_default_init
- source_excerpt: `declaration.internal_reg_default_init`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
declaration.internal_reg_default_init
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-62"></a>
### VG015: Internal non-array reg declaration `cnt_expected_dw_weight` must be explicitly initialized inside the module; when backfilling a missing initializer, use exact ` = 0;`.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:125`
- Evidence:
- node_kind: `verilog_rtl`
- detail: declaration.internal_reg_default_init
- source_excerpt: `declaration.internal_reg_default_init`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
declaration.internal_reg_default_init
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-63"></a>
### VG015: Internal non-array reg declaration `cnt_expected_dw_bias` must be explicitly initialized inside the module; when backfilling a missing initializer, use exact ` = 0;`.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:126`
- Evidence:
- node_kind: `verilog_rtl`
- detail: declaration.internal_reg_default_init
- source_excerpt: `declaration.internal_reg_default_init`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
declaration.internal_reg_default_init
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-64"></a>
### VG015: Internal non-array reg declaration `cnt_expected_pw_weight` must be explicitly initialized inside the module; when backfilling a missing initializer, use exact ` = 0;`.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:127`
- Evidence:
- node_kind: `verilog_rtl`
- detail: declaration.internal_reg_default_init
- source_excerpt: `declaration.internal_reg_default_init`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
declaration.internal_reg_default_init
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-65"></a>
### VG015: Internal non-array reg declaration `cnt_expected_pw_bias` must be explicitly initialized inside the module; when backfilling a missing initializer, use exact ` = 0;`.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:128`
- Evidence:
- node_kind: `verilog_rtl`
- detail: declaration.internal_reg_default_init
- source_excerpt: `declaration.internal_reg_default_init`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
declaration.internal_reg_default_init
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-66"></a>
### VG015: Internal non-array reg declaration `flag_halo_loaded` must be explicitly initialized inside the module; when backfilling a missing initializer, use exact ` = 0;`.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:129`
- Evidence:
- node_kind: `verilog_rtl`
- detail: declaration.internal_reg_default_init
- source_excerpt: `declaration.internal_reg_default_init`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
declaration.internal_reg_default_init
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-67"></a>
### VG015: Internal non-array reg declaration `flag_dw_cache_loaded` must be explicitly initialized inside the module; when backfilling a missing initializer, use exact ` = 0;`.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:130`
- Evidence:
- node_kind: `verilog_rtl`
- detail: declaration.internal_reg_default_init
- source_excerpt: `declaration.internal_reg_default_init`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
declaration.internal_reg_default_init
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-68"></a>
### VG015: Internal non-array reg declaration `flag_dw_weight_loaded` must be explicitly initialized inside the module; when backfilling a missing initializer, use exact ` = 0;`.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:131`
- Evidence:
- node_kind: `verilog_rtl`
- detail: declaration.internal_reg_default_init
- source_excerpt: `declaration.internal_reg_default_init`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
declaration.internal_reg_default_init
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-69"></a>
### VG015: Internal non-array reg declaration `flag_dw_bias_loaded` must be explicitly initialized inside the module; when backfilling a missing initializer, use exact ` = 0;`.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:132`
- Evidence:
- node_kind: `verilog_rtl`
- detail: declaration.internal_reg_default_init
- source_excerpt: `declaration.internal_reg_default_init`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
declaration.internal_reg_default_init
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-70"></a>
### VG015: Internal non-array reg declaration `flag_pw_weight_loaded` must be explicitly initialized inside the module; when backfilling a missing initializer, use exact ` = 0;`.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:133`
- Evidence:
- node_kind: `verilog_rtl`
- detail: declaration.internal_reg_default_init
- source_excerpt: `declaration.internal_reg_default_init`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
declaration.internal_reg_default_init
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-71"></a>
### VG015: Internal non-array reg declaration `flag_pw_bias_loaded` must be explicitly initialized inside the module; when backfilling a missing initializer, use exact ` = 0;`.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:134`
- Evidence:
- node_kind: `verilog_rtl`
- detail: declaration.internal_reg_default_init
- source_excerpt: `declaration.internal_reg_default_init`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
declaration.internal_reg_default_init
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-72"></a>
### VG013: Flag-like signal `mac_input_ready` should use `flag_` prefix unless it is an output bridge.
- Status: `failed`
- Severity: `error`
- Location: `file:down2_overlap_tile_runner.v:unknown`
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

<a id="vg-finding-73"></a>
### VG013: Flag-like signal `mac_result_valid` should use `flag_` prefix unless it is an output bridge.
- Status: `failed`
- Severity: `error`
- Location: `file:down2_overlap_tile_runner.v:unknown`
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

<a id="vg-finding-74"></a>
### VG013: Flag-like signal `pp_input_ready` should use `flag_` prefix unless it is an output bridge.
- Status: `failed`
- Severity: `error`
- Location: `file:down2_overlap_tile_runner.v:unknown`
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

<a id="vg-finding-75"></a>
### VG013: Flag-like signal `pp_output_valid` should use `flag_` prefix unless it is an output bridge.
- Status: `failed`
- Severity: `error`
- Location: `file:down2_overlap_tile_runner.v:unknown`
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

<a id="vg-finding-76"></a>
### VG013: Counter-like signal `pp_result_queue_count` should use `cnt_` prefix.
- Status: `failed`
- Severity: `error`
- Location: `file:down2_overlap_tile_runner.v:unknown`
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

<a id="vg-finding-77"></a>
### VG013: Counter-like signal `pp_meta_count` should use `cnt_` prefix.
- Status: `failed`
- Severity: `error`
- Location: `file:down2_overlap_tile_runner.v:unknown`
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

<a id="vg-finding-78"></a>
### VG013: Flag-like signal `pp_table_ready` should use `flag_` prefix unless it is an output bridge.
- Status: `failed`
- Severity: `error`
- Location: `file:down2_overlap_tile_runner.v:unknown`
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

<a id="vg-finding-79"></a>
### VG020: Always block `always@(*)` assigns multiple targets ['halo_index', 'kernel_index', 'next_mac_activation', 'next_mac_bias', 'next_mac_mask', 'next_mac_weight', 'output_channel', 'weight_index']; split to one target per always.
- Status: `failed`
- Severity: `error`
- Location: `file:down2_overlap_tile_runner.v:unknown`
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

<a id="vg-finding-80"></a>
### VG020: Always block `always@(*)` has complex lvalues and multiple targets; formatter must not guess a split.
- Status: `failed`
- Severity: `error`
- Location: `file:down2_overlap_tile_runner.v:unknown`
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

<a id="vg-finding-81"></a>
### VG020: Always block `always@(posedge i_clk or negedge i_rstn)` assigns multiple targets ['cnt_dw_writes', 'cnt_export', 'cnt_mac_group', 'cnt_output', 'cnt_position', 'cnt_pw_writes', 'flag_busy_o', 'flag_debug_layer_o', 'flag_debug_valid_o', 'flag_done_o', 'flag_export_done_o', 'flag_fault_o', 'flag_layer_pw', 'flag_result_reserved', 'flag_tile_valid', 'reg_debug_channel_o', 'reg_debug_phase_o', 'reg_debug_position_o', 'reg_debug_value_o', 'reg_mac_activation', 'reg_mac_bias', 'reg_mac_mask', 'reg_mac_weight', 'state_current']; split to one target per always.
- Status: `failed`
- Severity: `error`
- Location: `file:down2_overlap_tile_runner.v:unknown`
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

<a id="vg-finding-82"></a>
### VG020: Always block `always@(posedge i_clk or negedge i_rstn)` assigns multiple targets ['cnt_expected_dw_bias', 'cnt_expected_dw_cache', 'cnt_expected_dw_weight', 'cnt_expected_halo', 'cnt_expected_pw_bias', 'cnt_expected_pw_weight', 'cnt_preload_writes', 'flag_dw_bias_loaded', 'flag_dw_cache_loaded', 'flag_dw_weight_loaded', 'flag_halo_loaded', 'flag_load_fault', 'flag_pw_bias_loaded', 'flag_pw_weight_loaded', 'reg_dw_bias', 'reg_dw_cache', 'reg_dw_weight', 'reg_halo', 'reg_output_cache', 'reg_pw_bias', 'reg_pw_weight']; split to one target per always.
- Status: `failed`
- Severity: `error`
- Location: `file:down2_overlap_tile_runner.v:unknown`
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

<a id="vg-finding-83"></a>
### VG020: Always block `always@(posedge i_clk or negedge i_rstn)` has complex lvalues and multiple targets; formatter must not guess a split.
- Status: `failed`
- Severity: `error`
- Location: `file:down2_overlap_tile_runner.v:unknown`
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

<a id="vg-finding-84"></a>
### VG020: Always block `always@(posedge i_clk or negedge i_rstn)` assigns multiple targets ['cnt_core_cycles', 'cnt_export_cycles', 'cnt_mac_cycles', 'cnt_mac_results', 'cnt_post_accepts', 'cnt_post_cycles', 'cnt_pre_accepts', 'cnt_pre_cycles', 'cnt_scheduler_idle_cycles', 'cnt_silu_accepts', 'cnt_silu_cycles', 'cnt_storage_wait_cycles', 'cnt_writeback_cycles', 'cnt_writebacks']; split to one target per always.
- Status: `failed`
- Severity: `error`
- Location: `file:down2_overlap_tile_runner.v:unknown`
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

<a id="vg-finding-85"></a>
### VG023: FSM must use `state_current` and `state_next` signals.
- Status: `failed`
- Severity: `error`
- Location: `file:down2_overlap_tile_runner.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: fsm.three_segment
- source_excerpt: `fsm.three_segment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
fsm.three_segment
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-86"></a>
### VG023: FSM must be generated as at least state-register and next-state combinational blocks.
- Status: `failed`
- Severity: `error`
- Location: `file:down2_overlap_tile_runner.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: fsm.three_segment
- source_excerpt: `fsm.three_segment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `architecture`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
fsm.three_segment
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-87"></a>
### VG054: FSM delivery must keep separate state-register and next-state combinational blocks.
- Status: `failed`
- Severity: `error`
- Location: `file:down2_overlap_tile_runner.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: fsm.strict_three_segment
- source_excerpt: `fsm.strict_three_segment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `architecture`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
fsm.strict_three_segment
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-88"></a>
### VG031: Non-trivial RTL must use fixed Erie region banners.
- Status: `failed`
- Severity: `error`
- Location: `file:down2_overlap_tile_runner.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: regions.banner
- source_excerpt: `regions.banner`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
regions.banner
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-89"></a>
### VG040: localparam `ST_IDLE` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:57`
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

<a id="vg-finding-90"></a>
### VG040: localparam `ST_STORAGE` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:58`
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

<a id="vg-finding-91"></a>
### VG040: localparam `ST_MAC_SEND` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:59`
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

<a id="vg-finding-92"></a>
### VG040: localparam `ST_MAC_WAIT` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:60`
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

<a id="vg-finding-93"></a>
### VG040: localparam `ST_DW_DRAIN` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:61`
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

<a id="vg-finding-94"></a>
### VG040: localparam `ST_PW_DRAIN` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:62`
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

<a id="vg-finding-95"></a>
### VG040: localparam `ST_DONE` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:63`
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

<a id="vg-finding-96"></a>
### VG040: localparam `ST_FAULT` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:64`
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

<a id="vg-finding-97"></a>
### VG040: localparam `ST_EXPORT` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:65`
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

<a id="vg-finding-98"></a>
### VG040: port `i_clk` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:6`
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

<a id="vg-finding-99"></a>
### VG040: port `i_rstn` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:7`
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

<a id="vg-finding-100"></a>
### VG040: port `i_table_valid` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:8`
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

<a id="vg-finding-101"></a>
### VG040: port `i_table_addr` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:9`
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

<a id="vg-finding-102"></a>
### VG040: port `i_table_data` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:10`
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

<a id="vg-finding-103"></a>
### VG040: port `o_table_ready` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:11`
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

<a id="vg-finding-104"></a>
### VG040: port `o_table_loaded` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:12`
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

<a id="vg-finding-105"></a>
### VG040: port `o_table_fault` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:13`
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

<a id="vg-finding-106"></a>
### VG040: port `i_load_valid` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:14`
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
### VG040: port `i_load_kind` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:15`
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
### VG040: port `i_load_addr` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:16`
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
### VG040: port `i_load_data` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:17`
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
### VG040: port `o_load_ready` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:18`
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
### VG040: port `i_start` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:19`
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
### VG040: port `i_pw_only` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:20`
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
### VG040: port `i_commit_ready` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:21`
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
### VG040: port `o_busy` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:22`
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
### VG040: port `o_done` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:23`
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
### VG040: port `o_fault` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:24`
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
### VG040: port `i_export_start` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:25`
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
### VG040: port `i_output_ready` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:26`
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
### VG040: port `o_output_valid` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:27`
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
### VG040: port `o_output_data` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:28`
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
### VG040: port `o_output_index` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:29`
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
### VG040: port `o_export_done` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:30`
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
### VG040: port `o_debug_valid` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:31`
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
### VG040: port `o_debug_phase` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:32`
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
### VG040: port `o_debug_layer` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:33`
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
### VG040: port `o_debug_position` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:34`
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
### VG040: port `o_debug_channel` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:35`
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
### VG040: port `o_debug_value` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:36`
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
### VG040: port `o_preload_writes` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:37`
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
### VG040: port `o_core_cycles` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:38`
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
### VG040: port `o_mac_cycles` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:39`
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
### VG040: port `o_pre_cycles` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:40`
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
### VG040: port `o_silu_cycles` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:41`
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
### VG040: port `o_post_cycles` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:42`
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
### VG040: port `o_writeback_cycles` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:43`
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
### VG040: port `o_storage_wait_cycles` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:44`
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
### VG040: port `o_scheduler_idle_cycles` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:45`
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
### VG040: port `o_export_cycles` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:46`
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
### VG040: port `o_result_queue_count` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:47`
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
### VG040: port `o_result_reserved` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:48`
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
### VG040: port `o_meta_count` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:49`
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
### VG040: port `o_mac_result_count` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:50`
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
### VG040: port `o_pre_accept_count` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:51`
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
### VG040: port `o_silu_accept_count` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:52`
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
### VG040: port `o_post_accept_count` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:53`
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
### VG040: port `o_writeback_count` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:54`
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
### VG040: signal `reg_halo` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:67`
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
### VG040: signal `reg_dw_cache` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:68`
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
### VG040: signal `reg_output_cache` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:69`
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
### VG040: signal `reg_dw_weight` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:70`
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
### VG040: signal `reg_dw_bias` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:71`
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
### VG040: signal `reg_pw_weight` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:72`
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
### VG040: signal `reg_pw_bias` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:73`
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
### VG040: signal `state_current` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:75`
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
### VG040: signal `flag_layer_pw` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:76`
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
### VG040: signal `flag_busy_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:77`
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
### VG040: signal `flag_done_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:78`
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
### VG040: signal `flag_fault_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:79`
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
### VG040: signal `flag_load_fault` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:80`
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
### VG040: signal `flag_tile_valid` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:81`
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
### VG040: signal `flag_export_done_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:82`
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
### VG040: signal `flag_result_reserved` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:83`
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
### VG040: signal `cnt_position` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:84`
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
### VG040: signal `cnt_output` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:85`
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
### VG040: signal `cnt_mac_group` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:86`
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
### VG040: signal `cnt_export` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:87`
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
### VG040: signal `cnt_dw_writes` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:88`
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
### VG040: signal `cnt_pw_writes` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:89`
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
### VG040: signal `reg_mac_activation` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:91`
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
### VG040: signal `reg_mac_weight` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:92`
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
### VG040: signal `reg_mac_bias` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:93`
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
### VG040: signal `reg_mac_mask` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:94`
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
### VG040: signal `next_mac_activation` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:95`
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
### VG040: signal `next_mac_weight` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:96`
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
### VG040: signal `next_mac_bias` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:97`
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
### VG040: signal `next_mac_mask` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:98`
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
### VG040: signal `flag_debug_valid_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:100`
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
### VG040: signal `reg_debug_phase_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:101`
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
### VG040: signal `flag_debug_layer_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:102`
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
### VG040: signal `reg_debug_position_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:103`
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
### VG040: signal `reg_debug_channel_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:104`
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
### VG040: signal `reg_debug_value_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:105`
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
### VG040: signal `cnt_preload_writes` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:107`
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
### VG040: signal `cnt_core_cycles` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:108`
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
### VG040: signal `cnt_mac_cycles` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:109`
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
### VG040: signal `cnt_pre_cycles` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:110`
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
### VG040: signal `cnt_silu_cycles` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:111`
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
### VG040: signal `cnt_post_cycles` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:112`
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
### VG040: signal `cnt_writeback_cycles` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:113`
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
### VG040: signal `cnt_storage_wait_cycles` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:114`
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
### VG040: signal `cnt_scheduler_idle_cycles` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:115`
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

<a id="vg-finding-192"></a>
### VG040: signal `cnt_export_cycles` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:116`
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

<a id="vg-finding-193"></a>
### VG040: signal `cnt_mac_results` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:117`
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

<a id="vg-finding-194"></a>
### VG040: signal `cnt_pre_accepts` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:118`
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

<a id="vg-finding-195"></a>
### VG040: signal `cnt_silu_accepts` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:119`
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

<a id="vg-finding-196"></a>
### VG040: signal `cnt_post_accepts` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:120`
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

<a id="vg-finding-197"></a>
### VG040: signal `cnt_writebacks` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:121`
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

<a id="vg-finding-198"></a>
### VG040: signal `cnt_expected_halo` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:123`
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

<a id="vg-finding-199"></a>
### VG040: signal `cnt_expected_dw_cache` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:124`
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

<a id="vg-finding-200"></a>
### VG040: signal `cnt_expected_dw_weight` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:125`
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

<a id="vg-finding-201"></a>
### VG040: signal `cnt_expected_dw_bias` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:126`
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

<a id="vg-finding-202"></a>
### VG040: signal `cnt_expected_pw_weight` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:127`
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

<a id="vg-finding-203"></a>
### VG040: signal `cnt_expected_pw_bias` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:128`
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

<a id="vg-finding-204"></a>
### VG040: signal `flag_halo_loaded` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:129`
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

<a id="vg-finding-205"></a>
### VG040: signal `flag_dw_cache_loaded` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:130`
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

<a id="vg-finding-206"></a>
### VG040: signal `flag_dw_weight_loaded` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:131`
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

<a id="vg-finding-207"></a>
### VG040: signal `flag_dw_bias_loaded` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:132`
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

<a id="vg-finding-208"></a>
### VG040: signal `flag_pw_weight_loaded` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:133`
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

<a id="vg-finding-209"></a>
### VG040: signal `flag_pw_bias_loaded` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:134`
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

<a id="vg-finding-210"></a>
### VG040: signal `mac_input_ready` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:136`
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

<a id="vg-finding-211"></a>
### VG040: signal `mac_result_valid` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:137`
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

<a id="vg-finding-212"></a>
### VG040: signal `mac_result_data` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:138`
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

<a id="vg-finding-213"></a>
### VG040: signal `mac_fault` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:139`
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

<a id="vg-finding-214"></a>
### VG040: signal `flag_mac_input_valid` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:140`
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

<a id="vg-finding-215"></a>
### VG040: signal `flag_mac_input_accept` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:141`
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

<a id="vg-finding-216"></a>
### VG040: signal `flag_mac_result_ready_local` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:142`
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

<a id="vg-finding-217"></a>
### VG040: signal `flag_mac_result_accept` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:143`
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

<a id="vg-finding-218"></a>
### VG040: signal `flag_can_reserve` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:144`
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

<a id="vg-finding-219"></a>
### VG040: signal `wire_capacity_used` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:145`
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

<a id="vg-finding-220"></a>
### VG040: signal `pp_input_ready` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:147`
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

<a id="vg-finding-221"></a>
### VG040: signal `pp_output_valid` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:148`
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

<a id="vg-finding-222"></a>
### VG040: signal `pp_output_data` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:149`
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

<a id="vg-finding-223"></a>
### VG040: signal `pp_output_tag` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:150`
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

<a id="vg-finding-224"></a>
### VG040: signal `pp_fault` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:151`
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

<a id="vg-finding-225"></a>
### VG040: signal `pp_result_queue_count` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:152`
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

<a id="vg-finding-226"></a>
### VG040: signal `pp_meta_count` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:153`
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

<a id="vg-finding-227"></a>
### VG040: signal `pp_pre_busy` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:154`
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

<a id="vg-finding-228"></a>
### VG040: signal `pp_silu_busy` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:155`
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

<a id="vg-finding-229"></a>
### VG040: signal `pp_post_busy` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:156`
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

<a id="vg-finding-230"></a>
### VG040: signal `pp_pre_accept` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:157`
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

<a id="vg-finding-231"></a>
### VG040: signal `pp_silu_accept` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:158`
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

<a id="vg-finding-232"></a>
### VG040: signal `pp_post_accept` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:159`
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

<a id="vg-finding-233"></a>
### VG040: signal `pp_table_ready` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:160`
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

<a id="vg-finding-234"></a>
### VG040: signal `pp_table_loaded` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:161`
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

<a id="vg-finding-235"></a>
### VG040: signal `pp_table_fault` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:162`
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

<a id="vg-finding-236"></a>
### VG040: signal `flag_commit_accept` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:163`
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

<a id="vg-finding-237"></a>
### VG040: signal `wire_pw_group_base` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:165`
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

<a id="vg-finding-238"></a>
### VG040: signal `wire_dw_lane` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:166`
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

<a id="vg-finding-239"></a>
### VG040: signal `wire_dw_channel_base` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:167`
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

<a id="vg-finding-240"></a>
### VG040: signal `wire_result_lane_mask` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:168`
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

<a id="vg-finding-241"></a>
### VG040: signal `wire_result_channel_base` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:169`
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

<a id="vg-finding-242"></a>
### VG040: signal `flag_table_enable` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:170`
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

<a id="vg-finding-243"></a>
### VG040: signal `flag_load_accept` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:171`
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

<a id="vg-finding-244"></a>
### VG040: signal `flag_output_accept` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:172`
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

<a id="vg-finding-245"></a>
### VG040: signal `flag_start_accept` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:173`
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

<a id="vg-finding-246"></a>
### VG040: signal `lane_index` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:175`
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

<a id="vg-finding-247"></a>
### VG040: signal `kernel_index` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:176`
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

<a id="vg-finding-248"></a>
### VG040: signal `halo_index` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:177`
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

<a id="vg-finding-249"></a>
### VG040: signal `weight_index` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:178`
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

<a id="vg-finding-250"></a>
### VG040: signal `output_channel` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:179`
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

<a id="vg-finding-251"></a>
### VG040: assign `wire_pw_group_base` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:181`
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

<a id="vg-finding-252"></a>
### VG040: assign `wire_dw_lane` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:182`
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

<a id="vg-finding-253"></a>
### VG040: assign `wire_dw_channel_base` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:188`
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

<a id="vg-finding-254"></a>
### VG040: assign `wire_result_lane_mask` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:189`
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

<a id="vg-finding-255"></a>
### VG040: assign `wire_result_channel_base` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:190`
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

<a id="vg-finding-256"></a>
### VG040: assign `wire_capacity_used` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:191`
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

<a id="vg-finding-257"></a>
### VG040: assign `flag_can_reserve` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:192`
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

<a id="vg-finding-258"></a>
### VG040: assign `flag_mac_input_valid` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:193`
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

<a id="vg-finding-259"></a>
### VG040: assign `flag_mac_input_accept` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:194`
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

<a id="vg-finding-260"></a>
### VG040: assign `flag_mac_result_ready_local` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:195`
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

<a id="vg-finding-261"></a>
### VG040: assign `flag_mac_result_accept` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:197`
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

<a id="vg-finding-262"></a>
### VG040: assign `flag_commit_accept` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:198`
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

<a id="vg-finding-263"></a>
### VG040: assign `flag_table_enable` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:199`
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

<a id="vg-finding-264"></a>
### VG040: assign `flag_load_accept` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:200`
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

<a id="vg-finding-265"></a>
### VG040: assign `flag_output_accept` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:201`
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

<a id="vg-finding-266"></a>
### VG040: assign `flag_start_accept` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:202`
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

<a id="vg-finding-267"></a>
### VG040: assign `o_table_ready` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:208`
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

<a id="vg-finding-268"></a>
### VG040: assign `o_table_loaded` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:209`
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

<a id="vg-finding-269"></a>
### VG040: assign `o_table_fault` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:210`
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

<a id="vg-finding-270"></a>
### VG040: assign `o_load_ready` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:211`
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

<a id="vg-finding-271"></a>
### VG040: assign `o_busy` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:213`
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

<a id="vg-finding-272"></a>
### VG040: assign `o_done` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:214`
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

<a id="vg-finding-273"></a>
### VG040: assign `o_fault` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:215`
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

<a id="vg-finding-274"></a>
### VG040: assign `o_output_valid` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:216`
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

<a id="vg-finding-275"></a>
### VG040: assign `o_output_data` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:217`
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

<a id="vg-finding-276"></a>
### VG040: assign `o_output_index` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:218`
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

<a id="vg-finding-277"></a>
### VG040: assign `o_export_done` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:219`
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

<a id="vg-finding-278"></a>
### VG040: assign `o_debug_valid` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:220`
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

<a id="vg-finding-279"></a>
### VG040: assign `o_debug_phase` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:221`
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

<a id="vg-finding-280"></a>
### VG040: assign `o_debug_layer` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:222`
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

<a id="vg-finding-281"></a>
### VG040: assign `o_debug_position` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:223`
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

<a id="vg-finding-282"></a>
### VG040: assign `o_debug_channel` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:224`
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

<a id="vg-finding-283"></a>
### VG040: assign `o_debug_value` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:225`
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

<a id="vg-finding-284"></a>
### VG040: assign `o_preload_writes` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:226`
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

<a id="vg-finding-285"></a>
### VG040: assign `o_core_cycles` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:227`
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

<a id="vg-finding-286"></a>
### VG040: assign `o_mac_cycles` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:228`
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

<a id="vg-finding-287"></a>
### VG040: assign `o_pre_cycles` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:229`
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

<a id="vg-finding-288"></a>
### VG040: assign `o_silu_cycles` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:230`
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

<a id="vg-finding-289"></a>
### VG040: assign `o_post_cycles` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:231`
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

<a id="vg-finding-290"></a>
### VG040: assign `o_writeback_cycles` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:232`
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

<a id="vg-finding-291"></a>
### VG040: assign `o_storage_wait_cycles` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:233`
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

<a id="vg-finding-292"></a>
### VG040: assign `o_scheduler_idle_cycles` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:234`
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

<a id="vg-finding-293"></a>
### VG040: assign `o_export_cycles` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:235`
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

<a id="vg-finding-294"></a>
### VG040: assign `o_result_queue_count` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:236`
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

<a id="vg-finding-295"></a>
### VG040: assign `o_result_reserved` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:237`
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

<a id="vg-finding-296"></a>
### VG040: assign `o_meta_count` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:238`
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

<a id="vg-finding-297"></a>
### VG040: assign `o_mac_result_count` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:239`
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

<a id="vg-finding-298"></a>
### VG040: assign `o_pre_accept_count` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:240`
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

<a id="vg-finding-299"></a>
### VG040: assign `o_silu_accept_count` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:241`
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

<a id="vg-finding-300"></a>
### VG040: assign `o_post_accept_count` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:242`
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

<a id="vg-finding-301"></a>
### VG040: assign `o_writeback_count` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:243`
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

<a id="vg-finding-302"></a>
### VG040: Always block `always@(*)` should have a nearby leading comment explaining behavior.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:245`
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

<a id="vg-finding-303"></a>
### VG040: Always block `always@(posedge i_clk or negedge i_rstn)` should have a nearby leading comment explaining behavior.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:290`
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

<a id="vg-finding-304"></a>
### VG040: Always block `always@(posedge i_clk or negedge i_rstn)` should have a nearby leading comment explaining behavior.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:466`
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

<a id="vg-finding-305"></a>
### VG040: Always block `always@(posedge i_clk or negedge i_rstn)` should have a nearby leading comment explaining behavior.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:553`
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

<a id="vg-finding-306"></a>
### VG040: Instance `road_mac_probe_Inst_tile` should have a leading function/connection comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:614`
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

<a id="vg-finding-307"></a>
### VG040: Instance `road_postprocess_stream_Inst_tile` should have a leading function/connection comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:631`
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

<a id="vg-finding-308"></a>
### VG062: process assignment `next_mac_activation` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:246`
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
### VG062: process assignment `next_mac_weight` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:247`
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
### VG062: process assignment `next_mac_bias` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:248`
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
### VG062: process assignment `next_mac_mask` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:249`
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
### VG062: process assignment `kernel_index` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:250`
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
### VG062: process assignment `halo_index` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:251`
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
### VG062: process assignment `weight_index` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:252`
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
### VG062: process assignment `output_channel` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:253`
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
### VG062: process assignment `kernel_index` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:256`
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
### VG062: process assignment `next_mac_activation[lane_index * 8 +:8]` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:260`
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
### VG062: process assignment `next_mac_mask[lane_index]` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:261`
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
### VG062: process assignment `weight_index` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:262`
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
### VG062: process assignment `2'd0: next_mac_weight[lane_index * 8 +:8]` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:264`
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
### VG062: process assignment `2'd1: next_mac_weight[64 + lane_index * 8 +:8]` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:265`
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
### VG062: process assignment `default: next_mac_weight[128 + lane_index * 8 +:8]` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:266`
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
### VG062: process assignment `2'd0: next_mac_bias[31:0]` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:271`
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
### VG062: process assignment `2'd1: next_mac_bias[63:32]` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:272`
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
### VG062: process assignment `default: next_mac_bias[95:64]` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:273`
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
### VG062: process assignment `next_mac_activation[lane_index * 8 +:8]` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:277`
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
### VG062: process assignment `next_mac_mask[lane_index]` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:278`
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
### VG062: process assignment `output_channel` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:279`
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
### VG062: process assignment `next_mac_weight[lane_index * 8 +:8]` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:280`
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
### VG062: process assignment `next_mac_weight[64 + lane_index * 8 +:8]` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:281`
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
### VG062: process assignment `next_mac_weight[128 + lane_index * 8 +:8]` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:282`
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
### VG062: process assignment `next_mac_bias[31:0]` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:284`
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
### VG062: process assignment `next_mac_bias[63:32]` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:285`
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
### VG062: process assignment `next_mac_bias[95:64]` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:286`
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
### VG062: process assignment `state_current` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:292`
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
### VG062: process assignment `flag_layer_pw` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:293`
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
### VG062: process assignment `flag_busy_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:294`
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
### VG062: process assignment `flag_done_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:295`
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
### VG062: process assignment `flag_fault_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:296`
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
### VG062: process assignment `flag_tile_valid` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:297`
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
### VG062: process assignment `flag_export_done_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:298`
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
### VG062: process assignment `flag_result_reserved` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:299`
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
### VG062: process assignment `cnt_position` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:300`
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
### VG062: process assignment `cnt_output` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:301`
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

<a id="vg-finding-345"></a>
### VG062: process assignment `cnt_mac_group` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:302`
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

<a id="vg-finding-346"></a>
### VG062: process assignment `cnt_export` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:303`
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

<a id="vg-finding-347"></a>
### VG062: process assignment `cnt_dw_writes` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:304`
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

<a id="vg-finding-348"></a>
### VG062: process assignment `cnt_pw_writes` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:305`
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

<a id="vg-finding-349"></a>
### VG062: process assignment `reg_mac_activation` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:306`
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

<a id="vg-finding-350"></a>
### VG062: process assignment `reg_mac_weight` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:307`
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

<a id="vg-finding-351"></a>
### VG062: process assignment `reg_mac_bias` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:308`
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

<a id="vg-finding-352"></a>
### VG062: process assignment `reg_mac_mask` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:309`
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

<a id="vg-finding-353"></a>
### VG062: process assignment `flag_debug_valid_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:310`
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

<a id="vg-finding-354"></a>
### VG062: process assignment `reg_debug_phase_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:311`
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

<a id="vg-finding-355"></a>
### VG062: process assignment `flag_debug_layer_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:312`
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

<a id="vg-finding-356"></a>
### VG062: process assignment `reg_debug_position_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:313`
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

<a id="vg-finding-357"></a>
### VG062: process assignment `reg_debug_channel_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:314`
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

<a id="vg-finding-358"></a>
### VG062: process assignment `reg_debug_value_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:315`
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

<a id="vg-finding-359"></a>
### VG062: process assignment `flag_done_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:317`
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

<a id="vg-finding-360"></a>
### VG062: process assignment `flag_export_done_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:318`
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

<a id="vg-finding-361"></a>
### VG062: process assignment `flag_debug_valid_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:319`
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

<a id="vg-finding-362"></a>
### VG062: process assignment `flag_busy_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:321`
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

<a id="vg-finding-363"></a>
### VG062: process assignment `flag_fault_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:322`
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

<a id="vg-finding-364"></a>
### VG062: process assignment `flag_tile_valid` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:323`
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

<a id="vg-finding-365"></a>
### VG062: process assignment `flag_result_reserved` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:324`
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

<a id="vg-finding-366"></a>
### VG062: process assignment `state_current` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:325`
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

<a id="vg-finding-367"></a>
### VG062: process assignment `flag_debug_valid_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:328`
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

<a id="vg-finding-368"></a>
### VG062: process assignment `reg_debug_phase_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:329`
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

<a id="vg-finding-369"></a>
### VG062: process assignment `flag_debug_layer_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:330`
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

<a id="vg-finding-370"></a>
### VG062: process assignment `reg_debug_position_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:331`
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

<a id="vg-finding-371"></a>
### VG062: process assignment `reg_debug_channel_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:332`
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

<a id="vg-finding-372"></a>
### VG062: process assignment `reg_debug_value_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:333`
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

<a id="vg-finding-373"></a>
### VG062: process assignment `cnt_pw_writes` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:335`
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

<a id="vg-finding-374"></a>
### VG062: process assignment `cnt_dw_writes` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:337`
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

<a id="vg-finding-375"></a>
### VG062: process assignment `flag_layer_pw` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:343`
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

<a id="vg-finding-376"></a>
### VG062: process assignment `flag_busy_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:344`
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

<a id="vg-finding-377"></a>
### VG062: process assignment `flag_fault_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:345`
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

<a id="vg-finding-378"></a>
### VG062: process assignment `flag_tile_valid` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:346`
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

<a id="vg-finding-379"></a>
### VG062: process assignment `flag_result_reserved` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:347`
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

<a id="vg-finding-380"></a>
### VG062: process assignment `cnt_position` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:348`
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

<a id="vg-finding-381"></a>
### VG062: process assignment `cnt_output` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:349`
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

<a id="vg-finding-382"></a>
### VG062: process assignment `cnt_mac_group` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:350`
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

<a id="vg-finding-383"></a>
### VG062: process assignment `cnt_dw_writes` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:351`
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

<a id="vg-finding-384"></a>
### VG062: process assignment `cnt_pw_writes` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:352`
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

<a id="vg-finding-385"></a>
### VG062: process assignment `state_current` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:353`
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

<a id="vg-finding-386"></a>
### VG062: process assignment `cnt_export` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:355`
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

<a id="vg-finding-387"></a>
### VG062: process assignment `state_current` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:356`
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

<a id="vg-finding-388"></a>
### VG062: process assignment `reg_mac_activation` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:360`
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

<a id="vg-finding-389"></a>
### VG062: process assignment `reg_mac_weight` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:361`
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

<a id="vg-finding-390"></a>
### VG062: process assignment `reg_mac_bias` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:362`
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

<a id="vg-finding-391"></a>
### VG062: process assignment `reg_mac_mask` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:363`
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

<a id="vg-finding-392"></a>
### VG062: process assignment `state_current` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:364`
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

<a id="vg-finding-393"></a>
### VG062: process assignment `flag_result_reserved` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:369`
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

<a id="vg-finding-394"></a>
### VG062: process assignment `cnt_mac_group` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:370`
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

<a id="vg-finding-395"></a>
### VG062: process assignment `state_current` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:371`
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

<a id="vg-finding-396"></a>
### VG062: process assignment `state_current` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:373`
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

<a id="vg-finding-397"></a>
### VG062: process assignment `flag_result_reserved` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:379`
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

<a id="vg-finding-398"></a>
### VG062: process assignment `flag_debug_valid_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:380`
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

<a id="vg-finding-399"></a>
### VG062: process assignment `reg_debug_phase_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:381`
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

<a id="vg-finding-400"></a>
### VG062: process assignment `flag_debug_layer_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:382`
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

<a id="vg-finding-401"></a>
### VG062: process assignment `reg_debug_position_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:383`
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

<a id="vg-finding-402"></a>
### VG062: process assignment `reg_debug_channel_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:384`
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

<a id="vg-finding-403"></a>
### VG062: process assignment `reg_debug_value_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:385`
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

<a id="vg-finding-404"></a>
### VG062: process assignment `cnt_mac_group` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:386`
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

<a id="vg-finding-405"></a>
### VG062: process assignment `flag_busy_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:388`
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

<a id="vg-finding-406"></a>
### VG062: process assignment `flag_fault_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:389`
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

<a id="vg-finding-407"></a>
### VG062: process assignment `flag_tile_valid` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:390`
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

<a id="vg-finding-408"></a>
### VG062: process assignment `state_current` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:391`
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

<a id="vg-finding-409"></a>
### VG062: process assignment `cnt_output` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:394`
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

<a id="vg-finding-410"></a>
### VG062: process assignment `state_current` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:395`
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

<a id="vg-finding-411"></a>
### VG062: process assignment `cnt_position` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:397`
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

<a id="vg-finding-412"></a>
### VG062: process assignment `cnt_output` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:398`
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

<a id="vg-finding-413"></a>
### VG062: process assignment `state_current` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:399`
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

<a id="vg-finding-414"></a>
### VG062: process assignment `state_current` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:401`
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

<a id="vg-finding-415"></a>
### VG062: process assignment `cnt_output` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:405`
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

<a id="vg-finding-416"></a>
### VG062: process assignment `state_current` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:406`
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

<a id="vg-finding-417"></a>
### VG062: process assignment `cnt_position` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:408`
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

<a id="vg-finding-418"></a>
### VG062: process assignment `cnt_output` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:409`
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

<a id="vg-finding-419"></a>
### VG062: process assignment `state_current` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:410`
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

<a id="vg-finding-420"></a>
### VG062: process assignment `state_current` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:412`
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

<a id="vg-finding-421"></a>
### VG062: process assignment `flag_layer_pw` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:419`
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

<a id="vg-finding-422"></a>
### VG062: process assignment `cnt_position` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:420`
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

<a id="vg-finding-423"></a>
### VG062: process assignment `cnt_output` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:421`
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

<a id="vg-finding-424"></a>
### VG062: process assignment `cnt_mac_group` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:422`
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

<a id="vg-finding-425"></a>
### VG062: process assignment `state_current` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:423`
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

<a id="vg-finding-426"></a>
### VG062: process assignment `state_current` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:428`
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

<a id="vg-finding-427"></a>
### VG062: process assignment `flag_busy_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:432`
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

<a id="vg-finding-428"></a>
### VG062: process assignment `flag_done_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:433`
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

<a id="vg-finding-429"></a>
### VG062: process assignment `flag_tile_valid` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:434`
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

<a id="vg-finding-430"></a>
### VG062: process assignment `state_current` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:435`
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

<a id="vg-finding-431"></a>
### VG062: process assignment `flag_busy_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:438`
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

<a id="vg-finding-432"></a>
### VG062: process assignment `flag_fault_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:439`
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

<a id="vg-finding-433"></a>
### VG062: process assignment `flag_tile_valid` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:440`
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

<a id="vg-finding-434"></a>
### VG062: process assignment `flag_result_reserved` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:441`
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

<a id="vg-finding-435"></a>
### VG062: process assignment `state_current` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:442`
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

<a id="vg-finding-436"></a>
### VG062: process assignment `flag_export_done_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:447`
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

<a id="vg-finding-437"></a>
### VG062: process assignment `state_current` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:448`
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

<a id="vg-finding-438"></a>
### VG062: process assignment `cnt_export` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:450`
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

<a id="vg-finding-439"></a>
### VG062: process assignment `flag_busy_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:455`
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

<a id="vg-finding-440"></a>
### VG062: process assignment `flag_fault_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:456`
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

<a id="vg-finding-441"></a>
### VG062: process assignment `flag_tile_valid` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:457`
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

<a id="vg-finding-442"></a>
### VG062: process assignment `flag_result_reserved` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:458`
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

<a id="vg-finding-443"></a>
### VG062: process assignment `state_current` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:459`
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

<a id="vg-finding-444"></a>
### VG062: process assignment `cnt_preload_writes` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:468`
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

<a id="vg-finding-445"></a>
### VG062: process assignment `cnt_expected_halo` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:469`
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

<a id="vg-finding-446"></a>
### VG062: process assignment `cnt_expected_dw_cache` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:470`
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

<a id="vg-finding-447"></a>
### VG062: process assignment `cnt_expected_dw_weight` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:471`
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

<a id="vg-finding-448"></a>
### VG062: process assignment `cnt_expected_dw_bias` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:472`
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

<a id="vg-finding-449"></a>
### VG062: process assignment `cnt_expected_pw_weight` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:473`
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

<a id="vg-finding-450"></a>
### VG062: process assignment `cnt_expected_pw_bias` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:474`
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

<a id="vg-finding-451"></a>
### VG062: process assignment `flag_halo_loaded` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:475`
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

<a id="vg-finding-452"></a>
### VG062: process assignment `flag_dw_cache_loaded` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:476`
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

<a id="vg-finding-453"></a>
### VG062: process assignment `flag_dw_weight_loaded` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:477`
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

<a id="vg-finding-454"></a>
### VG062: process assignment `flag_dw_bias_loaded` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:478`
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

<a id="vg-finding-455"></a>
### VG062: process assignment `flag_pw_weight_loaded` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:479`
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

<a id="vg-finding-456"></a>
### VG062: process assignment `flag_pw_bias_loaded` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:480`
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

<a id="vg-finding-457"></a>
### VG062: process assignment `flag_load_fault` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:481`
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

<a id="vg-finding-458"></a>
### VG062: process assignment `cnt_preload_writes` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:484`
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

<a id="vg-finding-459"></a>
### VG062: process assignment `reg_halo[i_load_addr]` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:488`
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

<a id="vg-finding-460"></a>
### VG062: process assignment `flag_halo_loaded` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:489`
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

<a id="vg-finding-461"></a>
### VG062: process assignment `cnt_expected_halo` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:490`
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

<a id="vg-finding-462"></a>
### VG062: process assignment `flag_load_fault` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:492`
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

<a id="vg-finding-463"></a>
### VG062: process assignment `reg_dw_cache[i_load_addr]` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:497`
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

<a id="vg-finding-464"></a>
### VG062: process assignment `flag_dw_cache_loaded` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:498`
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

<a id="vg-finding-465"></a>
### VG062: process assignment `cnt_expected_dw_cache` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:499`
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

<a id="vg-finding-466"></a>
### VG062: process assignment `flag_load_fault` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:501`
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

<a id="vg-finding-467"></a>
### VG062: process assignment `reg_dw_weight[i_load_addr]` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:506`
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

<a id="vg-finding-468"></a>
### VG062: process assignment `flag_dw_weight_loaded` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:507`
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

<a id="vg-finding-469"></a>
### VG062: process assignment `cnt_expected_dw_weight` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:508`
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

<a id="vg-finding-470"></a>
### VG062: process assignment `flag_load_fault` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:510`
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

<a id="vg-finding-471"></a>
### VG062: process assignment `reg_dw_bias[i_load_addr]` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:515`
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

<a id="vg-finding-472"></a>
### VG062: process assignment `flag_dw_bias_loaded` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:516`
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

<a id="vg-finding-473"></a>
### VG062: process assignment `cnt_expected_dw_bias` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:517`
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

<a id="vg-finding-474"></a>
### VG062: process assignment `flag_load_fault` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:519`
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

<a id="vg-finding-475"></a>
### VG062: process assignment `reg_pw_weight[i_load_addr]` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:524`
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

<a id="vg-finding-476"></a>
### VG062: process assignment `flag_pw_weight_loaded` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:525`
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

<a id="vg-finding-477"></a>
### VG062: process assignment `cnt_expected_pw_weight` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:526`
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

<a id="vg-finding-478"></a>
### VG062: process assignment `flag_load_fault` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:528`
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

<a id="vg-finding-479"></a>
### VG062: process assignment `reg_pw_bias[i_load_addr]` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:533`
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

<a id="vg-finding-480"></a>
### VG062: process assignment `flag_pw_bias_loaded` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:534`
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

<a id="vg-finding-481"></a>
### VG062: process assignment `cnt_expected_pw_bias` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:535`
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

<a id="vg-finding-482"></a>
### VG062: process assignment `flag_load_fault` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:537`
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

<a id="vg-finding-483"></a>
### VG062: process assignment `cnt_core_cycles` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:555`
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

<a id="vg-finding-484"></a>
### VG062: process assignment `cnt_mac_cycles` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:556`
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

<a id="vg-finding-485"></a>
### VG062: process assignment `cnt_pre_cycles` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:557`
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

<a id="vg-finding-486"></a>
### VG062: process assignment `cnt_silu_cycles` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:558`
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

<a id="vg-finding-487"></a>
### VG062: process assignment `cnt_post_cycles` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:559`
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

<a id="vg-finding-488"></a>
### VG062: process assignment `cnt_writeback_cycles` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:560`
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

<a id="vg-finding-489"></a>
### VG062: process assignment `cnt_storage_wait_cycles` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:561`
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

<a id="vg-finding-490"></a>
### VG062: process assignment `cnt_scheduler_idle_cycles` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:562`
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

<a id="vg-finding-491"></a>
### VG062: process assignment `cnt_export_cycles` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:563`
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

<a id="vg-finding-492"></a>
### VG062: process assignment `cnt_mac_results` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:564`
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

<a id="vg-finding-493"></a>
### VG062: process assignment `cnt_pre_accepts` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:565`
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

<a id="vg-finding-494"></a>
### VG062: process assignment `cnt_silu_accepts` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:566`
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

<a id="vg-finding-495"></a>
### VG062: process assignment `cnt_post_accepts` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:567`
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

<a id="vg-finding-496"></a>
### VG062: process assignment `cnt_writebacks` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:568`
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

<a id="vg-finding-497"></a>
### VG062: process assignment `cnt_core_cycles` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:571`
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

<a id="vg-finding-498"></a>
### VG062: process assignment `cnt_mac_cycles` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:572`
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

<a id="vg-finding-499"></a>
### VG062: process assignment `cnt_pre_cycles` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:573`
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

<a id="vg-finding-500"></a>
### VG062: process assignment `cnt_silu_cycles` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:574`
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

<a id="vg-finding-501"></a>
### VG062: process assignment `cnt_post_cycles` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:575`
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

<a id="vg-finding-502"></a>
### VG062: process assignment `cnt_writeback_cycles` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:576`
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

<a id="vg-finding-503"></a>
### VG062: process assignment `cnt_storage_wait_cycles` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:577`
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

<a id="vg-finding-504"></a>
### VG062: process assignment `cnt_scheduler_idle_cycles` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:578`
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

<a id="vg-finding-505"></a>
### VG062: process assignment `cnt_mac_results` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:579`
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

<a id="vg-finding-506"></a>
### VG062: process assignment `cnt_pre_accepts` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:580`
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

<a id="vg-finding-507"></a>
### VG062: process assignment `cnt_silu_accepts` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:581`
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

<a id="vg-finding-508"></a>
### VG062: process assignment `cnt_post_accepts` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:582`
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

<a id="vg-finding-509"></a>
### VG062: process assignment `cnt_writebacks` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:583`
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

<a id="vg-finding-510"></a>
### VG062: process assignment `cnt_core_cycles` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:585`
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

<a id="vg-finding-511"></a>
### VG062: process assignment `cnt_mac_cycles` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:588`
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

<a id="vg-finding-512"></a>
### VG062: process assignment `cnt_storage_wait_cycles` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:596`
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

<a id="vg-finding-513"></a>
### VG062: process assignment `cnt_scheduler_idle_cycles` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:598`
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

<a id="vg-finding-514"></a>
### VG062: process assignment `cnt_export_cycles` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:607`
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

<a id="vg-finding-515"></a>
### VG062: process assignment `cnt_export_cycles` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:609`
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

<a id="vg-finding-516"></a>
### VG064: instance mapping `.i_clk` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:615`
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

<a id="vg-finding-517"></a>
### VG064: instance mapping `.i_rstn` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:616`
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

<a id="vg-finding-518"></a>
### VG064: instance mapping `.i_input_valid` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:617`
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

<a id="vg-finding-519"></a>
### VG064: instance mapping `.i_first` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:618`
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

<a id="vg-finding-520"></a>
### VG064: instance mapping `.i_last` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:619`
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

<a id="vg-finding-521"></a>
### VG064: instance mapping `.i_lane_mask` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:620`
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

<a id="vg-finding-522"></a>
### VG064: instance mapping `.i_activation_data` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:621`
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

<a id="vg-finding-523"></a>
### VG064: instance mapping `.i_weight_data` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:622`
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

<a id="vg-finding-524"></a>
### VG064: instance mapping `.i_bias_data` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:623`
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

<a id="vg-finding-525"></a>
### VG064: instance mapping `.i_result_ready` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:624`
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

<a id="vg-finding-526"></a>
### VG064: instance mapping `.o_input_ready` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:625`
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

<a id="vg-finding-527"></a>
### VG064: instance mapping `.o_result_valid` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:626`
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

<a id="vg-finding-528"></a>
### VG064: instance mapping `.o_result_data` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:627`
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

<a id="vg-finding-529"></a>
### VG064: instance mapping `.o_fault` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:628`
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

<a id="vg-finding-530"></a>
### VG064: instance mapping `.i_clk` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:632`
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

<a id="vg-finding-531"></a>
### VG064: instance mapping `.i_rstn` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:633`
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

<a id="vg-finding-532"></a>
### VG064: instance mapping `.i_table_valid` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:634`
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

<a id="vg-finding-533"></a>
### VG064: instance mapping `.i_table_addr` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:635`
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

<a id="vg-finding-534"></a>
### VG064: instance mapping `.i_table_data` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:636`
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

<a id="vg-finding-535"></a>
### VG064: instance mapping `.o_table_ready` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:637`
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

<a id="vg-finding-536"></a>
### VG064: instance mapping `.o_table_loaded` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:638`
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

<a id="vg-finding-537"></a>
### VG064: instance mapping `.o_table_fault` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:639`
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

<a id="vg-finding-538"></a>
### VG064: instance mapping `.i_input_valid` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:640`
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

<a id="vg-finding-539"></a>
### VG064: instance mapping `.i_result_data` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:641`
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

<a id="vg-finding-540"></a>
### VG064: instance mapping `.i_result_fault` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:642`
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

<a id="vg-finding-541"></a>
### VG064: instance mapping `.i_layer` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:643`
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

<a id="vg-finding-542"></a>
### VG064: instance mapping `.i_position` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:644`
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

<a id="vg-finding-543"></a>
### VG064: instance mapping `.i_channel_base` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:645`
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

<a id="vg-finding-544"></a>
### VG064: instance mapping `.i_lane_mask` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:646`
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

<a id="vg-finding-545"></a>
### VG064: instance mapping `.o_input_ready` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:647`
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

<a id="vg-finding-546"></a>
### VG064: instance mapping `.i_output_ready` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:648`
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

<a id="vg-finding-547"></a>
### VG064: instance mapping `.o_output_valid` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:649`
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

<a id="vg-finding-548"></a>
### VG064: instance mapping `.o_output_data` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:650`
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

<a id="vg-finding-549"></a>
### VG064: instance mapping `.o_output_tag` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:651`
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

<a id="vg-finding-550"></a>
### VG064: instance mapping `.o_fault` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:652`
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

<a id="vg-finding-551"></a>
### VG064: instance mapping `.o_result_queue_count` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:653`
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

<a id="vg-finding-552"></a>
### VG064: instance mapping `.o_meta_count` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:654`
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

<a id="vg-finding-553"></a>
### VG064: instance mapping `.o_pre_busy` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:655`
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

<a id="vg-finding-554"></a>
### VG064: instance mapping `.o_silu_busy` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:656`
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

<a id="vg-finding-555"></a>
### VG064: instance mapping `.o_post_busy` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:657`
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

<a id="vg-finding-556"></a>
### VG064: instance mapping `.o_pre_accept` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:658`
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

<a id="vg-finding-557"></a>
### VG064: instance mapping `.o_silu_accept` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:659`
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

<a id="vg-finding-558"></a>
### VG064: instance mapping `.o_post_accept` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `down2_overlap_tile_runner.v:660`
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

<a id="vg-finding-559"></a>
### VG042: Comment coverage is too low for generated RTL (0.00%); add semantic comments near declarations, assigns, always blocks, FSM, and instances.
- Status: `failed`
- Severity: `error`
- Location: `file:down2_overlap_tile_runner.v:unknown`
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

<a id="vg-finding-560"></a>
### VG080: procedural for 循环体对非循环变量执行了算术更新。
- Status: `failed`
- Severity: `WARNING`
- Location: `down2_overlap_tile_runner.v:256`
- Evidence:
- node_kind: `verilog_rtl`
- detail: kernel_index = cnt_mac_group * 8 + lane_index;
- source_excerpt: `kernel_index = cnt_mac_group * 8 + lane_index;`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
kernel_index = cnt_mac_group * 8 + lane_index;
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-561"></a>
### VG080: procedural for 循环体对非循环变量执行了算术更新。
- Status: `failed`
- Severity: `WARNING`
- Location: `down2_overlap_tile_runner.v:258`
- Evidence:
- node_kind: `verilog_rtl`
- detail: halo_index = ((((cnt_position >> 2) * 2 + kernel_index / 3) * 9 +
					              ((cnt_position & 4'h3) * 2 + kernel_index % 3)) * 16 + cnt_output);
- source_excerpt: `halo_index = ((((cnt_position >> 2) * 2 + kernel_index / 3) * 9 +
					              ((cnt_position & 4'h3) * 2 + kernel_index % 3)) * 16 + cnt_output);`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
halo_index = ((((cnt_position >> 2) * 2 + kernel_index / 3) * 9 +
					              ((cnt_position & 4'h3) * 2 + kernel_index % 3)) * 16 + cnt_output);
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-562"></a>
### VG080: procedural for 循环体对非循环变量执行了算术更新。
- Status: `failed`
- Severity: `WARNING`
- Location: `down2_overlap_tile_runner.v:262`
- Evidence:
- node_kind: `verilog_rtl`
- detail: weight_index = cnt_output * 9 + kernel_index;
- source_excerpt: `weight_index = cnt_output * 9 + kernel_index;`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
weight_index = cnt_output * 9 + kernel_index;
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-563"></a>
### VG080: procedural for 循环体对非循环变量执行了算术更新。
- Status: `failed`
- Severity: `WARNING`
- Location: `down2_overlap_tile_runner.v:279`
- Evidence:
- node_kind: `verilog_rtl`
- detail: output_channel = cnt_output * 3;
- source_excerpt: `output_channel = cnt_output * 3;`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
output_channel = cnt_output * 3;
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-564"></a>
### VG085: 表达式两侧位宽不一致。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:496`
- Evidence:
- node_kind: `verilog_rtl`
- detail: i_load_addr == cnt_expected_dw_cache
- source_excerpt: `i_load_addr == cnt_expected_dw_cache`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
i_load_addr == cnt_expected_dw_cache
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-565"></a>
### VG085: 表达式两侧位宽不一致。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:505`
- Evidence:
- node_kind: `verilog_rtl`
- detail: i_load_addr == cnt_expected_dw_weight
- source_excerpt: `i_load_addr == cnt_expected_dw_weight`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
i_load_addr == cnt_expected_dw_weight
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-566"></a>
### VG085: 表达式两侧位宽不一致。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:514`
- Evidence:
- node_kind: `verilog_rtl`
- detail: i_load_addr == cnt_expected_dw_bias
- source_excerpt: `i_load_addr == cnt_expected_dw_bias`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
i_load_addr == cnt_expected_dw_bias
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-567"></a>
### VG085: 表达式两侧位宽不一致。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:523`
- Evidence:
- node_kind: `verilog_rtl`
- detail: i_load_addr == cnt_expected_pw_weight
- source_excerpt: `i_load_addr == cnt_expected_pw_weight`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
i_load_addr == cnt_expected_pw_weight
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-568"></a>
### VG085: 表达式两侧位宽不一致。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:532`
- Evidence:
- node_kind: `verilog_rtl`
- detail: i_load_addr == cnt_expected_pw_bias
- source_excerpt: `i_load_addr == cnt_expected_pw_bias`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
i_load_addr == cnt_expected_pw_bias
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-569"></a>
### VG091: 数组索引应使用简单信号，避免直接嵌入表达式。
- Status: `failed`
- Severity: `WARNING`
- Location: `down2_overlap_tile_runner.v:277`
- Evidence:
- node_kind: `verilog_rtl`
- detail: reg_dw_cache[cnt_position * 16 + cnt_mac_group * 8 + lane_index]
- source_excerpt: `reg_dw_cache[cnt_position * 16 + cnt_mac_group * 8 + lane_index]`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
reg_dw_cache[cnt_position * 16 + cnt_mac_group * 8 + lane_index]
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-570"></a>
### VG091: 数组索引应使用简单信号，避免直接嵌入表达式。
- Status: `failed`
- Severity: `WARNING`
- Location: `down2_overlap_tile_runner.v:280`
- Evidence:
- node_kind: `verilog_rtl`
- detail: reg_pw_weight[output_channel * 16 + cnt_mac_group * 8 + lane_index]
- source_excerpt: `reg_pw_weight[output_channel * 16 + cnt_mac_group * 8 + lane_index]`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
reg_pw_weight[output_channel * 16 + cnt_mac_group * 8 + lane_index]
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-571"></a>
### VG091: 数组索引应使用简单信号，避免直接嵌入表达式。
- Status: `failed`
- Severity: `WARNING`
- Location: `down2_overlap_tile_runner.v:281`
- Evidence:
- node_kind: `verilog_rtl`
- detail: reg_pw_weight[(output_channel + 1) * 16 + cnt_mac_group * 8 + lane_index]
- source_excerpt: `reg_pw_weight[(output_channel + 1) * 16 + cnt_mac_group * 8 + lane_index]`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
reg_pw_weight[(output_channel + 1) * 16 + cnt_mac_group * 8 + lane_index]
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-572"></a>
### VG091: 数组索引应使用简单信号，避免直接嵌入表达式。
- Status: `failed`
- Severity: `WARNING`
- Location: `down2_overlap_tile_runner.v:282`
- Evidence:
- node_kind: `verilog_rtl`
- detail: reg_pw_weight[(output_channel + 2) * 16 + cnt_mac_group * 8 + lane_index]
- source_excerpt: `reg_pw_weight[(output_channel + 2) * 16 + cnt_mac_group * 8 + lane_index]`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
reg_pw_weight[(output_channel + 2) * 16 + cnt_mac_group * 8 + lane_index]
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-573"></a>
### VG091: 数组索引应使用简单信号，避免直接嵌入表达式。
- Status: `failed`
- Severity: `WARNING`
- Location: `down2_overlap_tile_runner.v:284`
- Evidence:
- node_kind: `verilog_rtl`
- detail: reg_pw_bias[cnt_output * 3]
- source_excerpt: `reg_pw_bias[cnt_output * 3]`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
reg_pw_bias[cnt_output * 3]
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-574"></a>
### VG091: 数组索引应使用简单信号，避免直接嵌入表达式。
- Status: `failed`
- Severity: `WARNING`
- Location: `down2_overlap_tile_runner.v:285`
- Evidence:
- node_kind: `verilog_rtl`
- detail: reg_pw_bias[cnt_output * 3 + 1]
- source_excerpt: `reg_pw_bias[cnt_output * 3 + 1]`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
reg_pw_bias[cnt_output * 3 + 1]
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-575"></a>
### VG091: 数组索引应使用简单信号，避免直接嵌入表达式。
- Status: `failed`
- Severity: `WARNING`
- Location: `down2_overlap_tile_runner.v:286`
- Evidence:
- node_kind: `verilog_rtl`
- detail: reg_pw_bias[cnt_output * 3 + 2]
- source_excerpt: `reg_pw_bias[cnt_output * 3 + 2]`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
reg_pw_bias[cnt_output * 3 + 2]
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-576"></a>
### VG094: FSM default 分支必须把 state_next 恢复到已声明的确定状态。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:266`
- Evidence:
- node_kind: `verilog_rtl`
- detail: begin
						flag_busy_o <= 1'b0;
						flag_fault_o <= 1'b1;
						flag_tile_valid <= 1'b0;
						flag_result_reserved <= 1'b0;
						state_current <= ST_FAULT;
					end
- source_excerpt: `begin
						flag_busy_o <= 1'b0;
						flag_fault_o <= 1'b1;
						flag_tile_valid <= 1'b0;
						flag_result_reserved <= 1'b0;
						state_current <= ST_FAULT;
					end`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
begin
						flag_busy_o <= 1'b0;
						flag_fault_o <= 1'b1;
						flag_tile_valid <= 1'b0;
						flag_result_reserved <= 1'b0;
						state_current <= ST_FAULT;
					end
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-577"></a>
### VG097: 缺少外部模块接口定义，无法静态比较端口位宽。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:614`
- Evidence:
- node_kind: `verilog_rtl`
- detail: road_mac_probe road_mac_probe_Inst_tile
- source_excerpt: `road_mac_probe road_mac_probe_Inst_tile`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
road_mac_probe road_mac_probe_Inst_tile
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-578"></a>
### VG097: 缺少外部模块接口定义，无法静态比较端口位宽。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:631`
- Evidence:
- node_kind: `verilog_rtl`
- detail: road_postprocess_stream road_postprocess_stream_Inst_tile
- source_excerpt: `road_postprocess_stream road_postprocess_stream_Inst_tile`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
road_postprocess_stream road_postprocess_stream_Inst_tile
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-579"></a>
### VG098: FSM 状态必须能从复位初态到达且具有可证明的后继转移。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:63`
- Evidence:
- node_kind: `verilog_rtl`
- detail: ST_DONE
- source_excerpt: `ST_DONE`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
ST_DONE
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-580"></a>
### VG098: FSM 状态必须能从复位初态到达且具有可证明的后继转移。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:61`
- Evidence:
- node_kind: `verilog_rtl`
- detail: ST_DW_DRAIN
- source_excerpt: `ST_DW_DRAIN`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
ST_DW_DRAIN
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-581"></a>
### VG098: FSM 状态必须能从复位初态到达且具有可证明的后继转移。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:65`
- Evidence:
- node_kind: `verilog_rtl`
- detail: ST_EXPORT
- source_excerpt: `ST_EXPORT`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
ST_EXPORT
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-582"></a>
### VG098: FSM 状态必须能从复位初态到达且具有可证明的后继转移。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:64`
- Evidence:
- node_kind: `verilog_rtl`
- detail: ST_FAULT
- source_excerpt: `ST_FAULT`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
ST_FAULT
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-583"></a>
### VG098: FSM 状态必须能从复位初态到达且具有可证明的后继转移。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:57`
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

<a id="vg-finding-584"></a>
### VG098: FSM 状态必须能从复位初态到达且具有可证明的后继转移。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:59`
- Evidence:
- node_kind: `verilog_rtl`
- detail: ST_MAC_SEND
- source_excerpt: `ST_MAC_SEND`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
ST_MAC_SEND
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-585"></a>
### VG098: FSM 状态必须能从复位初态到达且具有可证明的后继转移。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:60`
- Evidence:
- node_kind: `verilog_rtl`
- detail: ST_MAC_WAIT
- source_excerpt: `ST_MAC_WAIT`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
ST_MAC_WAIT
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-586"></a>
### VG098: FSM 状态必须能从复位初态到达且具有可证明的后继转移。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:62`
- Evidence:
- node_kind: `verilog_rtl`
- detail: ST_PW_DRAIN
- source_excerpt: `ST_PW_DRAIN`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
ST_PW_DRAIN
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-587"></a>
### VG098: FSM 状态必须能从复位初态到达且具有可证明的后继转移。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:58`
- Evidence:
- node_kind: `verilog_rtl`
- detail: ST_STORAGE
- source_excerpt: `ST_STORAGE`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
ST_STORAGE
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-588"></a>
### VG103: 同一控制路径重复写入同一信号。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: next_mac_weight
- source_excerpt: `next_mac_weight`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
next_mac_weight
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-589"></a>
### VG103: 同一控制路径重复写入同一信号。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: next_mac_weight
- source_excerpt: `next_mac_weight`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
next_mac_weight
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-590"></a>
### VG103: 同一控制路径重复写入同一信号。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: next_mac_bias
- source_excerpt: `next_mac_bias`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
next_mac_bias
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-591"></a>
### VG103: 同一控制路径重复写入同一信号。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: next_mac_bias
- source_excerpt: `next_mac_bias`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
next_mac_bias
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-592"></a>
### VG109: 组合逻辑 if 链缺少终止 else。
- Status: `failed`
- Severity: `WARNING`
- Location: `down2_overlap_tile_runner.v:257`
- Evidence:
- node_kind: `verilog_rtl`
- detail: if(kernel_index < 9)
- source_excerpt: `if(kernel_index < 9)`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
if(kernel_index < 9)
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-593"></a>
### VG110: 同一时序块中存在未统一复位的触发器目标。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:466`
- Evidence:
- node_kind: `verilog_rtl`
- detail: reg_dw_bias, reg_dw_cache, reg_dw_weight, reg_halo, reg_output_cache, reg_pw_bias, reg_pw_weight
- source_excerpt: `reg_dw_bias, reg_dw_cache, reg_dw_weight, reg_halo, reg_output_cache, reg_pw_bias, reg_pw_weight`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
reg_dw_bias, reg_dw_cache, reg_dw_weight, reg_halo, reg_output_cache, reg_pw_bias, reg_pw_weight
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-594"></a>
### VG113: 同一时序块中存在未统一复位的触发器目标。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:466`
- Evidence:
- node_kind: `verilog_rtl`
- detail: reg_dw_bias, reg_dw_cache, reg_dw_weight, reg_halo, reg_output_cache, reg_pw_bias, reg_pw_weight
- source_excerpt: `reg_dw_bias, reg_dw_cache, reg_dw_weight, reg_halo, reg_output_cache, reg_pw_bias, reg_pw_weight`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
reg_dw_bias, reg_dw_cache, reg_dw_weight, reg_halo, reg_output_cache, reg_pw_bias, reg_pw_weight
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-595"></a>
### VG122: 算术结果位宽超过赋值目标位宽。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:335`
- Evidence:
- node_kind: `verilog_rtl`
- detail: cnt_pw_writes <= cnt_pw_writes + 1'b1;
- source_excerpt: `cnt_pw_writes <= cnt_pw_writes + 1'b1;`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
cnt_pw_writes <= cnt_pw_writes + 1'b1;
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-596"></a>
### VG122: 算术结果位宽超过赋值目标位宽。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:337`
- Evidence:
- node_kind: `verilog_rtl`
- detail: cnt_dw_writes <= cnt_dw_writes + 1'b1;
- source_excerpt: `cnt_dw_writes <= cnt_dw_writes + 1'b1;`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
cnt_dw_writes <= cnt_dw_writes + 1'b1;
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-597"></a>
### VG122: 算术结果位宽超过赋值目标位宽。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:394`
- Evidence:
- node_kind: `verilog_rtl`
- detail: cnt_output <= cnt_output + 1'b1;
- source_excerpt: `cnt_output <= cnt_output + 1'b1;`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
cnt_output <= cnt_output + 1'b1;
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-598"></a>
### VG122: 算术结果位宽超过赋值目标位宽。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:397`
- Evidence:
- node_kind: `verilog_rtl`
- detail: cnt_position <= cnt_position + 1'b1;
- source_excerpt: `cnt_position <= cnt_position + 1'b1;`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
cnt_position <= cnt_position + 1'b1;
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-599"></a>
### VG122: 算术结果位宽超过赋值目标位宽。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:405`
- Evidence:
- node_kind: `verilog_rtl`
- detail: cnt_output <= cnt_output + 1'b1;
- source_excerpt: `cnt_output <= cnt_output + 1'b1;`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
cnt_output <= cnt_output + 1'b1;
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-600"></a>
### VG122: 算术结果位宽超过赋值目标位宽。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:408`
- Evidence:
- node_kind: `verilog_rtl`
- detail: cnt_position <= cnt_position + 1'b1;
- source_excerpt: `cnt_position <= cnt_position + 1'b1;`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
cnt_position <= cnt_position + 1'b1;
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-601"></a>
### VG122: 算术结果位宽超过赋值目标位宽。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:450`
- Evidence:
- node_kind: `verilog_rtl`
- detail: cnt_export <= cnt_export + 1'b1;
- source_excerpt: `cnt_export <= cnt_export + 1'b1;`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
cnt_export <= cnt_export + 1'b1;
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-602"></a>
### VG122: 算术结果位宽超过赋值目标位宽。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:484`
- Evidence:
- node_kind: `verilog_rtl`
- detail: cnt_preload_writes <= cnt_preload_writes + 1'b1;
- source_excerpt: `cnt_preload_writes <= cnt_preload_writes + 1'b1;`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
cnt_preload_writes <= cnt_preload_writes + 1'b1;
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-603"></a>
### VG122: 算术结果位宽超过赋值目标位宽。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:585`
- Evidence:
- node_kind: `verilog_rtl`
- detail: cnt_core_cycles <= cnt_core_cycles + 1'b1;
- source_excerpt: `cnt_core_cycles <= cnt_core_cycles + 1'b1;`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
cnt_core_cycles <= cnt_core_cycles + 1'b1;
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-604"></a>
### VG122: 算术结果位宽超过赋值目标位宽。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:588`
- Evidence:
- node_kind: `verilog_rtl`
- detail: cnt_mac_cycles <= cnt_mac_cycles + 1'b1;
- source_excerpt: `cnt_mac_cycles <= cnt_mac_cycles + 1'b1;`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
cnt_mac_cycles <= cnt_mac_cycles + 1'b1;
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-605"></a>
### VG122: 算术结果位宽超过赋值目标位宽。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:590`
- Evidence:
- node_kind: `verilog_rtl`
- detail: cnt_pre_cycles <= cnt_pre_cycles + 1'b1;
- source_excerpt: `cnt_pre_cycles <= cnt_pre_cycles + 1'b1;`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
cnt_pre_cycles <= cnt_pre_cycles + 1'b1;
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-606"></a>
### VG122: 算术结果位宽超过赋值目标位宽。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:591`
- Evidence:
- node_kind: `verilog_rtl`
- detail: cnt_silu_cycles <= cnt_silu_cycles + 1'b1;
- source_excerpt: `cnt_silu_cycles <= cnt_silu_cycles + 1'b1;`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
cnt_silu_cycles <= cnt_silu_cycles + 1'b1;
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-607"></a>
### VG122: 算术结果位宽超过赋值目标位宽。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:592`
- Evidence:
- node_kind: `verilog_rtl`
- detail: cnt_post_cycles <= cnt_post_cycles + 1'b1;
- source_excerpt: `cnt_post_cycles <= cnt_post_cycles + 1'b1;`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
cnt_post_cycles <= cnt_post_cycles + 1'b1;
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-608"></a>
### VG122: 算术结果位宽超过赋值目标位宽。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:593`
- Evidence:
- node_kind: `verilog_rtl`
- detail: cnt_writeback_cycles <= cnt_writeback_cycles + 1'b1;
- source_excerpt: `cnt_writeback_cycles <= cnt_writeback_cycles + 1'b1;`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
cnt_writeback_cycles <= cnt_writeback_cycles + 1'b1;
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-609"></a>
### VG122: 算术结果位宽超过赋值目标位宽。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:596`
- Evidence:
- node_kind: `verilog_rtl`
- detail: cnt_storage_wait_cycles <= cnt_storage_wait_cycles + 1'b1;
- source_excerpt: `cnt_storage_wait_cycles <= cnt_storage_wait_cycles + 1'b1;`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
cnt_storage_wait_cycles <= cnt_storage_wait_cycles + 1'b1;
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-610"></a>
### VG122: 算术结果位宽超过赋值目标位宽。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:598`
- Evidence:
- node_kind: `verilog_rtl`
- detail: cnt_scheduler_idle_cycles <= cnt_scheduler_idle_cycles + 1'b1;
- source_excerpt: `cnt_scheduler_idle_cycles <= cnt_scheduler_idle_cycles + 1'b1;`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
cnt_scheduler_idle_cycles <= cnt_scheduler_idle_cycles + 1'b1;
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-611"></a>
### VG122: 算术结果位宽超过赋值目标位宽。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:601`
- Evidence:
- node_kind: `verilog_rtl`
- detail: cnt_mac_results <= cnt_mac_results + 1'b1;
- source_excerpt: `cnt_mac_results <= cnt_mac_results + 1'b1;`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
cnt_mac_results <= cnt_mac_results + 1'b1;
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-612"></a>
### VG122: 算术结果位宽超过赋值目标位宽。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:602`
- Evidence:
- node_kind: `verilog_rtl`
- detail: cnt_pre_accepts <= cnt_pre_accepts + 1'b1;
- source_excerpt: `cnt_pre_accepts <= cnt_pre_accepts + 1'b1;`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
cnt_pre_accepts <= cnt_pre_accepts + 1'b1;
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-613"></a>
### VG122: 算术结果位宽超过赋值目标位宽。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:603`
- Evidence:
- node_kind: `verilog_rtl`
- detail: cnt_silu_accepts <= cnt_silu_accepts + 1'b1;
- source_excerpt: `cnt_silu_accepts <= cnt_silu_accepts + 1'b1;`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
cnt_silu_accepts <= cnt_silu_accepts + 1'b1;
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-614"></a>
### VG122: 算术结果位宽超过赋值目标位宽。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:604`
- Evidence:
- node_kind: `verilog_rtl`
- detail: cnt_post_accepts <= cnt_post_accepts + 1'b1;
- source_excerpt: `cnt_post_accepts <= cnt_post_accepts + 1'b1;`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
cnt_post_accepts <= cnt_post_accepts + 1'b1;
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-615"></a>
### VG122: 算术结果位宽超过赋值目标位宽。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:605`
- Evidence:
- node_kind: `verilog_rtl`
- detail: cnt_writebacks <= cnt_writebacks + 1'b1;
- source_excerpt: `cnt_writebacks <= cnt_writebacks + 1'b1;`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
cnt_writebacks <= cnt_writebacks + 1'b1;
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-616"></a>
### VG122: 算术结果位宽超过赋值目标位宽。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:609`
- Evidence:
- node_kind: `verilog_rtl`
- detail: cnt_export_cycles <= cnt_export_cycles + 1'b1;
- source_excerpt: `cnt_export_cycles <= cnt_export_cycles + 1'b1;`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
cnt_export_cycles <= cnt_export_cycles + 1'b1;
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-617"></a>
### VG125: 字面量声明为 5 位，但实际值只需要 2 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:182`
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

<a id="vg-finding-618"></a>
### VG125: 字面量声明为 5 位，但实际值只需要 3 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:183`
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

<a id="vg-finding-619"></a>
### VG125: 字面量声明为 5 位，但实际值只需要 4 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:183`
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

<a id="vg-finding-620"></a>
### VG125: 字面量声明为 5 位，但实际值只需要 4 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:184`
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

<a id="vg-finding-621"></a>
### VG125: 字面量声明为 5 位，但实际值只需要 4 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:184`
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

<a id="vg-finding-622"></a>
### VG125: 字面量声明为 5 位，但实际值只需要 1 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:185`
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

<a id="vg-finding-623"></a>
### VG125: 字面量声明为 5 位，但实际值只需要 3 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:185`
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

<a id="vg-finding-624"></a>
### VG125: 字面量声明为 5 位，但实际值只需要 3 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:186`
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

<a id="vg-finding-625"></a>
### VG125: 字面量声明为 5 位，但实际值只需要 4 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:186`
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

<a id="vg-finding-626"></a>
### VG125: 字面量声明为 5 位，但实际值只需要 4 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:187`
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

<a id="vg-finding-627"></a>
### VG125: 字面量声明为 2 位，但实际值只需要 1 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:187`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 2'd1
- source_excerpt: `2'd1`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
2'd1
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-628"></a>
### VG125: 字面量声明为 2 位，但实际值只需要 1 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:265`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 2'd1
- source_excerpt: `2'd1`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
2'd1
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-629"></a>
### VG125: 字面量声明为 2 位，但实际值只需要 1 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:272`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 2'd1
- source_excerpt: `2'd1`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
2'd1
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-630"></a>
### VG125: 字面量声明为 5 位，但实际值只需要 4 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:393`
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

<a id="vg-finding-631"></a>
### VG125: 字面量声明为 5 位，但实际值只需要 3 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:404`
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

<a id="vg-finding-632"></a>
### VG125: 字面量声明为 3 位，但实际值只需要 1 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:495`
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

<a id="vg-finding-633"></a>
### VG125: 字面量声明为 11 位，但实际值只需要 8 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:498`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 11'd255
- source_excerpt: `11'd255`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
11'd255
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-634"></a>
### VG125: 字面量声明为 11 位，但实际值只需要 8 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:499`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 11'd255
- source_excerpt: `11'd255`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
11'd255
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-635"></a>
### VG125: 字面量声明为 3 位，但实际值只需要 2 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:504`
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

<a id="vg-finding-636"></a>
### VG125: 字面量声明为 11 位，但实际值只需要 8 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:507`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 11'd143
- source_excerpt: `11'd143`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
11'd143
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-637"></a>
### VG125: 字面量声明为 11 位，但实际值只需要 8 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:508`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 11'd143
- source_excerpt: `11'd143`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
11'd143
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-638"></a>
### VG125: 字面量声明为 3 位，但实际值只需要 2 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:513`
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

<a id="vg-finding-639"></a>
### VG125: 字面量声明为 11 位，但实际值只需要 4 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:516`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 11'd15
- source_excerpt: `11'd15`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
11'd15
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-640"></a>
### VG125: 字面量声明为 11 位，但实际值只需要 4 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:517`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 11'd15
- source_excerpt: `11'd15`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
11'd15
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-641"></a>
### VG125: 字面量声明为 11 位，但实际值只需要 9 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:525`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 11'd383
- source_excerpt: `11'd383`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
11'd383
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-642"></a>
### VG125: 字面量声明为 11 位，但实际值只需要 9 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:526`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 11'd383
- source_excerpt: `11'd383`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
11'd383
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-643"></a>
### VG125: 字面量声明为 11 位，但实际值只需要 5 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:534`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 11'd23
- source_excerpt: `11'd23`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
11'd23
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-644"></a>
### VG125: 字面量声明为 11 位，但实际值只需要 5 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:535`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 11'd23
- source_excerpt: `11'd23`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
11'd23
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-645"></a>
### VG132: 未登记原语或外部模块的时钟角色无法静态确定。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:614`
- Evidence:
- node_kind: `verilog_rtl`
- detail: road_mac_probe road_mac_probe_Inst_tile
- source_excerpt: `road_mac_probe road_mac_probe_Inst_tile`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
road_mac_probe road_mac_probe_Inst_tile
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-646"></a>
### VG132: 未登记原语或外部模块的时钟角色无法静态确定。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:631`
- Evidence:
- node_kind: `verilog_rtl`
- detail: road_postprocess_stream road_postprocess_stream_Inst_tile
- source_excerpt: `road_postprocess_stream road_postprocess_stream_Inst_tile`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
road_postprocess_stream road_postprocess_stream_Inst_tile
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-647"></a>
### VG136: 组合逻辑依赖图中存在反馈环。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:175`
- Evidence:
- node_kind: `verilog_rtl`
- detail: lane_index
- source_excerpt: `lane_index`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
lane_index
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-648"></a>
### VG137: 存在无法静态确定的表达式位宽。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `run:unknown`
- Evidence:
- node_kind: `verilog_project`
- detail: gate_id=VG137; rule_key=assign_width_match; status=inconclusive; applicable=True; reason=存在无法静态确定的表达式位宽。
- source_excerpt: `gate_id=VG137; rule_key=assign_width_match; status=inconclusive; applicable=True; reason=存在无法静态确定的表达式位宽。`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
gate_id=VG137; rule_key=assign_width_match; status=inconclusive; applicable=True; reason=存在无法静态确定的表达式位宽。
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-649"></a>
### VG138: 常量未显式声明位宽和进制。
- Status: `failed`
- Severity: `WARNING`
- Location: `down2_overlap_tile_runner.v:250`
- Evidence:
- node_kind: `verilog_rtl`
- detail: = 0
- source_excerpt: `= 0`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
= 0
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-650"></a>
### VG138: 常量未显式声明位宽和进制。
- Status: `failed`
- Severity: `WARNING`
- Location: `down2_overlap_tile_runner.v:251`
- Evidence:
- node_kind: `verilog_rtl`
- detail: = 0
- source_excerpt: `= 0`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
= 0
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-651"></a>
### VG138: 常量未显式声明位宽和进制。
- Status: `failed`
- Severity: `WARNING`
- Location: `down2_overlap_tile_runner.v:252`
- Evidence:
- node_kind: `verilog_rtl`
- detail: = 0
- source_excerpt: `= 0`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
= 0
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-652"></a>
### VG138: 常量未显式声明位宽和进制。
- Status: `failed`
- Severity: `WARNING`
- Location: `down2_overlap_tile_runner.v:253`
- Evidence:
- node_kind: `verilog_rtl`
- detail: = 0
- source_excerpt: `= 0`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
= 0
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-653"></a>
### VG138: 常量未显式声明位宽和进制。
- Status: `failed`
- Severity: `WARNING`
- Location: `down2_overlap_tile_runner.v:255`
- Evidence:
- node_kind: `verilog_rtl`
- detail: = 0
- source_excerpt: `= 0`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
= 0
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-654"></a>
### VG138: 常量未显式声明位宽和进制。
- Status: `failed`
- Severity: `WARNING`
- Location: `down2_overlap_tile_runner.v:255`
- Evidence:
- node_kind: `verilog_rtl`
- detail: = lane_index + 1
- source_excerpt: `= lane_index + 1`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
= lane_index + 1
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-655"></a>
### VG138: 常量未显式声明位宽和进制。
- Status: `failed`
- Severity: `WARNING`
- Location: `down2_overlap_tile_runner.v:256`
- Evidence:
- node_kind: `verilog_rtl`
- detail: = cnt_mac_group * 8
- source_excerpt: `= cnt_mac_group * 8`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
= cnt_mac_group * 8
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-656"></a>
### VG138: 常量未显式声明位宽和进制。
- Status: `failed`
- Severity: `WARNING`
- Location: `down2_overlap_tile_runner.v:258`
- Evidence:
- node_kind: `verilog_rtl`
- detail: = ((((cnt_position >> 2) * 2 + kernel_index / 3) * 9
- source_excerpt: `= ((((cnt_position >> 2) * 2 + kernel_index / 3) * 9`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
= ((((cnt_position >> 2) * 2 + kernel_index / 3) * 9
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-657"></a>
### VG138: 常量未显式声明位宽和进制。
- Status: `failed`
- Severity: `WARNING`
- Location: `down2_overlap_tile_runner.v:262`
- Evidence:
- node_kind: `verilog_rtl`
- detail: = cnt_output * 9
- source_excerpt: `= cnt_output * 9`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
= cnt_output * 9
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-658"></a>
### VG138: 常量未显式声明位宽和进制。
- Status: `failed`
- Severity: `WARNING`
- Location: `down2_overlap_tile_runner.v:276`
- Evidence:
- node_kind: `verilog_rtl`
- detail: = 0
- source_excerpt: `= 0`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
= 0
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-659"></a>
### VG138: 常量未显式声明位宽和进制。
- Status: `failed`
- Severity: `WARNING`
- Location: `down2_overlap_tile_runner.v:276`
- Evidence:
- node_kind: `verilog_rtl`
- detail: = lane_index + 1
- source_excerpt: `= lane_index + 1`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
= lane_index + 1
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-660"></a>
### VG138: 常量未显式声明位宽和进制。
- Status: `failed`
- Severity: `WARNING`
- Location: `down2_overlap_tile_runner.v:277`
- Evidence:
- node_kind: `verilog_rtl`
- detail: = reg_dw_cache[cnt_position * 16 + cnt_mac_group * 8
- source_excerpt: `= reg_dw_cache[cnt_position * 16 + cnt_mac_group * 8`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
= reg_dw_cache[cnt_position * 16 + cnt_mac_group * 8
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-661"></a>
### VG138: 常量未显式声明位宽和进制。
- Status: `failed`
- Severity: `WARNING`
- Location: `down2_overlap_tile_runner.v:279`
- Evidence:
- node_kind: `verilog_rtl`
- detail: = cnt_output * 3
- source_excerpt: `= cnt_output * 3`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
= cnt_output * 3
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-662"></a>
### VG138: 常量未显式声明位宽和进制。
- Status: `failed`
- Severity: `WARNING`
- Location: `down2_overlap_tile_runner.v:280`
- Evidence:
- node_kind: `verilog_rtl`
- detail: = reg_pw_weight[output_channel * 16 + cnt_mac_group * 8
- source_excerpt: `= reg_pw_weight[output_channel * 16 + cnt_mac_group * 8`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
= reg_pw_weight[output_channel * 16 + cnt_mac_group * 8
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-663"></a>
### VG138: 常量未显式声明位宽和进制。
- Status: `failed`
- Severity: `WARNING`
- Location: `down2_overlap_tile_runner.v:281`
- Evidence:
- node_kind: `verilog_rtl`
- detail: = reg_pw_weight[(output_channel + 1) * 16 + cnt_mac_group * 8
- source_excerpt: `= reg_pw_weight[(output_channel + 1) * 16 + cnt_mac_group * 8`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
= reg_pw_weight[(output_channel + 1) * 16 + cnt_mac_group * 8
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-664"></a>
### VG138: 常量未显式声明位宽和进制。
- Status: `failed`
- Severity: `WARNING`
- Location: `down2_overlap_tile_runner.v:282`
- Evidence:
- node_kind: `verilog_rtl`
- detail: = reg_pw_weight[(output_channel + 2) * 16 + cnt_mac_group * 8
- source_excerpt: `= reg_pw_weight[(output_channel + 2) * 16 + cnt_mac_group * 8`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
= reg_pw_weight[(output_channel + 2) * 16 + cnt_mac_group * 8
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-665"></a>
### VG138: 常量未显式声明位宽和进制。
- Status: `failed`
- Severity: `WARNING`
- Location: `down2_overlap_tile_runner.v:285`
- Evidence:
- node_kind: `verilog_rtl`
- detail: = reg_pw_bias[cnt_output * 3
- source_excerpt: `= reg_pw_bias[cnt_output * 3`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
= reg_pw_bias[cnt_output * 3
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-666"></a>
### VG138: 常量未显式声明位宽和进制。
- Status: `failed`
- Severity: `WARNING`
- Location: `down2_overlap_tile_runner.v:286`
- Evidence:
- node_kind: `verilog_rtl`
- detail: = reg_pw_bias[cnt_output * 3
- source_excerpt: `= reg_pw_bias[cnt_output * 3`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
= reg_pw_bias[cnt_output * 3
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-667"></a>
### VG138: 常量未显式声明位宽和进制。
- Status: `failed`
- Severity: `WARNING`
- Location: `down2_overlap_tile_runner.v:333`
- Evidence:
- node_kind: `verilog_rtl`
- detail: = {{24
- source_excerpt: `= {{24`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
= {{24
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-668"></a>
### VG144: FSM 必须显式声明当前状态和下一状态寄存器。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:57`
- Evidence:
- node_kind: `verilog_rtl`
- detail: missing current/next state roles
- source_excerpt: `missing current/next state roles`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
missing current/next state roles
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-669"></a>
### VG145: 组合逻辑完整依赖锥最多允许三个源信号，超限逻辑必须由时序 reg 隔断。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:200`
- Evidence:
- node_kind: `verilog_rtl`
- detail: flag_load_accept: 6 sources: flag_load_fault, i_export_start, i_load_valid, i_start, pp_fault, state_current
- source_excerpt: `flag_load_accept: 6 sources: flag_load_fault, i_export_start, i_load_valid, i_start, pp_fault, state_current`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
flag_load_accept: 6 sources: flag_load_fault, i_export_start, i_load_valid, i_start, pp_fault, state_current
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-670"></a>
### VG145: 组合逻辑完整依赖锥最多允许三个源信号，超限逻辑必须由时序 reg 隔断。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:194`
- Evidence:
- node_kind: `verilog_rtl`
- detail: flag_mac_input_accept: 6 sources: cnt_mac_group, flag_result_reserved, mac_input_ready, pp_fault, pp_result_queue_count, state_current
- source_excerpt: `flag_mac_input_accept: 6 sources: cnt_mac_group, flag_result_reserved, mac_input_ready, pp_fault, pp_result_queue_count, state_current`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
flag_mac_input_accept: 6 sources: cnt_mac_group, flag_result_reserved, mac_input_ready, pp_fault, pp_result_queue_count, state_current
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-671"></a>
### VG145: 组合逻辑完整依赖锥最多允许三个源信号，超限逻辑必须由时序 reg 隔断。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:193`
- Evidence:
- node_kind: `verilog_rtl`
- detail: flag_mac_input_valid: 5 sources: cnt_mac_group, flag_result_reserved, pp_fault, pp_result_queue_count, state_current
- source_excerpt: `flag_mac_input_valid: 5 sources: cnt_mac_group, flag_result_reserved, pp_fault, pp_result_queue_count, state_current`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
flag_mac_input_valid: 5 sources: cnt_mac_group, flag_result_reserved, pp_fault, pp_result_queue_count, state_current
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-672"></a>
### VG145: 组合逻辑完整依赖锥最多允许三个源信号，超限逻辑必须由时序 reg 隔断。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:197`
- Evidence:
- node_kind: `verilog_rtl`
- detail: flag_mac_result_accept: 6 sources: flag_result_reserved, mac_result_valid, pp_fault, pp_result_queue_count, pp_table_loaded, state_current
- source_excerpt: `flag_mac_result_accept: 6 sources: flag_result_reserved, mac_result_valid, pp_fault, pp_result_queue_count, pp_table_loaded, state_current`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
flag_mac_result_accept: 6 sources: flag_result_reserved, mac_result_valid, pp_fault, pp_result_queue_count, pp_table_loaded, state_current
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-673"></a>
### VG145: 组合逻辑完整依赖锥最多允许三个源信号，超限逻辑必须由时序 reg 隔断。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:195`
- Evidence:
- node_kind: `verilog_rtl`
- detail: flag_mac_result_ready_local: 5 sources: flag_result_reserved, pp_fault, pp_result_queue_count, pp_table_loaded, state_current
- source_excerpt: `flag_mac_result_ready_local: 5 sources: flag_result_reserved, pp_fault, pp_result_queue_count, pp_table_loaded, state_current`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
flag_mac_result_ready_local: 5 sources: flag_result_reserved, pp_fault, pp_result_queue_count, pp_table_loaded, state_current
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-674"></a>
### VG145: 组合逻辑完整依赖锥最多允许三个源信号，超限逻辑必须由时序 reg 隔断。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:202`
- Evidence:
- node_kind: `verilog_rtl`
- detail: flag_start_accept: 13 sources: flag_dw_bias_loaded, flag_dw_cache_loaded, flag_dw_weight_loaded, flag_halo_loaded, flag_load_fault, flag_pw_bias_loaded, flag_pw_weight_loaded, i_pw_only, i_start, i_table_valid, pp_fault, pp_table_loaded, state_current
- source_excerpt: `flag_start_accept: 13 sources: flag_dw_bias_loaded, flag_dw_cache_loaded, flag_dw_weight_loaded, flag_halo_loaded, flag_load_fault, flag_pw_bias_loaded, flag_pw_weight_loaded, i_pw_only, i_start, i_table_valid, pp_fault, pp_table_loaded, state_current`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
flag_start_accept: 13 sources: flag_dw_bias_loaded, flag_dw_cache_loaded, flag_dw_weight_loaded, flag_halo_loaded, flag_load_fault, flag_pw_bias_loaded, flag_pw_weight_loaded, i_pw_only, i_start, i_table_valid, pp_fault, pp_table_loaded, state_current
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-675"></a>
### VG145: 组合逻辑完整依赖锥最多允许三个源信号，超限逻辑必须由时序 reg 隔断。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:245`
- Evidence:
- node_kind: `verilog_rtl`
- detail: halo_index: 4 sources: cnt_mac_group, cnt_output, cnt_position, flag_layer_pw
- source_excerpt: `halo_index: 4 sources: cnt_mac_group, cnt_output, cnt_position, flag_layer_pw`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
halo_index: 4 sources: cnt_mac_group, cnt_output, cnt_position, flag_layer_pw
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-676"></a>
### VG145: 组合逻辑完整依赖锥最多允许三个源信号，超限逻辑必须由时序 reg 隔断。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:245`
- Evidence:
- node_kind: `verilog_rtl`
- detail: next_mac_activation[lane_index*8+:8]: 6 sources: cnt_mac_group, cnt_output, cnt_position, flag_layer_pw, reg_dw_cache[cnt_position*16+cnt_mac_group*8+lane_index], reg_halo[halo_index]
- source_excerpt: `next_mac_activation[lane_index*8+:8]: 6 sources: cnt_mac_group, cnt_output, cnt_position, flag_layer_pw, reg_dw_cache[cnt_position*16+cnt_mac_group*8+lane_index], reg_halo[halo_index]`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
next_mac_activation[lane_index*8+:8]: 6 sources: cnt_mac_group, cnt_output, cnt_position, flag_layer_pw, reg_dw_cache[cnt_position*16+cnt_mac_group*8+lane_index], reg_halo[halo_index]
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-677"></a>
### VG145: 组合逻辑完整依赖锥最多允许三个源信号，超限逻辑必须由时序 reg 隔断。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:245`
- Evidence:
- node_kind: `verilog_rtl`
- detail: next_mac_bias[31:0]: 4 sources: cnt_output, flag_layer_pw, reg_dw_bias[cnt_output], reg_pw_bias[cnt_output*3]
- source_excerpt: `next_mac_bias[31:0]: 4 sources: cnt_output, flag_layer_pw, reg_dw_bias[cnt_output], reg_pw_bias[cnt_output*3]`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
next_mac_bias[31:0]: 4 sources: cnt_output, flag_layer_pw, reg_dw_bias[cnt_output], reg_pw_bias[cnt_output*3]
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-678"></a>
### VG145: 组合逻辑完整依赖锥最多允许三个源信号，超限逻辑必须由时序 reg 隔断。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:245`
- Evidence:
- node_kind: `verilog_rtl`
- detail: next_mac_bias[63:32]: 4 sources: cnt_output, flag_layer_pw, reg_dw_bias[cnt_output], reg_pw_bias[cnt_output*3+1]
- source_excerpt: `next_mac_bias[63:32]: 4 sources: cnt_output, flag_layer_pw, reg_dw_bias[cnt_output], reg_pw_bias[cnt_output*3+1]`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
next_mac_bias[63:32]: 4 sources: cnt_output, flag_layer_pw, reg_dw_bias[cnt_output], reg_pw_bias[cnt_output*3+1]
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-679"></a>
### VG145: 组合逻辑完整依赖锥最多允许三个源信号，超限逻辑必须由时序 reg 隔断。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:245`
- Evidence:
- node_kind: `verilog_rtl`
- detail: next_mac_bias[95:64]: 4 sources: cnt_output, flag_layer_pw, reg_dw_bias[cnt_output], reg_pw_bias[cnt_output*3+2]
- source_excerpt: `next_mac_bias[95:64]: 4 sources: cnt_output, flag_layer_pw, reg_dw_bias[cnt_output], reg_pw_bias[cnt_output*3+2]`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
next_mac_bias[95:64]: 4 sources: cnt_output, flag_layer_pw, reg_dw_bias[cnt_output], reg_pw_bias[cnt_output*3+2]
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-680"></a>
### VG145: 组合逻辑完整依赖锥最多允许三个源信号，超限逻辑必须由时序 reg 隔断。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:245`
- Evidence:
- node_kind: `verilog_rtl`
- detail: next_mac_weight[128+lane_index*8+:8]: 5 sources: cnt_mac_group, cnt_output, flag_layer_pw, reg_dw_weight[weight_index], reg_pw_weight[(output_channel+2)*16+cnt_mac_group*8+lane_index]
- source_excerpt: `next_mac_weight[128+lane_index*8+:8]: 5 sources: cnt_mac_group, cnt_output, flag_layer_pw, reg_dw_weight[weight_index], reg_pw_weight[(output_channel+2)*16+cnt_mac_group*8+lane_index]`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
next_mac_weight[128+lane_index*8+:8]: 5 sources: cnt_mac_group, cnt_output, flag_layer_pw, reg_dw_weight[weight_index], reg_pw_weight[(output_channel+2)*16+cnt_mac_group*8+lane_index]
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-681"></a>
### VG145: 组合逻辑完整依赖锥最多允许三个源信号，超限逻辑必须由时序 reg 隔断。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:245`
- Evidence:
- node_kind: `verilog_rtl`
- detail: next_mac_weight[64+lane_index*8+:8]: 5 sources: cnt_mac_group, cnt_output, flag_layer_pw, reg_dw_weight[weight_index], reg_pw_weight[(output_channel+1)*16+cnt_mac_group*8+lane_index]
- source_excerpt: `next_mac_weight[64+lane_index*8+:8]: 5 sources: cnt_mac_group, cnt_output, flag_layer_pw, reg_dw_weight[weight_index], reg_pw_weight[(output_channel+1)*16+cnt_mac_group*8+lane_index]`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
next_mac_weight[64+lane_index*8+:8]: 5 sources: cnt_mac_group, cnt_output, flag_layer_pw, reg_dw_weight[weight_index], reg_pw_weight[(output_channel+1)*16+cnt_mac_group*8+lane_index]
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-682"></a>
### VG145: 组合逻辑完整依赖锥最多允许三个源信号，超限逻辑必须由时序 reg 隔断。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:245`
- Evidence:
- node_kind: `verilog_rtl`
- detail: next_mac_weight[lane_index*8+:8]: 5 sources: cnt_mac_group, cnt_output, flag_layer_pw, reg_dw_weight[weight_index], reg_pw_weight[output_channel*16+cnt_mac_group*8+lane_index]
- source_excerpt: `next_mac_weight[lane_index*8+:8]: 5 sources: cnt_mac_group, cnt_output, flag_layer_pw, reg_dw_weight[weight_index], reg_pw_weight[output_channel*16+cnt_mac_group*8+lane_index]`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
next_mac_weight[lane_index*8+:8]: 5 sources: cnt_mac_group, cnt_output, flag_layer_pw, reg_dw_weight[weight_index], reg_pw_weight[output_channel*16+cnt_mac_group*8+lane_index]
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-683"></a>
### VG145: 组合逻辑完整依赖锥最多允许三个源信号，超限逻辑必须由时序 reg 隔断。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:211`
- Evidence:
- node_kind: `verilog_rtl`
- detail: o_load_ready: 5 sources: flag_load_fault, i_export_start, i_start, pp_fault, state_current
- source_excerpt: `o_load_ready: 5 sources: flag_load_fault, i_export_start, i_start, pp_fault, state_current`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
o_load_ready: 5 sources: flag_load_fault, i_export_start, i_start, pp_fault, state_current
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-684"></a>
### VG145: 组合逻辑完整依赖锥最多允许三个源信号，超限逻辑必须由时序 reg 隔断。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:208`
- Evidence:
- node_kind: `verilog_rtl`
- detail: o_table_ready: 4 sources: i_export_start, i_start, pp_table_ready, state_current
- source_excerpt: `o_table_ready: 4 sources: i_export_start, i_start, pp_table_ready, state_current`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
o_table_ready: 4 sources: i_export_start, i_start, pp_table_ready, state_current
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-685"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=ST_MAC_WAIT; child_output=down2_overlap_tile_runner.ST_MAC_WAIT; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=ST_MAC_WAIT; child_output=down2_overlap_tile_runner.ST_MAC_WAIT; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=ST_MAC_WAIT; child_output=down2_overlap_tile_runner.ST_MAC_WAIT; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-686"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=cnt_export_cycles$enable; child_output=down2_overlap_tile_runner.cnt_export_cycles$enable; operation_count=3; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=cnt_export_cycles$enable; child_output=down2_overlap_tile_runner.cnt_export_cycles$enable; operation_count=3; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=cnt_export_cycles$enable; child_output=down2_overlap_tile_runner.cnt_export_cycles$enable; operation_count=3; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-687"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=cnt_position$D; child_output=down2_overlap_tile_runner.cnt_position$D; operation_count=1; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=cnt_position$D; child_output=down2_overlap_tile_runner.cnt_position$D; operation_count=1; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=cnt_position$D; child_output=down2_overlap_tile_runner.cnt_position$D; operation_count=1; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-688"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=flag_debug_layer_o$D; child_output=down2_overlap_tile_runner.flag_debug_layer_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=flag_debug_layer_o$D; child_output=down2_overlap_tile_runner.flag_debug_layer_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=flag_debug_layer_o$D; child_output=down2_overlap_tile_runner.flag_debug_layer_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-689"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=flag_done_o$enable; child_output=down2_overlap_tile_runner.flag_done_o$enable; operation_count=1; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=flag_done_o$enable; child_output=down2_overlap_tile_runner.flag_done_o$enable; operation_count=1; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=flag_done_o$enable; child_output=down2_overlap_tile_runner.flag_done_o$enable; operation_count=1; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-690"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=mac_fault; child_output=down2_overlap_tile_runner.mac_fault; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=mac_fault; child_output=down2_overlap_tile_runner.mac_fault; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=mac_fault; child_output=down2_overlap_tile_runner.mac_fault; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-691"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=mac_input_ready; child_output=down2_overlap_tile_runner.mac_input_ready; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=mac_input_ready; child_output=down2_overlap_tile_runner.mac_input_ready; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=mac_input_ready; child_output=down2_overlap_tile_runner.mac_input_ready; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-692"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=mac_result_data; child_output=down2_overlap_tile_runner.mac_result_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=mac_result_data; child_output=down2_overlap_tile_runner.mac_result_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=mac_result_data; child_output=down2_overlap_tile_runner.mac_result_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-693"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=mac_result_valid; child_output=down2_overlap_tile_runner.mac_result_valid; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=mac_result_valid; child_output=down2_overlap_tile_runner.mac_result_valid; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=mac_result_valid; child_output=down2_overlap_tile_runner.mac_result_valid; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-694"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=pp_fault; child_output=down2_overlap_tile_runner.pp_fault; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=pp_fault; child_output=down2_overlap_tile_runner.pp_fault; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=pp_fault; child_output=down2_overlap_tile_runner.pp_fault; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-695"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=pp_input_ready; child_output=down2_overlap_tile_runner.pp_input_ready; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=pp_input_ready; child_output=down2_overlap_tile_runner.pp_input_ready; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=pp_input_ready; child_output=down2_overlap_tile_runner.pp_input_ready; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-696"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=pp_meta_count; child_output=down2_overlap_tile_runner.pp_meta_count; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=pp_meta_count; child_output=down2_overlap_tile_runner.pp_meta_count; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=pp_meta_count; child_output=down2_overlap_tile_runner.pp_meta_count; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-697"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=pp_output_data; child_output=down2_overlap_tile_runner.pp_output_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=pp_output_data; child_output=down2_overlap_tile_runner.pp_output_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=pp_output_data; child_output=down2_overlap_tile_runner.pp_output_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-698"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=pp_output_tag; child_output=down2_overlap_tile_runner.pp_output_tag; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=pp_output_tag; child_output=down2_overlap_tile_runner.pp_output_tag; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=pp_output_tag; child_output=down2_overlap_tile_runner.pp_output_tag; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-699"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=pp_output_valid; child_output=down2_overlap_tile_runner.pp_output_valid; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=pp_output_valid; child_output=down2_overlap_tile_runner.pp_output_valid; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=pp_output_valid; child_output=down2_overlap_tile_runner.pp_output_valid; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-700"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=pp_post_accept; child_output=down2_overlap_tile_runner.pp_post_accept; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=pp_post_accept; child_output=down2_overlap_tile_runner.pp_post_accept; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=pp_post_accept; child_output=down2_overlap_tile_runner.pp_post_accept; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-701"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=pp_post_busy; child_output=down2_overlap_tile_runner.pp_post_busy; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=pp_post_busy; child_output=down2_overlap_tile_runner.pp_post_busy; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=pp_post_busy; child_output=down2_overlap_tile_runner.pp_post_busy; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-702"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=pp_pre_accept; child_output=down2_overlap_tile_runner.pp_pre_accept; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=pp_pre_accept; child_output=down2_overlap_tile_runner.pp_pre_accept; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=pp_pre_accept; child_output=down2_overlap_tile_runner.pp_pre_accept; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-703"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=pp_pre_busy; child_output=down2_overlap_tile_runner.pp_pre_busy; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=pp_pre_busy; child_output=down2_overlap_tile_runner.pp_pre_busy; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=pp_pre_busy; child_output=down2_overlap_tile_runner.pp_pre_busy; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-704"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=pp_result_queue_count; child_output=down2_overlap_tile_runner.pp_result_queue_count; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=pp_result_queue_count; child_output=down2_overlap_tile_runner.pp_result_queue_count; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=pp_result_queue_count; child_output=down2_overlap_tile_runner.pp_result_queue_count; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-705"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=pp_silu_accept; child_output=down2_overlap_tile_runner.pp_silu_accept; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=pp_silu_accept; child_output=down2_overlap_tile_runner.pp_silu_accept; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=pp_silu_accept; child_output=down2_overlap_tile_runner.pp_silu_accept; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-706"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=pp_silu_busy; child_output=down2_overlap_tile_runner.pp_silu_busy; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=pp_silu_busy; child_output=down2_overlap_tile_runner.pp_silu_busy; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=pp_silu_busy; child_output=down2_overlap_tile_runner.pp_silu_busy; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-707"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=pp_table_fault; child_output=down2_overlap_tile_runner.pp_table_fault; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=pp_table_fault; child_output=down2_overlap_tile_runner.pp_table_fault; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=pp_table_fault; child_output=down2_overlap_tile_runner.pp_table_fault; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-708"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=pp_table_loaded; child_output=down2_overlap_tile_runner.pp_table_loaded; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=pp_table_loaded; child_output=down2_overlap_tile_runner.pp_table_loaded; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=pp_table_loaded; child_output=down2_overlap_tile_runner.pp_table_loaded; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-709"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=pp_table_ready; child_output=down2_overlap_tile_runner.pp_table_ready; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=pp_table_ready; child_output=down2_overlap_tile_runner.pp_table_ready; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=pp_table_ready; child_output=down2_overlap_tile_runner.pp_table_ready; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-710"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_debug_position_o$D; child_output=down2_overlap_tile_runner.reg_debug_position_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_debug_position_o$D; child_output=down2_overlap_tile_runner.reg_debug_position_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_debug_position_o$D; child_output=down2_overlap_tile_runner.reg_debug_position_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-711"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_debug_value_o$D; child_output=down2_overlap_tile_runner.reg_debug_value_o$D; operation_count=0; limit=3; inconclusive_reason=$signed: missing function definition | missing module implementation | reg_debug_value_o$D: missing storage data expression; loop_presence=unknown
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_debug_value_o$D; child_output=down2_overlap_tile_runner.reg_debug_value_o$D; operation_count=0; limit=3; inconclusive_reason=$signed: missing function definition | missing module implementation | reg_debug_value_o$D: missing storage data expression; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_debug_value_o$D; child_output=down2_overlap_tile_runner.reg_debug_value_o$D; operation_count=0; limit=3; inconclusive_reason=$signed: missing function definition | missing module implementation | reg_debug_value_o$D: missing storage data expression; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-712"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_dw_bias[i_load_addr]$D; child_output=down2_overlap_tile_runner.reg_dw_bias[i_load_addr]$D; operation_count=0; limit=3; inconclusive_reason=reg_dw_bias[i_load_addr]$D: missing storage data expression; loop_presence=absent
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_dw_bias[i_load_addr]$D; child_output=down2_overlap_tile_runner.reg_dw_bias[i_load_addr]$D; operation_count=0; limit=3; inconclusive_reason=reg_dw_bias[i_load_addr]$D: missing storage data expression; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_dw_bias[i_load_addr]$D; child_output=down2_overlap_tile_runner.reg_dw_bias[i_load_addr]$D; operation_count=0; limit=3; inconclusive_reason=reg_dw_bias[i_load_addr]$D: missing storage data expression; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-713"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_dw_cache[i_load_addr]$D; child_output=down2_overlap_tile_runner.reg_dw_cache[i_load_addr]$D; operation_count=0; limit=3; inconclusive_reason=reg_dw_cache[i_load_addr]$D: missing storage data expression; loop_presence=absent
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_dw_cache[i_load_addr]$D; child_output=down2_overlap_tile_runner.reg_dw_cache[i_load_addr]$D; operation_count=0; limit=3; inconclusive_reason=reg_dw_cache[i_load_addr]$D: missing storage data expression; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_dw_cache[i_load_addr]$D; child_output=down2_overlap_tile_runner.reg_dw_cache[i_load_addr]$D; operation_count=0; limit=3; inconclusive_reason=reg_dw_cache[i_load_addr]$D: missing storage data expression; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-714"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_dw_weight[i_load_addr]$D; child_output=down2_overlap_tile_runner.reg_dw_weight[i_load_addr]$D; operation_count=0; limit=3; inconclusive_reason=reg_dw_weight[i_load_addr]$D: missing storage data expression; loop_presence=absent
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_dw_weight[i_load_addr]$D; child_output=down2_overlap_tile_runner.reg_dw_weight[i_load_addr]$D; operation_count=0; limit=3; inconclusive_reason=reg_dw_weight[i_load_addr]$D: missing storage data expression; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_dw_weight[i_load_addr]$D; child_output=down2_overlap_tile_runner.reg_dw_weight[i_load_addr]$D; operation_count=0; limit=3; inconclusive_reason=reg_dw_weight[i_load_addr]$D: missing storage data expression; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-715"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_halo[i_load_addr]$D; child_output=down2_overlap_tile_runner.reg_halo[i_load_addr]$D; operation_count=0; limit=3; inconclusive_reason=reg_halo[i_load_addr]$D: missing storage data expression; loop_presence=absent
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_halo[i_load_addr]$D; child_output=down2_overlap_tile_runner.reg_halo[i_load_addr]$D; operation_count=0; limit=3; inconclusive_reason=reg_halo[i_load_addr]$D: missing storage data expression; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_halo[i_load_addr]$D; child_output=down2_overlap_tile_runner.reg_halo[i_load_addr]$D; operation_count=0; limit=3; inconclusive_reason=reg_halo[i_load_addr]$D: missing storage data expression; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-716"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_mac_activation$enable; child_output=down2_overlap_tile_runner.reg_mac_activation$enable; operation_count=1; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_mac_activation$enable; child_output=down2_overlap_tile_runner.reg_mac_activation$enable; operation_count=1; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_mac_activation$enable; child_output=down2_overlap_tile_runner.reg_mac_activation$enable; operation_count=1; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-717"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_mac_bias$enable; child_output=down2_overlap_tile_runner.reg_mac_bias$enable; operation_count=1; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_mac_bias$enable; child_output=down2_overlap_tile_runner.reg_mac_bias$enable; operation_count=1; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_mac_bias$enable; child_output=down2_overlap_tile_runner.reg_mac_bias$enable; operation_count=1; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-718"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_mac_mask$enable; child_output=down2_overlap_tile_runner.reg_mac_mask$enable; operation_count=1; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_mac_mask$enable; child_output=down2_overlap_tile_runner.reg_mac_mask$enable; operation_count=1; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_mac_mask$enable; child_output=down2_overlap_tile_runner.reg_mac_mask$enable; operation_count=1; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-719"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_mac_weight$enable; child_output=down2_overlap_tile_runner.reg_mac_weight$enable; operation_count=1; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_mac_weight$enable; child_output=down2_overlap_tile_runner.reg_mac_weight$enable; operation_count=1; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_mac_weight$enable; child_output=down2_overlap_tile_runner.reg_mac_weight$enable; operation_count=1; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-720"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_pw_bias[i_load_addr]$D; child_output=down2_overlap_tile_runner.reg_pw_bias[i_load_addr]$D; operation_count=0; limit=3; inconclusive_reason=reg_pw_bias[i_load_addr]$D: missing storage data expression; loop_presence=absent
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_pw_bias[i_load_addr]$D; child_output=down2_overlap_tile_runner.reg_pw_bias[i_load_addr]$D; operation_count=0; limit=3; inconclusive_reason=reg_pw_bias[i_load_addr]$D: missing storage data expression; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_pw_bias[i_load_addr]$D; child_output=down2_overlap_tile_runner.reg_pw_bias[i_load_addr]$D; operation_count=0; limit=3; inconclusive_reason=reg_pw_bias[i_load_addr]$D: missing storage data expression; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-721"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_pw_weight[i_load_addr]$D; child_output=down2_overlap_tile_runner.reg_pw_weight[i_load_addr]$D; operation_count=0; limit=3; inconclusive_reason=reg_pw_weight[i_load_addr]$D: missing storage data expression; loop_presence=absent
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_pw_weight[i_load_addr]$D; child_output=down2_overlap_tile_runner.reg_pw_weight[i_load_addr]$D; operation_count=0; limit=3; inconclusive_reason=reg_pw_weight[i_load_addr]$D: missing storage data expression; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_pw_weight[i_load_addr]$D; child_output=down2_overlap_tile_runner.reg_pw_weight[i_load_addr]$D; operation_count=0; limit=3; inconclusive_reason=reg_pw_weight[i_load_addr]$D: missing storage data expression; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-722"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=state_current$D; child_output=down2_overlap_tile_runner.state_current$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=state_current$D; child_output=down2_overlap_tile_runner.state_current$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=state_current$D; child_output=down2_overlap_tile_runner.state_current$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-723"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:290`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=state_current; child_output=down2_overlap_tile_runner.state_current; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=state_current; child_output=down2_overlap_tile_runner.state_current; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=state_current; child_output=down2_overlap_tile_runner.state_current; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-724"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:291`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=flag_layer_pw; child_output=down2_overlap_tile_runner.flag_layer_pw; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=flag_layer_pw; child_output=down2_overlap_tile_runner.flag_layer_pw; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=flag_layer_pw; child_output=down2_overlap_tile_runner.flag_layer_pw; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-725"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:292`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=flag_busy_o; child_output=down2_overlap_tile_runner.flag_busy_o; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=flag_busy_o; child_output=down2_overlap_tile_runner.flag_busy_o; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=flag_busy_o; child_output=down2_overlap_tile_runner.flag_busy_o; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-726"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:294`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=flag_result_reserved; child_output=down2_overlap_tile_runner.flag_result_reserved; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=flag_result_reserved; child_output=down2_overlap_tile_runner.flag_result_reserved; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=flag_result_reserved; child_output=down2_overlap_tile_runner.flag_result_reserved; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-727"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:294`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_mac_activation; child_output=down2_overlap_tile_runner.reg_mac_activation; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_mac_activation; child_output=down2_overlap_tile_runner.reg_mac_activation; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_mac_activation; child_output=down2_overlap_tile_runner.reg_mac_activation; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-728"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:295`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=cnt_mac_group; child_output=down2_overlap_tile_runner.cnt_mac_group; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=cnt_mac_group; child_output=down2_overlap_tile_runner.cnt_mac_group; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=cnt_mac_group; child_output=down2_overlap_tile_runner.cnt_mac_group; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-729"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:295`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=cnt_position; child_output=down2_overlap_tile_runner.cnt_position; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=cnt_position; child_output=down2_overlap_tile_runner.cnt_position; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=cnt_position; child_output=down2_overlap_tile_runner.cnt_position; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-730"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:295`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_mac_weight; child_output=down2_overlap_tile_runner.reg_mac_weight; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_mac_weight; child_output=down2_overlap_tile_runner.reg_mac_weight; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_mac_weight; child_output=down2_overlap_tile_runner.reg_mac_weight; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-731"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:296`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_mac_bias; child_output=down2_overlap_tile_runner.reg_mac_bias; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_mac_bias; child_output=down2_overlap_tile_runner.reg_mac_bias; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_mac_bias; child_output=down2_overlap_tile_runner.reg_mac_bias; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-732"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:297`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_mac_mask; child_output=down2_overlap_tile_runner.reg_mac_mask; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_mac_mask; child_output=down2_overlap_tile_runner.reg_mac_mask; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_mac_mask; child_output=down2_overlap_tile_runner.reg_mac_mask; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-733"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=ST_MAC_WAIT; child_output=down2_overlap_tile_runner.ST_MAC_WAIT; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=ST_MAC_WAIT; child_output=down2_overlap_tile_runner.ST_MAC_WAIT; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=ST_MAC_WAIT; child_output=down2_overlap_tile_runner.ST_MAC_WAIT; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-734"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=cnt_core_cycles$enable; child_output=down2_overlap_tile_runner.cnt_core_cycles$enable; operation_count=15; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=cnt_core_cycles$enable; child_output=down2_overlap_tile_runner.cnt_core_cycles$enable; operation_count=15; limit=3; inconclusive_reason=missing module implementation; loop_presence=present`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=cnt_core_cycles$enable; child_output=down2_overlap_tile_runner.cnt_core_cycles$enable; operation_count=15; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-735"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=cnt_dw_writes$enable; child_output=down2_overlap_tile_runner.cnt_dw_writes$enable; operation_count=18; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=cnt_dw_writes$enable; child_output=down2_overlap_tile_runner.cnt_dw_writes$enable; operation_count=18; limit=3; inconclusive_reason=missing module implementation; loop_presence=present`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=cnt_dw_writes$enable; child_output=down2_overlap_tile_runner.cnt_dw_writes$enable; operation_count=18; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-736"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=cnt_expected_dw_bias$enable; child_output=down2_overlap_tile_runner.cnt_expected_dw_bias$enable; operation_count=13; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=cnt_expected_dw_bias$enable; child_output=down2_overlap_tile_runner.cnt_expected_dw_bias$enable; operation_count=13; limit=3; inconclusive_reason=missing module implementation; loop_presence=present`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=cnt_expected_dw_bias$enable; child_output=down2_overlap_tile_runner.cnt_expected_dw_bias$enable; operation_count=13; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-737"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=cnt_expected_dw_cache$enable; child_output=down2_overlap_tile_runner.cnt_expected_dw_cache$enable; operation_count=13; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=cnt_expected_dw_cache$enable; child_output=down2_overlap_tile_runner.cnt_expected_dw_cache$enable; operation_count=13; limit=3; inconclusive_reason=missing module implementation; loop_presence=present`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=cnt_expected_dw_cache$enable; child_output=down2_overlap_tile_runner.cnt_expected_dw_cache$enable; operation_count=13; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-738"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=cnt_expected_dw_weight$enable; child_output=down2_overlap_tile_runner.cnt_expected_dw_weight$enable; operation_count=13; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=cnt_expected_dw_weight$enable; child_output=down2_overlap_tile_runner.cnt_expected_dw_weight$enable; operation_count=13; limit=3; inconclusive_reason=missing module implementation; loop_presence=present`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=cnt_expected_dw_weight$enable; child_output=down2_overlap_tile_runner.cnt_expected_dw_weight$enable; operation_count=13; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-739"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=cnt_expected_halo$enable; child_output=down2_overlap_tile_runner.cnt_expected_halo$enable; operation_count=13; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=cnt_expected_halo$enable; child_output=down2_overlap_tile_runner.cnt_expected_halo$enable; operation_count=13; limit=3; inconclusive_reason=missing module implementation; loop_presence=present`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=cnt_expected_halo$enable; child_output=down2_overlap_tile_runner.cnt_expected_halo$enable; operation_count=13; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-740"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=cnt_expected_pw_bias$enable; child_output=down2_overlap_tile_runner.cnt_expected_pw_bias$enable; operation_count=13; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=cnt_expected_pw_bias$enable; child_output=down2_overlap_tile_runner.cnt_expected_pw_bias$enable; operation_count=13; limit=3; inconclusive_reason=missing module implementation; loop_presence=present`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=cnt_expected_pw_bias$enable; child_output=down2_overlap_tile_runner.cnt_expected_pw_bias$enable; operation_count=13; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-741"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=cnt_expected_pw_weight$enable; child_output=down2_overlap_tile_runner.cnt_expected_pw_weight$enable; operation_count=13; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=cnt_expected_pw_weight$enable; child_output=down2_overlap_tile_runner.cnt_expected_pw_weight$enable; operation_count=13; limit=3; inconclusive_reason=missing module implementation; loop_presence=present`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=cnt_expected_pw_weight$enable; child_output=down2_overlap_tile_runner.cnt_expected_pw_weight$enable; operation_count=13; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-742"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=cnt_export$enable; child_output=down2_overlap_tile_runner.cnt_export$enable; operation_count=20; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=cnt_export$enable; child_output=down2_overlap_tile_runner.cnt_export$enable; operation_count=20; limit=3; inconclusive_reason=missing module implementation; loop_presence=present`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=cnt_export$enable; child_output=down2_overlap_tile_runner.cnt_export$enable; operation_count=20; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-743"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=cnt_export_cycles$enable; child_output=down2_overlap_tile_runner.cnt_export_cycles$enable; operation_count=3; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=cnt_export_cycles$enable; child_output=down2_overlap_tile_runner.cnt_export_cycles$enable; operation_count=3; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=cnt_export_cycles$enable; child_output=down2_overlap_tile_runner.cnt_export_cycles$enable; operation_count=3; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-744"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=cnt_mac_cycles$enable; child_output=down2_overlap_tile_runner.cnt_mac_cycles$enable; operation_count=20; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=cnt_mac_cycles$enable; child_output=down2_overlap_tile_runner.cnt_mac_cycles$enable; operation_count=20; limit=3; inconclusive_reason=missing module implementation; loop_presence=present`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=cnt_mac_cycles$enable; child_output=down2_overlap_tile_runner.cnt_mac_cycles$enable; operation_count=20; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-745"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=cnt_mac_group$enable; child_output=down2_overlap_tile_runner.cnt_mac_group$enable; operation_count=36; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=cnt_mac_group$enable; child_output=down2_overlap_tile_runner.cnt_mac_group$enable; operation_count=36; limit=3; inconclusive_reason=missing module implementation; loop_presence=present`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=cnt_mac_group$enable; child_output=down2_overlap_tile_runner.cnt_mac_group$enable; operation_count=36; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-746"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=cnt_mac_results$enable; child_output=down2_overlap_tile_runner.cnt_mac_results$enable; operation_count=23; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=cnt_mac_results$enable; child_output=down2_overlap_tile_runner.cnt_mac_results$enable; operation_count=23; limit=3; inconclusive_reason=missing module implementation; loop_presence=present`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=cnt_mac_results$enable; child_output=down2_overlap_tile_runner.cnt_mac_results$enable; operation_count=23; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-747"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=cnt_output$enable; child_output=down2_overlap_tile_runner.cnt_output$enable; operation_count=30; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=cnt_output$enable; child_output=down2_overlap_tile_runner.cnt_output$enable; operation_count=30; limit=3; inconclusive_reason=missing module implementation; loop_presence=present`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=cnt_output$enable; child_output=down2_overlap_tile_runner.cnt_output$enable; operation_count=30; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-748"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=cnt_position$D; child_output=down2_overlap_tile_runner.cnt_position$D; operation_count=1; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=cnt_position$D; child_output=down2_overlap_tile_runner.cnt_position$D; operation_count=1; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=cnt_position$D; child_output=down2_overlap_tile_runner.cnt_position$D; operation_count=1; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-749"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=cnt_position$enable; child_output=down2_overlap_tile_runner.cnt_position$enable; operation_count=30; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=cnt_position$enable; child_output=down2_overlap_tile_runner.cnt_position$enable; operation_count=30; limit=3; inconclusive_reason=missing module implementation; loop_presence=present`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=cnt_position$enable; child_output=down2_overlap_tile_runner.cnt_position$enable; operation_count=30; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-750"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=cnt_post_accepts$enable; child_output=down2_overlap_tile_runner.cnt_post_accepts$enable; operation_count=15; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=cnt_post_accepts$enable; child_output=down2_overlap_tile_runner.cnt_post_accepts$enable; operation_count=15; limit=3; inconclusive_reason=missing module implementation; loop_presence=present`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=cnt_post_accepts$enable; child_output=down2_overlap_tile_runner.cnt_post_accepts$enable; operation_count=15; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-751"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=cnt_post_cycles$enable; child_output=down2_overlap_tile_runner.cnt_post_cycles$enable; operation_count=15; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=cnt_post_cycles$enable; child_output=down2_overlap_tile_runner.cnt_post_cycles$enable; operation_count=15; limit=3; inconclusive_reason=missing module implementation; loop_presence=present`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=cnt_post_cycles$enable; child_output=down2_overlap_tile_runner.cnt_post_cycles$enable; operation_count=15; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-752"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=cnt_pre_accepts$enable; child_output=down2_overlap_tile_runner.cnt_pre_accepts$enable; operation_count=15; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=cnt_pre_accepts$enable; child_output=down2_overlap_tile_runner.cnt_pre_accepts$enable; operation_count=15; limit=3; inconclusive_reason=missing module implementation; loop_presence=present`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=cnt_pre_accepts$enable; child_output=down2_overlap_tile_runner.cnt_pre_accepts$enable; operation_count=15; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-753"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=cnt_pre_cycles$enable; child_output=down2_overlap_tile_runner.cnt_pre_cycles$enable; operation_count=15; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=cnt_pre_cycles$enable; child_output=down2_overlap_tile_runner.cnt_pre_cycles$enable; operation_count=15; limit=3; inconclusive_reason=missing module implementation; loop_presence=present`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=cnt_pre_cycles$enable; child_output=down2_overlap_tile_runner.cnt_pre_cycles$enable; operation_count=15; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-754"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=cnt_preload_writes$enable; child_output=down2_overlap_tile_runner.cnt_preload_writes$enable; operation_count=10; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=cnt_preload_writes$enable; child_output=down2_overlap_tile_runner.cnt_preload_writes$enable; operation_count=10; limit=3; inconclusive_reason=missing module implementation; loop_presence=present`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=cnt_preload_writes$enable; child_output=down2_overlap_tile_runner.cnt_preload_writes$enable; operation_count=10; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-755"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=cnt_pw_writes$enable; child_output=down2_overlap_tile_runner.cnt_pw_writes$enable; operation_count=18; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=cnt_pw_writes$enable; child_output=down2_overlap_tile_runner.cnt_pw_writes$enable; operation_count=18; limit=3; inconclusive_reason=missing module implementation; loop_presence=present`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=cnt_pw_writes$enable; child_output=down2_overlap_tile_runner.cnt_pw_writes$enable; operation_count=18; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-756"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=cnt_scheduler_idle_cycles$enable; child_output=down2_overlap_tile_runner.cnt_scheduler_idle_cycles$enable; operation_count=32; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=cnt_scheduler_idle_cycles$enable; child_output=down2_overlap_tile_runner.cnt_scheduler_idle_cycles$enable; operation_count=32; limit=3; inconclusive_reason=missing module implementation; loop_presence=present`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=cnt_scheduler_idle_cycles$enable; child_output=down2_overlap_tile_runner.cnt_scheduler_idle_cycles$enable; operation_count=32; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-757"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=cnt_silu_accepts$enable; child_output=down2_overlap_tile_runner.cnt_silu_accepts$enable; operation_count=15; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=cnt_silu_accepts$enable; child_output=down2_overlap_tile_runner.cnt_silu_accepts$enable; operation_count=15; limit=3; inconclusive_reason=missing module implementation; loop_presence=present`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=cnt_silu_accepts$enable; child_output=down2_overlap_tile_runner.cnt_silu_accepts$enable; operation_count=15; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-758"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=cnt_silu_cycles$enable; child_output=down2_overlap_tile_runner.cnt_silu_cycles$enable; operation_count=15; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=cnt_silu_cycles$enable; child_output=down2_overlap_tile_runner.cnt_silu_cycles$enable; operation_count=15; limit=3; inconclusive_reason=missing module implementation; loop_presence=present`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=cnt_silu_cycles$enable; child_output=down2_overlap_tile_runner.cnt_silu_cycles$enable; operation_count=15; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-759"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=cnt_storage_wait_cycles$enable; child_output=down2_overlap_tile_runner.cnt_storage_wait_cycles$enable; operation_count=29; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=cnt_storage_wait_cycles$enable; child_output=down2_overlap_tile_runner.cnt_storage_wait_cycles$enable; operation_count=29; limit=3; inconclusive_reason=missing module implementation; loop_presence=present`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=cnt_storage_wait_cycles$enable; child_output=down2_overlap_tile_runner.cnt_storage_wait_cycles$enable; operation_count=29; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-760"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=cnt_writeback_cycles$enable; child_output=down2_overlap_tile_runner.cnt_writeback_cycles$enable; operation_count=15; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=cnt_writeback_cycles$enable; child_output=down2_overlap_tile_runner.cnt_writeback_cycles$enable; operation_count=15; limit=3; inconclusive_reason=missing module implementation; loop_presence=present`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=cnt_writeback_cycles$enable; child_output=down2_overlap_tile_runner.cnt_writeback_cycles$enable; operation_count=15; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-761"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=cnt_writebacks$enable; child_output=down2_overlap_tile_runner.cnt_writebacks$enable; operation_count=17; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=cnt_writebacks$enable; child_output=down2_overlap_tile_runner.cnt_writebacks$enable; operation_count=17; limit=3; inconclusive_reason=missing module implementation; loop_presence=present`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=cnt_writebacks$enable; child_output=down2_overlap_tile_runner.cnt_writebacks$enable; operation_count=17; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-762"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=flag_busy_o$enable; child_output=down2_overlap_tile_runner.flag_busy_o$enable; operation_count=24; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=flag_busy_o$enable; child_output=down2_overlap_tile_runner.flag_busy_o$enable; operation_count=24; limit=3; inconclusive_reason=missing module implementation; loop_presence=present`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=flag_busy_o$enable; child_output=down2_overlap_tile_runner.flag_busy_o$enable; operation_count=24; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-763"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=flag_debug_layer_o$D; child_output=down2_overlap_tile_runner.flag_debug_layer_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=flag_debug_layer_o$D; child_output=down2_overlap_tile_runner.flag_debug_layer_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=flag_debug_layer_o$D; child_output=down2_overlap_tile_runner.flag_debug_layer_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-764"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=flag_debug_layer_o$enable; child_output=down2_overlap_tile_runner.flag_debug_layer_o$enable; operation_count=11; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=flag_debug_layer_o$enable; child_output=down2_overlap_tile_runner.flag_debug_layer_o$enable; operation_count=11; limit=3; inconclusive_reason=missing module implementation; loop_presence=present`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=flag_debug_layer_o$enable; child_output=down2_overlap_tile_runner.flag_debug_layer_o$enable; operation_count=11; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-765"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=flag_debug_valid_o$enable; child_output=down2_overlap_tile_runner.flag_debug_valid_o$enable; operation_count=11; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=flag_debug_valid_o$enable; child_output=down2_overlap_tile_runner.flag_debug_valid_o$enable; operation_count=11; limit=3; inconclusive_reason=missing module implementation; loop_presence=present`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=flag_debug_valid_o$enable; child_output=down2_overlap_tile_runner.flag_debug_valid_o$enable; operation_count=11; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-766"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=flag_done_o$enable; child_output=down2_overlap_tile_runner.flag_done_o$enable; operation_count=1; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=flag_done_o$enable; child_output=down2_overlap_tile_runner.flag_done_o$enable; operation_count=1; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=flag_done_o$enable; child_output=down2_overlap_tile_runner.flag_done_o$enable; operation_count=1; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-767"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=flag_dw_bias_loaded$enable; child_output=down2_overlap_tile_runner.flag_dw_bias_loaded$enable; operation_count=13; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=flag_dw_bias_loaded$enable; child_output=down2_overlap_tile_runner.flag_dw_bias_loaded$enable; operation_count=13; limit=3; inconclusive_reason=missing module implementation; loop_presence=present`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=flag_dw_bias_loaded$enable; child_output=down2_overlap_tile_runner.flag_dw_bias_loaded$enable; operation_count=13; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-768"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=flag_dw_cache_loaded$enable; child_output=down2_overlap_tile_runner.flag_dw_cache_loaded$enable; operation_count=13; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=flag_dw_cache_loaded$enable; child_output=down2_overlap_tile_runner.flag_dw_cache_loaded$enable; operation_count=13; limit=3; inconclusive_reason=missing module implementation; loop_presence=present`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=flag_dw_cache_loaded$enable; child_output=down2_overlap_tile_runner.flag_dw_cache_loaded$enable; operation_count=13; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-769"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=flag_dw_weight_loaded$enable; child_output=down2_overlap_tile_runner.flag_dw_weight_loaded$enable; operation_count=13; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=flag_dw_weight_loaded$enable; child_output=down2_overlap_tile_runner.flag_dw_weight_loaded$enable; operation_count=13; limit=3; inconclusive_reason=missing module implementation; loop_presence=present`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=flag_dw_weight_loaded$enable; child_output=down2_overlap_tile_runner.flag_dw_weight_loaded$enable; operation_count=13; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-770"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=flag_export_done_o$enable; child_output=down2_overlap_tile_runner.flag_export_done_o$enable; operation_count=4; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=flag_export_done_o$enable; child_output=down2_overlap_tile_runner.flag_export_done_o$enable; operation_count=4; limit=3; inconclusive_reason=missing module implementation; loop_presence=present`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=flag_export_done_o$enable; child_output=down2_overlap_tile_runner.flag_export_done_o$enable; operation_count=4; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-771"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=flag_fault_o$enable; child_output=down2_overlap_tile_runner.flag_fault_o$enable; operation_count=24; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=flag_fault_o$enable; child_output=down2_overlap_tile_runner.flag_fault_o$enable; operation_count=24; limit=3; inconclusive_reason=missing module implementation; loop_presence=present`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=flag_fault_o$enable; child_output=down2_overlap_tile_runner.flag_fault_o$enable; operation_count=24; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-772"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=flag_halo_loaded$enable; child_output=down2_overlap_tile_runner.flag_halo_loaded$enable; operation_count=13; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=flag_halo_loaded$enable; child_output=down2_overlap_tile_runner.flag_halo_loaded$enable; operation_count=13; limit=3; inconclusive_reason=missing module implementation; loop_presence=present`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=flag_halo_loaded$enable; child_output=down2_overlap_tile_runner.flag_halo_loaded$enable; operation_count=13; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-773"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=flag_layer_pw$enable; child_output=down2_overlap_tile_runner.flag_layer_pw$enable; operation_count=17; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=flag_layer_pw$enable; child_output=down2_overlap_tile_runner.flag_layer_pw$enable; operation_count=17; limit=3; inconclusive_reason=missing module implementation; loop_presence=present`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=flag_layer_pw$enable; child_output=down2_overlap_tile_runner.flag_layer_pw$enable; operation_count=17; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-774"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=flag_load_fault$enable; child_output=down2_overlap_tile_runner.flag_load_fault$enable; operation_count=28; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=flag_load_fault$enable; child_output=down2_overlap_tile_runner.flag_load_fault$enable; operation_count=28; limit=3; inconclusive_reason=missing module implementation; loop_presence=present`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=flag_load_fault$enable; child_output=down2_overlap_tile_runner.flag_load_fault$enable; operation_count=28; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-775"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=flag_pw_bias_loaded$enable; child_output=down2_overlap_tile_runner.flag_pw_bias_loaded$enable; operation_count=13; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=flag_pw_bias_loaded$enable; child_output=down2_overlap_tile_runner.flag_pw_bias_loaded$enable; operation_count=13; limit=3; inconclusive_reason=missing module implementation; loop_presence=present`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=flag_pw_bias_loaded$enable; child_output=down2_overlap_tile_runner.flag_pw_bias_loaded$enable; operation_count=13; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-776"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=flag_pw_weight_loaded$enable; child_output=down2_overlap_tile_runner.flag_pw_weight_loaded$enable; operation_count=13; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=flag_pw_weight_loaded$enable; child_output=down2_overlap_tile_runner.flag_pw_weight_loaded$enable; operation_count=13; limit=3; inconclusive_reason=missing module implementation; loop_presence=present`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=flag_pw_weight_loaded$enable; child_output=down2_overlap_tile_runner.flag_pw_weight_loaded$enable; operation_count=13; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-777"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=flag_result_reserved$enable; child_output=down2_overlap_tile_runner.flag_result_reserved$enable; operation_count=35; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=flag_result_reserved$enable; child_output=down2_overlap_tile_runner.flag_result_reserved$enable; operation_count=35; limit=3; inconclusive_reason=missing module implementation; loop_presence=present`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=flag_result_reserved$enable; child_output=down2_overlap_tile_runner.flag_result_reserved$enable; operation_count=35; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-778"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=flag_tile_valid$enable; child_output=down2_overlap_tile_runner.flag_tile_valid$enable; operation_count=24; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=flag_tile_valid$enable; child_output=down2_overlap_tile_runner.flag_tile_valid$enable; operation_count=24; limit=3; inconclusive_reason=missing module implementation; loop_presence=present`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=flag_tile_valid$enable; child_output=down2_overlap_tile_runner.flag_tile_valid$enable; operation_count=24; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-779"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=mac_fault; child_output=down2_overlap_tile_runner.mac_fault; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=mac_fault; child_output=down2_overlap_tile_runner.mac_fault; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=mac_fault; child_output=down2_overlap_tile_runner.mac_fault; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-780"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=mac_input_ready; child_output=down2_overlap_tile_runner.mac_input_ready; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=mac_input_ready; child_output=down2_overlap_tile_runner.mac_input_ready; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=mac_input_ready; child_output=down2_overlap_tile_runner.mac_input_ready; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-781"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=mac_result_data; child_output=down2_overlap_tile_runner.mac_result_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=mac_result_data; child_output=down2_overlap_tile_runner.mac_result_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=mac_result_data; child_output=down2_overlap_tile_runner.mac_result_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-782"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=mac_result_valid; child_output=down2_overlap_tile_runner.mac_result_valid; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=mac_result_valid; child_output=down2_overlap_tile_runner.mac_result_valid; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=mac_result_valid; child_output=down2_overlap_tile_runner.mac_result_valid; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-783"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=pp_fault; child_output=down2_overlap_tile_runner.pp_fault; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=pp_fault; child_output=down2_overlap_tile_runner.pp_fault; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=pp_fault; child_output=down2_overlap_tile_runner.pp_fault; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-784"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=pp_input_ready; child_output=down2_overlap_tile_runner.pp_input_ready; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=pp_input_ready; child_output=down2_overlap_tile_runner.pp_input_ready; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=pp_input_ready; child_output=down2_overlap_tile_runner.pp_input_ready; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-785"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=pp_meta_count; child_output=down2_overlap_tile_runner.pp_meta_count; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=pp_meta_count; child_output=down2_overlap_tile_runner.pp_meta_count; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=pp_meta_count; child_output=down2_overlap_tile_runner.pp_meta_count; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-786"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=pp_output_data; child_output=down2_overlap_tile_runner.pp_output_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=pp_output_data; child_output=down2_overlap_tile_runner.pp_output_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=pp_output_data; child_output=down2_overlap_tile_runner.pp_output_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-787"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=pp_output_tag; child_output=down2_overlap_tile_runner.pp_output_tag; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=pp_output_tag; child_output=down2_overlap_tile_runner.pp_output_tag; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=pp_output_tag; child_output=down2_overlap_tile_runner.pp_output_tag; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-788"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=pp_output_valid; child_output=down2_overlap_tile_runner.pp_output_valid; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=pp_output_valid; child_output=down2_overlap_tile_runner.pp_output_valid; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=pp_output_valid; child_output=down2_overlap_tile_runner.pp_output_valid; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-789"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=pp_post_accept; child_output=down2_overlap_tile_runner.pp_post_accept; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=pp_post_accept; child_output=down2_overlap_tile_runner.pp_post_accept; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=pp_post_accept; child_output=down2_overlap_tile_runner.pp_post_accept; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-790"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=pp_post_busy; child_output=down2_overlap_tile_runner.pp_post_busy; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=pp_post_busy; child_output=down2_overlap_tile_runner.pp_post_busy; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=pp_post_busy; child_output=down2_overlap_tile_runner.pp_post_busy; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-791"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=pp_pre_accept; child_output=down2_overlap_tile_runner.pp_pre_accept; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=pp_pre_accept; child_output=down2_overlap_tile_runner.pp_pre_accept; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=pp_pre_accept; child_output=down2_overlap_tile_runner.pp_pre_accept; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-792"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=pp_pre_busy; child_output=down2_overlap_tile_runner.pp_pre_busy; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=pp_pre_busy; child_output=down2_overlap_tile_runner.pp_pre_busy; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=pp_pre_busy; child_output=down2_overlap_tile_runner.pp_pre_busy; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-793"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=pp_result_queue_count; child_output=down2_overlap_tile_runner.pp_result_queue_count; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=pp_result_queue_count; child_output=down2_overlap_tile_runner.pp_result_queue_count; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=pp_result_queue_count; child_output=down2_overlap_tile_runner.pp_result_queue_count; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-794"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=pp_silu_accept; child_output=down2_overlap_tile_runner.pp_silu_accept; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=pp_silu_accept; child_output=down2_overlap_tile_runner.pp_silu_accept; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=pp_silu_accept; child_output=down2_overlap_tile_runner.pp_silu_accept; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-795"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=pp_silu_busy; child_output=down2_overlap_tile_runner.pp_silu_busy; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=pp_silu_busy; child_output=down2_overlap_tile_runner.pp_silu_busy; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=pp_silu_busy; child_output=down2_overlap_tile_runner.pp_silu_busy; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-796"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=pp_table_fault; child_output=down2_overlap_tile_runner.pp_table_fault; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=pp_table_fault; child_output=down2_overlap_tile_runner.pp_table_fault; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=pp_table_fault; child_output=down2_overlap_tile_runner.pp_table_fault; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-797"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=pp_table_loaded; child_output=down2_overlap_tile_runner.pp_table_loaded; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=pp_table_loaded; child_output=down2_overlap_tile_runner.pp_table_loaded; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=pp_table_loaded; child_output=down2_overlap_tile_runner.pp_table_loaded; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-798"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=pp_table_ready; child_output=down2_overlap_tile_runner.pp_table_ready; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=pp_table_ready; child_output=down2_overlap_tile_runner.pp_table_ready; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=pp_table_ready; child_output=down2_overlap_tile_runner.pp_table_ready; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-799"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_debug_channel_o$D; child_output=down2_overlap_tile_runner.reg_debug_channel_o$D; operation_count=25; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_debug_channel_o$D; child_output=down2_overlap_tile_runner.reg_debug_channel_o$D; operation_count=25; limit=3; inconclusive_reason=missing module implementation; loop_presence=present`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_debug_channel_o$D; child_output=down2_overlap_tile_runner.reg_debug_channel_o$D; operation_count=25; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-800"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_debug_channel_o$enable; child_output=down2_overlap_tile_runner.reg_debug_channel_o$enable; operation_count=11; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_debug_channel_o$enable; child_output=down2_overlap_tile_runner.reg_debug_channel_o$enable; operation_count=11; limit=3; inconclusive_reason=missing module implementation; loop_presence=present`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_debug_channel_o$enable; child_output=down2_overlap_tile_runner.reg_debug_channel_o$enable; operation_count=11; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-801"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_debug_phase_o$enable; child_output=down2_overlap_tile_runner.reg_debug_phase_o$enable; operation_count=11; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_debug_phase_o$enable; child_output=down2_overlap_tile_runner.reg_debug_phase_o$enable; operation_count=11; limit=3; inconclusive_reason=missing module implementation; loop_presence=present`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_debug_phase_o$enable; child_output=down2_overlap_tile_runner.reg_debug_phase_o$enable; operation_count=11; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-802"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_debug_position_o$D; child_output=down2_overlap_tile_runner.reg_debug_position_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_debug_position_o$D; child_output=down2_overlap_tile_runner.reg_debug_position_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_debug_position_o$D; child_output=down2_overlap_tile_runner.reg_debug_position_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-803"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_debug_position_o$enable; child_output=down2_overlap_tile_runner.reg_debug_position_o$enable; operation_count=11; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_debug_position_o$enable; child_output=down2_overlap_tile_runner.reg_debug_position_o$enable; operation_count=11; limit=3; inconclusive_reason=missing module implementation; loop_presence=present`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_debug_position_o$enable; child_output=down2_overlap_tile_runner.reg_debug_position_o$enable; operation_count=11; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-804"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_debug_value_o$D; child_output=down2_overlap_tile_runner.reg_debug_value_o$D; operation_count=0; limit=3; inconclusive_reason=$signed: missing function definition | missing module implementation | reg_debug_value_o$D: missing storage data expression; loop_presence=unknown
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_debug_value_o$D; child_output=down2_overlap_tile_runner.reg_debug_value_o$D; operation_count=0; limit=3; inconclusive_reason=$signed: missing function definition | missing module implementation | reg_debug_value_o$D: missing storage data expression; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_debug_value_o$D; child_output=down2_overlap_tile_runner.reg_debug_value_o$D; operation_count=0; limit=3; inconclusive_reason=$signed: missing function definition | missing module implementation | reg_debug_value_o$D: missing storage data expression; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-805"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_debug_value_o$enable; child_output=down2_overlap_tile_runner.reg_debug_value_o$enable; operation_count=11; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_debug_value_o$enable; child_output=down2_overlap_tile_runner.reg_debug_value_o$enable; operation_count=11; limit=3; inconclusive_reason=missing module implementation; loop_presence=present`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_debug_value_o$enable; child_output=down2_overlap_tile_runner.reg_debug_value_o$enable; operation_count=11; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-806"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_dw_bias[i_load_addr]$enable; child_output=down2_overlap_tile_runner.reg_dw_bias[i_load_addr]$enable; operation_count=13; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_dw_bias[i_load_addr]$enable; child_output=down2_overlap_tile_runner.reg_dw_bias[i_load_addr]$enable; operation_count=13; limit=3; inconclusive_reason=missing module implementation; loop_presence=present`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_dw_bias[i_load_addr]$enable; child_output=down2_overlap_tile_runner.reg_dw_bias[i_load_addr]$enable; operation_count=13; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-807"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_dw_cache[i_load_addr]$enable; child_output=down2_overlap_tile_runner.reg_dw_cache[i_load_addr]$enable; operation_count=13; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_dw_cache[i_load_addr]$enable; child_output=down2_overlap_tile_runner.reg_dw_cache[i_load_addr]$enable; operation_count=13; limit=3; inconclusive_reason=missing module implementation; loop_presence=present`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_dw_cache[i_load_addr]$enable; child_output=down2_overlap_tile_runner.reg_dw_cache[i_load_addr]$enable; operation_count=13; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-808"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_dw_weight[i_load_addr]$enable; child_output=down2_overlap_tile_runner.reg_dw_weight[i_load_addr]$enable; operation_count=13; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_dw_weight[i_load_addr]$enable; child_output=down2_overlap_tile_runner.reg_dw_weight[i_load_addr]$enable; operation_count=13; limit=3; inconclusive_reason=missing module implementation; loop_presence=present`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_dw_weight[i_load_addr]$enable; child_output=down2_overlap_tile_runner.reg_dw_weight[i_load_addr]$enable; operation_count=13; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-809"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_halo[i_load_addr]$enable; child_output=down2_overlap_tile_runner.reg_halo[i_load_addr]$enable; operation_count=13; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_halo[i_load_addr]$enable; child_output=down2_overlap_tile_runner.reg_halo[i_load_addr]$enable; operation_count=13; limit=3; inconclusive_reason=missing module implementation; loop_presence=present`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_halo[i_load_addr]$enable; child_output=down2_overlap_tile_runner.reg_halo[i_load_addr]$enable; operation_count=13; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-810"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_mac_activation$D; child_output=down2_overlap_tile_runner.reg_mac_activation$D; operation_count=32; limit=3; inconclusive_reason=missing module implementation | next_mac_activation: dynamic lvalue selection is not a static endpoint; loop_presence=present
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_mac_activation$D; child_output=down2_overlap_tile_runner.reg_mac_activation$D; operation_count=32; limit=3; inconclusive_reason=missing module implementation | next_mac_activation: dynamic lvalue selection is not a static endpoint; loop_presence=present`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_mac_activation$D; child_output=down2_overlap_tile_runner.reg_mac_activation$D; operation_count=32; limit=3; inconclusive_reason=missing module implementation | next_mac_activation: dynamic lvalue selection is not a static endpoint; loop_presence=present
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-811"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_mac_activation$enable; child_output=down2_overlap_tile_runner.reg_mac_activation$enable; operation_count=1; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_mac_activation$enable; child_output=down2_overlap_tile_runner.reg_mac_activation$enable; operation_count=1; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_mac_activation$enable; child_output=down2_overlap_tile_runner.reg_mac_activation$enable; operation_count=1; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-812"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_mac_bias$D; child_output=down2_overlap_tile_runner.reg_mac_bias$D; operation_count=26; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_mac_bias$D; child_output=down2_overlap_tile_runner.reg_mac_bias$D; operation_count=26; limit=3; inconclusive_reason=missing module implementation; loop_presence=present`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_mac_bias$D; child_output=down2_overlap_tile_runner.reg_mac_bias$D; operation_count=26; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-813"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_mac_bias$enable; child_output=down2_overlap_tile_runner.reg_mac_bias$enable; operation_count=1; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_mac_bias$enable; child_output=down2_overlap_tile_runner.reg_mac_bias$enable; operation_count=1; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_mac_bias$enable; child_output=down2_overlap_tile_runner.reg_mac_bias$enable; operation_count=1; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-814"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_mac_mask$D; child_output=down2_overlap_tile_runner.reg_mac_mask$D; operation_count=32; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_mac_mask$D; child_output=down2_overlap_tile_runner.reg_mac_mask$D; operation_count=32; limit=3; inconclusive_reason=missing module implementation; loop_presence=present`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_mac_mask$D; child_output=down2_overlap_tile_runner.reg_mac_mask$D; operation_count=32; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-815"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_mac_mask$enable; child_output=down2_overlap_tile_runner.reg_mac_mask$enable; operation_count=1; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_mac_mask$enable; child_output=down2_overlap_tile_runner.reg_mac_mask$enable; operation_count=1; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_mac_mask$enable; child_output=down2_overlap_tile_runner.reg_mac_mask$enable; operation_count=1; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-816"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_mac_weight$D; child_output=down2_overlap_tile_runner.reg_mac_weight$D; operation_count=54; limit=3; inconclusive_reason=missing module implementation | next_mac_weight: dynamic lvalue selection is not a static endpoint; loop_presence=present
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_mac_weight$D; child_output=down2_overlap_tile_runner.reg_mac_weight$D; operation_count=54; limit=3; inconclusive_reason=missing module implementation | next_mac_weight: dynamic lvalue selection is not a static endpoint; loop_presence=present`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_mac_weight$D; child_output=down2_overlap_tile_runner.reg_mac_weight$D; operation_count=54; limit=3; inconclusive_reason=missing module implementation | next_mac_weight: dynamic lvalue selection is not a static endpoint; loop_presence=present
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-817"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_mac_weight$enable; child_output=down2_overlap_tile_runner.reg_mac_weight$enable; operation_count=1; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_mac_weight$enable; child_output=down2_overlap_tile_runner.reg_mac_weight$enable; operation_count=1; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_mac_weight$enable; child_output=down2_overlap_tile_runner.reg_mac_weight$enable; operation_count=1; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-818"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_pw_bias[i_load_addr]$enable; child_output=down2_overlap_tile_runner.reg_pw_bias[i_load_addr]$enable; operation_count=13; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_pw_bias[i_load_addr]$enable; child_output=down2_overlap_tile_runner.reg_pw_bias[i_load_addr]$enable; operation_count=13; limit=3; inconclusive_reason=missing module implementation; loop_presence=present`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_pw_bias[i_load_addr]$enable; child_output=down2_overlap_tile_runner.reg_pw_bias[i_load_addr]$enable; operation_count=13; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-819"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_pw_weight[i_load_addr]$enable; child_output=down2_overlap_tile_runner.reg_pw_weight[i_load_addr]$enable; operation_count=13; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_pw_weight[i_load_addr]$enable; child_output=down2_overlap_tile_runner.reg_pw_weight[i_load_addr]$enable; operation_count=13; limit=3; inconclusive_reason=missing module implementation; loop_presence=present`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_pw_weight[i_load_addr]$enable; child_output=down2_overlap_tile_runner.reg_pw_weight[i_load_addr]$enable; operation_count=13; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-820"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=state_current$D; child_output=down2_overlap_tile_runner.state_current$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=state_current$D; child_output=down2_overlap_tile_runner.state_current$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=state_current$D; child_output=down2_overlap_tile_runner.state_current$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-821"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=state_current$enable; child_output=down2_overlap_tile_runner.state_current$enable; operation_count=46; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=state_current$enable; child_output=down2_overlap_tile_runner.state_current$enable; operation_count=46; limit=3; inconclusive_reason=missing module implementation; loop_presence=present`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=state_current$enable; child_output=down2_overlap_tile_runner.state_current$enable; operation_count=46; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-822"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:182`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=wire_dw_lane; child_output=down2_overlap_tile_runner.wire_dw_lane; operation_count=22; limit=3; inconclusive_reason=none; loop_presence=present
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=wire_dw_lane; child_output=down2_overlap_tile_runner.wire_dw_lane; operation_count=22; limit=3; inconclusive_reason=none; loop_presence=present`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=wire_dw_lane; child_output=down2_overlap_tile_runner.wire_dw_lane; operation_count=22; limit=3; inconclusive_reason=none; loop_presence=present
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-823"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:188`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=wire_dw_channel_base; child_output=down2_overlap_tile_runner.wire_dw_channel_base; operation_count=23; limit=3; inconclusive_reason=none; loop_presence=present
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=wire_dw_channel_base; child_output=down2_overlap_tile_runner.wire_dw_channel_base; operation_count=23; limit=3; inconclusive_reason=none; loop_presence=present`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=wire_dw_channel_base; child_output=down2_overlap_tile_runner.wire_dw_channel_base; operation_count=23; limit=3; inconclusive_reason=none; loop_presence=present
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-824"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:189`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=wire_result_lane_mask; child_output=down2_overlap_tile_runner.wire_result_lane_mask; operation_count=24; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=wire_result_lane_mask; child_output=down2_overlap_tile_runner.wire_result_lane_mask; operation_count=24; limit=3; inconclusive_reason=missing module implementation; loop_presence=present`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=wire_result_lane_mask; child_output=down2_overlap_tile_runner.wire_result_lane_mask; operation_count=24; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-825"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:190`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=wire_result_channel_base; child_output=down2_overlap_tile_runner.wire_result_channel_base; operation_count=25; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=wire_result_channel_base; child_output=down2_overlap_tile_runner.wire_result_channel_base; operation_count=25; limit=3; inconclusive_reason=missing module implementation; loop_presence=present`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=wire_result_channel_base; child_output=down2_overlap_tile_runner.wire_result_channel_base; operation_count=25; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-826"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:191`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=wire_capacity_used; child_output=down2_overlap_tile_runner.wire_capacity_used; operation_count=1; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=wire_capacity_used; child_output=down2_overlap_tile_runner.wire_capacity_used; operation_count=1; limit=3; inconclusive_reason=missing module implementation; loop_presence=present`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=wire_capacity_used; child_output=down2_overlap_tile_runner.wire_capacity_used; operation_count=1; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-827"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:192`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=flag_can_reserve; child_output=down2_overlap_tile_runner.flag_can_reserve; operation_count=6; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=flag_can_reserve; child_output=down2_overlap_tile_runner.flag_can_reserve; operation_count=6; limit=3; inconclusive_reason=missing module implementation; loop_presence=present`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=flag_can_reserve; child_output=down2_overlap_tile_runner.flag_can_reserve; operation_count=6; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-828"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:193`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=flag_mac_input_valid; child_output=down2_overlap_tile_runner.flag_mac_input_valid; operation_count=9; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=flag_mac_input_valid; child_output=down2_overlap_tile_runner.flag_mac_input_valid; operation_count=9; limit=3; inconclusive_reason=missing module implementation; loop_presence=present`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=flag_mac_input_valid; child_output=down2_overlap_tile_runner.flag_mac_input_valid; operation_count=9; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-829"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:194`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=flag_mac_input_accept; child_output=down2_overlap_tile_runner.flag_mac_input_accept; operation_count=10; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=flag_mac_input_accept; child_output=down2_overlap_tile_runner.flag_mac_input_accept; operation_count=10; limit=3; inconclusive_reason=missing module implementation; loop_presence=present`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=flag_mac_input_accept; child_output=down2_overlap_tile_runner.flag_mac_input_accept; operation_count=10; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-830"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:195`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=flag_mac_result_ready_local; child_output=down2_overlap_tile_runner.flag_mac_result_ready_local; operation_count=7; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=flag_mac_result_ready_local; child_output=down2_overlap_tile_runner.flag_mac_result_ready_local; operation_count=7; limit=3; inconclusive_reason=missing module implementation; loop_presence=present`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=flag_mac_result_ready_local; child_output=down2_overlap_tile_runner.flag_mac_result_ready_local; operation_count=7; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-831"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:197`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=flag_mac_result_accept; child_output=down2_overlap_tile_runner.flag_mac_result_accept; operation_count=8; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=flag_mac_result_accept; child_output=down2_overlap_tile_runner.flag_mac_result_accept; operation_count=8; limit=3; inconclusive_reason=missing module implementation; loop_presence=present`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=flag_mac_result_accept; child_output=down2_overlap_tile_runner.flag_mac_result_accept; operation_count=8; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-832"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:198`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=flag_commit_accept; child_output=down2_overlap_tile_runner.flag_commit_accept; operation_count=2; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=flag_commit_accept; child_output=down2_overlap_tile_runner.flag_commit_accept; operation_count=2; limit=3; inconclusive_reason=missing module implementation; loop_presence=present`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=flag_commit_accept; child_output=down2_overlap_tile_runner.flag_commit_accept; operation_count=2; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-833"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:199`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=flag_table_enable; child_output=down2_overlap_tile_runner.flag_table_enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=flag_table_enable; child_output=down2_overlap_tile_runner.flag_table_enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=present`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=flag_table_enable; child_output=down2_overlap_tile_runner.flag_table_enable; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-834"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:200`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=flag_load_accept; child_output=down2_overlap_tile_runner.flag_load_accept; operation_count=10; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=flag_load_accept; child_output=down2_overlap_tile_runner.flag_load_accept; operation_count=10; limit=3; inconclusive_reason=missing module implementation; loop_presence=present`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=flag_load_accept; child_output=down2_overlap_tile_runner.flag_load_accept; operation_count=10; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-835"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:201`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=flag_output_accept; child_output=down2_overlap_tile_runner.flag_output_accept; operation_count=2; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=flag_output_accept; child_output=down2_overlap_tile_runner.flag_output_accept; operation_count=2; limit=3; inconclusive_reason=missing module implementation; loop_presence=present`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=flag_output_accept; child_output=down2_overlap_tile_runner.flag_output_accept; operation_count=2; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-836"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:202`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=flag_start_accept; child_output=down2_overlap_tile_runner.flag_start_accept; operation_count=15; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=flag_start_accept; child_output=down2_overlap_tile_runner.flag_start_accept; operation_count=15; limit=3; inconclusive_reason=missing module implementation; loop_presence=present`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=flag_start_accept; child_output=down2_overlap_tile_runner.flag_start_accept; operation_count=15; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-837"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:208`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=o_table_ready; child_output=down2_overlap_tile_runner.o_table_ready; operation_count=6; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=o_table_ready; child_output=down2_overlap_tile_runner.o_table_ready; operation_count=6; limit=3; inconclusive_reason=missing module implementation; loop_presence=present`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=o_table_ready; child_output=down2_overlap_tile_runner.o_table_ready; operation_count=6; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-838"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:209`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=o_table_loaded; child_output=down2_overlap_tile_runner.o_table_loaded; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=o_table_loaded; child_output=down2_overlap_tile_runner.o_table_loaded; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=present`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=o_table_loaded; child_output=down2_overlap_tile_runner.o_table_loaded; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-839"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:210`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=o_table_fault; child_output=down2_overlap_tile_runner.o_table_fault; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=o_table_fault; child_output=down2_overlap_tile_runner.o_table_fault; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=present`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=o_table_fault; child_output=down2_overlap_tile_runner.o_table_fault; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-840"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:211`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=o_load_ready; child_output=down2_overlap_tile_runner.o_load_ready; operation_count=9; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=o_load_ready; child_output=down2_overlap_tile_runner.o_load_ready; operation_count=9; limit=3; inconclusive_reason=missing module implementation; loop_presence=present`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=o_load_ready; child_output=down2_overlap_tile_runner.o_load_ready; operation_count=9; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-841"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:213`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=o_busy; child_output=down2_overlap_tile_runner.o_busy; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=o_busy; child_output=down2_overlap_tile_runner.o_busy; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=present`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=o_busy; child_output=down2_overlap_tile_runner.o_busy; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-842"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:215`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=o_fault; child_output=down2_overlap_tile_runner.o_fault; operation_count=2; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=o_fault; child_output=down2_overlap_tile_runner.o_fault; operation_count=2; limit=3; inconclusive_reason=missing module implementation; loop_presence=present`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=o_fault; child_output=down2_overlap_tile_runner.o_fault; operation_count=2; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-843"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:216`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=o_output_valid; child_output=down2_overlap_tile_runner.o_output_valid; operation_count=1; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=o_output_valid; child_output=down2_overlap_tile_runner.o_output_valid; operation_count=1; limit=3; inconclusive_reason=missing module implementation; loop_presence=present`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=o_output_valid; child_output=down2_overlap_tile_runner.o_output_valid; operation_count=1; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-844"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:236`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=o_result_queue_count; child_output=down2_overlap_tile_runner.o_result_queue_count; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=o_result_queue_count; child_output=down2_overlap_tile_runner.o_result_queue_count; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=present`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=o_result_queue_count; child_output=down2_overlap_tile_runner.o_result_queue_count; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-845"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:237`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=o_result_reserved; child_output=down2_overlap_tile_runner.o_result_reserved; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=o_result_reserved; child_output=down2_overlap_tile_runner.o_result_reserved; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=present`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=o_result_reserved; child_output=down2_overlap_tile_runner.o_result_reserved; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-846"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:238`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=o_meta_count; child_output=down2_overlap_tile_runner.o_meta_count; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=o_meta_count; child_output=down2_overlap_tile_runner.o_meta_count; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=present`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=o_meta_count; child_output=down2_overlap_tile_runner.o_meta_count; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-847"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:245`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=next_mac_activation; child_output=down2_overlap_tile_runner.next_mac_activation; operation_count=32; limit=3; inconclusive_reason=missing module implementation | next_mac_activation: dynamic lvalue selection is not a static endpoint; loop_presence=present
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=next_mac_activation; child_output=down2_overlap_tile_runner.next_mac_activation; operation_count=32; limit=3; inconclusive_reason=missing module implementation | next_mac_activation: dynamic lvalue selection is not a static endpoint; loop_presence=present`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=next_mac_activation; child_output=down2_overlap_tile_runner.next_mac_activation; operation_count=32; limit=3; inconclusive_reason=missing module implementation | next_mac_activation: dynamic lvalue selection is not a static endpoint; loop_presence=present
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-848"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:246`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=next_mac_weight; child_output=down2_overlap_tile_runner.next_mac_weight; operation_count=54; limit=3; inconclusive_reason=missing module implementation | next_mac_weight: dynamic lvalue selection is not a static endpoint; loop_presence=present
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=next_mac_weight; child_output=down2_overlap_tile_runner.next_mac_weight; operation_count=54; limit=3; inconclusive_reason=missing module implementation | next_mac_weight: dynamic lvalue selection is not a static endpoint; loop_presence=present`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=next_mac_weight; child_output=down2_overlap_tile_runner.next_mac_weight; operation_count=54; limit=3; inconclusive_reason=missing module implementation | next_mac_weight: dynamic lvalue selection is not a static endpoint; loop_presence=present
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-849"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:247`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=next_mac_bias; child_output=down2_overlap_tile_runner.next_mac_bias; operation_count=26; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=next_mac_bias; child_output=down2_overlap_tile_runner.next_mac_bias; operation_count=26; limit=3; inconclusive_reason=missing module implementation; loop_presence=present`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=next_mac_bias; child_output=down2_overlap_tile_runner.next_mac_bias; operation_count=26; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-850"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:248`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=next_mac_mask; child_output=down2_overlap_tile_runner.next_mac_mask; operation_count=32; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=next_mac_mask; child_output=down2_overlap_tile_runner.next_mac_mask; operation_count=32; limit=3; inconclusive_reason=missing module implementation; loop_presence=present`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=next_mac_mask; child_output=down2_overlap_tile_runner.next_mac_mask; operation_count=32; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-851"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:249`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=kernel_index; child_output=down2_overlap_tile_runner.kernel_index; operation_count=24; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=kernel_index; child_output=down2_overlap_tile_runner.kernel_index; operation_count=24; limit=3; inconclusive_reason=missing module implementation; loop_presence=present`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=kernel_index; child_output=down2_overlap_tile_runner.kernel_index; operation_count=24; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-852"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:250`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=halo_index; child_output=down2_overlap_tile_runner.halo_index; operation_count=128; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=halo_index; child_output=down2_overlap_tile_runner.halo_index; operation_count=128; limit=3; inconclusive_reason=missing module implementation; loop_presence=present`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=halo_index; child_output=down2_overlap_tile_runner.halo_index; operation_count=128; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-853"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:251`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=weight_index; child_output=down2_overlap_tile_runner.weight_index; operation_count=48; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=weight_index; child_output=down2_overlap_tile_runner.weight_index; operation_count=48; limit=3; inconclusive_reason=missing module implementation; loop_presence=present`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=weight_index; child_output=down2_overlap_tile_runner.weight_index; operation_count=48; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-854"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:252`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=output_channel; child_output=down2_overlap_tile_runner.output_channel; operation_count=16; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=output_channel; child_output=down2_overlap_tile_runner.output_channel; operation_count=16; limit=3; inconclusive_reason=missing module implementation; loop_presence=present`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=output_channel; child_output=down2_overlap_tile_runner.output_channel; operation_count=16; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-855"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:253`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=next_mac_activation[lane_index*8+:8]; child_output=down2_overlap_tile_runner.next_mac_activation[lane_index*8+:8]; operation_count=32; limit=3; inconclusive_reason=missing module implementation | next_mac_activation[lane_index*8+:8]: dynamic lvalue selection is not a static endpoint; loop_presence=present
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=next_mac_activation[lane_index*8+:8]; child_output=down2_overlap_tile_runner.next_mac_activation[lane_index*8+:8]; operation_count=32; limit=3; inconclusive_reason=missing module implementation | next_mac_activation[lane_index*8+:8]: dynamic lvalue selection is not a static endpoint; loop_presence=present`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=next_mac_activation[lane_index*8+:8]; child_output=down2_overlap_tile_runner.next_mac_activation[lane_index*8+:8]; operation_count=32; limit=3; inconclusive_reason=missing module implementation | next_mac_activation[lane_index*8+:8]: dynamic lvalue selection is not a static endpoint; loop_presence=present
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-856"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:254`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=next_mac_bias[31:0]; child_output=down2_overlap_tile_runner.next_mac_bias[31:0]; operation_count=24; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=next_mac_bias[31:0]; child_output=down2_overlap_tile_runner.next_mac_bias[31:0]; operation_count=24; limit=3; inconclusive_reason=missing module implementation; loop_presence=present`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=next_mac_bias[31:0]; child_output=down2_overlap_tile_runner.next_mac_bias[31:0]; operation_count=24; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-857"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:254`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=next_mac_bias[63:32]; child_output=down2_overlap_tile_runner.next_mac_bias[63:32]; operation_count=25; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=next_mac_bias[63:32]; child_output=down2_overlap_tile_runner.next_mac_bias[63:32]; operation_count=25; limit=3; inconclusive_reason=missing module implementation; loop_presence=present`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=next_mac_bias[63:32]; child_output=down2_overlap_tile_runner.next_mac_bias[63:32]; operation_count=25; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-858"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:254`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=next_mac_bias[95:64]; child_output=down2_overlap_tile_runner.next_mac_bias[95:64]; operation_count=25; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=next_mac_bias[95:64]; child_output=down2_overlap_tile_runner.next_mac_bias[95:64]; operation_count=25; limit=3; inconclusive_reason=missing module implementation; loop_presence=present`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=next_mac_bias[95:64]; child_output=down2_overlap_tile_runner.next_mac_bias[95:64]; operation_count=25; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-859"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:254`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=next_mac_mask[0]; child_output=down2_overlap_tile_runner.next_mac_mask[0]; operation_count=25; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=next_mac_mask[0]; child_output=down2_overlap_tile_runner.next_mac_mask[0]; operation_count=25; limit=3; inconclusive_reason=missing module implementation; loop_presence=present`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=next_mac_mask[0]; child_output=down2_overlap_tile_runner.next_mac_mask[0]; operation_count=25; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-860"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:254`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=next_mac_mask[1]; child_output=down2_overlap_tile_runner.next_mac_mask[1]; operation_count=25; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=next_mac_mask[1]; child_output=down2_overlap_tile_runner.next_mac_mask[1]; operation_count=25; limit=3; inconclusive_reason=missing module implementation; loop_presence=present`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=next_mac_mask[1]; child_output=down2_overlap_tile_runner.next_mac_mask[1]; operation_count=25; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-861"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:254`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=next_mac_mask[2]; child_output=down2_overlap_tile_runner.next_mac_mask[2]; operation_count=25; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=next_mac_mask[2]; child_output=down2_overlap_tile_runner.next_mac_mask[2]; operation_count=25; limit=3; inconclusive_reason=missing module implementation; loop_presence=present`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=next_mac_mask[2]; child_output=down2_overlap_tile_runner.next_mac_mask[2]; operation_count=25; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-862"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:254`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=next_mac_mask[3]; child_output=down2_overlap_tile_runner.next_mac_mask[3]; operation_count=25; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=next_mac_mask[3]; child_output=down2_overlap_tile_runner.next_mac_mask[3]; operation_count=25; limit=3; inconclusive_reason=missing module implementation; loop_presence=present`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=next_mac_mask[3]; child_output=down2_overlap_tile_runner.next_mac_mask[3]; operation_count=25; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-863"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:254`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=next_mac_mask[4]; child_output=down2_overlap_tile_runner.next_mac_mask[4]; operation_count=25; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=next_mac_mask[4]; child_output=down2_overlap_tile_runner.next_mac_mask[4]; operation_count=25; limit=3; inconclusive_reason=missing module implementation; loop_presence=present`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=next_mac_mask[4]; child_output=down2_overlap_tile_runner.next_mac_mask[4]; operation_count=25; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-864"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:254`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=next_mac_mask[5]; child_output=down2_overlap_tile_runner.next_mac_mask[5]; operation_count=25; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=next_mac_mask[5]; child_output=down2_overlap_tile_runner.next_mac_mask[5]; operation_count=25; limit=3; inconclusive_reason=missing module implementation; loop_presence=present`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=next_mac_mask[5]; child_output=down2_overlap_tile_runner.next_mac_mask[5]; operation_count=25; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-865"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:254`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=next_mac_mask[6]; child_output=down2_overlap_tile_runner.next_mac_mask[6]; operation_count=25; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=next_mac_mask[6]; child_output=down2_overlap_tile_runner.next_mac_mask[6]; operation_count=25; limit=3; inconclusive_reason=missing module implementation; loop_presence=present`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=next_mac_mask[6]; child_output=down2_overlap_tile_runner.next_mac_mask[6]; operation_count=25; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-866"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:254`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=next_mac_mask[7]; child_output=down2_overlap_tile_runner.next_mac_mask[7]; operation_count=25; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=next_mac_mask[7]; child_output=down2_overlap_tile_runner.next_mac_mask[7]; operation_count=25; limit=3; inconclusive_reason=missing module implementation; loop_presence=present`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=next_mac_mask[7]; child_output=down2_overlap_tile_runner.next_mac_mask[7]; operation_count=25; limit=3; inconclusive_reason=missing module implementation; loop_presence=present
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-867"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:256`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=next_mac_weight[lane_index*8+:8]; child_output=down2_overlap_tile_runner.next_mac_weight[lane_index*8+:8]; operation_count=54; limit=3; inconclusive_reason=missing module implementation | next_mac_weight[lane_index*8+:8]: dynamic lvalue selection is not a static endpoint; loop_presence=present
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=next_mac_weight[lane_index*8+:8]; child_output=down2_overlap_tile_runner.next_mac_weight[lane_index*8+:8]; operation_count=54; limit=3; inconclusive_reason=missing module implementation | next_mac_weight[lane_index*8+:8]: dynamic lvalue selection is not a static endpoint; loop_presence=present`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=next_mac_weight[lane_index*8+:8]; child_output=down2_overlap_tile_runner.next_mac_weight[lane_index*8+:8]; operation_count=54; limit=3; inconclusive_reason=missing module implementation | next_mac_weight[lane_index*8+:8]: dynamic lvalue selection is not a static endpoint; loop_presence=present
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-868"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:257`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=next_mac_weight[64+lane_index*8+:8]; child_output=down2_overlap_tile_runner.next_mac_weight[64+lane_index*8+:8]; operation_count=54; limit=3; inconclusive_reason=missing module implementation | next_mac_weight[64+lane_index*8+:8]: dynamic lvalue selection is not a static endpoint; loop_presence=present
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=next_mac_weight[64+lane_index*8+:8]; child_output=down2_overlap_tile_runner.next_mac_weight[64+lane_index*8+:8]; operation_count=54; limit=3; inconclusive_reason=missing module implementation | next_mac_weight[64+lane_index*8+:8]: dynamic lvalue selection is not a static endpoint; loop_presence=present`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=next_mac_weight[64+lane_index*8+:8]; child_output=down2_overlap_tile_runner.next_mac_weight[64+lane_index*8+:8]; operation_count=54; limit=3; inconclusive_reason=missing module implementation | next_mac_weight[64+lane_index*8+:8]: dynamic lvalue selection is not a static endpoint; loop_presence=present
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-869"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:258`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=next_mac_weight[128+lane_index*8+:8]; child_output=down2_overlap_tile_runner.next_mac_weight[128+lane_index*8+:8]; operation_count=54; limit=3; inconclusive_reason=missing module implementation | next_mac_weight[128+lane_index*8+:8]: dynamic lvalue selection is not a static endpoint; loop_presence=present
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=next_mac_weight[128+lane_index*8+:8]; child_output=down2_overlap_tile_runner.next_mac_weight[128+lane_index*8+:8]; operation_count=54; limit=3; inconclusive_reason=missing module implementation | next_mac_weight[128+lane_index*8+:8]: dynamic lvalue selection is not a static endpoint; loop_presence=present`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=next_mac_weight[128+lane_index*8+:8]; child_output=down2_overlap_tile_runner.next_mac_weight[128+lane_index*8+:8]; operation_count=54; limit=3; inconclusive_reason=missing module implementation | next_mac_weight[128+lane_index*8+:8]: dynamic lvalue selection is not a static endpoint; loop_presence=present
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-870"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:290`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=state_current; child_output=down2_overlap_tile_runner.state_current; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=state_current; child_output=down2_overlap_tile_runner.state_current; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=state_current; child_output=down2_overlap_tile_runner.state_current; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-871"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:291`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=flag_layer_pw; child_output=down2_overlap_tile_runner.flag_layer_pw; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=flag_layer_pw; child_output=down2_overlap_tile_runner.flag_layer_pw; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=flag_layer_pw; child_output=down2_overlap_tile_runner.flag_layer_pw; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-872"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:292`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=flag_busy_o; child_output=down2_overlap_tile_runner.flag_busy_o; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=flag_busy_o; child_output=down2_overlap_tile_runner.flag_busy_o; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=flag_busy_o; child_output=down2_overlap_tile_runner.flag_busy_o; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-873"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:294`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=flag_result_reserved; child_output=down2_overlap_tile_runner.flag_result_reserved; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=flag_result_reserved; child_output=down2_overlap_tile_runner.flag_result_reserved; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=flag_result_reserved; child_output=down2_overlap_tile_runner.flag_result_reserved; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-874"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:294`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_mac_activation; child_output=down2_overlap_tile_runner.reg_mac_activation; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_mac_activation; child_output=down2_overlap_tile_runner.reg_mac_activation; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_mac_activation; child_output=down2_overlap_tile_runner.reg_mac_activation; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-875"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:295`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=cnt_mac_group; child_output=down2_overlap_tile_runner.cnt_mac_group; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=cnt_mac_group; child_output=down2_overlap_tile_runner.cnt_mac_group; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=cnt_mac_group; child_output=down2_overlap_tile_runner.cnt_mac_group; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-876"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:295`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=cnt_position; child_output=down2_overlap_tile_runner.cnt_position; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=cnt_position; child_output=down2_overlap_tile_runner.cnt_position; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=cnt_position; child_output=down2_overlap_tile_runner.cnt_position; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-877"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:295`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_mac_weight; child_output=down2_overlap_tile_runner.reg_mac_weight; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_mac_weight; child_output=down2_overlap_tile_runner.reg_mac_weight; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_mac_weight; child_output=down2_overlap_tile_runner.reg_mac_weight; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-878"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:296`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_mac_bias; child_output=down2_overlap_tile_runner.reg_mac_bias; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_mac_bias; child_output=down2_overlap_tile_runner.reg_mac_bias; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_mac_bias; child_output=down2_overlap_tile_runner.reg_mac_bias; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-879"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:297`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_mac_mask; child_output=down2_overlap_tile_runner.reg_mac_mask; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_mac_mask; child_output=down2_overlap_tile_runner.reg_mac_mask; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=down2_overlap_tile_runner.v:down2_overlap_tile_runner@4:1-663:1; instance_path=down2_overlap_tile_runner; specialization=0418b871a4899e1e58a9ccfbb9ca5ac5a4a7c37c1bf89452bcc1d5142ba0d495; target=reg_mac_mask; child_output=down2_overlap_tile_runner.reg_mac_mask; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-880"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:67`
- Evidence:
- node_kind: `verilog_rtl`
- detail: reg_halo
- source_excerpt: `reg_halo`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
reg_halo
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-881"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:68`
- Evidence:
- node_kind: `verilog_rtl`
- detail: reg_dw_cache
- source_excerpt: `reg_dw_cache`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
reg_dw_cache
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-882"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:69`
- Evidence:
- node_kind: `verilog_rtl`
- detail: reg_output_cache
- source_excerpt: `reg_output_cache`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
reg_output_cache
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-883"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:70`
- Evidence:
- node_kind: `verilog_rtl`
- detail: reg_dw_weight
- source_excerpt: `reg_dw_weight`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
reg_dw_weight
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-884"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:71`
- Evidence:
- node_kind: `verilog_rtl`
- detail: reg_dw_bias
- source_excerpt: `reg_dw_bias`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
reg_dw_bias
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-885"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:72`
- Evidence:
- node_kind: `verilog_rtl`
- detail: reg_pw_weight
- source_excerpt: `reg_pw_weight`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
reg_pw_weight
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-886"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:73`
- Evidence:
- node_kind: `verilog_rtl`
- detail: reg_pw_bias
- source_excerpt: `reg_pw_bias`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
reg_pw_bias
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-887"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:136`
- Evidence:
- node_kind: `verilog_rtl`
- detail: mac_input_ready
- source_excerpt: `mac_input_ready`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
mac_input_ready
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-888"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:137`
- Evidence:
- node_kind: `verilog_rtl`
- detail: mac_result_valid
- source_excerpt: `mac_result_valid`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
mac_result_valid
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-889"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:138`
- Evidence:
- node_kind: `verilog_rtl`
- detail: mac_result_data
- source_excerpt: `mac_result_data`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
mac_result_data
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-890"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:139`
- Evidence:
- node_kind: `verilog_rtl`
- detail: mac_fault
- source_excerpt: `mac_fault`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
mac_fault
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-891"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:147`
- Evidence:
- node_kind: `verilog_rtl`
- detail: pp_input_ready
- source_excerpt: `pp_input_ready`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
pp_input_ready
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-892"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:148`
- Evidence:
- node_kind: `verilog_rtl`
- detail: pp_output_valid
- source_excerpt: `pp_output_valid`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
pp_output_valid
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-893"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:149`
- Evidence:
- node_kind: `verilog_rtl`
- detail: pp_output_data
- source_excerpt: `pp_output_data`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
pp_output_data
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-894"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:150`
- Evidence:
- node_kind: `verilog_rtl`
- detail: pp_output_tag
- source_excerpt: `pp_output_tag`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
pp_output_tag
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-895"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:151`
- Evidence:
- node_kind: `verilog_rtl`
- detail: pp_fault
- source_excerpt: `pp_fault`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
pp_fault
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-896"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:152`
- Evidence:
- node_kind: `verilog_rtl`
- detail: pp_result_queue_count
- source_excerpt: `pp_result_queue_count`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
pp_result_queue_count
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-897"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:153`
- Evidence:
- node_kind: `verilog_rtl`
- detail: pp_meta_count
- source_excerpt: `pp_meta_count`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
pp_meta_count
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-898"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:154`
- Evidence:
- node_kind: `verilog_rtl`
- detail: pp_pre_busy
- source_excerpt: `pp_pre_busy`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
pp_pre_busy
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-899"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:155`
- Evidence:
- node_kind: `verilog_rtl`
- detail: pp_silu_busy
- source_excerpt: `pp_silu_busy`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
pp_silu_busy
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-900"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:156`
- Evidence:
- node_kind: `verilog_rtl`
- detail: pp_post_busy
- source_excerpt: `pp_post_busy`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
pp_post_busy
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-901"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:157`
- Evidence:
- node_kind: `verilog_rtl`
- detail: pp_pre_accept
- source_excerpt: `pp_pre_accept`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
pp_pre_accept
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-902"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:158`
- Evidence:
- node_kind: `verilog_rtl`
- detail: pp_silu_accept
- source_excerpt: `pp_silu_accept`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
pp_silu_accept
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-903"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:159`
- Evidence:
- node_kind: `verilog_rtl`
- detail: pp_post_accept
- source_excerpt: `pp_post_accept`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
pp_post_accept
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-904"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:160`
- Evidence:
- node_kind: `verilog_rtl`
- detail: pp_table_ready
- source_excerpt: `pp_table_ready`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
pp_table_ready
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-905"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:161`
- Evidence:
- node_kind: `verilog_rtl`
- detail: pp_table_loaded
- source_excerpt: `pp_table_loaded`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
pp_table_loaded
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-906"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:162`
- Evidence:
- node_kind: `verilog_rtl`
- detail: pp_table_fault
- source_excerpt: `pp_table_fault`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
pp_table_fault
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-907"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `down2_overlap_tile_runner.v:175`
- Evidence:
- node_kind: `verilog_rtl`
- detail: lane_index
- source_excerpt: `lane_index`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
lane_index
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

## Other deliverable findings

| Severity | Code | Path | Line | Message |
|---|---|---|---:|---|
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:6` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:7` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:8` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:9` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:10` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:11` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:12` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:13` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:14` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:15` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:16` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:17` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:18` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:19` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:20` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:21` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:22` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:23` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:24` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:25` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:26` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:27` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:28` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:29` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:30` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:31` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:32` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:33` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:34` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:35` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:36` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:37` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:38` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:39` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:40` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:41` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:42` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:43` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:44` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:45` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:46` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:47` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:48` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:49` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:50` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:51` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:52` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:53` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:54` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:57` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:58` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:59` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:60` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:61` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:62` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:63` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:64` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:65` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:67` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:68` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:69` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:70` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:71` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:72` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:73` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:75` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:76` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:77` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:78` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:79` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:80` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:81` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:82` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:83` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:84` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:85` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:86` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:87` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:88` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:89` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:91` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:92` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:93` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:94` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:95` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:96` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:97` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:98` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:100` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:101` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:102` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:103` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:104` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:105` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:107` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:108` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:109` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:110` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:111` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:112` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:113` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:114` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:115` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:116` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:117` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:118` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:119` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:120` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:121` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:123` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:124` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:125` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:126` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:127` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:128` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:129` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:130` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:131` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:132` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:133` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:134` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:136` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:137` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:138` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:139` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:140` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:141` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:142` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:143` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:144` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:145` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:147` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:148` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:149` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:150` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:151` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:152` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:153` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:154` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:155` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:156` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:157` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:158` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:159` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:160` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:161` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:162` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:163` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:165` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:166` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:167` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:168` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:169` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:170` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:171` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:172` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:173` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:175` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:176` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:177` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:178` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:179` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:181` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:182` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:188` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:189` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:190` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:191` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:192` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:193` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:194` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:195` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:197` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:198` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:199` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:200` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:201` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:202` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:208` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:209` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:210` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:211` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:213` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:214` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:215` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:216` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:217` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:218` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:219` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:220` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:221` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:222` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:223` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:224` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:225` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:226` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:227` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:228` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:229` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:230` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:231` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:232` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:233` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:234` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:235` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:236` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:237` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:238` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:239` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:240` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:241` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:242` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:243` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:245` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:290` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:466` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:553` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:614` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `down2_overlap_tile_runner.v:631` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
