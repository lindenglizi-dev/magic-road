# Read-only query of the imported frozen gate DB's effective route defaults.
import_device ph1_35p.db -package PH1P35MDG324 -speed 3
import_db gate.db
report_param -detail -stage route -file route_params_imported_default.rpt
set_param route fix_hold on
report_param -detail -stage route -file route_params_after_on.rpt
