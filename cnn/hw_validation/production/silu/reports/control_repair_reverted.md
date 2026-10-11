# Reverted control-pipeline experiment

## Scope

This report records a failed intermediate repair only. The experimental RTL was reverted and is not the frozen deliverable.

## Minimal reproduction

The existing `tb_silu_shared_unit.v` was compiled with the exact-interface `tb_ph1p_logic_eram_runtime_model.v` and the experimental RTL, then run with Icarus. The table contents at addresses 511, 512, 513, and 1023 matched the source table, but the registered loader/inference-open boundary changed the acceptance observation by one cycle.

Observed failures included:

- `TB_ERROR address-zero restart did not close inference`
- First exhaustive mismatch: `raw=-2048 got=-1 expected=0`
- Subsequent results followed a one-sample offset pattern.

## Disposition

The event-delayed loader and registered inference-open experiment was removed. The current source was rebuilt from source and passed the same full testbench as `TB_PASS inputs=65536 latency=5 ii=1 table_words=1024`. Strict control-cone refactoring is deferred to a new batch so this failed experiment cannot become the production baseline.
