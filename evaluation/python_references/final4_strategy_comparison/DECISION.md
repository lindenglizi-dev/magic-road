# Final-four candidate strategy diagnostic (superseded)

This first receipt allowed fixed-quota strategies to scan every eligible small
component after NMS rejection. The hardware-bounded rerun in
`../final4_strategy_comparison_bounded/` caps every strategy's internal small
pool at four entries and is the current source of truth. The measured outputs
did not change.

This comparison uses three previously opened development windows: 900 frames in
total, with 1,018 pedestrian annotation rows and 900 vehicle annotation rows.
Every strategy uses the same post-cleanup components, `peak_difference` small
ranking, perspective expansion, and `IoU > 0.3` NMS. Video is decoded once per
window and all strategies see the same component stream.

The primary geometry diagnostic is annotation coverage at IoU 0.25. IoU 0.10
only indicates loose contact, while IoU 0.50 is retained as a stricter check.

| Strategy | Ped @0.25 | Small ped @0.25 | Vehicle @0.25 | Main top-4 retained | Empty slots |
|---|---:|---:|---:|---:|---:|
| `main3_small1` | 381/1018 (37.43%) | 87/321 (27.10%) | 603/900 (67.00%) | 2689/3030 (88.75%) | 11 |
| `main2_small2` | 422/1018 (41.45%) | 95/321 (29.60%) | 602/900 (66.89%) | 1800/3030 (59.41%) | 0 |
| `internal8_to4` | 422/1018 (41.45%) | 91/321 (28.35%) | 603/900 (67.00%) | 2334/3030 (77.03%) | 0 |

`main3_small1` is dominated on pedestrian coverage. `main2_small2` and
`internal8_to4` tie on aggregate pedestrian coverage at the primary IoU.
`main2_small2` has the best small-pedestrian coverage and a slightly higher
window macro average. `internal8_to4` retains more baseline main candidates and
is stronger at loose IoU 0.10, but requires an eight-entry unified arbitration
stage.

The minimal Python front-runner is therefore `main2_small2`; keep
`internal8_to4` as the dynamic challenger until candidate crops are reviewed on
another development scene. This is not a frozen hardware or model decision.
The rows are correlated frame annotations, VIRAT annotations are incomplete,
and candidate coverage is not object recall, classification recall, or a false
positive rate. No blind-reserve input was opened.
