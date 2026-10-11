# Verilog deliverable gate

Root: `E:\project\qiansai\anlogic_topic2_work\lab1_sc500_road_vision\cnn\hw_validation\rom`
Delivery ready: `False`
Summary: **993 error(s)**, **95 strict warning(s)**

## Actionable VG findings

<a id="vg-finding-1"></a>
### VG024: Instance `u_lane_alpha` should follow `<module>_Inst_<role>` naming when practical.
- Status: `failed`
- Severity: `warning`
- Location: `file:road_yolo_numeric_rom_group.v:unknown`
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

<a id="vg-finding-2"></a>
### VG024: Instance `u_lane_beta` should follow `<module>_Inst_<role>` naming when practical.
- Status: `failed`
- Severity: `warning`
- Location: `file:road_yolo_numeric_rom_group.v:unknown`
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

<a id="vg-finding-3"></a>
### VG024: Instance `u_lane_gamma` should follow `<module>_Inst_<role>` naming when practical.
- Status: `failed`
- Severity: `warning`
- Location: `file:road_yolo_numeric_rom_group.v:unknown`
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

<a id="vg-finding-4"></a>
### VG024: Instance `u_lane_delta` should follow `<module>_Inst_<role>` naming when practical.
- Status: `failed`
- Severity: `warning`
- Location: `file:road_yolo_numeric_rom_group.v:unknown`
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

<a id="vg-finding-5"></a>
### VG061: Item `always@(posedge i_clk or negedge i_rstn)` must be placed in 输出信号处理区域, not `主要任务处理区域`.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:96`
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

<a id="vg-finding-6"></a>
### VG061: Item `always@(posedge i_clk or negedge i_rstn)` must be placed in 输出信号处理区域, not `主要任务处理区域`.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:104`
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

<a id="vg-finding-7"></a>
### VG056: Comment for parameter `C_LANE_ALPHA_FILE` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:52`
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

<a id="vg-finding-8"></a>
### VG041: Comment for parameter `C_LANE_ALPHA_FILE` looks generic: `parameter`.
- Status: `failed`
- Severity: `warning`
- Location: `road_yolo_numeric_rom_group.v:52`
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

<a id="vg-finding-9"></a>
### VG056: Comment for parameter `C_LANE_BETA_FILE` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:53`
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

<a id="vg-finding-10"></a>
### VG041: Comment for parameter `C_LANE_BETA_FILE` looks generic: `parameter`.
- Status: `failed`
- Severity: `warning`
- Location: `road_yolo_numeric_rom_group.v:53`
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

<a id="vg-finding-11"></a>
### VG056: Comment for parameter `C_LANE_GAMMA_FILE` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:54`
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

<a id="vg-finding-12"></a>
### VG041: Comment for parameter `C_LANE_GAMMA_FILE` looks generic: `parameter`.
- Status: `failed`
- Severity: `warning`
- Location: `road_yolo_numeric_rom_group.v:54`
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

<a id="vg-finding-13"></a>
### VG056: Comment for parameter `C_LANE_DELTA_FILE` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:55`
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

<a id="vg-finding-14"></a>
### VG041: Comment for parameter `C_LANE_DELTA_FILE` looks generic: `parameter`.
- Status: `failed`
- Severity: `warning`
- Location: `road_yolo_numeric_rom_group.v:55`
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

<a id="vg-finding-15"></a>
### VG056: Comment for port `i_clk` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:59`
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

<a id="vg-finding-16"></a>
### VG041: Comment for port `i_clk` looks generic: `port signal`.
- Status: `failed`
- Severity: `warning`
- Location: `road_yolo_numeric_rom_group.v:59`
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

<a id="vg-finding-17"></a>
### VG056: Comment for port `i_rstn` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:60`
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

<a id="vg-finding-18"></a>
### VG041: Comment for port `i_rstn` looks generic: `port signal`.
- Status: `failed`
- Severity: `warning`
- Location: `road_yolo_numeric_rom_group.v:60`
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

<a id="vg-finding-19"></a>
### VG056: Comment for port `i_word_addr` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:63`
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

<a id="vg-finding-20"></a>
### VG041: Comment for port `i_word_addr` looks generic: `port signal`.
- Status: `failed`
- Severity: `warning`
- Location: `road_yolo_numeric_rom_group.v:63`
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

<a id="vg-finding-21"></a>
### VG056: Comment for port `o_word_data` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:64`
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

<a id="vg-finding-22"></a>
### VG041: Comment for port `o_word_data` looks generic: `port signal`.
- Status: `failed`
- Severity: `warning`
- Location: `road_yolo_numeric_rom_group.v:64`
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

<a id="vg-finding-23"></a>
### VG056: Comment for signal `lane_alpha_data` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:69`
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

<a id="vg-finding-24"></a>
### VG041: Comment for signal `lane_alpha_data` looks generic: `signal`.
- Status: `failed`
- Severity: `warning`
- Location: `road_yolo_numeric_rom_group.v:69`
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

<a id="vg-finding-25"></a>
### VG056: Comment for signal `lane_beta_data` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:70`
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

<a id="vg-finding-26"></a>
### VG041: Comment for signal `lane_beta_data` looks generic: `signal`.
- Status: `failed`
- Severity: `warning`
- Location: `road_yolo_numeric_rom_group.v:70`
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

<a id="vg-finding-27"></a>
### VG056: Comment for signal `lane_gamma_data` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:71`
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

<a id="vg-finding-28"></a>
### VG041: Comment for signal `lane_gamma_data` looks generic: `signal`.
- Status: `failed`
- Severity: `warning`
- Location: `road_yolo_numeric_rom_group.v:71`
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

<a id="vg-finding-29"></a>
### VG056: Comment for signal `lane_delta_data` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:72`
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

<a id="vg-finding-30"></a>
### VG041: Comment for signal `lane_delta_data` looks generic: `signal`.
- Status: `failed`
- Severity: `warning`
- Location: `road_yolo_numeric_rom_group.v:72`
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

<a id="vg-finding-31"></a>
### VG056: Comment for signal `word_data_o` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:76`
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

<a id="vg-finding-32"></a>
### VG041: Comment for signal `word_data_o` looks generic: `signal`.
- Status: `failed`
- Severity: `warning`
- Location: `road_yolo_numeric_rom_group.v:76`
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

<a id="vg-finding-33"></a>
### VG056: Comment for signal `lower_pair_o` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:77`
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

<a id="vg-finding-34"></a>
### VG041: Comment for signal `lower_pair_o` looks generic: `signal`.
- Status: `failed`
- Severity: `warning`
- Location: `road_yolo_numeric_rom_group.v:77`
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

<a id="vg-finding-35"></a>
### VG056: Comment for signal `upper_pair_o` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:78`
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

<a id="vg-finding-36"></a>
### VG041: Comment for signal `upper_pair_o` looks generic: `signal`.
- Status: `failed`
- Severity: `warning`
- Location: `road_yolo_numeric_rom_group.v:78`
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

<a id="vg-finding-37"></a>
### VG056: Comment for assign `o_word_data` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:82`
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

<a id="vg-finding-38"></a>
### VG041: Comment for assign `o_word_data` looks generic: `assign`.
- Status: `failed`
- Severity: `warning`
- Location: `road_yolo_numeric_rom_group.v:82`
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

<a id="vg-finding-39"></a>
### VG040: Always block `always@(posedge i_clk or negedge i_rstn)` should have a nearby leading comment explaining behavior.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:104`
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

<a id="vg-finding-40"></a>
### VG040: Instance `u_lane_alpha` should have a leading function/connection comment.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:144`
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

<a id="vg-finding-41"></a>
### VG040: Instance `u_lane_beta` should have a leading function/connection comment.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:200`
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

<a id="vg-finding-42"></a>
### VG040: Instance `u_lane_gamma` should have a leading function/connection comment.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:256`
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

<a id="vg-finding-43"></a>
### VG040: Instance `u_lane_delta` should have a leading function/connection comment.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:312`
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

<a id="vg-finding-44"></a>
### VG062: process assignment `word_data_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:88`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `word_data_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:90`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `lower_pair_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:98`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `lower_pair_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:100`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `upper_pair_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:106`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `upper_pair_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:108`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG066: Comment for instance mapping `.dia` repeats or closely reuses comment from instance mapping `.dia`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:201`
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
### VG066: Comment for instance mapping `.addra` repeats or closely reuses comment from instance mapping `.addra`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:202`
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
### VG066: Comment for instance mapping `.cea` repeats or closely reuses comment from instance mapping `.cea`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:203`
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
### VG066: Comment for instance mapping `.ocea` repeats or closely reuses comment from instance mapping `.ocea`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:204`
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
### VG066: Comment for instance mapping `.clka` repeats or closely reuses comment from instance mapping `.clka`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:205`
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
### VG066: Comment for instance mapping `.wea` repeats or closely reuses comment from instance mapping `.wea`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:206`
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
### VG066: Comment for instance mapping `.rsta` repeats or closely reuses comment from instance mapping `.rsta`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:207`
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
### VG066: Comment for instance mapping `.bea` repeats or closely reuses comment from instance mapping `.bea`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:208`
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
### VG066: Comment for instance mapping `.dib` repeats or closely reuses comment from instance mapping `.dib`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:209`
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
### VG066: Comment for instance mapping `.addrb` repeats or closely reuses comment from instance mapping `.addrb`; write entity-specific RTL intent.
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

<a id="vg-finding-60"></a>
### VG066: Comment for instance mapping `.ceb` repeats or closely reuses comment from instance mapping `.ceb`; write entity-specific RTL intent.
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

<a id="vg-finding-61"></a>
### VG066: Comment for instance mapping `.oceb` repeats or closely reuses comment from instance mapping `.oceb`; write entity-specific RTL intent.
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

<a id="vg-finding-62"></a>
### VG066: Comment for instance mapping `.clkb` repeats or closely reuses comment from instance mapping `.clkb`; write entity-specific RTL intent.
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

<a id="vg-finding-63"></a>
### VG066: Comment for instance mapping `.web` repeats or closely reuses comment from instance mapping `.web`; write entity-specific RTL intent.
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

<a id="vg-finding-64"></a>
### VG066: Comment for instance mapping `.rstb` repeats or closely reuses comment from instance mapping `.rstb`; write entity-specific RTL intent.
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

<a id="vg-finding-65"></a>
### VG066: Comment for instance mapping `.beb` repeats or closely reuses comment from instance mapping `.beb`; write entity-specific RTL intent.
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

<a id="vg-finding-66"></a>
### VG066: Comment for instance mapping `.ecc_sbiterrinj` repeats or closely reuses comment from instance mapping `.ecc_sbiterrinj`; write entity-specific RTL intent.
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

<a id="vg-finding-67"></a>
### VG066: Comment for instance mapping `.ecc_dbiterrinj` repeats or closely reuses comment from instance mapping `.ecc_dbiterrinj`; write entity-specific RTL intent.
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

<a id="vg-finding-68"></a>
### VG066: Comment for instance mapping `.dob` repeats or closely reuses comment from instance mapping `.dob`; write entity-specific RTL intent.
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

<a id="vg-finding-69"></a>
### VG066: Comment for instance mapping `.ecc_sbiterr` repeats or closely reuses comment from instance mapping `.ecc_sbiterr`; write entity-specific RTL intent.
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

<a id="vg-finding-70"></a>
### VG066: Comment for instance mapping `.ecc_dbiterr` repeats or closely reuses comment from instance mapping `.ecc_dbiterr`; write entity-specific RTL intent.
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

<a id="vg-finding-71"></a>
### VG066: Comment for instance mapping `.DATA_WIDTH_A` repeats or closely reuses comment from instance mapping `.DATA_WIDTH_A`; write entity-specific RTL intent.
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

<a id="vg-finding-72"></a>
### VG066: Comment for instance mapping `.DATA_WIDTH_B` repeats or closely reuses comment from instance mapping `.DATA_WIDTH_B`; write entity-specific RTL intent.
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

<a id="vg-finding-73"></a>
### VG066: Comment for instance mapping `.ADDR_WIDTH_A` repeats or closely reuses comment from instance mapping `.ADDR_WIDTH_A`; write entity-specific RTL intent.
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

<a id="vg-finding-74"></a>
### VG066: Comment for instance mapping `.ADDR_WIDTH_B` repeats or closely reuses comment from instance mapping `.ADDR_WIDTH_B`; write entity-specific RTL intent.
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

<a id="vg-finding-75"></a>
### VG066: Comment for instance mapping `.DATA_DEPTH_A` repeats or closely reuses comment from instance mapping `.DATA_DEPTH_A`; write entity-specific RTL intent.
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

<a id="vg-finding-76"></a>
### VG066: Comment for instance mapping `.DATA_DEPTH_B` repeats or closely reuses comment from instance mapping `.DATA_DEPTH_B`; write entity-specific RTL intent.
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

<a id="vg-finding-77"></a>
### VG066: Comment for instance mapping `.BYTE_ENABLE` repeats or closely reuses comment from instance mapping `.BYTE_ENABLE`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:232`
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
### VG066: Comment for instance mapping `.BYTE_A` repeats or closely reuses comment from instance mapping `.BYTE_A`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:233`
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
### VG066: Comment for instance mapping `.BYTE_B` repeats or closely reuses comment from instance mapping `.BYTE_B`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:234`
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

<a id="vg-finding-80"></a>
### VG066: Comment for instance mapping `.MODE` repeats or closely reuses comment from instance mapping `.MODE`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:235`
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

<a id="vg-finding-81"></a>
### VG066: Comment for instance mapping `.REGMODE_A` repeats or closely reuses comment from instance mapping `.REGMODE_A`; write entity-specific RTL intent.
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

<a id="vg-finding-82"></a>
### VG066: Comment for instance mapping `.REGMODE_B` repeats or closely reuses comment from instance mapping `.REGMODE_B`; write entity-specific RTL intent.
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

<a id="vg-finding-83"></a>
### VG066: Comment for instance mapping `.WRITEMODE_A` repeats or closely reuses comment from instance mapping `.WRITEMODE_A`; write entity-specific RTL intent.
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

<a id="vg-finding-84"></a>
### VG066: Comment for instance mapping `.WRITEMODE_B` repeats or closely reuses comment from instance mapping `.WRITEMODE_B`; write entity-specific RTL intent.
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

<a id="vg-finding-85"></a>
### VG066: Comment for instance mapping `.RESETMODE_A` repeats or closely reuses comment from instance mapping `.RESETMODE_A`; write entity-specific RTL intent.
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

<a id="vg-finding-86"></a>
### VG066: Comment for instance mapping `.RESETMODE_B` repeats or closely reuses comment from instance mapping `.RESETMODE_B`; write entity-specific RTL intent.
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

<a id="vg-finding-87"></a>
### VG066: Comment for instance mapping `.OREGSET_A` repeats or closely reuses comment from instance mapping `.OREGSET_A`; write entity-specific RTL intent.
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

<a id="vg-finding-88"></a>
### VG066: Comment for instance mapping `.OREGSET_B` repeats or closely reuses comment from instance mapping `.OREGSET_B`; write entity-specific RTL intent.
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

<a id="vg-finding-89"></a>
### VG066: Comment for instance mapping `.SSROVERCE` repeats or closely reuses comment from instance mapping `.SSROVERCE`; write entity-specific RTL intent.
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

<a id="vg-finding-90"></a>
### VG066: Comment for instance mapping `.ECC_DECODE` repeats or closely reuses comment from instance mapping `.ECC_DECODE`; write entity-specific RTL intent.
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

<a id="vg-finding-91"></a>
### VG066: Comment for instance mapping `.ECC_ENCODE` repeats or closely reuses comment from instance mapping `.ECC_ENCODE`; write entity-specific RTL intent.
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

<a id="vg-finding-92"></a>
### VG066: Comment for instance mapping `.ASYNC_RESET_RELEASE_A` repeats or closely reuses comment from instance mapping `.ASYNC_RESET_RELEASE_A`; write entity-specific RTL intent.
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

<a id="vg-finding-93"></a>
### VG066: Comment for instance mapping `.ASYNC_RESET_RELEASE_B` repeats or closely reuses comment from instance mapping `.ASYNC_RESET_RELEASE_B`; write entity-specific RTL intent.
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

<a id="vg-finding-94"></a>
### VG066: Comment for instance mapping `.CLKMODE` repeats or closely reuses comment from instance mapping `.CLKMODE`; write entity-specific RTL intent.
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

<a id="vg-finding-95"></a>
### VG066: Comment for instance mapping `.DEBUGGABLE` repeats or closely reuses comment from instance mapping `.DEBUGGABLE`; write entity-specific RTL intent.
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

<a id="vg-finding-96"></a>
### VG066: Comment for instance mapping `.PACKABLE` repeats or closely reuses comment from instance mapping `.PACKABLE`; write entity-specific RTL intent.
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

<a id="vg-finding-97"></a>
### VG066: Comment for instance mapping `.FORCE_KEEP` repeats or closely reuses comment from instance mapping `.FORCE_KEEP`; write entity-specific RTL intent.
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

<a id="vg-finding-98"></a>
### VG066: Comment for instance mapping `.FILL_ALL` repeats or closely reuses comment from instance mapping `.FILL_ALL`; write entity-specific RTL intent.
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

<a id="vg-finding-99"></a>
### VG066: Comment for instance mapping `.dia` repeats or closely reuses comment from instance mapping `.dia`; write entity-specific RTL intent.
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

<a id="vg-finding-100"></a>
### VG066: Comment for instance mapping `.addra` repeats or closely reuses comment from instance mapping `.addra`; write entity-specific RTL intent.
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

<a id="vg-finding-101"></a>
### VG066: Comment for instance mapping `.cea` repeats or closely reuses comment from instance mapping `.cea`; write entity-specific RTL intent.
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

<a id="vg-finding-102"></a>
### VG066: Comment for instance mapping `.ocea` repeats or closely reuses comment from instance mapping `.ocea`; write entity-specific RTL intent.
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

<a id="vg-finding-103"></a>
### VG066: Comment for instance mapping `.clka` repeats or closely reuses comment from instance mapping `.clka`; write entity-specific RTL intent.
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

<a id="vg-finding-104"></a>
### VG066: Comment for instance mapping `.wea` repeats or closely reuses comment from instance mapping `.wea`; write entity-specific RTL intent.
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

<a id="vg-finding-105"></a>
### VG066: Comment for instance mapping `.rsta` repeats or closely reuses comment from instance mapping `.rsta`; write entity-specific RTL intent.
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

<a id="vg-finding-106"></a>
### VG066: Comment for instance mapping `.bea` repeats or closely reuses comment from instance mapping `.bea`; write entity-specific RTL intent.
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

<a id="vg-finding-107"></a>
### VG066: Comment for instance mapping `.dib` repeats or closely reuses comment from instance mapping `.dib`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:265`
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
### VG066: Comment for instance mapping `.addrb` repeats or closely reuses comment from instance mapping `.addrb`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:266`
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
### VG066: Comment for instance mapping `.ceb` repeats or closely reuses comment from instance mapping `.ceb`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:267`
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

<a id="vg-finding-110"></a>
### VG066: Comment for instance mapping `.oceb` repeats or closely reuses comment from instance mapping `.oceb`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:268`
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

<a id="vg-finding-111"></a>
### VG066: Comment for instance mapping `.clkb` repeats or closely reuses comment from instance mapping `.clkb`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:269`
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

<a id="vg-finding-112"></a>
### VG066: Comment for instance mapping `.web` repeats or closely reuses comment from instance mapping `.web`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:270`
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

<a id="vg-finding-113"></a>
### VG066: Comment for instance mapping `.rstb` repeats or closely reuses comment from instance mapping `.rstb`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:271`
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

<a id="vg-finding-114"></a>
### VG066: Comment for instance mapping `.beb` repeats or closely reuses comment from instance mapping `.beb`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:272`
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

<a id="vg-finding-115"></a>
### VG066: Comment for instance mapping `.ecc_sbiterrinj` repeats or closely reuses comment from instance mapping `.ecc_sbiterrinj`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:273`
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

<a id="vg-finding-116"></a>
### VG066: Comment for instance mapping `.ecc_dbiterrinj` repeats or closely reuses comment from instance mapping `.ecc_dbiterrinj`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:274`
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

<a id="vg-finding-117"></a>
### VG066: Comment for instance mapping `.dob` repeats or closely reuses comment from instance mapping `.dob`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:276`
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

<a id="vg-finding-118"></a>
### VG066: Comment for instance mapping `.ecc_sbiterr` repeats or closely reuses comment from instance mapping `.ecc_sbiterr`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:277`
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

<a id="vg-finding-119"></a>
### VG066: Comment for instance mapping `.ecc_dbiterr` repeats or closely reuses comment from instance mapping `.ecc_dbiterr`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:278`
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

<a id="vg-finding-120"></a>
### VG066: Comment for instance mapping `.DATA_WIDTH_A` repeats or closely reuses comment from instance mapping `.DATA_WIDTH_A`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:282`
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

<a id="vg-finding-121"></a>
### VG066: Comment for instance mapping `.DATA_WIDTH_B` repeats or closely reuses comment from instance mapping `.DATA_WIDTH_B`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:283`
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

<a id="vg-finding-122"></a>
### VG066: Comment for instance mapping `.ADDR_WIDTH_A` repeats or closely reuses comment from instance mapping `.ADDR_WIDTH_A`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:284`
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

<a id="vg-finding-123"></a>
### VG066: Comment for instance mapping `.ADDR_WIDTH_B` repeats or closely reuses comment from instance mapping `.ADDR_WIDTH_B`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:285`
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

<a id="vg-finding-124"></a>
### VG066: Comment for instance mapping `.DATA_DEPTH_A` repeats or closely reuses comment from instance mapping `.DATA_DEPTH_A`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:286`
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

<a id="vg-finding-125"></a>
### VG066: Comment for instance mapping `.DATA_DEPTH_B` repeats or closely reuses comment from instance mapping `.DATA_DEPTH_B`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:287`
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

<a id="vg-finding-126"></a>
### VG066: Comment for instance mapping `.BYTE_ENABLE` repeats or closely reuses comment from instance mapping `.BYTE_ENABLE`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:288`
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

<a id="vg-finding-127"></a>
### VG066: Comment for instance mapping `.BYTE_A` repeats or closely reuses comment from instance mapping `.BYTE_A`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:289`
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

<a id="vg-finding-128"></a>
### VG066: Comment for instance mapping `.BYTE_B` repeats or closely reuses comment from instance mapping `.BYTE_B`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:290`
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

<a id="vg-finding-129"></a>
### VG066: Comment for instance mapping `.MODE` repeats or closely reuses comment from instance mapping `.MODE`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:291`
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

<a id="vg-finding-130"></a>
### VG066: Comment for instance mapping `.REGMODE_A` repeats or closely reuses comment from instance mapping `.REGMODE_A`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:292`
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

<a id="vg-finding-131"></a>
### VG066: Comment for instance mapping `.REGMODE_B` repeats or closely reuses comment from instance mapping `.REGMODE_B`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:293`
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

<a id="vg-finding-132"></a>
### VG066: Comment for instance mapping `.WRITEMODE_A` repeats or closely reuses comment from instance mapping `.WRITEMODE_A`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:294`
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

<a id="vg-finding-133"></a>
### VG066: Comment for instance mapping `.WRITEMODE_B` repeats or closely reuses comment from instance mapping `.WRITEMODE_B`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:295`
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

<a id="vg-finding-134"></a>
### VG066: Comment for instance mapping `.RESETMODE_A` repeats or closely reuses comment from instance mapping `.RESETMODE_A`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:296`
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

<a id="vg-finding-135"></a>
### VG066: Comment for instance mapping `.RESETMODE_B` repeats or closely reuses comment from instance mapping `.RESETMODE_B`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:297`
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

<a id="vg-finding-136"></a>
### VG066: Comment for instance mapping `.OREGSET_A` repeats or closely reuses comment from instance mapping `.OREGSET_A`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:298`
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

<a id="vg-finding-137"></a>
### VG066: Comment for instance mapping `.OREGSET_B` repeats or closely reuses comment from instance mapping `.OREGSET_B`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:299`
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

<a id="vg-finding-138"></a>
### VG066: Comment for instance mapping `.SSROVERCE` repeats or closely reuses comment from instance mapping `.SSROVERCE`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:300`
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

<a id="vg-finding-139"></a>
### VG066: Comment for instance mapping `.ECC_DECODE` repeats or closely reuses comment from instance mapping `.ECC_DECODE`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:301`
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

<a id="vg-finding-140"></a>
### VG066: Comment for instance mapping `.ECC_ENCODE` repeats or closely reuses comment from instance mapping `.ECC_ENCODE`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:302`
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

<a id="vg-finding-141"></a>
### VG066: Comment for instance mapping `.ASYNC_RESET_RELEASE_A` repeats or closely reuses comment from instance mapping `.ASYNC_RESET_RELEASE_A`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:303`
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

<a id="vg-finding-142"></a>
### VG066: Comment for instance mapping `.ASYNC_RESET_RELEASE_B` repeats or closely reuses comment from instance mapping `.ASYNC_RESET_RELEASE_B`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:304`
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

<a id="vg-finding-143"></a>
### VG066: Comment for instance mapping `.CLKMODE` repeats or closely reuses comment from instance mapping `.CLKMODE`; write entity-specific RTL intent.
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

<a id="vg-finding-144"></a>
### VG066: Comment for instance mapping `.DEBUGGABLE` repeats or closely reuses comment from instance mapping `.DEBUGGABLE`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:306`
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

<a id="vg-finding-145"></a>
### VG066: Comment for instance mapping `.PACKABLE` repeats or closely reuses comment from instance mapping `.PACKABLE`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:307`
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

<a id="vg-finding-146"></a>
### VG066: Comment for instance mapping `.FORCE_KEEP` repeats or closely reuses comment from instance mapping `.FORCE_KEEP`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:308`
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

<a id="vg-finding-147"></a>
### VG066: Comment for instance mapping `.FILL_ALL` repeats or closely reuses comment from instance mapping `.FILL_ALL`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:310`
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

<a id="vg-finding-148"></a>
### VG066: Comment for instance mapping `.dia` repeats or closely reuses comment from instance mapping `.dia`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:313`
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

<a id="vg-finding-149"></a>
### VG066: Comment for instance mapping `.addra` repeats or closely reuses comment from instance mapping `.addra`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:314`
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

<a id="vg-finding-150"></a>
### VG066: Comment for instance mapping `.cea` repeats or closely reuses comment from instance mapping `.cea`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:315`
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

<a id="vg-finding-151"></a>
### VG066: Comment for instance mapping `.ocea` repeats or closely reuses comment from instance mapping `.ocea`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:316`
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

<a id="vg-finding-152"></a>
### VG066: Comment for instance mapping `.clka` repeats or closely reuses comment from instance mapping `.clka`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:317`
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

<a id="vg-finding-153"></a>
### VG066: Comment for instance mapping `.wea` repeats or closely reuses comment from instance mapping `.wea`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:318`
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

<a id="vg-finding-154"></a>
### VG066: Comment for instance mapping `.rsta` repeats or closely reuses comment from instance mapping `.rsta`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:319`
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

<a id="vg-finding-155"></a>
### VG066: Comment for instance mapping `.bea` repeats or closely reuses comment from instance mapping `.bea`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:320`
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

<a id="vg-finding-156"></a>
### VG066: Comment for instance mapping `.dib` repeats or closely reuses comment from instance mapping `.dib`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:321`
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

<a id="vg-finding-157"></a>
### VG066: Comment for instance mapping `.addrb` repeats or closely reuses comment from instance mapping `.addrb`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:322`
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

<a id="vg-finding-158"></a>
### VG066: Comment for instance mapping `.ceb` repeats or closely reuses comment from instance mapping `.ceb`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:323`
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

<a id="vg-finding-159"></a>
### VG066: Comment for instance mapping `.oceb` repeats or closely reuses comment from instance mapping `.oceb`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:324`
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

<a id="vg-finding-160"></a>
### VG066: Comment for instance mapping `.clkb` repeats or closely reuses comment from instance mapping `.clkb`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:325`
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

<a id="vg-finding-161"></a>
### VG066: Comment for instance mapping `.web` repeats or closely reuses comment from instance mapping `.web`; write entity-specific RTL intent.
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

<a id="vg-finding-162"></a>
### VG066: Comment for instance mapping `.rstb` repeats or closely reuses comment from instance mapping `.rstb`; write entity-specific RTL intent.
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

<a id="vg-finding-163"></a>
### VG066: Comment for instance mapping `.beb` repeats or closely reuses comment from instance mapping `.beb`; write entity-specific RTL intent.
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

<a id="vg-finding-164"></a>
### VG066: Comment for instance mapping `.ecc_sbiterrinj` repeats or closely reuses comment from instance mapping `.ecc_sbiterrinj`; write entity-specific RTL intent.
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

<a id="vg-finding-165"></a>
### VG066: Comment for instance mapping `.ecc_dbiterrinj` repeats or closely reuses comment from instance mapping `.ecc_dbiterrinj`; write entity-specific RTL intent.
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

<a id="vg-finding-166"></a>
### VG066: Comment for instance mapping `.dob` repeats or closely reuses comment from instance mapping `.dob`; write entity-specific RTL intent.
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

<a id="vg-finding-167"></a>
### VG066: Comment for instance mapping `.ecc_sbiterr` repeats or closely reuses comment from instance mapping `.ecc_sbiterr`; write entity-specific RTL intent.
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

<a id="vg-finding-168"></a>
### VG066: Comment for instance mapping `.ecc_dbiterr` repeats or closely reuses comment from instance mapping `.ecc_dbiterr`; write entity-specific RTL intent.
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

<a id="vg-finding-169"></a>
### VG066: Comment for instance mapping `.addra` repeats or closely reuses comment from instance mapping `.dia`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:146`
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

<a id="vg-finding-170"></a>
### VG066: Comment for instance mapping `.cea` repeats or closely reuses comment from instance mapping `.dia`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:147`
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

<a id="vg-finding-171"></a>
### VG066: Comment for instance mapping `.ocea` repeats or closely reuses comment from instance mapping `.dia`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:148`
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

<a id="vg-finding-172"></a>
### VG066: Comment for instance mapping `.clka` repeats or closely reuses comment from instance mapping `.dia`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:149`
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

<a id="vg-finding-173"></a>
### VG066: Comment for instance mapping `.wea` repeats or closely reuses comment from instance mapping `.dia`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:150`
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

<a id="vg-finding-174"></a>
### VG066: Comment for instance mapping `.rsta` repeats or closely reuses comment from instance mapping `.dia`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:151`
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

<a id="vg-finding-175"></a>
### VG066: Comment for instance mapping `.bea` repeats or closely reuses comment from instance mapping `.dia`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:152`
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

<a id="vg-finding-176"></a>
### VG066: Comment for instance mapping `.dib` repeats or closely reuses comment from instance mapping `.dia`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:153`
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

<a id="vg-finding-177"></a>
### VG066: Comment for instance mapping `.addrb` repeats or closely reuses comment from instance mapping `.dia`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:154`
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

<a id="vg-finding-178"></a>
### VG066: Comment for instance mapping `.ceb` repeats or closely reuses comment from instance mapping `.dia`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:155`
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

<a id="vg-finding-179"></a>
### VG066: Comment for instance mapping `.oceb` repeats or closely reuses comment from instance mapping `.dia`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:156`
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

<a id="vg-finding-180"></a>
### VG066: Comment for instance mapping `.clkb` repeats or closely reuses comment from instance mapping `.dia`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:157`
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

<a id="vg-finding-181"></a>
### VG066: Comment for instance mapping `.web` repeats or closely reuses comment from instance mapping `.dia`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:158`
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

<a id="vg-finding-182"></a>
### VG066: Comment for instance mapping `.rstb` repeats or closely reuses comment from instance mapping `.dia`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:159`
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

<a id="vg-finding-183"></a>
### VG066: Comment for instance mapping `.beb` repeats or closely reuses comment from instance mapping `.dia`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:160`
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

<a id="vg-finding-184"></a>
### VG066: Comment for instance mapping `.ecc_sbiterrinj` repeats or closely reuses comment from instance mapping `.dia`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:161`
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

<a id="vg-finding-185"></a>
### VG066: Comment for instance mapping `.ecc_dbiterrinj` repeats or closely reuses comment from instance mapping `.dia`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:162`
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

<a id="vg-finding-186"></a>
### VG066: Comment for instance mapping `.doa` repeats or closely reuses comment from instance mapping `.dia`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:163`
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

<a id="vg-finding-187"></a>
### VG066: Comment for instance mapping `.ecc_sbiterr` repeats or closely reuses comment from instance mapping `.dob`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:165`
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

<a id="vg-finding-188"></a>
### VG066: Comment for instance mapping `.ecc_dbiterr` repeats or closely reuses comment from instance mapping `.dob`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:166`
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

<a id="vg-finding-189"></a>
### VG066: Comment for instance mapping `.DATA_WIDTH_B` repeats or closely reuses comment from instance mapping `.DATA_WIDTH_A`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:171`
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

<a id="vg-finding-190"></a>
### VG066: Comment for instance mapping `.ADDR_WIDTH_A` repeats or closely reuses comment from instance mapping `.DATA_WIDTH_A`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:172`
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

<a id="vg-finding-191"></a>
### VG066: Comment for instance mapping `.ADDR_WIDTH_B` repeats or closely reuses comment from instance mapping `.DATA_WIDTH_A`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:173`
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

<a id="vg-finding-192"></a>
### VG066: Comment for instance mapping `.DATA_DEPTH_A` repeats or closely reuses comment from instance mapping `.DATA_WIDTH_A`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:174`
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

<a id="vg-finding-193"></a>
### VG066: Comment for instance mapping `.DATA_DEPTH_B` repeats or closely reuses comment from instance mapping `.DATA_WIDTH_A`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:175`
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

<a id="vg-finding-194"></a>
### VG066: Comment for instance mapping `.BYTE_ENABLE` repeats or closely reuses comment from instance mapping `.DATA_WIDTH_A`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:176`
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

<a id="vg-finding-195"></a>
### VG066: Comment for instance mapping `.BYTE_A` repeats or closely reuses comment from instance mapping `.DATA_WIDTH_A`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:177`
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

<a id="vg-finding-196"></a>
### VG066: Comment for instance mapping `.BYTE_B` repeats or closely reuses comment from instance mapping `.DATA_WIDTH_A`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:178`
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

<a id="vg-finding-197"></a>
### VG066: Comment for instance mapping `.MODE` repeats or closely reuses comment from instance mapping `.DATA_WIDTH_A`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:179`
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

<a id="vg-finding-198"></a>
### VG066: Comment for instance mapping `.REGMODE_A` repeats or closely reuses comment from instance mapping `.DATA_WIDTH_A`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:180`
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

<a id="vg-finding-199"></a>
### VG066: Comment for instance mapping `.REGMODE_B` repeats or closely reuses comment from instance mapping `.DATA_WIDTH_A`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:181`
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

<a id="vg-finding-200"></a>
### VG066: Comment for instance mapping `.WRITEMODE_A` repeats or closely reuses comment from instance mapping `.DATA_WIDTH_A`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:182`
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

<a id="vg-finding-201"></a>
### VG066: Comment for instance mapping `.WRITEMODE_B` repeats or closely reuses comment from instance mapping `.DATA_WIDTH_A`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:183`
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

<a id="vg-finding-202"></a>
### VG066: Comment for instance mapping `.RESETMODE_A` repeats or closely reuses comment from instance mapping `.DATA_WIDTH_A`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:184`
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

<a id="vg-finding-203"></a>
### VG066: Comment for instance mapping `.RESETMODE_B` repeats or closely reuses comment from instance mapping `.DATA_WIDTH_A`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:185`
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

<a id="vg-finding-204"></a>
### VG066: Comment for instance mapping `.OREGSET_A` repeats or closely reuses comment from instance mapping `.DATA_WIDTH_A`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:186`
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

<a id="vg-finding-205"></a>
### VG066: Comment for instance mapping `.OREGSET_B` repeats or closely reuses comment from instance mapping `.DATA_WIDTH_A`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:187`
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

<a id="vg-finding-206"></a>
### VG066: Comment for instance mapping `.SSROVERCE` repeats or closely reuses comment from instance mapping `.DATA_WIDTH_A`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:188`
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

<a id="vg-finding-207"></a>
### VG066: Comment for instance mapping `.ECC_DECODE` repeats or closely reuses comment from instance mapping `.DATA_WIDTH_A`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:189`
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

<a id="vg-finding-208"></a>
### VG066: Comment for instance mapping `.ECC_ENCODE` repeats or closely reuses comment from instance mapping `.DATA_WIDTH_A`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:190`
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

<a id="vg-finding-209"></a>
### VG066: Comment for instance mapping `.ASYNC_RESET_RELEASE_A` repeats or closely reuses comment from instance mapping `.DATA_WIDTH_A`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:191`
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

<a id="vg-finding-210"></a>
### VG066: Comment for instance mapping `.ASYNC_RESET_RELEASE_B` repeats or closely reuses comment from instance mapping `.DATA_WIDTH_A`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:192`
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

<a id="vg-finding-211"></a>
### VG066: Comment for instance mapping `.CLKMODE` repeats or closely reuses comment from instance mapping `.DATA_WIDTH_A`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:193`
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

<a id="vg-finding-212"></a>
### VG066: Comment for instance mapping `.DEBUGGABLE` repeats or closely reuses comment from instance mapping `.DATA_WIDTH_A`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:194`
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

<a id="vg-finding-213"></a>
### VG066: Comment for instance mapping `.PACKABLE` repeats or closely reuses comment from instance mapping `.DATA_WIDTH_A`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:195`
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

<a id="vg-finding-214"></a>
### VG066: Comment for instance mapping `.FORCE_KEEP` repeats or closely reuses comment from instance mapping `.DATA_WIDTH_A`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:196`
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

<a id="vg-finding-215"></a>
### VG066: Comment for instance mapping `.INIT_FILE` repeats or closely reuses comment from instance mapping `.DATA_WIDTH_A`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:197`
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

<a id="vg-finding-216"></a>
### VG066: Comment for instance mapping `.FILL_ALL` repeats or closely reuses comment from instance mapping `.DATA_WIDTH_A`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:198`
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

<a id="vg-finding-217"></a>
### VG066: Comment for instance mapping `.doa` repeats or closely reuses comment from instance mapping `.dia`; write entity-specific RTL intent.
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

<a id="vg-finding-218"></a>
### VG066: Comment for instance mapping `.INIT_FILE` repeats or closely reuses comment from instance mapping `.DATA_WIDTH_A`; write entity-specific RTL intent.
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

<a id="vg-finding-219"></a>
### VG066: Comment for instance mapping `.doa` repeats or closely reuses comment from instance mapping `.dia`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:275`
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

<a id="vg-finding-220"></a>
### VG066: Comment for instance mapping `.INIT_FILE` repeats or closely reuses comment from instance mapping `.DATA_WIDTH_A`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_group.v:309`
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

<a id="vg-finding-221"></a>
### VG066: Comment for instance mapping `.doa` repeats or closely reuses comment from instance mapping `.dia`; write entity-specific RTL intent.
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

<a id="vg-finding-222"></a>
### VG054: FSM next-state if / else if chain must end with an explicit else branch.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:182`
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

<a id="vg-finding-223"></a>
### VG063: Case branch leading comment must be the pure comment line immediately above the block.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:158`
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

<a id="vg-finding-224"></a>
### VG063: Case branch leading comment must be the pure comment line immediately above the block.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:161`
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

<a id="vg-finding-225"></a>
### VG063: Case branch leading comment must be the pure comment line immediately above the block.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:164`
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

<a id="vg-finding-226"></a>
### VG063: Case branch leading comment must be the pure comment line immediately above the block.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:167`
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

<a id="vg-finding-227"></a>
### VG063: Case branch leading comment must be the pure comment line immediately above the block.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:170`
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

<a id="vg-finding-228"></a>
### VG063: Case branch leading comment must be the pure comment line immediately above the block.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:173`
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

<a id="vg-finding-229"></a>
### VG063: Case branch leading comment must be the pure comment line immediately above the block.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:176`
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

<a id="vg-finding-230"></a>
### VG063: Case branch leading comment must be the pure comment line immediately above the block.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:179`
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

<a id="vg-finding-231"></a>
### VG063: Case branch leading comment must be the pure comment line immediately above the block.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:182`
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

<a id="vg-finding-232"></a>
### VG063: Case branch leading comment must be the pure comment line immediately above the block.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:191`
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

<a id="vg-finding-233"></a>
### VG063: Case branch leading comment must be the pure comment line immediately above the block.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:194`
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

<a id="vg-finding-234"></a>
### VG024: Instance `u_group_alpha` should follow `<module>_Inst_<role>` naming when practical.
- Status: `failed`
- Severity: `warning`
- Location: `file:road_yolo_numeric_rom_probe.v:unknown`
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

<a id="vg-finding-235"></a>
### VG024: Instance `u_group_beta` should follow `<module>_Inst_<role>` naming when practical.
- Status: `failed`
- Severity: `warning`
- Location: `file:road_yolo_numeric_rom_probe.v:unknown`
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

<a id="vg-finding-236"></a>
### VG024: Instance `u_group_gamma` should follow `<module>_Inst_<role>` naming when practical.
- Status: `failed`
- Severity: `warning`
- Location: `file:road_yolo_numeric_rom_probe.v:unknown`
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

<a id="vg-finding-237"></a>
### VG024: Instance `u_group_delta` should follow `<module>_Inst_<role>` naming when practical.
- Status: `failed`
- Severity: `warning`
- Location: `file:road_yolo_numeric_rom_probe.v:unknown`
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

<a id="vg-finding-238"></a>
### VG024: Instance `u_group_epsilon` should follow `<module>_Inst_<role>` naming when practical.
- Status: `failed`
- Severity: `warning`
- Location: `file:road_yolo_numeric_rom_probe.v:unknown`
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

<a id="vg-finding-239"></a>
### VG024: Instance `u_group_zeta` should follow `<module>_Inst_<role>` naming when practical.
- Status: `failed`
- Severity: `warning`
- Location: `file:road_yolo_numeric_rom_probe.v:unknown`
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

<a id="vg-finding-240"></a>
### VG024: Instance `u_group_eta` should follow `<module>_Inst_<role>` naming when practical.
- Status: `failed`
- Severity: `warning`
- Location: `file:road_yolo_numeric_rom_probe.v:unknown`
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

<a id="vg-finding-241"></a>
### VG024: Instance `u_group_theta` should follow `<module>_Inst_<role>` naming when practical.
- Status: `failed`
- Severity: `warning`
- Location: `file:road_yolo_numeric_rom_probe.v:unknown`
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

<a id="vg-finding-242"></a>
### VG024: Instance `u_group_iota` should follow `<module>_Inst_<role>` naming when practical.
- Status: `failed`
- Severity: `warning`
- Location: `file:road_yolo_numeric_rom_probe.v:unknown`
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

<a id="vg-finding-243"></a>
### VG024: Instance `u_group_kappa` should follow `<module>_Inst_<role>` naming when practical.
- Status: `failed`
- Severity: `warning`
- Location: `file:road_yolo_numeric_rom_probe.v:unknown`
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

<a id="vg-finding-244"></a>
### VG024: Instance `u_group_lambda` should follow `<module>_Inst_<role>` naming when practical.
- Status: `failed`
- Severity: `warning`
- Location: `file:road_yolo_numeric_rom_probe.v:unknown`
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

<a id="vg-finding-245"></a>
### VG024: Instance `u_group_mu` should follow `<module>_Inst_<role>` naming when practical.
- Status: `failed`
- Severity: `warning`
- Location: `file:road_yolo_numeric_rom_probe.v:unknown`
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

<a id="vg-finding-246"></a>
### VG024: Instance `u_group_nu` should follow `<module>_Inst_<role>` naming when practical.
- Status: `failed`
- Severity: `warning`
- Location: `file:road_yolo_numeric_rom_probe.v:unknown`
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

<a id="vg-finding-247"></a>
### VG024: Instance `u_group_xi` should follow `<module>_Inst_<role>` naming when practical.
- Status: `failed`
- Severity: `warning`
- Location: `file:road_yolo_numeric_rom_probe.v:unknown`
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

<a id="vg-finding-248"></a>
### VG061: Item `always@(posedge i_clk or negedge i_rstn)` must be placed in 输出信号处理区域, not `状态任务处理区域`.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:209`
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

<a id="vg-finding-249"></a>
### VG061: Item `always@(posedge i_clk or negedge i_rstn)` must be placed in 输出信号处理区域, not `状态任务处理区域`.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:217`
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

<a id="vg-finding-250"></a>
### VG061: Item `always@(posedge i_clk or negedge i_rstn)` must be placed in 输出信号处理区域, not `状态任务处理区域`.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:229`
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

<a id="vg-finding-251"></a>
### VG061: Item `always@(posedge i_clk or negedge i_rstn)` must be placed in 输出信号处理区域, not `状态任务处理区域`.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:243`
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

<a id="vg-finding-252"></a>
### VG061: Item `always@(posedge i_clk or negedge i_rstn)` must be placed in 输出信号处理区域, not `状态任务处理区域`.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:251`
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

<a id="vg-finding-253"></a>
### VG061: Item `always@(posedge i_clk or negedge i_rstn)` must be placed in 输出信号处理区域, not `主要任务处理区域`.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:260`
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

<a id="vg-finding-254"></a>
### VG061: Item `always@(posedge i_clk or negedge i_rstn)` must be placed in 输出信号处理区域, not `主要任务处理区域`.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:268`
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

<a id="vg-finding-255"></a>
### VG061: Item `always@(posedge i_clk or negedge i_rstn)` must be placed in 输出信号处理区域, not `主要任务处理区域`.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:276`
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

<a id="vg-finding-256"></a>
### VG061: Item `always@(posedge i_clk or negedge i_rstn)` must be placed in 输出信号处理区域, not `主要任务处理区域`.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:284`
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

<a id="vg-finding-257"></a>
### VG061: Item `always@(posedge i_clk or negedge i_rstn)` must be placed in 输出信号处理区域, not `主要任务处理区域`.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:292`
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

<a id="vg-finding-258"></a>
### VG061: Item `always@(posedge i_clk or negedge i_rstn)` must be placed in 输出信号处理区域, not `主要任务处理区域`.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:300`
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

<a id="vg-finding-259"></a>
### VG061: Item `always@(posedge i_clk or negedge i_rstn)` must be placed in 输出信号处理区域, not `主要任务处理区域`.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:308`
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

<a id="vg-finding-260"></a>
### VG061: Item `always@(posedge i_clk or negedge i_rstn)` must be placed in 输出信号处理区域, not `主要任务处理区域`.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:316`
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

<a id="vg-finding-261"></a>
### VG061: Item `always@(posedge i_clk or negedge i_rstn)` must be placed in 输出信号处理区域, not `主要任务处理区域`.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:324`
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

<a id="vg-finding-262"></a>
### VG061: Item `always@(posedge i_clk or negedge i_rstn)` must be placed in 输出信号处理区域, not `主要任务处理区域`.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:332`
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

<a id="vg-finding-263"></a>
### VG061: Item `always@(posedge i_clk or negedge i_rstn)` must be placed in 输出信号处理区域, not `主要任务处理区域`.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:340`
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

<a id="vg-finding-264"></a>
### VG061: Item `always@(posedge i_clk or negedge i_rstn)` must be placed in 输出信号处理区域, not `主要任务处理区域`.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:348`
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

<a id="vg-finding-265"></a>
### VG061: Item `always@(posedge i_clk or negedge i_rstn)` must be placed in 输出信号处理区域, not `主要任务处理区域`.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:356`
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

<a id="vg-finding-266"></a>
### VG061: Item `always@(posedge i_clk or negedge i_rstn)` must be placed in 输出信号处理区域, not `主要任务处理区域`.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:364`
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

<a id="vg-finding-267"></a>
### VG071: `输出信号处理区域` order must follow module interface outputs ['done_o', 'checksum_o'], not ['checksum_o', 'done_o'].
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:138`
- Evidence:
- node_kind: `verilog_rtl`
- detail: output.mirror.order
- source_excerpt: `output.mirror.order`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `interface`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
output.mirror.order
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-268"></a>
### VG056: Comment for localparam `ST_ISSUE` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:62`
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

<a id="vg-finding-269"></a>
### VG041: Comment for localparam `ST_ISSUE` looks generic: `parameter`.
- Status: `failed`
- Severity: `warning`
- Location: `road_yolo_numeric_rom_probe.v:62`
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

<a id="vg-finding-270"></a>
### VG056: Comment for localparam `ST_WAIT_PHY` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:63`
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

<a id="vg-finding-271"></a>
### VG041: Comment for localparam `ST_WAIT_PHY` looks generic: `parameter`.
- Status: `failed`
- Severity: `warning`
- Location: `road_yolo_numeric_rom_probe.v:63`
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

<a id="vg-finding-272"></a>
### VG056: Comment for localparam `ST_WAIT_GROUP` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:64`
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

<a id="vg-finding-273"></a>
### VG041: Comment for localparam `ST_WAIT_GROUP` looks generic: `parameter`.
- Status: `failed`
- Severity: `warning`
- Location: `road_yolo_numeric_rom_probe.v:64`
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

<a id="vg-finding-274"></a>
### VG056: Comment for localparam `ST_WAIT_PAIR` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:65`
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

<a id="vg-finding-275"></a>
### VG041: Comment for localparam `ST_WAIT_PAIR` looks generic: `parameter`.
- Status: `failed`
- Severity: `warning`
- Location: `road_yolo_numeric_rom_probe.v:65`
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

<a id="vg-finding-276"></a>
### VG056: Comment for localparam `ST_WAIT_QUAD` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:66`
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

<a id="vg-finding-277"></a>
### VG041: Comment for localparam `ST_WAIT_QUAD` looks generic: `parameter`.
- Status: `failed`
- Severity: `warning`
- Location: `road_yolo_numeric_rom_probe.v:66`
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

<a id="vg-finding-278"></a>
### VG056: Comment for localparam `ST_WAIT_OCT` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:67`
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

<a id="vg-finding-279"></a>
### VG041: Comment for localparam `ST_WAIT_OCT` looks generic: `parameter`.
- Status: `failed`
- Severity: `warning`
- Location: `road_yolo_numeric_rom_probe.v:67`
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

<a id="vg-finding-280"></a>
### VG056: Comment for localparam `ST_WAIT_SELECT` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:68`
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

<a id="vg-finding-281"></a>
### VG041: Comment for localparam `ST_WAIT_SELECT` looks generic: `parameter`.
- Status: `failed`
- Severity: `warning`
- Location: `road_yolo_numeric_rom_probe.v:68`
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

<a id="vg-finding-282"></a>
### VG056: Comment for localparam `ST_CAPTURE` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:69`
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

<a id="vg-finding-283"></a>
### VG041: Comment for localparam `ST_CAPTURE` looks generic: `parameter`.
- Status: `failed`
- Severity: `warning`
- Location: `road_yolo_numeric_rom_probe.v:69`
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

<a id="vg-finding-284"></a>
### VG056: Comment for localparam `ST_BIT` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:70`
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

<a id="vg-finding-285"></a>
### VG041: Comment for localparam `ST_BIT` looks generic: `parameter`.
- Status: `failed`
- Severity: `warning`
- Location: `road_yolo_numeric_rom_probe.v:70`
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

<a id="vg-finding-286"></a>
### VG056: Comment for localparam `ST_DONE` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:71`
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

<a id="vg-finding-287"></a>
### VG041: Comment for localparam `ST_DONE` looks generic: `parameter`.
- Status: `failed`
- Severity: `warning`
- Location: `road_yolo_numeric_rom_probe.v:71`
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

<a id="vg-finding-288"></a>
### VG056: Comment for port `i_clk` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:53`
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

<a id="vg-finding-289"></a>
### VG041: Comment for port `i_clk` looks generic: `port signal`.
- Status: `failed`
- Severity: `warning`
- Location: `road_yolo_numeric_rom_probe.v:53`
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

<a id="vg-finding-290"></a>
### VG056: Comment for port `i_rstn` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:54`
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

<a id="vg-finding-291"></a>
### VG041: Comment for port `i_rstn` looks generic: `port signal`.
- Status: `failed`
- Severity: `warning`
- Location: `road_yolo_numeric_rom_probe.v:54`
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

<a id="vg-finding-292"></a>
### VG056: Comment for port `o_done` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:57`
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

<a id="vg-finding-293"></a>
### VG041: Comment for port `o_done` looks generic: `port signal`.
- Status: `failed`
- Severity: `warning`
- Location: `road_yolo_numeric_rom_probe.v:57`
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

<a id="vg-finding-294"></a>
### VG056: Comment for port `o_checksum` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:58`
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

<a id="vg-finding-295"></a>
### VG041: Comment for port `o_checksum` looks generic: `port signal`.
- Status: `failed`
- Severity: `warning`
- Location: `road_yolo_numeric_rom_probe.v:58`
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

<a id="vg-finding-296"></a>
### VG056: Comment for signal `group_alpha_data` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:75`
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

<a id="vg-finding-297"></a>
### VG041: Comment for signal `group_alpha_data` looks generic: `signal`.
- Status: `failed`
- Severity: `warning`
- Location: `road_yolo_numeric_rom_probe.v:75`
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

<a id="vg-finding-298"></a>
### VG056: Comment for signal `group_beta_data` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:76`
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

<a id="vg-finding-299"></a>
### VG041: Comment for signal `group_beta_data` looks generic: `signal`.
- Status: `failed`
- Severity: `warning`
- Location: `road_yolo_numeric_rom_probe.v:76`
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

<a id="vg-finding-300"></a>
### VG056: Comment for signal `group_gamma_data` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:77`
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

<a id="vg-finding-301"></a>
### VG041: Comment for signal `group_gamma_data` looks generic: `signal`.
- Status: `failed`
- Severity: `warning`
- Location: `road_yolo_numeric_rom_probe.v:77`
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

<a id="vg-finding-302"></a>
### VG056: Comment for signal `group_delta_data` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:78`
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

<a id="vg-finding-303"></a>
### VG041: Comment for signal `group_delta_data` looks generic: `signal`.
- Status: `failed`
- Severity: `warning`
- Location: `road_yolo_numeric_rom_probe.v:78`
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

<a id="vg-finding-304"></a>
### VG056: Comment for signal `group_epsilon_data` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:79`
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

<a id="vg-finding-305"></a>
### VG041: Comment for signal `group_epsilon_data` looks generic: `signal`.
- Status: `failed`
- Severity: `warning`
- Location: `road_yolo_numeric_rom_probe.v:79`
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

<a id="vg-finding-306"></a>
### VG056: Comment for signal `group_zeta_data` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:80`
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

<a id="vg-finding-307"></a>
### VG041: Comment for signal `group_zeta_data` looks generic: `signal`.
- Status: `failed`
- Severity: `warning`
- Location: `road_yolo_numeric_rom_probe.v:80`
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

<a id="vg-finding-308"></a>
### VG056: Comment for signal `group_eta_data` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:81`
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

<a id="vg-finding-309"></a>
### VG041: Comment for signal `group_eta_data` looks generic: `signal`.
- Status: `failed`
- Severity: `warning`
- Location: `road_yolo_numeric_rom_probe.v:81`
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

<a id="vg-finding-310"></a>
### VG056: Comment for signal `group_theta_data` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:82`
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

<a id="vg-finding-311"></a>
### VG041: Comment for signal `group_theta_data` looks generic: `signal`.
- Status: `failed`
- Severity: `warning`
- Location: `road_yolo_numeric_rom_probe.v:82`
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

<a id="vg-finding-312"></a>
### VG056: Comment for signal `group_iota_data` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:83`
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

<a id="vg-finding-313"></a>
### VG041: Comment for signal `group_iota_data` looks generic: `signal`.
- Status: `failed`
- Severity: `warning`
- Location: `road_yolo_numeric_rom_probe.v:83`
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

<a id="vg-finding-314"></a>
### VG056: Comment for signal `group_kappa_data` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:84`
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

<a id="vg-finding-315"></a>
### VG041: Comment for signal `group_kappa_data` looks generic: `signal`.
- Status: `failed`
- Severity: `warning`
- Location: `road_yolo_numeric_rom_probe.v:84`
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

<a id="vg-finding-316"></a>
### VG056: Comment for signal `group_lambda_data` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:85`
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

<a id="vg-finding-317"></a>
### VG041: Comment for signal `group_lambda_data` looks generic: `signal`.
- Status: `failed`
- Severity: `warning`
- Location: `road_yolo_numeric_rom_probe.v:85`
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

<a id="vg-finding-318"></a>
### VG056: Comment for signal `group_mu_data` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:86`
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

<a id="vg-finding-319"></a>
### VG041: Comment for signal `group_mu_data` looks generic: `signal`.
- Status: `failed`
- Severity: `warning`
- Location: `road_yolo_numeric_rom_probe.v:86`
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

<a id="vg-finding-320"></a>
### VG056: Comment for signal `group_nu_data` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:87`
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

<a id="vg-finding-321"></a>
### VG041: Comment for signal `group_nu_data` looks generic: `signal`.
- Status: `failed`
- Severity: `warning`
- Location: `road_yolo_numeric_rom_probe.v:87`
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

<a id="vg-finding-322"></a>
### VG056: Comment for signal `group_xi_data` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:88`
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

<a id="vg-finding-323"></a>
### VG041: Comment for signal `group_xi_data` looks generic: `signal`.
- Status: `failed`
- Severity: `warning`
- Location: `road_yolo_numeric_rom_probe.v:88`
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

<a id="vg-finding-324"></a>
### VG056: Comment for signal `state_current` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:91`
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

<a id="vg-finding-325"></a>
### VG041: Comment for signal `state_current` looks generic: `signal`.
- Status: `failed`
- Severity: `warning`
- Location: `road_yolo_numeric_rom_probe.v:91`
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

<a id="vg-finding-326"></a>
### VG056: Comment for signal `state_next` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:92`
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

<a id="vg-finding-327"></a>
### VG041: Comment for signal `state_next` looks generic: `signal`.
- Status: `failed`
- Severity: `warning`
- Location: `road_yolo_numeric_rom_probe.v:92`
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

<a id="vg-finding-328"></a>
### VG056: Comment for signal `crc_bit_mix` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:95`
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

<a id="vg-finding-329"></a>
### VG041: Comment for signal `crc_bit_mix` looks generic: `signal`.
- Status: `failed`
- Severity: `warning`
- Location: `road_yolo_numeric_rom_probe.v:95`
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

<a id="vg-finding-330"></a>
### VG056: Comment for signal `crc_shifted` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:96`
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

<a id="vg-finding-331"></a>
### VG041: Comment for signal `crc_shifted` looks generic: `signal`.
- Status: `failed`
- Severity: `warning`
- Location: `road_yolo_numeric_rom_probe.v:96`
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

<a id="vg-finding-332"></a>
### VG056: Comment for signal `crc_updated` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:97`
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

<a id="vg-finding-333"></a>
### VG041: Comment for signal `crc_updated` looks generic: `signal`.
- Status: `failed`
- Severity: `warning`
- Location: `road_yolo_numeric_rom_probe.v:97`
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

<a id="vg-finding-334"></a>
### VG056: Comment for signal `final_bit` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:98`
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

<a id="vg-finding-335"></a>
### VG041: Comment for signal `final_bit` looks generic: `signal`.
- Status: `failed`
- Severity: `warning`
- Location: `road_yolo_numeric_rom_probe.v:98`
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

<a id="vg-finding-336"></a>
### VG056: Comment for signal `done_o` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:102`
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

<a id="vg-finding-337"></a>
### VG041: Comment for signal `done_o` looks generic: `signal`.
- Status: `failed`
- Severity: `warning`
- Location: `road_yolo_numeric_rom_probe.v:102`
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

<a id="vg-finding-338"></a>
### VG056: Comment for signal `checksum_o` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:103`
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

<a id="vg-finding-339"></a>
### VG041: Comment for signal `checksum_o` looks generic: `signal`.
- Status: `failed`
- Severity: `warning`
- Location: `road_yolo_numeric_rom_probe.v:103`
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

<a id="vg-finding-340"></a>
### VG056: Comment for signal `group_index_o` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:104`
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

<a id="vg-finding-341"></a>
### VG041: Comment for signal `group_index_o` looks generic: `signal`.
- Status: `failed`
- Severity: `warning`
- Location: `road_yolo_numeric_rom_probe.v:104`
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

<a id="vg-finding-342"></a>
### VG056: Comment for signal `word_addr_o` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:105`
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

<a id="vg-finding-343"></a>
### VG041: Comment for signal `word_addr_o` looks generic: `signal`.
- Status: `failed`
- Severity: `warning`
- Location: `road_yolo_numeric_rom_probe.v:105`
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

<a id="vg-finding-344"></a>
### VG056: Comment for signal `bit_index_o` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:106`
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

<a id="vg-finding-345"></a>
### VG041: Comment for signal `bit_index_o` looks generic: `signal`.
- Status: `failed`
- Severity: `warning`
- Location: `road_yolo_numeric_rom_probe.v:106`
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

<a id="vg-finding-346"></a>
### VG056: Comment for signal `word_buffer_o` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:107`
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

<a id="vg-finding-347"></a>
### VG041: Comment for signal `word_buffer_o` looks generic: `signal`.
- Status: `failed`
- Severity: `warning`
- Location: `road_yolo_numeric_rom_probe.v:107`
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

<a id="vg-finding-348"></a>
### VG056: Comment for signal `crc_o` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:108`
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

<a id="vg-finding-349"></a>
### VG041: Comment for signal `crc_o` looks generic: `signal`.
- Status: `failed`
- Severity: `warning`
- Location: `road_yolo_numeric_rom_probe.v:108`
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

<a id="vg-finding-350"></a>
### VG056: Comment for signal `pair_alpha_o` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:109`
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

<a id="vg-finding-351"></a>
### VG041: Comment for signal `pair_alpha_o` looks generic: `signal`.
- Status: `failed`
- Severity: `warning`
- Location: `road_yolo_numeric_rom_probe.v:109`
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

<a id="vg-finding-352"></a>
### VG056: Comment for signal `pair_beta_o` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:110`
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

<a id="vg-finding-353"></a>
### VG041: Comment for signal `pair_beta_o` looks generic: `signal`.
- Status: `failed`
- Severity: `warning`
- Location: `road_yolo_numeric_rom_probe.v:110`
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

<a id="vg-finding-354"></a>
### VG056: Comment for signal `pair_gamma_o` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:111`
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

<a id="vg-finding-355"></a>
### VG041: Comment for signal `pair_gamma_o` looks generic: `signal`.
- Status: `failed`
- Severity: `warning`
- Location: `road_yolo_numeric_rom_probe.v:111`
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

<a id="vg-finding-356"></a>
### VG056: Comment for signal `pair_delta_o` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:112`
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

<a id="vg-finding-357"></a>
### VG041: Comment for signal `pair_delta_o` looks generic: `signal`.
- Status: `failed`
- Severity: `warning`
- Location: `road_yolo_numeric_rom_probe.v:112`
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

<a id="vg-finding-358"></a>
### VG056: Comment for signal `pair_epsilon_o` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:113`
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

<a id="vg-finding-359"></a>
### VG041: Comment for signal `pair_epsilon_o` looks generic: `signal`.
- Status: `failed`
- Severity: `warning`
- Location: `road_yolo_numeric_rom_probe.v:113`
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

<a id="vg-finding-360"></a>
### VG056: Comment for signal `pair_zeta_o` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:114`
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

<a id="vg-finding-361"></a>
### VG041: Comment for signal `pair_zeta_o` looks generic: `signal`.
- Status: `failed`
- Severity: `warning`
- Location: `road_yolo_numeric_rom_probe.v:114`
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

<a id="vg-finding-362"></a>
### VG056: Comment for signal `pair_eta_o` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:115`
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

<a id="vg-finding-363"></a>
### VG041: Comment for signal `pair_eta_o` looks generic: `signal`.
- Status: `failed`
- Severity: `warning`
- Location: `road_yolo_numeric_rom_probe.v:115`
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

<a id="vg-finding-364"></a>
### VG056: Comment for signal `quad_alpha_o` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:116`
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

<a id="vg-finding-365"></a>
### VG041: Comment for signal `quad_alpha_o` looks generic: `signal`.
- Status: `failed`
- Severity: `warning`
- Location: `road_yolo_numeric_rom_probe.v:116`
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

<a id="vg-finding-366"></a>
### VG056: Comment for signal `quad_beta_o` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:117`
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

<a id="vg-finding-367"></a>
### VG041: Comment for signal `quad_beta_o` looks generic: `signal`.
- Status: `failed`
- Severity: `warning`
- Location: `road_yolo_numeric_rom_probe.v:117`
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

<a id="vg-finding-368"></a>
### VG056: Comment for signal `quad_gamma_o` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:118`
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

<a id="vg-finding-369"></a>
### VG041: Comment for signal `quad_gamma_o` looks generic: `signal`.
- Status: `failed`
- Severity: `warning`
- Location: `road_yolo_numeric_rom_probe.v:118`
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

<a id="vg-finding-370"></a>
### VG056: Comment for signal `quad_delta_o` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:119`
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

<a id="vg-finding-371"></a>
### VG041: Comment for signal `quad_delta_o` looks generic: `signal`.
- Status: `failed`
- Severity: `warning`
- Location: `road_yolo_numeric_rom_probe.v:119`
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

<a id="vg-finding-372"></a>
### VG056: Comment for signal `oct_lower_o` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:120`
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

<a id="vg-finding-373"></a>
### VG041: Comment for signal `oct_lower_o` looks generic: `signal`.
- Status: `failed`
- Severity: `warning`
- Location: `road_yolo_numeric_rom_probe.v:120`
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

<a id="vg-finding-374"></a>
### VG056: Comment for signal `oct_upper_o` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:121`
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

<a id="vg-finding-375"></a>
### VG041: Comment for signal `oct_upper_o` looks generic: `signal`.
- Status: `failed`
- Severity: `warning`
- Location: `road_yolo_numeric_rom_probe.v:121`
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

<a id="vg-finding-376"></a>
### VG056: Comment for signal `selected_word_o` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:122`
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

<a id="vg-finding-377"></a>
### VG041: Comment for signal `selected_word_o` looks generic: `signal`.
- Status: `failed`
- Severity: `warning`
- Location: `road_yolo_numeric_rom_probe.v:122`
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

<a id="vg-finding-378"></a>
### VG056: Comment for assign `crc_bit_mix` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:126`
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

<a id="vg-finding-379"></a>
### VG041: Comment for assign `crc_bit_mix` looks generic: `assign`.
- Status: `failed`
- Severity: `warning`
- Location: `road_yolo_numeric_rom_probe.v:126`
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

<a id="vg-finding-380"></a>
### VG056: Comment for assign `crc_shifted` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:127`
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

<a id="vg-finding-381"></a>
### VG041: Comment for assign `crc_shifted` looks generic: `assign`.
- Status: `failed`
- Severity: `warning`
- Location: `road_yolo_numeric_rom_probe.v:127`
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

<a id="vg-finding-382"></a>
### VG056: Comment for assign `crc_updated` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:128`
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

<a id="vg-finding-383"></a>
### VG041: Comment for assign `crc_updated` looks generic: `assign`.
- Status: `failed`
- Severity: `warning`
- Location: `road_yolo_numeric_rom_probe.v:128`
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

<a id="vg-finding-384"></a>
### VG056: Comment for assign `final_bit` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:129`
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

<a id="vg-finding-385"></a>
### VG041: Comment for assign `final_bit` looks generic: `assign`.
- Status: `failed`
- Severity: `warning`
- Location: `road_yolo_numeric_rom_probe.v:129`
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

<a id="vg-finding-386"></a>
### VG056: Comment for assign `o_done` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:133`
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

<a id="vg-finding-387"></a>
### VG041: Comment for assign `o_done` looks generic: `assign`.
- Status: `failed`
- Severity: `warning`
- Location: `road_yolo_numeric_rom_probe.v:133`
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

<a id="vg-finding-388"></a>
### VG056: Comment for assign `o_checksum` still uses formatter fallback text.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:134`
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

<a id="vg-finding-389"></a>
### VG041: Comment for assign `o_checksum` looks generic: `assign`.
- Status: `failed`
- Severity: `warning`
- Location: `road_yolo_numeric_rom_probe.v:134`
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

<a id="vg-finding-390"></a>
### VG040: Always block `always@(posedge i_clk or negedge i_rstn)` should have a nearby leading comment explaining behavior.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:146`
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

<a id="vg-finding-391"></a>
### VG040: Always block `always@(*)` should have a nearby leading comment explaining behavior.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:155`
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

<a id="vg-finding-392"></a>
### VG040: Always block `always@(posedge i_clk or negedge i_rstn)` should have a nearby leading comment explaining behavior.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:200`
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

<a id="vg-finding-393"></a>
### VG040: Always block `always@(posedge i_clk or negedge i_rstn)` should have a nearby leading comment explaining behavior.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:209`
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

<a id="vg-finding-394"></a>
### VG040: Always block `always@(posedge i_clk or negedge i_rstn)` should have a nearby leading comment explaining behavior.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:217`
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

<a id="vg-finding-395"></a>
### VG040: Always block `always@(posedge i_clk or negedge i_rstn)` should have a nearby leading comment explaining behavior.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:229`
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

<a id="vg-finding-396"></a>
### VG040: Always block `always@(posedge i_clk or negedge i_rstn)` should have a nearby leading comment explaining behavior.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:243`
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

<a id="vg-finding-397"></a>
### VG040: Always block `always@(posedge i_clk or negedge i_rstn)` should have a nearby leading comment explaining behavior.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:251`
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

<a id="vg-finding-398"></a>
### VG040: Always block `always@(posedge i_clk or negedge i_rstn)` should have a nearby leading comment explaining behavior.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:260`
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

<a id="vg-finding-399"></a>
### VG040: Always block `always@(posedge i_clk or negedge i_rstn)` should have a nearby leading comment explaining behavior.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:268`
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

<a id="vg-finding-400"></a>
### VG040: Always block `always@(posedge i_clk or negedge i_rstn)` should have a nearby leading comment explaining behavior.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:276`
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

<a id="vg-finding-401"></a>
### VG040: Always block `always@(posedge i_clk or negedge i_rstn)` should have a nearby leading comment explaining behavior.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:284`
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

<a id="vg-finding-402"></a>
### VG040: Always block `always@(posedge i_clk or negedge i_rstn)` should have a nearby leading comment explaining behavior.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:292`
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

<a id="vg-finding-403"></a>
### VG040: Always block `always@(posedge i_clk or negedge i_rstn)` should have a nearby leading comment explaining behavior.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:300`
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

<a id="vg-finding-404"></a>
### VG040: Always block `always@(posedge i_clk or negedge i_rstn)` should have a nearby leading comment explaining behavior.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:308`
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

<a id="vg-finding-405"></a>
### VG040: Always block `always@(posedge i_clk or negedge i_rstn)` should have a nearby leading comment explaining behavior.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:316`
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

<a id="vg-finding-406"></a>
### VG040: Always block `always@(posedge i_clk or negedge i_rstn)` should have a nearby leading comment explaining behavior.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:324`
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

<a id="vg-finding-407"></a>
### VG040: Always block `always@(posedge i_clk or negedge i_rstn)` should have a nearby leading comment explaining behavior.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:332`
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

<a id="vg-finding-408"></a>
### VG040: Always block `always@(posedge i_clk or negedge i_rstn)` should have a nearby leading comment explaining behavior.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:340`
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

<a id="vg-finding-409"></a>
### VG040: Always block `always@(posedge i_clk or negedge i_rstn)` should have a nearby leading comment explaining behavior.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:348`
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

<a id="vg-finding-410"></a>
### VG040: Always block `always@(posedge i_clk or negedge i_rstn)` should have a nearby leading comment explaining behavior.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:356`
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

<a id="vg-finding-411"></a>
### VG040: Always block `always@(posedge i_clk or negedge i_rstn)` should have a nearby leading comment explaining behavior.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:364`
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

<a id="vg-finding-412"></a>
### VG040: Instance `u_group_alpha` should have a leading function/connection comment.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:378`
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

<a id="vg-finding-413"></a>
### VG040: Instance `u_group_beta` should have a leading function/connection comment.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:390`
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

<a id="vg-finding-414"></a>
### VG040: Instance `u_group_gamma` should have a leading function/connection comment.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:402`
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

<a id="vg-finding-415"></a>
### VG040: Instance `u_group_delta` should have a leading function/connection comment.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:414`
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

<a id="vg-finding-416"></a>
### VG040: Instance `u_group_epsilon` should have a leading function/connection comment.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:426`
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

<a id="vg-finding-417"></a>
### VG040: Instance `u_group_zeta` should have a leading function/connection comment.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:438`
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

<a id="vg-finding-418"></a>
### VG040: Instance `u_group_eta` should have a leading function/connection comment.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:450`
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

<a id="vg-finding-419"></a>
### VG040: Instance `u_group_theta` should have a leading function/connection comment.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:462`
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

<a id="vg-finding-420"></a>
### VG040: Instance `u_group_iota` should have a leading function/connection comment.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:474`
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

<a id="vg-finding-421"></a>
### VG040: Instance `u_group_kappa` should have a leading function/connection comment.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:486`
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

<a id="vg-finding-422"></a>
### VG040: Instance `u_group_lambda` should have a leading function/connection comment.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:498`
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

<a id="vg-finding-423"></a>
### VG040: Instance `u_group_mu` should have a leading function/connection comment.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:510`
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

<a id="vg-finding-424"></a>
### VG040: Instance `u_group_nu` should have a leading function/connection comment.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:522`
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

<a id="vg-finding-425"></a>
### VG040: Instance `u_group_xi` should have a leading function/connection comment.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:534`
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

<a id="vg-finding-426"></a>
### VG062: process assignment `checksum_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:140`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `checksum_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:142`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `done_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:148`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `done_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:150`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `state_next` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:156`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `state_next` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:159`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `state_next` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:162`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `state_next` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:165`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `state_next` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:168`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `state_next` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:171`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `state_next` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:174`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `state_next` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:177`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `state_next` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:180`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `state_next` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:185`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `state_next` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:187`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `state_next` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:192`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `state_next` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:195`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
- Location: `road_yolo_numeric_rom_probe.v:202`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `state_current` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:204`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `group_index_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:211`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `group_index_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:213`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `word_addr_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:219`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `word_addr_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:222`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `word_addr_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:224`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `bit_index_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:231`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `bit_index_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:233`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `bit_index_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:236`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `bit_index_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:238`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `word_buffer_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:245`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `word_buffer_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:247`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `crc_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:253`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `crc_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:255`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `pair_alpha_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:262`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `pair_alpha_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:264`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `pair_beta_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:270`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `pair_beta_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:272`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `pair_gamma_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:278`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `pair_gamma_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:280`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `pair_delta_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:286`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `pair_delta_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:288`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `pair_epsilon_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:294`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `pair_epsilon_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:296`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `pair_zeta_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:302`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `pair_zeta_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:304`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `pair_eta_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:310`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `pair_eta_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:312`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `quad_alpha_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:318`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `quad_alpha_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:320`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `quad_beta_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:326`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `quad_beta_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:328`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `quad_gamma_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:334`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `quad_gamma_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:336`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `quad_delta_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:342`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `quad_delta_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:344`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `oct_lower_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:350`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `oct_lower_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:352`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `oct_upper_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:358`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `oct_upper_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:360`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `selected_word_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:366`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `selected_word_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:368`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG065: signal `crc_bit_mix` must be introduced by a group comment in `其他信号`.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:95`
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

<a id="vg-finding-487"></a>
### VG066: Comment for instance mapping `.i_clk` repeats or closely reuses comment from instance mapping `.i_clk`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:391`
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

<a id="vg-finding-488"></a>
### VG066: Comment for instance mapping `.i_rstn` repeats or closely reuses comment from instance mapping `.i_rstn`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:392`
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

<a id="vg-finding-489"></a>
### VG066: Comment for instance mapping `.i_word_addr` repeats or closely reuses comment from instance mapping `.i_word_addr`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:393`
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

<a id="vg-finding-490"></a>
### VG066: Comment for instance mapping `.C_LANE_ALPHA_FILE` repeats or closely reuses comment from instance mapping `.C_LANE_ALPHA_FILE`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:398`
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

<a id="vg-finding-491"></a>
### VG066: Comment for instance mapping `.C_LANE_BETA_FILE` repeats or closely reuses comment from instance mapping `.C_LANE_BETA_FILE`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:399`
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

<a id="vg-finding-492"></a>
### VG066: Comment for instance mapping `.C_LANE_GAMMA_FILE` repeats or closely reuses comment from instance mapping `.C_LANE_GAMMA_FILE`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:400`
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

<a id="vg-finding-493"></a>
### VG066: Comment for instance mapping `.i_clk` repeats or closely reuses comment from instance mapping `.i_clk`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:403`
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

<a id="vg-finding-494"></a>
### VG066: Comment for instance mapping `.i_rstn` repeats or closely reuses comment from instance mapping `.i_rstn`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:404`
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

<a id="vg-finding-495"></a>
### VG066: Comment for instance mapping `.i_word_addr` repeats or closely reuses comment from instance mapping `.i_word_addr`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:405`
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

<a id="vg-finding-496"></a>
### VG066: Comment for instance mapping `.C_LANE_ALPHA_FILE` repeats or closely reuses comment from instance mapping `.C_LANE_ALPHA_FILE`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:410`
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

<a id="vg-finding-497"></a>
### VG066: Comment for instance mapping `.C_LANE_BETA_FILE` repeats or closely reuses comment from instance mapping `.C_LANE_BETA_FILE`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:411`
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

<a id="vg-finding-498"></a>
### VG066: Comment for instance mapping `.C_LANE_GAMMA_FILE` repeats or closely reuses comment from instance mapping `.C_LANE_GAMMA_FILE`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:412`
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

<a id="vg-finding-499"></a>
### VG066: Comment for instance mapping `.i_clk` repeats or closely reuses comment from instance mapping `.i_clk`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:415`
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

<a id="vg-finding-500"></a>
### VG066: Comment for instance mapping `.i_rstn` repeats or closely reuses comment from instance mapping `.i_rstn`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:416`
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

<a id="vg-finding-501"></a>
### VG066: Comment for instance mapping `.i_word_addr` repeats or closely reuses comment from instance mapping `.i_word_addr`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:417`
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

<a id="vg-finding-502"></a>
### VG066: Comment for instance mapping `.C_LANE_ALPHA_FILE` repeats or closely reuses comment from instance mapping `.C_LANE_ALPHA_FILE`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:422`
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

<a id="vg-finding-503"></a>
### VG066: Comment for instance mapping `.C_LANE_BETA_FILE` repeats or closely reuses comment from instance mapping `.C_LANE_BETA_FILE`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:423`
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

<a id="vg-finding-504"></a>
### VG066: Comment for instance mapping `.C_LANE_GAMMA_FILE` repeats or closely reuses comment from instance mapping `.C_LANE_GAMMA_FILE`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:424`
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

<a id="vg-finding-505"></a>
### VG066: Comment for instance mapping `.i_clk` repeats or closely reuses comment from instance mapping `.i_clk`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:427`
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

<a id="vg-finding-506"></a>
### VG066: Comment for instance mapping `.i_rstn` repeats or closely reuses comment from instance mapping `.i_rstn`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:428`
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

<a id="vg-finding-507"></a>
### VG066: Comment for instance mapping `.i_word_addr` repeats or closely reuses comment from instance mapping `.i_word_addr`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:429`
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

<a id="vg-finding-508"></a>
### VG066: Comment for instance mapping `.C_LANE_ALPHA_FILE` repeats or closely reuses comment from instance mapping `.C_LANE_ALPHA_FILE`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:434`
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

<a id="vg-finding-509"></a>
### VG066: Comment for instance mapping `.C_LANE_BETA_FILE` repeats or closely reuses comment from instance mapping `.C_LANE_BETA_FILE`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:435`
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

<a id="vg-finding-510"></a>
### VG066: Comment for instance mapping `.C_LANE_GAMMA_FILE` repeats or closely reuses comment from instance mapping `.C_LANE_GAMMA_FILE`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:436`
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

<a id="vg-finding-511"></a>
### VG066: Comment for instance mapping `.i_clk` repeats or closely reuses comment from instance mapping `.i_clk`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:439`
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

<a id="vg-finding-512"></a>
### VG066: Comment for instance mapping `.i_rstn` repeats or closely reuses comment from instance mapping `.i_rstn`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:440`
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

<a id="vg-finding-513"></a>
### VG066: Comment for instance mapping `.i_word_addr` repeats or closely reuses comment from instance mapping `.i_word_addr`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:441`
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

<a id="vg-finding-514"></a>
### VG066: Comment for instance mapping `.C_LANE_ALPHA_FILE` repeats or closely reuses comment from instance mapping `.C_LANE_ALPHA_FILE`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:446`
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

<a id="vg-finding-515"></a>
### VG066: Comment for instance mapping `.C_LANE_BETA_FILE` repeats or closely reuses comment from instance mapping `.C_LANE_BETA_FILE`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:447`
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

<a id="vg-finding-516"></a>
### VG066: Comment for instance mapping `.C_LANE_GAMMA_FILE` repeats or closely reuses comment from instance mapping `.C_LANE_GAMMA_FILE`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:448`
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

<a id="vg-finding-517"></a>
### VG066: Comment for instance mapping `.i_clk` repeats or closely reuses comment from instance mapping `.i_clk`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:451`
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

<a id="vg-finding-518"></a>
### VG066: Comment for instance mapping `.i_rstn` repeats or closely reuses comment from instance mapping `.i_rstn`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:452`
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

<a id="vg-finding-519"></a>
### VG066: Comment for instance mapping `.i_word_addr` repeats or closely reuses comment from instance mapping `.i_word_addr`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:453`
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

<a id="vg-finding-520"></a>
### VG066: Comment for instance mapping `.C_LANE_ALPHA_FILE` repeats or closely reuses comment from instance mapping `.C_LANE_ALPHA_FILE`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:458`
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

<a id="vg-finding-521"></a>
### VG066: Comment for instance mapping `.C_LANE_BETA_FILE` repeats or closely reuses comment from instance mapping `.C_LANE_BETA_FILE`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:459`
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

<a id="vg-finding-522"></a>
### VG066: Comment for instance mapping `.C_LANE_GAMMA_FILE` repeats or closely reuses comment from instance mapping `.C_LANE_GAMMA_FILE`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:460`
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

<a id="vg-finding-523"></a>
### VG066: Comment for instance mapping `.i_clk` repeats or closely reuses comment from instance mapping `.i_clk`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:463`
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

<a id="vg-finding-524"></a>
### VG066: Comment for instance mapping `.i_rstn` repeats or closely reuses comment from instance mapping `.i_rstn`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:464`
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

<a id="vg-finding-525"></a>
### VG066: Comment for instance mapping `.i_word_addr` repeats or closely reuses comment from instance mapping `.i_word_addr`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:465`
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

<a id="vg-finding-526"></a>
### VG066: Comment for instance mapping `.C_LANE_ALPHA_FILE` repeats or closely reuses comment from instance mapping `.C_LANE_ALPHA_FILE`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:470`
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

<a id="vg-finding-527"></a>
### VG066: Comment for instance mapping `.C_LANE_BETA_FILE` repeats or closely reuses comment from instance mapping `.C_LANE_BETA_FILE`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:471`
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

<a id="vg-finding-528"></a>
### VG066: Comment for instance mapping `.C_LANE_GAMMA_FILE` repeats or closely reuses comment from instance mapping `.C_LANE_GAMMA_FILE`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:472`
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

<a id="vg-finding-529"></a>
### VG066: Comment for instance mapping `.i_clk` repeats or closely reuses comment from instance mapping `.i_clk`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:475`
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

<a id="vg-finding-530"></a>
### VG066: Comment for instance mapping `.i_rstn` repeats or closely reuses comment from instance mapping `.i_rstn`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:476`
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

<a id="vg-finding-531"></a>
### VG066: Comment for instance mapping `.i_word_addr` repeats or closely reuses comment from instance mapping `.i_word_addr`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:477`
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

<a id="vg-finding-532"></a>
### VG066: Comment for instance mapping `.C_LANE_ALPHA_FILE` repeats or closely reuses comment from instance mapping `.C_LANE_ALPHA_FILE`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:482`
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

<a id="vg-finding-533"></a>
### VG066: Comment for instance mapping `.C_LANE_BETA_FILE` repeats or closely reuses comment from instance mapping `.C_LANE_BETA_FILE`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:483`
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

<a id="vg-finding-534"></a>
### VG066: Comment for instance mapping `.C_LANE_GAMMA_FILE` repeats or closely reuses comment from instance mapping `.C_LANE_GAMMA_FILE`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:484`
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

<a id="vg-finding-535"></a>
### VG066: Comment for instance mapping `.i_clk` repeats or closely reuses comment from instance mapping `.i_clk`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:487`
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

<a id="vg-finding-536"></a>
### VG066: Comment for instance mapping `.i_rstn` repeats or closely reuses comment from instance mapping `.i_rstn`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:488`
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

<a id="vg-finding-537"></a>
### VG066: Comment for instance mapping `.i_word_addr` repeats or closely reuses comment from instance mapping `.i_word_addr`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:489`
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

<a id="vg-finding-538"></a>
### VG066: Comment for instance mapping `.C_LANE_ALPHA_FILE` repeats or closely reuses comment from instance mapping `.C_LANE_ALPHA_FILE`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:494`
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

<a id="vg-finding-539"></a>
### VG066: Comment for instance mapping `.C_LANE_BETA_FILE` repeats or closely reuses comment from instance mapping `.C_LANE_BETA_FILE`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:495`
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

<a id="vg-finding-540"></a>
### VG066: Comment for instance mapping `.C_LANE_GAMMA_FILE` repeats or closely reuses comment from instance mapping `.C_LANE_GAMMA_FILE`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:496`
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

<a id="vg-finding-541"></a>
### VG066: Comment for instance mapping `.i_clk` repeats or closely reuses comment from instance mapping `.i_clk`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:499`
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

<a id="vg-finding-542"></a>
### VG066: Comment for instance mapping `.i_rstn` repeats or closely reuses comment from instance mapping `.i_rstn`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:500`
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

<a id="vg-finding-543"></a>
### VG066: Comment for instance mapping `.i_word_addr` repeats or closely reuses comment from instance mapping `.i_word_addr`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:501`
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

<a id="vg-finding-544"></a>
### VG066: Comment for instance mapping `.C_LANE_ALPHA_FILE` repeats or closely reuses comment from instance mapping `.C_LANE_ALPHA_FILE`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:506`
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

<a id="vg-finding-545"></a>
### VG066: Comment for instance mapping `.C_LANE_BETA_FILE` repeats or closely reuses comment from instance mapping `.C_LANE_BETA_FILE`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:507`
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

<a id="vg-finding-546"></a>
### VG066: Comment for instance mapping `.C_LANE_GAMMA_FILE` repeats or closely reuses comment from instance mapping `.C_LANE_GAMMA_FILE`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:508`
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

<a id="vg-finding-547"></a>
### VG066: Comment for instance mapping `.i_clk` repeats or closely reuses comment from instance mapping `.i_clk`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:511`
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

<a id="vg-finding-548"></a>
### VG066: Comment for instance mapping `.i_rstn` repeats or closely reuses comment from instance mapping `.i_rstn`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:512`
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

<a id="vg-finding-549"></a>
### VG066: Comment for instance mapping `.i_word_addr` repeats or closely reuses comment from instance mapping `.i_word_addr`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:513`
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

<a id="vg-finding-550"></a>
### VG066: Comment for instance mapping `.C_LANE_ALPHA_FILE` repeats or closely reuses comment from instance mapping `.C_LANE_ALPHA_FILE`; write entity-specific RTL intent.
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

<a id="vg-finding-551"></a>
### VG066: Comment for instance mapping `.C_LANE_BETA_FILE` repeats or closely reuses comment from instance mapping `.C_LANE_BETA_FILE`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:519`
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

<a id="vg-finding-552"></a>
### VG066: Comment for instance mapping `.C_LANE_GAMMA_FILE` repeats or closely reuses comment from instance mapping `.C_LANE_GAMMA_FILE`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:520`
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

<a id="vg-finding-553"></a>
### VG066: Comment for instance mapping `.i_clk` repeats or closely reuses comment from instance mapping `.i_clk`; write entity-specific RTL intent.
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

<a id="vg-finding-554"></a>
### VG066: Comment for instance mapping `.i_rstn` repeats or closely reuses comment from instance mapping `.i_rstn`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:524`
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

<a id="vg-finding-555"></a>
### VG066: Comment for instance mapping `.i_word_addr` repeats or closely reuses comment from instance mapping `.i_word_addr`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:525`
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

<a id="vg-finding-556"></a>
### VG066: Comment for instance mapping `.C_LANE_ALPHA_FILE` repeats or closely reuses comment from instance mapping `.C_LANE_ALPHA_FILE`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:530`
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

<a id="vg-finding-557"></a>
### VG066: Comment for instance mapping `.C_LANE_BETA_FILE` repeats or closely reuses comment from instance mapping `.C_LANE_BETA_FILE`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:531`
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

<a id="vg-finding-558"></a>
### VG066: Comment for instance mapping `.C_LANE_GAMMA_FILE` repeats or closely reuses comment from instance mapping `.C_LANE_GAMMA_FILE`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:532`
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

<a id="vg-finding-559"></a>
### VG066: Comment for instance mapping `.i_clk` repeats or closely reuses comment from instance mapping `.i_clk`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:535`
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

<a id="vg-finding-560"></a>
### VG066: Comment for instance mapping `.i_rstn` repeats or closely reuses comment from instance mapping `.i_rstn`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:536`
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

<a id="vg-finding-561"></a>
### VG066: Comment for instance mapping `.i_word_addr` repeats or closely reuses comment from instance mapping `.i_word_addr`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:537`
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

<a id="vg-finding-562"></a>
### VG066: Comment for instance mapping `.i_rstn` repeats or closely reuses comment from instance mapping `.i_clk`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:380`
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

<a id="vg-finding-563"></a>
### VG066: Comment for instance mapping `.i_word_addr` repeats or closely reuses comment from instance mapping `.i_clk`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:381`
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

<a id="vg-finding-564"></a>
### VG066: Comment for instance mapping `.o_word_data` repeats or closely reuses comment from instance mapping `.i_clk`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:382`
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

<a id="vg-finding-565"></a>
### VG066: Comment for instance mapping `.C_LANE_BETA_FILE` repeats or closely reuses comment from instance mapping `.C_LANE_ALPHA_FILE`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:387`
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

<a id="vg-finding-566"></a>
### VG066: Comment for instance mapping `.C_LANE_GAMMA_FILE` repeats or closely reuses comment from instance mapping `.C_LANE_ALPHA_FILE`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:388`
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

<a id="vg-finding-567"></a>
### VG066: Comment for instance mapping `.o_word_data` repeats or closely reuses comment from instance mapping `.i_clk`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:394`
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

<a id="vg-finding-568"></a>
### VG066: Comment for instance mapping `.o_word_data` repeats or closely reuses comment from instance mapping `.i_clk`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:406`
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

<a id="vg-finding-569"></a>
### VG066: Comment for instance mapping `.o_word_data` repeats or closely reuses comment from instance mapping `.i_clk`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:418`
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

<a id="vg-finding-570"></a>
### VG066: Comment for instance mapping `.o_word_data` repeats or closely reuses comment from instance mapping `.i_clk`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:430`
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

<a id="vg-finding-571"></a>
### VG066: Comment for instance mapping `.o_word_data` repeats or closely reuses comment from instance mapping `.i_clk`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:442`
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

<a id="vg-finding-572"></a>
### VG066: Comment for instance mapping `.o_word_data` repeats or closely reuses comment from instance mapping `.i_clk`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:454`
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

<a id="vg-finding-573"></a>
### VG066: Comment for instance mapping `.o_word_data` repeats or closely reuses comment from instance mapping `.i_clk`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:466`
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

<a id="vg-finding-574"></a>
### VG066: Comment for instance mapping `.o_word_data` repeats or closely reuses comment from instance mapping `.i_clk`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:478`
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

<a id="vg-finding-575"></a>
### VG066: Comment for instance mapping `.o_word_data` repeats or closely reuses comment from instance mapping `.i_clk`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:490`
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

<a id="vg-finding-576"></a>
### VG066: Comment for instance mapping `.o_word_data` repeats or closely reuses comment from instance mapping `.i_clk`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:502`
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

<a id="vg-finding-577"></a>
### VG066: Comment for instance mapping `.o_word_data` repeats or closely reuses comment from instance mapping `.i_clk`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:514`
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

<a id="vg-finding-578"></a>
### VG066: Comment for instance mapping `.o_word_data` repeats or closely reuses comment from instance mapping `.i_clk`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:526`
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

<a id="vg-finding-579"></a>
### VG066: Comment for instance mapping `.o_word_data` repeats or closely reuses comment from instance mapping `.i_clk`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_yolo_numeric_rom_probe.v:538`
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

<a id="vg-finding-580"></a>
### VG097: 缺少外部模块接口定义，无法静态比较端口位宽。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:144`
- Evidence:
- node_kind: `verilog_rtl`
- detail: PH1P_LOGIC_ERAM u_lane_alpha
- source_excerpt: `PH1P_LOGIC_ERAM u_lane_alpha`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
PH1P_LOGIC_ERAM u_lane_alpha
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-581"></a>
### VG097: 缺少外部模块接口定义，无法静态比较端口位宽。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:200`
- Evidence:
- node_kind: `verilog_rtl`
- detail: PH1P_LOGIC_ERAM u_lane_beta
- source_excerpt: `PH1P_LOGIC_ERAM u_lane_beta`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
PH1P_LOGIC_ERAM u_lane_beta
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-582"></a>
### VG097: 缺少外部模块接口定义，无法静态比较端口位宽。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:256`
- Evidence:
- node_kind: `verilog_rtl`
- detail: PH1P_LOGIC_ERAM u_lane_gamma
- source_excerpt: `PH1P_LOGIC_ERAM u_lane_gamma`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
PH1P_LOGIC_ERAM u_lane_gamma
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-583"></a>
### VG097: 缺少外部模块接口定义，无法静态比较端口位宽。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:312`
- Evidence:
- node_kind: `verilog_rtl`
- detail: PH1P_LOGIC_ERAM u_lane_delta
- source_excerpt: `PH1P_LOGIC_ERAM u_lane_delta`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
PH1P_LOGIC_ERAM u_lane_delta
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-584"></a>
### VG097: 实例参数区、端口区或参数覆盖无法静态解析。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_probe.v:378`
- Evidence:
- node_kind: `verilog_rtl`
- detail: road_yolo_numeric_rom_group u_group_alpha
- source_excerpt: `road_yolo_numeric_rom_group u_group_alpha`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
road_yolo_numeric_rom_group u_group_alpha
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-585"></a>
### VG097: 实例参数区、端口区或参数覆盖无法静态解析。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_probe.v:390`
- Evidence:
- node_kind: `verilog_rtl`
- detail: road_yolo_numeric_rom_group u_group_beta
- source_excerpt: `road_yolo_numeric_rom_group u_group_beta`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
road_yolo_numeric_rom_group u_group_beta
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-586"></a>
### VG097: 实例参数区、端口区或参数覆盖无法静态解析。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_probe.v:402`
- Evidence:
- node_kind: `verilog_rtl`
- detail: road_yolo_numeric_rom_group u_group_gamma
- source_excerpt: `road_yolo_numeric_rom_group u_group_gamma`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
road_yolo_numeric_rom_group u_group_gamma
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-587"></a>
### VG097: 实例参数区、端口区或参数覆盖无法静态解析。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_probe.v:414`
- Evidence:
- node_kind: `verilog_rtl`
- detail: road_yolo_numeric_rom_group u_group_delta
- source_excerpt: `road_yolo_numeric_rom_group u_group_delta`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
road_yolo_numeric_rom_group u_group_delta
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-588"></a>
### VG097: 实例参数区、端口区或参数覆盖无法静态解析。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_probe.v:426`
- Evidence:
- node_kind: `verilog_rtl`
- detail: road_yolo_numeric_rom_group u_group_epsilon
- source_excerpt: `road_yolo_numeric_rom_group u_group_epsilon`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
road_yolo_numeric_rom_group u_group_epsilon
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-589"></a>
### VG097: 实例参数区、端口区或参数覆盖无法静态解析。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_probe.v:438`
- Evidence:
- node_kind: `verilog_rtl`
- detail: road_yolo_numeric_rom_group u_group_zeta
- source_excerpt: `road_yolo_numeric_rom_group u_group_zeta`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
road_yolo_numeric_rom_group u_group_zeta
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-590"></a>
### VG097: 实例参数区、端口区或参数覆盖无法静态解析。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_probe.v:450`
- Evidence:
- node_kind: `verilog_rtl`
- detail: road_yolo_numeric_rom_group u_group_eta
- source_excerpt: `road_yolo_numeric_rom_group u_group_eta`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
road_yolo_numeric_rom_group u_group_eta
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-591"></a>
### VG097: 实例参数区、端口区或参数覆盖无法静态解析。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_probe.v:462`
- Evidence:
- node_kind: `verilog_rtl`
- detail: road_yolo_numeric_rom_group u_group_theta
- source_excerpt: `road_yolo_numeric_rom_group u_group_theta`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
road_yolo_numeric_rom_group u_group_theta
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-592"></a>
### VG097: 实例参数区、端口区或参数覆盖无法静态解析。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_probe.v:474`
- Evidence:
- node_kind: `verilog_rtl`
- detail: road_yolo_numeric_rom_group u_group_iota
- source_excerpt: `road_yolo_numeric_rom_group u_group_iota`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
road_yolo_numeric_rom_group u_group_iota
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-593"></a>
### VG097: 实例参数区、端口区或参数覆盖无法静态解析。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_probe.v:486`
- Evidence:
- node_kind: `verilog_rtl`
- detail: road_yolo_numeric_rom_group u_group_kappa
- source_excerpt: `road_yolo_numeric_rom_group u_group_kappa`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
road_yolo_numeric_rom_group u_group_kappa
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-594"></a>
### VG097: 实例参数区、端口区或参数覆盖无法静态解析。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_probe.v:498`
- Evidence:
- node_kind: `verilog_rtl`
- detail: road_yolo_numeric_rom_group u_group_lambda
- source_excerpt: `road_yolo_numeric_rom_group u_group_lambda`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
road_yolo_numeric_rom_group u_group_lambda
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-595"></a>
### VG097: 实例参数区、端口区或参数覆盖无法静态解析。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_probe.v:510`
- Evidence:
- node_kind: `verilog_rtl`
- detail: road_yolo_numeric_rom_group u_group_mu
- source_excerpt: `road_yolo_numeric_rom_group u_group_mu`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
road_yolo_numeric_rom_group u_group_mu
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-596"></a>
### VG097: 实例参数区、端口区或参数覆盖无法静态解析。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_probe.v:522`
- Evidence:
- node_kind: `verilog_rtl`
- detail: road_yolo_numeric_rom_group u_group_nu
- source_excerpt: `road_yolo_numeric_rom_group u_group_nu`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
road_yolo_numeric_rom_group u_group_nu
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-597"></a>
### VG097: 实例参数区、端口区或参数覆盖无法静态解析。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_probe.v:534`
- Evidence:
- node_kind: `verilog_rtl`
- detail: road_yolo_numeric_rom_group u_group_xi
- source_excerpt: `road_yolo_numeric_rom_group u_group_xi`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
road_yolo_numeric_rom_group u_group_xi
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-598"></a>
### VG109: 组合逻辑 if 链缺少终止 else。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_yolo_numeric_rom_probe.v:183`
- Evidence:
- node_kind: `verilog_rtl`
- detail: if(final_bit == 1'b1)
- source_excerpt: `if(final_bit == 1'b1)`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
if(final_bit == 1'b1)
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
- Location: `road_yolo_numeric_rom_probe.v:213`
- Evidence:
- node_kind: `verilog_rtl`
- detail: group_index_o <= group_index_o + 1'b1;
- source_excerpt: `group_index_o <= group_index_o + 1'b1;`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
group_index_o <= group_index_o + 1'b1;
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
- Location: `road_yolo_numeric_rom_probe.v:224`
- Evidence:
- node_kind: `verilog_rtl`
- detail: word_addr_o <= word_addr_o + 1'b1;
- source_excerpt: `word_addr_o <= word_addr_o + 1'b1;`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
word_addr_o <= word_addr_o + 1'b1;
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
- Location: `road_yolo_numeric_rom_probe.v:238`
- Evidence:
- node_kind: `verilog_rtl`
- detail: bit_index_o <= bit_index_o + 1'b1;
- source_excerpt: `bit_index_o <= bit_index_o + 1'b1;`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
bit_index_o <= bit_index_o + 1'b1;
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-602"></a>
### VG125: 字面量声明为 160 位，但实际值只需要 1 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:88`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 160'b0
- source_excerpt: `160'b0`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
160'b0
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-603"></a>
### VG125: 字面量声明为 80 位，但实际值只需要 1 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:98`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 80'b0
- source_excerpt: `80'b0`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
80'b0
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-604"></a>
### VG125: 字面量声明为 80 位，但实际值只需要 1 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:106`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 80'b0
- source_excerpt: `80'b0`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
80'b0
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-605"></a>
### VG125: 字面量声明为 40 位，但实际值只需要 1 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:145`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 40'b0
- source_excerpt: `40'b0`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
40'b0
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-606"></a>
### VG125: 字面量声明为 40 位，但实际值只需要 1 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:153`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 40'b0
- source_excerpt: `40'b0`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
40'b0
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-607"></a>
### VG125: 字面量声明为 9 位，但实际值只需要 1 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:154`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 9'b0
- source_excerpt: `9'b0`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
9'b0
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-608"></a>
### VG125: 字面量声明为 40 位，但实际值只需要 1 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:201`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 40'b0
- source_excerpt: `40'b0`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
40'b0
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-609"></a>
### VG125: 字面量声明为 40 位，但实际值只需要 1 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:209`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 40'b0
- source_excerpt: `40'b0`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
40'b0
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-610"></a>
### VG125: 字面量声明为 9 位，但实际值只需要 1 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:210`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 9'b0
- source_excerpt: `9'b0`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
9'b0
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-611"></a>
### VG125: 字面量声明为 40 位，但实际值只需要 1 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:257`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 40'b0
- source_excerpt: `40'b0`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
40'b0
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-612"></a>
### VG125: 字面量声明为 40 位，但实际值只需要 1 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:265`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 40'b0
- source_excerpt: `40'b0`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
40'b0
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-613"></a>
### VG125: 字面量声明为 9 位，但实际值只需要 1 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:266`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 9'b0
- source_excerpt: `9'b0`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
9'b0
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-614"></a>
### VG125: 字面量声明为 40 位，但实际值只需要 1 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:313`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 40'b0
- source_excerpt: `40'b0`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
40'b0
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-615"></a>
### VG125: 字面量声明为 40 位，但实际值只需要 1 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:321`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 40'b0
- source_excerpt: `40'b0`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
40'b0
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-616"></a>
### VG125: 字面量声明为 9 位，但实际值只需要 1 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:322`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 9'b0
- source_excerpt: `9'b0`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
9'b0
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-617"></a>
### VG125: 字面量声明为 32 位，但实际值只需要 1 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_probe.v:140`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 32'b0
- source_excerpt: `32'b0`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
32'b0
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-618"></a>
### VG125: 字面量声明为 160 位，但实际值只需要 1 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_probe.v:245`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 160'b0
- source_excerpt: `160'b0`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
160'b0
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-619"></a>
### VG125: 字面量声明为 160 位，但实际值只需要 1 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_probe.v:262`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 160'b0
- source_excerpt: `160'b0`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
160'b0
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-620"></a>
### VG125: 字面量声明为 160 位，但实际值只需要 1 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_probe.v:270`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 160'b0
- source_excerpt: `160'b0`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
160'b0
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-621"></a>
### VG125: 字面量声明为 160 位，但实际值只需要 1 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_probe.v:278`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 160'b0
- source_excerpt: `160'b0`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
160'b0
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-622"></a>
### VG125: 字面量声明为 160 位，但实际值只需要 1 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_probe.v:286`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 160'b0
- source_excerpt: `160'b0`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
160'b0
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-623"></a>
### VG125: 字面量声明为 160 位，但实际值只需要 1 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_probe.v:294`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 160'b0
- source_excerpt: `160'b0`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
160'b0
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-624"></a>
### VG125: 字面量声明为 160 位，但实际值只需要 1 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_probe.v:302`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 160'b0
- source_excerpt: `160'b0`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
160'b0
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-625"></a>
### VG125: 字面量声明为 160 位，但实际值只需要 1 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_probe.v:310`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 160'b0
- source_excerpt: `160'b0`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
160'b0
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-626"></a>
### VG125: 字面量声明为 160 位，但实际值只需要 1 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_probe.v:318`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 160'b0
- source_excerpt: `160'b0`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
160'b0
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-627"></a>
### VG125: 字面量声明为 160 位，但实际值只需要 1 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_probe.v:326`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 160'b0
- source_excerpt: `160'b0`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
160'b0
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-628"></a>
### VG125: 字面量声明为 160 位，但实际值只需要 1 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_probe.v:334`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 160'b0
- source_excerpt: `160'b0`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
160'b0
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-629"></a>
### VG125: 字面量声明为 160 位，但实际值只需要 1 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_probe.v:342`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 160'b0
- source_excerpt: `160'b0`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
160'b0
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-630"></a>
### VG125: 字面量声明为 160 位，但实际值只需要 1 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_probe.v:350`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 160'b0
- source_excerpt: `160'b0`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
160'b0
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-631"></a>
### VG125: 字面量声明为 160 位，但实际值只需要 1 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_probe.v:358`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 160'b0
- source_excerpt: `160'b0`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
160'b0
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-632"></a>
### VG125: 字面量声明为 160 位，但实际值只需要 1 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_probe.v:366`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 160'b0
- source_excerpt: `160'b0`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
160'b0
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-633"></a>
### VG132: 时钟信号连接到了非时钟实例端口。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:149`
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

<a id="vg-finding-634"></a>
### VG132: 时钟信号连接到了非时钟实例端口。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:157`
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

<a id="vg-finding-635"></a>
### VG132: 时钟信号连接到了非时钟实例端口。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:205`
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

<a id="vg-finding-636"></a>
### VG132: 时钟信号连接到了非时钟实例端口。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:213`
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

<a id="vg-finding-637"></a>
### VG132: 时钟信号连接到了非时钟实例端口。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:261`
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

<a id="vg-finding-638"></a>
### VG132: 时钟信号连接到了非时钟实例端口。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:269`
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

<a id="vg-finding-639"></a>
### VG132: 时钟信号连接到了非时钟实例端口。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:317`
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

<a id="vg-finding-640"></a>
### VG132: 时钟信号连接到了非时钟实例端口。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:325`
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

<a id="vg-finding-641"></a>
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

<a id="vg-finding-642"></a>
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

<a id="vg-finding-643"></a>
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

<a id="vg-finding-644"></a>
### VG138: 常量未显式声明位宽和进制。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_yolo_numeric_rom_group.v:78`
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

<a id="vg-finding-645"></a>
### VG138: 常量未显式声明位宽和进制。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_yolo_numeric_rom_probe.v:91`
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

<a id="vg-finding-646"></a>
### VG138: 常量未显式声明位宽和进制。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_yolo_numeric_rom_probe.v:92`
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

<a id="vg-finding-647"></a>
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

<a id="vg-finding-648"></a>
### VG138: 常量未显式声明位宽和进制。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_yolo_numeric_rom_probe.v:103`
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

<a id="vg-finding-649"></a>
### VG138: 常量未显式声明位宽和进制。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_yolo_numeric_rom_probe.v:104`
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

<a id="vg-finding-651"></a>
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

<a id="vg-finding-652"></a>
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

<a id="vg-finding-653"></a>
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

<a id="vg-finding-654"></a>
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

<a id="vg-finding-655"></a>
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

<a id="vg-finding-656"></a>
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

<a id="vg-finding-657"></a>
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

<a id="vg-finding-658"></a>
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

<a id="vg-finding-659"></a>
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

<a id="vg-finding-660"></a>
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

<a id="vg-finding-661"></a>
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

<a id="vg-finding-662"></a>
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

<a id="vg-finding-663"></a>
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

<a id="vg-finding-664"></a>
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

<a id="vg-finding-665"></a>
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

<a id="vg-finding-666"></a>
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

<a id="vg-finding-667"></a>
### VG138: 常量未显式声明位宽和进制。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_yolo_numeric_rom_probe.v:122`
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

<a id="vg-finding-668"></a>
### VG145: 组合逻辑完整依赖锥最多允许三个源信号，超限逻辑必须由时序 reg 隔断。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_probe.v:128`
- Evidence:
- node_kind: `verilog_rtl`
- detail: crc_updated: 4 sources: bit_index_o, crc_o[0], crc_o[31:1], word_buffer_o[bit_index_o]
- source_excerpt: `crc_updated: 4 sources: bit_index_o, crc_o[0], crc_o[31:1], word_buffer_o[bit_index_o]`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
crc_updated: 4 sources: bit_index_o, crc_o[0], crc_o[31:1], word_buffer_o[bit_index_o]
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
- Location: `road_yolo_numeric_rom_probe.v:155`
- Evidence:
- node_kind: `verilog_rtl`
- detail: state_next: 4 sources: bit_index_o, group_index_o, state_current, word_addr_o
- source_excerpt: `state_next: 4 sources: bit_index_o, group_index_o, state_current, word_addr_o`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
state_next: 4 sources: bit_index_o, group_index_o, state_current, word_addr_o
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-670"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_group.v:road_yolo_numeric_rom_group@49:1-337:1; instance_path=road_yolo_numeric_rom_group; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_group.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_group.v:road_yolo_numeric_rom_group@49:1-337:1; instance_path=road_yolo_numeric_rom_group; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_group.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_group.v:road_yolo_numeric_rom_group@49:1-337:1; instance_path=road_yolo_numeric_rom_group; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_group.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-671"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_group.v:road_yolo_numeric_rom_group@49:1-337:1; instance_path=road_yolo_numeric_rom_group; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_group.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_group.v:road_yolo_numeric_rom_group@49:1-337:1; instance_path=road_yolo_numeric_rom_group; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_group.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_group.v:road_yolo_numeric_rom_group@49:1-337:1; instance_path=road_yolo_numeric_rom_group; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_group.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-672"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_group.v:road_yolo_numeric_rom_group@49:1-337:1; instance_path=road_yolo_numeric_rom_group; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_group.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_group.v:road_yolo_numeric_rom_group@49:1-337:1; instance_path=road_yolo_numeric_rom_group; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_group.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_group.v:road_yolo_numeric_rom_group@49:1-337:1; instance_path=road_yolo_numeric_rom_group; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_group.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-673"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_group.v:road_yolo_numeric_rom_group@49:1-337:1; instance_path=road_yolo_numeric_rom_group; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_group.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_group.v:road_yolo_numeric_rom_group@49:1-337:1; instance_path=road_yolo_numeric_rom_group; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_group.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_group.v:road_yolo_numeric_rom_group@49:1-337:1; instance_path=road_yolo_numeric_rom_group; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_group.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-674"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_group.v:road_yolo_numeric_rom_group@49:1-337:1; instance_path=road_yolo_numeric_rom_group; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lower_pair_o$D; child_output=road_yolo_numeric_rom_group.lower_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_group.v:road_yolo_numeric_rom_group@49:1-337:1; instance_path=road_yolo_numeric_rom_group; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lower_pair_o$D; child_output=road_yolo_numeric_rom_group.lower_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_group.v:road_yolo_numeric_rom_group@49:1-337:1; instance_path=road_yolo_numeric_rom_group; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lower_pair_o$D; child_output=road_yolo_numeric_rom_group.lower_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-675"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_group.v:road_yolo_numeric_rom_group@49:1-337:1; instance_path=road_yolo_numeric_rom_group; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=upper_pair_o$D; child_output=road_yolo_numeric_rom_group.upper_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_group.v:road_yolo_numeric_rom_group@49:1-337:1; instance_path=road_yolo_numeric_rom_group; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=upper_pair_o$D; child_output=road_yolo_numeric_rom_group.upper_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_group.v:road_yolo_numeric_rom_group@49:1-337:1; instance_path=road_yolo_numeric_rom_group; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=upper_pair_o$D; child_output=road_yolo_numeric_rom_group.upper_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-676"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_alpha; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/u_group_alpha.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_alpha; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/u_group_alpha.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_alpha; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/u_group_alpha.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-677"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_alpha; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/u_group_alpha.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_alpha; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/u_group_alpha.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_alpha; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/u_group_alpha.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-678"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_alpha; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/u_group_alpha.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_alpha; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/u_group_alpha.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_alpha; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/u_group_alpha.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-679"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_alpha; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/u_group_alpha.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_alpha; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/u_group_alpha.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_alpha; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/u_group_alpha.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-680"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_alpha; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lower_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_alpha.lower_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_alpha; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lower_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_alpha.lower_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_alpha; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lower_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_alpha.lower_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-681"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_alpha; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=upper_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_alpha.upper_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_alpha; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=upper_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_alpha.upper_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_alpha; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=upper_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_alpha.upper_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-682"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_beta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/u_group_beta.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_beta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/u_group_beta.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_beta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/u_group_beta.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-683"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_beta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/u_group_beta.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_beta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/u_group_beta.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_beta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/u_group_beta.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-684"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_beta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/u_group_beta.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_beta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/u_group_beta.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_beta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/u_group_beta.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-685"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_beta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/u_group_beta.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_beta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/u_group_beta.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_beta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/u_group_beta.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-686"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_beta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lower_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_beta.lower_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_beta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lower_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_beta.lower_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_beta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lower_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_beta.lower_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-687"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_beta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=upper_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_beta.upper_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_beta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=upper_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_beta.upper_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_beta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=upper_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_beta.upper_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-688"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_delta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/u_group_delta.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_delta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/u_group_delta.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_delta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/u_group_delta.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-689"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_delta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/u_group_delta.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_delta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/u_group_delta.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_delta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/u_group_delta.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-690"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_delta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/u_group_delta.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_delta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/u_group_delta.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_delta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/u_group_delta.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-691"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_delta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/u_group_delta.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_delta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/u_group_delta.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_delta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/u_group_delta.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-692"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_delta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lower_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_delta.lower_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_delta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lower_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_delta.lower_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_delta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lower_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_delta.lower_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-693"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_delta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=upper_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_delta.upper_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_delta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=upper_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_delta.upper_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_delta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=upper_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_delta.upper_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-694"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_epsilon; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/u_group_epsilon.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_epsilon; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/u_group_epsilon.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_epsilon; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/u_group_epsilon.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-695"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_epsilon; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/u_group_epsilon.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_epsilon; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/u_group_epsilon.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_epsilon; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/u_group_epsilon.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-696"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_epsilon; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/u_group_epsilon.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_epsilon; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/u_group_epsilon.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_epsilon; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/u_group_epsilon.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-697"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_epsilon; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/u_group_epsilon.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_epsilon; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/u_group_epsilon.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_epsilon; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/u_group_epsilon.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-698"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_epsilon; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lower_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_epsilon.lower_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_epsilon; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lower_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_epsilon.lower_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_epsilon; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lower_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_epsilon.lower_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-699"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_epsilon; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=upper_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_epsilon.upper_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_epsilon; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=upper_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_epsilon.upper_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_epsilon; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=upper_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_epsilon.upper_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-700"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_eta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/u_group_eta.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_eta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/u_group_eta.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_eta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/u_group_eta.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-701"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_eta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/u_group_eta.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_eta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/u_group_eta.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_eta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/u_group_eta.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-702"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_eta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/u_group_eta.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_eta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/u_group_eta.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_eta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/u_group_eta.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-703"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_eta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/u_group_eta.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_eta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/u_group_eta.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_eta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/u_group_eta.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-704"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_eta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lower_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_eta.lower_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_eta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lower_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_eta.lower_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_eta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lower_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_eta.lower_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-705"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_eta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=upper_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_eta.upper_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_eta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=upper_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_eta.upper_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_eta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=upper_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_eta.upper_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-706"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_gamma; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/u_group_gamma.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_gamma; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/u_group_gamma.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_gamma; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/u_group_gamma.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-707"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_gamma; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/u_group_gamma.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_gamma; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/u_group_gamma.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_gamma; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/u_group_gamma.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-708"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_gamma; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/u_group_gamma.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_gamma; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/u_group_gamma.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_gamma; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/u_group_gamma.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-709"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_gamma; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/u_group_gamma.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_gamma; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/u_group_gamma.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_gamma; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/u_group_gamma.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-710"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_gamma; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lower_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_gamma.lower_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_gamma; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lower_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_gamma.lower_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_gamma; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lower_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_gamma.lower_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-711"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_gamma; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=upper_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_gamma.upper_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_gamma; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=upper_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_gamma.upper_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_gamma; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=upper_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_gamma.upper_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-712"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_iota; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/u_group_iota.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_iota; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/u_group_iota.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_iota; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/u_group_iota.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-713"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_iota; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/u_group_iota.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_iota; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/u_group_iota.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_iota; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/u_group_iota.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-714"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_iota; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/u_group_iota.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_iota; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/u_group_iota.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_iota; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/u_group_iota.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-715"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_iota; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/u_group_iota.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_iota; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/u_group_iota.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_iota; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/u_group_iota.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-716"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_iota; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lower_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_iota.lower_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_iota; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lower_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_iota.lower_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_iota; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lower_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_iota.lower_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-717"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_iota; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=upper_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_iota.upper_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_iota; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=upper_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_iota.upper_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_iota; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=upper_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_iota.upper_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-718"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_kappa; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/u_group_kappa.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_kappa; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/u_group_kappa.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_kappa; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/u_group_kappa.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-719"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_kappa; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/u_group_kappa.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_kappa; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/u_group_kappa.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_kappa; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/u_group_kappa.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-720"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_kappa; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/u_group_kappa.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_kappa; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/u_group_kappa.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_kappa; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/u_group_kappa.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-721"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_kappa; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/u_group_kappa.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_kappa; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/u_group_kappa.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_kappa; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/u_group_kappa.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-722"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_kappa; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lower_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_kappa.lower_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_kappa; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lower_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_kappa.lower_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_kappa; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lower_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_kappa.lower_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-723"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_kappa; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=upper_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_kappa.upper_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_kappa; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=upper_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_kappa.upper_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_kappa; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=upper_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_kappa.upper_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-724"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_lambda; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/u_group_lambda.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_lambda; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/u_group_lambda.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_lambda; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/u_group_lambda.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-725"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_lambda; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/u_group_lambda.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_lambda; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/u_group_lambda.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_lambda; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/u_group_lambda.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-726"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_lambda; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/u_group_lambda.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_lambda; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/u_group_lambda.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_lambda; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/u_group_lambda.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-727"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_lambda; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/u_group_lambda.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_lambda; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/u_group_lambda.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_lambda; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/u_group_lambda.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-728"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_lambda; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lower_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_lambda.lower_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_lambda; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lower_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_lambda.lower_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_lambda; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lower_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_lambda.lower_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-729"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_lambda; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=upper_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_lambda.upper_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_lambda; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=upper_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_lambda.upper_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_lambda; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=upper_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_lambda.upper_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-730"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_mu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/u_group_mu.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_mu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/u_group_mu.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_mu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/u_group_mu.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-731"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_mu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/u_group_mu.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_mu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/u_group_mu.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_mu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/u_group_mu.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-732"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_mu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/u_group_mu.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_mu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/u_group_mu.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_mu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/u_group_mu.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-733"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_mu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/u_group_mu.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_mu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/u_group_mu.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_mu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/u_group_mu.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-734"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_mu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lower_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_mu.lower_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_mu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lower_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_mu.lower_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_mu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lower_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_mu.lower_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-735"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_mu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=upper_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_mu.upper_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_mu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=upper_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_mu.upper_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_mu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=upper_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_mu.upper_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-736"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_nu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/u_group_nu.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_nu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/u_group_nu.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_nu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/u_group_nu.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-737"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_nu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/u_group_nu.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_nu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/u_group_nu.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_nu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/u_group_nu.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-738"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_nu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/u_group_nu.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_nu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/u_group_nu.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_nu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/u_group_nu.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-739"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_nu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/u_group_nu.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_nu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/u_group_nu.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_nu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/u_group_nu.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-740"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_nu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lower_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_nu.lower_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_nu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lower_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_nu.lower_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_nu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lower_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_nu.lower_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-741"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_nu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=upper_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_nu.upper_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_nu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=upper_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_nu.upper_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_nu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=upper_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_nu.upper_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-742"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_theta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/u_group_theta.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_theta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/u_group_theta.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_theta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/u_group_theta.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-743"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_theta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/u_group_theta.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_theta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/u_group_theta.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_theta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/u_group_theta.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-744"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_theta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/u_group_theta.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_theta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/u_group_theta.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_theta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/u_group_theta.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-745"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_theta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/u_group_theta.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_theta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/u_group_theta.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_theta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/u_group_theta.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-746"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_theta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lower_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_theta.lower_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_theta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lower_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_theta.lower_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_theta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lower_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_theta.lower_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-747"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_theta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=upper_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_theta.upper_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_theta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=upper_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_theta.upper_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_theta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=upper_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_theta.upper_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-748"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_xi; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/u_group_xi.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_xi; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/u_group_xi.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_xi; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/u_group_xi.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-749"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_xi; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/u_group_xi.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_xi; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/u_group_xi.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_xi; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/u_group_xi.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-750"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_xi; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/u_group_xi.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_xi; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/u_group_xi.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_xi; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/u_group_xi.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-751"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_xi; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/u_group_xi.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_xi; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/u_group_xi.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_xi; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/u_group_xi.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-752"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_xi; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lower_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_xi.lower_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_xi; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lower_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_xi.lower_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_xi; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lower_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_xi.lower_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-753"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_xi; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=upper_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_xi.upper_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_xi; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=upper_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_xi.upper_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_xi; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=upper_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_xi.upper_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-754"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_zeta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/u_group_zeta.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_zeta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/u_group_zeta.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_zeta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/u_group_zeta.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-755"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_zeta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/u_group_zeta.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_zeta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/u_group_zeta.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_zeta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/u_group_zeta.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-756"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_zeta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/u_group_zeta.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_zeta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/u_group_zeta.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_zeta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/u_group_zeta.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-757"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_zeta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/u_group_zeta.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_zeta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/u_group_zeta.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_zeta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/u_group_zeta.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-758"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_zeta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lower_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_zeta.lower_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_zeta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lower_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_zeta.lower_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_zeta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lower_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_zeta.lower_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-759"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_zeta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=upper_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_zeta.upper_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_zeta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=upper_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_zeta.upper_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_zeta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=upper_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_zeta.upper_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-760"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe; specialization=bef1493c564833e173f6110d0a7e0cc1da79ebe54c3cdd5be8b1b48c94d0b282; target=bit_index_o$enable; child_output=road_yolo_numeric_rom_probe.bit_index_o$enable; operation_count=4; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe; specialization=bef1493c564833e173f6110d0a7e0cc1da79ebe54c3cdd5be8b1b48c94d0b282; target=bit_index_o$enable; child_output=road_yolo_numeric_rom_probe.bit_index_o$enable; operation_count=4; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe; specialization=bef1493c564833e173f6110d0a7e0cc1da79ebe54c3cdd5be8b1b48c94d0b282; target=bit_index_o$enable; child_output=road_yolo_numeric_rom_probe.bit_index_o$enable; operation_count=4; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-761"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe; specialization=bef1493c564833e173f6110d0a7e0cc1da79ebe54c3cdd5be8b1b48c94d0b282; target=checksum_o$D; child_output=road_yolo_numeric_rom_probe.checksum_o$D; operation_count=5; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe; specialization=bef1493c564833e173f6110d0a7e0cc1da79ebe54c3cdd5be8b1b48c94d0b282; target=checksum_o$D; child_output=road_yolo_numeric_rom_probe.checksum_o$D; operation_count=5; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe; specialization=bef1493c564833e173f6110d0a7e0cc1da79ebe54c3cdd5be8b1b48c94d0b282; target=checksum_o$D; child_output=road_yolo_numeric_rom_probe.checksum_o$D; operation_count=5; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-762"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe; specialization=bef1493c564833e173f6110d0a7e0cc1da79ebe54c3cdd5be8b1b48c94d0b282; target=checksum_o$enable; child_output=road_yolo_numeric_rom_probe.checksum_o$enable; operation_count=8; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe; specialization=bef1493c564833e173f6110d0a7e0cc1da79ebe54c3cdd5be8b1b48c94d0b282; target=checksum_o$enable; child_output=road_yolo_numeric_rom_probe.checksum_o$enable; operation_count=8; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe; specialization=bef1493c564833e173f6110d0a7e0cc1da79ebe54c3cdd5be8b1b48c94d0b282; target=checksum_o$enable; child_output=road_yolo_numeric_rom_probe.checksum_o$enable; operation_count=8; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-763"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe; specialization=bef1493c564833e173f6110d0a7e0cc1da79ebe54c3cdd5be8b1b48c94d0b282; target=crc_o$D; child_output=road_yolo_numeric_rom_probe.crc_o$D; operation_count=4; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe; specialization=bef1493c564833e173f6110d0a7e0cc1da79ebe54c3cdd5be8b1b48c94d0b282; target=crc_o$D; child_output=road_yolo_numeric_rom_probe.crc_o$D; operation_count=4; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe; specialization=bef1493c564833e173f6110d0a7e0cc1da79ebe54c3cdd5be8b1b48c94d0b282; target=crc_o$D; child_output=road_yolo_numeric_rom_probe.crc_o$D; operation_count=4; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-764"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe; specialization=bef1493c564833e173f6110d0a7e0cc1da79ebe54c3cdd5be8b1b48c94d0b282; target=done_o$enable; child_output=road_yolo_numeric_rom_probe.done_o$enable; operation_count=8; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe; specialization=bef1493c564833e173f6110d0a7e0cc1da79ebe54c3cdd5be8b1b48c94d0b282; target=done_o$enable; child_output=road_yolo_numeric_rom_probe.done_o$enable; operation_count=8; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe; specialization=bef1493c564833e173f6110d0a7e0cc1da79ebe54c3cdd5be8b1b48c94d0b282; target=done_o$enable; child_output=road_yolo_numeric_rom_probe.done_o$enable; operation_count=8; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-765"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe; specialization=bef1493c564833e173f6110d0a7e0cc1da79ebe54c3cdd5be8b1b48c94d0b282; target=group_index_o$enable; child_output=road_yolo_numeric_rom_probe.group_index_o$enable; operation_count=8; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe; specialization=bef1493c564833e173f6110d0a7e0cc1da79ebe54c3cdd5be8b1b48c94d0b282; target=group_index_o$enable; child_output=road_yolo_numeric_rom_probe.group_index_o$enable; operation_count=8; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe; specialization=bef1493c564833e173f6110d0a7e0cc1da79ebe54c3cdd5be8b1b48c94d0b282; target=group_index_o$enable; child_output=road_yolo_numeric_rom_probe.group_index_o$enable; operation_count=8; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-766"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe; specialization=bef1493c564833e173f6110d0a7e0cc1da79ebe54c3cdd5be8b1b48c94d0b282; target=state_current$D; child_output=road_yolo_numeric_rom_probe.state_current$D; operation_count=5; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe; specialization=bef1493c564833e173f6110d0a7e0cc1da79ebe54c3cdd5be8b1b48c94d0b282; target=state_current$D; child_output=road_yolo_numeric_rom_probe.state_current$D; operation_count=5; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe; specialization=bef1493c564833e173f6110d0a7e0cc1da79ebe54c3cdd5be8b1b48c94d0b282; target=state_current$D; child_output=road_yolo_numeric_rom_probe.state_current$D; operation_count=5; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-767"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe; specialization=bef1493c564833e173f6110d0a7e0cc1da79ebe54c3cdd5be8b1b48c94d0b282; target=word_addr_o$enable; child_output=road_yolo_numeric_rom_probe.word_addr_o$enable; operation_count=5; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe; specialization=bef1493c564833e173f6110d0a7e0cc1da79ebe54c3cdd5be8b1b48c94d0b282; target=word_addr_o$enable; child_output=road_yolo_numeric_rom_probe.word_addr_o$enable; operation_count=5; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe; specialization=bef1493c564833e173f6110d0a7e0cc1da79ebe54c3cdd5be8b1b48c94d0b282; target=word_addr_o$enable; child_output=road_yolo_numeric_rom_probe.word_addr_o$enable; operation_count=5; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-768"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_probe.v:128`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe; specialization=bef1493c564833e173f6110d0a7e0cc1da79ebe54c3cdd5be8b1b48c94d0b282; target=crc_updated; child_output=road_yolo_numeric_rom_probe.crc_updated; operation_count=4; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe; specialization=bef1493c564833e173f6110d0a7e0cc1da79ebe54c3cdd5be8b1b48c94d0b282; target=crc_updated; child_output=road_yolo_numeric_rom_probe.crc_updated; operation_count=4; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe; specialization=bef1493c564833e173f6110d0a7e0cc1da79ebe54c3cdd5be8b1b48c94d0b282; target=crc_updated; child_output=road_yolo_numeric_rom_probe.crc_updated; operation_count=4; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-769"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_probe.v:155`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe; specialization=bef1493c564833e173f6110d0a7e0cc1da79ebe54c3cdd5be8b1b48c94d0b282; target=state_next; child_output=road_yolo_numeric_rom_probe.state_next; operation_count=5; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe; specialization=bef1493c564833e173f6110d0a7e0cc1da79ebe54c3cdd5be8b1b48c94d0b282; target=state_next; child_output=road_yolo_numeric_rom_probe.state_next; operation_count=5; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe; specialization=bef1493c564833e173f6110d0a7e0cc1da79ebe54c3cdd5be8b1b48c94d0b282; target=state_next; child_output=road_yolo_numeric_rom_probe.state_next; operation_count=5; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-770"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_group.v:road_yolo_numeric_rom_group@49:1-337:1; instance_path=road_yolo_numeric_rom_group; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_group.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_group.v:road_yolo_numeric_rom_group@49:1-337:1; instance_path=road_yolo_numeric_rom_group; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_group.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_group.v:road_yolo_numeric_rom_group@49:1-337:1; instance_path=road_yolo_numeric_rom_group; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_group.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-771"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_group.v:road_yolo_numeric_rom_group@49:1-337:1; instance_path=road_yolo_numeric_rom_group; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_group.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_group.v:road_yolo_numeric_rom_group@49:1-337:1; instance_path=road_yolo_numeric_rom_group; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_group.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_group.v:road_yolo_numeric_rom_group@49:1-337:1; instance_path=road_yolo_numeric_rom_group; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_group.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-772"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_group.v:road_yolo_numeric_rom_group@49:1-337:1; instance_path=road_yolo_numeric_rom_group; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_group.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_group.v:road_yolo_numeric_rom_group@49:1-337:1; instance_path=road_yolo_numeric_rom_group; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_group.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_group.v:road_yolo_numeric_rom_group@49:1-337:1; instance_path=road_yolo_numeric_rom_group; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_group.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-773"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_group.v:road_yolo_numeric_rom_group@49:1-337:1; instance_path=road_yolo_numeric_rom_group; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_group.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_group.v:road_yolo_numeric_rom_group@49:1-337:1; instance_path=road_yolo_numeric_rom_group; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_group.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_group.v:road_yolo_numeric_rom_group@49:1-337:1; instance_path=road_yolo_numeric_rom_group; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_group.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-774"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_group.v:road_yolo_numeric_rom_group@49:1-337:1; instance_path=road_yolo_numeric_rom_group; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lower_pair_o$D; child_output=road_yolo_numeric_rom_group.lower_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_group.v:road_yolo_numeric_rom_group@49:1-337:1; instance_path=road_yolo_numeric_rom_group; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lower_pair_o$D; child_output=road_yolo_numeric_rom_group.lower_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_group.v:road_yolo_numeric_rom_group@49:1-337:1; instance_path=road_yolo_numeric_rom_group; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lower_pair_o$D; child_output=road_yolo_numeric_rom_group.lower_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-775"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_group.v:road_yolo_numeric_rom_group@49:1-337:1; instance_path=road_yolo_numeric_rom_group; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=upper_pair_o$D; child_output=road_yolo_numeric_rom_group.upper_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_group.v:road_yolo_numeric_rom_group@49:1-337:1; instance_path=road_yolo_numeric_rom_group; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=upper_pair_o$D; child_output=road_yolo_numeric_rom_group.upper_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_group.v:road_yolo_numeric_rom_group@49:1-337:1; instance_path=road_yolo_numeric_rom_group; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=upper_pair_o$D; child_output=road_yolo_numeric_rom_group.upper_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-776"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_alpha; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/u_group_alpha.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_alpha; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/u_group_alpha.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_alpha; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/u_group_alpha.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-777"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_alpha; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/u_group_alpha.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_alpha; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/u_group_alpha.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_alpha; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/u_group_alpha.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-778"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_alpha; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/u_group_alpha.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_alpha; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/u_group_alpha.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_alpha; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/u_group_alpha.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-779"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_alpha; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/u_group_alpha.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_alpha; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/u_group_alpha.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_alpha; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/u_group_alpha.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-780"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_alpha; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lower_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_alpha.lower_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_alpha; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lower_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_alpha.lower_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_alpha; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lower_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_alpha.lower_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-781"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_alpha; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=upper_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_alpha.upper_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_alpha; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=upper_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_alpha.upper_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_alpha; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=upper_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_alpha.upper_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-782"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_beta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/u_group_beta.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_beta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/u_group_beta.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_beta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/u_group_beta.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-783"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_beta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/u_group_beta.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_beta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/u_group_beta.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_beta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/u_group_beta.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-784"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_beta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/u_group_beta.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_beta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/u_group_beta.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_beta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/u_group_beta.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-785"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_beta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/u_group_beta.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_beta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/u_group_beta.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_beta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/u_group_beta.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-786"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_beta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lower_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_beta.lower_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_beta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lower_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_beta.lower_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_beta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lower_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_beta.lower_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-787"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_beta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=upper_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_beta.upper_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_beta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=upper_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_beta.upper_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_beta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=upper_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_beta.upper_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-788"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_delta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/u_group_delta.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_delta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/u_group_delta.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_delta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/u_group_delta.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-789"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_delta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/u_group_delta.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_delta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/u_group_delta.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_delta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/u_group_delta.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-790"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_delta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/u_group_delta.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_delta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/u_group_delta.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_delta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/u_group_delta.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-791"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_delta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/u_group_delta.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_delta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/u_group_delta.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_delta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/u_group_delta.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-792"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_delta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lower_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_delta.lower_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_delta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lower_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_delta.lower_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_delta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lower_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_delta.lower_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-793"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_delta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=upper_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_delta.upper_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_delta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=upper_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_delta.upper_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_delta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=upper_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_delta.upper_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-794"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_epsilon; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/u_group_epsilon.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_epsilon; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/u_group_epsilon.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_epsilon; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/u_group_epsilon.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-795"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_epsilon; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/u_group_epsilon.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_epsilon; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/u_group_epsilon.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_epsilon; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/u_group_epsilon.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-796"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_epsilon; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/u_group_epsilon.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_epsilon; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/u_group_epsilon.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_epsilon; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/u_group_epsilon.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-797"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_epsilon; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/u_group_epsilon.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_epsilon; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/u_group_epsilon.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_epsilon; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/u_group_epsilon.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-798"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_epsilon; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lower_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_epsilon.lower_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_epsilon; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lower_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_epsilon.lower_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_epsilon; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lower_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_epsilon.lower_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-799"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_epsilon; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=upper_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_epsilon.upper_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_epsilon; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=upper_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_epsilon.upper_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_epsilon; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=upper_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_epsilon.upper_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-800"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_eta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/u_group_eta.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_eta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/u_group_eta.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_eta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/u_group_eta.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-801"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_eta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/u_group_eta.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_eta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/u_group_eta.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_eta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/u_group_eta.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-802"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_eta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/u_group_eta.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_eta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/u_group_eta.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_eta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/u_group_eta.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-803"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_eta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/u_group_eta.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_eta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/u_group_eta.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_eta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/u_group_eta.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-804"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_eta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lower_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_eta.lower_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_eta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lower_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_eta.lower_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_eta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lower_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_eta.lower_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-805"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_eta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=upper_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_eta.upper_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_eta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=upper_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_eta.upper_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_eta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=upper_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_eta.upper_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-806"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_gamma; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/u_group_gamma.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_gamma; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/u_group_gamma.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_gamma; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/u_group_gamma.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-807"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_gamma; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/u_group_gamma.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_gamma; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/u_group_gamma.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_gamma; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/u_group_gamma.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-808"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_gamma; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/u_group_gamma.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_gamma; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/u_group_gamma.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_gamma; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/u_group_gamma.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-809"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_gamma; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/u_group_gamma.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_gamma; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/u_group_gamma.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_gamma; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/u_group_gamma.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-810"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_gamma; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lower_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_gamma.lower_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_gamma; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lower_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_gamma.lower_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_gamma; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lower_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_gamma.lower_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-811"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_gamma; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=upper_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_gamma.upper_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_gamma; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=upper_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_gamma.upper_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_gamma; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=upper_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_gamma.upper_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-812"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_iota; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/u_group_iota.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_iota; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/u_group_iota.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_iota; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/u_group_iota.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-813"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_iota; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/u_group_iota.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_iota; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/u_group_iota.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_iota; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/u_group_iota.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-814"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_iota; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/u_group_iota.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_iota; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/u_group_iota.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_iota; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/u_group_iota.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-815"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_iota; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/u_group_iota.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_iota; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/u_group_iota.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_iota; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/u_group_iota.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-816"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_iota; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lower_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_iota.lower_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_iota; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lower_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_iota.lower_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_iota; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lower_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_iota.lower_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-817"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_iota; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=upper_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_iota.upper_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_iota; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=upper_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_iota.upper_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_iota; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=upper_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_iota.upper_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-818"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_kappa; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/u_group_kappa.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_kappa; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/u_group_kappa.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_kappa; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/u_group_kappa.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-819"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_kappa; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/u_group_kappa.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_kappa; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/u_group_kappa.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_kappa; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/u_group_kappa.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-820"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_kappa; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/u_group_kappa.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_kappa; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/u_group_kappa.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_kappa; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/u_group_kappa.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-821"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_kappa; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/u_group_kappa.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_kappa; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/u_group_kappa.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_kappa; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/u_group_kappa.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-822"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_kappa; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lower_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_kappa.lower_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_kappa; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lower_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_kappa.lower_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_kappa; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lower_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_kappa.lower_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-823"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_kappa; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=upper_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_kappa.upper_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_kappa; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=upper_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_kappa.upper_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_kappa; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=upper_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_kappa.upper_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-824"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_lambda; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/u_group_lambda.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_lambda; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/u_group_lambda.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_lambda; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/u_group_lambda.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-825"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_lambda; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/u_group_lambda.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_lambda; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/u_group_lambda.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_lambda; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/u_group_lambda.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-826"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_lambda; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/u_group_lambda.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_lambda; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/u_group_lambda.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_lambda; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/u_group_lambda.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-827"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_lambda; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/u_group_lambda.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_lambda; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/u_group_lambda.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_lambda; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/u_group_lambda.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-828"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_lambda; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lower_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_lambda.lower_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_lambda; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lower_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_lambda.lower_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_lambda; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lower_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_lambda.lower_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-829"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_lambda; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=upper_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_lambda.upper_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_lambda; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=upper_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_lambda.upper_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_lambda; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=upper_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_lambda.upper_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-830"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_mu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/u_group_mu.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_mu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/u_group_mu.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_mu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/u_group_mu.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-831"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_mu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/u_group_mu.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_mu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/u_group_mu.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_mu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/u_group_mu.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-832"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_mu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/u_group_mu.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_mu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/u_group_mu.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_mu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/u_group_mu.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-833"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_mu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/u_group_mu.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_mu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/u_group_mu.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_mu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/u_group_mu.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-834"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_mu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lower_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_mu.lower_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_mu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lower_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_mu.lower_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_mu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lower_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_mu.lower_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-835"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_mu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=upper_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_mu.upper_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_mu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=upper_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_mu.upper_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_mu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=upper_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_mu.upper_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-836"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_nu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/u_group_nu.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_nu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/u_group_nu.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_nu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/u_group_nu.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-837"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_nu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/u_group_nu.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_nu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/u_group_nu.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_nu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/u_group_nu.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-838"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_nu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/u_group_nu.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_nu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/u_group_nu.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_nu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/u_group_nu.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-839"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_nu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/u_group_nu.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_nu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/u_group_nu.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_nu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/u_group_nu.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-840"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_nu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lower_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_nu.lower_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_nu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lower_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_nu.lower_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_nu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lower_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_nu.lower_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-841"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_nu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=upper_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_nu.upper_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_nu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=upper_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_nu.upper_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_nu; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=upper_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_nu.upper_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-842"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_theta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/u_group_theta.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_theta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/u_group_theta.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_theta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/u_group_theta.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-843"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_theta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/u_group_theta.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_theta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/u_group_theta.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_theta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/u_group_theta.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-844"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_theta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/u_group_theta.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_theta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/u_group_theta.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_theta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/u_group_theta.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-845"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_theta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/u_group_theta.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_theta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/u_group_theta.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_theta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/u_group_theta.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-846"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_theta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lower_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_theta.lower_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_theta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lower_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_theta.lower_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_theta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lower_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_theta.lower_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-847"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_theta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=upper_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_theta.upper_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_theta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=upper_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_theta.upper_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_theta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=upper_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_theta.upper_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-848"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_xi; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/u_group_xi.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_xi; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/u_group_xi.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_xi; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/u_group_xi.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-849"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_xi; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/u_group_xi.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_xi; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/u_group_xi.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_xi; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/u_group_xi.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-850"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_xi; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/u_group_xi.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_xi; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/u_group_xi.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_xi; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/u_group_xi.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-851"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_xi; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/u_group_xi.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_xi; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/u_group_xi.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_xi; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/u_group_xi.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-852"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_xi; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lower_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_xi.lower_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_xi; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lower_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_xi.lower_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_xi; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lower_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_xi.lower_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-853"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_xi; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=upper_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_xi.upper_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_xi; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=upper_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_xi.upper_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_xi; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=upper_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_xi.upper_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-854"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_zeta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/u_group_zeta.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_zeta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/u_group_zeta.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_zeta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_alpha_data; child_output=road_yolo_numeric_rom_probe/u_group_zeta.lane_alpha_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-855"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_zeta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/u_group_zeta.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_zeta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/u_group_zeta.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_zeta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_beta_data; child_output=road_yolo_numeric_rom_probe/u_group_zeta.lane_beta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-856"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_zeta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/u_group_zeta.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_zeta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/u_group_zeta.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_zeta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_delta_data; child_output=road_yolo_numeric_rom_probe/u_group_zeta.lane_delta_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-857"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_zeta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/u_group_zeta.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_zeta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/u_group_zeta.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_zeta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lane_gamma_data; child_output=road_yolo_numeric_rom_probe/u_group_zeta.lane_gamma_data; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-858"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_zeta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lower_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_zeta.lower_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_zeta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lower_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_zeta.lower_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_zeta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=lower_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_zeta.lower_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-859"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `inconclusive`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_zeta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=upper_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_zeta.upper_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_zeta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=upper_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_zeta.upper_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_yolo_numeric_rom_probe.v:road_yolo_numeric_rom_probe@49:1-541:1; instance_path=road_yolo_numeric_rom_probe/u_group_zeta; specialization=4ab99ecd51fad293f78358c9d6a277ba760fcd3d652fea524ab6259aa588a54f; target=upper_pair_o$D; child_output=road_yolo_numeric_rom_probe/u_group_zeta.upper_pair_o$D; operation_count=0; limit=3; inconclusive_reason=missing module implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-860"></a>
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

<a id="vg-finding-861"></a>
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

<a id="vg-finding-862"></a>
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

<a id="vg-finding-863"></a>
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

<a id="vg-finding-864"></a>
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

<a id="vg-finding-865"></a>
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

<a id="vg-finding-866"></a>
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

<a id="vg-finding-867"></a>
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

<a id="vg-finding-868"></a>
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

<a id="vg-finding-869"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_probe.v:75`
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

<a id="vg-finding-870"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_probe.v:76`
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

<a id="vg-finding-871"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_probe.v:77`
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

<a id="vg-finding-872"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_probe.v:78`
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

<a id="vg-finding-873"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_probe.v:79`
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

<a id="vg-finding-874"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_probe.v:80`
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

<a id="vg-finding-875"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_probe.v:81`
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

<a id="vg-finding-876"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_probe.v:82`
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

<a id="vg-finding-877"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_probe.v:83`
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

<a id="vg-finding-878"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_probe.v:84`
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

<a id="vg-finding-879"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_probe.v:85`
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

<a id="vg-finding-880"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_probe.v:86`
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

<a id="vg-finding-881"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_probe.v:87`
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

<a id="vg-finding-882"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_probe.v:88`
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

<a id="vg-finding-883"></a>
### VG157: 普通 RTL 注释不得携带版本字样；版本历史只能位于 formatter 固定文件头范围。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:15`
- Evidence:
- node_kind: `verilog_rtl`
- detail: markers=V0.21; kind=group_or_leading
- source_excerpt: `markers=V0.21; kind=group_or_leading`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
markers=V0.21; kind=group_or_leading
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-884"></a>
### VG157: 普通 RTL 注释不得携带版本字样；版本历史只能位于 formatter 固定文件头范围。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:19`
- Evidence:
- node_kind: `verilog_rtl`
- detail: markers=V0.21; kind=group_or_leading
- source_excerpt: `markers=V0.21; kind=group_or_leading`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
markers=V0.21; kind=group_or_leading
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-885"></a>
### VG157: 普通 RTL 注释不得携带版本字样；版本历史只能位于 formatter 固定文件头范围。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:38`
- Evidence:
- node_kind: `verilog_rtl`
- detail: markers=V0.21; kind=group_or_leading
- source_excerpt: `markers=V0.21; kind=group_or_leading`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
markers=V0.21; kind=group_or_leading
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-886"></a>
### VG157: 普通 RTL 注释不得携带版本字样；版本历史只能位于 formatter 固定文件头范围。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_group.v:42`
- Evidence:
- node_kind: `verilog_rtl`
- detail: markers=V0.21; kind=group_or_leading
- source_excerpt: `markers=V0.21; kind=group_or_leading`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
markers=V0.21; kind=group_or_leading
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-887"></a>
### VG157: 普通 RTL 注释不得携带版本字样；版本历史只能位于 formatter 固定文件头范围。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_probe.v:19`
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

<a id="vg-finding-888"></a>
### VG157: 普通 RTL 注释不得携带版本字样；版本历史只能位于 formatter 固定文件头范围。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_yolo_numeric_rom_probe.v:42`
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
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_group.v:52` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_group.v:53` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_group.v:54` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_group.v:55` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_group.v:59` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_group.v:60` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_group.v:63` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_group.v:64` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_group.v:69` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_group.v:70` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_group.v:71` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_group.v:72` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_group.v:76` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_group.v:77` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_group.v:78` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_group.v:82` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_group.v:96` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_group.v:104` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_group.v:113` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_group.v:169` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_group.v:225` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_group.v:281` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_probe.v:53` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_probe.v:54` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_probe.v:57` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_probe.v:58` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_probe.v:62` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_probe.v:63` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_probe.v:64` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_probe.v:65` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_probe.v:66` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_probe.v:67` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_probe.v:68` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_probe.v:69` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_probe.v:70` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_probe.v:71` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_probe.v:75` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_probe.v:76` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_probe.v:77` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_probe.v:78` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_probe.v:79` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_probe.v:80` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_probe.v:81` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_probe.v:82` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_probe.v:83` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_probe.v:84` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_probe.v:85` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_probe.v:86` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_probe.v:87` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_probe.v:88` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_probe.v:91` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_probe.v:92` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_probe.v:95` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_probe.v:96` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_probe.v:97` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_probe.v:98` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_probe.v:102` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_probe.v:103` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_probe.v:104` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_probe.v:105` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_probe.v:106` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_probe.v:107` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_probe.v:108` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_probe.v:109` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_probe.v:110` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_probe.v:111` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_probe.v:112` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_probe.v:113` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_probe.v:114` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_probe.v:115` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_probe.v:116` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_probe.v:117` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_probe.v:118` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_probe.v:119` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_probe.v:120` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_probe.v:121` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_probe.v:122` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_probe.v:126` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_probe.v:127` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_probe.v:128` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_probe.v:129` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_probe.v:133` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_probe.v:134` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_probe.v:146` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_probe.v:155` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_probe.v:200` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_probe.v:209` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_probe.v:217` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_probe.v:229` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_probe.v:243` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_probe.v:251` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_probe.v:260` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_probe.v:268` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_probe.v:276` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_probe.v:284` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_probe.v:292` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_probe.v:300` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_probe.v:308` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_probe.v:316` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_probe.v:324` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_probe.v:332` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_probe.v:340` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_probe.v:348` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_probe.v:356` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_probe.v:364` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_probe.v:373` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_probe.v:385` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_probe.v:397` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_probe.v:409` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_probe.v:421` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_probe.v:433` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_probe.v:445` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_probe.v:457` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_probe.v:469` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_probe.v:481` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_probe.v:493` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_probe.v:505` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_probe.v:517` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_yolo_numeric_rom_probe.v:529` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `tb_ph1p_logic_eram_sim.v:5` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `tb_ph1p_logic_eram_sim.v:6` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `tb_ph1p_logic_eram_sim.v:7` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `tb_ph1p_logic_eram_sim.v:8` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `tb_ph1p_logic_eram_sim.v:9` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `tb_ph1p_logic_eram_sim.v:10` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `tb_ph1p_logic_eram_sim.v:11` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `tb_ph1p_logic_eram_sim.v:12` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `tb_ph1p_logic_eram_sim.v:13` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `tb_ph1p_logic_eram_sim.v:14` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `tb_ph1p_logic_eram_sim.v:15` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `tb_ph1p_logic_eram_sim.v:16` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `tb_ph1p_logic_eram_sim.v:17` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `tb_ph1p_logic_eram_sim.v:18` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `tb_ph1p_logic_eram_sim.v:19` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `tb_ph1p_logic_eram_sim.v:20` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `tb_ph1p_logic_eram_sim.v:21` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `tb_ph1p_logic_eram_sim.v:22` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `tb_ph1p_logic_eram_sim.v:23` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `tb_ph1p_logic_eram_sim.v:24` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `tb_ph1p_logic_eram_sim.v:25` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `tb_ph1p_logic_eram_sim.v:26` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `tb_ph1p_logic_eram_sim.v:27` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `tb_ph1p_logic_eram_sim.v:28` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `tb_ph1p_logic_eram_sim.v:29` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `tb_ph1p_logic_eram_sim.v:30` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `tb_ph1p_logic_eram_sim.v:31` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `tb_ph1p_logic_eram_sim.v:32` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `tb_ph1p_logic_eram_sim.v:33` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `tb_ph1p_logic_eram_sim.v:34` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `tb_ph1p_logic_eram_sim.v:36` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `tb_ph1p_logic_eram_sim.v:37` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `tb_ph1p_logic_eram_sim.v:38` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `tb_ph1p_logic_eram_sim.v:39` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `tb_ph1p_logic_eram_sim.v:40` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `tb_ph1p_logic_eram_sim.v:41` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `tb_ph1p_logic_eram_sim.v:42` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `tb_ph1p_logic_eram_sim.v:43` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `tb_ph1p_logic_eram_sim.v:44` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `tb_ph1p_logic_eram_sim.v:45` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `tb_ph1p_logic_eram_sim.v:46` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `tb_ph1p_logic_eram_sim.v:47` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `tb_ph1p_logic_eram_sim.v:48` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `tb_ph1p_logic_eram_sim.v:49` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `tb_ph1p_logic_eram_sim.v:50` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `tb_ph1p_logic_eram_sim.v:51` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `tb_ph1p_logic_eram_sim.v:52` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `tb_ph1p_logic_eram_sim.v:53` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `tb_ph1p_logic_eram_sim.v:54` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `tb_ph1p_logic_eram_sim.v:55` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `tb_ph1p_logic_eram_sim.v:56` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `tb_ph1p_logic_eram_sim.v:57` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `tb_ph1p_logic_eram_sim.v:60` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `tb_ph1p_logic_eram_sim.v:62` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `tb_ph1p_logic_eram_sim.v:63` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `tb_ph1p_logic_eram_sim.v:64` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `tb_ph1p_logic_eram_sim.v:66` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `tb_ph1p_logic_eram_sim.v:71` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `tb_road_yolo_numeric_rom_probe.v:4` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `tb_road_yolo_numeric_rom_probe.v:7` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `tb_road_yolo_numeric_rom_probe.v:8` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `tb_road_yolo_numeric_rom_probe.v:9` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `tb_road_yolo_numeric_rom_probe.v:12` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `tb_road_yolo_numeric_rom_probe.v:13` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `tb_road_yolo_numeric_rom_probe.v:14` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `tb_road_yolo_numeric_rom_probe.v:15` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `tb_road_yolo_numeric_rom_probe.v:16` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `tb_road_yolo_numeric_rom_probe.v:17` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `tb_road_yolo_numeric_rom_probe.v:18` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `tb_road_yolo_numeric_rom_probe.v:19` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `tb_road_yolo_numeric_rom_probe.v:20` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `tb_road_yolo_numeric_rom_probe.v:21` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `tb_road_yolo_numeric_rom_probe.v:22` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `tb_road_yolo_numeric_rom_probe.v:23` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `tb_road_yolo_numeric_rom_probe.v:24` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `tb_road_yolo_numeric_rom_probe.v:25` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `tb_road_yolo_numeric_rom_probe.v:27` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `tb_road_yolo_numeric_rom_probe.v:34` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `tb_road_yolo_numeric_rom_probe.v:39` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `tb_road_yolo_numeric_rom_probe.v:55` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
