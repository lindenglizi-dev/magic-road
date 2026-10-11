# DDR 检测容量首轮诊断

仅软件诊断。固定开发视频从第 0 帧因果回放，统计第 120～1079 帧；不代表硬件时序或识别验收。

| 配置 | 行 run 峰值 | 累计标签峰值 | 容量失败帧/960 | 最长连续失败帧 |
|---|---:|---:|---:|---:|
| baseline256 | 17 | 121 | 833 | 818 |
| ddr640_capacity_observer | 16 | 190 | 843 | 795 |
| ddr640_rollback_on_capacity_failure | 26 | 1189 | 872 | 872 |

32 张人工确认帧的候选召回，IoU≥0.5，一对一、类别无关匹配；尚未经过分类器。

| 配置 | 全部面积合格候选：行人/机动车 | top4：行人/机动车 | 容量失败计漏检后的 top4：行人/机动车 |
|---|---|---|---|
| baseline256 | 12/46 / 3/11 | 11/46 / 3/11 | 1/46 / 0/11 |
| ddr640_capacity_observer | 5/46 / 2/11 | 5/46 / 2/11 | 0/46 / 0/11 |
| ddr640_rollback_on_capacity_failure | 0/46 / 0/11 | 0/46 / 0/11 | 0/46 / 0/11 |

背景回滚配置只模拟容量失败时撤销背景更新；没有自动重建背景，也不能作为正式部署方案。

证据边界：

- One registered development video; 960 workload frames and 32 reviewed frames, four correlated tracks.
- Native video cadence, causal updates from frame zero; not the final 15/20 Hz hardware scheduler.
- Unlimited storage observer; failure is a capacity-demand proxy, not RTL overflow/cycle equivalence.
- Counts include tiny components before area filtering; merged labels are not recycled.
- Rollback variant models capacity-only background cancellation; no DDR, CDC, display or recovery simulation.
- Class-blind proposal recall only; no classifier, FAR, precision or final recognition accuracy claim.
- No parameter sweep, training, blind-reserve access, production RTL or model modification.
