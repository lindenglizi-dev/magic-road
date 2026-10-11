from execute import HERE, TD, check, run

check()
d = HERE/'candidate/readback_physical'
d.mkdir()
run([TD],d,'td.log',stdin='source ../../readback_physical.tcl\nexit\n')
assert 'CANDIDATE_READBACK_COMPLETE' in (d/'td.log').read_text(encoding='utf-8')
check()
