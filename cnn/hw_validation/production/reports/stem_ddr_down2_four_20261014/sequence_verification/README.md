# Sixteen-Stem/four-down2 direct verification

This regression instantiates `road_stem_ddr_sequence` at 100 MHz and preserves the previous thirteen-case interface. The endpoint stores only accepted DUT writes; reads return those stored words. Golden vectors are comparators only.

Run from this directory:

```powershell
python .\run_verify.py
```

The runner uses ModelSim SE-64 2020.4 plus the Anlogic PH1P `ph1p_phy_gsr.v` and `ph1p_logic_eram.v` models. It writes all generated files below `sequence_verification/case0` and receipts below `sequence_verification/receipts`.

Cases remain `0..12`: normal; random request/response delay; long request/response delay; read corruption; response error; reset during the final Stem write response; reset while the final Stem write request is held; reset during the first overlapping-address read response; reset late in the fourth halo; reset during the fourth down2 run; reset during the fourth down2 export; dropped-read timeout; and DDR fault after a complete PASS.

Every successful full run checks 256 unique writes, the ordered 64/72/72/81 reads (including repeated ownership and 136 reads from indices 128..255), 4,096 Stem bytes, 5,184 halo bytes with per-tile padding 17/9/9/0, 1,536 PW bytes, and all 6,656 Stem/DW/PW accumulator, pre, SiLU, and post values. Both Stem and PW export indices must restart at zero for every tile. Reset cases require a fresh 1,024-entry SiLU table load and no old endpoint transaction.

`receipts/manifest.json` retains `result=PASS_13_OF_13`, `tb_sha256`, `dut_sha256`, and `program_sha256`, and also records the exact compile/run commands, all compiled source hashes, and each case's measured cycle count.
