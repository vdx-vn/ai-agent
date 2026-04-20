# Odoo Path Setup

Set these values for your environment before using the skill library:

- `<ODOO_DOCS_ROOT>` = absolute path to your local Odoo documentation clone
- `<ODOO_SOURCE_ROOT>` = absolute path to your local Odoo source clone
- `<ODOO_SERIES>` = Odoo branch or series like `17.0`, `18.0`, or `19.0`
- `<ODOO_MAJOR_VERSION>` = major version like `17`, `18`, or `19`

## Example
- `<ODOO_DOCS_ROOT>` = `/path/to/odoo/documentation`
- `<ODOO_SOURCE_ROOT>` = `/path/to/odoo/odoo`

## How to use these placeholders
- In skill reference files, paths under `content/...` are relative to `<ODOO_DOCS_ROOT>`.
- Paths under `odoo/...` or `addons/...` are relative to `<ODOO_SOURCE_ROOT>`.
- Version phrases inside the skills use `<ODOO_SERIES>` and `<ODOO_MAJOR_VERSION>`.
- If your team keeps multiple Odoo versions, point these placeholders at the exact version the skill library targets.

## Recommended workflow
1. Decide which Odoo docs repo and source repo are authoritative for the current project.
2. For a project-local copy, run:
   `python3 .claude/skills/scripts/materialize_odoo_skill_paths.py --docs-root /path/to/odoo/documentation --source-root /path/to/odoo/source`
3. The script will try to detect `<ODOO_SERIES>` automatically from git branch names or repo path names. If detection fails, pass `--version 18.0` or another supported series.
4. This writes `.claude/odoo-skill-paths.json` and replaces placeholders inside this project copy.
5. Project hooks can suggest this command automatically when you start a new Odoo project or ask to set one up.
6. If you prefer to keep placeholders, mentally substitute `<ODOO_DOCS_ROOT>` and `<ODOO_SOURCE_ROOT>` when reading skill references.

## Version target
This library was authored against:
- Odoo documentation branch <ODOO_SERIES>
- Odoo Community source branch <ODOO_SERIES>

## Local test harness config

For each Odoo project, keep the local base test command in `.claude/settings.local.json`:

```json
{
  "env": {
    "ODOO_TEST_BASE_CMD": "/path/to/python /path/to/odoo-bin -c /path/to/odoo.conf"
  }
}
```

`odoo-local-test-harness` treats this as the immutable base command, then appends `-d`, `--test-tags`, `--test-enable`, `-i` or `-u`, and `--stop-after-init` safely.
Keep this file local and uncommitted.
