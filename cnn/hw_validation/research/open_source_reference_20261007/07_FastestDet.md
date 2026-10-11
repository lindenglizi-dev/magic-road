# FastestDet：解码简单，但单尺度 stride16 不适合作为道路小目标直接替代

## 来源与边界

核查日期：2026-10-07；官方仓库 [`dog-qiuqiu/FastestDet`](https://github.com/dog-qiuqiu/FastestDet)，读取 `main` 源码。GitHub 限流下未稳定取得 commit SHA，以分支和日期为版本。许可证为 [`BSD-3-Clause`](https://github.com/dog-qiuqiu/FastestDet/blob/main/LICENSE.md)。README 报告 352×352、0.24M 参数、COCO AP50=25.3%、AP50:95=13.0%，RK3568 CPU/NCNN 4 核 23.51 ms、单核 70.62 ms；这些是作者 CPU 结果，不是本机或 FPGA 测量。

## 真实文件、层与接口

- [`module/shufflenetv2.py`](https://github.com/dog-qiuqiu/FastestDet/blob/main/module/shufflenetv2.py)：3×3/s2、max-pool/s2，stage 重复 `[4,8,4]`、输出 `48/96/192`；主支为 PW-ReLU→3×3 DW→PW-ReLU，stride1 做通道切半/重排后 concat，stride2 做双分支 concat。
- [`module/detector.py`](https://github.com/dog-qiuqiu/FastestDet/blob/main/module/detector.py)：取 stride8/16/32 的 P1/P2/P3，把 P1 平均池化到 stride16、P3 最近邻上采样到 stride16，三者 concat 后送入 96 通道 SPP，因此最终只有一个检测尺度。
- [`module/custom_layers.py`](https://github.com/dog-qiuqiu/FastestDet/blob/main/module/custom_layers.py)：所谓 SPP 实为三条 5×5 depthwise 链（1/2/3 层）concat，再 1×1 投影并与输入相加、ReLU；检测头再做 5×5 DW+1×1。输出 NCHW 为 `[N,5+C,H/16,W/16]`，两类即 `[N,7,18,32]`（512×288，若按 PyTorch NCHW 的 H=288、W=512）。通道依次为 obj、4 个回归量、C 类；anchor-free、无 DFL。
- [`module/loss.py`](https://github.com/dog-qiuqiu/FastestDet/blob/main/module/loss.py) 将一个 GT 扩到邻近四格，以 SIoU、类别 NLL、IoU-aware SmoothL1 objectness 训练；[`utils/tool.py`](https://github.com/dog-qiuqiu/FastestDet/blob/main/utils/tool.py) 用 `tanh` 解中心偏移、`sigmoid` 解归一化宽高，分数为 `obj^0.6*max(cls)^0.4`，再 batched NMS。 [`test.py`](https://github.com/dog-qiuqiu/FastestDet/blob/main/test.py) 和 [`example/onnx-runtime/runtime.py`](https://github.com/dog-qiuqiu/FastestDet/blob/main/example/onnx-runtime/runtime.py) 给出 ONNX opset11/TorchScript 与同样预后处理。实际浏览未见完整 CNN RTL、量化训练或 FPGA 部署源码。

512×288 时单尺度只有 32×18=576 个候选，两类原始输出仅 4032 个标量，确实比 RoadYOLO 三尺度后处理轻。但回归的宽高是整幅图归一化 sigmoid，不是当前候选的距离/边界形式；置信度还含非整数幂 `0.6/0.4`。若 FPGA 只输出原始张量给 CPU，需把带宽和软件时延计入；若硬件解码，则要为 tanh、sigmoid、幂运算和 NMS 定义近似误差，不能把“输出少”直接等同为完整链路更快。

## 与冻结 RoadYOLO 的关系

共同点是 anchor-free、DW/PW、concat/残差和轻量头；差异是 RoadYOLO 保留 stride4/8/16 三尺度及 SiLU/CSP-PAN，而 FastestDet 把所有特征压到 stride16，使用 ReLU、channel shuffle、5×5 DW、平均池化、tanh 和 softmax。对 person/vehicle 的远处小目标，取消 S4/S8 很可能降低召回，不能承诺 P95/R85。其约 0.24M 参数也大于 RoadYOLO 的 113,100 weights；单尺度输出小不代表 backbone MAC 小，必须统一 512×288/两类后统计。

最值得借的是“单点 `[obj,box,cls]` 输出+简单网格解码”，仅可列为后续获批后的 head-only 软件消融候选，本轮不实施；不宜直接换整网。head 替换仍需重训、阈值重标定、实现 tanh/sigmoid/softmax或等价近似，并重验 INT8 零点0、per-channel weight、per-tensor act、RNE饱和和 INT32 final。现有 down2 小块测得 5433 cycle，但验证核不是完整 CNN；Shuffle、add/concat、5×5 DW 不能只靠 `layer_table` 获得支持。

硬件上可先保留分数融合和 NMS 在软件端，RTL 只验证 `[obj,reg,cls]` 原始输出，这是一条可撤销的小改动；但 5×5 DW 行缓冲、P1 平均池化、P3 上采样、三路 concat 与 SPP 残差仍是新数据流。尤其三尺度先对齐再融合会抬高 feature RAM 峰值，必须在 108 EBRAM 预算下按生存期排程。ReLU 可删除 SiLU1024查表，却不足以抵消这些结构成本；应以综合后的 40 DSP/21216 Slice/100 MHz 和实测周期判断。

## 最小比较计划与结论

若后续获批，在同一 Road 数据与 512×288 上先保留 RoadYOLO backbone/neck，仅做 FastestDet 风格两类 head 的软件训练消融；同时保留原 head 对照，比较 AP、P/R、S4 小目标分桶和输出后处理耗时。通过精度门槛后，再做该 head 的逐层 INT8 bit-true、综合和周期测量；若仍无法由 63.66M 降至 20M，再评估缩通道，而不是先移除小目标尺度。结论：可研究 head 解码，不建议把官方单尺度整网当作低风险替代。

上述比较计划只是建议，须批准后执行。进入 RTL 的门槛是同测试集 P≥95%、R≥85%，远处 person/vehicle 召回可接受，且统一统计显示总周期有希望低于 20M、资源不越界；否则单尺度输出再小也不能替代当前三尺度检测。作者 NCNN 数字只用于说明软件可部署性。

## 简要总结

FastestDet 的单点 head 和解码最值得软件比较，但单尺度 stride16 对道路小目标风险过高。未经统一训练、精度和周期验证，不替换 RoadYOLO，也不修改 RTL。
