"""运行两个工作副本的独立 RTL 回归，并汇总当前工具与源码指纹。"""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import time


ROOT = Path(__file__).resolve().parent


def main():
    reports = ROOT / 'reports'
    reports.mkdir(exist_ok=True)
    result = {
        'time_utc': datetime.now(timezone.utc).isoformat(),
        'scope': 'standalone RTL only; not Croc CPU system or ASIC signoff',
        'python': sys.version,
        'tools': {name: shutil.which(name) for name in ('iverilog', 'vvp', 'verilator', 'yosys')},
        'checks': {},
    }
    for name in ('transformer', 'croc'):
        project = ROOT / 'projects' / name
        command = [sys.executable, str(project / 'scripts' / 'validate.py'), '--strict']
        started = time.time()
        print(f'Running {name}: {" ".join(command)}', flush=True)
        try:
            completed = subprocess.run(command, cwd=project, text=True,
                                       encoding='utf-8', errors='replace',
                                       capture_output=True, timeout=900)
            output = completed.stdout + completed.stderr
            summary_path = project / 'reports' / 'summary.json'
            summary = json.loads(summary_path.read_text(encoding='utf-8')) if summary_path.exists() else {}
            current = summary_path.exists() and summary_path.stat().st_mtime >= started
            passed = completed.returncode == 0 and current and summary.get('gate') == 'RTL_PASS'
            result['checks'][name] = {
                'status': 'PASS' if passed else 'FAIL',
                'returncode': completed.returncode,
                'current_summary': current,
                'summary': str(summary_path.relative_to(ROOT)),
                'elapsed_seconds': round(time.time() - started, 2),
            }
        except (OSError, subprocess.TimeoutExpired, ValueError) as error:
            output = str(error)
            result['checks'][name] = {'status': 'FAIL', 'error': str(error)}
        (reports / f'{name}.log').write_text(output, encoding='utf-8')
        print(f'{name}: {result["checks"][name]["status"]}', flush=True)

    result['source_sha256'] = {
        str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted((ROOT / 'projects').rglob('*'))
        if path.is_file() and path.suffix in ('.sv', '.py', '.hex', '.npz', '.txt')
        and not {'reports', '__pycache__'}.intersection(path.relative_to(ROOT).parts)
    }
    result['gate'] = 'RTL_PASS' if all(check['status'] == 'PASS' for check in result['checks'].values()) else 'FAIL'
    (reports / 'local_checks.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'FINAL: {result["gate"]}; reports/local_checks.json', flush=True)
    return 0 if result['gate'] == 'RTL_PASS' else 1


if __name__ == '__main__':
    raise SystemExit(main())
