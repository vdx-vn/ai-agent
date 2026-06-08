# Overview

Paths below are relative to:
- Docs repo: `<ODOO_DOCS_ROOT>`
- Source repo: `<ODOO_SOURCE_ROOT>`

## Project-local path resolution
Before using docs or source anchors, search upward from the current working directory for `.odoo-skills/project.json`. If it exists, read `docsRoot` as the Odoo docs tree and `sourceRoot` as the Odoo CE source tree. Prefer `.odoo-skills/project.json` over Docker Compose files, module READMEs, or ad hoc filesystem searches. If the config is absent, use the materialized placeholders above or ask for explicit roots.

## Primary routing rule
Use this skill only when the user wants release readiness or rollout sequencing. If the user needs CLI flag semantics or environment mechanics, hand off to `odoo-delivery-ops`. If the primary issue is data or schema evolution, compose with `odoo-upgrade-migration`.

Resolve the roots above from project setup first. All anchors below are relative to those roots. See `../../odoo-paths.md` for shared setup.

## Scope
Prepare release readiness for Odoo changes, including go or no-go criteria, staging checks, rollout sequencing, rollback considerations, and production-facing cautions.

## Primary artifact
Go or no-go rollout checklist with staging verification, release sequencing, rollback cautions, and production notes.

## Key checks
- Call out update or install order.
- Check migration, noupdate, and data-shape changes.
- List staging verification for critical workflows.
- Highlight public-route, accounting, inventory, or payroll risk.

## Key docs anchors
- `content/developer/reference/cli.rst`
- `content/administration/odoo_sh/getting_started/branches.rst`
- `content/administration/upgrade.rst`
- `content/developer/howtos/upgrade_custom_db.rst`

## Key source anchors
- `odoo/modules/loading.py`
- `odoo/modules/module.py`
- `odoo/http.py`

## Frequent sibling skills
- `odoo-delivery-ops`
- `odoo-upgrade-migration`
- `odoo-test`
