# DDR 目标逐项变化账本

仅报告候选几何与容量代理；以下“匹配”均为类别无关的一对一 IoU≥0.5 几何匹配。

| 配置/阶段 | 新增 | 损失 | 持续匹配 | 持续漏检 |
|---|---:|---:|---:|---:|
| baseline256/before_area | 8 | 1 | 14 | 34 |
| baseline256/area_all | 8 | 1 | 14 | 34 |
| baseline256/top4 | 8 | 2 | 12 | 35 |
| baseline256/capacity_top4 | 0 | 1 | 0 | 56 |
| ddr640/before_area | 12 | 0 | 7 | 38 |
| ddr640/area_all | 12 | 0 | 7 | 38 |
| ddr640/top4 | 11 | 1 | 6 | 39 |
| ddr640/capacity_top4 | 0 | 0 | 0 | 57 |

逐目标四阶段明细见 `target_stage_ledger.csv`；current→keep_all 新增/损失及像素证据见 `target_change_ledger.csv`；完整组件像素重叠图见 `component_overlap_graph.json`。

当前分支 capacity_top4 漏检的 raw/clean/run 最后 IoU≥0.5 匹配阶段：{'none': 72, 'clean': 20, 'run': 21}。

证据边界：

- Geometry proposal ledger only; no classifier or recognition-accuracy measurement.
- One development video, 32 confirmed frames, 57 moving ped/vehicle observations from four correlated tracks.
- Unmatched candidates and targets remain unknown/missed geometry observations, never automatic invalid labels.
- Pixel relations mean connected-component extension or merger only; they do not assert semantic target adhesion.
- Fixed min-run 2/5 versus1, fixed min-area16/100, project area ordering and Hungarian IoU>=0.5 matching; no sweep.
- Replay is causal from source frame0 through1050 with existing background/update/sampling settings.
- Capacity is the existing unlimited-reference demand proxy, not RTL overflow timing.
- No training, model/RTL/config modification, blind-reserve access, DDR/CDC/display or scheduler simulation.
