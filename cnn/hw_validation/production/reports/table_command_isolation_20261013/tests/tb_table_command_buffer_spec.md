# tb_table_command_buffer verification contract

`tb_table_command_buffer` verifies the one-entry table-command buffer inside
`road_frontend_shared_core` at 100 MHz. It uses the existing discrete wrapper
ports and active-low asynchronous reset; arithmetic values are not exercised.

## Required behavior

- External `i_table_valid && o_table_ready` transfers one
  `{address[9:0], data[15:0]}` command to the wrapper.
- Only registered pending payload reaches the postprocessor, so internal write
  acceptance is at least one clock after external acceptance.
- Pending payload remains stable under postprocessor backpressure. Pop and
  replacement push may occur together.
- Pending blocks select, load, start, and export admission.
- Loaded state accepts only address zero. A pending address 1023 may pop, but a
  simultaneous nonzero successor is rejected.
- Asynchronous reset cancels pending state and requires a fresh 1024-word load.
- Existing malformed-address sequencing still raises the postprocessor fault.

The focused test covers downstream backpressure, payload hold, command
barriers, same-cycle push/pop, deterministic bubbles, last-entry drain,
illegal loaded-state input, restart, asynchronous cancellation, malformed
sequencing, and a complete continuous reload. The inherited control test
covers a held unaccepted table request during computation and export.

```text
cycle                 N        N+1       N+2
external valid        1         1         0
external ready        1         1         -
pending before edge   0         1         1
PP valid              0         1         1
PP ready              0         1         1
event                 push     pop+push   pop
```
