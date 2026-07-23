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

## Project config precedence
Installed skills should search upward from the current working directory for `.odoo-skills/project.json` before resolving docs and source paths. Prefer `.odoo-skills/project.json` over Docker Compose files, module READMEs, or ad hoc filesystem searches because it stores the authoritative `docsRoot` and `sourceRoot` for the current project. Odoo test execution is handled by the separately-installed `odoo-cli` package, which reads `config/project.json` in the target Odoo project.

## Recommended workflow
1. Install repo entrypoints first with `python3 -m pip install -e .` from repo root.
2. Only do this for a local Odoo repository that needs local docs/source integration.
3. Run `odoo-skills project-setup` from the Odoo project root.
4. If `odoo-skills` is not on PATH, run `python3 -m tooling.cli project-setup`.
5. Command will ask for docs root, source root, and version if auto-detection fails, then write `.odoo-skills/project.json` and `.claude/odoo-skill-paths.json` for that project.
6. For Odoo test execution, install the separately-packaged `odoo-cli` in your Odoo project's Python environment and run `odoo runtime-test` with the desired options.
7. If you prefer to keep placeholders, mentally substitute `<ODOO_DOCS_ROOT>` and `<ODOO_SOURCE_ROOT>` when reading skill references.

## Version target
This library was authored against:
- Odoo documentation branch <ODOO_SERIES>
- Odoo Community source branch <ODOO_SERIES>
