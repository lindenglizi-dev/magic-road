"""在工程根目录运行：python sim/test_rotation_format.py。"""
import hashlib
import json
from pathlib import Path
import random
import shutil
import subprocess

root = Path(__file__).resolve().parent.parent
output = root / 'reports/optimized_build'
output.mkdir(parents=True, exist_ok=True)
limit = 65_536_000
mask = (1 << 48) - 1
math_checks = 0


def check(value):
    """直接比较旧64位公式与新定宽表达式。"""
    global math_checks
    bits = value & mask
    magnitude = (-bits) & mask if bits >> 47 else bits
    low = magnitude & ((1 << 26) - 1)
    clipped = magnitude >> 26 != 0 or low >= limit
    product = (low << 6) + (low << 5) + (low << 2)
    assert product < 1 << 33
    candidate = 99_999 if clipped else (product >> 16) & 0x1ffff
    old_scaled = (abs(value) * 100) >> 16
    assert clipped == (old_scaled > 99_999), value
    assert candidate == min(old_scaled, 99_999), value
    math_checks += 1


for digit in range(100_002):
    boundary = (digit * 65_536 + 99) // 100
    for offset in (-1, 0, 1):
        n = max(0, boundary + offset)
        check(n)
        check(-n)
rng = random.Random(20261020)
for _ in range(100_000):
    check(rng.randrange(-(1 << 47), 1 << 47))

values = [0, 1, -1, 655, -655, 656, -656, 65535, -65535, 65536, -65536,
          limit-1, -(limit-1), limit, -limit, limit+1, -(limit+1),
          (1 << 26)-1, -(1 << 26), (1 << 47)-1, -(1 << 47)]
values += [rng.randrange(-(1 << 47), 1 << 47) for _ in range(80)]
values += [rng.randrange(-limit, limit) for _ in range(80)]
rows = []
for index, value in enumerate(values):
    check(value)
    rpm = [0, 1, -1, (1 << 23)-1, -(1 << 23)][index % 5]
    phase = [0, 1, 32768, 65535][index % 4]
    rows.append(f'{value & mask:012x} {rpm & 0xffffff:06x} {phase:04x} '
                f'{(0xffffffff-index):08x} {(index*1234567) & 0xffffffff:08x} '
                f'{index % 8:x} {index % 16:x} {index % 16:x}\n')
# 原reason=15且输入未饱和时，显示溢出必须仍覆盖为14；输入饱和保持15。
rows += [f'{limit:012x} 800000 ffff ffffffff 89abcdef 7 f c\n',
         f'{limit:012x} 800000 ffff ffffffff 89abcdef 7 2 d\n']
(output / 'format_vectors.txt').write_text(''.join(rows), encoding='ascii')
iverilog = shutil.which('iverilog') or 'E:/project/qiansai/.tools/iverilog/bin/iverilog.exe'
vvp = shutil.which('vvp') or str(Path(iverilog).with_name('vvp.exe'))
image = output / 'format_test.vvp'
sources = [str(p) for p in (root / 'rtl').glob('*.v')]
commands = [
    ('compile', [iverilog, '-g2001', '-Wall', '-s', 'tb_ball_rotation_format', '-o', str(image),
                 str(root / 'sim/tb_ball_rotation_format.v'), *sources]),
    ('simulation', [vvp, str(image)]),
]
for name, command in commands:
    result = subprocess.run(command, cwd=root, capture_output=True, text=True, encoding='utf-8', errors='replace')
    log = result.stdout + result.stderr
    (output / f'format_{name}.log').write_text(log, encoding='utf-8')
    if result.returncode:
        print(log)
        result.check_returncode()
    if name == 'simulation':
        assert 'PASS ROTATION FORMAT:' in log, log
        print(log.strip())
(output / 'format_summary.json').write_text(json.dumps({
    'passed': True, 'mathematical_cases': math_checks, 'rtl_numeric_vectors': len(rows),
    'old_formula': 'min(floor(abs(signed48)*100/65536),99999)',
    'saturation_threshold': limit, 'cancellation': ['clear', 'mode', 'epoch', 'disable'],
    'formatter_done_collisions': ['capture', 'scale', 'load'], 'atomic_frame_commit': True,
    'source_hashes': {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
                      for p in [root / 'rtl/ball_runtime.v', root / 'sim/tb_ball_rotation_format.v']},
}, indent=2), encoding='utf-8')
print(f'PASS mathematical equivalence: {math_checks} cases')
