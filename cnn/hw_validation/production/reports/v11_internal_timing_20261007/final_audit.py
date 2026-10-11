"""Check real source identity and preserve diagnostic/production boundaries."""
import json
from pathlib import Path
from guard import ROOT, PREVIOUS, check, digest

def main():
    frozen = check()
    names = ('road_mac_probe.v', 'road_round_shift.v', 'silu_shared_unit.v')
    cores = {name: digest(PREVIOUS / 'gates/source_closure' / name) for name in names}
    identities = {}
    for name in names + ('road_postprocess_stream.v', 'down2_overlap_tile_runner.v', 'road_postprocess_low_io_top.v'):
        current = (PREVIOUS / 'gates/source_closure' / name if name in names else
                   ROOT / ('physical' if name == 'road_postprocess_low_io_top.v' else 'rtl') / name)
        snapshot = ROOT / 'gates/source_closure' / name
        assert digest(current) == digest(snapshot), f'Gate/current mismatch: {name}'
        identities[name] = digest(current)
    for name in names + ('road_postprocess_stream.v', 'down2_overlap_tile_runner.v'):
        actual = ROOT / 'verification/regression_candidate' / name
        assert digest(actual) == identities[name], f'Simulation/current mismatch: {name}'
    markers = {
        'verification/regression_candidate/vsim_runner.log': 'TB_PASS_DOWN2_TILE cases=4',
        'verification/regression_candidate/vsim_postprocess_attempt3.log': 'TB_PASS_POSTPROCESS',
    }
    logs = {}
    for relative, marker in markers.items():
        path = ROOT / relative
        data = path.read_text(encoding='utf-8', errors='replace')
        assert marker in data and 'TB_FAIL_' not in data and 'TB_ERROR_' not in data, relative
        logs[relative] = digest(path)
    data = (ROOT / 'verification/regression_candidate/vsim_postprocess_attempt3.log').read_text(encoding='utf-8', errors='replace')
    assert sum('TB_RESET_AGE_PASS age=' in line for line in data.splitlines()) == 25
    copied = {}
    for path in sorted((ROOT / 'verification/regression_candidate/vectors').iterdir()):
        if path.is_file():
            original = PREVIOUS / 'verification/regression_candidate/vectors' / path.name
            assert digest(path) == digest(original), f'Vector mismatch: {path.name}'
            copied[path.name] = digest(path)
    physical = json.loads((ROOT / 'physical/physical_status.json').read_text(encoding='utf-8'))
    gates = json.loads((ROOT / 'gates/summary.json').read_text(encoding='utf-8'))
    prebuild = json.loads((ROOT / 'physical/prebuild_manifest.json').read_text(encoding='utf-8'))
    assert len(prebuild['source_read_order']) == 6
    for source in prebuild['source_read_order']:
        path = (ROOT / 'physical' / source['path']).resolve()
        assert digest(path) == source['sha256'] == identities[path.name], f'Physical/current mismatch: {path}'
    assert prebuild['clock_mhz'] == 100 and prebuild['speed_grade'] == '-3'
    assert prebuild['device'] == 'PH1P35MDG324' and not prebuild['bitstream_requested']
    assert not prebuild['constraints']['exceptions_added']
    assert (ROOT / 'physical/pr.db').is_file(), 'No real routed database'
    evidence = {str(path.relative_to(ROOT)): digest(path) for path in
                (ROOT / 'physical/prebuild_manifest.json', ROOT / 'physical/pr.db',
                 ROOT / 'physical/final_timing.rpt', ROOT / 'physical/physical_status.json',
                 ROOT / 'gates/summary.json')}
    result = {'status': 'IDENTITY_CHECKED_NOT_PRODUCTION_SIGNOFF', 'frozen': frozen,
              'source_sha256': identities, 'immutable_core_sha256': cores,
              'functional_logs': logs, 'same_vector_files': len(copied), 'vector_sha256': copied,
              'evidence_sha256': evidence, 'physical_status': physical,
              'strict_errors': {key: value['errors'] for key, value in gates.items()},
              'production_delivery_pass': False, 'full_model_pass': False,
              'five_fps_pass': False, 'bitstream_generated': False}
    with (ROOT / 'FINAL_AUDIT.json').open('x', encoding='utf-8') as stream:
        json.dump(result, stream, indent=2)
        stream.write('\n')
    print(json.dumps({'status': result['status'], 'vector_files': len(copied), 'frozen': frozen}))

if __name__ == '__main__':
    main()
