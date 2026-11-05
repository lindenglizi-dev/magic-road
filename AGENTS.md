# Project storage and checkpoint workflow

For coding work and stage closeout, use `$project-hygiene` from
`.agents/skills/project-hygiene/SKILL.md`. These rules supplement the user's
instructions; they do not authorize unrelated publication or deletion.

- Use this checkout and its current branch. Do not create dated copies of the
  whole project. Use Git commits and release tags for source versions.
- The user has approved verified checkpoint commits and normal pushes for this
  project. After a meaningful successful milestone, inspect the diff, run the
  relevant checks, stage only explicit task files, run the staged-file gate,
  commit, push, and verify the remote branch SHA. A network failure leaves a
  local checkpoint and an explicit unsynced status, not discarded work.
- Preserve existing untracked files and other tasks' changes. Never stage them
  merely to make the working tree look clean. No force pushes or history edits.
- Put new regenerable outputs under `artifacts/`, or an explicitly configured
  output directory on E:. Do not relocate existing engineering inputs blindly.
- Keep source, constraints, required ROMs, test inputs, environment versions,
  reconstruction commands and compact validation evidence in Git. Do not ignore
  all `.hex`, `.rpt`, `.json` or model files by extension. Preserve complete
  required signoff evidence, manual annotations and unresolved failure cases.
- Store datasets, downloads and tool installations once. Record source URL,
  version, SHA-256, license/access requirements and a tested restore procedure.
  Keep an independent backup for irreplaceable data and owned model checkpoints.
  Do not upload credentials, licenses, private datasets or generated work libraries.
- Ordinary runs: keep two newest successes, one newest failure, every pinned
  baseline and every running/unresolved run. Only superseded, explicitly owned
  runs older than seven days may become cleanup candidates. Training must retain
  best and latest resumable checkpoints, including needed optimizer/RNG state.
- Run the storage scan at meaningful stage closeout and before large generation.
  A 30 GiB artifact budget and 30 GiB C: free-space warning are initial thresholds.
  Below 10 GiB free on C:, avoid new large downloads/builds until space is handled.
  Budget pressure never permits deleting pinned evidence or irreplaceable inputs.
- Scans and `.gitignore` do not delete files. Cleanup requires an approved list;
  use one literal target per command and recheck identity, links, active use and
  recoverability immediately before deletion. No wildcard cleanup or delete loops.
- Treat Codex sessions/databases/configuration/authentication and active runtimes
  as retained state. Use supported session deletion when explicitly requested;
  do not manually purge SQLite files or infer that a folder called cache is unused.
