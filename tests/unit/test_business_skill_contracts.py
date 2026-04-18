import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SKILLS_DIR = ROOT / "skills"

BUSINESS_SKILLS = [
    "odoo-business-sales",
    "odoo-business-purchase",
    "odoo-business-inventory",
    "odoo-business-manufacturing",
    "odoo-business-accounting",
    "odoo-business-hr",
    "odoo-business-timesheet-project-services",
    "odoo-business-expenses",
    "odoo-business-website-ecommerce",
]

PLACEHOLDER_RE = re.compile(r"<ODOO_[A-Z0-9_]+>")
TODO_RE = re.compile(r"\b(?:TODO|TBD)\b", re.IGNORECASE)
REFERENCE_FILES = [
    "references/overview.md",
    "references/checklist.md",
    "references/examples.md",
]


class BusinessSkillContractsTests(unittest.TestCase):
    def test_business_skills_have_no_release_blockers(self) -> None:
        for skill in BUSINESS_SKILLS:
            skill_dir = SKILLS_DIR / skill
            files_to_check = [skill_dir / "SKILL.md"]
            files_to_check.extend(
                skill_dir / relative_path
                for relative_path in REFERENCE_FILES
                if (skill_dir / relative_path).exists()
            )

            for file_path in files_to_check:
                with self.subTest(skill=skill, file=str(file_path.relative_to(skill_dir))):
                    self.assertTrue(file_path.exists(), f"missing {file_path.name} for {skill}")

                    text = file_path.read_text(encoding="utf-8")
                    self.assertIsNone(
                        PLACEHOLDER_RE.search(text),
                        f"{skill} {file_path.relative_to(skill_dir)} has unresolved <ODOO_*> placeholder",
                    )
                    self.assertIsNone(
                        TODO_RE.search(text),
                        f"{skill} {file_path.relative_to(skill_dir)} has unresolved TODO/TBD marker",
                    )


if __name__ == "__main__":
    unittest.main()
