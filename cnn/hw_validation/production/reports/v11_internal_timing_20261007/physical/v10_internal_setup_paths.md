# Frozen v10 internal setup failures

Extracted from `coverage_100000_violations.timing`; top-level output endpoints are excluded.

| Rank | Slack | Begin | End | Data path | Logic |
|---:|---:|---|---|---|---|
| 1 | -0.232 ns | `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/reg_group_mask_head_reg[1]_syn_14.clk` | `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/road_round_shift_Inst_pre/reg_absolute_reg[34]_syn_2.id` | 10.042ns (cell 4.973ns (49%), net 5.069ns (51%)) | 6 ( ADDER=2  LUT5=1  LUT3=1  DSPTADD=1  DSPMULT=1 ) |
| 2 | -0.152 ns | `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/reg_group_mask_head_reg[1]_syn_14.clk` | `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/road_round_shift_Inst_pre/reg_absolute_reg[31]_syn_2.ima` | 9.962ns (cell 5.191ns (52%), net 4.771ns (48%)) | 6 ( ADDER=2  LUT5=1  LUT3=1  DSPTADD=1  DSPMULT=1 ) |
| 3 | -0.151 ns | `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/silu_shared_unit_Inst_shared/table_fault_o_reg_syn_19.clk` | `down2_overlap_tile_runner_Inst_shell/cnt_output_reg[2]_syn_36.imb` | 9.893ns (cell 1.814ns (18%), net 8.079ns (82%)) | 7 ( LUT3=3  LUT6=1  LUT5=1  LUT4=1  LUT2=1 ) |
| 4 | -0.074 ns | `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/reg_group_mask_head_reg[1]_syn_14.clk` | `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/road_round_shift_Inst_pre/reg_absolute_reg[33]_syn_2.id` | 9.884ns (cell 4.914ns (49%), net 4.970ns (51%)) | 6 ( ADDER=2  LUT5=1  LUT3=1  DSPTADD=1  DSPMULT=1 ) |
| 5 | -0.056 ns | `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/reg_group_mask_head_reg[1]_syn_14.clk` | `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/road_round_shift_Inst_pre/reg_absolute_reg[29]_syn_2.id` | 9.931ns (cell 4.914ns (49%), net 5.017ns (51%)) | 6 ( ADDER=2  LUT5=1  LUT3=1  DSPTADD=1  DSPMULT=1 ) |
| 6 | -0.044 ns | `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/silu_shared_unit_Inst_shared/table_fault_o_reg_syn_19.clk` | `down2_overlap_tile_runner_Inst_shell/road_mac_probe_Inst_tile/mult17_syn_57.xa[1]` | 9.655ns (cell 0.977ns (10%), net 8.678ns (90%)) | 3 ( LUT4=2  LUT2=1 ) |
| 7 | -0.004 ns | `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/reg_group_mask_head_reg[1]_syn_14.clk` | `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/road_round_shift_Inst_pre/reg_absolute_reg[35]_syn_2.imf` | 9.814ns (cell 5.038ns (51%), net 4.776ns (49%)) | 6 ( ADDER=2  LUT5=1  LUT2=1  DSPTADD=1  DSPMULT=1 ) |

## Path 1: -0.232 ns

- Begin: `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/reg_group_mask_head_reg[1]_syn_14.clk`
- End: `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/road_round_shift_Inst_pre/reg_absolute_reg[34]_syn_2.id`
- Corner: `slow_m40c`
- Budget: 10.000ns { probe_clk rising@10.000ns - probe_clk rising@0.000ns }
- Data delay: 10.042ns (cell 4.973ns (49%), net 5.069ns (51%))
- Clock skew: 0.076ns
- Logic: 6 ( ADDER=2  LUT5=1  LUT3=1  DSPTADD=1  DSPMULT=1 )
- Max fanout: 38
- Source cone:
  - `../rtl/road_postprocess_stream.v(54)`
  - `../rtl/road_postprocess_stream.v(70)`
  - `../rtl/road_postprocess_stream.v(124)`
  - `../../v7_onchip_chain_20261006/inputs/road_round_shift.v(164)`
  - `../../v7_onchip_chain_20261006/inputs/road_round_shift.v(72)`
- Routed cell sequence:
  - `LUT5` → `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/wire_scalar_extended[0]_syn_2.ofb`
  - `DSPSIOU` → `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/mult0_syn_170.mult_x[0]`
  - `DSPMULT` → `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/mult0_syn_171.p[19]`
  - `DSPSIOU` → `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/mult0_syn_170.cpo[19]`
  - `DSPSIOU` → `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/mult0_syn_265.tadd_c[2]`
  - `DSPTADD` → `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/mult0_syn_360.sum[5]`
  - `DSPSIOU` → `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/mult0_syn_265.p[5]`
  - `ADDER` → `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/road_round_shift_Inst_pre/neg1_syn_172.fco_f`
  - `ADDER` → `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/road_round_shift_Inst_pre/neg1_syn_173.fco_f`
  - `ADDER` → `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/road_round_shift_Inst_pre/neg1_syn_174.fco_f`
  - `ADDER` → `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/road_round_shift_Inst_pre/neg1_syn_175.fco_f`
  - `ADDER` → `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/road_round_shift_Inst_pre/neg1_syn_176.fco_f`
  - `ADDER` → `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/road_round_shift_Inst_pre/neg1_syn_177.fco_f`
  - `ADDER` → `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/road_round_shift_Inst_pre/neg1_syn_178.fco_f`
  - `ADDER` → `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/road_round_shift_Inst_pre/neg1_syn_179.fco_f`
  - `ADDER` → `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/road_round_shift_Inst_pre/neg1_syn_180.fco_f`
  - `ADDER` → `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/road_round_shift_Inst_pre/neg1_syn_181.fco_f`
  - `ADDER` → `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/road_round_shift_Inst_pre/neg1_syn_182.fco`
  - `ADDER` → `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/road_round_shift_Inst_pre/neg1_syn_183.fco`
  - `ADDER` → `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/road_round_shift_Inst_pre/neg1_syn_184.ofb`

## Path 2: -0.152 ns

- Begin: `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/reg_group_mask_head_reg[1]_syn_14.clk`
- End: `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/road_round_shift_Inst_pre/reg_absolute_reg[31]_syn_2.ima`
- Corner: `slow_m40c`
- Budget: 10.000ns { probe_clk rising@10.000ns - probe_clk rising@0.000ns }
- Data delay: 9.962ns (cell 5.191ns (52%), net 4.771ns (48%))
- Clock skew: 0.076ns
- Logic: 6 ( ADDER=2  LUT5=1  LUT3=1  DSPTADD=1  DSPMULT=1 )
- Max fanout: 38
- Source cone:
  - `../rtl/road_postprocess_stream.v(54)`
  - `../rtl/road_postprocess_stream.v(70)`
  - `../rtl/road_postprocess_stream.v(124)`
  - `../../v7_onchip_chain_20261006/inputs/road_round_shift.v(164)`
  - `../../v7_onchip_chain_20261006/inputs/road_round_shift.v(72)`
- Routed cell sequence:
  - `LUT5` → `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/wire_scalar_extended[0]_syn_2.ofb`
  - `DSPSIOU` → `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/mult0_syn_170.mult_x[0]`
  - `DSPMULT` → `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/mult0_syn_171.p[19]`
  - `DSPSIOU` → `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/mult0_syn_170.cpo[19]`
  - `DSPSIOU` → `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/mult0_syn_265.tadd_c[2]`
  - `DSPTADD` → `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/mult0_syn_360.sum[5]`
  - `DSPSIOU` → `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/mult0_syn_265.p[5]`
  - `ADDER` → `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/road_round_shift_Inst_pre/neg1_syn_172.fco_f`
  - `ADDER` → `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/road_round_shift_Inst_pre/neg1_syn_173.fco_f`
  - `ADDER` → `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/road_round_shift_Inst_pre/neg1_syn_174.fco_f`
  - `ADDER` → `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/road_round_shift_Inst_pre/neg1_syn_175.fco_f`
  - `ADDER` → `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/road_round_shift_Inst_pre/neg1_syn_176.fco_f`
  - `ADDER` → `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/road_round_shift_Inst_pre/neg1_syn_177.fco_f`
  - `ADDER` → `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/road_round_shift_Inst_pre/neg1_syn_178.fco`
  - `ADDER` → `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/road_round_shift_Inst_pre/neg1_syn_179.fco`
  - `ADDER` → `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/road_round_shift_Inst_pre/neg1_syn_180.fco`
  - `ADDER` → `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/road_round_shift_Inst_pre/neg1_syn_181.ofb`
  - `LUT3` → `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/road_round_shift_Inst_pre/reg_absolute_reg[30]_syn_2.ofb`

## Path 3: -0.151 ns

- Begin: `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/silu_shared_unit_Inst_shared/table_fault_o_reg_syn_19.clk`
- End: `down2_overlap_tile_runner_Inst_shell/cnt_output_reg[2]_syn_36.imb`
- Corner: `slow_m40c`
- Budget: 10.000ns { probe_clk rising@10.000ns - probe_clk rising@0.000ns }
- Data delay: 9.893ns (cell 1.814ns (18%), net 8.079ns (82%))
- Clock skew: 0.119ns
- Logic: 7 ( LUT3=3  LUT6=1  LUT5=1  LUT4=1  LUT2=1 )
- Max fanout: 28
- Source cone:
  - `../rtl/road_postprocess_stream.v(13)`
  - `../rtl/down2_overlap_tile_runner.v(318)`
  - `../rtl/down2_overlap_tile_runner.v(289)`
  - `../rtl/down2_overlap_tile_runner.v(85)`
- Routed cell sequence:
  - `LUT3` → `down2_overlap_tile_runner_Inst_shell/mux106_syn_77.ofb`
  - `LUT6` → `down2_overlap_tile_runner_Inst_shell/mux106_syn_76.ofb`
  - `LUT4` → `down2_overlap_tile_runner_Inst_shell/mux106_syn_103.ofb`
  - `LUT3` → `down2_overlap_tile_runner_Inst_shell/flag_result_reserved_reg_syn_8.ofa`
  - `LUT2` → `reg_load_addr_reg[8]_syn_2.ofb`
  - `LUT3` → `down2_overlap_tile_runner_Inst_shell/cnt_output_reg[3]_syn_47.ofb`
  - `LUT5` → `down2_overlap_tile_runner_Inst_shell/cnt_output_reg[3]_syn_46.ofa`

## Path 4: -0.074 ns

- Begin: `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/reg_group_mask_head_reg[1]_syn_14.clk`
- End: `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/road_round_shift_Inst_pre/reg_absolute_reg[33]_syn_2.id`
- Corner: `slow_m40c`
- Budget: 10.000ns { probe_clk rising@10.000ns - probe_clk rising@0.000ns }
- Data delay: 9.884ns (cell 4.914ns (49%), net 4.970ns (51%))
- Clock skew: 0.076ns
- Logic: 6 ( ADDER=2  LUT5=1  LUT3=1  DSPTADD=1  DSPMULT=1 )
- Max fanout: 38
- Source cone:
  - `../rtl/road_postprocess_stream.v(54)`
  - `../rtl/road_postprocess_stream.v(70)`
  - `../rtl/road_postprocess_stream.v(124)`
  - `../../v7_onchip_chain_20261006/inputs/road_round_shift.v(164)`
  - `../../v7_onchip_chain_20261006/inputs/road_round_shift.v(72)`
- Routed cell sequence:
  - `LUT5` → `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/wire_scalar_extended[0]_syn_2.ofb`
  - `DSPSIOU` → `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/mult0_syn_170.mult_x[0]`
  - `DSPMULT` → `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/mult0_syn_171.p[19]`
  - `DSPSIOU` → `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/mult0_syn_170.cpo[19]`
  - `DSPSIOU` → `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/mult0_syn_265.tadd_c[2]`
  - `DSPTADD` → `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/mult0_syn_360.sum[5]`
  - `DSPSIOU` → `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/mult0_syn_265.p[5]`
  - `ADDER` → `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/road_round_shift_Inst_pre/neg1_syn_172.fco_f`
  - `ADDER` → `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/road_round_shift_Inst_pre/neg1_syn_173.fco_f`
  - `ADDER` → `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/road_round_shift_Inst_pre/neg1_syn_174.fco_f`
  - `ADDER` → `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/road_round_shift_Inst_pre/neg1_syn_175.fco_f`
  - `ADDER` → `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/road_round_shift_Inst_pre/neg1_syn_176.fco_f`
  - `ADDER` → `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/road_round_shift_Inst_pre/neg1_syn_177.fco_f`
  - `ADDER` → `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/road_round_shift_Inst_pre/neg1_syn_178.fco_f`
  - `ADDER` → `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/road_round_shift_Inst_pre/neg1_syn_179.fco_f`
  - `ADDER` → `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/road_round_shift_Inst_pre/neg1_syn_180.fco_f`
  - `ADDER` → `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/road_round_shift_Inst_pre/neg1_syn_181.fco_f`
  - `ADDER` → `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/road_round_shift_Inst_pre/neg1_syn_182.fco`
  - `ADDER` → `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/road_round_shift_Inst_pre/neg1_syn_183.ofb`

## Path 5: -0.056 ns

- Begin: `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/reg_group_mask_head_reg[1]_syn_14.clk`
- End: `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/road_round_shift_Inst_pre/reg_absolute_reg[29]_syn_2.id`
- Corner: `slow_m40c`
- Budget: 10.000ns { probe_clk rising@10.000ns - probe_clk rising@0.000ns }
- Data delay: 9.931ns (cell 4.914ns (49%), net 5.017ns (51%))
- Clock skew: 0.011ns
- Logic: 6 ( ADDER=2  LUT5=1  LUT3=1  DSPTADD=1  DSPMULT=1 )
- Max fanout: 38
- Source cone:
  - `../rtl/road_postprocess_stream.v(54)`
  - `../rtl/road_postprocess_stream.v(70)`
  - `../rtl/road_postprocess_stream.v(124)`
  - `../../v7_onchip_chain_20261006/inputs/road_round_shift.v(164)`
  - `../../v7_onchip_chain_20261006/inputs/road_round_shift.v(72)`
- Routed cell sequence:
  - `LUT5` → `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/wire_scalar_extended[0]_syn_2.ofb`
  - `DSPSIOU` → `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/mult0_syn_170.mult_x[0]`
  - `DSPMULT` → `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/mult0_syn_171.p[19]`
  - `DSPSIOU` → `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/mult0_syn_170.cpo[19]`
  - `DSPSIOU` → `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/mult0_syn_265.tadd_c[2]`
  - `DSPTADD` → `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/mult0_syn_360.sum[5]`
  - `DSPSIOU` → `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/mult0_syn_265.p[5]`
  - `ADDER` → `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/road_round_shift_Inst_pre/neg1_syn_172.fco_f`
  - `ADDER` → `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/road_round_shift_Inst_pre/neg1_syn_173.fco_f`
  - `ADDER` → `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/road_round_shift_Inst_pre/neg1_syn_174.fco_f`
  - `ADDER` → `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/road_round_shift_Inst_pre/neg1_syn_175.fco_f`
  - `ADDER` → `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/road_round_shift_Inst_pre/neg1_syn_176.fco_f`
  - `ADDER` → `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/road_round_shift_Inst_pre/neg1_syn_177.fco_f`
  - `ADDER` → `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/road_round_shift_Inst_pre/neg1_syn_178.fco`
  - `ADDER` → `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/road_round_shift_Inst_pre/neg1_syn_179.ofb`

## Path 6: -0.044 ns

- Begin: `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/silu_shared_unit_Inst_shared/table_fault_o_reg_syn_19.clk`
- End: `down2_overlap_tile_runner_Inst_shell/road_mac_probe_Inst_tile/mult17_syn_57.xa[1]`
- Corner: `slow_m40c`
- Budget: 10.000ns { probe_clk rising@10.000ns - probe_clk rising@0.000ns }
- Data delay: 9.655ns (cell 0.977ns (10%), net 8.678ns (90%))
- Clock skew: 0.059ns
- Logic: 3 ( LUT4=2  LUT2=1 )
- Max fanout: 54
- Source cone:
  - `../rtl/road_postprocess_stream.v(13)`
  - `../rtl/down2_overlap_tile_runner.v(289)`
  - `../rtl/down2_overlap_tile_runner.v(141)`
- Routed cell sequence:
  - `LUT4` → `down2_overlap_tile_runner_Inst_shell/cnt_mac_group_reg_syn_65.ofb`
  - `LUT4` → `down2_overlap_tile_runner_Inst_shell/cnt_mac_group_reg_syn_84.ofb`
  - `LUT2` → `down2_overlap_tile_runner_Inst_shell/road_mac_probe_Inst_tile/reg_activation_front_b[10]_syn_2.ofa`

## Path 7: -0.004 ns

- Begin: `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/reg_group_mask_head_reg[1]_syn_14.clk`
- End: `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/road_round_shift_Inst_pre/reg_absolute_reg[35]_syn_2.imf`
- Corner: `slow_m40c`
- Budget: 10.000ns { probe_clk rising@10.000ns - probe_clk rising@0.000ns }
- Data delay: 9.814ns (cell 5.038ns (51%), net 4.776ns (49%))
- Clock skew: 0.076ns
- Logic: 6 ( ADDER=2  LUT5=1  LUT2=1  DSPTADD=1  DSPMULT=1 )
- Max fanout: 38
- Source cone:
  - `../rtl/road_postprocess_stream.v(54)`
  - `../rtl/road_postprocess_stream.v(70)`
  - `../rtl/road_postprocess_stream.v(124)`
  - `../../v7_onchip_chain_20261006/inputs/road_round_shift.v(164)`
  - `../../v7_onchip_chain_20261006/inputs/road_round_shift.v(72)`
- Routed cell sequence:
  - `LUT5` → `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/wire_scalar_extended[0]_syn_2.ofb`
  - `DSPSIOU` → `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/mult0_syn_170.mult_x[0]`
  - `DSPMULT` → `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/mult0_syn_171.p[19]`
  - `DSPSIOU` → `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/mult0_syn_170.cpo[19]`
  - `DSPSIOU` → `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/mult0_syn_265.tadd_c[2]`
  - `DSPTADD` → `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/mult0_syn_360.sum[5]`
  - `DSPSIOU` → `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/mult0_syn_265.p[5]`
  - `ADDER` → `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/road_round_shift_Inst_pre/neg1_syn_172.fco_f`
  - `ADDER` → `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/road_round_shift_Inst_pre/neg1_syn_173.fco_f`
  - `ADDER` → `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/road_round_shift_Inst_pre/neg1_syn_174.fco_f`
  - `ADDER` → `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/road_round_shift_Inst_pre/neg1_syn_175.fco_f`
  - `ADDER` → `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/road_round_shift_Inst_pre/neg1_syn_176.fco_f`
  - `ADDER` → `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/road_round_shift_Inst_pre/neg1_syn_177.fco_f`
  - `ADDER` → `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/road_round_shift_Inst_pre/neg1_syn_178.fco_f`
  - `ADDER` → `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/road_round_shift_Inst_pre/neg1_syn_179.fco_f`
  - `ADDER` → `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/road_round_shift_Inst_pre/neg1_syn_180.fco_f`
  - `ADDER` → `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/road_round_shift_Inst_pre/neg1_syn_181.fco_f`
  - `ADDER` → `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/road_round_shift_Inst_pre/neg1_syn_182.fco`
  - `ADDER` → `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/road_round_shift_Inst_pre/neg1_syn_183.fco`
  - `ADDER` → `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/road_round_shift_Inst_pre/neg1_syn_184.fco`
  - `ADDER` → `down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/road_round_shift_Inst_pre/neg1_syn_185.ofb`
