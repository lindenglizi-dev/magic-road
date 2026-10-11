# SiLU停顿响应错位最小修复

v3 T05，任务分类repair/validate。原版AST与诊断为 `production/silu/reports/gate_attempt_6.json`，能够识别真实模块、端口、寄存器及原语实例；其严格门仍失败，不能宣布交付完成。

失败依据：完整官方PH1P_LOGIC_ERAM与GSR模型，raw 0/4/8/12连续查表；无停顿9/9通过，首结果出现后停顿1拍，raw4期望2却返回4。修正测试台末表项ready采样错误后仍复现。原始日志/波形由 `v3_silu_vendor_20261005` 保留。

根因：停顿冻结lookup地址寄存器及reg_ram_address/valid，但CEA常开，在该停顿沿RAM把后续地址的结果覆盖到DOA。恢复沿输出选择使用被冻结的旧控制，却读到更新的RAM值。

修改仅在本目录候选副本将 `.cea(1'b1)` 改为 `.cea(flag_pipeline_enable)`，不是门控时钟，不以input_valid替代流水使能。端口、延迟、II、所有表值、查表边界、pending及1024项装载规则不变。

合法table_transfer要求cnt_pending为0；合法在途守恒下output_valid意味着pending非0。因此接受表项时output_valid为0，pipeline_enable为1，装载不会被该CEA改动阻断。此不变量必须在官方回归中检查，不能只靠文字论证。装载与推理分离，不依赖同址读写碰撞结果。

官方模型已有CEA=0时保持DOA、NOREG时OCEA=0可用的实测；本候选仍需完整模块0/1/16/32/64拍反压、全输入域、随机背压、在途重载及复位回归。故障结果与修复结果分别留档。

风险：改变原语使能会改变非推进拍的RAM内部输出；无效状态不作为数值结果。但额外CEA路径的PH1P物理时序、RAM推断仍未验证，严格门禁未闭合则不运行正常发布P&R。原版保持不变，本版不直接合入生产、不生成位流或训练。
