# 视频ROI数据集制作工具

## 作用

`tools/roi_dataset_tool.py` 把道路视频转换成与FPGA分类链一致的人车ROI数据集：

```text
视频帧
  ↓ FPGA同款灰度：(R>>2)+(G>>1)+(B>>2)
  ↓ 从x/y=0开始每5像素采样一次
256×144分析画面
  ↓ 人工在分析画面框选目标
  ↓ FPGA同款Q8 DDA最近邻缩放
32×32灰度ROI
```

左侧窗口显示真正送入算法的灰度分析画面，框选必须在左侧进行；右侧显示原始彩色视频，只用于辅助辨认目标。

## 使用方法

训练视频：

```powershell
python .\tools\roi_dataset_tool.py `
  --video D:\road_video\train_01.mp4 `
  --output E:\project\qiansai\road_roi_dataset `
  --split train `
  --scene-id camera_train_01 `
  --stride 10
```

每个视频还必须指定连续拍摄/摄像机分组 `--scene-id`。训练、验证和测试必须来自不同 scene；同一原片、转码片或同一 scene 跨集合会被拒绝。

独立验证视频使用 `--split val`，独立测试视频使用 `--split test`：

```powershell
python .\tools\roi_dataset_tool.py `
  --video D:\road_video\test_01.mp4 `
  --output E:\project\qiansai\road_roi_dataset `
  --split test `
  --scene-id camera_test_01 `
  --stride 10
```

一个视频第一次写入manifest后就固定属于train、val或test之一；以后即使重新启动工具，也会拒绝把同一路径、相同哈希、同一派生文件族或同一scene写入另一侧，防止相邻帧及转码副本泄漏。

## 操作键

| 操作 | 按键/鼠标 |
|---|---|
| 框选目标 | 在左侧灰度图按住鼠标左键拖动 |
| 清除框 | 鼠标右键或 `C` |
| 保存为行人 | `P` |
| 保存为机动车 | `V` |
| 保存为无效候选（背景碎片、粘连框等） | `I` |
| 下一组帧 | `N`、空格或右方向键 |
| 上一组帧 | `B`或左方向键 |
| 增大/减小跳帧间隔 | `+` / `-` |
| 撤销本次运行最近一次保存 | `U` |
| 退出 | `Q`或Esc |

保存一个目标后不会自动跳帧，可以继续框选同一帧中的其他目标。

## 输出结构

```text
road_roi_dataset/
├─ train/
│  ├─ ped/*.png
│  ├─ vehicle/*.png
│  └─ invalid/*.png
├─ val/...
├─ test/
│  ├─ ped/*.png
│  └─ vehicle/*.png
├─ raw_crops/
│  ├─ train/...
│  └─ test/...
└─ manifest.csv
```

- `train/`、`val/`和`test/`中的图片是32×32灰度ROI；无效候选只用于评估当前二分类基线的误接受问题；
- `raw_crops/`保留缩放前的256×144分析域裁剪，用于审计框是否合理；
- `manifest.csv`记录视频、帧号、时间、框坐标、类别、文件路径和ROI哈希；
- 相同视频帧和相同框不会重复保存或保存成冲突类别；完全相同的32×32 ROI也会被拒绝。

## 框选原则

- 框住单个完整目标，尽量贴合目标外轮廓；
- 不要把相邻的人和车放进同一个框；
- 保留少量遮挡、截断和偏框样本，以接近CCL真实输出；
- 分析域宽或高不足2像素的目标不会保存；实际训练建议目标至少约6～8像素；
- 同一个目标不需要连续每帧都保存，默认每10帧查看一次，可以按场景调整。

工具会拒绝非1280×720输入。公开数据先使用 `tools/prepare_public_video.py` 生成带来源、哈希和几何记录的720p无损派生视频。

真实评估、三集合冻结、公开数据导入和 CCL 候选流程以 `REAL_DATA_WORKFLOW.md` 为准；本工具只负责人工标注入口。

## 自测

```powershell
python .\tools\roi_dataset_tool.py --self-test
```

自测覆盖灰度降采样、DDA缩放、保存、重复保护和撤销，不会打开GUI。
