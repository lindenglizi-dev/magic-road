# tb_ddr_pipeline 组合验证合同

100MHz单clk、异步低有效rst_n。实例ccl_pipeline_trial_top，WIDTH17、HEIGHT4、X5/Y3、L32/LABEL6、MAX_RUN64、min-run/area1。仅testbench使用task/层级观察，功能RTL无层级控制。

13个接受任务、13个完整终态：正常单矩形全部拒识；四候选但部分后级处理错误；双银行占用取消；A残余隔离后的B恢复；短行协议错误恢复；最后同步RAM返回与取消同拍；再次正常恢复；预置候选释放的零候选成功；无processed_error时的身份错配、完成数量不符、接受数量超限；重复完成0、0冒充0、1；预置旧显示ACK、提交背压、取消与发布同拍、错身份ACK及保持高电平改身份。最后源像素后还在RUN时验证input_complete阻止追加行。三次核心复位由硬件状态产生，TB不直接驱动drain_done或猜测固定等待。每个最终结果断言任务和帧身份；其余容量/面积边界回归独立保留。

矩形gold：x3～6/y0～3，面积16；条纹gold：每列偶数x为独立竖线，面积4，Top4标签1～4、x0/2/4/6。最后逐目标完成和汇总valid同拍时先记录目标，汇总保持至下一拍，验证不会读取旧完成数。读取实际顺序request/response接口，返回背压3周期并尝试提前表释放；候选延迟4周期、最终结果延迟3周期只用于制造压力，不作为功能排空依据。阶段报告与ACK是受控消费者模型，未执行ROI或分类/HDMI。

```json
{"signal":[{"name":"clk","wave":"p......"},{"name":"cancel","wave":"010...."},{"name":"banks_empty","wave":"0..1..."},{"name":"core_reset_active","wave":"0...10."},{"name":"candidate_valid","wave":"0.....1"}]}
```

时序声明未渲染。PASS需比较断言及任务计数，检查次数不是独立任务数量；timeout/compile失败工件保留。
