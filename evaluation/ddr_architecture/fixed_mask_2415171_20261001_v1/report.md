# DDR 固定 Mask 单因素审计

当前 min-run 与保留全部 run；背景历史、面积门槛及项目 Top4/匹配规则保持不变。

| 配置/分支 | 行 run 峰值 | 标签 p50 / p95 / max | 容量超限帧/960 | Top4 行人/机动车匹配 |
|---|---:|---|---:|---|
| baseline256/current | 17 | 81 / 103 / 121 | 833 | 11/46 / 3/11 |
| baseline256/keep_all | 20 | 97 / 119 / 130 | 888 | 15/46 / 5/11 |
| ddr640/current | 16 | 108 / 157 / 190 | 843 | 5/46 / 2/11 |
| ddr640/keep_all | 31 | 364 / 450 / 518 | 960 | 14/46 / 3/11 |

全量去噪后、min-run前 Mask 已保存，帧号对应原视频。容量与几何不是分类准确率；未匹配候选不能标为 invalid。

项目 Python observer 的分区检查不是生产 RTL 分区证明；RTL 分区仍列为接入前门禁。

证据边界：

- One development video, native cadence, replay from frame0; stats120..1079. Not 960 independent samples.
- 32 confirmed frames, 46 ped and 11 vehicle observations from four correlated tracks; moving-only scope.
- Fixed clean masks compare current min-run versus1; area/top4/background history remain fixed.
- Unmatched candidates are UNKNOWN, not invalid. New candidate semantics, FAR/precision and classification are unavailable.
- Independent RLE union_links differ from project union_requests; top4/matching use project rules.
- 3840 external RLE/OpenCV partition checks and128 project Python RLE partition checks do NOT prove production RTL partitions.
- Capacity is unlimited-reference demand, not RTL overflow timing. No deployment capacity is selected from this video.
- No DDR/CDC/display/scheduler, no rollback/recovery experiment, no classifier training and no blind-reserve access.
