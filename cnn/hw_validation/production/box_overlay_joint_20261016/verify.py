"""Run isolated native-DRAM/true-ROM video verification; retain every attempt."""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
import json
from pathlib import Path
import re
import runpy
import shutil
import sys
import uuid
import zlib

import run

ROOT = Path(__file__).resolve().parent
C9 = ROOT.parent / 'result_publish_joint_20261015'
VENDOR = C9 / 'vendor_rom'
DRAM = Path('E:/Anlogic/TD_6.2.1_Engineer_6.2.168.116/sim_release/ph1p/ph1p_logic_dram.v')


def warnings(log):
    found = re.findall(r'^#?\s*\*\* Warning[^\r\n]*', log, re.MULTILINE)
    known = [line for line in found if re.search(
        r'ph1p_logic_(?:eram|dram)\.v\((?:165|225)\): \(vopt-2697\) (?:MSB (?:167999|194623)|LSB (?:167928|194552)) of part-select into .INIT_FILE. is out of bounds', line)]
    unexpected = [line for line in found if line not in known]
    assert not unexpected, unexpected
    return {'known_vendor_init_bounds_count': len(known), 'unexpected': unexpected,
            'status': 'UNRESOLVED_VENDOR_INIT_FILE_BOUNDS'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--case', action='append', default=[])
    parser.add_argument('--protocol-only', action='store_true')
    args = parser.parse_args()
    run.check()
    manifest_path = ROOT / 'reference/vectors/vector_manifest.json'
    if not manifest_path.exists():
        manifest_path = ROOT / 'reference/vectors/vector_manifest.json'
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    cases = [item for item in manifest['cases'] if not args.case or item['name'] in args.case]
    assert cases and (not args.case or len(cases) == len(args.case))
    if not args.case:
        extra = dict(next(item for item in cases if item['name'] == 'live_withdraw'))
        extra.update(name='live_time_invalid_withdraw', invalid_withdraw=1)
        cases.append(extra)
    work = ROOT / 'verification/runs' / (datetime.now().strftime('%Y%m%d_%H%M%S_') + uuid.uuid4().hex[:8])
    work.mkdir(parents=True)
    snapshot = work / 'inputs'
    snapshot.mkdir()
    sources = [VENDOR / 'vendor/ph1p_logic_eram.v', VENDOR / 'vendor/ph1p_phy_gsr.v', DRAM,
               VENDOR / 'rtl/road_yolo_numeric_rom_group.v', VENDOR / 'rtl/road_numeric_rom_reader.v']
    sources += sorted((C9 / 'rtl').glob('*.v'))
    assert len(list((C9 / 'rtl').glob('*.v'))) == 7
    sources += [ROOT.parent / 'source_sof_identity_20261015/rtl/road_age_overlay.v',
                ROOT / 'rtl/road_box_line_overlay.v', ROOT / 'rtl/road_box_age_overlay.v',
                ROOT / 'verification/tb_road_box_overlay_joint.v', ROOT / 'verification/tb_road_box_overlay_protocol.v']
    bound = []
    for index, source in enumerate(sources):
        destination = snapshot / (str(index) + '_' + source.name)
        shutil.copyfile(source, destination)
        bound.append(destination)
    shutil.copytree(VENDOR / 'artifacts', work / 'artifacts')
    assert len(list((work / 'artifacts').glob('group_*_lane_*.dath'))) == 56
    heads = ROOT.parent / 'postprocess_golden_2fps_20261015/artifacts/real_image/heads_cell_order_112.hex'
    watched = sources + list((VENDOR / 'artifacts').iterdir()) + [heads, manifest_path,
                ROOT / 'reference/reference.py', Path(__file__).resolve(), ROOT / 'interfaces.json']
    tool_paths = [run.MSIM / (name + '.exe') for name in ('vlib', 'vlog', 'vsim')] + [Path(sys.executable)]
    watched += tool_paths
    for case in cases:
        watched += [manifest_path.parent / case['boxes_file'], manifest_path.parent / case['rgb_file']]
    before = {str(path): run.sha(path) for path in watched}
    run.save(work / 'hashes_before.json', before)
    run.save(work / 'tool_hashes.json', {str(path): run.sha(path) for path in tool_paths})
    results = []
    summary = {'status': 'FAIL', 'run_root': str(work), 'results': results,
               'raster': 'exact1650x750;blankSOF39970beforeDE;officialVTCnotinstantiated',
               'geometry_age': 'geometry-only age input injected; table kept coherent at2000ms unless expired/invalid case',
               'real_path': 'HEAD112->actual56laneROM->LUT->decodeTopK->NMS->publisher->threeTables->box->frozenAGE',
               'physical_timing_resources_board': 'NOT_RUN'}
    try:
        run.command([run.MSIM / 'vlib.exe', 'work'], work, 'vlib')
        run.command([run.MSIM / 'vlog.exe', '+define+USE_VENDOR_ROM', '-work', 'work', *bound], work, 'compile')
        protocol_do = work / 'protocol.do'
        protocol_do.write_text('onbreak {quit -code 2}\nonerror {quit -code 2}\nrun -all\nquit -code 0\n', encoding='ascii')
        protocol_log = run.command([run.MSIM / 'vsim.exe', '-c', '-quiet', '-voptargs=+acc',
                                  '-onfinish', 'exit', 'work.PH1P_PHY_GSR',
                                  'work.tb_road_box_overlay_protocol', '-do', protocol_do], work, 'protocol')
        assert 'TB_PASS_BOX_OVERLAY_PROTOCOL' in protocol_log
        summary['protocol'] = [line for line in protocol_log.splitlines() if 'PASS' in line]
        summary['protocol_warnings'] = warnings(protocol_log)
        if args.protocol_only:
            cases = []
        def run_case(case):
            name = case['name']
            simdir = work / name
            simdir.mkdir()
            shutil.copytree(work / 'work', simdir / 'work')
            shutil.copytree(work / 'artifacts', simdir / 'artifacts')
            rgb = simdir / 'active.rgb24'
            do = simdir / 'run.do'
            # This file is a generated tool artifact within a fresh simulation directory.
            do.write_text('onbreak {quit -code 2}\nonerror {quit -code 2}\nrun -all\nquit -code 0\n', encoding='ascii')
            plusargs = ['+MODE=' + ('0' if name == 'real7_final97' else '1'),
                        '+COUNT=' + str(case['box_count']), '+AGE_HEX=' + f"{case['age']:016x}",
                        '+BOXES=' + (manifest_path.parent / case['boxes_file']).as_posix(),
                        '+RGB=' + rgb.as_posix(), '+HEAD=' + heads.as_posix(),
                        '+WITHDRAW=' + str(case.get('withdraw_pixel', -1)),
                        '+INVALID_WITHDRAW=' + str(case.get('invalid_withdraw', 0))]
            log = run.command([run.MSIM / 'vsim.exe', '-c', '-quiet', '-voptargs=+acc',
                               '-onfinish', 'exit', '-l', simdir / 'transcript.log', '-wlf', simdir / 'wave.wlf', 'work.PH1P_PHY_GSR',
                               'work.tb_road_box_overlay_joint', *plusargs, '-do', do], simdir, 'vsim')
            assert 'TB_PASS_BOX_OVERLAY_JOINT' in log, name
            assert not re.search(r'\*\* (?:Error|Fatal)|TB_ERROR|Failed to open readmem', log), name
            actual = rgb.read_bytes()
            expected = zlib.decompress((manifest_path.parent / case['rgb_file']).read_bytes())
            if name == 'real7_final97':
                age_match = re.search(r'FRAME_AGE_INPUT age=(\d+) actual_time=(\d+) time_valid=1 injection=0', log)
                assert age_match, 'real time snapshot did not provide frame age'
                reference = runpy.run_path(str(ROOT / 'reference/reference.py'))
                expected = reference['render_frame'](reference['real_entries'](), age=int(age_match[1]), model='direct')
            mismatch = next((index for index, pair in enumerate(zip(actual, expected)) if pair[0] != pair[1]), None)
            item = {'name': name, 'bytes': len(actual), 'expected_bytes': len(expected),
                    'first_mismatch_byte': mismatch, 'rgb_sha256': run.sha(rgb),
                    'passed': actual == expected,
                    'metrics': [line for line in log.splitlines() if 'PASS_' in line or 'REAL_HEAD_' in line or 'FRAME_AGE_INPUT' in line],
                    'warnings': warnings(log)}
            assert item['passed'], item
            print('RGB_FRAME_PASS', name, len(actual), flush=True)
            return item
        # Every worker owns a copied library and ROM working directory.
        if cases:
            with ThreadPoolExecutor(max_workers=3) as pool:
                futures = [pool.submit(run_case, case) for case in cases]
                for future in as_completed(futures):
                    results.append(future.result())
                    run.save(work / 'summary.json', summary)
        summary['status'] = 'PASS'
    except Exception as exc:
        summary['failure'] = repr(exc)
        raise
    finally:
        after = {str(path): run.sha(path) for path in watched}
        run.save(work / 'hashes_after.json', after)
        summary['source_unchanged'] = before == after
        run.save(work / 'summary.json', summary)
        run.check()
        print('SUMMARY=' + str(work / 'summary.json'), flush=True)
    assert summary['source_unchanged']


if __name__ == '__main__':
    main()
