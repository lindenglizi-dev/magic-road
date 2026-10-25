"""复用原数据库约束复核；仅重导报告，不重新布局布线。"""
import importlib.util
from pathlib import Path

source = Path(__file__).resolve().parent.parent / 'stem_ddr_program_banks_20261014/recheck.py'
spec = importlib.util.spec_from_file_location('frozen_constraint_recheck', source)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

if __name__ == '__main__':
    module.main()
