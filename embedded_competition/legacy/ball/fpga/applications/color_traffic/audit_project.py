from pathlib import Path
import re, hashlib, json

root = Path(__file__).resolve().parent
base = root.parents[1] / 'lab_ex1_mipi_hdmi_SC520 (2)/lab_ex1_mipi_hdmi_SC520/lab_ex1_mipi_hdmi'
manifests = [root/'td_project/camera_to_dsi_display.al'] + list((root/'td_project').glob('*_Runs/*/*.prj'))
for manifest in manifests:
    text = manifest.read_text(encoding='utf-8')
    paths = re.findall(r'<File Path="([^"]+)"', text)
    resolved = [(manifest.parent/p).resolve() for p in paths]
    for p in resolved:
        assert p.exists(), (manifest, p)
        assert p.is_relative_to(root), (manifest, 'external dependency', p)
    for p in (root/'rtl').glob('*.v'):
        assert resolved.count(p.resolve()) == 1, (manifest, p)
changed=[]
for p in (base/'user_source').rglob('*'):
    if p.is_file():
        relative=p.relative_to(base)
        if p.read_bytes() != (root/relative).read_bytes(): changed.append(str(relative).replace('\\','/'))
assert set(changed)=={'user_source/hdl_source/isp/isp_top.v','user_source/hdl_source/design_top_wrapper.v','user_source/constraints_source/pin.adc'}, changed
pins=re.findall(r'LOCATION\s*=\s*([^;]+);',(root/'user_source/constraints_source/pin.adc').read_text(encoding='utf-8'))
assert len(pins)==len(set(pins)), 'duplicate pin'
hashes={str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (root/'rtl').glob('*.v')}
rtl_text='\n'.join(p.read_text(encoding='utf-8') for p in (root/'rtl').glob('*.v'))
assert len(re.findall(r'\bmodule\s+color_osd_assets_rom\b',rtl_text))==1, 'OSD ROM must be defined exactly once'
hashes['assets/anlogic_source.png']=hashlib.sha256((root/'assets/anlogic_source.png').read_bytes()).hexdigest()
(root/'reports/source_audit.json').write_text(json.dumps({'changed_baseline_files':changed,'rtl_sha256':hashes},indent=2),encoding='utf-8')
print('PASS project: 3 manifests, self-contained dependencies, 3 baseline integration edits, unique pins')
