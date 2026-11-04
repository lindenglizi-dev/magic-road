"""比较冻结原版与时钟使能版；复用摄像头完整开漏功能测试。"""
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess

root = Path(__file__).resolve().parent.parent
output = root / 'reports/optimized_build'
baseline = output / 'before/uii2c.v'
assert baseline.is_file(), baseline
current = root / 'user_source/hdl_source/uics500_cfg/uii2c.v'
config_dir = root / 'user_source/hdl_source/uics520_cfg'
reference = output / 'i2c_reference.v'
source = baseline.read_bytes()
renamed, count = re.subn(rb'\bmodule\s+uii2c\b', b'module uii2c_reference', source)
assert count == 1
reference.write_bytes(renamed)
reference_config = output / 'i2c_reference_config.v'
renamed_config, count = re.subn(rb'\buii2c\s*#\s*\(', b'uii2c_reference #(',
                              (config_dir / 'uicfgcs520.v').read_bytes())
assert count == 1
reference_config.write_bytes(renamed_config)
iverilog = shutil.which('iverilog') or 'E:/project/qiansai/.tools/iverilog/bin/iverilog.exe'
vvp = shutil.which('vvp') or str(Path(iverilog).with_name('vvp.exe'))
tables = [config_dir / name for name in ('uics520reg_720p60.v', 'SC520GainTbl.v', 'uics520regAE.v')]
wrapper = root / 'sim/tb_ball_i2c_equivalence.v'
original_bench = root / 'sim/tb_ball_camera_i2c.v'


def run(command, name):
    result = subprocess.run(command, cwd=root, capture_output=True, text=True,
                            encoding='utf-8', errors='replace', timeout=180)
    log = result.stdout + result.stderr
    (output / f'{name}.log').write_text(log, encoding='utf-8')
    if result.returncode:
        print(log)
        result.check_returncode()
    return log


def read_trace(path):
    events, pulses, starts = [], [], []
    for line in path.read_text(encoding='ascii').splitlines():
        fields = line.split()
        if fields[0] == 'P':
            pulses.append((int(fields[1]), int(fields[2])))
        else:
            events.append(tuple(fields[:-1]))
            if fields[0] == 'S':
                starts.append(int(fields[-1]))
    return events, pulses, starts


checks = []
for divider in (8, 237):
    for reset_stress in (0, 1):
        traces = []
        for variant in ('reference', 'candidate'):
            stem = f'i2c_{variant}_div{divider}_reset{reset_stress}'
            image = output / f'{stem}.vvp'
            sources = [reference, reference_config] if variant == 'reference' else [current, config_dir / 'uicfgcs520.v']
            run([iverilog, '-g2001', '-Wall', '-s', 'tb_ball_i2c_equivalence',
                 f'-Ptb_ball_i2c_equivalence.CLK_DIV={divider}',
                 f'-Ptb_ball_i2c_equivalence.RESET_STRESS={reset_stress}',
                 '-o', str(image), str(wrapper), str(original_bench), *map(str, sources + tables)], stem + '_compile')
            trace = output / f'{stem}_trace.txt'
            log = run([vvp, str(image), '+TRACE=' + str(trace)], stem + '_simulation')
            assert 'PASS camera I2C:' in log, log
            if reset_stress:
                assert 'PASS I2C RESET STRESS:' in log, log
            traces.append(read_trace(trace))
        old, new = traces
        assert old[0] == new[0], (divider, reset_stress, 'START/STOP/byte/ACK/NACK/reset sequence differs')
        assert old[1] == new[1], (divider, reset_stress, 'SCL pulse widths differ')
        # trace的%t单位为ps；每个SCL完整周期为2*(CLK_DIV//2+1)个10ns系统周期。
        period_ps = 2 * (divider // 2 + 1) * 10_000
        start_delta = max(abs(a-b) for a, b in zip(old[2], new[2]))
        assert start_delta <= period_ps, (divider, reset_stress, 'transaction starts shifted beyond one I2C cycle', start_delta)
        row = {'divider': divider, 'reset_stress': bool(reset_stress),
               'events': len(old[0]), 'full_scl_pulses': len(old[1]),
               'bytes_and_ack': sum(e[0] == 'B' for e in old[0]), 'max_start_delta_ps': start_delta}
        checks.append(row)
        print('PASS I2C equivalence', row, flush=True)
(output / 'i2c_equivalence_summary.json').write_text(json.dumps({
    'passed': True, 'checks': checks,
    'baseline_sha256': hashlib.sha256(source).hexdigest(),
    'candidate_sha256': hashlib.sha256(current.read_bytes()).hexdigest(),
    'reused_functional_bench': str(original_bench),
}, indent=2), encoding='utf-8')
