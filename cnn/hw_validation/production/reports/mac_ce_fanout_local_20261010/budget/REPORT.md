# 4x4 tile 任务预算修正报告

本报告只修正冻结 graph 的任务/存储口径，不是整网周期仿真，也不形成 FPS 结论。

## 结论

- 67 个卷积已逐层列账：Stem 1、DW 23、PW 43；原始预测 INT16 层 6。
- DW 三空间点严格限制在同一 4x4 tile、同一有效输出行；stride2 的 3 组/stride1 的 2 组只是任务模型，不代表现 RTL 已支持。
- `planned_issued_tasks` 全部为 `UNKNOWN`，指整层发射及未来适配策略未证；down2 固定满 tile 已实测 DW/PW 每 tile 各 128 任务。部分 tile 同时列逻辑有效行模型和满物理槽模型，填 0 不被解释为已实现跳行。
- down2 DW/PW 的 1 tile RTL 实测仅为 1095/592 拍；完整层 630720/340992 拍仅是 tile 数乘法外推。其余 65 层为 `UNMEASURED`。
- down2 DW 完整 4x4 tile：2,304 次有效乘法/9,216 个物理槽，平均利用率 25.0%。
- graph `storage.raw_bytes` 按 tile padding 复核；逻辑有效字节独立按 H×W×C×元素字节计算。

## 23 个 DW 旧/新任务差异

旧口径为 `H×ceil(W/3)×C`，会让三点包跨过 4 列 tile 边界；新口径逐 tile、逐有效行计算。

| layer | stride | old | new logical | full-slot model | delta |
|---|---:|---:|---:|---:|---:|
| down2.dw.conv | 2 | 49,536 | 73,728 | 73,728 | +24,192 |
| csp2.blocks.0.dw.conv | 1 | 37,152 | 55,296 | 55,296 | +18,144 |
| csp2.blocks.1.dw.conv | 1 | 37,152 | 55,296 | 55,296 | +18,144 |
| down3.dw.conv | 2 | 19,008 | 27,648 | 27,648 | +8,640 |
| csp3.blocks.0.dw.conv | 1 | 19,008 | 27,648 | 27,648 | +8,640 |
| csp3.blocks.1.dw.conv | 1 | 19,008 | 27,648 | 27,648 | +8,640 |
| csp3.blocks.2.dw.conv | 1 | 19,008 | 27,648 | 27,648 | +8,640 |
| down4.dw.conv | 2 | 9,504 | 13,824 | 15,360 | +4,320 |
| csp4.blocks.0.dw.conv | 1 | 9,504 | 13,824 | 15,360 | +4,320 |
| csp4.blocks.1.dw.conv | 1 | 9,504 | 13,824 | 15,360 | +4,320 |
| csp4.blocks.2.dw.conv | 1 | 9,504 | 13,824 | 15,360 | +4,320 |
| fuse3_td.block.dw.conv | 1 | 19,008 | 27,648 | 27,648 | +8,640 |
| fuse2_td.block.dw.conv | 1 | 37,152 | 55,296 | 55,296 | +18,144 |
| down3_bu.dw.conv | 2 | 19,008 | 27,648 | 27,648 | +8,640 |
| fuse3_bu.block.dw.conv | 1 | 19,008 | 27,648 | 27,648 | +8,640 |
| down4_bu.dw.conv | 2 | 9,504 | 13,824 | 15,360 | +4,320 |
| fuse4_bu.block.dw.conv | 1 | 9,504 | 13,824 | 15,360 | +4,320 |
| head2.cls_dw.conv | 1 | 148,608 | 221,184 | 221,184 | +72,576 |
| head2.reg_dw.conv | 1 | 148,608 | 221,184 | 221,184 | +72,576 |
| head3.cls_dw.conv | 1 | 38,016 | 55,296 | 55,296 | +17,280 |
| head3.reg_dw.conv | 1 | 38,016 | 55,296 | 55,296 | +17,280 |
| head4.cls_dw.conv | 1 | 9,504 | 13,824 | 15,360 | +4,320 |
| head4.reg_dw.conv | 1 | 9,504 | 13,824 | 15,360 | +4,320 |

## 部分 tile 策略

| layer | H×W×C | logical tasks | full-slot model | actual issued | logical/tile/allocated bytes |
|---|---|---:|---:|---|---|
| down4.dw.conv | 18x32x48 | 13,824 | 15,360 | UNKNOWN | 27,648/30,720/32,768 |
| down4.pw.conv | 18x32x96 | 18,432 | 20,480 | UNKNOWN | 55,296/61,440/61,440 |
| csp4.blocks.0.dw.conv | 18x32x48 | 13,824 | 15,360 | UNKNOWN | 27,648/30,720/32,768 |
| csp4.blocks.0.pw.conv | 18x32x48 | 9,216 | 10,240 | UNKNOWN | 27,648/30,720/32,768 |
| csp4.blocks.1.dw.conv | 18x32x48 | 13,824 | 15,360 | UNKNOWN | 27,648/30,720/32,768 |
| csp4.blocks.1.pw.conv | 18x32x48 | 9,216 | 10,240 | UNKNOWN | 27,648/30,720/32,768 |
| csp4.blocks.2.dw.conv | 18x32x48 | 13,824 | 15,360 | UNKNOWN | 27,648/30,720/32,768 |
| csp4.blocks.2.pw.conv | 18x32x48 | 9,216 | 10,240 | UNKNOWN | 27,648/30,720/32,768 |
| csp4.out.conv | 18x32x96 | 18,432 | 20,480 | UNKNOWN | 55,296/61,440/61,440 |
| sppf.squeeze.conv | 18x32x24 | 4,608 | 5,120 | UNKNOWN | 13,824/15,360/16,384 |
| sppf.out.conv | 18x32x96 | 18,432 | 20,480 | UNKNOWN | 55,296/61,440/61,440 |
| lateral4.conv | 18x32x48 | 9,216 | 10,240 | UNKNOWN | 27,648/30,720/32,768 |
| down4_bu.dw.conv | 18x32x48 | 13,824 | 15,360 | UNKNOWN | 27,648/30,720/32,768 |
| down4_bu.pw.conv | 18x32x96 | 18,432 | 20,480 | UNKNOWN | 55,296/61,440/61,440 |
| fuse4_bu.reduce.conv | 18x32x96 | 18,432 | 20,480 | UNKNOWN | 55,296/61,440/61,440 |
| fuse4_bu.block.dw.conv | 18x32x48 | 13,824 | 15,360 | UNKNOWN | 27,648/30,720/32,768 |
| fuse4_bu.block.pw.conv | 18x32x48 | 9,216 | 10,240 | UNKNOWN | 27,648/30,720/32,768 |
| head4.stem.conv | 18x32x48 | 9,216 | 10,240 | UNKNOWN | 27,648/30,720/32,768 |
| head4.cls_dw.conv | 18x32x48 | 13,824 | 15,360 | UNKNOWN | 27,648/30,720/32,768 |
| head4.cls_pw.conv | 18x32x48 | 9,216 | 10,240 | UNKNOWN | 27,648/30,720/32,768 |
| head4.cls_out | 18x32x2 | 576 | 640 | UNKNOWN | 2,304/2,560/4,096 |
| head4.reg_dw.conv | 18x32x48 | 13,824 | 15,360 | UNKNOWN | 27,648/30,720/32,768 |
| head4.reg_pw.conv | 18x32x48 | 9,216 | 10,240 | UNKNOWN | 27,648/30,720/32,768 |
| head4.reg_out | 18x32x5 | 1,152 | 1,280 | UNKNOWN | 5,760/6,400/8,192 |

`down4.pw.conv` 的固定例：18×32×96，逻辑任务 18,432，满槽模型 20,480；逻辑字节 55,296，tile 存储 61,440。实际发射策略仍 UNKNOWN。

## 20M 周期参考仍缺的实际项

- actual_issued_tasks_and_partial_tile_policy: UNKNOWN — 薄适配器尚未证明跳有效行或执行满槽
- per_layer_scheduler_launch_retire_and_drain: UNKNOWN — 67层调度器尚未实现和测量
- rom_transaction_bytes_and_wait: UNKNOWN — schema2真实消费者与缓存复用尚未测量
- ddr_read_write_beats_and_arbitration_wait: UNKNOWN — 真实PAXI闭环未建立
- parameter_load_and_overlap: UNKNOWN — down2动态pre/post与通道TEST参数已接入；schema2 ROM真实取参和整图层参数装载/重叠未测
- writeback_visibility_barrier: UNKNOWN — 写接受不等于写可见，实际完成事件未绑定
- non_convolution_nodes: UNKNOWN — pool、residual、concat、nearest尚无完整周期
- layer_transition_and_tensor_view_control: UNKNOWN — 106节点全图sequencer尚未闭合
- decode_topk_nms_and_result_table: UNKNOWN — 纯FPGA后处理尚未实现和测量
- capture_queue_cdc_display_and_real_backpressure: UNKNOWN — 完整视频/DDR/显示路径尚未集成

因此不计算未知项为 0，不从 20,000,000 拍中扣除已知项，不声明 5 FPS、余量或达标比例。

## 修订记录

- 上一版 JSON SHA256：`41d5709205091e32491f94f62bc7fc91d83144d69439e362efb79f839797ea70`。
- 上一版报告 SHA256：`c36f9db85c3d686b51833ab6b735afa4f9a1e4fa772233caed2eedad36d9cb89`。
- 本版仅澄清：down2 动态 pre/post 与通道 TEST 参数已接入；UNKNOWN 是 schema2 ROM 真实取参、整图层参数装载/重叠及整层发射策略未测。

## 输入与旧文件不变

- `cnn/hw_validation/production/graph_artifacts/graph.json`: `2daf982fc92e0f14d3b568fb1fbf441651e2122a0533edb6275dce230b010738`（前后相同）
- `cnn/hw_validation/production/reports/mac_task_stream_20261009/layer_budget.json`: `891715e9b5eabb27c225f05dc533ec883e8530e360237432cba12117fb2487d8`（前后相同）
- `cnn/hw_validation/production/reports/scheduler_predecode_20261010/layer_budget.json`: `acceab90e9249a509f4ebd77be68ee82926a5c173bfe55ffd025bc0a6dcb6375`（前后相同）
- `cnn/hw_validation/production/reports/control_operand_hold_20261009/layer_budget.json`: `acceab90e9249a509f4ebd77be68ee82926a5c173bfe55ffd025bc0a6dcb6375`（前后相同）
- `cnn/hw_validation/plans/global_closure_20261010/RoadYOLO_首批执行步骤与后续里程碑.md`: `7c821059c84f7c1c2ca1dabe7181b75c94a21dc44e99c0ce93e897216bc9264d`（前后相同）
- `cnn/hw_validation/production/reports/mac_ce_fanout_local_20261010/budget/build_tile_budget.py`: `00fae53d9e332e8ecb5ef42af8a1c1672b0d22556530531ff3eeba1f266143f0`（前后相同）

生成检查：67/23/43/1/6 数量、down2 固定断言、down4 部分 tile 例、所有 raw_bytes tile padding、旧 DW 公式与旧表一致、输入哈希前后一致，全部通过。
