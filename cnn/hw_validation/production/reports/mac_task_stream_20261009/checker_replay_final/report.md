# Project checker overlay strict replay

> Snapshot warning: this run is bound to the SHA-256-identified files currently under
> `gates_attempt3/baseline` and `gates_attempt3/candidate`. This replay is bound to the
> selected same-attempt original/fixed pair; it is not a strict delivery or deployment
> release while findings remain.

Pair binding: `baseline` is the original closure and `candidate` is the fixed closure
from the same `gates_attempt3` snapshot. Both copied closures contain the same eight RTL roots,
and their identical PH1P source is supplied only as an external interface.

The replay used copied closures under this directory, excluded PH1P from ordinary roots,
and supplied it only through the registered `--external-interface-source` option.
No RTL, checker, original report, TD, training, synthesis, or board state was modified.

## Results

| mode | raw errors | replay errors | delta | ready |
| --- | ---: | ---: | ---: | --- |
| baseline | 5249 | 4808 | -441 | False |
| candidate | 5416 | 4975 | -441 | False |

## Remaining categories

### baseline

- `width_and_arithmetic`: VG085=11, VG097=2, VG122=48, VG125=110, VG137=1, VG138=80
- `driver_and_feedback`: VG136=2, VG153=33
- `state_contract`: VG144=1
- `source_and_operation_budget`: VG145=64, VG146=831, VG147=553
- `format_comment_naming`: VG004=408, VG007=16, VG013=59, VG015=183, VG040=611, VG060=26, VG061=49, VG062=693, VG063=13, VG064=135, VG067=1, VG068=8, VG070=4, VG156=4, VG157=2

### candidate

- `width_and_arithmetic`: VG085=11, VG097=2, VG122=58, VG125=122, VG137=1, VG138=80
- `driver_and_feedback`: VG136=2, VG153=35
- `state_contract`: VG144=1
- `source_and_operation_budget`: VG145=81, VG146=850, VG147=587
- `format_comment_naming`: VG004=408, VG007=16, VG013=63, VG015=187, VG040=628, VG060=25, VG061=58, VG062=706, VG063=13, VG064=135, VG067=1, VG068=8, VG070=3, VG156=4, VG157=2

## Representative remaining findings

- `VG085`: `down2_dynamic_tile_runner.v:305` `i_load_addr == cnt_expected_dw_cache`; `down2_dynamic_tile_runner.v:381` `spatial_lane < wire_dw_post_count`; `down2_dynamic_tile_runner.v:432` `1'b1 == wire_dw_post_count`
- `VG097`: `down2_dynamic_tile_runner.v:903` `road_down2_dynamic_adapter.i_post_multiplier port_width=32 signal_width=1 expression=reg_post_multiplier[flag_layer_pw]`; `down2_dynamic_tile_runner.v:903` `road_down2_dynamic_adapter.i_post_shift port_width=6 signal_width=1 expression=reg_post_shift[flag_layer_pw]`
- `VG122`: `down2_dynamic_tile_runner.v:294` `assign wire_parameter_beta = wire_parameter_base + 6'd1;`; `down2_dynamic_tile_runner.v:295` `assign wire_parameter_gamma = wire_parameter_base + 6'd2;`; `down2_dynamic_tile_runner.v:464` `ptr_pw_meta_write <= ptr_pw_meta_write + 2'd1;`
- `VG136`: `down2_dynamic_tile_runner.v:221` `lane_index`; `road_dynamic_postprocess.v:129` `check_lane`
- `VG144`: `down2_dynamic_tile_runner.v:57` `missing current/next state roles`
- `VG145`: `down2_dynamic_tile_runner.v:261` `flag_can_reserve: 11 sources: cnt_pw_meta, flag_busy_o, flag_layer_pw, flag_result_reserved, mac_fault, mac_result_valid, pp_fault, pp_input_ready, pp_result_queue_count, pp_table_loaded, state_current`; `down2_dynamic_tile_runner.v:412` `flag_cnt_output_clear: 31 sources: cnt_dw_post_lane, cnt_dw_writes, cnt_mac_group, cnt_output, cnt_position, cnt_position[1:0], cnt_pw_meta, flag_busy_o, flag_control_loaded, flag_dw_bias_loaded, flag_dw_cache_loaded, flag_dw_weight_loaded, flag_fault_o, flag_halo_loaded, flag_layer_pw, flag_load_fault, flag_multiplier_loaded, flag_pw_bias_loaded, flag_pw_weight_loaded, flag_result_reserved, i_pw_only, i_start, i_table_valid, mac_fault, mac_input_ready, mac_result_valid, pp_fault, pp_input_ready, pp_result_queue_count, pp_table_loaded, state_current`; `down2_dynamic_tile_runner.v:412` `flag_cnt_output_increment: 18 sources: cnt_dw_post_lane, cnt_mac_group, cnt_output, cnt_position[1:0], cnt_pw_meta, flag_busy_o, flag_fault_o, flag_layer_pw, flag_load_fault, flag_result_reserved, mac_fault, mac_input_ready, mac_result_valid, pp_fault, pp_input_ready, pp_result_queue_count, pp_table_loaded, state_current`
- `VG146`: `down2_dynamic_tile_runner.v:4` `definition_root=down2_dynamic_tile_runner.v:down2_dynamic_tile_runner@4:1-941:1; instance_path=down2_dynamic_tile_runner; specialization=e3e89a18fd51dac5e8d6ca0584662fe34717775d32ec1f24f2aaa403ea511818; target=flag_debug_layer_o$D; child_output=down2_dynamic_tile_runner.flag_debug_layer_o$D; operation_count=0; limit=3; inconclusive_reason=unknown output driver; loop_presence=unknown`; `down2_dynamic_tile_runner.v:4` `definition_root=down2_dynamic_tile_runner.v:down2_dynamic_tile_runner@4:1-941:1; instance_path=down2_dynamic_tile_runner; specialization=e3e89a18fd51dac5e8d6ca0584662fe34717775d32ec1f24f2aaa403ea511818; target=pp_meta_count[0]; child_output=down2_dynamic_tile_runner.pp_meta_count[0]; operation_count=0; limit=3; inconclusive_reason=unknown output driver; loop_presence=unknown`; `down2_dynamic_tile_runner.v:4` `definition_root=down2_dynamic_tile_runner.v:down2_dynamic_tile_runner@4:1-941:1; instance_path=down2_dynamic_tile_runner; specialization=e3e89a18fd51dac5e8d6ca0584662fe34717775d32ec1f24f2aaa403ea511818; target=pp_meta_count[1]; child_output=down2_dynamic_tile_runner.pp_meta_count[1]; operation_count=0; limit=3; inconclusive_reason=unknown output driver; loop_presence=unknown`
- `VG147`: `down2_dynamic_tile_runner.v:4` `definition_root=down2_dynamic_tile_runner.v:down2_dynamic_tile_runner@4:1-941:1; instance_path=down2_dynamic_tile_runner; specialization=e3e89a18fd51dac5e8d6ca0584662fe34717775d32ec1f24f2aaa403ea511818; target=cnt_core_cycles$enable; child_output=down2_dynamic_tile_runner/road_postprocess_stream_Inst_tile/u_chain.cnt_core_cycles$enable; operation_count=19; limit=3; inconclusive_reason=unknown output driver; loop_presence=present`; `down2_dynamic_tile_runner.v:4` `definition_root=down2_dynamic_tile_runner.v:down2_dynamic_tile_runner@4:1-941:1; instance_path=down2_dynamic_tile_runner; specialization=e3e89a18fd51dac5e8d6ca0584662fe34717775d32ec1f24f2aaa403ea511818; target=cnt_dw_post_lane$enable; child_output=down2_dynamic_tile_runner/road_postprocess_stream_Inst_tile/u_chain.cnt_dw_post_lane$enable; operation_count=59; limit=3; inconclusive_reason=unknown output driver; loop_presence=present`; `down2_dynamic_tile_runner.v:4` `definition_root=down2_dynamic_tile_runner.v:down2_dynamic_tile_runner@4:1-941:1; instance_path=down2_dynamic_tile_runner; specialization=e3e89a18fd51dac5e8d6ca0584662fe34717775d32ec1f24f2aaa403ea511818; target=cnt_dw_writes$enable; child_output=down2_dynamic_tile_runner/road_postprocess_stream_Inst_tile/u_chain.cnt_dw_writes$enable; operation_count=62; limit=3; inconclusive_reason=unknown output driver; loop_presence=present`
- `VG153`: `down2_dynamic_tile_runner.v:68` `reg_halo`; `down2_dynamic_tile_runner.v:69` `reg_dw_cache`; `down2_dynamic_tile_runner.v:70` `reg_output_cache`

## Checker and regression evidence

- Existing `run_project_gate.py::regress(output)` reused: `True`.
- Imported module origins and SHA-256 values come from `checker_replay\regression\receipt.json` (`09d166fafa947a7c71bfcaaed062c6d9d0a0afcd445fda07618c2d97f8c09e5e`).
- Full raw/replay rule deltas, commands, input hashes, overlay hashes, and public matrices
  are recorded in `report.json` and `commands.json`.
- Gate return code 1 is expected while strict findings remain; report publication and
  regression worker must return usable evidence.
