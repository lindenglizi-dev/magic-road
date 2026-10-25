"""Small independent arithmetic oracle checks; no training or GPU access."""
import unittest
import json
import time
from pathlib import Path

import numpy as np

from cnn.integer import conv2d, encode_multiplier
from cnn.hw_validation.production.trained_integer import (
    conv_exact, nonconv, aligned_scales, IntegerModel, build_graph, parameter_shapes,
    FIELDS, write_package, load_package)


class TrainedIntegerTests(unittest.TestCase):
    def test_exact_convolution(self):
        rng = np.random.default_rng(42)
        for cin, cout, groups, kernel in [(3, 16, 1, 3), (5, 5, 5, 3), (12, 3, 1, 1), (6, 8, 2, 3)]:
            for stride in (1, 2):
                for padding in (0, kernel // 2):
                    image = rng.integers(-128, 128, (7, 9, cin), dtype=np.int16).astype(np.int8)
                    weight = rng.integers(-128, 128, (cout, cin // groups, kernel, kernel), dtype=np.int16).astype(np.int8)
                    bias = rng.integers(-100000, 100000, cout, dtype=np.int32)
                    np.testing.assert_array_equal(conv_exact(image, weight, bias, stride, padding, groups),
                                                  conv2d(image, weight, bias, stride, padding, groups))

    def test_extreme_and_overflow(self):
        image = np.full((1, 1, 2), -128, dtype=np.int8)
        weight = np.full((1, 2, 1, 1), -128, dtype=np.int8)
        with self.assertRaises(OverflowError):
            conv_exact(image, weight, np.array([2**31 - 1], dtype=np.int32))
        # Final sum is representable even though a partial could exceed INT32.
        image = np.array([[[127, 127]]], dtype=np.int8)
        weight = np.array([[[[127]], [[-127]]]], dtype=np.int8)
        np.testing.assert_array_equal(conv_exact(image, weight, np.array([2**31 - 1], dtype=np.int32)),
                                      [[[2**31 - 1]]])
        with self.assertRaises(ValueError):
            conv_exact(image.astype(np.float32), weight, np.zeros(1, dtype=np.int32))

    def test_nonconv_alignment(self):
        node = dict(op='residual_view', name='sum', output='sum', inputs=['a', 'b'])
        values = dict(a=np.array([[[-128, 127, 1]]], dtype=np.int8),
                      b=np.array([[[-1, 1, -1]]], dtype=np.int8))
        np.testing.assert_array_equal(nonconv(node, values)['sum'], [[[-128, 127, 0]]])
        graph = {'nodes': [node]}
        ranges = {name: {'max_abs': value} for name, value in [('a', 1), ('b', 2), ('sum', 3)]}
        scales, _ = aligned_scales(graph, ranges)
        self.assertEqual(set(scales.values()), {3 / 127})

    def test_package_schema_and_corruption(self):
        graph = build_graph()
        parameters, scales = {}, {'input': 1.0}
        for node in graph['nodes']:
            names = [v['output'] for v in node['outputs']] if node['op'] == 'split_view' else [node['output']]
            for name in names:
                scales[name] = 1 / 256 if node.get('dtype') == 'int16_q7_8' else 1.0
            if node['op'] == 'conv':
                parameters[node['name']] = {field: np.zeros(parameter_shapes(node)[field], dtype=dtype)
                                          for field, dtype in FIELDS if field in parameter_shapes(node)}
                if node['dtype'] == 'int8':
                    multiplier, shift = encode_multiplier(1 / (256 * scales[node['name']]))
                    parameters[node['name']]['post_multiplier'][0] = multiplier
                    parameters[node['name']]['post_shift'][0] = shift
        IntegerModel(graph, parameters, scales)
        with self.assertRaises(ValueError):
            IntegerModel(graph, parameters, dict(scales, **{'residual.00': 2.0}))
        with self.assertRaises(ValueError):
            IntegerModel(graph, parameters, dict(scales, input=0.5))
        path = (Path(__file__).resolve().parents[3] / 'cnn/reports/integer_unit_tests_20261013'
                / str(time.time_ns()) / 'package')
        write_package(path, graph, parameters, scales, {'purpose': 'unit_test_only'})
        load_package(path)
        manifest_path = path / 'manifest.json'
        original = manifest_path.read_text(encoding='utf-8')
        for field, value in [('dtype', '<i2'), ('shape', [113100]), ('name', 'fake.weights')]:
            modified = json.loads(original)
            modified['segments'][0][field] = value
            manifest_path.write_text(json.dumps(modified), encoding='utf-8')
            with self.assertRaises(ValueError):
                load_package(path)
        for key in ('layout', 'lane_files', 'scales', 'layers'):
            modified = json.loads(original)
            if key == 'layout':
                modified[key]['word_bytes'] = 16
            elif key == 'lane_files':
                modified[key][0]['sha256'] = '0' * 64
            elif key == 'layers':
                modified[key][0]['fields']['bias'] += 1
            else:
                modified[key]['stem.conv'] *= 2
            manifest_path.write_text(json.dumps(modified), encoding='utf-8')
            with self.assertRaises(ValueError):
                load_package(path)
        manifest_path.write_text(original, encoding='utf-8')
        lane = path / 'group_00_lane_0.dath'
        lane.write_text('ff' * 5 + '\n', encoding='ascii')
        with self.assertRaises(ValueError):
            load_package(path)

    def test_pool_padding_and_views(self):
        values = {'x': np.array([[[-12, -4]]], dtype=np.int8)}
        node = dict(op='maxpool', output='pool', inputs=['x'])
        np.testing.assert_array_equal(nonconv(node, values)['pool'], values['x'])
        node = dict(op='nearest_view', output='up', inputs=['x'], scale=[2, 2])
        self.assertEqual(nonconv(node, values)['up'].shape, (2, 2, 2))
        node = dict(op='split_view', inputs=['x'], outputs=[{'output': 'half', 'channel_offset': 1, 'channels': 1}])
        np.testing.assert_array_equal(nonconv(node, values)['half'], [[[-4]]])


if __name__ == '__main__':
    unittest.main()
