# 道路视角候选册（仅视觉分类）

本目录只用于选择道路视角/场景照片；没有训练、推理、改标签或读取标签内容。相似画面只标记为“视觉近似”，不据此认定为相同 `camera_id`。

## 当前候选

- 共 16 张：A 固定斜俯视通道 5 张，B 低机位/近地斜视 2 张，C 固定斜俯视停车场园区 2 张，D 高位斜视密集大路口 5 张，E 无人机高空 2 张。
- F 真正正俯视没有可靠本地代表，未用高位斜视图冒充。
- B 类的两张 CDnet 图只是行人场景视角示例，不是严格道路平视，也不代表完整人车训练 GT。
- `contact_sheet_1.jpg`、`contact_sheet_2.jpg` 是最终候选联系表；`candidates.json` 保存绝对原图路径、来源、split 角色、已知 frame/camera、缩略图路径、原图 SHA256/尺寸、视觉分类和不确定性。

## 实际读取边界

- Intersection-Flow-5K：只读取 `images/train`，从按文件名排序的 5483 张中等距取 16 张作有界视觉检查，保留 9 张。未访问 `images/test`、`images/val`、annotations 或 labels。
- Ground48：读取既有 `selection.json`；只查看 5 张此前已审阅 `raw.png`，保留 2 张。camera/frame 只采用 `selection.json` 明示值。
- SPD8：只查看既有审核包中的 8 张 `raw/*.jpg`，保留 1 张；未读取同名 JSON 标签。
- CDnet：读取 `catalog.json`；严格按其中 `split=train` 的 `busStation`、`pedestrians` 各取一张中部帧，未访问任何 test 场景图像。
- VisDrone：读取既有 development split 元数据；只查看两个标为 train 的序列中部帧，保留 2 张；未读取 annotations。

## 缺口

- 无可信的严格水平道路平视图。
- 无可信的明确低机位道路摄像头图；CDnet 只能作近地行人场景对照。
- 无可信的严格正俯视/垂直俯拍图。

复现与校验：

```powershell
python .\cnn\prepare_scene_view_candidates.py --build
python .\cnn\prepare_scene_view_candidates.py --validate
```
