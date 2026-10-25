# RGB halo 复用完整前三层验证报告

## 结论

冻结 RGB 复用 RTL 哈希 `50c803465badfe9b57a34cc803d1d30d85830d9ba00191be756b480b9f748214`、testbench 哈希 `5fc435dcf20072ed5b1e1f346bd14784f56065964a42a8db35aafb2d72035ba3` 下，原八例与新增两例共十例均得到预期收据。状态为 **S1_FUNCTIONAL_PASS_PHYSICAL_PREPARED_NOT_RUN**：完整受控 memory endpoint 功能已通过，S1 物理实现尚未运行。

normal 端点总周期为 **15,848,967**，相对未复用基线 17,252,079 精确减少 1,403,112 拍；这与 350,778 次直接推进、每次跳过四个映射状态相符。DDR 读写量保持 97,564/78,336，未以减少 DDR 读请求换取周期下降。

## 完整成功结果

| Case | 结果 | 端点总周期 | 写 | 读 | PW bytes | 十项互斥 bin |
|---|---|---:|---:|---:|---:|---|
| normal | PASS | 15,848,967 | 78,336 | 97,564 | 221,184 | 1, 138240, 2158, 1601676, 10914048, 776448, 1117948, 972288, 290880, 35280 |
| random backpressure | PASS | 16,311,442 | 78,336 | 97,564 | 221,184 | 1, 211645, 2158, 1735186, 10914048, 873369, 1240424, 972288, 327043, 35280 |
| 512-cycle request stall | PASS | 15,849,479 | 78,336 | 97,564 | 221,184 | 1, 138240, 2158, 1602188, 10914048, 776448, 1117948, 972288, 290880, 35280 |
| four-point reset cancel/recover | PASS | 15,848,967 | 78,336 | 97,564 | 221,184 | 1, 138240, 2158, 1601676, 10914048, 776448, 1117948, 972288, 290880, 35280 |
| real core-load stall 257 | PASS | 15,849,224 | 78,336 | 97,564 | 221,184 | 1, 138240, 2158, 1601933, 10914048, 776448, 1117948, 972288, 290880, 35280 |
| core-load stall/reset/recover | PASS | 15,848,967 | 78,336 | 97,564 | 221,184 | 1, 138240, 2158, 1601676, 10914048, 776448, 1117948, 972288, 290880, 35280 |

每个完整成功用例均核对 halo 1,306,368 项，acc/pre/SiLU/post 各 958,464 项；所有写地址按三个独立范围逐项匹配并用 seen 检查唯一性和洞。每行十项 bin 的和严格等于该行端点总周期。复位用例只报告清空后最后完整一代，取消前缀不混入周期或 bin。

## S1 边界与真实握手覆盖

每个完整成功用例均精确观测 350,778 次合格 RGB 直接推进、20,672 次 lane15 跨词回退、10,336 个 R14/G15/B0 像素和 10,336 个 R15/G0/B1 像素。tile0 的真实 DDR 返回数据定向确认 halo 33/34/35 的 R/G/B 归一化值为 `0x91/0x80/0x87`。

case8/9 同时 force 真实 Stem loader 的 `o_load_ready` 与 accept；背压期间内外 accept 均为0，完整 payload、halo cursor、channel、lane 和 line address 逐拍保持。case9 在该背压状态共同复位，检查 halo cursor、cache、table loaded 与夹具世代状态清零，再完成一次无泄漏整层运行。

## 故障闭锁结果

| Case | 预期结果 | 实际端点周期 | 证据 |
|---|---|---:|---|
| response error | status2/error7 | 144,425 | 首个读响应错误闭锁，禁止成功。 |
| dropped response | status2/error9 | 644,423 | 首个读响应丢失后由无进展看门狗闭锁。 |
| post-PASS DDR fault | status1→status2/error1 | 15,848,967 | 先完成全部 `check_success`，再注入 fault 并撤销 valid/ready。 |
| corrupt RGB read data | status2/error4 | 149,828 | 首个 RGB 128-bit beat 整拍取反；最终输出黄金比较由 DUT 自身闭锁。 |

整拍取反与单独损坏 bit0 不等价：早期基线诊断中的 bit0 微扰可能被量化路径消去，因此不构成“错误数据一定闭锁”的充分激励；本正式 case7 使用整拍取反，且关闭预期会被破坏的中间数值监视，避免让 TB 的预期 mismatch 冒充 DUT 捕获。

## 工具与八门证据

十例均由 ModelSim SE-64 2020.4 重新编译并运行。编译记录为 0 error/0 warning；仿真优化阶段只保留厂商 `ph1p_logic_eram.v:165` 的两条 `INIT_FILE` 越界 warning。编译闭包包含冻结 loader/sequence、复用八核、TB、`PH1P_PHY_GSR` 和 `PH1P_LOGIC_ERAM`。

仅 TB 的 readable-verilog 八门报告保存在 `tb_gate.json/.md`：`compile=passed`、`ast=passed`、`readability=passed`、`comment=failed(153)`、`naming=passed`、`profile=passed`、`testbench=not_requested`、`toolchain=not_requested`。153 项均是参数、信号、always、instance、task/port 未逐项添加规定的邻接解释注释；这是如实保留的静态注释门失败，不覆盖实际 ModelSim 功能收据。为保持已验证 TB 哈希，未用无关注释改写触发十例重跑。

## 源码与输入闭包

`suite_manifest.json` 绑定最终 TB、runner、RGB 复用 RTL、S1 reference、原 contract/generator 哈希及十个正式 case。每个 `receipt.json` 进一步记录全部编译源码、两份厂商模型、全部输入向量、机械转换向量、执行命令和哈希；`loop_table.hex` 与 `loop_parameters.hex` 均复制到独立运行目录。

本报告只证明受控 memory endpoint 上的完整前三层 RTL 行为。它不是 DDR 厂商协议模型、S1 综合/P&R、板卡、Flash、训练或部署验收证据。
