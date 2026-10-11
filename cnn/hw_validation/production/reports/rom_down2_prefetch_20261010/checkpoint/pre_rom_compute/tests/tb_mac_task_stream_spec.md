# 独立 MAC 连续任务自检

此无端口 testbench 不是可综合顶层。复用 `mac_reference.py` 生成的 119 个任务、849 个输入组，逐个比较 97 位原子终态。覆盖 1、2、3、24 组，随机气泡与输出背压、四槽满且活动归约继续、同拍入队出队及 first/pop、正负暂越 INT32 后恢复、两个最终原子故障、在途和满结果队列复位取消。时钟为 10 ns，所有输入在负沿设置、正沿握手。

预期结果为 `PASS mac_task_stream`，完整窗口 1,211 周期；不将此窗口作为完整层吞吐。复位后空闲期间不得出现旧结果。

协议周期图：[四槽任务流](../rtl/waveforms/road_mac_probe_pw_task_stream.svg)。图展示两组任务的入口理想连续段，实际随机自检以日志为准。

规范生成器不支持空 ports 的 TB contract；本文件为人工补充，不代表 canonical spec 或严格门禁通过。真实 ModelSim 编译与执行回执位于 `../mac_sim_attempt3/`；复位期间 ready=1 的断言与旧核一致，复位时序逻辑优先取消所有事务。
