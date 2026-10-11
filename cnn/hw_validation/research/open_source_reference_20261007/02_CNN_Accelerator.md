# CNN_Accelerator：DW/PW 源码核查与复用边界

## 来源、日期、许可证与成熟度

- 主来源：[仓库与 README](https://github.com/georgejesswin/CNN_Accelerator)，核查日期 2026-10-07，分支 `main`。本轮无法稳定取得最新 commit hash，按访问日分支快照记录。
- 根目录未发现 LICENSE，GitHub 也未显示许可证；在作者补充许可前，代码只能阅读、不能直接复制进比赛工程。仓库约 15 次提交、0 star，未见 testbench、CI、综合/时序/资源报告；成熟度按未验证 RTL 草案。

## 真实目录与重点文件

工程没有子目录，Verilog 均在根目录；README 所称 `conv_dw_pw_top.v`、`pointwise_layer_stream.v` 等与真实文件名不完全一致。关键文件为：

- [`conv_dw_pw.v`](https://github.com/georgejesswin/CNN_Accelerator/blob/main/conv_dw_pw.v)：DW→PW 直连顶层。
- [`depthwise_conv.v`](https://github.com/georgejesswin/CNN_Accelerator/blob/main/depthwise_conv.v)：逐通道实例窗口和 3×3 MAC，外包一拍 AXIS 输出寄存器。
- [`depthwise_image_control.v`](https://github.com/georgejesswin/CNN_Accelerator/blob/main/depthwise_image_control.v)：双行缓冲和 3×3 窗口。
- [`depthwise_mac.v`](https://github.com/georgejesswin/CNN_Accelerator/blob/main/depthwise_mac.v#L118-L156)：9 乘法、32-bit 加法树、直接 INT8 饱和。
- [`pointwise_conv.v`](https://github.com/georgejesswin/CNN_Accelerator/blob/main/pointwise_conv.v)、[`pointwise_fsm.v`](https://github.com/georgejesswin/CNN_Accelerator/blob/main/pointwise_fsm.v)、[`pointwise_mac`](https://github.com/georgejesswin/CNN_Accelerator/blob/main/pointwise_mac)、[`pointwise_weight.v`](https://github.com/georgejesswin/CNN_Accelerator/blob/main/pointwise_weight.v)：PW 分块控制、MAC 树和权重块 RAM。

## 数据流、量化与握手核查

README 的默认 PAR16×16 意味着 256 个并行乘法，不是当前 24MAC。DW 每通道并行 9 乘法，16 通道即 144 个；若一乘法映射一 DSP，显然超过 40 DSP，但实际 LUT/DSP 分配尚未综合，不能写成实测资源。源码无 bias、scale、RNE；DW 32-bit 求和后[直接裁剪到 INT8](https://github.com/georgejesswin/CNN_Accelerator/blob/main/depthwise_mac.v#L130-L156)，PW 64-bit 累加后同样直接饱和，不能满足当前“每路≤192 有效乘积、24 组汇总 INT32、RNE、饱和、SiLU1024 LUT”的契约。

README 声称 backpressure-safe，但源码不足以支持：DW 只用输出寄存器 `valid&&!ready` 阻止新输入，[MAC valid 流水却不随 stall 停止](https://github.com/georgejesswin/CNN_Accelerator/blob/main/depthwise_conv.v#L60-L66)，已有在途结果会继续到达，却因 stall 分支只保持旧输出而[无法被捕获](https://github.com/georgejesswin/CNN_Accelerator/blob/main/depthwise_conv.v#L105-L136)。PW FSM 在 IDLE 只看 `s_axis_tvalid` 跳转，下一拍 LOAD 才锁数据；`ready=IDLE`，[采样并未显式绑定 `valid&&ready`](https://github.com/georgejesswin/CNN_Accelerator/blob/main/pointwise_fsm.v#L68-L76)，若上游按握手后撤数据会锁错。

另有确定宽度问题：顶层声明 `feature_full_reg` 为 `CIN*DATA_W` 并随后做全宽动态切片，但 FSM 的 `feature_vec/feature_reg` 只有 `PAR_CIN*DATA_W`，[默认 CIN32/PAR16 会被截断](https://github.com/georgejesswin/CNN_Accelerator/blob/main/pointwise_fsm.v#L20-L27)；连接与切片见 [`pointwise_conv.v` 57–108 行](https://github.com/georgejesswin/CNN_Accelerator/blob/main/pointwise_conv.v#L57-L108)。迭代数虽用 ceil、COUT 写回有边界判断，但 CIN 尾块没有显式零化；非整除通道会越界或混入无效 lane。

## 与 RoadYOLO 的相同与差异

相同点是真 DW3×3+PW1×1、INT8、行缓冲、通道分块，概念上最接近当前小块。差异是它固定一像素全通道向量、无 stride2/halo 契约、无 SiLU/偏置/尺度/RNE，并且接口与数值均未闭环。将并行度缩成 8×3 时，16→24 这一个小块可整除，但全网的 stem 3、branch 12、head 2/5 等仍需 ceil、尾 lane 清零和输出 mask，不能据此直接参数化通吃。

## 采用分级与省时建议

- **可直接用：无**（许可缺失且握手/位宽有阻断问题）。
- **需移植：** 仅可重写其 PW 分块计数思想；必须以当前 INT32/RNE/饱和契约为准。
- **仅理念：** 行缓冲、weight tiling、输出通道 mask。
- **最省时优化：** 不换核；沿用现有 MAC lane mask，先核对全图分块计数、CIN 尾输入置零、COUT 尾写 mask 是否覆盖 stem 3、branch 12、head 2/5，仅补缺口；对 `valid&&ready` 建断言。63,662,586 cycle 仅为当前条件外推，不是已知整网实测；没有真实层 cycle 证据不做 systolic/跨像素重构。

## 未验证风险与下步最小验证

以上握手风险是静态推断，本轮未运行仿真、综合或板测；八项门禁均未执行。最小验证是写一个三拍反压波形：在 DW 流水有多项在途时拉低 `m_ready`，断言输出数据稳定且每项恰好一次；再用 CIN=17、COUT=5 暴露截断/尾 lane。任一失败即可确认“不直接复用”，无需先适配 PH1P。

## 简要总结

该仓库的 DW/PW 分块概念有参考价值，但握手、位宽和数值尚有阻断风险，不能直接作为 RoadYOLO 的 AXIS 或数值实现。
