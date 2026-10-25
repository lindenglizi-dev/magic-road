"""Reuse the frozen verification driver; all writes stay in this candidate."""
import argparse
import importlib.util
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parent
BASE=ROOT.parent/'stem_ddr_down2_four_20261014'
spec=importlib.util.spec_from_file_location('frozen_four_tile_driver',BASE/'run.py')
driver=importlib.util.module_from_spec(spec)
spec.loader.exec_module(driver)
driver.ROOT=ROOT

PROJECT,PREVIOUS,SKILL,MSIM=driver.PROJECT,driver.PREVIOUS,driver.SKILL,driver.MSIM
sha,save,fresh,command,check,timing=driver.sha,driver.save,driver.fresh,driver.command,driver.check,driver.timing


def dependency():
    sys.path.insert(0,str(SKILL))
    import json
    from scripts.python.toolchain.dependency_state import check_dependencies
    result=check_dependencies(json.loads((SKILL/'config/defaults.json').read_text(encoding='utf-8')),
                              state_path=ROOT/'dependency_state.json')
    save(ROOT/'dependency_preflight.json',result)
    assert result['required_ok']
    print('DEPENDENCIES_PASS')


def physical():
    assert not list(ROOT.glob('physical*')),'Only one complete implementation is approved for this candidate'
    driver.physical()


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=('check','dependency','gate','integrated','physical'))
    action=parser.parse_args().action
    if action in ('dependency','physical','check'):
        globals()[action]()
    else:
        getattr(driver,action)()
