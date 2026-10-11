# DDR 候选链固定 Mask 诊断工具

## 这个工具做什么

本工具只读取**去噪之后、最短 run 过滤之前**导出的二值 Mask，对同一张 Mask 比较：

1. 当前最短 run 门槛，例如 5。
2. 保留所有非空 run，即最短 run 为 1。

其余面积门槛、面积 Top-K 和评估规则保持一致。输出逐帧前景像素数、run 数、独立 RLE 参考的标签分配数与 union 数、连通域和候选框。可选输入人工标注，计算 IoU≥0.5、类别无关、最大匹配数优先的一对一候选匹配。

它还将本工具的独立 RLE 分区逐像素与 OpenCV 8 连通分区比较。数字标签 ID 不要求一致，但像素分组必须一致。

**不含你的当前 RLE 源码，所以这项一致性检查验证的是本工具，不是已经证明你的工程 CCL 正确。** 要检查工程，必须将工程在同一张过滤后 Mask 上的结果另行比对。

## 不做什么

- 不读取或修改生产 RTL、模型、背景算法、阈值冻结文件。
- 不训练，不扫参数，不访问 blind / test / reserve。
- 不重新解码视频，不重建背景历史，不模拟 DDR / CDC / 调度 / 显示。
- 不是 RTL 周期或溢出等价模型；标签分配策略、Top-K 并列排序可能与工程不同。
- 不声称提高了真实视频召回；附带的测试和 demo 全是合成输入。
- 固定 Mask 的对照只归因空间处理。容量会反过来影响背景更新的分支，仍需从第0帧分别因果重放，不能把此工具的结果冒充全链反事实。

## 运行环境

Python、NumPy、OpenCV。开发时使用 Python 环境中的 NumPy 2.3.5、OpenCV 4.13.0；这些是工具测试环境信息，不是要求你重装已有软件。

先运行：

```powershell
python -m unittest -v test_ddr_mask_audit.py
```

9 个测试方法包括：空图/全前景、多旧标签桥接、斜向8连通、左右边界、多帧清零、128张固定随机图、细高组件、累计标签需求、阴影值拒绝及非贪心一对一匹配。

## 输入合同

### Mask

目录中每个文件为一个二维 `.npy` 数组，文件名使用 `frame_000120.npy` 或 `000120.npy`。帧号必须是原始源视频的第0帧起编号。

仅允许像素值 0、1、255。127 等阴影/未知值会被拒绝，避免把阴影无声地当成前景。必须由来源算法显式决定如何处理阴影，不能在这里偷偷改变语义。

必须导出 **after_cleanup_before_min_run** 阶段；已经删掉短 run 的 Mask 无法恢复被删像素。导出应是既有因果回放的旁路观察，不得在每张审核帧重新学习背景。例如在本地既有脚本中正确的阶段增加：

```python
# clean_mask 是既有软件流程当前帧的去噪输出，frame_id 是源帧号。
# 这里只示意导出位置；不是你的实际工程变量名。
np.save(output_dir / f"frame_{frame_id:06d}.npy", clean_mask)
```

本工具无法验证这些 Mask 来自哪段视频或是否从第0帧因果产生。报告会明确记录 `input_provenance_verified=false`，逐文件记录哈希；视频哈希、原回放配置及收据仍应由你的既有运行记录提供。

### 人工标注（可选）

```json
{
  "coordinate_convention": "xyxy_half_open_in_mask_pixels",
  "frames": [
    {
      "frame_id": 120,
      "width": 640,
      "height": 360,
      "objects": [
        {"id": "person_1_at_120", "class": "ped", "bbox_xyxy": [10, 20, 25, 60]}
      ]
    }
  ]
}
```

- 坐标已经位于 Mask 分辨率，采用半开区间 `[x0,x1) × [y0,y1)`。
- 工具不猜原图与检测图映射，也不自动缩放标注。原工程若使用闭区间，需要显式转换。
- 类别字符串原样保存，不合并骑行者与人车类别，不自动补人工标签。
- `ignore` / `iscrowd` 为真会报错；需要此类评估语义时使用项目既有评估器。
- 未标注的帧不当成空场景；未提供标注就不报告召回。
- 匹配为类别无关的一对一最大基数匹配；并列采用确定性顺序。它可能与既有评估器的次级优化和并列规则不同，正式对照仍应复用原评估器。

## 对真实导出 Mask 运行

```powershell
python ddr_mask_audit.py --mask-dir .\clean_masks --input-stage after_cleanup_before_min_run --current-min-run 5 --min-area 100 --top-k 4 --start-frame 120 --end-frame 1079 --out .\audit_report.json
```

有标注时追加：

```text
--annotations .\reviewed_annotations.json
```

只有核对实际容量口径后，才追加：

```text
--run-capacity 64 --usable-labels 32
```

这里的 32 只是语法示例。`usable-labels` 表示**扣除背景或其他保留编号后真正能用的前景标签数**，不能未经核对直接照搬 `MAX_LABEL`。不传容量时相关指标为 `null`，不会假装通过。

工具不会覆盖已有输出；更换文件名可保留实验记录。缺失帧会显式列出，不把少量 Mask 冒充 960 帧完整结果。

## 合成 demo

```powershell
python ddr_mask_audit.py --mask-dir .\synthetic_demo\masks --input-stage after_cleanup_before_min_run --current-min-run 5 --min-area 100 --annotations .\synthetic_demo\annotations.json --start-frame 120 --end-frame 120 --out .\demo_local_report.json
```

demo 是3像素宽、40像素高的二值组件，面积120。最短run=5会删除整个组件；保留短run后，组件仍满足面积≥100。**它只证明该门槛可能误删面积合格组件，不证明你的视频恰好因此漏检。**

## 读报告与下一步

- `reference_current_min_run` 与 `reference_keep_all_runs`：固定 Mask 上的两个软件参考。
- 若保留短run后真实目标候选恢复、但标签需求上升：说明召回与容量必须同时设计，不能直接把新门槛塞入32标签的正式链。
- 若没有恢复：停止盲目减门槛，查看原始差分、cleanup前后像素、连通域是否粘连或映射错误。
- 与工程CCL对照时，先确保双方输入为完全相同的过滤后Mask；再比较像素分区、BBox和面积，不比较任意标签ID。
- 跨配置背景历史不同、尤其容量回滚配置，必须第0帧重新因果回放才能给出最终候选召回。

参考接口：OpenCV 4.13.0 `connectedComponentsWithStats` / `connectedComponents`，官方文档 `https://docs.opencv.org/4.13.0/d3/dc0/group__imgproc__shape.html`。
