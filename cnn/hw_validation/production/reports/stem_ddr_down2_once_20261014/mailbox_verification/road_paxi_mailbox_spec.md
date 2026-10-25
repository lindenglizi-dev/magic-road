# road_paxi_mailbox 规格

## 用途与边界

`road_paxi_mailbox` 是本次独立 Stem→DDR→down2 一次性实验的单槽跨时钟邮箱。源域为 100 MHz，DDR 用户域约 133.33 MHz。模块不提供异步 FIFO、写提交证明、重试、地址复用或单边复位恢复。

## 源接口

- 请求只在 `i_req_valid && o_req_ready` 接受。接受后，类型、25 位原生地址和 128 位写数据冻结，直到对应源响应被 `i_rsp_ready` 消费。
- 响应复制完整后置 `o_rsp_valid`；反压期间 `o_rsp_data` 与 `o_rsp_error` 保持不变。
- 从请求接受至响应消费只有一个所有者。消费响应前 `o_req_ready=0`。

## CDC 合同

请求方向使用 `req_toggle_src → req_toggle_meta_ddr → req_toggle_sync_ddr`。源冻结槽在 toggle 前写入；DDR 域检测其与 `req_toggle_seen_ddr` 不同后复制。响应方向使用 `rsp_toggle_ddr → rsp_toggle_meta_src → rsp_toggle_sync_src`，源端消费后通过 `rsp_ack_toggle_src → rsp_ack_meta_ddr → rsp_ack_sync_ddr` 确认。

请求保持窗口从源请求握手开始，至少持续到源响应消费；响应保持窗口从 DDR 发布 `rsp_toggle_ddr` 开始，持续到 `rsp_ack_sync_ddr` 返回同一世代。两个多位总线都不独立逐位同步，只在上述冻结窗口内由目标域复制一次。

## PAXI 周期

- 写：`o_awvalid` 先独立保持到 `i_awready`；AW 接受后的紧接下一 DDR 拍首次置 `o_wvalid`，并保持到 `i_wready`。不允许 W 先于 AW。写响应仅表示 AW 与 W 均已接受，不表示提交。
- 读：`o_arvalid` 保持到 `i_arready`。`o_rready` 在 AR 接受同拍即有效，因此支持同拍 `i_rvalid`。唯一返回必须同时带 `i_rlast`。
- `o_wstrb=16'h0000`；`o_wlast=o_wvalid`。

## 地址、超时与错误

合法原生地址为 `[25'h1a00000, 26'h2000000)`，且低三位为零。`C_TIMEOUT` 默认 `27'h7ffffff`，仅 TB 覆盖为 8。

`o_rsp_error`：bit0 地址；bit1 PHY；bit2 缺少 RLAST；bit3 意外 R 或超时。任一错误锁存 `o_fault`，不重试，只能由两域共同复位清除。空闲期意外 R 没有请求所有者，因此只锁存 fault，不伪造源响应。

## 复位

`i_rstn` 与 `i_ddr_rstn` 必须来自同一原始复位：共同异步断言，在各自时钟域同步释放。禁止只重启一个域。共同复位清除所有 toggle、冻结载荷、状态、响应和 fault，不允许旧结果泄漏。

## 验证

真实 ModelSim 2020.4 回归覆盖 normal、AW/W 分阶段反压、有限随机样式停顿、长响应反压、AR 同拍 R、RLAST 错误、空闲意外 R、PHY 掉线、超时、写/读/响应多个共同复位位置、复位后无旧结果，以及异相时钟下请求/响应一次性守恒。

周期图见 [road_paxi_mailbox_cycleWave.json](road_paxi_mailbox_cycleWave.json)。
