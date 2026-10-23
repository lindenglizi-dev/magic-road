"""Cycle-oriented software contract model for Lesson 18's one-outstanding OBI adapter.
This tests an independent protocol model, not the RTL. Uses valid/ready events.
"""
from dataclasses import dataclass
from random import Random
BASE=0x20001000
@dataclass(frozen=True)
class Request:
    addr:int
    write:bool
    data:int
    be:int
    aid:int
class Adapter:
    def __init__(self):
        self.valid=False
        self.rid=0
        self.error=False
        self.rdata=0
        self.memory={0x10:0,0x14:0,0x18:0,0x1c:0,0x20:0,0x24:0,0x28:0,0x2c:0}
        self.accepted=0
        self.responded=0
    def tick(self,req=None):
        old_valid=self.valid
        grant=not old_valid
        if old_valid:self.responded+=1
        self.valid=False
        if req is not None and grant:
            self.accepted+=1
            off=req.addr-BASE
            readable=off in (0,4) or off in self.memory or (0x40<=off<=0x7c and off%4==0)
            writable=off==0 or off in self.memory
            bad=(req.addr<BASE or req.addr>=BASE+4096 or off%4!=0 or
                 (req.write and (not writable or req.be!=15)) or
                 (not req.write and not readable))
            self.valid=True; self.rid=req.aid;self.error=bad
            self.rdata=0 if bad else self.memory.get(off,0)
            if req.write and not bad and off in self.memory:
                self.memory[off]=req.data & 0xffffffff
        return grant,old_valid

def run():
    m=Adapter(); rng=Random(20261023)
    source=[Request(BASE+0x10,True,0xFE030201,15,2),
            Request(BASE+0x10,False,0,15,3),
            Request(BASE+0x1010,True,0xDEADBEEF,15,5),
            Request(BASE+0x10,True,0xDEADBEEF,3,6)]
    for i in range(1000):
        off=rng.choice([0,4,0x10,0x14,0x20,0x40,0x7c,0x80,0x1000,0x11])
        source.append(Request(BASE+off,rng.random()<0.5,rng.getrandbits(32),rng.choice([15,7,3]),rng.randrange(8)))
    pending=[];next_i=0;latency=[];accepted=0
    for cyc in range(5000):
        req=source[next_i] if next_i<len(source) else None
        prev=m.valid;previous=(m.rid,m.error,m.rdata)
        grant,responded=m.tick(req)
        if prev:
            rid,bad,_=previous
            expected=pending.pop(0)
            assert rid==expected[0] and bad==expected[1]
            latency.append(cyc-expected[2])
        if req and grant:
            assert m.valid and m.rid==req.aid
            expected_bad=(req.addr<BASE or req.addr>=BASE+4096 or ((req.addr-BASE)%4) or
                (req.write and (req.be!=15 or ((req.addr-BASE) not in [0,*m.memory]))) or
                (not req.write and ((req.addr-BASE) not in [0,4,*m.memory,*range(0x40,0x80,4)])))
            assert m.error==bool(expected_bad)
            pending.append((req.aid,bool(expected_bad),cyc))
            next_i+=1;accepted+=1
        if next_i==len(source) and not pending and not m.valid:break
    assert accepted==len(source)
    assert m.accepted==m.responded==len(source)
    print('PASS OBI cycle model:',accepted,'accepted and returned, no lost transaction')
    print('NOTE this model does not compile or execute SystemVerilog')
if __name__=='__main__':run()
