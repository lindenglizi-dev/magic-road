from pathlib import Path
import os,sys,subprocess,json,hashlib,zlib
A=Path(__file__).resolve().parent
R=A.parent
D=R/'build/route'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def save(name,value):(A/name).write_text(json.dumps(value,ensure_ascii=False,indent=2),encoding='utf-8')
def py(path,*args):subprocess.run([sys.executable,str(path),*args],cwd=R,check=True)
def td(script,log,marker):
 out=A/log
 with out.open('w',encoding='utf-8') as f:result=subprocess.run([os.environ['TD_EXEC'],str(script).replace('\\','/')],cwd=A,stdin=subprocess.DEVNULL,stdout=f,stderr=subprocess.STDOUT)
 text=out.read_text(encoding='utf-8',errors='replace')
 assert result.returncode==0 and marker in text,(script,'工具未返回通过标志')
 return result.returncode

def main():
 assert 'TD_EXEC' in os.environ and 'VIVADO_BIN' in os.environ,'请设置工具路径'
 assert not (R/'output/rebuilt/ball_algorithm_rebuilt.bit').exists() and not (D/'routed.db').exists(),'请使用新构建目录，保留已有结果'
 py(A/'prepare_manifest.py');py(A/'run_tests.py')
 td(A/'build.tcl','gate_native.log','PASS COMBINED_FIRST_GATE')
 save('scalar_gate_receipt.json',{'pass':True,'exit':0,'native_log_sha256':sha(A/'gate_native.log'),'gate_db_sha256':sha(R/'build/gate/gate.db')})
 td(A/'placement/seed0_auto/run.tcl','place_auto_native.log','PASS_PLACE_SCREEN_ONLY_NOT_ROUTED')
 p=A/'placement/seed0_auto/place.db';crc=f'{zlib.crc32(p.read_bytes()):08x}'
 save('selected_route_current.json',{'selected':'seed0_auto','place_db':str(p),'place_db_sha256':sha(p)})
 binding='set selected_place {'+p.as_posix()+'}\n'
 binding+='if {[file size $selected_place] != '+str(p.stat().st_size)+'} {error "布局文件大小变化"}\n'
 binding+='set h [open $selected_place rb]\nset c [format %08x [zlib crc32 [read $h]]]\nclose $h\n'
 binding+='if {$c ne "'+crc+'"} {error "布局文件内容变化"}\n'
 binding+='puts "VERIFIED_SELECTED_CURRENT_PLACE=$selected_place CRC32=$c"\n'
 (A/'placement/current_binding.tcl').write_text(binding,encoding='utf-8')
 td(A/'route_auto.tcl','route_auto_native.log','PASS FULL_APPLICATION_PRIMARY_SDC_SIGNOFF')
 save('route_current_receipt.json',{'exit':0,'primary_timing_pass':True,'native_log_sha256':sha(A/'route_auto_native.log'),'primary_checked_db_sha256':sha(D/'primary_checked.db')})
 td(A/'qualify.tcl','qualification_native.log','PASS_DUAL_VIEW_TIMING_QUALIFIED_NO_BITGEN')
 save('qualification_receipt.json',{'pass':True,'exit':0,'native_log_sha256':sha(A/'qualification_native.log'),'checked_db_sha256':sha(D/'checked.db')})
 py(A/'review_bytes.py');py(A/'audit/audit_preflight.py','--require-checked')
 td(A/'audit/run_checked_audit.tcl','audit/checked_clock_audit.log','CHECKED_CLOCK_EVIDENCE_EXPORTED_NOT_INDEPENDENTLY_APPROVED')
 for name in ['inspect_checked_clocks.py','review_checked_pad_por.py','review_checked_native.py','review_clock_warning_evidence.py']:py(A/'audit'/name)
 py(A/'audit/emit_current_review_receipt.py','--checked-db-sha256',sha(D/'checked.db'),'--scope-sha256',sha(A/'audit/audit_scope_inventory.json'))
 td(A/'bitgen.tcl','bitgen_native.log','PASS_FULL_APPLICATION_ETHERNET_BITSTREAM_GENERATED')
 print('位流生成完成，尚需上板验证。')
if __name__=='__main__':main()
