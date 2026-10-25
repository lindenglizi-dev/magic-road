"""Reconstruct the routed 4096x64 loader program, including optimized zero bits."""
import argparse
import re
from pathlib import Path
import run


def output_lanes(expression):
    bits=[]
    for token in expression.strip('{}').split(','):
        token=token.strip()
        match=re.fullmatch(r'\\u_sequence/reg_command\s+\[(\d+)(?::(\d+))?\]',token)
        if match:
            high,low=int(match[1]),int(match[2] or match[1])
            bits.extend(range(high,low-1,-1))
        elif token==r'\u_sequence/u_core/i_table_data [0]':
            bits.append(0)
        else:
            assert re.fullmatch(r'open_n\d+',token),token
            bits.append(None)
    return list(reversed(bits))


def audit(work,expected):
    words=[int(line,16) for line in expected.read_text().splitlines()]
    assert len(words)==4096
    text=(work/'routed_netlist.v').read_text(encoding='utf-8')
    reconstructed=[0]*4096
    covered,cells=set(),[]
    for parameters,name,ports in re.findall(r'PH1P_PHY_ERAM_V2\s*#\((.*?)\)\s+(\\\S+)\s+\((.*?)\);',text,re.S):
        if not name.startswith('\\u_sequence/ramread0_'):
            continue
        assert '.DATA_WIDTH_B("5")' in parameters and '.WEBMUX("0")' in parameters
        address=re.search(r'\.addrb\((.*?)\)',ports,re.S)[1]
        assert re.fullmatch(r'\{\\u_sequence/cnt_program\s+\[11:1\],\\u_sequence/cnt_program\[0\]_dup_\d+\s*,2\x27b11\}',address),address
        data,parity={},{}
        for prefix,index,value in re.findall(r'\.(INITP|INIT)_([0-9A-F]{2})\(256\x27h([0-9A-F]+)\)',parameters):
            (parity if prefix=='INITP' else data)[int(index,16)]=int(value,16)
        assert set(data)==set(range(64)) and set(parity)==set(range(16))
        for port,table,width in [('dob',data,4),('dob_extra',parity,1)]:
            match=re.search(r'\.'+port+r'\((.*?)\)',ports,re.S)
            if not match:
                continue
            connected=output_lanes(match[1])
            assert all(bit is None for bit in connected[width:])
            content=sum(value<<(index*256) for index,value in table.items())
            for lane,bit in enumerate(connected[:width]):
                if bit is None:
                    continue
                assert bit not in covered
                covered.add(bit)
                for address,word in enumerate(words):
                    actual=(content>>(address*width+lane))&1
                    assert actual==((word>>bit)&1),('PROGRAM_INIT_MISMATCH',name,address,bit)
                    reconstructed[address] |= actual<<bit
        cells.append(name)
    assert len(cells)==10 and len(covered)==48
    assert reconstructed==words,'Omitted command bits are not all zero'
    receipt={'passed':True,'program_words':4096,'word_bits':64,'compared_bits':262144,
             'cells':cells,'physical_bits':48,'constant_zero_bits':sorted(set(range(64))-covered),
             'expected_sha256':run.sha(expected),'netlist_sha256':run.sha(work/'routed_netlist.v'),
             'scope':'Routed program INIT and address/output wiring; excludes silicon readback'}
    run.save(work/'program_audit.json',receipt)
    print('PROGRAM_INIT_PASS words=4096 bits=262144 cells=10')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('physical',type=Path)
    parser.add_argument('--expected',type=Path,default=run.ROOT/'vectors/program.hex')
    args=parser.parse_args()
    audit(args.physical.resolve(),args.expected.resolve())
