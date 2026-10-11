# 256 检测线 ROI 失败定位账本

本报告只重整已冻结的逐目标、ROI 和模型分数记录；未解码视频、未重算候选、未训练模型、未改变阈值。

## 定位结果

| 类型 | frame/track | current | keep_all | 结论 |
|---|---|---|---|---|
| Top4 排名损失 | 450/p01 | cc62 rank4, IoU=0.5315, ped, margin=-162060145 | 同一 cc62 rank6, IoU=0.5315, 未进入 Top4 | 组件和框未变，分类前已被更大的组件挤出。 |
| 几何合格但类别翻转 | 360/p01 | cc46 rank3, IoU=0.6434, ped, margin=-94508688 | cc52 rank3, IoU=0.7532, vehicle, margin=31963081 | merged_multiple_old_components 后裁剪与分数改变；float 与量化路径同向翻转。 |
| 几何合格但类别翻转 | 690/p02 | cc41 rank3, IoU=0.5148, ped, margin=-44521448 | cc46 rank3, IoU=0.7507, vehicle, margin=7630269 | merged_multiple_old_components 后裁剪与分数改变；float 与量化路径同向翻转。 |
| 几何合格但类别翻转 | 1050/p02 | cc13 rank1, IoU=0.6771, ped, margin=-252482169 | cc1 rank1, IoU=0.6205, vehicle, margin=57931908 | merged_multiple_old_components 后裁剪与分数改变；float 与量化路径同向翻转。 |

## 工程含义

- `f450/p01` 不能靠分类器修复：目标组件仍满足 IoU≥0.5，但从面积 rank4 降至 rank6，在 ROI 启动前已经丢失。
- `f360/p01`、`f690/p02`、`f1050/p02` 两侧都满足 IoU≥0.5；三例均是多个旧组件连接后的裁剪变化，已有 HOG324 浮点和量化记录都由 ped 变为 vehicle。
- 这些记录不证明哪个视觉结构造成合并，也不支持调阈值、训练新模型或将 keep_all 设为默认。
- 未匹配目标和候选仍是 unknown/missed geometry；没有任何条目被自动标为 invalid。

## 证据边界

这是历史结果重整，不是新增识别准确率证据。`f450/p01` 的 keep_all 分支没有独立保存分类输出；由于账本证明组件、框和像素关系不变，本报告仅引用原 selected crop 的已存分数，并明确标记为非独立记录。

输入文件 SHA-256：

- `evaluation/ddr_architecture/target_change_20261001_v2/target_change_ledger.csv`: `ffa4c160f58049703a1974010931cf40899b1fc7b5d855a6c5ae388fc717b00e`
- `evaluation/ddr_architecture/target_change_20261001_v2/target_stage_ledger.csv`: `05279fbbff54a037ad081ab5fe29b13a2a062db667e5d6fc2ce1fc2eebef9362`
- `evaluation/local_scene_pilots/intersection_2415171_crop_change_v2/all_targets.json`: `e31f1472f2ebac1d59419e4b4a2eecf1227d8b9bda469c45e2627bf5080aa183`
- `evaluation/local_scene_pilots/intersection_2415171_margin_change_v1/score_changes.json`: `6f8dcd246643179f47249bb2a594c69ad9d0a097335473c78f6aab7ffb57aa66`
