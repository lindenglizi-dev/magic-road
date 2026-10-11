"""独立进程复核适配正负例，保存实际输出和源码哈希。"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
TEST = HERE.parent / 'v5_checker_adapter_20261005/test_v5_checker_adapter.py'
SKILL = 'C:/Users/lenovo/.codex/skills/readable-verilog-generator'


def main():
    test_hash = hashlib.sha256(TEST.read_bytes()).hexdigest()
    overlay = HERE / 'checker_snapshot_final'
    assert overlay.is_dir()
    code = (f'import sys,runpy; sys.path[:0]=[{str(overlay)!r},{SKILL!r}]; '
            f'sys.argv=[{TEST.name!r}]; runpy.run_path({str(TEST)!r},run_name="__main__")')
    command = [sys.executable, '-B', '-X', 'utf8', '-c', code]
    result = subprocess.run(command, cwd=HERE, capture_output=True, encoding='utf-8', timeout=60)
    (HERE / 'main_adapter_recheck.log').write_text(result.stdout + result.stderr, encoding='utf-8')
    report = {'command': command, 'cwd': str(HERE), 'exit': result.returncode,
              'test_source': str(TEST), 'test_sha256': test_hash, 'overlay': str(overlay),
              'test_unchanged_during_run': hashlib.sha256(TEST.read_bytes()).hexdigest() == test_hash}
    (HERE / 'main_adapter_recheck.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    assert result.returncode == 0 and report['test_unchanged_during_run']
    print(result.stderr)


if __name__ == '__main__':
    main()
