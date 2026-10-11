# Shared SiLU PH1P prototype receipt

## Frozen decision

- `integration_release=false`
- Current-source Python and Icarus functional evidence passed.
- Final strict gate: `delivery_ready=false`, `errors=174`, `strict_warnings=0`.
- No TD, board test, Flash, training, or production integration was run.

## Current implementation

- Signed INT16 Q7.8. Raw `<= -2048` returns zero; raw `>= 2048` returns identity; middle values use signed RNE divide-by-four plus 512.
- Addresses 0 through 1023 use the runtime table; address 1024 returns hardwired 2047.
- One `PH1P_LOGIC_ERAM` is instantiated in `SP` mode with a 1024-by-20 A port. The 16-bit table word is sign-extended; the B port is disabled.
- No initialization file and no table reset. Reset revokes loaded metadata and requires a complete reload.
- Unexpected accepted addresses raise sticky fault and are blocked from the physical write enable. Address zero restarts.
- Global backpressure freezes the sample pipeline. Measured latency is 5 cycles; no-stall II is 1.

## Functional evidence

Python:

```powershell
E:\project\qiansai\.tools\road_yolo_venv\Scripts\python.exe -B -X utf8 cnn\hw_validation\production\silu\verify_vectors.py
```

PASS: 1024 table words and all 65536 signed inputs. Raw log: `reports/python_vectors_final.log`.

Icarus, compiled from the current source:

```powershell
E:\project\qiansai\.tools\iverilog\bin\iverilog.exe -g2005 -Wall -s tb_silu_shared_unit -o cnn\hw_validation\production\silu\generated\tb_silu_source_restored.vvp cnn\hw_validation\production\silu\tb_ph1p_logic_eram_runtime_model.v cnn\hw_validation\production\silu\silu_shared_unit.v cnn\hw_validation\production\silu\tb_silu_shared_unit.v
E:\project\qiansai\.tools\iverilog\bin\vvp.exe cnn\hw_validation\production\silu\generated\tb_silu_source_restored.vvp
```

PASS: `TB_PASS inputs=65536 latency=5 ii=1 table_words=1024`. Raw log: `reports/iverilog_run_final.log`.

Directed checks cover illegal first address/no physical write, sticky fault, address-zero recovery, complete activation, three-cycle output hold, reload waiting for pending results, reset cancellation, and complete post-reset reload. The PH1P model has the exact public port list and synchronous runtime read/write behavior; it is not mapping or silicon evidence.

## Canonical spec

`scripts.python.workflow.cli write-spec` regenerated `spec/spec/silu_shared_unit_spec.md` and its WaveDrom JSON5/SVG files from the current RTL and `cnn/hw_validation/settings.json`. The spec records PH1P 1024-by-20 runtime loading, no table reset, latency 5, and II=1.

## Final strict gate

Reports: `reports/gate_attempt_6.json` and `reports/gate_attempt_6.md`. The run supplied `cnn/hw_validation/interfaces/ph1p_eram_interface_complete.v`.

| State | Result | Errors |
| --- | --- | ---: |
| compile | passed | 0 |
| ast | failed | 1 |
| readability | failed | 160 |
| comment | failed | 13 |
| naming | failed | 6 |
| profile | passed | 0 |
| testbench | not_requested | 0 |
| toolchain | not_requested | 0 |

Rule counts: VG138 38; VG062 31; VG146 20; VG060 17; `COMMENT_COMMENT_PLACEMENT` 13; VG040 12; VG145 9; VG125 6; VG147 5; VG085/VG122 4 each; VG066 3; VG061/VG132 2 each; VG013/VG063/VG065/VG084/VG097/VG137/VG153 1 each.

Real module-owned operation blockers include `cnt_pending$enable` 7, `cnt_table_expected$enable` 14, `flag_input_valid$D` 6, `output_data_o$enable` 7, `table_fault_o$enable` 14, `table_loaded_o$enable` 14, `table_ready_o` 7, and `input_ready_o` 5. These are not waived by simulation.

Separate vendor/tool boundary: the high-level gate does not have governed PH1P implementation semantics. It leaves primitive implementation, RAM read-data driver, clock associations, and dependent cones inconclusive (VG097/VG132/VG137/VG146/VG147/VG153). The supplied interface source proves port visibility only, not mapping, timing, or hardware behavior.

The failed registered-loader experiment was reverted; its minimal failure record is `reports/control_repair_reverted.md`. The current source was then rebuilt and rerun through all 65536 inputs.

## Frozen hashes

| Artifact | SHA-256 |
| --- | --- |
| `silu_shared_unit.v` | `ee9beb80decb4f276b9ff81214c22f044a71ac1ffc8c72beb1378e6ddb07a7ed` |
| `tb_silu_shared_unit.v` | `56d30f664c6412f0585a2dcb7017035678bc30521ae4b7e86b4a1b2aa9e60800` |
| `tb_ph1p_logic_eram_runtime_model.v` | `0e42914a2258e8fa9ed1088ede13d6cdd636fe9b8e76bc58155946ae179abd31` |
| `verify_vectors.py` | `4bb78f6b467afa2f3aaccebec369775adea34f453acb8acafc3fd54e3ef4f788` |
| `requirements.md` | `857be119d804e39cf8161ea6f509d6e120ee18038292581aba6914f96b35db64` |
| `codegen_plan.md` | `55c5d32ea2cdf54f7f8fb94ae47f29b96d1e2cbf28e104edc81884ed63a6e988` |
| `silu_shared_unit_spec_input.json` | `4ae27068149d1846925dfb91bfc7204aca72eb1c7696db155ef759d989f9719f` |
| `spec/spec/silu_shared_unit_spec.md` | `3603c36a88cbe05452ba9c93b10863a29eb6e6268e5094ad4729211366217752` |
| `generated/silu_table.hex` | `05d6d7062a6b6d0c9178562168d7f8e1554182bb99878b85a0cb6faeb71a25a6` |
| `generated/silu_expected.hex` | `4f6552528d4035f14203e9aafbf8142ad3de8cd5867a0cfdfdcacb5131b908e2` |
| `generated/tb_silu_source_restored.vvp` | `f45d00274503ab442ee310c6883a5b7cf01f8ea4739bbed0839208a3a839cef0` |
| `reports/python_vectors_final.log` | `ec5522d037cbbc183fac74ff8e179ec411996a8806f9610edbda75926f71e253` |
| `reports/iverilog_run_final.log` | `ba66f65ade17732a6abd8d7e0435d8597fe0ea0e3e2218067de94d4eca7855fb` |
| `reports/gate_attempt_6.json` | `3219e6c5a071cc4ad639e85c3f3771978ffa17ae049875f531252ee69d5bb7a5` |

## Release boundary

This is a functionally verified PH1P-interface prototype, not a strict-green production module. Do not connect it to the production classifier or make a one-ERAM/timing claim until module-owned strict findings are repaired and vendor TD confirms mapping and timing.
