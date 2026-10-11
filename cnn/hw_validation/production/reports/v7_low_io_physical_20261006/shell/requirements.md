# Low-I/O physical shell requirements

- Top-level ports are one 100 MHz clock, one active-low asynchronous reset, one 16-bit ready-valid receive channel, and one 16-bit ready-valid transmit channel: 38 package bits total.
- The shell is an independent diagnostic wrapper around the frozen `road_onchip_chain`; it does not change the MAC, round, SiLU, cache, reset, or fixed requantization contracts.
- A runtime table frame delivers all 1024 signed 16-bit SiLU values in ascending implicit address order. A reset invalidates the table and all later computation is blocked until the table is loaded again.
- Exactly one run is allowed after each reset and table reload. After that run only export, diagnostic-read, and status commands are accepted until the next reset.
- A packet frame contains dynamic `first`, `last`, eight-bit lane mask, 64-bit activations, 192-bit weights, and 96-bit biases. Payload words are transferred least-significant word first.
- Up to 96 complete packets are buffered. Each position has one through 24 packets, no more than 192 enabled products, and exactly one first and one last marker. One through four complete positions are accepted.
- A run completes only after the last packet handshake is followed by an observed core-ready busy interval and a later return to ready. Packet acceptance alone is not completion.
- Export reads the frozen chain cache through its real request/response interface. Only `positions * 3` committed values are exported by the normal command; an explicit diagnostic-read command covers uncommitted-address faults.
- Output words are held stable until accepted. Status fields are snapshotted before a multiword response.
- Preload, core-run, and export wall-clock cycles are counted separately. The checksum is auxiliary and never substitutes for comparing every result word.
- Illegal framing, incomplete positions, inconsistent packet counts, table omission, or reduction-bound violations block a run and latch a shell fault until reset.

