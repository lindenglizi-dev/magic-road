"""完整前三层DDR验证；输出限定本目录，复用已冻结工具。"""
import argparse
import importlib.util
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
BASE = ROOT.parent / 'stem_ddr_loop_20261015'
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


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('check', 'dependency', 'gate', 'physical'))
    action = parser.parse_args().action
    if action in ('check', 'dependency'):
        globals()[action]()
    else:
        if action == 'physical':
            assert not list(ROOT.glob('physical*')), 'One complete implementation per frozen candidate'
        getattr(driver, action)()
