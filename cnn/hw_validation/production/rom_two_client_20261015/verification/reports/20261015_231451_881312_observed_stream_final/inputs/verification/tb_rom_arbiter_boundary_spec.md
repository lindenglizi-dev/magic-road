# tb_rom_arbiter_boundary verification contract

One no-port Verilog testbench instantiates one arbiter and exactly one unchanged real reader. The real reader owns the 14-group/56-lane PH1P model closure. `reader_gate` is an explicit testbench request-acceptance interposer: it gates both request-valid and request-ready, never the ROM data or its response timing.

The passive scoreboard separates client admission, physical reader acceptance, and owner response consumption. It compares each completed 160-bit word against the frozen physical payload, checks a single outstanding owner, registered forwarding, held request/response payload, and zero nonowner data. Both continuous clients must alternate admissions; sole clients must complete independently. The first response is held for 43 cycles with its owner's ready low and the other ready high. Remaining ready values follow a deterministic LFSR. Two common-reset cases abort an admitted request before physical acceptance and a held actual-reader response. Recovery reads use the same instance.

Fairness is admission order, conditional on eventual reader acceptance/return and owner ready. The test's finite stalls do not establish an unconditional cycle upper bound. It neither forces ROM data/fault nor audits all 7168 words.

```json
{"signal":[{"name":"clk","wave":"p.........."},{"name":"both_req","wave":"01........0"},{"name":"param_admit","wave":"010........"},{"name":"reader_gate","wave":"0..1......."},{"name":"physical_accept","wave":"0..10......"},{"name":"owner","wave":"=.........=","data":["PARAM","LUT"]},{"name":"owner_response","wave":"0.....1..0."},{"name":"owner_ready","wave":"0.......10."},{"name":"nonowner_ready","wave":"1.........."}],"head":{"text":"Schematic: real reader wait compressed; ready interposer is testbench only"}}
```

Success requires all comparisons, the coverage counts, the watchdog and the unique `TB_PASS_ROM_ARBITER_BOUNDARY` marker. The no-port TB form is accepted by ModelSim but rejected by the current formatter/spec document port contract; strict-gate failure remains in `gates/boundary.json`. This companion is manual documentation, not a claimed successful `write-spec` result.
