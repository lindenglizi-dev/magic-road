# Low-I/O physical shell code-generation plan

1. Freeze and hash the existing chain plus its MAC, round, SiLU, table, and test vectors.
2. Model the 16-bit command stream and reduction guards in `low_io_protocol_reference.py`.
3. Implement one Verilog-2001 wrapper with a 96-packet buffer, a one-word table skid register, run draining, real cache readback, and one-word transmit holding register.
4. Verify partial frames, receive and transmit backpressure, one-to-four positions, 13-channel tails, saturation, atomic MAC fault, diagnostic invalid read, and reset cancellation.
5. Run the strict deliverable gate without suppressing findings. Simulator evidence and strict-style evidence remain separate.
6. Hand the frozen wrapper and source manifest to the physical-flow owner; this directory does not run TD or generate a bitstream.

