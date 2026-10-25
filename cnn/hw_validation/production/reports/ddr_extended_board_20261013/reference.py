"""Pack the frozen boundary vectors into a checked, single-command ROM."""
from collections import Counter
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT.parent / 'ddr_offline_boundaries_20261013/vectors.txt'


def generate(out):
    rows = [tuple(int(field, 16) for field in line.split())
            for line in SOURCE.read_text(encoding='ascii').splitlines()]
    assert len(rows) == 1102
    selected = [row for row in rows if row[0] in (0, 1)]
    assert Counter(row[0] for row in selected) == {0: 528, 1: 528}
    memory, commands, slots = {}, [], {}
    for index, (write, address, mask, data, expected, slot) in enumerate(selected):
        assert 0x03400000 <= address <= 0x03fffff0 and address % 16 == 0
        assert 0 <= mask <= 0xffff
        slots[address] = slot
        if write:
            old = memory.get(address, 0)
            result = bytes((old if mask & (1 << lane) else data).to_bytes(16, 'little')[lane]
                           for lane in range(16))
            memory[address] = int.from_bytes(result, 'little')
            assert memory[address] == expected
        else:
            assert memory[address] == expected
        payload = data if write else expected
        native = address >> 1
        word = payload | mask << 128 | native << 144 | write << 169 | index << 170 | 0xa5 << 181
        assert (word >> 181) == 0xa5 and (word >> 170) & 0x7ff == index
        assert ((word >> 144) & 0x1ffffff) * 2 == address
        commands.append(word)
    assert len(slots) == 194 and len(commands) == 1056
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    (out / 'vectors.hex').write_text(''.join(f'{word:048x}\n' for word in commands + [0] * (2048-len(commands))), encoding='ascii')
    (out / 'board_vectors.txt').write_text(''.join(' '.join(f'{value:x}' for value in row) + '\n' for row in selected), encoding='ascii')
    receipt = {'commands': len(commands), 'writes': 528, 'reads': 528, 'addresses': 194,
               'filtered_invalid_requests': 46, 'rom_bits': 192, 'rom_depth': 2048,
               'source': str(SOURCE), 'source_sha256': hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
               'rom_sha256': hashlib.sha256((out / 'vectors.hex').read_bytes()).hexdigest(),
               'byte_range': ['0x03400000', '0x04000000'], 'native_unit_bytes': 2,
               'layout': {'data': [127, 0], 'mask': [143, 128], 'native_address': [168, 144],
                          'write': [169, 169], 'index': [180, 170], 'magic_a5': [188, 181], 'zero': [191, 189]},
               'boundary': 'Frozen-vector replay; does not model DDR controller completion or physical capacity'}
    (out / 'reference.json').write_text(json.dumps(receipt, indent=2), encoding='utf-8')
    return receipt


if __name__ == '__main__':
    print(json.dumps(generate(ROOT)))
