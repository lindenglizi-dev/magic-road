# Shared SiLU RTL requirements

## Scope and authority

- This isolated production-structure prototype does not connect or modify the production top level, DDR bridge, immutable ROM, MAC, parameters, Flash, training, or board flows.
- Numeric authority is `cnn/integer.py` (SHA-256 `441b91d86895fb0c0337583325fb9cc39624026a6759d39da51aaab49a5ca040`) and `cnn/artifacts/shared_tables_v2/silu.hex` (SHA-256 `05d6d7062a6b6d0c9178562168d7f8e1554182bb99878b85a0cb6faeb71a25a6`).
- The DUT is synthesizable Verilog-2001. Its table is populated only by runtime writes; no DUT `initial`, `$readmemh`, or embedded initialization file is allowed.

## Numeric contract

- Input and output are signed 16-bit Q7.8 values.
- Raw input `<= -2048` returns zero; raw input `>= 2048` returns the raw input.
- Otherwise compute `round_div_even(raw, 4) + 512` exactly as `cnn.integer.round_div_even`.
- Stored addresses are 0 through 1023. Address 1024 returns the hardwired `silu_upper=2047`; it is not a hidden 1025th word.
- Every other middle-domain address returns its signed 16-bit loaded table word.

## Runtime load contract

- A complete image is exactly 1024 accepted writes in strict address order 0 through 1023.
- Address 0 explicitly starts or restarts an image after reset, after a fault, or after a completed image, but only while the result pipeline is empty.
- An accepted unexpected address sets a sticky fault and is not written. Only a later accepted address 0 clears the fault and starts a new image.
- `o_table_loaded` becomes one only after the final correctly ordered address 1023 transfer.
- Reset cancels pipeline and clears loaded/fault/progress metadata, but does not clear or initialize the array; a complete reload is required.
- Any asserted load valid blocks inference acceptance. A new load waits for the result pipeline to empty.

## Streaming contract

- Input and output use independent ready/valid handshakes; transfer is `valid && ready`.
- One global pipeline clock-enable advances all sample data/valid registers. Output backpressure holds every stage and keeps visible output stable.
- Inference ready is low unless the table is loaded, no load is presented, and the pipeline can advance.
- Reset cancels all in-flight samples without publishing results.
- Target initiation interval is one cycle when loaded and unstalled; measured latency is reported from simulation.

## Memory and evidence boundary

- The RTL instantiates one `PH1P_LOGIC_ERAM` in `SP` mode with a 1024-by-20 A port. Each signed 16-bit table word is sign-extended into the 20-bit physical word; the B port is disabled.
- `INIT_FILE="NONE"` and `FILL_ALL="NONE"`; reset never clears the primitive contents. `o_table_loaded` stays fail-closed until a new 1024-word image is accepted.
- The local Icarus model reproduces the exact public primitive port list plus synchronous runtime read/write behavior. It is simulation evidence only. Without vendor TD mapping and timing evidence, there is no claim of one physical ERAM, frequency, routing, or silicon behavior.
- The rounded quotient and lookup address remain named RTL registers for golden intermediate inspection.

## Acceptance checks

- Python verifies the source hashes, all table words, RNE address cases, endpoints, tails, and all 65536 signed inputs against `cnn.integer.silu`.
- Icarus loads 1024 words through the DUT handshake and compares all 65536 inputs with the Python-exported exhaustive vector.
- Directed tests cover backpressure, stable output, reset cancellation/reload, illegal order, address-zero restart, and inference refusal during load.
- Canonical spec rendering and all eight strict public gate states must pass before static prototype release.
