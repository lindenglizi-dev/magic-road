# tb_counter_prepare 测试边界

无外部端口。内部 clk 周期 10ns，rstn 由测试平台异步断言并在下降沿释放；没有真实板级复位签核含义。

该测试强制发行状态、计数和接受条件，先给准备寄存器一个合法捕获沿，再释放 count 并检查递推。包含 1,024 个 DW/PW、位置、通道、长停顿和故障优先级变体，DW g0/g1/g2、PW g0/g1、STORAGE、DW_DRAIN 共七组明确的复位身份，以及 IDLE/start、DW_DRAIN 直接清零分支。

故障优先级用例允许 force 产生真实接口不会出现的组合，故只证明对应保持分支，不是合法握手的可达性证据。复位从非零准备值开始检查；DW_DRAIN 使用真实的 count=0。合法完整事务由 tb_frontend_shared 补充。

沿前/沿后检查机制见 [观察器说明](counter_prepared_check_spec.md)。无端口顶层无法通过当前规格生成器的非空端口检查，本说明不替代该失败记录。
