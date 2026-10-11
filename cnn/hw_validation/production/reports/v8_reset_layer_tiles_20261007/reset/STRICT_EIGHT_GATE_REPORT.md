# Strict eight-gate report

Date: 2026-10-07  
Policy: failures are evidence and are not waived, suppressed, or relabeled as passes. Functional ModelSim execution is reported separately from the static gate's optional `toolchain` row.

## Frozen baseline evidence retained

| Object | Total errors | compile | ast | readability | comment | naming | profile | testbench | toolchain | Evidence SHA-256 |
| --- | ---: | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| frozen 38-bit shell | 667 | pass | fail 12 | fail 654 | fail 1 | fail 32 | fail 1 | not requested | not requested | `b6f92f5a7ff3c0b17272aec6ee9ad77f8c81169cde44b83feee1eb72521c3fc4` |
| frozen on-chip chain | 374 | pass | fail 1 | fail 370 | fail 3 | fail 12 | pass | pass | not requested | `ff31f0e2adefb4e134fc9b7598a16b32b6b004b3659422b508ec57a36af73c52` |
| frozen included testbench | 219 | fail 1 | fail 2 | fail 125 | fail 93 | fail 120 | fail 1 | pass | not requested | `f567a81df6cf07be92f271270a006169dae81319686eced3ae5434affb528d5c` |

The historical `667 / 374 / 219` counts remain present in their original reports. No old file was rewritten.

## New reset candidate evidence

| Object | Total errors | compile | ast | readability | comment | naming | profile | testbench | toolchain | Evidence SHA-256 |
| --- | ---: | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `road_low_io_reset_shell.v` | 54 | pass | fail 1 | fail 52 | fail 1 | fail 7 | pass | not requested | not requested | `06ae08bc5b2ee48e042bbb11a7c688553244d393ba21ae8b175645e2130c3ce5` |
| reset-focused TB | 148 | fail 1 | fail 2 | fail 119 | fail 28 | fail 112 | fail 1 | pass | not requested | `11c507913823e672f96b1a877246b5146ec2c32ba9f40d851a64183d5f6bf282` |

Neither new object is strict-delivery-ready. The wrapper was deliberately frozen at SHA-256 `8bd23e055a25af2691c867bad3f1d7e16b81fd39614748c4e988b1113493538e` after physical build source capture; style-only edits would invalidate that physical provenance and were not made.

The adapted fourteen-case TB has two current, non-passing static artifacts after its vector-path-only update:

- `strict_regression_tb_qg.json`: strict quality gate with testbench rules enabled, 125 errors, 0 warnings, SHA-256 `e0e48742a45fcdbfda9cf0c6d528a3d40a7aa515f2819a57023cb042e0150b2c`.
- `strict_regression_tb.json`: comment-aware review, 93 errors, 0 strict warnings, `delivery_ready=false`, SHA-256 `90ed80c1edaf9c5684b56c0ef6286d427b4e1d113e58961f7449869345b48558`.

These two adapted-TB runs use different gate entry points, so their error counts are not additive. They do not replace or erase the frozen baseline integrated TB report with 219 errors. The adapted TB's executable result is independently `TB_PASS_LOW_IO cases=14 errors=0` under ModelSim with the vendor ERAM model.

## Interpretation

- Static strict status: **failed and retained**.
- ModelSim functional status: **passed 14 regression cases plus 6 reset cases**.
- Physical status: **not deployment-ready**; routed setup passes, while minimum/removal findings remain in the physical reports.
- No waiver, new timing exception, behavioral memory substitution, production bitstream, board programming, or Flash action was used.
