# ConvKing2022：对 RoadYOLO 的可用边界

## 来源、日期、许可证与成熟度

- 主来源：[仓库](https://github.com/redlightASl/ConvKing2022)、[README](https://github.com/redlightASl/ConvKing2022/blob/master/README.md)、[MIT LICENSE](https://github.com/redlightASl/ConvKing2022/blob/master/LICENSE)，核查日期 2026-10-07，分支 `master`。GitHub 本轮未稳定返回最新 commit hash，因此本文不伪造固定版本号。
- README 明说目标是把“修改后的 MobileNetV2-YOLOv3”部署到 PGL22G，但[没有完成整套部署且缺少可用互联](https://github.com/redlightASl/ConvKing2022/blob/master/README.md#L3-L15)。这只是作者的网络命名，不能自动等同某个官方 YOLOv3-Nano 实现。仓库仅 3 次提交、无发布版本；成熟度应按竞赛原型/参考代码，而非可替换 IP。

## 真实目录与重点文件

README 的目录示意写有 `rtl`，但仓库根实际可见的是 `algorithm/`、`dataset/`、`doc/`、`project/ConvKing/`、`report/复赛资料/`、`tools/`；真实 RTL 位于 `project/ConvKing/source/`。重点是：

- [`Accelerator/Conv/conv_top.v`](https://github.com/redlightASl/ConvKing2022/blob/master/project/ConvKing/source/Accelerator/Conv/conv_top.v#L1-L166)：卷积 FSM 与 buffer/search/cal 串接。
- [`conv_buffer.v`](https://github.com/redlightASl/ConvKing2022/blob/master/project/ConvKing/source/Accelerator/Conv/conv_buffer.v)：从整幅打包向量取窗。
- [`conv_cal.v`](https://github.com/redlightASl/ConvKing2022/blob/master/project/ConvKing/source/Accelerator/Conv/conv_cal.v#L37-L88)：调用 `mult_add` IP、保存结果并加偏置。
- [`mobilenet_invres.v`](https://github.com/redlightASl/ConvKing2022/blob/master/project/ConvKing/source/Accelerator/mobilenet_invres.v) 与 [`mobilenet_top.v`](https://github.com/redlightASl/ConvKing2022/blob/master/project/ConvKing/source/Accelerator/mobilenet_top.v)：当前只是空端口壳实例。
- [`Bridge/axi/aq_axi_master.v`](https://github.com/redlightASl/ConvKing2022/blob/master/project/ConvKing/source/Bridge/axi/aq_axi_master.v#L340-L383)：独立 AXI master 模板，不等于 CNN 已接通。

## 数据流、接口、量化与握手

`conv_top` 的输入是整幅 packed `img`、packed `weight`、窄 `bias`，控制为 `conv_en/conv_fin`，并非像素流 ready/valid；接口证据见[端口 22–27 行](https://github.com/redlightASl/ConvKing2022/blob/master/project/ConvKing/source/Accelerator/Conv/conv_top.v#L22-L27)。`conv_cal` 只保留 24-bit `data_link`，再截成参数化窄结果后直接加零扩展 bias，[没有 RoadYOLO 所需的 signed 33-bit 中间、INT32 bias、RNE 与饱和](https://github.com/redlightASl/ConvKing2022/blob/master/project/ConvKing/source/Accelerator/Conv/conv_cal.v#L37-L78)。

AXI 模板存在伪握手风险：读状态在 `M_AXI_RVALID` 即推进，而 `RD_FIFO_WE=M_AXI_RVALID`；即使 `RD_FIFO_FULL` 令 `RREADY` 下降，状态/写使能仍可变化，见[346、380–383 行](https://github.com/redlightASl/ConvKing2022/blob/master/project/ConvKing/source/Bridge/axi/aq_axi_master.v#L346-L383)。这是静态源码推断，本轮未仿真。

## 与 RoadYOLO 的相同与差异

相同点是集创赛、CNN/YOLO、INT 量化与卷积模块化背景，但板卡和厂商并不相同：ConvKing 使用紫光同创 PGL22G，当前工程使用安路 PH1P35。RoadYOLO 已冻结 512×288、two-class anchor-free、stride 4/8/16、DW/PW CSP、SiLU、INT8 zero=0，并已有 24MAC（8 输入×3 输出）与精确数值契约；本工程既非该图结构，也没有对应 DW/PW、SiLU LUT 或尾 lane 规则。

## 采用分级与省时建议

- **可直接用：无。** MIT 只解决法律许可，不解决接口、数值和时序正确性。
- **需移植：** 最多参考其工程分层或量化脚本组织；RTL 必须重写接口和数值路径。
- **仅理念：** packed 小规模卷积 FSM、主机侧量化流程。
- **最省时优化：** 不移植 ConvKing 数据通路；保留当前 8×3 核，只把现有串行 MAC 任务调度和后处理按全网 cycle 表逐项削减。若要借鉴，先只提取一项权重排列规则并用当前 golden 数据验证，绝不引入其 AXI master。

## 未验证风险与下步最小验证

未运行其 RTL、TestBench、综合或板测；`mult_add`/Pango IP 参数、符号性、溢出和 PH1P35MDG324 映射均未确认。八项门禁 `compile/ast/readability/comment/naming/profile/testbench/toolchain` 本轮均为未执行，不代表通过。最小验证仅应做：对 `conv_cal` 构造正负极值与偏置向量，证明其结果不能满足当前 INT32+RNE+饱和契约；结论成立即停止移植。

## 简要总结

ConvKing2022 适合作为“同类竞赛为何卡在互联”的反例和组织参考，但板卡、厂商、接口和数值均不同，不是 RoadYOLO 的直接加速核候选。
