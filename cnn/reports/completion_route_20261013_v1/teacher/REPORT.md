# YOLOX-S teacher on the exact development-17 GT

Status: CPU evaluation completed once with 2 threads. This is development evidence, not formal acceptance or FPGA throughput.

## Overall comparison (score threshold 0.5, IoU 0.5)

| model | class | P@.5 | R@.5 | AP50 | AP50:95 |
|---|---|---:|---:|---:|---:|
| official YOLOX-S teacher | person | 93.10% | 88.04% | 88.66% | 46.93% |
| official YOLOX-S teacher | vehicle | 94.52% | 79.31% | 78.96% | 45.61% |
| replay-G10 | person | 74.42% | 34.78% | 47.50% | 15.09% |
| replay-G10 | vehicle | 68.33% | 47.13% | 50.82% | 19.37% |
| E7 | person | 80.77% | 22.83% | 39.00% | 9.98% |
| E7 | vehicle | 78.00% | 44.83% | 49.57% | 18.51% |

Teacher minus replay-G10 is +18.68/+53.26/+41.16/+31.84 percentage points for person P/R/AP50/AP50:95, and +26.19/+32.18/+28.14/+26.24 points for vehicle.

## Real camera groups

| camera | images; GT P/V | teacher person AP50 / AP50:95 | replay person | teacher vehicle AP50 / AP50:95 | replay vehicle |
|---|---:|---:|---:|---:|---:|
| PETS09-S2L1-view1 | 13; 84/26 | 89.96 / 48.94 | 48.55 / 15.91 | 100.00 / 59.36 | 22.66 / 7.84 |
| virat-010107-camera-b | 2; 6/54 | 56.44 / 17.99 | 50.50 / 9.54 | 65.95 / 36.07 | 53.62 / 20.90 |
| virat-parking-lot-camera-a | 2; 2/7 | 100.00 / 32.62 | 50.50 / 20.20 | 98.14 / 86.88 | 100.00 / 50.13 |

The teacher advantage is directionally consistent across cameras. The only AP50 reversal is vehicle on the two-frame parking-lot group (98.14 vs replay 100.00) with seven GT vehicles; teacher AP50:95 is still +36.75 points there. Treat the two-frame groups as descriptive, not stable estimates.

## Input and policy boundary

- Same 17 original image files, exact same human GT/ignore rows, and same Top-128/max-32/NMS contract were verified across all three reports.
- Inputs are not tensor-identical: teacher uses original BGR, center-letterbox 1280x720, area resize to 1024x576, FP32 0..255; students use RGB, 512x288, FP32 minus 128. This is not a resolution-matched ablation.
- Teacher predictions and the dense train cache contain no GT and must not replace human labels.
- A single equal-budget 10-update distillation control is justified by the large teacher margin. Do not infer that it will transfer; stop after that controlled comparison rather than scan weights or epochs.

## Traceability

- Teacher weights SHA256: `f55ded7181e1b0c13285c56e7790b8f0e8f8db590fe4edb37f0b7f345c913a30`
- YOLOX source tree SHA256: `2ff03bf022efb8f37ed91d062be163ee51a59d0a11cf1a64e1dad8ae410268ef`
- Evaluation dataset SHA256: `6af48b5ec8da6550a5d0af31db8b8f58d1fc8c9960df0eda9a66ad7c94f5f5e1`
- Evaluated image-content SHA256: `373af83998b9cf08f9ba3715416415486c82ec050df8cbab2aefb5835876e3d0`
- Teacher evaluation SHA256: `82a55f18db78b76cc37e8dca487776b1fab680df4dc5fce8ccf7b54939ed2788`
- Evaluation source closure and input report hashes are in `comparison17.json`; stdout/stderr and the initial wrong-interpreter failure are retained.
- Train-86 cache SHA256: `37c2edfcf416167c3c230a079aa7c4ff33e067fe0a37bcff15ee4ea318595927`; its receipt verifies 86/86 keys, shapes, dtype, finiteness and binding metadata, but does not claim numerical re-inference comparison.
