# counter_prepared_check 验证接口

此模块在 tb_counter_prepare.v 中，只读观察调度器，不参与综合。

输入为 clk、rstn、state[3:0]、layer_pw、position[3:0]、count[4:0]、prepared[4:0]、accept、last_group、start_accept、dw_writes[8:0]、pp_fault、load_fault；无输出端口。

每个上升沿采集旧状态，按照修改前的 clear/increment 递推计算期望 count；沿后 1ns 比较实际 count。合法末组接受时同时核对 prepared。rstn 下降后 1ns 核对两个寄存器均清零。checks、last_checks、stalled_last_checks、fault_checks、reset_checks 是测试统计，不是被测接口。

正常计数应保持到接受沿；PW 最后位置/组保持 7，DW 15 回绕 0，PP/load 故障优先保持。连续两组 PW 的周期图见 [计算模块周期说明](../rtl/road_down2_tile_scheduler_spec.md)。

此文件为人工核实的测试说明。规定的规格生成器拒绝无端口测试顶层，原失败记录在 test_specifications/；未把该步骤标为严格通过。
