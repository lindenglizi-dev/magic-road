# round 长停顿验证接口与周期契约

任务：v3 T04，testbench-only。功能DUT为同哈希 `road_round_shift.v`；端口、位宽、最近偶数舍入和饱和均沿用 `production/round/road_round_shift.contract.json`，没有修改DUT。

testbench为无外部端口的仿真顶层。正式write-spec要求非空端口，不伪造端口来绕过；本说明为人工测试契约，不宣称正式规范生成门通过。

周期：在 `i_rstn=1 && i_advance=1` 的posedge接受有效输入。接受边沿算第一拍，第九个使能边沿后出现结果，即8个使能间隔；停顿不接受输入、不推进记分板、不重复计数保持的valid。逐拍比较全部DUT寄存器，复位优先于advance。

```text
时钟边沿        e0  e1  e2  [停顿16/32/64拍] e3 … e8
advance          1   1   1   0 … 0           1  … 1
输入tag          A   B   C   不接受新事务     D  …
内部状态         →   →   →   完全保持         →  … →
A的输出valid     0   0   0   保持             0  … 1
```

参考：原始7042个Fraction黄金向量，随机暂停Xorshift32初态42；不改表值及向量字节。三段定向长停顿的流水必须非空，另有占用6拍后停顿16拍再异步复位、释放时继续停顿32拍及空流水12拍检查。最早4个旧事务与后续6个事务均合法取消，不与最终7042个正常输出混算。

正常结果：7042输出、14084中间量、1278停顿（112定向+1166随机）、5fault、模拟总时间95.976 us。9使能边沿/II=1未变。摘要将fault输出数据归零（契约规定fault时数据未定义），预期00014ec4；初版原始数据摘要0001313a只供观察，不能作故障数据数值验收。

负测试：同一可执行文件加 `+INJECT_STALL_FAULT`，仅在仿真中破坏停顿期间商寄存器，应返回1并报告 `FAIL stall changes payload or intermediate`。不修改DUT输入副本。

命令：`iverilog -g2001 -s tb_road_round_shift_stall -o round_stall.vvp road_round_shift.v tb_road_round_shift_stall.v`，随后 `vvp round_stall.vvp +COUNT=7042`；负例再加上述选项。实际工具为工程 `.tools/iverilog/bin/`。

门禁区别：Icarus编译及正负自检已执行。严格formatter检查同目录设计+仿真代码返回1，包含TB解析、风格/命名/注释诊断，记录在strict_gate.json/md。改成显式空端口头后仍失败，故解析原因未确认，不简单归因无端口。不能称严格交付通过，也不能将413条重叠/派生诊断称413个硬件错误。没有绕过门禁运行修改后的TD或将TB交付为生产RTL。
