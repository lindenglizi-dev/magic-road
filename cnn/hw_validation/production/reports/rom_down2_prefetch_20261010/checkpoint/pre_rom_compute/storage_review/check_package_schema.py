"""Read-only integrity check for the existing schema1/schema2 TEST packages."""

from __future__ import annotations

import hashlib
import json
import re
import zlib
from pathlib import Path


HERE = Path(__file__).resolve().parent
HW_VALIDATION = HERE.parents[3]
OUTPUT = HERE / "package_schema_check.json"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def file_sha256(path: Path) -> str:
    return sha256(path.read_bytes())


def line_count(path: Path) -> int:
    with path.open("r", encoding="ascii") as handle:
        return sum(1 for _ in handle)


def segment_count(segment: dict) -> int:
    if "count" in segment:
        return segment["count"]
    count = 1
    for dimension in segment["shape"]:
        count *= dimension
    return count


def normalized_package(name: str, directory: Path) -> dict:
    manifest_path = directory / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    schema = manifest["schema_version"]
    if schema == 1:
        artifacts = manifest["artifacts"]
        layout = manifest["layout"]
        lane_entries = [
            {
                "name": entry["path"],
                "group": entry["group"],
                "lane": entry["lane"],
                "lines": entry["lines"],
                "sha256": entry["sha256"],
            }
            for entry in artifacts["lane_files"]
        ]
        return {
            "name": name,
            "directory": directory,
            "manifest_path": manifest_path,
            "manifest": manifest,
            "payload_path": directory / artifacts["payload"]["path"],
            "payload_sha256": artifacts["payload"]["sha256"],
            "padded_path": directory / artifacts["padded"]["path"],
            "padded_sha256": artifacts["padded"]["sha256"],
            "crc32": artifacts["crc32"]["value_hex"].lower(),
            "words_path": directory / artifacts["words"]["path"],
            "words_sha256": artifacts["words"]["sha256"],
            "words_lines": artifacts["words"]["lines"],
            "lane_entries": lane_entries,
            "payload_bytes": layout["payload_bytes"],
            "padded_bytes": layout["padded_bytes"],
            "padding_bytes": layout["padding_bytes"],
            "word_bytes": layout["word_bytes"],
            "words_per_group": layout["words_per_group"],
            "groups": layout["group_count"],
            "lanes": layout["physical_lane_count"],
            "lane_bytes": layout["physical_lane_bytes"],
        }
    if schema == 2:
        layout = manifest["layout"]
        lane_entries = []
        for entry in manifest["lane_files"]:
            match = re.fullmatch(r"group_(\d+)_lane_(\d+)\.dath", entry["name"])
            if not match:
                raise ValueError(f"unexpected schema2 lane name: {entry['name']}")
            lane_entries.append(
                {
                    "name": entry["name"],
                    "group": int(match.group(1)),
                    "lane": int(match.group(2)),
                    "lines": layout["words_per_group"],
                    "sha256": entry["sha256"],
                }
            )
        return {
            "name": name,
            "directory": directory,
            "manifest_path": manifest_path,
            "manifest": manifest,
            "payload_path": directory / "numeric_test.bin",
            "payload_sha256": manifest["payload_sha256"],
            "padded_path": directory / "numeric_test_padded.bin",
            "padded_sha256": manifest["physical_sha256"],
            "crc32": manifest["physical_crc32"].lower(),
            "words_path": directory / "words.dath",
            "words_sha256": None,
            "words_lines": layout["groups"] * layout["words_per_group"],
            "lane_entries": lane_entries,
            "payload_bytes": manifest["payload_bytes"],
            "padded_bytes": manifest["payload_bytes"] + manifest["padding_bytes"],
            "padding_bytes": manifest["padding_bytes"],
            "word_bytes": layout["word_bytes"],
            "words_per_group": layout["words_per_group"],
            "groups": layout["groups"],
            "lanes": layout["lanes"],
            "lane_bytes": layout["lane_bytes"],
        }
    raise ValueError(f"unsupported schema: {schema}")


def check_package(package: dict) -> dict:
    manifest = package["manifest"]
    payload = package["payload_path"].read_bytes()
    padded = package["padded_path"].read_bytes()
    segments = manifest["segments"]
    errors: list[str] = []

    def check(condition: bool, message: str) -> None:
        if not condition:
            errors.append(message)

    check(len(payload) == package["payload_bytes"], "payload length mismatch")
    check(len(padded) == package["padded_bytes"], "padded length mismatch")
    check(len(padded) - len(payload) == package["padding_bytes"], "padding length mismatch")
    check(padded[: len(payload)] == payload, "padded prefix differs from payload")
    check(set(padded[len(payload) :]) <= {0}, "padding is not all zero")
    check(sha256(payload) == package["payload_sha256"], "payload SHA256 mismatch")
    check(sha256(padded) == package["padded_sha256"], "padded SHA256 mismatch")
    check(f"{zlib.crc32(padded) & 0xffffffff:08x}" == package["crc32"], "padded CRC32 mismatch")

    cursor = 0
    segment_hash_failures = 0
    segment_count_length_failures = 0
    dtype_bytes = {"int8": 1, "uint8": 1, "int16": 2, "uint16": 2, "<i2": 2, "<u2": 2, "int32_le": 4}
    for index, segment in enumerate(segments):
        offset = segment["offset"]
        length = segment["length"]
        check(offset == cursor, f"segment {index} is not contiguous at offset {offset}, expected {cursor}")
        cursor = offset + length
        if sha256(payload[offset:cursor]) != segment["sha256"]:
            segment_hash_failures += 1
        width = dtype_bytes.get(segment["dtype"])
        if width is None or segment_count(segment) * width != length:
            segment_count_length_failures += 1
    check(cursor == len(payload), "segments do not cover the payload exactly")
    check(segment_hash_failures == 0, f"{segment_hash_failures} segment SHA256 mismatches")
    check(segment_count_length_failures == 0, f"{segment_count_length_failures} segment count/length mismatches")

    layer_segment_failures = 0
    segments_by_name = {segment["name"]: segment for segment in segments}
    for layer in manifest["layers"]:
        if "segment_names" in layer:
            owned = [segments_by_name.get(name) for name in layer["segment_names"]]
            if any(segment is None for segment in owned):
                layer_segment_failures += 1
                continue
            if min(segment["offset"] for segment in owned) != layer["offset"]:
                layer_segment_failures += 1
            if max(segment["offset"] + segment["length"] for segment in owned) != layer["end_offset_exclusive"]:
                layer_segment_failures += 1
        else:
            for field, offset in layer["fields"].items():
                segment = segments_by_name.get(f"{layer['name']}.{field}")
                if segment is None or segment["offset"] != offset:
                    layer_segment_failures += 1
    check(layer_segment_failures == 0, f"{layer_segment_failures} layer boundary/segment mismatches")

    expected_lane_pairs = {(group, lane) for group in range(package["groups"]) for lane in range(package["lanes"])}
    actual_lane_pairs = {(entry["group"], entry["lane"]) for entry in package["lane_entries"]}
    check(actual_lane_pairs == expected_lane_pairs, "lane group/index coverage mismatch")
    lane_hash_failures = 0
    lane_line_failures = 0
    lane_content_failures = 0
    for entry in package["lane_entries"]:
        path = package["directory"] / entry["name"]
        if file_sha256(path) != entry["sha256"]:
            lane_hash_failures += 1
        if line_count(path) != entry["lines"]:
            lane_line_failures += 1
        actual_lines = path.read_text(encoding="ascii").splitlines()
        group_base = entry["group"] * package["words_per_group"] * package["word_bytes"]
        expected_lines = []
        for word_index in range(package["words_per_group"]):
            lane_base = group_base + word_index * package["word_bytes"] + entry["lane"] * package["lane_bytes"]
            expected_lines.append(padded[lane_base : lane_base + package["lane_bytes"]][::-1].hex())
        if actual_lines != expected_lines:
            lane_content_failures += 1
    check(lane_hash_failures == 0, f"{lane_hash_failures} lane SHA256 mismatches")
    check(lane_line_failures == 0, f"{lane_line_failures} lane line-count mismatches")
    check(lane_content_failures == 0, f"{lane_content_failures} lane reconstruction mismatches")

    actual_word_lines = package["words_path"].read_text(encoding="ascii").splitlines()
    expected_word_lines = [
        padded[offset : offset + package["word_bytes"]][::-1].hex()
        for offset in range(0, len(padded), package["word_bytes"])
    ]
    check(len(actual_word_lines) == package["words_lines"], "word file line-count mismatch")
    check(actual_word_lines == expected_word_lines, "word file does not reconstruct padded bytes")
    if package["words_sha256"] is not None:
        check(file_sha256(package["words_path"]) == package["words_sha256"], "word file SHA256 mismatch")

    roles: dict[str, dict[str, int]] = {}
    for segment in segments:
        role = segment.get("role") or segment.get("kind") or "schema1_name_encoded"
        aggregate = roles.setdefault(role, {"segments": 0, "bytes": 0, "values": 0})
        aggregate["segments"] += 1
        aggregate["bytes"] += segment["length"]
        aggregate["values"] += segment_count(segment)

    return {
        "schema_version": manifest["schema_version"],
        "status": manifest["status"],
        "manifest_sha256": file_sha256(package["manifest_path"]),
        "payload": {
            "bytes": len(payload),
            "sha256_expected": package["payload_sha256"],
            "sha256_actual": sha256(payload),
        },
        "physical": {
            "bytes": len(padded),
            "padding_bytes": package["padding_bytes"],
            "sha256_expected": package["padded_sha256"],
            "sha256_actual": sha256(padded),
            "crc32_expected": package["crc32"],
            "crc32_actual": f"{zlib.crc32(padded) & 0xffffffff:08x}",
            "geometry": {
                "groups": package["groups"],
                "words_per_group": package["words_per_group"],
                "word_bits": package["word_bytes"] * 8,
                "lanes": package["lanes"],
                "lane_bits": package["lane_bytes"] * 8,
                "total_words": package["groups"] * package["words_per_group"],
            },
        },
        "fields": {
            "segments": len(segments),
            "contiguous_coverage": cursor == len(payload),
            "segment_sha256_failures": segment_hash_failures,
            "count_length_failures": segment_count_length_failures,
            "layer_boundary_failures": layer_segment_failures,
            "role_aggregates": roles,
        },
        "lane_files": {
            "count": len(package["lane_entries"]),
            "expected_count": package["groups"] * package["lanes"],
            "lines_each": package["words_per_group"],
            "sha256_failures": lane_hash_failures,
            "line_count_failures": lane_line_failures,
            "padded_byte_reconstruction_failures": lane_content_failures,
        },
        "words_file": {
            "lines": len(actual_word_lines),
            "expected_lines": package["words_lines"],
            "padded_byte_reconstruction_match": actual_word_lines == expected_word_lines,
            "sha256_actual": file_sha256(package["words_path"]),
        },
        "errors": errors,
        "integrity_pass": not errors,
    }


def main() -> int:
    packages = [
        normalized_package("schema1_historical_test", HW_VALIDATION / "rom" / "artifacts"),
        normalized_package("schema2_current_test", HW_VALIDATION / "production" / "numeric_artifacts"),
    ]
    checks = {package["name"]: check_package(package) for package in packages}
    first_payload_difference = next(
        (index for index, pair in enumerate(zip(packages[0]["payload_path"].read_bytes(), packages[1]["payload_path"].read_bytes())) if pair[0] != pair[1]),
        None,
    )
    schema1_segments = packages[0]["manifest"]["segments"]
    schema2_segments = packages[1]["manifest"]["segments"]
    offset_length_count_equal = [
        (item["offset"], item["length"], segment_count(item)) for item in schema1_segments
    ] == [
        (item["offset"], item["length"], segment_count(item)) for item in schema2_segments
    ]
    report = {
        "schema": "road-yolo-package-schema-check-v1",
        "date": "2026-10-10",
        "operation": "read_only_existing_artifacts_no_regeneration",
        "overall_integrity_pass": all(item["integrity_pass"] for item in checks.values()),
        "packages": checks,
        "comparison": {
            "same_payload_length": packages[0]["payload_bytes"] == packages[1]["payload_bytes"],
            "same_physical_geometry": all(
                packages[0][key] == packages[1][key]
                for key in ("padded_bytes", "word_bytes", "words_per_group", "groups", "lanes", "lane_bytes")
            ),
            "same_segment_offset_length_count_layout": offset_length_count_equal,
            "payload_sha256_equal": packages[0]["payload_sha256"] == packages[1]["payload_sha256"],
            "first_payload_difference_offset": first_payload_difference,
            "field_semantics_equal": False,
            "semantic_difference": {
                "schema1_per_channel": "output requant",
                "schema2_per_channel": "accumulator to Q7.8 pre-SiLU",
                "schema1_per_silu_layer": "pre-SiLU pair",
                "schema2_per_silu_layer": "SiLU to INT8 post",
            },
            "interchangeable": False,
            "reason": "The 14x512x160 geometry is reusable, but schema, field meanings, payload SHA256, padded SHA256, and CRC32 differ.",
        },
        "evidence_boundary": [
            "Both packages are deterministic TEST fixtures, not E7/QAT/trained deployment weights.",
            "Integrity checks do not prove ROM RTL addressing, vendor initialization, synthesis mapping, or runtime readback.",
        ],
    }
    OUTPUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}")
    return 0 if report["overall_integrity_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
