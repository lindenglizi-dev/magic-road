# `tb_frontend_ddr_tensor` 验证规格

## 目标与边界

本 testbench 独立验证固定 512×288 RGB 输入经过完整 Stem、DW3s2、PW 三层的外部序列器。端点是受控 128-bit memory model，只返回 DUT 先前实际接受的写数据；它不是 DDR 厂商时序模型，也不证明板级 DDR、电气、训练精度或整网性能。

时钟为 100 MHz，低有效共同复位。外部原生地址严格使用 `native_address = byte_address >> 1`，128-bit 字步长为 8：输入从 `0x1a00000` 起 27,648 字，Stem 从 `0x1a80000` 起 36,864 字，PW 从 `0x1b00000` 起 13,824 字。

## 必须观测的行为

1. 逐项核对 78,336 次接受写请求的地址、唯一性和完整 128-bit 数据；结束时三个地址空间无洞、无重复。
2. 逐项核对 97,564 次接受读请求的顺序：RGB 51,357 次、DW 46,207 次，二进制 byte trace 转换为 native 地址后比较。
3. 每次读响应只来自端点 memory。输入和 Stem 数据只有在对应写请求被 DUT 接受后才可读。
4. 核对全部 559,872 个 Stem halo 和 746,496 个 DW halo。RGB 有效值以端点 raw byte 异或 `0x80` 等价执行 `raw-128`；Stem padding 使用 kind1/data0；DW 有效值按 signed int8，DW padding为 kind0/data0。有效 halo 同时核对 16-byte line 对齐后的 native 地址。
5. 通过外部 tag 和 `u_pp.reg_retire_tags` 解析内部 tag，逐项核对 Stem 589,824、DW 147,456、PW 221,184 个 acc/pre/SiLU/post。任一阶段重复索引、越界或数值不一致立即失败。
6. 完整成功必须得到写 78,336、读 97,564、PW 输出 221,184 bytes、Stem tile 2,304、down tile 576、SiLU 表 1,024 项和零基末命令 10,799（共执行 10,800 条）。
7. 十项互斥 cycle bin 之和必须严格等于端点总周期；不把 pre/SiLU/post 活动周期相加冒充总周期。

## Case

| Case | 规格 |
|---:|---|
| 0 | 无背压完整正常运行。 |
| 1 | LFSR 驱动 request ready 和 0–7 拍响应延迟，完整运行。 |
| 2 | 首次 RGB 读请求额外保持 512 拍 request stall，期间请求 payload 必须稳定，随后完整运行。 |
| 3 | 依次在输入填充、SiLU 半表、RGB read-response 等待、Stem 导出字中途取消共同复位；每代清除 endpoint pending、memory、seen 和计数，最后一代完整运行。 |
| 4 | 首个读响应返回非零 error，必须以 error7 失败。 |
| 5 | 丢弃首个读响应，必须由无进展看门狗以 error9 失败。 |
| 6 | 完整 PASS 后拉高 DDR fault，状态必须从1撤销为2、error1，且请求/响应 ready 撤销。 |
| 7 | 首个 RGB 读 beat 整个 128-bit 反相；中间数值监视明确停用以免把预期破坏冒充 DUT 捕获，必须由 DUT 输出黄金比较以 error4 闭锁。 |

## 通过定义

ModelSim 编译必须 0 error/0 warning；运行只接受 `TB_PASS_FRONTEND_DDR` 或 `TB_PASS_EXPECTED_FAULT` 收据。所有运行在新的保留目录中，命令、日志、源码/向量/厂商模型哈希及机械转换哈希写入 `receipt.json`。

