#!/usr/bin/env python3
"""Read-only formatter audit for the isolated CCL pipeline source."""
from __future__ import annotations

import hashlib
import json
import platform
import sys
from pathlib import Path

sys.path.insert(0, str(Path.cwd()))
from scripts.python.quality.formatter_config import create_formatter_backend


AUDIT = Path(__file__).resolve().parent
PROJECT = AUDIT.parents[3]
SOURCE = PROJECT / 'tests/experimental_ddr_ccl/ccl_pipeline_trial_top.v'
SKILL = Path.cwd()
TRACKED = {
    'defaults': SKILL / 'assets/verilog_formatter_config/defaults.json',
    'formatter_normalize': SKILL / 'assets/verilog_formatter_config/profiles/formatter-normalize.json',
    'engine': SKILL / 'scripts/python/quality/formatter_backend/engine.py',
    'parser': SKILL / 'scripts/python/quality/formatter_backend/parse_mixin.py',
    'always_split': SKILL / 'scripts/python/quality/formatter_backend/analysis_mixin.py',
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def text_digest(text: str) -> str:
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def non_whitespace_digest(text: str) -> str:
    return text_digest(''.join(text.split()))


def split_grouped_nonblocking_lines(text: str) -> tuple[str, list[int]]:
    """Put each grouped nonblocking assignment on its own physical line."""
    output = []
    changed_lines = []
    for line_number, line in enumerate(text.splitlines(), 1):
        if line.count(';') > 1 and '<=' in line:
            indent = line[:len(line) - len(line.lstrip())]
            statements = [item.strip() for item in line.split(';') if item.strip()]
            output.extend(f'{indent}{statement};' for statement in statements)
            changed_lines.append(line_number)
        else:
            output.append(line)
    return '\n'.join(output) + '\n', changed_lines


def error_chain(action):
    try:
        value = action()
    except Exception as exc:  # Record the formatter's complete cause chain.
        messages = []
        current = exc
        while current is not None:
            messages.append(f'{type(current).__name__}: {current}')
            current = current.__cause__
        return {'status': 'failed', 'error_chain': messages}
    return {'status': 'passed', 'result_chars': len(value) if isinstance(value, str) else None}


source = SOURCE.read_text(encoding='utf-8')
source_hash_before = digest(SOURCE)
tool_hashes_before = {name: digest(path) for name, path in TRACKED.items()}
engine = create_formatter_backend(profile='formatter-normalize')
module_name, parameters, ports, body = engine._parse_module(source)
failed_always = {}
original_split = engine._split_single_always_block


def traced_split(block, *, inside_generate=False):
    try:
        return original_split(block, inside_generate=inside_generate)
    except Exception:
        failed_always.update({
            'header': block.header,
            'targets': list(block.targets),
            'target_count': len(block.targets),
            'trigger_kind': block.trigger_kind,
            'contains_if': block.contains_if,
            'contains_case': block.contains_case,
            'lines': list(block.lines),
        })
        raise


engine._split_single_always_block = traced_split

fail_example = (AUDIT / 'minimal_multi_target_fail.v').read_text(encoding='utf-8')
pass_example = (AUDIT / 'minimal_split_pass.v').read_text(encoding='utf-8')
line_split_source, line_split_numbers = split_grouped_nonblocking_lines(source)
(AUDIT / 'current_source_snapshot.v').write_bytes(SOURCE.read_bytes())
(AUDIT / 'equivalent_line_split_preview.v').write_text(line_split_source, encoding='utf-8')
preview_name, preview_parameters, preview_ports, preview_body = engine._parse_module(line_split_source)
parameter_signature = [
    (item.keyword, item.name, item.value, item.decl_spec) for item in parameters
]
preview_parameter_signature = [
    (item.keyword, item.name, item.value, item.decl_spec) for item in preview_parameters
]
port_signature = [
    (item.direction, item.width, item.name, item.signed, item.unpacked) for item in ports
]
preview_port_signature = [
    (item.direction, item.width, item.name, item.signed, item.unpacked) for item in preview_ports
]
result = {
    'status': 'read_only_formatter_audit',
    'runtime': {'python': platform.python_version(), 'platform': platform.platform()},
    'source': str(SOURCE),
    'source_sha256': source_hash_before,
    'formatter_profile': 'formatter-normalize',
    'tool_hashes': tool_hashes_before,
    'direct_parse': {
        'status': 'passed', 'module': module_name,
        'parameter_count': len(parameters), 'port_count': len(ports),
        'parameters': [item.name for item in parameters],
        'ports': [item.name for item in ports], 'body_chars': len(body),
    },
    'format_text_current': error_chain(lambda: engine.format_text(source, SOURCE)),
    'minimal_grouped_assignments': error_chain(
        lambda: create_formatter_backend(profile='formatter-normalize').format_text(fail_example)
    ),
    'minimal_line_separated_assignments': error_chain(
        lambda: create_formatter_backend(profile='formatter-normalize').format_text(pass_example)
    ),
    'after_equivalent_line_split': error_chain(
        lambda: create_formatter_backend(profile='formatter-normalize').format_text(
            line_split_source, SOURCE
        )
    ),
    'equivalent_line_split': {
        'changed_physical_lines': line_split_numbers,
        'changed_physical_line_count': len(line_split_numbers),
        'source_non_whitespace_sha256': non_whitespace_digest(source),
        'preview_non_whitespace_sha256': non_whitespace_digest(line_split_source),
    },
    'snapshot': {
        'path': str(AUDIT / 'current_source_snapshot.v'),
        'sha256': digest(AUDIT / 'current_source_snapshot.v'),
    },
    'preview_direct_parse': {
        'status': 'passed',
        'module': preview_name,
        'parameter_count': len(preview_parameters),
        'port_count': len(preview_ports),
        'body_chars': len(preview_body),
        'module_equal': preview_name == module_name,
        'parameter_defaults_equal': preview_parameter_signature == parameter_signature,
        'port_declarations_equal': preview_port_signature == port_signature,
    },
}
result['failed_always'] = failed_always
gate_path = AUDIT / 'pipeline_gate.json'
if gate_path.exists():
    gate = json.loads(gate_path.read_text(encoding='utf-8'))
    result['strict_gate'] = {
        'delivery_ready': gate['delivery_ready'],
        'errors': gate['errors'],
        'strict_warnings': gate['strict_warnings'],
        'checks': gate['checks'],
        'report_sha256': digest(gate_path),
    }
if digest(SOURCE) != source_hash_before:
    raise AssertionError('pipeline source changed during read-only audit')
if {name: digest(path) for name, path in TRACKED.items()} != tool_hashes_before:
    raise AssertionError('formatter implementation or configuration changed during audit')
if digest(AUDIT / 'current_source_snapshot.v') != source_hash_before:
    raise AssertionError('saved source snapshot does not match the audited source')
if non_whitespace_digest(source) != non_whitespace_digest(line_split_source):
    raise AssertionError('line-only preview changed the non-whitespace token stream')
if not all(result['preview_direct_parse'][key] for key in (
        'module_equal', 'parameter_defaults_equal', 'port_declarations_equal')):
    raise AssertionError('line-only preview changed the parsed module interface')

(AUDIT / 'audit.json').write_text(
    json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8'
)
current_error = result['format_text_current']['error_chain'][0]
minimal_error = result['minimal_grouped_assignments']['error_chain'][0]
lines = [
    '# Formatter parser compatibility audit', '',
    f'- Source SHA256: `{source_hash_before}`',
    f'- Direct `_parse_module`: PASS, {len(parameters)} parameters, {len(ports)} ports.',
    f'- Current `format_text`: `{current_error}`',
    f'- Minimal grouped-assignment reproducer: `{minimal_error}`',
    f"- Same minimal assignments placed on separate lines: {result['minimal_line_separated_assignments']['status']}.",
    f"- Actual rejected block targets: {failed_always.get('target_count')}.",
    f"- Line-only preview: {len(line_split_numbers)} physical lines expanded; `format_text` {result['after_equivalent_line_split']['status']}.",
    f"- Source/preview non-whitespace hashes equal: {non_whitespace_digest(source) == non_whitespace_digest(line_split_source)}.", '',
    '- Direct parser comparison: module name, all 11 parameter defaults, and all 68 port ',
    'declarations are identical between source and preview.', '',
    'Conclusion: the source is valid to the direct module/ANSI-port parser. The current failure ',
    'comes from the large main sequential process containing multiple nonblocking assignments ',
    'on one physical line. The normalizer treats each such line as one statement and rejects it ',
    'because that statement writes multiple targets. A paired-FSM block with one assignment per ',
    'line is auto-splittable. Expanding the 25 grouped physical lines preserves the non-whitespace ',
    'token stream and allows `format_text` to pass, so a bounded formatting-only fix exists; no ',
    'manual repartition of the main sequential process is required.', '',
    'No source or skill file was modified. Full exception chains, current interface names and ',
    'tool hashes are in `audit.json`; the exact input and review-only line-split preview are saved ',
    'beside this report.',
]
if 'strict_gate' in result:
    checks = result['strict_gate']['checks']
    lines.extend([
        '', '## Bounded strict-gate run', '',
        f"- Delivery ready: `{result['strict_gate']['delivery_ready']}`; errors: {result['strict_gate']['errors']}; strict warnings: {result['strict_gate']['strict_warnings']}.",
        f"- Compile/parser check: {checks['compile']['status']} ({checks['compile']['modules']} module, {checks['compile']['parse_errors']} parse errors).",
        f"- Formatter AST check: {checks['ast']['status']} ({checks['ast']['formatter_errors']} formatter error).",
        f"- Readability: {checks['readability']['status']}; comment: {checks['comment']['status']}; naming: {checks['naming']['status']}; profile: {checks['profile']['status']}.",
        '- This strict-gate result is a recorded failure, not a pass inferred from compilation.',
        '- Full evidence is in `pipeline_gate.json` and `pipeline_gate.md`.',
    ])
(AUDIT / 'audit.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
print(json.dumps(result, ensure_ascii=False, indent=2))
