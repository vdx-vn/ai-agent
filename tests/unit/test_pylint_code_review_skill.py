import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2] / "skills" / "pylint-code-review"


class PylintCodeReviewSkillTests(unittest.TestCase):
    def test_skill_exists_with_required_contract(self) -> None:
        skill = ROOT / "SKILL.md"
        script = ROOT / "scripts" / "check_pylint.py"
        overview = ROOT / "references" / "overview.md"
        checklist = ROOT / "references" / "checklist.md"
        examples = ROOT / "references" / "examples.md"
        checks = ROOT / "references" / "pylint_checks.md"

        self.assertTrue(skill.exists(), skill)
        self.assertTrue(script.exists(), script)
        self.assertTrue(overview.exists(), overview)
        self.assertTrue(checklist.exists(), checklist)
        self.assertTrue(examples.exists(), examples)
        self.assertTrue(checks.exists(), checks)

        skill_text = skill.read_text(encoding="utf-8")
        for heading in [
            "# Purpose",
            "# Primary routing rule",
            "# Use this skill when",
            "# Do not use this skill when",
            "# Required inputs",
            "# Workflow",
            "# Output contract",
        ]:
            with self.subTest(heading=heading):
                self.assertIn(heading, skill_text)

        self.assertIn("scripts/check_pylint.py", skill_text)
        self.assertIn("references/pylint_checks.md", skill_text)

        overview_text = overview.read_text(encoding="utf-8")
        self.assertIn("## Primary routing rule", overview_text)
        self.assertIn("non-Python", overview_text)


if __name__ == "__main__":
    unittest.main()
