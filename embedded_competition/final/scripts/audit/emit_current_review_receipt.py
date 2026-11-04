
from pathlib import Path
from datetime import datetime
import argparse
import hashlib
import json
import tkinter
import zlib

OUT=Path(__file__).parent
ART=OUT.parent
ROOT=Path(__file__).resolve().parents[2]
RUN=ROOT/'build/route'
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def load(path):return json.loads(path.read_text(encoding='utf-8-sig'))
def main():
 parser=argparse.ArgumentParser()
 parser.add_argument('--checked-db-sha256',required=True)
 parser.add_argument('--scope-sha256',required=True)
 args=parser.parse_args()
 checked=RUN/'checked.db';scope_path=OUT/'audit_scope_inventory.json'
 assert sha(checked)==args.checked_db_sha256.lower()
 assert sha(scope_path)==args.scope_sha256.lower()
 scope=load(scope_path)
 assert not scope['pending_or_unresolved'] and not scope['static_failures']
 assert scope['counts']==load(ART/'release_counts.json')
 primary_path=OUT/'checked_primary_source_coverage_review.json'
 pad_path=OUT/'checked_pad_por_review.json'
 clock_path=OUT/'checked_clock_warning_review.json'
 primary,pad,clock=[load(path) for path in [primary_path,pad_path,clock_path]]
 assert primary['source_freeze']==primary['coverage']=='PASS' and not primary['unresolved']
 assert primary['drc_evidence']['native_physical_checks_completed_without_routing_open_multidrive_abnormal_failure']
 assert pad['pad']==pad['por']=='PASS' and not pad['unresolved']
 assert clock['clock']=='PASS' and not clock['unresolved']
 assert pad['checked_db_sha256']==clock['checked_db_sha256']==sha(checked)
 evidence={}
 for path,review in [(primary_path,primary),(pad_path,pad),(clock_path,clock)]:
  for name,digest in review['evidence_sha256'].items():
   assert sha(Path(name))==digest.lower(),name
   assert name not in evidence or evidence[name]==digest.lower(),name
   evidence[name]=digest.lower()
  evidence[str(path)]=sha(path)
 for group,base in [('input_bindings',ROOT),('script_bindings',ROOT),('flow_bindings',ART)]:
  for relative,entry in scope[group].items():assert sha(base/relative)==entry['sha256'],(group,relative)
 import subprocess,sys
 functional_path=ART/'functional_review.json'
 before=sha(functional_path)
 subprocess.run([sys.executable,str(ART/'review_bytes.py')],check=True)
 assert sha(functional_path)==before,'Functional evidence changed since preflight'
 functional=load(functional_path)
 assert functional['native_equivalence_pass']
 evidence[str(functional_path)]=before
 for case in list(functional['native_checks'].values()):
  run=Path(case['run_dir'])
  for name,digest in [('simulation.log',case['log_sha256']),('source_receipt.json',case['source_receipt_sha256'])]:
   assert sha(run/name)==digest
   evidence[str(run/name)]=digest
 marker=RUN/'qualification.pass'
 assert marker.read_text().splitlines()[0]=='PASS FULL_APPLICATION_TWO_VIEW_TIMING_QUALIFIED'
 assert marker.stat().st_mtime>=checked.stat().st_mtime
 receipt_path=RUN/'independent_audit.receipt'
 assert not receipt_path.exists(),'Do not overwrite an approved receipt'
 tcl=tkinter.Tcl()
 def dictionary(*items):return tcl.call('dict','create',*items)
 def binding(path):
  data=path.read_bytes()
  return dictionary('path',str(path),'size',len(data),'crc32',f'{zlib.crc32(data):08x}','sha256',hashlib.sha256(data).hexdigest())
 reports={'source_freeze':primary_path,'drc':OUT/'checked_clock_audit.log','pad':pad_path,'clock':clock_path,'coverage':primary_path}
 groups={group:dictionary(*[item for relative in sorted(scope[group]) for item in (relative,binding(base/relative))])
         for group,base in [('input_bindings',ROOT),('script_bindings',ROOT),('flow_bindings',ART)]}
 report=dict(result='PASS',status='PASS_CURRENT_CHECKED_PHYSICAL_AUDIT',created_local=datetime.now().astimezone().isoformat(),
  reviewer='本地源码、时序、时钟、引脚与复位检查',
  root=str(ROOT),checked_db_sha256=sha(checked),scope_sha256=sha(scope_path),unresolved_findings=[],
  checks={name:'PASS' for name in reports},evidence_sha256=evidence,
  counts=scope['counts'],retained_clock_warnings=clock['reviewed_PHY5079_PHY5088'],
  limits=['No native TD/bitgen/board action performed by this binder.','Legacy strict formatter/style failures remain separate from real physical timing qualification.',functional['scope'], 'This run does not claim new recognition ground truth, complete DDR/IP replay or board acceptance.'])
 audit=dictionary('version','1','reviewer',report['reviewer'],'result','PASS','unresolved_findings','0',
  'checks',dictionary(*[item for name in reports for item in (name,'PASS')]),
  'checked_db',binding(checked),'primary_sdc',binding(ROOT/'td_project/camera_to_dsi_display.sdc'),
  'reports',dictionary(*[item for name,path in reports.items() for item in (name,binding(path))]),
  *[item for name,value in groups.items() for item in (name,value)])
 preview=OUT/'independent_audit_receipt_preview.txt'
 preview.write_text('PASS FULL_APPLICATION_INDEPENDENT_AUDIT\n'+str(tcl.call('format','%s',audit))+'\n',encoding='utf-8')
 consumer=(ART/'bitgen.tcl').read_text(encoding='utf-8-sig')
 procedures=consumer[consumer.index('proc audit_file_binding'):consumer.index('\nrequire_independent_audit "$run_dir/')]
 tcl.eval(procedures)
 tcl.setvar('project_root',ROOT.as_posix());tcl.setvar('execution_root',ART.as_posix())
 tcl.call('require_independent_audit',str(preview),str(checked),str(ROOT/'td_project/camera_to_dsi_display.sdc'))
 receipt_path.write_bytes(preview.read_bytes())
 tcl.call('require_independent_audit',str(receipt_path),str(checked),str(ROOT/'td_project/camera_to_dsi_display.sdc'))
 (OUT/'actual_independent_review.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
 print('PASS_BOUND_CURRENT_INDEPENDENT_AUDIT_OFFLINE_CONSUMER_VERIFIED_NO_BITGEN')
if __name__=='__main__':main()
