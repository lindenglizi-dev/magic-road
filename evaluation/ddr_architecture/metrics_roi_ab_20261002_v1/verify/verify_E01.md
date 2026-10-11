# Independent E01 verification

Status: **PASS**

No video was decoded. The verifier used the saved 32 frame bindings, `roi_pixels.npz`, frozen public annotations/candidates/capacity files, and current receipt-bound model files. No blind, test, or reserved path was accessed.

## Recomputed evidence

- Predictions: 236 = 118 A + 118 B; B reuse/new = 14/104.
- Truth: 57 target observations = 46 ped + 11 vehicle across 32 frames and 4 tracks.
- Capacity failures: L32 833/960 and L128 0/960; reviewed frames L32 28/32 and L128 0/32.
- Independent exhaustive matching reproduced 171 target/view rows exactly: True.
- All 236 NPZ ROIs and HOG324 float/Q scores reproduced exactly, including all 104 newly inferred B rows: True.
- Historical remap C->A and D->B reproduced for all 14 retained matches: True.
- Receipt bindings: 52 inputs, 6 sources/runtime copies, 138 protected files, and 15 original artifacts all current: True.

## Paired tables

- `pre_capacity`: ped {'n00': 39, 'n01': 0, 'n10': 2, 'n11': 5, 'denominator': 46}; vehicle {'n00': 9, 'n01': 0, 'n10': 0, 'n11': 2, 'denominator': 11}
- `proxy_L32_R64`: ped {'n00': 45, 'n01': 0, 'n10': 0, 'n11': 1, 'denominator': 46}; vehicle {'n00': 11, 'n01': 0, 'n10': 0, 'n11': 0, 'denominator': 11}
- `proxy_L128_R64`: ped {'n00': 39, 'n01': 0, 'n10': 2, 'n11': 5, 'denominator': 46}; vehicle {'n00': 9, 'n01': 0, 'n10': 0, 'n11': 2, 'denominator': 11}

## Lost correct targets

- frame 360 `p01` / `local_baseline_main4:f000360:slot2:cc46`: A q=-94508688 (-1.28195514745, ped), B q=53862380 (0.730611722121, vehicle).
- frame 690 `p02` / `local_baseline_main4:f000690:slot2:cc41`: A q=-44521448 (-0.603907435851, ped), B q=95311753 (1.29284825509, vehicle).

## Boundary

Unknown candidates remain unknown; they are not counted as invalid, so precision, F1, and invalid FAR remain N/A. The supplemental `E01_RESULTS.md` and `loss_cases/` were added after the original receipt and are reported separately from its 15-artifact protected set.

Machine-readable details: `verify_E01.json`. Failures: none.
