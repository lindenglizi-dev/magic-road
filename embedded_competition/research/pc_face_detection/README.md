# 静态图像人脸检测操作说明

## 1. 这项任务最终要得到什么

静态图像人脸检测是电脑端算法验证，不需要 FPGA 开发板。输入一张 JPG/PNG 图片，程序应输出：

1. 图片中检测到的人脸数量；
2. 每张人脸的矩形框坐标 `(x, y, width, height)`；
3. 画好人脸框的结果图片；
4. 一份 JSON 结果，供以后与 FPGA 输出逐项比较；
5. 单张图片的检测耗时。

这一步只回答“人脸在哪里”。判断这个人是谁属于下一阶段的人脸识别，需要人脸对齐、特征提取和特征比对。

## 2. 当前工程情况

安路官方工程已经实现摄像头输入、RAW/ISP、DDR 帧缓存和 HDMI 显示，没有人脸检测模块。当前目录也没有现成的人脸检测脚本和模型。因此需要先建立电脑端参考程序。

本目录提供的 `detect_static.py` 使用 OpenCV 自带的 Haar 分类器，不需要下载模型，也不需要开发板。它适合先跑通完整流程和建立测试规范。Haar 的结果不是最终 FPGA 算法方案。

## 3. 准备测试图片

在本目录建立 `images` 文件夹，准备至少 10 张图片：

| 类型 | 建议数量 | 用途 |
|---|---:|---|
| 单人正脸、光照正常 | 2 | 验证基本流程 |
| 多人正脸 | 2 | 验证多框输出 |
| 侧脸、低头或遮挡 | 2 | 观察漏检 |
| 较暗、逆光 | 2 | 观察光照影响 |
| 没有人脸 | 2 | 观察误检 |

文件名建议使用 `single_01.jpg`、`multi_01.jpg`、`dark_01.jpg`、`no_face_01.jpg`。如果图片中包含同学或老师，保存和展示前应征得本人同意。

## 4. 运行步骤

在 PowerShell 中执行：

```powershell
cd E:\project\qiansai\pc_face_detection
python .\detect_static.py .\images\single_01.jpg
```

本机已经安装 Python 3.13 和 OpenCV 4.13，可直接运行。若在另一台电脑上缺少 OpenCV，可执行：

```powershell
python -m pip install -r .\requirements.txt
```

程序默认将结果保存到：

```text
results/single_01_detected.png
results/single_01_detections.json
```

也可以指定输出位置：

```powershell
python .\detect_static.py .\images\single_01.jpg `
  --output .\results\my_result.png `
  --json .\results\my_result.json
```

## 5. 检查结果

打开结果图片，逐项检查：

- 框是否覆盖完整人脸；
- 一张脸是否出现多个重复框；
- 多人图片是否每个人都有框；
- 背景是否被误认为人脸；
- JSON 中 `face_count` 是否与图片中的框数量一致；
- `x + width` 和 `y + height` 是否没有超出图像边界。

`stage_weight` 是 Haar 分类器的级联权重，可用于同一检测器内部排序，不是 0～1 的概率。

## 6. 参数怎么调

默认参数是：

```text
scale_factor = 1.10
min_neighbors = 5
min_size = 30
```

- 漏检较多：先把 `--min-neighbors` 调到 4，再把 `--min-size` 调小；
- 误检较多：把 `--min-neighbors` 调到 6 或 7；
- 小脸检测不到：把 `--min-size` 调到 20，但耗时和误检可能增加；
- `--scale-factor` 越接近 1，尺度搜索越细，通常更慢。

示例：

```powershell
python .\detect_static.py .\images\multi_01.jpg --min-neighbors 4 --min-size 20
```

一次只改变一个参数，并把结果记录下来，否则无法判断变化来自哪个参数。

## 7. 当天应完成的成果

最低完成标准：

- 脚本能处理任意指定 JPG/PNG；
- 至少完成 10 张不同类型图片测试；
- 每张图片都有结果图和 JSON；
- 建立一张测试记录表，填写实际人脸数、检测数、漏检数、误检数和耗时；
- 总结三种典型失败情况。

建议统计：

```text
召回率 = 正确检测到的人脸数 / 图片中实际人脸数
精确率 = 正确检测到的人脸数 / 程序输出的人脸框数
```

测试图片少时，这两个数字只用于比较参数和算法，不能当成正式模型精度。

## 8. 与 FPGA 项目的关系

电脑端结果会成为后续硬件实现的参考：

1. 确定输入图像尺寸、颜色格式和人脸框坐标定义；
2. 收集适合项目场景的测试图；
3. 明确检测算法的输入、输出和阈值；
4. 将同一张图片转换为 FPGA 像素流；
5. 比较 FPGA 输出框与电脑端黄金结果；
6. 最后再接 OSD，在 HDMI 画面上显示检测框。

如果最终采用神经网络检测器，可以在电脑端增加 YuNet 等模型作为精度参考。OpenCV 官方示例使用 `FaceDetectorYN` 加载 YuNet ONNX 模型，并输出人脸框和五个关键点。模型是否适合当前 FPGA 资源，需要经过定点化、算力、片上存储和带宽评估后决定。
