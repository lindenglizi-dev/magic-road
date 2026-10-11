# tb_down2_overlap_tile_runner 变更规格

原无端口仿真根与全部输入、黄金期望及驱动不变。实例为冻结runner、post、round、SiLU与唯一修改的MAC；原Icarus ERAM行为模型不变。

三套完整4×4 down2 DW16/s2→PW16→24向量、独立PW和seed1d0f随机MAC ready继续执行。保留各级acc/pre/SiLU/post、输出位置、地址、cache读写、reserve计数、队列满、三路原子故障、末组溢出、表重装及各阶段复位检查。

只修订已改变的等待断言：last→ACK10→7；每DW任务WAIT10→7；完整256任务总WAIT2560→1792。无停顿排空仍56；固定seed5eed提交背压的排空实测58，因此该用例明确独立期望58，不用放宽比较掩盖错误。首轮11项旧时序断言失败完整保留在tile_initial.log，非RTL数值失败。

计时：完整预装载2894拍（1024表项+1864张量项及控制）、核心3257拍、导出449拍/384传输，三窗口分开。core状态互斥计数须等于端点经过时间；模块忙周期可能重叠，禁止相加。故障提前退出不能算加速。

周期图：[road_mac_probe_stream-terminal.svg](../spec/mac_stream/waveforms/road_mac_probe_stream-terminal.svg)。完整DW/PW实际各任务时间戳见tile_final.log的JOB_TURN_TRACE。无端口TB规格人工编写；未假设write-spec支持空端口模块。
