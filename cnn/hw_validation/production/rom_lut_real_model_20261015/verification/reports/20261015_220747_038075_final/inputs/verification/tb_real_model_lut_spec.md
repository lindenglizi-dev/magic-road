# tb_real_model_lut

100 MHz simulation clock; service and its single real reader share active-low asynchronous reset. Instantiate only the production wiring top. Passive hierarchy observations count real ROM acceptance, return and wait; no ROM output, fault, ready or delay is forced.

Checks: all 1024 sigmoid and 256 exp values from frozen payload offsets; dynamic full kind/address/tag/frame/model identity despite idle request-field changes; exact one ROM read per legal default-base entry; 37-cycle client hold; wrong model and exp indices 256/1023 error without ROM read; cancellation before a physical read; cancellation after acceptance with real late response drained before restart; common reset during real read WAIT and held client response.

Timing scenario: `client accept → registered address divide/locate → real reader accept → real reader WAIT → complete client response → ready`. Acceptance cycle is the client handshake rising edge; response cycle is the first rising edge exposing valid. CSV records every completed query. Controlled endpoint fault injection and odd relocation are prior separate evidence, not repeated or relabeled as real-ROM tests.
