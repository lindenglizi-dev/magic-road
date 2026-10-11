"""在全新独立库复跑固定官方模型用例，旧失败与旧库保持不变。"""
import hashlib
import json
import shutil
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
FROZEN = HERE.parent / 'v4_silu_regression_20261005'
OUTPUT = HERE.parent / 'v5_vendor_regression_final_traces_20261005'
TOOLS = Path('D:/modeltech64_2020.4/win64')


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    assert not OUTPUT.exists(), 'Use a new run directory, do not overwrite evidence'
    evidence = json.loads((FROZEN / 'evidence.json').read_text(encoding='utf-8-sig'))
    for item in evidence['inputs']:
        assert sha(item['path']) == item['sha256'], item['path']
    OUTPUT.mkdir()
    shutil.copyfile(FROZEN / 'modelsim.ini', OUTPUT / 'modelsim.ini')
    records = []

    def run(name, executable, arguments):
        command = [str(TOOLS / executable), *[str(value).replace('\\', '/') for value in arguments]]
        result = subprocess.run(command, cwd=OUTPUT, capture_output=True, encoding='utf-8',
                                errors='replace', timeout=60)
        (OUTPUT / (name + '_console.log')).write_text(result.stdout + result.stderr, encoding='utf-8')
        records.append({'name': name, 'command': command, 'cwd': str(OUTPUT),
                        'exit': result.returncode, 'tool_sha256': sha(command[0])})
        (OUTPUT / 'commands.json').write_text(json.dumps(records, indent=2), encoding='utf-8')
        assert result.returncode == 0, name

    for library, source_kind in [('old_work', 'original'), ('candidate_work', 'candidate')]:
        run(library + '_create', 'vlib.exe', [OUTPUT / library])
        run(library + '_map', 'vmap.exe', ['-modelsimini', 'modelsim.ini', library, OUTPUT / library])
        sources = [FROZEN / 'vendor_sources/ph1p_logic_eram.v', FROZEN / 'vendor_sources/ph1p_phy_gsr.v',
                   FROZEN / source_kind / 'silu_shared_unit.v', FROZEN / 'tb_silu_vendor_stall.v',
                   FROZEN / 'tb_silu_vendor_contract.v', FROZEN / 'tb_silu_shared_unit.v',
                   FROZEN / 'tb_silu_vendor_random.v']
        run(library + '_compile', 'vlog.exe', ['-modelsimini', 'modelsim.ini',
            '-work', library, '-l', OUTPUT / (library + '_compile.log'), *sources])
    completed_cases = []
    for index, case in enumerate(evidence['cases']):
        name = f'case_{index:02d}'
        if index == 0:
            library, top, arguments = 'old_work', 'tb_silu_vendor_stall', ['+STALL=0']
        elif index == 1:
            library, top, arguments = 'old_work', 'tb_silu_vendor_contract', ['+STALL=1']
        elif index < 6:
            library, top = 'candidate_work', 'tb_silu_vendor_contract'
            arguments = ['+STALL=' + str([1, 16, 32, 64][index - 2])]
        else:
            library, arguments = 'candidate_work', []
            top = 'tb_silu_shared_unit' if index == 6 else 'tb_silu_vendor_random'
        log = OUTPUT / (name + '.log')
        run(name, 'vsim.exe', ['-c', '-modelsimini', 'modelsim.ini', '-l', log.name,
            '-wlf', OUTPUT / (name + '.wlf'), library + '.PH1P_PHY_GSR', library + '.' + top,
            *arguments, '+TRACE=' + name + '.csv', '-do', 'run 2 ms; quit -f'])
        text = log.read_text(encoding='utf-8-sig')
        assert case['marker'] in text, (name, 'missing fixed marker')
        if case['status'] == 'pass':
            assert not any(marker in text for marker in ('TB_ERROR', 'TB_FAIL', 'TB_MISMATCH')), name
        else:
            assert 'RAM output changed on frozen edge' in text
            assert 'raw=4 lookup=513 got=4 expected=2' in text
        assert 'Failed to open file' not in text, (name, 'incomplete trace evidence')
        trace = OUTPUT / (name + '.csv')
        if 1 <= index <= 5:
            assert trace.is_file() and trace.stat().st_size > 0, name
        completed_cases.append({'name': name, 'expected_status': case['status'], 'marker': case['marker'],
                                'log': str(log), 'log_sha256': sha(log), 'new_run': True,
                                'cycle_trace': str(trace) if trace.exists() else None,
                                'cycle_trace_sha256': sha(trace) if trace.exists() else None})
        print(json.dumps({'case': name, 'verified': True, 'status': case['status']}), flush=True)
    report = {'new_run': True, 'cases': completed_cases, 'commands': records,
              'input_closure': evidence['inputs'], 'frozen_source': str(FROZEN),
              'warning': 'Official encrypted INIT_FILE warnings retained; runtime values verified only',
              'td_executed': False, 'production_modified': False}
    (OUTPUT / 'results.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    assert len(completed_cases) == 8


if __name__ == '__main__':
    main()
