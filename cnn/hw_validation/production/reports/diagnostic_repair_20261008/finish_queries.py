"""Read back the existing candidate DB, without rerunning implementation."""
from execute import HERE, TD, check, run

check()
d = HERE / 'candidate/readback'
d.mkdir()
run([TD], d, 'td.log', stdin='source ../../readback.tcl\nexit\n')
assert 'CANDIDATE_READBACK_COMPLETE' in (d/'td.log').read_text(encoding='utf-8')
check()
