"""Derive the three directed-chain records with the frozen v7 reference."""
import importlib.util
import json
from pathlib import Path


REPORT = Path(__file__).resolve().parent
REFERENCE = REPORT.parent / "v7_minimal_chain_20261006" / "reference.py"
SPEC = importlib.util.spec_from_file_location("v7_minimal_reference", REFERENCE)
REFERENCE_MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(REFERENCE_MODULE)

table = REFERENCE_MODULE.hex_signed(REFERENCE.parent / "inputs" / "silu_table.hex")
records = []
stage_words = []
feature_words = []
for accumulator, multiplier, shift in ((100000, 1, 0), (-100000, 3, 2), (8, 5, 4)):
    pre_product, pre_rounded, pre_value = REFERENCE_MODULE.quant(
        accumulator, multiplier, shift, 16
    )
    table_address, silu_value = REFERENCE_MODULE.activate(pre_value, table)
    post_product, post_rounded, feature = REFERENCE_MODULE.quant(
        silu_value, 1, 4, 8
    )
    records.append(
        {
            "accumulator": accumulator,
            "pre_product": pre_product,
            "pre_rounded": pre_rounded,
            "pre_saturated": pre_value,
            "silu_input": pre_value,
            "silu_address": table_address,
            "silu_output": silu_value,
            "post_product": post_product,
            "post_rounded": post_rounded,
            "feature_int8": feature,
        }
    )
    packed = (
        ((accumulator & 0xFFFFFFFF) << 184)
        | ((pre_product & 0xFFFFFFFFFFFFFFFF) << 120)
        | ((pre_value & 0xFFFF) << 104)
        | ((silu_value & 0xFFFF) << 88)
        | ((post_product & 0xFFFFFFFFFFFFFFFF) << 24)
        | ((post_rounded & 0xFFFF) << 8)
        | (feature & 0xFF)
    )
    stage_words.append(f"{packed:054x}")
    feature_words.append(f"{feature & 0xFF:02x}")

print(
    json.dumps(
        {
            "reference": str(REFERENCE),
            "bias": [100000, -100000, 8],
            "zero_products": True,
            "records": records,
            "expected_stages_hex": stage_words,
            "expected_features_hex": feature_words,
        },
        indent=2,
    )
)
