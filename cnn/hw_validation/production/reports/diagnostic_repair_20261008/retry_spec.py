"""Retry documentation with host file access; keep the original failure log."""
import sys
from execute import HERE, TOP, run

d = HERE/'candidate/spec_retry'
d.mkdir()
run([sys.executable,'-B','-X','utf8','-m','scripts.python.workflow.cli','write-spec',
     '--spec',HERE/'candidate/shell.contract.json','--out-dir',d,
     '--source',HERE/'candidate/rtl'/TOP,'--language','zh'],d,'spec.log')
print('CANDIDATE_SPEC_AND_WAVEDROM_PASS')
