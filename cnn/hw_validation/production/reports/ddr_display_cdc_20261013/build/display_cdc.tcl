# Approved bundled-data CDC only. Resolve actual A/B pins, never packed cell names.
# SWUG200 sections 3.11.2/3.11.3: datapath_only includes C2Q/net/setup,
# removes clock jitter/skew/pessimism and automatically cuts matching hold.
proc cdc_q {logical} {
    set net [get_nets -quiet -hier "road_selftest_display_Inst/$logical"]
    if {[llength $net] == 0} {return {}}
    if {[llength $net] != 1} {error "CDC ambiguous net $logical"}
    set outputs [get_pins -of $net -filter {DIRECTION == output} *]
    if {[llength $outputs] != 1} {error "CDC ambiguous driver $logical: $outputs"}
    set ref [get_property REF_NAME $outputs]
    if {$ref != "oqa" && $ref != "oqb" && $ref != "q"} {error "CDC non-register driver $logical $outputs"}
    return $outputs
}
proc cdc_d {q} {
    if {[llength $q] != 1} {error "CDC missing register Q"}
    set cell [get_cells -hier [get_property PARENT_CELL $q]]
    if {[llength $cell] != 1} {error "CDC ambiguous register cell $q"}
    set model [get_property REF_NAME $cell]
    if {$model == "AL_MAP_SEQ" && [get_property REF_NAME $q] == "q"} {
        set pin [get_pins -hier "[get_property NAME $cell].d"]
        if {[llength $pin] != 1} {error "CDC missing logical D $q"}
        return $pin
    }
    if {$model != "PH1P_PHY_LSLICE"} {error "CDC unsupported register $q $model"}
    set attrs [get_property ATTRIBUTES $cell]
    if {[get_property REF_NAME $q] == "oqa"} {
        if {![regexp {REGA_SD = :IMA;} $attrs]} {error "CDC unsupported A input $q $attrs"}
        set pin [get_pins -hier "[get_property NAME $cell].ima"]
    } else {
        if {![regexp {REGB_SD = :IMB;} $attrs]} {error "CDC unsupported B input $q $attrs"}
        set pin [get_pins -hier "[get_property NAME $cell].imb"]
    }
    if {[llength $pin] != 1} {error "CDC missing D $q"}
    return $pin
}
proc cdc_clock {q} {
    set cell [get_property PARENT_CELL $q]
    set pin [get_pins -hier "$cell.clk"]
    if {[llength $pin] != 1} {error "CDC missing clock $q"}
    return $pin
}
set cdc_map [open display_cdc_mapping.tsv w]
set cdc_sdc [open resolved_display.sdc w]
puts $cdc_sdc "# Approved exact first-stage CDC entries and bounded frozen payload; generated from actual pin connectivity."
puts $cdc_map "kind\tlogical\tsource_q\tdestination_d\tdestination_q"
foreach pair {{reg_request reg_request_meta} {reg_acknowledge reg_ack_meta}} {
    lassign $pair source target
    set src [cdc_q $source]
    set target_q [cdc_q $target]
    set dst [cdc_d $target_q]
    if {[get_property NET_NAME $src] != [get_property NET_NAME $dst]} {error "CDC control not direct $pair"}
    puts $cdc_sdc [format {set_false_path -from [get_pins {%s}] -through [get_pins {%s}] -to [get_pins {%s}]} [lindex [cdc_clock $src] 0] [lindex $src 0] [lindex $dst 0]]
    puts $cdc_map "first_stage\t$source->$target\t$src\t$dst\t$target_q"
}
set cdc_payload_count 0
set cdc_unique_pairs {}
set cdc_source_clocks {}
set cdc_source_qs {}
set cdc_destination_ds {}
set cdc_absent_bits {}
for {set bit 0} {$bit < 256} {incr bit} {
    set src [cdc_q [format {reg_hold_payload[%d]} $bit]]
    set target_q [cdc_q [format {o_active_payload[%d]} $bit]]
    if {[llength $src] == 0 && [llength $target_q] == 0} {
        lappend cdc_absent_bits $bit
        continue
    }
    if {[llength $src] != 1 || [llength $target_q] != 1} {error "CDC partial payload bit $bit"}
    set dst [cdc_d $target_q]
    if {[get_property NET_NAME $src] != [get_property NET_NAME $dst]} {error "CDC payload not direct bit $bit"}
    # through Q prevents selecting the unrelated register packed in the same cell.
    set key [list [lindex $src 0] [lindex $dst 0]]
    if {[lsearch -exact $cdc_unique_pairs $key] == -1} {
        lappend cdc_unique_pairs $key
        lappend cdc_source_clocks [lindex [cdc_clock $src] 0]
        lappend cdc_source_qs [lindex $src 0]
        lappend cdc_destination_ds [lindex $dst 0]
        puts $cdc_sdc [format {set_max_delay -from [get_pins {%s}] -through [get_pins {%s}] -to [get_pins {%s}] -datapath_only 7.500} [lindex [cdc_clock $src] 0] [lindex $src 0] [lindex $dst 0]]
    }
    puts $cdc_map "payload\t$bit\t$src\t$dst\t$target_q"
    incr cdc_payload_count
}
puts $cdc_map "absent_constant_bits\t$cdc_absent_bits"
close $cdc_map
close $cdc_sdc
if {$cdc_payload_count == 0} {error "CDC empty payload selection"}
set cdc_expected_absent {}
for {set bit 128} {$bit < 180} {incr bit} {
    if {((0x4444523254455 >> ($bit - 128)) & 1) == 0} {lappend cdc_expected_absent $bit}
}
for {set bit 212} {$bit < 237} {incr bit} {
    if {$bit != 215 && $bit != 216} {lappend cdc_expected_absent $bit}
}
if {$cdc_absent_bits != $cdc_expected_absent} {error "CDC missing bits not explained by constant-zero payload: $cdc_absent_bits"}
if {[llength $cdc_unique_pairs] != 182 && [llength $cdc_unique_pairs] != 199} {error "CDC unexpected payload count"}
puts "CDC_CONSTRAINTS_RESOLVED first_stage=2 payload=$cdc_payload_count unique=[llength $cdc_unique_pairs] absent=[llength $cdc_absent_bits]"
