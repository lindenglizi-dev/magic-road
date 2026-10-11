# 真实数据闭环实施状态

日期：2026-09-26

## 结论

真实数据工具链和测量入口已经就绪，但没有真实训练结论。用户排除了 `video/first`（机位与初始背景不稳定）；该素材未写入数据集。公开数据尚未取得并完成许可/标注适配，因此当前状态为 `real_dataset_ready=false`、`real_model_trained=false`。

建议但未冻结的V1目标为：行人Recall≥85%、机动车Recall≥90%、无效候选误接受率≤10%、RTL与定点Python分类不一致为0。工具不会依据这些数字自动宣布达标。

## 已实现

- 标注 manifest 新增 train/val/test、scene、源视频SHA-256、派生文件族、ROI来源和复核人；跨集合的场景、文件哈希、文件族和像素哈希均失败关闭。
- 人工标注支持 invalid；公开标注框、人工框和真实 CCL 框分别记录为 annotated/manual/ccl。
- 公开视频准备保留URL、许可URL、原始资产哈希、帧映射、几何变换和无损720p输出哈希；非720p不再静默缩放进入硬件回放。
- 训练只用train拟合，以同来源val选择C；模型、标准、ROM、对拍向量和完整manifest被冻结后，才允许一次独立test。
- 输出每类precision/recall、混淆矩阵、样本数、逐样本预测和失败清单。二分类无拒识器时，invalid误接受率明确为100%，分数不称为概率。
- CCL候选从RTL回放的灰度HEX裁剪，保留几何类别仅供诊断；没有人工复核标签就不能进入数据集。

## 仿真测量

- 原有10组RTL回归通过。
- Python与RTL的64项HOG特征逐项一致。
- 生成权重ROM、Python定点分数和RTL分数一致（合成工具链样本，仅证明工具链）。
- 新增四对象测量夹具使用真实ROI/HOG/SVM模块、一拍模拟RAM和全1测试权重：4096像素、256特征、4结果全部通过。
- 100 MHz 下，任务到最后分类结果4176周期（41.76µs）；任务到RAM释放4110周期（41.10µs）；释放后66周期产生最后结果。这支持“读完即可归还bank，分类身份另存”的判断，但未包含CDC、连续捕获和调度。
- 12帧被排除视频的诊断回放得到 EOF→对象表279–610周期、EOF→Tracker 286–617周期；第5帧起出现label overflow/core_error，因此这些数字不能作为最坏时延或算法质量结论。
- 完整连续采集下的bank占用、等待原因、真实丢帧率和HDMI延迟仍未测量。

## 验证边界

- `run_iverilog.ps1`、数据契约7项测试、HOG交叉对拍、SVM ROM/RTL自测和四对象测量夹具均通过。
- Icarus `-Wall` 仅报告既有设计模块缺少显式timescale；正式RTL没有为消除该警告而修改。
- readable-verilog严格deliverable gate及focused quality gate各运行超过两分钟无输出，已终止；因此公开矩阵中的compile/ast/readability/comment/naming/profile状态均为未取得结果，不能标为通过。
- 工具预检没有本地Vivado/xsim，也没有已确认远程服务器；新增测量夹具未综合。正式顶层和TD工程未修改，所以没有伪造新的综合/布局布线结论。

## 下一外部输入

取得公开序列后，必须先确认适用条款、下载地址、原始类别和帧号/框坐标定义。建议优先选同一类固定机位中同时覆盖人车的VIRAT地面序列，再用CDnet压力测试前景、UA-DETRAC补车辆；AI City Track3不能把未标注车辆当负样本。完成scene划分和类别映射后，按 `REAL_DATA_WORKFLOW.md` 导入并训练。
