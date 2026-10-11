# road_round_shift implementation order

Contract: requirements.json. Python oracle: reference.py uses exact Fraction rounding,
and cross-checks the existing cnn.integer.requantize on legal int32 products.

Registers: magnitude/sign/shift → quotient/mask/half → remainder →
above/tie-and-odd → increment → rounded magnitude → signed result →
saturation flags → int16 result. Valid, fault and tag follow the same nine stages.
All stages have one common clock enable, no gated clock. No multiplier is added.

Verification: all legal shifts, positive/negative ties, saturation edges, random
products, invalid shift, INT64_MIN, bubbles, stalls and reset cancellation.
The enclosing activation pipeline owns downstream readiness and drives i_advance.
This primitive does not independently derive ready from downstream valid.

The installed catalog has no readable-python-generator/readable-script-generator;
Python is checked with CPU self-tests, not claimed to pass those unavailable skills.
