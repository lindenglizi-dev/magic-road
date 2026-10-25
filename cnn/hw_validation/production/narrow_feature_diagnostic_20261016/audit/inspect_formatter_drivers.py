"""Read-only closure audit using the installed formatter AST, never a second parser."""
import hashlib
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
SKILL = Path('C:/Users/lenovo/.codex/skills/readable-verilog-generator')
sys.path.insert(0, str(SKILL))
from scripts.python.quality.formatter_ast import build_ast_report_for_path
from scripts.python.quality.vg_contract_liveness import _module_signal_facts

ROOT = Path(__file__).resolve().parent
OLD = ROOT.parent.parent / 'workstore_feature_20261016/frozen'
files = sorted((OLD / 'rtl').glob('*.v')) + sorted((OLD / 'reused').glob('*.v'))
if len(sys.argv) > 1:
    files += [Path(sys.argv[1])]
reports = []
modules = {}
for path in files:
    print('AST_START', path.name, flush=True)
    cache = ROOT / (path.name + '.ast.json')
    source_hash = hashlib.sha256(path.read_bytes()).hexdigest()
    if cache.exists() and json.loads(cache.read_text(encoding='utf-8'))['sha256'] == source_hash:
        report = json.loads(cache.read_text(encoding='utf-8'))['report']
    else:
        report = build_ast_report_for_path(path)
        cache.write_text(json.dumps(dict(sha256=source_hash, report=report), ensure_ascii=False), encoding='utf-8')
    text = path.read_text(encoding='utf-8-sig')
    reports.append(dict(path=str(path), sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                        summary=report['summary'], diagnostics=report['diagnostics']))
    for module in report['modules']:
        modules[module['name']] = (path, module, tuple(text.splitlines()))
    print('AST_DONE', path.name, report['summary'], flush=True)

# Exact real PH1P interface from TD arch/ph1p_macro.v: output-only opens are separate.
primitive_inputs = set('dia addra cea ocea clka wea rsta bea dib addrb ceb oceb clkb web rstb beb ecc_sbiterrinj ecc_dbiterrinj'.split())
primitive_outputs = set('doa dob ecc_sbiterr ecc_dbiterr'.split())
connections, findings = [], []
for name, (path, module, lines) in modules.items():
    facts = _module_signal_facts(module, lines)
    resolved = set(facts['drivers'])
    child_drivers = {}
    for inst in module['instances']:
        child = inst['module_name']
        directions = {}
        if child in modules:
            directions = {p['name']: p['direction'] for p in modules[child][1]['ports']}
        elif child == 'PH1P_LOGIC_ERAM':
            directions = {p: 'input' for p in primitive_inputs}
            directions.update({p: 'output' for p in primitive_outputs})
        associations = inst.get('port_associations', [])
        seen = set()
        for assoc in associations:
            formal = assoc.get('formal_name')
            actual = assoc.get('actual', {})
            seen.add(formal)
            direction = directions.get(formal, 'unknown')
            refs = actual.get('references', [])
            if direction == 'output':
                resolved.update(refs)
                for ref in refs:
                    child_drivers.setdefault(ref, []).append(inst['instance_name'] + '.' + str(formal))
            if direction == 'unknown' or (direction == 'input' and assoc.get('explicit_unconnected')):
                connections.append(dict(module=name, instance=inst['instance_name'], child=child,
                    formal=formal, direction=direction, actual=actual, issue='unknown_or_empty_input'))
        for formal, direction in directions.items():
            if formal not in seen:
                connections.append(dict(module=name, instance=inst['instance_name'], child=child,
                    formal=formal, direction=direction, issue='omitted_port'))
    candidates = set(facts['reads']) & set(facts['declarations'])
    candidates |= {p for p, d in facts['ports'].items() if d == 'output'}
    for symbol in sorted(candidates - facts['drivers']):
        declaration = facts['declarations'].get(symbol)
        if declaration and declaration['kind'] in {'params', 'localparams'}:
            continue
        findings.append(dict(module=name, file=str(path), symbol=symbol,
            line=declaration['line'] if declaration else None,
            classification='driven_by_known_child_output' if symbol in resolved else 'unresolved_effective_driver',
            child_drivers=child_drivers.get(symbol, [])))
result = dict(parser='installed readable-verilog-generator formatter_ast', sources=reports,
              module_count=len(modules), connections=connections, raw_local_driver_candidates=findings,
              modules={name: module for name, (_, module, _) in modules.items()})
output = ROOT / ('formatter_driver_audit_wrapper.json' if len(sys.argv) > 1 else 'formatter_driver_audit_frozen.json')
output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
print('AUDIT_OUTPUT', output, flush=True)
print('UNRESOLVED', sum(f['classification'] == 'unresolved_effective_driver' for f in findings), flush=True)
