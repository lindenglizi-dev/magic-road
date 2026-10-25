# QAT 部署等价前向准备记录

日期：2026-10-13。状态：**CPU 数值门禁通过；未启动 GPU 训练；未形成模型候选。**

## 交付

- `cnn/hw_validation/production/qat_exact.py` 提供 `QATExactModel`。
- 构造：`QATExactModel(graph, folded, scales, weight_scales)`。
- 包装载：`QATExactModel.from_package(package_dir, folded, quantization)`；会验证折叠参数可逐字段重现输入包。
- `forward(centered_nchw, capture=False)` 返回三个反量化 Q7.8 head；`capture=True` 额外返回逐节点 trace。
- `integer_forward` 返回原始 INT16 head；`export_package` 使用冻结的逐输出通道 weight scale，不按更新后权重重新估计 scale。

前向实际执行 INT8 权重、INT32 bias、整数卷积累加、INT64 乘移位 RNE、SiLU LUT、输出饱和、残差相加饱和和固定 Q7.8 head。梯度走局部浮点 STE；每个卷积 pre 和每个图输出均由自定义 autograd 节点直接返回整数参考值，下游继续消费这个精确值，不通过浮点加减抵消来伪造相等。

## 证据

- max-abs v2 包：同一真实训练帧上，113 个图输出、67 个卷积 pre、3 个最终 head 全部与 `IntegerModel` bit-exact；共 181 个可捕获张量（含输入）。
- 合成标量损失：全部参数梯度存在且有限；一次 CPU SGD 更新改变 FP32 参数。
- 更新后按冻结 weight scale 导出到本报告的 `test_exports/`，重新载入后三个 head 与更新前的 QAT 整数路径 bit-exact；导出 provenance 标明 `numeric_selftest_not_quality_run`。
- 既有整数算子回归合并执行 15/15 通过，最终复跑 Python 测试时间 12.182 秒，外层墙钟 17.283 秒。
- 已拒绝的 MSE 包只做兼容性检查：同一真实帧 181 个 trace 张量精确，单次 QAT 前向约 2.537 秒；这不改变其精度结论，也不选择它训练。

## 边界

当前实现每次前向都把可训练参数编码为 NumPy 整数，并由 CPU `IntegerModel` 执行完整 67 层后再建立 STE 图。这适合作为前向门禁和小规模梯度验证，但约 2.5 秒/帧的 CPU 成本不适合直接做正式训练。它没有集成 `train.py`、保护式 GPU 启动器、损失训练循环、AMP 或断点恢复，也没有保存候选模型。现有包写入器仍使用固有的 `TRAINED_PTQ_DIAGNOSTIC_NOT_QAT_NOT_BOARD_QUALIFIED` 状态；本轮只在 provenance 中进一步标注数值自测，不能把测试导出称为 QAT 质量结果或生产包。

