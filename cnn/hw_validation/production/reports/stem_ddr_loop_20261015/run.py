"""循环调度候选；复用冻结工具，所有产物写入本目录。"""
import argparse
import importlib.util
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
BASE = ROOT.parent / 'stem_ddr_program_banks_20261014'
spec = importlib.util.spec_from_file_location('frozen_four_tile_driver', ROOT.parent / 'stem_ddr_down2_four_20261014/run.py')
driver = importlib.util.module_from_spec(spec)
spec.loader.exec_module(driver)
driver.ROOT = ROOT
PROJECT, PREVIOUS, SKILL, MSIM = driver.PROJECT, driver.PREVIOUS, driver.SKILL, driver.MSIM
sha, save, fresh, command, check, timing = driver.sha, driver.save, driver.fresh, driver.command, driver.check, driver.timing


def dependency():
    import json
    sys.path.insert(0, str(SKILL))
    from scripts.python.toolchain.dependency_state import check_dependencies
    result = check_dependencies(json.loads((SKILL / 'config/defaults.json').read_text(encoding='utf-8')),
                                state_path=ROOT / 'dependency_state.json')
    save(ROOT / 'dependency_preflight.json', result)
    assert result['required_ok']


def integrated():
    import shutil
    check()
    work = fresh('integrated_simulation')
    for path in (ROOT / 'vectors').glob('*.hex'):
        shutil.copyfile(path, work / path.name)
    vendor = Path('E:/Anlogic/TD_6.2.1_Engineer_6.2.168.116/sim_release/ph1p')
    paths = [vendor / 'ph1p_logic_eram.v', vendor / 'ph1p_phy_gsr.v', *sorted((ROOT / 'reused').glob('*.v')),
             ROOT / 'rtl/road_frontend_load_sequence.v', ROOT / 'rtl/road_stem_ddr_sequence.v',
             ROOT / 'rtl/road_paxi_mailbox.v', ROOT / 'tests/tb_stem_ddr_mailbox.v']
    hashes = {str(p): sha(p) for p in paths}
    command([MSIM / 'vlib.exe', 'work'], work, 'vlib')
    command([MSIM / 'vlog.exe', '-work', 'work', '+incdir+' + str(ROOT / 'rtl'), *paths], work, 'vlog')
    results = []
    for mode in (0, 1):
        output = command([MSIM / 'vsim.exe', '-c', '-lib', 'work', 'PH1P_PHY_GSR', 'tb_stem_ddr_mailbox',
                          f'+MODE={mode}', '+VECTORS=' + str(ROOT / 'vectors'), '-do',
                          'onerror {quit -code 1}; onbreak {quit -code 1}; run -all; quit -code 0'], work, f'mode_{mode}')
        assert f'STEM_DDR_MAILBOX_PASS mode={mode} ' in output
        results.append({'mode': mode, 'passed': True, 'lines': [s for s in output.splitlines()
                        if 'INTEGRATED_BIN' in s or 'STEM_DDR_MAILBOX_PASS' in s]})
    save(work / 'receipt.json', {'results': results, 'source_hashes': hashes,
         'scope': 'Actual frozen arithmetic and mailbox, controlled PAXI memory endpoint'})
    assert all(sha(p) == h for p, h in hashes.items())
    check()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('check', 'dependency', 'gate', 'integrated', 'physical'))
    action = parser.parse_args().action
    if action in ('check', 'dependency', 'integrated'):
        globals()[action]()
    else:
        if action == 'physical':
            assert not list(ROOT.glob('physical*')), 'One complete implementation per frozen candidate'
        getattr(driver, action)()
