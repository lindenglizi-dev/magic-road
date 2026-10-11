# road_postprocess_stream specification

## Contract

`road_postprocess_stream` is a single-clock Verilog-2001 postprocess pipeline. It keeps the frozen `road_round_shift` and `silu_shared_unit` arithmetic unchanged and instantiates two round units plus one shared SiLU unit.

- Reset is asynchronous active-low `i_rstn`.
- The atomic input is `{alpha,beta,gamma}` in `i_result_data[31:0]`, `[63:32]`, `[95:64]` with layer, position, aligned triple channel base, and lane mask.
- DW input uses one lane selected by the one-hot mask; PW input uses `3'b111`. Both use an aligned channel base and publish channel `base + selected_lane`.
- Fixed pre factors are `[1,3,5]`, shifts are `[0,2,4]`; post factor is `1`, post shift is `4`.
- The 16-bit tag is `{layer,position[3:0],channel[4:0],6'b0}` and is unchanged through both round units. The eight-entry FIFO supplies the tag across the SiLU unit, which has no tag port.
- The result FIFO stores two complete atomic triples. A group leaves the FIFO only when its final selected scalar is accepted by the pre-round pipeline.
- `o_output_valid`, `o_output_data`, and `o_output_tag` hold under downstream backpressure.
- A terminal input fault, malformed lane/base metadata, arithmetic fault, or table fault latches `o_fault`, suppresses all later input/output handshakes, and requires external reset. Reset also invalidates the unchanged SiLU table, so a complete reload is required before reuse.
- Scalars committed before the fault edge may remain in an internal tile cache, but they are unpublished; the owning runner must suppress whole-tile completion and export. No lane from the faulted atomic input is enqueued.
- The only new observation ports are `o_pre_accept`, `o_silu_accept`, and `o_post_accept`. Both round units and the SiLU unit retain their original ports and source bytes.

## Timing and handshake

`pre_advance = !pre_result_valid || silu_input_handshake`. `post_advance = !post_result_valid || final_output_ready`. Metadata is pushed only by the actual SiLU input handshake and popped only by the actual SiLU output handshake.

Without stalls, a scalar accepted by the pre-round unit at edge `t` becomes visible at the final output after edge `t+23` and is committed by a ready-valid handshake at edge `t+24`. Stalls extend elapsed time without changing ordering, tag, or arithmetic.

## Corner cases

- PW bases are `0,3,...,21`; DW bases are `0,3,...,15` and `base+lane <= 15`.
- A faulted atomic result enqueues no lanes.
- Simultaneous result FIFO push/pop and metadata FIFO push/pop preserve count and ordering.
- INT8 saturation maps values above 127 to 127 and values below -128 to -128.
- SiLU endpoint behavior is owned by the unchanged core, including its address-1024 upper endpoint path.

## Verification cases

1. Continuous PW triples and changing DW selected lanes.
2. Input bubbles and simultaneous queue push/pop.
3. Two full result entries and denied third input.
4. Long final backpressure with stable data/tag and eventual drain.
5. Reset with every queue and pipeline region occupied.
6. Atomic input fault and each round fault with no faulted-lane output.
7. No-stall `+23` valid and `+24` commit endpoints.

## Timing diagram

WaveJSON source: `waveforms/road_postprocess_stream_no_stall.json5`.

