# Shared SiLU code-generation plan

1. Freeze the Python authority and exported table hashes in requirements and receipt.
2. Render a canonical module specification and WaveDrom diagrams before RTL.
3. Implement one Verilog-2001 module with ordered runtime load/restart, fail-closed loaded state, global-CE streaming, exact signed RNE divide-by-four, hardwired tails, and one runtime-written `PH1P_LOGIC_ERAM` lookup.
4. Implement a Python audit that imports `cnn.integer`, checks published assets, and emits deterministic local table and exhaustive expected vectors.
5. Implement an exact-interface Icarus PH1P behavior model and a self-checking testbench that drives runtime load, exhausts all signed codes, and tests fault/restart, stalls, stable hold, and reset cancellation.
6. Run canonical spec rendering, Python audit, Icarus, and strict deliverable gate. Repair RTL at most three gate rounds; preserve failures rather than weakening semantics.
7. Freeze hashes and report latency, initiation interval, all public gate states, simulation counts, and the unproven physical-memory boundary.
