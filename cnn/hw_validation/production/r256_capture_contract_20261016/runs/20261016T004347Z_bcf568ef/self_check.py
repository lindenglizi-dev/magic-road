"""R256 CPU自检与黄金数据导出；全部写入本候选的新run，不启动外部工具。"""
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
from itertools import chain, islice
import json
from pathlib import Path
import random
import shutil
import sys
from time import perf_counter
import uuid
import zlib

import reference as ref

ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parents[3]
PRODUCTION = ROOT.parent
CONTRACT = PROJECT / 'cnn/hw_validation/plans/resource_budget_20261015/r256_candidate_contract_20261016.json'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def save(path, value):
    path = path.resolve()
    if not path.is_relative_to(ROOT):
        raise ValueError('outputs must stay inside this candidate')
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def input_paths():
    capture = PRODUCTION / 'camera_capture_2fps_20261015'
    display = PRODUCTION / 'box_overlay_joint_20261016'
    dispatch = PRODUCTION / 'frame_ready_dispatch_20261016'
    return [CONTRACT, PROJECT / 'AGENTS.md', PROJECT / 'MULTI_AGENT_WORKFLOW.md',
            capture / 'interfaces.json', capture / 'rtl/road_area_resize.v',
            capture / 'rtl/road_capture_slots.v',
            dispatch / 'rtl/road_capture_slots.v', dispatch / 'integration_contract.txt',
            display / 'artifact_hashes.json', display / 'status.json', display / 'handoff.txt',
            display / 'verification/summary.json', display / 'source_manifest.json',
            display / 'rtl/road_box_line_overlay.v', display / 'rtl/road_box_age_overlay.v',
            ROOT / 'reference.py', ROOT / 'self_check.py', ROOT / 'interface_contract.txt']


def frame(name):
    """合成测试图，不包含训练/验证集，不是识别精度证据。"""
    if name in ('zero', 'full255', 'center128'):
        value = {'zero': 0, 'full255': 255, 'center128': 128}[name]
        return bytes([value]) * ref.INPUT_BYTES
    if name == 'random_seed42':
        return random.Random(42).randbytes(ref.INPUT_BYTES)
    colors = ((255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0),
              (255, 0, 255), (0, 255, 255), (255, 255, 255), (0, 0, 0))
    data = bytearray()
    for y in range(720):
        for x in range(1280):
            if name == 'colorbars':
                pixel = colors[x // 160]
            elif name == 'numbered':
                pixel = (x & 255, y & 255, (x // 4 + 17 * y) & 255)
            elif name == 'checkerboard':
                value = 255 * ((x + y) % 2)
                pixel = (value, 255 - value, value)
            elif name == 'four_borders':
                pixel = (255 * (x in (0, 1279)), 255 * (y in (0, 719)),
                         255 * (x in (0, 1279) and y in (0, 719)))
            elif name == 'double_rounding_witness':
                value = 3 if x % 5 == 4 else 0
                pixel = (value, value, value)
            else:
                raise ValueError(name)
            data.extend(pixel)
    return bytes(data)


def require_reject(events):
    try:
        ref.resize_awb96(events)
    except ValueError:
        return
    raise AssertionError('invalid frame accepted')


def self_check(work):
    # Fraction.round提供独立的精确RNE oracle，无浮点误差。
    assert all(ref.round_sum25(value) == round(Fraction(value, 25)) for value in range(6376))
    for value in (-1, 6376):
        try:
            ref.round_sum25(value)
        except ValueError:
            pass
        else:
            raise AssertionError('out-of-range sum accepted')
    results = []
    names = ('zero', 'full255', 'center128', 'colorbars', 'numbered', 'checkerboard',
             'four_borders', 'random_seed42', 'double_rounding_witness')
    for index, name in enumerate(names):
        source = frame(name)
        start = perf_counter()
        direct = ref.resize_rgb888(source)
        streamed, metrics = ref.resize_awb96(ref.awb96_events(
            source, sof_with_valid=index % 2 == 0, bubble_every=19))
        assert direct == streamed and len(direct) == 110592
        assert metrics['horizontal_phase_beat_counts'] == [46080] * 5
        assert metrics['horizontal_completion_lane_counts_low_to_high'] == [46080] * 4
        signed = ref.centered_int8(direct)
        assert len(signed) == 110592 and all(b == a - 128 for a, b in zip(direct, signed))
        records = list(ref.output_records(direct))
        assert len(records) == 36864 and sum(item['sof'] for item in records) == 1
        assert sum(item['eol'] for item in records) == 144 and sum(item['eof'] for item in records) == 1
        reconstructed = bytearray()
        for position, item in enumerate(records):
            assert item['lane_mask'] == 1 and item['x'] == position % 256 and item['y'] == position // 256
            assert item['pixels'] < (1 << 24)
            reconstructed.extend(item['pixels'].to_bytes(3, 'little'))
        assert reconstructed == direct and records[-1]['x'] == 255 and records[-1]['y'] == 143
        if name == 'zero': assert signed[0] == -128
        if name == 'full255': assert signed[0] == 127
        if name == 'center128': assert not any(signed)
        if name == 'double_rounding_witness': assert set(direct) == {1}
        directory = work / name
        directory.mkdir()
        (directory / 'source.rgb888.zlib').write_bytes(zlib.compress(source))
        (directory / 'golden.rgb888').write_bytes(direct)
        (directory / 'golden.int8').write_bytes(signed.tobytes())
        item = {'name': name, 'source_sha256': digest(source), 'RGB_sha256': digest(direct),
                'INT8_sha256': digest(signed.tobytes()), 'RGB_bytes': len(direct),
                'directory': str(directory.relative_to(ROOT)), 'metrics': metrics,
                'CPU_seconds_direct_and_stream_and_checks': perf_counter() - start}
        results.append(item)
        save(work / 'progress.json', results)
        print('PASS', name, len(direct), flush=True)
    zero = bytes(ref.INPUT_BYTES)
    prefix = lambda count: islice(ref.awb96_events(zero), count)
    invalid = (
        (), ((0, True, False, False),), ((0, False, True, True),),
        ((0, True, True, True),), ((1 << 96, True, True, False),),
        prefix(319), prefix(321),
        chain(prefix(2), ((0, False, True, False),)),
        chain(prefix(319), ((0, True, False, False),)),
        chain(ref.awb96_events(zero), ((0, True, False, False),)))
    for events in invalid:
        require_reject(events)
    for bad in (bytes(110591), ref.centered_int8(bytes(110592))):
        try:
            ref.centered_int8(bad)
        except ValueError:
            pass
        else:
            raise AssertionError('bad shape or second signed centering accepted')
    # 5x5中每行[0,0,0,0,3]：先舍入512四点[0,1;0,1]再减半得到0，直接得到1。
    old_values = [round(Fraction(value, 25)) for value in (0, 30, 0, 30)]
    assert round(Fraction(sum(old_values), 4)) == 0 and ref.round_sum25(15) == 1
    return {'status': 'PASS_CPU_REFERENCE_ONLY', 'cases': results, 'frame_cases': len(results),
            'RGB_byte_comparisons': len(results) * 110592, 'RNE_sum_cases': 6376,
            'rejected_frame_cases': 10, 'centering_negative_cases': 2,
            'double_rounding_witness': {'source_5x5_sum': 15, 'direct': 1, 'via_rounded512_then_half': 0},
            'not_evidence_of': ['RTL cycle timing', 'resource mapping', 'DDR visibility', 'CNN accuracy', 'FPS', 'board']}


def main():
    started = perf_counter()
    paths = input_paths()
    before = {str(path): digest(path.read_bytes()) for path in paths}
    common = json.loads(CONTRACT.read_text(encoding='utf-8'))
    assert common['input_tensor']['bytes'] == ref.OUTPUT_BYTES
    assert common['input_tensor']['width'] == 256 and common['input_tensor']['height'] == 144
    assert common['resize']['divisor'] == 25 and common['resize']['rounding'] == 'nearest_even_once'
    display = PRODUCTION / 'box_overlay_joint_20261016'
    old = json.loads((display / 'artifact_hashes.json').read_text(encoding='utf-8'))
    # 封存既有收据及关键源；不重跑18帧、不再次散列全部大型波形库。
    for name in ('status.json', 'handoff.txt', 'verification/summary.json',
                 'source_manifest.json', 'rtl/road_box_line_overlay.v', 'rtl/road_box_age_overlay.v'):
        assert digest((display / name).read_bytes()) == old[str(Path(name))]
    assert json.loads((display / 'verification/summary.json').read_text(encoding='utf-8'))['main_frames'] == 18
    save(ROOT / 'inputs.json', {'files': before, 'display_full_artifact_index': str(display / 'artifact_hashes.json'),
        'display_regression_rerun': False, 'closure_note': 'full previous manifest retained; selected source and receipt hashes verified'})
    work = ROOT / 'runs' / (datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ_') + uuid.uuid4().hex[:8])
    work.mkdir(parents=True)
    for name in ('reference.py', 'self_check.py', 'interface_contract.txt'):
        shutil.copyfile(ROOT / name, work / name)
    shutil.copyfile(CONTRACT, work / 'candidate_contract.json')
    receipt = {'status': 'FAIL', 'failure': 'not completed'}
    try:
        receipt = self_check(work)
    except Exception as exc:
        receipt = {'status': 'FAIL', 'failure': repr(exc)}
        raise
    finally:
        after = {str(path): digest(path.read_bytes()) for path in paths}
        receipt.update(source_unchanged=before == after, inputs_before=before, inputs_after=after,
                       Python_executable=sys.executable, Python_version=sys.version,
                       Python_SHA256=digest(Path(sys.executable).read_bytes()),
                       CPU_seconds_total=perf_counter() - started)
        save(work / 'receipt.json', receipt)
    assert receipt['source_unchanged']
    save(ROOT / 'golden_manifest.json', {'run': str(work.relative_to(ROOT)),
        'receipt': str((work / 'receipt.json').relative_to(ROOT)), 'receipt_sha256': digest((work / 'receipt.json').read_bytes()),
        'cases': receipt['cases'], 'contract_source_sha256': before[str(CONTRACT)]})
    save(ROOT / 'status.json', {'phase': 'REFERENCE_HANDOFF_READY', 'functional_reference_pass': True,
        'candidate': common['candidate_tag'], 'frames': receipt['frame_cases'], 'RGB_bytes_each': 110592,
        'report': str((work / 'receipt.json').relative_to(ROOT)), 'RTL_modified': False,
        'training_recalibration_TD_bitstream_board_Flash': False,
        'hardware_blockers': ['capture credit and slot metadata ordering', 'real write_visible', 'last response consumption and reset drain'],
        'RTL_gates': {key: 'NOT_RUN' for key in ('compile','ast','readability','comment','naming','profile','testbench','toolchain')}})
    print('REFERENCE_HANDOFF', work / 'receipt.json', flush=True)


if __name__ == '__main__':
    main()
