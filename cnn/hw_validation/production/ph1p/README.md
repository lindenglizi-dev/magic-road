# PH1P semantic adapter

This directory contains a narrow, fail-closed interface adapter for the one
`PH1P_LOGIC_ERAM` configuration currently instantiated by the SiLU unit.

The check pins the bytes before the vendor source's
`` `pragma protect begin_protected`` marker, verifies the exact public port
order and parameter defaults, then verifies the current named SiLU instance is
the audited 20-bit by 1024-word configuration. It invokes the public
`run_vg_semantic_gate(..., primitive_profile=...)` API with only `clka` and
`clkb` classified as clocks. All RAM outputs remain `opaque` because the
encrypted implementation does not provide public behavioural evidence for
NOREG timing.

This report is additive. It neither changes nor replaces the existing strict
quality-gate report, and it is not evidence of synthesis mapping, timing,
vendor behaviour, or board operation.
