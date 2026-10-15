# ROM-R1 candidate handoff — 2026-10-15

## Scope and status

- Branch observed: `work/roadyolo`; no commit was created.
- Candidate root: this directory only. The historical `reports/rom_current_down2_20261013/` tree was treated as read-only.
- Implemented ROM-R1 only: removed the second-stage 160-bit `word_data_o` register from each `road_yolo_numeric_rom_group` instance and directly concatenated the retained registered 80-bit lower/upper pairs.
- The group output becomes visible one clock earlier. `road_numeric_rom_reader` remains unchanged and still samples at `cnt_wait == 4'd7`; its external request/response/data/fault behavior is cycle-identical in the exhaustive comparison below.
- No R2, wait shortening, numeric/kernel/port/II/reset/protocol change, timing exception, TD build, bitstream, training, or board operation was performed.
- Overall status: **functional simulation passed; strict style gate not delivery-ready; physical resource/timing evidence not run**.

## Exact RTL delta and provenance

- Historical group SHA-256 before and after work: `A3EAFE9E403A4292E4458C2FE0C30A77DCE400AC00A3D52459B41FD8E4CE391C` (unchanged).
- Candidate group SHA-256: `05F1D9D70ACAA9FF96265A24D2B359B09C97CCA60A9CEB26E3839FC0B0AAE5CB`.
- Reader SHA-256, historical = candidate: `D22A4FFEC8E3B8536408A117865394C38B8999F7D9BB621CA5CA11E193C79421`.
- Prefetch SHA-256, historical = candidate: `CD20611A1C9493C5FCBC3F30B0188E8BB3815B7F80B3E14F0FEFB64A9511DD80`.
- Top SHA-256, historical = candidate: `B4D9A7599F3E20DD9619E5520E3029C74E78C6C7C705620FB3265B2432609992`.
- All 60 copied initialization artifacts match the historical source by filename and SHA-256; mismatch count is zero.
- The three inherited testbench sources match the historical source byte-for-byte.
- Closure search found `road_numeric_rom_reader.v` as the only selected-closure consumer of `road_yolo_numeric_rom_group` (14 instances). No historical file was globally replaced.
- The removed declaration is 160 bits per group × 14 instances = **2240 structurally declared register bits**. This is not a measured Slice/PLB/MSlice reduction.

## Functional receipts

ModelSim SE-64 2020.4 used the installed Anlogic PH1P ERAM model and `PH1P_PHY_GSR`. The exact compile and simulation invocations are preserved as the first command lines in `reports/simulation_candidate/vlog.log` and each test log.

1. Exhaustive old/new reader comparison
   - Baseline: `reports/simulation_baseline/tb_rom_reader_cycle_trace.log`
   - Candidate: `reports/simulation_candidate/tb_rom_reader_cycle_trace.log`
   - Both report: `TB_PASS_ROM_READER_CYCLE_TRACE words=7168 group_edges=28 wait_reset=1 response_reset=1 max_hold=17 invalid=7168`.
   - Both traces contain 90,114 lines and SHA-256 `515E5B561853538A5B881B8148DEDEBC8B3CF44AB930D080ABBF14C71E42E4C4`; strict line-order comparison found zero differences.
   - Coverage includes every valid word 0..7167, all 14 groups' first/last words, full response backpressure holds, WAIT reset, held-RESPONSE reset, and invalid address 7168 without a fabricated completion.

2. Inherited `tb_rom_reader`
   - Receipt: `reports/simulation_candidate/tb_rom_reader.log`
   - Result: `TB_PASS_ROM_READER words=35 bank_boundaries=28 reset_cancel=1 hold=17 invalid=1`; ModelSim errors 0, warnings 112.

3. Inherited `tb_parameter_prefetch`
   - Receipt: `reports/simulation_candidate/tb_parameter_prefetch.log`
   - Result: `PREFETCH_STALL_PASS count=1676 cycles=13174` and `TB_PASS_PARAMETER_PREFETCH stalled=2 reset_cancel=1 shift63=1 negative_multiplier=1`; errors 0, warnings 0.

4. Inherited `tb_rom_down2`
   - Receipt: `reports/simulation_candidate/tb_rom_down2.log`
   - Result: seven tile cases pass and `TB_PASS_ROM_DOWN2 tiles=7 resets=boot_table_busy invalid_address=checked`; errors 0, warnings 114.
   - Candidate `cycles.csv` SHA-256 equals the historical receipt: `F66F9EC596DEAF4840C35A1148F30CB11CECCC86AD7ACA7C3AD9E9F52E04EFFF`.

The ERAM-heavy tests retain the vendor model's historical `INIT_FILE` part-select warnings; they are not treated as new candidate failures.

## Specification and eight strict gates

- Generated specification: `reports/specification/spec/rom_reader_r1/road_yolo_numeric_rom_group_spec.md`.
- Generated cycle diagram: `reports/specification/spec/rom_reader_r1/waveforms/road_yolo_numeric_rom_group_pair-capture.svg` (source JSON5 beside it).
- WaveDrom preflight first failed in the sandbox temporary directory with a permission error; the authorized local rerun passed using Node 24.21.0, npm 11.19.0, and installed WaveDrom 3.6.1. Nothing was installed.
- Full raw strict-gate outputs remain locally under `reports/gate_original/` and `reports/gate_candidate/`; they are intentionally git-ignored because each JSON exceeds a common remote single-file limit.

| Gate | Actual status | Evidence |
|---|---|---|
| compile | passed | 0 errors, 0 warnings, 7 files/modules |
| AST | failed | 8 formatter errors |
| readability | failed | 5868 errors, 27 warnings |
| comment | failed | 777 errors |
| naming | failed | 1172 errors, 27 warnings |
| profile | failed | 8 errors, 19 warnings |
| testbench static gate | passed | 0 errors, 0 warnings |
| optional toolchain gate | not requested | ModelSim execution is separately evidenced above |

Strict delivery status is therefore false: 6653 errors and 27 strict warnings. These closure-wide legacy/profile diagnostics were recorded rather than expanded into an unrelated formatting rewrite.

For context, the same full-closure gate on the untouched historical RTL also failed with 6651 errors and 27 strict warnings. Candidate counts differ by two total errors: VG138 decreases from 64 to 62 and VG155 increases from 5 to 9; all eight gate statuses are unchanged. The extra VG155 locations reported by the gate are in unchanged reader/prefetch/top/scheduler sources, not in the edited group. This diagnostic delta is recorded, not waived or presented as a pass.

## Not covered / claims deliberately withheld

- No synthesis/place-route/TD run: no measured ERAM, Slice/PLB/MSlice, Fmax, WNS/TNS, power, or route result.
- No claim that physical resources decrease by 2240 bits; only the RTL declaration delta is asserted.
- No bitstream, training, deployment, camera, DDR-loop, or board validation.
- The gate's historical-format diagnostics remain open; they do not negate the separately executed cycle-accurate functional receipts, but the candidate is not strict-gate delivery-ready.
