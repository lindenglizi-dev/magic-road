# 安路道路视觉项目当前架构

## 1. 当前作品定位

本工程以安路官方 `lab_ex1_mipi_hdmi_SC500_720P` 为底座，在不阻塞原摄像头到 HDMI 显示链路的前提下，增加一条完全由 FPGA RTL 实现的道路目标分析链。

当前已经形成的闭环是：

1. SC500 实时采集 1280×720 图像，官方 ISP、DDR 和 HDMI 链维持原功能；
2. 从 ISP 的 AWB 输出旁路抽取 256×144 灰度分析流；
3. 背景差分、二值去噪和 RLE-CCL 每帧寻找运动目标；
4. 最多四个候选目标进入跟踪、事件判断和 HDMI 画框；
5. 同帧灰度图和候选框在 100 MHz 域配对，裁剪并缩放成 32×32 ROI；
6. ROI 经 Sobel 和方向直方图生成 64 维 HOG cell 特征，为下一阶段定点分类器提供输入。

当前“检测、跟踪、画框、ROI、HOG 特征”已实现，64周期串行线性SVM内积核也已完成独立仿真；但真实训练权重、权重ROM和分类结果回写尚未接入总顶层。因此，当前 HDMI 框颜色仍使用几何规则产生的临时类别，不应把它当作最终人车识别精度。

## 2. 总体数据流

```text
SC500 MIPI RAW10
       │  摄像头时钟域 S_csi_rx_clk
       ▼
MIPI RX → RAW10解包 → ISP/去马赛克/AWB
                         │
             ┌───────────┴────────────────────────────┐
             │                                        │
             │ 官方显示主链                           │ 非阻塞分析旁路
             ▼                                        ▼
       96→128位打包 → DDR帧缓存                 awb96_analysis_adapter
             │                                        │
             ▼                                        ▼
       HDMI mixer/时序 → HDMI输出               256×144灰度流
                                                      │
                         ┌────────────────────────────┴──────────────────────┐
                         │                                                   │
                         ▼                                                   ▼
                  前景检测/CCL链                                      双bank灰度帧缓存
         background_model → binary_cleanup_3x3                      gray_frame_pingpong
                         → rle_ccl_top                                      │
                         → geometry_classifier                             │
                         → object_frame_store                              │
                         │                                                 │
              ┌──────────┴──────────┐                                      │
              ▼                     ▼                                      │
       object_tracker       roi_object_snapshot_cdc                        │
              │                     │ 候选框+源帧号                          │ 灰度帧+源帧号
              ▼                     └──────────────────┬───────────────────┘
       track_event_detector                            │ 100 MHz算法域
              │                                       ▼
              │                               roi_frame_reader
              │                         任意候选框 → 32×32灰度ROI
              │                                       │
              │                                       ▼
              │                              hog_sobel_gradient
              │                          30×30有效梯度、4方向量化
              │                                       │
              │                                       ▼
              │                              hog_cell_histogram
              │                           4×4 cells × 4 bins
              │                              64维HOG特征
              │                                       │
              │                              下一阶段：定点SVM
              │
              ▼  track_snapshot_cdc
       HDMI像素域冻结跟踪表 → road_box_overlay → road_status_overlay → HDMI
```

这不是把降低分辨率后的画面送到 HDMI。HDMI 始终显示官方 1280×720 主链画面；256×144 只供算法使用，检测框坐标在显示端放大 5 倍后叠加。

## 3. 三个时钟域及跨域边界

| 时钟域 | 主要模块 | 处理内容 | 跨域方式 |
|---|---|---|---|
| `S_csi_rx_clk` | ISP、分析适配、背景差分、去噪、CCL、跟踪、事件 | 与摄像头像素同步的逐帧分析 | 帧级数据先冻结，再使用 toggle 握手 |
| `S_100m_clk` | 双bank帧缓存读口、ROI读取、Sobel、HOG直方图 | 候选目标的随机读和特征提取 | 只读取已发布且已取得所有权的bank |
| `S_hdmi_pixel_clk` | 跟踪快照、框和状态叠加 | 在原始HDMI画面显示结果 | 收到完整冻结的跟踪表后一次更新 |

跨域不直接采样正在变化的多位总线。`roi_object_snapshot_cdc` 和 `track_snapshot_cdc` 都先在源域冻结一整组数据，再用事件握手通知目标域读取。

## 4. 检测、跟踪与事件链

### 4.1 分析流生成

`awb96_analysis_adapter.v` 从 AWB 输出按水平、垂直各 5 倍抽样，把 1280×720 RGB 转成 256×144 灰度流，同时重新产生 `valid/x/y/sof/eol/eof`。原显示链不等待分析链，因此算法不会降低 HDMI 帧率。

### 4.2 前景检测

`background_model.v` 为每个 256×144 像素保存背景灰度，当前差分阈值为 20。前四帧用于背景学习，之后以低速更新背景；前景像素可冻结背景更新。地址由坐标生成，而不是依赖自由递增计数器。

`binary_cleanup_3x3.v` 使用完整 3×3 邻域清除孤立噪声。当前要求中心为前景且邻域至少有 3 个前景点，边界作零填充。

### 4.3 CCL与候选目标

`rle_ccl_top.v` 先把每行连续前景压成 run，再匹配相邻行、管理 label、合并等价关系，最后按面积挑选最多四个候选目标。默认约束包括：

- 每行最多 64 个 run；
- 每帧最多 32 个 label；
- 最小 run 长度 2；
- 最小目标面积 16 个分析像素。

`object_geometry_classifier.v` 根据宽、高、面积和填充率给出临时类别。它的作用是让当前工程在没有训练权重时仍能画出不同颜色的框，不是最终 HOG-SVM 分类器。

`object_frame_store.v` 以帧为单位提交对象表。如果该帧发生背景、CCL或分类协议错误，则提交明确的空表，不把半帧结果泄漏给跟踪器。

### 4.4 跟踪与事件

`object_tracker.v` 对最多四个对象做帧间关联，维护 ID、可见/确认状态、速度和 miss 计数。

`track_event_detector.v` 基于轨迹执行越线、区域进入/离开和停留类判断。当前警戒区及越线坐标在 `foreground_ccl_top.v` 参数中配置。

## 5. 帧缓存、ROI与HOG链

### 5.1 双bank灰度帧缓存

`gray_frame_bank_ram.v` 用 18 个原生 ERAM 保存一帧 256×144×8 bit 灰度图；两个bank合计使用 36 个 ERAM。

`gray_frame_pingpong.v` 管理发布和所有权：

- 摄像头域只写当前空闲bank；
- 完整且协议正确的帧才发布；
- 算法域取得bank所有权后，写侧不得覆盖；
- 两个bank都不可写时明确丢帧，而不是破坏算法正在读取的数据；
- 读写两侧都对坐标、地址、帧尾和非法释放进行检查。

帧缓存和候选框都携带同一个源帧编号。即使缓存因冲突丢帧，编号也不会悄悄错位。

### 5.2 候选框快照与帧配对

`roi_object_snapshot_cdc.v` 在摄像头域冻结最多四个候选框及其类别、数量和帧号，再送到 100 MHz 域。

`roi_frame_reader.v` 只有在候选框帧号与已发布灰度帧号相等时才开始读取；若不匹配，则丢弃较旧一方。这样不会发生“用上一帧框裁下一帧图”的错误。

### 5.3 32×32 ROI归一化

每个候选框输出固定 1024 个灰度像素，接口为：

```text
roi_valid
roi_object_index[1:0]
roi_x[4:0], roi_y[4:0]
roi_gray[7:0]
```

横纵坐标使用 Q8 DDA 最近邻采样：

```text
step_x = bbox_width  << 3
step_y = bbox_height << 3
```

运行时不需要乘法器或除法器。一个目标在 100 MHz 下输出约 10.24 μs，四个目标约 40.96 μs，不包含很小的读延迟和切换开销。

### 5.4 Sobel梯度

`hog_sobel_gradient.v` 使用两行 32 像素缓存形成流式 3×3 窗口，输出 ROI 内部坐标 1..30 的 30×30 梯度：

```text
magnitude ≈ |Gx| + |Gy|
direction_bin = 0° / 45° / 90° / 135°
```

方向量化只用比较、移位和符号判断，不使用反正切或浮点运算。模块同时检查 ROI 必须按 `(0,0)` 到 `(31,31)` 顺序输入且对象编号在一幅 ROI 内保持不变。

### 5.5 Cell方向直方图

`hog_cell_histogram.v` 把 32×32 ROI 划成 4×4 个 8×8 cell，每个 cell 累计四个方向bin，共输出 64 个 18 bit 特征：

```text
feature_valid
feature_object_index[1:0]
feature_cell_x[1:0], feature_cell_y[1:0]
feature_bin[1:0]
feature_value[17:0]
feature_object_done
```

边缘没有完整 3×3 邻域，所以实际参与累计的是 30×30 梯度。直方图在一幅 ROI 结束后用 64 个时钟顺序输出并随输出清零。下一幅 ROI 的前两行尚不会产生梯度，这段 64 周期空档允许特征输出完成，因此不需要给 ROI 读口增加反压。

当前顶层把特征折叠成校验值送到 HDMI 第四块诊断区域，用于证明 HOG 链持续运行。此校验值不是分类结果。

## 6. HDMI显示结果

`track_snapshot_cdc.v` 把完整跟踪表送入 HDMI 像素域，`road_box_overlay.v` 将 256×144 坐标放大 5 倍画到 1280×720 画面：

- 绿色：临时行人类别；
- 青色：临时车辆类别；
- 洋红：未知类别。

左上角四个 16×16 状态块：

- 绿色：曾检测到目标；
- 黄色：曾触发事件；
- 红色：曾出现分析、跨域、帧缓存、ROI或HOG协议错误；
- 蓝色变化块：HOG 已输出对象特征，颜色变化来自特征校验值。

## 7. 关键文件职责

| 层级 | 文件 | 当前职责 |
|---|---|---|
| 总顶层 | `design_top_wrapper.v` | 保留官方链并实例化整条道路视觉支链 |
| 输入适配 | `awb96_analysis_adapter.v` | RGB转灰度、5×5降采样、生成分析坐标协议 |
| 前景 | `background_model.v` | 背景学习、更新、差分与地址保护 |
| 去噪 | `binary_cleanup_3x3.v` | 3×3二值形态清理 |
| 连通域 | `run_detector.v`、`row_matcher.v`、`label_manager.v`、`frame_resolver.v`、`top4_selector.v`、`rle_ccl_top.v` | RLE-CCL与最多四目标选择 |
| 当前分类 | `object_geometry_classifier.v` | 几何规则临时类别 |
| 帧提交 | `object_frame_store.v` | 原子提交对象表，错误帧提交空表 |
| 跟踪事件 | `object_tracker.v`、`track_event_detector.v` | 四目标跟踪和道路事件 |
| 帧缓存 | `gray_frame_bank_ram.v`、`gray_frame_pingpong.v` | 双时钟双bank灰度帧缓存与所有权控制 |
| ROI跨域 | `roi_object_snapshot_cdc.v` | 候选框帧级快照和跨域 |
| ROI读取 | `roi_frame_reader.v` | 帧号配对、bbox裁剪、32×32归一化 |
| HOG前端 | `hog_sobel_gradient.v`、`hog_cell_histogram.v` | 梯度、4方向量化和64维cell特征 |
| SVM内积核 | `hog_linear_svm.v` | 每周期处理一个特征，64周期完成带偏置线性内积；等待训练权重ROM接入 |
| 训练导出 | `tools/train_hog_svm.py` | 位精确提取特征、训练线性SVM、量化并生成Verilog权重ROM |
| 数据制作 | `tools/roi_dataset_tool.py` | 视频同款灰度/5倍采样、人工框选、DDA生成32×32 ROI及manifest |
| 显示跨域 | `track_snapshot_cdc.v` | 跟踪表帧级快照和跨域 |
| 显示叠加 | `road_box_overlay.v`、`road_status_overlay.v` | 目标框和诊断状态显示 |

## 8. 已完成验证

执行：

```powershell
.\tests\run_iverilog.ps1
```

当前十组 RTL 回归覆盖：

1. AWB旁路到背景、CCL、跟踪和事件的端到端链；
2. 3×3二值去噪；
3. 跟踪表CDC和HDMI画框；
4. 双bank所有权、错误帧丢弃和冲突恢复；
5. 候选框CDC和错误帧空表；
6. bbox到32×32 ROI的地址、数据和数量；
7. 坐标异常检测及背景RAM写保护；
8. CCL错误帧不泄漏部分对象；
9. Sobel梯度、方向量化和4×4×4直方图输出。
10. 串行SVM的有符号乘加、偏置、正负分类和乱序保护。

此外可执行：

```powershell
.\tests\run_hog_crosscheck.ps1
```

该测试由 `tools/hog_reference.py` 生成一幅同时覆盖四个方向bin的确定性ROI和软件黄金特征，RTL读取相同1024个像素并导出64项特征，最后逐项比较。当前结果为64项全部一致。

执行 `tests/run_svm_training_selftest.ps1` 可进一步验证从训练、标准化折叠、12 bit量化、Verilog ROM生成到RTL串行内积的完整工具链。合成自测已经做到Python与RTL分数完全一致；合成数据准确率仅用于自测，不能作为作品指标。

真实数据可由 `tools/roi_dataset_tool.py` 制作。工具在256×144硬件分析画面上框选目标，保留缩放前裁剪，同时生成32×32训练ROI和可追溯manifest，并阻止同一视频跨train/test、同框冲突标签以及完全重复ROI。

完整综合、布局布线已通过，报告由 `td_project/road_elaborate.tcl` 生成：

- LUT6：15,693 / 21,216（73.97%）；
- Slice：18,003 / 21,216（84.86%）；
- Slice Register：19,323 / 42,432（45.54%）；
- ERAM20K：94 / 108（87.04%）；
- DSP：9 / 40（22.50%）；
- Setup：SWNS +0.110 ns，STNS 0；
- Hold：HWNS +0.020 ns，HTNS 0。

结论是当前HOG版本可以完成布局布线且没有静态时序违例，但Slice和setup裕量已经偏紧。后续分类器必须采用时分复用的串行MAC和小型权重ROM；在加入更多功能前，也应评估把当前分布式直方图迁移到ERAM或降低其组合扇出。

## 9. 当前边界与下一阶段

### 已实现

- 官方摄像头、ISP、DDR、HDMI主链；
- 256×144实时背景差分和去噪；
- RLE-CCL最多四候选框；
- 临时几何分类、四目标跟踪、事件与HDMI框；
- 稳定的双bank帧缓存和候选框/帧号配对；
- 32×32 ROI归一化；
- 30×30 Sobel梯度和64维HOG cell特征；
- 协议错误检测、错误帧隔离和九组RTL回归。

### 尚未实现

- HOG block归一化或其他特征尺度处理；
- 训练得到并量化的SVM权重与权重ROM；
- 串行SVM与总顶层HOG流的正式连接；
- SVM类别回写到跟踪表和HDMI框；
- 板上摄像头相位、真实道路阈值、帧率与长期稳定性验证。

### 建议的下一步顺序

1. 收集或裁剪32×32的人、车和困难负样本，并沿用当前软件参考模型提取完全一致的64维特征；
2. 训练线性SVM，记录数据划分、准确率、混淆矩阵以及原始浮点权重；
3. 对权重和偏置定点化，生成64×12 bit权重ROM，并离线复算量化分类结果；
4. 将权重ROM和已有 `hog_linear_svm.v` 接入总顶层；
5. 增加按 `frame_id + object_index` 对齐的分类结果表，再更新跟踪类别；
6. 上板后先验主视频，再验状态块、框、ROI/HOG/SVM运行，最后调整真实场景阈值和数据集。

不要立即增加另一套CNN或完整帧缓存。当前优先目标是让已有64维特征形成可训练、可量化、可回写的闭环；完成这一步后再根据实测准确率决定是否升级描述子或分类器。
