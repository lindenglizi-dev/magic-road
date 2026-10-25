# Verilog deliverable gate

Root: `E:\project\qiansai\anlogic_topic2_work\lab1_sc500_road_vision\cnn\hw_validation\production\csp_first_closure\rtl`
Delivery ready: `False`
Summary: **323 error(s)**, **2 strict warning(s)**

## Actionable VG findings

<a id="vg-finding-1"></a>
### VG067: Header must end at the last Chinese history record; do not keep extra summary comments between the header and `module`.
- Status: `failed`
- Severity: `error`
- Location: `road_csp_first_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: header.trailing_summary_comment
- source_excerpt: `header.trailing_summary_comment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
header.trailing_summary_comment
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-2"></a>
### VG024: Instance `u_mac` should follow `<module>_Inst_<role>` naming when practical.
- Status: `failed`
- Severity: `warning`
- Location: `file:road_csp_first_probe.v:unknown`
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
### VG024: Instance `u_pp` should follow `<module>_Inst_<role>` naming when practical.
- Status: `failed`
- Severity: `warning`
- Location: `file:road_csp_first_probe.v:unknown`
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
### VG061: Item `always@(posedge i_clk or negedge i_rstn)` must be placed in 输出信号处理区域, not `主要任务处理区域`.
- Status: `failed`
- Severity: `error`
- Location: `road_csp_first_probe.v:371`
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

<a id="vg-finding-5"></a>
### VG040: Always block `always@(posedge i_clk or negedge i_rstn)` should have a nearby leading comment explaining behavior.
- Status: `failed`
- Severity: `error`
- Location: `road_csp_first_probe.v:206`
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

<a id="vg-finding-6"></a>
### VG040: Always block `always@(posedge i_clk or negedge i_rstn)` should have a nearby leading comment explaining behavior.
- Status: `failed`
- Severity: `error`
- Location: `road_csp_first_probe.v:214`
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

<a id="vg-finding-7"></a>
### VG040: Always block `always@(posedge i_clk or negedge i_rstn)` should have a nearby leading comment explaining behavior.
- Status: `failed`
- Severity: `error`
- Location: `road_csp_first_probe.v:222`
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

<a id="vg-finding-8"></a>
### VG040: Always block `always@(posedge i_clk or negedge i_rstn)` should have a nearby leading comment explaining behavior.
- Status: `failed`
- Severity: `error`
- Location: `road_csp_first_probe.v:231`
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

<a id="vg-finding-9"></a>
### VG040: Always block `always@(posedge i_clk or negedge i_rstn)` should have a nearby leading comment explaining behavior.
- Status: `failed`
- Severity: `error`
- Location: `road_csp_first_probe.v:244`
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

<a id="vg-finding-10"></a>
### VG040: Always block `always@(posedge i_clk or negedge i_rstn)` should have a nearby leading comment explaining behavior.
- Status: `failed`
- Severity: `error`
- Location: `road_csp_first_probe.v:257`
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

<a id="vg-finding-11"></a>
### VG040: Always block `always@(posedge i_clk or negedge i_rstn)` should have a nearby leading comment explaining behavior.
- Status: `failed`
- Severity: `error`
- Location: `road_csp_first_probe.v:278`
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

<a id="vg-finding-12"></a>
### VG040: Always block `always@(posedge i_clk or negedge i_rstn)` should have a nearby leading comment explaining behavior.
- Status: `failed`
- Severity: `error`
- Location: `road_csp_first_probe.v:291`
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

<a id="vg-finding-13"></a>
### VG040: Always block `always@(posedge i_clk or negedge i_rstn)` should have a nearby leading comment explaining behavior.
- Status: `failed`
- Severity: `error`
- Location: `road_csp_first_probe.v:299`
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

<a id="vg-finding-14"></a>
### VG040: Always block `always@(posedge i_clk or negedge i_rstn)` should have a nearby leading comment explaining behavior.
- Status: `failed`
- Severity: `error`
- Location: `road_csp_first_probe.v:307`
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

<a id="vg-finding-15"></a>
### VG040: Always block `always@(posedge i_clk or negedge i_rstn)` should have a nearby leading comment explaining behavior.
- Status: `failed`
- Severity: `error`
- Location: `road_csp_first_probe.v:315`
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

<a id="vg-finding-16"></a>
### VG040: Always block `always@(posedge i_clk or negedge i_rstn)` should have a nearby leading comment explaining behavior.
- Status: `failed`
- Severity: `error`
- Location: `road_csp_first_probe.v:323`
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

<a id="vg-finding-17"></a>
### VG040: Always block `always@(posedge i_clk or negedge i_rstn)` should have a nearby leading comment explaining behavior.
- Status: `failed`
- Severity: `error`
- Location: `road_csp_first_probe.v:331`
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

<a id="vg-finding-18"></a>
### VG040: Always block `always@(posedge i_clk or negedge i_rstn)` should have a nearby leading comment explaining behavior.
- Status: `failed`
- Severity: `error`
- Location: `road_csp_first_probe.v:339`
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

<a id="vg-finding-19"></a>
### VG040: Always block `always@(posedge i_clk or negedge i_rstn)` should have a nearby leading comment explaining behavior.
- Status: `failed`
- Severity: `error`
- Location: `road_csp_first_probe.v:347`
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

<a id="vg-finding-20"></a>
### VG040: Always block `always@(posedge i_clk or negedge i_rstn)` should have a nearby leading comment explaining behavior.
- Status: `failed`
- Severity: `error`
- Location: `road_csp_first_probe.v:355`
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

<a id="vg-finding-21"></a>
### VG040: Always block `always@(posedge i_clk or negedge i_rstn)` should have a nearby leading comment explaining behavior.
- Status: `failed`
- Severity: `error`
- Location: `road_csp_first_probe.v:363`
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

<a id="vg-finding-22"></a>
### VG040: Always block `always@(posedge i_clk or negedge i_rstn)` should have a nearby leading comment explaining behavior.
- Status: `failed`
- Severity: `error`
- Location: `road_csp_first_probe.v:371`
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

<a id="vg-finding-23"></a>
### VG040: Instance `u_mac` should have a leading function/connection comment.
- Status: `failed`
- Severity: `error`
- Location: `road_csp_first_probe.v:382`
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

<a id="vg-finding-24"></a>
### VG040: Instance `u_pp` should have a leading function/connection comment.
- Status: `failed`
- Severity: `error`
- Location: `road_csp_first_probe.v:399`
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

<a id="vg-finding-25"></a>
### VG062: process assignment `output_data_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_csp_first_probe.v:200`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.procedural_assignment
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-26"></a>
### VG062: process assignment `output_data_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_csp_first_probe.v:202`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.procedural_assignment
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-27"></a>
### VG062: process assignment `output_tag_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_csp_first_probe.v:208`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.procedural_assignment
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-28"></a>
### VG062: process assignment `output_tag_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_csp_first_probe.v:210`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.procedural_assignment
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-29"></a>
### VG062: process assignment `output_address_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_csp_first_probe.v:216`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.procedural_assignment
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-30"></a>
### VG062: process assignment `output_address_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_csp_first_probe.v:218`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.procedural_assignment
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-31"></a>
### VG062: process assignment `output_sum_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_csp_first_probe.v:224`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.procedural_assignment
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-32"></a>
### VG062: process assignment `output_sum_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_csp_first_probe.v:226`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.procedural_assignment
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-33"></a>
### VG062: process assignment `flag_owned` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_csp_first_probe.v:233`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.procedural_assignment
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-34"></a>
### VG062: process assignment `flag_owned` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_csp_first_probe.v:236`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.procedural_assignment
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-35"></a>
### VG062: process assignment `flag_owned` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_csp_first_probe.v:239`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.procedural_assignment
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-36"></a>
### VG062: process assignment `flag_closed` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_csp_first_probe.v:246`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.procedural_assignment
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-37"></a>
### VG062: process assignment `flag_closed` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_csp_first_probe.v:249`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.procedural_assignment
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-38"></a>
### VG062: process assignment `flag_closed` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_csp_first_probe.v:252`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.procedural_assignment
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-39"></a>
### VG062: process assignment `flag_fault` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_csp_first_probe.v:259`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.procedural_assignment
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-40"></a>
### VG062: process assignment `flag_fault` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_csp_first_probe.v:262`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.procedural_assignment
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-41"></a>
### VG062: process assignment `flag_fault` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_csp_first_probe.v:266`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.procedural_assignment
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-42"></a>
### VG062: process assignment `flag_fault` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_csp_first_probe.v:270`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.procedural_assignment
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-43"></a>
### VG062: process assignment `flag_fault` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_csp_first_probe.v:273`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.procedural_assignment
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-44"></a>
### VG062: process assignment `reg_remaining` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_csp_first_probe.v:280`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `reg_remaining` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_csp_first_probe.v:283`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `reg_remaining` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_csp_first_probe.v:286`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `reg_output_mask` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_csp_first_probe.v:293`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `reg_output_mask` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_csp_first_probe.v:295`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `reg_tags` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_csp_first_probe.v:301`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `reg_tags` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_csp_first_probe.v:303`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `reg_addresses` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_csp_first_probe.v:309`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG062: process assignment `reg_addresses` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_csp_first_probe.v:311`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.procedural_assignment
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-53"></a>
### VG062: process assignment `reg_pre_multipliers` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_csp_first_probe.v:317`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.procedural_assignment
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-54"></a>
### VG062: process assignment `reg_pre_multipliers` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_csp_first_probe.v:319`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.procedural_assignment
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-55"></a>
### VG062: process assignment `reg_pre_shifts` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_csp_first_probe.v:325`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.procedural_assignment
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-56"></a>
### VG062: process assignment `reg_pre_shifts` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_csp_first_probe.v:327`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.procedural_assignment
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-57"></a>
### VG062: process assignment `reg_post_multiplier` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_csp_first_probe.v:333`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.procedural_assignment
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-58"></a>
### VG062: process assignment `reg_post_multiplier` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_csp_first_probe.v:335`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.procedural_assignment
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-59"></a>
### VG062: process assignment `reg_post_shift` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_csp_first_probe.v:341`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.procedural_assignment
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-60"></a>
### VG062: process assignment `reg_post_shift` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_csp_first_probe.v:343`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.procedural_assignment
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-61"></a>
### VG062: process assignment `flag_residual` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_csp_first_probe.v:349`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.procedural_assignment
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-62"></a>
### VG062: process assignment `flag_residual` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_csp_first_probe.v:351`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.procedural_assignment
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-63"></a>
### VG062: process assignment `reg_bypass` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_csp_first_probe.v:357`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.procedural_assignment
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-64"></a>
### VG062: process assignment `reg_bypass` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_csp_first_probe.v:359`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.procedural_assignment
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-65"></a>
### VG062: process assignment `flag_input_fault` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_csp_first_probe.v:365`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.procedural_assignment
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-66"></a>
### VG062: process assignment `flag_input_fault` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_csp_first_probe.v:367`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.procedural_assignment
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-67"></a>
### VG062: process assignment `flag_valid_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_csp_first_probe.v:373`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.procedural_assignment
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-68"></a>
### VG062: process assignment `flag_valid_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_csp_first_probe.v:375`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.procedural_assignment
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-69"></a>
### VG062: process assignment `flag_valid_o` should have a same-line semantic comment.
- Status: `failed`
- Severity: `error`
- Location: `road_csp_first_probe.v:377`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.procedural_assignment
- source_excerpt: `comments.procedural_assignment`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
comments.procedural_assignment
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-70"></a>
### VG065: signal `wire_pp_match` must be introduced by a group comment in `其他信号`.
- Status: `failed`
- Severity: `error`
- Location: `road_csp_first_probe.v:140`
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

<a id="vg-finding-71"></a>
### VG065: signal `flag_valid_o` must be introduced by a group comment in `输出信号`.
- Status: `failed`
- Severity: `error`
- Location: `road_csp_first_probe.v:149`
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

<a id="vg-finding-72"></a>
### VG066: Comment for instance mapping `.i_clk` repeats or closely reuses comment from instance mapping `.i_clk`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_csp_first_probe.v:400`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.repeated_semantic
- source_excerpt: `comments.repeated_semantic`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG066: Comment for instance mapping `.i_rstn` repeats or closely reuses comment from instance mapping `.i_rstn`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_csp_first_probe.v:401`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.repeated_semantic
- source_excerpt: `comments.repeated_semantic`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG066: Comment for instance mapping `.i_rstn` repeats or closely reuses comment from instance mapping `.i_clk`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_csp_first_probe.v:384`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.repeated_semantic
- source_excerpt: `comments.repeated_semantic`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG066: Comment for instance mapping `.i_first` repeats or closely reuses comment from instance mapping `.i_clk`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_csp_first_probe.v:386`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.repeated_semantic
- source_excerpt: `comments.repeated_semantic`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG066: Comment for instance mapping `.i_last` repeats or closely reuses comment from instance mapping `.i_clk`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_csp_first_probe.v:387`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.repeated_semantic
- source_excerpt: `comments.repeated_semantic`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG066: Comment for instance mapping `.i_lane_mask` repeats or closely reuses comment from instance mapping `.i_clk`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_csp_first_probe.v:388`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.repeated_semantic
- source_excerpt: `comments.repeated_semantic`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG066: Comment for instance mapping `.i_activation_data` repeats or closely reuses comment from instance mapping `.i_clk`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_csp_first_probe.v:389`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.repeated_semantic
- source_excerpt: `comments.repeated_semantic`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG066: Comment for instance mapping `.i_weight_data` repeats or closely reuses comment from instance mapping `.i_clk`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_csp_first_probe.v:390`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.repeated_semantic
- source_excerpt: `comments.repeated_semantic`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG066: Comment for instance mapping `.i_bias_data` repeats or closely reuses comment from instance mapping `.i_clk`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_csp_first_probe.v:391`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.repeated_semantic
- source_excerpt: `comments.repeated_semantic`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG066: Comment for instance mapping `.o_input_ready` repeats or closely reuses comment from instance mapping `.i_clk`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_csp_first_probe.v:393`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.repeated_semantic
- source_excerpt: `comments.repeated_semantic`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG066: Comment for instance mapping `.o_result_valid` repeats or closely reuses comment from instance mapping `.i_clk`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_csp_first_probe.v:394`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.repeated_semantic
- source_excerpt: `comments.repeated_semantic`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG066: Comment for instance mapping `.o_result_data` repeats or closely reuses comment from instance mapping `.i_clk`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_csp_first_probe.v:395`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.repeated_semantic
- source_excerpt: `comments.repeated_semantic`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG066: Comment for instance mapping `.o_fault` repeats or closely reuses comment from instance mapping `.i_clk`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_csp_first_probe.v:396`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.repeated_semantic
- source_excerpt: `comments.repeated_semantic`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG066: Comment for instance mapping `.i_table_addr` repeats or closely reuses comment from instance mapping `.i_clk`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_csp_first_probe.v:403`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.repeated_semantic
- source_excerpt: `comments.repeated_semantic`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG066: Comment for instance mapping `.i_table_data` repeats or closely reuses comment from instance mapping `.i_clk`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_csp_first_probe.v:404`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.repeated_semantic
- source_excerpt: `comments.repeated_semantic`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG066: Comment for instance mapping `.o_table_ready` repeats or closely reuses comment from instance mapping `.i_clk`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_csp_first_probe.v:405`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.repeated_semantic
- source_excerpt: `comments.repeated_semantic`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG066: Comment for instance mapping `.o_table_loaded` repeats or closely reuses comment from instance mapping `.i_clk`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_csp_first_probe.v:406`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.repeated_semantic
- source_excerpt: `comments.repeated_semantic`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG066: Comment for instance mapping `.i_input_valid` repeats or closely reuses comment from instance mapping `.i_result_ready`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_csp_first_probe.v:407`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.repeated_semantic
- source_excerpt: `comments.repeated_semantic`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG066: Comment for instance mapping `.i_accumulators` repeats or closely reuses comment from instance mapping `.i_clk`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_csp_first_probe.v:408`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.repeated_semantic
- source_excerpt: `comments.repeated_semantic`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG066: Comment for instance mapping `.i_pre_multipliers` repeats or closely reuses comment from instance mapping `.i_clk`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_csp_first_probe.v:409`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.repeated_semantic
- source_excerpt: `comments.repeated_semantic`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG066: Comment for instance mapping `.i_pre_shifts` repeats or closely reuses comment from instance mapping `.i_clk`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_csp_first_probe.v:410`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.repeated_semantic
- source_excerpt: `comments.repeated_semantic`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG066: Comment for instance mapping `.i_post_multiplier` repeats or closely reuses comment from instance mapping `.i_clk`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_csp_first_probe.v:411`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.repeated_semantic
- source_excerpt: `comments.repeated_semantic`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG066: Comment for instance mapping `.i_post_shift` repeats or closely reuses comment from instance mapping `.i_clk`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_csp_first_probe.v:412`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.repeated_semantic
- source_excerpt: `comments.repeated_semantic`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG066: Comment for instance mapping `.i_activate` repeats or closely reuses comment from instance mapping `.i_clk`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_csp_first_probe.v:413`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.repeated_semantic
- source_excerpt: `comments.repeated_semantic`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG066: Comment for instance mapping `.i_lane_mask` repeats or closely reuses comment from instance mapping `.i_clk`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_csp_first_probe.v:414`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.repeated_semantic
- source_excerpt: `comments.repeated_semantic`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG066: Comment for instance mapping `.i_tags` repeats or closely reuses comment from instance mapping `.i_clk`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_csp_first_probe.v:415`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.repeated_semantic
- source_excerpt: `comments.repeated_semantic`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG066: Comment for instance mapping `.i_input_fault` repeats or closely reuses comment from instance mapping `.i_clk`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_csp_first_probe.v:416`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.repeated_semantic
- source_excerpt: `comments.repeated_semantic`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG066: Comment for instance mapping `.o_input_ready` repeats or closely reuses comment from instance mapping `.i_clk`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_csp_first_probe.v:417`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.repeated_semantic
- source_excerpt: `comments.repeated_semantic`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG066: Comment for instance mapping `.i_output_ready` repeats or closely reuses comment from instance mapping `.i_clk`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_csp_first_probe.v:418`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.repeated_semantic
- source_excerpt: `comments.repeated_semantic`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG066: Comment for instance mapping `.o_output_valid` repeats or closely reuses comment from instance mapping `.i_clk`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_csp_first_probe.v:419`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.repeated_semantic
- source_excerpt: `comments.repeated_semantic`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG066: Comment for instance mapping `.o_output_data` repeats or closely reuses comment from instance mapping `.i_clk`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_csp_first_probe.v:420`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.repeated_semantic
- source_excerpt: `comments.repeated_semantic`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG066: Comment for instance mapping `.o_output_tag` repeats or closely reuses comment from instance mapping `.i_clk`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_csp_first_probe.v:421`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.repeated_semantic
- source_excerpt: `comments.repeated_semantic`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG066: Comment for instance mapping `.o_output_int16` repeats or closely reuses comment from instance mapping `.i_clk`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_csp_first_probe.v:422`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.repeated_semantic
- source_excerpt: `comments.repeated_semantic`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG066: Comment for instance mapping `.o_fault` repeats or closely reuses comment from instance mapping `.i_clk`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `road_csp_first_probe.v:423`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.repeated_semantic
- source_excerpt: `comments.repeated_semantic`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG085: 表达式两侧位宽不一致。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:168`
- Evidence:
- node_kind: `verilog_rtl`
- detail: pp_tag == reg_tags
- source_excerpt: `pp_tag == reg_tags`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
pp_tag == reg_tags
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-107"></a>
### VG085: 表达式两侧位宽不一致。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:169`
- Evidence:
- node_kind: `verilog_rtl`
- detail: pp_tag == reg_tags
- source_excerpt: `pp_tag == reg_tags`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
pp_tag == reg_tags
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-108"></a>
### VG085: 表达式两侧位宽不一致。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:170`
- Evidence:
- node_kind: `verilog_rtl`
- detail: pp_tag == reg_tags
- source_excerpt: `pp_tag == reg_tags`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
pp_tag == reg_tags
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-109"></a>
### VG085: 表达式两侧位宽不一致。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:171`
- Evidence:
- node_kind: `verilog_rtl`
- detail: output_tag_o == reg_tags
- source_excerpt: `output_tag_o == reg_tags`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
output_tag_o == reg_tags
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-110"></a>
### VG085: 表达式两侧位宽不一致。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:172`
- Evidence:
- node_kind: `verilog_rtl`
- detail: output_tag_o == reg_tags
- source_excerpt: `output_tag_o == reg_tags`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
output_tag_o == reg_tags
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-111"></a>
### VG085: 表达式两侧位宽不一致。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:173`
- Evidence:
- node_kind: `verilog_rtl`
- detail: output_tag_o == reg_tags
- source_excerpt: `output_tag_o == reg_tags`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
output_tag_o == reg_tags
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-112"></a>
### VG093: 异步复位信号被连接到普通数据赋值右值。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:164`
- Evidence:
- node_kind: `verilog_rtl`
- detail: flag_pp_output_ready = i_rstn && !o_fault && (!flag_valid_o || i_output_ready)
- source_excerpt: `flag_pp_output_ready = i_rstn && !o_fault && (!flag_valid_o || i_output_ready)`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
flag_pp_output_ready = i_rstn && !o_fault && (!flag_valid_o || i_output_ready)
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-113"></a>
### VG093: 异步复位信号被连接到普通数据赋值右值。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:186`
- Evidence:
- node_kind: `verilog_rtl`
- detail: o_input_ready = i_rstn && o_table_loaded && !o_fault && flag_group_enable && flag_mac_ready
- source_excerpt: `o_input_ready = i_rstn && o_table_loaded && !o_fault && flag_group_enable && flag_mac_ready`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
o_input_ready = i_rstn && o_table_loaded && !o_fault && flag_group_enable && flag_mac_ready
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-114"></a>
### VG093: 异步复位信号被连接到普通数据赋值右值。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:189`
- Evidence:
- node_kind: `verilog_rtl`
- detail: o_output_valid = flag_valid_o && i_rstn && !o_fault
- source_excerpt: `o_output_valid = flag_valid_o && i_rstn && !o_fault`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
o_output_valid = flag_valid_o && i_rstn && !o_fault
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-115"></a>
### VG125: 字面量声明为 9 位，但实际值只需要 12 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:178`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 9'sh07f
- source_excerpt: `9'sh07f`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
9'sh07f
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-116"></a>
### VG125: 字面量声明为 9 位，但实际值只需要 12 位。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:179`
- Evidence:
- node_kind: `verilog_rtl`
- detail: 9'sh180
- source_excerpt: `9'sh180`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
9'sh180
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-117"></a>
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

<a id="vg-finding-118"></a>
### VG138: 常量未显式声明位宽和进制。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_csp_first_probe.v:108`
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

<a id="vg-finding-119"></a>
### VG138: 常量未显式声明位宽和进制。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_csp_first_probe.v:109`
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

<a id="vg-finding-120"></a>
### VG138: 常量未显式声明位宽和进制。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_csp_first_probe.v:110`
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

<a id="vg-finding-121"></a>
### VG138: 常量未显式声明位宽和进制。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_csp_first_probe.v:111`
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

<a id="vg-finding-122"></a>
### VG138: 常量未显式声明位宽和进制。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_csp_first_probe.v:112`
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

<a id="vg-finding-123"></a>
### VG138: 常量未显式声明位宽和进制。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_csp_first_probe.v:113`
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

<a id="vg-finding-124"></a>
### VG138: 常量未显式声明位宽和进制。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_csp_first_probe.v:114`
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

<a id="vg-finding-125"></a>
### VG138: 常量未显式声明位宽和进制。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_csp_first_probe.v:115`
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

<a id="vg-finding-126"></a>
### VG138: 常量未显式声明位宽和进制。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_csp_first_probe.v:116`
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

<a id="vg-finding-127"></a>
### VG138: 常量未显式声明位宽和进制。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_csp_first_probe.v:119`
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

<a id="vg-finding-128"></a>
### VG138: 常量未显式声明位宽和进制。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_csp_first_probe.v:120`
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

<a id="vg-finding-129"></a>
### VG138: 常量未显式声明位宽和进制。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_csp_first_probe.v:121`
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

<a id="vg-finding-130"></a>
### VG138: 常量未显式声明位宽和进制。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_csp_first_probe.v:122`
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

<a id="vg-finding-131"></a>
### VG138: 常量未显式声明位宽和进制。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_csp_first_probe.v:123`
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

<a id="vg-finding-132"></a>
### VG138: 常量未显式声明位宽和进制。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_csp_first_probe.v:149`
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

<a id="vg-finding-133"></a>
### VG138: 常量未显式声明位宽和进制。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_csp_first_probe.v:155`
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

<a id="vg-finding-134"></a>
### VG138: 常量未显式声明位宽和进制。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_csp_first_probe.v:156`
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

<a id="vg-finding-135"></a>
### VG138: 常量未显式声明位宽和进制。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_csp_first_probe.v:157`
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

<a id="vg-finding-136"></a>
### VG138: 常量未显式声明位宽和进制。
- Status: `failed`
- Severity: `WARNING`
- Location: `road_csp_first_probe.v:158`
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

<a id="vg-finding-137"></a>
### VG145: 组合逻辑完整依赖锥最多允许三个源信号，超限逻辑必须由时序 reg 隔断。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:167`
- Evidence:
- node_kind: `verilog_rtl`
- detail: flag_acc_accept: 7 sources: flag_closed, flag_fault, flag_mac_valid, flag_owned, flag_pp_ready, mac_fault, pp_fault
- source_excerpt: `flag_acc_accept: 7 sources: flag_closed, flag_fault, flag_mac_valid, flag_owned, flag_pp_ready, mac_fault, pp_fault`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
flag_acc_accept: 7 sources: flag_closed, flag_fault, flag_mac_valid, flag_owned, flag_pp_ready, mac_fault, pp_fault
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-138"></a>
### VG145: 组合逻辑完整依赖锥最多允许三个源信号，超限逻辑必须由时序 reg 隔断。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:163`
- Evidence:
- node_kind: `verilog_rtl`
- detail: flag_group_accept: 10 sources: flag_closed, flag_fault, flag_mac_ready, flag_owned, i_first, i_input_valid, i_rstn, mac_fault, pp_fault, table_loaded_o
- source_excerpt: `flag_group_accept: 10 sources: flag_closed, flag_fault, flag_mac_ready, flag_owned, i_first, i_input_valid, i_rstn, mac_fault, pp_fault, table_loaded_o`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
flag_group_accept: 10 sources: flag_closed, flag_fault, flag_mac_ready, flag_owned, i_first, i_input_valid, i_rstn, mac_fault, pp_fault, table_loaded_o
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-139"></a>
### VG145: 组合逻辑完整依赖锥最多允许三个源信号，超限逻辑必须由时序 reg 隔断。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:165`
- Evidence:
- node_kind: `verilog_rtl`
- detail: flag_pp_accept: 7 sources: flag_fault, flag_pp_valid, flag_valid_o, i_output_ready, i_rstn, mac_fault, pp_fault
- source_excerpt: `flag_pp_accept: 7 sources: flag_fault, flag_pp_valid, flag_valid_o, i_output_ready, i_rstn, mac_fault, pp_fault`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
flag_pp_accept: 7 sources: flag_fault, flag_pp_valid, flag_valid_o, i_output_ready, i_rstn, mac_fault, pp_fault
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-140"></a>
### VG145: 组合逻辑完整依赖锥最多允许三个源信号，超限逻辑必须由时序 reg 隔断。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:164`
- Evidence:
- node_kind: `verilog_rtl`
- detail: flag_pp_output_ready: 6 sources: flag_fault, flag_valid_o, i_output_ready, i_rstn, mac_fault, pp_fault
- source_excerpt: `flag_pp_output_ready: 6 sources: flag_fault, flag_valid_o, i_output_ready, i_rstn, mac_fault, pp_fault`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
flag_pp_output_ready: 6 sources: flag_fault, flag_valid_o, i_output_ready, i_rstn, mac_fault, pp_fault
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-141"></a>
### VG145: 组合逻辑完整依赖锥最多允许三个源信号，超限逻辑必须由时序 reg 隔断。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:178`
- Evidence:
- node_kind: `verilog_rtl`
- detail: flag_sum_high: 11 sources: flag_residual, pp_data[7:0], pp_data[7], pp_tag, reg_bypass[15:8], reg_bypass[23:16], reg_bypass[7:0], reg_output_mask[0], reg_output_mask[1], reg_tags[15:0], reg_tags[31:16]
- source_excerpt: `flag_sum_high: 11 sources: flag_residual, pp_data[7:0], pp_data[7], pp_tag, reg_bypass[15:8], reg_bypass[23:16], reg_bypass[7:0], reg_output_mask[0], reg_output_mask[1], reg_tags[15:0], reg_tags[31:16]`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
flag_sum_high: 11 sources: flag_residual, pp_data[7:0], pp_data[7], pp_tag, reg_bypass[15:8], reg_bypass[23:16], reg_bypass[7:0], reg_output_mask[0], reg_output_mask[1], reg_tags[15:0], reg_tags[31:16]
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-142"></a>
### VG145: 组合逻辑完整依赖锥最多允许三个源信号，超限逻辑必须由时序 reg 隔断。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:179`
- Evidence:
- node_kind: `verilog_rtl`
- detail: flag_sum_low: 11 sources: flag_residual, pp_data[7:0], pp_data[7], pp_tag, reg_bypass[15:8], reg_bypass[23:16], reg_bypass[7:0], reg_output_mask[0], reg_output_mask[1], reg_tags[15:0], reg_tags[31:16]
- source_excerpt: `flag_sum_low: 11 sources: flag_residual, pp_data[7:0], pp_data[7], pp_tag, reg_bypass[15:8], reg_bypass[23:16], reg_bypass[7:0], reg_output_mask[0], reg_output_mask[1], reg_tags[15:0], reg_tags[31:16]`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
flag_sum_low: 11 sources: flag_residual, pp_data[7:0], pp_data[7], pp_tag, reg_bypass[15:8], reg_bypass[23:16], reg_bypass[7:0], reg_output_mask[0], reg_output_mask[1], reg_tags[15:0], reg_tags[31:16]
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-143"></a>
### VG145: 组合逻辑完整依赖锥最多允许三个源信号，超限逻辑必须由时序 reg 隔断。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:166`
- Evidence:
- node_kind: `verilog_rtl`
- detail: flag_write_accept: 6 sources: flag_fault, flag_valid_o, i_output_ready, i_rstn, mac_fault, pp_fault
- source_excerpt: `flag_write_accept: 6 sources: flag_fault, flag_valid_o, i_output_ready, i_rstn, mac_fault, pp_fault`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
flag_write_accept: 6 sources: flag_fault, flag_valid_o, i_output_ready, i_rstn, mac_fault, pp_fault
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-144"></a>
### VG145: 组合逻辑完整依赖锥最多允许三个源信号，超限逻辑必须由时序 reg 隔断。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:186`
- Evidence:
- node_kind: `verilog_rtl`
- detail: o_input_ready: 9 sources: flag_closed, flag_fault, flag_mac_ready, flag_owned, i_first, i_rstn, mac_fault, pp_fault, table_loaded_o
- source_excerpt: `o_input_ready: 9 sources: flag_closed, flag_fault, flag_mac_ready, flag_owned, i_first, i_rstn, mac_fault, pp_fault, table_loaded_o`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
o_input_ready: 9 sources: flag_closed, flag_fault, flag_mac_ready, flag_owned, i_first, i_rstn, mac_fault, pp_fault, table_loaded_o
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-145"></a>
### VG145: 组合逻辑完整依赖锥最多允许三个源信号，超限逻辑必须由时序 reg 隔断。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:189`
- Evidence:
- node_kind: `verilog_rtl`
- detail: o_output_valid: 5 sources: flag_fault, flag_valid_o, i_rstn, mac_fault, pp_fault
- source_excerpt: `o_output_valid: 5 sources: flag_fault, flag_valid_o, i_rstn, mac_fault, pp_fault`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
o_output_valid: 5 sources: flag_fault, flag_valid_o, i_rstn, mac_fault, pp_fault
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-146"></a>
### VG145: 组合逻辑完整依赖锥最多允许三个源信号，超限逻辑必须由时序 reg 隔断。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:184`
- Evidence:
- node_kind: `verilog_rtl`
- detail: o_table_ready: 5 sources: flag_fault, flag_owned, flag_pp_table_ready, mac_fault, pp_fault
- source_excerpt: `o_table_ready: 5 sources: flag_fault, flag_owned, flag_pp_table_ready, mac_fault, pp_fault`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
o_table_ready: 5 sources: flag_fault, flag_owned, flag_pp_table_ready, mac_fault, pp_fault
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-147"></a>
### VG145: 组合逻辑完整依赖锥最多允许三个源信号，超限逻辑必须由时序 reg 隔断。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:176`
- Evidence:
- node_kind: `verilog_rtl`
- detail: wire_address: 8 sources: pp_tag, reg_addresses[31:0], reg_addresses[63:32], reg_addresses[95:64], reg_output_mask[0], reg_output_mask[1], reg_tags[15:0], reg_tags[31:16]
- source_excerpt: `wire_address: 8 sources: pp_tag, reg_addresses[31:0], reg_addresses[63:32], reg_addresses[95:64], reg_output_mask[0], reg_output_mask[1], reg_tags[15:0], reg_tags[31:16]`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
wire_address: 8 sources: pp_tag, reg_addresses[31:0], reg_addresses[63:32], reg_addresses[95:64], reg_output_mask[0], reg_output_mask[1], reg_tags[15:0], reg_tags[31:16]
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-148"></a>
### VG145: 组合逻辑完整依赖锥最多允许三个源信号，超限逻辑必须由时序 reg 隔断。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:175`
- Evidence:
- node_kind: `verilog_rtl`
- detail: wire_bypass: 9 sources: flag_residual, pp_tag, reg_bypass[15:8], reg_bypass[23:16], reg_bypass[7:0], reg_output_mask[0], reg_output_mask[1], reg_tags[15:0], reg_tags[31:16]
- source_excerpt: `wire_bypass: 9 sources: flag_residual, pp_tag, reg_bypass[15:8], reg_bypass[23:16], reg_bypass[7:0], reg_output_mask[0], reg_output_mask[1], reg_tags[15:0], reg_tags[31:16]`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
wire_bypass: 9 sources: flag_residual, pp_tag, reg_bypass[15:8], reg_bypass[23:16], reg_bypass[7:0], reg_output_mask[0], reg_output_mask[1], reg_tags[15:0], reg_tags[31:16]
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-149"></a>
### VG145: 组合逻辑完整依赖锥最多允许三个源信号，超限逻辑必须由时序 reg 隔断。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:180`
- Evidence:
- node_kind: `verilog_rtl`
- detail: wire_saturated: 11 sources: flag_residual, pp_data[7:0], pp_data[7], pp_tag, reg_bypass[15:8], reg_bypass[23:16], reg_bypass[7:0], reg_output_mask[0], reg_output_mask[1], reg_tags[15:0], reg_tags[31:16]
- source_excerpt: `wire_saturated: 11 sources: flag_residual, pp_data[7:0], pp_data[7], pp_tag, reg_bypass[15:8], reg_bypass[23:16], reg_bypass[7:0], reg_output_mask[0], reg_output_mask[1], reg_tags[15:0], reg_tags[31:16]`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
wire_saturated: 11 sources: flag_residual, pp_data[7:0], pp_data[7], pp_tag, reg_bypass[15:8], reg_bypass[23:16], reg_bypass[7:0], reg_output_mask[0], reg_output_mask[1], reg_tags[15:0], reg_tags[31:16]
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-150"></a>
### VG145: 组合逻辑完整依赖锥最多允许三个源信号，超限逻辑必须由时序 reg 隔断。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:177`
- Evidence:
- node_kind: `verilog_rtl`
- detail: wire_sum: 11 sources: flag_residual, pp_data[7:0], pp_data[7], pp_tag, reg_bypass[15:8], reg_bypass[23:16], reg_bypass[7:0], reg_output_mask[0], reg_output_mask[1], reg_tags[15:0], reg_tags[31:16]
- source_excerpt: `wire_sum: 11 sources: flag_residual, pp_data[7:0], pp_data[7], pp_tag, reg_bypass[15:8], reg_bypass[23:16], reg_bypass[7:0], reg_output_mask[0], reg_output_mask[1], reg_tags[15:0], reg_tags[31:16]`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
wire_sum: 11 sources: flag_residual, pp_data[7:0], pp_data[7], pp_tag, reg_bypass[15:8], reg_bypass[23:16], reg_bypass[7:0], reg_output_mask[0], reg_output_mask[1], reg_tags[15:0], reg_tags[31:16]
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
- Location: `road_csp_first_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_closed$enable; child_output=road_csp_first_probe.flag_closed$enable; operation_count=30; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_closed$enable; child_output=road_csp_first_probe.flag_closed$enable; operation_count=30; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_closed$enable; child_output=road_csp_first_probe.flag_closed$enable; operation_count=30; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
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
- Location: `road_csp_first_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_fault$enable; child_output=road_csp_first_probe.flag_fault$enable; operation_count=63; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_fault$enable; child_output=road_csp_first_probe.flag_fault$enable; operation_count=63; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_fault$enable; child_output=road_csp_first_probe.flag_fault$enable; operation_count=63; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
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
- Location: `road_csp_first_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_input_fault$enable; child_output=road_csp_first_probe.flag_input_fault$enable; operation_count=15; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_input_fault$enable; child_output=road_csp_first_probe.flag_input_fault$enable; operation_count=15; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_input_fault$enable; child_output=road_csp_first_probe.flag_input_fault$enable; operation_count=15; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-154"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_mac_ready; child_output=road_csp_first_probe.flag_mac_ready; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_mac_ready; child_output=road_csp_first_probe.flag_mac_ready; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_mac_ready; child_output=road_csp_first_probe.flag_mac_ready; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-155"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_mac_valid; child_output=road_csp_first_probe.flag_mac_valid; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_mac_valid; child_output=road_csp_first_probe.flag_mac_valid; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_mac_valid; child_output=road_csp_first_probe.flag_mac_valid; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
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
- Location: `road_csp_first_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_owned$enable; child_output=road_csp_first_probe.flag_owned$enable; operation_count=30; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_owned$enable; child_output=road_csp_first_probe.flag_owned$enable; operation_count=30; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_owned$enable; child_output=road_csp_first_probe.flag_owned$enable; operation_count=30; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-157"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_pp_rawmode; child_output=road_csp_first_probe.flag_pp_rawmode; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_pp_rawmode; child_output=road_csp_first_probe.flag_pp_rawmode; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_pp_rawmode; child_output=road_csp_first_probe.flag_pp_rawmode; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-158"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_pp_ready; child_output=road_csp_first_probe.flag_pp_ready; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_pp_ready; child_output=road_csp_first_probe.flag_pp_ready; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_pp_ready; child_output=road_csp_first_probe.flag_pp_ready; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-159"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_pp_table_ready; child_output=road_csp_first_probe.flag_pp_table_ready; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_pp_table_ready; child_output=road_csp_first_probe.flag_pp_table_ready; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_pp_table_ready; child_output=road_csp_first_probe.flag_pp_table_ready; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-160"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_pp_valid; child_output=road_csp_first_probe.flag_pp_valid; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_pp_valid; child_output=road_csp_first_probe.flag_pp_valid; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_pp_valid; child_output=road_csp_first_probe.flag_pp_valid; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
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
- Location: `road_csp_first_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_residual$enable; child_output=road_csp_first_probe.flag_residual$enable; operation_count=15; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_residual$enable; child_output=road_csp_first_probe.flag_residual$enable; operation_count=15; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_residual$enable; child_output=road_csp_first_probe.flag_residual$enable; operation_count=15; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-162"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_valid_o$D; child_output=road_csp_first_probe.flag_valid_o$D; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_valid_o$D; child_output=road_csp_first_probe.flag_valid_o$D; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_valid_o$D; child_output=road_csp_first_probe.flag_valid_o$D; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
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
- Location: `road_csp_first_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_valid_o$enable; child_output=road_csp_first_probe.flag_valid_o$enable; operation_count=9; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_valid_o$enable; child_output=road_csp_first_probe.flag_valid_o$enable; operation_count=9; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_valid_o$enable; child_output=road_csp_first_probe.flag_valid_o$enable; operation_count=9; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-164"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=mac_data; child_output=road_csp_first_probe.mac_data; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=mac_data; child_output=road_csp_first_probe.mac_data; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=mac_data; child_output=road_csp_first_probe.mac_data; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-165"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=mac_fault; child_output=road_csp_first_probe.mac_fault; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=mac_fault; child_output=road_csp_first_probe.mac_fault; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=mac_fault; child_output=road_csp_first_probe.mac_fault; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
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
- Location: `road_csp_first_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=output_address_o$D; child_output=road_csp_first_probe.output_address_o$D; operation_count=6; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=output_address_o$D; child_output=road_csp_first_probe.output_address_o$D; operation_count=6; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=output_address_o$D; child_output=road_csp_first_probe.output_address_o$D; operation_count=6; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-167"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=output_address_o$enable; child_output=road_csp_first_probe.output_address_o$enable; operation_count=9; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=output_address_o$enable; child_output=road_csp_first_probe.output_address_o$enable; operation_count=9; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=output_address_o$enable; child_output=road_csp_first_probe.output_address_o$enable; operation_count=9; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-168"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=output_data_o$D; child_output=road_csp_first_probe.output_data_o$D; operation_count=13; limit=3; inconclusive_reason=$signed: missing function definition | external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=output_data_o$D; child_output=road_csp_first_probe.output_data_o$D; operation_count=13; limit=3; inconclusive_reason=$signed: missing function definition | external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=output_data_o$D; child_output=road_csp_first_probe.output_data_o$D; operation_count=13; limit=3; inconclusive_reason=$signed: missing function definition | external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-169"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=output_data_o$enable; child_output=road_csp_first_probe.output_data_o$enable; operation_count=9; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=output_data_o$enable; child_output=road_csp_first_probe.output_data_o$enable; operation_count=9; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=output_data_o$enable; child_output=road_csp_first_probe.output_data_o$enable; operation_count=9; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-170"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=output_sum_o$D; child_output=road_csp_first_probe.output_sum_o$D; operation_count=9; limit=3; inconclusive_reason=$signed: missing function definition | external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=output_sum_o$D; child_output=road_csp_first_probe.output_sum_o$D; operation_count=9; limit=3; inconclusive_reason=$signed: missing function definition | external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=output_sum_o$D; child_output=road_csp_first_probe.output_sum_o$D; operation_count=9; limit=3; inconclusive_reason=$signed: missing function definition | external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-171"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=output_sum_o$enable; child_output=road_csp_first_probe.output_sum_o$enable; operation_count=9; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=output_sum_o$enable; child_output=road_csp_first_probe.output_sum_o$enable; operation_count=9; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=output_sum_o$enable; child_output=road_csp_first_probe.output_sum_o$enable; operation_count=9; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-172"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=output_tag_o$D; child_output=road_csp_first_probe.output_tag_o$D; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=output_tag_o$D; child_output=road_csp_first_probe.output_tag_o$D; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=output_tag_o$D; child_output=road_csp_first_probe.output_tag_o$D; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-173"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=output_tag_o$enable; child_output=road_csp_first_probe.output_tag_o$enable; operation_count=9; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=output_tag_o$enable; child_output=road_csp_first_probe.output_tag_o$enable; operation_count=9; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=output_tag_o$enable; child_output=road_csp_first_probe.output_tag_o$enable; operation_count=9; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-174"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=pp_data; child_output=road_csp_first_probe.pp_data; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=pp_data; child_output=road_csp_first_probe.pp_data; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=pp_data; child_output=road_csp_first_probe.pp_data; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-175"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=pp_fault; child_output=road_csp_first_probe.pp_fault; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=pp_fault; child_output=road_csp_first_probe.pp_fault; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=pp_fault; child_output=road_csp_first_probe.pp_fault; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-176"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=pp_tag; child_output=road_csp_first_probe.pp_tag; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=pp_tag; child_output=road_csp_first_probe.pp_tag; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=pp_tag; child_output=road_csp_first_probe.pp_tag; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-177"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_addresses$enable; child_output=road_csp_first_probe.reg_addresses$enable; operation_count=15; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_addresses$enable; child_output=road_csp_first_probe.reg_addresses$enable; operation_count=15; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_addresses$enable; child_output=road_csp_first_probe.reg_addresses$enable; operation_count=15; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-178"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_bypass$enable; child_output=road_csp_first_probe.reg_bypass$enable; operation_count=15; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_bypass$enable; child_output=road_csp_first_probe.reg_bypass$enable; operation_count=15; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_bypass$enable; child_output=road_csp_first_probe.reg_bypass$enable; operation_count=15; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-179"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_output_mask$enable; child_output=road_csp_first_probe.reg_output_mask$enable; operation_count=15; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_output_mask$enable; child_output=road_csp_first_probe.reg_output_mask$enable; operation_count=15; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_output_mask$enable; child_output=road_csp_first_probe.reg_output_mask$enable; operation_count=15; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-180"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_post_multiplier$enable; child_output=road_csp_first_probe.reg_post_multiplier$enable; operation_count=15; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_post_multiplier$enable; child_output=road_csp_first_probe.reg_post_multiplier$enable; operation_count=15; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_post_multiplier$enable; child_output=road_csp_first_probe.reg_post_multiplier$enable; operation_count=15; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-181"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_post_shift$enable; child_output=road_csp_first_probe.reg_post_shift$enable; operation_count=15; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_post_shift$enable; child_output=road_csp_first_probe.reg_post_shift$enable; operation_count=15; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_post_shift$enable; child_output=road_csp_first_probe.reg_post_shift$enable; operation_count=15; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-182"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_pre_multipliers$enable; child_output=road_csp_first_probe.reg_pre_multipliers$enable; operation_count=15; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_pre_multipliers$enable; child_output=road_csp_first_probe.reg_pre_multipliers$enable; operation_count=15; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_pre_multipliers$enable; child_output=road_csp_first_probe.reg_pre_multipliers$enable; operation_count=15; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-183"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_pre_shifts$enable; child_output=road_csp_first_probe.reg_pre_shifts$enable; operation_count=15; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_pre_shifts$enable; child_output=road_csp_first_probe.reg_pre_shifts$enable; operation_count=15; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_pre_shifts$enable; child_output=road_csp_first_probe.reg_pre_shifts$enable; operation_count=15; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-184"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_remaining$D; child_output=road_csp_first_probe.reg_remaining$D; operation_count=8; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_remaining$D; child_output=road_csp_first_probe.reg_remaining$D; operation_count=8; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_remaining$D; child_output=road_csp_first_probe.reg_remaining$D; operation_count=8; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-185"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_remaining$enable; child_output=road_csp_first_probe.reg_remaining$enable; operation_count=20; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_remaining$enable; child_output=road_csp_first_probe.reg_remaining$enable; operation_count=20; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_remaining$enable; child_output=road_csp_first_probe.reg_remaining$enable; operation_count=20; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-186"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_tags$enable; child_output=road_csp_first_probe.reg_tags$enable; operation_count=15; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_tags$enable; child_output=road_csp_first_probe.reg_tags$enable; operation_count=15; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_tags$enable; child_output=road_csp_first_probe.reg_tags$enable; operation_count=15; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-187"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=table_loaded_o; child_output=road_csp_first_probe.table_loaded_o; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=table_loaded_o; child_output=road_csp_first_probe.table_loaded_o; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=table_loaded_o; child_output=road_csp_first_probe.table_loaded_o; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-188"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:162`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_group_enable; child_output=road_csp_first_probe.flag_group_enable; operation_count=4; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_group_enable; child_output=road_csp_first_probe.flag_group_enable; operation_count=4; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_group_enable; child_output=road_csp_first_probe.flag_group_enable; operation_count=4; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-189"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:163`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_group_accept; child_output=road_csp_first_probe.flag_group_accept; operation_count=12; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_group_accept; child_output=road_csp_first_probe.flag_group_accept; operation_count=12; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_group_accept; child_output=road_csp_first_probe.flag_group_accept; operation_count=12; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-190"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:164`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_pp_output_ready; child_output=road_csp_first_probe.flag_pp_output_ready; operation_count=7; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_pp_output_ready; child_output=road_csp_first_probe.flag_pp_output_ready; operation_count=7; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_pp_output_ready; child_output=road_csp_first_probe.flag_pp_output_ready; operation_count=7; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-191"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:165`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_pp_accept; child_output=road_csp_first_probe.flag_pp_accept; operation_count=8; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_pp_accept; child_output=road_csp_first_probe.flag_pp_accept; operation_count=8; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_pp_accept; child_output=road_csp_first_probe.flag_pp_accept; operation_count=8; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-192"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:166`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_write_accept; child_output=road_csp_first_probe.flag_write_accept; operation_count=6; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_write_accept; child_output=road_csp_first_probe.flag_write_accept; operation_count=6; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_write_accept; child_output=road_csp_first_probe.flag_write_accept; operation_count=6; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-193"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:167`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_acc_accept; child_output=road_csp_first_probe.flag_acc_accept; operation_count=7; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_acc_accept; child_output=road_csp_first_probe.flag_acc_accept; operation_count=7; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_acc_accept; child_output=road_csp_first_probe.flag_acc_accept; operation_count=7; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-194"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:168`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=wire_pp_match[0]; child_output=road_csp_first_probe.wire_pp_match[0]; operation_count=2; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=wire_pp_match[0]; child_output=road_csp_first_probe.wire_pp_match[0]; operation_count=2; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=wire_pp_match[0]; child_output=road_csp_first_probe.wire_pp_match[0]; operation_count=2; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-195"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:169`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=wire_pp_match[1]; child_output=road_csp_first_probe.wire_pp_match[1]; operation_count=2; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=wire_pp_match[1]; child_output=road_csp_first_probe.wire_pp_match[1]; operation_count=2; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=wire_pp_match[1]; child_output=road_csp_first_probe.wire_pp_match[1]; operation_count=2; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-196"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:170`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=wire_pp_match[2]; child_output=road_csp_first_probe.wire_pp_match[2]; operation_count=2; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=wire_pp_match[2]; child_output=road_csp_first_probe.wire_pp_match[2]; operation_count=2; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=wire_pp_match[2]; child_output=road_csp_first_probe.wire_pp_match[2]; operation_count=2; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-197"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:171`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=wire_write_match[0]; child_output=road_csp_first_probe.wire_write_match[0]; operation_count=2; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=wire_write_match[0]; child_output=road_csp_first_probe.wire_write_match[0]; operation_count=2; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=wire_write_match[0]; child_output=road_csp_first_probe.wire_write_match[0]; operation_count=2; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-198"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:172`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=wire_write_match[1]; child_output=road_csp_first_probe.wire_write_match[1]; operation_count=2; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=wire_write_match[1]; child_output=road_csp_first_probe.wire_write_match[1]; operation_count=2; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=wire_write_match[1]; child_output=road_csp_first_probe.wire_write_match[1]; operation_count=2; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-199"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:173`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=wire_write_match[2]; child_output=road_csp_first_probe.wire_write_match[2]; operation_count=2; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=wire_write_match[2]; child_output=road_csp_first_probe.wire_write_match[2]; operation_count=2; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=wire_write_match[2]; child_output=road_csp_first_probe.wire_write_match[2]; operation_count=2; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-200"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:174`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=wire_after_write; child_output=road_csp_first_probe.wire_after_write; operation_count=8; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=wire_after_write; child_output=road_csp_first_probe.wire_after_write; operation_count=8; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=wire_after_write; child_output=road_csp_first_probe.wire_after_write; operation_count=8; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-201"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:175`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=wire_bypass; child_output=road_csp_first_probe.wire_bypass; operation_count=8; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=wire_bypass; child_output=road_csp_first_probe.wire_bypass; operation_count=8; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=wire_bypass; child_output=road_csp_first_probe.wire_bypass; operation_count=8; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-202"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:176`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=wire_address; child_output=road_csp_first_probe.wire_address; operation_count=6; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=wire_address; child_output=road_csp_first_probe.wire_address; operation_count=6; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=wire_address; child_output=road_csp_first_probe.wire_address; operation_count=6; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-203"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:177`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=wire_sum; child_output=road_csp_first_probe.wire_sum; operation_count=9; limit=3; inconclusive_reason=$signed: missing function definition | external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=wire_sum; child_output=road_csp_first_probe.wire_sum; operation_count=9; limit=3; inconclusive_reason=$signed: missing function definition | external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=wire_sum; child_output=road_csp_first_probe.wire_sum; operation_count=9; limit=3; inconclusive_reason=$signed: missing function definition | external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-204"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:178`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_sum_high; child_output=road_csp_first_probe.flag_sum_high; operation_count=10; limit=3; inconclusive_reason=$signed: missing function definition | external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_sum_high; child_output=road_csp_first_probe.flag_sum_high; operation_count=10; limit=3; inconclusive_reason=$signed: missing function definition | external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_sum_high; child_output=road_csp_first_probe.flag_sum_high; operation_count=10; limit=3; inconclusive_reason=$signed: missing function definition | external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-205"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:179`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_sum_low; child_output=road_csp_first_probe.flag_sum_low; operation_count=10; limit=3; inconclusive_reason=$signed: missing function definition | external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_sum_low; child_output=road_csp_first_probe.flag_sum_low; operation_count=10; limit=3; inconclusive_reason=$signed: missing function definition | external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_sum_low; child_output=road_csp_first_probe.flag_sum_low; operation_count=10; limit=3; inconclusive_reason=$signed: missing function definition | external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-206"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:180`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=wire_saturated; child_output=road_csp_first_probe.wire_saturated; operation_count=13; limit=3; inconclusive_reason=$signed: missing function definition | external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=wire_saturated; child_output=road_csp_first_probe.wire_saturated; operation_count=13; limit=3; inconclusive_reason=$signed: missing function definition | external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=wire_saturated; child_output=road_csp_first_probe.wire_saturated; operation_count=13; limit=3; inconclusive_reason=$signed: missing function definition | external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-207"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:184`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=o_table_ready; child_output=road_csp_first_probe.o_table_ready; operation_count=6; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=o_table_ready; child_output=road_csp_first_probe.o_table_ready; operation_count=6; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=o_table_ready; child_output=road_csp_first_probe.o_table_ready; operation_count=6; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-208"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:185`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=o_table_loaded; child_output=road_csp_first_probe.o_table_loaded; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=o_table_loaded; child_output=road_csp_first_probe.o_table_loaded; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=o_table_loaded; child_output=road_csp_first_probe.o_table_loaded; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-209"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:186`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=o_input_ready; child_output=road_csp_first_probe.o_input_ready; operation_count=11; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=o_input_ready; child_output=road_csp_first_probe.o_input_ready; operation_count=11; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=o_input_ready; child_output=road_csp_first_probe.o_input_ready; operation_count=11; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-210"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:189`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=o_output_valid; child_output=road_csp_first_probe.o_output_valid; operation_count=5; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=o_output_valid; child_output=road_csp_first_probe.o_output_valid; operation_count=5; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=o_output_valid; child_output=road_csp_first_probe.o_output_valid; operation_count=5; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-211"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:194`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=o_fault; child_output=road_csp_first_probe.o_fault; operation_count=2; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=o_fault; child_output=road_csp_first_probe.o_fault; operation_count=2; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=o_fault; child_output=road_csp_first_probe.o_fault; operation_count=2; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-212"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:231`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_owned; child_output=road_csp_first_probe.flag_owned; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_owned; child_output=road_csp_first_probe.flag_owned; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_owned; child_output=road_csp_first_probe.flag_owned; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-213"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:244`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_closed; child_output=road_csp_first_probe.flag_closed; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_closed; child_output=road_csp_first_probe.flag_closed; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_closed; child_output=road_csp_first_probe.flag_closed; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-214"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:291`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_output_mask; child_output=road_csp_first_probe.reg_output_mask; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_output_mask; child_output=road_csp_first_probe.reg_output_mask; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_output_mask; child_output=road_csp_first_probe.reg_output_mask; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-215"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:299`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_tags; child_output=road_csp_first_probe.reg_tags; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_tags; child_output=road_csp_first_probe.reg_tags; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_tags; child_output=road_csp_first_probe.reg_tags; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-216"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:315`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_pre_multipliers; child_output=road_csp_first_probe.reg_pre_multipliers; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_pre_multipliers; child_output=road_csp_first_probe.reg_pre_multipliers; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_pre_multipliers; child_output=road_csp_first_probe.reg_pre_multipliers; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-217"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:323`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_pre_shifts; child_output=road_csp_first_probe.reg_pre_shifts; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_pre_shifts; child_output=road_csp_first_probe.reg_pre_shifts; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_pre_shifts; child_output=road_csp_first_probe.reg_pre_shifts; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-218"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:331`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_post_multiplier; child_output=road_csp_first_probe.reg_post_multiplier; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_post_multiplier; child_output=road_csp_first_probe.reg_post_multiplier; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_post_multiplier; child_output=road_csp_first_probe.reg_post_multiplier; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-219"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:339`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_post_shift; child_output=road_csp_first_probe.reg_post_shift; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_post_shift; child_output=road_csp_first_probe.reg_post_shift; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_post_shift; child_output=road_csp_first_probe.reg_post_shift; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-220"></a>
### VG146: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:363`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_input_fault; child_output=road_csp_first_probe.flag_input_fault; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_input_fault; child_output=road_csp_first_probe.flag_input_fault; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_input_fault; child_output=road_csp_first_probe.flag_input_fault; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-221"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_closed$enable; child_output=road_csp_first_probe.flag_closed$enable; operation_count=30; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_closed$enable; child_output=road_csp_first_probe.flag_closed$enable; operation_count=30; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_closed$enable; child_output=road_csp_first_probe.flag_closed$enable; operation_count=30; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-222"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_fault$enable; child_output=road_csp_first_probe.flag_fault$enable; operation_count=63; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_fault$enable; child_output=road_csp_first_probe.flag_fault$enable; operation_count=63; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_fault$enable; child_output=road_csp_first_probe.flag_fault$enable; operation_count=63; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-223"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_input_fault$enable; child_output=road_csp_first_probe.flag_input_fault$enable; operation_count=15; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_input_fault$enable; child_output=road_csp_first_probe.flag_input_fault$enable; operation_count=15; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_input_fault$enable; child_output=road_csp_first_probe.flag_input_fault$enable; operation_count=15; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-224"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_mac_ready; child_output=road_csp_first_probe.flag_mac_ready; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_mac_ready; child_output=road_csp_first_probe.flag_mac_ready; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_mac_ready; child_output=road_csp_first_probe.flag_mac_ready; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-225"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_mac_valid; child_output=road_csp_first_probe.flag_mac_valid; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_mac_valid; child_output=road_csp_first_probe.flag_mac_valid; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_mac_valid; child_output=road_csp_first_probe.flag_mac_valid; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-226"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_owned$enable; child_output=road_csp_first_probe.flag_owned$enable; operation_count=30; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_owned$enable; child_output=road_csp_first_probe.flag_owned$enable; operation_count=30; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_owned$enable; child_output=road_csp_first_probe.flag_owned$enable; operation_count=30; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-227"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_pp_rawmode; child_output=road_csp_first_probe.flag_pp_rawmode; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_pp_rawmode; child_output=road_csp_first_probe.flag_pp_rawmode; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_pp_rawmode; child_output=road_csp_first_probe.flag_pp_rawmode; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-228"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_pp_ready; child_output=road_csp_first_probe.flag_pp_ready; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_pp_ready; child_output=road_csp_first_probe.flag_pp_ready; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_pp_ready; child_output=road_csp_first_probe.flag_pp_ready; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-229"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_pp_table_ready; child_output=road_csp_first_probe.flag_pp_table_ready; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_pp_table_ready; child_output=road_csp_first_probe.flag_pp_table_ready; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_pp_table_ready; child_output=road_csp_first_probe.flag_pp_table_ready; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-230"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_pp_valid; child_output=road_csp_first_probe.flag_pp_valid; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_pp_valid; child_output=road_csp_first_probe.flag_pp_valid; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_pp_valid; child_output=road_csp_first_probe.flag_pp_valid; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-231"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_residual$enable; child_output=road_csp_first_probe.flag_residual$enable; operation_count=15; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_residual$enable; child_output=road_csp_first_probe.flag_residual$enable; operation_count=15; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_residual$enable; child_output=road_csp_first_probe.flag_residual$enable; operation_count=15; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-232"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_valid_o$D; child_output=road_csp_first_probe.flag_valid_o$D; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_valid_o$D; child_output=road_csp_first_probe.flag_valid_o$D; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_valid_o$D; child_output=road_csp_first_probe.flag_valid_o$D; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-233"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_valid_o$enable; child_output=road_csp_first_probe.flag_valid_o$enable; operation_count=9; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_valid_o$enable; child_output=road_csp_first_probe.flag_valid_o$enable; operation_count=9; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_valid_o$enable; child_output=road_csp_first_probe.flag_valid_o$enable; operation_count=9; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-234"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=mac_data; child_output=road_csp_first_probe.mac_data; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=mac_data; child_output=road_csp_first_probe.mac_data; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=mac_data; child_output=road_csp_first_probe.mac_data; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-235"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=mac_fault; child_output=road_csp_first_probe.mac_fault; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=mac_fault; child_output=road_csp_first_probe.mac_fault; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=mac_fault; child_output=road_csp_first_probe.mac_fault; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-236"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=output_address_o$D; child_output=road_csp_first_probe.output_address_o$D; operation_count=6; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=output_address_o$D; child_output=road_csp_first_probe.output_address_o$D; operation_count=6; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=output_address_o$D; child_output=road_csp_first_probe.output_address_o$D; operation_count=6; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-237"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=output_address_o$enable; child_output=road_csp_first_probe.output_address_o$enable; operation_count=9; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=output_address_o$enable; child_output=road_csp_first_probe.output_address_o$enable; operation_count=9; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=output_address_o$enable; child_output=road_csp_first_probe.output_address_o$enable; operation_count=9; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-238"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=output_data_o$D; child_output=road_csp_first_probe.output_data_o$D; operation_count=13; limit=3; inconclusive_reason=$signed: missing function definition | external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=output_data_o$D; child_output=road_csp_first_probe.output_data_o$D; operation_count=13; limit=3; inconclusive_reason=$signed: missing function definition | external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=output_data_o$D; child_output=road_csp_first_probe.output_data_o$D; operation_count=13; limit=3; inconclusive_reason=$signed: missing function definition | external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-239"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=output_data_o$enable; child_output=road_csp_first_probe.output_data_o$enable; operation_count=9; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=output_data_o$enable; child_output=road_csp_first_probe.output_data_o$enable; operation_count=9; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=output_data_o$enable; child_output=road_csp_first_probe.output_data_o$enable; operation_count=9; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-240"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=output_sum_o$D; child_output=road_csp_first_probe.output_sum_o$D; operation_count=9; limit=3; inconclusive_reason=$signed: missing function definition | external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=output_sum_o$D; child_output=road_csp_first_probe.output_sum_o$D; operation_count=9; limit=3; inconclusive_reason=$signed: missing function definition | external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=output_sum_o$D; child_output=road_csp_first_probe.output_sum_o$D; operation_count=9; limit=3; inconclusive_reason=$signed: missing function definition | external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-241"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=output_sum_o$enable; child_output=road_csp_first_probe.output_sum_o$enable; operation_count=9; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=output_sum_o$enable; child_output=road_csp_first_probe.output_sum_o$enable; operation_count=9; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=output_sum_o$enable; child_output=road_csp_first_probe.output_sum_o$enable; operation_count=9; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-242"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=output_tag_o$D; child_output=road_csp_first_probe.output_tag_o$D; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=output_tag_o$D; child_output=road_csp_first_probe.output_tag_o$D; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=output_tag_o$D; child_output=road_csp_first_probe.output_tag_o$D; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-243"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=output_tag_o$enable; child_output=road_csp_first_probe.output_tag_o$enable; operation_count=9; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=output_tag_o$enable; child_output=road_csp_first_probe.output_tag_o$enable; operation_count=9; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=output_tag_o$enable; child_output=road_csp_first_probe.output_tag_o$enable; operation_count=9; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-244"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=pp_data; child_output=road_csp_first_probe.pp_data; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=pp_data; child_output=road_csp_first_probe.pp_data; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=pp_data; child_output=road_csp_first_probe.pp_data; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-245"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=pp_fault; child_output=road_csp_first_probe.pp_fault; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=pp_fault; child_output=road_csp_first_probe.pp_fault; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=pp_fault; child_output=road_csp_first_probe.pp_fault; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-246"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=pp_tag; child_output=road_csp_first_probe.pp_tag; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=pp_tag; child_output=road_csp_first_probe.pp_tag; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=pp_tag; child_output=road_csp_first_probe.pp_tag; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-247"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_addresses$enable; child_output=road_csp_first_probe.reg_addresses$enable; operation_count=15; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_addresses$enable; child_output=road_csp_first_probe.reg_addresses$enable; operation_count=15; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_addresses$enable; child_output=road_csp_first_probe.reg_addresses$enable; operation_count=15; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-248"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_bypass$enable; child_output=road_csp_first_probe.reg_bypass$enable; operation_count=15; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_bypass$enable; child_output=road_csp_first_probe.reg_bypass$enable; operation_count=15; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_bypass$enable; child_output=road_csp_first_probe.reg_bypass$enable; operation_count=15; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-249"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_output_mask$enable; child_output=road_csp_first_probe.reg_output_mask$enable; operation_count=15; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_output_mask$enable; child_output=road_csp_first_probe.reg_output_mask$enable; operation_count=15; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_output_mask$enable; child_output=road_csp_first_probe.reg_output_mask$enable; operation_count=15; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-250"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_post_multiplier$enable; child_output=road_csp_first_probe.reg_post_multiplier$enable; operation_count=15; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_post_multiplier$enable; child_output=road_csp_first_probe.reg_post_multiplier$enable; operation_count=15; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_post_multiplier$enable; child_output=road_csp_first_probe.reg_post_multiplier$enable; operation_count=15; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-251"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_post_shift$enable; child_output=road_csp_first_probe.reg_post_shift$enable; operation_count=15; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_post_shift$enable; child_output=road_csp_first_probe.reg_post_shift$enable; operation_count=15; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_post_shift$enable; child_output=road_csp_first_probe.reg_post_shift$enable; operation_count=15; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-252"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_pre_multipliers$enable; child_output=road_csp_first_probe.reg_pre_multipliers$enable; operation_count=15; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_pre_multipliers$enable; child_output=road_csp_first_probe.reg_pre_multipliers$enable; operation_count=15; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_pre_multipliers$enable; child_output=road_csp_first_probe.reg_pre_multipliers$enable; operation_count=15; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-253"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_pre_shifts$enable; child_output=road_csp_first_probe.reg_pre_shifts$enable; operation_count=15; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_pre_shifts$enable; child_output=road_csp_first_probe.reg_pre_shifts$enable; operation_count=15; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_pre_shifts$enable; child_output=road_csp_first_probe.reg_pre_shifts$enable; operation_count=15; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-254"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_remaining$D; child_output=road_csp_first_probe.reg_remaining$D; operation_count=8; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_remaining$D; child_output=road_csp_first_probe.reg_remaining$D; operation_count=8; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_remaining$D; child_output=road_csp_first_probe.reg_remaining$D; operation_count=8; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-255"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_remaining$enable; child_output=road_csp_first_probe.reg_remaining$enable; operation_count=20; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_remaining$enable; child_output=road_csp_first_probe.reg_remaining$enable; operation_count=20; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_remaining$enable; child_output=road_csp_first_probe.reg_remaining$enable; operation_count=20; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-256"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_tags$enable; child_output=road_csp_first_probe.reg_tags$enable; operation_count=15; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_tags$enable; child_output=road_csp_first_probe.reg_tags$enable; operation_count=15; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_tags$enable; child_output=road_csp_first_probe.reg_tags$enable; operation_count=15; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-257"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:49`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=table_loaded_o; child_output=road_csp_first_probe.table_loaded_o; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=table_loaded_o; child_output=road_csp_first_probe.table_loaded_o; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=table_loaded_o; child_output=road_csp_first_probe.table_loaded_o; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-258"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:162`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_group_enable; child_output=road_csp_first_probe.flag_group_enable; operation_count=4; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_group_enable; child_output=road_csp_first_probe.flag_group_enable; operation_count=4; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_group_enable; child_output=road_csp_first_probe.flag_group_enable; operation_count=4; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-259"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:163`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_group_accept; child_output=road_csp_first_probe.flag_group_accept; operation_count=12; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_group_accept; child_output=road_csp_first_probe.flag_group_accept; operation_count=12; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_group_accept; child_output=road_csp_first_probe.flag_group_accept; operation_count=12; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-260"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:164`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_pp_output_ready; child_output=road_csp_first_probe.flag_pp_output_ready; operation_count=7; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_pp_output_ready; child_output=road_csp_first_probe.flag_pp_output_ready; operation_count=7; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_pp_output_ready; child_output=road_csp_first_probe.flag_pp_output_ready; operation_count=7; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-261"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:165`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_pp_accept; child_output=road_csp_first_probe.flag_pp_accept; operation_count=8; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_pp_accept; child_output=road_csp_first_probe.flag_pp_accept; operation_count=8; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_pp_accept; child_output=road_csp_first_probe.flag_pp_accept; operation_count=8; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-262"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:166`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_write_accept; child_output=road_csp_first_probe.flag_write_accept; operation_count=6; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_write_accept; child_output=road_csp_first_probe.flag_write_accept; operation_count=6; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_write_accept; child_output=road_csp_first_probe.flag_write_accept; operation_count=6; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-263"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:167`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_acc_accept; child_output=road_csp_first_probe.flag_acc_accept; operation_count=7; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_acc_accept; child_output=road_csp_first_probe.flag_acc_accept; operation_count=7; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_acc_accept; child_output=road_csp_first_probe.flag_acc_accept; operation_count=7; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-264"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:168`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=wire_pp_match[0]; child_output=road_csp_first_probe.wire_pp_match[0]; operation_count=2; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=wire_pp_match[0]; child_output=road_csp_first_probe.wire_pp_match[0]; operation_count=2; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=wire_pp_match[0]; child_output=road_csp_first_probe.wire_pp_match[0]; operation_count=2; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-265"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:169`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=wire_pp_match[1]; child_output=road_csp_first_probe.wire_pp_match[1]; operation_count=2; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=wire_pp_match[1]; child_output=road_csp_first_probe.wire_pp_match[1]; operation_count=2; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=wire_pp_match[1]; child_output=road_csp_first_probe.wire_pp_match[1]; operation_count=2; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-266"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:170`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=wire_pp_match[2]; child_output=road_csp_first_probe.wire_pp_match[2]; operation_count=2; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=wire_pp_match[2]; child_output=road_csp_first_probe.wire_pp_match[2]; operation_count=2; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=wire_pp_match[2]; child_output=road_csp_first_probe.wire_pp_match[2]; operation_count=2; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-267"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:171`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=wire_write_match[0]; child_output=road_csp_first_probe.wire_write_match[0]; operation_count=2; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=wire_write_match[0]; child_output=road_csp_first_probe.wire_write_match[0]; operation_count=2; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=wire_write_match[0]; child_output=road_csp_first_probe.wire_write_match[0]; operation_count=2; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-268"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:172`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=wire_write_match[1]; child_output=road_csp_first_probe.wire_write_match[1]; operation_count=2; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=wire_write_match[1]; child_output=road_csp_first_probe.wire_write_match[1]; operation_count=2; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=wire_write_match[1]; child_output=road_csp_first_probe.wire_write_match[1]; operation_count=2; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-269"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:173`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=wire_write_match[2]; child_output=road_csp_first_probe.wire_write_match[2]; operation_count=2; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=wire_write_match[2]; child_output=road_csp_first_probe.wire_write_match[2]; operation_count=2; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=wire_write_match[2]; child_output=road_csp_first_probe.wire_write_match[2]; operation_count=2; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-270"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:174`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=wire_after_write; child_output=road_csp_first_probe.wire_after_write; operation_count=8; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=wire_after_write; child_output=road_csp_first_probe.wire_after_write; operation_count=8; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=wire_after_write; child_output=road_csp_first_probe.wire_after_write; operation_count=8; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-271"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:175`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=wire_bypass; child_output=road_csp_first_probe.wire_bypass; operation_count=8; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=wire_bypass; child_output=road_csp_first_probe.wire_bypass; operation_count=8; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=wire_bypass; child_output=road_csp_first_probe.wire_bypass; operation_count=8; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-272"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:176`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=wire_address; child_output=road_csp_first_probe.wire_address; operation_count=6; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=wire_address; child_output=road_csp_first_probe.wire_address; operation_count=6; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=wire_address; child_output=road_csp_first_probe.wire_address; operation_count=6; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-273"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:177`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=wire_sum; child_output=road_csp_first_probe.wire_sum; operation_count=9; limit=3; inconclusive_reason=$signed: missing function definition | external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=wire_sum; child_output=road_csp_first_probe.wire_sum; operation_count=9; limit=3; inconclusive_reason=$signed: missing function definition | external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=wire_sum; child_output=road_csp_first_probe.wire_sum; operation_count=9; limit=3; inconclusive_reason=$signed: missing function definition | external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-274"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:178`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_sum_high; child_output=road_csp_first_probe.flag_sum_high; operation_count=10; limit=3; inconclusive_reason=$signed: missing function definition | external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_sum_high; child_output=road_csp_first_probe.flag_sum_high; operation_count=10; limit=3; inconclusive_reason=$signed: missing function definition | external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_sum_high; child_output=road_csp_first_probe.flag_sum_high; operation_count=10; limit=3; inconclusive_reason=$signed: missing function definition | external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-275"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:179`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_sum_low; child_output=road_csp_first_probe.flag_sum_low; operation_count=10; limit=3; inconclusive_reason=$signed: missing function definition | external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_sum_low; child_output=road_csp_first_probe.flag_sum_low; operation_count=10; limit=3; inconclusive_reason=$signed: missing function definition | external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_sum_low; child_output=road_csp_first_probe.flag_sum_low; operation_count=10; limit=3; inconclusive_reason=$signed: missing function definition | external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-276"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:180`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=wire_saturated; child_output=road_csp_first_probe.wire_saturated; operation_count=13; limit=3; inconclusive_reason=$signed: missing function definition | external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=wire_saturated; child_output=road_csp_first_probe.wire_saturated; operation_count=13; limit=3; inconclusive_reason=$signed: missing function definition | external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=wire_saturated; child_output=road_csp_first_probe.wire_saturated; operation_count=13; limit=3; inconclusive_reason=$signed: missing function definition | external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-277"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:184`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=o_table_ready; child_output=road_csp_first_probe.o_table_ready; operation_count=6; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=o_table_ready; child_output=road_csp_first_probe.o_table_ready; operation_count=6; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=o_table_ready; child_output=road_csp_first_probe.o_table_ready; operation_count=6; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-278"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:185`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=o_table_loaded; child_output=road_csp_first_probe.o_table_loaded; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=o_table_loaded; child_output=road_csp_first_probe.o_table_loaded; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=o_table_loaded; child_output=road_csp_first_probe.o_table_loaded; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-279"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:186`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=o_input_ready; child_output=road_csp_first_probe.o_input_ready; operation_count=11; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=o_input_ready; child_output=road_csp_first_probe.o_input_ready; operation_count=11; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=o_input_ready; child_output=road_csp_first_probe.o_input_ready; operation_count=11; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-280"></a>
### VG147: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:189`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=o_output_valid; child_output=road_csp_first_probe.o_output_valid; operation_count=5; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=o_output_valid; child_output=road_csp_first_probe.o_output_valid; operation_count=5; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=o_output_valid; child_output=road_csp_first_probe.o_output_valid; operation_count=5; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-281"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:194`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=o_fault; child_output=road_csp_first_probe.o_fault; operation_count=2; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=o_fault; child_output=road_csp_first_probe.o_fault; operation_count=2; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=o_fault; child_output=road_csp_first_probe.o_fault; operation_count=2; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-282"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:231`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_owned; child_output=road_csp_first_probe.flag_owned; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_owned; child_output=road_csp_first_probe.flag_owned; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_owned; child_output=road_csp_first_probe.flag_owned; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-283"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:244`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_closed; child_output=road_csp_first_probe.flag_closed; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_closed; child_output=road_csp_first_probe.flag_closed; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_closed; child_output=road_csp_first_probe.flag_closed; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-284"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:291`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_output_mask; child_output=road_csp_first_probe.reg_output_mask; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_output_mask; child_output=road_csp_first_probe.reg_output_mask; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_output_mask; child_output=road_csp_first_probe.reg_output_mask; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-285"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:299`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_tags; child_output=road_csp_first_probe.reg_tags; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_tags; child_output=road_csp_first_probe.reg_tags; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_tags; child_output=road_csp_first_probe.reg_tags; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-286"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:315`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_pre_multipliers; child_output=road_csp_first_probe.reg_pre_multipliers; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_pre_multipliers; child_output=road_csp_first_probe.reg_pre_multipliers; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_pre_multipliers; child_output=road_csp_first_probe.reg_pre_multipliers; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-287"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:323`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_pre_shifts; child_output=road_csp_first_probe.reg_pre_shifts; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_pre_shifts; child_output=road_csp_first_probe.reg_pre_shifts; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_pre_shifts; child_output=road_csp_first_probe.reg_pre_shifts; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-288"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:331`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_post_multiplier; child_output=road_csp_first_probe.reg_post_multiplier; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_post_multiplier; child_output=road_csp_first_probe.reg_post_multiplier; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_post_multiplier; child_output=road_csp_first_probe.reg_post_multiplier; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-289"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:339`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_post_shift; child_output=road_csp_first_probe.reg_post_shift; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_post_shift; child_output=road_csp_first_probe.reg_post_shift; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=reg_post_shift; child_output=road_csp_first_probe.reg_post_shift; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-290"></a>
### VG147: 当前目标的组合操作锥包含 formatter 无法确定的结构，禁止按低计数放行。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:363`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_input_fault; child_output=road_csp_first_probe.flag_input_fault; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
- source_excerpt: `definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_input_fault; child_output=road_csp_first_probe.flag_input_fault; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=road_csp_first_probe.v:road_csp_first_probe@49:1-426:1; instance_path=road_csp_first_probe; specialization=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; target=flag_input_fault; child_output=road_csp_first_probe.flag_input_fault; operation_count=0; limit=3; inconclusive_reason=external interface has no implementation; loop_presence=unknown
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-291"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:99`
- Evidence:
- node_kind: `verilog_rtl`
- detail: mac_data
- source_excerpt: `mac_data`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
mac_data
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-292"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:100`
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

<a id="vg-finding-293"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:103`
- Evidence:
- node_kind: `verilog_rtl`
- detail: pp_data
- source_excerpt: `pp_data`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
pp_data
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-294"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:104`
- Evidence:
- node_kind: `verilog_rtl`
- detail: pp_tag
- source_excerpt: `pp_tag`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
pp_tag
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-295"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:105`
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

<a id="vg-finding-296"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:124`
- Evidence:
- node_kind: `verilog_rtl`
- detail: flag_mac_ready
- source_excerpt: `flag_mac_ready`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
flag_mac_ready
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-297"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:125`
- Evidence:
- node_kind: `verilog_rtl`
- detail: flag_mac_valid
- source_excerpt: `flag_mac_valid`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
flag_mac_valid
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-298"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:126`
- Evidence:
- node_kind: `verilog_rtl`
- detail: flag_pp_ready
- source_excerpt: `flag_pp_ready`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
flag_pp_ready
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-299"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:127`
- Evidence:
- node_kind: `verilog_rtl`
- detail: flag_pp_valid
- source_excerpt: `flag_pp_valid`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
flag_pp_valid
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-300"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:128`
- Evidence:
- node_kind: `verilog_rtl`
- detail: flag_pp_rawmode
- source_excerpt: `flag_pp_rawmode`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
flag_pp_rawmode
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-301"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:129`
- Evidence:
- node_kind: `verilog_rtl`
- detail: flag_pp_table_ready
- source_excerpt: `flag_pp_table_ready`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
flag_pp_table_ready
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-302"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:140`
- Evidence:
- node_kind: `verilog_rtl`
- detail: wire_pp_match
- source_excerpt: `wire_pp_match`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
wire_pp_match
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-303"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:141`
- Evidence:
- node_kind: `verilog_rtl`
- detail: wire_write_match
- source_excerpt: `wire_write_match`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
wire_write_match
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-304"></a>
### VG153: 信号被读取但没有可确认的驱动源。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `road_csp_first_probe.v:152`
- Evidence:
- node_kind: `verilog_rtl`
- detail: table_loaded_o
- source_excerpt: `table_loaded_o`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
table_loaded_o
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

## Other deliverable findings

| Severity | Code | Path | Line | Message |
|---|---|---|---:|---|
| error | COMMENT_COMMENT_PLACEMENT | `road_csp_first_probe.v:206` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_csp_first_probe.v:214` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_csp_first_probe.v:222` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_csp_first_probe.v:231` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_csp_first_probe.v:244` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_csp_first_probe.v:257` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_csp_first_probe.v:278` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_csp_first_probe.v:291` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_csp_first_probe.v:299` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_csp_first_probe.v:307` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_csp_first_probe.v:315` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_csp_first_probe.v:323` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_csp_first_probe.v:331` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_csp_first_probe.v:339` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_csp_first_probe.v:347` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_csp_first_probe.v:355` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_csp_first_probe.v:363` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_csp_first_probe.v:371` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_csp_first_probe.v:382` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
| error | COMMENT_COMMENT_PLACEMENT | `road_csp_first_probe.v:399` |  | Verilog code line must use a same-line or adjacent explanatory comment in the requested language. |
