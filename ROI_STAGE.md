# CCL候选框到32×32 ROI阶段

## 当前链路

```text
摄像头域                                      100 MHz算法域

CCL/几何分类候选框 ─ roi_object_snapshot_cdc ─┐
                                               ├─ 帧号匹配
双ERAM灰度帧 ───── gray_frame_pingpong ────────┘
                                                     │
                                              roi_frame_reader
                                                     │
                                       32×32灰度ROI像素流
                                                     │
                                            Sobel/HOG cell特征
                                                     │
                                              下一步：定点SVM
```

## 实现内容

- `roi_object_snapshot_cdc.v`：按帧冻结最多四个候选框，跨时钟传输框、类别、数量和源帧编号。
- `roi_frame_reader.v`：等待帧与框编号匹配，逐框生成帧缓存地址，将任意尺寸候选框最近邻归一化成32×32。
- `gray_frame_pingpong.v`：发布ID改为源帧编号；即使某帧因bank冲突未缓存，后续编号仍与CCL结果保持一致。
- `design_top_wrapper.v`：正式移除全帧probe读取路径，接入候选框CDC和ROI读取器。

## 地址算法

每个方向使用Q8定点DDA：

```text
step_x = bbox_width  × 256 / 32 = bbox_width  << 3
step_y = bbox_height × 256 / 32 = bbox_height << 3
初值取半个step，使采样点位于目标像素中心。
```

因此综合后没有新增DSP。每个ROI固定输出1024个像素，输出同时带 `object_index、roi_x、roi_y、gray`，可直接接梯度/HOG流水线。

## 验证结果

- 8组Icarus回归全部通过，其中2组专门验证ROI链。
- LUT6：14,093 / 21,216（66.43%）。
- Slice：16,626 / 21,216（78.37%）。
- Register：17,522 / 42,432（41.29%）。
- ERAM20K：94 / 108（87.04%）。
- DSP：9 / 40（22.50%）。
- Setup SWNS +1.168 ns；Hold HWNS +0.020 ns；无违例。

## HOG后续进展

已接入 `hog_sobel_gradient.v` 和 `hog_cell_histogram.v`：32×32 ROI输出30×30有效Sobel梯度，量化为4个无符号方向，再形成4×4 cells × 4 bins的64维特征。下一步是冻结特征定义、建立PC端参考模型并接入定点线性SVM。

包含HOG后的最新布局布线结果为：LUT6 15,693（73.97%）、Slice 18,003（84.86%）、ERAM 94（87.04%）、DSP 9（22.50%），Setup SWNS +0.110 ns，Hold HWNS +0.020 ns。当前无违例，但资源和时序裕量都要求后续采用串行复用结构。
