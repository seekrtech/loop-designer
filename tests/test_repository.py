from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]


class RepositoryTests(unittest.TestCase):
    def documents(self):
        return [p for p in ROOT.rglob("*.md")
                if not any(part.startswith(".") for part in p.relative_to(ROOT).parts)]

    def test_no_untranslated_cjk_text(self):
        # A regression check for this English rewrite, not a language classifier.
        for path in self.documents():
            with self.subTest(path=path.relative_to(ROOT)):
                self.assertIsNone(re.search(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]",
                                            path.read_text(encoding="utf-8")))

    def test_local_document_links_resolve(self):
        for path in self.documents():
            for target in re.findall(r"\]\(([^)]+)\)", path.read_text(encoding="utf-8")):
                if "://" in target or target.startswith("#"):
                    continue
                with self.subTest(source=path.name, target=target):
                    self.assertTrue((path.parent / target.split("#")[0]).is_file())

    def test_skill_identity_and_bundled_resources(self):
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertTrue(skill.startswith("---\nname: loop-designer\ndescription: "))
        self.assertEqual(len(skill.split("---\n", 2)), 3)
        self.assertTrue((ROOT / "scripts" / "loop_run.py").is_file())
        self.assertTrue((ROOT / "references" / "run-helper.md").is_file())


if __name__ == "__main__":
    unittest.main()
