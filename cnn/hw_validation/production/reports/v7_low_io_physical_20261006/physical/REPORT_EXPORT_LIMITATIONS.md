# Report export limitations retained

`report_route_status -drc -file shell_route_status.rpt` executed in the baseline run, but TD 6.2.168116 did not create the requested file. The same behavior occurred for `hold_fix_route_status.rpt` in the candidate. The DRC stages and their results are preserved in `td_20261006_185614.log` and `hold_fix_candidate/td_20261006_191214.log`, including no multi-drive, clock-net status, passed bound/sigmap/self-driven checks, PHY-1035/1039 warnings, and the PHY-5089 abnormal-path warning.

The missing standalone files are treated as an export limitation, not as proof that DRC passed without warnings and not as a reason to rerun or relax constraints.

