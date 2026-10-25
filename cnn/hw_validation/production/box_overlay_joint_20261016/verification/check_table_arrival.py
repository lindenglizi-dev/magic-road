"""Supplement an existing immutable compile closure with active-video arrival."""
import argparse
from datetime import datetime
from pathlib import Path
import shutil
import sys
import uuid
import zlib

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import run
from verify import warnings


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('compiled_run', type=Path)
    args = parser.parse_args()
    base = args.compiled_run.resolve()
    base.relative_to(ROOT / 'verification/runs')
    run.check()
    work = ROOT / 'verification/runs' / (datetime.now().strftime('%Y%m%d_%H%M%S_') + uuid.uuid4().hex[:8])
    work.mkdir(parents=True)
    shutil.copytree(base / 'work', work / 'work')
    shutil.copytree(base / 'inputs', work / 'inputs')
    shutil.copytree(base / 'artifacts', work / 'artifacts')
    helper = ROOT / 'verification/tb_road_box_table_arrival.v'
    shutil.copyfile(helper, work / helper.name)
    vectors = ROOT / 'reference/vectors'
    boxes = vectors / 'count_64.boxes.hex'
    golden = vectors / 'count_64.rgb24.zlib'
    paths = list((work / 'inputs').iterdir()) + list((work / 'artifacts').iterdir()) + [helper,boxes,golden,Path(__file__).resolve()]
    hashes = {str(path): run.sha(path) for path in paths}
    summary = {'status': 'FAIL', 'compile_base': str(base), 'hashes_before': hashes,
               'tools': {name: run.sha(run.MSIM / (name + '.exe')) for name in ('vlog', 'vsim')}}
    try:
        run.command([run.MSIM / 'vlog.exe', '-work', 'work', work / helper.name], work, 'compile')
        do = work / 'run.do'
        do.write_text('onbreak {quit -code 2}\nonerror {quit -code 2}\nrun -all\nquit -code 0\n', encoding='ascii')
        rgb = work / 'active.rgb24'
        log = run.command([run.MSIM / 'vsim.exe', '-c', '-quiet', '-voptargs=+acc', '-onfinish', 'exit',
                           'work.PH1P_PHY_GSR', 'work.tb_road_box_table_arrival', '+MODE=1', '+COUNT=64', '+AGE_HEX=000000000000007b',
                           '+BOXES=' + boxes.as_posix(), '+RGB=' + rgb.as_posix(), '-do', do], work, 'arrival')
        assert 'TB_PASS_BOX_OVERLAY_JOINT' in log and 'TABLE_ARRIVAL_SOF_PASS' in log
        assert rgb.read_bytes() == zlib.decompress(golden.read_bytes())
        summary.update(status='PASS', warnings=warnings(log), fullframe_bytes=rgb.stat().st_size,
                       rgb_sha256=run.sha(rgb), metrics=[line for line in log.splitlines() if 'ARRIVAL_' in line or 'PASS_BOX' in line])
    finally:
        summary['hashes_after'] = {str(path): run.sha(path) for path in paths}
        summary['source_unchanged'] = summary['hashes_after'] == hashes
        run.save(work / 'summary.json', summary)
        run.check()
        print('SUMMARY=' + str(work / 'summary.json'))
    assert summary['source_unchanged']


if __name__ == '__main__':
    main()
