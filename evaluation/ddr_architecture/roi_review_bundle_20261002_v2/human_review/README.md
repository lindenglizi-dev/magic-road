# VIRAT 010107 background subtype review

This package contains a bounded human review of deduplicated invalid candidates plus protection controls.

## Human fields

For rows with `review_role=background_subtype_target`, set `background_subtype` to exactly one of:
`shadow`, `parking_line_related`, `background_change`, `other`, or `uncertain`.
Also fill `reviewer`, `reviewed_at`, and optionally `review_note`.

Rows with `review_role=protection_control` are known ped/rider controls removed by the causal 2-of-3 diagnostic.
Do not assign them a background subtype; leave `background_subtype` blank and use `review_note` only for review comments.

## Panel legend

- Yellow: raw component box.
- Magenta: selected or expanded candidate box.
- Signed difference: blue means darker than background; red means brighter.
- Masks show raw threshold, 3x3 cleanup, and row minimum-run stages.

Selected invalid candidates: 22; protection controls: 5.
Selection was deterministic and used no annotation or visual cherry-picking.
