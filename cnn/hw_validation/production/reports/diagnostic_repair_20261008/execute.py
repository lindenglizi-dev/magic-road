"""隔离诊断：拆分源清单、复跑回归；所有输出限定在本目录。"""
from pathlib import Path
import hashlib
import json
import os
import shutil
import subprocess
import sys

HERE = Path(__file__).resolve().parent
REPORTS = HERE.parent
OLD = REPORTS / 'dynamic_control_timing_20261008'
A = REPORTS / 'timing_scope_recheck_20261008'
PROJECT = HERE.parents[4]
SKILL = Path('C:/Users/lenovo/.codex/skills/readable-verilog-generator')
IVERILOG = Path('E:/project/qiansai/.tools/iverilog/bin/iverilog.exe')
VVP = IVERILOG.with_name('vvp.exe')
TD = Path('E:/Anlogic/TD_6.2.1_Engineer_6.2.168.116/bin/td_commands_prompt.exe')
MSIM = Path('D:/modeltech64_2020.4/win64')
CORE = ('road_dynamic_postprocess.v', 'road_dynamic_requant.v',
        'road_round_shift.v', 'silu_shared_unit.v')
MODEL = 'ph1p_logic_eram_runtime_model.v'
TOP = 'road_dynamic_low_io_top.v'


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1048576), b''):
            h.update(chunk)
    return h.hexdigest()


def output(path):
    path = path.resolve()
    if not path.is_relative_to(HERE):
        raise ValueError('Output outside isolated validation directory')
    return path


def write(path, value):
    with output(path).open('x', encoding='utf-8') as f:
        json.dump(value, f, ensure_ascii=False, indent=2)


def check():
    frozen = json.loads((HERE / 'frozen.json').read_text(encoding='utf-8'))
    assert all(Path(p).is_file() and sha(Path(p)) == h for p, h in frozen.items()), 'Old evidence changed'
    print('OLD_FREEZE_PASS', len(frozen), flush=True)


def run(args, cwd, log, stdin=None, allowed=(0,)):
    cwd = output(cwd)
    with output(cwd / log).open('x', encoding='utf-8') as f:
        p = subprocess.run([str(a) for a in args], cwd=cwd, stdout=f,
                           stderr=subprocess.STDOUT, input=stdin, text=True,
                           env={**os.environ, 'PYTHONPATH': str(SKILL)})
    assert p.returncode in allowed, (p.returncode, str(cwd / log))
    return p.returncode


def initialize():
    assert not (HERE / 'frozen.json').exists()
    frozen = json.loads((A / 'frozen_inputs.json').read_text(encoding='utf-8'))
    receipt = json.loads((A / 'delivery_receipt.json').read_text(encoding='utf-8'))
    frozen.update({str(A / p): h for p, h in receipt['artifacts'].items()})
    extras = [A / 'delivery_receipt.json', OLD / 'tb_low_io.v',
              OLD / 'candidate/tb_road_dynamic_postprocess.v',
              OLD / 'candidate/batches.txt', OLD / 'candidate/counts.vh',
              OLD / 'candidate/table.hex', OLD / 'candidate/results.csv',
              OLD / 'shell.contract.json']
    for path in extras:
        frozen[str(path)] = sha(path)
    write(HERE / 'frozen.json', frozen)
    check()
    for folder in ('original_full', 'hardware', 'model', 'candidate/rtl',
                   'baseline_sim', 'candidate_sim', 'gates', 'candidate/physical'):
        (HERE / folder).mkdir(parents=True)
    for p in (A / 'snapshot/rtl').glob('*.v'):
        shutil.copy2(p, HERE / 'original_full' / p.name)
        shutil.copy2(p, HERE / ('model' if p.name == MODEL else 'hardware') / p.name)
        if p.name != MODEL:
            shutil.copy2(p, HERE / 'candidate/rtl' / p.name)
    for folder in ('baseline_sim', 'candidate_sim'):
        for name in ('batches.txt', 'counts.vh', 'table.hex'):
            shutil.copy2(OLD / 'candidate' / name, HERE / folder / name)
        shutil.copy2(OLD / 'candidate/tb_road_dynamic_postprocess.v', HERE / folder / 'tb_road_dynamic_postprocess.v')
        shutil.copy2(OLD / 'tb_low_io.v', HERE / folder / 'tb_low_io.v')
    for name in ('shell.sdc', 'shell.adc'):
        shutil.copy2(A / 'snapshot' / name, HERE / 'candidate/physical' / name)
    write(HERE / 'source_lists.json', {
        'hardware': [TOP, *CORE], 'simulation_only': [MODEL],
        'historical_full_gate': [TOP, *CORE, MODEL],
        'warning': 'Scope separation does not waive model findings or approve hardware delivery',
        'tools': {str(p): sha(p) for p in (IVERILOG, VVP, TD)}})


def gates(candidate=False):
    check()
    cases = [('candidate', HERE / 'candidate/rtl')] if candidate else [
        ('original_full', HERE / 'original_full'), ('hardware', HERE / 'hardware'),
        ('model', HERE / 'model')]
    interface = PROJECT / 'cnn/hw_validation/interfaces/ph1p_eram_interface_complete.v'
    for label, path in cases:
        dest = HERE / 'gates' / label
        dest.mkdir()
        args = [sys.executable, '-B', '-X', 'utf8', '-m',
                'scripts.python.validation.generated_deliverable_gate', path,
                '--json', dest / 'gate.json', '--markdown', dest / 'gate.md']
        if label in ('hardware', 'candidate'):
            assert interface.is_file(), interface
            args += ['--external-interface-source', interface]
        code = run(args, dest, 'gate.log', allowed=(0, 1))
        g = json.loads((dest / 'gate.json').read_text(encoding='utf-8'))
        assert g['checks']['compile']['status'] == 'passed', label
        write(dest / 'receipt.json', {'exit_code': code, 'errors': g['errors'],
              'strict_warnings': g['strict_warnings'],
              'checks': {k: v['status'] for k, v in g['checks'].items()},
              'source_sha256': {p.name: sha(p) for p in path.glob('*.v')},
              'interface_sha256': sha(interface) if label in ('hardware', 'candidate') else None})
        print('STRICT_GATE', label, g['errors'], g['strict_warnings'], flush=True)
    check()


def simulate(candidate=False):
    check()
    directory = HERE / ('candidate_sim' if candidate else 'baseline_sim')
    rtl = HERE / ('candidate/rtl' if candidate else 'hardware')
    sources = [rtl / n for n in CORE] + [HERE / 'model' / MODEL]
    for top, tb in [('tb_road_dynamic_postprocess', directory / 'tb_road_dynamic_postprocess.v'),
                    ('tb_low_io', directory / 'tb_low_io.v')]:
        run([IVERILOG, '-g2001', '-Wall', '-I', directory, '-s', top,
             '-o', directory / (top + '.vvp'), tb, rtl / TOP, *sources],
            directory, top + '_compile.log')
        run([VVP, directory / (top + '.vvp')], directory, top + '.log')
        text = (directory / (top + '.log')).read_text(encoding='utf-8')
        assert 'PASS' in text and 'FATAL' not in text, text
        print(directory.name, text.strip(), flush=True)
    assert (directory / 'results.csv').read_bytes() == (OLD / 'candidate/results.csv').read_bytes()
    write(directory / 'receipt.json', {'status': 'FUNCTION_PASS_NOT_PHYSICAL_SIGNOFF',
          'results_sha256': sha(directory / 'results.csv'),
          'source_sha256': {p.name: sha(p) for p in [rtl / TOP, *sources]},
          'arithmetic_unchanged': all(sha(rtl / n) == sha(HERE / 'hardware' / n) for n in CORE)})
    check()


def modelsim(candidate=False, host=False):
    """Icarus壳编译发生访问异常时，保留失败并用已安装ModelSim独立核对。"""
    check()
    parent = HERE / ('candidate_sim' if candidate else 'baseline_sim')
    directory = parent / ('modelsim_host' if host else 'modelsim')
    directory.mkdir()
    for name in ('batches.txt', 'counts.vh', 'table.hex'):
        shutil.copy2(parent / name, directory / name)
    rtl = HERE / ('candidate/rtl' if candidate else 'hardware')
    sources = [rtl / TOP, *[rtl / n for n in CORE], HERE / 'model' / MODEL]
    run([MSIM / 'vlib.exe', 'work'], directory, 'vlib.log')
    run([MSIM / 'vlog.exe', '-work', 'work', '+incdir+.', *sources,
         parent / 'tb_road_dynamic_postprocess.v', parent / 'tb_low_io.v',
         HERE / 'tb_reset_contract.v'], directory, 'vlog.log')
    for top in ('tb_road_dynamic_postprocess', 'tb_low_io', 'tb_reset_contract'):
        run([MSIM / 'vsim.exe', '-c', '-lib', 'work', top, '-do',
             'onerror {quit -code 1}; onbreak {quit -code 1}; run -all; quit -code 0'],
            directory, top + '.log')
        text = (directory / (top + '.log')).read_text(encoding='utf-8')
        assert 'PASS' in text and 'Fatal:' not in text and '** Error:' not in text, top
        print(parent.name, top, '\n'.join(l for l in text.splitlines() if 'PASS' in l), flush=True)
    assert (directory / 'results.csv').read_bytes() == (OLD / 'candidate/results.csv').read_bytes()
    write(directory / 'receipt.json', {'status': 'MODELSIM_FUNCTION_PASS_NOT_PHYSICAL',
          'results_sha256': sha(directory / 'results.csv'),
          'tool_sha256': {str(MSIM / n): sha(MSIM / n) for n in ('vlib.exe','vlog.exe','vsim.exe')},
          'rtl_sha256': {p.name: sha(p) for p in sources},
          'arithmetic_unchanged': all(sha(rtl / n) == sha(HERE / 'hardware' / n) for n in CORE),
          'no_metastability_proof': True})
    check()


if __name__ == '__main__':
    action = sys.argv[1]
    if action == 'init':
        initialize()
    elif action == 'gates':
        gates()
    elif action == 'candidate-gate':
        gates(True)
    elif action == 'sim':
        simulate()
    elif action == 'candidate-sim':
        simulate(True)
    elif action == 'modelsim':
        modelsim()
    elif action == 'candidate-modelsim':
        modelsim(True)
    elif action == 'modelsim-host':
        modelsim(host=True)
    elif action == 'candidate-modelsim-host':
        modelsim(True, host=True)
    elif action == 'check':
        check()
    else:
        raise ValueError(action)
