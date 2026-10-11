# road_mac_probe 规范

## 1. 模块目的

`road_mac_probe` 接收三输出通道、每通道八项的 signed INT8 乘加组。单个归约序列允许每拍输入一组，`last` 后等待一个保持型终态输出。

## 2. 接口

接口与冻结参考同名同宽：`i_clk`、异步低有效 `i_rstn`、输入 ready/valid、`first/last`、8 位 lane mask、64 位激活、192 位权重、96 位 bias，以及输出 ready/valid、96 位结果和原子 fault。

## 3. 数值行为

每路点积为八个受 mask 控制的 signed8 × signed8 乘积之和，归约宽度依次为 16、17、18、19 位。A5 以 signed33 历史值或 `first` 对齐的 signed32 bias 符号扩展值作为基值，做 signed34 加法并正常写回 signed33。只有 `last` 检查 signed INT32；任一路越界时 fault 为 1 且三路输出为零。

## 4. 周期行为

- A0：输入握手与负载锁存。
- A1：24 路乘积寄存。
- A2/A3/A4：两项、四项、八项归约。
- A5：三路跨组累加，末组锁存终态。
- A6-A8：终态合法对齐。
- A9：`o_result_valid` 与结果/fault 可见。

接受 `last` 后 `o_input_ready` 变低，并保持到结果握手。输出背压期间 payload 稳定。复位时 ready 为 1、valid 为 0。

## 5. 边界条件

- 全 mask 关闭时点积为零。
- `first=0` 合法地继续历史累加，复位后的历史值为零。
- `first=1` 替代历史值而不是与历史值相加。
- 上层负责 signed33 有限范围；本模块不增加非末组 fault 口径。

## 6. 验证场景

连续 24 组、带空泡输入、正负 INT8、部分/全 mask、first0/first1、末组 INT32 正负越界、输出背压、流水中异步复位。

## 7. WaveDrom

规范波形见 `road_mac_probe_timing.json5`。其中 `L` 为 last 输入，`R` 为握手后的保持结果。

