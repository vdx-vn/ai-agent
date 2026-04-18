import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PUBLIC_SKILLS_ROOT = ROOT / "skills"

REQUIRED_PUBLIC_SKILLS = {
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
    "odoo-business-sales",
    "odoo-business-purchase",
    "odoo-business-inventory",
    "odoo-business-manufacturing",
    "odoo-business-accounting",
    "odoo-business-hr",
    "odoo-business-timesheet-project-services",
    "odoo-business-expenses",
    "odoo-business-website-ecommerce",
}


class PublicSkillTreeTests(unittest.TestCase):
    def test_public_skill_directories_match_exact_approved_set(self) -> None:
        public_skill_dirs = {
            path.name for path in PUBLIC_SKILLS_ROOT.iterdir() if path.is_dir()
        }

        self.assertSetEqual(
            public_skill_dirs,
            REQUIRED_PUBLIC_SKILLS,
            "Public skills directory set mismatch. "
            f"Missing={sorted(REQUIRED_PUBLIC_SKILLS - public_skill_dirs)}, "
            f"Extra={sorted(public_skill_dirs - REQUIRED_PUBLIC_SKILLS)}",
        )

    def test_required_public_skills_exist_with_skill_md(self) -> None:
        missing_skill_files = [
            str(PUBLIC_SKILLS_ROOT / skill_name / "SKILL.md")
            for skill_name in sorted(REQUIRED_PUBLIC_SKILLS)
            if not (PUBLIC_SKILLS_ROOT / skill_name / "SKILL.md").exists()
        ]

        self.assertEqual(
            missing_skill_files,
            [],
            "Missing required public skill files: " + ", ".join(missing_skill_files),
        )

    def test_notebooklm_project_is_not_public(self) -> None:
        self.assertFalse(
            (PUBLIC_SKILLS_ROOT / "notebooklm-project").exists(),
            "skills/notebooklm-project must not exist",
        )

    def test_no_pycache_or_pyc_under_public_skills(self) -> None:
        pycache_dirs = [
            str(path)
            for path in PUBLIC_SKILLS_ROOT.rglob("__pycache__")
            if path.is_dir()
        ]
        pyc_files = [str(path) for path in PUBLIC_SKILLS_ROOT.rglob("*.pyc")]

        self.assertEqual(
            pycache_dirs,
            [],
            "__pycache__ directories must not exist under skills/: "
            + ", ".join(pycache_dirs),
        )
        self.assertEqual(
            pyc_files,
            [],
            ".pyc files must not exist under skills/: " + ", ".join(pyc_files),
        )


if __name__ == "__main__":
    unittest.main()
