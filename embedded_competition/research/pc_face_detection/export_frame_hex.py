"""Convert an image into the RGB888 HEX stream used by the RTL testbench."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import cv2
import numpy as np


def read_image(path: Path) -> np.ndarray:
    encoded = np.fromfile(path, dtype=np.uint8)
    image = cv2.imdecode(encoded, cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError(f"无法读取图片：{path}")
    return image


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="导出RTL仿真使用的逐像素RGB888 HEX文件")
    parser.add_argument("image", type=Path, help="输入图片")
    parser.add_argument("--output", type=Path, required=True, help="输出HEX文件")
    parser.add_argument("--width", type=int, default=1024)
    parser.add_argument("--height", type=int, default=600)
    parser.add_argument(
        "--strict-size",
        action="store_true",
        help="要求输入尺寸完全一致，不执行缩放",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    source = args.image.resolve()
    output = args.output.resolve()
    if not source.is_file():
        raise FileNotFoundError(f"输入图片不存在：{source}")
    if args.width <= 0 or args.height <= 0:
        raise ValueError("宽度和高度必须大于0")

    bgr = read_image(source)
    source_height, source_width = bgr.shape[:2]
    if args.strict_size and (source_width != args.width or source_height != args.height):
        raise ValueError(
            f"输入尺寸为{source_width}x{source_height}，要求{args.width}x{args.height}"
        )
    if source_width != args.width or source_height != args.height:
        bgr = cv2.resize(bgr, (args.width, args.height), interpolation=cv2.INTER_AREA)

    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="ascii", newline="\n") as stream:
        for row in rgb:
            for red, green, blue in row:
                stream.write(f"{int(red):02X}{int(green):02X}{int(blue):02X}\n")

    metadata = {
        "source": str(source),
        "hex_file": str(output),
        "width": args.width,
        "height": args.height,
        "pixel_count": args.width * args.height,
        "format": "RGB888",
        "word_format": "RRGGBB",
        "scan_order": "row-major, top-to-bottom, left-to-right",
    }
    metadata_path = output.with_suffix(output.suffix + ".json")
    metadata_path.write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print(f"已输出{metadata['pixel_count']}个RGB888像素")
    print(f"HEX：{output}")
    print(f"元数据：{metadata_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
