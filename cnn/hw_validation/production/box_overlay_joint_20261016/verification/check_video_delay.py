"""Narrow independent changing-RGB two-register check, no CNN claim."""
from datetime import datetime
from pathlib import Path
import shutil
import sys
import uuid

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import run
from verify import warnings


def main():
    run.check()
    work = ROOT / 'verification/runs' / (datetime.now().strftime('%Y%m%d_%H%M%S_') + uuid.uuid4().hex[:8])
    work.mkdir(parents=True)
    paths = [Path('E:/Anlogic/TD_6.2.1_Engineer_6.2.168.116/sim_release/ph1p/ph1p_logic_dram.v'),
             ROOT.parent / 'source_sof_identity_20261015/rtl/road_age_overlay.v',
             ROOT / 'rtl/road_box_line_overlay.v', ROOT / 'rtl/road_box_age_overlay.v',
             ROOT / 'verification/tb_road_box_video_delay.v', Path(__file__).resolve()]
    hashes = {str(path): run.sha(path) for path in paths}
    bound = []
    for path in paths:
        copy = work / path.name
        shutil.copyfile(path, copy)
        if path.suffix == '.v':
            bound.append(copy)
    summary = {'status': 'FAIL', 'hashes_before': hashes,
               'tools': {name: run.sha(run.MSIM / (name + '.exe')) for name in ('vlib', 'vlog', 'vsim')}}
    try:
        run.command([run.MSIM / 'vlib.exe', 'work'], work, 'vlib')
        run.command([run.MSIM / 'vlog.exe', '-work', 'work', *bound], work, 'compile')
        do = work / 'run.do'
        do.write_text('onbreak {quit -code 2}\nonerror {quit -code 2}\nrun -all\nquit -code 0\n', encoding='ascii')
        log = run.command([run.MSIM / 'vsim.exe', '-c', '-quiet', '-voptargs=+acc', '-onfinish', 'exit',
                           'work.tb_road_box_video_delay', '-do', do], work, 'video_delay')
        assert 'TB_PASS_BOX_VIDEO_DELAY' in log
        summary.update(status='PASS', warnings=warnings(log))
    finally:
        summary['hashes_after'] = {str(path): run.sha(path) for path in paths}
        summary['source_unchanged'] = summary['hashes_after'] == hashes
        run.save(work / 'summary.json', summary)
        run.check()
        print('SUMMARY=' + str(work / 'summary.json'))
    assert summary['source_unchanged']


if __name__ == '__main__':
    main()
