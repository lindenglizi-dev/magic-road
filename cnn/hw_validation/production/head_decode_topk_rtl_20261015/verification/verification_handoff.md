# Head Decode Top-K verification handoff (2026-10-15)

## Verdict

- Functional simulation: **13/13 runs passed** (11 regression vectors, protocol faults, and SCAN/SORT/DECODE reset injection).
- RTL mismatch found: **none**.
- Tool verdict: **SIM_PASS_COMPILE_ABNORMAL**. Icarus produced the simulation image and every `vvp` run returned 0, but the compiler process returned Windows exception code `3221225477`; this is intentionally not reported as an all-green compile.
- No CNN/Python inference, training, TD, synthesis, bitstream, board, Flash, or DDR loop was run.

Authoritative machine-readable evidence is `reports/summary.json`; per-run logs are in `reports/*.log`.

## Exact command and run parameters

```powershell
python .\cnn\hw_validation\production\head_decode_topk_rtl_20261015\verification\run_rtl.py --suite all --timeout 600
```

- Simulator: local `iverilog/vvp`
- Compile mode: `-g2012` (DUT source remains Verilog-2001)
- Clock: 100 MHz
- Frame token: `0x10203040`
- Watchdog: 20,000,000 cycles per run
- SEALED backpressure: 13 cycles
- selected-read response backpressure: 7 cycles
- Explicit input/LUT stall case: `threshold_equal_inclusive_and_below`
- Payload SHA-256: `b35d4a66a69e441dc29bc60c7e3f507661f48da5f33b810d7340f6ed17a65145`
- Model ID: `0xB35D4A66`

## Final source hashes used by this run

| File | SHA-256 |
|---|---|
| `rtl/road_head_decode_topk.v` | `c1560e608dfb571b5c268908734d7b3f694fff25be7db13ca802226ed1c5df02` |
| `rtl/road_candidate_ram.v` | `c5d80e1ed84c89c1615ec254dabd80437ad3c0edb4abe62f087d2d17f7789eab` |
| `verification/tb_road_head_decode_topk.v` | `5e3a4db2c49d2f6cf3b11b74577b8a53a0cadc47c043e44449e3b95735ecc0d5` |
| `verification/run_rtl.py` | `905f845a94d446b08aa062f4405d8958d1b89d82ece64288881989187c649212` |
| `verification/prepare_vectors.py` | `8695c649d393809015ca9e97035631b06001195ec07d4fef57786d0fca21afd9` |
| `verification/assets/cases.json` | `14bd5c85df42824bfd661ddeabd96585d260e478782ea9dde4fc6c515d40ac72` |
| `verification/assets/sigmoid_lut_16.hex` | `889fa62b54d26210c37e9260c3e954d1913c0606593381152a2846b2609419ca` |
| `verification/assets/exp_lut_16.hex` | `135731b97a0a144eacf953b80a540eb68591bcb6b5bddb588824917218ca8d0c` |

## Cycle and memory evidence

Counters are mutually exclusive phase cycles. RAM counts at seal are the endpoint snapshot; post-NMS reads are reported separately so they are not charged twice to the shared NMS budget.

| Case | start-to-seal | SCAN | SORT | DECODE | input wait | LUT wait | RAM wait | seal R/W words | post-NMS reads |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| real image | 837581 | 835788 | 709 | 1083 | 1 | 54698 | 868 | 268 / 236 | 316 |
| empty | 616911 | 616898 | 6 | 5 | 1 | 0 | 0 | 0 / 0 | 0 |
| threshold equality | 617064 | 616947 | 6 | 109 | 2 | 41 | 24 | 4 / 8 | 8 |
| Top128 ties | 710191 | 643612 | 43534 | 23043 | 1 | 1024 | 49704 | 17104 / 13448 | 18128 |
| full heap replace | 667770 | 631685 | 24560 | 11524 | 1 | 768 | 26896 | 9316 / 7240 | 9828 |
| cross-scale order | 617329 | 616960 | 94 | 274 | 1 | 12 | 152 | 40 / 48 | 52 |
| person/vehicle same box | 617105 | 616914 | 6 | 183 | 1 | 8 | 48 | 8 / 16 | 16 |
| same-class duplicate | 617162 | 616933 | 44 | 184 | 1 | 8 | 84 | 20 / 28 | 28 |
| zero area after clipping | 617007 | 616906 | 6 | 94 | 1 | 4 | 24 | 4 / 8 | 8 |
| zero area occupies TopK | 663549 | 630254 | 21770 | 11524 | 1 | 512 | 24852 | 8552 / 6724 | 9064 |
| source collapse | 617007 | 616906 | 6 | 94 | 1 | 4 | 24 | 4 / 8 | 8 |

For every sealed regression case, the testbench checks person/vehicle counts and every 160-bit decoded word against the saved golden artifacts. The controlled LUT endpoint supplies the saved sigmoid/exp tables and checks/echoes kind, address, tag, frame token, model ID, and error.

## SEALED/read/finish contract for C9 integration

- `SEALED`: token and class counts remain stable while valid is backpressured. The valid/ready transfer hands the shared candidate RAM to NMS; the profile snapshot is frozen at the first SEALED assertion, before NMS reads increase the live RAM counters.
- `READ`: allow at most one unresolved NMS read. Response echoes class/index/data/error and must remain stable until accepted. Out-of-range reads return error and drive phase `FAULT` (`o_phase=5`).
- `FINISH`: matching frame token plus no unresolved read releases the block to FREE. A mismatched finish token drives the specified finish fault.
- `ABORT/reset`: the verification LUT service flushes pending requests and old responses together with the DUT. This test does not claim cancellation of an external DDR transaction.
- NMS remains a separate shared-RAM consumer. The reported endpoint cycles do not include NMS work, do not allocate another 2 MiB, and do not convert CPU time into FPGA cycles.

## Coverage and diagnostics

Covered: real image, empty table, inclusive threshold equality, TopK full replacement, equal-score ties across scales, zero-area candidate retained in TopK, source-coordinate collapse, input bubbles, long LUT/backpressure waits, seal wait, one unresolved NMS read, selected-response backpressure, wrong cell/model/LUT identity, LUT error, invalid NMS read, wrong finish, abort with an outstanding LUT transaction, and reset during SCAN/SORT/DECODE.

The strict readable-Verilog deliverable gate currently reports **20** `COMMENT_COMMENT_PLACEMENT` errors for 20 of 40 testbench-task checks (not 21). Compile, AST, readability, naming, and profile checks pass; the gate's optional testbench/toolchain stages were not requested. This is a comment-classifier result, separate from the real local Icarus run above. Evidence: `reports/tb_deliverable_gate.json` and `.md`.

ModelSim 2020.4 was present but could not start on this Windows host because of an invalid system-DLL relocation error. No synthetic failure log was added.
