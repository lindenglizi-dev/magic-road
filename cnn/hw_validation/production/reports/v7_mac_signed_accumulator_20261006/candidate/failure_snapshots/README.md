# Failure snapshot provenance

`vg122_operand34_reconstructed.v` is an explicitly reconstructed evidence snapshot, not the delivery candidate.

- Expected and obtained SHA256: `61A1867FFB6ED660AE7BEA4646695964380157521BD55760B7E4F3355014CC12`.
- It matches the source analyzed by `../strict_candidate.json` and the coordinator's first width audit.
- The live file was not copied before the first gate run. The snapshot was reconstructed from the frozen source plus the retained minimal width patch, then its hash was checked against the previously recorded source hash.
- Its three VG122 findings are genuine: each expression added two 34-bit operands into a 34-bit target.

The final candidate instead forms a 34-bit sum from two signed 33-bit operands in the same cycle. It adds no register stage.
