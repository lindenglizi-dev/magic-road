
import_device ph1_35p.db -package PH1P35MDG324 -speed 3
import_db $::env(RX_AUDIT_DB)
write_verilog $::env(RX_AUDIT_NETLIST) -implement
exit
