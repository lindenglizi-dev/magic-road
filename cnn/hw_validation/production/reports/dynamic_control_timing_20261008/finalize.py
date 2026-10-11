"""Bind measured results, physical inputs and unchanged earlier versions."""
import json
import re
from prepare import HERE, check, sha

def tokens(text):
    return re.sub(r'\s+', '', re.sub(r'//[^\n]*|/\*.*?\*/','',text,flags=re.S))

def main():
    check()
    assert (HERE/'baseline/results.csv').read_bytes()==(HERE/'candidate/results.csv').read_bytes()
    assert (HERE/'baseline/batch_cycles.csv').read_bytes()==(HERE/'candidate/batch_cycles.csv').read_bytes()
    assert len((HERE/'candidate/results.csv').read_text().splitlines())==604
    assert len((HERE/'candidate/batch_cycles.csv').read_text().splitlines())==330
    shell=(HERE/'road_dynamic_low_io_top.v').read_text(encoding='utf-8')
    for which in ('baseline','candidate'):
        folder=HERE/which
        assert tokens(shell)==tokens((folder/'physical/road_dynamic_low_io_top.v').read_text(encoding='utf-8'))
        for name in ('road_dynamic_requant.v','road_round_shift.v','silu_shared_unit.v'):
            assert sha(folder/'rtl'/name)==sha(HERE/'baseline/rtl'/name)
        bound=json.loads((folder/'physical/input_hashes.json').read_text(encoding='utf-8'))
        for path,digest in bound.items():
            assert sha(folder/path)==digest,(which,path)
        log=(folder/'physical/td_actual.log').read_text(encoding='utf-8')
        assert 'No multi-drive.' in log
        timing=(folder/'physical/check_timing_verbose.rpt').read_text(encoding='utf-8')
        assert 'There are 0 combinational loops.' in timing
    hashes={p.relative_to(HERE).as_posix():sha(p) for p in HERE.rglob('*') if p.is_file()
            and p.name!='execution_receipt.json' and '__pycache__' not in p.parts}
    receipt={'status':'TASKS_1_4_DIAGNOSTIC_COMPLETE_NOT_PRODUCTION_READY',
             'old_frozen_files':228,'identical_outputs':604,'identical_individual_cycle_windows':330,
             'core_cycle_total':15388,'shell_test_total':46151,
             'shell_whitespace_only_after_physical_build':True,
             'frozen_arithmetic_byte_identical':True,
             'no_mac_ii_reset_numerical_interface_changes':True,
             'strict_failed':True,'external_and_reset_entry_signoff':False,
             'hashes':hashes}
    (HERE/'execution_receipt.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2),encoding='utf-8')
    print('FINAL_BIND_PASS',len(hashes),'files, 330 cycle windows, 604 outputs')

if __name__=='__main__': main()
