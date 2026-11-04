"""成像标定的整数语义：曝光半行计数、已知增益档和稳定白平衡。"""
from pathlib import Path

EXPOSURES = (1991, 480, 240, 120)
GAINS = (144, 176, 80, 112)

def neutral(pixel):
    low, high = min(pixel), max(pixel)
    return low >= 16 and high <= 224 and 2*high <= 3*low

def gains(pixels):
    samples = [pixel for pixel in pixels if neutral(pixel)]
    if len(samples) < 64:
        return None
    red, green, blue = map(sum, zip(*samples))
    return tuple(max(32768, min(131072, (green << 16)//channel)) for channel in (red, blue))

def smooth(current, target):
    difference = abs(target-current)
    return current+difference//4 if target >= current else current-difference//4

def main():
    assert len(set(EXPOSURES)) == 4 and max(EXPOSURES) <= 1991
    assert gains([(200, 20, 20)]*1000) is None
    assert gains([(60, 120, 130)]*1000) is None
    assert gains([(80, 100, 120)]*64) == (81920, 54613)
    assert smooth(65536, 81920) == 69632
    rows = []
    for red in (16, 32, 64, 80, 100, 160, 224):
        for green in (16, 32, 64, 100, 160, 224):
            for blue in (16, 32, 64, 120, 160, 224):
                expected = gains([(red, green, blue)]*64)
                if expected:
                    rows.append(f'{red} {green} {blue} {expected[0]} {expected[1]}\n')
    Path(__file__).with_name('wb_vectors.txt').write_text(''.join(rows), encoding='ascii')
    print(f'PASS calibration semantic model: {len(rows)} exact integer gain vectors')

if __name__ == '__main__':
    main()
