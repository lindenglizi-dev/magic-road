# Formatter parser compatibility audit

- Source SHA256: `ac38e5485edda708485de6962f3973a5b726ff70da17c9df4b0ea7b57313a3e0`
- Direct `_parse_module`: PASS, 11 parameters, 68 ports.
- Current `format_text`: `VerilogFormatterError: > ERR: [Python] Strict always split failure: Strict mode [always_split_violation]: always@(posedge i_clk or negedge i_rstn). Suggestion: Split this multi-target always block manually before formatting.`
- Minimal grouped-assignment reproducer: `VerilogFormatterError: > ERR: [Python] Strict always split failure: Strict mode [always_split_violation]: always@(posedge i_clk or negedge i_rstn). Suggestion: Split this multi-target always block manually before formatting.`
- Same minimal assignments placed on separate lines: passed.
- Actual rejected block targets: 32.
- Line-only preview: 25 physical lines expanded; `format_text` passed.
- Source/preview non-whitespace hashes equal: True.

- Direct parser comparison: module name, all 11 parameter defaults, and all 68 port 
declarations are identical between source and preview.

Conclusion: the source is valid to the direct module/ANSI-port parser. The current failure 
comes from the large main sequential process containing multiple nonblocking assignments 
on one physical line. The normalizer treats each such line as one statement and rejects it 
because that statement writes multiple targets. A paired-FSM block with one assignment per 
line is auto-splittable. Expanding the 25 grouped physical lines preserves the non-whitespace 
token stream and allows `format_text` to pass, so a bounded formatting-only fix exists; no 
manual repartition of the main sequential process is required.

No source or skill file was modified. Full exception chains, current interface names and 
tool hashes are in `audit.json`; the exact input and review-only line-split preview are saved 
beside this report.

## Bounded strict-gate run

- Delivery ready: `False`; errors: 1556; strict warnings: 20.
- Compile/parser check: passed (1 module, 0 parse errors).
- Formatter AST check: failed (1 formatter error).
- Readability: failed; comment: failed; naming: failed; profile: failed.
- This strict-gate result is a recorded failure, not a pass inferred from compilation.
- Full evidence is in `pipeline_gate.json` and `pipeline_gate.md`.
