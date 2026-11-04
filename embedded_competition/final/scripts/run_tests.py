from pathlib import Path
import os,shutil,subprocess,json,hashlib,sys
R=Path(__file__).resolve().parent.parent
A=R/'scripts'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 binpath=Path(os.environ['VIVADO_BIN'])
 common=[str(p) for p in (R/'rtl').glob('*.v')]
 ref=R/'tests/rtl'
 common += [str(p) for p in ref.glob('reference*.v')]
 checks={}
 for name in ['tb_counter_equivalence','tb_counter_generic','tb_runtime_commit','tb_osd_visibility']:
  out=R/'build/tests'/name;out.mkdir(parents=True,exist_ok=True)
  for p in ref.glob('*.hex'):shutil.copy2(p,out/p.name)
  sources=common+[str(ref/(name+'.v'))]
  before=[{'path':p,'sha256':sha(Path(p))} for p in sources]
  env=dict(os.environ,TEMP=str(out),TMP=str(out))
  for command,log in [('xvlog', 'compile.log'),('xelab','elaborate.log'),('xsim','simulation.log')]:
   args={'xvlog':sources,'xelab':[name,'-s','checked','-mt','off','-timescale','1ns/1ps'],'xsim':['checked','-runall']}[command]
   with (out/log).open('w',encoding='utf-8') as f:subprocess.run([str(binpath/(command+'.bat'))]+args,cwd=out,env=env,stdout=f,stderr=subprocess.STDOUT,check=True)
  log=(out/'simulation.log').read_text(encoding='utf-8',errors='replace')
  assert 'PASS' in log and 'Fatal:' not in log and 'Error:' not in log,name
  changed=[x for x in before if sha(Path(x['path']))!=x['sha256']];assert not changed
  receipt=out/'source_receipt.json';receipt.write_text(json.dumps({'sources':before,'changed':changed},indent=2),encoding='utf-8')
  checks[name]={'run_dir':str(out),'pass_':True,'log_sha256':sha(out/'simulation.log'),'source_receipt_sha256':sha(receipt)}
  print('通过',name)
 (A/'functional_review.json').write_text(json.dumps({'native_equivalence_pass':True,'scope':'计数器、提交控制和显示对照；结果完成脉冲由测试驱动，不代表实物识别验收。','native_checks':checks,'unchanged_hardware_files':{}},ensure_ascii=False,indent=2),encoding='utf-8')
if __name__=='__main__':main()
