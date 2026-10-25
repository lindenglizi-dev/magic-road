# tb_program_banks 人工接口与周期说明

自动规格工具拒绝空端口列表，失败日志保存在 `../testbench_specification/testbench.log`。本文补充真实说明，不代表该自动生成门通过，不为消除诊断虚构端口。

本模块没有外部端口，只用于仿真。内部 `clk` 周期10ns，`rstn` 低有效，`address` 为13位，`expected` 从冻结的8192词 `program.hex` 读取。

每个地址在下降沿设置PC并强制实际调度器为FETCH；上升沿后1ns检查完整64位命令和寄存的bank选择。随后强制为不取指的PHY状态，翻转PC的bank位，连续两个上升沿后检查命令保持。覆盖地址0..8191，包括4095→4096。最后撤销force并断言复位立即撤销请求/响应许可。

该测试的force不属于可综合RTL；其状态输出不能作为CNN通过证据。真正计算、反压和复位恢复由同目录的13项序列回归及双时钟联调验证。

周期图沿用同一取指契约：[FETCH与bank边界](../rtl/spec/program_banks/waveforms/road_stem_ddr_sequence_bank-boundary.svg)。

正例检查8192词、16384次保持；负例只在隔离目录替换低bank副本，必须报告 `BANK_WORD_MISMATCH address=0`。原向量和RTL不变。
