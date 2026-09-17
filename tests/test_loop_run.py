import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "loop_run.py"
spec = importlib.util.spec_from_file_location("loop_run", SCRIPT)
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)


class RunTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.run = self.root / "trial"
        helper.create_run(self.run, "Source-checked draft", ["Names match", "Dates checked"])

    def write(self, filename, data):
        (self.run / filename).write_text(json.dumps(data), encoding="utf-8")

    def completed(self):
        (self.run / "evidence.txt").write_text("Synthetic test evidence", encoding="utf-8")
        record = helper.read_json(self.run / "run.json")
        record["status"] = "complete"
        record["revisions"] = 2
        for check in record["checks"]:
            check.update(status="passed", evidence=["evidence.txt"])
        self.write("run.json", record)
        return record

    def test_initialization_is_pending(self):
        record = helper.read_json(self.run / "run.json")
        self.assertEqual(record["status"], "in_progress")
        self.assertEqual(record["revisions"], 0)
        self.assertTrue(all(c["status"] == "pending" for c in record["checks"]))
        with self.assertRaises(ValueError):
            helper.validate_completion(self.run)

    def test_existing_run_is_unchanged(self):
        before = {p.name: p.read_bytes() for p in self.run.iterdir()}
        with self.assertRaises(FileExistsError):
            helper.create_run(self.run, "Different goal", ["Different check"])
        self.assertEqual(before, {p.name: p.read_bytes() for p in self.run.iterdir()})

    def test_symlink_destination_is_rejected(self):
        for name, target in [("existing", self.run), ("broken", self.root / "missing")]:
            link = self.root / name
            link.symlink_to(target, target_is_directory=True)
            with self.assertRaises(FileExistsError):
                helper.create_run(link, "Goal", ["Check"])

    def test_invalid_contract_input_creates_nothing(self):
        cases = [("", ["Check"], 2), ("Goal", [], 2), ("Goal", [" "], 2),
                 ("Goal", ["Same", " Same "], 2), ("Goal", ["Check"], -1)]
        for goal, checks, limit in cases:
            destination = self.root / "invalid"
            with self.assertRaises(ValueError):
                helper.create_run(destination, goal, checks, limit)
            self.assertFalse(destination.exists())

    def test_complete_record_passes_without_mutation(self):
        self.completed()
        before = (self.run / "run.json").read_bytes()
        self.assertEqual(helper.validate_completion(self.run), 2)
        self.assertEqual((self.run / "run.json").read_bytes(), before)

    def test_incomplete_statuses_fail(self):
        for status in ["pending", "failed", "unverified"]:
            record = self.completed()
            record["checks"][0]["status"] = status
            self.write("run.json", record)
            with self.subTest(status=status), self.assertRaises(ValueError):
                helper.validate_completion(self.run)

    def test_missing_or_duplicate_check_fails(self):
        for change in ["remove", "duplicate", "extra"]:
            record = self.completed()
            if change == "remove":
                record["checks"].pop()
            elif change == "duplicate":
                record["checks"].append(record["checks"][0])
            else:
                record["checks"].append({"id": "c3", "status": "passed", "evidence": ["evidence.txt"]})
            self.write("run.json", record)
            with self.subTest(change=change), self.assertRaises(ValueError):
                helper.validate_completion(self.run)

    def test_invalid_revision_counts_fail(self):
        for value in [3, -1, True, 1.5, "2", None]:
            record = self.completed()
            record["revisions"] = value
            self.write("run.json", record)
            with self.subTest(value=value), self.assertRaises(ValueError):
                helper.validate_completion(self.run)

    def test_invalid_evidence_fails(self):
        outside = self.root / "outside.txt"
        outside.write_text("Outside this run", encoding="utf-8")
        (self.run / "escape.txt").symlink_to(outside)
        (self.run / "empty.txt").touch()
        for evidence in [[], ["missing.txt"], ["empty.txt"], ["."],
                         ["../outside.txt"], ["escape.txt"], [str(outside)], [42]]:
            record = self.completed()
            record["checks"][0]["evidence"] = evidence
            self.write("run.json", record)
            with self.subTest(evidence=evidence), self.assertRaises((ValueError, OSError)):
                helper.validate_completion(self.run)

    def test_malformed_records_fail(self):
        for content in ["not json", "[]", "null"]:
            (self.run / "run.json").write_text(content, encoding="utf-8")
            with self.subTest(content=content), self.assertRaises(ValueError):
                helper.validate_completion(self.run)

    def test_empty_contract_is_not_a_vacuous_pass(self):
        self.completed()
        contract = helper.read_json(self.run / "contract.json")
        contract["checks"] = []
        self.write("contract.json", contract)
        with self.assertRaises(ValueError):
            helper.validate_completion(self.run)

    def test_cli_failure_and_success(self):
        before = subprocess.run([sys.executable, str(SCRIPT), "check", str(self.run)],
                                capture_output=True, text=True)
        self.assertEqual(before.returncode, 1)
        self.completed()
        after = subprocess.run([sys.executable, str(SCRIPT), "check", str(self.run)],
                               capture_output=True, text=True)
        self.assertEqual(after.returncode, 0)
        self.assertIn("does not verify", after.stdout)

    def test_cli_init(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "init", str(self.root / "cli"),
             "--goal", "Goal", "--check", "Condition"],
            capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((self.root / "cli" / "run.json").is_file())


if __name__ == "__main__":
    unittest.main()
