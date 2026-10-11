# Commands and exits

Commands were run from this `candidate` directory unless another working directory is shown. The installed readable-Verilog workflow and project-local Python were used. Dedicated readable-Python/readable-script skills were unavailable; no new Python or shell implementation was added here.

## Spec and WaveDrom

```powershell
$env:PYTHONPATH='<production>/checker_overlay;C:/Users/lenovo/.codex/skills/readable-verilog-generator'
E:/project/qiansai/.tools/road_yolo_venv/Scripts/python.exe -m scripts.python.workflow.cli write-spec --spec road_mac_probe.contract.json --out-dir . --source road_mac_probe.v --language zh
```

Exit `0`. Generated `spec/mac/road_mac_probe_spec.md` and the JSON5/SVG WaveDrom pair. The waveform includes the signed33 bit-32 excursion, recovery, and terminal INT32 check.

## Strict gates

```powershell
E:/project/qiansai/.tools/road_yolo_venv/Scripts/python.exe -m scripts.python.validation.generated_deliverable_gate ../../v7_minimal_chain_20261006/inputs/road_mac_probe.v --spec <mac>/road_mac_probe.contract.json --comment-language zh --json strict_baseline.json --markdown strict_baseline.md
E:/project/qiansai/.tools/road_yolo_venv/Scripts/python.exe -m scripts.python.validation.generated_deliverable_gate road_mac_probe.v --spec road_mac_probe.contract.json --comment-language zh --json strict_candidate_pass.json --markdown strict_candidate_pass.md
```

Both final commands exited `0`, with `delivery_ready=true`, zero errors, and zero strict warnings. For both objects, compile, AST, readability, comment, naming, and profile passed; testbench and optional toolchain checks were not requested.

Retained repair evidence:

- `strict_candidate.json`: first candidate, exit `1`, three VG122 findings because two already-expanded 34-bit operands implied a generic 35-bit result.
- `failure_snapshots/vg122_operand34_reconstructed.v`: explicitly reconstructed source matching that report's SHA256 exactly; it is evidence only, not a candidate.
- `strict_candidate_final.json`: next run, exit `1`, `errors=4`; it retains three explicit VG060 comment-column issue records plus the corresponding formatter-AST error summary.
- `strict_candidate_pass.json`: final run after the same-cycle signed33-plus-signed33 adder and local comment alignment, exit `0`.

No non-strict, warn-only, threshold, rule, filename, or module exemption was used.

## Frozen base and tail regressions

```powershell
E:/project/qiansai/.tools/iverilog/bin/iverilog.exe -g2001 -Wall -s tb_road_mac_probe -o final_base_tail.vvp road_mac_probe.v ../../v7_minimal_chain_20261006/inputs/tb_road_mac_probe.v
E:/project/qiansai/.tools/iverilog/bin/vvp.exe final_base_tail.vvp +VECTORS=../../v7_minimal_chain_20261006/mac_16_channels.txt
E:/project/qiansai/.tools/iverilog/bin/vvp.exe final_base_tail.vvp +VECTORS=../../v7_minimal_chain_20261006/mac_13_channels.txt
```

Compile exit `0`; both simulations exited `0` and printed `PASS cases=8 errors=0 reset=1`.

## Full frozen MAC stream regression

Run from `cnn/hw_validation/mac` with this candidate RTL replacing only the same-named DUT source:

```powershell
E:/project/qiansai/.tools/iverilog/bin/iverilog.exe -g2001 -Wall -s tb_road_mac_stream_probe -o <candidate>/signed33_stream_final.vvp <candidate>/road_mac_probe.v road_mac_stream_probe.v tb_road_mac_stream_probe.v
E:/project/qiansai/.tools/iverilog/bin/vvp.exe <candidate>/signed33_stream_final.vvp +VECTORS=mac_vectors.txt
```

Compile exit `0`; simulation exit `0`:

```text
VERILOG-GEN-RESULT PASS cases=1031 errors=0 reset=1 dynamic_words=12 io=140
```

The frozen 1031 vectors contained no expectation that conflicted with terminal-only overflow semantics; they therefore required no edits or filtering.

## Signed33 directed suite

```powershell
E:/project/qiansai/.tools/iverilog/bin/iverilog.exe -g2001 -Wall -s tb_road_mac_signed_accumulator -o signed33_directed_final.vvp road_mac_probe.v ../verification/tb_road_mac_signed_accumulator.v
E:/project/qiansai/.tools/iverilog/bin/vvp.exe signed33_directed_final.vvp +VECTORS=../verification/signed33_vectors.txt +TRACE=signed33_timing_trace_final.csv
```

Compile exit `0`; simulation exit `0`:

```text
VERILOG-GEN-RESULT PASS vectors=84 errors=0 busy_hold=593 resets=10 ready_high=1 latency=9 ii_nonlast=11 ii_stall3=16
```

The 12 cases cover positive and negative temporary INT32 excursions and recovery on alpha/beta/gamma, terminal positive/negative overflow per channel, atomic all-zero fault output, bias extremes, 24 beats / 192 terms, tail masks, backpressure, ready-high terminal acceptance, and ten reset cancellation points.

The frozen legacy RTL was separately compiled with the same testbench in `LEGACY_NEGATIVE` mode. It exited `0` and printed:

```text
VERILOG-GEN-NEGATIVE PASS legacy_early_faults=2 errors=0
```

This is a real counterexample to the old per-group policy, not a checker exemption.

## Official ModelSim confirmation

The independent verifier recompiled the final candidate SHA256 `F8BF6C...478E8` with ModelSim SE-64 2020.4 and ran the same frozen 84-beat suite. `vlog` and `vsim` both completed with zero errors and zero warnings. The retained raw logs are `../verification/modelsim_candidate_compile.log` and `../verification/modelsim_candidate.log`.

```text
VERILOG-GEN-RESULT PASS vectors=84 errors=0 busy_hold=593 resets=10 ready_high=1 latency=9 ii_nonlast=11 ii_stall3=16
```

The frozen legacy source was independently compiled and executed in negative mode. `../verification/modelsim_legacy_negative.log` records zero tool errors/warnings and `PASS legacy_early_faults=2 errors=0`.
