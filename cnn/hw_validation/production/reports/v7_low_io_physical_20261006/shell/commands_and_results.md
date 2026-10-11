# Commands and retained results

## Python contract and trace checks

Run with `E:/project/qiansai/.tools/road_yolo_venv/Scripts/python.exe` from this directory:

```text
python low_io_protocol_reference.py
REFERENCE_PASS packets=24 positions=1 max_terms=192

python analyze_shell_trace.py
TRACE_PASS runs=11 base_delta=436

python generate_phase_cycle_csv.py
PHASE_CSV_PASS completed=11 cancelled=1

python freeze_manifest.py
MANIFEST_PASS shell_sha256=c7bd74ccf995f7f7a8527e7c6f8f661183bccd0a3f266922d4c0a026d019f5d5
```

## Final clean ModelSim evidence

The final clean library is `shell_work_frozen`. It compiles the frozen chain, signed-33 MAC, round unit, SiLU, official PH1P models, shell, and testbench, then simulates both `PH1P_PHY_GSR` and `tb_road_low_io_physical_shell`.

```text
modelsim_shell_compile_frozen_c7bd.log: Errors: 0, Warnings: 0
modelsim_shell_run_frozen_c7bd.log: TB_PASS_LOW_IO cases=14 errors=0 io_bits=38 max_packets=96 max_groups=24 max_terms=192
modelsim_shell_run_frozen_c7bd.log: Errors: 0, Warnings: 2
```

The two simulation warnings are the retained vendor-model `INIT_FILE` MSB/LSB out-of-bounds warnings from `ph1p_logic_eram.v(165)`.

## Strict delivery checks

The canonical strict command was run against the frozen shell source. The TB was also run with `--include-testbench` so it was not counted as an empty/excluded source set.

```text
generated_deliverable_gate road_low_io_physical_shell.v
delivery_ready=False errors=667 strict_warnings=0

generated_deliverable_gate tb_road_low_io_physical_shell.v --include-testbench
delivery_ready=False errors=219 strict_warnings=0
```

The older `strict_tb.json` has 93 comment findings but `include_testbench=false`, so its compile/AST/readability passes are not used as TB source evidence. The authoritative explicit TB report is `strict_tb_included.json`.

External ModelSim success is documented separately and does not convert either report's public `toolchain: not_requested` field into a pass.
