# PH1P interface support receipt

Status: interface-only adapter implemented and executed. This receipt does not
claim the high-level eight-gate flow is green, and does not release SiLU for TD
or production integration.

## Bound authority

- Vendor source: `E:\Anlogic\TD_6.2.1_Engineer_6.2.168.116\sim_release\ph1p\ph1p_logic_eram.v`
- Protected marker byte offset: `9077`
- Public-header SHA-256: `9e1c7a39b4f0d8ecbe78301a737674beac63b53237d1970b0003439822cb1627`
- Full observed vendor-file SHA-256: `70d89b70bdd51812ad86b91e88526b4604ebb117516efda5af976fcddb2e69af`
- Protected payload interpreted: `false`
- SiLU RTL SHA-256: `ee9beb80decb4f276b9ff81214c22f044a71ac1ffc8c72beb1378e6ddb07a7ed`
- Admitted instance: `PH1P_LOGIC_ERAM_Inst_silu_table`
- Admitted configuration: exact current `20 x 1024`, `MODE="SP"`, `REGMODE_A/B="NOREG"` binding recorded in `ph1p_semantic_report.json`

The explicit profile uses the exact public port order and concrete widths.
Only `clka` and `clkb` have `clock_input` roles. `doa`, `dob`,
`ecc_sbiterr`, and `ecc_dbiterr` are all `opaque`. No `state_cut` or read
latency is asserted.

## Execution

The project venv ran:

```powershell
E:\project\qiansai\.tools\road_yolo_venv\Scripts\python.exe -B -X utf8 cnn\hw_validation\production\ph1p\run_ph1p_semantic_check.py --rtl cnn\hw_validation\production\silu\silu_shared_unit.v --vendor-source E:\Anlogic\TD_6.2.1_Engineer_6.2.168.116\sim_release\ph1p\ph1p_logic_eram.v --skill-root C:\Users\lenovo\.codex\skills\readable-verilog-generator --output cnn\hw_validation\production\ph1p\ph1p_semantic_report.json
```

Result: process exit `0`, `interface_support_ready=true`, and
`semantic_gate.delivery_ready=false`.

Required negative checks all passed:

- unknown module remains inconclusive and receives no profile;
- modified `DATA_WIDTH_A=16` is rejected;
- non-literal `DATA_WIDTH_A=SOME_EXPR` is rejected by full association parsing;
- duplicate `DATA_WIDTH_A` association is rejected;
- modified `dia.width=16` is rejected;
- adding a clock role to ordinary data is rejected, while the public role API
  recognizes only `clka` and `clkb` as PH1P clocks among the checked signals.

Frozen artifact SHA-256 values:

- `run_ph1p_semantic_check.py`: `32559a0f11d6e6d21d8e36c2f7ed7cbcdd7dd0304b33b1fcf7f52300a85e410e`
- `ph1p_semantic_report.json`: `93f72809d8b7c2e3304b8222101af4ea43e0c098b672a2405b03b30da494363d`
- `ph1p_semantic_report.md`: `e9c3a9745a225418072e00bda21fcf449236b6075d684cf84e51d8972c6bb663`

## Standalone semantic result

The public `run_vg_semantic_gate(..., primitive_profile=profile)` API executed
against the current SiLU RTL. Of 87 semantic rules, 76 passed, 7 failed, and 4
were inconclusive. Remaining delivery issues are:

`VG084:1, VG085:4, VG097:1, VG122:4, VG125:6, VG137:1, VG138:38, VG145:9, VG146:38, VG147:20, VG153:1`.

In particular, VG097 remains inconclusive at the parameterized PH1P instance,
and opaque RAM output facts remain unknown to downstream cone/driver rules.
That is intentional fail-closed behavior, not evidence of vendor timing.

## Unproven and prohibited conclusions

- The encrypted implementation and `NOREG` read latency are not proven.
- RAM collision, reset-release, synthesis mapping, timing, and board behavior
  are not proven.
- The existing strict gate was not changed or replaced.
- No installed skill was modified or monkeypatched.
- TD and board tests were not run.
