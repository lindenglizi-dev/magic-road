# road_mac_probe II=1 独立验证回执

## 结论

冻结候选在独立核级功能仿真和未修改的 v8 层级回归中通过。当前源码 SHA256：

`04a8519e0c9e464add189ee4eb4c5ac25a6c7c716ce0ca4adf2f8fbb0fd19b51`

本回执不作 release-ready 结论：独立复跑的 strict gate 为非通过状态（431 errors；AST、readability、naming 未通过），与 core owner 保留报告一致。功能 PASS 不覆盖该静态门槛。

## 独立 MAC 流验证

- Python golden 独立生成 17 个事务、123 个输入组；未读取 core owner 的 Python reference。
- 实际 ready/valid 握手接受 123 组；A4 三路 dot 对拍 123 组；A5 signed34 candidate 与 signed33 accumulator 对拍 123 组。
- 17 个 last 终态均在 last 接受后 9 周期出现；9 个越界终态均为三路原子零输出。
- 组内实测 97 个 II=1 间隔和 9 个输入空泡间隔。24 组连续案例逐周期接受，不把 fault 提前终止计入 II。
- 覆盖正/负暂时越出 INT32 后恢复、正/负最终溢出、三路单独及同时 fault、24 组/每输出 192 个有效乘积、INT8/INT32 极值、tail mask、bias 仅 first 使用、first0 继续、first1 重开、随机空泡、30 周期输出背压和 last 后输入阻断。
- A1 至 A9 九个 offset 分别施加异步复位；全部立即清 valid/结果/累加器，并在累计 135 个后续观察周期中无 ghost result。

证据：`modelsim_stream_compile_final2.log`、`modelsim_stream_run_final.log`、`stream_trace_final.csv`、`stream_vectors.json`。

## 未修改 v8 层级回归

编译闭包仅把库中的 `road_mac_probe.v` 替换为冻结候选；以下内容原样复用：

- `v8_reset_layer_tiles_20261007/layers/down2_tile_runner.v`
- `v8_reset_layer_tiles_20261007/layers/tb_down2_tile_runner.v`
- v8 `reference.py` 与全部 `vectors/*.hex`
- v7 `ph1p_logic_eram.v`、`ph1p_phy_gsr.v`、`road_round_shift.v`、`silu_shared_unit.v`

最终仿真 `Errors: 0, Warnings: 0`，四个案例均通过；完成 9216 个 debug 中间值比较、1536 个导出握手比较，并通过原有 in-flight reset 与 atomic fault probe。

| 窗口 | v8 旧周期 | II=1 候选周期 | 变化 |
|---|---:|---:|---:|
| DW core | 13312 | 11008 | -2304 (-17.308%) |
| PW core | 14081 | 12929 | -1152 (-8.181%) |
| 完整 DW+PW core | 27393 | 23937 | -3456 (-12.616%) |
| DW MAC 桶 | 5376 | 3072 | -2304 |
| PW MAC 桶 | 2688 | 1536 | -1152 |
| full preload endpoint | 2894 | 2894 | 0 |
| PW-only preload endpoint | 1692 | 1692 | 0 |
| 每案例 export | 449 / 384 transfers | 449 / 384 transfers | 0 |

其余 pre/SiLU/post/writeback/storage/scheduler 桶保持旧值；DW/PW/总 core 计数仍互斥相加。证据：`modelsim_layer_compile.log`、`modelsim_layer_run_final2.log`。

## 保留失败与无效轮次

- `python_reference_first_attempt.log`：golden 自检的预期总数写成 125，实际构造为 123；仅修正验证断言。
- `modelsim_vlib_first_attempt.log`：sandbox 内 Windows DLL relocation，按授权在同一限定命令外运行；未做系统修复。
- `modelsim_stream_run_first.log`：DUT 的 123/A4/A5/17/9 均零误差，但 TB 共享循环变量导致只执行 1/9 reset，语义 FAIL；仅修 TB 循环变量后重跑。
- `modelsim_layer_run.log`：运行目录错误，20 个 `readmem` ENOENT，合计 22 warnings；即使旧 TB 打印 PASS，X 与 X 的 case-inequality 不足以证明数值一致，本轮明确作废。
- `modelsim_layer_run_final.log`：Windows 反斜杠 `-modelsimini` 路径被 ModelSim 错解析，exit 1；改用正斜杠后重跑。
- `collector_first_attempt.log`：回执解析器把 `LAYER_CYCLE_RESULT` 误计为 `CYCLE_RESULT`；只修精确前缀过滤。
- `independent_strict_first_attempt.log`：从 verification 子目录调用时预扫描失败；从 v9 根目录重试后正常产出报告，结果仍是 431 errors、delivery-ready=false。

## 命令、哈希与边界

完整命令/退出码见 `commands.json`；源码、向量、日志和工具逐项 SHA256 见 `source_closure_manifest.json`；机器可读结论见 `verification_receipt.json`。

验证边界不含 TD、训练、生产接入、bitgen、板级、Flash 或形式证明。层级周期仅代表冻结 v8 小块调度和同一 backpressure 模式，不外推为全网络吞吐。
