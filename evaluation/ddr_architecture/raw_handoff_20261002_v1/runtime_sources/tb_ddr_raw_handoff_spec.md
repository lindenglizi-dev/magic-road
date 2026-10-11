# tb_ddr_raw_handoff 定向验证合同

本测试只读取隔离模块 `tests/experimental_ddr_ccl/ccl_raw_run_table.v`，不修改功能 RTL。参数固定为 `MAX_RUN=64`、`ADDR_WIDTH=6`、`X_WIDTH=8`、`Y_WIDTH=8`。

## 时钟、请求和保持

所有输入在单一 `clk` 域的上升沿采样；`rst_n` 是异步低有效复位，`frame_clear` 是同步高有效清帧。测试在下降沿建立输入，使其跨下一上升沿稳定。`run_valid` 和 `row_end` 只在 `row_write_ready=1` 时作为合法输入；run 的起止坐标在 `run_valid` 采样沿保持，`row_end_y` 在 `row_end` 采样沿保持。`row_release` 只在 `raw_locked=1` 时合法。

`rd_req` 和 `rd_idx` 在上升沿采样；`rd_valid` 及 `rd_start/rd_end` 随该沿注册，并在随后一个完整周期有效。请求撤销后 `rd_valid` 必须回到 0；数据寄存器保留上次值，但消费者只能在 `rd_valid=1` 时采样。

## 同拍行交接

测试先令 A 为旧读银行、B 为新写银行，再让 `row_release` 与 B 的 `row_end` 同拍；随后交换方向，令 B 为旧读银行、A 为新写银行并重复一次。每次必须同时发生两个事件：旧银行清空并翻转读所有权，新银行保留其独立的 y、run 数量和有序 run 内容。测试通过公开读接口逐项读取，并用内部 full/count/bank 指针仅作定向诊断。

## 非法输入和恢复

两银行均 full 时 `row_write_ready=0`。此时额外 `run_valid` 必须置位 `raw_overrun` 和 `protocol_error`，且不能破坏两个已提交银行；释放旧读银行后，另一银行仍可完整读取。错误保持到 `frame_clear`，清帧后重新接收正常行。

`run_valid` 与 `row_end` 同拍始终非法。现有模块会暂存该拍数据并置位 `protocol_error`；测试明确不把它计为正常交接，也不读取或发布该行，而是要求上层以错误资格丢弃并执行 `frame_clear` 后再恢复。

```json
{"signal":[{"name":"clk","wave":"p....."},{"name":"row_release","wave":"001000"},{"name":"row_end","wave":"001000"},{"name":"old_full","wave":"1.0..."},{"name":"new_full","wave":"0.1..."},{"name":"raw_row_y","wave":"=.=...","data":["old","new"]}],"head":{"text":"旧读银行释放与另一写银行完成同拍交接"}}
```

通过标志为 `PASS raw handoff checks=<N> handoffs=2 illegal=2 reads=10`。该仿真不证明器件 RAM 推断、综合时序、真实 DDR/CDC、完整 CCL 吞吐或生产接入。
