# Loop Designer

An interactive workflow-design skill by Seekrtech for Claude Code and Codex.

Start with a real work example, not a prompt-writing exercise. Your agent interviews you one question at a time, maps the workflow, and defines completion checks, bounded repairs and human decisions. This repository is in English; interviews follow your preferred language.

## Paste this into your agent

```text
Set up Seekrtech's Loop Designer skill:
https://github.com/seekrtech/loop-designer

Read INSTALL.md and SKILL.md from the same repository version first.
Confirm which agent tool and workspace I want; default to workspace-only installation.
Keep the repository as the single source and link it into the tool's skills directory.
Inspect existing directories or links, including broken links, without replacing them.
Preserve other skills, MCP connections, account settings and permissions.
Do not execute my actual workflow during installation.
Report the source commit, installation path and read-verification result.
If runtime discovery cannot be verified, say so and offer direct reading of SKILL.md.
Then ask, in my preferred language: "Which recurring part of your work would you like to stop supervising every time?"
Wait for my answer before continuing the interview.
```

See [INSTALL.md](INSTALL.md) for setup, verification and updates. No company account or Company Context connection is required.

## How the interview works

1. Describe one real task: what arrives and what must be handed over.
2. Clarify steps, branches, returns and handoffs.
3. Inspect the current Graph and select a small segment to automate.
4. Zoom into its Loop: act, check, repair, stop or ask a person.
5. Confirm the design, create a task-specific skill and try it within your authorization.

One core question per turn, with at most one related follow-up. Unknowns stay visible. You can correct the diagrams as the design evolves.

**Graph describes relationships between steps; Loop describes feedback-driven progress.** They overlap rather than form a hierarchy. Neither extra branches nor repeated revisions are required for their own sake.

## Deliverables

- `design.md`: workflow, local Loop, completion conditions and decisions.
- `skill/SKILL.md`: reusable instructions for your task.
- A separate run directory per execution: outputs, `run.json` checks and `run.md` decision notes.

For design only, say "Interview and design first; do not execute." Execution requires authorized material, available tools and a clear scope. Work products stay in your selected workspace, not this repository.

## Mechanical safeguards

The optional Python 3 helper creates fresh run directories without overwriting prior runs and validates completion records against pending checks, revision limits and missing evidence files. See [the run helper guide](references/run-helper.md).

It does not execute arbitrary commands, access company services, control every agent action or prove an evidence file's contents. Task-specific tests and human acceptance remain necessary. No third-party Python packages are required.

## Boundaries

This is a skill with supporting scripts, not an execution engine, security sandbox or background scheduler. Instructions do not replace tool permissions. Practice defaults exclude sending, publishing and production writes. Company Context is optional; authorized documents work too.

## Validation and research

From the repository root:

```sh
python3 -m unittest discover -s tests -v
git diff --check
```

Tests cover run creation, completion-record failures and repository hygiene. [Interview scenarios](tests/interview-cases.md) describe separate behavioral checks. Neither unit tests nor text probes prove end-to-end operation in every Claude Code or Codex version.

See [design sources and tradeoffs](research/design-sources.md) for the pinned public repositories behind environment discovery, loop contracts, handoffs and progressive interviewing.
