# HOG324 真实候选 pilot 决策

状态：继续扩充 HOG324 证据并建立整数参考；模型、拒识阈值、候选接口和生产 RTL 均未冻结。

## 输入边界

- 训练参数来自 360 个已审计真值框 ROI：`000201` 和 `000206`，ped 160、vehicle 200。64 维与 HOG324 分别训练，不迁移权重。
- 候选诊断加载既有参数，不在候选集重训。
- 验证门禁只使用 `split=val` 的 `000200`、`000203`。fill-only 中属于 train 的 `000206` 六组只用于错误分析。
- 70 个既有 CCL 候选与 54 个 fill-only 组分别报告；合并结果仅作描述，不作为正式验收。
- `010106`、`010108_01` blind reserve 未解码、未读取内容；`000205/000207` development holdout 也未用于本轮诊断。

## 人工审核收口

原始 CSV 保持不变，派生表只使用 `review_basis_canonical=human_visual_review`。字面占位日期转为空值，实际 `2026/9/27` 规范化为 `2026-09-27`，另用 `normalized_at` 表示处理时间。

fill-only 共 54 个唯一时间组：19 个 `ped_full`、14 个 `ped_truncated`、21 个 `background_fragment`；24 个裁剪可用、30 个不可用。新增槽位语义目标比例为 33/54=61.1%，达到 60% pilot 门槛；语义目标中可用裁剪为 24/33=72.7%，未达到 80% 门槛，所以候选规则不能冻结。

internal8 共 120 条实质记录，另有 1 条空记录忽略。它仅用于失败类型分析，不进入训练、验证、拒识阈值或正式指标。三条不确定记录排除在指标外，七条背景备注缺失保留为开放审核缺口。

## 预先声明的验证门禁

在两个验证 scene 的 47 个 ped 和 32 个 vehicle 唯一记录上，量化 HOG324 与重训的 64 维参考结果为：

| Scene | 64维 Ped | HOG324-Q Ped | 64维 Vehicle | HOG324-Q Vehicle |
|---|---:|---:|---:|---:|
| `virat-ground-000200` | 28/38 | 37/38 | 16/16 | 16/16 |
| `virat-ground-000203` | 7/9 | 9/9 | 16/16 | 16/16 |
| 合并 | 35/47 | 46/47 | 32/32 | 32/32 |

两个 scene 的行人正确数均未下降且都提高；合并多正确 11 个，超过至少 3 个的门槛；车辆无损失。ped/vehicle balanced accuracy 从 87.23% 提高到 98.94%，增加 11.70 个百分点。因此 pilot 路线门禁通过。

这一结论只表示 HOG324 值得补充数据和整数化。`000203` 只有 9 个行人组，当前只有两个验证 scene，不能据此冻结模型或宣称跨场景稳定。

## 量化与拒识

- 124 个诊断 ROI 上，OpenCV 浮点 HOG324 输出经过 Q1.12 特征和 16 位权重量化后，分类标签不一致为 0。
- 最大归一化分数误差为 0.00172545；全部样本满足逐样本 margin 符号稳定充分条件。
- 这只验证了浮点描述子输出后的量化线性层。梯度、方向桶、空间插值、L2-Hys、舍入和饱和仍未形成整数 HOG 合同，也不是 Python/RTL bit-exact 证据。
- 原始二分类器对 invalid 的误接受率为 100%。对所有结果可变的整数 `abs(score_q)` 阈值扫描后，纯验证合并集、fill-only、70 项 CCL 和描述性合并四种范围均没有同时满足 Person≥85%、Vehicle≥90%、invalid FAR≤10% 的点，因此没有选择阈值。未来阈值选择只允许使用冻结的纯验证集和显式人工 invalid。

## 当前决定

1. 保留 `fill_only_T100` 为 `experiment_roi_contract_v1` 的诊断合同；任何裁剪、阈值、扩框、NMS 或代表帧变化都会使本轮模型指标失效。
2. 补充至少一个未参与规则制定的固定机位验证 scene，并把 ped、vehicle、invalid 各扩展到至少 100 个唯一时间组；参与逐 scene 判断的类别每 scene 至少 20 组。
3. 候选质量先满足新增槽位语义目标≥60%、语义目标可用裁剪≥80%、单 scene 分别≥50%/70%。当前 72.7% 的总体可用裁剪率是直接阻断项。
4. HOG324 继续路线可以并行建立完整整数 Python 参考和资源/周期模型，但拒识问题尚未解决，不能冻结模型接口。
5. 若扩充数据后 HOG324 或整数资源门禁失败，再启动受限 tiny-CNN；当前不训练 tiny-CNN。
6. 生产 RTL、正式顶层和 blind reserve 保持不变。

证据入口：

- [人工审核收据](candidate_reviews/finalized_20260927/receipt.json)
- [实验 ROI 合同](experiment_roi_contract_v1.json)
- [HOG324 v2 报告](../external_reference_exploration/results/opencv_hog_candidate_diagnostic_v2/report.json)
- [严格验证门禁逐 scene 表](../external_reference_exploration/results/opencv_hog_candidate_diagnostic_v2/approved_validation_pilot_gate.csv)
- [整数拒识曲线](../external_reference_exploration/results/opencv_hog_candidate_diagnostic_v2/threshold_scan.csv)
