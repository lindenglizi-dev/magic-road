from pathlib import Path
import json,hashlib
A=Path(__file__).resolve().parent
R=A.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 files=[]
 for root in ['rtl','ethernet','user_source','td_project','pc_app','tests']:
  for p in sorted((R/root).rglob('*')):
   if p.is_file() and '__pycache__' not in p.parts:files.append(p)
 for p in sorted(A.rglob('*')):
  if p.is_file() and p.suffix in {'.py','.ps1','.tcl','.adc','.txt'} and p.name not in {'source_counts.tcl','current_binding.tcl'}:files.append(p)
 entries=[{'path':str(p),'relative':p.relative_to(R).as_posix(),'sha256':sha(p)} for p in files]
 (A/'scalar_gate_source_before.json').write_text(json.dumps(entries,indent=2),encoding='utf-8')
 (A/'source_binding.json').write_text(json.dumps({str(p):sha(p) for p in files},indent=2),encoding='utf-8')
 flows=[p.relative_to(A).as_posix() for p in files if p.is_relative_to(A)]
 counts={'inputs':sum(not e['relative'].startswith('scripts/') for e in entries),'project_scripts':len(flows),'flow_expected':len(flows),'flow_present':len(flows)}
 (A/'flow_files.json').write_text(json.dumps(flows,indent=2),encoding='utf-8')
 (A/'release_counts.json').write_text(json.dumps(counts,indent=2),encoding='utf-8')
 (A/'source_counts.tcl').write_text('set release_input_count '+str(counts['inputs'])+'\nset release_script_count '+str(len(flows))+'\nset release_flow_files {'+' '.join(flows)+'}\n',encoding='utf-8')
 print('输入清单已建立',counts)
if __name__=='__main__':main()
