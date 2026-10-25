"""One real CPU batch forward/backward; no optimizer update or candidate save."""
import faulthandler
import gc
import json
import os
import time

faulthandler.enable()
print(json.dumps(dict(event='real_probe_start', pid=os.getpid())), flush=True)
import torch
from cnn.hw_validation.production import train_qat_frozen_stem_continue as runner
from cnn.loss import YOLOXLoss

if torch.cuda.is_available():
    raise RuntimeError('CUDA must be hidden')
torch.set_num_threads(2)
torch.use_deterministic_algorithms(True)
started = time.perf_counter()
data, window, folded, identity, protocol, ancestry, parent = runner.prepare()
print(json.dumps(dict(event='parent_loaded', seconds=time.perf_counter()-started)), flush=True)
model, optimizer = runner.frozen.make_model(folded, torch.device('cpu'))
runner.load_state(model, optimizer, parent)
window.set_epoch(0, mosaic=False)
samples = [window[i] for i in range(2)]
images = torch.stack([s[0] for s in samples])
targets = [s[1] for s in samples]
print(json.dumps(dict(event='images_ready')), flush=True)
for iteration in range(6):
    optimizer.zero_grad(set_to_none=True)
    heads = model(images)
    print(json.dumps(dict(event='forward_done', iteration=iteration+1)), flush=True)
    losses = YOLOXLoss()(heads, targets)
    losses['loss'].backward()
    assert all(p.grad is not None and torch.isfinite(p.grad).all() for p in model.parameters())
    print(json.dumps(dict(event='backward_done', iteration=iteration+1,
                         loss=float(losses['loss'].detach()))), flush=True)
    del heads, losses
    gc.collect()
print(json.dumps(dict(event='real_probe_passed', finite_gradients=132,
    optimizer_updates=0, iterations=6,
    seconds=time.perf_counter()-started)), flush=True)
