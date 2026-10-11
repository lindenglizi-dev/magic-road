"""Inspect actual hierarchy drivers and width bounds; retain strict findings."""
from pathlib import Path
from collections import Counter
import json
import re
import subprocess
import sys
from prepare import HERE, OLD, sha, check

SKILL = Path('C:/Users/lenovo/.codex/skills/readable-verilog-generator')
sys.path.insert(0, str(SKILL))

def main(which):
    folder = HERE / which
    findings = json.loads((HERE / 'semantic_findings.json').read_text(encoding='utf-8'))
    evidence = []
    sources = {p.stem: p.read_text(encoding='utf-8') for p in (folder / 'rtl').glob('*.v')}
    for finding in findings:
        if finding['rule_id'] != 'VG153':
            continue
        symbol = finding['symbol']; source = sources[Path(finding['path']).stem]
        if symbol == 'memory_words':
            assert re.search(r'memory_words\[.*?\]\s*<=', source)
            driver = 'Clocked indexed write in simulation-only RAM model; excluded from TD synthesis.'
        else:
            matches = re.findall(r'\.(\w+)\(\s*' + re.escape(symbol) + r'\s*\)', source)
            drivers = []
            for port in matches:
                for module, child in sources.items():
                    if re.search(r'\boutput\b[^;\n]*\b' + re.escape(port) + r'\b', child):
                        drivers.append((module, port))
            assert drivers, (symbol, matches)
            driver = str(drivers)
        evidence.append({'file': finding['path'], 'line': finding['line'], 'signal': symbol,
                         'actual_driver': driver, 'strict_status': 'failed_retained'})
    # INT32 * unsigned31 has magnitude <= 2^31*(2^31-1) < 2^62.
    maximum_product = (1 << 31) * ((1 << 31)-1)
    assert maximum_product < (1 << 63)
    assert 19*16 == 304 and 96+96+18+32+6+1+3+48+1 == 301
    # Flags referencing async reset are intentional immediate cancel, not waived.
    counts = Counter(f['rule_id'] for f in findings)
    report = {'inspected_hierarchy_driver_findings': evidence,
              'retained_semantic_counts': dict(counts),
              'width_proof': {'max_product_magnitude': maximum_product, 'signed_product_bits':64,
                             'packet_bits':304,'used_packet_bits':301,'tail_padding_bits':3},
              'limitations': ['Simulation and source driver checks are not exhaustive formal proof.',
                 'VG093 remains failed: immediate cancellation uses reset in ready/valid.',
                 'VG145/VG146 are dependency-cone risks; physical endpoints decide optimization.',
                 'VG138 literal sizing includes style and semantic risk; retained, not blanket waived.',
                 'VG151 entries here are simulation primitive parameter declarations, not deployed arithmetic.',
                 'Multi-driver and combinational-loop conclusions require actual TD DRC too.']}
    (folder / 'semantic_audit.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    # Fresh gate includes the shell, frozen arithmetic and simulation primitive.
    import shutil
    shutil.copy2(HERE / 'road_dynamic_low_io_top.v', folder / 'rtl/road_dynamic_low_io_top.v')
    with (folder / 'gate.log').open('w', encoding='utf-8') as stream:
        code = subprocess.run([sys.executable,'-B','-X','utf8','-m',
            'scripts.python.validation.generated_deliverable_gate', str(folder / 'rtl'),
            '--json',str(folder / 'gate.json'),'--markdown',str(folder / 'gate.md')],
            cwd=HERE, env={**__import__('os').environ,'PYTHONPATH':str(SKILL)},
            stdout=stream, stderr=subprocess.STDOUT).returncode
    assert code in (0,1), code
    gate = json.loads((folder / 'gate.json').read_text(encoding='utf-8'))
    print('DRIVER_INSPECTED', len(evidence), 'GATE_ERRORS',gate['errors'],
          'CHECKS',{k:v['status'] for k,v in gate['checks'].items()})
    check()

if __name__ == '__main__':
    main(sys.argv[1])
