import json
import tempfile
import unittest
from pathlib import Path

from tooling.materialization.materialize_odoo_skill_paths import materialize_skills


class MaterializeSkillsTests(unittest.TestCase):
    def test_materialize_replaces_placeholders_and_writes_richer_config(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            docs_root = root / "odoo-docs-18.0"
            source_root = root / "odoo-src"
            skills_root = root / "skills"
            config_path = root / "config" / "odoo-skill-paths.json"
            target_file = skills_root / "odoo-build" / "SKILL.md"

            docs_root.mkdir()
            source_root.mkdir()
            target_file.parent.mkdir(parents=True)
            target_file.write_text(
                "Docs: <ODOO_DOCS_ROOT>\n"
                "Source: <ODOO_SOURCE_ROOT>\n"
                "Series: <ODOO_SERIES>\n"
                "Major: <ODOO_MAJOR_VERSION>\n",
                encoding="utf-8",
            )

            result = materialize_skills(
                docs_root=docs_root,
                source_root=source_root,
                version="18.0",
                skills_root=skills_root,
                config_path=config_path,
                extra_metadata={"project": "demo"},
            )

            self.assertEqual(result.version, "18.0")
            self.assertEqual(result.major_version, "18")
            self.assertEqual(result.version_source, "--version")
            self.assertEqual(result.mode, "initial")
            self.assertEqual(result.materialized_files, [target_file])

            self.assertEqual(
                target_file.read_text(encoding="utf-8"),
                f"Docs: {docs_root}\n"
                f"Source: {source_root}\n"
                "Series: 18.0\n"
                "Major: 18\n",
            )

            config = json.loads(config_path.read_text(encoding="utf-8"))
            self.assertEqual(config["docsRoot"], str(docs_root))
            self.assertEqual(config["sourceRoot"], str(source_root))
            self.assertEqual(config["version"], "18.0")
            self.assertEqual(config["majorVersion"], "18")
            self.assertEqual(config["versionSource"], "--version")
            self.assertEqual(config["skillsRoot"], str(skills_root))
            self.assertEqual(config["mode"], "initial")
            self.assertEqual(config["materializedFiles"], [str(target_file)])
            self.assertIn("materializedAt", config)
            self.assertEqual(config["project"], "demo")

    def test_materialize_force_rewrites_existing_values(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            old_docs_root = root / "odoo-docs-17.0"
            old_source_root = root / "odoo-src-17.0"
            new_docs_root = root / "odoo-docs-18.0"
            new_source_root = root / "odoo-src-18.0"
            skills_root = root / "skills"
            config_path = root / "config" / "odoo-skill-paths.json"
            target_file = skills_root / "odoo-build" / "SKILL.md"

            old_docs_root.mkdir()
            old_source_root.mkdir()
            new_docs_root.mkdir()
            new_source_root.mkdir()
            target_file.parent.mkdir(parents=True)
            target_file.write_text(
                f"Docs: {old_docs_root}\n"
                f"Source: {old_source_root}\n"
                "Odoo CE 17\n"
                "branch 17.0\n",
                encoding="utf-8",
            )
            config_path.parent.mkdir(parents=True)
            config_path.write_text(
                json.dumps(
                    {
                        "docsRoot": str(old_docs_root),
                        "sourceRoot": str(old_source_root),
                        "version": "17.0",
                        "majorVersion": "17",
                    }
                ),
                encoding="utf-8",
            )

            result = materialize_skills(
                docs_root=new_docs_root,
                source_root=new_source_root,
                version="18.0",
                skills_root=skills_root,
                config_path=config_path,
                force=True,
            )

            self.assertEqual(result.mode, "force")
            self.assertEqual(result.materialized_files, [target_file])
            self.assertEqual(
                target_file.read_text(encoding="utf-8"),
                f"Docs: {new_docs_root}\n"
                f"Source: {new_source_root}\n"
                "Odoo CE 18\n"
                "branch 18.0\n",
            )

            config = json.loads(config_path.read_text(encoding="utf-8"))
            self.assertEqual(config["mode"], "force")
            self.assertEqual(config["materializedFiles"], [str(target_file)])

    def test_materialize_force_rewrites_series_and_major_from_prior_materialization(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            docs_root_v18 = root / "odoo-docs-18.0"
            source_root_v18 = root / "odoo-src-18.0"
            docs_root_v19 = root / "odoo-docs-19.0"
            source_root_v19 = root / "odoo-src-19.0"
            skills_root = root / "skills"
            config_path = root / "config" / "odoo-skill-paths.json"
            target_file = skills_root / "odoo-build" / "SKILL.md"

            docs_root_v18.mkdir()
            source_root_v18.mkdir()
            docs_root_v19.mkdir()
            source_root_v19.mkdir()
            target_file.parent.mkdir(parents=True)
            target_file.write_text(
                "Docs: <ODOO_DOCS_ROOT>\n"
                "Source: <ODOO_SOURCE_ROOT>\n"
                "Series: <ODOO_SERIES>\n"
                "Major: <ODOO_MAJOR_VERSION>\n",
                encoding="utf-8",
            )

            materialize_skills(
                docs_root=docs_root_v18,
                source_root=source_root_v18,
                version="18.0",
                skills_root=skills_root,
                config_path=config_path,
            )

            result = materialize_skills(
                docs_root=docs_root_v19,
                source_root=source_root_v19,
                version="19.0",
                skills_root=skills_root,
                config_path=config_path,
                force=True,
            )

            self.assertEqual(result.mode, "force")
            self.assertEqual(result.materialized_files, [target_file])
            self.assertEqual(
                target_file.read_text(encoding="utf-8"),
                f"Docs: {docs_root_v19}\n"
                f"Source: {source_root_v19}\n"
                "Series: 19.0\n"
                "Major: 19\n",
            )

    def test_materialize_dry_run_reports_changes_without_writing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            docs_root = root / "odoo-docs-18.0"
            source_root = root / "odoo-src"
            skills_root = root / "skills"
            config_path = root / "config" / "odoo-skill-paths.json"
            target_file = skills_root / "odoo-build" / "SKILL.md"

            docs_root.mkdir()
            source_root.mkdir()
            target_file.parent.mkdir(parents=True)
            original_text = "Docs: <ODOO_DOCS_ROOT>\nSeries: <ODOO_SERIES>\n"
            target_file.write_text(original_text, encoding="utf-8")

            result = materialize_skills(
                docs_root=docs_root,
                source_root=source_root,
                version="18.0",
                skills_root=skills_root,
                config_path=config_path,
                dry_run=True,
            )

            self.assertEqual(result.mode, "dry-run")
            self.assertEqual(result.materialized_files, [target_file])
            self.assertEqual(target_file.read_text(encoding="utf-8"), original_text)
            self.assertFalse(config_path.exists())


if __name__ == "__main__":
    unittest.main()
