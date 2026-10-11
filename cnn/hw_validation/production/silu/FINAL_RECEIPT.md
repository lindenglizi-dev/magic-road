# Superseded SiLU receipt

This historical receipt is superseded by `FINAL_RECEIPT_CURRENT.md`, which records the current PH1P source, latency-5 regression, gate attempt 6, and frozen hashes.

## Frozen decision

- `integration_release=false`
- Functional Python and Icarus evidence passed.
- The third and final strict static gate did not pass: `delivery_ready=false`, `errors=230`, `strict_warnings=0`.
- No further gate repair is permitted in this batch. The module must not be connected to the production wrapper or submitted to TD on the basis of this receipt.

## Implemented contract

- Signed INT16 Q7.8 input/output.
- Raw `<= -2048` returns zero; raw `>= 2048` returns identity.
- Middle address is exact signed RNE division by four plus 512.
- Stored addresses 0..1023 use the runtime-loaded table; address 1024 returns hardwired 2047.
- Ordered runtime loading requires 0..1023. Address zero restarts a complete image after reset, fault, or prior completion when no sample is pending.
- Load faults are sticky until address-zero restart. Partial or faulty load never opens inference.
- Reset cancels the sample pipeline and revokes loaded metadata without clearing the table array.
- Global output-backpressure hold is preserved. Measured no-stall latency is 4 cycles and measured initiation interval is 1 cycle.

## Functional evidence

Tools:

- Python 3.13.12 from `E:\project\qiansai\.tools\road_yolo_venv\Scripts\python.exe`
- Icarus Verilog 12.0 devel build `s20150603-1539-g2693dd32b`
- WaveDrom 3.6.1

Python command:

```powershell
E:\project\qiansai\.tools\road_yolo_venv\Scripts\python.exe -B -X utf8 cnn\hw_validation\production\silu\verify_vectors.py
```

Result: PASS, 1024 table words and all 65536 signed input codes. Log: `reports/python_vectors_final.log`.

Icarus commands:

```powershell
E:\project\qiansai\.tools\iverilog\bin\iverilog.exe -g2005 -Wall -s tb_silu_shared_unit -o cnn\hw_validation\production\silu\generated\tb_silu_shared_unit_final.vvp cnn\hw_validation\production\silu\silu_shared_unit.v cnn\hw_validation\production\silu\tb_silu_shared_unit.v
E:\project\qiansai\.tools\iverilog\bin\vvp.exe cnn\hw_validation\production\silu\generated\tb_silu_shared_unit_final.vvp
```

Result: `TB_PASS inputs=65536 latency=4 ii=1 table_words=1024`. Logs: `reports/iverilog_compile_final.log` and `reports/iverilog_run_final.log`.

Directed coverage included illegal first load address, sticky fault, address-zero recovery, full load activation, output stability for three stalled cycles, reload waiting for a pending result, inference closure during reload, reset cancellation, reset revoking loaded state, and complete post-reset reload.

Canonical specification command used `scripts.python.workflow.cli write-spec` with the local `cnn/hw_validation/settings.json`. It produced `spec/spec/silu_shared_unit_spec.md` and two WaveDrom JSON5/SVG pairs. Formatter fixed-point was checked after the final RTL repair: first pass equals source and the next pass is stable.

## Strict gate evidence

Final command:

```powershell
E:\project\qiansai\.tools\road_yolo_venv\Scripts\python.exe -B -X utf8 -m scripts.python.validation.generated_deliverable_gate cnn\hw_validation\production\silu\silu_shared_unit.v --spec cnn\hw_validation\production\silu\silu_shared_unit_spec_input.json --comment-language zh --formatter-profile formatter-normalize --json cnn\hw_validation\production\silu\reports\gate_attempt_3.json --markdown cnn\hw_validation\production\silu\reports\gate_attempt_3.md
```

Public states:

| State | Result | Errors | Notes |
| --- | --- | ---: | --- |
| compile | passed | 0 | Formatter AST compile state, independently confirmed by Icarus |
| ast | passed | 0 | Strict parser succeeded |
| readability | failed | 218 | Includes operation/source budgets, comment coverage, literals, and memory endpoint findings |
| comment | failed | 12 | Missing nearby semantic block comments |
| naming | failed | 3 | Includes pending-counter classification and output grouping |
| profile | failed | 1 | Strict profile not satisfied |
| testbench | not_requested | 0 | Deliverable gate did not scan TB; external self-checking Icarus run passed |
| toolchain | not_requested | 0 | Deliverable gate optional toolchain state; external Icarus evidence is separate |

Largest final rule counts:

- VG062 process-assignment comments: 103
- VG146 operation budget/inconclusive endpoints: 38
- VG138 explicit literal width/base: 32
- COMMENT_COMMENT_PLACEMENT and VG040: 12 each
- VG145 source-cone limit: 7
- VG125 literal minimal width: 6
- VG085 relational width and VG122 arithmetic width: 4 each
- VG070 output grouping: 3
- VG110, VG113, and VG153 each flag the inferred runtime-written table because the required reset contract intentionally does not clear it and the gate cannot confirm the dynamic memory endpoint.

The gate report paths are `reports/gate_attempt_3.json`, `reports/gate_attempt_3.md`, and `reports/gate_attempt_3.log`. Earlier failed evidence remains in `gate_attempt_1.*` and `gate_attempt_2.*`.

## Frozen hashes

| Artifact | SHA-256 |
| --- | --- |
| `silu_shared_unit.v` | `7d6fdbe7755eb7ca4f624c0b7f169e3d1ca419677d676f6b40d6b7dc0f0ca681` |
| `tb_silu_shared_unit.v` | `eb402e0c9ccad00eb5ca46aa90c464c10fa44ab38f0e429f0635ddbf8be96ceb` |
| `verify_vectors.py` | `4bb78f6b467afa2f3aaccebec369775adea34f453acb8acafc3fd54e3ef4f788` |
| `requirements.md` | `4add277c69c2446ad72cde9728d8740f2c3386fc86debcd7340caaaeb67d8a35` |
| `codegen_plan.md` | `0b9e0896f08103ddb2c7bab28a4cfd2f72133f68a7451fb05d3ba6422c934257` |
| `silu_shared_unit_spec_input.json` | `1af0b11a014e013c2efe0373ef580ca067ff8a1efc3881a876422e6981a40d92` |
| `generated/silu_table.hex` | `05d6d7062a6b6d0c9178562168d7f8e1554182bb99878b85a0cb6faeb71a25a6` |
| `generated/silu_expected.hex` | `4f6552528d4035f14203e9aafbf8142ad3de8cd5867a0cfdfdcacb5131b908e2` |
| `reports/gate_attempt_3.json` | `cfc20294b41a351b250b429bce571235eaefe99440000cdf65c45393cd96a93c` |

## Hardware boundary

The RTL has one unpacked 1024-by-16 active table and a clocked lookup. This is only an inferred-memory coding target. No TD synthesis or vendor mapping was run here, so there is no evidence for PH1P narrow-port selection, one ERAM, primitive count, frequency, or routed timing. A mock/simulator PASS is not controller or silicon evidence.

The interface carries no transaction tag. Any later production wrapper must preserve sample identity through a real handshake FIFO or an equivalent proven ownership mechanism; fixed-cycle tag delay is not valid under backpressure.
