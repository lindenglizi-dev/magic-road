# tb_csp_family_client

## Intent

One parameterized Verilog-2001 self-checker for the fixed CSP3 (`36x64x48`) and CSP4 (`18x32x96`) seven-stage clients. It instantiates the same frozen `road_csp_first_probe` arithmetic closure used by CSP2 and contains no private MAC, SiLU, or live-memory golden substitution.

## Observable contract

- `C_FAMILY=3` selects half/full channels `24/48`, 144 tiles, and 442,368 total logical outputs.
- `C_FAMILY=4` selects half/full channels `48/96`, 40 physical tiles, and 221,184 total logical outputs. The last tile row has only `y=16,17`; physical `y=18,19` bytes remain poisoned and unwritten.
- Stages `0,2,4` are DW, stages `1,3,5` are residual PW, and stage `6` is the final full-channel PW.
- The read service is one-outstanding, 16-byte aligned and 128-bit. Source bytes are immutable; intermediate bytes become readable only after a matching accepted stage barrier.
- Parameter channel/group widths are 7/4 bits. Response stability therefore covers all 458 payload bits.

## Numerical checking

Every logical output is compared exactly once at accumulator, pre-requant, SiLU, post-requant, residual sum and final output checkpoints. The arithmetic owner is unchanged; the testbench only packs frozen parameters and compares its internal accepted checkpoints against independently generated HWC reference files.

Accepted-group accounting is independent of client counters. A DW three-output task must accept masks `ff,7f` (15 values) and a tail task `ff,01` (9 values). PW group count is derived from the actual fixed input channels: 3/6 groups for CSP3 half/full and 6/12 for CSP4 half/full.

## Memory and address coverage

All stage storage starts poisoned. Only accepted DUT writes update it, and only an accepted matching barrier copies write visibility forward. The scoreboard decodes every physical `tile4x4_hwc` address to logical HWC, rejects duplicate or padding writes, requires every logical value once, and records all 144 CSP3 or 40 CSP4 tiles for every stage.

## Cases and markers

`../tb_contract.json` is authoritative for cases and machine fields. CASE0 is one normal full run. CASE1 is one randomized-stall full run. CASE2 resets during stage 2 after at least 128 writes, reloads all 1024 SiLU entries, and restarts. CASE3/4 corrupt a read/parameter response. CASE5 corrupts an arithmetic output address or the first barrier. Wrapper CASE99 runs CASE0 with `NEGATIVE_ACC=1` and must fail on a real accumulator comparison.

Every `CSP_FAMILY_PASS`, `CSP_FAMILY_EXPECTED_FAULT`, `CSP_FAMILY_PROGRESS`, `CSP_FAMILY_STAGE`, `CSP_FAMILY_STATE`, and `CSP_FAMILY_RUN` line includes `family`. Successful full runs require exact endpoint cycles equal to the sum of raw states 0 through 16.

## Timing scenario

```json5
{signal: [
  {name: 'clk', wave: 'p............'},
  {name: 'start', wave: '010..........'},
  {name: 'stage', wave: 'x=.=.=.=.=.=.=x', data: ['0','1','2','3','4','5','6']},
  {name: 'barrier', wave: '0.1010101010101'},
  {name: 'done', wave: '0............1'}
]}
```

The next stage cannot consume the prior stage until the matching visibility barrier is accepted.

## Evidence boundary

The testbench can establish local ModelSim functional closure only. It does not prove synthesis, resource mapping, timing, physical DDR behavior, full-network FPS, deployment QAT, bitstream, board operation, or model accuracy.
