# tb_csp_layer_client

## Intent

Strict self-checking Verilog-2001 testbench for one full 72x128 five-stage execution of `road_csp_layer_client`, connected to the existing single reused `road_csp_first_probe` arithmetic closure. It reuses the frozen road input, parameters, SiLU table, and full-HWC intermediate vectors from `csp2_complete_20261015/reference`.

## Interface and launch

- Clock: 100 MHz (`10 ns` period).
- Reset: common asynchronous active-low reset for the layer client, arithmetic closure, and test services.
- One accepted `i_start` launches all 576 raster tiles for all five stages; tile coordinates are observations, not launch inputs.
- Selection uses `+CASE`, `+VECTORS`, and optional `+FAULT_KIND`, `+RESET_STAGE`, and `+NEGATIVE_ACC` as defined by `../tb_contract.json`.
- `o_test_complete` is asserted only after the selected case has completed every required scoreboard check and emitted its machine marker.

## Memory and visibility contract

- The read service accepts exactly one outstanding 16-byte-aligned request and returns 128 bits with byte `n` in `[n*8 +: 8]`.
- Only `source.hex` initializes readable input data. Intermediate memories start poisoned and are modified only by accepted DUT writes.
- Every byte of every block read must lie in the immutable source region or in a stage region made visible by that stage's matching accepted barrier.
- A matching barrier snapshots actual written bytes as visible. Golden output arrays never populate live intermediate memory.
- Every physical output address is decoded through the independent `tile4x4_hwc` mapping, compared against full-HWC golden values, and accepted exactly once.

## Numerical and coverage contract

- The testbench checks all 663,552 accumulator, pre-requantization, SiLU, post-requantization, residual-sum, and output values.
- Per-stage output counts are `[110592, 110592, 110592, 110592, 221184]`; task counts are `[55296, 36864, 55296, 36864, 73728]`; arithmetic-group counts are `[110592, 73728, 110592, 73728, 221184]`.
- Five independent 576-bit tile ledgers require every 4x4 tile, including all corners and tails, to appear in every stage.
- Full-frame completion requires five matching accepted barriers, all write/intermediate seen maps complete, and the exact aggregate counts in `tb_contract.json`.
- The testbench emits raw `state_current` cycle counts and per-stage ledgers. State interpretation remains runner-owned.

## Cases

- CASE0: one normal full-frame run.
- CASE1: one normal run followed by one deterministic randomized-stall run without reloading the SiLU table.
- CASE2: common reset in a selected active stage, SiLU table reload, then one clean full-frame restart.
- CASE3: wrong read response address.
- CASE4: wrong parameter response layer identity.
- CASE5: wrong arithmetic output address or wrong barrier layer, selected by `FAULT_KIND`.
- Runner wrapper CASE99 invokes CASE0 with `+NEGATIVE_ACC=1`; success requires a real fatal containing `NEGATIVE_ACC injected acc mismatch` and forbids a PASS marker.

## Ready/valid checks

Request, response, arithmetic-group, arithmetic-output, write, and barrier payloads must remain stable while their `valid` is blocked by `ready`. Counts advance only on accepted handshakes. A 50,000,000-cycle watchdog bounds each active run.

## Timing scenario

```json5
{signal: [
  {name: 'clk', wave: 'p..........'},
  {name: 'start', wave: '010........'},
  {name: 'layer', wave: 'x=.=.=.=.=x', data: ['0', '1', '2', '3', '4']},
  {name: 'barrier', wave: '0.101010101'},
  {name: 'done', wave: '0.........1'}
]}
```

Each layer covers the complete tile raster before its visibility barrier. The next layer cannot read the prior stage until the matching barrier is accepted.

## Evidence boundary

This testbench provides ModelSim functional evidence only. It does not establish synthesis, timing closure, physical DDR behavior, bitstream behavior, board operation, or model accuracy.
