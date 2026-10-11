# H1-B code generation plan

1. Freeze the requirements above and model the state transitions in Python before writing RTL.
2. Keep one global owner register and one FSM: idle, read-address, read-return, write-address, write-data, write-commit, held-result, and fault.
3. Cache address/data/mask/epoch/owner at the upstream handshake. Emit W only after AW acceptance so W can never win first.
4. Preserve the cached owner through cancellation until the controller-side read return or explicit commit event drains.
5. Use no timeout, queue, reorder table, generated-IP edit, or production READY path.
6. Generate the Verilog-2001 module and one fixed-seed directed testbench from the Python contract cases.
7. Render the canonical same-name spec and timing diagrams, run the strict eight-gate report, then compile and execute with local Icarus.
8. Report mock evidence separately from unresolved controller/vendor evidence.

The deliberately small ceiling is one controller request and one held result globally. Add an owner FIFO only after vendor return ordering is proven and measured throughput requires concurrency.

