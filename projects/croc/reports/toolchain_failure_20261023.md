# 2026-10-23 Icarus driver failure evidence

During the first `python scripts/validate.py --strict` invocation from the
project root, static checks, the independent model, functional compile and
functional simulation passed. The stress compile returned Windows exception
code `3221225477` (`0xC0000005`), with empty stdout and stderr:

```text
iverilog -g2012 -s tb_croc_gemm_obi_stress -o reports/stress.vvp tb/croc_pkg_stub.sv rtl/mac_array_4x4.sv rtl/gemm_mmio_4x4.sv rtl/croc_gemm_obi.sv tb/tb_croc_gemm_obi_stress.sv
```

The generated summary correctly reported `gate=FAIL`; the stress simulation was
`SKIP`. An existing `.vvp` file is not evidence that this compile invocation
succeeded. No automatic retry or exception-code suppression was added.

Earlier direct compilations and execution of both TBs had succeeded; the issue
is therefore a host/toolchain reliability concern until reproduced and resolved.
The runner subsequently sets `TMPDIR`, `TMP` and `TEMP` to the workspace-owned
`reports/tmp` directory to isolate temporary-file permissions. The current
`summary.json` records the outcome of its latest invocation only.
