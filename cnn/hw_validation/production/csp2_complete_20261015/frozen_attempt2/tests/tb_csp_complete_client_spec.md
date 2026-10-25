# tb_csp_complete_client

## Intent

Strict self-checking Verilog-2001 testbench for `road_csp_complete_client` connected to the single reused `road_csp_first_probe` arithmetic closure. The testbench supplies only the frozen SiLU table, frozen package parameters, ready/valid backpressure, and a controlled logical-byte memory.

## Interface

- `o_test_complete`: asserted only after the selected case emits its required machine marker and all checks have passed.
- Clock: 100 MHz (`10 ns` period).
- Reset: common asynchronous active-low reset for client, arithmetic closure, and test services.
- Selection: `+CASE`, `+VECTORS`, and the optional `+FAULT_KIND`, `+RESET_STAGE`, and `+NEGATIVE_ACC` plusargs defined by `../tb_contract.json`.

## Behavioral contract

- Only `source.hex` initializes feature memory. Stage memories are populated exclusively by accepted DUT writes.
- A stage read is legal only after that stage's matching visibility barrier has been accepted.
- Every accepted logical-byte read address is independently reconstructed from the active layer, tile coordinate, task coordinate, group, lane, window, and bypass mode.
- Parameter responses are built from the emitted OIHW weights and quantization field arrays. DW lanes receive sparse shifted 3x3 coefficients; PW lanes use `channel+lane` and the current eight-input group.
- Accumulator, pre-requantization, SiLU, post-requantization, residual sum, final output, and output address are checked against the full-HWC reference arrays. Duplicate or missing events fail.
- Request, response, arithmetic-group, write, and barrier payloads remain stable while valid is blocked by ready.
- Completion requires five matching accepted visibility barriers.

## Timing scenarios

### Normal tile

```json5
{signal: [
  {name: 'clk', wave: 'p........'},
  {name: 'start', wave: '010......'},
  {name: 'core_valid', wave: '0.1..0...'},
  {name: 'write_valid', wave: '0....10..'},
  {name: 'barrier_valid', wave: '0......10'},
  {name: 'done', wave: '0.......1'}
]}
```

The sequence repeats across all five layers. Arithmetic and memory progress only on real ready/valid handshakes.

### Barrier delay

```json5
{signal: [
  {name: 'clk', wave: 'p......'},
  {name: 'barrier_valid', wave: '01...0.'},
  {name: 'barrier_ready', wave: '0...10.'},
  {name: 'layer', wave: 'x=...x.', data: ['N']},
  {name: 'done', wave: '0......'}
]}
```

`done` remains low while the barrier is stalled; the layer and barrier payload remain stable.

## Evidence boundary

This testbench provides ModelSim functional evidence only. It does not claim synthesis, timing, physical DDR behavior, bitstream, board operation, or model accuracy.
