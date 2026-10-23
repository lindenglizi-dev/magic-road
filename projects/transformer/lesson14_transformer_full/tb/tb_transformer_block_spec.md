# tb_transformer_block：测试契约

无外部端口，生成 10 ns 周期时钟。异步低有效复位在第 4 个下降沿释放，随后以两个下降沿之间的单拍 `start` 启动；检查器在上升沿读取有效输出。SRAM 模型以 NBA 提供固定一周期读响应，写入始终接受。

```json
{"signal":[{"name":"clk","wave":"p......."},{"name":"rst_n","wave":"0...1..."},{"name":"start","wave":"0....10."},{"name":"busy","wave":"0.....1."}]}
```

输入为 `+CASE=vectors/<case>` 的原始 config、稀疏 X/W 和 Golden 张量。推荐唯一总入口是工作区根目录的 `python projects/transformer/scripts/validate.py --strict`，先由 Python 解析并从 X/W 重算 Golden，再编译/运行 TB。直接 `vvp` 不保证 Golden 文件已经预检。

本轮新增三组 32 位 `q_wr_data/key_wr_data/v_wr_data`，匹配 DUT 的四 lane INT8 写数据总线；原 `.*` 因缺声明无法 elaboration。新增最终 Q/Key 物理 Bank 逐点对拍，避免二者同时置换某列但 Score 不变而漏报。原 V、ACT、Hidden 布局检查保持。

通过条件：无 `$fatal`、7 次 GEMM 顺序正确、输出次数和地址范围正确、QKV raw/量化值、Score、P、PV、ACT、Hidden、Final 全部与 Golden 相等，以及 Q/Key/V/ACT/Hidden 物理 Bank 对拍。现有百万拍 watchdog 适用于当前小例，不保证维度上界在此预算内。

2026-10-23 本地 Icarus 实测：demo 244、edge_5x7 1178、random_00 486、sat_1x1 139 cycles，均 PASS。计数从释放复位起，含启动前空拍。该行记录原四案例数值基线；下述控制模式另行覆盖启动与恢复。存储延迟保持固定一周期。

## 控制与恢复模式（2026-10-24）

`vvp <新编译的 tb_transformer.out> +CASE=vectors/demo +CONTROL` 复用同一 SRAM 模型、Golden、逐点/物理 Bank 对拍和计数检查。默认不带 `+CONTROL` 的四个数值案例保持原检查。控制模式使用 demo（L=2、D=4、F=6），不代表所有维度与故障交叉组合均已验证。

- 18 个非法启动：L=0/65、D=0/257、F=0/257、scale=0/65537；X/WQ/WK/WV/Q/Key/V/Score/W1/W2 各自 base+span=2^AW+1。每次检查立即 done=1、busy=0、无读写或 GEMM 启动；随后四拍 done=0 且 error=1，即使外部配置已恢复合法。再无复位执行完整 demo，检查 error 清除和全部数值。
- 一个地址边界接受：Q 逻辑输出 base+L*D=2^AW，必须成功启动；在超出测试 SRAM 容量的访问前异步复位，再运行完整 demo。只证明配置边界判定，不是高地址 SRAM 数值测试。
- 一个 busy 单拍 start：Key GEMM 正在读时，将所有配置组改变（含非法维度/scale/base）并脉冲 start，然后恢复外部配置。原任务仍完成 7 次 GEMM、全部 Golden 和准确计数；结束后六拍无第二次 done、启动或流量。start 持续到 IDLE 的语义不在此用例内。
- 五个异步复位点：Q 的已返回但尚未消费读响应、Q 的有效量化输出、Softmax 的 Score 行输入响应、Softmax 的 P 输出、FFN2 的 Y 写回。触发条件须在 watchdog 内真实出现；下降沿后 2 ns 断言 reset，1 ns 后即检查 busy/done/error 和流量已清零。复位跨三个下降沿以清除外部读响应，释放后检查三拍静默；poison 中间 Bank、清 scoreboard 后完整 demo 恢复。未将空闲 DRAIN 状态当作活跃流水验证。
- 一个运行时读响应错误：Q 的首个 lane 0 必需 X 响应丢 valid。故障任务只检查确已注入、在 Q 阶段 error=1 且 done 单拍、busy=0 和完成后无流量；故障输出不计数值通过。随后不复位执行完整合法 demo，验证上一任务错误不会污染新任务。

每个完整 demo 应恰有 GEMM=7、QKV=24、Score=4、P=4、PV=8、ACT=8、Hidden=12、Final=8，并保留 Q/Key/V/P/ACT/Hidden 物理 Bank 对拍。控制模式合计 26 个完整任务（18 个非法配置恢复、1 个地址边界恢复、1 个 busy-start 任务、5 个复位恢复、1 个读故障恢复）；另有 5 个中止任务、1 个地址边界中止任务和 1 个故障任务。最终 marker 为 `PASS TRANSFORMER_CONTROL`，须与进程 exit=0 同时成立。

Top 非法配置产生 done 脉冲，与 GEMM 单元 bad_dim 的无 done 拒绝不同。Top error 粘滞到 reset 或下一次 start。修前故障恢复日志 `../../reports/rtl_control_before_fix.log` 记录旧 GEMM 错误在下一任务 ISSUE 周期污染 top.error 的失败；RTL 修复见 `../rtl/transformer_block_top_spec.md`。修前日志中的第二复位点为 DRAIN；最终测试已加强为 Q 的有效量化输出。

```json
{"signal":[{"name":"clk","wave":"p......."},{"name":"start_invalid","wave":"010....."},{"name":"done","wave":"0.10...."},{"name":"busy","wave":"0......."},{"name":"error","wave":"0.1....."},{"name":"traffic","wave":"0......."}]}
```

本测试沿用项目 SystemVerilog。仅识别 `.v` 的 readable gate 对此文件不适用；编译与仿真以实际 Icarus 命令/退出码为准，未取得 ASIC、时序或随机存储延迟证据。
