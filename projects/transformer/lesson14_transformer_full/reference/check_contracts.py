#!/usr/bin/env python3
"""Check generated vector/layout contracts without claiming RTL simulation."""
from pathlib import Path
import numpy as np
from softmax_fixed import scale_for_dim, softmax_fixed
root=Path(__file__).resolve().parents[1]

def signhex(path,bits):
    a=[int(s,16) for s in path.read_text().split()]
    return np.asarray([x-(1<<bits) if x & (1<<(bits-1)) else x for x in a],dtype=np.int64)

def main():
    checks=0
    for name in ['demo','edge_5x7','random_00','sat_1x1']:
       case=root/'vectors'/name
       l,d,*rest=[int(x) for x in (case/'config.txt').read_text().split()]
       qkv=signhex(case/'out.hex',8).reshape(3,l,d)
       raw=signhex(case/'raw.hex',32).reshape(3,l,d)
       score=signhex(case/'score.hex',32).reshape(l,l)
       p=signhex(case/'prob.hex',8).reshape(l,l)
       out=signhex(case/'pv.hex',32).reshape(l,d)
       scale=int((case/'softmax_scale.txt').read_text())
       assert scale==scale_for_dim(d)
       assert np.array_equal(score,qkv[0]@qkv[1].T)
       expect_p=np.minimum(127,(np.array([softmax_fixed(row,scale) for row in score])+1)//2)
       assert np.array_equal(p,expect_p)
       assert np.array_equal(out,p@qkv[2])
       for row in range(l):
           for col in range(d):
               qbank=row%4;qaddr=(row//4)*d+col
               vbank=col%4;vaddr=row*((d+3)//4)+col//4
               assert qaddr<((l+3)//4)*d
               assert vaddr<l*((d+3)//4)
               checks+=1
           for col in range(l):
               pbank=row%4;paddr=(row//4)*l+col
               assert paddr<((l+3)//4)*l
               checks+=1
       print(f'PASS {name}: L={l} D={d}, GEMM5 outputs = {l*d}, bank contracts checked')
    # One and only one GEMM instance in full top.
    rtl=(root/'rtl'/'transformer_block_top.sv').read_text()
    assert rtl.count('u_gemm (')==1
    assert rtl.count('u_softmax(')==1
    assert rtl.count('u_attn_requant (')==1
    assert rtl.count('u_ffn_requant (')==1
    print(f'PASS {checks} address assertions, single GEMM, Attention/FFN requant and independent Softmax verified (Python / source-level only)')
if __name__=='__main__': main()
