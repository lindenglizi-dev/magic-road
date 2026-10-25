# Preserved first local launch failure

Attempt: `20261015_220321_258395_sandbox`.

Command: `python verification/run_real_rom.py`, cwd is the new real-model package root. Python reached `subprocess.run` for the exact `vlib` argv recorded in that attempt's `summary.json`, then Windows refused process creation with `OSError: [WinError 623]` (invalid system DLL relocation). No ModelSim compile or simulation ran; no child return code exists. The initial runner did not catch OSError, so the original summary remains `STARTED`, not PASS. This supplemental receipt explicitly classifies it as `PROCESS_LAUNCH_FAILED` while preserving the original file and immutable input closure.

The runner now catches OSError and records it as a failed process launch. The following elevated attempt reached compile successfully but exposed a separate library-name invocation error. Both failures remain retained; neither was counted as successful verification.
