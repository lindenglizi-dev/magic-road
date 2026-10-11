# VERIFY current — VIRAT pilot / Python-first contracts

Date: 2026-09-27  
Role: independent VERIFY  
Verdict: **pilot implementation verified with explicit acceptance blockers**. The 429-sample VIRAT train/validation set is technically traceable and leakage-free for diagnostic fitting. It is not acceptance evidence: the test split is absent, invalid/CCL-labelled candidates are absent, criteria are not frozen, the pilot person recall is 60%, and the VIRAT usage-agreement acceptance receipt is still pending.

## 1. Public-data and dataset integrity

- Raw VIRAT annotations use exactly eight integer fields and contain frame 0, so the converter correctly treats `current_frame` as zero-based.
- Twelve terminal rows with `frame_index == decoded_frame_count` are excluded as `frame_out_of_range`; no global `-1` shift or clamp-to-last-frame is used.
- Official types are mapped as `1 -> ped`, `2/3 -> vehicle`, `4/5 -> ignore`. The 21,840 undocumented type-0 rows in clip 000206 remain `ignore` with their original type retained; they are not negative, person, or vehicle samples.
- The catalog records source URLs, expected byte counts, video/annotation hashes and the official format README hash. License status remains `pilot_research_files_present_usage_acceptance_pending`; `user_acceptance_receipt` is `pending_user_confirmation`.
- `road_roi_dataset_virat/manifest.csv` has SHA-256 `ef4bd105844a11720ea07d504a6137132cce81ad62a77aba06f9d47b19ff666d` and 429 audited 32x32 ROIs:

| Split / scene | ped | vehicle | total |
|---|---:|---:|---:|
| train / 000201 | 32 | 73 | 105 |
| train / 000206 | 128 | 127 | 255 |
| val / 000200 | 21 | 12 | 33 |
| val / 000203 | 24 | 12 | 36 |
| total | 205 | 224 | 429 |

- Audit checks for scene, source-family, source-hash and ROI-pixel-hash leakage all pass. Every scene belongs to one split only. There are zero manifest rows in `test`; test clips 000205/000207 were used only for mapping QA and were not imported, fitted or scored.
- Sampling obeys the configured stride and per-track/per-scene-label caps. The train set remains source-imbalanced: scene 000206 contributes 255/360 train samples. Contact-sheet mapping passed, but distant people are often only 2–6 analysis pixels wide; this is a model-resolution limitation.

## 2. Diagnostic fit boundary and recomputation

`diagnostic_virat_fit.py` selects only VIRAT `annotated` rows in `train` and `val`, refuses an imported test row, uses fixed `C=1.0`, writes `*.diagnostic.*` artifacts, sets every freeze flag false, and creates no `freeze.json`.

An independent rerun reproduced the stored result exactly at the count/confusion/disagreement level:

- train 360; validation 69; prediction CSV contains only val scenes 000200 and 000203;
- float and fixed confusion matrix: `[[27,18],[0,24]]` for `[ped, vehicle]`;
- person recall 27/45 = 0.60; vehicle recall 24/24 = 1.00; accuracy 51/69 = 0.73913;
- float/fixed class disagreements: 0; diagnostic failures: 18;
- worst fixed score bound 2,478,629,956 is below the 40-bit signed accumulator limit 549,755,813,887.

This does not meet the provisional person-recall suggestion of 85%. Vehicle recall alone cannot establish acceptance. The manifest contains no `invalid`, so actual invalid false-accept rate is unmeasured. A pure two-class classifier has a 100% invalid-accept baseline by construction, and the unit fixture asserts that behavior, but it is not a measured VIRAT result.

Formal fit with `evaluation/criteria.pending.json` fails closed as intended because `frozen=false`; the command exits 1 before creating the output directory or freeze artifact.

## 3. Candidate-chain reference and 60-frame RTL replay

- Static configuration matches the deployed wrapper: threshold 20, `background_update_enable=1`, `freeze_foreground=1`; post-learning background update uses shift 4 with foreground freeze. `MIN_RUN_LENGTH=2` is present in `foreground_ccl_top -> rle_ccl_top -> run_detector`, and Python filters horizontal runs shorter than two.
- The reference remains an algorithm/coordinate model, not a cycle-accurate RLE/CCL model. It does not model `MAX_RUN=64`, `MAX_LABEL=32`, internal union timing or overflow/discard behavior.
- **The new 60-frame VIRAT result was covered.** The hashed parity report records 88 Python candidates and 88 RTL candidates, with all 88 ordered top-four bbox/area records exactly equal and zero mismatches. Both referenced input hashes match current files; all RTL source hashes in the measurement receipt also match.
- The replay observed 60 EOF, object-done and tracker-done pulses and zero `core_error` cycles. EOF-to-object latency is 279–564 cycles (mean 418.82); EOF-to-tracker is 286–577 cycles (mean 430.22).
- This replay is paced by row gaps/completion waits and is not a source-FPS continuous stream. It does not measure CDC, full capture-to-release bank ownership, drop rate, HDMI alignment or production throughput.
- CCL candidate export contains 88 unlabelled candidates. Annotation overlap is diagnostic only: VIRAT tracks are not exhaustive background truth, so unmatched candidates remain pending review and are not auto-labelled invalid.

## 4. Single-task protocol contract

The executable Python contract and 14 reference tests verify:

- EOF freezes the task payload; the source keeps transaction/frame/bank/generation/payload stable until a matching synchronized ack.
- Destination copies only after synchronized request arrival. `destination_ram_read_done` schedules ack; ack arrival releases only the source bank. `algorithm_done` is legal only after read-done and may occur later, so ack can intentionally precede HOG/SVM completion.
- A synchronized request remains visible while the executor is busy and is accepted when the executor becomes idle.
- Matching includes transaction ID, source frame ID, bank ID and bank generation. Duplicate/stale request and ack tests pass, including small-width frame/transaction wrap where an old ack cannot release a reused bank with a new generation.
- With an old task outstanding, a free second bank may capture. If the old ack has not arrived by the new EOF, the new frame is discarded rather than queued. If ack and EOF occur together, CDC ack release executes first and the new EOF publishes in the same model tick.
- Coordinated reset clears banks, mailboxes, queued CDC events, executor and display state.
- HDMI uses a pending snapshot; the latest complete result before VSYNC wins and increments overwrite accounting. VSYNC atomically freezes the active snapshot with source/display frame IDs and modulo delta.
- Four accelerated randomized trials (seeds 1, 7, 23, 101; 2,000 cycles each) pass.

This is a protocol specification, not RTL/CDC proof. In RTL, `ram_read_done` must be generated after capturing the last synchronous RAM response, not after merely issuing the last read address. Transaction/generation widths, maximum stale-message lifetime, reset release, handshake structure and the physical HDMI VSYNC edge/polarity still require architecture freeze and assertions.

## 5. Reproducible checks

| Command | Result |
|---|---|
| `python tools/audit_roi_dataset.py --dataset road_roi_dataset_virat` | PASS; 429 samples; leakage/hash/pixel checks pass; test absent |
| `python tests/test_python_references.py` | PASS; 14 tests |
| `python tests/test_road_evaluation.py` | PASS; 13 tests |
| `python tools/diagnostic_virat_fit.py --dataset road_roi_dataset_virat --output %TEMP%\\qiansai_verify_diagnostic` | PASS; reproduces stored counts/confusions; no test/freeze |
| `python tools/train_hog_svm.py --dataset road_roi_dataset_virat --output %TEMP%\\qiansai_verify_formal_unfrozen --phase fit --train-source annotated --criteria evaluation/criteria.pending.json` | EXPECTED REJECT; exits 1 with `formal fit requires criteria.frozen=true`; no output/freeze |
| `powershell -ExecutionPolicy Bypass -File tests/run_iverilog.ps1` | PASS; 10 existing RTL benches |

Readable-Verilog validation boundary: compile, testbench and local Icarus toolchain checks pass for the existing 10 benches. No functional RTL was added in this wave. AST/readability/comment/naming/profile gates were not rerun, so no strict ASIC/readability-gate claim is made.

## 6. Blocking items before acceptance or RTL implementation

1. Record explicit VIRAT usage-agreement acceptance; do not call the dataset license-complete or redistributable before then.
2. Freeze evaluation criteria before validation tuning and keep test scenes untouched until model/preprocessing/thresholds are frozen.
3. Add human-reviewed invalid and real CCL candidate labels; measure invalid false accept and candidate-input recall separately.
4. Investigate the 60% person recall and the loss of small distant pedestrians before declaring the 32x32/64-feature model viable.
5. Run real ROI feature/score Python-to-RTL parity; the current 88/88 result covers candidate bbox/area only.
6. Before protocol RTL, freeze identity widths and prove the stale-message alias bound, final-response-based RAM read-done, coordinated reset, same-cycle priority and HDMI VSYNC convention.

