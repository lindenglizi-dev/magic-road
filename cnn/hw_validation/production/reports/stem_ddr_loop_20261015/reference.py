"""用阶段/计数重建6092条命令；先证明与已上板程序逐位相同。"""
import run


def generate():
    root = run.ROOT
    words = [int(v, 16) for v in (run.BASE / 'vectors/program.hex').read_text(encoding='ascii').split()]
    length = 6092
    expected = words[:length]
    cursor = 0
    rebuilt, table, parameters, pixels = [], [], [], []
    segments = []

    def append(op, count=1, kind=0, source='control'):
        nonlocal cursor
        start = cursor
        for index in range(count):
            value = expected[cursor] & 0xffffffff
            address = index if source != 'control' else 0
            pixel_kind = (expected[cursor] >> 46) & 7 if source == 'pixel' else kind
            if source == 'control':
                value = 1 if op == 4 else 0
            actual = (op << 60) | (address << 49) | (pixel_kind << 46) | value
            assert actual == expected[cursor], (cursor, actual, expected[cursor])
            if source == 'table':
                assert value == ((value & 0x7fff) - (value & 0x8000)) & 0xffffffff
                table.append(value & 0xffff)
            elif source == 'parameter':
                parameters.append(value)
            elif source == 'pixel':
                assert pixel_kind in (0, 1) and 0 <= value <= 255
                assert pixel_kind == 0 or value == 0
                pixels.append(pixel_kind << 8 | value)
            rebuilt.append(actual)
            cursor += 1
        segments.append({'offset': start, 'length': count, 'op': op, 'kind': kind, 'source': source})

    append(0, 1024, source='table')
    for kind, count in ((2, 432), (3, 16), (4, 16), (5, 16), (6, 2)):
        append(1, count, kind, 'parameter')
    for _ in range(16):
        append(1, 243, source='pixel')
        append(2)
        append(3)
    append(4)
    for kind, count in ((2, 144), (3, 16), (4, 384), (5, 24), (6, 40), (7, 44)):
        append(1, count, kind, 'parameter')
    for _ in range(4):
        append(5)
        append(2)
        append(6)
    append(7)
    assert cursor == length and rebuilt == expected
    assert (len(table), len(parameters), len(pixels)) == (1024, 1134, 3888)
    for name, values, bits, depth in (('loop_table.hex', table, 16, 1024),
                                     ('loop_parameters.hex', parameters, 32, 2048),
                                     ('loop_pixels.hex', pixels, 12, 4096)):
        content = ''.join(f'{v:0{bits // 4}x}\n' for v in values + [0] * (depth - len(values)))
        for folder in ('vectors', 'rtl'):
            (root / folder / name).write_text(content, encoding='ascii')
    run.save(root / 'loop_reference.json', {'passed': True, 'instructions': length,
        'all_commands_bit_identical': True, 'segments': segments,
        'data_entries': {'table_int16': 1024, 'parameters_int32': 1134, 'pixels_uint9': 3888},
        'declared_bits': 1024 * 16 + 2048 * 32 + 4096 * 9,
        'old_command_bits': 8192 * 64, 'program_sha256': run.sha(run.BASE / 'vectors/program.hex'),
        'scope': 'Same four-tile payloads; loop scheduling changes command representation only'})
    print('LOOP_REFERENCE_PASS 6092 commands bit-identical', flush=True)


if __name__ == '__main__':
    run.check()
    generate()
    run.check()
