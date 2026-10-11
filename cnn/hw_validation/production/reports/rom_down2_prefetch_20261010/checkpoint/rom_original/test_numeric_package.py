"""Regression tests for the deterministic numeric ROM package."""

from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
import zlib
from pathlib import Path

import numpy as np

from generate_numeric_package import (
    GROUP_BYTES,
    GROUP_COUNT,
    LANE_BYTES,
    PADDED_BYTES,
    PAYLOAD_BYTES,
    STATUS,
    WORD_BYTES,
    WORDS_PER_GROUP,
    build_payload,
    write_package,
)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def decode_lane_file(path: Path) -> list[bytes]:
    lines = path.read_text(encoding="ascii").splitlines()
    if len(lines) != WORDS_PER_GROUP:
        raise AssertionError(f"{path.name} has {len(lines)} lines")
    return [bytes.fromhex(line)[::-1] for line in lines]


class NumericPackageTest(unittest.TestCase):
    def test_payload_is_repeatable_and_manifest_is_contiguous(self) -> None:
        first, first_manifest = build_payload()
        second, second_manifest = build_payload()
        self.assertEqual(first, second)
        self.assertEqual(first_manifest, second_manifest)
        self.assertEqual(len(first), PAYLOAD_BYTES)
        self.assertEqual(first_manifest["status"], STATUS)
        expected_offset = 0
        for segment in first_manifest["segments"]:
            self.assertEqual(segment["offset"], expected_offset)
            end = segment["end_offset_exclusive"]
            self.assertEqual(digest(first[expected_offset:end]), segment["sha256"])
            expected_offset = end
        self.assertEqual(expected_offset, PAYLOAD_BYTES)

    def test_files_reconstruct_every_padded_byte(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output_dir = Path(temporary)
            manifest = write_package(output_dir)
            payload = (output_dir / manifest["artifacts"]["payload"]["path"]).read_bytes()
            padded = (output_dir / manifest["artifacts"]["padded"]["path"]).read_bytes()
            self.assertEqual(len(payload), PAYLOAD_BYTES)
            self.assertEqual(len(padded), PADDED_BYTES)
            self.assertEqual(padded[:PAYLOAD_BYTES], payload)
            self.assertEqual(padded[PAYLOAD_BYTES:], bytes(PADDED_BYTES - PAYLOAD_BYTES))
            reconstructed = bytearray()
            for group_index in range(GROUP_COUNT):
                lane_words = [
                    decode_lane_file(output_dir / f"group_{group_index:02d}_lane_{lane}.dath")
                    for lane in range(4)
                ]
                for word_index in range(WORDS_PER_GROUP):
                    word = b"".join(lane_words[lane][word_index] for lane in range(4))
                    self.assertEqual(len(word), WORD_BYTES)
                    reconstructed.extend(word)
            self.assertEqual(bytes(reconstructed), padded)
            self.assertEqual(digest(payload), manifest["artifacts"]["payload"]["sha256"])
            self.assertEqual(digest(padded), manifest["artifacts"]["padded"]["sha256"])
            self.assertEqual(len(manifest["artifacts"]["lane_files"]), GROUP_COUNT * 4)
            words = (output_dir / manifest["artifacts"]["words"]["path"]).read_text(
                encoding="ascii").splitlines()
            self.assertEqual(len(words), GROUP_COUNT * WORDS_PER_GROUP)
            words_reconstructed = b"".join(bytes.fromhex(line)[::-1] for line in words)
            self.assertEqual(words_reconstructed, padded)
            self.assertEqual(manifest["artifacts"]["crc32"]["value_hex"],
                             f"{zlib.crc32(padded) & 0xFFFFFFFF:08x}")
            self.assertEqual(GROUP_BYTES, WORD_BYTES * WORDS_PER_GROUP)
            self.assertEqual(LANE_BYTES * 4, WORD_BYTES)

    def test_lut_segments_match_shared_integer_tables(self) -> None:
        from cnn.integer import tables

        payload, manifest = build_payload()
        expected = {
            "shared_lut.silu": np.asarray(tables()["silu"], dtype="<i2").tobytes(),
            "shared_lut.sigmoid": np.asarray(tables()["sigmoid"], dtype="<u2").tobytes(),
            "shared_lut.exp": np.asarray(tables()["exp"], dtype="<u2").tobytes(),
        }
        by_name = {segment["name"]: segment for segment in manifest["segments"]}
        for name, expected_bytes in expected.items():
            segment = by_name[name]
            actual = payload[segment["offset"]:segment["end_offset_exclusive"]]
            self.assertEqual(actual, expected_bytes)

    def test_saved_manifest_matches_returned_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output_dir = Path(temporary)
            expected = write_package(output_dir)
            saved = json.loads((output_dir / "manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(saved, expected)


if __name__ == "__main__":
    unittest.main()
