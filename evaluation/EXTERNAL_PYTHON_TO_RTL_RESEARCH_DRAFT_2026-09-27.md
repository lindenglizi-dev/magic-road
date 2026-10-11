# 外部 Python 识别方案转 RTL 调研草案

状态：中断时进度快照，仅保存调研结论；未批准实施，未修改现有 Python 流程、状态文件、工作流或正式 RTL。

保存日期：2026-09-27。

## 原始问题

评估网络上已有的优秀 Python 识别项目，先在本项目真实 32×32 ROI 上验证，再决定是否转换为安路 FPGA RTL。

## 架构领导者决策

外部项目只作为可复现的 Python 算法参考、训练工具和权重来源，不直接移植整套推理框架。最多并行验证两条路线：

1. 主线：固定 32×32 灰度输入的 HOG/手工特征＋线性 SVM。
2. 挑战线：从头训练、算子受限的整数小型 CNN。

两条路线必须使用相同的真实候选 ROI、scene 划分、人工标签和指标。先证明跨场景分类收益，再投入 RTL。

## 外部项目初步结论

| 项目/路线 | 可借鉴内容 | 对安路 RTL 的判断 |
|---|---|---|
| 项目自有整数 Cell-HOG＋scikit-learn `LinearSVC` | 位宽明确、权重和偏置易导出、逐级对拍容易 | 当前部署主线 |
| scikit-image HOG＋`LinearSVC` | 建立 144/324 维浮点上界和特征消融 | 可独立重写为 RTL，但标准归一化和插值成本较高 |
| OpenCV `HOGDescriptor`＋线性 SVM | 第二套浮点实现和特征排列交叉检查 | 可参考，内置行人权重不可直接使用 |
| 分块 LBP＋`LinearSVC` | 比较、计数、直方图，硬件代价低 | 仅作低成本消融 |
| VLFeat/dlib FHOG | 31 通道 FHOG 结构参考 | 特征和归一化更重，本阶段不作为实现基础 |
| Brevitas/QKeras | 量化感知训练、显式低位权重/激活 | 可用于训练整数小 CNN |
| FINN | QONNX、逐层验证、数据流架构方法 | 硬件生成依赖 AMD/Xilinx Vitis/Vivado，不能直接作为安路生成器 |
| hls4ml | 定点精度配置、复用因子、逐层 profiling | 后端面向 Vivado/Vitis、Intel、Catapult/oneAPI；可借方法，不能直接生成安路 RTL |

## 传统特征主线

建议在固定数据和 ROI 上比较：

1. 当前项目整数 Cell-HOG：4×4 cell、4 个方向 bin，共 64 维。
2. 紧凑 HOG：8×8 cell、2×2 block、4 bin，共 144 维。
3. 常规 HOG：8×8 cell、2×2 block、9 bin，共 324 维。
4. 分块 LBP：`P=8, R=1, uniform`，4×4 分块，每块 10 个模式，共 160 维。

全部使用显式配置的线性分类器，并导出 `coef_`、`intercept_`、原始 margin、浮点特征和定点特征。二次、多项式和 RBF 核暂不进入 RTL 候选。

scikit-image HOG 只能作为显式配置的浮点参考。必须冻结版本、梯度边界、方向 bin、block 布局、插值、归一化和特征排列，不能依赖默认参数。项目自有 64 维实现应称为轻量 Cell-HOG，不能宣称与标准 Dalal–Triggs HOG 等价。

OpenCV 默认行人检测器针对 64×128 窗口，Daimler 检测器针对 48×96 窗口，不能把其预训练权重缩放后用于本项目 32×32 人车分类。OpenCV 线性 SVM 的 `rho` 符号、类别方向和压缩支持向量需要逐样本分数核对。

## 整数小型 CNN 挑战线

只允许固定 32×32 输入、普通 3×3 卷积、ReLU、固定池化、全局平均或小型全连接。BatchNorm 在推理前折叠。首轮探索上限：

- int8 权重和激活；
- 权重不超过 32 KiB；
- 峰值激活不超过 32 KiB；
- 每 ROI 不超过约 1M MAC；
- 不使用注意力、动态形状、复杂归一化或浮点后处理；
- 导出每层整数张量、尺度、零点、舍入、饱和和累加位宽。

上述数字只是淘汰明显过大模型的探索上限，不代表现有 FPGA 已确认具备这些余量。正式选择前仍需当前器件综合后的 BRAM、DSP、LUT、时钟和帧间周期余量。

推荐借鉴 Brevitas 或 QKeras 的量化训练语义，网络结构和 RTL仍由本项目独立实现。FINN/hls4ml 的生成结果不能直接作为安路工程交付物。

## 共同验证门槛

- 固定同一批 baseline 主框和 fill-only 新增 small，不为不同分类器更换候选集合。
- 按 scene 分 train/val/test，禁止相邻帧或同一轨迹跨集合。
- 分别报告 ped、vehicle、background 的混淆矩阵、precision/recall 和拒识。
- 主框与新增 small 分开报告；截断、遮挡、粘连、y 带和尺寸带分层报告。
- 同时给出场景宏平均、最差场景和样本数。
- 未匹配 VIRAT 标注的候选不得自动作为背景。
- 浮点与定点逐层/逐阶段比较，最终分类不一致必须为 0 才能进入 RTL。
- 报告权重、峰值激活、行缓存、MAC、每 ROI 周期和最多四 ROI 的帧内预算。

以下情况立即否决 RTL 转换：Python 无法复现；预处理或权重来源不明；收益来自数据泄漏或人工挑选；32×32 真实候选上无稳定跨场景收益；关键类别定点性能明显退化；资源或吞吐超限；缺少中间参考向量；依赖非安路厂商专有核；许可不清。

## 主要官方来源

- [scikit-image HOG](https://scikit-image.org/docs/stable/api/skimage.feature.html#skimage.feature.hog)
- [Dalal–Triggs HOG 原始论文](https://lear.inrialpes.fr/people/triggs/pubs/Dalal-cvpr05.pdf)
- [scikit-learn LinearSVC](https://scikit-learn.org/stable/modules/generated/sklearn.svm.LinearSVC.html)
- [OpenCV HOGDescriptor](https://docs.opencv.org/4.x/d5/d33/structcv_1_1HOGDescriptor.html)
- [OpenCV SVM](https://docs.opencv.org/4.x/d1/d2d/classcv_1_1ml_1_1SVM.html)
- [scikit-image LBP](https://scikit-image.org/docs/stable/api/skimage.feature.html#skimage.feature.local_binary_pattern)
- [Brevitas 官方仓库](https://github.com/Xilinx/brevitas)
- [QKeras 官方仓库](https://github.com/google/qkeras)
- [FINN 官方文档](https://finn.readthedocs.io/en/latest/)
- [FINN 端到端流程](https://finn.readthedocs.io/en/latest/end_to_end_flow.html)
- [hls4ml 状态与后端](https://fastmachinelearning.org/hls4ml/intro/status.html)
- [hls4ml 定点与复用概念](https://github.com/fastmachinelearning/hls4ml/blob/main/docs/api/concepts.rst)

## 许可初查

scikit-image 和 scikit-learn 使用 BSD 类许可证；OpenCV 4.5 之后为 Apache-2.0；QKeras 和 hls4ml 为 Apache-2.0；FINN 为 BSD-3-Clause 类许可。软件许可不自动覆盖数据集、论文附件或预训练权重，正式复用前仍需逐项记录。

## 中断点与未完成项

- 量化 CNN/FPGA 工具的独立验证角色在调研过程中被中断，尚未提交最终交叉审查。
- 尚未选定具体小 CNN 拓扑，也未安装、下载或运行任何外部仓库。
- 尚未建立 64/144/324 HOG 与 160 LBP 的统一实验脚本。
- 尚缺当前 FPGA 综合后的剩余 BRAM/DSP/LUT 和真实可用计算周期，CNN 探索上限未转为器件门槛。
- 本草案不改变当前 fill-only T100 人工审核门禁，也不授权访问 blind reserve。

如恢复此任务，下一步应先完成独立来源复核，再新增隔离的 Python 特征消融脚本；不要直接编写 CNN RTL。
