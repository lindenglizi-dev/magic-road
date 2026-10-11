# VIRAT 地面完整帧审核说明

本包只准备开发集人工审核，不含模型预测、训练或评分。`raw_frames/` 是 1280×720
无损原帧；`official_overlays/` 仅叠加 VIRAT source-provided boxes。官方框不是完整背景
真值，不能据此把未框区域当负样本。

## 填写顺序

1. 先锁定 `frame_review_manifest.csv` 的行和图像哈希，不增删或替换抽样帧。
2. 对每帧核完所有可见 person，以及 car/bus/truck/motorcycle/bicycle 五类 vehicle。
3. 骑行者必须分别给 person 框和对应两轮车 vehicle 框，允许重叠，并填写相同
   `rider_pair_id`。无法判定的区域设为 ignore，不猜类别。
4. 对既有官方框在 `source_box_review.csv` 填 `human_box_status`：
   `valid|adjust|relabel|ignore|uncertain`。坐标或类别修订只填 human_* 字段，不改 source 字段。
5. 漏框追加到 `human_additions.csv`；`semantic_class` 取
   `person|car|bus|truck|motorcycle|bicycle|other`，`model_label` 只取
   `ped|vehicle|ignore`。坐标是零起始、闭区间，必须落在 1280×720 内。
6. 确认框、漏标、ignore 和骑行者均核完后，才把帧级五个 `human_*_complete`
   填 `yes`，补 reviewer/reviewed_at。任一不确定则保持空白或填 `no`。

## 接续门禁

人工签署前固定为 `annotation_complete=false`、`training_eligible=false`、
`formal_acceptance=false`。审核完成后应由独立导入器验证 sample_id、图像哈希、坐标、
target_id 唯一性和骑行者成对关系，生成新版本目录；不得覆盖本包，也不得把官方框自动
升级为完整真值。source time group 按同 clip + target_id + label 贪心选择至少 2000 ms
间隔的代表帧；它不是 box-frame row 数，也尚不是人工核实组数。

## 恢复

脚本拒绝覆盖已有目录。中断或校验失败时保留原目录作为失败证据，换一个新的输出目录重跑；
成功包可用 `--verify-existing <目录>` 只读复核全部产物 SHA-256。
