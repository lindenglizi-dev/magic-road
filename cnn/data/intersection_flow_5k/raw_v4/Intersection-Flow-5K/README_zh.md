# **Intersection-Flow-5K: 一个用于目标检测的高密度交通监控数据集**

[![Paper](https://img.shields.io/badge/Paper-arXiv:2508.19565-b31b1b.svg)](https://arxiv.org/abs/2508.19565) 
[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-blue.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/)


欢迎来到 **Intersection-Flow-5K** 数据集的官方代码库，该数据集在我们的论文中被首次提出：

> **FlowDet: Overcoming Perspective and Scale Challenges in Real-Time End-to-End Traffic Detection**
>
> *Yuhang Zhao, Zixing Wang*
>
> *PRCV, 2025*

本数据集专为解决真实世界中基于固定基础设施的交通监控所面临的独特挑战而设计。其特点包括高密度场景、极端尺度变化和持续性的严重遮挡，为现代目标检测器提供了一个富有挑战性的基准。

## **1. 数据集亮点与挑战**

现有的目标检测基准往往无法充分反映固定摄像头交通监控场景的复杂性。Intersection-Flow-5K 的创建旨在填补这一空白，提供了一系列独特的挑战：

*   **极端尺度变化**: 在单帧图像中，目标尺寸范围极广，从远处的车辆（小至 `15x15` 像素）到近处的大型卡车（超过 `800x600` 像素）。
*   **高目标密度与严重遮挡**: 数据集包含了交通高峰时段的场景，其中大量车辆重叠，导致了持续且严重的遮挡（最高达85%的遮挡物体也被标注）。
*   **多样化的环境条件**: 数据采集自7个不同的城市交叉路口，涵盖了不同时间段（白天、带眩光的夜间）和天气状况（晴天、阴天、雨天）。
*   **全面的高质量标注**: 为关键的交通参与者提供了精确、高质量的边界框标注。

该基准非常适合从事鲁棒目标检测、小目标检测、密集场景检测以及实时智能交通系统（ITS）领域的研究人员。

## **2. 数据集概览**

*   **任务类型**: 目标检测
*   **图像总数**: 6,928 张高分辨率图像 (`1920x1080`)
    *   **训练集**: 5,483 张 (70%)
    *   **验证集**: 722 张 (15%)
    *   **测试集**: 723 张 (15%)
*   **标注框总数**: 超过 95,000 个
*   **类别数量**: 8
*   **类别列表 (`classes.txt`)**:

    ```txt
    vehicle
    bus
    bicycle
    pedestrian
    engine
    truck
    tricycle
    obstacle
    ```

## **3. 目录结构**

数据集的组织结构如下：

```bash
Intersection-Flow-5K/
├── images/                   # 原始高分辨率图像
│   ├── train/                # 5,483 张
│   ├── val/                  # 722 张
│   └── test/                 # 723 张
│
├── labels/                   # YOLO .txt 格式的标注
│   ├── train/
│   ├── val/
│   └── test/
│
├── annotations/              # PASCAL VOC .xml 格式的标注
│   ├── train/
│   ├── val/
│   └── test/
│
├── test_coco.json            # COCO .json 格式的测试集标注
│
├── intersection.yaml         # 用于 YOLO 的数据集配置文件
├── classes.txt               # 类别名称列表
│
├── convert_coco.py           # coco格式转换的示例脚本 (可选)
│
└── README.md            
│
└── README_zh.md  
```

## **4. 标注格式**

为了最大化与各种检测框架的兼容性，我们提供了三种标准格式的标注：**YOLO**、**PASCAL VOC** 和 **COCO (仅测试集)**。

### **4.1 YOLO 格式 (`.txt`)**

位于 `labels/` 目录下。每张图像对应一个 `.txt` 文件，其中每一行代表一个目标。

*   **格式**: `<class_id> <x_center> <y_center> <width> <height>` (所有值均归一化到 `[0, 1]`)。
*   **示例** (对应 `1920x1080` 分辨率的 `image_001.txt`):
    ```txt
    0 0.5416 0.6111 0.1041 0.1851  # 一个 'car' 目标
    2 0.2343 0.7870 0.1562 0.2222  # 一个 'truck' 目标
    ```

### **4.2 PASCAL VOC 格式 (`.xml`)**

位于 `annotations/` 目录下。每张图像对应一个 `.xml` 文件，其中包含目标的绝对像素坐标。

*   **格式**: 边界框由 `<xmin>`, `<ymin>`, `<xmax>`, `<ymax>` 定义。
*   **示例** (`image_001.xml`):
    ```xml
    <annotation>
        ...
        <size>
            <width>1920</width>
            <height>1080</height>
        </size>
        <object>
            <name>car</name>
            <bndbox>
                <xmin>940</xmin>
                <ymin>560</ymin>
                <xmax>1140</xmax>
                <ymax>760</ymax>
            </bndbox>
        </object>
        ...
    </annotation>
    ```

### **4.3 COCO 格式 (`.json`)**

我们提供了 `test_coco.json` 文件，以便使用标准的 COCO 评估脚本轻松评测测试集。`convert_coco.py` 脚本可作为参考，用于将 YOLO/VOC 标注转换为 COCO 格式。

## **5. 如何使用**

### **5.1 在 YOLO 框架中 (例如 YOLOv8, YOLOv10)**

本数据集已为现代 YOLO 框架准备就绪。您只需在训练命令中指向提供的 `intersection.yaml` 文件即可。

1.  **修改 `intersection.yaml`**: 确保 YAML 文件中的路径相对于您的项目根目录是正确的。
    ```yaml
    # intersection.yaml
    path: /path/to/Intersection-Flow-5K  # 重要: 请更新此路径
    train: images/train
    val: images/val
    test: images/test

    # Classes
    nc: 8
    names: ['vehicle', 'bus', 'bicycle', 'pedestrian', 'engine', 'truck', 'tricycle', 'obstacle']  
    ```

2.  **开始训练**:
    ```bash
    # YOLOv8 训练示例
    yolo detect train data=intersection.yaml model=yolov8l.pt epochs=200 imgsz=640 ...
    ```

### **5.2 在 MMDetection 或 TensorFlow Object Detection API 中**

这些框架通常支持 PASCAL VOC 或 COCO 格式。

*   **使用 VOC 格式**: 将您的数据配置指向 `images/` 和 `annotations/` 目录。您可能需要为 `train`, `val`, `test` 集提供相应的文件列表。
*   **使用 COCO 格式**: 使用提供的 `test_coco.json` 进行评估。对于训练/验证，您可以使用 `convert_coco.py` 脚本从 VOC/YOLO 标注生成 `train.json` 和 `val.json`。

## **6. 如何引用**

如果您在研究中使用了 Intersection-Flow-5K 数据集，或认为我们关于 FlowDet 的工作对您有所帮助，请引用我们的论文：

```bibtex
@inproceedings{zhao2025flowdet,
  title     = {FlowDet: Overcoming Perspective and Scale Challenges in Real-Time End-to-End Traffic Detection},
  author    = {Yuhang Zhao and Zixing Wang},
  booktitle = {PRCV},
  year      = {2025}
}
```

## **7. 许可协议**

本数据集采用 [知识共享署名-非商业性使用-相同方式共享 4.0 国际许可协议 (Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License)](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.zh) 进行许可。您可以出于非商业目的自由分享和改编本材料，但必须提供适当的署名。