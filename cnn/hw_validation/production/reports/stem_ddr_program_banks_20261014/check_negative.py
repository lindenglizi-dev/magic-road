"""Prove the RTL word checker rejects a swapped program bank."""
import shutil
import run

run.check()
work=run.fresh('bank_negative')
for path in (run.ROOT/'vectors').glob('*.hex'):
    shutil.copyfile(path,work/path.name)
shutil.copyfile(run.ROOT/'vectors/program_high.hex',work/'program_low.hex')
shutil.copytree(run.ROOT/'bank_simulation/work',work/'work')
output=run.command([run.MSIM/'vsim.exe','-c','-lib','work','PH1P_PHY_GSR','tb_program_banks','-do',
    'onerror {quit -code 1}; onbreak {quit -code 1}; run -all; quit -code 0'],work,'vsim',allowed=(0,1,2))
assert 'BANK_WORD_MISMATCH address=0' in output
run.save(work/'receipt.json',{'passed':True,'expected_failure':'BANK_WORD_MISMATCH address=0',
    'mutation':'Only this isolated copy of program_low.hex was replaced with high bank',
    'real_vectors_unchanged':True})
run.check()
print('BANK_NEGATIVE_PASS swapped bank rejected')
