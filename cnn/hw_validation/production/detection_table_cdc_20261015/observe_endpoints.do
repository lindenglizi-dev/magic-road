onerror {quit -code 1}
onbreak {quit -code 1}
vcd file endpoints.vcd
vcd add /tb_road_detection_table_cdc/i_src_clk
vcd add /tb_road_detection_table_cdc/i_src_entry_valid
vcd add /tb_road_detection_table_cdc/o_src_entry_ready_500
vcd add /tb_road_detection_table_cdc/i_src_meta_valid
vcd add /tb_road_detection_table_cdc/i_src_metadata
vcd add /tb_road_detection_table_cdc/o_src_meta_ready_500
vcd add /tb_road_detection_table_cdc/o_src_copy_ack_500
vcd add /tb_road_detection_table_cdc/o_dst_copy_busy_500
vcd add /tb_road_detection_table_cdc/o_dst_pending_valid_500
vcd add /tb_road_detection_table_cdc/o_dst_update_500
run -all
vcd flush
quit -code 0
