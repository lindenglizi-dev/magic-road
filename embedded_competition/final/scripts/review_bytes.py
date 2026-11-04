from pathlib import Path
import json,hashlib
A=Path(__file__).parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
r=json.loads((A/'functional_review.json').read_text(encoding='utf-8'))
assert r['native_equivalence_pass']
assert set(r['native_checks'])=={'tb_counter_equivalence','tb_counter_generic','tb_runtime_commit','tb_osd_visibility'}
for c in r['native_checks'].values():
 p=Path(c['run_dir']);assert c['pass_']
 assert sha(p/'simulation.log')==c['log_sha256'] and sha(p/'source_receipt.json')==c['source_receipt_sha256']
 receipt=json.loads((p/'source_receipt.json').read_text(encoding='utf-8'));assert not receipt['changed']
 for s in receipt['sources']:assert sha(Path(s['path']))==s['sha256']
for p,h in json.loads((A/'source_binding.json').read_text(encoding='utf-8')).items():assert sha(Path(p))==h
print('通过：源码与原生回归结果绑定检查')
