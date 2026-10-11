# Commands and exits

All commands were run from the `physical` directory unless a different working
directory is stated.  Native Python/script skills were unavailable; the local
project Python and standard-library fallback were used.

## Python reference

```powershell
E:\project\qiansai\.tools\road_yolo_venv\Scripts\python.exe reference.py
```

Exit: `0`.  Raw output: `logs/reference_stdout.log`.

## RTL simulation

```powershell
E:\project\qiansai\.tools\iverilog\bin\iverilog.exe -g2012 -Wall -s tb_silu_internal_probe -o logs\silu_internal_probe.vvp tb\tb_silu_internal_probe.v rtl\silu_internal_probe.v rtl\silu_shared_unit.v ..\..\..\silu\tb_ph1p_logic_eram_runtime_model.v
E:\project\qiansai\.tools\iverilog\bin\vvp.exe logs\silu_internal_probe.vvp
```

Compile exit: `0`. Simulation exit: `0`. Raw output:
`logs/simulation_stdout.log`.

## Spec and waveform generation

Run from `E:\project\qiansai`, with the checker overlay ahead of the installed
readable-Verilog skill on `PYTHONPATH`:

```powershell
E:\project\qiansai\.tools\road_yolo_venv\Scripts\python.exe -m scripts.python.workflow.cli write-spec --spec <physical>/silu_internal_probe.contract.json --out-dir <physical> --source <physical>/rtl/silu_internal_probe.v --language zh
```

Exit: `0`.  The first attempt from the global skill directory was rejected by
the workspace path guard; the successful command above produced the retained
spec and WaveDrom files without changing the global skill.

## Strict diagnostics

The overlay plus installed skill `quality-gate` was run in strict mode for the
probe file and for the two-file RTL closure.  Both commands exited `1`, as
expected for retained diagnostics.  Exact machine-readable results are
`probe_strict.json` and `closure_strict.json`; their Markdown companions are
retained beside them.  No `--non-strict`, `--warn-only`, threshold change, or
rule/file/module exemption was used.

## TD implementation

Run from `physical/td`:

```powershell
E:\Anlogic\TD_6.2.1_Engineer_6.2.168.116\bin\td_commands_prompt.exe build.tcl
E:\Anlogic\TD_6.2.1_Engineer_6.2.168.116\bin\td_commands_prompt.exe export_internal.tcl
```

Final build exit: `0`.  First export exit: `0`.  Full endpoint/reset export
exit: `0`.  The successful build transcript is `td_20261006_020212.log`; the
full-export transcript is `td_20261006_020615.log`.

An earlier sandboxed TD attempt reached correct vendor elaboration and one-RAM
mapping but could not write `gate.db`; its process nevertheless returned zero.
It is not used as success evidence.  The final run was allowed to write only
inside this authorized physical evidence directory, and success was checked
from generated databases, netlists, reports, and transcript contents rather
than process status alone.
