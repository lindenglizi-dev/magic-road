"""Reuse bounded tools without writing any frozen candidate."""
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BASE = ROOT.parent / 'detection_table_cdc_20261015'
spec = importlib.util.spec_from_file_location('frozen_table_tools', BASE / 'run.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
PROJECT, SKILL, MSIM = module.PROJECT, module.SKILL, module.MSIM
sha, save, fresh, command, check = module.sha, module.save, module.fresh, module.command, module.check
save.__globals__['ROOT'] = ROOT
dependency = module.dependency
dependency.__globals__['ROOT'] = ROOT

if __name__ == '__main__':
    dependency()
