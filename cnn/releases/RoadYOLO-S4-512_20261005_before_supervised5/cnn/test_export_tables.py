"""Check serialized LUT words, exhaustive vectors, hashes and no-overwrite behavior."""

import hashlib
import json
from pathlib import Path
import tempfile
import unittest

import numpy as np

from .export_tables import export_tables
from .integer import exponent, sigmoid, silu, tables


class ExportTablesTest(unittest.TestCase):
    def test_export_and_exhaustive_roundtrip(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / 'assets'
            manifest = export_tables(output)
            expected = dict(tables())
            domain = np.arange(-32768, 32768)
            expected.update(silu_golden=silu(domain), sigmoid_golden=sigmoid(domain),
                            exp_golden=exponent(np.arange(-1024, 897)))
            for record in manifest['files']:
                binary = (output / record['bin']['path']).read_bytes()
                values = np.frombuffer(binary, dtype=record['dtype'])
                np.testing.assert_array_equal(values, expected[record['name']])
                words = [int(line, 16) for line in
                         (output / record['hex']['path']).read_text().splitlines()]
                np.testing.assert_array_equal(words, values.astype(np.uint16))
                for extension in ('bin', 'hex'):
                    row = record[extension]
                    data = (output / row['path']).read_bytes()
                    self.assertEqual(len(data), row['bytes'])
                    self.assertEqual(hashlib.sha256(data).hexdigest(), row['sha256'])
            self.assertEqual(json.loads((output / 'manifest.json').read_text()), manifest)
            with self.assertRaises(FileExistsError):
                export_tables(output)
            self.assertEqual(json.loads((output / 'manifest.json').read_text()), manifest)


if __name__ == '__main__':
    unittest.main()
