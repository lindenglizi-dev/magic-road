# **Intersection-Flow-5K: A High-Density Traffic Surveillance Dataset for Object Detection**

[![Paper](https://img.shields.io/badge/Paper-arXiv:2508.19565-b31b1b.svg)](https://arxiv.org/abs/2508.19565)  
[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-blue.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/)

Welcome to the official repository for the **Intersection-Flow-5K** dataset, introduced in our paper:

> **FlowDet: Overcoming Perspective and Scale Challenges in Real-Time End-to-End Traffic Detection**
>
> *Yuhang Zhao, Zixing Wang*
>
> *PRCV, 2025*

This dataset is specifically designed to address the unique challenges of real-world, infrastructure-based traffic monitoring. It features high-density scenes, extreme scale variations, and severe, persistent occlusions, providing a challenging benchmark for modern object detectors.

## **1. Dataset Highlights & Challenges**

Existing object detection benchmarks often fall short of capturing the complexities of fixed-camera traffic surveillance. Intersection-Flow-5K was created to fill this gap, offering a unique set of challenges:

*   **Extreme Scale Variation**: Objects range from distant vehicles appearing as small as `15x15` pixels to large trucks occupying over `800x600` pixels within a single frame.
*   **High Object Density & Severe Occlusion**: The dataset includes rush-hour scenes with numerous overlapping vehicles, leading to persistent and severe occlusions (up to 75% annotated).
*   **Diverse Environmental Conditions**: Data was collected from 7 distinct urban intersections, covering various times of day (daylight, nighttime with glare) and weather conditions (clear, overcast, rainy).
*   **Comprehensive Annotations**: Meticulously annotated with high-quality bounding boxes for crucial traffic participants.

This benchmark is ideal for researchers working on robust object detection, small object detection, detection in crowded scenes, and real-time intelligent transportation systems (ITS).

## **2. Dataset Overview**

*   **Task Type**: Object Detection
*   **Total Images**: 6,928 high-resolution (`1920x1080`) images
    *   **Training Set**: 5,483 images (80%)
    *   **Validation Set**: 722 images (10%)
    *   **Test Set**: 723 images (10%)
*   **Total Annotations**: Over 95,000 bounding boxes
*   **Number of Categories**: 8
*   **Category List (`classes.txt`)**:

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

## **3. Directory Structure**

The dataset is organized as follows:

```bash
Intersection-Flow-5K/
├── images/                   # Original high-resolution images
│   ├── train/                # 5,483 images
│   ├── val/                  # 722 images
│   └── test/                 # 723 images
│
├── labels/                   # Annotations in YOLO .txt format
│   ├── train/
│   ├── val/
│   └── test/
│
├── annotations/              # Annotations in PASCAL VOC .xml format
│   ├── train/
│   ├── val/
│   └── test/
│
├── test_coco.json            # Annotations for the test set in COCO .json format
│
├── intersection.yaml         # Dataset configuration file for YOLO
├── classes.txt               # List of class names
│
├── convert_coco.py           # Example script for coco format conversion (optional)
│
└── README.md            
│
└── README_zh.md  

```

## **4. Annotation Formats**

To maximize compatibility with various detection frameworks, we provide annotations in three standard formats: **YOLO**, **PASCAL VOC**, and **COCO (for the test set)**.

### **4.1 YOLO Format (`.txt`)**

Located in the `labels/` directory. Each image has a corresponding `.txt` file where each line represents an object.

*   **Format**: `<class_id> <x_center> <y_center> <width> <height>` (all values are normalized to `[0, 1]`).
*   **Example** (`image_001.txt` for a `1920x1080` image):
    ```txt
    0 0.5416 0.6111 0.1041 0.1851  # A 'car' object
    2 0.2343 0.7870 0.1562 0.2222  # A 'truck' object
    ```

### **4.2 PASCAL VOC Format (`.xml`)**

Located in the `annotations/` directory. Each image has a corresponding `.xml` file containing object bounding boxes in absolute pixel coordinates.

*   **Format**: Bounding boxes are defined by `<xmin>`, `<ymin>`, `<xmax>`, `<ymax>`.
*   **Example** (`image_001.xml`):
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

### **4.3 COCO Format (`.json`)**

We provide `test_coco.json` for easy evaluation of the test set using standard COCO evaluation scripts. The `convert_coco.py` script can be used as a reference to convert YOLO/VOC annotations to the COCO format if needed for your custom splits.

## **5. How to Use**

### **5.1 With YOLO Frameworks (YOLOv8, YOLOv10, etc.)**

This dataset is ready to use with modern YOLO frameworks. Just point your training command to the provided `intersection.yaml` file.

1.  **Modify `intersection.yaml`**: Ensure the paths in the YAML file are correct relative to your project's root directory.
    ```yaml
    # intersection.yaml
    path: /path/to/Intersection-Flow-5K  # IMPORTANT: Update this path
    train: images/train
    val: images/val
    test: images/test

    # Classes
    nc: 8
    names: ['vehicle', 'bus', 'bicycle', 'pedestrian', 'engine', 'truck', 'tricycle', 'obstacle']  
    ```

2.  **Start Training**:
    ```bash
    # Example for YOLOv8
    yolo detect train data=intersection.yaml model=yolov8l.pt epochs=200 imgsz=640 ...
    ```

### **5.2 With MMDetection or TensorFlow Object Detection API**

These frameworks typically support PASCAL VOC or COCO formats.

*   **For VOC Format**: Point your data configuration to use the `images/` and `annotations/` directories. You will need to provide a file list for the `train`, `val`, and `test` splits.
*   **For COCO Format**: Use the provided `test_coco.json` for evaluation. For training/validation, you can use the `convert_coco.py` script to generate `train.json` and `val.json` from the VOC/YOLO annotations.

## **6. Citation**

If you use the Intersection-Flow-5K dataset or find our work on FlowDet beneficial to your research, please cite our paper:

```bibtex
@inproceedings{zhao2025flowdet,
  title     = {FlowDet: Overcoming Perspective and Scale Challenges in Real-Time End-to-End Traffic Detection},
  author    = {Yuhang Zhao and Zixing Wang},
  booktitle = {PRCV},
  year      = {2025}
}
```

## **7. License**

This dataset is licensed under the [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License](https://creativecommons.org/licenses/by-nc-sa/4.0/). You are free to share and adapt the material for non-commercial purposes, provided you give appropriate credit.
