"""Export quantized NumPy arrays to Verilog $readmemh files.

Expected convention:
  * convolution weights: int8 arrays in OIHW order
  * fully connected weights: int8 arrays in output-input order
  * biases: int32 arrays

Every scalar is written on its own line in C-order. Signed values are encoded
as two's-complement hexadecimal words.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np


SUPPORTED_DTYPES = {
    np.dtype("int8"): (8, 2),
    np.dtype("uint8"): (8, 2),
    np.dtype("int16"): (16, 4),
    np.dtype("uint16"): (16, 4),
    np.dtype("int32"): (32, 8),
    np.dtype("uint32"): (32, 8),
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="将量化NPZ参数导出为RTL使用的$readmemh文件"
    )
    parser.add_argument("npz", type=Path, help="包含整数权重和偏置的NPZ文件")
    parser.add_argument("output_dir", type=Path, help="MEM文件输出目录")
    return parser.parse_args()


def encode_scalar(value: int, bits: int, hex_digits: int) -> str:
    mask = (1 << bits) - 1
    return f"{value & mask:0{hex_digits}X}"


def main() -> int:
    args = parse_args()
    source = args.npz.resolve()
    output_dir = args.output_dir.resolve()
    if not source.is_file():
        raise FileNotFoundError(f"NPZ文件不存在：{source}")

    output_dir.mkdir(parents=True, exist_ok=True)
    manifest: dict[str, object] = {
        "source": str(source),
        "flatten_order": "C",
        "arrays": {},
    }

    with np.load(source, allow_pickle=False) as archive:
        for name in sorted(archive.files):
            array = np.asarray(archive[name])
            if array.dtype not in SUPPORTED_DTYPES:
                raise TypeError(
                    f"{name}的数据类型为{array.dtype}，只支持整数8/16/32位"
                )
            bits, hex_digits = SUPPORTED_DTYPES[array.dtype]
            safe_name = name.replace("/", "_").replace(".", "_")
            mem_path = output_dir / f"{safe_name}.mem"
            flat = array.reshape(-1, order="C")
            with mem_path.open("w", encoding="ascii", newline="\n") as stream:
                for value in flat:
                    stream.write(encode_scalar(int(value), bits, hex_digits) + "\n")

            manifest["arrays"][name] = {
                "file": mem_path.name,
                "shape": list(array.shape),
                "dtype": str(array.dtype),
                "bits": bits,
                "element_count": int(array.size),
            }
            print(f"{name}: {array.shape} {array.dtype} -> {mem_path.name}")

    manifest_path = output_dir / "weights_manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"清单：{manifest_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
