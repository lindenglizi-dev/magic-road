foreach command {import_db read_db derive_clocks report_timing_path get_clocks report_clock_summary create_generated_clock} {
    puts "AUDIT_HELP $command"
    catch {help $command} result
    puts $result
}
