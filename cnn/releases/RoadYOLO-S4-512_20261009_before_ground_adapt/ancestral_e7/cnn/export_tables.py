"""Export the fixed shared LUTs and exhaustive integer boundary vectors, not weights."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np

from . import integer


def export_tables(output: Path) -> dict:
    constants = integer.tables()
    domain = np.arange(-32768, 32768, dtype=np.int64)
    records = [
        ('silu', constants['silu'], None),
        ('sigmoid', constants['sigmoid'], None),
        ('exp', constants['exp'], None),
        ('silu_golden', integer.silu(domain), [-32768, 32767]),
        ('sigmoid_golden', integer.sigmoid(domain), [-32768, 32767]),
        ('exp_golden', integer.exponent(np.arange(-1024, 897)), [-1024, 896]),
    ]
    # Exclusive directory creation: even an interrupted earlier export is preserved.
    output.mkdir(parents=True, exist_ok=False)
    manifest = {
        'format': 'road-yolo-shared-tables-v1',
        'status': 'integer_reference_assets_not_trained_model_or_RTL_acceptance',
        'integer_source_sha256': hashlib.sha256(Path(integer.__file__).read_bytes()).hexdigest(),
        'contract_sha256': hashlib.sha256(Path(__file__).with_name('contract.json')
                                         .read_bytes()).hexdigest(),
        'word_bits': 16, 'binary_endianness': 'little',
        'hex': 'one_four_digit_twos_complement_word_per_line_for_readmemh',
        'rounding': 'nearest_even',
        'silu_upper': constants['silu_upper'],
        'sigmoid_upper': constants['sigmoid_upper'],
        'files': [],
    }
    for name, values, input_range in records:
        dtype = '<i2' if values.dtype.kind == 'i' else '<u2'
        payload = values.astype(dtype).tobytes()
        hex_payload = ''.join(f'{int(value) & 65535:04x}\n' for value in values).encode('ascii')
        entry = {'name': name, 'entries': len(values), 'dtype': dtype,
                 'input_q8_range': input_range}
        for suffix, data in (('bin', payload), ('hex', hex_payload)):
            path = output / f'{name}.{suffix}'
            with path.open('xb') as handle:
                handle.write(data)
            entry[suffix] = {'path': path.name, 'bytes': len(data),
                             'sha256': hashlib.sha256(data).hexdigest()}
        manifest['files'].append(entry)
    # Publish only after every asset was written successfully.
    with (output / 'manifest.json').open('x', encoding='utf-8') as handle:
        json.dump(manifest, handle, indent=2)
        handle.write('\n')
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(export_tables(args.output), indent=2))


if __name__ == '__main__':
    main()
