# Agent setup guide

Install Loop Designer; do not execute the user's workflow. Read this guide and `SKILL.md` from the same version. Stay within the requested scope. If network or filesystem access is unavailable, report the limitation rather than changing sources or permissions.

## 1. Confirm the target

Identify Claude Code, Codex, or both, and confirm the absolute workspace path. Default to workspace-only installation. Use personal scope only when requested. Both tools should reference the same checkout.

| Tool | Workspace entry | Personal entry, when requested |
|---|---|---|
| Codex | `<workspace>/.agents/skills/loop-designer` | `~/.agents/skills/loop-designer` |
| Claude Code | `<workspace>/.claude/skills/loop-designer` | `~/.claude/skills/loop-designer` |

The entry must expose `SKILL.md`. This repository's root is the skill source.

## 2. Obtain and inspect the source

Choose a persistent checkout location, not a temporary directory. Clone:

```text
https://github.com/seekrtech/loop-designer.git
```

If the destination exists, inspect its origin, local changes and commit first. Preserve existing files and modifications. Using an existing checkout is not permission to update it silently.

Read the instructions and confirm frontmatter name `loop-designer`. Inspect `scripts/loop_run.py` before using it. Record the full commit SHA and disclose local modifications. Installation needs no setup script, third-party package, MCP configuration or API key. The optional run helper requires Python 3; its absence does not prevent the interview.

## 3. Create the entry

Inspect the parent and target, including broken symlinks. Report conflicts and ask before changing them. Reuse an entry already pointing to the correct source.

Create a directory symlink to the resolved absolute repository root. On macOS/Linux use `ln -s` without force options. If symlinks are unsupported, explain and ask whether to use a copy. A copy must include `SKILL.md`, `scripts/loop_run.py` and `references/run-helper.md`; omit `.git`, tests and user outputs. A copy is a versioned snapshot requiring deliberate updates.

If an entry cannot be created, offer direct reading of the source without claiming installation succeeded. Preserve unrelated skills, AGENTS.md, CLAUDE.md, MCP and permissions. Installation does not authorize commits or pushes in the user's workspace.

## 4. Verify and hand off

1. Read `SKILL.md` through the installed entry and compare it with the source. Confirm script and guide references resolve.
2. Report source URL, full SHA, local modification status, scope and absolute entry path.
3. Check whether the tool discovers `loop-designer`. A new conversation or reload may be needed. File existence is not runtime discovery.
4. If invocation is available, try "Interview only; do not execute." Verify it asks a core question and waits instead of inventing a complete workflow. Mark this unverified if you cannot perform it.
5. Offer invocation through the skill selector or direct reading of the verified absolute path.

An installation smoke test does not authorize company-data access or real workflow execution. The user still chooses material and scope.

## Updates and removal

For an authorized update, verify remote, branch and clean working tree, then fast-forward, inspect changes and repeat verification. Stop on divergence or local edits; do not force-reset. Loaded instructions may require a new conversation.

For removal, remove only the confirmed tool entry, preserving the source checkout and work products. Confirm scope and backup before removing a copied installation.

## Official references

The initial setup design was checked against these sources on 2026-09-17. Product versions and organization policies may differ; use current documentation and actual verification when they do.

- [Codex: Build skills](https://learn.chatgpt.com/docs/build-skills)
- [Claude Code: Extend Claude with skills](https://code.claude.com/docs/en/skills)
