"""Build one CPU-only dense teacher cache for the replay-G10 train split."""
from pathlib import Path

import torch

from cnn.teacher import build_cache

ROOT = Path(__file__).resolve().parents[4]

torch.set_num_threads(2)
result = build_cache(
    ROOT / "cnn/reports/ac_optimization_20261013_v1/trial/dataset.json",
    Path(__file__).with_name("teacher_train86.pt"),
    ROOT / "cnn/teacher_assets/source/YOLOX-0.3.0",
    ROOT / "cnn/teacher_assets/yolox_s.pth",
    "train", 86, torch.device("cpu"),
)
print(result)
