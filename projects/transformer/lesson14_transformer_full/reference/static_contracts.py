from pathlib import Path
import re
r=Path(__file__).resolve().parents[1]
sv=(r/'rtl/transformer_block_top.sv').read_text()
tb=(r/'tb/tb_transformer_block.sv').read_text()
header=sv[sv.index('module transformer_block_top'):sv.index(');',sv.index('module transformer_block_top'))]
ports=set()
for line in header.splitlines():
 line=line.strip()
 if line.startswith(('input logic','output logic')):
  line=line.split('//')[0]
  line=re.sub(r'\[[^]]+\]','',line)
  line=re.sub(r'^(input|output)\s+logic\s+','',line)
  for tok in line.split(','):
   name=tok.strip().strip(',')
   if re.fullmatch(r'[a-zA-Z_]\w*',name):ports.add(name)
# Check name presence only: comments/uses also match, so this cannot prove
# declarations or widths. Actual elaboration of the TB's .* is authoritative.
missing=[]
for name in sorted(ports):
 if not re.search(r'\b'+re.escape(name)+r'\b',tb):missing.append(name)
print('top ports',len(ports),'missing TB name mentions',missing,'(declarations NOT checked)')
assert not missing
# Upper block instance should be unique; common gemm instantiation unchanged.
assert sv.count('u_gemm (')==1
assert sv.count('u_softmax(')==1
assert sv.count('u_attn_requant (')==1
assert sv.count('u_ffn_requant (')==1
for s in ('PH_Q=0','PH_K=1','PH_V=2','PH_SCORE=3','PH_PV=4','PH_FFN1=5','PH_FFN2=6'):
 assert s in sv,s
assert 'full_attention_top.sv' not in (r/'scripts/run_iverilog.sh').read_text()
assert 'full_attention_top.sv' not in (r/'scripts/run_modelsim.do').read_text()
# Check sparse format and address layout against every original operand byte.
import numpy as np
DEPTH=65536
for case in ('demo','edge_5x7','random_00','sat_1x1'):
 d=r/'vectors'/case
 z=np.load(d/'reference.npz')
 def parse_sparse(path):
  bank={};addr=None
  for line in path.read_text().splitlines():
   if line.startswith('@'):addr=int(line[1:],16)
   else:
    assert addr is not None and addr not in bank
    bank[addr]=int(line,16);addr+=1
  return bank
 xm=parse_sparse(d/'x_sparse.hex'); wm=parse_sparse(d/'weights_sparse.hex')
 cfg=list(map(int,(d/'config.txt').read_text().split()))
 F,ats,hs,w1b,w2b=map(int,(d/'ffn_config.txt').read_text().split())
 x=z['X']; W=z['W'];L,D=x.shape
 for row in range(L):
  for col in range(D):
   p=(row%4)*DEPTH+cfg[5]+(row//4)*D+col
   assert xm[p]==int(x[row,col])%256
 for n in range(3):
  for row in range(D):
   for col in range(D):
    p=(col%4)*DEPTH+cfg[6+n]+row*((D+3)//4)+col//4
    assert wm[p]==int(W[n,row,col])%256
 assert w2b + F*((D+3)//4) < DEPTH
 print('sparse memory PASS',case,'X/three weights')
print('PASS source-level structural and memory-image checks (NOT SV compiler)')
