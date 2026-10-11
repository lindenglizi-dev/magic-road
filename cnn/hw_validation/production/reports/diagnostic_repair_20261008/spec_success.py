import sys
from execute import HERE, TOP, run

d = HERE/'candidate/spec_success'
d.mkdir()
run([sys.executable,'-B','-X','utf8','-m','scripts.python.workflow.cli','write-spec',
     '--spec',HERE/'candidate/shell.contract.json','--out-dir',d,
     '--source',HERE/'candidate/rtl'/TOP,'--language','zh'],HERE,'spec_success.log')
print('CANDIDATE_SPEC_AND_WAVEDROM_PASS')
