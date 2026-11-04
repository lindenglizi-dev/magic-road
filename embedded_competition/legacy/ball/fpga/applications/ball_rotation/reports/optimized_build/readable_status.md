# Runtime documentation and strict static checks

Source: `rtl/ball_runtime.v`

Runtime SHA256: `2eb661b43781cbf64af15783066dc853ea950fd4adde38ab54bc104f7ef0fd5d`

WaveDrom rendering and exact module/port cross-check: passed.

| Gate | State | Errors | Warnings |
| --- | --- | --- | --- |
| compile | passed | 0 | 0 |
| ast | failed | 1 | 0 |
| readability | failed | 2294 | 5 |
| comment | failed | 203 | 0 |
| naming | failed | 649 | 5 |
| profile | failed | 4 | 0 |
| testbench | not_requested | 0 | 0 |
| toolchain | not_requested | 0 | 0 |

Strict delivery ready: **false**. Total errors: 2498; strict warnings: 5.

AST parsing has zero parse errors; the AST gate fails formatter-template consistency. Static compile is distinct from simulation/synthesis. Existing strict findings were reported without RTL reformatting or architecture changes.

The source contract and companion specify default face=0/rotation=1, capture-scale-load sequencing, clear/epoch/new-result cancellation, display saturation precedence, and unchanged pixel latency. The top-wrapper companion records the two-register debug-vsync synchronizer and current SDC scope.
