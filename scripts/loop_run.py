#!/usr/bin/env python3
"""Create isolated run records and validate completion claims, not task correctness."""

import argparse
import json
from pathlib import Path
import sys


def read_json(path):
    with path.open(encoding="utf-8") as source:
        return json.load(source)


def write_json(path, value):
    with path.open("x", encoding="utf-8") as target:
        json.dump(value, target, indent=2, ensure_ascii=False)
        target.write("\n")


def nonnegative_int(value):
    return type(value) is int and value >= 0


def create_run(destination, goal, conditions, max_revisions=2):
    """Only initialize a new directory; never modify a preexisting destination."""
    if not goal.strip() or not conditions or any(not c.strip() for c in conditions):
        raise ValueError("A goal and at least one nonempty completion condition are required.")
    if not nonnegative_int(max_revisions):
        raise ValueError("The revision budget must be a nonnegative integer.")
    if len(set(c.strip() for c in conditions)) != len(conditions):
        raise ValueError("Completion conditions must be distinct.")
    contract = {
        "goal": goal.strip(),
        "max_revisions": max_revisions,
        "checks": [
            {"id": f"c{index}", "condition": condition.strip()}
            for index, condition in enumerate(conditions, 1)
        ],
    }
    destination = Path(destination).absolute()
    destination.mkdir(parents=True, exist_ok=False)
    write_json(destination / "contract.json", contract)
    write_json(destination / "run.json", {
        "status": "in_progress",
        "revisions": 0,
        "checks": [
            {"id": check["id"], "status": "pending", "evidence": []}
            for check in contract["checks"]
        ],
    })
    with (destination / "run.md").open("x", encoding="utf-8") as target:
        target.write("# Run notes\n\n"
                     "Record authorized input locations, skill version, actions, "
                     "human decisions, unresolved issues and the next step here.\n"
                     "This initialized record is not evidence of execution.\n")
    return destination


def validate_completion(directory):
    """Reject incomplete records; existing evidence still needs substantive review."""
    directory = Path(directory).resolve(strict=True)
    contract = read_json(directory / "contract.json")
    record = read_json(directory / "run.json")
    if not isinstance(contract, dict) or not isinstance(record, dict):
        raise ValueError("Contract and run record must be JSON objects.")
    if not isinstance(contract.get("goal"), str) or not contract["goal"].strip():
        raise ValueError("The contract needs a goal.")
    limit, revisions = contract.get("max_revisions"), record.get("revisions")
    if not nonnegative_int(limit) or not nonnegative_int(revisions):
        raise ValueError("Revision count and budget must be nonnegative integers.")
    if revisions > limit:
        raise ValueError("Revision budget exceeded; a revised agreement is required.")
    expected, actual = contract.get("checks"), record.get("checks")
    if not isinstance(expected, list) or not expected or not isinstance(actual, list):
        raise ValueError("An agreed, nonempty check list and run results are required.")

    def index_checks(checks):
        indexed = {}
        for check in checks:
            if not isinstance(check, dict):
                raise ValueError("Each check must be an object.")
            key = check.get("id")
            if not isinstance(key, str) or not key.strip() or key in indexed:
                raise ValueError("Check IDs must be unique, nonempty strings.")
            indexed[key] = check
        return indexed

    required = index_checks(expected)
    results = index_checks(actual)
    for check in required.values():
        if not isinstance(check.get("condition"), str) or not check["condition"].strip():
            raise ValueError("Every agreed check needs a completion condition.")
    if required.keys() != results.keys():
        raise ValueError("Run checks must match the agreed contract; none may be dropped or added.")
    if record.get("status") != "complete":
        raise ValueError("Run is not marked complete.")
    for key, check in results.items():
        if check.get("status") != "passed":
            raise ValueError(f"{key}: check has not passed.")
        evidence = check.get("evidence")
        if not isinstance(evidence, list) or not evidence:
            raise ValueError(f"{key}: evidence files are required.")
        for item in evidence:
            if not isinstance(item, str) or not item.strip() or Path(item).is_absolute():
                raise ValueError(f"{key}: evidence must be a relative file path inside this run.")
            path = (directory / item).resolve(strict=True)
            if directory not in path.parents:
                raise ValueError(f"{key}: evidence escapes this run directory.")
            if not path.is_file() or path.stat().st_size == 0:
                raise ValueError(f"{key}: evidence must be an existing, nonempty file.")
    return len(required)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    init = commands.add_parser("init", help="Create a fresh run with pending checks.")
    init.add_argument("directory", type=Path)
    init.add_argument("--goal", required=True)
    init.add_argument("--check", action="append", required=True, dest="conditions")
    init.add_argument("--max-revisions", type=int, default=2)
    check = commands.add_parser("check", help="Validate a completion record without changing it.")
    check.add_argument("directory", type=Path)
    args = parser.parse_args()
    try:
        if args.command == "init":
            path = create_run(args.directory, args.goal, args.conditions, args.max_revisions)
            print(f"Created {path}; all checks are pending. No task has been executed.")
        else:
            count = validate_completion(args.directory)
            print(f"Completion record valid: {count} checks have evidence files. "
                  "This does not verify evidence truth or task quality.")
    except (ValueError, OSError, RuntimeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
