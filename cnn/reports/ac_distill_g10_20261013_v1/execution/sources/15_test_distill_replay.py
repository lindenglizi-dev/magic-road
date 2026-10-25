"""Replay teacher-key coverage and exact CPU resume through the actual trainer."""
from contextlib import redirect_stdout
import io
from pathlib import Path
import tempfile
from unittest.mock import patch

import torch

from . import train
from .test_replay_sampling import Pool, args, schedule
from .test_finetune_schedule import _TinyModel, _TinyLoss, _same, _fails


class KeyedPool(Pool):
    def __init__(self, split):
        super().__init__(split)
        for index, row in enumerate(self.rows):
            row['teacher_key'] = str(index)


class TinyTeacher:
    def __init__(self, *_args):
        pass

    def require_keys(self, keys):
        assert len(keys) == 44 and set(keys) == {str(i) for i in range(44)}

    def batch(self, keys, device):
        return torch.tensor([float(key) / 50 for key in keys], device=device)


def main():
    torch.set_num_threads(1)
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        manifest = root/'dataset.json'
        manifest.write_text('{}', encoding='utf-8')
        teacher = root/'teacher.pt'
        teacher.write_bytes(b'CPU integration stub, not a real teacher cache')
        with (patch.object(train, 'load_dataset_manifest', return_value=(
                    dict(replay_sampling=schedule()), [dict(image='tiny', image_sha256='0'*64)])),
              patch.object(train, 'make_frame_dataset',
                           side_effect=lambda _rows, split, *_a, **_kw: KeyedPool(split)),
              patch.object(train, 'RoadYOLOS4', _TinyModel),
              patch.object(train, 'YOLOXLoss', _TinyLoss),
              patch.object(train, 'TeacherCache', TinyTeacher),
              patch.object(train, 'dense_distillation_loss',
                           side_effect=lambda output, cached, _targets:
                           (output.mean((1, 2, 3)) - cached).square().mean()),
              patch.object(torch.cuda, 'is_available', return_value=False),
              redirect_stdout(io.StringIO())):
            continuous = args(manifest, root/'continuous')
            continuous.phase, continuous.teacher_cache = 'distill', teacher
            assert train.train(continuous) == 0
            segmented = args(manifest, root/'segmented', 1)
            segmented.phase, segmented.teacher_cache = 'distill', teacher
            assert train.train(segmented) == 0
            segmented.resume = segmented.output/'last_resume.pt'
            segmented.stop_after_epoch = 0
            segmented.distill_weight = 0.5
            _fails(lambda: train.train(segmented))
            segmented.distill_weight = continuous.distill_weight
            assert train.train(segmented) == 0
        left, right = [torch.load(path/'last.pt', weights_only=False, map_location='cpu')
                       for path in (continuous.output, segmented.output)]
        for key in ('model', 'optimizer', 'scaler', 'rng_state'):
            _same(left[key], right[key])
        assert left['trained_steps'] == right['trained_steps'] == 2
        assert left['last_optimizer_effective_batch'] == 22
        assert left['training_protocol']['phase'] == 'distill'
        assert left['training_protocol']['teacher_cache_sha256'] == train.sha256(teacher)
    print('PASS replay distill: full-pool teacher keys, batch22, changed-contract rejection, exact CPU resume')


if __name__ == '__main__':
    main()
