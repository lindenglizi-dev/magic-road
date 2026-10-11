"""Narrow negative and rounding checks for teacher development evaluation."""
from pathlib import Path

import numpy as np
import torch

from .dataset import _refuse_blind
from .evaluate_teacher import quantize_heads
from .evaluate import load_validation_subset


def main():
    raw = torch.zeros(1, 7, 1, 1)
    raw[0, :, 0, 0] = torch.tensor([.5 / 256, 1.5 / 256, -.5 / 256,
                                    -1.5 / 256, 200., -200., 0.])
    heads = quantize_heads([raw])
    np.testing.assert_array_equal(heads[0][0, 0], [0, 2, 0, -2, 32767, -32768, 0])
    assert heads[0].dtype == np.int16
    try:
        _refuse_blind(Path("new_blind_reserve/dataset.json"))
    except ValueError:
        pass
    else:
        raise AssertionError("teacher evaluator accepted blind reserve")
    try:
        load_validation_subset(Path("cnn/data/virat_diagnostic/dataset.json"), None, 2)
    except ValueError:
        pass
    else:
        raise AssertionError("teacher evaluator accepted incomplete VIRAT GT")
    print("teacher evaluation rounding and forbidden/incomplete data checks passed")


if __name__ == "__main__":
    main()
