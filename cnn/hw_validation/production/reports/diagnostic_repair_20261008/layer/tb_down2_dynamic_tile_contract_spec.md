# tb_down2_dynamic_tile_contract 验证契约

本文件为无外部端口的Verilog-2001仿真顶层，驱动100MHz时钟及DUT异步取消。DUT接口规格与周期图见[runner说明](spec_verified_files/spec/down2_dynamic_tile/down2_dynamic_tile_runner_spec.md)及[结果保持周期图](spec_verified_files/spec/down2_dynamic_tile/waveforms/down2_dynamic_tile_runner_result-stall.svg)。

输入来自当前运行目录的vectors：1024项SiLU表、1296字节halo、144个DW权重、16个DW偏置、384个PW权重、24个PW偏置，以及独立整数参考的acc、pre/SiLU/post、提交和最终输出。

三位置无停顿与随机反压共六例，第七例在持有结果期间复位后完整重新装载。逐项检查640个acc、1920个中间值、640个唯一tag/提交和384个导出；DW接受256批、PW128批；完成时pending/reservation/metadata清空。

每个busy周期按commit_stall、commit、pre、SiLU、post、选择、存储、MAC/等待、排空依次归入一个类别，断言类别求和等于核心窗口，且DW段加PW段等于核心窗口。装表、预载和导出独立计数。反压期间有效结果及payload保持，完整装载前启动无效。

TB显式连接或留空全部49个DUT端口，o_fault接出并每拍检查。内部观察用于本探针数值和占用统计，不是新增生产接口；数字仿真不模拟亚稳态、不测DDR或整网速度。通过标记为TB_PASS_DOWN2_DYNAMIC_TILE和逐例LAYER_CONTRACT_PASS。

旧TB及旧日志保留；本TB只增加计数闭合、队列清空、端口完整连接，DUT算术不变。
