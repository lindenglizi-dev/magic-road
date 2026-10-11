"""Keep strict failures visible for original and actual v11 source closure."""
import argparse
import json
import shutil
import sys
from pathlib import Path
from guard import ROOT, PREVIOUS, bounded, check, digest, run

SKILL = Path(r'C:\Users\lenovo\.codex\skills\readable-verilog-generator')
PROJECT = ROOT.parents[4]

def worker(target, output):
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(SKILL))
    from scripts.python.workflow.workspace import use_workspace_root
    from scripts.python.quality.deliverable_gate import run_verilog_deliverable_gate, write_verilog_deliverable_gate_report
    from scripts.python.quality.quality_gate import EXTERNAL_INTERFACE_SOURCES_SPEC_KEY
    spec = {EXTERNAL_INTERFACE_SOURCES_SPEC_KEY: (PROJECT / 'cnn/hw_validation/interfaces/ph1p_eram_interface_complete.v',)}
    with use_workspace_root(ROOT):
        gate = run_verilog_deliverable_gate(target, spec=spec, strict=True, include_testbench=False)
        write_verilog_deliverable_gate_report(gate, json_path=output.with_suffix('.json'), markdown_path=output.with_suffix('.md'))
    print(json.dumps({'errors': gate['errors'], 'delivery_ready': gate['delivery_ready']}))
    return 0 if gate['delivery_ready'] else 1

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--worker', action='store_true')
    parser.add_argument('--target', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    if args.worker:
        return worker(bounded(args.target), bounded(args.output))
    check()
    closure = ROOT / 'gates/source_closure'
    closure.mkdir(parents=True, exist_ok=False)
    cores = [PREVIOUS / 'gates/source_closure' / name for name in
             ('road_mac_probe.v', 'road_round_shift.v', 'silu_shared_unit.v')]
    inputs = cores + [ROOT / 'rtl/road_postprocess_stream.v', ROOT / 'rtl/down2_overlap_tile_runner.v',
                      ROOT / 'physical/road_postprocess_low_io_top.v']
    identities = {}
    for path in inputs:
        target = closure / path.name
        shutil.copyfile(path, target)
        identities[str(path)] = {'sha256': digest(path), 'snapshot': str(target)}
    (ROOT / 'gates/source_manifest.json').write_text(json.dumps(identities, indent=2) + '\n', encoding='utf-8')
    results = {}
    for target in (ROOT / 'rtl/road_postprocess_stream.v', ROOT / 'rtl/down2_overlap_tile_runner.v', closure):
        prefix = ROOT / 'gates' / target.stem
        code = run([sys.executable, '-B', '-X', 'utf8', str(Path(__file__).resolve()),
                    '--worker', '--target', str(target), '--output', str(prefix)],
                   ROOT, prefix.with_suffix('.log'), timeout=1800)
        if code not in (0, 1) or not prefix.with_suffix('.json').exists():
            raise RuntimeError(f'Gate invocation failed: {target}, exit={code}')
        gate = json.loads(prefix.with_suffix('.json').read_text(encoding='utf-8'))
        results[target.stem] = {'exit': code, 'errors': gate['errors'], 'strict_warnings': gate['strict_warnings'],
                               'delivery_ready': gate['delivery_ready'],
                               'checks': {key: value['status'] for key, value in gate['checks'].items()},
                               'rules': gate['delivery_issues_by_rule'], 'raw_sha256': digest(prefix.with_suffix('.json'))}
    (ROOT / 'gates/summary.json').write_text(json.dumps(results, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(results))
    print(json.dumps(check()))

if __name__ == '__main__':
    raise SystemExit(main())
