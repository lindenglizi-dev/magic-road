# 候选整数化准备（非部署包）

本目录绑定 `ac_replay_g10_20261013_v1/last.pt`，完成两项有界工作：

- `folded_fp32_weights.pt`：67 层 Conv-BN 折叠后的 FP32 权重与偏置，仅供后续整数契约准备，不是模型 ROM。
- `calibration_ranges.json`：只用清单中的全部 86 张 `train` 图前向得到的 67 个卷积输入、61 个 SiLU 输出和 6 个原始预测头范围；未前向 `val` 或盲测图。

`report.json` 记录输入、源码、输出哈希，4 张真实训练图的 FP32 准备资产近似等价、从 FP64 源参数重算折叠的严格公式核查、有限值检查和当前未闭合风险。脚本固定 CPU 2 线程，不训练、不调用教师、不执行 QAT，也不生成可烧录文件。

复跑：

```powershell
$env:CUDA_VISIBLE_DEVICES=''
E:\project\qiansai\.tools\road_yolo_venv\Scripts\python.exe .\prepare_integer_assets.py
```

后续仍需单独完成 INT32 bias 编码、concat/residual 尺度对齐、pre/post 整数重定标契约、部署等价 QAT 与正式精度/硬件验证。
