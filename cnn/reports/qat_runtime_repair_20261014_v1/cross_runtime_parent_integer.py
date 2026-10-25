"""Compare the old 2.4.6 parent integer trace to the saved 2.3.5 control."""
import json
from pathlib import Path
import numpy as np
import torch
from cnn.hw_validation.production import train_qat as base
from cnn.hw_validation.production import train_qat_frozen_stem as frozen
from cnn.hw_validation.production.probe_qat_numpy235 import array_hash, parameter_hash
from cnn.hw_validation.production.run_trained_integer import centered, save
from cnn.hw_validation.production.trained_integer import load_package
from cnn.train import FullFrameDataset, load_dataset_snapshot, sha256

if np.__version__ != '2.4.6' or torch.cuda.is_available():
    raise RuntimeError('original NumPy CPU-only reference required')
torch.set_num_threads(2)
folder = base.PROJECT / 'cnn/reports/qat_runtime_repair_20261014_v1'
control = json.loads((folder / 'numpy235_control/preflight.json').read_text())
_, snapshot = load_dataset_snapshot(base.TRAIN)
dataset = FullFrameDataset(snapshot.rows, 'train', mosaic=False)
sample = dataset[0][0]
integer, manifest = load_package(frozen.OUT / 'package')
_, _, values = integer.forward(centered(sample), capture=True)
actual = dict(all_integer_capture_sha256=array_hash(values),
              parameter_codes_sha256=parameter_hash(integer.parameters))
assert all(value == control['trace'][field] for field, value in actual.items())
save(folder / 'cross_runtime_parent_integer.json', dict(passed=True,
    reference_numpy_version=np.__version__, reference_numpy_path=np.__file__,
    comparison_numpy_version='2.3.5', captures=len(values),
    input_image=dataset.rows[0]['image'], parent_payload_sha256=manifest['payload_sha256'],
    trace_hashes=actual, control_preflight_sha256=sha256(folder / 'numpy235_control/preflight.json'),
    script_sha256=sha256(Path(__file__)), GPU_used=False, optimizer_updates=0))
print(json.dumps(dict(event='cross_runtime_248_integer_tensors_exact', **actual)), flush=True)
