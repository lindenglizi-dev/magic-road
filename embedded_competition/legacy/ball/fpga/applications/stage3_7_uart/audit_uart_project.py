"""Validate the V2 graph, deleted legacy modules, local sources and UART pins."""
from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parent
BASE = ROOT.parent / 'stage3_7_keys'
baseline = json.loads((ROOT/'reports/source_baseline.json').read_text())
for name, digest in baseline.items():
    assert hashlib.sha256((BASE/name).read_bytes()).hexdigest() == digest, f'Original changed: {name}'
changed = {
    'rtl/key_mode_control.v', 'rtl/stage3_7_runtime.v',
    'user_source/hdl_source/design_top_wrapper.v',
    'user_source/hdl_source/isp/isp_top.v',
    'user_source/constraints_source/pin.adc',
    'rtl/algorithm_label_osd.v',
    'user_source/hdl_source/awb.v',
}
retired = {
    'binary_open_4px', 'binary_close_4px', 'binary_denoise_4px', 'binary_fill_holes_4px',
    'binary_cleanup_4px', 'binary_cleanup_stream_4px', 'binary_morph_top',
    'gray_filter_stream_4px', 'gaussian_filter_4px', 'image_algorithm_stage7_96',
}
for name in retired:
    assert not (ROOT/'rtl'/f'{name}.v').exists(), f'Retired module remains: {name}'
for name, digest in baseline.items():
    if name.startswith(('rtl/', 'user_source/')) and name not in changed:
        if Path(name).stem in retired:
            continue
        assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest() == digest, f'Unexpected copy edit: {name}'
for project in [ROOT/'td_project/camera_to_dsi_display.al', *ROOT.glob('td_project/*_Runs/*/*.prj')]:
    text = project.read_text(encoding='utf-8')
    assert 'applications/stage3_7_keys' not in text
    files = re.findall(r'<File Path="([^"]+)"', text)
    assert not any(Path(name).stem in retired for name in files), 'Retired source still compiled'
    for name in files:
        path = (project.parent / name).resolve()
        assert path.is_relative_to(ROOT), (project, path)
        assert path.is_file(), path
    for name in ['uart_rx.v', 'uart_mode_protocol.v', 'uart_mode_link.v', 'gray_median_4px.v', 'rgb_point_adjust_4px.v',
                 'uart_frame_rx.v','uart_frame_tx.v','vision_uart_control.v','vision_video_control.v',
                 'color_traffic_core.v','roi_border_overlay.v','image_upload_engine.v','image_ddr_bridge.v','pc_image_replay.v']:
        assert sum(p.endswith('/'+name) for p in files) == 1
pins = re.findall(r'set_pin_assignment\s*\{\s*(.*?)\s*\}\s*\{\s*LOCATION\s*=\s*(\w+)',
                  (ROOT/'user_source/constraints_source/pin.adc').read_text())
assert len({pin for _,pin in pins}) == len(pins), 'Duplicate pin'
assert dict(pins)['I_uart_rx']=='J1' and dict(pins)['O_uart_tx']=='H1'
config=json.loads((ROOT/'pc_upper/config/algorithms.json').read_text(encoding='utf-8'))
assert config['protocol_version']==2
assert [item['command'] for item in config['modes']]==list(range(12))
assert all(item['name'].startswith(f'{i}. ') for i,item in enumerate(config['modes']))
assert len(json.loads((ROOT/'sim/osd_font.json').read_text(encoding='utf-8'))['labels'])==12
isp=(ROOT/'user_source/hdl_source/isp/isp_top.v').read_text(encoding='utf-8')
assert '.camera_rgb(awb_O_tdata)' in isp and '.I_rgb(process_rgb)' in isp, 'Camera path must retain official AWB output'
assert '.I_rgb(awb_uncorrected)' not in isp, 'Uncorrected sensor RGB must not drive original mode'
original=(ROOT.parent/'color_traffic/rtl/color_traffic_core.v').read_text(encoding='utf-8')
adapted=(ROOT/'rtl/color_traffic_core.v').read_text(encoding='utf-8')
for func in ('classify','palette'):
    pattern=r'function\s+\[[^\]]+\]\s+'+func+r';.*?endfunction'
    assert re.search(pattern,original,re.S)[0]==re.search(pattern,adapted,re.S)[0], 'ROI color math changed'
assert original[original.index(' winner=0;'):original.index(' always @(posedge')]==adapted[adapted.index(' winner=0;'):adapted.index(' always @(posedge')], 'ROI thresholds/voting changed'
print(f'PASS V2 modes/OSD/config, local source lists, UART J1/H1, camera AWB tap, preserved ROI thresholds/voting, baseline algorithm/DDR files')
