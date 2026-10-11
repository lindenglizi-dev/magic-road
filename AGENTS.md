# Project instructions for coding agents

## Current phase and sources of truth

- The current phase is real-data validation. Do not modify the production FPGA top level merely to replace missing data or measurements.
- Use `CURRENT_ARCHITECTURE.md` when a task changes module boundaries, clocks, CDC, frame identity, ROI ownership, or the display path.
- Use `REAL_DATA_WORKFLOW.md` for dataset, training, evaluation, and simulation-measurement work.
- Check `evaluation/status.json` for current evidence and blockers. The thresholds in `evaluation/criteria.pending.json` are proposals until `frozen` is true.
- The implemented baseline is a 32x32 grayscale ROI, 64 HOG features, and a fixed-point linear binary SVM. Do not substitute the 64x128/3780-feature/dual-SVM sketch from the external multi-agent proposal.

## Python before new RTL behavior

- For new or uncertain algorithms, arithmetic, quantization, scheduling, or rejection logic, first make a small Python reference with explicit inputs, outputs, rounding, saturation, and test vectors. Then implement RTL against that contract.
- Compare meaningful intermediate values as well as final classes. For the classifier path this includes ROI pixels, gradients or bins, 64 features, fixed-point products/accumulation, score, and class.
- This rule does not require rewriting already-understood RTL in Python for documentation-only, wiring-only, or mechanical maintenance tasks.

## Multi-agent work

- For work that benefits from delegation, read `MULTI_AGENT_WORKFLOW.md` and use its role, ownership, model, and handoff matrix.
- The coordinator owns task decomposition, interface consistency, integration, and the final answer. Assign each subagent one concrete, bounded deliverable.
- Use no more than three active subagents at once in this environment. Do not make agents edit the same file concurrently.
- Cross-owner interface changes must be surfaced to the coordinator before implementation. Continue independent analysis and tests while the interface decision is pending.

## Change and verification boundaries

- Keep production RTL unchanged during the current real-data phase unless the user explicitly changes that priority or measured evidence justifies a scoped integration task.
- Never infer that a CDC bus is safe from a synchronized pulse alone. State the source hold rule, destination capture rule, acknowledgement point, reset behavior, and payload stability interval.
- Never infer that an ROI bank can be released from `done` alone. Identify the last RAM read or an explicit `ram_read_done`-equivalent event and tie release to it.
- Preserve scene-level train/validation/test isolation. Do not random-split adjacent frames or treat unlabeled image regions as negative samples.
- Run checks relevant to the files changed. Record command, inputs, model or source hashes when available, and the boundary of what a simulation actually measured.

## Git workspace

- Git was initialized on 2026-10-11 at the user's request. `main` holds the initial baseline; `work/roadyolo` is the initial working branch. Confirm the current branch before editing and keep changes on that branch unless asked otherwise.
- See `GIT_WORKFLOW.md` for tracked scope and local-only assets. Keep disjoint file ownership and explicit handoffs when agents share this checkout.

## CNN hardware validation principles

- The user-approved 2026-10-08 framework is an important project memory: read `cnn/hw_validation/plans/competition_framework_20261008/RoadYOLO_训练与RTL整体技术框架.md` and its evidence index for CNN continuation. It supersedes the historical HOG/SVM target architecture for independent CNN work, not the untouched production implementation. Reuse current student/arithmetic assets; defer unrelated audits while retaining change-relevant numerical, handshake, implementation and timing evidence. Saved baseline figures are not current whole-system measurements.
- For the independent CNN validation work, follow the user-approved `../../嵌赛_CNN验证问题分析与完整解决方案.md` (2026-10-05). Its historical figures are not new measurements.
- Bind each result to the complete source/configuration/numerical input closure and tool hashes; preserve failed reports and immutable input snapshots.
- Project-local checker fixes require original/fixed full-gate comparison and real negative regressions. Unknown interfaces remain blocking; never add fake drivers or suppress real errors.
- Keep numerical tests, vendor RAM behavior, physical mapping/timing, and full-network/board acceptance separate. Local probes do not prove whole-network throughput or accuracy.
- Diagnose hold by actual path/clock/constraint evidence. Never change constraints solely to make a report green; never treat undocumented RAM collision or power-up observations as silicon guarantees.
- Continue only inside `cnn/hw_validation/` unless the user explicitly authorizes wider integration. Do not restart training or program Flash as part of validation.
