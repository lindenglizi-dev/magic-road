# Hardware-bounded final-four candidate comparison

All three strategies use at most four main candidates and four small candidates
internally, then emit no more than four boxes. This removes the unbounded refill
advantage from the first comparison. The three existing development windows
cover 900 frames, 1,018 pedestrian annotation rows and 900 vehicle annotation
rows. Video was decoded once per window and every strategy saw the same component
stream.

| Strategy | Ped @0.25 | Small ped @0.25 | Vehicle @0.25 | Main top-4 retained | Empty slots |
|---|---:|---:|---:|---:|---:|
| `main3_small1` | 381/1018 (37.43%) | 87/321 (27.10%) | 603/900 (67.00%) | 2689/3030 (88.75%) | 11 |
| `main2_small2` | 422/1018 (41.45%) | 95/321 (29.60%) | 602/900 (66.89%) | 1800/3030 (59.41%) | 0 |
| `internal8_to4` | 422/1018 (41.45%) | 91/321 (28.35%) | 603/900 (67.00%) | 2334/3030 (77.03%) | 0 |

The bounded rerun produced the same selected boxes and metrics as the first run,
so no strategy depended on scanning beyond the peak-ranked four small candidates
in these windows.

`main3_small1` is weaker on pedestrian geometry. `main2_small2` and
`internal8_to4` tie on aggregate pedestrian coverage at the primary IoU 0.25.
The fixed 2+2 quota covers four more very small pedestrian rows, but loses five
baseline-covered pedestrian rows and one vehicle row. Unified 8-to-4 preserves
all baseline-covered rows, retains 77.03% rather than 59.41% of the original main
top-4, and performs better at loose IoU 0.10.

The current Python recommendation is `internal8_to4` when baseline preservation
matters. `main2_small2` remains the simpler fixed-quota fallback. Neither is
frozen for RTL: perspective calibration needs another development scene, and all
new crops must be reviewed before classification metrics are reused.

These are correlated annotation-frame observations. VIRAT annotations are
incomplete, and candidate coverage is not object recall, classification recall,
or a false-positive rate. No blind-reserve input was opened.
