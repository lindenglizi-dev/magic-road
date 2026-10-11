# v13 DW 三空间点候选只读审查

日期：2026-10-08。角色：`review`。本审查不修改 RTL/Testbench，不运行 TD，不做格式问题展开。

## 审查闭包

- 候选：`rtl/down2_overlap_tile_runner.v`
  - SHA256：`cbab6698e829dbb5f71d06378b006ca2d0c64341aa288b8fe2d06bdbc3507c68`
- 回归副本：`verification/regression_candidate/down2_overlap_tile_runner.v`
  - 与候选同哈希。
- 冻结后处理：`rtl/road_postprocess_stream.v`
  - SHA256：`a51590f53c62f3a6dc51eaded0c77301b692f0cf2ae95109bd1e73afb29193fb`
  - 与 v12 原文件同哈希，后处理接口与固定系数实现未改。
- 最终功能日志：`verification/regression_candidate/v13_triplet_final.log`
  - 结尾为 `TB_PASS_DOWN2_TILE cases=4`（第 46 行）。

## 结论

在这个固定 `4x4/s2/16ch DW -> 24ch PW` 小块闭包内，未发现阻止该候选继续进入物理验证的功能缺陷。

已核对的新增 DW 路径如下：

- 21 个并集槽按三拍发射；第三拍由 `kernel_index < 21` 形成 `mask=8'h1f`，halo 横向超出 9 列时保留零激活，不产生越界数组读取（runner 第 315–335 行）。
- 稀疏权重按三个空间 lane 的 `0/2/4` 列偏移展开，同一个逻辑通道和同一偏置进入三个 MAC lane；行尾 `wire_dw_post_count=1` 时只装 lane0（runner 第 214、326–342 行）。
- 结果先锁存到 `reg_dw_triplet_result`，再在 `ST_DW_POST` 中逐路提交；只有 `flag_pp_input_accept` 才推进 lane/position/task，因此反压时数据和元数据保持（runner 第 459–461、483–510 行）。
- post 物理 lane 为 `logical_channel % 3`，base 为 `channel-lane`，position 为 `anchor+lane`；行尾不跨行（runner 第 205–222、498–505 行）。
- MAC 的 `first/last` 仍由组 0/2 产生，偏置只由冻结 MAC 的 first 语义加入一次；末组任一 lane 的 INT32 fault 在进入 `ST_DW_POST` 前转入 fault，三路都不发布（runner 第 224–238、449–461、714–725 行）。
- PW 数据排布、两拍 MAC、三通道 post 语义保持原路径；PW-only 的 384 个输出仍逐级对拍通过（最终日志第 32–36 行）。

## 问题与证据边界

### 中：原 `o_mac_cycles/o_storage_wait_cycles` 不能单独作为互斥主原因统计

`flag_pp_input_valid` 在 `pp_result_queue_count==1` 时被主动压低，但 post 的 `pp_input_ready` 仍可为 1（runner 第 234–238 行；post 第 146–148 行）。runner 又把全部 `ST_DW_POST` 周期计入 `o_mac_cycles`，只在 `~pp_input_ready` 时增加 `o_storage_wait_cycles`（runner 第 682–695 行）。因此自然 queue 保留等待不会进入 `storage_wait`，而会包含在 `mac` 中。

实际无反压日志同时给出 `mac=4224, storage_wait=0` 和 `queue_wait=128`（最终日志第 13–17 行），证明这不是纯命名假设。它不改变功能结果，但禁止把原两个接口计数解释成“有效 MAC 周期”和“全部存储等待”的互斥分解。

当前 TB 已提供补偿证据：全块状态互斥计数 `640 storage + 640 send + 2560 wait + 384 dw_post + 56 drain + 1 done = 4281 core`，且 `other=0`（最终日志第 17、23、29 行）；DW post 另列 `256 accepted scalar + 128 queue_wait + 0 ready_wait = 384`（第 16、22、28 行）。后续周期报告应引用这组状态/事件分类，不应只引用原 `mac/storage_wait` 字段。

## 覆盖核查

- 三套完整 DW/PW 向量逐级 acc/pre/SiLU/post/最终缓存通过；每套 `128 tasks / 384 beats / 256 DW scalars / 64 tail scalars`，256 个 DW 地址唯一且完整（最终日志第 13–31 行）。
- 新状态的四个无停顿任务均为 `storage=3, send=3, wait=10, post=5, accepts=3`（第 5–10 行）。
- `ST_DW_POST` lane0/1/2 分别保持 64 拍，payload、position、channel base、mask、reservation 不变；lane2 中复位取消，随后 20 拍无 ghost（第 4 行；TB 第 840–907 行）。
- DW 新增空间 lane1/2 的正负单 lane overflow 共四例均原子 fault，pre/writeback/DW commit/export 均为零；两个合法极限不误报 fault（最终日志第 38–43 行；TB 第 946–1006、1179–1184 行）。
- 随机 commit 反压、表装载互斥、ack-local 四态、缓存单写口比较和旧 PW-only 路径均保留通过（最终日志第 1–2、25–36、44–45 行）。

## 八项门禁状态

`gates/runner.json` 生成于最终候选哈希之前，不能当作当前哈希的最终严格门禁。其公开状态仅记录为：

| 门禁 | 保存状态 | 本审查解释 |
|---|---|---|
| compile | passed | 旧候选静态解析通过；当前候选另有 Verilog-2001 编译并执行通过，但未重跑严格门禁 |
| ast | failed | 未闭合 |
| readability | failed | 未闭合，本轮按要求不做格式展开 |
| comment | failed | 未闭合，本轮按要求不做格式展开 |
| naming | failed | 未闭合，本轮按要求不做格式展开 |
| profile | failed | 未闭合 |
| testbench | not_requested | 严格门禁未纳入 TB；独立 vvp 回归通过不改写该字段 |
| toolchain | not_requested | 严格门禁未登记外部实现；功能仿真不等于 TD/综合/布局布线 |

## 未覆盖范围

- 本审查不评价正在另行执行的 TD 资源与时序结果，也不把 v12 物理结果继承给 v13。
- 当前数值是测试参数小块，不是 Ground48、部署 QAT、67 层 DDR 闭环或整机 5 FPS 证明。
- 当前 halo 是已预装 9x9 小块；外部 DDR/tile reader 的真实边界取数、返回归属和可见性仍需阶段 D 单独证明。
