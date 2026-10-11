# `road_postprocess_low_io_top` structured review

Status: pre-RTL protocol review. Arithmetic behavior is not redefined here.

## Interface

The top has exactly 38 external bits: `i_clk`, active-low `i_rstn`, 16-bit RX ready-valid, and 16-bit TX ready-valid. It adds no UART, AXI, DDR, or board protocol. Accepted RX words frame runtime SiLU table entries, runner load writes, start, and export. Each exported runner result is two TX words: `0x8xxx` metadata containing the nine-bit index, then `0x90xx` containing the exact INT8 data byte. The runner output is acknowledged only with the second word.

## Reset

External reset assertion is asynchronous. Release passes through two flip-flops; the second stage drives the complete shell and runner. RX ready and TX valid are masked until the second stage is high. Reset cancels partial frames and held responses. A new session must reload all dynamic state and the complete 1024-entry table.

## Timing and handshake

RX payload is consumed only when valid and ready are both high. Table and load payloads are held to the runner until its corresponding ready is high; the shell does not infer fixed latency. TX valid and data remain stable under backpressure. The export adapter holds one runner result across the metadata and data transfers, and asserts runner output-ready only on the data-word transfer.

## Width and numerical behavior

The load descriptor transports the runner's three-bit kind and eleven-bit address; its two reserved bits must be zero. Two following words reconstruct signed 32-bit data low-word first. Commands `0x6000` and `0x6001` drive a retained commit-ready register low or high, so the queue-full and writeback-backpressure paths remain runtime-observable and cannot be reduced to a tied constant. The shell performs no rounding, saturation, coefficient substitution, or compile-time operand injection. Result data is the runner's signed INT8 byte; its sign is not recomputed.

## Synthesis and physical scope

The physical top must instantiate `down2_overlap_tile_runner`, whose closure contains the real DW/PW scheduler, dynamic storage, two group buffers, metadata FIFO, frozen v9 MAC, two unchanged round instances, one unchanged SiLU RAM, and result cache. The TD project targets PH1P35MDG324 speed grade -3 at 100 MHz. It stops after route/STA and intentionally has no bit generation.

## Verification coverage

The narrow-shell regression must load the table and all runtime runner memories, start a full PW tile, toggle commit-ready through both levels while the result queue fills and drains, apply RX/TX backpressure, export every result, and compare index/data bit-exactly. Reset is injected during table, load, busy, metadata hold, and data hold. Physical audit must discover primitives from the routed netlist rather than assume old hierarchy or counts.

## Risks and fail-closed decisions

- P&R is blocked until the runner's functional regression passes and its full source closure is hashed.
- Zero input/output delay is diagnostic only; it is expected to preserve external hold exposure and is not production signoff.
- Missing output endpoints, corner coverage, RAM/DSP collections, or a generic `SYN-5025` explanation is a physical failure, not a warning waiver.
- Fixed pre/post coefficients may legally fold. The audit distinguishes that from missing the required 24 MAC DSPs or dynamic feature/table/result storage.
