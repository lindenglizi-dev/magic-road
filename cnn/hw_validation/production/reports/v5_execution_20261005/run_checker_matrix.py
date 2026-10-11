"""独立进程加载旧或工程内新检查器，保留完整严格门和差异。"""
import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
SKILL = Path('C:/Users/lenovo/.codex/skills/readable-verilog-generator')
OVERLAY = ROOT / 'checker_overlay'
SPEC = ROOT / 'reports/v3_silu_stall_candidate_20261005/silu_shared_unit_spec_input.json'
INTERFACE = ROOT.parent / 'interfaces/ph1p_eram_interface_complete.v'
TARGETS = {'original': ROOT / 'silu/silu_shared_unit.v',
           'candidate': ROOT / 'reports/v3_silu_stall_candidate_20261005/silu_shared_unit.v'}


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def worker(mode, variant, output, overlay):
    sys.path[:0] = ([str(overlay)] if mode == 'new' else []) + [str(SKILL)]
    from scripts.python.validation.generated_deliverable_gate import main
    # 同源参数、规格、严格默认、纯接口文件；不删除任何报告项。
    sys.argv = ['generated_deliverable_gate', str(TARGETS[variant]), '--spec', str(SPEC),
                '--external-interface-source', str(INTERFACE),
                '--json', str(output / 'gate.json'), '--markdown', str(output / 'gate.md')]
    try:
        gate_exit = main()
    except SystemExit as exc:
        gate_exit = exc.code
    origins = []
    for name, module in sorted(sys.modules.items()):
        path = getattr(module, '__file__', None)
        if name.startswith('scripts.') and path and Path(path).is_file():
            origins.append({'module': name, 'path': str(path), 'sha256': digest(path)})
    receipt = {'mode': mode, 'variant': variant, 'gate_exit': gate_exit,
               'cwd': str(Path.cwd()), 'argv': sys.argv,
               'source_sha256': digest(TARGETS[variant]), 'spec_sha256': digest(SPEC),
               'interface_sha256': digest(INTERFACE), 'loaded_runtime': origins}
    (output / 'receipt.json').write_text(json.dumps(receipt, indent=2), encoding='utf-8')
    return gate_exit


def identity(issue):
    return json.dumps(issue, sort_keys=True, ensure_ascii=False)


def compare(label):
    differences, summary = [], []
    for variant in TARGETS:
        old = json.loads((HERE / f'old_{variant}/gate.json').read_text(encoding='utf-8'))
        new = json.loads((HERE / f'new_{variant}_{label}/gate.json').read_text(encoding='utf-8'))
        # 把每条原始项逐项匹配；变化项作为removed+added保留，不猜根因。
        from collections import Counter
        remaining_old = Counter(identity(issue) for issue in old['issues'])
        remaining_new = Counter(identity(issue) for issue in new['issues'])
        same = remaining_old & remaining_new
        for status, counts in (('removed_or_changed', remaining_old - same),
                               ('added_or_changed', remaining_new - same)):
            for raw, count in counts.items():
                differences.extend({'variant': variant, 'status': status,
                                    'raw_issue': json.loads(raw),
                                    'explanation_status': 'requires_adapter_evidence_or_manual_review'}
                                   for _ in range(count))
        summary.append({'variant': variant, 'old_errors': old['errors'], 'new_errors': new['errors'],
                        'unchanged_raw_issues': sum(same.values()),
                        'removed_or_changed': sum((remaining_old - same).values()),
                        'added_or_changed': sum((remaining_new - same).values()),
                        'new_delivery_ready': new['delivery_ready'], 'checks': new['checks'],
                        'old_rules': old['delivery_issues_by_rule'],
                        'new_rules': new['delivery_issues_by_rule']})
    result = {'groups': summary, 'raw_changes': differences,
              'normal_physical_admission': all(row['new_delivery_ready'] for row in summary)}
    (HERE / f'matrix_comparison_{label}.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(summary, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', choices=['old', 'new'])
    parser.add_argument('--variant', choices=list(TARGETS))
    parser.add_argument('--worker', action='store_true')
    parser.add_argument('--compare', action='store_true')
    parser.add_argument('--label', choices=['ownership', 'final'])
    parser.add_argument('--overlay', type=Path, default=OVERLAY)
    args = parser.parse_args()
    if args.compare:
        if not args.label:
            parser.error('--label required for comparison')
        compare(args.label)
        return 0
    if not args.mode or not args.variant:
        parser.error('--mode and --variant required')
    suffix = '_' + args.label if args.label else ''
    output = HERE / f'{args.mode}_{args.variant}{suffix}'
    if args.worker:
        return worker(args.mode, args.variant, output, args.overlay)
    output.mkdir(exist_ok=False)
    command = [sys.executable, '-B', '-X', 'utf8', str(Path(__file__).resolve()),
               '--worker', '--mode', args.mode, '--variant', args.variant, '--overlay', str(args.overlay)]
    if args.label:
        command.extend(['--label', args.label])
    completed = subprocess.run(command, cwd=HERE, capture_output=True, encoding='utf-8', timeout=180)
    (output / 'console.log').write_text(completed.stdout + completed.stderr, encoding='utf-8')
    (output / 'process.json').write_text(json.dumps({'command': command, 'cwd': str(HERE),
                                                  'exit': completed.returncode}, indent=2), encoding='utf-8')
    assert completed.returncode in (0, 1), f'Gate invocation failed: {output}'
    assert (output / 'gate.json').is_file()
    gate = json.loads((output / 'gate.json').read_text(encoding='utf-8'))
    print(json.dumps({'mode': args.mode, 'variant': args.variant, 'exit': completed.returncode,
                      'errors': gate['errors'], 'ready': gate['delivery_ready']}))
    return 0  # 执行成功与门禁是否通过分别记录。


if __name__ == '__main__':
    raise SystemExit(main())
