
from pathlib import Path
from datetime import datetime
from collections import Counter
import argparse
import hashlib
import json
import re
import xml.etree.ElementTree as ET
import zlib

OUT=Path(__file__).parent
ART=OUT.parent
ROOT=Path(__file__).resolve().parents[2]
RUN=ROOT/'build/route'
def read(path):
 return json.loads(path.read_text(encoding='utf-8-sig'))
def binding(path):
 data=path.read_bytes()
 return dict(path=str(path),size=len(data),sha256=hashlib.sha256(data).hexdigest(),crc32=f'{zlib.crc32(data):08x}')
def main():
 parser=argparse.ArgumentParser()
 parser.add_argument('--require-checked',action='store_true')
 args=parser.parse_args()
 freeze=read(ART/'scalar_gate_source_before.json')
 inputs={};project_scripts={};unresolved=[]
 for entry in freeze:
  path=ROOT/entry['relative']; relative=entry['relative']
  if not path.is_file() or binding(path)['sha256']!=entry['sha256']:unresolved.append('FROZEN_SOURCE_CHANGED: '+relative)
  (project_scripts if relative.startswith('scripts/') else inputs)[relative]=binding(path)
 counts=read(ART/'release_counts.json')
 assert len(inputs)==counts['inputs'] and len(project_scripts)==counts['project_scripts']
 references=[];excluded_metadata=[]
 text=(ROOT/'td_project/ball_face.al').read_text(encoding='utf-8-sig')
 for ref in re.findall(r'<File Path="([^"\n]+)"',text):
  path=(ROOT/'td_project'/ref).resolve()
  assert path.is_relative_to(ROOT) and path.is_file(),ref
  references.append(dict(declared=ref,resolved=str(path)))
 gate_paths={ROOT/entry['relative'] for entry in freeze}
 frozen_scripts={}
 flow={}
 FLOW_FILES=read(ART/'flow_files.json')
 for relative in FLOW_FILES:
  path=(ART/relative).resolve()
  assert path.is_relative_to(ART.resolve()) and path.relative_to(ART.resolve()).as_posix()==relative
  if path.is_file():flow[relative]=binding(path)
  else:unresolved.append('FLOW_PREPARATION_PENDING: '+relative)
 actual=read(ART/'selected_route_current.json')
 route_log=(ART/'route_auto_native.log').read_text(encoding='utf-8',errors='replace')
 selected_path=Path(actual['place_db']).as_posix()
 selected_crc=binding(Path(actual['place_db']))['crc32']
 if f'VERIFIED_SELECTED_CURRENT_PLACE={selected_path} CRC32={selected_crc}' not in route_log:unresolved.append('NATIVE_SELECTED_PLACE_BINDING_NOT_VERIFIED')
 if f'start command "import_db {selected_path}"' not in route_log:unresolved.append('NATIVE_IMPORTED_PLACE_PATH_MISMATCH')
 if binding(Path(actual['place_db']))['sha256']!=actual['place_db_sha256']:unresolved.append('SELECTED_PLACE_DB_CHANGED')
 if actual['selected']!='seed0_auto':unresolved.append('WRONG_SELECTED_TRIAL')
                                                                                            
 route_parameters=RUN/'final_applied_route_params.rpt'
 parameter_text=route_parameters.read_text(encoding='utf-8-sig')
 for name,value in [('effort','normal'),('timing','on'),('fix_hold','on'),('post_route_opt','on')]:
  if not re.search(r'^\s*'+name+r'\s*\|\s*'+value+r'\s*\|',parameter_text,re.M):unresolved.append('ACTUAL_ROUTE_PARAMETER_CHANGED: '+name)

 for path in [RUN/'routed.db',RUN/'primary_checked.db',RUN/'checked.db',RUN/'qualification.pass',
              ART/'route_current_receipt.json',ART/'qualification_receipt.json']:
  if not path.is_file() or path.stat().st_size==0:unresolved.append('FINAL_EVIDENCE_PENDING: '+str(path))
 if (ART/'qualification_receipt.json').is_file() and not read(ART/'qualification_receipt.json').get('pass'):
  unresolved.append('QUALIFICATION_RECEIPT_NOT_PASSED')
 if (ART/'route_current_receipt.json').is_file() and not read(ART/'route_current_receipt.json').get('primary_timing_pass'):
  unresolved.append('ROUTE_RECEIPT_NOT_PASSED')
 selected_log=(ART/'place_auto_native.log').read_text(encoding='utf-8',errors='replace')
 clock_counts=[int(value) for value in re.findall(r'VERIFIED_ACTUAL_CLOCK_SET=(\d+)',selected_log)]
 if not clock_counts or set(clock_counts)!={19}:unresolved.append('CURRENT_SELECTED_CLOCK_SET_NOT_19')
 functional=read(ART/'functional_review.json')
 if not functional['native_equivalence_pass']:unresolved.append('FUNCTIONAL_REVIEW_NOT_PASSED')
 for name,case in functional['native_checks'].items():
  run=Path(case['run_dir'])
  if not case['pass_'] or binding(run/'simulation.log')['sha256']!=case['log_sha256']:unresolved.append('NATIVE_LOG_CHANGED: '+name)
  receipt=read(run/'source_receipt.json')
  if receipt['changed'] or binding(run/'source_receipt.json')['sha256']!=case['source_receipt_sha256']:unresolved.append('NATIVE_RECEIPT_CHANGED: '+name)
  for item in receipt['sources']:
   if binding(Path(item['path']))['sha256']!=item['sha256'].lower():unresolved.append('NATIVE_SOURCE_CHANGED: '+item['path'])
 for relative,digest in functional['unchanged_hardware_files'].items():
  if binding(ROOT/relative)['sha256']!=digest:unresolved.append('UNCHANGED_BACKEND_CHANGED: '+relative)

 static_fail=[item for item in unresolved if not item.startswith(('FINAL_EVIDENCE_PENDING:','FLOW_PREPARATION_PENDING:'))]
 result=dict(status='PENDING_PHYSICAL_AUDIT' if unresolved else 'READY_FOR_READ_ONLY_CHECKED_EXPORT_NOT_APPROVAL',
  created_local=datetime.now().astimezone().isoformat(),project=str(ROOT),run_dir=str(RUN),
  reviewer='本地验证工具',pending_or_unresolved=unresolved,static_failures=static_fail,
  input_bindings=inputs,script_bindings=project_scripts,flow_bindings=flow,
  counts=dict(inputs=len(inputs),project_scripts=len(project_scripts),flow_expected=len(FLOW_FILES),flow_present=len(flow)),
  gate_freeze=binding(ART/'scalar_gate_source_before.json'),
  frozen_suffix_counts=dict(Counter(Path(item['relative']).suffix for item in freeze)),
  project_al_references=references,reviewed_excluded_generator_metadata=excluded_metadata,selected_placement=binding(ART/'selected_route_current.json'),
  clock_contract='19 actual clocks;18 activity-bearing summary frequency rows; tif_c20_in derived12.075ns clock has no active endpoint but remains a required actual clock with parent derivation/period.',
  functional_receipt=binding(ART/'functional_review.json'),native_route_parameters=binding(route_parameters),final_approval=False)
 (OUT/'audit_scope_inventory.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
 print(json.dumps(dict(status=result['status'],counts=result['counts'],al_references=len(references),pending_or_unresolved=unresolved),ensure_ascii=False))
 if args.require_checked:
  if unresolved:raise SystemExit(2)
  checked=binding(RUN/'checked.db')
  (ART/'checked_binding.json').write_text(json.dumps(dict(status='BOUND_ONLY_NOT_APPROVED',checked_db_sha256=checked['sha256'],checked_db=checked,
    scope_inventory=binding(OUT/'audit_scope_inventory.json')),indent=2),encoding='utf-8')
 if static_fail:raise SystemExit(1)
if __name__=='__main__':main()
