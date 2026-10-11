"""冻结本轮实际交付文件索引；不删除历史失败或冒充工具门通过。"""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPORTS = HERE.parent


def main():
    roots = [HERE, REPORTS / 'v5_checker_adapter_20261005', REPORTS / 'v5_remaining_review_20261005',
             REPORTS / 'v5_vendor_regression_20261005',
             REPORTS / 'v5_vendor_regression_fixed_paths_20261005',
             REPORTS / 'v5_vendor_regression_final_traces_20261005',
             REPORTS.parent / 'checker_overlay']
    files = []
    for root in roots:
        for path in sorted(root.rglob('*')):
            # 大型仿真库是可复现缓存，不用二进制缓存冒充源码/结果闭包。
            if not path.is_file() or path.name == 'execution_index.json':
                continue
            if any(part in {'__pycache__', 'old_work', 'candidate_work'} for part in path.parts):
                continue
            files.append({'path': str(path), 'bytes': path.stat().st_size,
                          'sha256': hashlib.sha256(path.read_bytes()).hexdigest()})
    assert files and len({row['path'] for row in files}) == len(files)
    for row in files:
        assert hashlib.sha256(Path(row['path']).read_bytes()).hexdigest() == row['sha256']
    report = {'files': files, 'verified': True,
              'scope': 'Actual v5 evidence and project overlay; excludes binary simulator caches and this index itself',
              'production_rtl_changed': False, 'td_run': False, 'flash_written': False}
    (HERE / 'execution_index.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'files': len(files), 'verified': True}))


if __name__ == '__main__':
    main()
