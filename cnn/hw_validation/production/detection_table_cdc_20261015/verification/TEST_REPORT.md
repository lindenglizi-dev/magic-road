# Detection table CDC functional verification report

## Result

All eight final ModelSim cases passed against the frozen RTL, testbench, runner, CPU SRIF reference, and age-telemetry reference hashes recorded in `suite_manifest.json`. Every final compile and simulation reported zero errors and zero warnings.

| Case | Result | Key receipt |
|---:|---|---|
| 0 | PASS | 600010 source / 449985 destination clocks; 6 exact ticks and 6 updates; req→update 4 destination clocks; busy round trip 6–7 source clocks |
| 1 | PASS | 400011 source / 450026 destination clocks; watchdog withdrawal at exactly 150001 destination clocks; recovered to 4 total updates |
| 10 | PASS | counts 0/1/32/33/64; 130 accepted CPU-vector entries; 5 seals, 5 acks, 5 SOF updates; maximum unstalled 64-entry copy 64 destination clocks |
| 11 | PASS | 3 tables / 66 entries / 3 acks / 3 updates; 512-clock disabled-copy interval; maximum observed copy-busy interval 545 destination clocks including the controlled stall |
| 12 | PASS | reset at every copy cursor 0..63; 66 common resets including setup/recovery; 4097 accepted entries; only the final recovery publication acknowledged and activated |
| 13 | PASS | 11 complete one-entry tables; default 500 and independent 2000 boundaries; diagnostic status 1/2/3; invalid-age sentinel and overflow saturation |
| 14 | PASS | partial abort recovery; one sealed-abort error pulse with continued copy; 64 entries accepted on 64 adjacent source clocks and fully read back |
| 20 | PASS | real time→table connection; 5 time updates, 2 table acks/updates; 74994 destination clocks of blocked copy wait; watchdog withdrawal and first-update recovery |

## Endpoint accounting

- Preload is a source-domain interval. The explicit throughput proof is 64 different entries accepted on 64 adjacent 100 MHz source edges (II=1). Case totals that also contain abort setup are not presented as preload latency.
- Seal-to-ack crosses domains and includes stable metadata capture, entry copy, and acknowledgement synchronization. The unstalled 64-entry destination copy occupies 64 destination clocks; the 512-clock gate stall produces a measured 545-clock copy-busy interval for the 33-entry case. Metadata and payload identity are checked at the active output before the acked source generation is reused.
- Pending-to-SOF is externally controlled. Case 11 deliberately holds the second sealed generation behind a full pending slot for 200 destination clocks, then proves the old active table remains intact. Last-copy plus SOF does not bypass; a later SOF is required.
- The integrated case's 74994-destination-clock blocked interval is reported as backpressure waiting, not compute or preload time. `road_time_snapshot` continues independently and produces five real updates in the same run.
- Time case totals are free-running watchdog evidence. They are not added to source preload, cross-domain copy, or SOF wait intervals.

## Age and identity decisions

The default instance accepts raw age 496 (`age_upper=500`) and rejects 497. The independent 2000 ms instance accepts 1996 and rejects 1997 without changing the default parameter. No-active, time-invalid, epoch mismatch, invalid timestamp order, future timestamps, and 65-bit age overflow report `UINT64_MAX`. Model/status mismatches with otherwise valid time retain mathematical age telemetry but cannot draw. Count-zero and status 1/2/3 tables are complete active diagnostic publications and acknowledge normally, while draw remains false.

## Public eight-gate status

| Gate | State | Evidence |
|---|---|---|
| compile | PASS | Readable-Verilog static parser plus all final ModelSim compiles |
| ast | FAIL | Strict formatter-AST reports retained in `time_deliverable_gate.json` and `table_deliverable_gate.json` |
| readability | FAIL | Strict style gate reports 97 time and 628 table readability errors |
| comment | MIXED | Time comment gate passes; table comment gate reports 111 missing/invalid comment placements |
| naming | FAIL | Strict gate reports 4 time and 133 table naming errors |
| profile | PASS | Both files resolve the configured profile/rulebook |
| testbench | PASS | Eight final retained cases, including direct integration and continuous II=1 load |
| toolchain | PASS | ModelSim SE-64 2020.4 compile and execution, zero errors/warnings in final runs |

Functional simulation is therefore PASS, but the strict Readable-Verilog delivery gate is not ready. These style/AST findings were not repaired because this verifier was not authorized to change frozen RTL.

## Retained failures and boundary

Retained failures include two prefreeze timeout-literal syntax attempts, one time-watchdog testbench delta-order failure, and one absolute-vector-path truncation failure. They are fixture evidence and do not replace final receipts.

This work does not establish physical CDC/MTBF safety, RAM mapping, synthesis, place-and-route, TD timing, bitstream, board operation, camera SOF timebase integration, training, or end-to-end detector execution.
