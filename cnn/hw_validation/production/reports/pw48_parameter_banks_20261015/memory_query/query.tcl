import_device ph1_35p.db -package PH1P35MDG324 -speed 3
open_project road_pw_validation_top.al -single_run
import_db source.db
report_ram_utilization -file ram.rpt
puts "MEMORY_QUERY_DONE"
close_project
exit
