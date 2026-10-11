"""Build the deterministic seed-42 ROM test package and physical lane files."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import zlib
from pathlib import Path
from typing import Any

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from cnn.integer import tables  # noqa: E402
from cnn.model import RoadYOLOS4  # noqa: E402


SEED = 42
PAYLOAD_BYTES = 140_522
PADDED_BYTES = 143_360
WORD_BYTES = 20
LANE_BYTES = 5
WORDS_PER_GROUP = 512
GROUP_BYTES = WORD_BYTES * WORDS_PER_GROUP
GROUP_COUNT = 14
STATUS = "deterministic_test_fixture_not_trained_model_or_frozen_deployment_artifact"


def sha256(data: bytes) -> str:
    """Return a lowercase SHA-256 digest."""
    return hashlib.sha256(data).hexdigest()


def source_sha256(relative_path: str) -> str:
    """Hash one package-defining project source file."""
    return sha256((PROJECT_ROOT / relative_path).read_bytes())


def is_silu_layer(layer_name: str) -> bool:
    """The six detection output convolutions intentionally omit SiLU."""
    return not layer_name.endswith((".cls_out", ".reg_out"))


def make_segment(name: str, kind: str, data: bytes, offset: int,
                 **metadata: Any) -> dict[str, Any]:
    """Describe one contiguous payload segment."""
    end = offset + len(data)
    segment = {
        "name": name,
        "kind": kind,
        "offset": offset,
        "length": len(data),
        "end_offset_exclusive": end,
        "sha256": sha256(data),
        "start_word": offset // WORD_BYTES,
        "start_byte_in_word": offset % WORD_BYTES,
        "end_word": (end - 1) // WORD_BYTES,
        "end_byte_in_word": (end - 1) % WORD_BYTES,
        "start_group": offset // GROUP_BYTES,
        "end_group": (end - 1) // GROUP_BYTES,
    }
    segment.update(metadata)
    return segment


def encode_lane_line(chunk: bytes) -> str:
    """Encode five little-endian package bytes as one 40-bit hex word."""
    if len(chunk) != LANE_BYTES:
        raise ValueError("lane chunk must contain exactly five bytes")
    return chunk[::-1].hex()


def build_payload() -> tuple[bytes, dict[str, Any]]:
    """Create payload bytes and their self-describing manifest."""
    rng = np.random.Generator(np.random.PCG64(SEED))
    architecture = RoadYOLOS4().architecture_manifest()
    layers = architecture["layers"]
    payload = bytearray()
    segments: list[dict[str, Any]] = []
    layer_records: list[dict[str, Any]] = []
    counts = {
        "layers": 0,
        "silu_layers": 0,
        "weights_int8": 0,
        "bias_int32": 0,
        "output_requant_pairs": 0,
        "pre_silu_requant_pairs": 0,
    }

    def append(name: str, kind: str, data: bytes, **metadata: Any) -> dict[str, Any]:
        segment = make_segment(name, kind, data, len(payload), **metadata)
        payload.extend(data)
        segments.append(segment)
        return segment

    for layer_index, layer in enumerate(layers):
        layer_name = str(layer["name"])
        output_channels = int(layer["out_channels"])
        weight_shape = [
            output_channels,
            int(layer["in_channels"]) // int(layer["groups"]),
            int(layer["kernel"][0]),
            int(layer["kernel"][1]),
        ]
        weight_count = int(np.prod(weight_shape, dtype=np.int64))
        weights = rng.integers(-128, 128, size=weight_count,
                               dtype=np.int16).astype(np.int8).tobytes()
        biases = rng.integers(-1_000_000, 1_000_001, size=output_channels,
                             dtype=np.int32).astype("<i4", copy=False).tobytes()
        multipliers = rng.integers(1, 1 << 30, size=output_channels,
                                  dtype=np.int32).astype("<i4", copy=False).tobytes()
        shifts = rng.integers(0, 63, size=output_channels, dtype=np.uint8).tobytes()
        layer_segments = [
            append(f"{layer_name}.weights", "weights_int8", weights,
                   layer_index=layer_index, shape=weight_shape, dtype="int8"),
            append(f"{layer_name}.bias", "folded_bias_int32", biases,
                   layer_index=layer_index, shape=[output_channels], dtype="int32_le"),
            append(f"{layer_name}.requant_multiplier", "output_requant_multiplier_int32",
                   multipliers, layer_index=layer_index, shape=[output_channels],
                   dtype="int32_le"),
            append(f"{layer_name}.requant_shift", "output_requant_shift_uint8", shifts,
                   layer_index=layer_index, shape=[output_channels], dtype="uint8"),
        ]
        has_silu = is_silu_layer(layer_name)
        if has_silu:
            pre_multiplier = rng.integers(1, 1 << 30, dtype=np.int32)
            pre_shift = rng.integers(0, 63, dtype=np.uint8)
            layer_segments.extend([
                append(f"{layer_name}.pre_silu_multiplier",
                       "pre_silu_requant_multiplier_int32",
                       np.asarray([pre_multiplier], dtype="<i4").tobytes(),
                       layer_index=layer_index, shape=[1], dtype="int32_le"),
                append(f"{layer_name}.pre_silu_shift", "pre_silu_requant_shift_uint8",
                       np.asarray([pre_shift], dtype=np.uint8).tobytes(),
                       layer_index=layer_index, shape=[1], dtype="uint8"),
            ])
            counts["silu_layers"] += 1
            counts["pre_silu_requant_pairs"] += 1
        layer_records.append({
            "index": layer_index,
            "name": layer_name,
            "weight_shape": weight_shape,
            "output_channels": output_channels,
            "has_silu": has_silu,
            "offset": layer_segments[0]["offset"],
            "end_offset_exclusive": layer_segments[-1]["end_offset_exclusive"],
            "segment_names": [segment["name"] for segment in layer_segments],
        })
        counts["layers"] += 1
        counts["weights_int8"] += weight_count
        counts["bias_int32"] += output_channels
        counts["output_requant_pairs"] += output_channels

    shared_tables = tables()
    lut_inputs = (
        ("shared_lut.silu", "silu_lut_int16", np.asarray(shared_tables["silu"], dtype="<i2")),
        ("shared_lut.sigmoid", "sigmoid_lut_uint16",
         np.asarray(shared_tables["sigmoid"], dtype="<u2")),
        ("shared_lut.exp", "exp_lut_uint16", np.asarray(shared_tables["exp"], dtype="<u2")),
    )
    for name, kind, array in lut_inputs:
        append(name, kind, array.tobytes(), shape=[int(array.size)], dtype=str(array.dtype))

    if counts != {
        "layers": 67,
        "silu_layers": 61,
        "weights_int8": 113_100,
        "bias_int32": 2_501,
        "output_requant_pairs": 2_501,
        "pre_silu_requant_pairs": 61,
    }:
        raise AssertionError(f"architecture count mismatch: {counts}")
    if len(payload) != PAYLOAD_BYTES:
        raise AssertionError(f"payload is {len(payload)} bytes, expected {PAYLOAD_BYTES}")

    manifest = {
        "schema_version": 1,
        "status": STATUS,
        "seed": SEED,
        "rng": "numpy.random.Generator(PCG64)",
        "byte_order": "little",
        "architecture_name": architecture["name"],
        "source_sha256": {
            path: source_sha256(path)
            for path in ("cnn/contract.json", "cnn/integer.py", "cnn/model.py")
        },
        "layout": {
            "payload_bytes": PAYLOAD_BYTES,
            "padded_bytes": PADDED_BYTES,
            "padding_bytes": PADDED_BYTES - PAYLOAD_BYTES,
            "word_bytes": WORD_BYTES,
            "words_per_group": WORDS_PER_GROUP,
            "group_bytes": GROUP_BYTES,
            "group_count": GROUP_COUNT,
            "physical_lane_count": 4,
            "physical_lane_bytes": LANE_BYTES,
        },
        "counts": counts,
        "layers": layer_records,
        "segments": segments,
        "lut_constants": {
            "silu_upper": int(shared_tables["silu_upper"]),
            "sigmoid_upper": int(shared_tables["sigmoid_upper"]),
        },
    }
    return bytes(payload), manifest


def write_package(output_dir: Path) -> dict[str, Any]:
    """Write payload, padded image, manifest, and 56 physical lane files."""
    output_dir.mkdir(parents=True, exist_ok=True)
    payload, manifest = build_payload()
    padded = payload + bytes(PADDED_BYTES - len(payload))
    payload_path = output_dir / "numeric_test_seed42.bin"
    padded_path = output_dir / "numeric_test_seed42_padded.bin"
    words_path = output_dir / "numeric_test_seed42_words.dath"
    checksum_path = output_dir / "numeric_test_seed42_crc32.vh"
    payload_path.write_bytes(payload)
    padded_path.write_bytes(padded)
    word_lines = [
        padded[offset:offset + WORD_BYTES][::-1].hex()
        for offset in range(0, PADDED_BYTES, WORD_BYTES)
    ]
    word_text = "\n".join(word_lines) + "\n"
    words_path.write_text(word_text, encoding="ascii", newline="\n")
    checksum = zlib.crc32(padded) & 0xFFFFFFFF
    checksum_text = f"localparam [31:0] C_EXPECTED_CHECKSUM = 32'h{checksum:08X};\n"
    checksum_path.write_text(checksum_text, encoding="ascii", newline="\n")

    lane_files = []
    for group_index in range(GROUP_COUNT):
        group = padded[group_index * GROUP_BYTES:(group_index + 1) * GROUP_BYTES]
        for lane_index in range(4):
            lines = []
            for word_index in range(WORDS_PER_GROUP):
                base = word_index * WORD_BYTES + lane_index * LANE_BYTES
                lines.append(encode_lane_line(group[base:base + LANE_BYTES]))
            lane_name = f"group_{group_index:02d}_lane_{lane_index}.dath"
            lane_text = "\n".join(lines) + "\n"
            (output_dir / lane_name).write_text(lane_text, encoding="ascii", newline="\n")
            lane_files.append({
                "group": group_index,
                "lane": lane_index,
                "path": lane_name,
                "lines": WORDS_PER_GROUP,
                "sha256": sha256(lane_text.encode("ascii")),
            })

    manifest["artifacts"] = {
        "payload": {"path": payload_path.name, "sha256": sha256(payload)},
        "padded": {"path": padded_path.name, "sha256": sha256(padded)},
        "words": {"path": words_path.name, "lines": len(word_lines),
                  "sha256": sha256(word_text.encode("ascii"))},
        "crc32": {"path": checksum_path.name, "value_hex": f"{checksum:08x}",
                  "sha256": sha256(checksum_text.encode("ascii"))},
        "lane_files": lane_files,
    }
    manifest_path = output_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
                             encoding="utf-8", newline="\n")
    return manifest


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path,
                        default=Path(__file__).resolve().parent / "artifacts")
    return parser.parse_args()


if __name__ == "__main__":
    written_manifest = write_package(parse_args().output_dir)
    print(json.dumps({
        "status": written_manifest["status"],
        "payload_sha256": written_manifest["artifacts"]["payload"]["sha256"],
        "padded_sha256": written_manifest["artifacts"]["padded"]["sha256"],
        "segments": len(written_manifest["segments"]),
        "lane_files": len(written_manifest["artifacts"]["lane_files"]),
    }, indent=2))
