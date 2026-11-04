"""Run a simple face detector on one static image.

This is the PC reference pipeline for the FPGA face-recognition project.  It
uses OpenCV's bundled Haar cascade, so no board or extra model download is
required.  The output consists of an annotated image and a JSON file with the
detected bounding boxes.
"""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import cv2
import numpy as np


def read_image(path: Path) -> np.ndarray:
    """Read an image while supporting non-ASCII Windows paths."""
    encoded = np.fromfile(path, dtype=np.uint8)
    image = cv2.imdecode(encoded, cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError(f"无法读取图片：{path}")
    return image


def write_image(path: Path, image: np.ndarray) -> None:
    """Write an image while supporting non-ASCII Windows paths."""
    suffix = path.suffix.lower() or ".png"
    ok, encoded = cv2.imencode(suffix, image)
    if not ok:
        raise ValueError(f"无法编码输出图片：{path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    encoded.tofile(path)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="对一张静态图片进行人脸检测，保存画框图片和坐标 JSON。"
    )
    parser.add_argument("image", type=Path, help="输入 JPG/PNG 图片路径")
    parser.add_argument("--output", type=Path, help="画框结果图片路径")
    parser.add_argument("--json", dest="json_path", type=Path, help="检测结果 JSON 路径")
    parser.add_argument("--scale-factor", type=float, default=1.10, help="图像金字塔缩放比例")
    parser.add_argument("--min-neighbors", type=int, default=5, help="候选框确认阈值")
    parser.add_argument("--min-size", type=int, default=30, help="最小人脸边长（像素）")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    image_path = args.image.resolve()
    if not image_path.is_file():
        raise FileNotFoundError(f"输入图片不存在：{image_path}")
    if args.scale_factor <= 1.0:
        raise ValueError("--scale-factor 必须大于 1.0")
    if args.min_neighbors < 0 or args.min_size <= 0:
        raise ValueError("--min-neighbors 不能小于 0，--min-size 必须大于 0")

    result_dir = Path(__file__).resolve().parent / "results"
    output_path = (args.output or result_dir / f"{image_path.stem}_detected.png").resolve()
    json_path = (args.json_path or result_dir / f"{image_path.stem}_detections.json").resolve()

    image = read_image(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)

    cascade_path = Path(cv2.data.haarcascades) / "haarcascade_frontalface_default.xml"
    detector = cv2.CascadeClassifier(str(cascade_path))
    if detector.empty():
        raise RuntimeError(f"无法加载 OpenCV Haar 分类器：{cascade_path}")

    start = time.perf_counter()
    boxes, _, stage_weights = detector.detectMultiScale3(
        gray,
        scaleFactor=args.scale_factor,
        minNeighbors=args.min_neighbors,
        minSize=(args.min_size, args.min_size),
        outputRejectLevels=True,
    )
    elapsed_ms = (time.perf_counter() - start) * 1000.0

    detections: list[dict[str, float | int]] = []
    pairs = zip(boxes, stage_weights)
    for index, (box, stage_weight) in enumerate(pairs):
        x, y, width, height = (int(value) for value in box)
        score = float(stage_weight)
        detections.append(
            {
                "id": index,
                "x": x,
                "y": y,
                "width": width,
                "height": height,
                # Haar stage weight is useful for ranking, but is not a probability.
                "stage_weight": round(score, 6),
            }
        )
        cv2.rectangle(image, (x, y), (x + width, y + height), (0, 255, 0), 2)
        cv2.putText(
            image,
            f"face {index}",
            (x, max(18, y - 7)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (0, 255, 0),
            2,
            cv2.LINE_AA,
        )

    write_image(output_path, image)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    report = {
        "input_image": str(image_path),
        "output_image": str(output_path),
        "image_width": int(image.shape[1]),
        "image_height": int(image.shape[0]),
        "detector": "opencv_haar_frontalface_default",
        "parameters": {
            "scale_factor": args.scale_factor,
            "min_neighbors": args.min_neighbors,
            "min_size": args.min_size,
        },
        "elapsed_ms": round(elapsed_ms, 3),
        "face_count": len(detections),
        "faces": detections,
    }
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"检测完成：{len(detections)} 张人脸")
    print(f"耗时：{elapsed_ms:.3f} ms")
    print(f"结果图片：{output_path}")
    print(f"坐标文件：{json_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
