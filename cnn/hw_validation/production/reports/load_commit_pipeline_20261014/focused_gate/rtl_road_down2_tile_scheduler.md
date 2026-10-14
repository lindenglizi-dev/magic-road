# Verilog deliverable gate

Root: `E:\project\qiansai\anlogic_topic2_work\lab1_sc500_road_vision\cnn\hw_validation\production\reports\load_commit_pipeline_20261014\rtl\road_down2_tile_scheduler.v`
Delivery ready: `False`
Summary: **529 error(s)**, **0 strict warning(s)**

## Actionable VG findings

<a id="vg-finding-1"></a>
### VG000: > ERR: [Python] control parser strict failure.
- Status: `failed`
- Severity: `error`
- Location: `file:road_down2_tile_scheduler.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: FORMATTER_AST_PARSE
- source_excerpt: `FORMATTER_AST_PARSE`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
FORMATTER_AST_PARSE
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-2"></a>
### VG007: Standard bilingual header with English/Chinese sections is required.
- Status: `failed`
- Severity: `error`
- Location: `road_down2_tile_scheduler.v:1`
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

<a id="vg-finding-3"></a>
### VG007: English header is missing required field(s): Company, Engineer, Create Date, Design Name, Module Name, Description, Simulations, Referrences, Dependencies, Version, Revision Date, History
- Status: `failed`
- Severity: `error`
- Location: `road_down2_tile_scheduler.v:1`
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

<a id="vg-finding-4"></a>
### VG007: Chinese header is missing required field(s): 版权归属, 开发人员, 创建日期, 设计名称, 模块名称, 模块说明, 仿真工程, 参考资料, 依赖文件, 当前版本, 修订日期, 修订历史
- Status: `failed`
- Severity: `error`
- Location: `road_down2_tile_scheduler.v:1`
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

<a id="vg-finding-5"></a>
### VG068: Header Description/Simulations fields must use the fixed bilingual path contract (`description/testbench` in English and `Description/TestBench` in Chinese).
- Status: `failed`
- Severity: `error`
- Location: `road_down2_tile_scheduler.v:1`
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

<a id="vg-finding-6"></a>
### VG007: Header history must contain at least one dated record with a Vx.y version.
- Status: `failed`
- Severity: `error`
- Location: `road_down2_tile_scheduler.v:1`
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

<a id="vg-finding-7"></a>
### VG025: Control statements must use explicit begin/end blocks.
- Status: `failed`
- Severity: `error`
- Location: `road_down2_tile_scheduler.v:583`
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
### VG025: Control statements must use explicit begin/end blocks.
- Status: `failed`
- Severity: `error`
- Location: `road_down2_tile_scheduler.v:819`
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

<a id="vg-finding-9"></a>
### VG025: Control statements must use explicit begin/end blocks.
- Status: `failed`
- Severity: `error`
- Location: `road_down2_tile_scheduler.v:929`
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

<a id="vg-finding-10"></a>
### VG025: Control statements must use explicit begin/end blocks.
- Status: `failed`
- Severity: `error`
- Location: `road_down2_tile_scheduler.v:973`
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

<a id="vg-finding-11"></a>
### VG025: Control statements must use explicit begin/end blocks.
- Status: `failed`
- Severity: `error`
- Location: `road_down2_tile_scheduler.v:983`
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

<a id="vg-finding-12"></a>
### VG025: Control statements must use explicit begin/end blocks.
- Status: `failed`
- Severity: `error`
- Location: `road_down2_tile_scheduler.v:1102`
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
- Location: `road_down2_tile_scheduler.v:1111`
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
### VG042: Comment coverage is too low for generated RTL (1.76%); add semantic comments near declarations, assigns, always blocks, FSM, and instances.
- Status: `failed`
- Severity: `error`
- Location: `file:road_down2_tile_scheduler.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.coverage
- source_excerpt: `comments.coverage`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG072: > ERR: [Python] control parser strict failure.
- Status: `error`
- Severity: `BLOCKER`
- Location: `file:road_down2_tile_scheduler.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: FORMATTER_AST_PARSE
- source_excerpt: `FORMATTER_AST_PARSE`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
FORMATTER_AST_PARSE
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-16"></a>
### VG073: > ERR: [Python] control parser strict failure.
- Status: `error`
- Severity: `BLOCKER`
- Location: `file:road_down2_tile_scheduler.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: FORMATTER_AST_PARSE
- source_excerpt: `FORMATTER_AST_PARSE`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
FORMATTER_AST_PARSE
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-17"></a>
### VG074: > ERR: [Python] control parser strict failure.
- Status: `error`
- Severity: `BLOCKER`
- Location: `file:road_down2_tile_scheduler.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: FORMATTER_AST_PARSE
- source_excerpt: `FORMATTER_AST_PARSE`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
FORMATTER_AST_PARSE
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-18"></a>
### VG075: > ERR: [Python] control parser strict failure.
- Status: `error`
- Severity: `BLOCKER`
- Location: `file:road_down2_tile_scheduler.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: FORMATTER_AST_PARSE
- source_excerpt: `FORMATTER_AST_PARSE`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
FORMATTER_AST_PARSE
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-19"></a>
### VG076: > ERR: [Python] control parser strict failure.
- Status: `error`
- Severity: `BLOCKER`
- Location: `file:road_down2_tile_scheduler.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: FORMATTER_AST_PARSE
- source_excerpt: `FORMATTER_AST_PARSE`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
FORMATTER_AST_PARSE
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-20"></a>
### VG077: > ERR: [Python] control parser strict failure.
- Status: `error`
- Severity: `BLOCKER`
- Location: `file:road_down2_tile_scheduler.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: FORMATTER_AST_PARSE
- source_excerpt: `FORMATTER_AST_PARSE`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
FORMATTER_AST_PARSE
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-21"></a>
### VG078: > ERR: [Python] control parser strict failure.
- Status: `error`
- Severity: `BLOCKER`
- Location: `file:road_down2_tile_scheduler.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: FORMATTER_AST_PARSE
- source_excerpt: `FORMATTER_AST_PARSE`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
FORMATTER_AST_PARSE
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-22"></a>
### VG079: > ERR: [Python] control parser strict failure.
- Status: `error`
- Severity: `BLOCKER`
- Location: `file:road_down2_tile_scheduler.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: FORMATTER_AST_PARSE
- source_excerpt: `FORMATTER_AST_PARSE`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
FORMATTER_AST_PARSE
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-23"></a>
### VG080: > ERR: [Python] control parser strict failure.
- Status: `error`
- Severity: `BLOCKER`
- Location: `file:road_down2_tile_scheduler.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: FORMATTER_AST_PARSE
- source_excerpt: `FORMATTER_AST_PARSE`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
FORMATTER_AST_PARSE
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-24"></a>
### VG081: > ERR: [Python] control parser strict failure.
- Status: `error`
- Severity: `BLOCKER`
- Location: `file:road_down2_tile_scheduler.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: FORMATTER_AST_PARSE
- source_excerpt: `FORMATTER_AST_PARSE`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
FORMATTER_AST_PARSE
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-25"></a>
### VG082: > ERR: [Python] control parser strict failure.
- Status: `error`
- Severity: `BLOCKER`
- Location: `file:road_down2_tile_scheduler.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: FORMATTER_AST_PARSE
- source_excerpt: `FORMATTER_AST_PARSE`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
FORMATTER_AST_PARSE
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-26"></a>
### VG083: > ERR: [Python] control parser strict failure.
- Status: `error`
- Severity: `BLOCKER`
- Location: `file:road_down2_tile_scheduler.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: FORMATTER_AST_PARSE
- source_excerpt: `FORMATTER_AST_PARSE`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
FORMATTER_AST_PARSE
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-27"></a>
### VG084: > ERR: [Python] control parser strict failure.
- Status: `error`
- Severity: `BLOCKER`
- Location: `file:road_down2_tile_scheduler.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: FORMATTER_AST_PARSE
- source_excerpt: `FORMATTER_AST_PARSE`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
FORMATTER_AST_PARSE
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-28"></a>
### VG085: > ERR: [Python] control parser strict failure.
- Status: `error`
- Severity: `BLOCKER`
- Location: `file:road_down2_tile_scheduler.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: FORMATTER_AST_PARSE
- source_excerpt: `FORMATTER_AST_PARSE`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
FORMATTER_AST_PARSE
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-29"></a>
### VG086: > ERR: [Python] control parser strict failure.
- Status: `error`
- Severity: `BLOCKER`
- Location: `file:road_down2_tile_scheduler.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: FORMATTER_AST_PARSE
- source_excerpt: `FORMATTER_AST_PARSE`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
FORMATTER_AST_PARSE
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-30"></a>
### VG087: > ERR: [Python] control parser strict failure.
- Status: `error`
- Severity: `BLOCKER`
- Location: `file:road_down2_tile_scheduler.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: FORMATTER_AST_PARSE
- source_excerpt: `FORMATTER_AST_PARSE`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
FORMATTER_AST_PARSE
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-31"></a>
### VG088: > ERR: [Python] control parser strict failure.
- Status: `error`
- Severity: `BLOCKER`
- Location: `file:road_down2_tile_scheduler.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: FORMATTER_AST_PARSE
- source_excerpt: `FORMATTER_AST_PARSE`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
FORMATTER_AST_PARSE
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-32"></a>
### VG089: > ERR: [Python] control parser strict failure.
- Status: `error`
- Severity: `BLOCKER`
- Location: `file:road_down2_tile_scheduler.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: FORMATTER_AST_PARSE
- source_excerpt: `FORMATTER_AST_PARSE`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
FORMATTER_AST_PARSE
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-33"></a>
### VG090: > ERR: [Python] control parser strict failure.
- Status: `error`
- Severity: `BLOCKER`
- Location: `file:road_down2_tile_scheduler.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: FORMATTER_AST_PARSE
- source_excerpt: `FORMATTER_AST_PARSE`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
FORMATTER_AST_PARSE
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-34"></a>
### VG091: > ERR: [Python] control parser strict failure.
- Status: `error`
- Severity: `BLOCKER`
- Location: `file:road_down2_tile_scheduler.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: FORMATTER_AST_PARSE
- source_excerpt: `FORMATTER_AST_PARSE`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
FORMATTER_AST_PARSE
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-35"></a>
### VG092: > ERR: [Python] control parser strict failure.
- Status: `error`
- Severity: `BLOCKER`
- Location: `file:road_down2_tile_scheduler.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: FORMATTER_AST_PARSE
- source_excerpt: `FORMATTER_AST_PARSE`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
FORMATTER_AST_PARSE
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-36"></a>
### VG093: > ERR: [Python] control parser strict failure.
- Status: `error`
- Severity: `BLOCKER`
- Location: `file:road_down2_tile_scheduler.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: FORMATTER_AST_PARSE
- source_excerpt: `FORMATTER_AST_PARSE`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
FORMATTER_AST_PARSE
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-37"></a>
### VG094: > ERR: [Python] control parser strict failure.
- Status: `error`
- Severity: `BLOCKER`
- Location: `file:road_down2_tile_scheduler.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: FORMATTER_AST_PARSE
- source_excerpt: `FORMATTER_AST_PARSE`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
FORMATTER_AST_PARSE
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-38"></a>
### VG095: > ERR: [Python] control parser strict failure.
- Status: `error`
- Severity: `BLOCKER`
- Location: `file:road_down2_tile_scheduler.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: FORMATTER_AST_PARSE
- source_excerpt: `FORMATTER_AST_PARSE`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
FORMATTER_AST_PARSE
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-39"></a>
### VG096: > ERR: [Python] control parser strict failure.
- Status: `error`
- Severity: `BLOCKER`
- Location: `file:road_down2_tile_scheduler.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: FORMATTER_AST_PARSE
- source_excerpt: `FORMATTER_AST_PARSE`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
FORMATTER_AST_PARSE
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-40"></a>
### VG097: > ERR: [Python] control parser strict failure.
- Status: `error`
- Severity: `BLOCKER`
- Location: `file:road_down2_tile_scheduler.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: FORMATTER_AST_PARSE
- source_excerpt: `FORMATTER_AST_PARSE`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
FORMATTER_AST_PARSE
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-41"></a>
### VG098: > ERR: [Python] control parser strict failure.
- Status: `error`
- Severity: `BLOCKER`
- Location: `file:road_down2_tile_scheduler.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: FORMATTER_AST_PARSE
- source_excerpt: `FORMATTER_AST_PARSE`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
FORMATTER_AST_PARSE
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-42"></a>
### VG099: > ERR: [Python] control parser strict failure.
- Status: `error`
- Severity: `BLOCKER`
- Location: `file:road_down2_tile_scheduler.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: FORMATTER_AST_PARSE
- source_excerpt: `FORMATTER_AST_PARSE`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
FORMATTER_AST_PARSE
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-43"></a>
### VG100: > ERR: [Python] control parser strict failure.
- Status: `error`
- Severity: `BLOCKER`
- Location: `file:road_down2_tile_scheduler.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: FORMATTER_AST_PARSE
- source_excerpt: `FORMATTER_AST_PARSE`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
FORMATTER_AST_PARSE
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-44"></a>
### VG101: > ERR: [Python] control parser strict failure.
- Status: `error`
- Severity: `BLOCKER`
- Location: `file:road_down2_tile_scheduler.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: FORMATTER_AST_PARSE
- source_excerpt: `FORMATTER_AST_PARSE`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
FORMATTER_AST_PARSE
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-45"></a>
### VG102: > ERR: [Python] control parser strict failure.
- Status: `error`
- Severity: `BLOCKER`
- Location: `file:road_down2_tile_scheduler.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: FORMATTER_AST_PARSE
- source_excerpt: `FORMATTER_AST_PARSE`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
FORMATTER_AST_PARSE
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-46"></a>
### VG103: > ERR: [Python] control parser strict failure.
- Status: `error`
- Severity: `BLOCKER`
- Location: `file:road_down2_tile_scheduler.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: FORMATTER_AST_PARSE
- source_excerpt: `FORMATTER_AST_PARSE`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
FORMATTER_AST_PARSE
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-47"></a>
### VG104: > ERR: [Python] control parser strict failure.
- Status: `error`
- Severity: `BLOCKER`
- Location: `file:road_down2_tile_scheduler.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: FORMATTER_AST_PARSE
- source_excerpt: `FORMATTER_AST_PARSE`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
FORMATTER_AST_PARSE
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-48"></a>
### VG105: > ERR: [Python] control parser strict failure.
- Status: `error`
- Severity: `BLOCKER`
- Location: `file:road_down2_tile_scheduler.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: FORMATTER_AST_PARSE
- source_excerpt: `FORMATTER_AST_PARSE`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
FORMATTER_AST_PARSE
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-49"></a>
### VG106: > ERR: [Python] control parser strict failure.
- Status: `error`
- Severity: `BLOCKER`
- Location: `file:road_down2_tile_scheduler.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: FORMATTER_AST_PARSE
- source_excerpt: `FORMATTER_AST_PARSE`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
FORMATTER_AST_PARSE
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-50"></a>
### VG107: > ERR: [Python] control parser strict failure.
- Status: `error`
- Severity: `BLOCKER`
- Location: `file:road_down2_tile_scheduler.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: FORMATTER_AST_PARSE
- source_excerpt: `FORMATTER_AST_PARSE`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
FORMATTER_AST_PARSE
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-51"></a>
### VG108: > ERR: [Python] control parser strict failure.
- Status: `error`
- Severity: `BLOCKER`
- Location: `file:road_down2_tile_scheduler.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: FORMATTER_AST_PARSE
- source_excerpt: `FORMATTER_AST_PARSE`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
FORMATTER_AST_PARSE
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-52"></a>
### VG109: > ERR: [Python] control parser strict failure.
- Status: `error`
- Severity: `BLOCKER`
- Location: `file:road_down2_tile_scheduler.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: FORMATTER_AST_PARSE
- source_excerpt: `FORMATTER_AST_PARSE`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
FORMATTER_AST_PARSE
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-53"></a>
### VG110: > ERR: [Python] control parser strict failure.
- Status: `error`
- Severity: `BLOCKER`
- Location: `file:road_down2_tile_scheduler.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: FORMATTER_AST_PARSE
- source_excerpt: `FORMATTER_AST_PARSE`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
FORMATTER_AST_PARSE
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-54"></a>
### VG111: > ERR: [Python] control parser strict failure.
- Status: `error`
- Severity: `BLOCKER`
- Location: `file:road_down2_tile_scheduler.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: FORMATTER_AST_PARSE
- source_excerpt: `FORMATTER_AST_PARSE`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
FORMATTER_AST_PARSE
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-55"></a>
### VG112: > ERR: [Python] control parser strict failure.
- Status: `error`
- Severity: `BLOCKER`
- Location: `file:road_down2_tile_scheduler.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: FORMATTER_AST_PARSE
- source_excerpt: `FORMATTER_AST_PARSE`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
FORMATTER_AST_PARSE
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-56"></a>
### VG113: > ERR: [Python] control parser strict failure.
- Status: `error`
- Severity: `BLOCKER`
- Location: `file:road_down2_tile_scheduler.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: FORMATTER_AST_PARSE
- source_excerpt: `FORMATTER_AST_PARSE`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
FORMATTER_AST_PARSE
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-57"></a>
### VG114: > ERR: [Python] control parser strict failure.
- Status: `error`
- Severity: `BLOCKER`
- Location: `file:road_down2_tile_scheduler.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: FORMATTER_AST_PARSE
- source_excerpt: `FORMATTER_AST_PARSE`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
FORMATTER_AST_PARSE
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-58"></a>
### VG115: > ERR: [Python] control parser strict failure.
- Status: `error`
- Severity: `BLOCKER`
- Location: `file:road_down2_tile_scheduler.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: FORMATTER_AST_PARSE
- source_excerpt: `FORMATTER_AST_PARSE`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
FORMATTER_AST_PARSE
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-59"></a>
### VG116: > ERR: [Python] control parser strict failure.
- Status: `error`
- Severity: `BLOCKER`
- Location: `file:road_down2_tile_scheduler.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: FORMATTER_AST_PARSE
- source_excerpt: `FORMATTER_AST_PARSE`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
FORMATTER_AST_PARSE
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-60"></a>
### VG117: > ERR: [Python] control parser strict failure.
- Status: `error`
- Severity: `BLOCKER`
- Location: `file:road_down2_tile_scheduler.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: FORMATTER_AST_PARSE
- source_excerpt: `FORMATTER_AST_PARSE`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
FORMATTER_AST_PARSE
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-61"></a>
### VG118: > ERR: [Python] control parser strict failure.
- Status: `error`
- Severity: `BLOCKER`
- Location: `file:road_down2_tile_scheduler.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: FORMATTER_AST_PARSE
- source_excerpt: `FORMATTER_AST_PARSE`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
FORMATTER_AST_PARSE
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-62"></a>
### VG119: > ERR: [Python] control parser strict failure.
- Status: `error`
- Severity: `BLOCKER`
- Location: `file:road_down2_tile_scheduler.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: FORMATTER_AST_PARSE
- source_excerpt: `FORMATTER_AST_PARSE`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
FORMATTER_AST_PARSE
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-63"></a>
### VG120: > ERR: [Python] control parser strict failure.
- Status: `error`
- Severity: `BLOCKER`
- Location: `file:road_down2_tile_scheduler.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: FORMATTER_AST_PARSE
- source_excerpt: `FORMATTER_AST_PARSE`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
FORMATTER_AST_PARSE
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-64"></a>
### VG121: > ERR: [Python] control parser strict failure.
- Status: `error`
- Severity: `BLOCKER`
- Location: `file:road_down2_tile_scheduler.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: FORMATTER_AST_PARSE
- source_excerpt: `FORMATTER_AST_PARSE`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
FORMATTER_AST_PARSE
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-65"></a>
### VG122: > ERR: [Python] control parser strict failure.
- Status: `error`
- Severity: `BLOCKER`
- Location: `file:road_down2_tile_scheduler.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: FORMATTER_AST_PARSE
- source_excerpt: `FORMATTER_AST_PARSE`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
FORMATTER_AST_PARSE
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-66"></a>
### VG123: > ERR: [Python] control parser strict failure.
- Status: `error`
- Severity: `BLOCKER`
- Location: `file:road_down2_tile_scheduler.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: FORMATTER_AST_PARSE
- source_excerpt: `FORMATTER_AST_PARSE`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
FORMATTER_AST_PARSE
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-67"></a>
### VG124: > ERR: [Python] control parser strict failure.
- Status: `error`
- Severity: `BLOCKER`
- Location: `file:road_down2_tile_scheduler.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: FORMATTER_AST_PARSE
- source_excerpt: `FORMATTER_AST_PARSE`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
FORMATTER_AST_PARSE
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-68"></a>
### VG125: > ERR: [Python] control parser strict failure.
- Status: `error`
- Severity: `BLOCKER`
- Location: `file:road_down2_tile_scheduler.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: FORMATTER_AST_PARSE
- source_excerpt: `FORMATTER_AST_PARSE`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
FORMATTER_AST_PARSE
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-69"></a>
### VG126: > ERR: [Python] control parser strict failure.
- Status: `error`
- Severity: `BLOCKER`
- Location: `file:road_down2_tile_scheduler.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: FORMATTER_AST_PARSE
- source_excerpt: `FORMATTER_AST_PARSE`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
FORMATTER_AST_PARSE
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-70"></a>
### VG127: > ERR: [Python] control parser strict failure.
- Status: `error`
- Severity: `BLOCKER`
- Location: `file:road_down2_tile_scheduler.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: FORMATTER_AST_PARSE
- source_excerpt: `FORMATTER_AST_PARSE`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
FORMATTER_AST_PARSE
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-71"></a>
### VG128: > ERR: [Python] control parser strict failure.
- Status: `error`
- Severity: `BLOCKER`
- Location: `file:road_down2_tile_scheduler.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: FORMATTER_AST_PARSE
- source_excerpt: `FORMATTER_AST_PARSE`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
FORMATTER_AST_PARSE
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-72"></a>
### VG129: > ERR: [Python] control parser strict failure.
- Status: `error`
- Severity: `BLOCKER`
- Location: `file:road_down2_tile_scheduler.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: FORMATTER_AST_PARSE
- source_excerpt: `FORMATTER_AST_PARSE`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
FORMATTER_AST_PARSE
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-73"></a>
### VG130: > ERR: [Python] control parser strict failure.
- Status: `error`
- Severity: `BLOCKER`
- Location: `file:road_down2_tile_scheduler.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: FORMATTER_AST_PARSE
- source_excerpt: `FORMATTER_AST_PARSE`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
FORMATTER_AST_PARSE
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-74"></a>
### VG131: > ERR: [Python] control parser strict failure.
- Status: `error`
- Severity: `BLOCKER`
- Location: `file:road_down2_tile_scheduler.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: FORMATTER_AST_PARSE
- source_excerpt: `FORMATTER_AST_PARSE`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
FORMATTER_AST_PARSE
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-75"></a>
### VG132: > ERR: [Python] control parser strict failure.
- Status: `error`
- Severity: `BLOCKER`
- Location: `file:road_down2_tile_scheduler.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: FORMATTER_AST_PARSE
- source_excerpt: `FORMATTER_AST_PARSE`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
FORMATTER_AST_PARSE
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-76"></a>
### VG133: > ERR: [Python] control parser strict failure.
- Status: `error`
- Severity: `BLOCKER`
- Location: `file:road_down2_tile_scheduler.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: FORMATTER_AST_PARSE
- source_excerpt: `FORMATTER_AST_PARSE`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
FORMATTER_AST_PARSE
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-77"></a>
### VG134: > ERR: [Python] control parser strict failure.
- Status: `error`
- Severity: `BLOCKER`
- Location: `file:road_down2_tile_scheduler.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: FORMATTER_AST_PARSE
- source_excerpt: `FORMATTER_AST_PARSE`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
FORMATTER_AST_PARSE
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-78"></a>
### VG135: > ERR: [Python] control parser strict failure.
- Status: `error`
- Severity: `BLOCKER`
- Location: `file:road_down2_tile_scheduler.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: FORMATTER_AST_PARSE
- source_excerpt: `FORMATTER_AST_PARSE`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
FORMATTER_AST_PARSE
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-79"></a>
### VG136: > ERR: [Python] control parser strict failure.
- Status: `error`
- Severity: `BLOCKER`
- Location: `file:road_down2_tile_scheduler.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: FORMATTER_AST_PARSE
- source_excerpt: `FORMATTER_AST_PARSE`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
FORMATTER_AST_PARSE
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-80"></a>
### VG137: > ERR: [Python] control parser strict failure.
- Status: `error`
- Severity: `BLOCKER`
- Location: `file:road_down2_tile_scheduler.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: FORMATTER_AST_PARSE
- source_excerpt: `FORMATTER_AST_PARSE`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
FORMATTER_AST_PARSE
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-81"></a>
### VG138: > ERR: [Python] control parser strict failure.
- Status: `error`
- Severity: `BLOCKER`
- Location: `file:road_down2_tile_scheduler.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: FORMATTER_AST_PARSE
- source_excerpt: `FORMATTER_AST_PARSE`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
FORMATTER_AST_PARSE
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-82"></a>
### VG139: > ERR: [Python] control parser strict failure.
- Status: `error`
- Severity: `BLOCKER`
- Location: `file:road_down2_tile_scheduler.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: FORMATTER_AST_PARSE
- source_excerpt: `FORMATTER_AST_PARSE`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
FORMATTER_AST_PARSE
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-83"></a>
### VG140: > ERR: [Python] control parser strict failure.
- Status: `error`
- Severity: `BLOCKER`
- Location: `file:road_down2_tile_scheduler.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: FORMATTER_AST_PARSE
- source_excerpt: `FORMATTER_AST_PARSE`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
FORMATTER_AST_PARSE
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-84"></a>
### VG141: > ERR: [Python] control parser strict failure.
- Status: `error`
- Severity: `BLOCKER`
- Location: `file:road_down2_tile_scheduler.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: FORMATTER_AST_PARSE
- source_excerpt: `FORMATTER_AST_PARSE`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
FORMATTER_AST_PARSE
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-85"></a>
### VG142: > ERR: [Python] control parser strict failure.
- Status: `error`
- Severity: `BLOCKER`
- Location: `file:road_down2_tile_scheduler.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: FORMATTER_AST_PARSE
- source_excerpt: `FORMATTER_AST_PARSE`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
FORMATTER_AST_PARSE
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-86"></a>
### VG143: > ERR: [Python] control parser strict failure.
- Status: `error`
- Severity: `BLOCKER`
- Location: `file:road_down2_tile_scheduler.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: FORMATTER_AST_PARSE
- source_excerpt: `FORMATTER_AST_PARSE`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
FORMATTER_AST_PARSE
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-87"></a>
### VG144: > ERR: [Python] control parser strict failure.
- Status: `error`
- Severity: `BLOCKER`
- Location: `file:road_down2_tile_scheduler.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: FORMATTER_AST_PARSE
- source_excerpt: `FORMATTER_AST_PARSE`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
FORMATTER_AST_PARSE
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-88"></a>
### VG145: > ERR: [Python] control parser strict failure.
- Status: `error`
- Severity: `BLOCKER`
- Location: `file:road_down2_tile_scheduler.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: FORMATTER_AST_PARSE
- source_excerpt: `FORMATTER_AST_PARSE`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
FORMATTER_AST_PARSE
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-89"></a>
### VG146: > ERR: [Python] control parser strict failure.
- Status: `error`
- Severity: `BLOCKER`
- Location: `file:road_down2_tile_scheduler.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: FORMATTER_AST_PARSE
- source_excerpt: `FORMATTER_AST_PARSE`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
FORMATTER_AST_PARSE
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-90"></a>
### VG147: > ERR: [Python] control parser strict failure.
- Status: `error`
- Severity: `BLOCKER`
- Location: `file:road_down2_tile_scheduler.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: FORMATTER_AST_PARSE
- source_excerpt: `FORMATTER_AST_PARSE`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
FORMATTER_AST_PARSE
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-91"></a>
### VG150: > ERR: [Python] control parser strict failure.
- Status: `error`
- Severity: `BLOCKER`
- Location: `file:road_down2_tile_scheduler.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: FORMATTER_AST_PARSE
- source_excerpt: `FORMATTER_AST_PARSE`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
FORMATTER_AST_PARSE
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-92"></a>
### VG151: > ERR: [Python] control parser strict failure.
- Status: `error`
- Severity: `BLOCKER`
- Location: `file:road_down2_tile_scheduler.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: FORMATTER_AST_PARSE
- source_excerpt: `FORMATTER_AST_PARSE`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
FORMATTER_AST_PARSE
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-93"></a>
### VG152: > ERR: [Python] control parser strict failure.
- Status: `error`
- Severity: `BLOCKER`
- Location: `file:road_down2_tile_scheduler.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: FORMATTER_AST_PARSE
- source_excerpt: `FORMATTER_AST_PARSE`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
FORMATTER_AST_PARSE
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-94"></a>
### VG153: > ERR: [Python] control parser strict failure.
- Status: `error`
- Severity: `BLOCKER`
- Location: `file:road_down2_tile_scheduler.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: FORMATTER_AST_PARSE
- source_excerpt: `FORMATTER_AST_PARSE`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
FORMATTER_AST_PARSE
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-95"></a>
### VG154: > ERR: [Python] control parser strict failure.
- Status: `error`
- Severity: `BLOCKER`
- Location: `file:road_down2_tile_scheduler.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: FORMATTER_AST_PARSE
- source_excerpt: `FORMATTER_AST_PARSE`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
FORMATTER_AST_PARSE
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-96"></a>
### VG155: > ERR: [Python] control parser strict failure.
- Status: `error`
- Severity: `BLOCKER`
- Location: `file:road_down2_tile_scheduler.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: FORMATTER_AST_PARSE
- source_excerpt: `FORMATTER_AST_PARSE`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
FORMATTER_AST_PARSE
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-97"></a>
### VG156: > ERR: [Python] control parser strict failure.
- Status: `error`
- Severity: `BLOCKER`
- Location: `file:road_down2_tile_scheduler.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: FORMATTER_AST_PARSE
- source_excerpt: `FORMATTER_AST_PARSE`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
FORMATTER_AST_PARSE
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-98"></a>
### VG157: > ERR: [Python] control parser strict failure.
- Status: `error`
- Severity: `BLOCKER`
- Location: `file:road_down2_tile_scheduler.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: FORMATTER_AST_PARSE
- source_excerpt: `FORMATTER_AST_PARSE`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
FORMATTER_AST_PARSE
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-99"></a>
### VG158: > ERR: [Python] control parser strict failure.
- Status: `error`
- Severity: `BLOCKER`
- Location: `file:road_down2_tile_scheduler.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: FORMATTER_AST_PARSE
- source_excerpt: `FORMATTER_AST_PARSE`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
FORMATTER_AST_PARSE
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

## Other deliverable findings

| Severity | Code | Path | Line | Message |
|---|---|---|---:|---|
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:6` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:7` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:8` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:9` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:10` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:11` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:12` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:13` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:14` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:15` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:16` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:17` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:18` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:19` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:20` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:21` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:22` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:23` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:24` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:25` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:26` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:27` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:28` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:29` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:30` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:31` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:32` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:33` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:34` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:35` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:36` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:37` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:38` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:39` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:40` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:41` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:42` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:43` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:44` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:45` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:46` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:47` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:48` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:49` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:50` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:51` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:52` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:53` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:54` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:55` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:56` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:57` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:58` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:59` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:60` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:61` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:62` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:63` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:64` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:65` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:66` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:67` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:68` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:69` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:70` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:71` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:72` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:73` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:74` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:75` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:76` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:77` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:78` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:79` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:80` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:81` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:82` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:83` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:84` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:85` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:88` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:89` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:90` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:91` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:92` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:93` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:94` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:95` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:96` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:97` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:99` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:100` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:101` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:102` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:103` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:104` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:106` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:107` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:108` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:109` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:110` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:111` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:112` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:113` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:114` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:115` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:117` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:118` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:119` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:120` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:121` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:122` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:124` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:125` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:126` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:127` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:128` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:129` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:130` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:131` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:133` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:134` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:135` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:136` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:137` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:138` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:139` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:140` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:141` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:142` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:144` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:146` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:147` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:148` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:149` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:150` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:151` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:152` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:153` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:154` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:155` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:156` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:157` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:158` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:159` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:160` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:161` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:162` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:164` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:165` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:166` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:167` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:168` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:169` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:170` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:171` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:173` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:174` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:175` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:176` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:177` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:178` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:180` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:181` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:182` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:183` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:184` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:185` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:186` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:187` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:188` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:189` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:190` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:191` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:192` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:193` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:194` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:195` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:196` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:198` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:199` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:200` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:201` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:202` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:203` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:204` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:205` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:206` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:207` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:208` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:209` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:211` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:212` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:213` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:214` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:215` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:217` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:218` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:219` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:220` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:221` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:222` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:223` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:224` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:225` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:226` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:227` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:228` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:229` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:230` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:231` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:232` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:234` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:235` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:236` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:237` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:238` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:239` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:240` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:241` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:242` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:243` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:244` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:245` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:246` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:247` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:248` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:249` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:251` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:252` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:253` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:254` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:255` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:256` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:257` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:258` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:259` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:260` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:261` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:262` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:263` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:264` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:265` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:266` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:267` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:268` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:269` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:270` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:271` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:272` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:273` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:274` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:275` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:276` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:277` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:278` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:279` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:280` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:281` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:282` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:283` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:284` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:285` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:286` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:287` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:288` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:289` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:290` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:291` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:292` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:293` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:294` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:295` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:297` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:298` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:299` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:300` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:301` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:302` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:303` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:304` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:305` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:306` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:309` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:310` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:316` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:317` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:318` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:319` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:320` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:321` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:322` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:323` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:324` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:325` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:326` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:327` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:328` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:329` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:330` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:331` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:332` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:333` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:335` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:337` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:339` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:341` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:343` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:346` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:347` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:348` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:359` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:360` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:361` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:363` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:364` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:365` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:368` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:372` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:374` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:375` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:376` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:377` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:378` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:379` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:388` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:389` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:391` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:395` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:396` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:402` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:403` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:404` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:405` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:407` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:408` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:409` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:410` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:411` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:412` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:414` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:415` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:416` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:417` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:422` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:423` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:424` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:425` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:426` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:432` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:434` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:435` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:436` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:443` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:444` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:445` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:448` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:450` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:452` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:453` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:456` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:458` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:459` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:461` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:462` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:464` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:466` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:468` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:469` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:470` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:471` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:472` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:473` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:474` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:475` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:476` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:477` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:478` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:479` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:480` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:481` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:482` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:483` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:484` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:485` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:486` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:487` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:488` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:489` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:490` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:491` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:492` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:493` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:494` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:495` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:496` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:497` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:498` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:499` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:500` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:501` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:502` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:503` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:504` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:505` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:506` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:507` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:508` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:509` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:510` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:511` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:512` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:513` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:514` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:515` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:516` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:519` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:531` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:541` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:555` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:614` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:631` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:640` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:667` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:867` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:896` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:1011` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:1028` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_down2_tile_scheduler.v:1069` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
