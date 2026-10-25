# road_paxi_mailbox CDC 物理复核交接

## 请求方向

- 发布寄存器：`req_toggle_src`。
- 同步链：`req_toggle_meta_ddr`、`req_toggle_sync_ddr`；均带 `ASYNC_REG` 属性。
- 目标世代：`req_toggle_seen_ddr`。
- 源冻结总线：`reg_req_write_hold_src`、`reg_req_addr_hold_src[24:0]`、`reg_req_data_hold_src[127:0]`。
- 目标复制总线：`reg_req_write_ddr`、`reg_req_addr_ddr[24:0]`、`reg_req_data_ddr[127:0]`。
- 保持窗口：源请求握手先写冻结槽并翻转 `req_toggle_src`；冻结槽持续不变直到匹配的 `o_rsp_valid && i_rsp_ready`。DDR 在 toggle 经过两级同步后检测世代差并复制，因此复制前已有至少两级目标时钟的稳定余量，复制后仍保持到事务结束。

## 响应方向

- 发布寄存器：`rsp_toggle_ddr`。
- DDR 冻结总线：`reg_rsp_data_hold_ddr[127:0]`、`reg_rsp_error_hold_ddr[3:0]`。
- 同步链：`rsp_toggle_meta_src`、`rsp_toggle_sync_src`；均带 `ASYNC_REG` 属性。
- 源世代：`rsp_toggle_seen_src`；源复制寄存器为 `rsp_data_o[127:0]`、`rsp_error_o[3:0]`。
- 消费确认：`rsp_ack_toggle_src` 经 `rsp_ack_meta_ddr`、`rsp_ack_sync_ddr` 返回。
- 保持窗口：DDR 先写完整响应再翻转 `rsp_toggle_ddr`；冻结响应保持到 `rsp_ack_sync_ddr == rsp_toggle_ddr`。源域复制完成后保持输出到真实 valid/ready 消费。

## 故障方向

- DDR 粘滞源：`flag_fault_ddr`。
- 源域同步链：`fault_meta_src`、`fault_sync_src`；均带 `ASYNC_REG` 属性。
- `o_fault` 由 `fault_sync_src` 驱动。故障只由两域共同复位清除。

## 物理检查要求

对三组单比特同步链检查同域相邻放置、首级到次级的实际数据路径、恢复/移除和两时钟关系；对两组冻结多位总线检查发布寄存器到目标复制寄存器的实际最大/最小延迟及与同步 toggle 的相对到达裕量。当前未添加任何 false path、max delay、multicycle 或 bus skew 例外；若真实 P&R 不能以原时钟关系闭合，先报告精确对象和路径，不直接加例外。
