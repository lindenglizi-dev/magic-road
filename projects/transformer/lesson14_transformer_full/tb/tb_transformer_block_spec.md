# tb_transformer_block：测试契约

无外部端口，生成 10 ns 周期时钟。异步低有效复位在第 4 个下降沿释放，随后以两个下降沿之间的单拍 `start` 启动；检查器在上升沿读取有效输出。SRAM 模型以 NBA 提供固定一周期读响应，写入始终接受。

```json
{"signal":[{"name":"clk","wave":"p......."},{"name":"rst_n","wave":"0...1..."},{"name":"start","wave":"0....10."},{"name":"busy","wave":"0.....1."}]}
```

输入为 `+CASE=vectors/<case>` 的原始 config、稀疏 X/W 和 Golden 张量。推荐唯一总入口是工作区根目录的 `python projects/transformer/scripts/validate.py --strict`，先由 Python 解析并从 X/W 重算 Golden，再编译/运行 TB。直接 `vvp` 不保证 Golden 文件已经预检。

本轮新增三组 32 位 `q_wr_data/key_wr_data/v_wr_data`，匹配 DUT 的四 lane INT8 写数据总线；原 `.*` 因缺声明无法 elaboration。新增最终 Q/Key 物理 Bank 逐点对拍，避免二者同时置换某列但 Score 不变而漏报。原 V、ACT、Hidden 布局检查保持。

通过条件：无 `$fatal`、7 次 GEMM 顺序正确、输出次数和地址范围正确、QKV raw/量化值、Score、P、PV、ACT、Hidden、Final 全部与 Golden 相等，以及 Q/Key/V/ACT/Hidden 物理 Bank 对拍。现有百万拍 watchdog 适用于当前小例，不保证维度上界在此预算内。

2026-10-23 本地 Icarus 实测：demo 244、edge_5x7 1178、random_00 486、sat_1x1 139 cycles，均 PASS。计数从释放复位起，含启动前空拍。未加入非法配置、复位中断、连续任务或随机存储延迟测试。
