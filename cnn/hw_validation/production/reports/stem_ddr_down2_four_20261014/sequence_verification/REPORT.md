# Four-tile direct sequence verification report

Date: 2026-10-14  
Result: `PASS_13_OF_13`

## Executed command and toolchain

```powershell
cd E:\project\qiansai\anlogic_topic2_work\lab1_sc500_road_vision\cnn\hw_validation\production\reports\stem_ddr_down2_four_20261014\sequence_verification
python .\run_verify.py
```

The runner invoked ModelSim SE-64 2020.4 at 100 MHz, compiled the real `PH1P_LOGIC_ERAM` and `PH1P_PHY_GSR` vendor models, loaded `PH1P_PHY_GSR`, and ran cases 0 through 12. The exact compiler and simulator argument arrays are retained in `receipts/manifest.json`; `case0/compile.log` reports 0 errors and 0 warnings.

## Bound source closure

| Input | SHA256 |
|---|---|
| `tests/tb_stem_ddr_sequence.v` | `6B3C8CACCC7892E357961334B1039BD4469F6265FF8F91411BBCFA1E4D6B9D49` |
| `rtl/road_stem_ddr_sequence.v` | `4CC56326AB4C9C495A9FBC564BA4397730A309A9574A1CC48B11F39AEA33A523` |
| `vectors/program.hex` | `72FE99E836AD5BB1C2088CE196422DF0EF7024E9168D925046996A297FC5056A` |
| `reference.json` | `8F5A8FDBCCA8D19464D9435B0905B657A0055E49403F740A42B52AD2D0BCBB43` |
| vendor `ph1p_phy_gsr.v` | `787312A19B4007BEF3B76986BCE267966B2D04C1871290CE29905629E38F1524` |
| vendor `ph1p_logic_eram.v` | `70D89B70BDD51812AD86B91E88526B4604EBB117516EFDA5AF976FCDDB2E69AF` |

The manifest also records SHA256 for all eight reused RTL files.

## Case results

The cycle value is the DUT endpoint counter. For reset cases it is the clean rerun generation after the counter was reset; the full two-generation simulation time remains in each ModelSim log.

| Case | Scenario | Status/error | Cycles |
|---:|---|---|---:|
| 0 | normal | 1/0 | 122,921 |
| 1 | random request bubbles and response delay | 1/0 | 127,898 |
| 2 | long request and response wait | 1/0 | 209,576 |
| 3 | read-data corruption | 2/5 expected | 106,119 |
| 4 | response error | 2/7 expected | 11,762 |
| 5 | reset during final Stem write response, then rerun | 1/0 | 122,921 |
| 6 | reset while final Stem write request is held, then rerun | 1/0 | 122,921 |
| 7 | reset during first overlapping-address read response, then rerun | 1/0 | 122,921 |
| 8 | reset late in fourth halo load, then rerun | 1/0 | 122,921 |
| 9 | reset during fourth down2 run, then rerun | 1/0 | 122,921 |
| 10 | reset during fourth down2 export, then rerun | 1/0 | 122,921 |
| 11 | dropped read response watchdog | 2/9 expected | 125,672 |
| 12 | DDR fault after full PASS | 2/1 expected | 122,921 |

## Full-path checks

- 16 Stem tiles exported 4,096 bytes and produced 256 unique accepted 128-bit writes.
- Four down2 tiles consumed exactly 64/72/72/81 words, in the 289-entry `read_indices.hex` order. Repeated words are counted per consumer; all 256 written slots are visited, 33 reads are repeats, and 136 reads use indices 128 through 255 as real data rather than padding.
- Halo scoreboards checked 5,184 loaded bytes and per-tile padding counts 17/9/9/0, including horizontal and vertical tile seams.
- PW exported 1,536 bytes. Stem local export index restarted at zero for all 16 tiles; PW local export index restarted at zero for all four tiles, including tiles three and four.
- Every successful full run compared Stem 4,096, DW 1,024, and PW 1,536 values independently at each of accumulator, pre-requant, SiLU, and post-requant stages: 6,656 checks per stage and 26,624 intermediate comparisons total.
- The six reset cases observed two complete 1,024-entry table loads, cleared endpoint ownership, rejected stale transactions, and completed without old arithmetic/output leakage.
- Golden values only drive comparisons. Read response data is sourced from the endpoint memory populated by accepted DUT writes.

## Readable-Verilog public gate matrix

| Gate | Result | Evidence boundary |
|---|---|---|
| compile | passed | formatter/static gate and ModelSim compile 0 errors/0 warnings |
| ast | passed | formatter AST |
| readability | passed | strict quality gate |
| comment | failed | 147 placement findings on testbench declarations/processes |
| naming | passed | strict quality gate |
| profile | passed | strict quality gate |
| testbench | passed externally | actual 13-case ModelSim execution; generic gate did not request execution |
| toolchain | passed for requested simulation | ModelSim plus instantiated vendor ERAM and loaded GSR; no synthesis claim |

The comment-only gate debt is retained in `deliverable_gate.json`/`.md`; it is non-functional and was not expanded into 147 declaration comments in this bounded verification change.

## Measurement boundary

This is a direct request/response endpoint regression for the frozen candidate and real shared arithmetic core. It proves the stated sequence, data ownership, numerical stages, backpressure, reset, timeout, and post-PASS fault behavior. It does not prove PAXI mailbox CDC, place-and-route timing, full-network DDR throughput, deployment QAT accuracy, bitstream operation, or board behavior.
