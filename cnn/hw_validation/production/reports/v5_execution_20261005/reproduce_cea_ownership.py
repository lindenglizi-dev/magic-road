"""两操作数中间使能污染的独立旧/新检查器最小复现。"""
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL = 'C:/Users/lenovo/.codex/skills/readable-verilog-generator'


def worker(mode):
    sys.path[:0] = ([str(HERE / 'checker_snapshot_final')] if mode == 'new' else []) + [SKILL]
    from scripts.python.quality.vg_semantic_facts import build_vg_facts
    from scripts.python.quality.vg_comb_targets import (
        build_module_implementation_index, enumerate_definition_roots, build_hierarchy_bindings)
    facts = build_vg_facts(HERE / 'cea_dependency_probe.v',
                           external_interface_sources=(HERE / 'opaque_ram_interface.v',))
    assert not facts.parse_errors
    index = build_module_implementation_index(facts)
    roots = enumerate_definition_roots(index)
    assert len(roots) == 1
    graph = build_hierarchy_bindings(roots[0], index, {})
    drivers = {endpoint.target: [{'kind': producer.kind, 'reason': producer.unknown_reason}
                                 for producer in producers]
               for endpoint, producers in graph.endpoint_drivers}
    unknown = [row for row in drivers['flag_enable'] if row['reason']]
    assert bool(unknown) == (mode == 'old')
    assert any(row['reason'] for row in drivers['wire_data'])
    print(json.dumps({'mode': mode, 'flag_enable_drivers': drivers['flag_enable'],
                      'ram_output_drivers': drivers['wire_data'], 'passed': True}))


def main():
    if len(sys.argv) == 2:
        worker(sys.argv[1])
        return
    results = []
    for mode in ('old', 'new'):
        command = [sys.executable, '-B', '-X', 'utf8', str(Path(__file__).resolve()), mode]
        result = subprocess.run(command, cwd=HERE, capture_output=True, encoding='utf-8', timeout=30)
        results.append({'command': command, 'cwd': str(HERE), 'exit': result.returncode,
                        'stdout': result.stdout, 'stderr': result.stderr})
        assert result.returncode == 0, results[-1]
    (HERE / 'cea_minimal_reproduction.json').write_text(
        json.dumps({'new_run': True, 'results': results, 'passed': True,
                    'scope': 'Input producer direction only; opaque output implementation remains unknown'}, indent=2),
        encoding='utf-8')
    print(json.dumps({'old_pollution_reproduced': True, 'new_input_sink_isolated': True,
                      'ram_output_still_unknown': True}))


if __name__ == '__main__':
    main()
