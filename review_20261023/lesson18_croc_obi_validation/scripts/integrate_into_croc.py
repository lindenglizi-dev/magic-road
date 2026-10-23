#!/usr/bin/env python3
"""Patch an UNMODIFIED Croc checkout at the official user_domain hook.
Idempotent; checks the exact expected source structure before editing.
Back up any user changes separately before running on a modified checkout.
"""
import pathlib, re, shutil, sys
src=pathlib.Path(__file__).resolve().parents[1]
if len(sys.argv)!=2:
    sys.exit('usage: python3 scripts/integrate_into_croc.py /path/to/croc')
croc=pathlib.Path(sys.argv[1]).resolve()
check=[croc/'rtl/user_domain.sv',croc/'rtl/user_pkg.sv',croc/'Bender.yml']
if not all(f.is_file() for f in check): sys.exit('Not a Croc checkout (expected user_domain.sv, user_pkg.sv and Bender.yml)')
user=check[0].read_text(); pkg=check[1].read_text(); bender=check[2].read_text()
inst='''  croc_gemm_obi i_gemm_obi (
    .clk_i      (clk_i),
    .rst_ni     (rst_ni),
    .obi_req_i  (user_design_obi_req),
    .obi_rsp_o  (user_design_obi_rsp)
  );'''
pattern=r'  obi_err_sbr #\([\s\S]*?\) i_your_design_goes_here \([\s\S]*?\n  \);'
if 'croc_gemm_obi i_gemm_obi' not in user:
    user,n=re.subn(pattern,lambda _:inst,user,count=1)
    if n!=1:sys.exit('Unexpected Croc user_domain template; edit integration manually')
# Shrink default huge UserDesign window and reserve 0x20000000 for ROM.
start='start_addr: croc_pkg::UserBaseAddr,'
end='end_addr:   croc_pkg::UserBaseAddr + 32\'h1000_0000'
if start in pkg and end in pkg:
    pkg=pkg.replace(start,'start_addr: croc_pkg::UserBaseAddr + 32\'h0000_1000,')
    pkg=pkg.replace(end, 'end_addr:   croc_pkg::UserBaseAddr + 32\'h0000_2000')
elif "start_addr: croc_pkg::UserBaseAddr + 32'h0000_1000" not in pkg:
    sys.exit('Unexpected Croc UserAddrMap: edit map manually')
# Bender order: modules before user_domain. Only one module list addition.
lines=['      - rtl/gemm_accel/mac_array_4x4.sv','      - rtl/gemm_accel/gemm_mmio_4x4.sv','      - rtl/gemm_accel/croc_gemm_obi.sv']
if 'rtl/gemm_accel/croc_gemm_obi.sv' not in bender:
    anchor='      - rtl/user_domain.sv'
    if bender.count(anchor)!=1:sys.exit('Unexpected Bender module list; edit manually')
    bender=bender.replace(anchor,'\n'.join(lines)+'\n'+anchor)
# Writes only after full preflight.
(croc/'rtl/gemm_accel').mkdir(exist_ok=True)
for n in ['mac_array_4x4.sv','gemm_mmio_4x4.sv','croc_gemm_obi.sv']:
    shutil.copy2(src/'rtl'/n,croc/'rtl/gemm_accel'/n)
check[0].write_text(user);check[1].write_text(pkg);check[2].write_text(bender)
(croc/'sw/test').mkdir(parents=True, exist_ok=True)
shutil.copy2(src/'sw/gemm_test.c', croc/'sw/test/gemm_obi_test.c')
print('INTEGRATED: gemm at 0x20001000 through user_domain/user_pkg + Bender')
print('NEXT: regenerate Bender flists, run Croc simulation with a RISC-V image')
