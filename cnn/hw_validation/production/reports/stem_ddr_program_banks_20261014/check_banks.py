"""Full ROM and frozen regression checks, no synthesis or board access."""
import difflib
import json
from pathlib import Path
import shutil
import sys

import run

ROOT,BASE=run.ROOT,run.BASE
run.check()
words=(ROOT/'vectors/program.hex').read_text(encoding='ascii').splitlines()
low=(ROOT/'vectors/program_low.hex').read_text(encoding='ascii').splitlines()
high=(ROOT/'vectors/program_high.hex').read_text(encoding='ascii').splitlines()
assert len(low)==len(high)==4096 and low+high==words
work=run.fresh('bank_simulation')
for path in (ROOT/'vectors').glob('*.hex'):
    shutil.copyfile(path,work/path.name)
vendor=Path('E:/Anlogic/TD_6.2.1_Engineer_6.2.168.116/sim_release/ph1p')
sources=[vendor/'ph1p_logic_eram.v',vendor/'ph1p_phy_gsr.v',*sorted((ROOT/'reused').glob('*.v')),
         ROOT/'rtl/road_stem_ddr_sequence.v',ROOT/'tests/tb_program_banks.v']
run.command([run.MSIM/'vlib.exe','work'],work,'vlib')
run.command([run.MSIM/'vlog.exe','-work','work','+incdir+'+str(ROOT/'rtl'),*sources],work,'vlog')
output=run.command([run.MSIM/'vsim.exe','-c','-lib','work','PH1P_PHY_GSR','tb_program_banks','-do',
    'onerror {quit -code 1}; onbreak {quit -code 1}; run -all; quit -code 0'],work,'vsim',allowed=(0,1,2))
assert 'PROGRAM_BANKS_PASS words=8192 hold_checks=16384 latency_change=0' in output
run.save(work/'receipt.json',{'passed':True,'words':8192,'hold_checks':16384,'latency_change':0,
    'source_hashes':{str(p):run.sha(p) for p in sources}})
before=(BASE/'rtl/road_stem_ddr_sequence.v').read_text(encoding='utf-8')
after=(ROOT/'rtl/road_stem_ddr_sequence.v').read_text(encoding='utf-8')
(ROOT/'source_diff.patch').write_text(''.join(difflib.unified_diff(before.splitlines(True),after.splitlines(True),
    fromfile='frozen_four_tile/road_stem_ddr_sequence.v',tofile='explicit_banks/road_stem_ddr_sequence.v')),encoding='utf-8')
run.command([sys.executable,'-B','-X','utf8',ROOT/'sequence_verification/run_verify.py'],ROOT,'direct_regression')
manifest=json.loads((ROOT/'sequence_verification/receipts/manifest.json').read_text(encoding='utf-8'))
baseline=json.loads((BASE/'sequence_verification/receipts/manifest.json').read_text(encoding='utf-8'))
assert manifest['case_cycles']==baseline['case_cycles'],(manifest['case_cycles'],baseline['case_cycles'])
run.save(ROOT/'functional_comparison.json',{'passed':True,'all_13_case_cycles_identical':True,
    'case_cycles':manifest['case_cycles'],'program_sha256':run.sha(ROOT/'vectors/program.hex'),
    'baseline_program_sha256':run.sha(BASE/'vectors/program.hex'),'changed_rtl_sha256':run.sha(ROOT/'rtl/road_stem_ddr_sequence.v')})
run.check()
print('BANK_AND_13_CASES_PASS; all case cycles identical')
