# Verilog deliverable gate

Root: `E:\project\qiansai\anlogic_topic2_work\lab1_sc500_road_vision\cnn\hw_validation\production\reports\functional_completion_20261008`
Delivery ready: `False`
Summary: **161 error(s)**, **1 strict warning(s)**

## Actionable VG findings

<a id="vg-finding-1"></a>
### VG007: Standard bilingual header with English/Chinese sections is required.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_requant.v:1`
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
- Location: `road_dynamic_requant.v:1`
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
- Location: `road_dynamic_requant.v:1`
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
- Location: `road_dynamic_requant.v:1`
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
- Location: `road_dynamic_requant.v:1`
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
### VG009: Module `road_dynamic_requant` port list should use Chinese group comments such as 全局信号, 用户接口, or protocol 接口 groups.
- Status: `failed`
- Severity: `error`
- Location: `file:road_dynamic_requant.v:unknown`
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

<a id="vg-finding-7"></a>
### VG015: Internal non-array reg declaration `reg_product` must be explicitly initialized inside the module; when backfilling a missing initializer, use exact ` = 0;`.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_requant.v:20`
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

<a id="vg-finding-8"></a>
### VG015: Internal non-array reg declaration `reg_shift` must be explicitly initialized inside the module; when backfilling a missing initializer, use exact ` = 0;`.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_requant.v:21`
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
### VG015: Internal non-array reg declaration `reg_tag` must be explicitly initialized inside the module; when backfilling a missing initializer, use exact ` = 0;`.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_requant.v:22`
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
### VG015: Internal non-array reg declaration `flag_product_valid` must be explicitly initialized inside the module; when backfilling a missing initializer, use exact ` = 0;`.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_requant.v:23`
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

<a id="vg-finding-11"></a>
### VG020: Always block `always@(posedge i_clk or negedge i_rstn)` assigns multiple targets ['flag_product_valid', 'reg_product', 'reg_shift', 'reg_tag']; split to one target per always.
- Status: `failed`
- Severity: `error`
- Location: `file:road_dynamic_requant.v:unknown`
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
### VG024: Instance `u_round` should follow `<module>_Inst_<role>` naming when practical.
- Status: `failed`
- Severity: `warning`
- Location: `file:road_dynamic_requant.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: instance.naming
- source_excerpt: `instance.naming`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `structure`
- Bad example:
```text
instance.naming
```
- Good example:
```text
调整结构关系后重新检查组合锥、实例连接和相关下游节点。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-13"></a>
### VG031: Non-trivial RTL must use fixed Erie region banners.
- Status: `failed`
- Severity: `error`
- Location: `file:road_dynamic_requant.v:unknown`
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

<a id="vg-finding-14"></a>
### VG040: port `i_clk` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_requant.v:5`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.coverage
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-15"></a>
### VG040: port `i_rstn` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_requant.v:6`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.coverage
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-16"></a>
### VG040: port `i_input_valid` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_requant.v:7`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.coverage
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-17"></a>
### VG040: port `i_accumulator` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_requant.v:8`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.coverage
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-18"></a>
### VG040: port `i_multiplier` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_requant.v:9`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.coverage
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-19"></a>
### VG040: port `i_shift` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_requant.v:10`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.coverage
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-20"></a>
### VG040: port `i_tag` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_requant.v:11`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG040: port `o_input_ready` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_requant.v:12`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG040: port `i_output_ready` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_requant.v:13`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG040: port `o_output_valid` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_requant.v:14`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG040: port `o_output_data` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_requant.v:15`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG040: port `o_output_tag` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_requant.v:16`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG040: port `o_fault` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_requant.v:17`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG040: signal `reg_product` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_requant.v:20`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG040: signal `reg_shift` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_requant.v:21`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG040: signal `reg_tag` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_requant.v:22`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG040: signal `flag_product_valid` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_requant.v:23`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG040: signal `wire_multiplier` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_requant.v:24`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG040: signal `flag_advance` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_requant.v:25`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG040: signal `flag_round_valid` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_requant.v:26`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.coverage
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-34"></a>
### VG040: signal `wire_round_data` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_requant.v:27`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.coverage
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-35"></a>
### VG040: signal `wire_round_tag` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_requant.v:28`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.coverage
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-36"></a>
### VG040: signal `flag_round_fault` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_requant.v:29`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.coverage
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-37"></a>
### VG040: assign `wire_multiplier` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_requant.v:32`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG040: assign `flag_advance` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_requant.v:33`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG040: assign `o_input_ready` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_requant.v:34`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG040: assign `o_output_valid` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_requant.v:35`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG040: assign `o_output_data` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_requant.v:36`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG040: assign `o_output_tag` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_requant.v:37`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG040: assign `o_fault` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_requant.v:38`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `reg_product` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_requant.v:43`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `reg_shift` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_requant.v:44`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `reg_tag` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_requant.v:45`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `flag_product_valid` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_requant.v:46`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `flag_product_valid` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_requant.v:48`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `reg_product` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_requant.v:50`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `reg_shift` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_requant.v:51`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `reg_tag` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_requant.v:52`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG064: instance mapping `.i_clk` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_requant.v:59`
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

<a id="vg-finding-53"></a>
### VG064: instance mapping `.i_input_valid` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_requant.v:60`
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

<a id="vg-finding-54"></a>
### VG064: instance mapping `.i_shift` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_requant.v:61`
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

<a id="vg-finding-55"></a>
### VG064: instance mapping `.o_result_valid` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_requant.v:62`
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

<a id="vg-finding-56"></a>
### VG064: instance mapping `.o_result_tag` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_dynamic_requant.v:63`
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

<a id="vg-finding-57"></a>
### VG042: Comment coverage is too low for generated RTL (0.00%); add semantic comments near declarations, assigns, always blocks, FSM, and instances.
- Status: `failed`
- Severity: `error`
- Location: `file:road_dynamic_requant.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG093: 异步复位信号被连接到普通数据赋值右值。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_requant.v:33`
- Evidence:
- node_kind: `verilog_rtl`
- detail: flag_advance = i_rstn && (!flag_round_valid || i_output_ready)
- source_excerpt: `flag_advance = i_rstn && (!flag_round_valid || i_output_ready)`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
flag_advance = i_rstn && (!flag_round_valid || i_output_ready)
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-59"></a>
### VG093: 异步复位信号被连接到普通数据赋值右值。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_requant.v:35`
- Evidence:
- node_kind: `verilog_rtl`
- detail: o_output_valid = i_rstn && flag_round_valid
- source_excerpt: `o_output_valid = i_rstn && flag_round_valid`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
o_output_valid = i_rstn && flag_round_valid
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-60"></a>
### VG138: 常量未显式声明位宽和进制。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_dynamic_requant.v:57`
- Evidence:
- node_kind: `verilog_rtl`
- detail: =63
- source_excerpt: `=63`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
=63
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-61"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `dependencies/road_round_shift.v:47`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_requant.v:road_dynamic_requant@4:1-65:1; instance_path=road_dynamic_requant/u_round; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=fault_o$D; child_output=road_dynamic_requant/u_round.fault_o$D; operation_count=4; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_dynamic_requant.v:road_dynamic_requant@4:1-65:1; instance_path=road_dynamic_requant/u_round; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=fault_o$D; child_output=road_dynamic_requant/u_round.fault_o$D; operation_count=4; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_requant.v:road_dynamic_requant@4:1-65:1; instance_path=road_dynamic_requant/u_round; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=fault_o$D; child_output=road_dynamic_requant/u_round.fault_o$D; operation_count=4; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-62"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `dependencies/road_round_shift.v:47`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_requant.v:road_dynamic_requant@4:1-65:1; instance_path=road_dynamic_requant/u_round; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_valid_pipe$D; child_output=road_dynamic_requant/u_round.flag_valid_pipe$D; operation_count=4; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_dynamic_requant.v:road_dynamic_requant@4:1-65:1; instance_path=road_dynamic_requant/u_round; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_valid_pipe$D; child_output=road_dynamic_requant/u_round.flag_valid_pipe$D; operation_count=4; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_requant.v:road_dynamic_requant@4:1-65:1; instance_path=road_dynamic_requant/u_round; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_valid_pipe$D; child_output=road_dynamic_requant/u_round.flag_valid_pipe$D; operation_count=4; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-63"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `dependencies/road_round_shift.v:47`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_requant.v:road_dynamic_requant@4:1-65:1; instance_path=road_dynamic_requant/u_round; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_above$D; child_output=road_dynamic_requant/u_round.reg_above$D; operation_count=5; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_dynamic_requant.v:road_dynamic_requant@4:1-65:1; instance_path=road_dynamic_requant/u_round; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_above$D; child_output=road_dynamic_requant/u_round.reg_above$D; operation_count=5; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_requant.v:road_dynamic_requant@4:1-65:1; instance_path=road_dynamic_requant/u_round; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_above$D; child_output=road_dynamic_requant/u_round.reg_above$D; operation_count=5; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-64"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `dependencies/road_round_shift.v:47`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_requant.v:road_dynamic_requant@4:1-65:1; instance_path=road_dynamic_requant/u_round; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_above_maximum$D; child_output=road_dynamic_requant/u_round.reg_above_maximum$D; operation_count=5; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_dynamic_requant.v:road_dynamic_requant@4:1-65:1; instance_path=road_dynamic_requant/u_round; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_above_maximum$D; child_output=road_dynamic_requant/u_round.reg_above_maximum$D; operation_count=5; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_requant.v:road_dynamic_requant@4:1-65:1; instance_path=road_dynamic_requant/u_round; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_above_maximum$D; child_output=road_dynamic_requant/u_round.reg_above_maximum$D; operation_count=5; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-65"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `dependencies/road_round_shift.v:47`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_requant.v:road_dynamic_requant@4:1-65:1; instance_path=road_dynamic_requant/u_round; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_absolute$D; child_output=road_dynamic_requant/u_round.reg_absolute$D; operation_count=6; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_dynamic_requant.v:road_dynamic_requant@4:1-65:1; instance_path=road_dynamic_requant/u_round; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_absolute$D; child_output=road_dynamic_requant/u_round.reg_absolute$D; operation_count=6; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_requant.v:road_dynamic_requant@4:1-65:1; instance_path=road_dynamic_requant/u_round; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_absolute$D; child_output=road_dynamic_requant/u_round.reg_absolute$D; operation_count=6; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-66"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `dependencies/road_round_shift.v:47`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_requant.v:road_dynamic_requant@4:1-65:1; instance_path=road_dynamic_requant/u_round; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_absolute_delay$D; child_output=road_dynamic_requant/u_round.reg_absolute_delay$D; operation_count=4; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_dynamic_requant.v:road_dynamic_requant@4:1-65:1; instance_path=road_dynamic_requant/u_round; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_absolute_delay$D; child_output=road_dynamic_requant/u_round.reg_absolute_delay$D; operation_count=4; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_requant.v:road_dynamic_requant@4:1-65:1; instance_path=road_dynamic_requant/u_round; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_absolute_delay$D; child_output=road_dynamic_requant/u_round.reg_absolute_delay$D; operation_count=4; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-67"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `dependencies/road_round_shift.v:47`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_requant.v:road_dynamic_requant@4:1-65:1; instance_path=road_dynamic_requant/u_round; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_bad_product$D; child_output=road_dynamic_requant/u_round.reg_bad_product$D; operation_count=5; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_dynamic_requant.v:road_dynamic_requant@4:1-65:1; instance_path=road_dynamic_requant/u_round; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_bad_product$D; child_output=road_dynamic_requant/u_round.reg_bad_product$D; operation_count=5; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_requant.v:road_dynamic_requant@4:1-65:1; instance_path=road_dynamic_requant/u_round; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_bad_product$D; child_output=road_dynamic_requant/u_round.reg_bad_product$D; operation_count=5; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-68"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `dependencies/road_round_shift.v:47`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_requant.v:road_dynamic_requant@4:1-65:1; instance_path=road_dynamic_requant/u_round; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_bad_shift$D; child_output=road_dynamic_requant/u_round.reg_bad_shift$D; operation_count=5; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_dynamic_requant.v:road_dynamic_requant@4:1-65:1; instance_path=road_dynamic_requant/u_round; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_bad_shift$D; child_output=road_dynamic_requant/u_round.reg_bad_shift$D; operation_count=5; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_requant.v:road_dynamic_requant@4:1-65:1; instance_path=road_dynamic_requant/u_round; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_bad_shift$D; child_output=road_dynamic_requant/u_round.reg_bad_shift$D; operation_count=5; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-69"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `dependencies/road_round_shift.v:47`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_requant.v:road_dynamic_requant@4:1-65:1; instance_path=road_dynamic_requant/u_round; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_below_minimum$D; child_output=road_dynamic_requant/u_round.reg_below_minimum$D; operation_count=5; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_dynamic_requant.v:road_dynamic_requant@4:1-65:1; instance_path=road_dynamic_requant/u_round; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_below_minimum$D; child_output=road_dynamic_requant/u_round.reg_below_minimum$D; operation_count=5; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_requant.v:road_dynamic_requant@4:1-65:1; instance_path=road_dynamic_requant/u_round; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_below_minimum$D; child_output=road_dynamic_requant/u_round.reg_below_minimum$D; operation_count=5; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-70"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `dependencies/road_round_shift.v:47`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_requant.v:road_dynamic_requant@4:1-65:1; instance_path=road_dynamic_requant/u_round; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_fault_pipe$D; child_output=road_dynamic_requant/u_round.reg_fault_pipe$D; operation_count=5; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_dynamic_requant.v:road_dynamic_requant@4:1-65:1; instance_path=road_dynamic_requant/u_round; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_fault_pipe$D; child_output=road_dynamic_requant/u_round.reg_fault_pipe$D; operation_count=5; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_requant.v:road_dynamic_requant@4:1-65:1; instance_path=road_dynamic_requant/u_round; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_fault_pipe$D; child_output=road_dynamic_requant/u_round.reg_fault_pipe$D; operation_count=5; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-71"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `dependencies/road_round_shift.v:47`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_requant.v:road_dynamic_requant@4:1-65:1; instance_path=road_dynamic_requant/u_round; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_fraction_pipe$D; child_output=road_dynamic_requant/u_round.reg_fraction_pipe$D; operation_count=5; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_dynamic_requant.v:road_dynamic_requant@4:1-65:1; instance_path=road_dynamic_requant/u_round; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_fraction_pipe$D; child_output=road_dynamic_requant/u_round.reg_fraction_pipe$D; operation_count=5; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_requant.v:road_dynamic_requant@4:1-65:1; instance_path=road_dynamic_requant/u_round; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_fraction_pipe$D; child_output=road_dynamic_requant/u_round.reg_fraction_pipe$D; operation_count=5; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-72"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `dependencies/road_round_shift.v:47`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_requant.v:road_dynamic_requant@4:1-65:1; instance_path=road_dynamic_requant/u_round; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_half$D; child_output=road_dynamic_requant/u_round.reg_half$D; operation_count=6; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_dynamic_requant.v:road_dynamic_requant@4:1-65:1; instance_path=road_dynamic_requant/u_round; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_half$D; child_output=road_dynamic_requant/u_round.reg_half$D; operation_count=6; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_requant.v:road_dynamic_requant@4:1-65:1; instance_path=road_dynamic_requant/u_round; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_half$D; child_output=road_dynamic_requant/u_round.reg_half$D; operation_count=6; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-73"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `dependencies/road_round_shift.v:47`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_requant.v:road_dynamic_requant@4:1-65:1; instance_path=road_dynamic_requant/u_round; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_half_delay$D; child_output=road_dynamic_requant/u_round.reg_half_delay$D; operation_count=4; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_dynamic_requant.v:road_dynamic_requant@4:1-65:1; instance_path=road_dynamic_requant/u_round; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_half_delay$D; child_output=road_dynamic_requant/u_round.reg_half_delay$D; operation_count=4; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_requant.v:road_dynamic_requant@4:1-65:1; instance_path=road_dynamic_requant/u_round; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_half_delay$D; child_output=road_dynamic_requant/u_round.reg_half_delay$D; operation_count=4; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-74"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `dependencies/road_round_shift.v:47`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_requant.v:road_dynamic_requant@4:1-65:1; instance_path=road_dynamic_requant/u_round; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_increment$D; child_output=road_dynamic_requant/u_round.reg_increment$D; operation_count=6; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_dynamic_requant.v:road_dynamic_requant@4:1-65:1; instance_path=road_dynamic_requant/u_round; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_increment$D; child_output=road_dynamic_requant/u_round.reg_increment$D; operation_count=6; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_requant.v:road_dynamic_requant@4:1-65:1; instance_path=road_dynamic_requant/u_round; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_increment$D; child_output=road_dynamic_requant/u_round.reg_increment$D; operation_count=6; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-75"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `dependencies/road_round_shift.v:47`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_requant.v:road_dynamic_requant@4:1-65:1; instance_path=road_dynamic_requant/u_round; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_mask$D; child_output=road_dynamic_requant/u_round.reg_mask$D; operation_count=6; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_dynamic_requant.v:road_dynamic_requant@4:1-65:1; instance_path=road_dynamic_requant/u_round; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_mask$D; child_output=road_dynamic_requant/u_round.reg_mask$D; operation_count=6; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_requant.v:road_dynamic_requant@4:1-65:1; instance_path=road_dynamic_requant/u_round; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_mask$D; child_output=road_dynamic_requant/u_round.reg_mask$D; operation_count=6; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-76"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `dependencies/road_round_shift.v:47`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_requant.v:road_dynamic_requant@4:1-65:1; instance_path=road_dynamic_requant/u_round; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_narrow_value$D; child_output=road_dynamic_requant/u_round.reg_narrow_value$D; operation_count=4; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_dynamic_requant.v:road_dynamic_requant@4:1-65:1; instance_path=road_dynamic_requant/u_round; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_narrow_value$D; child_output=road_dynamic_requant/u_round.reg_narrow_value$D; operation_count=4; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_requant.v:road_dynamic_requant@4:1-65:1; instance_path=road_dynamic_requant/u_round; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_narrow_value$D; child_output=road_dynamic_requant/u_round.reg_narrow_value$D; operation_count=4; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-77"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `dependencies/road_round_shift.v:47`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_requant.v:road_dynamic_requant@4:1-65:1; instance_path=road_dynamic_requant/u_round; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_quotient$D; child_output=road_dynamic_requant/u_round.reg_quotient$D; operation_count=5; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_dynamic_requant.v:road_dynamic_requant@4:1-65:1; instance_path=road_dynamic_requant/u_round; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_quotient$D; child_output=road_dynamic_requant/u_round.reg_quotient$D; operation_count=5; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_requant.v:road_dynamic_requant@4:1-65:1; instance_path=road_dynamic_requant/u_round; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_quotient$D; child_output=road_dynamic_requant/u_round.reg_quotient$D; operation_count=5; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-78"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `dependencies/road_round_shift.v:47`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_requant.v:road_dynamic_requant@4:1-65:1; instance_path=road_dynamic_requant/u_round; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_quotient_compare$D; child_output=road_dynamic_requant/u_round.reg_quotient_compare$D; operation_count=4; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_dynamic_requant.v:road_dynamic_requant@4:1-65:1; instance_path=road_dynamic_requant/u_round; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_quotient_compare$D; child_output=road_dynamic_requant/u_round.reg_quotient_compare$D; operation_count=4; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_requant.v:road_dynamic_requant@4:1-65:1; instance_path=road_dynamic_requant/u_round; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_quotient_compare$D; child_output=road_dynamic_requant/u_round.reg_quotient_compare$D; operation_count=4; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-79"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `dependencies/road_round_shift.v:47`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_requant.v:road_dynamic_requant@4:1-65:1; instance_path=road_dynamic_requant/u_round; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_quotient_increment$D; child_output=road_dynamic_requant/u_round.reg_quotient_increment$D; operation_count=4; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_dynamic_requant.v:road_dynamic_requant@4:1-65:1; instance_path=road_dynamic_requant/u_round; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_quotient_increment$D; child_output=road_dynamic_requant/u_round.reg_quotient_increment$D; operation_count=4; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_requant.v:road_dynamic_requant@4:1-65:1; instance_path=road_dynamic_requant/u_round; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_quotient_increment$D; child_output=road_dynamic_requant/u_round.reg_quotient_increment$D; operation_count=4; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-80"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `dependencies/road_round_shift.v:47`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_requant.v:road_dynamic_requant@4:1-65:1; instance_path=road_dynamic_requant/u_round; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_quotient_rem$D; child_output=road_dynamic_requant/u_round.reg_quotient_rem$D; operation_count=4; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_dynamic_requant.v:road_dynamic_requant@4:1-65:1; instance_path=road_dynamic_requant/u_round; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_quotient_rem$D; child_output=road_dynamic_requant/u_round.reg_quotient_rem$D; operation_count=4; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_requant.v:road_dynamic_requant@4:1-65:1; instance_path=road_dynamic_requant/u_round; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_quotient_rem$D; child_output=road_dynamic_requant/u_round.reg_quotient_rem$D; operation_count=4; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-81"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `dependencies/road_round_shift.v:47`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_requant.v:road_dynamic_requant@4:1-65:1; instance_path=road_dynamic_requant/u_round; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_remainder$D; child_output=road_dynamic_requant/u_round.reg_remainder$D; operation_count=5; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_dynamic_requant.v:road_dynamic_requant@4:1-65:1; instance_path=road_dynamic_requant/u_round; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_remainder$D; child_output=road_dynamic_requant/u_round.reg_remainder$D; operation_count=5; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_requant.v:road_dynamic_requant@4:1-65:1; instance_path=road_dynamic_requant/u_round; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_remainder$D; child_output=road_dynamic_requant/u_round.reg_remainder$D; operation_count=5; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-82"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `dependencies/road_round_shift.v:47`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_requant.v:road_dynamic_requant@4:1-65:1; instance_path=road_dynamic_requant/u_round; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_rounded_magnitude$D; child_output=road_dynamic_requant/u_round.reg_rounded_magnitude$D; operation_count=5; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_dynamic_requant.v:road_dynamic_requant@4:1-65:1; instance_path=road_dynamic_requant/u_round; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_rounded_magnitude$D; child_output=road_dynamic_requant/u_round.reg_rounded_magnitude$D; operation_count=5; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_requant.v:road_dynamic_requant@4:1-65:1; instance_path=road_dynamic_requant/u_round; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_rounded_magnitude$D; child_output=road_dynamic_requant/u_round.reg_rounded_magnitude$D; operation_count=5; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-83"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `dependencies/road_round_shift.v:47`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_requant.v:road_dynamic_requant@4:1-65:1; instance_path=road_dynamic_requant/u_round; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_shift$D; child_output=road_dynamic_requant/u_round.reg_shift$D; operation_count=4; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_dynamic_requant.v:road_dynamic_requant@4:1-65:1; instance_path=road_dynamic_requant/u_round; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_shift$D; child_output=road_dynamic_requant/u_round.reg_shift$D; operation_count=4; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_requant.v:road_dynamic_requant@4:1-65:1; instance_path=road_dynamic_requant/u_round; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_shift$D; child_output=road_dynamic_requant/u_round.reg_shift$D; operation_count=4; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-84"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `dependencies/road_round_shift.v:47`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_requant.v:road_dynamic_requant@4:1-65:1; instance_path=road_dynamic_requant/u_round; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_sign_pipe$D; child_output=road_dynamic_requant/u_round.reg_sign_pipe$D; operation_count=4; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_dynamic_requant.v:road_dynamic_requant@4:1-65:1; instance_path=road_dynamic_requant/u_round; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_sign_pipe$D; child_output=road_dynamic_requant/u_round.reg_sign_pipe$D; operation_count=4; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_requant.v:road_dynamic_requant@4:1-65:1; instance_path=road_dynamic_requant/u_round; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_sign_pipe$D; child_output=road_dynamic_requant/u_round.reg_sign_pipe$D; operation_count=4; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-85"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `dependencies/road_round_shift.v:47`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_requant.v:road_dynamic_requant@4:1-65:1; instance_path=road_dynamic_requant/u_round; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_signed_value$D; child_output=road_dynamic_requant/u_round.reg_signed_value$D; operation_count=6; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_dynamic_requant.v:road_dynamic_requant@4:1-65:1; instance_path=road_dynamic_requant/u_round; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_signed_value$D; child_output=road_dynamic_requant/u_round.reg_signed_value$D; operation_count=6; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_requant.v:road_dynamic_requant@4:1-65:1; instance_path=road_dynamic_requant/u_round; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_signed_value$D; child_output=road_dynamic_requant/u_round.reg_signed_value$D; operation_count=6; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-86"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `dependencies/road_round_shift.v:47`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_requant.v:road_dynamic_requant@4:1-65:1; instance_path=road_dynamic_requant/u_round; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_tag_pipe$D; child_output=road_dynamic_requant/u_round.reg_tag_pipe$D; operation_count=4; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_dynamic_requant.v:road_dynamic_requant@4:1-65:1; instance_path=road_dynamic_requant/u_round; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_tag_pipe$D; child_output=road_dynamic_requant/u_round.reg_tag_pipe$D; operation_count=4; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_requant.v:road_dynamic_requant@4:1-65:1; instance_path=road_dynamic_requant/u_round; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_tag_pipe$D; child_output=road_dynamic_requant/u_round.reg_tag_pipe$D; operation_count=4; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-87"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `dependencies/road_round_shift.v:47`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_requant.v:road_dynamic_requant@4:1-65:1; instance_path=road_dynamic_requant/u_round; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_tie_odd$D; child_output=road_dynamic_requant/u_round.reg_tie_odd$D; operation_count=6; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_dynamic_requant.v:road_dynamic_requant@4:1-65:1; instance_path=road_dynamic_requant/u_round; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_tie_odd$D; child_output=road_dynamic_requant/u_round.reg_tie_odd$D; operation_count=6; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_requant.v:road_dynamic_requant@4:1-65:1; instance_path=road_dynamic_requant/u_round; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_tie_odd$D; child_output=road_dynamic_requant/u_round.reg_tie_odd$D; operation_count=6; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-88"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `dependencies/road_round_shift.v:47`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_requant.v:road_dynamic_requant@4:1-65:1; instance_path=road_dynamic_requant/u_round; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=result_data_o$D; child_output=road_dynamic_requant/u_round.result_data_o$D; operation_count=6; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_dynamic_requant.v:road_dynamic_requant@4:1-65:1; instance_path=road_dynamic_requant/u_round; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=result_data_o$D; child_output=road_dynamic_requant/u_round.result_data_o$D; operation_count=6; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_requant.v:road_dynamic_requant@4:1-65:1; instance_path=road_dynamic_requant/u_round; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=result_data_o$D; child_output=road_dynamic_requant/u_round.result_data_o$D; operation_count=6; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-89"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `dependencies/road_round_shift.v:47`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_requant.v:road_dynamic_requant@4:1-65:1; instance_path=road_dynamic_requant/u_round; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=result_tag_o$D; child_output=road_dynamic_requant/u_round.result_tag_o$D; operation_count=4; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_dynamic_requant.v:road_dynamic_requant@4:1-65:1; instance_path=road_dynamic_requant/u_round; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=result_tag_o$D; child_output=road_dynamic_requant/u_round.result_tag_o$D; operation_count=4; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_requant.v:road_dynamic_requant@4:1-65:1; instance_path=road_dynamic_requant/u_round; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=result_tag_o$D; child_output=road_dynamic_requant/u_round.result_tag_o$D; operation_count=4; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-90"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `dependencies/road_round_shift.v:47`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_requant.v:road_dynamic_requant@4:1-65:1; instance_path=road_dynamic_requant/u_round; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=result_valid_o$D; child_output=road_dynamic_requant/u_round.result_valid_o$D; operation_count=4; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_dynamic_requant.v:road_dynamic_requant@4:1-65:1; instance_path=road_dynamic_requant/u_round; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=result_valid_o$D; child_output=road_dynamic_requant/u_round.result_valid_o$D; operation_count=4; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_requant.v:road_dynamic_requant@4:1-65:1; instance_path=road_dynamic_requant/u_round; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=result_valid_o$D; child_output=road_dynamic_requant/u_round.result_valid_o$D; operation_count=4; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-91"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_requant.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_requant.v:road_dynamic_requant@4:1-65:1; instance_path=road_dynamic_requant; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_product_valid$D; child_output=road_dynamic_requant.flag_product_valid$D; operation_count=4; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_dynamic_requant.v:road_dynamic_requant@4:1-65:1; instance_path=road_dynamic_requant; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_product_valid$D; child_output=road_dynamic_requant.flag_product_valid$D; operation_count=4; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_requant.v:road_dynamic_requant@4:1-65:1; instance_path=road_dynamic_requant; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_product_valid$D; child_output=road_dynamic_requant.flag_product_valid$D; operation_count=4; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-92"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_requant.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_requant.v:road_dynamic_requant@4:1-65:1; instance_path=road_dynamic_requant; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_product$D; child_output=road_dynamic_requant.reg_product$D; operation_count=1; limit=3; inconclusive_reason=$signed: missing function definition; loop_presence=absent
- source_excerpt: `definition_root=road_dynamic_requant.v:road_dynamic_requant@4:1-65:1; instance_path=road_dynamic_requant; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_product$D; child_output=road_dynamic_requant.reg_product$D; operation_count=1; limit=3; inconclusive_reason=$signed: missing function definition; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_requant.v:road_dynamic_requant@4:1-65:1; instance_path=road_dynamic_requant; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_product$D; child_output=road_dynamic_requant.reg_product$D; operation_count=1; limit=3; inconclusive_reason=$signed: missing function definition; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-93"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_requant.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_requant.v:road_dynamic_requant@4:1-65:1; instance_path=road_dynamic_requant; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_product$enable; child_output=road_dynamic_requant.reg_product$enable; operation_count=4; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_dynamic_requant.v:road_dynamic_requant@4:1-65:1; instance_path=road_dynamic_requant; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_product$enable; child_output=road_dynamic_requant.reg_product$enable; operation_count=4; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_requant.v:road_dynamic_requant@4:1-65:1; instance_path=road_dynamic_requant; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_product$enable; child_output=road_dynamic_requant.reg_product$enable; operation_count=4; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-94"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_requant.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_requant.v:road_dynamic_requant@4:1-65:1; instance_path=road_dynamic_requant; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_shift$enable; child_output=road_dynamic_requant.reg_shift$enable; operation_count=4; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_dynamic_requant.v:road_dynamic_requant@4:1-65:1; instance_path=road_dynamic_requant; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_shift$enable; child_output=road_dynamic_requant.reg_shift$enable; operation_count=4; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_requant.v:road_dynamic_requant@4:1-65:1; instance_path=road_dynamic_requant; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_shift$enable; child_output=road_dynamic_requant.reg_shift$enable; operation_count=4; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-95"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_requant.v:4`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_requant.v:road_dynamic_requant@4:1-65:1; instance_path=road_dynamic_requant; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_tag$enable; child_output=road_dynamic_requant.reg_tag$enable; operation_count=4; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_dynamic_requant.v:road_dynamic_requant@4:1-65:1; instance_path=road_dynamic_requant; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_tag$enable; child_output=road_dynamic_requant.reg_tag$enable; operation_count=4; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_requant.v:road_dynamic_requant@4:1-65:1; instance_path=road_dynamic_requant; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_tag$enable; child_output=road_dynamic_requant.reg_tag$enable; operation_count=4; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-96"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_requant.v:32`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_dynamic_requant.v:road_dynamic_requant@4:1-65:1; instance_path=road_dynamic_requant; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=wire_multiplier; child_output=road_dynamic_requant.wire_multiplier; operation_count=0; limit=3; inconclusive_reason=$signed: missing function definition; loop_presence=absent
- source_excerpt: `definition_root=road_dynamic_requant.v:road_dynamic_requant@4:1-65:1; instance_path=road_dynamic_requant; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=wire_multiplier; child_output=road_dynamic_requant.wire_multiplier; operation_count=0; limit=3; inconclusive_reason=$signed: missing function definition; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_dynamic_requant.v:road_dynamic_requant@4:1-65:1; instance_path=road_dynamic_requant; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=wire_multiplier; child_output=road_dynamic_requant.wire_multiplier; operation_count=0; limit=3; inconclusive_reason=$signed: missing function definition; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-97"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_requant.v:26`
- Evidence:
- node_kind: `verilog_rtl`
- detail: flag_round_valid
- source_excerpt: `flag_round_valid`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
flag_round_valid
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-98"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_requant.v:27`
- Evidence:
- node_kind: `verilog_rtl`
- detail: wire_round_data
- source_excerpt: `wire_round_data`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
wire_round_data
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-99"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_requant.v:28`
- Evidence:
- node_kind: `verilog_rtl`
- detail: wire_round_tag
- source_excerpt: `wire_round_tag`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
wire_round_tag
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-100"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_dynamic_requant.v:29`
- Evidence:
- node_kind: `verilog_rtl`
- detail: flag_round_fault
- source_excerpt: `flag_round_fault`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
flag_round_fault
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

## Other deliverable findings

| Severity | Code | Path | Line | Message |
|---|---|---|---:|---|
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_requant.v:5` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_requant.v:6` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_requant.v:7` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_requant.v:8` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_requant.v:9` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_requant.v:10` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_requant.v:11` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_requant.v:12` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_requant.v:13` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_requant.v:14` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_requant.v:15` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_requant.v:16` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_requant.v:17` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_requant.v:20` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_requant.v:21` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_requant.v:22` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_requant.v:23` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_requant.v:24` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_requant.v:25` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_requant.v:26` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_requant.v:27` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_requant.v:28` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_requant.v:29` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_requant.v:32` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_requant.v:33` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_requant.v:34` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_requant.v:35` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_requant.v:36` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_requant.v:37` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_requant.v:38` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_dynamic_requant.v:58` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `tb_road_dynamic_requant.v:4` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `tb_road_dynamic_requant.v:5` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `tb_road_dynamic_requant.v:6` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `tb_road_dynamic_requant.v:7` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `tb_road_dynamic_requant.v:8` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `tb_road_dynamic_requant.v:9` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `tb_road_dynamic_requant.v:10` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `tb_road_dynamic_requant.v:11` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `tb_road_dynamic_requant.v:12` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `tb_road_dynamic_requant.v:13` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `tb_road_dynamic_requant.v:14` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `tb_road_dynamic_requant.v:15` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `tb_road_dynamic_requant.v:16` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `tb_road_dynamic_requant.v:17` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `tb_road_dynamic_requant.v:18` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `tb_road_dynamic_requant.v:19` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `tb_road_dynamic_requant.v:20` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `tb_road_dynamic_requant.v:21` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `tb_road_dynamic_requant.v:22` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `tb_road_dynamic_requant.v:23` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `tb_road_dynamic_requant.v:24` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `tb_road_dynamic_requant.v:25` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `tb_road_dynamic_requant.v:26` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `tb_road_dynamic_requant.v:27` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `tb_road_dynamic_requant.v:28` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `tb_road_dynamic_requant.v:29` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `tb_road_dynamic_requant.v:30` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `tb_road_dynamic_requant.v:37` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `tb_road_dynamic_requant.v:62` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
