# Read the routed database; never route, export a database, or generate bits.
import_device ph1_35p.db -package PH1P35MDG324 -speed 3
import_db ../physical_attempt2/pr.db
read_sdc ../physical_attempt2/board.sdc
update_timing -mode final
export_sdc -file expanded.sdc
print_sdc_clock_tree
set holds [get_regs -hier {*reg_hold_payload*}]
set active [get_regs -hier {*reg_active_payload*}]
set request [get_regs -hier {*reg_request_reg*}]
set request_meta [get_regs -hier {*reg_request_meta*}]
set ack [get_regs -hier {*reg_acknowledge*}]
set ack_meta [get_regs -hier {*reg_ack_meta*}]
puts "CDC_OBJECT_COUNTS holds=[llength $holds] active=[llength $active] request=[llength $request] request_meta=[llength $request_meta] ack=[llength $ack] ack_meta=[llength $ack_meta]"
report_timing_path -from $holds -to $active -ep_num 1000 -path_num 1 -file cdc_payload.timing
report_timing_path -from $request -to $request_meta -ep_num 100 -path_num 1 -file cdc_request.timing
report_timing_path -from $ack -to $ack_meta -ep_num 100 -path_num 1 -file cdc_ack.timing
report_timing_path -from [get_regs -hier {*reg_pixel_release*}] -to [get_regs -hier {*u_hdmi_tx*}] -ep_num 10000 -path_num 1 -file hdmi_reset.timing
