# 旧 HOG-SVM 工程优化记录

日期：2026-10-11。工程：`E:/project/qiansai/anlogic_topic2_work/lab1_sc500_road_vision`。

## 本次结论

旧工程仍保留，入口为 `tools/train_hog_svm.py`、`tools/hog_reference.py`，HOG324诊断模型在 `external_reference_exploration/results/opencv_hog_diagnostic/`。历史生产模块在 `user_source/hdl_source/road_vision/`。当前同目录的RoadYOLO/CNN是另一条工作线，本轮没有修改其代码、数据或训练。

本批只接纳不改变模型和候选输出的Python提速，修复一个阻止诊断完成的拼图错误。**没有获得识别准确率提升，不替换分类权重，不改生产RTL。**

## 已落地的修改

1. `candidate_chain_reference.filter_short_runs`：最短长度1直接返回规范化mask；默认长度2用左右相邻像素运算判断所属run；其他长度保持原实现。增加二维输入检查。规则仍是run长度至少2，没有放宽为1。
2. `hog_reference.extract_features`：缓存三行并一次读取8个Sobel邻点，减少重复索引；保留梯度表达式、幅值上限、方向优先级、cell编号和整数累加。增加32×32形状检查；无新增依赖、无模型变化。
3. `local_background_counterfactual.draw_panel`：原图为三通道、mask为二维，旧代码直接拼接会崩溃；现将显示用mask转为BGR。该修改只影响审核图，不改算法输入。新增实际拼图shape/dtype/像素自检。

编辑前的三个工具及原测试文件保存在 `before/`。本批开始时工程尚未建立Git；2026-10-11并行任务建立了仓库，当前分支为 `work/roadyolo`。用户随后授权每个验证通过阶段单独提交并推送；远程尚未配置时只作本地提交。初始快照发生在本批文件写入期间，留下三个文件末尾未完整入库；本阶段提交保存已验证的完整文件及结果。没有覆盖旧模型、原始人审文件或历史实验。

## 最终基准与验证

见 `benchmark.json`，固定5轮、交替新旧顺序、取中位数；均为本机CPU函数测量。

| 函数 | 原实现 | 优化后 | 加速比 |
|---|---:|---:|---:|
| HOG64 / ROI | 0.7124 ms | 0.6424 ms | 1.109× |
| 默认Run过滤 / 256×144 mask | 3.6120 ms | 0.09047 ms | 39.924× |

- 429个train/val真实ROI：使用已有读取器核对像素哈希，64维特征、方向计数及固定SVM分数零差异。
- 32张已存真实clean mask：长度1/2/3新旧过滤零差异；默认结果与旧run mask逐像素一致，Top4 bbox/area与冻结记录一致。
- `python tests/test_python_references.py CandidateReferenceTests`：18项通过；含256种8像素行的穷举、边界、非连续内存、非二值输入、空宽及非法维度。
- `python tests/test_hog_reference.py`：2项通过；24种ROI由独立OpenCV Sobel及数组累加校验特征和bin计数，并检查非法尺寸。
- `python tools/local_background_counterfactual.py --self-check`：通过，含真实拼图路径回归。

首次候选测试因沙箱临时目录权限失败；同一组测试在正常权限下复跑通过。没有重新运行RTL或板级测试，这些速度数字不代表FPGA频率、帧率或全视频吞吐。

## 固定背景分割对照：不采用

沿用旧计划的固定MOG2参数：history=500、varThreshold=16、detectShadows=false、learningRate=-1。连续解码frame0..1050，只评分既定32帧；下游cleanup、min-run2、area16、Top4和HOG64/HOG324参数保持固定。一次处理1051帧用时12.81秒；这是离线运行时间，不是板级性能。

结果：`mog2_fixed_v2/report.json`、逐帧与配对清单及6张失败图。原崩溃尝试在 `mog2_fixed/FAILED_INCOMPLETE.json` 保留，不计为有效结果。

| IoU≥0.5，同一批移动目标 | 原基线 | 固定MOG2 |
|---|---:|---:|
| Top4行人覆盖 | 11/46 | 2/46 |
| Top4车辆覆盖 | 3/11 | 1/11 |
| Top4合计覆盖 | 14/57 | 3/57 |
| 定位且HOG324分类正确：行人 | 7/46 | 2/46 |
| 定位且HOG324分类正确：车辆 | 2/11 | 1/11 |

配对结果为新增2、保留1、丢失13、共同漏检41。因此拒绝该固定配置，不继续扫MOG2参数，不把更干净的背景当作优化成功。这不等于否定所有背景建模方法。OpenCV没有生产RTL标签容量限制，32帧中13帧组件数下界仍超过32。

当前分母是一个场景、32帧、4条相关轨迹的57次观测；缺少完整背景真值，precision与invalid FAR仍为空。MOG2结果先于HOG标量循环重构生成，HOG324实现未修改。工具版本、输入和依赖哈希见各自收据；不把历史运行收据改写成当前代码版本。

## 准确率工作的下一步

- 旧 `evaluation/status.json` 停留在2026-09-30，不能作为CNN主线的最新状态。本报告只更新旧HOG分支的本批结论。
- 旧入口下未找到 `intersection_3785878_train_fullgt_review.json` 与 `intersection_3785878_candidate_review.json` 的人工完成导出；原状态仍待标签、来源许可与场景族确认。没有搜索blind/test数据，也没有用AI预标注替代人工。
- 准确率改进继续区分候选定位和分类适配：先完成典型Mask的正式32标签容量RTL对照；若位置线索存在而框不完整，再做少量受限窗口实验。
- 独立训练标注齐备后再执行既定的单次C=1 HOG324适配；不将已用于开发判断的32帧加入训练，不调测试阈值，不通过新增训练轮次掩盖数据缺口。

## 复跑入口

在工程根目录执行：

```powershell
python tests/test_hog_reference.py
python tests/test_python_references.py CandidateReferenceTests
python evaluation/hog_svm_optimization_20261011/verify_and_benchmark.py
python tools/local_background_counterfactual.py --self-check
```

完整MOG2回放必须提供新输出目录；不覆盖 `mog2_fixed_v2/`。测试及基准包含数据契约校验；基准不拟合模型、不读取test、不修改RTL。

独立子代理审查未完成，本批没有将代理启动请求当作审查通过；以上结论来自协调代理实际运行的检查。
