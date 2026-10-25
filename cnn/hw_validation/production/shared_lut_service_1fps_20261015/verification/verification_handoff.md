# Shared LUT service verification handoff (2026-10-15)

## Result

- Qualified local compile and simulation: **PASS**. The sandbox-escalated invocation used the same checked-in DUT/TB and existing local Icarus/VVP; compiler and simulator both returned 0.
- Default production offsets: all 1024 sigmoid and 256 exp entries matched the frozen G10 payload exactly, including kind/address/tag/frame-token/model-ID echo.
- Test-only offsets 19/39: all 1280 entries matched; 129 lane-19 entries used the required second word. Production parameter defaults were not changed.
- No RTL mismatch was found. The controlled endpoint maintained one unresolved ROM transaction and held valid payloads under backpressure.

The authoritative machine summary, hashes, commands, and attempt history are in `reports/final_summary.json`.

## Actual timing and ROM traffic

| Instance / set | Queries | Latency from LUT request accept to response valid | ROM word reads |
|---|---:|---:|---:|
| Production offsets, exhaustive | 1280 | min/max/avg = 23/23/23.00 cycles | 1280 |
| Odd 19/39 offsets, exhaustive | 1280 | min/max/avg = 23/26/23.30 cycles | 1409 |
| Production instance, all directed scenarios included | — | variable by injected stalls | 1288 |
| Odd instance, all directed scenarios included | — | variable by injected stalls | 1410 |

The three extra cycles on lane19 are the second controlled-ROM request/return path. Default production offsets contain no cross-word entries. Latency numbers above are endpoint-query cycles only; no reader fixed-wait, DDR, CNN, NMS, CPU conversion, TD, or physical timing is implied.

## Protocol coverage

- Long LUT response hold and ROM request/response delay; request bubbles and dynamic identities.
- Wrong model, exp index 256, and exp index 1023: held error response, original identity, zero data, no ROM read.
- Cancel before ROM acceptance: request suppressed with no endpoint read.
- Cancel after accepted untagged read: no reuse until the late response was drained and discarded; a following query completed normally.
- Cancel between odd lane19 word reads: exactly one word was read and the second request was suppressed.
- Common reset during ROM wait and during held LUT response: no old response leaked.
- Reader fault: owned request returned error and sticky service fault; cancel did not clear it, common reset did.

## Tool receipts

Two normal sandbox runner compiles and one short-path sandbox diagnostic compile produced a VVP image but terminated with Windows access-violation code `3221225477` (`-1073741819`). Each is retained as a failed compile and was not counted as PASS. The short-path image was run only as an explicitly unqualified diagnostic.

One authorized same-source local compile outside that sandbox returned 0, after which VVP returned 0 and printed `TB_PASS_SHARED_LUT`. Evidence:

- `reports/compile_attempt_1.json` / `.log`
- `reports/compile_attempt_2.json` / `.log`
- `reports/compile_shortpath_diagnostic.json`
- `reports/compile_attempt_3_escalated.json` / `.log`
- `reports/simulation_qualified.log`
- `reports/simulation_unqualified_after_compile_failure.log`

No ModelSim retry, installation, remote fallback, or generated failure log was used.

## Gate and scope boundary

The **TB-only** strict readable-Verilog gate for `verification/tb_road_shared_lut_service.v` passes compile, AST, readability, naming, and profile. It remains `delivery_ready=false` solely because the English-comment placement classifier reports 105 testbench comment errors; testbench/toolchain subchecks were not requested by that static gate. This 105 count is not the whole-component result: the main agent's separate DUT gate at `gates/attempt_01.json` reports 526 findings with AST, readability, and naming failures. Neither result replaces or negates the qualified external compiler/simulator evidence, and the component must not be called an eight-gate pass.

The test ROM is a verification-only 7168×160 rendering regenerated directly from the unique G10 package after checking payload SHA-256 `b35d4a66a69e441dc29bc60c7e3f507661f48da5f33b810d7340f6ed17a65145`. It is not a production ROM copy or C7 connection. No ROM-R1 source, production RTL/defaults, CNN, NMS, DDR, training, TD, bitstream, board, or Flash content was changed or exercised.

`readable-python-generator` and `readable-script-generator` were unavailable; they were not installed and no result claims those gates.
