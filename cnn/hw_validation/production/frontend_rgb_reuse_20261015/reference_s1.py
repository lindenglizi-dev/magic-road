"""Before RTL: prove RGB channel reuse against every frozen halo byte address."""
from collections import Counter
import struct
import run


def main():
    run.check()
    path = run.ROOT / 'vectors/stem_halo_byte_addr_s32.bin'
    addresses = [value for value, in struct.iter_unpack('<i', path.read_bytes())]
    assert len(addresses) == 2304 * 243
    counts = Counter()
    trace = []
    for tile in range(2304):
        cache = None
        reuse = False
        line = lane = 0
        local = addresses[tile * 243:(tile + 1) * 243]
        for index, address in enumerate(local):
            channel = index % 3
            if reuse:
                lane += 1
                assert address >= 0 and (address >> 1) & ~7 == line and address & 15 == lane
                counts['direct_channel_advances'] += 1
            elif address >= 0:
                line, lane = (address >> 1) & ~7, address & 15
            if address >= 0 and cache != line:
                trace.append(line)
                cache = line
            reuse = address >= 0 and channel < 2 and cache == line and lane < 15
            if channel < 2 and address >= 0:
                if lane == 15:
                    counts['cross_word_fallbacks'] += 1
                if channel == 0 and lane == 14:
                    counts['R14_G15_B0_pixels'] += 1
                if channel == 0 and lane == 15:
                    counts['R15_G0_B1_pixels'] += 1
            if address < 0:
                counts['padding_bytes'] += 1
        assert not reuse
    old_trace = [value >> 1 for value, in struct.iter_unpack('<I',
                  (run.ROOT / 'vectors/stem_read_trace_byte_addr_u32.bin').read_bytes())]
    assert trace == old_trace and len(trace) == 51357
    saved = counts['direct_channel_advances'] * 4
    run.save(run.ROOT / 'reference_s1.json', {'passed': True, 'halo_addresses': len(addresses),
        'source_sha256': run.sha(path), 'counts': dict(counts), 'rgb_reads_unchanged': len(trace),
        'saved_mapping_state_cycles': saved, 'expected_normal_cycles': 17252079 - saved,
        'contract': 'Only valid same-pixel channels with cache hit and lane<15 skip four mapping states; no DDR reads removed'})
    print({'counts': dict(counts), 'saved_cycles': saved, 'expected_cycles': 17252079 - saved}, flush=True)


if __name__ == '__main__':
    main()
