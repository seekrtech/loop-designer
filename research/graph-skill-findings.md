# Public workflow/graph skill review

Reviewed 2026-09-17. Scope: primary instruction files only; no upstream code installed or executed. Recommendations below describe instruction design, **not measured agent behavior or production reliability**.

## Source and license

- Repository: [kvergins/codex-agent-org-designer-skill](https://github.com/kvergins/codex-agent-org-designer-skill).
- Pinned commit: `dac94295d70551ec4913c82d3942aca1d7fa13bc`.
- Read: [SKILL.md](https://github.com/kvergins/codex-agent-org-designer-skill/blob/dac94295d70551ec4913c82d3942aca1d7fa13bc/agent-org-designer/SKILL.md), [references/playbooks.md](https://github.com/kvergins/codex-agent-org-designer-skill/blob/dac94295d70551ec4913c82d3942aca1d7fa13bc/agent-org-designer/references/playbooks.md), and [LICENSE](https://github.com/kvergins/codex-agent-org-designer-skill/blob/dac94295d70551ec4913c82d3942aca1d7fa13bc/LICENSE).
- MIT, copyright 2026 Kris Vergins. The license requires its copyright and permission notice when redistributing copies or substantial portions. Prefer independently written, attributed synthesis; do not copy its templates wholesale without including the required notice.

## Useful design patterns

| Upstream evidence | Recommendation for this skill |
|---|---|
| `SKILL.md` — Core Elements and Workflow: starts with an outcome, maps a workflow, then specifies local loops, verification, human input and handoffs. | Retain our existing progressive Graph + local Loop interview. This is a conceptual fit, not a reason to replace the interview with a company operating-model questionnaire. |
| `playbooks.md` — Loop-Design Mode: distinguishes trigger, context, produced artifact, verifier, allowed actions and accountable human. | Add a brief handoff contract only where the current interview exposes a gap: what artifact, which checks passed, unresolved issues, and who receives/decides next. A step being complete is not permission to execute the next step. |
| `playbooks.md` — Run Mode: a human-input item includes work already attempted, missing information and the decision needed to unblock. | Refine our existing human-decision prompt to include attempted actions and evidence alongside options and impact. Preserve the state needed to resume rather than asking an isolated "Is this okay?". |
| `SKILL.md` — Autonomy Ladder and Dynamics: verification strength constrains autonomy; degraded quality can return a loop to reviewed operation. | In plain language, define a conditional fallback: if the agreed check becomes unavailable or untrustworthy, stop unattended progression and hand over the current result for review. Do not infer new authority merely from earlier successful runs. |
| `playbooks.md` — Correction-Log Mode: human corrections can become better context requirements, checks, instructions or accepted examples. | After a run, ask whether the correction is a one-off decision or a reusable rule. Propose an explicit rule update for confirmation; keep the execution record separate. Our skill already avoids rewriting its rules every iteration—preserve that boundary. |
| `SKILL.md` — Dynamics / Goodhart and `playbooks.md` — Rollout Mode: compare speed and quality, not automation volume alone. | At the end of a small trial, ask one lightweight usefulness question: did the loop save work while meeting the same acceptance standard? Optional timing plus observed corrections is sufficient; no dashboard needed. |

All row references refer to the commit-pinned files linked above.

## Do not adopt literally

- **A broad first-turn intake and default full operating-model output.** Upstream asks for company stage, goals, tools and bottlenecks and supports ten modes. Our audience benefits from one concrete work example and one question at a time. Keep the workshop-sized scope.
- **Treat every graph node as an iterative loop.** Upstream frames workflows as loops; our existing distinction is more precise for this workshop: a graph node may be deterministic, human-owned, or a loop, and a graph itself may contain cycles.
- **Escalate every failed verification immediately.** Upstream's collaboration/run checklist routes failure to a human. Our bounded local repair rule should remain: fix evidence-backed, authorized gaps within budget; escalate novel decisions, missing capability or non-progress.
- **Automatically modify the workflow after each human response.** Upstream recommends logging corrections and updating loops. A one-time exception is not a durable policy. Obtain confirmation before promoting it to reusable instructions or expanding authority.
- **Introduce L0–L5 terminology, runner-assignment matrices or a 14–30 day pilot by default.** These are useful enterprise operating-model devices, but unnecessary cognitive load for a one-hour, non-engineer interview exercise.
- **Use a second agent's opinion as equivalent to objective proof.** Upstream lists a second agent as one verifier option. Our checks should distinguish deterministic evidence, source-based checks and subjective review; consensus alone must not be reported as verified correctness.

## Minimal integration target

Most of the useful foundations already exist locally. Add only: (1) explicit handoff contents, (2) attempted actions in human-decision packets, (3) reviewed fallback when checks lose reliability, and (4) a confirmed distinction between one-off corrections and reusable rule changes. Cover these with interview scenarios; do not add modes, tools, dependencies or a separate execution framework.
