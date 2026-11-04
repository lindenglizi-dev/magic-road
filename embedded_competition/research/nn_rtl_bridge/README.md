# 神经网络与RTL交换目录

详细流程见 `anlogic_topic2_work/NN_RTL_INTEGRATION_GUIDE.md`。

将Python量化模型保存为NPZ后，可以执行：

```powershell
python .\export_npz_to_mem.py .\model\model_int8.npz .\weights
```

NPZ内数组命名建议：

```text
conv1.weight  int8  [8,1,3,3]
conv1.bias    int32 [8]
conv2.weight  int8  [16,8,3,3]
conv2.bias    int32 [16]
conv3.weight  int8  [16,16,3,3]
conv3.bias    int32 [16]
fc.weight     int8  [N,16]
fc.bias       int32 [N]
```

导出脚本采用C顺序展开，并把负数写成二进制补码十六进制。硬件读取顺序必须保持一致。
