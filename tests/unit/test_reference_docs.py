import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

REQUIRED_DOCS = {
    ROOT / "docs" / "reference" / "library-manifest.md",
    ROOT / "docs" / "reference" / "shared-taxonomy.md",
    ROOT / "docs" / "reference" / "trigger-matrix.md",
    ROOT / "docs" / "reference" / "evaluation-harness.md",
    ROOT / "docs" / "reference" / "skill-inventory.json",
    ROOT / "docs" / "reference" / "odoo-paths.md",
    ROOT / "docs" / "authoring" / "odoo-paths.md",
}


class ReferenceDocsTests(unittest.TestCase):
    def test_required_reference_docs_exist(self) -> None:
        missing = [str(path) for path in sorted(REQUIRED_DOCS) if not path.exists()]
        self.assertEqual(
            missing,
            [],
            "Missing required reference docs: " + ", ".join(missing),
        )

    def test_skill_inventory_names_match_skills_directory_names(self) -> None:
        inventory_path = ROOT / "docs" / "reference" / "skill-inventory.json"
        inventory_data = json.loads(inventory_path.read_text(encoding="utf-8"))

        inventory_names = {entry["name"] for entry in inventory_data["skills"]}
        skill_dir_names = {
            path.name for path in (ROOT / "skills").iterdir() if path.is_dir()
        }

        self.assertSetEqual(
            inventory_names,
            skill_dir_names,
            "skill-inventory.json names must exactly match directories under skills/",
        )


if __name__ == "__main__":
    unittest.main()
