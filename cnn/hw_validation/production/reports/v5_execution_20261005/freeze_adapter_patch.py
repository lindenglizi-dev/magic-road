"""记录项目适配与安装源的完整差分，核对最终 overlay 未漂移。"""
import difflib
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
OVERLAY = HERE.parent.parent / 'checker_overlay'
FROZEN = HERE / 'checker_snapshot_final'
SKILL = Path('C:/Users/lenovo/.codex/skills/readable-verilog-generator')
BEFORE = HERE.parent / 'v5_checker_adapter_20261005/pre_change_overlay'


def main():
    rows, patches, v5_patches = [], [], []
    for path in sorted(FROZEN.rglob('*.py')):
        relative = path.relative_to(FROZEN)
        active, upstream = OVERLAY / relative, SKILL / relative
        content = path.read_bytes()
        assert active.read_bytes() == content, str(relative)
        old = upstream.read_text(encoding='utf-8').splitlines(True) if upstream.exists() else []
        new = path.read_text(encoding='utf-8').splitlines(True)
        patch = ''.join(difflib.unified_diff(old, new, fromfile='installed/' + relative.as_posix(),
                                            tofile='project/' + relative.as_posix()))
        patches.append(patch)
        before = BEFORE / relative
        previous = before.read_text(encoding='utf-8').splitlines(True) if before.exists() else []
        v5_patch = ''.join(difflib.unified_diff(previous, new, fromfile='pre_v5/' + relative.as_posix(),
                                               tofile='v5/' + relative.as_posix()))
        v5_patches.append(v5_patch)
        rows.append({'relative': relative.as_posix(), 'frozen_path': str(path),
                     'sha256': hashlib.sha256(content).hexdigest(),
                     'upstream_sha256': hashlib.sha256(upstream.read_bytes()).hexdigest() if upstream.exists() else None,
                     'changed_from_installed': bool(patch), 'active_equals_frozen': True})
        rows[-1].update({'pre_v5_sha256': hashlib.sha256(before.read_bytes()).hexdigest() if before.exists() else None,
                         'changed_this_v5': bool(v5_patch)})
    (HERE / 'project_adapter.patch').write_text(''.join(patches), encoding='utf-8')
    (HERE / 'v5_only_adapter.patch').write_text(''.join(v5_patches), encoding='utf-8')
    (HERE / 'adapter_sources.json').write_text(json.dumps(rows, indent=2), encoding='utf-8')
    print(json.dumps({'frozen_python_files': len(rows), 'active_equals_frozen': True}))


if __name__ == '__main__':
    main()
