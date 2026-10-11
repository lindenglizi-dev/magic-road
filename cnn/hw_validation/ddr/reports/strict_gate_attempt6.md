# Verilog deliverable gate

Root: `E:\project\qiansai\anlogic_topic2_work\lab1_sc500_road_vision\cnn\hw_validation\ddr\paxi_single_outstanding_bridge.v`
Delivery ready: `False`
Summary: **42 error(s)**, **0 strict warning(s)**

## Actionable VG findings

<a id="vg-finding-1"></a>
### VG057: AXI port `o_paxi_accepted_write` is in section `w` after `other`; expected order is clock_reset -> aw -> w -> b -> ar -> r -> other.
- Status: `failed`
- Severity: `error`
- Location: `paxi_single_outstanding_bridge.v:83`
- Evidence:
- node_kind: `verilog_rtl`
- detail: protocol.port_order
- source_excerpt: `protocol.port_order`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `interface`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
protocol.port_order
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-2"></a>
### VG054: FSM next-state if / else if chain must end with an explicit else branch.
- Status: `failed`
- Severity: `error`
- Location: `paxi_single_outstanding_bridge.v:462`
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

<a id="vg-finding-3"></a>
### VG031: Region banners appear out of the required order.
- Status: `failed`
- Severity: `error`
- Location: `file:paxi_single_outstanding_bridge.v:unknown`
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

<a id="vg-finding-4"></a>
### VG061: Item `flag_req_write_cache` must be placed in 标志信号, not `输出信号`.
- Status: `failed`
- Severity: `error`
- Location: `paxi_single_outstanding_bridge.v:170`
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

<a id="vg-finding-5"></a>
### VG061: Item `reg_epoch` must be placed in 寄存器信号, not `输出信号`.
- Status: `failed`
- Severity: `error`
- Location: `paxi_single_outstanding_bridge.v:171`
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

<a id="vg-finding-6"></a>
### VG061: Item `reg_owner` must be placed in 寄存器信号, not `输出信号`.
- Status: `failed`
- Severity: `error`
- Location: `paxi_single_outstanding_bridge.v:172`
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

<a id="vg-finding-7"></a>
### VG061: Item `reg_paxi_addr` must be placed in 寄存器信号, not `输出信号`.
- Status: `failed`
- Severity: `error`
- Location: `paxi_single_outstanding_bridge.v:186`
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

<a id="vg-finding-8"></a>
### VG061: Item `always@(posedge i_clk or negedge i_rstn)` must be placed in 主要任务处理区域, not `输出信号处理区域`.
- Status: `failed`
- Severity: `error`
- Location: `paxi_single_outstanding_bridge.v:254`
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

<a id="vg-finding-9"></a>
### VG061: Item `always@(posedge i_clk or negedge i_rstn)` must be placed in 主要任务处理区域, not `输出信号处理区域`.
- Status: `failed`
- Severity: `error`
- Location: `paxi_single_outstanding_bridge.v:264`
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

<a id="vg-finding-10"></a>
### VG061: Item `always@(posedge i_clk or negedge i_rstn)` must be placed in 主要任务处理区域, not `输出信号处理区域`.
- Status: `failed`
- Severity: `error`
- Location: `paxi_single_outstanding_bridge.v:293`
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

<a id="vg-finding-11"></a>
### VG061: Item `always@(posedge i_clk or negedge i_rstn)` must be placed in 主要任务处理区域, not `输出信号处理区域`.
- Status: `failed`
- Severity: `error`
- Location: `paxi_single_outstanding_bridge.v:302`
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

<a id="vg-finding-12"></a>
### VG070: `输出信号` item `flag_req_write_cache` must use group label `结果接口`, not `unknown`.
- Status: `failed`
- Severity: `error`
- Location: `paxi_single_outstanding_bridge.v:170`
- Evidence:
- node_kind: `verilog_rtl`
- detail: output.mirror.group_label
- source_excerpt: `output.mirror.group_label`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
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

<a id="vg-finding-13"></a>
### VG071: `输出信号` order must follow module interface outputs ['flag_req_write_cache', 'flag_req_write_cache', 'reg_epoch', 'reg_owner', 'result_read_data_o', 'paxi_accepted_write_o', 'reg_epoch', 'reg_owner', 'drain_done_o', 'cnt_late_discard_o', 'cnt_cancelled_drain_o', 'reg_paxi_addr', 'reg_paxi_addr', 'paxi_wdata_o', 'paxi_wmask_o'], not ['flag_req_write_cache', 'reg_epoch', 'reg_owner', 'result_read_data_o', 'paxi_accepted_write_o', 'drain_done_o', 'cnt_late_discard_o', 'cnt_cancelled_drain_o', 'reg_paxi_addr', 'paxi_wdata_o', 'paxi_wmask_o'].
- Status: `failed`
- Severity: `error`
- Location: `paxi_single_outstanding_bridge.v:170`
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

<a id="vg-finding-14"></a>
### VG070: `输出信号连线` item `o_result_valid` must use group label `结果接口`, not `请求接口`.
- Status: `failed`
- Severity: `error`
- Location: `paxi_single_outstanding_bridge.v:204`
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

<a id="vg-finding-15"></a>
### VG070: `输出信号处理区域` item `flag_req_write_cache` must use group label `结果接口`, not `状态遥测`.
- Status: `failed`
- Severity: `error`
- Location: `paxi_single_outstanding_bridge.v:254`
- Evidence:
- node_kind: `verilog_rtl`
- detail: output.mirror.group_label
- source_excerpt: `output.mirror.group_label`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
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

<a id="vg-finding-16"></a>
### VG071: `输出信号处理区域` order must follow module interface outputs ['flag_req_write_cache', 'flag_req_write_cache', 'reg_epoch', 'reg_owner', 'result_read_data_o', 'paxi_accepted_write_o', 'reg_epoch', 'reg_owner', 'drain_done_o', 'cnt_late_discard_o', 'cnt_cancelled_drain_o', 'reg_paxi_addr', 'reg_paxi_addr', 'paxi_wdata_o', 'paxi_wmask_o'], not ['drain_done_o', 'flag_req_write_cache', 'reg_paxi_addr', 'paxi_wdata_o', 'paxi_wmask_o', 'reg_epoch', 'reg_owner', 'result_read_data_o', 'paxi_accepted_write_o', 'cnt_late_discard_o', 'cnt_cancelled_drain_o'].
- Status: `failed`
- Severity: `error`
- Location: `paxi_single_outstanding_bridge.v:245`
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

<a id="vg-finding-17"></a>
### VG065: signal group comment must have exactly one blank line above unless it follows a region banner.
- Status: `failed`
- Severity: `error`
- Location: `paxi_single_outstanding_bridge.v:173`
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

<a id="vg-finding-18"></a>
### VG065: signal group comment must have exactly one blank line above unless it follows a region banner.
- Status: `failed`
- Severity: `error`
- Location: `paxi_single_outstanding_bridge.v:181`
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

<a id="vg-finding-19"></a>
### VG066: Comment for Always block `always@(posedge i_clk or negedge i_rstn)` repeats or closely reuses comment from Always block `always@(posedge i_clk or negedge i_rstn)`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `paxi_single_outstanding_bridge.v:291`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.repeated_semantic
- source_excerpt: `comments.repeated_semantic`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG066: Comment for Always block `always@(posedge i_clk or negedge i_rstn)` repeats or closely reuses comment from Always block `always@(*)`; write entity-specific RTL intent.
- Status: `failed`
- Severity: `error`
- Location: `paxi_single_outstanding_bridge.v:330`
- Evidence:
- node_kind: `verilog_rtl`
- detail: comments.repeated_semantic
- source_excerpt: `comments.repeated_semantic`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `mechanical`; human review required: `False`
- Example 1 kind: `verilog`
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
### VG109: 组合逻辑 if 链缺少终止 else。
- Status: `failed`
- Severity: `WARNING`
- Location: `paxi_single_outstanding_bridge.v:247`
- Evidence:
- node_kind: `verilog_rtl`
- detail: if(state_current == ST_IDLE)
- source_excerpt: `if(state_current == ST_IDLE)`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
if(state_current == ST_IDLE)
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-22"></a>
### VG109: 组合逻辑 if 链缺少终止 else。
- Status: `failed`
- Severity: `WARNING`
- Location: `paxi_single_outstanding_bridge.v:463`
- Evidence:
- node_kind: `verilog_rtl`
- detail: if(flag_bad_protocol == 1'b1)
- source_excerpt: `if(flag_bad_protocol == 1'b1)`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
if(flag_bad_protocol == 1'b1)
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-23"></a>
### VG122: 算术结果位宽超过赋值目标位宽。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `paxi_single_outstanding_bridge.v:336`
- Evidence:
- node_kind: `verilog_rtl`
- detail: cnt_late_discard_o <= cnt_late_discard_o + 1'b1;
- source_excerpt: `cnt_late_discard_o <= cnt_late_discard_o + 1'b1;`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
cnt_late_discard_o <= cnt_late_discard_o + 1'b1;
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-24"></a>
### VG122: 算术结果位宽超过赋值目标位宽。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `paxi_single_outstanding_bridge.v:345`
- Evidence:
- node_kind: `verilog_rtl`
- detail: cnt_cancelled_drain_o <= cnt_cancelled_drain_o + 1'b1;
- source_excerpt: `cnt_cancelled_drain_o <= cnt_cancelled_drain_o + 1'b1;`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
cnt_cancelled_drain_o <= cnt_cancelled_drain_o + 1'b1;
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-25"></a>
### VG122: 算术结果位宽超过赋值目标位宽。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `paxi_single_outstanding_bridge.v:347`
- Evidence:
- node_kind: `verilog_rtl`
- detail: cnt_cancelled_drain_o <= cnt_cancelled_drain_o + 1'b1;
- source_excerpt: `cnt_cancelled_drain_o <= cnt_cancelled_drain_o + 1'b1;`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
cnt_cancelled_drain_o <= cnt_cancelled_drain_o + 1'b1;
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-26"></a>
### VG145: 组合逻辑完整依赖锥最多允许三个源信号，超限逻辑必须由时序 reg 隔断。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `paxi_single_outstanding_bridge.v:362`
- Evidence:
- node_kind: `verilog_rtl`
- detail: state_next: 17 sources: flag_addr_aligned, flag_addr_range, flag_bad_commit, flag_bad_last, flag_bad_return, flag_cancelled, flag_req_write_cache, i_cancel, i_commit_confirmed, i_paxi_arready, i_paxi_awready, i_paxi_rlast, i_paxi_rvalid, i_paxi_wready, i_req_valid, i_result_ready, state_current
- source_excerpt: `state_next: 17 sources: flag_addr_aligned, flag_addr_range, flag_bad_commit, flag_bad_last, flag_bad_return, flag_cancelled, flag_req_write_cache, i_cancel, i_commit_confirmed, i_paxi_arready, i_paxi_awready, i_paxi_rlast, i_paxi_rvalid, i_paxi_wready, i_req_valid, i_result_ready, state_current`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
state_next: 17 sources: flag_addr_aligned, flag_addr_range, flag_bad_commit, flag_bad_last, flag_bad_return, flag_cancelled, flag_req_write_cache, i_cancel, i_commit_confirmed, i_paxi_arready, i_paxi_awready, i_paxi_rlast, i_paxi_rvalid, i_paxi_wready, i_req_valid, i_result_ready, state_current
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-27"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `paxi_single_outstanding_bridge.v:254`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=paxi_single_outstanding_bridge.v:paxi_single_outstanding_bridge; instance_path=paxi_single_outstanding_bridge; specialization=default; target=flag_req_write_cache; child_output=paxi_single_outstanding_bridge.flag_req_write_cache; operation_count=7; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=paxi_single_outstanding_bridge.v:paxi_single_outstanding_bridge; instance_path=paxi_single_outstanding_bridge; specialization=default; target=flag_req_write_cache; child_output=paxi_single_outstanding_bridge.flag_req_write_cache; operation_count=7; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=paxi_single_outstanding_bridge.v:paxi_single_outstanding_bridge; instance_path=paxi_single_outstanding_bridge; specialization=default; target=flag_req_write_cache; child_output=paxi_single_outstanding_bridge.flag_req_write_cache; operation_count=7; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-28"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `paxi_single_outstanding_bridge.v:264`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=paxi_single_outstanding_bridge.v:paxi_single_outstanding_bridge; instance_path=paxi_single_outstanding_bridge; specialization=default; target=reg_paxi_addr; child_output=paxi_single_outstanding_bridge.reg_paxi_addr; operation_count=7; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=paxi_single_outstanding_bridge.v:paxi_single_outstanding_bridge; instance_path=paxi_single_outstanding_bridge; specialization=default; target=reg_paxi_addr; child_output=paxi_single_outstanding_bridge.reg_paxi_addr; operation_count=7; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=paxi_single_outstanding_bridge.v:paxi_single_outstanding_bridge; instance_path=paxi_single_outstanding_bridge; specialization=default; target=reg_paxi_addr; child_output=paxi_single_outstanding_bridge.reg_paxi_addr; operation_count=7; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-29"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `paxi_single_outstanding_bridge.v:274`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=paxi_single_outstanding_bridge.v:paxi_single_outstanding_bridge; instance_path=paxi_single_outstanding_bridge; specialization=default; target=paxi_wdata_o; child_output=paxi_single_outstanding_bridge.paxi_wdata_o; operation_count=7; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=paxi_single_outstanding_bridge.v:paxi_single_outstanding_bridge; instance_path=paxi_single_outstanding_bridge; specialization=default; target=paxi_wdata_o; child_output=paxi_single_outstanding_bridge.paxi_wdata_o; operation_count=7; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=paxi_single_outstanding_bridge.v:paxi_single_outstanding_bridge; instance_path=paxi_single_outstanding_bridge; specialization=default; target=paxi_wdata_o; child_output=paxi_single_outstanding_bridge.paxi_wdata_o; operation_count=7; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-30"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `paxi_single_outstanding_bridge.v:283`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=paxi_single_outstanding_bridge.v:paxi_single_outstanding_bridge; instance_path=paxi_single_outstanding_bridge; specialization=default; target=paxi_wmask_o; child_output=paxi_single_outstanding_bridge.paxi_wmask_o; operation_count=7; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=paxi_single_outstanding_bridge.v:paxi_single_outstanding_bridge; instance_path=paxi_single_outstanding_bridge; specialization=default; target=paxi_wmask_o; child_output=paxi_single_outstanding_bridge.paxi_wmask_o; operation_count=7; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=paxi_single_outstanding_bridge.v:paxi_single_outstanding_bridge; instance_path=paxi_single_outstanding_bridge; specialization=default; target=paxi_wmask_o; child_output=paxi_single_outstanding_bridge.paxi_wmask_o; operation_count=7; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-31"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `paxi_single_outstanding_bridge.v:293`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=paxi_single_outstanding_bridge.v:paxi_single_outstanding_bridge; instance_path=paxi_single_outstanding_bridge; specialization=default; target=reg_epoch; child_output=paxi_single_outstanding_bridge.reg_epoch; operation_count=7; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=paxi_single_outstanding_bridge.v:paxi_single_outstanding_bridge; instance_path=paxi_single_outstanding_bridge; specialization=default; target=reg_epoch; child_output=paxi_single_outstanding_bridge.reg_epoch; operation_count=7; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=paxi_single_outstanding_bridge.v:paxi_single_outstanding_bridge; instance_path=paxi_single_outstanding_bridge; specialization=default; target=reg_epoch; child_output=paxi_single_outstanding_bridge.reg_epoch; operation_count=7; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-32"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `paxi_single_outstanding_bridge.v:302`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=paxi_single_outstanding_bridge.v:paxi_single_outstanding_bridge; instance_path=paxi_single_outstanding_bridge; specialization=default; target=reg_owner; child_output=paxi_single_outstanding_bridge.reg_owner; operation_count=7; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=paxi_single_outstanding_bridge.v:paxi_single_outstanding_bridge; instance_path=paxi_single_outstanding_bridge; specialization=default; target=reg_owner; child_output=paxi_single_outstanding_bridge.reg_owner; operation_count=7; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=paxi_single_outstanding_bridge.v:paxi_single_outstanding_bridge; instance_path=paxi_single_outstanding_bridge; specialization=default; target=reg_owner; child_output=paxi_single_outstanding_bridge.reg_owner; operation_count=7; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-33"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `paxi_single_outstanding_bridge.v:312`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=paxi_single_outstanding_bridge.v:paxi_single_outstanding_bridge; instance_path=paxi_single_outstanding_bridge; specialization=default; target=result_read_data_o; child_output=paxi_single_outstanding_bridge.result_read_data_o; operation_count=6; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=paxi_single_outstanding_bridge.v:paxi_single_outstanding_bridge; instance_path=paxi_single_outstanding_bridge; specialization=default; target=result_read_data_o; child_output=paxi_single_outstanding_bridge.result_read_data_o; operation_count=6; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=paxi_single_outstanding_bridge.v:paxi_single_outstanding_bridge; instance_path=paxi_single_outstanding_bridge; specialization=default; target=result_read_data_o; child_output=paxi_single_outstanding_bridge.result_read_data_o; operation_count=6; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-34"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `paxi_single_outstanding_bridge.v:332`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=paxi_single_outstanding_bridge.v:paxi_single_outstanding_bridge; instance_path=paxi_single_outstanding_bridge; specialization=default; target=cnt_late_discard_o; child_output=paxi_single_outstanding_bridge.cnt_late_discard_o; operation_count=5; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=paxi_single_outstanding_bridge.v:paxi_single_outstanding_bridge; instance_path=paxi_single_outstanding_bridge; specialization=default; target=cnt_late_discard_o; child_output=paxi_single_outstanding_bridge.cnt_late_discard_o; operation_count=5; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=paxi_single_outstanding_bridge.v:paxi_single_outstanding_bridge; instance_path=paxi_single_outstanding_bridge; specialization=default; target=cnt_late_discard_o; child_output=paxi_single_outstanding_bridge.cnt_late_discard_o; operation_count=5; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-35"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `paxi_single_outstanding_bridge.v:341`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=paxi_single_outstanding_bridge.v:paxi_single_outstanding_bridge; instance_path=paxi_single_outstanding_bridge; specialization=default; target=cnt_cancelled_drain_o; child_output=paxi_single_outstanding_bridge.cnt_cancelled_drain_o; operation_count=12; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=paxi_single_outstanding_bridge.v:paxi_single_outstanding_bridge; instance_path=paxi_single_outstanding_bridge; specialization=default; target=cnt_cancelled_drain_o; child_output=paxi_single_outstanding_bridge.cnt_cancelled_drain_o; operation_count=12; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=paxi_single_outstanding_bridge.v:paxi_single_outstanding_bridge; instance_path=paxi_single_outstanding_bridge; specialization=default; target=cnt_cancelled_drain_o; child_output=paxi_single_outstanding_bridge.cnt_cancelled_drain_o; operation_count=12; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-36"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `paxi_single_outstanding_bridge.v:353`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=paxi_single_outstanding_bridge.v:paxi_single_outstanding_bridge; instance_path=paxi_single_outstanding_bridge; specialization=default; target=state_current; child_output=paxi_single_outstanding_bridge.state_current; operation_count=63; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=paxi_single_outstanding_bridge.v:paxi_single_outstanding_bridge; instance_path=paxi_single_outstanding_bridge; specialization=default; target=state_current; child_output=paxi_single_outstanding_bridge.state_current; operation_count=63; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=paxi_single_outstanding_bridge.v:paxi_single_outstanding_bridge; instance_path=paxi_single_outstanding_bridge; specialization=default; target=state_current; child_output=paxi_single_outstanding_bridge.state_current; operation_count=63; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-37"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `paxi_single_outstanding_bridge.v:362`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=paxi_single_outstanding_bridge.v:paxi_single_outstanding_bridge; instance_path=paxi_single_outstanding_bridge; specialization=default; target=state_next; child_output=paxi_single_outstanding_bridge.state_next; operation_count=63; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=paxi_single_outstanding_bridge.v:paxi_single_outstanding_bridge; instance_path=paxi_single_outstanding_bridge; specialization=default; target=state_next; child_output=paxi_single_outstanding_bridge.state_next; operation_count=63; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=paxi_single_outstanding_bridge.v:paxi_single_outstanding_bridge; instance_path=paxi_single_outstanding_bridge; specialization=default; target=state_next; child_output=paxi_single_outstanding_bridge.state_next; operation_count=63; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-38"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `paxi_single_outstanding_bridge.v:470`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=paxi_single_outstanding_bridge.v:paxi_single_outstanding_bridge; instance_path=paxi_single_outstanding_bridge; specialization=default; target=flag_cancelled; child_output=paxi_single_outstanding_bridge.flag_cancelled; operation_count=11; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=paxi_single_outstanding_bridge.v:paxi_single_outstanding_bridge; instance_path=paxi_single_outstanding_bridge; specialization=default; target=flag_cancelled; child_output=paxi_single_outstanding_bridge.flag_cancelled; operation_count=11; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=paxi_single_outstanding_bridge.v:paxi_single_outstanding_bridge; instance_path=paxi_single_outstanding_bridge; specialization=default; target=flag_cancelled; child_output=paxi_single_outstanding_bridge.flag_cancelled; operation_count=11; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-39"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `paxi_single_outstanding_bridge.v:481`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=paxi_single_outstanding_bridge.v:paxi_single_outstanding_bridge; instance_path=paxi_single_outstanding_bridge; specialization=default; target=flag_cancel_before_terminal; child_output=paxi_single_outstanding_bridge.flag_cancel_before_terminal; operation_count=19; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=paxi_single_outstanding_bridge.v:paxi_single_outstanding_bridge; instance_path=paxi_single_outstanding_bridge; specialization=default; target=flag_cancel_before_terminal; child_output=paxi_single_outstanding_bridge.flag_cancel_before_terminal; operation_count=19; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=paxi_single_outstanding_bridge.v:paxi_single_outstanding_bridge; instance_path=paxi_single_outstanding_bridge; specialization=default; target=flag_cancel_before_terminal; child_output=paxi_single_outstanding_bridge.flag_cancel_before_terminal; operation_count=19; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-40"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `paxi_single_outstanding_bridge.v:521`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=paxi_single_outstanding_bridge.v:paxi_single_outstanding_bridge; instance_path=paxi_single_outstanding_bridge; specialization=default; target=flag_bad_last; child_output=paxi_single_outstanding_bridge.flag_bad_last; operation_count=4; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=paxi_single_outstanding_bridge.v:paxi_single_outstanding_bridge; instance_path=paxi_single_outstanding_bridge; specialization=default; target=flag_bad_last; child_output=paxi_single_outstanding_bridge.flag_bad_last; operation_count=4; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=paxi_single_outstanding_bridge.v:paxi_single_outstanding_bridge; instance_path=paxi_single_outstanding_bridge; specialization=default; target=flag_bad_last; child_output=paxi_single_outstanding_bridge.flag_bad_last; operation_count=4; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-41"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `paxi_single_outstanding_bridge.v:531`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=paxi_single_outstanding_bridge.v:paxi_single_outstanding_bridge; instance_path=paxi_single_outstanding_bridge; specialization=default; target=flag_addr_range; child_output=paxi_single_outstanding_bridge.flag_addr_range; operation_count=10; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=paxi_single_outstanding_bridge.v:paxi_single_outstanding_bridge; instance_path=paxi_single_outstanding_bridge; specialization=default; target=flag_addr_range; child_output=paxi_single_outstanding_bridge.flag_addr_range; operation_count=10; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=paxi_single_outstanding_bridge.v:paxi_single_outstanding_bridge; instance_path=paxi_single_outstanding_bridge; specialization=default; target=flag_addr_range; child_output=paxi_single_outstanding_bridge.flag_addr_range; operation_count=10; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

<a id="vg-finding-42"></a>
### VG146: 组合逻辑操作锥超过强预算；优先加入流水寄存器、注册标志或预译码，并将复杂 FSM 条件拆为多周期时序步骤。这些修改可能改变可见延迟；若协议延迟不可变化，必须阻断并进行人工架构审查。
- Status: `failed`
- Severity: `BLOCKER`
- Location: `paxi_single_outstanding_bridge.v:540`
- Evidence:
- node_kind: `verilog_rtl`
- detail: definition_root=paxi_single_outstanding_bridge.v:paxi_single_outstanding_bridge; instance_path=paxi_single_outstanding_bridge; specialization=default; target=flag_addr_aligned; child_output=paxi_single_outstanding_bridge.flag_addr_aligned; operation_count=8; limit=3; inconclusive_reason=none; loop_presence=absent
- source_excerpt: `definition_root=paxi_single_outstanding_bridge.v:paxi_single_outstanding_bridge; instance_path=paxi_single_outstanding_bridge; specialization=default; target=flag_addr_aligned; child_output=paxi_single_outstanding_bridge.flag_addr_aligned; operation_count=8; limit=3; inconclusive_reason=none; loop_presence=absent`
- How to fix: 修复 evidence 所代表的违规事实，并在修改后重新运行对应 VG 门禁。
- Steps:
  1. 打开 location 指向的文件或结构范围，核对 evidence 与当前源码是否一致。
  2. 按 instruction 修改问题片段，保留模块接口、复位和时序契约。
  3. 重新运行对应 VG 门禁，并检查示例方向是否适用于当前模块。
- Risk: `behavioral`; human review required: `True`
- Example 1 kind: `verilog`
- Bad example:
```text
definition_root=paxi_single_outstanding_bridge.v:paxi_single_outstanding_bridge; instance_path=paxi_single_outstanding_bridge; specialization=default; target=flag_addr_aligned; child_output=paxi_single_outstanding_bridge.flag_addr_aligned; operation_count=8; limit=3; inconclusive_reason=none; loop_presence=absent
```
- Good example:
```text
按当前模块接口、时序和可综合约束重写该片段，并保留可追溯的结构事实。
```
- Example note: 示例表达修改方向，不替代当前模块的接口、时序和综合约束审查。

