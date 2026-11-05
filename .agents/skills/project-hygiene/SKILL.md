---
name: project-hygiene
description: Manage project checkpoint commits, storage growth and retention of generated artifacts during development and stage closeout. Use for project housekeeping, Git checkpoint workflows, cache audits and artifact cleanup planning; do not treat this skill as permission to delete files or publish unrelated changes.
---

# Project hygiene

Keep source versions in one Git checkout, generated outputs bounded, and important
results recoverable. Follow the project's AGENTS.md and the user's authorizations.

## Stage closeout

1. Establish repository root, current branch, upstream and pre-existing changes.
   Reuse existing tests and generators; do not copy the entire project for safety.
2. Run the smallest meaningful verification for the actual change. Preserve the
   result, reproduction command, input/configuration hashes and source version.
   Large waveforms/build databases stay outside source history unless selected
   as necessary release evidence.
3. Stage explicit task paths only. Run this skill's `scripts/hygiene.py staged
   --repo REPO`. It checks the Git index, not working-tree file sizes. Resolve
   large-file, generated-directory and credential-filename findings before commit.
   It is a filename/size gate, not a comprehensive secret scanner; inspect the diff.
4. If checkpoint push is authorized, commit, normal-push the current branch, and
   compare HEAD with `git ls-remote` for that remote branch. Upstream tracking
   status alone is not proof of a successful current upload. Verify separately
   stored assets/LFS objects before removing any local originals. If authorization
   is absent, ask once for the checkpoint policy, not again at every milestone.
5. Run `scripts/hygiene.py scan --repo REPO`. Report warnings, unsynced status and
   cleanup candidates. The report keeps one baseline file and computes subsequent
   growth; first-run sizes are not historical growth measurements.

Use Python from the project's normal environment. Script paths are relative to
the installed skill directory, not an assumed current working directory.

## Generated run retention

New disposable run directories belong under `REPO/artifacts/`. Only directories
with an explicit `run.json` marker participate in candidate selection:

```json
{"project_hygiene": 1, "status": "success", "finished_at": "2026-11-05T12:00:00+08:00", "pinned": false, "source_commit": "SOURCE_COMMIT_SHA"}
```

Use `failed` for a resolved failure retained as a diagnostic example, and `running`
for active work. Pin unresolved failures and research/release baselines. Record
parameters, environment and input checksums alongside the marker. Unknown folders,
invalid markers, links, scan errors, running runs and pinned runs are retained.
Keep the two latest successes and latest failure, plus every pinned/running run.
Only additional completed runs older than seven days become candidates. This is
a proposed retention policy, not evidence that a run is actually safe to delete.

## Cache and cleanup handling

- The scan covers selected Codex, package-manager and extension caches; it does
  not read their contents or classify all contents as disposable. Active runtime
  references and session/database ownership need separate checks.
- Keep important decisions and reproduction instructions in project documents.
  For obsolete sessions, inspect this installed Codex version's supported delete
  command when the user requests deletion. Archiving is not a disk-space guarantee.
- Cleanup is a separate authorized action. Present exact paths, sizes, reasons
  and recovery dependencies; follow the user's deletion rules. This script has
  no deletion mode. Recheck reparse points and active use before any literal-path
  cleanup command. Never use `git clean -fdx` as general housekeeping.
- Reuse the existing Git/GitHub tools. Do not install plugins, create schedules,
  change remotes, rewrite history or migrate the Codex home merely to run this skill.
