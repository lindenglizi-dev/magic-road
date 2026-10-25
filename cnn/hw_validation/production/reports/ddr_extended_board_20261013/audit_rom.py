"""Compare routed PH1P 2048x10 ROM INIT data against every frozen command bit."""
import argparse
import re
from pathlib import Path
import run


def lanes(expression):
    bits = []
    for token in expression.strip('{}').split(','):
        match = re.fullmatch(r'\\road_ddr_selftest_Inst/reg_rom\s+\[(\d+)(?::(\d+))?\]', token.strip())
        if match:
            high, low = int(match[1]), int(match[2] or match[1])
            bits.extend(range(high, low-1, -1))
        else:
            assert re.fullmatch(r'open_n\d+', token.strip()), token
            bits.append(None)
    return list(reversed(bits))


def audit(work):
    text = (work/'routed_netlist.v').read_text(encoding='utf-8')
    words = [int(line,16) for line in (run.ROOT/'vectors.hex').read_text().splitlines()]
    assert len(words) == 2048
    covered, cells = set(), []
    reconstructed = [0]*2048
    for parameters, name, ports in re.findall(r'PH1P_PHY_ERAM_V2\s*#\((.*?)\)\s+(\\\S+)\s+\((.*?)\);', text, re.S):
        if not name.startswith('\\road_ddr_selftest_Inst/'):
            continue
        mode = int(re.search(r'\.DATA_WIDTH_B\("(\d+)"\)',parameters)[1])
        assert mode in (10,2) and '.WEBMUX("0")' in parameters
        address_pattern = (r'\.addrb\(\{\\road_ddr_selftest_Inst/cnt_command\s*,3\x27b111\}\)' if mode == 10
                           else r'\.addrb\(\{2\x27b00,\\road_ddr_selftest_Inst/cnt_command\s*,1\x27b1\}\)')
        assert re.search(address_pattern, ports)
        data, parity = {}, {}
        for prefix, index, value in re.findall(r'\.(INITP|INIT)_([0-9A-F]{2})\(256\x27h([0-9A-F]+)\)', parameters):
            (parity if prefix == 'INITP' else data)[int(index,16)] = int(value,16)
        assert set(data) == set(range(64)) and set(parity) == set(range(16))
        sections = [('dob',data,8),('dob_extra',parity,2)] if mode == 10 else [('dob',data,2)]
        for port, table, width in sections:
            connected = lanes(re.search(r'\.'+port+r'\((.*?)\)',ports,re.S)[1])
            assert all(bit is None for bit in connected[width:])
            contents = sum(value << (index*256) for index,value in table.items())
            for lane, bit in enumerate(connected[:width]):
                if bit is None:
                    continue
                assert bit not in covered
                covered.add(bit)
                for address, expected in enumerate(words):
                    actual = (contents >> (address*width+lane)) & 1
                    assert actual == ((expected >> bit)&1), (name,address,bit)
                    reconstructed[address] |= actual << bit
        cells.append(name)
    assert len(cells) == 19 and len(covered) == 182
    assert reconstructed == words, 'Omitted bits are not all constant zero'
    receipt = {'passed':True,'cells':cells,'rom_words':2048,'physical_bits_per_word':182,
               'constant_zero_bits':sorted(set(range(192))-covered),'compared_bits':2048*192,
               'netlist_sha256':run.sha(work/'routed_netlist.v'),'vectors_sha256':run.sha(run.ROOT/'vectors.hex'),
               'scope':'Routed INIT contents and address/output wiring; not a board readback'}
    run.save(work/'rom_audit.json',receipt)
    print('ROM_INIT_PASS cells=19 words=2048 bits=393216')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('physical',type=Path)
    audit(parser.parse_args().physical.resolve())
