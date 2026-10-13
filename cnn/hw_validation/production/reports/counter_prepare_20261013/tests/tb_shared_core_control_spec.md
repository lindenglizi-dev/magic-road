# tb_shared_core_control 计数观察增量

无外部端口；沿用原时钟、复位、装表、交接和控制测试。

只新增只读 counter_prepared_check，核对原计数递推和异步复位清零；没有改变控制激励。原 in-flight reset 用例运行在 Stem，不能把它称为 down2 各发行组复位覆盖。down2 定向复位身份由 tb_counter_prepare 单独覆盖。

观察器机制见 [观察器说明](counter_prepared_check_spec.md)。本说明为人工核实的无端口测试文档，规格生成器对此类顶层的失败记录继续保留。
