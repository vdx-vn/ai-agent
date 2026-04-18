import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SKILLS_DIR = ROOT / "skills"

TASK_TECH_SKILLS = [
    "odoo-think",
    "odoo-plan",
    "odoo-build",
    "odoo-review",
    "odoo-test",
    "odoo-ship",
    "odoo-reflect",
    "odoo-delivery-ops",
    "odoo-local-test-harness",
    "odoo-architecture",
    "odoo-orm-modeling",
    "odoo-view-ui",
    "odoo-security",
    "odoo-testing-reference",
    "odoo-performance",
    "odoo-integration-api",
    "odoo-upgrade-migration",
]

REQUIRED_SECTIONS = [
    "# Purpose",
    "# Primary routing rule",
    "# Use this skill when",
    "# Do not use this skill when",
    "# Required inputs",
    "# Workflow",
    "# Output contract",
]

PLACEHOLDER_RE = re.compile(r"<ODOO_[A-Z0-9_]+>")
TODO_RE = re.compile(r"\b(?:TODO|TBD)\b", re.IGNORECASE)


class SkillContractsTests(unittest.TestCase):
    def test_task_technical_skills_match_contract(self) -> None:
        for skill in TASK_TECH_SKILLS:
            with self.subTest(skill=skill):
                skill_path = SKILLS_DIR / skill / "SKILL.md"
                self.assertTrue(skill_path.exists(), f"missing SKILL.md for {skill}")
                text = skill_path.read_text(encoding="utf-8")

                for section in REQUIRED_SECTIONS:
                    self.assertIn(section, text, f"{skill} missing section {section}")

                self.assertIsNone(
                    PLACEHOLDER_RE.search(text),
                    f"{skill} has unresolved <ODOO_*> placeholder",
                )
                self.assertIsNone(
                    TODO_RE.search(text),
                    f"{skill} has unresolved TODO/TBD marker",
                )


if __name__ == "__main__":
    unittest.main()
