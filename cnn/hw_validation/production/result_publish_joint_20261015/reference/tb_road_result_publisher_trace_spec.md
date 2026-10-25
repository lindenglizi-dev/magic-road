# road_result_publisher Python trace replay

The testbench has no ports. It instantiates the unchanged publisher with all 35 real ports, drives all 21 non-clock inputs from the 500-cycle Python golden trace, and compares all 13 outputs before each active edge using four-state inequality. The clock is driven separately at a 10 ns period; a new case label adds a reset assertion before its first vector.

Each vector contains `new_case`, inputs in canonical specification order except `i_clk`, outputs in canonical order, expected state (3 bits), and expected accepted count (7 bits). Total width is 850 bits. State and count are additionally observed after each edge. Each of 33 case labels starts a fresh model instance; common reset makes the RTL initial state match that instance. Reset vectors inside a case are replayed unchanged.

`generate_trace_vectors.py` only packages the existing golden trace; it does not calculate expected RTL values. `run_trace.ps1` binds the exact publisher SHA256, checks the golden input closure, keeps each invocation in a unique directory, and requires a complete PASS marker. This is publisher cycle equivalence evidence only; it does not replace CDC, full-chain, resource, timing, or board validation. No port was invented to satisfy a specification renderer.

The named timing illustration is [trace_waveform.json5](trace_waveform.json5), rendered by the governed WaveDrom runtime to [trace_waveform.svg](trace_waveform.svg). It shows the drive/preedge-check/postedge-check sequence schematically; the 500-cycle golden trace and simulator transcript provide the actual cycle evidence.

The strict gate with `--include-testbench` is preserved in [trace_tb_gate.json](gates/trace_tb_gate.json) and [trace_tb_gate.md](gates/trace_tb_gate.md): delivery_ready=false, 255 errors, 0 strict warnings. It reports formatter/parser limitations for this portless source and style failures; those findings are retained without source repair. ModelSim's actual compilation and 500-cycle simulation remain independently passed with zero errors/warnings. No canonical port was invented and no canonical write-spec was attempted for this portless module.
