# IBM AccDNN：旧式 Caffe→RTL 编译器的可借鉴范围

核查日期：2026-10-07。对象为 IBM/AccDNN，固定到归档分支提交 [`932579548283a9f2da3f366e131e37c48ac58eaf`](https://github.com/IBM/AccDNN/tree/932579548283a9f2da3f366e131e37c48ac58eaf)。仓库声明 [Apache-2.0](https://github.com/IBM/AccDNN/blob/932579548283a9f2da3f366e131e37c48ac58eaf/LICENSE)，但已于 2024-07-18 被所有者归档。本轮仅源码阅读，未安装 Ristretto Caffe、未运行 codegen、仿真或 Vivado，因此成熟度结论是“有论文和示例的历史研究工具”，不是当前环境已复现工具链。

## 源码事实，不只看 README

[README](https://github.com/IBM/AccDNN/blob/932579548283a9f2da3f366e131e37c48ac58eaf/README.md)明确限制：输入必须是 Caffe；仅支持卷积、maxpool、全连接、BN；卷积+全连接少于 15 层；生成流程测试于 Vivado 2017.4，而示例仿真只支持 Vivado 2013.4。源码还有 Python 2 痕迹（`ConfigParser`、无括号 `print`）。这些依赖足以排除“直接对接当前 PyTorch RoadYOLO”。

更关键的是 [`model.py`](https://github.com/IBM/AccDNN/blob/932579548283a9f2da3f366e131e37c48ac58eaf/model.py)：解析器只实例化 `Convolution/ConvolutionRistretto`、`InnerProduct/FcRistretto`、`Pooling`；BN、Scale、ReLU 被融合到上一层，其他类型直接 `raise Layer type ... is not supported`。源码没有 Depthwise、SiLU、Concat、Upsample 分派。虽然普通 convolution 接收 `group`，也不能据此宣称已正确支持当前 DW、channel concat、residual、nearest-upsample 与 anchor-free head。

量化契约同样不匹配。[`layers/layer.py`](https://github.com/IBM/AccDNN/blob/932579548283a9f2da3f366e131e37c48ac58eaf/layers/layer.py)只记录 `input_dw/input_dq/param_ww/param_wq/output_dw/output_dq` 的定点位宽和 Q 位；README 支持 activation 8/16 bit、weight 4/8/16 bit，并要求 8-bit 双乘场景的 KPF 与 kernel 数为偶数。它不是当前“每输出通道 weight scale + per-tensor activation + zero-point 0 + RNE/saturation + SiLU 表”的导出器。

## 真实目录/产物职责

| 路径 | 可核实职责 |
|---|---|
| [`codegen.py`](https://github.com/IBM/AccDNN/blob/932579548283a9f2da3f366e131e37c48ac58eaf/codegen.py) | 校验 prototxt/caffemodel/优化文件，调用解析、自动并行度、COE/IP/RTL/清单/时序生成；会清空既有 build 输出，故本轮未运行。 |
| [`model.py`](https://github.com/IBM/AccDNN/blob/932579548283a9f2da3f366e131e37c48ac58eaf/model.py) | 网络解析、层连接、CPF/KPF 自动优化、DDR 带宽/资源 profile、权重 COE/bin、file list；源码也生成 multicycle 约束，本轮只记录其存在，**不移植任何 multicycle 约束**。 |
| [`layers/`](https://github.com/IBM/AccDNN/tree/932579548283a9f2da3f366e131e37c48ac58eaf/layers) | 只有 convolution、innerproduct、pooling 和基类；按层生成专用 Verilog。 |
| [`lib/verilog/`](https://github.com/IBM/AccDNN/tree/932579548283a9f2da3f366e131e37c48ac58eaf/lib/verilog) | 地址、位截断、BN/bias/ReLU、控制和总线宽度转换等旧 Xilinx RTL 库。 |
| 生成 `build/` | `src/model.v`、`coe/`、`timing/`、`ips.tcl`、`imp_file.f`、`file_list.txt`；这是生成物组织规范，不是现成 RoadYOLO RTL。 |

其性能思想是按层选择 CPF（并行输入通道）和 KPF（并行输出核），让流水层延迟接近；profile 同时报 DDR 带宽、DSP、BRAM，并允许每个带权层设置 0–2 拍 DMA delay。优点是“资源预算—并行度—带宽”一起看；风险是它偏向少于 15 个主层、每层专用硬件和多 DMA 通道，与当前 67 卷积、仅 40 DSP/108 ERAM 的时分复用执行机差异很大。

## 对 RoadYOLO 的具体取舍

- **直接复用：无。** 仓库有 Apache-2.0 声明，但当前没有一项能在不改接口、算子和数值契约的情况下直接接入。
- **需移植：** 把 CPF/KPF 配置表简化成现有调度器的每层 `cin_tile/cout_tile` 与预计读写字节，输出一张“MAC 拍、halo/行填充拍、DDR 拍、postprocess 拍”的静态表；不要移植 Caffe 解析和 Verilog 生成器。
- **理念复用：** profile 必须拒绝“需求带宽大于实测 PAXI 带宽”的候选，并单列权重装载、层间可见性和 DMA delay；这可帮助定位 63,662,586 拍预算中真正的等待项。
- **不适合替代：** 当前 `graph.py` 已有 split/concat/nearest/residual 虚拟视图和递归地址映射，无需重做 AccDNN 式通用编译器；AccDNN 也没有所需 SiLU、DW、concat、upsample 和纯 FPGA NMS。

最小验证：只选一个 16ch DW3×3/s2 + PW16→24 层，把现有冻结图导出的尺寸/步长/量化参数喂给简化 profile；预测值必须与 5,433 拍实测逐项对账，误差来源可归入 MAC、RAM、PAXI 或后处理。随后再对三种尺度各测一层；在误差稳定前，不用自动优化结果承诺 5 FPS。

## 简短总结

AccDNN 值得抄的是按层并行度与 DDR/资源联合报表，不值得抄的是过时的 Caffe→通用 RTL 工具链；它不能即插即用，也不能补齐当前算子和数值契约。
