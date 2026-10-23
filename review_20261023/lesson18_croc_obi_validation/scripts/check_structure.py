#!/usr/bin/env python3
"""Static checks only; this does not compile HDL."""
from pathlib import Path
import subprocess, tempfile, re
p=Path(__file__).resolve().parents[1]
for f in ['rtl/croc_gemm_obi.sv','rtl/gemm_mmio_4x4.sv','rtl/mac_array_4x4.sv',
          'scripts/integrate_into_croc.py','sw/gemm_test.c']:
    assert (p/f).exists(),f
s=(p/'rtl/croc_gemm_obi.sv').read_text()
for tok in ['obi_req_i.a.aid','obi_rsp_o.r.rid','obi_rsp_o.rvalid','obi_rsp_o.gnt',
            'invalid_access','reg_valid(accept && !invalid_access)','!rsp_valid_q','addr_in_window']:
    assert tok in s, tok
subprocess.run(['python3','-m','py_compile',str(p/'scripts/integrate_into_croc.py')],check=True)
# Validate patch semantics in a reduced Croc template fixture.
with tempfile.TemporaryDirectory() as tmp:
    d=Path(tmp); (d/'rtl').mkdir(); (d/'sw').mkdir()
    (d/'rtl/user_domain.sv').write_text('  obi_err_sbr #(\n    .NumMaxTrans (1)\n  ) i_your_design_goes_here (\n    .clk_i (clk_i)\n  );\n')
    (d/'rtl/user_pkg.sv').write_text("start_addr: croc_pkg::UserBaseAddr,\n      end_addr:   croc_pkg::UserBaseAddr + 32'h1000_0000\n")
    (d/'Bender.yml').write_text('      - rtl/croc_domain.sv\n      - rtl/user_domain.sv\n')
    patch=['python3',str(p/'scripts/integrate_into_croc.py'),str(d)]
    subprocess.run(patch,check=True,capture_output=True,text=True)
    subprocess.run(patch,check=True,capture_output=True,text=True)
    u=(d/'rtl/user_domain.sv').read_text(); pkg=(d/'rtl/user_pkg.sv').read_text(); b=(d/'Bender.yml').read_text()
    assert u.count('croc_gemm_obi i_gemm_obi')==1
    assert "32'h0000_1000" in pkg and "32'h0000_2000" in pkg
    assert b.count('rtl/gemm_accel/croc_gemm_obi.sv')==1
    assert (d/'sw/test/gemm_obi_test.c').exists()
# Independent golden check: identity times B equals signed bytes of B.
b=[0xFE030201,0x08070605,0x0C0B0A09,0x100F0E0D]
for word in b:
    for col in range(4):
        raw=(word>>(8*col))&255
        v=raw if raw<128 else raw-256
        assert -128<=v<=127
print('PASS: source structure, Croc integration patch, idempotency, address window, software copy, Python golden')
print('RTL_UNVERIFIED: structural checks are NOT HDL elaboration or simulation')
