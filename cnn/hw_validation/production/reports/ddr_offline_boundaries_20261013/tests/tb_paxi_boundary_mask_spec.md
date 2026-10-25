# `tb_paxi_boundary_mask` interface and timing contract

## Scope

This is an offline testbench for the unchanged
`cnn/hw_validation/ddr/paxi_single_outstanding_bridge.v`. It is not a DDR
controller, PHY, board, capacity, throughput, or persistence test. A generated
`i_commit_confirmed` pulse means only that this conditional endpoint accepted
and applied the observed write; it is not evidence that real DDR completed it.

## Runtime inputs

The top is `tb_paxi_boundary_mask`. The simulator working directory must contain
`vectors.txt` and `addresses.hex`, and must provide:

- `+MODE=0|1|2`: no backpressure, fixed-seed bounded random stalls, or periodic
  1024-cycle stalls.
- `+COUNT=N`: exact number of vector lines to consume.
- `+SLOTS=N`: exact number of address lines; `1 <= N <= 1024`.

Each vector line has six whitespace-separated, prefix-free hexadecimal fields:

```text
op byte_addr mask16 write_data128 expected_read128 slot_index
```

`op=0/1/2/3` means legal read, legal write, illegal read, or illegal write.
`addresses.hex[slot_index]` must equal `byte_addr`.

## Address, data, and endpoint model

- Legal byte addresses are 16-byte aligned and in `[0x03400000, 0x04000000)`.
- The observed native PAXI address must equal `byte_addr >> 1`.
- A 128-bit word is little-endian: lane 0 is bits `[7:0]`.
- Write-mask bit 1 preserves its byte lane; bit 0 writes the observed WDATA byte.
- Sparse memory is indexed only after matching the actually observed PAXI
  address against `addresses.hex`. It is updated only on actual W handshakes.
  `expected_read128` is used solely by the checker and never updates the model.
- A read response is generated at least one cycle after AR acceptance because
  the frozen bridge cannot accept AR and R in the same cycle.

## Handshake and ownership checks

- A request is consumed only on `i_req_valid && o_req_ready`; the testbench
  poisons every upstream payload field immediately after that handshake.
- AW must be accepted before WVALID may appear.
- AW, W, AR, and result payloads must remain stable while blocked.
- Results must retain operation, commit state, epoch, owner, and read data until
  `i_result_ready` accepts them.
- Illegal vectors must enter sticky fault without AW, W, or AR issue; a
  coordinated reset precedes the next vector.
- Six directed cancellation cases cover blocked AW, W, and AR, commit wait,
  return wait, and result backpressure. Each case waits for drain, checks that no
  old result leaks, then completes a read with a new owner. Each named wait is
  held for 1024 measured cycles in the directed suite; request ready and drain
  must remain low throughout. The result case applies its 1024-cycle
  backpressure before cancellation because its endpoint terminal event has
  already occurred.

## Timing examples

Rendered protocol schematics: [write](../specification_attempt3/write.svg),
[read](../specification_attempt3/read.svg). These are illustrative, not captured
waveforms. The canonical writer rejected the genuinely portless testbench with
`ports must be non-empty`; its log is retained in `specification_attempt3`.
The configured WaveDrom runtime rendered both SVGs without adding fake ports.

```json
{signal: [
  {name: "clk", wave: "p......."},
  {name: "req_valid", wave: "010....."},
  {name: "req_ready", wave: "1......."},
  {name: "awvalid", wave: "0.1.0..."},
  {name: "awready", wave: "0..10..."},
  {name: "wvalid", wave: "0...1.0."},
  {name: "wready", wave: "0....10."}
]}
```

The W channel is absent until the cycle after the AW handshake. Backpressure may
extend either valid interval without changing its payload.

```json
{signal: [
  {name: "clk", wave: "p......."},
  {name: "arvalid", wave: "01.0...."},
  {name: "arready", wave: "0.10...."},
  {name: "rvalid", wave: "0..1.0.."},
  {name: "result_valid", wave: "0....1.0"},
  {name: "result_ready", wave: "0.....10"}
]}
```

RVALID starts no earlier than the cycle after AR acceptance. RESULT payload is
held until its ready handshake.

## Completion markers

Every run prints one `SUMMARY` line containing mode, vector/read/write/invalid
counts, six cancellation cases, errors, total observed clock cycles, and the
observed maximum AW/W/AR/commit/return/result wait cycles. Success additionally prints
`PAXI_BOUNDARY_PASS`; any self-check failure prints an explicit `> ERR:` line and
the final `PAXI_BOUNDARY_FAIL` marker before `$finish`.
