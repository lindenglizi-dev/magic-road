"""只读核对冻结编译清单；只在本目录写审计证据，不解析或修改 Verilog。"""
from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
import re
import subprocess

HERE = Path(__file__).resolve().parent
PROD = HERE.parents[1]
ROOT = PROD.parents[2]
C9 = PROD / 'frame_ready_dispatch_20261016'
C8 = PROD / 'box_overlay_joint_20261016'
GATES = ('compile', 'ast', 'readability', 'comment', 'naming', 'profile', 'testbench', 'toolchain')
WATCHED = {}


def read(path):
    path = Path(path).resolve()
    data = path.read_bytes()
    WATCHED[str(path)] = hashlib.sha256(data).hexdigest()
    return data.decode('utf-8-sig', errors='replace')


def load(path):
    return json.loads(read(path))


def save(name, value):
    path = HERE / name
    assert path.parent == HERE
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def table(name, rows):
    assert rows
    with (HERE / name).open('w', encoding='utf-8-sig', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def sha(path):
    read(path)
    return WATCHED[str(Path(path).resolve())]


def main():
    branch = subprocess.check_output(['git', 'branch', '--show-current'], cwd=ROOT, text=True).strip()
    assert branch == 'work/roadyolo'
    read(Path(__file__))
    for path in (ROOT / 'AGENTS.md', ROOT / 'MULTI_AGENT_WORKFLOW.md',
                 ROOT / 'cnn/hw_validation/plans/resource_budget_20261015/第八批任务_R256零训练与资源诊断_20261016.txt',
                 ROOT / 'cnn/hw_validation/plans/resource_budget_20261015/r256_candidate_contract_20261016.json'):
        read(path)
    c9 = load(C9 / 'verification/final_verification_receipt.json')
    s9 = Path(c9['evidence']['source_snapshot'])
    run9 = s9.parent
    summary9 = load(run9 / 'summary.json')
    compile9 = read(run9 / 'compile.log')
    c8 = load(C8 / 'verification/summary.json')
    run8 = Path(c8['fullframe_suite']).parent
    summary8 = load(run8 / 'summary.json')
    command8 = load(run8 / 'compile.command.json')
    hashes8 = load(run8 / 'hashes_before.json')
    assert command8['returncode'] == 0 and 'Errors: 0, Warnings: 0' in compile9
    files9 = sorted(s9.glob('*.v'))
    files8 = [Path(p) for p in command8['argv'] if str(p).endswith('.v')]
    assert len(files9) == 16 and len(files8) == 17
    chains = {
        'C9_dispatch_real_then_empty': (files9, 'tb_road_dispatch_publish', C9 / 'rtl'),
        'C8_fullframe_real7': (files8, 'tb_road_box_overlay_joint', PROD / 'result_publish_joint_20261015/rtl'),
    }
    bindings = []
    closure = []
    replacements = []
    literal_hits = []
    unchanged_points = []
    texts = {}
    inspected_current = set()
    literal_map = {12096: 3024, 12095: 3023, 169344: 42336,
                   9216: 2304, 9215: 2303, 11520: 2880, 11519: 2879,
                   131072: 65536, 73728: 36864}
    # 仅文本检索常量，不据此推导模块结构或声称 AST 通过。
    numbers = re.compile(r"(?<![\w])(?:(\d+)'[sS]?([dDhHbBoO])([0-9a-fA-F_]+)|(\d+))(?![\w])")
    for chain, (files, top, live_root) in chains.items():
        for path in files:
            text = read(path)
            texts[path] = text
            name = re.sub(r'^\d+_', '', path.name)
            if files is files8:
                originals = [Path(p) for p in hashes8 if Path(p).name == name and p.endswith('.v')]
                assert len(originals) == 1, (name, originals)
                actual = originals[0]
                assert sha(path) == hashes8[str(actual)]
            elif name.startswith('tb_'):
                actual = C9 / 'verification' / name
            elif name in ('road_numeric_rom_reader.v', 'road_yolo_numeric_rom_group.v'):
                actual = C9 / 'vendor_rom/rtl' / name
            elif name.startswith('ph1p_'):
                actual = C9 / 'vendor_rom/vendor' / name
            else:
                actual = live_root / name
            inspected_current.add(actual.resolve())
            assert sha(actual) == sha(path), (chain, name, 'current/snapshot mismatch')
            closure.append(dict(chain=chain, compiled_file=str(path), current_file=str(actual or ''),
                                sha256=sha(path), current_matches_snapshot=bool(actual),
                                proof=str(run9 / 'compile.log' if files is files9 else run8 / 'compile.command.json')))
            if name in c9['evidence']['core_sha256']:
                assert sha(path) == c9['evidence']['core_sha256'][name]
            for line_number, line in enumerate(text.splitlines(), 1):
                code = line.split('//', 1)[0]
                for match in numbers.finditer(code):
                    value = int(match[3].replace('_', ''), {'d': 10, 'h': 16, 'b': 2, 'o': 8}[match[2].lower()]) if match[2] else int(match[4])
                    if value in literal_map:
                        literal_hits.append(dict(chain=chain, file=str(path), line=line_number,
                            literal=match[0], numeric_value=value, proposed_value=literal_map[value],
                            excerpt=line.strip(), classification='context_review_not_blind_replace'))
            instance = top + ('.c2' if name == 'road_head_decode_topk.v' else '.c9' if name == 'road_nms_serial.v' else '.publisher' if name == 'road_result_publisher.v' else '')
            if name in ('road_head_decode_topk.v', 'road_nms_serial.v', 'road_result_publisher.v'):
                bindings.append(dict(chain=chain, top=top, instance=instance, module=name[:-2],
                                     compiled_file=str(path), current_file=str(actual), sha256=sha(path)))
            for number, line in enumerate(text.splitlines(), 1):
                old = new = reason = None
                if name == 'road_head_decode_topk.v':
                    if 'assign grid_last_x=' in line:
                        old, new, reason = '127,63,31', '63,31,15', 'three scale last column'
                    elif 'assign grid_last_y=' in line:
                        old, new, reason = '71,35,17', '35,17,8', 'three scale last row; P4 height9'
                    elif 'assign axis_limit=' in line:
                        old, new, reason = '73728,131072', '36864,65536', 'network Q8 y/x limits'
                    elif "cnt_cell==14'd12095" in line:
                        old, new, reason = "14'd12095", "14'd3023", 'full head stream terminal cell'
                elif name == 'road_nms_serial.v':
                    if "18'd131072" in line:
                        old, new, reason = '131072,73728', '65536,36864', 'current/retained Q8 geometry validation'
                    elif 'reg_scale_' in line and '[8:0]' in line:
                        old, new, reason = '[8:0],9\'d256,[9]', '[7:0],8\'d128,[8]', 'RNE denominator512 to256; tie and parity'
                    elif 'reg_source_' in line and 'reg_scale_' in line and '[20:9]' in line:
                        old, new, reason = '[20:9]', '[19:8]', '12-bit quotient; bounded product<=327680<2^19; retain21-bit product register'
                    elif 'reg_scale_' in line and '{1\'b0, reg_current' in line:
                        old, new, reason = 'q8*5 shift/add', 'retain q8*5 shift/add', 'numerator5 unchanged; do not multiply old rounded pixel by2'
                elif name.startswith('tb_') and '12096' in line:
                    old, new, reason = '12096', '3024', 'future candidate testbench/vector length; old frozen fixture stays unchanged'
                if old:
                    replacements.append(dict(chain=chain, file=str(path), current_file=str(actual or ''),
                        line=number, instance=instance if name.startswith('road_') else top,
                        old=old, new=new, reason=reason, excerpt=line.strip(),
                        category='RETAIN_NUMERATOR5' if new.startswith('retain') else 'FUTURE_GEOMETRY_OR_FIXTURE_LENGTH_ADAPTATION',
                        action_this_batch='READ_ONLY_NO_EDIT'))
                if (('THRESHOLD=' in line) or ('selected_count<8\'d128' in line)
                    or ('cnt_kept == 6\'d32' in line) or ('cnt_entry >= 7\'d64' in line)
                    or ('AGE_LIMIT_MS(2000)' in line)):
                    unchanged_points.append(dict(chain=chain, file=str(path), current_file=str(actual),
                        line=number, excerpt=line.strip(), action='RETAIN',
                        note='32768 is frozen diagnostic threshold, not newly qualified accuracy threshold; age override2000 retains capture-time contract'))

    # 实例绑定逐项由实际 TB 源定位；无需第二份 Verilog parser。
    for item in bindings:
        path = next(p for p in chains[item['chain']][0] if p.name.endswith(item['top'] + '.v'))
        marker = item['module'] + ' ' + item['instance'].split('.')[-1] + '('
        lines = texts[path].splitlines()
        locations = [i for i, line in enumerate(lines, 1) if marker in line]
        assert len(locations) == 1, marker
        item['binding_file'], item['binding_line'] = str(path), locations[0]

    # 仅三个同名后处理文件的历史候选，不把这些检索命中当实际实例化。
    historical = []
    active = {p.resolve() for files, _, _ in chains.values() for p in files} | inspected_current
    for name in ('road_head_decode_topk.v', 'road_nms_serial.v', 'road_result_publisher.v'):
        for path in sorted(PROD.rglob(name)):
            if path.resolve() in active or HERE in path.parents:
                continue
            text = read(path)
            hit_lines = [i for i, line in enumerate(text.splitlines(), 1)
                         if any(str(value) in line for value in literal_map)]
            historical.append(dict(file=str(path), sha256=sha(path),
                status='NOT_IN_SELECTED_C9_OR_C8_COMPILE_LIST', literal_hit_lines=','.join(map(str, hit_lines))))

    prior_gates = []
    gate_paths = [C9 / 'gates/dispatcher_unique.json',
                  PROD / 'head_decode_topk_rtl_20261015/gates/attempt_01.json',
                  PROD / 'nms_serial_rtl_20261015/gate_rtl_final.json',
                  PROD / 'result_publish_joint_20261015/gates/publisher.json',
                  C8 / 'gate_attempt3/road_box_line_overlay.json',
                  C8 / 'gate_attempt3/road_box_age_overlay.json']
    gate_paths += [C9 / 'verification' / row['report'] for row in c9['evidence']['gates']]
    for path in gate_paths:
        report = load(path)
        checks = report.get('checks', {})
        prior_gates.append(dict(file=str(path), sha256=sha(path),
            errors=report.get('errors'), strict_warnings=report.get('strict_warnings'),
            ready=report.get('delivery_ready', report.get('ready')),
            checks={key: checks.get(key, {}).get('status', 'NOT_RECORDED') for key in GATES},
            raw_checks=checks, execution_this_batch='NOT_RUN'))

    ref_paths = [ROOT / 'cnn/integer.py',
        PROD / 'postprocess_golden_2fps_20261015/golden.py',
        PROD / 'postprocess_joint_1fps_20261015/verify_vectors.py',
        PROD / 'postprocess_joint_1fps_20261015/vector_manifest.json',
        PROD / 'head_decode_topk_rtl_20261015/verification/assets/sigmoid_lut_16.hex',
        PROD / 'head_decode_topk_rtl_20261015/verification/assets/exp_lut_16.hex']
    references = [dict(file=str(path), sha256=sha(path)) for path in ref_paths]
    assert references[0]['sha256'] == '441b91d86895fb0c0337583325fb9cc39624026a6759d39da51aaab49a5ca040'
    assert references[4]['sha256'] == '889fa62b54d26210c37e9260c3e954d1913c0606593381152a2846b2609419ca'
    assert references[5]['sha256'] == '135731b97a0a144eacf953b80a540eb68591bcb6b5bddb588824917218ca8d0c'
    contract = dict(references=references, thresholds_uint16=[32768, 32768], threshold_comparison='>=',
        threshold_status='CURRENT_FROZEN_DIAGNOSTIC_ONLY_NOT_NEW_ACCURACY_ACCEPTANCE',
        sigmoid='INT16 Q7.8; RNE(raw/4)+512; raw<=-2048=>0; raw>=2048=>65535; index1024=>sigmoid_upper',
        sigmoid_lut_entries=1024, exp_lut_entries=256,
        exponent='clip raw to[-1024,896]; address=RNE((raw+1024)*255/1920); UINT16 Q6.10 table',
        score='RNE(objectness_uint16*class_uint16/65536)',
        ranking='descending(score,-global_cell_id); class0 then class1; equal score earlier cell wins',
        topk_per_class=128, max_boxes_per_class=32, max_boxes_total=64,
        geometry='center_q8=(raw_xy+grid_xy*256)*stride; size_q8=RNE(exp*stride/4); half=RNE(size/2); clip half-open endpoints',
        candidate_q8_limits=[65536, 36864], zero_area='removed after Top128, never before ranking',
        nms='same class only; suppress iff3*intersection>area_a+area_b; equality atIoU1/2 retained',
        restore_old='RNE(box_q8*5/512)', restore_new='RNE(box_q8*5/256) once, then source[0,1280]x[0,720] clamp',
        source_rounding_collapse='existing reference retains valid network box even when final source endpoints round equal; renderer skips collapsed geometry',
        unchanged=['24MAC/signed33/RNE/SiLU', 'age2000ms from capture timestamp', 'READY visibility and last-read release', 'dispatcher protocol', 'source epoch/frame/task identity', 'SOF full-table switch'])
    table('actual_source_closure.csv', closure)
    table('actual_replacement_points.csv', replacements)
    table('literal_hits_selected_closure.csv', literal_hits)
    table('historical_copies_not_selected.csv', historical)
    table('unchanged_contract_points.csv', unchanged_points)
    save('actual_instance_bindings.json', bindings)
    save('postprocess_reference_contract.json', contract)
    mismatches = []
    for q8 in range(65537):
        product = q8 * 5
        quotient = (product >> 8) & 4095  # 候选[19:8]，保持原12位像素输出。
        remainder = product & 255
        sliced = quotient + int(remainder > 128 or (remainder == 128 and (product >> 8) & 1))
        expected, rest = divmod(product, 256)
        expected += int(rest * 2 > 256 or (rest * 2 == 256 and expected % 2))
        if sliced != expected:
            mismatches.append([q8, sliced, expected])
        assert product <= 327680 < (1 << 19) and sliced <= 1280
    assert not mismatches
    save('source_restore_rne_exhaustive_receipt.json', dict(status='PASS',
        tested_q8_values=65537, inclusive_q8_range=[0, 65536], y_range_included=[0, 36864],
        multiply='retain21-bit q8*5 register', quotient_slice='[19:8]12bits',
        remainder='[7:0]', tie_half=128, parity_bit=8, rounding_increment="12'd1",
        mathematical_reference='nearest-even(q8*5/256) once', mismatches=mismatches,
        max_product=327680, max_source_pixel=1280, old_RTL_changed=False,
        boundary='Python arithmetic exhaustive check only; no Verilog simulation or gate'))
    save('original_eight_gates.json', dict(this_batch={key: 'NOT_RUN' for key in GATES}, originals=prior_gates))
    absent = {value: sum(row['numeric_value'] == value for row in literal_hits) for value in literal_map}
    adaptation_count = sum(row['category'] == 'FUTURE_GEOMETRY_OR_FIXTURE_LENGTH_ADAPTATION' for row in replacements)
    retained_count = sum(row['category'] == 'RETAIN_NUMERATOR5' for row in replacements)
    save('audit_receipt.json', dict(status='PASS_READ_ONLY_ACTUAL_SOURCE_CLOSURE_AUDIT', branch=branch,
        C9_receipt=str(C9 / 'verification/final_verification_receipt.json'), C9_summary=str(run9 / 'summary.json'),
        C9_original_status=c9['status'], C9_protocol_scenarios=c9['protocol_scenarios'],
        C9_real_then_empty=c9['joint_counts'], C8_summary=str(C8 / 'verification/summary.json'),
        C8_original_status=c8['status'], C8_fullframes=c8['main_frames'], C8_actual_compile=str(run8 / 'compile.command.json'),
        compiled_source_rows=len(closure), bindings=len(bindings), replacement_rows=len(replacements),
        audit_row_meaning='audited future adaptation/retention locations; not58bugs or58mandatory edits',
        future_geometry_or_fixture_length_adaptation_rows=adaptation_count,
        retain_numerator5_rows=retained_count, other_unchanged_contract_rows=len(unchanged_points),
        historical_copy_count=len(historical), numeric_occurrences_in_selected_closure=absent,
        scale_cuts_old=[0, 9216, 11520, 12096], scale_cuts_new=[0, 2304, 2880, 3024],
        source_restore_quotient='[19:8]12bits;[20:8]would silently assign13bits to12bits; bounded product top bits zero',
        absent_literals_boundary='169344/9216/11520 not actual decode arithmetic constants; head byte count is external producer/graph contract, scale boundaries are implicit grid counters',
        source_closure_scope='two selected saved-head fixtures; not production top/full CNN/DDR; snapshot vendor compile sources included',
        source_equivalence='current postprocess copies match their selected snapshots and C9 accepted core hashes',
        eight_gates_this_batch={key: 'NOT_RUN' for key in GATES}, simulations_this_batch=0, TD_this_batch=0,
        source_edits=0, strict_python_script_skill='UNAVAILABLE_NOT_CLAIMED',
        limits='original strict failures and vendor bounds warnings retained; no value-level CNN or physical proof'))
    source_hashes = dict(WATCHED)
    changed = [path for path, expected in source_hashes.items()
               if hashlib.sha256(Path(path).read_bytes()).hexdigest() != expected]
    assert not changed, changed
    save('read_source_hashes.json', dict(before=source_hashes, after=source_hashes,
        checked_files=len(source_hashes), changed=changed, unchanged=True,
        hash_check='each source re-read from disk after all audit outputs; no old source writes'))
    print('READ_ONLY_AUDIT_PASS', len(closure), 'compiled sources;', len(replacements),
          'replacement rows;', len(source_hashes), 'inputs unchanged')


if __name__ == '__main__':
    main()
