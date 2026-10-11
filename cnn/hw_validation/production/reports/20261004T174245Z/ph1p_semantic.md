# PH1P interface-only semantic check

- Interface support ready: `true`
- Eight-gate delivery claimed: `false`
- Existing strict gate modified: `false`
- Public header SHA-256: `9e1c7a39b4f0d8ecbe78301a737674beac63b53237d1970b0003439822cb1627`
- SiLU RTL SHA-256: `ee9beb80decb4f276b9ff81214c22f044a71ac1ffc8c72beb1378e6ddb07a7ed`
- Semantic delivery ready: `false`
- Semantic rule status counts: `{"error": 0, "failed": 7, "inconclusive": 4, "not_run": 0, "passed": 76}`
- Semantic delivery issues: `{"VG084": 1, "VG085": 4, "VG097": 1, "VG122": 4, "VG125": 6, "VG137": 1, "VG138": 38, "VG145": 9, "VG146": 38, "VG147": 20, "VG153": 1}`

## Scope boundary

Only the exact current 20x1024 SiLU instance is admitted. The encrypted vendor body was not interpreted. REGMODE=NOREG timing is not treated as proven, so doa, dob, ecc_sbiterr, and ecc_dbiterr remain opaque; no state_cut is asserted.

## Required negative checks

- unknown_module_rejected: `PASS`
- bad_parameter_rejected: `PASS`
- nonliteral_parameter_rejected: `PASS`
- duplicate_parameter_rejected: `PASS`
- bad_port_width_rejected: `PASS`
- ordinary_data_not_clock: `PASS`

## Remaining boundary

This is a standalone semantic API report, not the high-level eight-gate quality report. It supplies exact interface widths and clock roles only. Vendor read latency, output-register behaviour, collision semantics, reset release behaviour, synthesis mapping, timing closure, and board behaviour remain unproven. TD was not run.
