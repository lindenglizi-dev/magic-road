# down2_overlap_tile_runner specification

## Contract

`down2_overlap_tile_runner` preserves the frozen tile loader, dynamic on-chip stores, 4x4 DW/PW addressing, export stream, and arithmetic-core interfaces of `down2_tile_runner`. It replaces only the serial postprocess schedule with a reserved two-entry result queue and the independent `road_postprocess_stream`.

- Frozen MAC: one unchanged `road_mac_probe` instance, two eight-lane groups per DW scalar or PW output triple.
- Frozen postprocess arithmetic: two unchanged `road_round_shift` instances and one unchanged `silu_shared_unit` inside the postprocess module.
- `i_commit_ready` is the only new functional input. It backpressures internal DW/PW cache writes without changing the external export `i_output_ready` interface.
- A first accepted MAC group reserves one complete result entry. `R <= 1` and `Q + R <= 2`. The reservation becomes a queued result only on the terminal MAC/postprocess input handshake and is released on that edge.
- DW supplies aligned base `floor(channel/3)*3` and one-hot lane `channel mod 3`; PW supplies base `group*3` and all lanes.
- PW scheduling begins only after all 256 DW writeback handshakes. Successful completion occurs only after all 384 PW writeback handshakes.
- Any load, table, MAC, or postprocess fault clears whole-tile visibility. Export is possible only after fault-free completion.

## Counters

`o_core_cycles` is the accepted-start to final-write completion window. MAC/pre/SiLU/post/writeback counters are non-exclusive occupancy counts and may overlap. Storage-wait and scheduler-idle are mutually exclusive stall categories selected by priority; neither is summed with busy occupancy to claim elapsed time.

The five busy/occupancy counters are deliberately non-exclusive and must never be added to estimate total cycles. Only the endpoint window and mutually exclusive stall categories support elapsed-time accounting.

Endpoint counters increment only on actual handshakes: terminal MAC result, pre-round scalar input, SiLU input, SiLU output/post-round input, and cache writeback. Queue count, reservation, and metadata count are exposed independently.

The preserved single debug event port is informational and cannot represent all simultaneous pipeline events. Verification uses the independent hierarchical handshake taps below `road_postprocess_stream_Inst_tile` and a tag-indexed scoreboard.

## Reset and backpressure

Asynchronous low reset cancels the scheduler, reservation, queues, in-flight valids, completion visibility, and counters. Array contents are ignored until preload flags are rebuilt. Export and postprocess outputs hold data/index/tag under their respective ready-low conditions.

A fault can occur after earlier results were written to an internal cache, including a write accepted on the fault-detection edge. Those writes are unpublished transactions: the runner clears whole-tile validity and forbids export until external reset and a complete reload rebuild all validity flags.

## Interface delta and frozen cores

- The old runner interface is preserved on the newly named wrapper `down2_overlap_tile_runner`.
- New wrapper input: `i_commit_ready`.
- New wrapper observations: queue count, reservation, metadata count, and five handshake endpoint counts.
- New postprocess-only observations: `o_pre_accept`, `o_silu_accept`, and `o_post_accept`; the runner uses ordinary wires, not synthesizable hierarchical references.
- `road_mac_probe`, both `road_round_shift` instances, and `silu_shared_unit` have zero source or port changes. No new coefficient, arithmetic, or debug port is added to any frozen arithmetic core.

## Verification cases

1. Original four full/PW-only tile cases with accumulator, pre, SiLU, post, and final comparisons.
2. Long `i_commit_ready=0` interval filling both result entries without third-task admission.
3. Simultaneous queue push/pop and PW triple serialization.
4. Reset in MAC, queue, each postprocess region, DW drain, PW drain, and export.
5. MAC atomic overflow and malformed preload with no tile export.
6. Endpoint counts: 256 DW writes before PW first group and 384 PW writes before done.

## Timing diagram

WaveJSON source: `waveforms/down2_overlap_tile_runner_layer_boundary.json5`.

