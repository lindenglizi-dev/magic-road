# `tb_road_dynamic_postprocess` verification specification

## Scope

This self-checking Verilog-2001 testbench validates only the isolated
`road_dynamic_postprocess` core in one `i_clk` domain. It does not claim
synthesis, physical timing, DDR, full-network throughput, or board behavior.

The DUT interface is the preserved table/batch/result ready-valid interface plus
read-only diagnostic outputs for ingress count, retirement count, SiLU metadata
count, stage busy, and stage acceptance. No internal state name is part of the
testbench contract.

## Clock and reset

- `i_clk`: 100 MHz nominal test clock (`10 ns` period).
- `i_rstn`: asynchronous active-low assertion. The testbench holds reset low for
  three falling edges and supplies synchronous external release.
- Reset cancels all accepted work and table state. Every recovery reloads the
  complete 1024-entry SiLU table in sequential address order before accepting a
  new batch.

## Required behavior

1. A batch and one of eight retirement slots are reserved on the same
   `i_input_valid && o_input_ready` edge.
2. At most two accepted batches wait in ingress, eight batches wait in ordered
   retirement, and eight metadata records wait for the shared SiLU result.
3. Capacity ready signals may bubble when a full FIFO pops on the same edge; no
   combinational capacity look-ahead is required.
4. Each active lane performs RNE/saturating INT32-to-INT16 pre-requantization.
   Activated batches then use the unchanged shared SiLU and RNE/saturating INT8
   post-requantization. Raw batches emit the INT16 pre-result.
5. Batches retire in acceptance order. A good batch becomes externally visible
   only after all its active lane results are complete, then emits active lanes
   in ascending lane order without interleaving another batch.
6. Tags are opaque payload. Repeated tags cannot be used as slot identity.
7. The single result write port gives post-requantization priority. A colliding
   raw completion waits and retries; neither result may be lost or duplicated.
8. Fault detection immediately blocks new batch acceptance. Work already
   accepted may continue internally, but no younger batch is externally visible.
   Older good batches retire intact, including a batch already partly emitted.
   The fault batch emits zero scalars, younger reservations are flushed when the
   fault record reaches the retirement head, and `o_fault` then remains high
   until reset.
9. `o_output_valid` and its complete payload remain stable while
   `i_output_ready` is low.

## Verification cases

- Replay the preserved 330 batches and compare all 604 scalar outputs against
  the saved results. The corpus covers masks `1..7`, raw and activated modes,
  random accumulators, per-lane coefficients, shifts, tags, and saturation edges.
- Continuous input followed by deterministic random gaps; deterministic random
  output backpressure, an 80-cycle stall, periodic 64-cycle stalls, and an
  observed full two-entry ingress queue and eight-slot retirement queue.
- A diagnostic-only force holds the internal SiLU-to-post acceptance event low
  while preserving SiLU ready, solely to fill and check all eight metadata FIFO
  entries. The test releases the force and resets immediately; outputs discarded
  by this artificial gate are never compared or presented as functional traffic.
  The receipt reports the natural metadata high-water mark separately from this
  synthetic capacity stimulus.
- Two batches with identical tags but different coefficients and modes.
- Alternating raw/activated traffic to exercise concurrent pre/post operation and
  the post-priority/raw-retry writeback rule.
- A later fault accepted after lane zero of an older three-lane batch has retired;
  lanes one and two must still retire before sticky public fault.
- A one-edge testbench-only `post_result_fault` pulse on the final lane of a
  younger activated batch, with an older good batch held at the output and one
  more younger batch already accepted. The older batch must emit all three
  scalars; the faulting and younger batches must emit none; public sticky fault
  appears only after the older batch leaves the retirement head.
- Six fault variants: upstream fault, active pre shift 63, active negative-encoded
  multiplier, post shift 63, negative-encoded post multiplier, and zero mask.
- Illegal values in inactive lanes and post fields of raw mode are ignored.
- Reset while ingress, pre, SiLU, metadata, post, and held output are observable;
  reset during a partial table load; complete table reload after every reset.

## Timing diagram

The diagram is illustrative and intentionally has no fixed arithmetic latency.

```json
{
  "signal": [
    {"name": "i_clk", "wave": "p............."},
    {"name": "batch_accept", "wave": "010..10......."},
    {"name": "older_output", "wave": "0.....1.1.1..."},
    {"name": "i_output_ready", "wave": "0.....10.1...."},
    {"name": "fault_detected_internal", "wave": "0.......1....."},
    {"name": "o_input_ready", "wave": "1.......0....."},
    {"name": "o_fault", "wave": "0..........1.."}
  ]
}
```

The essential ordering is: the internal later-batch fault stops new input, the
remaining older output is still held/retired correctly, and public fault becomes
visible only when the fault record reaches the retirement head.
