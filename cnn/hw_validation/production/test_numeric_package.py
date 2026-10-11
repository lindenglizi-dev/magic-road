import hashlib
from pathlib import Path
import tempfile
import unittest

import numeric_package


class NumericPackageTest(unittest.TestCase):
    def test_layout_roles_hashes_and_no_implicit_model_export(self):
        payload, physical, manifest = numeric_package.build_package()
        self.assertEqual(len(payload), 140522)
        self.assertEqual(len(physical), 14 * 512 * 20)
        self.assertEqual(physical[140522:], bytes(2838))
        self.assertIn("NOT_TRAINED", manifest["status"])
        self.assertEqual(hashlib.sha256(payload).hexdigest(), manifest["payload_sha256"])
        cursor = 0
        for segment in manifest["segments"]:
            self.assertEqual(segment["offset"], cursor)
            data = payload[cursor:cursor + segment["length"]]
            self.assertEqual(hashlib.sha256(data).hexdigest(), segment["sha256"])
            cursor += len(data)
        self.assertEqual(cursor, len(payload))
        self.assertEqual(sum("post_shift" in layer["fields"] for layer in manifest["layers"]), 61)
        self.assertEqual(sum(layer["output_dtype"] == "int16_q7_8" for layer in manifest["layers"]), 6)
        self.assertEqual(numeric_package.build_package()[0], payload)

    def test_all_fifty_six_physical_lanes_roundtrip(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest = numeric_package.write_package(root)
            for lane in manifest["lane_files"]:
                self.assertEqual(hashlib.sha256((root / lane["name"]).read_bytes()).hexdigest(),
                                 lane["sha256"])
            restored = bytearray()
            for group in range(14):
                lanes = [(root / f"group_{group:02d}_lane_{lane}.dath").read_text().splitlines()
                         for lane in range(4)]
                self.assertTrue(all(len(lane) == 512 for lane in lanes))
                for word in range(512):
                    for lane in lanes:
                        restored.extend(bytes.fromhex(lane[word])[::-1])
            self.assertEqual(bytes(restored), (root / "numeric_test_padded.bin").read_bytes())
            self.assertEqual(hashlib.sha256(restored).hexdigest(), manifest["physical_sha256"])


if __name__ == "__main__":
    unittest.main()
