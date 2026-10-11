# Verilog deliverable gate

Root: `E:\project\qiansai\anlogic_topic2_work\lab1_sc500_road_vision\cnn\hw_validation\production\reports\v10_postprocess_overlap_20261007\rtl\road_postprocess_stream.v`
Delivery ready: `False`
Summary: **669 error(s)**, **0 strict warning(s)**

## Actionable VG findings

<a id="vg-finding-1"></a>
### VG007: Standard bilingual header with English/Chinese sections is required.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:1`
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
- Location: `road_postprocess_stream.v:1`
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
- Location: `road_postprocess_stream.v:1`
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
- Location: `road_postprocess_stream.v:1`
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
- Location: `road_postprocess_stream.v:1`
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
### VG040: Generated explanatory comments should be Chinese-first.
- Status: `failed`
- Severity: `error`
- Location: `file:road_postprocess_stream.v:unknown`
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

<a id="vg-finding-7"></a>
### VG009: Module `road_postprocess_stream` port list should use Chinese group comments such as 全局信号, 用户接口, or protocol 接口 groups.
- Status: `failed`
- Severity: `error`
- Location: `file:road_postprocess_stream.v:unknown`
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

<a id="vg-finding-8"></a>
### VG015: Internal non-array reg declaration `reg_group_data_head` must be explicitly initialized inside the module; when backfilling a missing initializer, use exact ` = 0;`.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:46`
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

<a id="vg-finding-9"></a>
### VG015: Internal non-array reg declaration `reg_group_data_tail` must be explicitly initialized inside the module; when backfilling a missing initializer, use exact ` = 0;`.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:47`
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

<a id="vg-finding-10"></a>
### VG015: Internal non-array reg declaration `reg_group_layer_head` must be explicitly initialized inside the module; when backfilling a missing initializer, use exact ` = 0;`.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:48`
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
### VG015: Internal non-array reg declaration `reg_group_layer_tail` must be explicitly initialized inside the module; when backfilling a missing initializer, use exact ` = 0;`.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:49`
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
### VG015: Internal non-array reg declaration `reg_group_position_head` must be explicitly initialized inside the module; when backfilling a missing initializer, use exact ` = 0;`.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:50`
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
### VG015: Internal non-array reg declaration `reg_group_position_tail` must be explicitly initialized inside the module; when backfilling a missing initializer, use exact ` = 0;`.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:51`
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
### VG015: Internal non-array reg declaration `reg_group_channel_head` must be explicitly initialized inside the module; when backfilling a missing initializer, use exact ` = 0;`.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:52`
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
### VG015: Internal non-array reg declaration `reg_group_channel_tail` must be explicitly initialized inside the module; when backfilling a missing initializer, use exact ` = 0;`.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:53`
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
### VG015: Internal non-array reg declaration `reg_group_mask_head` must be explicitly initialized inside the module; when backfilling a missing initializer, use exact ` = 0;`.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:54`
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

<a id="vg-finding-17"></a>
### VG015: Internal non-array reg declaration `reg_group_mask_tail` must be explicitly initialized inside the module; when backfilling a missing initializer, use exact ` = 0;`.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:55`
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
### VG015: Internal non-array reg declaration `cnt_result_queue` must be explicitly initialized inside the module; when backfilling a missing initializer, use exact ` = 0;`.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:56`
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
### VG015: Internal non-array reg declaration `cnt_meta_read` must be explicitly initialized inside the module; when backfilling a missing initializer, use exact ` = 0;`.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:59`
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
### VG015: Internal non-array reg declaration `cnt_meta_write` must be explicitly initialized inside the module; when backfilling a missing initializer, use exact ` = 0;`.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:60`
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
### VG015: Internal non-array reg declaration `cnt_meta` must be explicitly initialized inside the module; when backfilling a missing initializer, use exact ` = 0;`.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:61`
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
### VG015: Internal non-array reg declaration `cnt_pre_inflight` must be explicitly initialized inside the module; when backfilling a missing initializer, use exact ` = 0;`.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:62`
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
### VG015: Internal non-array reg declaration `cnt_post_inflight` must be explicitly initialized inside the module; when backfilling a missing initializer, use exact ` = 0;`.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:63`
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
### VG015: Internal non-array reg declaration `flag_fatal` must be explicitly initialized inside the module; when backfilling a missing initializer, use exact ` = 0;`.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:64`
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
### VG013: Flag-like signal `wire_scalar_extended` should use `flag_` prefix unless it is an output bridge.
- Status: `failed`
- Severity: `error`
- Location: `file:road_postprocess_stream.v:unknown`
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

<a id="vg-finding-26"></a>
### VG013: Flag-like signal `wire_factor_extended` should use `flag_` prefix unless it is an output bridge.
- Status: `failed`
- Severity: `error`
- Location: `file:road_postprocess_stream.v:unknown`
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

<a id="vg-finding-27"></a>
### VG013: Flag-like signal `pre_result_valid` should use `flag_` prefix unless it is an output bridge.
- Status: `failed`
- Severity: `error`
- Location: `file:road_postprocess_stream.v:unknown`
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

<a id="vg-finding-28"></a>
### VG013: Flag-like signal `silu_input_ready` should use `flag_` prefix unless it is an output bridge.
- Status: `failed`
- Severity: `error`
- Location: `file:road_postprocess_stream.v:unknown`
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
### VG013: Flag-like signal `silu_table_ready` should use `flag_` prefix unless it is an output bridge.
- Status: `failed`
- Severity: `error`
- Location: `file:road_postprocess_stream.v:unknown`
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
### VG013: Flag-like signal `silu_output_valid` should use `flag_` prefix unless it is an output bridge.
- Status: `failed`
- Severity: `error`
- Location: `file:road_postprocess_stream.v:unknown`
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
### VG013: Flag-like signal `post_result_valid` should use `flag_` prefix unless it is an output bridge.
- Status: `failed`
- Severity: `error`
- Location: `file:road_postprocess_stream.v:unknown`
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
### VG020: Always block `always@(posedge i_clk or negedge i_rstn)` assigns multiple targets ['cnt_result_queue', 'reg_group_channel_head', 'reg_group_channel_tail', 'reg_group_data_head', 'reg_group_data_tail', 'reg_group_layer_head', 'reg_group_layer_tail', 'reg_group_mask_head', 'reg_group_mask_tail', 'reg_group_position_head', 'reg_group_position_tail']; split to one target per always.
- Status: `failed`
- Severity: `error`
- Location: `file:road_postprocess_stream.v:unknown`
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

<a id="vg-finding-33"></a>
### VG020: Always block `always@(posedge i_clk or negedge i_rstn)` assigns multiple targets ['cnt_meta', 'cnt_meta_read', 'cnt_meta_write', 'reg_meta_fifo']; split to one target per always.
- Status: `failed`
- Severity: `error`
- Location: `file:road_postprocess_stream.v:unknown`
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

<a id="vg-finding-34"></a>
### VG020: Always block `always@(posedge i_clk or negedge i_rstn)` has complex lvalues and multiple targets; formatter must not guess a split.
- Status: `failed`
- Severity: `error`
- Location: `file:road_postprocess_stream.v:unknown`
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

<a id="vg-finding-35"></a>
### VG020: Always block `always@(posedge i_clk or negedge i_rstn)` assigns multiple targets ['cnt_post_inflight', 'cnt_pre_inflight', 'flag_fatal']; split to one target per always.
- Status: `failed`
- Severity: `error`
- Location: `file:road_postprocess_stream.v:unknown`
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

<a id="vg-finding-36"></a>
### VG031: Non-trivial RTL must use fixed Erie region banners.
- Status: `failed`
- Severity: `error`
- Location: `file:road_postprocess_stream.v:unknown`
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

<a id="vg-finding-37"></a>
### VG040: localparam `PRE_FACTOR_ALPHA` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:37`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.coverage
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-38"></a>
### VG040: localparam `PRE_FACTOR_BETA` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:38`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.coverage
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-39"></a>
### VG040: localparam `PRE_FACTOR_GAMMA` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:39`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.coverage
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-40"></a>
### VG040: localparam `PRE_SHIFT_ALPHA` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:40`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.coverage
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-41"></a>
### VG040: localparam `PRE_SHIFT_BETA` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:41`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.coverage
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-42"></a>
### VG040: localparam `PRE_SHIFT_GAMMA` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:42`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.coverage
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-43"></a>
### VG040: localparam `POST_FACTOR` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:43`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.coverage
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-44"></a>
### VG040: localparam `POST_SHIFT` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:44`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.coverage
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-45"></a>
### VG040: port `i_clk` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:6`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.coverage
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-46"></a>
### VG040: port `i_rstn` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:7`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.coverage
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-47"></a>
### VG040: port `i_table_valid` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:8`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.coverage
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-48"></a>
### VG040: port `i_table_addr` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:9`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.coverage
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-49"></a>
### VG040: port `i_table_data` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:10`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.coverage
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-50"></a>
### VG040: port `o_table_ready` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:11`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.coverage
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-51"></a>
### VG040: port `o_table_loaded` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:12`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.coverage
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-52"></a>
### VG040: port `o_table_fault` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:13`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.coverage
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-53"></a>
### VG040: port `i_input_valid` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:14`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.coverage
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-54"></a>
### VG040: port `i_result_data` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:15`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.coverage
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-55"></a>
### VG040: port `i_result_fault` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:16`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.coverage
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-56"></a>
### VG040: port `i_layer` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:17`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.coverage
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-57"></a>
### VG040: port `i_position` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:18`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.coverage
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-58"></a>
### VG040: port `i_channel_base` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:19`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.coverage
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-59"></a>
### VG040: port `i_lane_mask` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:20`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.coverage
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-60"></a>
### VG040: port `o_input_ready` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:21`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.coverage
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-61"></a>
### VG040: port `i_output_ready` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:22`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.coverage
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-62"></a>
### VG040: port `o_output_valid` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:23`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.coverage
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-63"></a>
### VG040: port `o_output_data` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:24`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.coverage
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-64"></a>
### VG040: port `o_output_tag` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:25`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.coverage
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-65"></a>
### VG040: port `o_fault` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:26`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.coverage
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-66"></a>
### VG040: port `o_result_queue_count` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:27`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.coverage
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-67"></a>
### VG040: port `o_meta_count` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:28`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.coverage
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-68"></a>
### VG040: port `o_pre_busy` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:29`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.coverage
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-69"></a>
### VG040: port `o_silu_busy` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:30`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.coverage
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-70"></a>
### VG040: port `o_post_busy` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:31`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.coverage
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-71"></a>
### VG040: port `o_pre_accept` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:32`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.coverage
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-72"></a>
### VG040: port `o_silu_accept` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:33`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.coverage
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-73"></a>
### VG040: port `o_post_accept` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:34`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.coverage
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-74"></a>
### VG040: signal `reg_group_data_head` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:46`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.coverage
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-75"></a>
### VG040: signal `reg_group_data_tail` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:47`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.coverage
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-76"></a>
### VG040: signal `reg_group_layer_head` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:48`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.coverage
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-77"></a>
### VG040: signal `reg_group_layer_tail` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.coverage
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-78"></a>
### VG040: signal `reg_group_position_head` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:50`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.coverage
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-79"></a>
### VG040: signal `reg_group_position_tail` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:51`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.coverage
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-80"></a>
### VG040: signal `reg_group_channel_head` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:52`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.coverage
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-81"></a>
### VG040: signal `reg_group_channel_tail` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:53`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.coverage
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-82"></a>
### VG040: signal `reg_group_mask_head` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:54`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.coverage
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-83"></a>
### VG040: signal `reg_group_mask_tail` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:55`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.coverage
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-84"></a>
### VG040: signal `cnt_result_queue` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:56`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.coverage
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-85"></a>
### VG040: signal `reg_meta_fifo` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:58`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.coverage
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-86"></a>
### VG040: signal `cnt_meta_read` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:59`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.coverage
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-87"></a>
### VG040: signal `cnt_meta_write` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:60`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.coverage
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-88"></a>
### VG040: signal `cnt_meta` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:61`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.coverage
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-89"></a>
### VG040: signal `cnt_pre_inflight` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:62`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG040: signal `cnt_post_inflight` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:63`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG040: signal `flag_fatal` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:64`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG040: signal `wire_selected_lane` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:66`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG040: signal `wire_scalar_data` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:67`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG040: signal `wire_pre_factor` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:68`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG040: signal `wire_pre_shift` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:69`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG040: signal `wire_scalar_extended` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:70`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG040: signal `wire_factor_extended` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:71`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG040: signal `wire_pre_product` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:72`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG040: signal `wire_scalar_channel` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:73`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG040: signal `wire_scalar_tag` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:74`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG040: signal `flag_scalar_valid` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:75`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG040: signal `flag_scalar_last` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:76`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG040: signal `flag_group_push` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:77`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG040: signal `flag_group_pop` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:78`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG040: signal `flag_base_aligned` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:79`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG040: signal `flag_lane_shape_valid` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:80`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG040: signal `flag_input_shape_fault` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:81`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG040: signal `flag_input_accept` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:82`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG040: signal `flag_fault_event` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:83`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG040: signal `flag_pre_advance` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:85`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG040: signal `flag_pre_accept` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:86`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG040: signal `pre_result_valid` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:87`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG040: signal `pre_result_data` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:88`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG040: signal `pre_result_tag` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:89`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG040: signal `pre_result_fault` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:90`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG040: signal `silu_input_ready` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:92`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG040: signal `silu_table_ready` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:93`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG040: signal `silu_table_loaded` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:94`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG040: signal `silu_table_fault` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:95`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG040: signal `silu_output_valid` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:96`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG040: signal `silu_output_data` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:97`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG040: signal `flag_silu_accept` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:98`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG040: signal `flag_silu_output_ready` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:99`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG040: signal `flag_post_advance` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:101`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG040: signal `flag_post_accept` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:102`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG040: signal `post_result_valid` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:103`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG040: signal `post_result_data` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:104`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG040: signal `post_result_tag` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:105`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG040: signal `post_result_fault` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:106`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG040: signal `flag_output_accept` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:107`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG040: signal `wire_post_product` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:108`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG040: signal `wire_output_saturated` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:109`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG040: signal `flag_pipeline_empty` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:110`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG040: signal `flag_table_forward` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:111`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG040: assign `wire_selected_lane` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:113`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG040: assign `wire_scalar_data` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:115`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG040: assign `wire_pre_factor` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:118`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG040: assign `wire_pre_shift` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:120`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG040: assign `wire_scalar_extended` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:122`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG040: assign `wire_factor_extended` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:123`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG040: assign `wire_pre_product` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:124`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG040: assign `wire_scalar_channel` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:125`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG040: assign `wire_scalar_tag` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:126`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG040: assign `flag_scalar_valid` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:127`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG040: assign `flag_scalar_last` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:129`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG040: assign `flag_base_aligned` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:131`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG040: assign `flag_lane_shape_valid` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:135`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG040: assign `flag_input_shape_fault` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:138`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG040: assign `o_input_ready` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:141`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG040: assign `flag_input_accept` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:143`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG040: assign `flag_group_push` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:144`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG040: assign `flag_group_pop` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:145`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG040: assign `flag_silu_accept` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:147`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG040: assign `flag_pre_advance` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:149`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG040: assign `flag_pre_accept` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:150`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG040: assign `flag_post_advance` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:152`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG040: assign `flag_silu_output_ready` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:154`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG040: assign `flag_post_accept` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:155`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG040: assign `flag_output_accept` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:156`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG040: assign `wire_post_product` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:157`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG040: assign `wire_output_saturated` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:158`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG040: assign `flag_fault_event` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:161`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG040: assign `flag_pipeline_empty` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:164`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG040: assign `flag_table_forward` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:166`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG040: assign `o_table_ready` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:168`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG040: assign `o_table_loaded` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:169`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG040: assign `o_table_fault` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:170`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG040: assign `o_output_valid` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:171`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG040: assign `o_output_data` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:172`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG040: assign `o_output_tag` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:173`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG040: assign `o_fault` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:174`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG040: assign `o_result_queue_count` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:175`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG040: assign `o_meta_count` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:176`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG040: assign `o_pre_busy` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:177`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG040: assign `o_silu_busy` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:178`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG040: assign `o_post_busy` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:179`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG040: assign `o_pre_accept` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:180`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG040: assign `o_silu_accept` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:181`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG040: assign `o_post_accept` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:182`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG040: Always block `always@(posedge i_clk or negedge i_rstn)` should have a nearby leading comment explaining behavior.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:184`
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

<a id="vg-finding-181"></a>
### VG040: Always block `always@(posedge i_clk or negedge i_rstn)` should have a nearby leading comment explaining behavior.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:264`
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

<a id="vg-finding-182"></a>
### VG040: Always block `always@(posedge i_clk or negedge i_rstn)` should have a nearby leading comment explaining behavior.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:289`
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

<a id="vg-finding-183"></a>
### VG040: Instance `road_round_shift_Inst_pre` should have a leading function/connection comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:313`
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

<a id="vg-finding-184"></a>
### VG040: Instance `silu_shared_unit_Inst_shared` should have a leading function/connection comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:327`
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

<a id="vg-finding-185"></a>
### VG040: Instance `road_round_shift_Inst_post` should have a leading function/connection comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:344`
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

<a id="vg-finding-186"></a>
### VG062: process assignment `reg_group_data_head` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:186`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.procedural_assignment
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-187"></a>
### VG062: process assignment `reg_group_data_tail` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:187`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.procedural_assignment
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-188"></a>
### VG062: process assignment `reg_group_layer_head` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:188`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.procedural_assignment
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-189"></a>
### VG062: process assignment `reg_group_layer_tail` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:189`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.procedural_assignment
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-190"></a>
### VG062: process assignment `reg_group_position_head` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:190`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.procedural_assignment
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-191"></a>
### VG062: process assignment `reg_group_position_tail` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:191`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.procedural_assignment
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-192"></a>
### VG062: process assignment `reg_group_channel_head` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:192`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.procedural_assignment
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-193"></a>
### VG062: process assignment `reg_group_channel_tail` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:193`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `reg_group_mask_head` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:194`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `reg_group_mask_tail` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:195`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `cnt_result_queue` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:196`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `reg_group_mask_head` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:198`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `reg_group_mask_tail` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:199`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `cnt_result_queue` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:200`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `cnt_result_queue` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:204`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `reg_group_data_head` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:206`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `reg_group_layer_head` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:207`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `reg_group_position_head` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:208`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `reg_group_channel_head` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:209`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `reg_group_mask_head` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:210`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `reg_group_data_tail` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:212`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `reg_group_layer_tail` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:213`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `reg_group_position_tail` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:214`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `reg_group_channel_tail` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:215`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `reg_group_mask_tail` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:216`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `reg_group_mask_head` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:218`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `cnt_result_queue` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:223`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `reg_group_data_head` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:225`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `reg_group_layer_head` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:226`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `reg_group_position_head` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:227`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `reg_group_channel_head` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:228`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `reg_group_mask_head` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:229`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `reg_group_mask_head` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:231`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `cnt_result_queue` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:235`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `reg_group_data_head` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:237`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `reg_group_layer_head` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:238`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `reg_group_position_head` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:239`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `reg_group_channel_head` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:240`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `reg_group_mask_head` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:241`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `reg_group_data_tail` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:242`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `reg_group_layer_tail` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:243`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `reg_group_position_tail` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:244`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `reg_group_channel_tail` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:245`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `reg_group_mask_tail` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:246`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `reg_group_data_head` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:248`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `reg_group_layer_head` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:249`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `reg_group_position_head` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:250`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `reg_group_channel_head` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:251`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `reg_group_mask_head` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:252`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `reg_group_mask_head` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:257`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `cnt_meta_read` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:266`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `cnt_meta_write` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:267`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `cnt_meta` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:268`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `cnt_meta_read` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:270`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `cnt_meta_write` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:271`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `cnt_meta` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:272`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `reg_meta_fifo[cnt_meta_write]` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:275`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `cnt_meta_write` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:276`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `cnt_meta_read` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:279`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `cnt_pre_inflight` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:291`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `cnt_post_inflight` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:292`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `flag_fatal` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:293`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `cnt_pre_inflight` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:295`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `cnt_post_inflight` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:296`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `flag_fatal` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:297`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `flag_fatal` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:309`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG064: instance mapping `.i_clk` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:314`
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

<a id="vg-finding-253"></a>
### VG064: instance mapping `.i_rstn` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:315`
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

<a id="vg-finding-254"></a>
### VG064: instance mapping `.i_advance` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:316`
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

<a id="vg-finding-255"></a>
### VG064: instance mapping `.i_input_valid` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:317`
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

<a id="vg-finding-256"></a>
### VG064: instance mapping `.i_product` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:318`
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

<a id="vg-finding-257"></a>
### VG064: instance mapping `.i_shift` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:319`
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

<a id="vg-finding-258"></a>
### VG064: instance mapping `.i_tag` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:320`
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

<a id="vg-finding-259"></a>
### VG064: instance mapping `.o_result_valid` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:321`
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

<a id="vg-finding-260"></a>
### VG064: instance mapping `.o_result_data` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:322`
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

<a id="vg-finding-261"></a>
### VG064: instance mapping `.o_result_tag` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:323`
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

<a id="vg-finding-262"></a>
### VG064: instance mapping `.o_fault` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:324`
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

<a id="vg-finding-263"></a>
### VG064: instance mapping `.i_clk` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:328`
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

<a id="vg-finding-264"></a>
### VG064: instance mapping `.i_rstn` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:329`
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

<a id="vg-finding-265"></a>
### VG064: instance mapping `.i_table_valid` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:330`
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

<a id="vg-finding-266"></a>
### VG064: instance mapping `.i_table_addr` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:331`
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

<a id="vg-finding-267"></a>
### VG064: instance mapping `.i_table_data` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:332`
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

<a id="vg-finding-268"></a>
### VG064: instance mapping `.i_input_valid` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:333`
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

<a id="vg-finding-269"></a>
### VG064: instance mapping `.i_input_data` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:334`
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

<a id="vg-finding-270"></a>
### VG064: instance mapping `.i_output_ready` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:335`
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

<a id="vg-finding-271"></a>
### VG064: instance mapping `.o_table_ready` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:336`
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

<a id="vg-finding-272"></a>
### VG064: instance mapping `.o_input_ready` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:337`
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

<a id="vg-finding-273"></a>
### VG064: instance mapping `.o_output_valid` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:338`
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

<a id="vg-finding-274"></a>
### VG064: instance mapping `.o_output_data` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:339`
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

<a id="vg-finding-275"></a>
### VG064: instance mapping `.o_table_loaded` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:340`
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

<a id="vg-finding-276"></a>
### VG064: instance mapping `.o_table_fault` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:341`
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

<a id="vg-finding-277"></a>
### VG064: instance mapping `.i_clk` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:345`
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

<a id="vg-finding-278"></a>
### VG064: instance mapping `.i_rstn` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:346`
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

<a id="vg-finding-279"></a>
### VG064: instance mapping `.i_advance` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:347`
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

<a id="vg-finding-280"></a>
### VG064: instance mapping `.i_input_valid` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:348`
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

<a id="vg-finding-281"></a>
### VG064: instance mapping `.i_product` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:349`
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

<a id="vg-finding-282"></a>
### VG064: instance mapping `.i_shift` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:350`
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

<a id="vg-finding-283"></a>
### VG064: instance mapping `.i_tag` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:351`
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

<a id="vg-finding-284"></a>
### VG064: instance mapping `.o_result_valid` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:352`
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

<a id="vg-finding-285"></a>
### VG064: instance mapping `.o_result_data` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:353`
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

<a id="vg-finding-286"></a>
### VG064: instance mapping `.o_result_tag` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:354`
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

<a id="vg-finding-287"></a>
### VG064: instance mapping `.o_fault` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_postprocess_stream.v:355`
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

<a id="vg-finding-288"></a>
### VG042: Comment coverage is too low for generated RTL (0.00%); add semantic comments near declarations, assigns, always blocks, FSM, and instances.
- Status: `failed`
- Severity: `error`
- Location: `file:road_postprocess_stream.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG084: 存在无法静态确定的 case 控制项或标签位宽。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `run:unknown`
- Evidence:
- node_kind: `verilog_project`
- detail: gate_id=VG084; rule_key=case_item_in_range_width; status=inconclusive; applicable=True; reason=存在无法静态确定的 case 控制项或标签位宽。
- source_excerpt: `gate_id=VG084; rule_key=case_item_in_range_width; status=inconclusive; applicable=True; reason=存在无法静态确定的 case 控制项或标签位宽。`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
gate_id=VG084; rule_key=case_item_in_range_width; status=inconclusive; applicable=True; reason=存在无法静态确定的 case 控制项或标签位宽。
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-290"></a>
### VG097: 缺少外部模块接口定义，无法静态比较端口位宽。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:313`
- Evidence:
- node_kind: `verilog_rtl`
- detail: road_round_shift road_round_shift_Inst_pre
- source_excerpt: `road_round_shift road_round_shift_Inst_pre`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
road_round_shift road_round_shift_Inst_pre
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-291"></a>
### VG097: 缺少外部模块接口定义，无法静态比较端口位宽。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:327`
- Evidence:
- node_kind: `verilog_rtl`
- detail: silu_shared_unit silu_shared_unit_Inst_shared
- source_excerpt: `silu_shared_unit silu_shared_unit_Inst_shared`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
silu_shared_unit silu_shared_unit_Inst_shared
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-292"></a>
### VG097: 缺少外部模块接口定义，无法静态比较端口位宽。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:344`
- Evidence:
- node_kind: `verilog_rtl`
- detail: road_round_shift road_round_shift_Inst_post
- source_excerpt: `road_round_shift road_round_shift_Inst_post`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
road_round_shift road_round_shift_Inst_post
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-293"></a>
### VG110: 同一时序块中存在未统一复位的触发器目标。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:264`
- Evidence:
- node_kind: `verilog_rtl`
- detail: reg_meta_fifo
- source_excerpt: `reg_meta_fifo`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
reg_meta_fifo
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-294"></a>
### VG113: 同一时序块中存在未统一复位的触发器目标。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:264`
- Evidence:
- node_kind: `verilog_rtl`
- detail: reg_meta_fifo
- source_excerpt: `reg_meta_fifo`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
reg_meta_fifo
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-295"></a>
### VG122: 算术结果位宽超过赋值目标位宽。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:204`
- Evidence:
- node_kind: `verilog_rtl`
- detail: cnt_result_queue <= cnt_result_queue + 1'b1;
- source_excerpt: `cnt_result_queue <= cnt_result_queue + 1'b1;`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
cnt_result_queue <= cnt_result_queue + 1'b1;
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-296"></a>
### VG122: 算术结果位宽超过赋值目标位宽。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:223`
- Evidence:
- node_kind: `verilog_rtl`
- detail: cnt_result_queue <= cnt_result_queue - 1'b1;
- source_excerpt: `cnt_result_queue <= cnt_result_queue - 1'b1;`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
cnt_result_queue <= cnt_result_queue - 1'b1;
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-297"></a>
### VG122: 算术结果位宽超过赋值目标位宽。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:276`
- Evidence:
- node_kind: `verilog_rtl`
- detail: cnt_meta_write <= cnt_meta_write + 1'b1;
- source_excerpt: `cnt_meta_write <= cnt_meta_write + 1'b1;`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
cnt_meta_write <= cnt_meta_write + 1'b1;
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-298"></a>
### VG122: 算术结果位宽超过赋值目标位宽。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:279`
- Evidence:
- node_kind: `verilog_rtl`
- detail: cnt_meta_read <= cnt_meta_read + 1'b1;
- source_excerpt: `cnt_meta_read <= cnt_meta_read + 1'b1;`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
cnt_meta_read <= cnt_meta_read + 1'b1;
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-299"></a>
### VG122: 算术结果位宽超过赋值目标位宽。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:282`
- Evidence:
- node_kind: `verilog_rtl`
- detail: cnt_meta <= cnt_meta + 1'b1;
- source_excerpt: `cnt_meta <= cnt_meta + 1'b1;`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
cnt_meta <= cnt_meta + 1'b1;
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-300"></a>
### VG122: 算术结果位宽超过赋值目标位宽。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:283`
- Evidence:
- node_kind: `verilog_rtl`
- detail: cnt_meta <= cnt_meta - 1'b1;
- source_excerpt: `cnt_meta <= cnt_meta - 1'b1;`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
cnt_meta <= cnt_meta - 1'b1;
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-301"></a>
### VG122: 算术结果位宽超过赋值目标位宽。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:300`
- Evidence:
- node_kind: `verilog_rtl`
- detail: cnt_pre_inflight <= cnt_pre_inflight + 1'b1;
- source_excerpt: `cnt_pre_inflight <= cnt_pre_inflight + 1'b1;`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
cnt_pre_inflight <= cnt_pre_inflight + 1'b1;
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-302"></a>
### VG122: 算术结果位宽超过赋值目标位宽。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:301`
- Evidence:
- node_kind: `verilog_rtl`
- detail: cnt_pre_inflight <= cnt_pre_inflight - 1'b1;
- source_excerpt: `cnt_pre_inflight <= cnt_pre_inflight - 1'b1;`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
cnt_pre_inflight <= cnt_pre_inflight - 1'b1;
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-303"></a>
### VG122: 算术结果位宽超过赋值目标位宽。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:305`
- Evidence:
- node_kind: `verilog_rtl`
- detail: cnt_post_inflight <= cnt_post_inflight + 1'b1;
- source_excerpt: `cnt_post_inflight <= cnt_post_inflight + 1'b1;`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
cnt_post_inflight <= cnt_post_inflight + 1'b1;
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-304"></a>
### VG122: 算术结果位宽超过赋值目标位宽。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:306`
- Evidence:
- node_kind: `verilog_rtl`
- detail: cnt_post_inflight <= cnt_post_inflight - 1'b1;
- source_excerpt: `cnt_post_inflight <= cnt_post_inflight - 1'b1;`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
cnt_post_inflight <= cnt_post_inflight - 1'b1;
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-305"></a>
### VG125: 字面量声明为 2 位，但实际值只需要 1 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:114`
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

<a id="vg-finding-306"></a>
### VG125: 字面量声明为 2 位，但实际值只需要 1 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:116`
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

<a id="vg-finding-307"></a>
### VG125: 字面量声明为 2 位，但实际值只需要 1 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:119`
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

<a id="vg-finding-308"></a>
### VG125: 字面量声明为 2 位，但实际值只需要 1 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:121`
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

<a id="vg-finding-309"></a>
### VG125: 字面量声明为 5 位，但实际值只需要 2 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:131`
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

<a id="vg-finding-310"></a>
### VG125: 字面量声明为 5 位，但实际值只需要 3 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:132`
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

<a id="vg-finding-311"></a>
### VG125: 字面量声明为 5 位，但实际值只需要 4 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:132`
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

<a id="vg-finding-312"></a>
### VG125: 字面量声明为 5 位，但实际值只需要 4 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:133`
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

<a id="vg-finding-313"></a>
### VG125: 字面量声明为 5 位，但实际值只需要 4 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:133`
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

<a id="vg-finding-314"></a>
### VG125: 字面量声明为 2 位，但实际值只需要 1 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:140`
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

<a id="vg-finding-315"></a>
### VG125: 字面量声明为 5 位，但实际值只需要 4 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:140`
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

<a id="vg-finding-316"></a>
### VG125: 字面量声明为 16 位，但实际值只需要 7 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:158`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 16'sd127
- source_excerpt: `16'sd127`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
16'sd127
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-317"></a>
### VG125: 字面量声明为 8 位，但实际值只需要 7 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:158`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 8'sd127
- source_excerpt: `8'sd127`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
8'sd127
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-318"></a>
### VG125: 字面量声明为 16 位，但实际值只需要 8 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:159`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 16'sd128
- source_excerpt: `16'sd128`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
16'sd128
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-319"></a>
### VG132: 未登记原语或外部模块的时钟角色无法静态确定。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:313`
- Evidence:
- node_kind: `verilog_rtl`
- detail: road_round_shift road_round_shift_Inst_pre
- source_excerpt: `road_round_shift road_round_shift_Inst_pre`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
road_round_shift road_round_shift_Inst_pre
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-320"></a>
### VG132: 未登记原语或外部模块的时钟角色无法静态确定。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:327`
- Evidence:
- node_kind: `verilog_rtl`
- detail: silu_shared_unit silu_shared_unit_Inst_shared
- source_excerpt: `silu_shared_unit silu_shared_unit_Inst_shared`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
silu_shared_unit silu_shared_unit_Inst_shared
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-321"></a>
### VG132: 未登记原语或外部模块的时钟角色无法静态确定。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:344`
- Evidence:
- node_kind: `verilog_rtl`
- detail: road_round_shift road_round_shift_Inst_post
- source_excerpt: `road_round_shift road_round_shift_Inst_post`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
road_round_shift road_round_shift_Inst_post
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-322"></a>
### VG138: 常量未显式声明位宽和进制。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_postprocess_stream.v:122`
- Evidence:
- node_kind: `verilog_rtl`
- detail: = {{32
- source_excerpt: `= {{32`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
= {{32
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-323"></a>
### VG138: 常量未显式声明位宽和进制。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_postprocess_stream.v:123`
- Evidence:
- node_kind: `verilog_rtl`
- detail: = {{32
- source_excerpt: `= {{32`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
= {{32
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-324"></a>
### VG145: 组合逻辑完整依赖锥最多允许三个源信号，超限逻辑必须由时序 reg 隔断。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:161`
- Evidence:
- node_kind: `verilog_rtl`
- detail: flag_fault_event: 16 sources: cnt_result_queue, flag_fatal, i_channel_base, i_input_valid, i_lane_mask, i_lane_mask[1], i_lane_mask[2], i_layer, i_result_fault, i_table_valid, post_result_fault, post_result_valid, pre_result_fault, pre_result_valid, silu_table_fault, silu_table_loaded
- source_excerpt: `flag_fault_event: 16 sources: cnt_result_queue, flag_fatal, i_channel_base, i_input_valid, i_lane_mask, i_lane_mask[1], i_lane_mask[2], i_layer, i_result_fault, i_table_valid, post_result_fault, post_result_valid, pre_result_fault, pre_result_valid, silu_table_fault, silu_table_loaded`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
flag_fault_event: 16 sources: cnt_result_queue, flag_fatal, i_channel_base, i_input_valid, i_lane_mask, i_lane_mask[1], i_lane_mask[2], i_layer, i_result_fault, i_table_valid, post_result_fault, post_result_valid, pre_result_fault, pre_result_valid, silu_table_fault, silu_table_loaded
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-325"></a>
### VG145: 组合逻辑完整依赖锥最多允许三个源信号，超限逻辑必须由时序 reg 隔断。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:145`
- Evidence:
- node_kind: `verilog_rtl`
- detail: flag_group_pop: 10 sources: cnt_meta, cnt_result_queue, flag_fatal, pre_result_fault, pre_result_valid, reg_group_mask_head, reg_group_mask_head[0], reg_group_mask_head[1], silu_input_ready, silu_table_loaded
- source_excerpt: `flag_group_pop: 10 sources: cnt_meta, cnt_result_queue, flag_fatal, pre_result_fault, pre_result_valid, reg_group_mask_head, reg_group_mask_head[0], reg_group_mask_head[1], silu_input_ready, silu_table_loaded`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
flag_group_pop: 10 sources: cnt_meta, cnt_result_queue, flag_fatal, pre_result_fault, pre_result_valid, reg_group_mask_head, reg_group_mask_head[0], reg_group_mask_head[1], silu_input_ready, silu_table_loaded
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-326"></a>
### VG145: 组合逻辑完整依赖锥最多允许三个源信号，超限逻辑必须由时序 reg 隔断。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:144`
- Evidence:
- node_kind: `verilog_rtl`
- detail: flag_group_push: 12 sources: cnt_result_queue, flag_fatal, i_channel_base, i_input_valid, i_lane_mask, i_lane_mask[1], i_lane_mask[2], i_layer, i_result_fault, i_table_valid, silu_table_fault, silu_table_loaded
- source_excerpt: `flag_group_push: 12 sources: cnt_result_queue, flag_fatal, i_channel_base, i_input_valid, i_lane_mask, i_lane_mask[1], i_lane_mask[2], i_layer, i_result_fault, i_table_valid, silu_table_fault, silu_table_loaded`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
flag_group_push: 12 sources: cnt_result_queue, flag_fatal, i_channel_base, i_input_valid, i_lane_mask, i_lane_mask[1], i_lane_mask[2], i_layer, i_result_fault, i_table_valid, silu_table_fault, silu_table_loaded
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-327"></a>
### VG145: 组合逻辑完整依赖锥最多允许三个源信号，超限逻辑必须由时序 reg 隔断。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:143`
- Evidence:
- node_kind: `verilog_rtl`
- detail: flag_input_accept: 6 sources: cnt_result_queue, flag_fatal, i_input_valid, i_table_valid, silu_table_fault, silu_table_loaded
- source_excerpt: `flag_input_accept: 6 sources: cnt_result_queue, flag_fatal, i_input_valid, i_table_valid, silu_table_fault, silu_table_loaded`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
flag_input_accept: 6 sources: cnt_result_queue, flag_fatal, i_input_valid, i_table_valid, silu_table_fault, silu_table_loaded
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-328"></a>
### VG145: 组合逻辑完整依赖锥最多允许三个源信号，超限逻辑必须由时序 reg 隔断。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:138`
- Evidence:
- node_kind: `verilog_rtl`
- detail: flag_input_shape_fault: 5 sources: i_channel_base, i_lane_mask, i_lane_mask[1], i_lane_mask[2], i_layer
- source_excerpt: `flag_input_shape_fault: 5 sources: i_channel_base, i_lane_mask, i_lane_mask[1], i_lane_mask[2], i_layer`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
flag_input_shape_fault: 5 sources: i_channel_base, i_lane_mask, i_lane_mask[1], i_lane_mask[2], i_layer
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-329"></a>
### VG145: 组合逻辑完整依赖锥最多允许三个源信号，超限逻辑必须由时序 reg 隔断。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:156`
- Evidence:
- node_kind: `verilog_rtl`
- detail: flag_output_accept: 4 sources: flag_fatal, i_output_ready, post_result_fault, post_result_valid
- source_excerpt: `flag_output_accept: 4 sources: flag_fatal, i_output_ready, post_result_fault, post_result_valid`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
flag_output_accept: 4 sources: flag_fatal, i_output_ready, post_result_fault, post_result_valid
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-330"></a>
### VG145: 组合逻辑完整依赖锥最多允许三个源信号，超限逻辑必须由时序 reg 隔断。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:164`
- Evidence:
- node_kind: `verilog_rtl`
- detail: flag_pipeline_empty: 4 sources: cnt_meta, cnt_post_inflight, cnt_pre_inflight, cnt_result_queue
- source_excerpt: `flag_pipeline_empty: 4 sources: cnt_meta, cnt_post_inflight, cnt_pre_inflight, cnt_result_queue`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
flag_pipeline_empty: 4 sources: cnt_meta, cnt_post_inflight, cnt_pre_inflight, cnt_result_queue
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-331"></a>
### VG145: 组合逻辑完整依赖锥最多允许三个源信号，超限逻辑必须由时序 reg 隔断。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:155`
- Evidence:
- node_kind: `verilog_rtl`
- detail: flag_post_accept: 6 sources: cnt_meta, flag_fatal, i_output_ready, post_result_fault, post_result_valid, silu_output_valid
- source_excerpt: `flag_post_accept: 6 sources: cnt_meta, flag_fatal, i_output_ready, post_result_fault, post_result_valid, silu_output_valid`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
flag_post_accept: 6 sources: cnt_meta, flag_fatal, i_output_ready, post_result_fault, post_result_valid, silu_output_valid
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-332"></a>
### VG145: 组合逻辑完整依赖锥最多允许三个源信号，超限逻辑必须由时序 reg 隔断。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:152`
- Evidence:
- node_kind: `verilog_rtl`
- detail: flag_post_advance: 4 sources: flag_fatal, i_output_ready, post_result_fault, post_result_valid
- source_excerpt: `flag_post_advance: 4 sources: flag_fatal, i_output_ready, post_result_fault, post_result_valid`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
flag_post_advance: 4 sources: flag_fatal, i_output_ready, post_result_fault, post_result_valid
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-333"></a>
### VG145: 组合逻辑完整依赖锥最多允许三个源信号，超限逻辑必须由时序 reg 隔断。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:150`
- Evidence:
- node_kind: `verilog_rtl`
- detail: flag_pre_accept: 8 sources: cnt_meta, cnt_result_queue, flag_fatal, pre_result_fault, pre_result_valid, reg_group_mask_head, silu_input_ready, silu_table_loaded
- source_excerpt: `flag_pre_accept: 8 sources: cnt_meta, cnt_result_queue, flag_fatal, pre_result_fault, pre_result_valid, reg_group_mask_head, silu_input_ready, silu_table_loaded`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
flag_pre_accept: 8 sources: cnt_meta, cnt_result_queue, flag_fatal, pre_result_fault, pre_result_valid, reg_group_mask_head, silu_input_ready, silu_table_loaded
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-334"></a>
### VG145: 组合逻辑完整依赖锥最多允许三个源信号，超限逻辑必须由时序 reg 隔断。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:149`
- Evidence:
- node_kind: `verilog_rtl`
- detail: flag_pre_advance: 5 sources: cnt_meta, flag_fatal, pre_result_fault, pre_result_valid, silu_input_ready
- source_excerpt: `flag_pre_advance: 5 sources: cnt_meta, flag_fatal, pre_result_fault, pre_result_valid, silu_input_ready`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
flag_pre_advance: 5 sources: cnt_meta, flag_fatal, pre_result_fault, pre_result_valid, silu_input_ready
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-335"></a>
### VG145: 组合逻辑完整依赖锥最多允许三个源信号，超限逻辑必须由时序 reg 隔断。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:127`
- Evidence:
- node_kind: `verilog_rtl`
- detail: flag_scalar_valid: 4 sources: cnt_result_queue, flag_fatal, reg_group_mask_head, silu_table_loaded
- source_excerpt: `flag_scalar_valid: 4 sources: cnt_result_queue, flag_fatal, reg_group_mask_head, silu_table_loaded`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
flag_scalar_valid: 4 sources: cnt_result_queue, flag_fatal, reg_group_mask_head, silu_table_loaded
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-336"></a>
### VG145: 组合逻辑完整依赖锥最多允许三个源信号，超限逻辑必须由时序 reg 隔断。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:147`
- Evidence:
- node_kind: `verilog_rtl`
- detail: flag_silu_accept: 5 sources: cnt_meta, flag_fatal, pre_result_fault, pre_result_valid, silu_input_ready
- source_excerpt: `flag_silu_accept: 5 sources: cnt_meta, flag_fatal, pre_result_fault, pre_result_valid, silu_input_ready`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
flag_silu_accept: 5 sources: cnt_meta, flag_fatal, pre_result_fault, pre_result_valid, silu_input_ready
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-337"></a>
### VG145: 组合逻辑完整依赖锥最多允许三个源信号，超限逻辑必须由时序 reg 隔断。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:154`
- Evidence:
- node_kind: `verilog_rtl`
- detail: flag_silu_output_ready: 5 sources: cnt_meta, flag_fatal, i_output_ready, post_result_fault, post_result_valid
- source_excerpt: `flag_silu_output_ready: 5 sources: cnt_meta, flag_fatal, i_output_ready, post_result_fault, post_result_valid`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
flag_silu_output_ready: 5 sources: cnt_meta, flag_fatal, i_output_ready, post_result_fault, post_result_valid
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-338"></a>
### VG145: 组合逻辑完整依赖锥最多允许三个源信号，超限逻辑必须由时序 reg 隔断。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:166`
- Evidence:
- node_kind: `verilog_rtl`
- detail: flag_table_forward: 6 sources: cnt_meta, cnt_post_inflight, cnt_pre_inflight, cnt_result_queue, flag_fatal, i_table_valid
- source_excerpt: `flag_table_forward: 6 sources: cnt_meta, cnt_post_inflight, cnt_pre_inflight, cnt_result_queue, flag_fatal, i_table_valid`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
flag_table_forward: 6 sources: cnt_meta, cnt_post_inflight, cnt_pre_inflight, cnt_result_queue, flag_fatal, i_table_valid
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-339"></a>
### VG145: 组合逻辑完整依赖锥最多允许三个源信号，超限逻辑必须由时序 reg 隔断。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:141`
- Evidence:
- node_kind: `verilog_rtl`
- detail: o_input_ready: 5 sources: cnt_result_queue, flag_fatal, i_table_valid, silu_table_fault, silu_table_loaded
- source_excerpt: `o_input_ready: 5 sources: cnt_result_queue, flag_fatal, i_table_valid, silu_table_fault, silu_table_loaded`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
o_input_ready: 5 sources: cnt_result_queue, flag_fatal, i_table_valid, silu_table_fault, silu_table_loaded
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-340"></a>
### VG145: 组合逻辑完整依赖锥最多允许三个源信号，超限逻辑必须由时序 reg 隔断。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:182`
- Evidence:
- node_kind: `verilog_rtl`
- detail: o_post_accept: 6 sources: cnt_meta, flag_fatal, i_output_ready, post_result_fault, post_result_valid, silu_output_valid
- source_excerpt: `o_post_accept: 6 sources: cnt_meta, flag_fatal, i_output_ready, post_result_fault, post_result_valid, silu_output_valid`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
o_post_accept: 6 sources: cnt_meta, flag_fatal, i_output_ready, post_result_fault, post_result_valid, silu_output_valid
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-341"></a>
### VG145: 组合逻辑完整依赖锥最多允许三个源信号，超限逻辑必须由时序 reg 隔断。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:180`
- Evidence:
- node_kind: `verilog_rtl`
- detail: o_pre_accept: 8 sources: cnt_meta, cnt_result_queue, flag_fatal, pre_result_fault, pre_result_valid, reg_group_mask_head, silu_input_ready, silu_table_loaded
- source_excerpt: `o_pre_accept: 8 sources: cnt_meta, cnt_result_queue, flag_fatal, pre_result_fault, pre_result_valid, reg_group_mask_head, silu_input_ready, silu_table_loaded`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
o_pre_accept: 8 sources: cnt_meta, cnt_result_queue, flag_fatal, pre_result_fault, pre_result_valid, reg_group_mask_head, silu_input_ready, silu_table_loaded
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-342"></a>
### VG145: 组合逻辑完整依赖锥最多允许三个源信号，超限逻辑必须由时序 reg 隔断。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:181`
- Evidence:
- node_kind: `verilog_rtl`
- detail: o_silu_accept: 5 sources: cnt_meta, flag_fatal, pre_result_fault, pre_result_valid, silu_input_ready
- source_excerpt: `o_silu_accept: 5 sources: cnt_meta, flag_fatal, pre_result_fault, pre_result_valid, silu_input_ready`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
o_silu_accept: 5 sources: cnt_meta, flag_fatal, pre_result_fault, pre_result_valid, silu_input_ready
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-343"></a>
### VG145: 组合逻辑完整依赖锥最多允许三个源信号，超限逻辑必须由时序 reg 隔断。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:168`
- Evidence:
- node_kind: `verilog_rtl`
- detail: o_table_ready: 6 sources: cnt_meta, cnt_post_inflight, cnt_pre_inflight, cnt_result_queue, flag_fatal, silu_table_ready
- source_excerpt: `o_table_ready: 6 sources: cnt_meta, cnt_post_inflight, cnt_pre_inflight, cnt_result_queue, flag_fatal, silu_table_ready`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
o_table_ready: 6 sources: cnt_meta, cnt_post_inflight, cnt_pre_inflight, cnt_result_queue, flag_fatal, silu_table_ready
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-344"></a>
### VG145: 组合逻辑完整依赖锥最多允许三个源信号，超限逻辑必须由时序 reg 隔断。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:124`
- Evidence:
- node_kind: `verilog_rtl`
- detail: wire_pre_product: 5 sources: reg_group_data_head[31:0], reg_group_data_head[63:32], reg_group_data_head[95:64], reg_group_mask_head[0], reg_group_mask_head[1]
- source_excerpt: `wire_pre_product: 5 sources: reg_group_data_head[31:0], reg_group_data_head[63:32], reg_group_data_head[95:64], reg_group_mask_head[0], reg_group_mask_head[1]`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
wire_pre_product: 5 sources: reg_group_data_head[31:0], reg_group_data_head[63:32], reg_group_data_head[95:64], reg_group_mask_head[0], reg_group_mask_head[1]
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-345"></a>
### VG145: 组合逻辑完整依赖锥最多允许三个源信号，超限逻辑必须由时序 reg 隔断。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:115`
- Evidence:
- node_kind: `verilog_rtl`
- detail: wire_scalar_data: 5 sources: reg_group_data_head[31:0], reg_group_data_head[63:32], reg_group_data_head[95:64], reg_group_mask_head[0], reg_group_mask_head[1]
- source_excerpt: `wire_scalar_data: 5 sources: reg_group_data_head[31:0], reg_group_data_head[63:32], reg_group_data_head[95:64], reg_group_mask_head[0], reg_group_mask_head[1]`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
wire_scalar_data: 5 sources: reg_group_data_head[31:0], reg_group_data_head[63:32], reg_group_data_head[95:64], reg_group_mask_head[0], reg_group_mask_head[1]
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-346"></a>
### VG145: 组合逻辑完整依赖锥最多允许三个源信号，超限逻辑必须由时序 reg 隔断。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:122`
- Evidence:
- node_kind: `verilog_rtl`
- detail: wire_scalar_extended: 5 sources: reg_group_data_head[31:0], reg_group_data_head[63:32], reg_group_data_head[95:64], reg_group_mask_head[0], reg_group_mask_head[1]
- source_excerpt: `wire_scalar_extended: 5 sources: reg_group_data_head[31:0], reg_group_data_head[63:32], reg_group_data_head[95:64], reg_group_mask_head[0], reg_group_mask_head[1]`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
wire_scalar_extended: 5 sources: reg_group_data_head[31:0], reg_group_data_head[63:32], reg_group_data_head[95:64], reg_group_mask_head[0], reg_group_mask_head[1]
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-347"></a>
### VG145: 组合逻辑完整依赖锥最多允许三个源信号，超限逻辑必须由时序 reg 隔断。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:126`
- Evidence:
- node_kind: `verilog_rtl`
- detail: wire_scalar_tag: 5 sources: reg_group_channel_head, reg_group_layer_head, reg_group_mask_head[0], reg_group_mask_head[1], reg_group_position_head
- source_excerpt: `wire_scalar_tag: 5 sources: reg_group_channel_head, reg_group_layer_head, reg_group_mask_head[0], reg_group_mask_head[1], reg_group_position_head`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
wire_scalar_tag: 5 sources: reg_group_channel_head, reg_group_layer_head, reg_group_mask_head[0], reg_group_mask_head[1], reg_group_position_head
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-348"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=POST_SHIFT; child_output=road_postprocess_stream.POST_SHIFT; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=POST_SHIFT; child_output=road_postprocess_stream.POST_SHIFT; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=POST_SHIFT; child_output=road_postprocess_stream.POST_SHIFT; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-349"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=cnt_meta$D; child_output=road_postprocess_stream.cnt_meta$D; operation_count=1; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=cnt_meta$D; child_output=road_postprocess_stream.cnt_meta$D; operation_count=1; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=cnt_meta$D; child_output=road_postprocess_stream.cnt_meta$D; operation_count=1; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-350"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=cnt_meta$enable; child_output=road_postprocess_stream.cnt_meta$enable; operation_count=69; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=cnt_meta$enable; child_output=road_postprocess_stream.cnt_meta$enable; operation_count=69; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=cnt_meta$enable; child_output=road_postprocess_stream.cnt_meta$enable; operation_count=69; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-351"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=cnt_meta_read$D; child_output=road_postprocess_stream.cnt_meta_read$D; operation_count=1; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=cnt_meta_read$D; child_output=road_postprocess_stream.cnt_meta_read$D; operation_count=1; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=cnt_meta_read$D; child_output=road_postprocess_stream.cnt_meta_read$D; operation_count=1; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-352"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=cnt_meta_read$enable; child_output=road_postprocess_stream.cnt_meta_read$enable; operation_count=62; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=cnt_meta_read$enable; child_output=road_postprocess_stream.cnt_meta_read$enable; operation_count=62; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=cnt_meta_read$enable; child_output=road_postprocess_stream.cnt_meta_read$enable; operation_count=62; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-353"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=cnt_meta_write$enable; child_output=road_postprocess_stream.cnt_meta_write$enable; operation_count=58; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=cnt_meta_write$enable; child_output=road_postprocess_stream.cnt_meta_write$enable; operation_count=58; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=cnt_meta_write$enable; child_output=road_postprocess_stream.cnt_meta_write$enable; operation_count=58; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-354"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=cnt_post_inflight$enable; child_output=road_postprocess_stream.cnt_post_inflight$enable; operation_count=67; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=cnt_post_inflight$enable; child_output=road_postprocess_stream.cnt_post_inflight$enable; operation_count=67; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=cnt_post_inflight$enable; child_output=road_postprocess_stream.cnt_post_inflight$enable; operation_count=67; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-355"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=cnt_pre_inflight$enable; child_output=road_postprocess_stream.cnt_pre_inflight$enable; operation_count=67; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=cnt_pre_inflight$enable; child_output=road_postprocess_stream.cnt_pre_inflight$enable; operation_count=67; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=cnt_pre_inflight$enable; child_output=road_postprocess_stream.cnt_pre_inflight$enable; operation_count=67; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-356"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=cnt_result_queue$enable; child_output=road_postprocess_stream.cnt_result_queue$enable; operation_count=76; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=cnt_result_queue$enable; child_output=road_postprocess_stream.cnt_result_queue$enable; operation_count=76; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=cnt_result_queue$enable; child_output=road_postprocess_stream.cnt_result_queue$enable; operation_count=76; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-357"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_fatal$D; child_output=road_postprocess_stream.flag_fatal$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_fatal$D; child_output=road_postprocess_stream.flag_fatal$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_fatal$D; child_output=road_postprocess_stream.flag_fatal$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-358"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_fatal$enable; child_output=road_postprocess_stream.flag_fatal$enable; operation_count=51; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_fatal$enable; child_output=road_postprocess_stream.flag_fatal$enable; operation_count=51; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_fatal$enable; child_output=road_postprocess_stream.flag_fatal$enable; operation_count=51; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-359"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=post_result_data; child_output=road_postprocess_stream.post_result_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=post_result_data; child_output=road_postprocess_stream.post_result_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=post_result_data; child_output=road_postprocess_stream.post_result_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-360"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=post_result_fault; child_output=road_postprocess_stream.post_result_fault; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=post_result_fault; child_output=road_postprocess_stream.post_result_fault; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=post_result_fault; child_output=road_postprocess_stream.post_result_fault; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-361"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=post_result_tag; child_output=road_postprocess_stream.post_result_tag; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=post_result_tag; child_output=road_postprocess_stream.post_result_tag; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=post_result_tag; child_output=road_postprocess_stream.post_result_tag; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-362"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=post_result_valid; child_output=road_postprocess_stream.post_result_valid; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=post_result_valid; child_output=road_postprocess_stream.post_result_valid; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=post_result_valid; child_output=road_postprocess_stream.post_result_valid; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-363"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=pre_result_data; child_output=road_postprocess_stream.pre_result_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=pre_result_data; child_output=road_postprocess_stream.pre_result_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=pre_result_data; child_output=road_postprocess_stream.pre_result_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-364"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=pre_result_fault; child_output=road_postprocess_stream.pre_result_fault; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=pre_result_fault; child_output=road_postprocess_stream.pre_result_fault; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=pre_result_fault; child_output=road_postprocess_stream.pre_result_fault; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-365"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=pre_result_tag; child_output=road_postprocess_stream.pre_result_tag; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=pre_result_tag; child_output=road_postprocess_stream.pre_result_tag; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=pre_result_tag; child_output=road_postprocess_stream.pre_result_tag; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-366"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=pre_result_valid; child_output=road_postprocess_stream.pre_result_valid; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=pre_result_valid; child_output=road_postprocess_stream.pre_result_valid; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=pre_result_valid; child_output=road_postprocess_stream.pre_result_valid; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-367"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=reg_group_channel_head$enable; child_output=road_postprocess_stream.reg_group_channel_head$enable; operation_count=79; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=reg_group_channel_head$enable; child_output=road_postprocess_stream.reg_group_channel_head$enable; operation_count=79; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=reg_group_channel_head$enable; child_output=road_postprocess_stream.reg_group_channel_head$enable; operation_count=79; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-368"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=reg_group_channel_tail$enable; child_output=road_postprocess_stream.reg_group_channel_tail$enable; operation_count=78; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=reg_group_channel_tail$enable; child_output=road_postprocess_stream.reg_group_channel_tail$enable; operation_count=78; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=reg_group_channel_tail$enable; child_output=road_postprocess_stream.reg_group_channel_tail$enable; operation_count=78; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-369"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=reg_group_data_head$enable; child_output=road_postprocess_stream.reg_group_data_head$enable; operation_count=79; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=reg_group_data_head$enable; child_output=road_postprocess_stream.reg_group_data_head$enable; operation_count=79; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=reg_group_data_head$enable; child_output=road_postprocess_stream.reg_group_data_head$enable; operation_count=79; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-370"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=reg_group_data_tail$enable; child_output=road_postprocess_stream.reg_group_data_tail$enable; operation_count=78; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=reg_group_data_tail$enable; child_output=road_postprocess_stream.reg_group_data_tail$enable; operation_count=78; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=reg_group_data_tail$enable; child_output=road_postprocess_stream.reg_group_data_tail$enable; operation_count=78; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-371"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=reg_group_layer_head$enable; child_output=road_postprocess_stream.reg_group_layer_head$enable; operation_count=79; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=reg_group_layer_head$enable; child_output=road_postprocess_stream.reg_group_layer_head$enable; operation_count=79; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=reg_group_layer_head$enable; child_output=road_postprocess_stream.reg_group_layer_head$enable; operation_count=79; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-372"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=reg_group_layer_tail$enable; child_output=road_postprocess_stream.reg_group_layer_tail$enable; operation_count=78; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=reg_group_layer_tail$enable; child_output=road_postprocess_stream.reg_group_layer_tail$enable; operation_count=78; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=reg_group_layer_tail$enable; child_output=road_postprocess_stream.reg_group_layer_tail$enable; operation_count=78; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-373"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=reg_group_mask_head$D; child_output=road_postprocess_stream.reg_group_mask_head$D; operation_count=8; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=reg_group_mask_head$D; child_output=road_postprocess_stream.reg_group_mask_head$D; operation_count=8; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=reg_group_mask_head$D; child_output=road_postprocess_stream.reg_group_mask_head$D; operation_count=8; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-374"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=reg_group_mask_head$enable; child_output=road_postprocess_stream.reg_group_mask_head$enable; operation_count=79; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=reg_group_mask_head$enable; child_output=road_postprocess_stream.reg_group_mask_head$enable; operation_count=79; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=reg_group_mask_head$enable; child_output=road_postprocess_stream.reg_group_mask_head$enable; operation_count=79; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-375"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=reg_group_mask_tail$enable; child_output=road_postprocess_stream.reg_group_mask_tail$enable; operation_count=78; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=reg_group_mask_tail$enable; child_output=road_postprocess_stream.reg_group_mask_tail$enable; operation_count=78; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=reg_group_mask_tail$enable; child_output=road_postprocess_stream.reg_group_mask_tail$enable; operation_count=78; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-376"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=reg_group_position_head$enable; child_output=road_postprocess_stream.reg_group_position_head$enable; operation_count=79; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=reg_group_position_head$enable; child_output=road_postprocess_stream.reg_group_position_head$enable; operation_count=79; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=reg_group_position_head$enable; child_output=road_postprocess_stream.reg_group_position_head$enable; operation_count=79; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-377"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=reg_group_position_tail$enable; child_output=road_postprocess_stream.reg_group_position_tail$enable; operation_count=78; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=reg_group_position_tail$enable; child_output=road_postprocess_stream.reg_group_position_tail$enable; operation_count=78; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=reg_group_position_tail$enable; child_output=road_postprocess_stream.reg_group_position_tail$enable; operation_count=78; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-378"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=reg_meta_fifo; child_output=road_postprocess_stream.reg_meta_fifo; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=reg_meta_fifo; child_output=road_postprocess_stream.reg_meta_fifo; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=reg_meta_fifo; child_output=road_postprocess_stream.reg_meta_fifo; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-379"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=reg_meta_fifo[cnt_meta_write]$D; child_output=road_postprocess_stream.reg_meta_fifo[cnt_meta_write]$D; operation_count=0; limit=3; inconclusive_reason=reg_meta_fifo[cnt_meta_write]$D: missing storage data expression; loop_presence=absent
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=reg_meta_fifo[cnt_meta_write]$D; child_output=road_postprocess_stream.reg_meta_fifo[cnt_meta_write]$D; operation_count=0; limit=3; inconclusive_reason=reg_meta_fifo[cnt_meta_write]$D: missing storage data expression; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=reg_meta_fifo[cnt_meta_write]$D; child_output=road_postprocess_stream.reg_meta_fifo[cnt_meta_write]$D; operation_count=0; limit=3; inconclusive_reason=reg_meta_fifo[cnt_meta_write]$D: missing storage data expression; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-380"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=reg_meta_fifo[cnt_meta_write]$enable; child_output=road_postprocess_stream.reg_meta_fifo[cnt_meta_write]$enable; operation_count=58; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=reg_meta_fifo[cnt_meta_write]$enable; child_output=road_postprocess_stream.reg_meta_fifo[cnt_meta_write]$enable; operation_count=58; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=reg_meta_fifo[cnt_meta_write]$enable; child_output=road_postprocess_stream.reg_meta_fifo[cnt_meta_write]$enable; operation_count=58; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-381"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=silu_input_ready; child_output=road_postprocess_stream.silu_input_ready; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=silu_input_ready; child_output=road_postprocess_stream.silu_input_ready; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=silu_input_ready; child_output=road_postprocess_stream.silu_input_ready; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-382"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=silu_output_data; child_output=road_postprocess_stream.silu_output_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=silu_output_data; child_output=road_postprocess_stream.silu_output_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=silu_output_data; child_output=road_postprocess_stream.silu_output_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-383"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=silu_output_valid; child_output=road_postprocess_stream.silu_output_valid; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=silu_output_valid; child_output=road_postprocess_stream.silu_output_valid; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=silu_output_valid; child_output=road_postprocess_stream.silu_output_valid; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-384"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=silu_table_fault; child_output=road_postprocess_stream.silu_table_fault; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=silu_table_fault; child_output=road_postprocess_stream.silu_table_fault; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=silu_table_fault; child_output=road_postprocess_stream.silu_table_fault; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-385"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=silu_table_loaded; child_output=road_postprocess_stream.silu_table_loaded; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=silu_table_loaded; child_output=road_postprocess_stream.silu_table_loaded; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=silu_table_loaded; child_output=road_postprocess_stream.silu_table_loaded; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-386"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=silu_table_ready; child_output=road_postprocess_stream.silu_table_ready; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=silu_table_ready; child_output=road_postprocess_stream.silu_table_ready; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=silu_table_ready; child_output=road_postprocess_stream.silu_table_ready; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-387"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:115`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=wire_scalar_data; child_output=road_postprocess_stream.wire_scalar_data; operation_count=6; limit=3; inconclusive_reason=$signed: missing function definition; loop_presence=absent
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=wire_scalar_data; child_output=road_postprocess_stream.wire_scalar_data; operation_count=6; limit=3; inconclusive_reason=$signed: missing function definition; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=wire_scalar_data; child_output=road_postprocess_stream.wire_scalar_data; operation_count=6; limit=3; inconclusive_reason=$signed: missing function definition; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-388"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:118`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=wire_pre_factor; child_output=road_postprocess_stream.wire_pre_factor; operation_count=6; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=wire_pre_factor; child_output=road_postprocess_stream.wire_pre_factor; operation_count=6; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=wire_pre_factor; child_output=road_postprocess_stream.wire_pre_factor; operation_count=6; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-389"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:120`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=wire_pre_shift; child_output=road_postprocess_stream.wire_pre_shift; operation_count=6; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=wire_pre_shift; child_output=road_postprocess_stream.wire_pre_shift; operation_count=6; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=wire_pre_shift; child_output=road_postprocess_stream.wire_pre_shift; operation_count=6; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-390"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:122`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=wire_scalar_extended; child_output=road_postprocess_stream.wire_scalar_extended; operation_count=0; limit=3; inconclusive_reason=wire_scalar_extended: > ERR: [Python] expected '}', got '{'; loop_presence=absent
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=wire_scalar_extended; child_output=road_postprocess_stream.wire_scalar_extended; operation_count=0; limit=3; inconclusive_reason=wire_scalar_extended: > ERR: [Python] expected '}', got '{'; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=wire_scalar_extended; child_output=road_postprocess_stream.wire_scalar_extended; operation_count=0; limit=3; inconclusive_reason=wire_scalar_extended: > ERR: [Python] expected '}', got '{'; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-391"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:123`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=wire_factor_extended; child_output=road_postprocess_stream.wire_factor_extended; operation_count=0; limit=3; inconclusive_reason=wire_factor_extended: > ERR: [Python] expected '}', got '{'; loop_presence=absent
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=wire_factor_extended; child_output=road_postprocess_stream.wire_factor_extended; operation_count=0; limit=3; inconclusive_reason=wire_factor_extended: > ERR: [Python] expected '}', got '{'; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=wire_factor_extended; child_output=road_postprocess_stream.wire_factor_extended; operation_count=0; limit=3; inconclusive_reason=wire_factor_extended: > ERR: [Python] expected '}', got '{'; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-392"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:124`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=wire_pre_product; child_output=road_postprocess_stream.wire_pre_product; operation_count=1; limit=3; inconclusive_reason=$signed: missing function definition | missing module implementation | wire_factor_extended: > ERR: [Python] expected '}', got '{' | wire_scalar_extended: > ERR: [Python] expected '}', got '{'; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=wire_pre_product; child_output=road_postprocess_stream.wire_pre_product; operation_count=1; limit=3; inconclusive_reason=$signed: missing function definition | missing module implementation | wire_factor_extended: > ERR: [Python] expected '}', got '{' | wire_scalar_extended: > ERR: [Python] expected '}', got '{'; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=wire_pre_product; child_output=road_postprocess_stream.wire_pre_product; operation_count=1; limit=3; inconclusive_reason=$signed: missing function definition | missing module implementation | wire_factor_extended: > ERR: [Python] expected '}', got '{' | wire_scalar_extended: > ERR: [Python] expected '}', got '{'; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-393"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:126`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=wire_scalar_tag; child_output=road_postprocess_stream.wire_scalar_tag; operation_count=3; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=wire_scalar_tag; child_output=road_postprocess_stream.wire_scalar_tag; operation_count=3; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=wire_scalar_tag; child_output=road_postprocess_stream.wire_scalar_tag; operation_count=3; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-394"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:127`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_scalar_valid; child_output=road_postprocess_stream.flag_scalar_valid; operation_count=6; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_scalar_valid; child_output=road_postprocess_stream.flag_scalar_valid; operation_count=6; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_scalar_valid; child_output=road_postprocess_stream.flag_scalar_valid; operation_count=6; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-395"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:129`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_scalar_last; child_output=road_postprocess_stream.flag_scalar_last; operation_count=4; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_scalar_last; child_output=road_postprocess_stream.flag_scalar_last; operation_count=4; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_scalar_last; child_output=road_postprocess_stream.flag_scalar_last; operation_count=4; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-396"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:131`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_base_aligned; child_output=road_postprocess_stream.flag_base_aligned; operation_count=15; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_base_aligned; child_output=road_postprocess_stream.flag_base_aligned; operation_count=15; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_base_aligned; child_output=road_postprocess_stream.flag_base_aligned; operation_count=15; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-397"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:135`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_lane_shape_valid; child_output=road_postprocess_stream.flag_lane_shape_valid; operation_count=7; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_lane_shape_valid; child_output=road_postprocess_stream.flag_lane_shape_valid; operation_count=7; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_lane_shape_valid; child_output=road_postprocess_stream.flag_lane_shape_valid; operation_count=7; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-398"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:138`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_input_shape_fault; child_output=road_postprocess_stream.flag_input_shape_fault; operation_count=35; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_input_shape_fault; child_output=road_postprocess_stream.flag_input_shape_fault; operation_count=35; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_input_shape_fault; child_output=road_postprocess_stream.flag_input_shape_fault; operation_count=35; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-399"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:141`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=o_input_ready; child_output=road_postprocess_stream.o_input_ready; operation_count=8; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=o_input_ready; child_output=road_postprocess_stream.o_input_ready; operation_count=8; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=o_input_ready; child_output=road_postprocess_stream.o_input_ready; operation_count=8; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-400"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:143`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_input_accept; child_output=road_postprocess_stream.flag_input_accept; operation_count=9; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_input_accept; child_output=road_postprocess_stream.flag_input_accept; operation_count=9; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_input_accept; child_output=road_postprocess_stream.flag_input_accept; operation_count=9; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-401"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:144`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_group_push; child_output=road_postprocess_stream.flag_group_push; operation_count=48; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_group_push; child_output=road_postprocess_stream.flag_group_push; operation_count=48; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_group_push; child_output=road_postprocess_stream.flag_group_push; operation_count=48; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-402"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:145`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_group_pop; child_output=road_postprocess_stream.flag_group_pop; operation_count=21; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_group_pop; child_output=road_postprocess_stream.flag_group_pop; operation_count=21; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_group_pop; child_output=road_postprocess_stream.flag_group_pop; operation_count=21; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-403"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:147`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_silu_accept; child_output=road_postprocess_stream.flag_silu_accept; operation_count=7; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_silu_accept; child_output=road_postprocess_stream.flag_silu_accept; operation_count=7; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_silu_accept; child_output=road_postprocess_stream.flag_silu_accept; operation_count=7; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-404"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:149`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_pre_advance; child_output=road_postprocess_stream.flag_pre_advance; operation_count=9; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_pre_advance; child_output=road_postprocess_stream.flag_pre_advance; operation_count=9; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_pre_advance; child_output=road_postprocess_stream.flag_pre_advance; operation_count=9; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-405"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:150`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_pre_accept; child_output=road_postprocess_stream.flag_pre_accept; operation_count=16; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_pre_accept; child_output=road_postprocess_stream.flag_pre_accept; operation_count=16; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_pre_accept; child_output=road_postprocess_stream.flag_pre_accept; operation_count=16; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-406"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:152`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_post_advance; child_output=road_postprocess_stream.flag_post_advance; operation_count=6; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_post_advance; child_output=road_postprocess_stream.flag_post_advance; operation_count=6; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_post_advance; child_output=road_postprocess_stream.flag_post_advance; operation_count=6; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-407"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:154`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_silu_output_ready; child_output=road_postprocess_stream.flag_silu_output_ready; operation_count=10; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_silu_output_ready; child_output=road_postprocess_stream.flag_silu_output_ready; operation_count=10; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_silu_output_ready; child_output=road_postprocess_stream.flag_silu_output_ready; operation_count=10; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-408"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:155`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_post_accept; child_output=road_postprocess_stream.flag_post_accept; operation_count=11; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_post_accept; child_output=road_postprocess_stream.flag_post_accept; operation_count=11; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_post_accept; child_output=road_postprocess_stream.flag_post_accept; operation_count=11; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-409"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:156`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_output_accept; child_output=road_postprocess_stream.flag_output_accept; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_output_accept; child_output=road_postprocess_stream.flag_output_accept; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_output_accept; child_output=road_postprocess_stream.flag_output_accept; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-410"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:157`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=wire_post_product; child_output=road_postprocess_stream.wire_post_product; operation_count=1; limit=3; inconclusive_reason=$signed: missing function definition | missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=wire_post_product; child_output=road_postprocess_stream.wire_post_product; operation_count=1; limit=3; inconclusive_reason=$signed: missing function definition | missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=wire_post_product; child_output=road_postprocess_stream.wire_post_product; operation_count=1; limit=3; inconclusive_reason=$signed: missing function definition | missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-411"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:158`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=wire_output_saturated; child_output=road_postprocess_stream.wire_output_saturated; operation_count=6; limit=3; inconclusive_reason=$signed: missing function definition | missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=wire_output_saturated; child_output=road_postprocess_stream.wire_output_saturated; operation_count=6; limit=3; inconclusive_reason=$signed: missing function definition | missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=wire_output_saturated; child_output=road_postprocess_stream.wire_output_saturated; operation_count=6; limit=3; inconclusive_reason=$signed: missing function definition | missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-412"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:161`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_fault_event; child_output=road_postprocess_stream.flag_fault_event; operation_count=51; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_fault_event; child_output=road_postprocess_stream.flag_fault_event; operation_count=51; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_fault_event; child_output=road_postprocess_stream.flag_fault_event; operation_count=51; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-413"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:164`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_pipeline_empty; child_output=road_postprocess_stream.flag_pipeline_empty; operation_count=7; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_pipeline_empty; child_output=road_postprocess_stream.flag_pipeline_empty; operation_count=7; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_pipeline_empty; child_output=road_postprocess_stream.flag_pipeline_empty; operation_count=7; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-414"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:166`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_table_forward; child_output=road_postprocess_stream.flag_table_forward; operation_count=10; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_table_forward; child_output=road_postprocess_stream.flag_table_forward; operation_count=10; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_table_forward; child_output=road_postprocess_stream.flag_table_forward; operation_count=10; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-415"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:168`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=o_table_ready; child_output=road_postprocess_stream.o_table_ready; operation_count=10; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=o_table_ready; child_output=road_postprocess_stream.o_table_ready; operation_count=10; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=o_table_ready; child_output=road_postprocess_stream.o_table_ready; operation_count=10; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-416"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:169`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=o_table_loaded; child_output=road_postprocess_stream.o_table_loaded; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=o_table_loaded; child_output=road_postprocess_stream.o_table_loaded; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=o_table_loaded; child_output=road_postprocess_stream.o_table_loaded; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-417"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:170`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=o_table_fault; child_output=road_postprocess_stream.o_table_fault; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=o_table_fault; child_output=road_postprocess_stream.o_table_fault; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=o_table_fault; child_output=road_postprocess_stream.o_table_fault; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-418"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:171`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=o_output_valid; child_output=road_postprocess_stream.o_output_valid; operation_count=4; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=o_output_valid; child_output=road_postprocess_stream.o_output_valid; operation_count=4; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=o_output_valid; child_output=road_postprocess_stream.o_output_valid; operation_count=4; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-419"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:172`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=o_output_data; child_output=road_postprocess_stream.o_output_data; operation_count=6; limit=3; inconclusive_reason=$signed: missing function definition | missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=o_output_data; child_output=road_postprocess_stream.o_output_data; operation_count=6; limit=3; inconclusive_reason=$signed: missing function definition | missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=o_output_data; child_output=road_postprocess_stream.o_output_data; operation_count=6; limit=3; inconclusive_reason=$signed: missing function definition | missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-420"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:173`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=o_output_tag; child_output=road_postprocess_stream.o_output_tag; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=o_output_tag; child_output=road_postprocess_stream.o_output_tag; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=o_output_tag; child_output=road_postprocess_stream.o_output_tag; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-421"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:174`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=o_fault; child_output=road_postprocess_stream.o_fault; operation_count=1; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=o_fault; child_output=road_postprocess_stream.o_fault; operation_count=1; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=o_fault; child_output=road_postprocess_stream.o_fault; operation_count=1; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-422"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:176`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=o_meta_count; child_output=road_postprocess_stream.o_meta_count; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=o_meta_count; child_output=road_postprocess_stream.o_meta_count; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=o_meta_count; child_output=road_postprocess_stream.o_meta_count; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-423"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:178`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=o_silu_busy; child_output=road_postprocess_stream.o_silu_busy; operation_count=1; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=o_silu_busy; child_output=road_postprocess_stream.o_silu_busy; operation_count=1; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=o_silu_busy; child_output=road_postprocess_stream.o_silu_busy; operation_count=1; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-424"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:180`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=o_pre_accept; child_output=road_postprocess_stream.o_pre_accept; operation_count=16; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=o_pre_accept; child_output=road_postprocess_stream.o_pre_accept; operation_count=16; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=o_pre_accept; child_output=road_postprocess_stream.o_pre_accept; operation_count=16; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-425"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:181`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=o_silu_accept; child_output=road_postprocess_stream.o_silu_accept; operation_count=7; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=o_silu_accept; child_output=road_postprocess_stream.o_silu_accept; operation_count=7; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=o_silu_accept; child_output=road_postprocess_stream.o_silu_accept; operation_count=7; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-426"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:182`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=o_post_accept; child_output=road_postprocess_stream.o_post_accept; operation_count=11; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=o_post_accept; child_output=road_postprocess_stream.o_post_accept; operation_count=11; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=o_post_accept; child_output=road_postprocess_stream.o_post_accept; operation_count=11; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-427"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:264`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=cnt_meta_read; child_output=road_postprocess_stream.cnt_meta_read; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=cnt_meta_read; child_output=road_postprocess_stream.cnt_meta_read; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=cnt_meta_read; child_output=road_postprocess_stream.cnt_meta_read; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-428"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:266`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=cnt_meta; child_output=road_postprocess_stream.cnt_meta; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=cnt_meta; child_output=road_postprocess_stream.cnt_meta; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=cnt_meta; child_output=road_postprocess_stream.cnt_meta; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-429"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:291`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_fatal; child_output=road_postprocess_stream.flag_fatal; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_fatal; child_output=road_postprocess_stream.flag_fatal; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_fatal; child_output=road_postprocess_stream.flag_fatal; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-430"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=POST_SHIFT; child_output=road_postprocess_stream.POST_SHIFT; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=POST_SHIFT; child_output=road_postprocess_stream.POST_SHIFT; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=POST_SHIFT; child_output=road_postprocess_stream.POST_SHIFT; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-431"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=cnt_meta$D; child_output=road_postprocess_stream.cnt_meta$D; operation_count=1; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=cnt_meta$D; child_output=road_postprocess_stream.cnt_meta$D; operation_count=1; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=cnt_meta$D; child_output=road_postprocess_stream.cnt_meta$D; operation_count=1; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-432"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=cnt_meta$enable; child_output=road_postprocess_stream.cnt_meta$enable; operation_count=69; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=cnt_meta$enable; child_output=road_postprocess_stream.cnt_meta$enable; operation_count=69; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=cnt_meta$enable; child_output=road_postprocess_stream.cnt_meta$enable; operation_count=69; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-433"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=cnt_meta_read$D; child_output=road_postprocess_stream.cnt_meta_read$D; operation_count=1; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=cnt_meta_read$D; child_output=road_postprocess_stream.cnt_meta_read$D; operation_count=1; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=cnt_meta_read$D; child_output=road_postprocess_stream.cnt_meta_read$D; operation_count=1; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-434"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=cnt_meta_read$enable; child_output=road_postprocess_stream.cnt_meta_read$enable; operation_count=62; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=cnt_meta_read$enable; child_output=road_postprocess_stream.cnt_meta_read$enable; operation_count=62; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=cnt_meta_read$enable; child_output=road_postprocess_stream.cnt_meta_read$enable; operation_count=62; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-435"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=cnt_meta_write$enable; child_output=road_postprocess_stream.cnt_meta_write$enable; operation_count=58; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=cnt_meta_write$enable; child_output=road_postprocess_stream.cnt_meta_write$enable; operation_count=58; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=cnt_meta_write$enable; child_output=road_postprocess_stream.cnt_meta_write$enable; operation_count=58; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-436"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=cnt_post_inflight$enable; child_output=road_postprocess_stream.cnt_post_inflight$enable; operation_count=67; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=cnt_post_inflight$enable; child_output=road_postprocess_stream.cnt_post_inflight$enable; operation_count=67; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=cnt_post_inflight$enable; child_output=road_postprocess_stream.cnt_post_inflight$enable; operation_count=67; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-437"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=cnt_pre_inflight$enable; child_output=road_postprocess_stream.cnt_pre_inflight$enable; operation_count=67; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=cnt_pre_inflight$enable; child_output=road_postprocess_stream.cnt_pre_inflight$enable; operation_count=67; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=cnt_pre_inflight$enable; child_output=road_postprocess_stream.cnt_pre_inflight$enable; operation_count=67; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-438"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=cnt_result_queue$enable; child_output=road_postprocess_stream.cnt_result_queue$enable; operation_count=76; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=cnt_result_queue$enable; child_output=road_postprocess_stream.cnt_result_queue$enable; operation_count=76; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=cnt_result_queue$enable; child_output=road_postprocess_stream.cnt_result_queue$enable; operation_count=76; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-439"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_fatal$D; child_output=road_postprocess_stream.flag_fatal$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_fatal$D; child_output=road_postprocess_stream.flag_fatal$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_fatal$D; child_output=road_postprocess_stream.flag_fatal$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-440"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_fatal$enable; child_output=road_postprocess_stream.flag_fatal$enable; operation_count=51; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_fatal$enable; child_output=road_postprocess_stream.flag_fatal$enable; operation_count=51; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_fatal$enable; child_output=road_postprocess_stream.flag_fatal$enable; operation_count=51; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-441"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=post_result_data; child_output=road_postprocess_stream.post_result_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=post_result_data; child_output=road_postprocess_stream.post_result_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=post_result_data; child_output=road_postprocess_stream.post_result_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-442"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=post_result_fault; child_output=road_postprocess_stream.post_result_fault; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=post_result_fault; child_output=road_postprocess_stream.post_result_fault; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=post_result_fault; child_output=road_postprocess_stream.post_result_fault; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-443"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=post_result_tag; child_output=road_postprocess_stream.post_result_tag; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=post_result_tag; child_output=road_postprocess_stream.post_result_tag; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=post_result_tag; child_output=road_postprocess_stream.post_result_tag; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-444"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=post_result_valid; child_output=road_postprocess_stream.post_result_valid; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=post_result_valid; child_output=road_postprocess_stream.post_result_valid; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=post_result_valid; child_output=road_postprocess_stream.post_result_valid; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-445"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=pre_result_data; child_output=road_postprocess_stream.pre_result_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=pre_result_data; child_output=road_postprocess_stream.pre_result_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=pre_result_data; child_output=road_postprocess_stream.pre_result_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-446"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=pre_result_fault; child_output=road_postprocess_stream.pre_result_fault; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=pre_result_fault; child_output=road_postprocess_stream.pre_result_fault; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=pre_result_fault; child_output=road_postprocess_stream.pre_result_fault; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-447"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=pre_result_tag; child_output=road_postprocess_stream.pre_result_tag; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=pre_result_tag; child_output=road_postprocess_stream.pre_result_tag; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=pre_result_tag; child_output=road_postprocess_stream.pre_result_tag; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-448"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=pre_result_valid; child_output=road_postprocess_stream.pre_result_valid; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=pre_result_valid; child_output=road_postprocess_stream.pre_result_valid; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=pre_result_valid; child_output=road_postprocess_stream.pre_result_valid; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-449"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=reg_group_channel_head$enable; child_output=road_postprocess_stream.reg_group_channel_head$enable; operation_count=79; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=reg_group_channel_head$enable; child_output=road_postprocess_stream.reg_group_channel_head$enable; operation_count=79; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=reg_group_channel_head$enable; child_output=road_postprocess_stream.reg_group_channel_head$enable; operation_count=79; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-450"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=reg_group_channel_tail$enable; child_output=road_postprocess_stream.reg_group_channel_tail$enable; operation_count=78; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=reg_group_channel_tail$enable; child_output=road_postprocess_stream.reg_group_channel_tail$enable; operation_count=78; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=reg_group_channel_tail$enable; child_output=road_postprocess_stream.reg_group_channel_tail$enable; operation_count=78; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-451"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=reg_group_data_head$enable; child_output=road_postprocess_stream.reg_group_data_head$enable; operation_count=79; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=reg_group_data_head$enable; child_output=road_postprocess_stream.reg_group_data_head$enable; operation_count=79; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=reg_group_data_head$enable; child_output=road_postprocess_stream.reg_group_data_head$enable; operation_count=79; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-452"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=reg_group_data_tail$enable; child_output=road_postprocess_stream.reg_group_data_tail$enable; operation_count=78; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=reg_group_data_tail$enable; child_output=road_postprocess_stream.reg_group_data_tail$enable; operation_count=78; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=reg_group_data_tail$enable; child_output=road_postprocess_stream.reg_group_data_tail$enable; operation_count=78; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-453"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=reg_group_layer_head$enable; child_output=road_postprocess_stream.reg_group_layer_head$enable; operation_count=79; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=reg_group_layer_head$enable; child_output=road_postprocess_stream.reg_group_layer_head$enable; operation_count=79; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=reg_group_layer_head$enable; child_output=road_postprocess_stream.reg_group_layer_head$enable; operation_count=79; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-454"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=reg_group_layer_tail$enable; child_output=road_postprocess_stream.reg_group_layer_tail$enable; operation_count=78; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=reg_group_layer_tail$enable; child_output=road_postprocess_stream.reg_group_layer_tail$enable; operation_count=78; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=reg_group_layer_tail$enable; child_output=road_postprocess_stream.reg_group_layer_tail$enable; operation_count=78; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-455"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=reg_group_mask_head$enable; child_output=road_postprocess_stream.reg_group_mask_head$enable; operation_count=79; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=reg_group_mask_head$enable; child_output=road_postprocess_stream.reg_group_mask_head$enable; operation_count=79; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=reg_group_mask_head$enable; child_output=road_postprocess_stream.reg_group_mask_head$enable; operation_count=79; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-456"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=reg_group_mask_tail$enable; child_output=road_postprocess_stream.reg_group_mask_tail$enable; operation_count=78; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=reg_group_mask_tail$enable; child_output=road_postprocess_stream.reg_group_mask_tail$enable; operation_count=78; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=reg_group_mask_tail$enable; child_output=road_postprocess_stream.reg_group_mask_tail$enable; operation_count=78; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-457"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=reg_group_position_head$enable; child_output=road_postprocess_stream.reg_group_position_head$enable; operation_count=79; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=reg_group_position_head$enable; child_output=road_postprocess_stream.reg_group_position_head$enable; operation_count=79; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=reg_group_position_head$enable; child_output=road_postprocess_stream.reg_group_position_head$enable; operation_count=79; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-458"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=reg_group_position_tail$enable; child_output=road_postprocess_stream.reg_group_position_tail$enable; operation_count=78; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=reg_group_position_tail$enable; child_output=road_postprocess_stream.reg_group_position_tail$enable; operation_count=78; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=reg_group_position_tail$enable; child_output=road_postprocess_stream.reg_group_position_tail$enable; operation_count=78; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-459"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=reg_meta_fifo; child_output=road_postprocess_stream.reg_meta_fifo; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=reg_meta_fifo; child_output=road_postprocess_stream.reg_meta_fifo; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=reg_meta_fifo; child_output=road_postprocess_stream.reg_meta_fifo; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-460"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=reg_meta_fifo[cnt_meta_write]$enable; child_output=road_postprocess_stream.reg_meta_fifo[cnt_meta_write]$enable; operation_count=58; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=reg_meta_fifo[cnt_meta_write]$enable; child_output=road_postprocess_stream.reg_meta_fifo[cnt_meta_write]$enable; operation_count=58; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=reg_meta_fifo[cnt_meta_write]$enable; child_output=road_postprocess_stream.reg_meta_fifo[cnt_meta_write]$enable; operation_count=58; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-461"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=silu_input_ready; child_output=road_postprocess_stream.silu_input_ready; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=silu_input_ready; child_output=road_postprocess_stream.silu_input_ready; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=silu_input_ready; child_output=road_postprocess_stream.silu_input_ready; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-462"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=silu_output_data; child_output=road_postprocess_stream.silu_output_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=silu_output_data; child_output=road_postprocess_stream.silu_output_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=silu_output_data; child_output=road_postprocess_stream.silu_output_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-463"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=silu_output_valid; child_output=road_postprocess_stream.silu_output_valid; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=silu_output_valid; child_output=road_postprocess_stream.silu_output_valid; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=silu_output_valid; child_output=road_postprocess_stream.silu_output_valid; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-464"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=silu_table_fault; child_output=road_postprocess_stream.silu_table_fault; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=silu_table_fault; child_output=road_postprocess_stream.silu_table_fault; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=silu_table_fault; child_output=road_postprocess_stream.silu_table_fault; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-465"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=silu_table_loaded; child_output=road_postprocess_stream.silu_table_loaded; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=silu_table_loaded; child_output=road_postprocess_stream.silu_table_loaded; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=silu_table_loaded; child_output=road_postprocess_stream.silu_table_loaded; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-466"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=silu_table_ready; child_output=road_postprocess_stream.silu_table_ready; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=silu_table_ready; child_output=road_postprocess_stream.silu_table_ready; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=silu_table_ready; child_output=road_postprocess_stream.silu_table_ready; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-467"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:120`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=wire_pre_shift; child_output=road_postprocess_stream.wire_pre_shift; operation_count=6; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=wire_pre_shift; child_output=road_postprocess_stream.wire_pre_shift; operation_count=6; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=wire_pre_shift; child_output=road_postprocess_stream.wire_pre_shift; operation_count=6; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-468"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:124`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=wire_pre_product; child_output=road_postprocess_stream.wire_pre_product; operation_count=1; limit=3; inconclusive_reason=$signed: missing function definition | missing module implementation | wire_factor_extended: > ERR: [Python] expected '}', got '{' | wire_scalar_extended: > ERR: [Python] expected '}', got '{'; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=wire_pre_product; child_output=road_postprocess_stream.wire_pre_product; operation_count=1; limit=3; inconclusive_reason=$signed: missing function definition | missing module implementation | wire_factor_extended: > ERR: [Python] expected '}', got '{' | wire_scalar_extended: > ERR: [Python] expected '}', got '{'; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=wire_pre_product; child_output=road_postprocess_stream.wire_pre_product; operation_count=1; limit=3; inconclusive_reason=$signed: missing function definition | missing module implementation | wire_factor_extended: > ERR: [Python] expected '}', got '{' | wire_scalar_extended: > ERR: [Python] expected '}', got '{'; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-469"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:126`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=wire_scalar_tag; child_output=road_postprocess_stream.wire_scalar_tag; operation_count=3; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=wire_scalar_tag; child_output=road_postprocess_stream.wire_scalar_tag; operation_count=3; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=wire_scalar_tag; child_output=road_postprocess_stream.wire_scalar_tag; operation_count=3; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-470"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:127`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_scalar_valid; child_output=road_postprocess_stream.flag_scalar_valid; operation_count=6; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_scalar_valid; child_output=road_postprocess_stream.flag_scalar_valid; operation_count=6; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_scalar_valid; child_output=road_postprocess_stream.flag_scalar_valid; operation_count=6; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-471"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:141`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=o_input_ready; child_output=road_postprocess_stream.o_input_ready; operation_count=8; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=o_input_ready; child_output=road_postprocess_stream.o_input_ready; operation_count=8; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=o_input_ready; child_output=road_postprocess_stream.o_input_ready; operation_count=8; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-472"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:143`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_input_accept; child_output=road_postprocess_stream.flag_input_accept; operation_count=9; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_input_accept; child_output=road_postprocess_stream.flag_input_accept; operation_count=9; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_input_accept; child_output=road_postprocess_stream.flag_input_accept; operation_count=9; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-473"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:144`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_group_push; child_output=road_postprocess_stream.flag_group_push; operation_count=48; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_group_push; child_output=road_postprocess_stream.flag_group_push; operation_count=48; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_group_push; child_output=road_postprocess_stream.flag_group_push; operation_count=48; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-474"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:145`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_group_pop; child_output=road_postprocess_stream.flag_group_pop; operation_count=21; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_group_pop; child_output=road_postprocess_stream.flag_group_pop; operation_count=21; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_group_pop; child_output=road_postprocess_stream.flag_group_pop; operation_count=21; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-475"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:147`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_silu_accept; child_output=road_postprocess_stream.flag_silu_accept; operation_count=7; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_silu_accept; child_output=road_postprocess_stream.flag_silu_accept; operation_count=7; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_silu_accept; child_output=road_postprocess_stream.flag_silu_accept; operation_count=7; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-476"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:149`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_pre_advance; child_output=road_postprocess_stream.flag_pre_advance; operation_count=9; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_pre_advance; child_output=road_postprocess_stream.flag_pre_advance; operation_count=9; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_pre_advance; child_output=road_postprocess_stream.flag_pre_advance; operation_count=9; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-477"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:150`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_pre_accept; child_output=road_postprocess_stream.flag_pre_accept; operation_count=16; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_pre_accept; child_output=road_postprocess_stream.flag_pre_accept; operation_count=16; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_pre_accept; child_output=road_postprocess_stream.flag_pre_accept; operation_count=16; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-478"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:152`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_post_advance; child_output=road_postprocess_stream.flag_post_advance; operation_count=6; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_post_advance; child_output=road_postprocess_stream.flag_post_advance; operation_count=6; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_post_advance; child_output=road_postprocess_stream.flag_post_advance; operation_count=6; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-479"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:154`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_silu_output_ready; child_output=road_postprocess_stream.flag_silu_output_ready; operation_count=10; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_silu_output_ready; child_output=road_postprocess_stream.flag_silu_output_ready; operation_count=10; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_silu_output_ready; child_output=road_postprocess_stream.flag_silu_output_ready; operation_count=10; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-480"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:155`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_post_accept; child_output=road_postprocess_stream.flag_post_accept; operation_count=11; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_post_accept; child_output=road_postprocess_stream.flag_post_accept; operation_count=11; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_post_accept; child_output=road_postprocess_stream.flag_post_accept; operation_count=11; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-481"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:156`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_output_accept; child_output=road_postprocess_stream.flag_output_accept; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_output_accept; child_output=road_postprocess_stream.flag_output_accept; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_output_accept; child_output=road_postprocess_stream.flag_output_accept; operation_count=5; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-482"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:157`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=wire_post_product; child_output=road_postprocess_stream.wire_post_product; operation_count=1; limit=3; inconclusive_reason=$signed: missing function definition | missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=wire_post_product; child_output=road_postprocess_stream.wire_post_product; operation_count=1; limit=3; inconclusive_reason=$signed: missing function definition | missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=wire_post_product; child_output=road_postprocess_stream.wire_post_product; operation_count=1; limit=3; inconclusive_reason=$signed: missing function definition | missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-483"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:158`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=wire_output_saturated; child_output=road_postprocess_stream.wire_output_saturated; operation_count=6; limit=3; inconclusive_reason=$signed: missing function definition | missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=wire_output_saturated; child_output=road_postprocess_stream.wire_output_saturated; operation_count=6; limit=3; inconclusive_reason=$signed: missing function definition | missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=wire_output_saturated; child_output=road_postprocess_stream.wire_output_saturated; operation_count=6; limit=3; inconclusive_reason=$signed: missing function definition | missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-484"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:161`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_fault_event; child_output=road_postprocess_stream.flag_fault_event; operation_count=51; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_fault_event; child_output=road_postprocess_stream.flag_fault_event; operation_count=51; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_fault_event; child_output=road_postprocess_stream.flag_fault_event; operation_count=51; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-485"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:164`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_pipeline_empty; child_output=road_postprocess_stream.flag_pipeline_empty; operation_count=7; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_pipeline_empty; child_output=road_postprocess_stream.flag_pipeline_empty; operation_count=7; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_pipeline_empty; child_output=road_postprocess_stream.flag_pipeline_empty; operation_count=7; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-486"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:166`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_table_forward; child_output=road_postprocess_stream.flag_table_forward; operation_count=10; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_table_forward; child_output=road_postprocess_stream.flag_table_forward; operation_count=10; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_table_forward; child_output=road_postprocess_stream.flag_table_forward; operation_count=10; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-487"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:168`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=o_table_ready; child_output=road_postprocess_stream.o_table_ready; operation_count=10; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=o_table_ready; child_output=road_postprocess_stream.o_table_ready; operation_count=10; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=o_table_ready; child_output=road_postprocess_stream.o_table_ready; operation_count=10; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-488"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:169`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=o_table_loaded; child_output=road_postprocess_stream.o_table_loaded; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=o_table_loaded; child_output=road_postprocess_stream.o_table_loaded; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=o_table_loaded; child_output=road_postprocess_stream.o_table_loaded; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-489"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:170`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=o_table_fault; child_output=road_postprocess_stream.o_table_fault; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=o_table_fault; child_output=road_postprocess_stream.o_table_fault; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=o_table_fault; child_output=road_postprocess_stream.o_table_fault; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-490"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:171`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=o_output_valid; child_output=road_postprocess_stream.o_output_valid; operation_count=4; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=o_output_valid; child_output=road_postprocess_stream.o_output_valid; operation_count=4; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=o_output_valid; child_output=road_postprocess_stream.o_output_valid; operation_count=4; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-491"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:172`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=o_output_data; child_output=road_postprocess_stream.o_output_data; operation_count=6; limit=3; inconclusive_reason=$signed: missing function definition | missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=o_output_data; child_output=road_postprocess_stream.o_output_data; operation_count=6; limit=3; inconclusive_reason=$signed: missing function definition | missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=o_output_data; child_output=road_postprocess_stream.o_output_data; operation_count=6; limit=3; inconclusive_reason=$signed: missing function definition | missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-492"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:173`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=o_output_tag; child_output=road_postprocess_stream.o_output_tag; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=o_output_tag; child_output=road_postprocess_stream.o_output_tag; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=o_output_tag; child_output=road_postprocess_stream.o_output_tag; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-493"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:174`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=o_fault; child_output=road_postprocess_stream.o_fault; operation_count=1; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=o_fault; child_output=road_postprocess_stream.o_fault; operation_count=1; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=o_fault; child_output=road_postprocess_stream.o_fault; operation_count=1; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-494"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:176`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=o_meta_count; child_output=road_postprocess_stream.o_meta_count; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=o_meta_count; child_output=road_postprocess_stream.o_meta_count; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=o_meta_count; child_output=road_postprocess_stream.o_meta_count; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-495"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:178`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=o_silu_busy; child_output=road_postprocess_stream.o_silu_busy; operation_count=1; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=o_silu_busy; child_output=road_postprocess_stream.o_silu_busy; operation_count=1; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=o_silu_busy; child_output=road_postprocess_stream.o_silu_busy; operation_count=1; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-496"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:180`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=o_pre_accept; child_output=road_postprocess_stream.o_pre_accept; operation_count=16; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=o_pre_accept; child_output=road_postprocess_stream.o_pre_accept; operation_count=16; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=o_pre_accept; child_output=road_postprocess_stream.o_pre_accept; operation_count=16; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-497"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:181`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=o_silu_accept; child_output=road_postprocess_stream.o_silu_accept; operation_count=7; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=o_silu_accept; child_output=road_postprocess_stream.o_silu_accept; operation_count=7; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=o_silu_accept; child_output=road_postprocess_stream.o_silu_accept; operation_count=7; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-498"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:182`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=o_post_accept; child_output=road_postprocess_stream.o_post_accept; operation_count=11; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=o_post_accept; child_output=road_postprocess_stream.o_post_accept; operation_count=11; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=o_post_accept; child_output=road_postprocess_stream.o_post_accept; operation_count=11; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-499"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:264`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=cnt_meta_read; child_output=road_postprocess_stream.cnt_meta_read; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=cnt_meta_read; child_output=road_postprocess_stream.cnt_meta_read; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=cnt_meta_read; child_output=road_postprocess_stream.cnt_meta_read; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-500"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:266`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=cnt_meta; child_output=road_postprocess_stream.cnt_meta; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=cnt_meta; child_output=road_postprocess_stream.cnt_meta; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=cnt_meta; child_output=road_postprocess_stream.cnt_meta; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-501"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:291`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_fatal; child_output=road_postprocess_stream.flag_fatal; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_fatal; child_output=road_postprocess_stream.flag_fatal; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_postprocess_stream.v:road_postprocess_stream@4:1-358:1; instance_path=road_postprocess_stream; specialization=416269521ae6c138d678ea58e7c159836aef401b59061e5224fa778cf6388047; target=flag_fatal; child_output=road_postprocess_stream.flag_fatal; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-502"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:58`
- Evidence:
- node_kind: `verilog_rtl`
- detail: reg_meta_fifo
- source_excerpt: `reg_meta_fifo`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
reg_meta_fifo
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-503"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:87`
- Evidence:
- node_kind: `verilog_rtl`
- detail: pre_result_valid
- source_excerpt: `pre_result_valid`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
pre_result_valid
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-504"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:88`
- Evidence:
- node_kind: `verilog_rtl`
- detail: pre_result_data
- source_excerpt: `pre_result_data`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
pre_result_data
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-505"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:89`
- Evidence:
- node_kind: `verilog_rtl`
- detail: pre_result_tag
- source_excerpt: `pre_result_tag`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
pre_result_tag
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-506"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:90`
- Evidence:
- node_kind: `verilog_rtl`
- detail: pre_result_fault
- source_excerpt: `pre_result_fault`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
pre_result_fault
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-507"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:92`
- Evidence:
- node_kind: `verilog_rtl`
- detail: silu_input_ready
- source_excerpt: `silu_input_ready`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
silu_input_ready
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-508"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:93`
- Evidence:
- node_kind: `verilog_rtl`
- detail: silu_table_ready
- source_excerpt: `silu_table_ready`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
silu_table_ready
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-509"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:94`
- Evidence:
- node_kind: `verilog_rtl`
- detail: silu_table_loaded
- source_excerpt: `silu_table_loaded`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
silu_table_loaded
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-510"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:95`
- Evidence:
- node_kind: `verilog_rtl`
- detail: silu_table_fault
- source_excerpt: `silu_table_fault`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
silu_table_fault
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-511"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:96`
- Evidence:
- node_kind: `verilog_rtl`
- detail: silu_output_valid
- source_excerpt: `silu_output_valid`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
silu_output_valid
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-512"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:97`
- Evidence:
- node_kind: `verilog_rtl`
- detail: silu_output_data
- source_excerpt: `silu_output_data`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
silu_output_data
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-513"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:103`
- Evidence:
- node_kind: `verilog_rtl`
- detail: post_result_valid
- source_excerpt: `post_result_valid`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
post_result_valid
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-514"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:104`
- Evidence:
- node_kind: `verilog_rtl`
- detail: post_result_data
- source_excerpt: `post_result_data`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
post_result_data
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-515"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:105`
- Evidence:
- node_kind: `verilog_rtl`
- detail: post_result_tag
- source_excerpt: `post_result_tag`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
post_result_tag
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-516"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_postprocess_stream.v:106`
- Evidence:
- node_kind: `verilog_rtl`
- detail: post_result_fault
- source_excerpt: `post_result_fault`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
post_result_fault
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

## Other deliverable findings

| Severity | Code | Path | Line | Message |
|---|---|---|---:|---|
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:6` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:7` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:8` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:9` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:10` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:11` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:12` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:13` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:14` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:15` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:16` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:17` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:18` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:19` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:20` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:21` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:22` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:23` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:24` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:25` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:26` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:27` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:28` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:29` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:30` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:31` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:32` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:33` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:34` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:37` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:38` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:39` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:40` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:41` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:42` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:43` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:44` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:46` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:47` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:48` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:49` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:50` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:51` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:52` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:53` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:54` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:55` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:56` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:58` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:59` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:60` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:61` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:62` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:63` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:64` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:66` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:67` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:68` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:69` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:70` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:71` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:72` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:73` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:74` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:75` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:76` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:77` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:78` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:79` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:80` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:81` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:82` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:83` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:85` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:86` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:87` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:88` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:89` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:90` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:92` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:93` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:94` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:95` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:96` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:97` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:98` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:99` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:101` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:102` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:103` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:104` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:105` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:106` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:107` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:108` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:109` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:110` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:111` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:113` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:115` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:118` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:120` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:122` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:123` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:124` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:125` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:126` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:127` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:129` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:131` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:135` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:138` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:141` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:143` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:144` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:145` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:147` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:149` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:150` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:152` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:154` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:155` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:156` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:157` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:158` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:161` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:164` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:166` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:168` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:169` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:170` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:171` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:172` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:173` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:174` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:175` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:176` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:177` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:178` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:179` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:180` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:181` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:182` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:184` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:264` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:289` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:313` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:327` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_postprocess_stream.v:344` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
