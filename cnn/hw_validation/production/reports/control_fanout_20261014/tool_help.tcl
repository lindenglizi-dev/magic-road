puts "DB_COMMANDS [info commands *db*]"
puts "HELP_COMMANDS [info commands *help*]"
foreach command_name {phys_opt import_db read_db open_db report_nets} {
    puts "HELP_BEGIN $command_name"
    if {[catch {help $command_name} detail]} {puts "HELP_ERROR $detail"}
    puts "HELP_END $command_name"
}
exit
