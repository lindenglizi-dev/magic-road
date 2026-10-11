# 三个 ROI 翻转实例的成对解释

本报告只重整已保存的 ROI、裁剪参数、评分和特征向量；未解码视频、未重裁剪、未提取新特征、未运行模型、未训练或扫描阈值。

## 成对结果

| 实例 | analysis crop（baseline → min_run1） | HOG324 float（baseline → min_run1） | HOG324 Q（baseline → min_run1） | 量化增量重构 |
|---|---|---|---|---|
| f000360_p01 | `[154, 112, 161, 132]` → `[154, 112, 164, 135]` | -1.28174762494 ped → 0.434055387746 vehicle | -94508688 ped → 31963081 vehicle | 126471769 = Σ324 product delta |
| f000690_p02 | `[0, 90, 9, 107]` → `[0, 87, 9, 114]` | -0.604131112368 ped → 0.102480580735 vehicle | -44521448 ped → 7630269 vehicle | 52151717 = Σ324 product delta |
| f001050_p02 | `[0, 30, 53, 143]` → `[0, 1, 101, 143]` | -3.42520839075 ped → 0.786354750478 vehicle | -252482169 ped → 57931908 vehicle | 310414077 = Σ324 product delta |

每个实例的 baseline/min_run1 图像是原 PNG 的逐字节复制。`pair_explanations.json` 给出闭区间 analysis/source 框、输入宽高、32 个 x/y 最近邻采样索引、ROI 像素哈希、HOG64/HOG324 原始已存评分和向量键。`feature_contributions.csv` 展开三组 324 维已存特征、乘积与 delta。

## 观测与推断

**观测：** 三例的新框都包含旧框，ROI 像素哈希均改变；HOG324 浮点与量化路径均由 ped 翻为 vehicle。量化分数增量分别由 324 个已存乘积差精确重构，浮点分数也由已存特征和哈希绑定的线性权重复核。

**推断：** 在这三例中，裁剪内容变化足以解释线性评分越过零点。贡献最大的特征索引只解释算术，不证明哪个视觉对象或方向结构造成翻转。

## 明确缺失

- Full HOG64 feature vectors and per-feature contributions were not saved; only their feature hashes, scores, and predictions exist.
- No verified semantic mapping from OpenCV HOG324 feature index to a named spatial/orientation bin was saved.
- No integer-gradient/bin HOG324 or RTL feature/score trace exists for these pairs.
- No saved evidence identifies the visual owner or semantic cause of each changed edge.

HOG324 工件自身状态是 `diagnostic_float_model_not_frozen_not_rtl`；这里的“冻结”仅指输入文件由哈希和收据锁定，不表示部署模型已冻结。三个例子不支持统一扩框/缩框、沿用旧类别、改阈值、重新训练或 RTL 接入。
