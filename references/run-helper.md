# Run helper

Use this helper after the user confirms the completion conditions and local destination. It requires Python 3 with only the standard library. Resolve the script relative to the installed Loop Designer directory, not the current working directory.

## Initialize once per run

Example with synthetic document checks; replace these with the actual agreed conditions:

```sh
python3 /absolute/path/to/loop-designer/scripts/loop_run.py init /absolute/path/to/task/runs/trial-01 \
  --goal "Prepare a source-checked draft for human review" \
  --check "Names match the authorized source" \
  --check "Missing dates remain explicitly unresolved" \
  --max-revisions 2
```

The helper creates a new directory with:

- `contract.json`: agreed goal, conditions and revision limit.
- `run.json`: pending check results and a revision count starting at zero.
- `run.md`: a place for input references, skill version, actions, decisions and next steps.

An existing destination, including a symlink, is rejected. Choose a new run name; resume an existing run by reading it rather than reinitializing it. An interrupted initialization may leave a partial new directory; inspect it and choose another destination without deleting prior work.

## Execute and record

Perform the task through the authorized tools. Preserve original inputs. Save actual check output or human-review evidence inside the run directory, including source provenance where applicable. An external source can be cited in a local evidence report; never invent its contents.

Update `run.json` as work progresses. Count each revision after the initial output. A check starts as `pending`, can be `failed` or `unverified`, and becomes `passed` only after its substantive check succeeds. Record waiting, blocked or stopped work honestly; only use run status `complete` when every agreed condition has passed.

For example, a completed check entry could be:

```json
{
  "id": "c1",
  "status": "passed",
  "evidence": ["evidence/names-check.txt"]
}
```

Replace that path with an actual nonempty evidence file. Every original check ID must remain in the run record. Keep the contract unchanged during a run; an explicitly approved contract change belongs in a new run with the decision recorded. This is an instruction boundary, not tamper-proof storage.

## Validate before reporting completion

```sh
python3 /absolute/path/to/loop-designer/scripts/loop_run.py check /absolute/path/to/task/runs/trial-01
```

Exit code 0 means the record has a goal, a nonempty matching check set, a revision count within budget, complete/passed statuses and nonempty evidence files inside this run. Missing files, escaping paths, duplicate or omitted check IDs and unsupported completion claims return a nonzero exit code. The command is read-only.

This is not a task runner or sandbox. It cannot establish whether checks actually ran, whether evidence is truthful or fresh, whether the contract is appropriate, or whether an agent edited the contract or acted outside scope. Human review and task-specific verification remain necessary. Report the helper result separately from those checks.

If Python is unavailable, keep equivalent records manually and label mechanical validation unverified; do not install software without permission. For generated task skills, copy this guide and the script into their resources, or reference a verified persistent installation. Do not assume the original repository will always be present.
