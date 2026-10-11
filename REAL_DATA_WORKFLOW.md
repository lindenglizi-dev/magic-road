# 真实数据闭环：实施入口与当前状态

2026-09-26：正式 FPGA 顶层、算法 RTL、TD 源清单和时序约束均未修改。

## 当前素材与指标

- 用户要求排除 `video/first`：机位不稳、初始背景抖动。该目录未加入训练集。
- 排除前已完成一个 12 帧诊断回放，结果仅供定位输入与检测行为，不进入模型评估。
- 已取得并核对 6 段官方 VIRAT Ground Release 2.0 视频及配套 object 标注；视频字节数、SHA256、首/中/末帧解码均通过。官方标注中 12 行恰好指向 `frame_index == frame_count`，已原样记录到 `excluded_annotations.csv`，不平移、不钳位。
- VIRAT 使用协议为 `VIRAT Video Dataset Usage Agreement, 1-4-11`。用户已于2026-09-27在本任务中确认接受，收据保存于 `public_data/raw/virat_ground_v2/docs/user_acceptance_receipt.json`；这只记录本项目的本机研究使用状态，不推断再分发权利。
- 独立的 `road_roi_dataset_virat/` 已包含 429 个真值框 ROI：train 360（ped 160、vehicle 200），val 69（ped 45、vehicle 24）；split 字段为 test 的两个 scene 已被查看像素、标签和32×32 ROI以做映射 QA，因此只能算 development holdout。它们没有导入、训练或评分，但不能再作为严格盲测；正式结论需要新增未查看 scene。旧 `road_roi_dataset/` 混合 CDnet、UA-DETRAC mirror 与 VIRAT，只能作为 combined pilot，不能用于 VIRAT-only 正式结论。
- 建议目标：行人 Recall ≥85%，机动车 Recall ≥90%，无效候选误接受率 ≤10%，RTL/定点 Python 分类不一致为0。
- 上述均为**建议目标、未冻结**，见 `evaluation/criteria.pending.json`。机动车暂含汽车、公交、货车；自行车、摩托车、骑行者保留原类别，待定义。
- 这里的分类 Recall 分母是已获得候选框的有效人/车 ROI；端到端 Recall 还包括检测漏检，必须另测，不能混称。

## 公开数据选择

推荐先取得同一类固定机位场景中同时有人和车的标注视频，如 VIRAT 的合适地面序列；CDnet 用于前景压力测试及其独立行人子集，UA-DETRAC 用于补充车辆。

| 来源 | 本项目用途 | 使用边界 |
|---|---|---|
| [CDnet 2014](https://jacarini.dinf.usherbrooke.ca/dataset2014/) | 背景分割、阴影/动态背景压力；单独的行人框子集 | 通用前景掩码不是人/车标签；0/50/85/170/255 的语义不能全部二值化为有效负样本 |
| [UA-DETRAC 原论文](https://arxiv.org/abs/1511.04136) | 车辆框、遮挡与尺度覆盖 | 主要为车辆；不能仅据此训练两类，也不能把未标人群当背景；本次官网访问未成功，不冒认已取得下载许可 |
| [VIRAT](https://viratdata.org/) | 人、车及交互场景；优先固定地面镜头 | 地面数据有使用协议，版本及标注格式需一致；本轮未代替用户接受协议 |
| [AI City 2021](https://www.aicitychallenge.org/2021-data-and-evaluation/) | 后续车辆场景补充 | 各 track 标注不同；Track3 仅标注跨至少两摄像头的车辆，并非画面所有车辆；不能将未标目标作为负例 |
| [Pexels](https://www.pexels.com/license/) / [Pixabay](https://pixabay.com/service/license-summary/) | 固定机位演示和手工标注补充 | 是素材平台；取得视频与逐框语义真值是两件事，保留来源及对应许可 |

选择规则：按摄像机/连续拍摄组隔离 train/val/test，同一原片、裁剪片、转码片不得跨集合。避免“所有行人来自A数据集、所有车辆来自B数据集”的背景捷径。先确认官方许可与可获取性，再只下载少量符合场景的序列。

严格盲测预留已取得全新的 `010106` 与 `010108_01` 两个 scene，共4个配对文件；官方字节数和 SHA-512 全部通过，结果见 `evaluation/public_data/virat_ground_v2/blind_reserve_integrity.json`。额外但未配对的 `010108_02` 视频隔离在 `extra_unpaired/`，不进入数据闭环。在模型、预处理和阈值冻结前，盲测目录只运行以下哈希检查，不解码视频、不解析标注：

```powershell
python tools/verify_blind_reserve.py --root public_data/raw/virat_ground_v2_blind_reserve --request evaluation/public_data/virat_ground_v2/next_download_request.json --output evaluation/public_data/virat_ground_v2/blind_reserve_integrity.json
```

## 工具与命令

以下命令在本工程目录执行。

### 0. VIRAT Release 2.0 转换与隔离导入

```powershell
python tools/convert_virat_ground.py --root public_data/raw/virat_ground_v2 --output evaluation/public_data/virat_ground_v2
python tools/import_virat_rois.py --canonical evaluation/public_data/virat_ground_v2 --dataset road_roi_dataset_virat --output evaluation/public_data/virat_ground_v2/virat_only_import
python tools/audit_roi_dataset.py --dataset road_roi_dataset_virat --output evaluation/public_data/virat_ground_v2/virat_dataset_audit.json
```

`road_roi_dataset_virat` 和 `virat_only_import` 必须是新目录或空目录；导入器遇到已有产物会失败，防止重跑把原审计收据覆盖成“0个导入”。固定 scene split 为 train=`000201,000206`，val=`000200,000203`，development holdout=`000205,000207`。导入器先按轨迹以 30 帧间隔抽稀，再限制每轨迹 12 个、每 scene/class 128 个，避免相邻帧和长轨迹主导样本。type 1→ped，type 2/3→vehicle，type 4/5→ignore；Release 2 README 未定义但文件中出现的 type 0 保留原值并映射为 ignore。

### 1. 准备公开素材

`tools/prepare_public_video.py` 接受视频或图片序列，输出 FFV1 无损720p视频及逐帧映射、哈希、缩放/补边参数。不同于传感器 ISP 等价性，这只是显式、可追溯的输入准备。图片序列必须提供原始 FPS，不插帧。

```powershell
python tools/prepare_public_video.py --input D:/datasets/sequence --output public_clips/sequence_a --dataset-name Example --sequence-id sequence_a --scene-id camera_a --source-url https://example.org/dataset --license-url https://example.org/license --fps 25 --annotations D:/datasets/sequence_a_canonical.csv
```

标注适配为 CSV：`frame_index,xmin,ymin,xmax,ymax,label,original_label,object_id`，0起始帧号、闭区间框。label 显式映射到 ped/vehicle/invalid/ignore；不同数据集的坐标和帧号不能猜测，保留 original_label。

```powershell
python tools/import_public_rois.py --prepared public_clips/sequence_a --dataset road_roi_dataset --split train --stride 10
```

公开标注框记为 `roi_source=annotated`，与 `manual` 和 `ccl` 分开报告。不要把未标区域自动导入 invalid。

### 2. 人工框与无效候选

```powershell
python tools/roi_dataset_tool.py --video public_clips/sequence_a/Example_sequence_a.avi --output road_roi_dataset --split train --scene-id camera_a
```

P=行人，V=机动车，I=无效候选。train/val/test 均支持。同一场景、视频哈希、原片/派生文件族跨集合会被拒绝。老 manifest 缺失来源字段时失败并提示迁移，不静默推断。

### 3. 真实 CCL 框

```powershell
python tools/video_to_gray_frames.py public_clips/sequence_a/Example_sequence_a.avi video_cases/sequence_a --max-frames 60
python tools/measure_existing_sim.py --bench video --frames video_cases/sequence_a --frame-count 60 --output evaluation/measurements/sequence_a
python tools/ccl_roi_candidates.py --frames video_cases/sequence_a --objects evaluation/measurements/sequence_a/objects.csv --output evaluation/candidates/sequence_a --scene-id camera_a --split train
```

检查 candidates.csv 对应的帧和框，填写 label/reviewer 后导入：

```powershell
python tools/ccl_roi_candidates.py --frames video_cases/sequence_a --objects evaluation/measurements/sequence_a/objects.csv --output evaluation/candidates/sequence_a --scene-id camera_a --split train --reviewed evaluation/candidates/sequence_a/candidates.csv --dataset road_roi_dataset
```

工具读取回放灰度 HEX 裁剪，使用源帧映射；保留几何类别作诊断，绝不自动当真值。语义不明者留空待审，粘连多目标记 invalid（本版本单目标分类契约）。

### 4. 诊断拟合、验证集调参、冻结模型、独立测试

指标和 invalid/CCL 样本尚未冻结前，只运行固定 `C=1.0` 的 VIRAT-only 诊断。它不读取 test、不生成 `freeze.json`，也不允许作为 RTL 接入证据：

```powershell
python tools/diagnostic_virat_fit.py --dataset road_roi_dataset_virat --output evaluation/public_data/virat_ground_v2/pilot_fit
```

当前诊断结果：val ped recall=0.60、vehicle recall=1.00，浮点/定点分类不一致为0。两个验证 scene 的行人召回分别为0.571和0.625；按256×144分析框高度分组，`h<=6` 的25个人样本召回仅0.48，`h=7..9` 的14个为0.714，说明极低像素行人是主要瓶颈之一。行人召回明显低于建议目标；该次拟合只使用标注框，没有 invalid 或 CCL 候选，因而它本身不能测拒识或端到端召回。

已对 `VIRAT_S_000201_02_000590_000623` 的前60帧运行现有 RTL 回放并导出真实 CCL 候选：4帧背景学习，后56帧共88个框，所有协议/overflow/core error 标志为0。Python候选参考与RTL的有序 top-4 框坐标及面积为88/88完全一致。EOF→object done 为279–564周期（均值418.82），EOF→Tracker done 为286–577周期（均值430.22）；回放由测试夹具等待完成并插入行空档，这些周期不是连续采集吞吐。88个候选已经完成审核：15 ped、55 vehicle、18 invalid；该窗口属于训练 scene 且连续帧高度相关，没有批量导入训练集。

为节省仿真时间，先用 Python 扫描验证 scene，再选择三个20帧窗口做 RTL：`000200` 源帧608–627得到34个候选（16 vehicle、18 invalid），源帧1840–1859得到16个 ped；`000203` 源帧600–619得到20个候选（4 ped、16 vehicle）。三段 Python/RTL bbox+area 分别为34/34、16/16和20/20完全一致；后两段使用 `--skip-vcd`，只收集候选/轨迹收据，不重复生成大波形，因此没有新增周期证据。第二 scene 中官方标注未覆盖一辆移动作业车和一名被标牌部分遮挡的行人，已通过原始720p上下文图显式人工审核，不能把 annotation-unmatched 自动当 invalid。合并70个验证候选后，当前固定模型 ped recall=55%、vehicle recall=100%、invalid误接受率=100%，浮点/定点分类不一致为0。`abs(score)<T` 只能把已有分类改为invalid，不能纠正9个 ped→vehicle，因此任何该类阈值的行人召回上限仍是55%；当前不得进入RTL分类接入。

Python扩框消融显示统一扩0/2/4/6个分析像素时，ped recall分别为43.75%/43.75%/56.25%/18.75%，vehicle recall均为100%；扩4有所改善但远低于建议目标。扩框会改变所有crop内容，原invalid框还常把真实车辆纳入；这些recall只作敏感性诊断，正式采用前必须重新审核全部扩框样本，不能沿用原标签计算验收指标。再将训练scene中抽稀的9个ped与16个vehicle CCL样本加入诊断拟合，标注框和CCL框召回均未改善（仍为60%和43.75%），说明少量同场景域适配不足，下一轮应优先检查候选框完整性、ROI预处理和特征表达，而不是写RTL。

固定 C=1.0、32×32拉伸和同一 scene split 的纯 Python 特征容量消融进一步表明：现有64维为 annotated/CCL ped recall=60%/55%；64维加4个框几何量为75.56%/75%；横向8格、纵向4格的128维加几何为91.11%/80%；8×8空间网格256维加几何共260维时为91.11%/85%。最后一项的 annotated/CCL vehicle recall 为91.67%/100%。260维在两个 scene 的52个有效 CCL候选上刚好达到建议的候选分类行人目标，但这些是三个短且连续相关窗口，消融未包含 invalid 拒识、定点范围或 RTL 实现，不能据此冻结硬件接口。

更关键的是候选覆盖诊断：两个验证视频均从clip frame 0连续运行背景模型，只在frame 600–899统计官方ped标注；当前部署参数（256×144、阈值20、面积16、top-4）的IoU≥0.1覆盖均为0，分母分别为455和263条相关annotation-frame row。旧的frame600冷启动扫描已在JSON收据中明确标为superseded。逐级统计显示目标框内前景信号大多通过raw/clean/run：`000203` 为454/428/414行，`000200` 为263/263/263行，因此主要问题在组件框、面积排序和top-4预算。`000203` 的目标组件面积中位数6、排名中位数9；top-32加最小6×6框的目标条件诊断可覆盖93.41%，但这不是可直接部署的候选器。`000200` 的最佳组件面积中位数131而IoU中位数仅3.86%，最小框修复也只覆盖33.84%，一次3×3开运算只有9.89%，需要显式处理粘连或错误框形。弱化清理到面积4、top-16虽让`000203`达到86.37%，但300帧固定产生4800候选，在`000200`仍为0。下一步不继续全局参数或形态学盲扫，而是设计固定预算的小组件支路和局部拆分策略，并重新审核其ROI。

固定预算原型现已保留部署面积top-4，并增加4个面积2–15的小组件槽，总预算≤8。`peak_difference`评分在`000203` frame 600–899覆盖278/455条ped标注行（IoU≥0.1为61.10%），在`000200`重遮挡段覆盖89/263（33.84%），在同scene后续可见段frame 1600–1899把部署主支路的163/300提高到274/300（91.33%）。抽样原图表明确有行人响应，但紧框常只含头肩/上身；后续可见段提高到IoU≥0.25时只剩8/300。

现已用另一训练scene `VIRAT_S_000206_07_001501_001600` 的frame 600–1499验证透视阈值，并将四个开发窗口汇总。对ped IoU≥0.25，`y=90/100/110`的逐窗口宏平均分别为36.09%/39.19%/38.90%，逐标注行微平均分别为39.40%/37.90%/36.85%。`y=90`受长scene样本数主导但在`000200`重遮挡窗口明显退化；`y=100`目前只是跨窗口较稳健的折中。由此否定把`y=110`作为通用常量，透视阈值必须按固定摄像机标定并作为可配置参数，尚未冻结。

在新scene和`y=100`下再次比较最终四框：ped IoU≥0.25覆盖为`3主+1小` 2670/10114、`2主+2小` 2294/10114、`内部8再选4` 3797/10114；vehicle覆盖分别为949/4035、547/4035、557/4035，main保留率分别为75.00%/50.00%/58.13%。内部8策略增加ped覆盖，但相对baseline丢失561条原本覆盖的vehicle标注行；3+1更能保留车辆。因此没有一个策略在新scene上同时支配人、车和主支路保留率，`内部8再选4`接口暂不冻结。

随后按“主候选优先、小候选先填空、最多替换一次末位主候选”的受保护仲裁契约，在同一四个开发窗口上扫描24组替换参数，并加入`T90/T100/T110`三组仅填空消融。所有24组替换策略都在`000206`窗口产生vehicle baseline损失，未通过逐窗口vehicle IoU≥0.25和0.5均`lost=0`的开发门禁，因此整个替换族已否决。三组fill-only均通过车辆零损失门禁，main rank0–3全部100%保留。`T90`相对`T100/T110`只有极小开发集差异，且差异来自长训练窗口，不能称为最佳或冻结参数。

领导决策选择区间中点`fill_only_T100`进入人工审核，`T90/T110`只作敏感性对照。T100在四个窗口的ped annotation-row geometry coverage、IoU≥0.25净增分别为`+47/+2/+105/+13`，每窗均不退化；这些数字不是检测召回或分类准确率。完整收据和12份CSV位于`evaluation/python_references/guarded_final4_arbitration_*`。

已从新scene生成120个候选的人工审核批次：90个small、30个main，共10页联系表，位置为`evaluation/candidate_reviews/final4_internal8_000206_f600_1499_y100/`。审核类别固定为`ped_full`、`ped_truncated`、`vehicle`、`merged_target`、`background_fragment`、`other_ignore`。初步目视筛查确认其中同时存在完整或部分人体、多人粘连、车辆局部和路面/背景碎片；VIRAT标注重叠只作提示。`review_manifest.csv`的人工作答字段保持空白，批次状态为`pending_explicit_human_review_training_imported_false`，在逐框签署前不进入训练或分类验收。

新策略的成对审核批次位于`evaluation/candidate_reviews/guarded_fill_only_T100_paired_review/`。579个实际填空候选按固定的帧间隔、原始框IoU、中心距离和最长30源帧跨度规则形成54个唯一时间组，其中45组稳定、9组阈值敏感；目标60组仍缺6组，因此全部54组入审，没有复制相邻帧或放宽规则。每组图显示首/中/末帧、同帧baseline主框、T100最终框、原始/扩框裁剪以及T90/T100/T110状态。54行清单、54张组图和9页联系表已通过独立哈希与字段复核，12个人工字段保持空白且没有导入训练。旧internal8批次不能替代新策略的成对审核证据。

复现实验：

```powershell
python tools/fixed_budget_candidate_prototype.py --video <video.mp4> --annotations evaluation/public_data/virat_ground_v2/annotations.csv --clip-id <clip-id> --start-frame <N> --frames 300 --scorer peak_difference --output evaluation/python_references/<fixed-budget-case>
python tools/sweep_fixed_budget_box_geometry.py --candidate-dir evaluation/python_references/<fixed-budget-case> --output evaluation/python_references/<fixed-budget-case>/box_geometry_sweep.json
python tools/sweep_perspective_threshold_final4.py --video <video.mp4> --annotations evaluation/public_data/virat_ground_v2/annotations.csv --clip-id <clip-id> --start-frame <N> --frames <count> --perspective-y-threshold 90 --perspective-y-threshold 100 --perspective-y-threshold 110 --output evaluation/python_references/<threshold-case>
python tools/summarize_perspective_threshold_sweeps.py --report evaluation/python_references/<case-a>/report.json --report evaluation/python_references/<case-b>/report.json --threshold 90 --threshold 100 --threshold 110 --output evaluation/python_references/<cross-scene-summary>
python tools/prepare_final4_candidate_review.py --candidates evaluation/python_references/<case>/candidates.csv --annotations evaluation/public_data/virat_ground_v2/annotations.csv --output evaluation/candidate_reviews/<review-batch> --sample-size 120
python -B tools/guarded_final4_arbitration.py --output evaluation/python_references --output-prefix guarded_final4_arbitration_
python -B tools/prepare_guarded_fill_review.py --output evaluation/candidate_reviews/guarded_fill_only_T100_paired_review
```

这些报告中的覆盖分母是相关逐帧标注，VIRAT又不是完整背景真值；候选数量只表示处理负载。任何透视阈值都属于固定机位标定，不能直接跨机位复用。

只有 `criteria.json` 明确写入 `"frozen": true`，且所有验收阈值为非空数值后，正式入口才允许验证集调参与生成冻结文件。`freeze.json` 只冻结数据、模型和 ROM 工件；是否通过验收由 metrics 中逐项 criteria 检查给出，不能把“已冻结”解释为“已达标”：

```powershell
python tools/train_hog_svm.py --dataset road_roi_dataset_virat --output experiments/annotated_baseline --phase fit --train-source annotated --criteria evaluation/criteria.frozen.json
python tools/train_hog_svm.py --dataset road_roi_dataset_virat --output experiments/annotated_baseline --phase test
```

真实数据不再允许随机拆分回退。fit 只用训练集拟合标准化/分类器，以同来源验证集的 balanced accuracy 选 C；并列选较小 C。不打开测试集特征调参。上面的 test 命令是未来入口；当前 `000205/000207` 已做映射 QA，只是 development holdout，正式盲测必须换用尚未查看的新 scene。test 要求 manifest、模型、标准、ROM 与对拍向量哈希未变；同一实验拒绝重复 test。

输出：model.json、freeze.json、criteria.json、ROM及对拍向量、val/test_metrics.json、逐样本 predictions.csv、failures.csv。metrics.json 为最近阶段摘要；按 manual/annotated/ccl 分组，缺失组标为 not_measured。

当前二分类基线**没有拒识器**，无效候选会强制落入人/车，误接受率按100%报告。分数不是概率。可用此基线判断问题规模，但不能据此声称满足≤10%的建议目标。实际拒识方法需要验证集证据后另行确定。

### 5. Python 候选链与单任务协议参考

```powershell
python tools/candidate_chain_reference.py --video public_data/raw/virat_ground_v2/video_original/VIRAT_S_000201_02_000590_000623.mp4 --output evaluation/python_references/candidate_chain_virat_000201 --frames 60 --mode deployed
python tools/video_to_gray_frames.py public_data/raw/virat_ground_v2/video_original/VIRAT_S_000201_02_000590_000623.mp4 video_cases/virat_000201_60f --max-frames 60
python tools/measure_existing_sim.py --bench video --frames video_cases/virat_000201_60f --frame-count 60 --output evaluation/measurements/virat_000201_60f
python tools/compare_candidate_reference_rtl.py --python-summary evaluation/python_references/candidate_chain_virat_000201/run_summary.json --rtl-objects evaluation/measurements/virat_000201_60f/objects.csv --output evaluation/python_references/candidate_vs_rtl_virat_000201/report.json
python tools/ccl_roi_candidates.py --frames video_cases/virat_000201_60f --objects evaluation/measurements/virat_000201_60f/objects.csv --output evaluation/candidates/virat_000201_60f --scene-id virat-ground-000201 --split train
python tools/match_ccl_candidates_to_annotations.py --annotations evaluation/public_data/virat_ground_v2/annotations.csv --candidates evaluation/candidates/virat_000201_60f/candidates.csv --frame-manifest video_cases/virat_000201_60f/manifest.json --clip-id VIRAT_S_000201_02_000590_000623 --output evaluation/candidates/virat_000201_60f/annotation_overlap
python tools/single_task_protocol_model.py --output evaluation/python_references/single_task_protocol
python -m unittest tests/test_python_references.py tests/test_road_evaluation.py
```

长视频先运行 `tools/select_candidate_windows.py` 排短窗口；只需候选框一致性时给 `measure_existing_sim.py` 加 `--skip-vcd`。该模式仍编译并运行原视频bench，校验 `events/frame_summary/objects/tracks` 四份非空收据，但明确不产出周期指标。`video_to_gray_frames.py --start-frame N` 用精确零起始帧号，避免秒数换算舍入。

候选参数先在 Python 中扫描，并明确标记非RTL证据。评估中段窗口时必须从clip frame 0预热背景，只统计`--start-frame`之后的行；不带pre-roll的旧参数/分辨率扫描仅保留为冷启动诊断：

```powershell
python tools/candidate_temporal_sweep.py --video <video.mp4> --annotations evaluation/public_data/virat_ground_v2/annotations.csv --clip-id <clip-id> --target-label ped --warmup-start-frame 0 --start-frame 600 --frames 300 --variant 5,20,16,4,1,0,3,2 --output evaluation/python_references/<case>/continuous_candidate_sweep.json
python tools/analyze_candidate_misses.py --video <video.mp4> --annotations evaluation/public_data/virat_ground_v2/annotations.csv --clip-id <clip-id> --target-label ped --warmup-start-frame 0 --start-frame 600 --frames 300 --output evaluation/python_references/<case>/component_miss_analysis.json
```

未匹配官方标注的候选先生成原始分辨率上下文再人工赋类；工具会记录源视频、候选表、frame map和所有输出图哈希：

```powershell
python tools/render_candidate_contexts.py --candidates evaluation/candidates/<case> --frame-map video_cases/<case>/manifest.json --source-video <video.mp4> --output evaluation/candidates/<case>/context_review --slot 1
```

候选链 `deployed` 模式包含实际顶层固定的背景更新（shift 4、冻结前景）、阈值20、3×3清理、最短水平 run=2、8连通、面积16和 top4；它没有建模 MAX_RUN/MAX_LABEL 溢出及逐周期标签合并，不能替代 RTL 回放。单任务协议明确：源端发布后保持 payload/bank 稳定；目的端在请求被接受时复制元数据；最后一次同步 RAM 读数据被捕获后才发 ack；ack 可早于最终分类；空闲的第二个 bank 可以同时采集下一帧，但到该帧 EOF 时旧事务仍未 ack 就整帧丢弃，不增加发布队列；若 ack 与新 EOF 同拍，先释放旧 bank 再发布新任务。下一请求由唯一邮箱事务保持可见直到执行器空闲；匹配包含 transaction、source frame、bank 和 bank generation。名义接口使用32位 frame/transaction/bank-generation；它仍依赖“任何旧 CDC 消息在完整元组回绕前消失”的有界消息寿命，RTL 冻结前必须用复位和最大延迟证明该条件。HDMI 结果先进入 pending；同一 VSYNC 前有多个结果时采用最新完整快照并计数覆盖，只在 VSYNC 原子切换 active，记录生效 HDMI 帧号、源帧号及模回绕差值，然后保持整帧。只有两个帧计数器的复位和帧率关系已经实测对齐时，这个模差值才能解释为物理帧延迟；否则仅保留帧号对。

## 仿真证据与限制

```powershell
python tests/test_road_evaluation.py
python tools/roi_dataset_tool.py --self-test
python tools/measure_existing_sim.py --bench pipeline --output evaluation/measurements/pipeline
```

测量程序保留 source SHA256、命令、日志和压缩波形；观察器只在仿真工程中添加，不编辑正式 RTL。

- 四对象真实 ROI/HOG/SVM 模块串接，RAM为一拍同步模型，权重全1；验证4096像素、256特征、4个分数。不是训练模型测试。
- task→最后结果为4176个100MHz周期，即41.76µs；task→释放为4110周期，释放后66周期最后SVM结果才产生。
- 单元 bank 测试是8×4，并有故意冲突，不能据此计算真实道路丢帧率。
- 回放bench以行空档和完成等待推进，不是按源视频FPS发送SOF，不能把输出周期当成板上FPS。
- 60帧VIRAT回放已给出 EOF→CCL→Tracker 延迟和真实候选框，但测试夹具会等待每帧处理完成；真实连续采集的全尺寸bank占用/等待原因、CDC压力和HDMI延迟仍待后续集成/板上测量，没有把回放耗时冒充这些结果。

## 后续接入检查清单（暂不实施）

统一源帧身份；忙时框表不可覆盖；任务身份与Track槽复用核验；显示pending/active帧边界切换；读请求拥有者输出排空完成；以实测决定单任务读完ack是否足够；取消未论证的N+2超时；CDC复位和数据保持约束；最后才判断是否需要双向邮箱排队。

## 010107 开发验证扩展（2026-09-27）

新增固定机位片段 `VIRAT_S_010107_02_000282_000312` 已通过官方大小/SHA-512、1280×720、479帧、23.97 FPS 与标注边界检查。frame 0、239、478 的目视 QA 显示机位固定且官方框映射正确。该片段通过独立 `split_overlay.json` 记录为 `dev_validation_extension`，没有修改历史 catalog，也没有用于训练或阈值选择。

`tools/run_virat_scene_extension.py` 从 frame 0 单次因果解码，预热120帧（5.006秒），再完整评分 120–478 三个连续区间。baseline 共1127个候选；`fill_only_T100` 共1401个，新增small 274个，所有baseline主候选保留且每帧不超过4个。按同一轨迹至少间隔30个源帧抽出83个代表，生成83张全帧审核图、83个真实32×32 ROI和14页联系表。

首次评分只加载冻结的HOG64/HOG324参数；没有重训、修改C、选择拒识阈值或改变T100。83行人工字段保持空白，完成 `evaluation/scene_extensions/virat_010107_02_t100/review_manifest.csv` 前，本场景不产生准确率、候选质量验收或RTL冻结结论。`candidate_condition` 统一使用 `complete/truncated/merged/background_fragment/other`。完整边界见 `evaluation/scene_extensions/VIRAT_010107_COORDINATOR_REVIEW.md`，最终收据SHA-256为 `b25b7df3d24d051de6a0bad693871314334ad4ccef8aa8bd9e977a09ef261337`。

审计补记：一次用于寻找010107记录的宽范围 `rg` 搜索可能在进程层扫描了旧 blind reserve 的两份 annotation TXT；命令没有输出其内容，MP4也未匹配，但严格“从未读取”声明已经撤销。事件记录在 `evaluation/public_data/virat_ground_v2/blind_reserve_access_events.jsonl`。若正式测试要求OS层从未访问，必须换用新的未访问场景，不能继续称旧reserve为严格blind。

### 010107 人工审核结论（2026-09-28）

用户填写的 `1.csv` 实际是OOXML工作簿。导入器按文件头识别格式，原文件不修改，并验证83个sample ID及36个非人工字段共2,988个单元格与冻结清单语义一致。规范化产物位于 `evaluation/scene_extensions/virat_010107_02_t100_review_v1/`，收据SHA-256为 `f4ed09fe4377ee2a30e303b93b90d383d26733ab0a20f97c286c9dcd9600ebf3`。

审核得到26个ped、53个invalid和4个骑自行车的人，没有vehicle。骑行者保留为 `review_class=ignore, semantic_subtype=rider_bicycle`：计入真实语义目标候选质量，不进入ped/vehicle训练或分类指标，也不计入invalid误接受分母。用户指出多数背景响应来自移动影子或停车线；由于没有逐候选背景子类标签，该信息只作为场景级观察保存。

预声明候选门禁失败：small分支的可训练语义目标为8/30=26.7%，包含骑行者后为9/30=30%，均低于60%；全场景分别为26/83=31.3%和30/83=36.1%，均低于50%。26个ped均标为crop usable，但13个merged、13个truncated，没有完整单目标ROI。HOG64与HOG324-Q分别只正确识别9/26和11/26个ped；53个invalid的二分类原生误接受率均为100%，绝对分数阈值扫描没有满足ped recall≥85%且invalid FAR≤10%的点。车辆为0，因此不能评价车辆召回。

`fill_only_T100` 终止作为待部署候选，保留为失败基线；不继续局部扫T100、不进入RTL、也不立即启动tiny-CNN。下一步先做失败来源定位，再最多测试两种机制明确的Python消融：有符号灰度变化/背景亮度诊断，以及组件短时持续性/形状诊断。每项都必须成对报告去掉的invalid和损失的ped；框或ROI改变后旧标签不得自动继承。

失败来源sidecar随后从frame 0单次因果重放479帧，并对83/83候选完成身份核对。`run/raw>=0.5`和`>=0.75`没有删除任何small；`2-of-3`持续性保留4/8个small ped、3/21个small invalid和0/1个small rider，虽然减少18个invalid，却同时损失一半行人及骑行者，因此两类过滤都被否决为部署规则。main按合同完全不受影响，仍有32个invalid。signed灰度变化在main与small分支的ped/invalid之间方向反转，不能采用统一“暗化即阴影”规则，也没有继续搜索极性阈值。收据位于 `evaluation/scene_extensions/virat_010107_failure_sources_v1/receipt.json`，SHA-256为 `105d8b99cb52e48c49f1b6f5edb6a12132d0edf8349a88447c166bebe7920ad5`。

为把用户的场景级观察转为逐项证据，已生成有限背景子类复核包：invalid按审核时序轨迹去重后，main仅10轨因而全选，small从20轨按正/负差分和持续/短暂四象限固定抽12轨；另加入被`2-of-3`误删的4个small ped和1个rider作为保护对照。共27行真CSV、27张多视图panel和7张联系表。只对22个`background_subtype_target`填写 `shadow/parking_line_related/background_change/other/uncertain`；5个`protection_control`不得填写背景真值。入口为 `evaluation/scene_extensions/virat_010107_background_subtype_review_v1/review_manifest.csv`，收据SHA-256为 `7063429571ca519dd4806879971cbb357c63b2b2f05e0ae5688705e073f54d14`。
