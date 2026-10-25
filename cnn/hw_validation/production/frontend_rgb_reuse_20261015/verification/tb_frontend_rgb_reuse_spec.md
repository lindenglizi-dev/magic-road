# RGB halo 复用完整前三层 TB 规格

## 目标与边界

本 testbench 在 100 MHz、低有效共同复位下，独立验证 512×288 RGB 输入经过完整 Stem、DW3s2、PW 三层时，RGB halo 同像素相邻通道复用不会改变功能、DDR 事务或算术结果。受控 128-bit memory endpoint 只返回 DUT 先前实际接受的写数据；它不是 DDR 厂商时序模型，也不证明综合、布局布线、板卡 DDR、Flash、训练精度或整网性能。

地址统一使用 `native_address = byte_address >> 1`。输入从 `0x1a00000` 起 27,648 个 128-bit 字，Stem 从 `0x1a80000` 起 36,864 字，PW 从 `0x1b00000` 起 13,824 字。

## 完整功能检查

1. 逐项核对 78,336 次接受写请求的完整 128-bit 数据、地址范围和唯一性；结束时三个地址空间均无洞、无重复。
2. 逐项核对 97,564 次接受读请求的顺序：RGB 51,357 次、DW 46,207 次；二进制 byte trace 机械转换成 native 地址后比较。
3. 每个有效读响应必须来自 endpoint memory，输入和 Stem 数据只有在对应写请求实际接受后才可读。
4. 核对全部 559,872 个 Stem halo 和 746,496 个 DW halo。RGB 有效 byte 以 raw 异或 `0x80` 等价执行减 128；RGB padding 为 kind1/data0；DW 有效值按 signed int8，DW padding 为 kind0/data0。有效 halo 同时核对 16-byte line 对齐后的 native 地址。
5. 通过外部 tag 与 `u_pp.reg_retire_tags` 映射逐项核对 Stem 589,824、DW 147,456、PW 221,184 个 acc/pre/SiLU/post。重复、越界、洞或任一数值不匹配立即失败。
6. 完整成功必须得到写 78,336、读 97,564、PW 输出 221,184 bytes、Stem tile 2,304、down tile 576、SiLU 表 1,024 项及零基末命令 10,799（共 10,800 条）。
7. 十项互斥 cycle bin 之和必须严格等于 endpoint 总周期；不得把并行算术模块的忙周期相加冒充总周期。

## S1 RGB 复用专门检查

复用资格仅为：当前 byte 非 padding、RGB cache 有效且命中、`channel < 2`、`lane < 15`，并且当前 byte 已被真实 Stem loader 接受。每次合格接受后，下一拍必须仍在 `ST_HALO_BYTE`，halo address、channel 和 lane 各加一。跨词、cache miss、padding、B 通道均必须回到原映射路径。

完整成功用例必须同时覆盖并精确计数：直接推进 350,778 次，`channel < 2 && lane == 15` 跨词回退 20,672 次，R14/G15/B0 像素 10,336 个，R15/G0/B1 像素 10,336 个。tile0 的实际 memory 数据还定向核对 halo 33/34/35 为 R/G/B，归一化值分别为 `0x91/0x80/0x87`。

核心 load 背压必须作用于真实 Stem 消费者 `u_core.u_stem.o_load_ready` 和其 accept，而非只压外层 ready。背压期间内外 accept 均为 0，kind/address/data、halo cursor、channel、lane 和 line address 必须逐拍保持。复位用例还必须清空 halo cursor、RGB cache、SiLU table loaded、endpoint pending、memory、seen 和全部本代计数，随后完整重跑不得泄漏上一代状态。

## Case

| Case | 规格 |
|---:|---|
| 0 | 无背压完整正常运行；端点周期必须精确为 15,848,967。 |
| 1 | LFSR 驱动 request ready 和 0–7 拍响应延迟，完整运行。 |
| 2 | 首次 RGB 读请求额外保持 512 拍 request stall；payload 稳定，随后完整运行，周期 15,849,479。 |
| 3 | 依次在输入填充、SiLU 半表、RGB response 等待、Stem 导出字中途共同复位取消；每代清夹具，最后一代完整运行。 |
| 4 | 首个读响应返回非零 error，必须以 status2/error7 闭锁，禁止成功。 |
| 5 | 丢弃首个读响应，必须由无进展看门狗以 status2/error9 闭锁。 |
| 6 | 完整 `check_success` 后拉高 DDR fault，状态必须由1变2、error1，请求与响应 ready 撤销。 |
| 7 | 首个 RGB 128-bit read beat 整拍取反；暂停预期会被破坏的数值监视，最终必须由 DUT 输出黄金比较以 status2/error4 闭锁。 |
| 8 | 在真实 R14/G15/B0 边界将 Stem loader 消费端背压 257 拍；payload/cursor 保持，释放后完整运行，周期 15,849,224。 |
| 9 | 同一真实边界背压 32 拍后保持 force 执行共同复位；清除全部世代状态后完整重跑，周期 15,848,967。 |

## 通过定义

ModelSim 必须完成冻结源码、复用八核、两层序列器、TB、`PH1P_PHY_GSR` 与 `PH1P_LOGIC_ERAM` 的重新编译，并只接受 `TB_PASS_FRONTEND_DDR` 或 `TB_PASS_EXPECTED_FAULT` 收据。每次运行保存在独立目录，`receipt.json` 记录全部编译源码、厂商模型、输入向量、机械转换向量、命令与哈希。
