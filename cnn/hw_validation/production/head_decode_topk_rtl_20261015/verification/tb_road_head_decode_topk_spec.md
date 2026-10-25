# tb_road_head_decode_topk verification contract

## Scope

This Verilog-2001 testbench validates `road_head_decode_topk` at its frozen native interfaces. It does not duplicate the production ROM, execute CNN inference, implement NMS, run TD, or claim physical resource mapping.

## Inputs and identity

- Clock: 100 MHz, 10 ns period.
- Reset: active-low `i_rstn`; reset and `i_abort` also flush the controlled LUT endpoint.
- Model: full payload SHA256 `b35d4a66a69e441dc29bc60c7e3f507661f48da5f33b810d7340f6ed17a65145`, interface model ID `32'hB35D4A66`.
- Cells: exactly 12,096 saved 112-bit words in global S4/S8/S16 cell order.
- LUT data: exported from `cnn.integer.tables()` into 1024-entry sigmoid and 256-entry exp memory files. The endpoint returns echoed kind/address/tag/frame/model fields and supports request and response delay.
- Expected records: the saved `top128_decoded_160.hex` files, compared as complete 160-bit values after seal.

## Observable success

For each of the real-image and ten compact pipeline cases:

1. Start and all cell transfers complete only on `valid && ready`.
2. Seal remains stable under 13 cycles of backpressure.
3. Person/vehicle counts match the saved sorted Top128 metadata.
4. Every in-range NMS read response echoes class/index and matches the corresponding full DECODED160 record.
5. A second read request is rejected while one read is outstanding; selected responses remain stable under seven cycles of backpressure.
6. Matching finish returns ownership to FREE without fault.

The protocol suite checks wrong model, wrong cell ID/token, each LUT echo identity field, LUT error, out-of-range read, wrong finish token, and abort while a LUT response is pending. The reset suite independently asserts reset in SCAN, SORT, and DECODE. No failing path may assert seal.

## Measurements

Each successful endpoint run prints:

- start acceptance to first seal-valid cycle;
- mutually exclusive observed SCAN/SORT/DECODE phase cycles;
- DUT scan/sort/decode counters;
- input/LUT/RAM wait counters;
- RAM read/write word counters.

These are local RTL endpoint cycles only. They do not allocate the shared 2M postprocess budget twice and do not convert CPU time to FPGA cycles.

## Timing diagram

The controlled backpressure sequence is recorded in `waveforms/tb_road_head_decode_topk_backpressure.json5`. Request and response payloads must remain stable throughout each wait interval.

## Public delivery gates

The applicable public gates are `compile`, `ast`, `readability`, `comment`, `naming`, `profile`, `testbench`, and `toolchain`. The requested external evidence is a real local simulator compile and execution; static gates are reported separately and do not replace it.

