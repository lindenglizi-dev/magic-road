# v9 frozen-MAC 38-bit shell verification

Status: **PASS** for the frozen functional shell scope.

- Frozen MAC SHA-256: `04a8519e0c9e464add189ee4eb4c5ac25a6c7c716ce0ca4adf2f8fbb0fd19b51`.
- The copied 14-case and 6-case TB sources are byte-identical to the v8 originals. Numeric and timing assertions were not changed.
- Final runs used only the v9 verification working directory and a separate `shell_work_v9_lib` ModelSim library.
- 14-case shell regression: `TB_PASS_LOW_IO`, 405785 ns, 0 errors, 2 known ERAM warnings.
- 6-case reset regression: `TB_PASS_RESET`, 41440 ns, two-stage release and first consume on edge 3, 0 errors, 2 known ERAM warnings.
- No final log contains a failed-open, ENOENT, readmem, `TB_ERROR`, or `TB_FAIL` indication.
- Final post-run freeze audit: v8 250 files and legacy 360 files unchanged.

## Mutually exclusive core-cycle accounting

Each half-open core interval is assigned to exactly one chain-state bucket. The old cycles are comparison data only; the old 436-cycle base is not asserted for the new MAC.

| Run | New core | MAC | Pre-requant | SiLU | Post-requant | Commit | Fault | Old core |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| base16 | 396 | 48 | 132 | 84 | 120 | 12 | 0 | 436 |
| tail13 | 396 | 48 | 132 | 84 | 120 | 12 | 0 | 436 |
| saturation | 98 | 11 | 33 | 21 | 30 | 3 | 0 | 98 |
| atomic_fault | 12 | 11 | 0 | 0 | 0 | 0 | 1 | 13 |
| positive_recovery | 99 | 12 | 33 | 21 | 30 | 3 | 0 | 109 |
| negative_recovery | 99 | 12 | 33 | 21 | 30 | 3 | 0 | 109 |
| maximum_192_legal | 121 | 34 | 33 | 21 | 30 | 3 | 0 | 351 |
| maximum_192_fault | 35 | 34 | 0 | 0 | 0 | 0 | 1 | 266 |
| maximum_96_packets | 484 | 136 | 132 | 84 | 120 | 12 | 0 | 1404 |
| held_export_setup | 98 | 11 | 33 | 21 | 30 | 3 | 0 | 98 |
| reset_recovery_run | 98 | 11 | 33 | 21 | 30 | 3 | 0 | 98 |

The new base16 and tail13 windows are 396 cycles: 48 MAC + 132 pre-requant + 84 SiLU + 120 post-requant + 12 commit + 0 fault. The non-MAC buckets are unchanged from the old baseline; only the MAC bucket falls from 88 to 48.

## Retained failures and scope incident

- The first sandbox launches failed with the known Windows DLL relocation error; logs are retained and the same scoped ModelSim commands were rerun outside the sandbox.
- The first v9-cwd 14-case attempt used an absolute vector path longer than the unchanged TB's 128-byte task argument. It failed with 8 errors and 3 warnings. The final run restored the exact old relative paths, which resolve correctly from `verification`, and passed.
- Before the final v9-only runs, an earlier unchanged-TB run was mistakenly launched from the old v8 reset directory and overwrote its relative `shell_cycle_trace.csv`. That was an out-of-scope write. The file was restored from a frozen identical v7 copy to SHA-256 `8177bc890522004a5cb7b75680e6201ab3f303295ae97bd20aec80893969b44b`; subsequent full 250+360-file audits pass. This history is disclosed even though the restored content now matches.

This supplemental receipt does not modify the already frozen main verification closure or authorize TD, training, bitgen, board, or Flash work.
