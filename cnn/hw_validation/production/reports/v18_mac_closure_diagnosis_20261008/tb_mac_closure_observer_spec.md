# tb_mac_closure_observer：冻结核逐拍观测

本文件配套 `tb_mac_closure_observer.v`，为非综合、无端口、只读层次引用的诊断模块。不驱动DUT，不改变握手或数据，不属于新算术候选。

## 接口与计时

观测路径：`tb_down2_overlap_tile_runner.down2_overlap_tile_runner_Inst_tb.road_mac_probe_Inst_tile`。
观测 `i_clk`、低有效异步 `i_rstn`、输入接受及last、结果接受、final stage0..3的数据/有效/故障和保持型输出。与冻结TB一起作为两个仿真根展开。

last在时钟沿前握手为c0；NBA完成后1 ns观测发布。A5(c5)采集96位安全终态和故障，c6/c7/c8校验三级搬运，c9及其后的阻塞周期校验输出保持一致。ACK在时钟沿前检查，最早c10。复位取消观测上下文，不误报旧任务完成。错误以 `CLOSURE_ERROR` 输出，配套检查脚本要求零错误及原TB成功标记。

## 周期示意

以下是由本轮日志核实的无背压情形；不是亚稳态或物理时序证明。

```json
{"signal":[{"name":"cycle","wave":"============","data":["c0","c1","c2","c3","c4","c5","c6","c7","c8","c9","c10","c11"]},{"name":"last_accept","wave":"10.........."},{"name":"final_stage0","wave":"0....10....."},{"name":"final_stage1","wave":"0.....10...."},{"name":"final_stage2","wave":"0......10..."},{"name":"final_stage3","wave":"0.......10.."},{"name":"output_valid_after_NBA","wave":"0........10."},{"name":"ack_before_NBA","wave":"0.........10"}]}
```

规范生成限制：技能 `write-spec` 当前要求至少一个模块端口，不支持这个真实无端口仿真根；不编造端口来让生成器通过。本配套规格及WaveJSON为人工编写，未声称完成该工具生成或SVG渲染。严格检查另见 `observer_gate.json/md`，不因此豁免门禁。

## 范围与边界

复用三套完整DW/PW向量、PW单独运行、随机ready、复位及末组溢出回归。仅证明冻结版本的终态搬运与输出时序；不证明省略寄存级后的时序、吞吐或精度。行为RAM仍为原Icarus模型，不替代厂商模型及上板验证。
