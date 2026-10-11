# 窄口验证壳完整输出自检

无端口仿真顶层，复用冻结 38 位低 I/O 壳。复位同步释放后装满 1,024 项 SiLU 表及运行期测试参数，经原窄口载入真实操作数，逐项导出三个空间 tile 共 1,152 字节，并校验报告的核心计数为 2,607。表未满、参数未满不得启动；复位后不能依赖旧存储位。

分别运行最终 RTL、`physical_attempt3/gate_netlist.v` 和 `physical_opt/routed_netlist.v`，固定和动态 stress 两套共 2,304 字节/实现。网表功能仿真不带 SDF，不能替代实际 setup、hold、recovery、removal 检查；优化实现另保留全部物理报告。

协议周期图：[装载后启动与任务流](../rtl/waveforms/down2_dynamic_tile_runner_pw_task_stream.svg)。图省略长装载和导出时段，吞吐采用核心端点计数。

canonical spec 的空 ports 限制未闭合；此文件仅补充接口/测试说明。输出回执位于 `../shell_rtl_attempt3/`、`../shell_gate_attempt3/` 与 `../shell_routed_opt/`，以实际 receipt.json 是否存在及结果为准。
