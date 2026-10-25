"""Reject the four concrete width/layout regressions before hardware use."""
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]


def validate(program,addresses,mapping,reads):
    assert len(program)==8192 and program[6091]>>60==7
    assert all(word==0 for word in program[6092:])
    expected_addresses=[(0x03500000+((ty*64+tx)*16+y*4+x)*16)//2
        for ty in range(4) for tx in range(4) for y in range(4) for x in range(4)]
    assert addresses==expected_addresses and len(set(addresses))==256
    expected_map=[]
    for ty,tx in ((0,0),(0,1),(1,0),(1,1)):
        for y in range(9):
            for x in range(9):
                gy,gx=ty*8+y-1,tx*8+x-1
                expected_map.append(256 if gy<0 or gx<0 else ((gy//4)*4+gx//4)*16+(gy%4)*4+gx%4)
        expected_map.extend([256]*47)
    assert mapping==expected_map
    assert reads==[i for i in expected_map if i!=256]
    assert len(reads)==289 and len(set(reads))==256


def main():
    names=('program.hex','stem_addresses.hex','halo_map.hex','read_indices.hex')
    values=[[int(s,16) for s in (ROOT/'vectors'/n).read_text().splitlines()] for n in names]
    validate(*values)
    rejected=[]
    mutations=[('program_truncated',0,values[0][:4096]),
        ('wrong_contiguous_row_stride',1,[values[1][0]+8*i for i in range(256)]),
        ('padding_index_collision',2,[v&255 for v in values[2]]),
        ('missing_write_address',1,values[1][:-1]),
        ('duplicate_write_address',1,[values[1][0]]+values[1][:-1]),
        ('missing_read',3,values[3][:-1]),
        ('wrong_overlap_read_order',3,list(reversed(values[3])))]
    for name,index,replacement in mutations:
        candidate=values.copy()
        candidate[index]=replacement
        try:
            validate(*candidate)
        except AssertionError:
            rejected.append(name)
        else:
            raise AssertionError(('NEGATIVE_CASE_ACCEPTED',name))
    receipt={'passed':True,'positive_cases':1,'rejected':rejected,
        'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'input_hashes':{n:hashlib.sha256((ROOT/'vectors'/n).read_bytes()).hexdigest() for n in names}}
    (ROOT/'vector_negative_receipt.json').write_text(json.dumps(receipt,indent=2),encoding='utf-8')
    print('VECTOR_CONTRACT_PASS positive=1 negative=7')


if __name__=='__main__':
    main()
