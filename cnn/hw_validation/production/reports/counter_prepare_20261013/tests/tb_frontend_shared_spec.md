# tb_frontend_shared 计数观察增量

无外部端口；沿用原内部 100MHz 测试时钟、向量、随机种子及驱动周期。

仅新增只读 counter_prepared_check 观察器，不改变原握手或负载。normal、stalls 各完成 2,304 个 Stem tile 和 576 个 DW/PW tile；结束前必须记录 147,456 次合法末组接受。每次接受均核对准备值和旧计数递推，原数值、地址、导出和周期检查继续执行。

观察器每个上升沿后 1ns 检查；机制见 [观察器说明](counter_prepared_check_spec.md)。本说明为人工核实的无端口测试文档，规格生成器对此类顶层的失败记录继续保留。
