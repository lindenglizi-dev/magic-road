"""Actual existing VTC+mixer cycle probe, all outputs in this candidate."""
import json
import shutil
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import run

run.check()
work = run.fresh('timing_probe/attempt')
sources = [run.PROJECT / 'user_source/hdl_source/vtc/uivtc.v',
           run.PROJECT / 'user_source/hdl_source/hdmi_mixer.v',
           run.ROOT / 'timing_probe/tb_official_video_budget.v']
before = {str(p): run.sha(p) for p in sources}
run.save(work / 'sources_before.json', before)
snapshot = work / 'inputs'
snapshot.mkdir()
for source in sources:
    shutil.copyfile(source, snapshot / source.name)
run.command([run.MSIM / 'vlib.exe', 'work'], work, 'vlib')
run.command([run.MSIM / 'vlog.exe', '-work', 'work', *sources], work, 'compile')
log = run.command([run.MSIM / 'vsim.exe', '-c', '-t', '1ps', 'work.tb_official_video_budget',
                   '-do', 'onbreak {quit -code 1}; run -all; quit -code 0'], work, 'simulate')
assert 'TB_PASS_OFFICIAL_VIDEO_BUDGET' in log and '** Error:' not in log and '** Fatal:' not in log
assert all(run.sha(p) == digest for p, digest in before.items())
run.save(work / 'receipt.json', {'status': 'PASS', 'source_hashes': before,
    'tools': {str(run.MSIM / (n + '.exe')): run.sha(run.MSIM / (n + '.exe')) for n in ('vlib','vlog','vsim')},
    'metrics': [line for line in log.splitlines() if 'BUDGET' in line],
    'scope': 'actual unchanged official VTC+mixer only; not camera/DDR/HDMI-transmitter or physical timing'})
run.check()
print(work, 'PASS')
