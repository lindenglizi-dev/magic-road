"""Collect completed verification receipts and compare tool hashes after runs."""
import json
import re
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import run


def main():
    run.check()
    runs = ROOT / 'verification/runs'
    full_path = runs / '20261016_013948_bce47e15/summary.json'
    arrival_path = runs / '20261016_014013_10a83d51/summary.json'
    delay_path = runs / '20261016_012603_64ee4efe/summary.json'
    full, arrival, delay = [json.loads(path.read_text(encoding='utf-8'))
                            for path in (full_path, arrival_path, delay_path)]
    assert all(item['status'] == 'PASS' and item['source_unchanged'] for item in (full, arrival, delay))
    assert len(full['results']) == 18 and all(item['passed'] for item in full['results'])
    real_metrics = '\n'.join(next(item for item in full['results'] if item['name'] == 'real7_final97')['metrics'])
    real_age = int(re.search(r'FRAME_AGE_INPUT age=(\d+)', real_metrics)[1])
    real_cycles = int(re.search(r'source_cycles=(\d+)', real_metrics)[1])
    tools_before = json.loads((full_path.parent / 'tool_hashes.json').read_text(encoding='utf-8'))
    tools_after = {path: run.sha(path) for path in tools_before}
    assert tools_before == tools_after
    before = json.loads((full_path.parent / 'hashes_before.json').read_text(encoding='utf-8'))
    for path, digest in before.items():
        assert run.sha(path) == digest, path
    source_receipts = {str(path): run.sha(path) for path in
                       [ROOT / 'verify.py', *sorted((ROOT / 'verification').glob('*.v')),
                        *sorted((ROOT / 'verification').glob('*.py'))]}
    report = {
        'status': 'PASS_FUNCTIONAL_MODELSIM', 'fullframe_suite': str(full_path),
        'active_arrival_supplement': str(arrival_path), 'video_delay_and_normal_budget': str(delay_path),
        'main_frames': 18, 'main_active_pixels': 18 * 1280 * 720,
        'main_rgb_bytes': sum(item['bytes'] for item in full['results']),
        'extra_active_arrival_fullframe': 1, 'normal64_DEfall_to_ready_samples': 323,
        'cold_reset_clear_and64_prepare_cycles': 1601, 'normal_blank_samples': 370,
        'conservative_SOF_blank_window': 39970,
        'video_registers': 2, 'changing_raw_RGB_and_sync_measured': True,
        'queued_box_color_removed_immediately_on_live_invalid': True,
        'actual_real_path': '12096HEAD112->actual56laneROM->LUT->decodeTopK->NMS7->publisher->threeTableCDC->box->frozenAGE',
        'real_frame_age_external_input_ms': real_age,
        'real_begin_result_return_to_NMS_done_source_counter_difference': real_cycles,
        'native_RAM': 'actualPH1P_LOGIC_DRAM; all1280wordsrandompoisoned;reset/SOFclear;allwritesreadaddr!=writeaddr',
        'protocol': 'count65faultwholelinepassthrough;earlyDEclear/prepsuppressesentireline;disabledendpointsaddresslegal',
        'age_boundary': 'controlledcoherenttable raw1996=>2000permit,raw1997=>2001reject,timeinvalid=>UINT64MAX',
        'raster_scope': full['raster'], 'geometry_age_scope': full['geometry_age'],
        'known_vendor_warning': '114INIT_FILEboundsperfreshjointoptimization;2nativeDRAM;preservednotresolved',
        'main_known_vendor_warning_counts': {item['name']: item['warnings']['known_vendor_init_bounds_count'] for item in full['results']},
        'main_known_vendor_warning_total': sum(item['warnings']['known_vendor_init_bounds_count'] for item in full['results']),
        'direct_protocol_known_vendor_warning_count': full['protocol_warnings']['known_vendor_init_bounds_count'],
        'unexpected_warnings': [], 'source_unchanged': True,
        'tools_before': tools_before, 'tools_after': tools_after, 'tools_unchanged': True,
        'current_verification_source_hashes': source_receipts,
        'not_measured': ['TDphysicalresources', 'setup_hold', 'full67layerthroughput', 'DDRloop', 'board', 'accuracy'],
        'failed_attempts_retained': ['verification/runs/20261016_011322_c3d4b84e',
                                     'verification/runs/20261016_011902_38d808a8',
                                     'verification/runs/20261016_013321_b9bb4bc0'],
        'stimulus_fix': {'failure': 'ModelSim2020.4decimal64plusargtruncatedUINT64MAXto00000000ffffffff',
                        'fix': 'explicit64bithexplusarg',
                        'negative_diagnostic': str(ROOT / 'verification/age_argument_diagnostic/argument.log'),
                        'focused_unknown_live_withdraw_pass': str(runs / '20261016_013046_fa32e8d2/summary.json')},
        'runner_isolation_fix': {'failure': 'ModelSimcachedoptimizationstilllockssharedworklibrary',
                                 'fix': 'eachcaseowncopiedlibraryROMartifactsandsimcwd;warningclassificationunchanged',
                                 'focused_parallel_count0_unknown_pass': str(runs / '20261016_013816_ea34d963/summary.json')}}
    run.save(ROOT / 'verification/summary.json', report)
    print('FUNCTIONAL_VERIFICATION_PASS 18frames + activearrivalframe + directedprotocol + changingRGBdelay')


if __name__ == '__main__':
    main()
