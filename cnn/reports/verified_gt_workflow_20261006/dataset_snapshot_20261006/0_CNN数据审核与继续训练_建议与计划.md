# CNN 数据审核与继续训练建议及计划

## 第一部分：建议

### 1. 当前阶段的核心目标

当前阶段不应优先继续扩大数据下载规模，而应先把现有数据中的标签从“已有标签 / 官方来源框”升级为可以正式用于训练和评估的 **人工审核真值（Verified GT）**。

建议当前工作的优先级调整为：

> 冻结标注规则 → AI辅助找疑点 → 人工逐图审核 → AI二次查漏 → 冻结Verified GT → CNN小规模训练 → 错误分析 → 再决定是否扩展数据。

其中最重要的原则是：

> **AI负责尽可能发现疑点，人负责最终确认。**

AI可以提示“这里可能漏了一个人”“这里可能有一辆静止车辆”“这个框可能过大”，但AI不能直接把这些候选自动写入最终真值。

---

### 2. 数据建议划分为四个独立数据桶

建议把当前数据明确划分为以下四类，避免后续训练、验证和压力测试相互混淆。

| 数据桶 | 用途 | 是否进入正式训练 |
|---|---|---|
| 128张训练审核帧 | 建立正式训练真值 | 审核完成后进入 |
| 原有道路地面审核图 | 道路场景开发与跨机位验证 | 以开发/验证为主 |
| 新增24张VIRAT庭院帧 | 行人、背景、远距离压力测试 | 可作为辅助训练桶 |
| Blind / 盲测预留 | 最终独立测试 | 不进入训练 |

新增24张VIRAT庭院帧可以保留为：

```text
person_background_aux
```

它们不应被用于宣称已经拥有第三个道路机位，也不建议与道路验证集混在一起只报告一个总AP。

最终建议至少分别记录：

```text
Road-camera validation
Courtyard/person stress test
Cross-camera road validation
Blind test
```

---

### 3. 先冻结标注规则，再开始人工审核

在开始正式人工审核之前，建议先建立：

```text
annotation_policy_v1.md
```

必须明确以下规则。

#### 3.1 Person

- 完整可见的人：标记为 `person`
- 部分遮挡但可明确判断为人：标记为 `person`
- 遮挡严重、无法可靠判断人体范围：标记为 `ignore`
- 目标极小、只有几个像素且无法确认：标记为 `ignore`

#### 3.2 Rider / 骑行者

如果最终分类只包含：

```text
person
vehicle
```

则必须明确骑行者中的人是否独立标为 `person`。

推荐规则：

```text
骑行者人体 -> person
自行车/摩托车 -> 按vehicle定义决定是否标vehicle
```

如果 `vehicle` 包含：

```text
car / bus / truck / motorcycle / bicycle
```

则骑行场景应同时存在：

```text
person box
vehicle box
```

如果 `vehicle` 只定义为：

```text
car / bus / truck
```

则自行车不应在部分图片中标vehicle、部分图片中又不标。

一致性比少量漏框更重要。

---

### 4. AI应作为“审核助手”，而不是自动标注器

推荐结构：

```text
原图
 │
 ├──────────────> 当前GT / 官方标签
 │
 └──────────────> Teacher CNN预测
                         │
                         ▼
                  与GT进行差异比较
                         │
                         ▼
                  生成疑似问题列表
                         │
                         ▼
                     人工审核
                         │
              ┌──────────┴──────────┐
              ▼                     ▼
           确认补标                ignore
              │
              └──────────┬──────────┘
                         ▼
                   Verified GT
```

Teacher模型的作用是：

> 尽量把人容易忽略的区域找出来。

而不是：

> 自动生成最终训练标签。

---

### 5. Teacher审核模式建议使用低置信度阈值

正式推理时可能使用：

```text
conf = 0.4
```

但审核模式应适当降低，例如初始可尝试：

```text
conf = 0.10 ~ 0.15
NMS IoU ≈ 0.6
```

这里的目标不是获得漂亮的Precision，而是提高：

> **疑似漏标签候选的召回率。**

例如一个 `confidence=0.18` 的远处person，在正式检测中可能会被过滤，但在人工审核中非常有价值。

---

### 6. 自动生成四种主要疑点

Teacher预测和当前GT之间进行IoU和类别匹配后，可生成以下四类审核任务。

#### 6.1 疑似漏标

```text
Teacher有目标
GT没有对应目标
```

属于最高优先级。

#### 6.2 疑似错误标签

```text
GT有目标
Teacher完全没有对应响应
```

不能自动删除，只标记为：

```text
CHECK_GT
```

#### 6.3 疑似框范围错误

Teacher与GT类别一致，但框范围差异明显，例如：

```text
CHECK_BOX
```

#### 6.4 类别冲突

例如：

```text
GT      = person
Teacher = vehicle
```

进入：

```text
CHECK_CLASS
```

IoU阈值只作为排序和辅助审核标准，不作为最终真值判断依据。

---

### 7. 增加与CNN无关的几何检查

一些标签错误无需依赖AI，可以程序自动检查：

```text
x1 < 0
y1 < 0
x2 > image_width
y2 > image_height
x2 <= x1
y2 <= y1
```

还应检查：

- 极小异常框
- 极大异常框
- 高重合重复框
- 越界框
- 空框
- 类别ID非法
- 图片与标签尺寸不一致

例如：

```text
same class
IoU > 0.9
```

可标记为：

```text
duplicate_warning
```

---

### 8. 人工审核不要简单按文件顺序进行

建议给每一张图片生成：

```text
review_score
```

例如：

```text
S =
3 × unmatched_prediction
+ 2 × boundary_warning
+ 2 × class_conflict
+ 1 × small_object_warning
```

优先审核高风险图片。

但是：

> **全部128张最终仍需人工看完。**

AI排序的作用只是决定：

> 先看哪一张。

而不是决定：

> 哪些图片可以跳过。

---

### 9. 人工审核界面建议固定显示三种视图

每张图片至少同时准备：

```text
1. RAW
2. GT Overlay
3. GT + Teacher + Suspicious Overlay
```

建议布局：

```text
┌────────────────────┐
│       RAW          │
│      原始图片       │
└────────────────────┘

┌────────────────────┐
│       GT           │
│      当前标签       │
└────────────────────┘

┌────────────────────┐
│   GT + Teacher     │
│     AI疑点叠图      │
└────────────────────┘
```

其中RAW原图必须单独查看一次。

原因是如果人工一直看已有框，很容易产生“这些区域应该已经检查过”的视觉暗示，从而忽略漏标目标。

---

### 10. 人工审核操作建议固定为五类

审核不要全部采用自由文本记录。

推荐统一为：

```text
A = ACCEPT
M = MODIFY_BOX
N = NEW_LABEL
I = IGNORE
D = DELETE_WRONG_LABEL
```

审核日志示例：

```csv
image_id,target_id,action,class,reason
frame001,p03,A,person,ok
frame001,p07,M,person,box_too_large
frame001,new01,N,vehicle,missed_parked_car
frame001,new02,I,person,too_occluded
```

这样后续可以直接统计：

- 新增了多少person
- 新增了多少vehicle
- 修改了多少框
- 删除了多少错误标签
- 有多少目标进入ignore
- 有多少问题来自静止车辆
- 有多少问题来自骑行者
- 有多少问题来自远处小目标

---

### 11. 少量漏标签的处理原则

#### 11.1 明确可确认的漏标签

如果人工确认目标确实存在，应：

> **直接人工补为正式GT。**

例如原标签：

```text
person = 3
vehicle = 2
```

审核后发现远处还有一个person：

```text
person = 4
vehicle = 2
```

不建议因为数量少就继续保留错误标签。

#### 11.2 不直接采用Teacher的框

正确流程应为：

```text
Teacher提出候选
    ↓
人工查看RAW原图
    ↓
确认目标存在
    ↓
人工调整bbox
    ↓
保存为Verified GT
```

建议在数据来源中记录：

```json
{
  "source": "manual_review",
  "ai_assisted": true,
  "verified": true
}
```

不要把这种人工确认后的标签称为：

```text
pseudo_label
```

#### 11.3 无法确认的目标

例如远处只有几像素：

```text
Teacher: person 0.21
```

人工又无法确定其是否真的是人，则不要强行标：

```text
person
```

建议设为：

```text
IGNORE
```

因为：

- 错误标成person会形成错误正监督；
- 当作background可能形成错误负监督；
- ignore最稳妥。

---

### 12. 静止车辆必须作为专项检查项

道路视频数据中常见的问题是：

```text
moving car  -> 有标签
parked car  -> 没有标签
```

如果你的任务要求检测“画面中所有车辆”，而原始数据只倾向于标活动目标，那么CNN将收到矛盾监督：

```text
一辆车 = vehicle
旁边停着的车 = background
```

因此建议道路图片全部增加：

```text
parked_vehicle_check = true
```

并且人工确认：

> 画面中的全部可见静止车辆是否都符合你的vehicle定义。

---

### 13. 发现系统性漏标时，不应继续零散修补

如果审核128张后发现：

```text
person漏标 = 5
vehicle漏标 = 4
```

而且类型分散，可视为零散漏标。

但如果发现：

```text
vehicle漏标 = 43
其中39个都是parked vehicle
```

则说明问题不是随机漏标，而是：

> **原标签体系与当前任务定义不一致。**

此时应重新扫描所有vehicle场景。

同理，如果骑行者中的person普遍没有单独标注，则应重新检查全部rider样本，而不能只修Teacher找到的几个。

---

### 14. 建议保留标签版本和修改记录

不要覆盖原标签。

推荐：

```text
labels_v1_original/
labels_v2_verified/
annotation_patch.json
```

示例：

```json
{
  "frame_037": {
    "add": [
      {
        "class": "person",
        "bbox": [421, 205, 447, 289],
        "reason": "missed_small_person"
      }
    ]
  }
}
```

然后由程序生成：

```text
labels_verified/
```

最终形成：

```text
原始标签
   ↓
审核修改记录
   ↓
Verified GT
```

这对后续复现、比赛答辩和错误追踪非常有价值。

---

### 15. 人工审核后应再跑一次AI查漏

推荐流程：

```text
第一次Teacher审核
        ↓
人工补漏
        ↓
GT v2
        ↓
第二次Teacher审核
        ↓
重新比较mismatch
```

如果第二轮仍存在大量：

```text
unmatched_predictions
```

则说明人工审核可能仍然存在系统性遗漏，应继续检查。

---

### 16. 建议建立审核统计表

最终至少记录：

| 项目 | 数量 |
|---|---:|
| Images reviewed | 128 |
| Person original | - |
| Person added | - |
| Person modified | - |
| Vehicle original | - |
| Vehicle added | - |
| Vehicle modified | - |
| Ignore added | - |
| Duplicate removed | - |
| Rider cases | - |
| Parked vehicle cases | - |
| AI suggestions checked | - |
| AI suggestions accepted | - |

还可以计算：

```text
AI suggestion precision
```

例如：

```text
AI提出36个疑似漏标
人工确认14个

14 / 36 = 38.9%
```

这里不需要追求AI建议Precision很高。

真正重要的是：

> AI不要漏掉太多真正的漏标签。

---

### 17. 正式CNN训练建议从小实验开始

人工真值审核完成后，不建议立刻直接做大规模训练。

#### Round 0：冻结真值

生成：

```text
GT_verified_v1
```

并记录：

- 文件列表
- 标签数量
- SHA哈希
- 数据划分
- 标注规则版本

#### Round 1：Smoke Test

只训练：

```text
1 ~ 3 epoch
```

用于检查：

- 数据能否正常加载
- bbox格式是否正确
- loss是否正常下降
- 类别是否颠倒
- 是否存在NaN
- resize / augmentation是否错误

这一步不用于评价最终AP。

#### Round 2：Baseline

完成正式基线训练，至少记录：

```text
Precision
Recall
mAP50
mAP50-95
per-class AP
```

#### Round 3：辅助庭院数据对照

建立：

```text
A: road only
B: road + courtyard person auxiliary
```

重点比较：

```text
person recall
false positive
road AP
```

如果庭院数据加入后：

```text
person recall ↑
road AP不下降
```

才考虑保留进入正式训练。

否则24张庭院素材保留为：

```text
stress test
```

而不是训练数据。

---

### 18. Teacher 256张覆盖实验应放在人工真值门禁之后

推荐顺序：

```text
128 train人工审核
        ↓
Verified GT v1
        ↓
基础CNN训练
        ↓
Teacher 256 train覆盖检查
        ↓
错误类型统计
        ↓
决定是否扩大数据
        ↓
S / D两组训练对照
```

不建议：

```text
Teacher 256
    ↓
自动补标签
    ↓
直接训练
```

---

## 第二部分：计划步骤

### 阶段0：冻结数据和标注规则

#### Step 0.1 建立当前数据快照

记录：

```text
dataset_snapshot_YYYYMMDD/
```

内容包括：

- 128张训练审核帧
- 原始标签
- 道路审核图
- 新增24张VIRAT庭院图
- blind测试预留清单
- 数据来源信息
- SHA哈希

要求：

> 后续所有修改都生成新版本，不直接覆盖原始数据。

---

#### Step 0.2 编写标注规范

新建：

```text
annotation_policy_v1.md
```

明确：

- person定义
- vehicle定义
- rider处理
- parked vehicle处理
- 遮挡目标处理
- 小目标处理
- ignore标准
- bbox边界标准

完成后才能进入正式审核。

---

### 阶段1：建立审核工程

建议目录：

```text
dataset_review/
├── images/
├── labels_original/
├── teacher_predictions/
├── overlays_original/
├── overlays_teacher/
├── overlays_compare/
├── review_queue/
├── patches/
├── labels_verified/
│
├── annotation_policy_v1.md
├── review_manifest.json
├── audit_log.csv
└── review_summary.json
```

每张图片使用唯一ID，例如：

```text
VIRAT_S_010001_00_000019_000065_f000120
```

不建议使用：

```text
001.jpg
002.jpg
```

---

### 阶段2：生成审核清单

编写：

```text
01_build_review_manifest.py
```

功能：

1. 扫描全部待审核图片；
2. 检查图片是否存在；
3. 检查标签是否存在；
4. 记录图片尺寸；
5. 记录来源视频；
6. 记录帧号；
7. 记录camera / scene；
8. 记录train / dev / blind属性；
9. 建立唯一image_id；
10. 输出：

```text
review_manifest.json
```

---

### 阶段3：运行Teacher审核模式

编写：

```text
02_run_teacher_review.py
```

Teacher使用低置信度：

```text
conf = 0.10 ~ 0.15
NMS IoU ≈ 0.6
```

输出：

```text
teacher_predictions/
```

要求保存：

- bbox
- class
- confidence
- image_id
- model version
- inference config

不能直接修改GT。

---

### 阶段4：比较Teacher与GT

编写：

```text
03_match_teacher_gt.py
```

为每一个预测寻找同类GT。

建议生成：

```text
MATCHED
UNMATCHED_PRED
UNMATCHED_GT
CHECK_BOX
CHECK_CLASS
```

例如：

```text
IoU > 0.5
    -> matched

0.2 < IoU <= 0.5
    -> CHECK_BOX

IoU <= 0.2
    -> UNMATCHED_PRED
```

具体阈值只作为审核提示，可根据后续实验调整。

---

### 阶段5：运行标签几何检查

编写：

```text
04_validate_annotation_geometry.py
```

检查：

- bbox越界
- bbox宽高<=0
- 极小框
- 极大框
- 重复框
- 类别非法
- 图片/标签不对应
- 坐标格式错误

输出：

```text
geometry_warning.json
```

---

### 阶段6：建立风险排序

编写：

```text
05_rank_suspicious_frames.py
```

例如：

```text
review_score =
3 × unmatched_prediction
+ 2 × boundary_warning
+ 2 × class_conflict
+ 1 × small_object_warning
```

输出：

```text
review_queue/
    0001_highest_risk.json
    0002.json
    ...
```

高风险先审，但128张必须最终全部完成。

---

### 阶段7：生成审核叠图

编写：

```text
06_make_review_overlays.py
```

每张图片生成：

```text
RAW
GT
Teacher
GT + Teacher + Suspicious
```

建议视觉上区分：

```text
GT
Teacher prediction
unmatched prediction
class conflict
boundary warning
```

同时保证RAW原图不带框。

---

### 阶段8：进行人工审核

每张图片执行：

#### 8.1 先看RAW

检查全部可见：

```text
person
vehicle
rider
parked vehicle
small object
occluded object
```

#### 8.2 再看GT

检查：

- 是否漏标
- 是否错标
- 框范围
- 类别
- 重复框

#### 8.3 再看AI疑点

检查Teacher提出的：

```text
UNMATCHED_PRED
CHECK_BOX
CHECK_CLASS
```

#### 8.4 记录人工决策

仅使用：

```text
A = ACCEPT
M = MODIFY_BOX
N = NEW_LABEL
I = IGNORE
D = DELETE_WRONG_LABEL
```

写入：

```text
audit_log.csv
```

---

### 阶段9：专项复查三类高风险目标

全部128张审核完成后，再针对以下三类进行专项扫描。

#### 9.1 Parked Vehicle

检查所有道路图片中的静止车辆。

#### 9.2 Rider

检查所有骑行者：

```text
person是否独立标注
vehicle是否符合统一定义
```

#### 9.3 Small / Distant Object

集中检查：

```text
远处行人
远处车辆
遮挡目标
边缘目标
```

如果发现某一类出现系统性漏标：

> 重新扫描该类别相关的全部样本，而不是只修已发现图片。

---

### 阶段10：生成标签补丁

人工修改不直接覆盖原始标签。

生成：

```text
annotation_patch.json
```

例如：

```json
{
  "frame_037": {
    "add": [
      {
        "class": "person",
        "bbox": [421, 205, 447, 289],
        "reason": "missed_small_person"
      }
    ]
  }
}
```

---

### 阶段11：应用补丁并生成Verified GT

编写：

```text
07_apply_annotation_patch.py
```

输入：

```text
labels_original/
annotation_patch.json
```

输出：

```text
labels_verified/
```

保留完整：

```text
Original
Patch
Verified
```

三层关系。

---

### 阶段12：再次运行Teacher查漏

重新执行：

```text
02_run_teacher_review.py
03_match_teacher_gt.py
```

但这次比较：

```text
Teacher
vs
Verified GT
```

观察：

```text
UNMATCHED_PRED
CHECK_BOX
CHECK_CLASS
```

是否明显下降。

如果仍大量集中在某一类别，应返回阶段9专项复查。

---

### 阶段13：生成审核统计报告

编写：

```text
08_build_review_report.py
```

输出：

```text
review_summary.json
review_summary.md
```

至少统计：

```text
Images reviewed
Person original
Person added
Person modified
Vehicle original
Vehicle added
Vehicle modified
Ignore added
Wrong label deleted
Duplicate removed
Rider reviewed
Parked vehicle reviewed
AI suggestions checked
AI suggestions accepted
```

---

### 阶段14：冻结Verified GT v1

完成审核后建立：

```text
verified_dataset_v1/
```

记录：

```text
images.txt
labels.txt
dataset_split.json
annotation_policy_v1.md
review_summary.json
sha256.txt
```

从这一刻开始：

> 不再随意修改v1。

后续修改必须生成：

```text
verified_dataset_v2
```

---

### 阶段15：CNN Smoke Test

先运行：

```text
1 ~ 3 epoch
```

只检查：

- dataset加载
- label格式
- bbox范围
- loss
- NaN
- augmentation
- resize
- class mapping

通过后再进行正式实验。

---

### 阶段16：训练CNN Baseline

训练：

```text
Baseline A
```

保存：

```text
Precision
Recall
mAP50
mAP50-95
Person AP
Vehicle AP
confusion matrix
false positive samples
false negative samples
```

同时记录：

```text
seed
model config
dataset hash
training config
checkpoint hash
```

---

### 阶段17：进行庭院辅助数据对照

建立：

```text
Experiment A:
Road only

Experiment B:
Road + Courtyard person auxiliary
```

保持：

```text
模型结构一致
超参数一致
随机种子尽量一致
```

重点比较：

```text
Person Recall
Person AP
Vehicle AP
Road validation AP
False Positive
```

只有在道路性能没有明显下降的情况下，才考虑将庭院数据正式并入训练集。

---

### 阶段18：Teacher 256张Train覆盖试验

在Verified GT门禁通过后，再运行Teacher对256张训练候选的覆盖检查。

目的：

```text
寻找仍未覆盖的困难样本
寻找系统性类别问题
寻找下一批最有价值的数据
```

不能直接将Teacher输出写入GT。

---

### 阶段19：根据证据决定S / D两组实验

在完成：

```text
Verified GT
Baseline
Teacher 256覆盖检查
```

后，再决定：

```text
S组
D组
```

是否各运行2轮对照。

避免在标签质量尚未确认前消耗大量训练资源。

---

## 推荐脚本目录

最终建议形成：

```text
tools/
├── 01_build_review_manifest.py
├── 02_run_teacher_review.py
├── 03_match_teacher_gt.py
├── 04_validate_annotation_geometry.py
├── 05_rank_suspicious_frames.py
├── 06_make_review_overlays.py
├── 07_apply_annotation_patch.py
├── 08_build_review_report.py
└── 09_freeze_verified_dataset.py
```

整体数据流：

```text
                   Teacher CNN
                       │
                       ▼
               teacher_predictions
                       │
                       │
Original GT ───────────┼─────────────┐
                       │             │
                       ▼             │
              IoU / class compare    │
                       │             │
                       ▼             │
                 review_queue        │
                       │             │
                       ▼             │
                  Manual Review      │
                       │             │
                       ▼             │
               annotation_patch      │
                       │             │
                       ▼             │
                 Verified GT ◄───────┘
                       │
                       ▼
                 CNN Baseline
                       │
                       ▼
               Error Analysis
                       │
                       ▼
             Teacher 256 Coverage
                       │
                       ▼
                  S / D Experiments
```

---

## 当前最优先执行顺序

如果只看下一阶段，建议严格按照：

```text
1. 冻结annotation_policy_v1
2. 完成128张训练帧人工审核
3. 完成道路地面审核
4. 专项检查rider / parked vehicle / small object
5. AI二次查漏
6. 生成Verified GT v1
7. 冻结hash和审核报告
8. CNN Smoke Test
9. CNN Baseline
10. Teacher 256覆盖检查
11. 决定是否扩充数据和运行S/D实验
```

当前阶段最重要的产物不是新的模型权重，而是：

```text
Verified GT v1
```

只有这一层稳定后，后续Precision、Recall、AP和不同训练方案之间的比较才真正有意义。
