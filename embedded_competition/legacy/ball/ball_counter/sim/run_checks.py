"""运行多球计数和像素链路检查。需要Python 3.10及Icarus Verilog。"""
from pathlib import Path
import os
import shutil
import subprocess
import sys
import time

root = Path(__file__).resolve().parents[1]
compiler = shutil.which('iverilog')
runtime = shutil.which('vvp')
if not compiler or not runtime:
    sys.exit('请将 Icarus Verilog 的 bin 目录加入 PATH。')
work = root / 'build' / ('sim_' + time.strftime('%Y%m%d_%H%M%S'))
(work / 'sim').mkdir(parents=True)
(work / 'reports').mkdir()
for name in ('test_multi.py', 'tb_ball_multi.v', 'tb_ball_multi_runtime.v'):
    shutil.copy2(root / 'sim' / name, work / 'sim' / name)
shutil.copy2(root / 'multi_model.py', work / 'multi_model.py')
environment = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
subprocess.run([sys.executable, str(work / 'sim/test_multi.py')], cwd=work, env=environment, check=True)
sources = [str(path) for path in sorted((root / 'rtl').glob('*.v'))]
for top in ('tb_ball_multi', 'tb_ball_multi_runtime'):
    output = work / (top + '.vvp')
    with (work / (top + '_compile.log')).open('w') as log:
        subprocess.run([compiler, '-g2005', '-s', top, '-o', str(output), str(work / 'sim' / (top + '.v')), *sources], cwd=work, stdout=log, stderr=subprocess.STDOUT, check=True)
    result = subprocess.run([runtime, str(output)], cwd=work, capture_output=True, text=True, check=True)
    (work / (top + '_result.log')).write_text(result.stdout + result.stderr, encoding='utf-8')
    print(result.stdout, end='')
print('检查完成，输出目录：', work)
