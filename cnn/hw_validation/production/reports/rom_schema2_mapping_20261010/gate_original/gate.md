# Verilog deliverable gate

Root: `E:\project\qiansai\anlogic_topic2_work\lab1_sc500_road_vision\cnn\hw_validation\production\reports\rom_schema2_mapping_20261010\baseline`
Delivery ready: `False`
Summary: **441 error(s)**, **0 strict warning(s)**

## Actionable VG findings

<a id="vg-finding-1"></a>
### VG063: Instance comment must have exactly one blank line above unless it follows a region banner.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:150`
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

<a id="vg-finding-2"></a>
### VG063: Instance comment must have exactly one blank line above unless it follows a region banner.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:208`
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

<a id="vg-finding-3"></a>
### VG063: Instance comment must have exactly one blank line above unless it follows a region banner.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:266`
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

<a id="vg-finding-4"></a>
### VG063: Instance comment must have exactly one blank line above unless it follows a region banner.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:324`
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

<a id="vg-finding-5"></a>
### VG066: Comment for instance mapping `.dia` repeats or closely reuses comment from instance mapping `.dia`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:210`
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

<a id="vg-finding-6"></a>
### VG066: Comment for instance mapping `.addra` repeats or closely reuses comment from instance mapping `.addra`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:211`
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
### VG066: Comment for instance mapping `.cea` repeats or closely reuses comment from instance mapping `.cea`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:212`
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
### VG066: Comment for instance mapping `.ocea` repeats or closely reuses comment from instance mapping `.ocea`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:213`
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
### VG066: Comment for instance mapping `.clka` repeats or closely reuses comment from instance mapping `.clka`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:214`
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
### VG066: Comment for instance mapping `.wea` repeats or closely reuses comment from instance mapping `.wea`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:215`
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

<a id="vg-finding-11"></a>
### VG066: Comment for instance mapping `.rsta` repeats or closely reuses comment from instance mapping `.rsta`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:216`
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

<a id="vg-finding-12"></a>
### VG066: Comment for instance mapping `.bea` repeats or closely reuses comment from instance mapping `.bea`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:217`
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

<a id="vg-finding-13"></a>
### VG066: Comment for instance mapping `.dib` repeats or closely reuses comment from instance mapping `.dib`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:218`
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

<a id="vg-finding-14"></a>
### VG066: Comment for instance mapping `.addrb` repeats or closely reuses comment from instance mapping `.addrb`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:219`
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

<a id="vg-finding-15"></a>
### VG066: Comment for instance mapping `.ceb` repeats or closely reuses comment from instance mapping `.ceb`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:220`
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

<a id="vg-finding-16"></a>
### VG066: Comment for instance mapping `.oceb` repeats or closely reuses comment from instance mapping `.oceb`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:221`
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

<a id="vg-finding-17"></a>
### VG066: Comment for instance mapping `.clkb` repeats or closely reuses comment from instance mapping `.clkb`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:222`
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

<a id="vg-finding-18"></a>
### VG066: Comment for instance mapping `.web` repeats or closely reuses comment from instance mapping `.web`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:223`
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

<a id="vg-finding-19"></a>
### VG066: Comment for instance mapping `.rstb` repeats or closely reuses comment from instance mapping `.rstb`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:224`
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

<a id="vg-finding-20"></a>
### VG066: Comment for instance mapping `.beb` repeats or closely reuses comment from instance mapping `.beb`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:225`
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

<a id="vg-finding-21"></a>
### VG066: Comment for instance mapping `.ecc_sbiterrinj` repeats or closely reuses comment from instance mapping `.ecc_sbiterrinj`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:226`
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

<a id="vg-finding-22"></a>
### VG066: Comment for instance mapping `.ecc_dbiterrinj` repeats or closely reuses comment from instance mapping `.ecc_dbiterrinj`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:227`
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

<a id="vg-finding-23"></a>
### VG066: Comment for instance mapping `.doa` repeats or closely reuses comment from instance mapping `.doa`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:228`
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

<a id="vg-finding-24"></a>
### VG066: Comment for instance mapping `.dob` repeats or closely reuses comment from instance mapping `.dob`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:229`
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

<a id="vg-finding-25"></a>
### VG066: Comment for instance mapping `.ecc_sbiterr` repeats or closely reuses comment from instance mapping `.ecc_sbiterr`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:230`
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

<a id="vg-finding-26"></a>
### VG066: Comment for instance mapping `.ecc_dbiterr` repeats or closely reuses comment from instance mapping `.ecc_dbiterr`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:231`
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
### VG066: Comment for instance mapping `.DATA_WIDTH_A` repeats or closely reuses comment from instance mapping `.DATA_WIDTH_A`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:236`
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
### VG066: Comment for instance mapping `.DATA_WIDTH_B` repeats or closely reuses comment from instance mapping `.DATA_WIDTH_B`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:237`
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

<a id="vg-finding-29"></a>
### VG066: Comment for instance mapping `.ADDR_WIDTH_A` repeats or closely reuses comment from instance mapping `.ADDR_WIDTH_A`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:238`
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

<a id="vg-finding-30"></a>
### VG066: Comment for instance mapping `.ADDR_WIDTH_B` repeats or closely reuses comment from instance mapping `.ADDR_WIDTH_B`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:239`
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

<a id="vg-finding-31"></a>
### VG066: Comment for instance mapping `.DATA_DEPTH_A` repeats or closely reuses comment from instance mapping `.DATA_DEPTH_A`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:240`
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

<a id="vg-finding-32"></a>
### VG066: Comment for instance mapping `.DATA_DEPTH_B` repeats or closely reuses comment from instance mapping `.DATA_DEPTH_B`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:241`
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

<a id="vg-finding-33"></a>
### VG066: Comment for instance mapping `.BYTE_ENABLE` repeats or closely reuses comment from instance mapping `.BYTE_ENABLE`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:242`
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

<a id="vg-finding-34"></a>
### VG066: Comment for instance mapping `.BYTE_A` repeats or closely reuses comment from instance mapping `.BYTE_A`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:243`
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

<a id="vg-finding-35"></a>
### VG066: Comment for instance mapping `.BYTE_B` repeats or closely reuses comment from instance mapping `.BYTE_B`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:244`
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

<a id="vg-finding-36"></a>
### VG066: Comment for instance mapping `.MODE` repeats or closely reuses comment from instance mapping `.MODE`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:245`
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

<a id="vg-finding-37"></a>
### VG066: Comment for instance mapping `.REGMODE_A` repeats or closely reuses comment from instance mapping `.REGMODE_A`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:246`
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

<a id="vg-finding-38"></a>
### VG066: Comment for instance mapping `.REGMODE_B` repeats or closely reuses comment from instance mapping `.REGMODE_B`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:247`
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

<a id="vg-finding-39"></a>
### VG066: Comment for instance mapping `.WRITEMODE_A` repeats or closely reuses comment from instance mapping `.WRITEMODE_A`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:248`
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

<a id="vg-finding-40"></a>
### VG066: Comment for instance mapping `.WRITEMODE_B` repeats or closely reuses comment from instance mapping `.WRITEMODE_B`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:249`
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

<a id="vg-finding-41"></a>
### VG066: Comment for instance mapping `.RESETMODE_A` repeats or closely reuses comment from instance mapping `.RESETMODE_A`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:250`
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

<a id="vg-finding-42"></a>
### VG066: Comment for instance mapping `.RESETMODE_B` repeats or closely reuses comment from instance mapping `.RESETMODE_B`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:251`
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

<a id="vg-finding-43"></a>
### VG066: Comment for instance mapping `.OREGSET_A` repeats or closely reuses comment from instance mapping `.OREGSET_A`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:252`
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

<a id="vg-finding-44"></a>
### VG066: Comment for instance mapping `.OREGSET_B` repeats or closely reuses comment from instance mapping `.OREGSET_B`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:253`
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

<a id="vg-finding-45"></a>
### VG066: Comment for instance mapping `.SSROVERCE` repeats or closely reuses comment from instance mapping `.SSROVERCE`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:254`
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

<a id="vg-finding-46"></a>
### VG066: Comment for instance mapping `.ECC_DECODE` repeats or closely reuses comment from instance mapping `.ECC_DECODE`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:255`
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

<a id="vg-finding-47"></a>
### VG066: Comment for instance mapping `.ECC_ENCODE` repeats or closely reuses comment from instance mapping `.ECC_ENCODE`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:256`
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

<a id="vg-finding-48"></a>
### VG066: Comment for instance mapping `.ASYNC_RESET_RELEASE_A` repeats or closely reuses comment from instance mapping `.ASYNC_RESET_RELEASE_A`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:257`
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

<a id="vg-finding-49"></a>
### VG066: Comment for instance mapping `.ASYNC_RESET_RELEASE_B` repeats or closely reuses comment from instance mapping `.ASYNC_RESET_RELEASE_B`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:258`
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

<a id="vg-finding-50"></a>
### VG066: Comment for instance mapping `.CLKMODE` repeats or closely reuses comment from instance mapping `.CLKMODE`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:259`
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

<a id="vg-finding-51"></a>
### VG066: Comment for instance mapping `.DEBUGGABLE` repeats or closely reuses comment from instance mapping `.DEBUGGABLE`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:260`
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

<a id="vg-finding-52"></a>
### VG066: Comment for instance mapping `.PACKABLE` repeats or closely reuses comment from instance mapping `.PACKABLE`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:261`
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

<a id="vg-finding-53"></a>
### VG066: Comment for instance mapping `.FORCE_KEEP` repeats or closely reuses comment from instance mapping `.FORCE_KEEP`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:262`
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

<a id="vg-finding-54"></a>
### VG066: Comment for instance mapping `.INIT_FILE` repeats or closely reuses comment from instance mapping `.INIT_FILE`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:263`
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

<a id="vg-finding-55"></a>
### VG066: Comment for instance mapping `.FILL_ALL` repeats or closely reuses comment from instance mapping `.FILL_ALL`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:264`
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

<a id="vg-finding-56"></a>
### VG066: Comment for instance mapping `.REGMODE_B` repeats or closely reuses comment from instance mapping `.REGMODE_B`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:305`
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

<a id="vg-finding-57"></a>
### VG066: Comment for instance mapping `.dia` repeats or closely reuses comment from instance mapping `.dia`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:326`
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

<a id="vg-finding-58"></a>
### VG066: Comment for instance mapping `.addra` repeats or closely reuses comment from instance mapping `.addra`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:327`
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

<a id="vg-finding-59"></a>
### VG066: Comment for instance mapping `.cea` repeats or closely reuses comment from instance mapping `.cea`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:328`
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

<a id="vg-finding-60"></a>
### VG066: Comment for instance mapping `.ocea` repeats or closely reuses comment from instance mapping `.ocea`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:329`
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

<a id="vg-finding-61"></a>
### VG066: Comment for instance mapping `.clka` repeats or closely reuses comment from instance mapping `.clka`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:330`
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

<a id="vg-finding-62"></a>
### VG066: Comment for instance mapping `.wea` repeats or closely reuses comment from instance mapping `.wea`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:331`
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

<a id="vg-finding-63"></a>
### VG066: Comment for instance mapping `.rsta` repeats or closely reuses comment from instance mapping `.rsta`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:332`
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

<a id="vg-finding-64"></a>
### VG066: Comment for instance mapping `.bea` repeats or closely reuses comment from instance mapping `.bea`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:333`
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

<a id="vg-finding-65"></a>
### VG066: Comment for instance mapping `.dib` repeats or closely reuses comment from instance mapping `.dib`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:334`
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

<a id="vg-finding-66"></a>
### VG066: Comment for instance mapping `.addrb` repeats or closely reuses comment from instance mapping `.addrb`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:335`
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

<a id="vg-finding-67"></a>
### VG066: Comment for instance mapping `.ceb` repeats or closely reuses comment from instance mapping `.ceb`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:336`
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

<a id="vg-finding-68"></a>
### VG066: Comment for instance mapping `.oceb` repeats or closely reuses comment from instance mapping `.oceb`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:337`
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

<a id="vg-finding-69"></a>
### VG066: Comment for instance mapping `.clkb` repeats or closely reuses comment from instance mapping `.clkb`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:338`
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

<a id="vg-finding-70"></a>
### VG066: Comment for instance mapping `.web` repeats or closely reuses comment from instance mapping `.web`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:339`
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

<a id="vg-finding-71"></a>
### VG066: Comment for instance mapping `.rstb` repeats or closely reuses comment from instance mapping `.rstb`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:340`
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

<a id="vg-finding-72"></a>
### VG066: Comment for instance mapping `.beb` repeats or closely reuses comment from instance mapping `.beb`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:341`
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

<a id="vg-finding-73"></a>
### VG066: Comment for instance mapping `.ecc_sbiterrinj` repeats or closely reuses comment from instance mapping `.ecc_sbiterrinj`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:342`
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

<a id="vg-finding-74"></a>
### VG066: Comment for instance mapping `.ecc_dbiterrinj` repeats or closely reuses comment from instance mapping `.ecc_dbiterrinj`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:343`
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

<a id="vg-finding-75"></a>
### VG066: Comment for instance mapping `.doa` repeats or closely reuses comment from instance mapping `.doa`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:344`
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

<a id="vg-finding-76"></a>
### VG066: Comment for instance mapping `.dob` repeats or closely reuses comment from instance mapping `.dob`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:345`
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

<a id="vg-finding-77"></a>
### VG066: Comment for instance mapping `.ecc_sbiterr` repeats or closely reuses comment from instance mapping `.ecc_sbiterr`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:346`
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

<a id="vg-finding-78"></a>
### VG066: Comment for instance mapping `.ecc_dbiterr` repeats or closely reuses comment from instance mapping `.ecc_dbiterr`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:347`
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

<a id="vg-finding-79"></a>
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 46.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:96`
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
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 46.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:97`
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
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 46.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:98`
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
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 46.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:124`
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
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 46.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:125`
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
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 46.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:126`
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
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 46.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:129`
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
### VG060: Inline comment must start at display column 48, aligned from region anchor column 48; got 46.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:132`
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
### VG063: Case branch comment must have exactly one blank line above unless it follows a region banner.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:186`
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

<a id="vg-finding-88"></a>
### VG063: Instance comment must have exactly one blank line above unless it follows a region banner.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:579`
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

<a id="vg-finding-89"></a>
### VG063: Instance comment must have exactly one blank line above unless it follows a region banner.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:593`
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

<a id="vg-finding-90"></a>
### VG063: Instance comment must have exactly one blank line above unless it follows a region banner.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:607`
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

<a id="vg-finding-91"></a>
### VG063: Instance comment must have exactly one blank line above unless it follows a region banner.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:621`
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

<a id="vg-finding-92"></a>
### VG063: Instance comment must have exactly one blank line above unless it follows a region banner.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:635`
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

<a id="vg-finding-93"></a>
### VG063: Instance comment must have exactly one blank line above unless it follows a region banner.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:649`
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

<a id="vg-finding-94"></a>
### VG063: Instance comment must have exactly one blank line above unless it follows a region banner.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:663`
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

<a id="vg-finding-95"></a>
### VG063: Instance comment must have exactly one blank line above unless it follows a region banner.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:677`
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

<a id="vg-finding-96"></a>
### VG063: Instance comment must have exactly one blank line above unless it follows a region banner.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:691`
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

<a id="vg-finding-97"></a>
### VG063: Instance comment must have exactly one blank line above unless it follows a region banner.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:705`
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

<a id="vg-finding-98"></a>
### VG063: Instance comment must have exactly one blank line above unless it follows a region banner.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:719`
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

<a id="vg-finding-99"></a>
### VG063: Instance comment must have exactly one blank line above unless it follows a region banner.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:733`
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

<a id="vg-finding-100"></a>
### VG063: Instance comment must have exactly one blank line above unless it follows a region banner.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:747`
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

<a id="vg-finding-101"></a>
### VG063: Instance comment must have exactly one blank line above unless it follows a region banner.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:761`
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

<a id="vg-finding-102"></a>
### VG065: signal `crc_bit_mix` must be introduced by a group comment in `其他信号`.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:135`
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

<a id="vg-finding-103"></a>
### VG066: Comment for signal `group_mu_data` repeats or closely reuses comment from signal `group_beta_data`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:91`
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

<a id="vg-finding-104"></a>
### VG066: Comment for signal `group_nu_data` repeats or closely reuses comment from signal `group_gamma_data`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:92`
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

<a id="vg-finding-105"></a>
### VG066: Comment for signal `group_xi_data` repeats or closely reuses comment from signal `group_delta_data`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:93`
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

<a id="vg-finding-106"></a>
### VG066: Comment for Always block `always@(posedge i_clk or negedge i_rstn)` repeats or closely reuses comment from Always block `always@(posedge i_clk or negedge i_rstn)`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:518`
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

<a id="vg-finding-107"></a>
### VG066: Comment for process assignment `reg_quad_beta` repeats or closely reuses comment from process assignment `reg_quad_alpha`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:521`
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

<a id="vg-finding-108"></a>
### VG066: Comment for process assignment `reg_quad_beta` repeats or closely reuses comment from process assignment `reg_quad_alpha`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:523`
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

<a id="vg-finding-109"></a>
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

<a id="vg-finding-110"></a>
### VG097: 实例参数区、端口区或参数覆盖无法静态解析。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:151`
- Evidence:
- node_kind: `verilog_rtl`
- detail: PH1P_LOGIC_ERAM PH1P_LOGIC_ERAM_Inst_alpha
- source_excerpt: `PH1P_LOGIC_ERAM PH1P_LOGIC_ERAM_Inst_alpha`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
PH1P_LOGIC_ERAM PH1P_LOGIC_ERAM_Inst_alpha
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-111"></a>
### VG097: 实例参数区、端口区或参数覆盖无法静态解析。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:209`
- Evidence:
- node_kind: `verilog_rtl`
- detail: PH1P_LOGIC_ERAM PH1P_LOGIC_ERAM_Inst_beta
- source_excerpt: `PH1P_LOGIC_ERAM PH1P_LOGIC_ERAM_Inst_beta`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
PH1P_LOGIC_ERAM PH1P_LOGIC_ERAM_Inst_beta
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-112"></a>
### VG097: 实例参数区、端口区或参数覆盖无法静态解析。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:267`
- Evidence:
- node_kind: `verilog_rtl`
- detail: PH1P_LOGIC_ERAM PH1P_LOGIC_ERAM_Inst_gamma
- source_excerpt: `PH1P_LOGIC_ERAM PH1P_LOGIC_ERAM_Inst_gamma`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
PH1P_LOGIC_ERAM PH1P_LOGIC_ERAM_Inst_gamma
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-113"></a>
### VG097: 实例参数区、端口区或参数覆盖无法静态解析。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:325`
- Evidence:
- node_kind: `verilog_rtl`
- detail: PH1P_LOGIC_ERAM PH1P_LOGIC_ERAM_Inst_delta
- source_excerpt: `PH1P_LOGIC_ERAM PH1P_LOGIC_ERAM_Inst_delta`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
PH1P_LOGIC_ERAM PH1P_LOGIC_ERAM_Inst_delta
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-114"></a>
### VG097: 实例参数区、端口区或参数覆盖无法静态解析。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_probe.v:580`
- Evidence:
- node_kind: `verilog_rtl`
- detail: road_yolo_numeric_rom_group road_yolo_numeric_rom_group_Inst_alpha
- source_excerpt: `road_yolo_numeric_rom_group road_yolo_numeric_rom_group_Inst_alpha`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
road_yolo_numeric_rom_group road_yolo_numeric_rom_group_Inst_alpha
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-115"></a>
### VG097: 实例参数区、端口区或参数覆盖无法静态解析。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_probe.v:594`
- Evidence:
- node_kind: `verilog_rtl`
- detail: road_yolo_numeric_rom_group road_yolo_numeric_rom_group_Inst_beta
- source_excerpt: `road_yolo_numeric_rom_group road_yolo_numeric_rom_group_Inst_beta`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
road_yolo_numeric_rom_group road_yolo_numeric_rom_group_Inst_beta
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-116"></a>
### VG097: 实例参数区、端口区或参数覆盖无法静态解析。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_probe.v:608`
- Evidence:
- node_kind: `verilog_rtl`
- detail: road_yolo_numeric_rom_group road_yolo_numeric_rom_group_Inst_gamma
- source_excerpt: `road_yolo_numeric_rom_group road_yolo_numeric_rom_group_Inst_gamma`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
road_yolo_numeric_rom_group road_yolo_numeric_rom_group_Inst_gamma
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-117"></a>
### VG097: 实例参数区、端口区或参数覆盖无法静态解析。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_probe.v:622`
- Evidence:
- node_kind: `verilog_rtl`
- detail: road_yolo_numeric_rom_group road_yolo_numeric_rom_group_Inst_delta
- source_excerpt: `road_yolo_numeric_rom_group road_yolo_numeric_rom_group_Inst_delta`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
road_yolo_numeric_rom_group road_yolo_numeric_rom_group_Inst_delta
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-118"></a>
### VG097: 实例参数区、端口区或参数覆盖无法静态解析。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_probe.v:636`
- Evidence:
- node_kind: `verilog_rtl`
- detail: road_yolo_numeric_rom_group road_yolo_numeric_rom_group_Inst_epsilon
- source_excerpt: `road_yolo_numeric_rom_group road_yolo_numeric_rom_group_Inst_epsilon`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
road_yolo_numeric_rom_group road_yolo_numeric_rom_group_Inst_epsilon
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-119"></a>
### VG097: 实例参数区、端口区或参数覆盖无法静态解析。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_probe.v:650`
- Evidence:
- node_kind: `verilog_rtl`
- detail: road_yolo_numeric_rom_group road_yolo_numeric_rom_group_Inst_zeta
- source_excerpt: `road_yolo_numeric_rom_group road_yolo_numeric_rom_group_Inst_zeta`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
road_yolo_numeric_rom_group road_yolo_numeric_rom_group_Inst_zeta
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-120"></a>
### VG097: 实例参数区、端口区或参数覆盖无法静态解析。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_probe.v:664`
- Evidence:
- node_kind: `verilog_rtl`
- detail: road_yolo_numeric_rom_group road_yolo_numeric_rom_group_Inst_eta
- source_excerpt: `road_yolo_numeric_rom_group road_yolo_numeric_rom_group_Inst_eta`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
road_yolo_numeric_rom_group road_yolo_numeric_rom_group_Inst_eta
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-121"></a>
### VG097: 实例参数区、端口区或参数覆盖无法静态解析。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_probe.v:678`
- Evidence:
- node_kind: `verilog_rtl`
- detail: road_yolo_numeric_rom_group road_yolo_numeric_rom_group_Inst_theta
- source_excerpt: `road_yolo_numeric_rom_group road_yolo_numeric_rom_group_Inst_theta`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
road_yolo_numeric_rom_group road_yolo_numeric_rom_group_Inst_theta
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-122"></a>
### VG097: 实例参数区、端口区或参数覆盖无法静态解析。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_probe.v:692`
- Evidence:
- node_kind: `verilog_rtl`
- detail: road_yolo_numeric_rom_group road_yolo_numeric_rom_group_Inst_iota
- source_excerpt: `road_yolo_numeric_rom_group road_yolo_numeric_rom_group_Inst_iota`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
road_yolo_numeric_rom_group road_yolo_numeric_rom_group_Inst_iota
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-123"></a>
### VG097: 实例参数区、端口区或参数覆盖无法静态解析。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_probe.v:706`
- Evidence:
- node_kind: `verilog_rtl`
- detail: road_yolo_numeric_rom_group road_yolo_numeric_rom_group_Inst_kappa
- source_excerpt: `road_yolo_numeric_rom_group road_yolo_numeric_rom_group_Inst_kappa`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
road_yolo_numeric_rom_group road_yolo_numeric_rom_group_Inst_kappa
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-124"></a>
### VG097: 实例参数区、端口区或参数覆盖无法静态解析。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_probe.v:720`
- Evidence:
- node_kind: `verilog_rtl`
- detail: road_yolo_numeric_rom_group road_yolo_numeric_rom_group_Inst_lambda
- source_excerpt: `road_yolo_numeric_rom_group road_yolo_numeric_rom_group_Inst_lambda`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
road_yolo_numeric_rom_group road_yolo_numeric_rom_group_Inst_lambda
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-125"></a>
### VG097: 实例参数区、端口区或参数覆盖无法静态解析。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_probe.v:734`
- Evidence:
- node_kind: `verilog_rtl`
- detail: road_yolo_numeric_rom_group road_yolo_numeric_rom_group_Inst_mu
- source_excerpt: `road_yolo_numeric_rom_group road_yolo_numeric_rom_group_Inst_mu`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
road_yolo_numeric_rom_group road_yolo_numeric_rom_group_Inst_mu
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-126"></a>
### VG097: 实例参数区、端口区或参数覆盖无法静态解析。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_probe.v:748`
- Evidence:
- node_kind: `verilog_rtl`
- detail: road_yolo_numeric_rom_group road_yolo_numeric_rom_group_Inst_nu
- source_excerpt: `road_yolo_numeric_rom_group road_yolo_numeric_rom_group_Inst_nu`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
road_yolo_numeric_rom_group road_yolo_numeric_rom_group_Inst_nu
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-127"></a>
### VG097: 实例参数区、端口区或参数覆盖无法静态解析。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_probe.v:762`
- Evidence:
- node_kind: `verilog_rtl`
- detail: road_yolo_numeric_rom_group road_yolo_numeric_rom_group_Inst_xi
- source_excerpt: `road_yolo_numeric_rom_group road_yolo_numeric_rom_group_Inst_xi`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
road_yolo_numeric_rom_group road_yolo_numeric_rom_group_Inst_xi
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-128"></a>
### VG098: FSM 状态必须能从复位初态到达且具有可证明的后继转移。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_probe.v:76`
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

<a id="vg-finding-129"></a>
### VG098: FSM 状态必须能从复位初态到达且具有可证明的后继转移。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_probe.v:75`
- Evidence:
- node_kind: `verilog_rtl`
- detail: ST_FINISH
- source_excerpt: `ST_FINISH`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
ST_FINISH
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-130"></a>
### VG098: FSM 状态必须能从复位初态到达且具有可证明的后继转移。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_probe.v:74`
- Evidence:
- node_kind: `verilog_rtl`
- detail: ST_GROUP_ADVANCE
- source_excerpt: `ST_GROUP_ADVANCE`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
ST_GROUP_ADVANCE
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-131"></a>
### VG098: FSM 状态必须能从复位初态到达且具有可证明的后继转移。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_probe.v:73`
- Evidence:
- node_kind: `verilog_rtl`
- detail: ST_WORD_INCREMENT
- source_excerpt: `ST_WORD_INCREMENT`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
ST_WORD_INCREMENT
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-132"></a>
### VG122: 算术结果位宽超过赋值目标位宽。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_probe.v:344`
- Evidence:
- node_kind: `verilog_rtl`
- detail: cnt_group_index <= cnt_group_index + 4'd1;
- source_excerpt: `cnt_group_index <= cnt_group_index + 4'd1;`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
cnt_group_index <= cnt_group_index + 4'd1;
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-133"></a>
### VG122: 算术结果位宽超过赋值目标位宽。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_probe.v:355`
- Evidence:
- node_kind: `verilog_rtl`
- detail: cnt_word_addr <= cnt_word_addr + 9'd1;
- source_excerpt: `cnt_word_addr <= cnt_word_addr + 9'd1;`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
cnt_word_addr <= cnt_word_addr + 9'd1;
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-134"></a>
### VG122: 算术结果位宽超过赋值目标位宽。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_probe.v:370`
- Evidence:
- node_kind: `verilog_rtl`
- detail: cnt_bit_index <= cnt_bit_index + 8'd1;
- source_excerpt: `cnt_bit_index <= cnt_bit_index + 8'd1;`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
cnt_bit_index <= cnt_bit_index + 8'd1;
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-135"></a>
### VG125: 字面量声明为 4 位，但实际值只需要 1 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_probe.v:344`
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

<a id="vg-finding-136"></a>
### VG125: 字面量声明为 9 位，但实际值只需要 1 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_probe.v:355`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 9'd1
- source_excerpt: `9'd1`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
9'd1
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-137"></a>
### VG125: 字面量声明为 8 位，但实际值只需要 1 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_probe.v:370`
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

<a id="vg-finding-138"></a>
### VG132: 时钟信号连接到了非时钟实例端口。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:156`
- Evidence:
- node_kind: `verilog_rtl`
- detail: .clka(i_clk)
- source_excerpt: `.clka(i_clk)`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
.clka(i_clk)
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-139"></a>
### VG132: 时钟信号连接到了非时钟实例端口。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:164`
- Evidence:
- node_kind: `verilog_rtl`
- detail: .clkb(i_clk)
- source_excerpt: `.clkb(i_clk)`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
.clkb(i_clk)
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-140"></a>
### VG132: 时钟信号连接到了非时钟实例端口。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:214`
- Evidence:
- node_kind: `verilog_rtl`
- detail: .clka(i_clk)
- source_excerpt: `.clka(i_clk)`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
.clka(i_clk)
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-141"></a>
### VG132: 时钟信号连接到了非时钟实例端口。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:222`
- Evidence:
- node_kind: `verilog_rtl`
- detail: .clkb(i_clk)
- source_excerpt: `.clkb(i_clk)`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
.clkb(i_clk)
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-142"></a>
### VG132: 时钟信号连接到了非时钟实例端口。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:272`
- Evidence:
- node_kind: `verilog_rtl`
- detail: .clka(i_clk)
- source_excerpt: `.clka(i_clk)`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
.clka(i_clk)
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-143"></a>
### VG132: 时钟信号连接到了非时钟实例端口。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:280`
- Evidence:
- node_kind: `verilog_rtl`
- detail: .clkb(i_clk)
- source_excerpt: `.clkb(i_clk)`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
.clkb(i_clk)
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-144"></a>
### VG132: 时钟信号连接到了非时钟实例端口。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:330`
- Evidence:
- node_kind: `verilog_rtl`
- detail: .clka(i_clk)
- source_excerpt: `.clka(i_clk)`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
.clka(i_clk)
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-145"></a>
### VG132: 时钟信号连接到了非时钟实例端口。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:338`
- Evidence:
- node_kind: `verilog_rtl`
- detail: .clkb(i_clk)
- source_excerpt: `.clkb(i_clk)`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
.clkb(i_clk)
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-146"></a>
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

<a id="vg-finding-147"></a>
### VG138: 常量未显式声明位宽和进制。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_yolo_numeric_rom_group.v:76`
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

<a id="vg-finding-148"></a>
### VG138: 常量未显式声明位宽和进制。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_yolo_numeric_rom_group.v:77`
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

<a id="vg-finding-149"></a>
### VG138: 常量未显式声明位宽和进制。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_yolo_numeric_rom_group.v:81`
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

<a id="vg-finding-150"></a>
### VG138: 常量未显式声明位宽和进制。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_yolo_numeric_rom_group.v:92`
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

<a id="vg-finding-151"></a>
### VG138: 常量未显式声明位宽和进制。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_yolo_numeric_rom_group.v:102`
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

<a id="vg-finding-152"></a>
### VG138: 常量未显式声明位宽和进制。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_yolo_numeric_rom_group.v:111`
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

<a id="vg-finding-153"></a>
### VG138: 常量未显式声明位宽和进制。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_yolo_numeric_rom_probe.v:96`
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

<a id="vg-finding-154"></a>
### VG138: 常量未显式声明位宽和进制。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_yolo_numeric_rom_probe.v:97`
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

<a id="vg-finding-155"></a>
### VG138: 常量未显式声明位宽和进制。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_yolo_numeric_rom_probe.v:98`
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

<a id="vg-finding-156"></a>
### VG138: 常量未显式声明位宽和进制。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_yolo_numeric_rom_probe.v:101`
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

<a id="vg-finding-157"></a>
### VG138: 常量未显式声明位宽和进制。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_yolo_numeric_rom_probe.v:102`
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

<a id="vg-finding-158"></a>
### VG138: 常量未显式声明位宽和进制。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_yolo_numeric_rom_probe.v:105`
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

<a id="vg-finding-159"></a>
### VG138: 常量未显式声明位宽和进制。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_yolo_numeric_rom_probe.v:106`
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

<a id="vg-finding-160"></a>
### VG138: 常量未显式声明位宽和进制。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_yolo_numeric_rom_probe.v:107`
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

<a id="vg-finding-161"></a>
### VG138: 常量未显式声明位宽和进制。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_yolo_numeric_rom_probe.v:108`
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

<a id="vg-finding-162"></a>
### VG138: 常量未显式声明位宽和进制。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_yolo_numeric_rom_probe.v:109`
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

<a id="vg-finding-163"></a>
### VG138: 常量未显式声明位宽和进制。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_yolo_numeric_rom_probe.v:110`
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

<a id="vg-finding-164"></a>
### VG138: 常量未显式声明位宽和进制。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_yolo_numeric_rom_probe.v:111`
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

<a id="vg-finding-165"></a>
### VG138: 常量未显式声明位宽和进制。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_yolo_numeric_rom_probe.v:112`
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

<a id="vg-finding-166"></a>
### VG138: 常量未显式声明位宽和进制。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_yolo_numeric_rom_probe.v:113`
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

<a id="vg-finding-167"></a>
### VG138: 常量未显式声明位宽和进制。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_yolo_numeric_rom_probe.v:114`
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

<a id="vg-finding-168"></a>
### VG138: 常量未显式声明位宽和进制。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_yolo_numeric_rom_probe.v:115`
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

<a id="vg-finding-169"></a>
### VG138: 常量未显式声明位宽和进制。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_yolo_numeric_rom_probe.v:116`
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

<a id="vg-finding-170"></a>
### VG138: 常量未显式声明位宽和进制。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_yolo_numeric_rom_probe.v:117`
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

<a id="vg-finding-171"></a>
### VG138: 常量未显式声明位宽和进制。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_yolo_numeric_rom_probe.v:118`
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

<a id="vg-finding-172"></a>
### VG138: 常量未显式声明位宽和进制。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_yolo_numeric_rom_probe.v:119`
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

<a id="vg-finding-173"></a>
### VG138: 常量未显式声明位宽和进制。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_yolo_numeric_rom_probe.v:120`
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

<a id="vg-finding-174"></a>
### VG138: 常量未显式声明位宽和进制。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_yolo_numeric_rom_probe.v:121`
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

<a id="vg-finding-175"></a>
### VG138: 常量未显式声明位宽和进制。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_yolo_numeric_rom_probe.v:124`
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

<a id="vg-finding-176"></a>
### VG138: 常量未显式声明位宽和进制。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_yolo_numeric_rom_probe.v:129`
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

<a id="vg-finding-177"></a>
### VG138: 常量未显式声明位宽和进制。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_yolo_numeric_rom_probe.v:132`
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

<a id="vg-finding-178"></a>
### VG138: 常量未显式声明位宽和进制。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_yolo_numeric_rom_probe.v:141`
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

<a id="vg-finding-179"></a>
### VG138: 常量未显式声明位宽和进制。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_yolo_numeric_rom_probe.v:142`
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

<a id="vg-finding-180"></a>
### VG138: 常量未显式声明位宽和进制。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_yolo_numeric_rom_probe.v:173`
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

<a id="vg-finding-181"></a>
### VG138: 常量未显式声明位宽和进制。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_yolo_numeric_rom_probe.v:299`
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

<a id="vg-finding-182"></a>
### VG138: 常量未显式声明位宽和进制。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_yolo_numeric_rom_probe.v:333`
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

<a id="vg-finding-183"></a>
### VG138: 常量未显式声明位宽和进制。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_yolo_numeric_rom_probe.v:342`
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

<a id="vg-finding-184"></a>
### VG138: 常量未显式声明位宽和进制。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_yolo_numeric_rom_probe.v:353`
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

<a id="vg-finding-185"></a>
### VG138: 常量未显式声明位宽和进制。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_yolo_numeric_rom_probe.v:357`
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

<a id="vg-finding-186"></a>
### VG138: 常量未显式声明位宽和进制。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_yolo_numeric_rom_probe.v:366`
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

<a id="vg-finding-187"></a>
### VG138: 常量未显式声明位宽和进制。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_yolo_numeric_rom_probe.v:368`
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

<a id="vg-finding-188"></a>
### VG138: 常量未显式声明位宽和进制。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_yolo_numeric_rom_probe.v:379`
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

<a id="vg-finding-189"></a>
### VG138: 常量未显式声明位宽和进制。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_yolo_numeric_rom_probe.v:412`
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

<a id="vg-finding-190"></a>
### VG138: 常量未显式声明位宽和进制。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_yolo_numeric_rom_probe.v:427`
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

<a id="vg-finding-191"></a>
### VG138: 常量未显式声明位宽和进制。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_yolo_numeric_rom_probe.v:449`
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

<a id="vg-finding-192"></a>
### VG138: 常量未显式声明位宽和进制。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_yolo_numeric_rom_probe.v:458`
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

<a id="vg-finding-193"></a>
### VG138: 常量未显式声明位宽和进制。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_yolo_numeric_rom_probe.v:467`
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

<a id="vg-finding-194"></a>
### VG138: 常量未显式声明位宽和进制。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_yolo_numeric_rom_probe.v:476`
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

<a id="vg-finding-195"></a>
### VG138: 常量未显式声明位宽和进制。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_yolo_numeric_rom_probe.v:485`
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

<a id="vg-finding-196"></a>
### VG138: 常量未显式声明位宽和进制。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_yolo_numeric_rom_probe.v:494`
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

<a id="vg-finding-197"></a>
### VG138: 常量未显式声明位宽和进制。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_yolo_numeric_rom_probe.v:503`
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

<a id="vg-finding-198"></a>
### VG138: 常量未显式声明位宽和进制。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_yolo_numeric_rom_probe.v:512`
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

<a id="vg-finding-199"></a>
### VG138: 常量未显式声明位宽和进制。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_yolo_numeric_rom_probe.v:521`
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

<a id="vg-finding-200"></a>
### VG138: 常量未显式声明位宽和进制。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_yolo_numeric_rom_probe.v:530`
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

<a id="vg-finding-201"></a>
### VG138: 常量未显式声明位宽和进制。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_yolo_numeric_rom_probe.v:539`
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

<a id="vg-finding-202"></a>
### VG138: 常量未显式声明位宽和进制。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_yolo_numeric_rom_probe.v:548`
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

<a id="vg-finding-203"></a>
### VG138: 常量未显式声明位宽和进制。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_yolo_numeric_rom_probe.v:557`
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

<a id="vg-finding-204"></a>
### VG138: 常量未显式声明位宽和进制。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_yolo_numeric_rom_probe.v:566`
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

<a id="vg-finding-205"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_group.v:road_yolo_numeric_rom_group@49:1-350:1; instance_path=road_yolo_numeric_rom_group; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_group.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_group.v:road_yolo_numeric_rom_group@49:1-350:1; instance_path=road_yolo_numeric_rom_group; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_group.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_group.v:road_yolo_numeric_rom_group@49:1-350:1; instance_path=road_yolo_numeric_rom_group; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_group.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-206"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_group.v:road_yolo_numeric_rom_group@49:1-350:1; instance_path=road_yolo_numeric_rom_group; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_group.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_group.v:road_yolo_numeric_rom_group@49:1-350:1; instance_path=road_yolo_numeric_rom_group; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_group.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_group.v:road_yolo_numeric_rom_group@49:1-350:1; instance_path=road_yolo_numeric_rom_group; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_group.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-207"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_group.v:road_yolo_numeric_rom_group@49:1-350:1; instance_path=road_yolo_numeric_rom_group; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_group.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_group.v:road_yolo_numeric_rom_group@49:1-350:1; instance_path=road_yolo_numeric_rom_group; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_group.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_group.v:road_yolo_numeric_rom_group@49:1-350:1; instance_path=road_yolo_numeric_rom_group; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_group.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-208"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_group.v:road_yolo_numeric_rom_group@49:1-350:1; instance_path=road_yolo_numeric_rom_group; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_group.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_group.v:road_yolo_numeric_rom_group@49:1-350:1; instance_path=road_yolo_numeric_rom_group; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_group.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_group.v:road_yolo_numeric_rom_group@49:1-350:1; instance_path=road_yolo_numeric_rom_group; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_group.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-209"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_group.v:road_yolo_numeric_rom_group@49:1-350:1; instance_path=road_yolo_numeric_rom_group; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_lower_pair$D; child_output=road_yolo_numeric_rom_group.reg_lower_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_group.v:road_yolo_numeric_rom_group@49:1-350:1; instance_path=road_yolo_numeric_rom_group; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_lower_pair$D; child_output=road_yolo_numeric_rom_group.reg_lower_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_group.v:road_yolo_numeric_rom_group@49:1-350:1; instance_path=road_yolo_numeric_rom_group; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_lower_pair$D; child_output=road_yolo_numeric_rom_group.reg_lower_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-210"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_group.v:road_yolo_numeric_rom_group@49:1-350:1; instance_path=road_yolo_numeric_rom_group; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_upper_pair$D; child_output=road_yolo_numeric_rom_group.reg_upper_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_group.v:road_yolo_numeric_rom_group@49:1-350:1; instance_path=road_yolo_numeric_rom_group; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_upper_pair$D; child_output=road_yolo_numeric_rom_group.reg_upper_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_group.v:road_yolo_numeric_rom_group@49:1-350:1; instance_path=road_yolo_numeric_rom_group; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_upper_pair$D; child_output=road_yolo_numeric_rom_group.reg_upper_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-211"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_alpha; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_alpha.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_alpha; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_alpha.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_alpha; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_alpha.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-212"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_alpha; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_alpha.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_alpha; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_alpha.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_alpha; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_alpha.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-213"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_alpha; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_alpha.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_alpha; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_alpha.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_alpha; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_alpha.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-214"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_alpha; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_alpha.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_alpha; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_alpha.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_alpha; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_alpha.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-215"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_alpha; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_lower_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_alpha.reg_lower_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_alpha; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_lower_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_alpha.reg_lower_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_alpha; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_lower_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_alpha.reg_lower_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-216"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_alpha; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_upper_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_alpha.reg_upper_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_alpha; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_upper_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_alpha.reg_upper_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_alpha; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_upper_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_alpha.reg_upper_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-217"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_beta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_beta.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_beta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_beta.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_beta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_beta.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-218"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_beta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_beta.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_beta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_beta.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_beta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_beta.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-219"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_beta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_beta.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_beta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_beta.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_beta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_beta.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-220"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_beta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_beta.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_beta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_beta.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_beta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_beta.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-221"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_beta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_lower_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_beta.reg_lower_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_beta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_lower_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_beta.reg_lower_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_beta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_lower_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_beta.reg_lower_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-222"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_beta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_upper_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_beta.reg_upper_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_beta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_upper_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_beta.reg_upper_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_beta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_upper_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_beta.reg_upper_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-223"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_delta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_delta.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_delta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_delta.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_delta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_delta.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-224"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_delta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_delta.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_delta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_delta.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_delta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_delta.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-225"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_delta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_delta.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_delta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_delta.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_delta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_delta.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-226"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_delta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_delta.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_delta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_delta.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_delta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_delta.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-227"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_delta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_lower_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_delta.reg_lower_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_delta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_lower_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_delta.reg_lower_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_delta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_lower_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_delta.reg_lower_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-228"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_delta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_upper_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_delta.reg_upper_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_delta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_upper_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_delta.reg_upper_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_delta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_upper_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_delta.reg_upper_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-229"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_epsilon; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_epsilon.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_epsilon; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_epsilon.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_epsilon; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_epsilon.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-230"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_epsilon; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_epsilon.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_epsilon; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_epsilon.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_epsilon; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_epsilon.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-231"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_epsilon; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_epsilon.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_epsilon; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_epsilon.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_epsilon; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_epsilon.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-232"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_epsilon; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_epsilon.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_epsilon; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_epsilon.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_epsilon; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_epsilon.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-233"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_epsilon; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_lower_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_epsilon.reg_lower_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_epsilon; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_lower_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_epsilon.reg_lower_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_epsilon; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_lower_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_epsilon.reg_lower_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-234"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_epsilon; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_upper_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_epsilon.reg_upper_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_epsilon; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_upper_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_epsilon.reg_upper_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_epsilon; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_upper_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_epsilon.reg_upper_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-235"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_eta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_eta.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_eta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_eta.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_eta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_eta.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-236"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_eta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_eta.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_eta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_eta.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_eta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_eta.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-237"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_eta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_eta.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_eta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_eta.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_eta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_eta.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-238"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_eta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_eta.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_eta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_eta.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_eta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_eta.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-239"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_eta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_lower_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_eta.reg_lower_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_eta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_lower_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_eta.reg_lower_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_eta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_lower_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_eta.reg_lower_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-240"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_eta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_upper_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_eta.reg_upper_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_eta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_upper_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_eta.reg_upper_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_eta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_upper_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_eta.reg_upper_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-241"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_gamma; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_gamma.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_gamma; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_gamma.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_gamma; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_gamma.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-242"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_gamma; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_gamma.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_gamma; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_gamma.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_gamma; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_gamma.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-243"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_gamma; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_gamma.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_gamma; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_gamma.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_gamma; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_gamma.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-244"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_gamma; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_gamma.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_gamma; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_gamma.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_gamma; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_gamma.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-245"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_gamma; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_lower_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_gamma.reg_lower_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_gamma; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_lower_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_gamma.reg_lower_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_gamma; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_lower_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_gamma.reg_lower_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-246"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_gamma; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_upper_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_gamma.reg_upper_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_gamma; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_upper_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_gamma.reg_upper_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_gamma; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_upper_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_gamma.reg_upper_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-247"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_iota; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_iota.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_iota; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_iota.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_iota; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_iota.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-248"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_iota; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_iota.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_iota; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_iota.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_iota; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_iota.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-249"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_iota; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_iota.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_iota; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_iota.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_iota; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_iota.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-250"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_iota; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_iota.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_iota; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_iota.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_iota; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_iota.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-251"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_iota; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_lower_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_iota.reg_lower_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_iota; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_lower_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_iota.reg_lower_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_iota; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_lower_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_iota.reg_lower_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-252"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_iota; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_upper_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_iota.reg_upper_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_iota; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_upper_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_iota.reg_upper_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_iota; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_upper_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_iota.reg_upper_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-253"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_kappa; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_kappa.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_kappa; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_kappa.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_kappa; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_kappa.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-254"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_kappa; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_kappa.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_kappa; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_kappa.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_kappa; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_kappa.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-255"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_kappa; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_kappa.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_kappa; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_kappa.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_kappa; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_kappa.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-256"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_kappa; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_kappa.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_kappa; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_kappa.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_kappa; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_kappa.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-257"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_kappa; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_lower_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_kappa.reg_lower_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_kappa; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_lower_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_kappa.reg_lower_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_kappa; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_lower_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_kappa.reg_lower_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-258"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_kappa; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_upper_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_kappa.reg_upper_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_kappa; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_upper_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_kappa.reg_upper_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_kappa; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_upper_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_kappa.reg_upper_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-259"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_lambda; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_lambda.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_lambda; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_lambda.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_lambda; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_lambda.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-260"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_lambda; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_lambda.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_lambda; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_lambda.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_lambda; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_lambda.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-261"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_lambda; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_lambda.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_lambda; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_lambda.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_lambda; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_lambda.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-262"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_lambda; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_lambda.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_lambda; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_lambda.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_lambda; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_lambda.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-263"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_lambda; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_lower_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_lambda.reg_lower_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_lambda; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_lower_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_lambda.reg_lower_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_lambda; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_lower_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_lambda.reg_lower_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-264"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_lambda; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_upper_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_lambda.reg_upper_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_lambda; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_upper_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_lambda.reg_upper_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_lambda; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_upper_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_lambda.reg_upper_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-265"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_mu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_mu.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_mu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_mu.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_mu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_mu.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-266"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_mu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_mu.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_mu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_mu.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_mu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_mu.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-267"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_mu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_mu.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_mu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_mu.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_mu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_mu.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-268"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_mu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_mu.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_mu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_mu.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_mu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_mu.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-269"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_mu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_lower_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_mu.reg_lower_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_mu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_lower_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_mu.reg_lower_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_mu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_lower_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_mu.reg_lower_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-270"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_mu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_upper_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_mu.reg_upper_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_mu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_upper_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_mu.reg_upper_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_mu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_upper_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_mu.reg_upper_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-271"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_nu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_nu.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_nu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_nu.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_nu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_nu.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-272"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_nu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_nu.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_nu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_nu.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_nu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_nu.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-273"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_nu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_nu.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_nu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_nu.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_nu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_nu.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-274"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_nu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_nu.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_nu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_nu.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_nu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_nu.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-275"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_nu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_lower_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_nu.reg_lower_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_nu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_lower_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_nu.reg_lower_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_nu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_lower_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_nu.reg_lower_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-276"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_nu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_upper_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_nu.reg_upper_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_nu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_upper_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_nu.reg_upper_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_nu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_upper_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_nu.reg_upper_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-277"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_theta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_theta.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_theta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_theta.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_theta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_theta.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-278"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_theta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_theta.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_theta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_theta.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_theta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_theta.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-279"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_theta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_theta.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_theta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_theta.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_theta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_theta.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-280"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_theta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_theta.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_theta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_theta.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_theta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_theta.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-281"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_theta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_lower_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_theta.reg_lower_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_theta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_lower_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_theta.reg_lower_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_theta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_lower_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_theta.reg_lower_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-282"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_theta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_upper_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_theta.reg_upper_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_theta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_upper_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_theta.reg_upper_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_theta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_upper_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_theta.reg_upper_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-283"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_xi; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_xi.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_xi; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_xi.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_xi; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_xi.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-284"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_xi; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_xi.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_xi; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_xi.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_xi; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_xi.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-285"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_xi; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_xi.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_xi; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_xi.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_xi; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_xi.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-286"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_xi; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_xi.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_xi; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_xi.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_xi; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_xi.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-287"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_xi; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_lower_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_xi.reg_lower_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_xi; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_lower_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_xi.reg_lower_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_xi; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_lower_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_xi.reg_lower_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-288"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_xi; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_upper_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_xi.reg_upper_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_xi; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_upper_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_xi.reg_upper_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_xi; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_upper_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_xi.reg_upper_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-289"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_zeta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_zeta.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_zeta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_zeta.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_zeta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_zeta.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-290"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_zeta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_zeta.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_zeta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_zeta.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_zeta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_zeta.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-291"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_zeta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_zeta.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_zeta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_zeta.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_zeta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_zeta.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-292"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_zeta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_zeta.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_zeta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_zeta.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_zeta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_zeta.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-293"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_zeta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_lower_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_zeta.reg_lower_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_zeta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_lower_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_zeta.reg_lower_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_zeta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_lower_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_zeta.reg_lower_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-294"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_zeta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_upper_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_zeta.reg_upper_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_zeta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_upper_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_zeta.reg_upper_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_zeta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_upper_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_zeta.reg_upper_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-295"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_group.v:road_yolo_numeric_rom_group@49:1-350:1; instance_path=road_yolo_numeric_rom_group; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_group.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_group.v:road_yolo_numeric_rom_group@49:1-350:1; instance_path=road_yolo_numeric_rom_group; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_group.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_group.v:road_yolo_numeric_rom_group@49:1-350:1; instance_path=road_yolo_numeric_rom_group; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_group.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-296"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_group.v:road_yolo_numeric_rom_group@49:1-350:1; instance_path=road_yolo_numeric_rom_group; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_group.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_group.v:road_yolo_numeric_rom_group@49:1-350:1; instance_path=road_yolo_numeric_rom_group; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_group.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_group.v:road_yolo_numeric_rom_group@49:1-350:1; instance_path=road_yolo_numeric_rom_group; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_group.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-297"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_group.v:road_yolo_numeric_rom_group@49:1-350:1; instance_path=road_yolo_numeric_rom_group; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_group.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_group.v:road_yolo_numeric_rom_group@49:1-350:1; instance_path=road_yolo_numeric_rom_group; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_group.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_group.v:road_yolo_numeric_rom_group@49:1-350:1; instance_path=road_yolo_numeric_rom_group; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_group.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-298"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_group.v:road_yolo_numeric_rom_group@49:1-350:1; instance_path=road_yolo_numeric_rom_group; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_group.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_group.v:road_yolo_numeric_rom_group@49:1-350:1; instance_path=road_yolo_numeric_rom_group; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_group.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_group.v:road_yolo_numeric_rom_group@49:1-350:1; instance_path=road_yolo_numeric_rom_group; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_group.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-299"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_group.v:road_yolo_numeric_rom_group@49:1-350:1; instance_path=road_yolo_numeric_rom_group; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_lower_pair$D; child_output=road_yolo_numeric_rom_group.reg_lower_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_group.v:road_yolo_numeric_rom_group@49:1-350:1; instance_path=road_yolo_numeric_rom_group; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_lower_pair$D; child_output=road_yolo_numeric_rom_group.reg_lower_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_group.v:road_yolo_numeric_rom_group@49:1-350:1; instance_path=road_yolo_numeric_rom_group; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_lower_pair$D; child_output=road_yolo_numeric_rom_group.reg_lower_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-300"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_group.v:road_yolo_numeric_rom_group@49:1-350:1; instance_path=road_yolo_numeric_rom_group; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_upper_pair$D; child_output=road_yolo_numeric_rom_group.reg_upper_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_group.v:road_yolo_numeric_rom_group@49:1-350:1; instance_path=road_yolo_numeric_rom_group; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_upper_pair$D; child_output=road_yolo_numeric_rom_group.reg_upper_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_group.v:road_yolo_numeric_rom_group@49:1-350:1; instance_path=road_yolo_numeric_rom_group; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_upper_pair$D; child_output=road_yolo_numeric_rom_group.reg_upper_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-301"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_alpha; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_alpha.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_alpha; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_alpha.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_alpha; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_alpha.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-302"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_alpha; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_alpha.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_alpha; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_alpha.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_alpha; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_alpha.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-303"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_alpha; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_alpha.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_alpha; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_alpha.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_alpha; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_alpha.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-304"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_alpha; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_alpha.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_alpha; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_alpha.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_alpha; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_alpha.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-305"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_alpha; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_lower_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_alpha.reg_lower_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_alpha; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_lower_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_alpha.reg_lower_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_alpha; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_lower_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_alpha.reg_lower_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-306"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_alpha; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_upper_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_alpha.reg_upper_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_alpha; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_upper_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_alpha.reg_upper_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_alpha; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_upper_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_alpha.reg_upper_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-307"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_beta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_beta.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_beta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_beta.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_beta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_beta.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-308"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_beta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_beta.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_beta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_beta.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_beta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_beta.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-309"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_beta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_beta.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_beta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_beta.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_beta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_beta.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-310"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_beta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_beta.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_beta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_beta.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_beta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_beta.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-311"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_beta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_lower_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_beta.reg_lower_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_beta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_lower_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_beta.reg_lower_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_beta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_lower_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_beta.reg_lower_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-312"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_beta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_upper_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_beta.reg_upper_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_beta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_upper_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_beta.reg_upper_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_beta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_upper_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_beta.reg_upper_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-313"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_delta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_delta.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_delta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_delta.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_delta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_delta.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-314"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_delta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_delta.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_delta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_delta.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_delta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_delta.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-315"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_delta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_delta.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_delta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_delta.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_delta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_delta.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-316"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_delta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_delta.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_delta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_delta.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_delta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_delta.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-317"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_delta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_lower_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_delta.reg_lower_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_delta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_lower_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_delta.reg_lower_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_delta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_lower_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_delta.reg_lower_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-318"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_delta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_upper_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_delta.reg_upper_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_delta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_upper_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_delta.reg_upper_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_delta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_upper_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_delta.reg_upper_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-319"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_epsilon; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_epsilon.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_epsilon; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_epsilon.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_epsilon; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_epsilon.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-320"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_epsilon; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_epsilon.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_epsilon; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_epsilon.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_epsilon; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_epsilon.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-321"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_epsilon; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_epsilon.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_epsilon; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_epsilon.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_epsilon; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_epsilon.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-322"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_epsilon; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_epsilon.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_epsilon; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_epsilon.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_epsilon; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_epsilon.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-323"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_epsilon; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_lower_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_epsilon.reg_lower_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_epsilon; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_lower_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_epsilon.reg_lower_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_epsilon; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_lower_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_epsilon.reg_lower_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-324"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_epsilon; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_upper_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_epsilon.reg_upper_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_epsilon; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_upper_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_epsilon.reg_upper_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_epsilon; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_upper_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_epsilon.reg_upper_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-325"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_eta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_eta.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_eta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_eta.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_eta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_eta.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-326"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_eta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_eta.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_eta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_eta.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_eta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_eta.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-327"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_eta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_eta.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_eta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_eta.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_eta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_eta.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-328"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_eta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_eta.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_eta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_eta.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_eta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_eta.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-329"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_eta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_lower_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_eta.reg_lower_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_eta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_lower_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_eta.reg_lower_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_eta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_lower_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_eta.reg_lower_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-330"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_eta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_upper_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_eta.reg_upper_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_eta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_upper_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_eta.reg_upper_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_eta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_upper_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_eta.reg_upper_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-331"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_gamma; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_gamma.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_gamma; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_gamma.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_gamma; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_gamma.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-332"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_gamma; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_gamma.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_gamma; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_gamma.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_gamma; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_gamma.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-333"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_gamma; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_gamma.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_gamma; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_gamma.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_gamma; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_gamma.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-334"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_gamma; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_gamma.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_gamma; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_gamma.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_gamma; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_gamma.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-335"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_gamma; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_lower_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_gamma.reg_lower_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_gamma; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_lower_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_gamma.reg_lower_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_gamma; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_lower_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_gamma.reg_lower_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-336"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_gamma; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_upper_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_gamma.reg_upper_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_gamma; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_upper_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_gamma.reg_upper_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_gamma; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_upper_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_gamma.reg_upper_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-337"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_iota; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_iota.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_iota; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_iota.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_iota; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_iota.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-338"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_iota; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_iota.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_iota; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_iota.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_iota; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_iota.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-339"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_iota; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_iota.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_iota; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_iota.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_iota; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_iota.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-340"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_iota; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_iota.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_iota; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_iota.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_iota; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_iota.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-341"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_iota; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_lower_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_iota.reg_lower_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_iota; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_lower_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_iota.reg_lower_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_iota; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_lower_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_iota.reg_lower_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-342"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_iota; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_upper_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_iota.reg_upper_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_iota; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_upper_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_iota.reg_upper_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_iota; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_upper_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_iota.reg_upper_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-343"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_kappa; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_kappa.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_kappa; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_kappa.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_kappa; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_kappa.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-344"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_kappa; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_kappa.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_kappa; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_kappa.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_kappa; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_kappa.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-345"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_kappa; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_kappa.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_kappa; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_kappa.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_kappa; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_kappa.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-346"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_kappa; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_kappa.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_kappa; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_kappa.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_kappa; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_kappa.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-347"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_kappa; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_lower_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_kappa.reg_lower_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_kappa; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_lower_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_kappa.reg_lower_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_kappa; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_lower_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_kappa.reg_lower_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-348"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_kappa; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_upper_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_kappa.reg_upper_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_kappa; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_upper_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_kappa.reg_upper_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_kappa; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_upper_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_kappa.reg_upper_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-349"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_lambda; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_lambda.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_lambda; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_lambda.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_lambda; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_lambda.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-350"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_lambda; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_lambda.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_lambda; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_lambda.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_lambda; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_lambda.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-351"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_lambda; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_lambda.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_lambda; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_lambda.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_lambda; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_lambda.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-352"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_lambda; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_lambda.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_lambda; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_lambda.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_lambda; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_lambda.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-353"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_lambda; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_lower_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_lambda.reg_lower_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_lambda; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_lower_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_lambda.reg_lower_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_lambda; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_lower_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_lambda.reg_lower_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-354"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_lambda; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_upper_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_lambda.reg_upper_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_lambda; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_upper_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_lambda.reg_upper_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_lambda; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_upper_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_lambda.reg_upper_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-355"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_mu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_mu.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_mu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_mu.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_mu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_mu.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-356"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_mu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_mu.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_mu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_mu.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_mu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_mu.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-357"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_mu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_mu.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_mu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_mu.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_mu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_mu.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-358"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_mu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_mu.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_mu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_mu.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_mu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_mu.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-359"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_mu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_lower_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_mu.reg_lower_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_mu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_lower_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_mu.reg_lower_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_mu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_lower_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_mu.reg_lower_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-360"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_mu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_upper_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_mu.reg_upper_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_mu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_upper_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_mu.reg_upper_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_mu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_upper_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_mu.reg_upper_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-361"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_nu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_nu.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_nu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_nu.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_nu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_nu.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-362"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_nu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_nu.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_nu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_nu.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_nu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_nu.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-363"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_nu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_nu.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_nu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_nu.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_nu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_nu.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-364"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_nu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_nu.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_nu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_nu.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_nu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_nu.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-365"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_nu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_lower_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_nu.reg_lower_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_nu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_lower_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_nu.reg_lower_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_nu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_lower_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_nu.reg_lower_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-366"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_nu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_upper_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_nu.reg_upper_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_nu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_upper_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_nu.reg_upper_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_nu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_upper_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_nu.reg_upper_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-367"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_theta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_theta.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_theta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_theta.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_theta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_theta.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-368"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_theta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_theta.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_theta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_theta.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_theta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_theta.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-369"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_theta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_theta.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_theta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_theta.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_theta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_theta.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-370"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_theta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_theta.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_theta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_theta.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_theta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_theta.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-371"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_theta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_lower_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_theta.reg_lower_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_theta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_lower_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_theta.reg_lower_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_theta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_lower_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_theta.reg_lower_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-372"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_theta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_upper_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_theta.reg_upper_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_theta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_upper_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_theta.reg_upper_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_theta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_upper_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_theta.reg_upper_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-373"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_xi; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_xi.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_xi; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_xi.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_xi; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_xi.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-374"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_xi; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_xi.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_xi; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_xi.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_xi; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_xi.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-375"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_xi; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_xi.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_xi; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_xi.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_xi; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_xi.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-376"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_xi; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_xi.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_xi; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_xi.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_xi; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_xi.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-377"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_xi; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_lower_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_xi.reg_lower_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_xi; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_lower_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_xi.reg_lower_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_xi; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_lower_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_xi.reg_lower_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-378"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_xi; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_upper_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_xi.reg_upper_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_xi; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_upper_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_xi.reg_upper_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_xi; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_upper_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_xi.reg_upper_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-379"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_zeta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_zeta.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_zeta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_zeta.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_zeta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_zeta.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-380"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_zeta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_zeta.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_zeta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_zeta.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_zeta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_zeta.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-381"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_zeta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_zeta.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_zeta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_zeta.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_zeta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_zeta.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-382"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_zeta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_zeta.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_zeta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_zeta.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_zeta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_zeta.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-383"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_zeta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_lower_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_zeta.reg_lower_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_zeta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_lower_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_zeta.reg_lower_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_zeta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_lower_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_zeta.reg_lower_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-384"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_zeta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_upper_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_zeta.reg_upper_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_zeta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_upper_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_zeta.reg_upper_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-769:1; instance_path=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_zeta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=reg_upper_pair$D; child_output=road_yolo_numeric_rom_probe/road_yolo_numeric_rom_group_Inst_zeta.reg_upper_pair$D; operation_count=0; limit=3; inconclusive_reason=external output implementation is unknown; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-385"></a>
### VG151: 参数默认值无法在受限环境中确定。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `file:road_yolo_numeric_rom_group.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: C_LANE_ALPHA_FILE, C_LANE_BETA_FILE, C_LANE_GAMMA_FILE, C_LANE_DELTA_FILE
- source_excerpt: `C_LANE_ALPHA_FILE, C_LANE_BETA_FILE, C_LANE_GAMMA_FILE, C_LANE_DELTA_FILE`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
C_LANE_ALPHA_FILE, C_LANE_BETA_FILE, C_LANE_GAMMA_FILE, C_LANE_DELTA_FILE
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-386"></a>
### VG151: 公开 parameter 没有适用的参数合同。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:52`
- Evidence:
- node_kind: `verilog_rtl`
- detail: C_LANE_ALPHA_FILE
- source_excerpt: `C_LANE_ALPHA_FILE`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `interface`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
C_LANE_ALPHA_FILE
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-387"></a>
### VG151: 公开 parameter 没有适用的参数合同。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:53`
- Evidence:
- node_kind: `verilog_rtl`
- detail: C_LANE_BETA_FILE
- source_excerpt: `C_LANE_BETA_FILE`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `interface`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
C_LANE_BETA_FILE
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-388"></a>
### VG151: 公开 parameter 没有适用的参数合同。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:54`
- Evidence:
- node_kind: `verilog_rtl`
- detail: C_LANE_GAMMA_FILE
- source_excerpt: `C_LANE_GAMMA_FILE`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `interface`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
C_LANE_GAMMA_FILE
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-389"></a>
### VG151: 公开 parameter 没有适用的参数合同。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:55`
- Evidence:
- node_kind: `verilog_rtl`
- detail: C_LANE_DELTA_FILE
- source_excerpt: `C_LANE_DELTA_FILE`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `interface`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
C_LANE_DELTA_FILE
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-390"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:69`
- Evidence:
- node_kind: `verilog_rtl`
- detail: lane_alpha_data
- source_excerpt: `lane_alpha_data`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
lane_alpha_data
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-391"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:70`
- Evidence:
- node_kind: `verilog_rtl`
- detail: lane_beta_data
- source_excerpt: `lane_beta_data`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
lane_beta_data
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-392"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:71`
- Evidence:
- node_kind: `verilog_rtl`
- detail: lane_gamma_data
- source_excerpt: `lane_gamma_data`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
lane_gamma_data
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-393"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:72`
- Evidence:
- node_kind: `verilog_rtl`
- detail: lane_delta_data
- source_excerpt: `lane_delta_data`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
lane_delta_data
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-394"></a>
### VG153: 子模块输出的完整位宽或唯一驱动关系无法确认。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `file:road_yolo_numeric_rom_probe.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: group_alpha_data
- source_excerpt: `group_alpha_data`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
group_alpha_data
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-395"></a>
### VG153: 子模块输出的完整位宽或唯一驱动关系无法确认。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `file:road_yolo_numeric_rom_probe.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: group_beta_data
- source_excerpt: `group_beta_data`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
group_beta_data
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-396"></a>
### VG153: 子模块输出的完整位宽或唯一驱动关系无法确认。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `file:road_yolo_numeric_rom_probe.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: group_delta_data
- source_excerpt: `group_delta_data`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
group_delta_data
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-397"></a>
### VG153: 子模块输出的完整位宽或唯一驱动关系无法确认。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `file:road_yolo_numeric_rom_probe.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: group_epsilon_data
- source_excerpt: `group_epsilon_data`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
group_epsilon_data
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-398"></a>
### VG153: 子模块输出的完整位宽或唯一驱动关系无法确认。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `file:road_yolo_numeric_rom_probe.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: group_eta_data
- source_excerpt: `group_eta_data`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
group_eta_data
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-399"></a>
### VG153: 子模块输出的完整位宽或唯一驱动关系无法确认。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `file:road_yolo_numeric_rom_probe.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: group_gamma_data
- source_excerpt: `group_gamma_data`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
group_gamma_data
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-400"></a>
### VG153: 子模块输出的完整位宽或唯一驱动关系无法确认。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `file:road_yolo_numeric_rom_probe.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: group_iota_data
- source_excerpt: `group_iota_data`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
group_iota_data
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-401"></a>
### VG153: 子模块输出的完整位宽或唯一驱动关系无法确认。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `file:road_yolo_numeric_rom_probe.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: group_kappa_data
- source_excerpt: `group_kappa_data`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
group_kappa_data
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-402"></a>
### VG153: 子模块输出的完整位宽或唯一驱动关系无法确认。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `file:road_yolo_numeric_rom_probe.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: group_lambda_data
- source_excerpt: `group_lambda_data`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
group_lambda_data
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-403"></a>
### VG153: 子模块输出的完整位宽或唯一驱动关系无法确认。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `file:road_yolo_numeric_rom_probe.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: group_mu_data
- source_excerpt: `group_mu_data`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
group_mu_data
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-404"></a>
### VG153: 子模块输出的完整位宽或唯一驱动关系无法确认。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `file:road_yolo_numeric_rom_probe.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: group_nu_data
- source_excerpt: `group_nu_data`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
group_nu_data
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-405"></a>
### VG153: 子模块输出的完整位宽或唯一驱动关系无法确认。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `file:road_yolo_numeric_rom_probe.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: group_theta_data
- source_excerpt: `group_theta_data`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
group_theta_data
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-406"></a>
### VG153: 子模块输出的完整位宽或唯一驱动关系无法确认。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `file:road_yolo_numeric_rom_probe.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: group_xi_data
- source_excerpt: `group_xi_data`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
group_xi_data
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-407"></a>
### VG153: 子模块输出的完整位宽或唯一驱动关系无法确认。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `file:road_yolo_numeric_rom_probe.v:unknown`
- Evidence:
- node_kind: `verilog_rtl`
- detail: group_zeta_data
- source_excerpt: `group_zeta_data`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
group_zeta_data
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-408"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_probe.v:80`
- Evidence:
- node_kind: `verilog_rtl`
- detail: group_alpha_data
- source_excerpt: `group_alpha_data`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
group_alpha_data
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-409"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_probe.v:81`
- Evidence:
- node_kind: `verilog_rtl`
- detail: group_beta_data
- source_excerpt: `group_beta_data`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
group_beta_data
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-410"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_probe.v:82`
- Evidence:
- node_kind: `verilog_rtl`
- detail: group_gamma_data
- source_excerpt: `group_gamma_data`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
group_gamma_data
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-411"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_probe.v:83`
- Evidence:
- node_kind: `verilog_rtl`
- detail: group_delta_data
- source_excerpt: `group_delta_data`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
group_delta_data
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-412"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_probe.v:84`
- Evidence:
- node_kind: `verilog_rtl`
- detail: group_epsilon_data
- source_excerpt: `group_epsilon_data`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
group_epsilon_data
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-413"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_probe.v:85`
- Evidence:
- node_kind: `verilog_rtl`
- detail: group_zeta_data
- source_excerpt: `group_zeta_data`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
group_zeta_data
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-414"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_probe.v:86`
- Evidence:
- node_kind: `verilog_rtl`
- detail: group_eta_data
- source_excerpt: `group_eta_data`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
group_eta_data
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-415"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_probe.v:87`
- Evidence:
- node_kind: `verilog_rtl`
- detail: group_theta_data
- source_excerpt: `group_theta_data`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
group_theta_data
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-416"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_probe.v:88`
- Evidence:
- node_kind: `verilog_rtl`
- detail: group_iota_data
- source_excerpt: `group_iota_data`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
group_iota_data
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-417"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_probe.v:89`
- Evidence:
- node_kind: `verilog_rtl`
- detail: group_kappa_data
- source_excerpt: `group_kappa_data`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
group_kappa_data
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-418"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_probe.v:90`
- Evidence:
- node_kind: `verilog_rtl`
- detail: group_lambda_data
- source_excerpt: `group_lambda_data`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
group_lambda_data
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-419"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_probe.v:91`
- Evidence:
- node_kind: `verilog_rtl`
- detail: group_mu_data
- source_excerpt: `group_mu_data`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
group_mu_data
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-420"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_probe.v:92`
- Evidence:
- node_kind: `verilog_rtl`
- detail: group_nu_data
- source_excerpt: `group_nu_data`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
group_nu_data
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-421"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_probe.v:93`
- Evidence:
- node_kind: `verilog_rtl`
- detail: group_xi_data
- source_excerpt: `group_xi_data`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
group_xi_data
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

## Other deliverable findings

| Severity | Code | Path | Line | Message |
|---|---|---|---:|---|
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_group.v:119` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_group.v:177` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_group.v:235` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_group.v:293` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_probe.v:574` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_probe.v:588` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_probe.v:602` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_probe.v:616` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_probe.v:630` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_probe.v:644` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_probe.v:658` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_probe.v:672` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_probe.v:686` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_probe.v:700` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_probe.v:714` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_probe.v:728` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_probe.v:742` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_probe.v:756` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
