import_device ph1_35p.db -package PH1P35MDG324 -speed 3
open_project road_rom_current_down2_top.al -single_run
import_db {E:/project/qiansai/anlogic_topic2_work/lab1_sc500_road_vision/cnn/hw_validation/production/reports/load_commit_pipeline_20261014/physical/before_replication.db}
puts "ADVANCE_QUERY_BEGIN"
report_nets [get_nets -hier {u_compute/u_pp/u_pre/u_round/i_advance}] -connection -pin_display_limit 2000
puts "ADVANCE_QUERY_END"
foreach net [get_nets -hier {u_rom/cnt_wait_b_n*}] {
 puts "ROM_QUERY_BEGIN $net"
 report_nets $net -connection -pin_display_limit 2000
 puts "ROM_QUERY_END"
}
close_project
exit
