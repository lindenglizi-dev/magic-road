
from pathlib import Path
from datetime import datetime
import hashlib
import json
import re
import tkinter

OUT=Path(__file__).parent
ART=OUT.parent
ROOT=Path(__file__).resolve().parents[2]
RUN=ROOT/'build/route'
def read(path):return path.read_text(encoding='utf-8-sig')
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def load(path):return json.loads(read(path))
def main():
 scope=load(OUT/'audit_scope_inventory.json')
 assert not scope['pending_or_unresolved'], 'PENDING: source/flow/route/qualification prerequisites are incomplete'
 assert scope['counts']==load(ART/'release_counts.json')
 for group,base in [('input_bindings',ROOT),('script_bindings',ROOT),('flow_bindings',ART)]:
  for relative,entry in scope[group].items():
   assert sha(base/relative)==entry['sha256'],(group,relative)
 binding=load(ART/'checked_binding.json')
 assert sha(RUN/'checked.db')==binding['checked_db_sha256']
 assert sha(OUT/'audit_scope_inventory.json')==binding['scope_inventory']['sha256']
 gate=load(ART/'scalar_gate_receipt.json')
 route=load(ART/'route_current_receipt.json')
 qualified=load(ART/'qualification_receipt.json')
                                                                                 
                                                                                          
 assert gate['pass'] and gate['exit']==0
 assert sha(ART/'gate_native.log')==gate['native_log_sha256']
 assert sha(ROOT/'build/gate/gate.db')==gate['gate_db_sha256']
 assert route['primary_timing_pass'] and route['exit']==0
 assert sha(ART/'route_auto_native.log')==route['native_log_sha256']
 assert sha(RUN/'primary_checked.db')==route['primary_checked_db_sha256']
 assert qualified['pass'] and qualified['exit']==0
 assert sha(ART/'qualification_native.log')==qualified['native_log_sha256']
 assert sha(RUN/'checked.db')==qualified['checked_db_sha256']
 for source,digest in load(ART/'source_binding.json').items():assert sha(Path(source))==digest
 assert sha(RUN/'routed.db')==sha(RUN/'primary_checked.db')
 marker=RUN/'qualification.pass'
 assert read(marker).splitlines()[0]=='PASS FULL_APPLICATION_TWO_VIEW_TIMING_QUALIFIED'
 assert marker.stat().st_mtime>=(RUN/'checked.db').stat().st_mtime
 qualifier=read(ART/'qualify.tcl')
 procedures=qualifier[qualifier.index('proc read_bytes'):qualifier.index('\ncd $run_dir')]
 tcl=tkinter.Tcl();tcl.eval(procedures);tcl.eval('proc puts args {}')
 baseline=tcl.call('require_active_exceptions',str(RUN/'frozen_placed_exceptions.timing'),0)
 paths=[ART/'scalar_gate_source_before.json',ART/'scalar_gate_receipt.json',ART/'route_current_receipt.json',ART/'qualification_receipt.json',
        OUT/'audit_scope_inventory.json',ART/'checked_binding.json',ART/'qualify.tcl',ART/'source_binding.json',RUN/'checked.db',RUN/'routed.db',RUN/'primary_checked.db',marker]
 for name,folder,hold in [('candidate_final.timing',RUN,1),('qualification_primary.timing',RUN,1),
    ('qualification_pure_data7.timing',RUN,0),('qualification_restored_primary.timing',RUN,1),
    ('checked_clock_summary.timing',OUT,1)]:
  path=folder/name;tcl.call('require_global',str(path),hold);paths.append(path)
 for name,folder,pure in [('candidate_exception.timing',RUN,0),('qualification_primary_exceptions.timing',RUN,0),
    ('qualification_pure_data7_exceptions.timing',RUN,1),('qualification_restored_primary_exceptions.timing',RUN,0),
    ('checked_exceptions.timing',OUT,0)]:
  path=folder/name;tcl.call('require_active_exceptions',str(path),pure,baseline);paths.append(path)
 pairs={}
 for suffix,count in [('init8',8),('sys50_usr',116),('usr_sys50',-1)]:
  primary=tcl.call('require_pair',str(RUN/f'qualification_primary_{suffix}.timing'),count,count,0,'' if suffix=='usr_sys50' else '0.000')
  actual=int(tcl.call('dict','get',primary,'Max'))
  identities=list(tcl.splitlist(tcl.call('dict','get',primary,'MaxEndpoints')))
  assert actual==len(identities) and actual>0
  pairs[suffix]=dict(paths=actual,max_endpoints=identities)
  for name,folder,pure in [(f'qualification_primary_{suffix}.timing',RUN,0),
                          (f'qualification_pure_data7_{suffix}.timing',RUN,1),(f'checked_{suffix}.timing',OUT,0)]:
   path=folder/name
   result=tcl.call('require_pair',str(path),actual,0 if pure else actual,pure,'' if suffix=='usr_sys50' else '0.000')
   assert list(tcl.splitlist(tcl.call('dict','get',result,'MaxEndpoints')))==identities,path
   paths.append(path)
  if suffix=='sys50_usr':
   path=RUN/'qualification_restored_primary_sys50_usr.timing'
   restored=tcl.call('require_pair',str(path),actual,actual,0,'0.000')
   assert list(tcl.splitlist(tcl.call('dict','get',restored,'MaxEndpoints')))==identities
   paths.append(path)
 assert sha(OUT/'actual_checked.sdc')==sha(RUN/'qualification_restored_primary.sdc')
 log=read(OUT/'checked_clock_audit.log')
 assert 'CHECKED_CLOCK_EVIDENCE_EXPORTED_NOT_INDEPENDENTLY_APPROVED' in log
 assert 'start command "import_db '+(RUN/'checked.db').as_posix()+'"' in log
 assert not re.search(r'(?m)^(?:RUN|PHY|USR)-\d+[^\n]*(?:ERROR|FATAL)',log)
 assert not re.search(r'(?m)^USR-6135\b',log)
 start=log.index('start command "report_route_status -drc -file checked_drc.rpt"')
 end=log.index('start command "export_sdc -file actual_checked.sdc"',start)
 drc=log[start:end]
 for phrase in ['Lut Bridge Check','Physical Net Status Check','No multi-drive.','Clock Net Status Check','No abnormal timing path.']:
  assert phrase in drc,phrase
 for stage in ['Lut Bridge Check','Physical Net Status Check','Clock Net Status Check','Abnormal Timing Path check']:
  assert re.search(r'End Stage [0-9]+ \| '+re.escape(stage)+';',drc),stage
 assert not re.search(r'(?im)^.*\b(?:ERROR|FATAL|open nets?|unrouted)\b.*[1-9][0-9]*',drc)
 route_log=read(ART/'route_auto_native.log')
 assert 'over cnt = 0(0%), over = 0, worst = 0' in route_log
 assert 'PASS FULL_APPLICATION_PRIMARY_SDC_SIGNOFF' in route_log
 assert 'PASS_DUAL_VIEW_TIMING_QUALIFIED_NO_BITGEN' in read(ART/'qualification_native.log')
 coverage=read(OUT/'checked_clock_checks.rpt')
 original=ART/'fixtures/coverage_contract.txt'
 expected_header=read(original).split('\n\n',1)[0]
 assert coverage.split('\n\n',1)[0]==expected_header
 no_paths=coverage[coverage.index('8. checking no path constraints.'):coverage.index('9. checking path exception constraints')]
 actual_no_paths=[line.strip() for line in no_paths.splitlines() if line.strip().startswith('set_')]
 assert actual_no_paths==[
  'set_max_delay -datapath_only -from [get_clocks MIPI_RX_BYTE_CLK] -to [get_clocks ETH_TX_CLK] 7.000',
  'set_false_path -hold -from [get_clocks MIPI_RX_BYTE_CLK] -to [get_clocks ETH_TX_CLK] 7.000']

 summary=read(OUT/'checked_clock_summary.timing')
 timing={key:float(re.search(key+r':\s*(-?[0-9.]+)ns',summary)[1]) for key in ('SWNS','STNS','HWNS','HTNS')}
 assert min(timing.values())>=0 and timing['STNS']==timing['HTNS']==0
 assert 'Check Corner        : Both (Slow and Fast)' in summary
 for condition in ['Slow     | yes      yes','Fast     | yes      yes']:assert condition in summary
 paths.extend([OUT/'checked_clock_audit.log',OUT/'checked_clock_summary.timing',OUT/'checked_clock_checks.rpt',
    OUT/'actual_checked.sdc',RUN/'qualification_restored_primary.sdc',ART/'route_auto_native.log',ART/'qualification_native.log',
    RUN/'frozen_placed_exceptions.timing',original,Path(__file__)])
 report=dict(status='PASS_CURRENT_SOURCE_PRIMARY_TWO_VIEW_ENDPOINTS_AND_COVERAGE',
  created_local=datetime.now().astimezone().isoformat(),reviewer='本地验证工具',project=str(ROOT),
  source_freeze='PASS',coverage='PASS',hardware_inputs=scope['counts']['inputs'],project_scripts=scope['counts']['project_scripts'],actual_flow_files=scope['counts']['flow_present'],
  global_setup_hold_ns=timing,coverage_percent=float(re.search(r'STA coverage\s*:\s*([0-9.]+)%',summary)[1]),
  coverage_floor_percent=98.66,whole_pair_checks=pairs,same_endpoint_identity_across_views=True,
  drc_evidence=dict(native_physical_checks_completed_without_routing_open_multidrive_abnormal_failure=True,
    actual_report=str(OUT/'checked_clock_audit.log'),standalone_report_exists=(OUT/'checked_drc.rpt').is_file(),
    note='Native stdout DRC checks are bound; retained PHY5079/5088 warnings require the separate physical clock-graph review.'),
  evidence_sha256={str(path):sha(path) for path in paths},unresolved=[],
  scope='Offline current physical/source/coverage review only; pad/POR and clock reviews must independently finish before final receipt. Strict style and board acceptance are separate.')
 (OUT/'checked_primary_source_coverage_review.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
 print(report['status']);print(timing)
if __name__=='__main__':main()
