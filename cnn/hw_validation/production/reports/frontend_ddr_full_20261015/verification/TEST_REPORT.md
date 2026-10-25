# 完整前三层 DDR 受控端点验证报告

## 结论

最终 testbench 哈希 `3da21f7f28b67a73bef4fbc97208723accf968e00315b07d37052c7e521a3bd5` 下，完整 normal、随机请求/响应背压、512 拍 stall、四位置共同复位取消后完整恢复，以及四个故障用例均得到预期收据。normal 的端点总周期是 **17,252,079**，不是 raw 子模块忙周期之和。

本报告只证明新完整外部序列器、固定层加载器、复用八核、两 ROM 和受控 memory endpoint 的 ModelSim 行为。它不是 DDR 厂商模型、综合/P&R、板卡、Flash、训练、整网精度或持续视频证据。

## 完整成功结果

| Case | 结果 | 端点总周期 | 写 | 读 | PW bytes | 十项互斥 bin |
|---|---|---:|---:|---:|---:|---|
| normal | PASS | 17,252,079 | 78,336 | 97,564 | 221,184 | 1, 138240, 2158, 3004788, 10914048, 776448, 1117948, 972288, 290880, 35280 |
| random backpressure | PASS | 17,714,841 | 78,336 | 97,564 | 221,184 | 1, 211645, 2158, 3139789, 10914048, 871929, 1240461, 972288, 327242, 35280 |
| 512-cycle stall | PASS | 17,252,591 | 78,336 | 97,564 | 221,184 | 1, 138240, 2158, 3005300, 10914048, 776448, 1117948, 972288, 290880, 35280 |
| reset cancel/recover | PASS | 17,252,079 | 78,336 | 97,564 | 221,184 | 1, 138240, 2158, 3004788, 10914048, 776448, 1117948, 972288, 290880, 35280 |

每个完整成功用例核对 halo 1,306,368 项，acc/pre/SiLU/post 各 958,464 项；完整写地址按三个独立范围逐项匹配并用 seen 检查唯一性和洞。reset case 的报告周期和 bin 只来自清空后的最后完整一代，先前四个取消前缀不混入端点总周期。

## 故障闭锁结果

| Case | 预期结果 | 实际端点周期 | 证据 |
|---|---|---:|---|
| response error | status2/error7 | 144,425 | 首个读响应错误立即闭锁，禁止成功。 |
| dropped response | status2/error9 | 644,423 | 首个读响应丢失后无进展看门狗闭锁。 |
| post-PASS DDR fault | status1→status2/error1 | 17,252,079 | 先执行完整 `check_success`，再注入 fault；valid/ready 撤销。 |
| corrupted read beat | status2/error4 | 150,308 | 首个 RGB 128-bit beat 全反相，DUT 在末输出黄金比较闭锁。 |

保留负例 `corrupt_read_data_20261015_161147_561917` 只翻转首 beat 的 bit0，完整运行仍 PASS，说明该微扰被当前量化路径消去；TB 将其判为“未捕获故障”，没有冒充成功。随后采用整 beat 反相才得到可观察且由 DUT 自身闭锁的 error4。

## 地址转换证据

`stem_read_trace_byte_addr_u32.bin` 首个 little-endian uint32 是十进制 54,525,952，即 byte `0x03400000`；按合约右移一位后 native 为 `0x01a00000`，机械转换文件首行也是 `01a00000`，DUT 首读为 `0x01a00000`。首次夹具运行把八位十六进制行读入 25-bit 数组，ModelSim 日志同时记录 “Too many digits” 和 TB 实际 `expected=xxxxxxx`；最终改用 32-bit trace 数组，数量仍严格为 RGB 51,357、DW 46,207。

## 八门与工具证据

严格 TB 静态门禁保存在 `tb_gate.json/.md`：`compile=passed`、`ast=passed`、`readability=passed`、`comment=failed(137)`、`naming=passed`、`profile=passed`、`testbench=not_requested`、`toolchain=not_requested`。comment 失败是本 testbench 未逐个参数、信号、always 和 task 添加规定中文邻接注释；未改写成通过。

实际外部工具证据单列：ModelSim SE-64 2020.4；每个运行重新编译 loader、sequence、复用八核、TB、`PH1P_PHY_GSR` 和 `PH1P_LOGIC_ERAM`，编译 0 error/0 warning。运行期只有厂商 `ph1p_logic_eram.v:165` 两条固定 INIT_FILE 越界 warning。严格门禁的 `not_requested` 不覆盖也不否定这些实际 ModelSim 收据。

## 源码与输入闭包

`suite_manifest.json` 绑定最终 TB、runner、reference contract/generator 哈希和八个正式 case。每个 case 的 `receipt.json` 进一步记录全部编译源码、两份厂商模型、全部输入 vector、机械转换 vector、命令与日志哈希。normal 收据中的 `loop_table.hex` 和 `loop_parameters.hex` 均属于输入向量闭包并复制进独立运行目录。

