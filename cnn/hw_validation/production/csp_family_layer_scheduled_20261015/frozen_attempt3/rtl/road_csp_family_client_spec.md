# road_csp_family_client specification

## Intent

`road_csp_family_client` schedules exactly the frozen CSP3 or CSP4 graph
selected by compile-time parameter `C_FAMILY=3` or `C_FAMILY=4`. It reuses one
external arithmetic owner and one 16-byte logical memory service. It does not
implement arithmetic, SiLU, a parameter ROM, DDR transport, or a generic graph
engine.

## Interface and reset

The port list and handshake meanings match the sealed CSP2 client, except the
parameter channel identity is seven bits and parameter group identity is four
bits. `i_rstn` is asynchronous active-low reset. After reset, a start is
accepted only when the client is idle and `i_table_loaded` is high. Valid
payloads remain stable until their matching ready handshake. Cancel and all
identity, address, memory, core, or barrier errors enter sticky fault until
reset.

## Cycle behavior

Each layer visits its 4x4 tiles in y-major then x-major order. A tile is fully
prefetched before parameter collection and task issue. DW layers issue a
three-spatial task and a one-spatial tail for each valid row and channel.
Residual PW layers issue every valid pixel for each three-output group. The
final fuse reads its two physical halves into one logical full-channel cache.
After all writes of a layer are accepted, the client waits for the matching
visibility barrier before starting the next layer.

## Constraints and corner cases

- Only `C_FAMILY=3` and `C_FAMILY=4` are legal.
- CSP3 is 36x64, half 24, full 48; CSP4 is 18x32, half 48, full 96.
- CSP4's final tile row exposes two valid rows; y=18 and y=19 are never written.
- DW out-of-image halo is zero. Physical tile padding is not a logical image row.
- The byte cache and weight bank are not reset; prefetch/parameter collection
  completely overwrite every subsequently read entry.
- One read request and one parameter request may be outstanding in their
  respective sequential phases.
- Output retirement requires both the core output and external writer to
  accept the same legal lane in the same cycle.

## Verification cases

1. Run both legal families with zero stalls and compare every source address,
   parameter identity, core task, write address, barrier and request count to
   the frozen graph reference.
2. Apply random ready/valid bubbles and prove the accepted transaction sequence
   is unchanged.
3. Hold every request and core result under long backpressure and check payload
   stability and single consumption.
4. Check CSP4's y=16 tile reads zero for halo beyond H=18 and emits no y=18/19
   output address in any of the seven stages.
5. Inject wrong layer/channel/group/window, wrong read address, read error,
   wrong core tag/address, duplicate result, barrier mismatch, core fault and
   cancel; each must reject unsafe progress and retain fault until reset.

## Timing diagram

The diagram shows the layer-ending write, visibility barrier and next-layer
start. `write_accept` abbreviates `o_write_valid && i_write_ready` and
`barrier_accept` abbreviates `o_barrier_valid && i_barrier_ready` with matching
layer identity.

```json
{
  "signal": [
    {"name": "i_clk", "wave": "p......."},
    {"name": "write_accept", "wave": "010....."},
    {"name": "o_barrier_valid", "wave": "0.1..0.."},
    {"name": "i_barrier_ready", "wave": "0...10.."},
    {"name": "barrier_accept", "wave": "0...10.."},
    {"name": "o_layer", "wave": "=....=..", "data": ["N", "N+1"]},
    {"name": "next_layer_prefetch", "wave": "0.....10"}
  ]
}
```

The graph allocation table, alias lifetimes, cache-port ownership and exact
request ledger are normative in `design_contract.txt` beside this file.
