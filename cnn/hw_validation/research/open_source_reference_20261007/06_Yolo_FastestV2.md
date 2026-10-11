# Yolo-FastestV2：可借鉴轻骨干，但不是可直接替换的 RTL

## 来源与边界

核查日期：2026-10-07；官方仓库 [`dog-qiuqiu/Yolo-FastestV2`](https://github.com/dog-qiuqiu/Yolo-FastestV2)，读取 `main` 当前页面与源码。GitHub 页面限流，未取得可复核的完整 commit SHA，因此本文以分支和日期标识版本。仓库根目录实际浏览未见 `LICENSE` 文件，README 也未声明许可证，复用代码前须向作者确认授权。README 报告 352×352、0.25M 参数、0.212G FLOPs、COCO mAP@0.5=24.10%，以及 Kirin 990/NCNN 4 核 3.29 ms、单核 5.37 ms；均是作者平台数据，不是 FPGA 成绩。

## 真实文件、层与接口

- [`model/backbone/shufflenetv2.py`](https://github.com/dog-qiuqiu/Yolo-FastestV2/blob/main/model/backbone/shufflenetv2.py)：`first_conv` 3×3/s2、max-pool/s2，ShuffleNetV2 重复数 `[4,8,4]`、通道 `24/48/96/192`；stride=1 时切半并 concat，stride=2 双分支 concat，激活 ReLU，无 CSP 残差加法。
- [`model/fpn.py`](https://github.com/dog-qiuqiu/Yolo-FastestV2/blob/main/model/fpn.py) 与 [`model/detector.py`](https://github.com/dog-qiuqiu/Yolo-FastestV2/blob/main/model/detector.py)：仅取 stride16 的 96 通道 C2 与 stride32 的 192 通道 C3；C3 上采样后与 C2 concat，两个尺度均变为 72 通道，再经 5×5 DW/PW 头。每尺度输出 reg=`4A`、obj=`A`、cls=`C`，默认 A=3；本项目两类时导出 NHWC 通道数为 `12+3+2=17`，且类别图在解码时复制给三个 anchor，并非每 anchor 独立分类。
- [`utils/loss.py`](https://github.com/dog-qiuqiu/Yolo-FastestV2/blob/main/utils/loss.py) 用 anchor 比例匹配、邻格扩展、CIoU、objectness BCE 和分类交叉熵；[`utils/utils.py`](https://github.com/dog-qiuqiu/Yolo-FastestV2/blob/main/utils/utils.py) 用 `sigmoid*2-0.5` 解中心、`(sigmoid*2)^2*anchor` 解宽高，再做 softmax、obj×cls 与 NMS。 [`pytorch2onnx.py`](https://github.com/dog-qiuqiu/Yolo-FastestV2/blob/main/pytorch2onnx.py) 仅导出 ONNX opset 11。实际浏览的官方仓库提供 PyTorch/ONNX/NCNN 示例，未见完整 CNN RTL、定点量化或 FPGA 流水实现。

把输入改为 512×288 后，两个原始输出面应为 32×18 与 16×9；两类时分别含 9792 和 2448 个标量，解码后共有 `(32×18+16×9)×3=2160` 个 anchor 候选。该接口不仅改变候选数量，还要求保存两套 anchor 常数、实现指数形态的平方宽高解码以及类相关 NMS。输入预处理也需从官方示例的 `/255` 明确转换为本项目 `pixel-128` 的有符号 INT8 约定，不能混用量化尺度。

## 与冻结 RoadYOLO 的关系

共同点是 DW/PW、concat、多尺度和整数化潜力；差异更关键：RoadYOLO 是 512×288、person/vehicle、anchor-free stride4/8/16、SiLU/CSP-PAN，67 conv、24/48/96 通道；本模型是 anchor-based stride16/32、ReLU、Shuffle split/shuffle、5×5 DW 和 softmax。删掉 stride4 会直接伤害道路小目标，不能承诺 P95/R85。作者“0.25M 参数”还大于当前 RoadYOLO 的 113,100 weights；参数更少/更多都不等于 MAC 或 100 MHz 周期更少，必须统一到 512×288、两类后重算。

可借鉴：把某个 CSP 块做成 Shuffle 分支的受控消融，或在批准重训后比较 ReLU 替 SiLU；不建议整网替换。当前 SiLU 1024 项查表仅占 1 EBRAM，不应把换激活当作首选时序修复。整换需重训/标定 anchor、重写 split/shuffle/concat、5×5 DW、softmax 与解码/NMS，并重新做 INT8 QAT、per-output-channel 权重、per-tensor activation、RNE/饱和及输入 `pixel-128` 对齐。现有 24-MAC 核只验证过 down2 小块（5433 cycle），不是完整 CNN；`layer_table` 不能因此令硬件通用。

RTL 代价还包括 ShuffleNet 的半通道旁路与物理重排。若直接落存储器重排，会增加地址生成和多 bank 冲突；若只做逻辑通道映射，则后续 PW 权重排布必须同步离线重排。5×5 DW 也不能按现有 3×3 行缓冲器无损复用，需要更深窗口或拆算，都会改变 40 DSP、108 EBRAM、21216 Slice 基线及周期。故任何“省 SiLU LUT”的收益都要与新增 shuffle/5×5/anchor decode 一起综合。

## 最小比较计划与结论

后续若获批准，先固定同一数据划分、512×288、两类和相同评价脚本，只做软件候选消融；本轮不训练、不改 RTL。导出逐层张量，统计真实 MAC、峰值 feature RAM、S4 小目标召回。仅当精度门槛通过，再选一个 Shuffle 块做 INT8 bit-true 与现有小块周期对比，最后外推全网是否可从条件估计 63.66M cycle 压到 20M。结论：仅把 ReLU/Shuffle 列为局部研究项，不接受“换 0.25M 模型即可 5 fps”的推断。

进入 RTL 的门槛应同时包含：同测试集 P≥95%、R≥85%，小目标召回不出现不可接受退化；统一口径 MAC 与逐层周期预测显示可接近 20M cycle；峰值缓存和综合后资源不超过器件预算。任何一项不满足，就保留当前 RoadYOLO，不以作者移动端速度补证。

## 简要总结

Yolo-FastestV2 可作为 Shuffle/ReLU 局部软件消融参考，但 anchor、低分辨率检测头和 5×5 数据流使其不是低成本 RTL 替代。本轮保持 RoadYOLO 与硬件不变。
