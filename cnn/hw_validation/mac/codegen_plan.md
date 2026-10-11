# Road MAC probe code-generation plan

1. Freeze an 8-input by 3-output signed INT8 beat contract with one shared lane mask.
2. Implement the Python integer model and deterministic seed-42 vectors before RTL.
3. Register 24 products, then use registered pair, quad, and eight-term reductions.
4. Select bias or retained accumulator before the reduction reaches the 33-bit candidate stage.
5. Detect overflow from the two top candidate bits, suppress accumulator commit on fault, and hold the result channel under backpressure.
6. Compare the DUT against generated vectors, reset cancellation, and stable stalled output in a self-checking Verilog testbench.
7. Render the canonical module specification and run the strict eight-gate report before treating the probe as reusable.

The probe accepts only one beat in flight. This intentionally trades throughput for a small, reviewable control path and does not estimate a complete convolution layer or full-network FPS.
