# Candidate review

Allowed `review_class`: ped_full, ped_truncated, vehicle, merged_target, background_fragment, other_ignore. Every sampled row requires an explicit human decision. Annotation hints are sampling aids only; unmatched never means background. Use `ped_truncated` only when the candidate box cuts visible body parts; scene occlusion belongs in `occlusion`. `background_fragment`, `merged_target`, and `other_ignore` require a note. Set `review_basis=human_visual_review`. No sample is imported into training by this tool.
