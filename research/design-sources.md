# Public skill design comparison

Reviewed 2026-09-17 against commit-pinned GitHub instruction files. No upstream scripts were installed or executed. This compares instruction design, not measured reliability, performance or cost.

The integration is independently written synthesis rather than copied templates or code. GitHub license metadata identified the repositories below as MIT. Before importing third-party files or substantial excerpts, check the pinned license and preserve its notices.

## Sources and decisions

| Source | Useful pattern | Local integration | Deliberately excluded |
|---|---|---|---|
| [0xArx/loopcoding-skill](https://github.com/0xArx/loopcoding-skill/blob/cb0486def1b2109c249cfb6d08af2850139d5ca4/SKILL.md) | Discover capabilities before interviewing unknowns; separate design from activation | Task-scoped capability checks and explicit missing-tool handoffs | Broad private configuration scans, assumed scheduling or multi-agent support, unverified performance figures |
| [AV-CSE31/loopright](https://github.com/AV-CSE31/loopright/blob/3c72e4ca7dbe00f1ac91d8e75c012c0575d49151/skills/loopright/SKILL.md) | Contracts covering state, progress, invariants, budget and evidence | Observable gaps, preserved standards and deterministic checks where applicable | Numerous modes, code scanners and a full technical taxonomy |
| [LoopRight agent-loop reference](https://github.com/AV-CSE31/loopright/blob/3c72e4ca7dbe00f1ac91d8e75c012c0575d49151/skills/loopright/references/agent-loops.md) | Preserve attempts and hypotheses; stored state can preserve mistakes; govern rule changes | Evidence-backed human questions and one-off versus durable corrections | Automatic generalization from one failure or expanded production authority |
| [kvergins/agent-org-designer](https://github.com/kvergins/codex-agent-org-designer-skill/blob/dac94295d70551ec4913c82d3942aca1d7fa13bc/agent-org-designer/SKILL.md) and [playbooks](https://github.com/kvergins/codex-agent-org-designer-skill/blob/dac94295d70551ec4913c82d3942aca1d7fa13bc/agent-org-designer/references/playbooks.md) | Local loops connected by handoffs; verifier strength constrains autonomy | Handoff contents, accountable owners and fallback when checks fail | Company-wide intake, autonomy levels, long rollouts and treating every node as a loop |
| [obra/superpowers brainstorming](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/skills/brainstorming/SKILL.md) | One question at a time, alternatives and incremental design confirmation | Conversational interviewing and confirmation before execution | Mandatory companion skills, repeated approval of already authorized routine work, visual server setup |
| [lunkerchen/loop-engineering-skill](https://github.com/lunkerchen/loop-engineering-skill/blob/0a17778e56ed29e0db93a8e2daedb940f65a51d1/SKILL.md) | Separate execution from verification; diagnose before changing approach | Comparison supporting evidence and bounded-retry rules | Assuming independent API calls remove bias, fixed cost claims, its open/closed classification, mandatory Hermes, subagents or cron |

See [the detailed Graph review](graph-skill-findings.md).

## Workshop-specific synthesis

Before generating a task skill, walk through success, missing data or failed checks, and out-of-scope or no-progress routes. This is our teaching adaptation of contracts, routing and failure handling, not a verbatim upstream procedure.

Use the same step names in Graph and local Loop. A tabletop walkthrough reveals design gaps; it is not evidence of execution.

## Script support added during the English rewrite

The independently authored [run helper](../references/run-helper.md) creates fresh run records and checks completion claims against required checks, evidence-file existence and revision budgets. It is not an imported upstream runtime. It adds no third-party dependencies or multi-agent requirement.

The helper cannot verify semantic truth, prevent edits outside its interface or make an agent comply. Keep its record checks separate from actual task verification and host permissions.

## Validation evidence and limits

The earlier instruction revision passed skill-format and whitespace validation. Two single-turn text probes used local Qwen3-Coder-Next with the then-current skill and no tool or file access:

- G: the reply refused to treat another agent's opinion or an earlier pass as current evidence. Its explanation was longer than desirable for the interview.
- H: the reply retained local-draft and no-sending boundaries without claiming a durable rule change. With no file writes, it did not prove correct exception persistence.
- E and F were specified but not executed.

Those probes predate the English rewrite and do not validate its behavior. Run the current automated tests using the command in [README.md](../README.md); they test mechanics, not interview quality. Full interviews, generated artifacts, second-input reuse and actual Claude Code/Codex execution remain separate verification tasks.

The English rewrite passed 16 automated tests on 2026-09-17, covering helper initialization, completion-record rejection, CLI behavior, local document links and untranslated CJK text. Skill-format validation and whitespace checks also passed. These results do not extend the earlier behavioral probes to the rewritten instructions.
