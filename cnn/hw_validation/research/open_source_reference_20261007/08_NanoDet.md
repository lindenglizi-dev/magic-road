# NanoDet-Plus：训练与特征融合参考价值高，硬件替换成本最高

## 来源与边界

核查日期：2026-10-07；官方仓库 [`RangiLyu/nanodet`](https://github.com/RangiLyu/nanodet)，`main` 页面可见最新提交短 SHA `be9b4a9`（2024-01-08），本文据该分支源码；许可证为 [`Apache-2.0`](https://github.com/RangiLyu/nanodet/blob/main/LICENSE)。README 报告 NanoDet-Plus-m-416（ShuffleNetV2 1.0x）COCO mAP@0.5:0.95=30.4、1.52G FLOPs、1.17M 参数；320 版 mAP@0.5:0.95=27.0、0.9G、1.17M。97 fps/10.23 ms 是作者移动 ARM/NCNN口径，不是 FPGA 结果。

## 真实文件、层与接口

- [`config/nanodet-plus-m_416.yml`](https://github.com/RangiLyu/nanodet/blob/main/config/nanodet-plus-m_416.yml) 才是可复现结构入口：ShuffleNetV2-1.0x 输出 `116/232/464`，激活 LeakyReLU；GhostPAN 统一 96 通道、5×5 depthwise，并增加一级，检测 strides=`[8,16,32,64]`、`reg_max=7`。训练时另有 192 通道辅助头，推理不保留。
- [`nanodet/model/backbone/shufflenetv2.py`](https://github.com/RangiLyu/nanodet/blob/main/nanodet/model/backbone/shufflenetv2.py)：stride1 将输入 chunk 为两半，仅计算一半，concat 后执行显式 channel shuffle；stride2 双分支 concat。它没有 CSP 结构，默认配置也没有残差 add。
- [`nanodet/model/fpn/ghost_pan.py`](https://github.com/RangiLyu/nanodet/blob/main/nanodet/model/fpn/ghost_pan.py)：1×1 reduce，top-down 上采样+concat、bottom-up 5×5 DW 下采样+concat，GhostBottleneck 生成廉价特征；额外层以两路 stride2 结果相加。
- [`nanodet/model/head/nanodet_plus_head.py`](https://github.com/RangiLyu/nanodet/blob/main/nanodet/model/head/nanodet_plus_head.py)：每尺度两层 5×5 DW/PW，1×1 输出 `C+4*(reg_max+1)`；两类、reg_max=7 时每点 34 通道。四尺度展平后为 `[N,sum(Hs*Ws),34]`。它是 anchor-free point prior，但框为四边 8-bin 分布，经 softmax/Integral 得距离、乘 stride 后转 xyxy；分类 sigmoid，再 multiclass NMS。损失是 QFL+DFL+GIoU，正样本由 DynamicSoftLabelAssigner 分配。 [`tools/export_onnx.py`](https://github.com/RangiLyu/nanodet/blob/main/tools/export_onnx.py) 导出/简化 ONNX opset11。实际浏览官方仓库未见完整 CNN RTL 或面向安路器件的定点流水。

按 512×288 和 ceil 对齐估算，stride8/16/32/64 分别是 64×36、32×18、16×9、8×5，共 3064 个 point；两类原始 head 为 104176 个标量。分类只占 6128 个，其余 98048 个是四边 8-bin 分布。DFL 的价值在训练和定位表达力，而在本项目中会显著增加输出写回、softmax 与乘加；若保留当前直接框回归，这部分硬件成本可完全避免，因此不能未经消融就整头照搬。

## 与冻结 RoadYOLO 的关系

共同点是 anchor-free、多尺度、DW/PW、PAN 式 concat；差异是 RoadYOLO 为 stride4/8/16、24/48/96、SiLU/CSP，NanoDet-Plus 默认 stride8 起步、116/232/464 backbone、96 通道 GhostPAN、LeakyReLU、shuffle、Ghost、add 和 DFL。对道路小目标，缺少 S4 可能显著降召回；DFL 又把两类 head 从直接框回归扩为 34 通道并增加 softmax/加权求和，RTL 与带宽压力明显。1.17M 参数约为 RoadYOLO 113,100 weights 的十倍，不能因“Nano”名称推断 MAC/周期更低；必须统一为 512×288、两类并实算。

可借鉴的是 DSLA/QFL/DFL 的软件训练消融、GhostPAN 的融合思想；这些仅是后续获批后的软件消融建议，本轮不训练、不改 RTL。最小风险优先只借动态分配/QFL，不改推理图。若换 backbone/neck/head，则需重训和 INT8 QAT，并新增 shuffle、LeakyReLU、Ghost 分支、add、5×5 DW、四尺度 DFL decode/NMS；现有 24-MAC 仅有 down2 小块 5433-cycle 证据，并非完整 CNN。已验证的数值边界是有符号 33 位中间和、每路最多 192 个有效乘积、分 24 组并对末组做 INT32 检查，不能误写成位宽；这些证据不能直接继承到新算子，`layer_table` 也不能令核自动支持。

数值接口也不兼容：官方配置输入按 BGR 均值/方差归一化，而冻结链路是 `pixel-128`；LeakyReLU 负半轴、DFL softmax 概率与积分距离都需要新的定点误差预算。Ghost 模块的廉价特征通常依赖 concat 和后续混合，不能只数卷积权重；额外层的两路 add 还要求量化 scale 对齐。在 40 DSP、108 EBRAM、21216 Slice、100 MHz 约束下，应先把这些算子逐块建模，再决定是否值得牺牲现有已验证的 SiLU/3×3 数据通路。

## 最小比较计划与结论

若后续获批，第一阶段保持 RoadYOLO 推理结构，只做原分配损失与 DSLA/QFL 的 FP32 软件比较；第二阶段才做 96 通道 GhostPAN 单块或 DFL head 单独消融，统一 512×288/两类，统计 MAC、峰值 RAM、S4 小目标召回和导出算子。候选通过 P/R 后再逐层做量化误差、bit-true、综合资源与周期，目标仍是从条件估计 63.66M cycle 降到 20M。结论：NanoDet 更适合作为训练/融合参考，不是当前 100 MHz、40 DSP、108 EBRAM 预算下的快捷整网替换。

该计划须另行批准，本轮不执行。只有同测试集达到 P≥95%、R≥85%，小目标分桶无明显退化，并且量化后 DFL/GhostPAN 的实际周期、缓存和综合资源均满足 20M cycle 与器件预算，才进入 RTL 原型；否则只保留不改变推理图的训练方法。移动端 mAP/FPS 不能替代这些门槛。

## 简要总结

NanoDet-Plus 最适合作为 DSLA/QFL/GhostPAN 的训练与融合参考；DFL、四尺度和新算子使整网 RTL 迁移成本最高。本轮不训练、不改 RTL，优先保留不改变推理图的方法。
