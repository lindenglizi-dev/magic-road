# VIRAT 010107-02 候选人工审核指南

适用批次：`evaluation/scene_extensions/virat_010107_02_t100/`

权威人工输入：`review_manifest.csv`

本指南放在批次目录之外，避免改变原批次的封存产物集合。原始 `receipt.json` 的 SHA-256 仍为：

`b25b7df3d24d051de6a0bad693871314334ad4ccef8aa8bd9e977a09ef261337`

## 1. 三类图片分别做什么

### 1.1 映射抽查图：只检查视频与官方标注是否对齐

文件：

- `mapping_qa/frame_000000_official_annotations.jpg`
- `mapping_qa/frame_000239_official_annotations.jpg`
- `mapping_qa/frame_000478_official_annotations.jpg`
- `mapping_qa/contact_sheet_first_middle_last.jpg`

这组图不是逐候选审核图，也不对应 `review_manifest.csv` 的某一行。它只回答四个问题：

1. 视频和 `.viratdata.objects.txt` 是否属于同一版本；
2. 标注帧号是否从 0 开始且没有前后错一帧；
3. 官方坐标映射回 1280×720 原图时是否发生缩放、偏移或裁剪错误；
4. 这种对齐在视频开头、中间和末尾是否保持一致。

映射图中的颜色含义：

- 绿色：VIRAT 原始类型 1，行人；
- 蓝色：VIRAT 原始类型 2/3，车辆；
- 灰色：当前二分类任务忽略的原始类型；
- `id… t…`：官方对象 ID 与原始类型。

注意：VIRAT 标注并不保证画面内所有可见对象都被标出。因此，“映射图中没有官方框”不能作为 `background_fragment` 或 `invalid` 的依据。

### 1.2 联系表：只用于快速定位样本

文件：`contact_sheets/contact_sheet_01.jpg` 至 `contact_sheet_14.jpg`

- 每页 6 项，按 `review_manifest.csv` 行顺序排列；最后一页不足 6 项；
- 每项标题给出 `sample_id`、帧号和候选分支；
- 联系表适合快速浏览和找到异常项；
- 联系表经过缩小，不能作为遮挡、截断和可用性的最终判断依据。

### 1.3 逐项审核图与 32×32 ROI：填写表格的正式证据

每一行用两个文件：

- `review_frame_path`：带上下文的 1280×720 审核图；
- `roi_32x32_path`：分类器实际收到的 32×32 灰度 ROI。

审核图中的颜色含义：

- 黄色 `SELECT` 外框：当前 CSV 行真正要审核的候选；
- 左下黄色边框 `SELECTED 32x32 ROI`：当前候选实际缩放后的分类输入；
- 蓝色 `B0`～`B3`：同一帧的基线 main4 候选，只用于判断是否重复、是否新增目标；
- 绿色 `F0`～`F3`：T100 最终输出中的主候选；
- 品红色 `F0`～`F3`：T100 为补足空槽而加入的小候选；
- 橙色细框：形态学连通域的原始范围，只用于理解扩框前后的关系。

同一候选可能同时显示蓝框、绿框和黄色外圈，这是多种策略选择了同一个区域，不是三个人工审核对象。每一行始终只审核黄色 `SELECT` 对应的一个候选。

映射图与审核图的蓝色含义不同：映射图蓝色是官方车辆标注；审核图蓝色是基线候选 `B#`。

## 2. 图片是如何选取的

### 2.1 映射抽查图的选取方式

视频共 479 帧，帧号为 0～478。脚本固定选择：

- 首帧：`0`；
- 中间帧：`frame_count // 2 = 239`；
- 末帧：`frame_count - 1 = 478`。

这三帧是确定性选择，不是随机抽样，也不是按人车数量挑选。选择它们是为了以最低人工成本发现贯穿视频的帧号错位和坐标映射错误。它们不能证明其余 476 帧全部无误；若三张中任一张整体错位，应停止候选审核并先修复映射。

### 2.2 83 个候选审核项的选取方式

脚本从第 0 帧开始连续解码一次，背景模型不在三个统计区间之间重置。前 5 秒作为预热，因此候选审核从第 120 帧开始。审核区间为：

- `interval_1`：120～239；
- `interval_2`：240～359；
- `interval_3`：360～478。

每帧最多保留 4 个 `fill_only_T100` 最终候选。为了避免把同一目标的相邻帧重复交给人工审核，脚本先给候选分配时间轨迹：

1. 若候选与当帧官方人车框的 IoU ≥ 0.1，则使用官方对象 ID 形成轨迹；
2. 否则使用短时几何关联：与前一轨迹相隔不超过 5 个源视频帧、IoU ≥ 0.3，且中心点在 256×144 分析坐标中每个方向相差不超过 3 像素；
3. 对每条轨迹选第一次出现的候选；之后只有距离上一次已选代表至少 30 个源视频帧时才再选一次。

最终得到 83 项：53 个主候选、30 个补槽小候选。它们按处理和发现顺序写入 CSV，并未按 `ped/vehicle/invalid` 平衡，也没有依据 HOG64/HOG324 的预测或分数挑选。

官方标注只参与轨迹关联和生成 `annotation_hint_*`。这些提示不是人工真值；没有提示也不等于背景。

## 3. 每一行的固定审核流程

1. 在联系表中找到 `sample_id`，只用于快速定位。
2. 打开该行 `review_frame_path`，找到黄色 `SELECT`。
3. 观察黄色框内的内容和周围完整画面，判断目标身份、遮挡来源和裁剪边界。
4. 打开该行 `roi_32x32_path`，或看审核图左下角的最近邻放大图。判断分类器实际输入是否仍保留足够类别信息。
5. 只有判断 `same_frame_new_target` 和 `duplicate_of_baseline` 时，才比较蓝色 `B#`。
6. 不根据绿色／品红色框外的其他人车填写当前行，也不根据 HOG 预测反推人工类别。
7. 按下列顺序填写 12 个人工字段。所有自动生成字段保持不变。

## 4. 按 CSV 顺序填写人工字段

### 4.1 `review_class`

允许值：`ped`、`vehicle`、`invalid`、`ignore`

判断对象是黄色 `SELECT` 对应的实际 32×32 ROI：

- `ped`：ROI 中具有足够行人结构，可以明确判断为人；
- `vehicle`：ROI 中具有足够汽车、公交或货车结构，可以明确判断为机动车；
- `invalid`：没有足够的人或车类别信息，例如纯背景、停车线、阴影、单独车轮、单独腿部、极小模糊碎片；
- `ignore`：画面中有真实目标，但不属于当前稳定的二分类口径或无法给出唯一类别，例如自行车、摩托车、骑行者，或人车同时占据主要区域且无法确定主类。

多人粘在同一框内但都属于人，可填 `ped`，同时把 `candidate_condition` 填为 `merged`。多辆车同理。若人与车都占据显著区域且无法给唯一真值，填 `ignore + merged`。

不要因为全帧附近存在人或车就填 `ped/vehicle`。目标必须实际进入黄色候选，并在 32×32 ROI 中留下足够类别信息。

### 4.2 `candidate_condition`

允许值：`complete`、`truncated`、`merged`、`background_fragment`、`other`

- `complete`：一个主要目标约 90% 以上位于黄色候选内，关键结构未被候选边界切断；
- `truncated`：目标存在，但黄色候选切掉明显部分。缺头、只剩躯干、只剩腿、只剩车轮均属于此项；
- `merged`：黄色候选中有两个或更多有意义目标，或人车被连成一个候选；“人在车旁边”本身不算 merged，只有两者都实际进入候选且共同影响 ROI 才算；
- `background_fragment`：候选主要是停车线、树影、路面、建筑边缘等背景变化，没有可审核的人车目标；
- `other`：以上四项都不合适，例如范围内只有任务外类别，或图像质量导致无法确定候选性质。

若同时“截断且粘连”，优先填 `merged`，并在 `review_note` 说明哪个目标被截断。

### 4.3 `crop_usable`

允许值：`yes`、`no`、`uncertain`

此字段只回答：“把全帧上下文拿掉后，这张 32×32 ROI 是否仍足以支持当前 `review_class`？”

- `yes`：从 32×32 ROI 本身能稳定看出类别；
- `no`：必须依赖全帧位置或附近目标才能猜，或只剩孤立部件、纯背景、严重混合；
- `uncertain`：在 32×32 中勉强可见，但无法稳定判断。

统一下限：候选保留的目标范围粗略少于完整目标的 60%，原则上填 `no`；60%～90% 再依据类别结构判断；达到 90% 左右且结构清楚通常填 `yes`。比例只作肉眼分档，不要求逐像素测量。

结构规则：

- 行人缺头但保留躯干和双腿的整体轮廓，可以是 `yes`；
- 只有腿、只有头或一条肢体，填 `no`；
- 车辆需保留车身主体，并至少能看到车顶／车厢／前后轮廓中的两个结构线索；只有车轮、保险杠或一小段车身填 `no`；
- `review_class=invalid` 时通常填 `no`；
- `review_class=ignore` 时，若任务外目标本身清晰可辨可以填 `yes`，否则填 `no/uncertain`。

### 4.4 `occlusion`

允许值：`none`、`partial`、`heavy`、`uncertain`

遮挡是指目标被车、其他人、树、柱子等场景物体挡住；黄色框裁掉目标不叫遮挡。

- `none`：被遮挡部分约 0%～10%；
- `partial`：被遮挡部分约大于 10% 且不超过 50%；
- `heavy`：被遮挡部分大于 50%；
- `uncertain`：无法区分目标本来就只有这些像素，还是被场景物体挡住。

人在车前面且身体完整可见，填 `none`。人在车后面、腿被车挡住，按被挡比例填 `partial` 或 `heavy`。如果黄色框只截到脚，但全帧中的人没有被别的物体遮挡，应填 `none`，截断由后面的 `truncation_reason` 表示。

对纯背景 `invalid + background_fragment`，填 `none`。

### 4.5 `truncation_reason`

允许值：`none`、`crop_tight`、`frame_edge`、`uncertain`

- `none`：黄色候选没有切掉目标；纯背景项也填 `none`；
- `crop_tight`：目标在原始全帧中存在，但黄色候选边界过紧而切掉目标；
- `frame_edge`：目标本身越过 1280×720 原视频边缘，缺失部分无法从该帧取得；
- `uncertain`：无法判断缺失来自候选裁剪还是真实遮挡／模糊。

通常 `candidate_condition=truncated` 时本字段不能填 `none`。若目标既在源帧边缘又被候选进一步裁紧，填 `frame_edge`，并在备注写明还存在 `crop_tight`。

### 4.6 `same_frame_new_target`

允许值：`yes`、`no`、`uncertain`

这个字段比较当前黄色候选与同一帧所有蓝色 `B#`：

- `yes`：黄色候选提供了一个蓝色基线候选都没有提供的、可用的新目标；
- `no`：它是背景／无效碎片，或目标已经被某个蓝色 `B#` 表示；
- `uncertain`：无法确认蓝框中是否已经包含同一目标的可用类别信息。

“框相交”不等于重复。例：一个蓝色大框主要表示汽车，黄色小框表示站在车旁或车前的人；即使两框相交，只要蓝框不能提供可用的行人 ROI，黄色行人仍可填 `yes`。

若当前行为 `branch=main_area_topk` 且黄色框与某个蓝色 `B#` 是同一矩形，它按构造不是新目标，填 `no`。

### 4.7 `duplicate_of_baseline`

允许值：`yes`、`no`、`uncertain`

- `yes`：当前黄色候选与某个蓝色 `B#` 表示同一个现实目标；
- `no`：没有蓝色 `B#` 表示这个目标；
- `uncertain`：目标太小、粘连或遮挡，无法确认是否为同一现实目标。

优先依据同一目标身份判断，不按框是否接触判断。黄色框只截到某辆车的车轮，而蓝框包含该车，仍是同一现实目标，可填 `yes`；此时可以同时填写 `review_class=invalid`、`crop_usable=no`。

`branch=main_area_topk` 的候选由基线保留而来，通常应填 `yes`，并选择与黄色框重合的蓝色编号。

### 4.8 `duplicate_baseline_number`

只在 `duplicate_of_baseline=yes` 时填写：`B0`、`B1`、`B2` 或 `B3`。

- 填审核图上实际印出的蓝色编号；
- 当前批次使用 `B#`，不是旧审核图中的 `M#`；
- 若多个蓝框都覆盖该目标，填对同一目标表达最直接、范围最接近的一个；
- `duplicate_of_baseline=no` 或 `uncertain` 时留空，并在 uncertain 情况下写备注。

### 4.9 `reviewer`

填写审核人可追溯名称，例如姓名、固定缩写或账号。整个批次保持同一种写法。

### 4.10 `reviewed_at`

填写审核日期，格式固定为 `YYYY-MM-DD`，例如 `2026-09-28`。

### 4.11 `review_basis`

本批次统一填写：`human_visual_review`

不要填写模型名或 `annotation_hint`，因为最终标签来自人工查看审核图与实际 32×32 ROI。

### 4.12 `review_note`

用短句记录判断依据。以下情况必须填写：

- `review_class=invalid` 或 `ignore`；
- `candidate_condition` 不是 `complete`；
- `crop_usable=no/uncertain`；
- `occlusion=heavy/uncertain`；
- `truncation_reason` 不是 `none`；
- 任一新增／重复字段为 `uncertain`；
- 人车同时进入候选，或多个同类目标粘连。

推荐格式：`可见内容；不可用或歧义原因；与 B# 的关系`。

示例：

- `only pedestrian legs remain after crop; no stable 32x32 person structure`
- `parking-line fragment only; no visible target`
- `pedestrian and vehicle both dominate ROI; mixed-class merged candidate`
- `same vehicle as B2; selected crop contains wheel only`

## 5. 常见组合

| 情况 | review_class | candidate_condition | crop_usable | occlusion | truncation_reason |
|---|---|---|---|---|---|
| 人体基本完整，结构清楚 | ped | complete | yes | none/partial | none |
| 缺头但躯干和腿完整可辨 | ped | truncated | yes | none | crop_tight |
| 只截到人的腿 | invalid | truncated | no | none | crop_tight |
| 车辆只剩单个车轮 | invalid | truncated | no | none | crop_tight |
| 停车线或路面变化 | invalid | background_fragment | no | none | none |
| 两个人落入一个框，仍明显都是人 | ped | merged | 视 ROI 而定 | 视场景而定 | none/crop_tight |
| 人和车共同占据主要区域，无法给唯一类别 | ignore | merged | no | 视场景而定 | none/crop_tight |
| 自行车／摩托车／骑行者 | ignore | other | 视清晰度而定 | 视场景而定 | none/crop_tight |

## 6. 提交前逐行检查

- 每行只判断黄色 `SELECT`，没有把其他绿框、品红框或蓝框当成当前审核对象；
- `review_class` 来自人眼判断，没有照抄 `hog64_prediction`、`hog324_*_prediction` 或 `annotation_hint_label`；
- `crop_usable` 已查看实际 `roi_32x32_path`，没有只看全帧；
- 遮挡与裁剪分开：场景物体挡住写 `occlusion`，黄色边界切掉写 `truncation_reason`；
- `duplicate_of_baseline=yes` 时填写了 `B#`；其他情况该编号为空；
- `reviewer`、`reviewed_at`、`review_basis` 均已填写；
- 必须备注的异常项已有简短依据；
- 未改动自动生成列、路径、哈希和模型诊断列。

完成后再运行一致性检查和统计。不得根据统计结果回头改变本指南中的人工门槛，也不得依据模型预测修改人工标签。
