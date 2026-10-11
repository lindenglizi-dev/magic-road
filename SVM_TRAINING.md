# HOG-SVM训练与权重导出

> 真实数据训练现在以 `REAL_DATA_WORKFLOW.md` 为准：必须使用 manifest、train/val/test 场景隔离、验证集调参、模型冻结后单次测试，并分开报告人工框、公开标注框和CCL框。真实数据不要照搬本文件后面的旧目录和命令；随机拆分只保留给 `--self-test` 工具链自测，不得用于真实模型结论。

## 1. 这一步解决什么

`tools/train_hog_svm.py` 使用与RTL逐位一致的灰度、32×32缩放、Sobel、方向量化和64维HOG特征训练二分类线性SVM，并自动完成：

1. 标准化参数折叠进线性权重和偏置；
2. 浮点模型测试；
3. 12 bit有符号权重和40 bit偏置量化；
4. 量化模型复算及溢出上界检查；
5. 生成可综合的 `hog_svm_weights.v`；
6. 输出权重、模型参数、混淆矩阵和可供RTL复验的测试向量。

## 2. 数据目录

可以使用 `tools/roi_dataset_tool.py` 从道路视频直接制作以下目录，具体操作见 `ROI_DATASET_TOOL.md`。

推荐明确分开训练集和测试集：

```text
dataset/
├─ train/
│  ├─ ped/
│  │  ├─ sequence_01/*.png
│  │  └─ sequence_02/*.png
│  └─ vehicle/
│     ├─ sequence_03/*.png
│     └─ sequence_04/*.png
└─ test/
   ├─ ped/*.png
   └─ vehicle/*.png
```

每张图片必须是“一个目标的紧致候选框裁剪”，不是完整道路画面。脚本允许任意图像尺寸，并使用与 `roi_frame_reader.v` 相同的像素中心最近邻DDA缩放到32×32。

训练集和测试集应来自不同原始视频或不同拍摄时段。不要把同一段视频的相邻帧随机分到两边，否则测试准确率会严重虚高。

建议第一版至少准备：

- 行人训练图200张以上、测试图50张以上；
- 车辆训练图200张以上、测试图50张以上；
- 包含远近、明暗、遮挡、侧面以及CCL框不完整的困难样本；
- 最终以板上CCL实际裁出的ROI为主，而不是只用干净公开数据集。

若目录中没有 `train/` 和 `test/`，脚本会执行分层随机切分，只适合早期调试。

## 3. 训练命令

```powershell
python .\tools\train_hog_svm.py `
  --dataset D:\road_roi_dataset `
  --output .\trained_model
```

主要输出：

| 文件 | 作用 |
|---|---|
| `hog_svm_weights.v` | 64×12 bit权重ROM及40 bit偏置，可接FPGA总顶层 |
| `hog_svm_weights.hex` | 量化权重审计文件 |
| `model.json` | 浮点折叠权重、量化权重、类别和特征顺序 |
| `metrics.json` | 浮点/定点准确率、混淆矩阵、溢出上界 |
| `svm_test_*.hex` | Python与RTL最终内积对照向量 |

类别约定固定为：负分=`ped`/RTL类别1，非负分=`vehicle`/RTL类别2。

## 4. 工具链自测

```powershell
.\tests\run_svm_training_selftest.ps1
```

自测会生成纵向“行人”和横向“车辆”合成图形，只验证训练、量化、Verilog ROM生成和RTL内积是否一致。其准确率不代表真实人车识别性能。

当前自测结果：

```text
96个合成样本
浮点测试准确率 100%
12 bit定点测试准确率 100%
RTL分数与Python分数完全一致
40 bit累加器最坏上界检查通过
```

## 5. 接入总顶层前的验收线

真实模型至少要满足：

1. 明确独立测试集，而不是同视频相邻帧随机切分；
2. 定点准确率与浮点准确率差距不超过约1个百分点；
3. 分别报告行人和车辆召回率，不能只报告总体准确率；
4. `worst_score_bound` 小于40 bit有符号累加器上限；
5. 使用导出的测试向量再次跑RTL ROM/内积对照；
6. 达标后才把生成的权重ROM复制进 `user_source/hdl_source/road_vision/` 并连接总顶层。

如果真实准确率不足，先检查CCL框质量、样本覆盖和类别不平衡，再决定是否增加HOG归一化或升级特征；不要先盲目换CNN。
