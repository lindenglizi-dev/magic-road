"""沿用已验证的原约束重读流程，只处理本候选路由数据库。"""
import importlib.util
from pathlib import Path

source = Path(__file__).resolve().parent.parent / 'stem_ddr_program_banks_20261014/recheck.py'
spec = importlib.util.spec_from_file_location('frozen_constraint_recheck', source)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

if __name__ == '__main__':
    module.main()
