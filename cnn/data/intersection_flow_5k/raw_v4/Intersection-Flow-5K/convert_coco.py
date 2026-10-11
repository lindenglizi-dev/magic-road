import os
import json
import cv2
from tqdm import tqdm
import argparse

def yolo2coco_split(yolo_dataset_path, split, output_path):
    """
    将 YOLO 格式的数据集（按 train/val/test 划分）转换为 COCO 格式。

    :param yolo_dataset_path: YOLO 数据集的根目录。
    :param split: 要转换的数据子集，可选值为 'train', 'val', 'test'。
    :param output_path: 输出 COCO json 文件的完整路径。
    """

    print(f"开始转换 YOLO 数据集 '{split}' 子集到 COCO 格式...")

    # --- 1. 定义和检查路径 ---
    images_dir = os.path.join(yolo_dataset_path, 'images', split)
    labels_dir = os.path.join(yolo_dataset_path, 'labels', split)
    classes_file = os.path.join(yolo_dataset_path, 'classes.txt')
    split_file_list = os.path.join(yolo_dataset_path, f'{split}.txt')

    for p in [images_dir, labels_dir, classes_file, split_file_list]:
        if not os.path.exists(p):
            raise FileNotFoundError(f"错误: 找不到必要的文件或文件夹 '{p}'")

    # --- 2. 创建 categories 部分 ---
    print("正在读取类别信息...")
    with open(classes_file, 'r') as f:
        classes = [line.strip() for line in f.readlines()]
    
    categories = []
    for i, cls_name in enumerate(classes):
        categories.append({
            "id": i,
            "name": cls_name,
            "supercategory": "object"
        })
    print(f"共找到 {len(classes)} 个类别。")

    # --- 3. 读取指定子集的文件列表 ---
    print(f"正在从 {split_file_list} 读取文件列表...")
    with open(split_file_list, 'r') as f:
        # 读取并清理路径，只保留文件名（不含扩展名）
        # 假设 .txt 文件中的路径是类似 "./images/train/image1.jpg"
        image_paths = [line.strip() for line in f.readlines()]
        filenames = [os.path.splitext(os.path.basename(p))[0] for p in image_paths]
    print(f"将在 '{split}' 子集中处理 {len(filenames)} 张图片。")


    # --- 4. 初始化 COCO json 结构 ---
    coco_output = {
        "info": {"description": f"'{split}' split of YOLO dataset converted to COCO format."},
        "licenses": [],
        "images": [],
        "annotations": [],
        "categories": categories
    }

    image_id_counter = 1
    annotation_id_counter = 1

    print("正在处理图片和标注...")
    # --- 5. 创建 images 和 annotations 部分 ---
    for filename in tqdm(filenames, desc=f"转换 {split} 集"):
        img_path = os.path.join(images_dir, filename + '.jpg') # 假设都是 .jpg，如果不是需要修改
        
        if not os.path.exists(img_path):
             # 尝试其他可能的后缀
            found = False
            for ext in ['.jpeg', '.png']:
                potential_path = os.path.join(images_dir, filename + ext)
                if os.path.exists(potential_path):
                    img_path = potential_path
                    found = True
                    break
            if not found:
                print(f"警告: 在 {images_dir} 中找不到图片文件 {filename}，跳过。")
                continue
        
        # 读取图片尺寸
        image = cv2.imread(img_path)
        if image is None:
            print(f"警告: 无法读取图片 {img_path}，跳过。")
            continue
        height, width, _ = image.shape

        # 添加到 images 列表
        image_info = {
            "id": image_id_counter,
            "file_name": os.path.basename(img_path),
            "width": width,
            "height": height
        }
        coco_output["images"].append(image_info)

        # 处理对应的标签文件
        label_path = os.path.join(labels_dir, filename + '.txt')
        if os.path.exists(label_path):
            with open(label_path, 'r') as f:
                for line in f.readlines():
                    try:
                        class_id, cx_norm, cy_norm, w_norm, h_norm = map(float, line.strip().split())
                        
                        w_abs = w_norm * width
                        h_abs = h_norm * height
                        x_min = (cx_norm * width) - (w_abs / 2)
                        y_min = (cy_norm * height) - (h_abs / 2)

                        annotation_info = {
                            "id": annotation_id_counter,
                            "image_id": image_id_counter,
                            "category_id": int(class_id),
                            "bbox": [round(x_min, 2), round(y_min, 2), round(w_abs, 2), round(h_abs, 2)],
                            "area": round(w_abs * h_abs, 2),
                            "iscrowd": 0,
                            "segmentation": []
                        }
                        coco_output["annotations"].append(annotation_info)
                        annotation_id_counter += 1
                    except ValueError:
                        print(f"警告: 无法解析标签文件 {label_path} 中的行: '{line.strip()}'，跳过该行。")

        image_id_counter += 1

    # --- 6. 保存为 json 文件 ---
    print(f"正在保存 COCO json 文件到 {output_path}...")
    with open(output_path, 'w') as f:
        json.dump(coco_output, f, indent=4)
    
    print("\n转换完成！")
    print(f"总共处理了 {image_id_counter - 1} 张图片。")
    print(f"总共生成了 {annotation_id_counter - 1} 个标注。")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Convert YOLO dataset (with train/val/test splits) to COCO format.")
    parser.add_argument('--yolo_path', type=str, default='.', 
                        help="Path to the root directory of the YOLO dataset (default: current directory).")
    parser.add_argument('--split', type=str, required=True, choices=['train', 'val', 'test'],
                        help="Which split to convert: 'train', 'val', or 'test'.")
    parser.add_argument('--output_json', type=str, required=True, 
                        help="Path to save the output COCO format json file (e.g., 'val_coco.json').")
    
    args = parser.parse_args()
    
    yolo2coco_split(args.yolo_path, args.split, args.output_json)
