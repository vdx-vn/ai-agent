# Overview

Paths below are relative to:
- Docs repo: `<ODOO_DOCS_ROOT>`
- Source repo: `<ODOO_SOURCE_ROOT>`

## Project-local path resolution
Before using docs or source anchors, search upward from the current working directory for `.odoo-skills/project.json`. If it exists, read `docsRoot` as the Odoo docs tree and `sourceRoot` as the Odoo CE source tree. Prefer `.odoo-skills/project.json` over Docker Compose files, module READMEs, or ad hoc filesystem searches. If the config is absent, use the materialized placeholders above or ask for explicit roots.

## Primary routing rule
Use this skill only when the primary requested output is a view, action, menu, template, or client-side UI decision.

Resolve the roots above from project setup first. All anchors below are relative to those roots. See `../../odoo-paths.md` for shared setup.

## Scope
Guide Odoo views, actions, menus, QWeb, backend UI, and OWL or web-client UI changes.

## Primary artifact
UI guidance with view strategy, inheritance notes, and action or menu recommendations.

## Key checks
- Prefer view inheritance over full replacements when stable.
- Keep menus and actions aligned with business flow.
- Call out fragile xpath or template overrides.
- Separate backend UI concerns from website or ecommerce entrypoints when needed.

## Key docs anchors
- `content/developer/reference/frontend/` (subdirectory; frontend.rst is a thin toctree stub in v19)
- `content/developer/reference/backend/http.rst`
- `content/contributing/development/coding_guidelines.rst`

## Key source anchors
- `odoo/addons/base/models/ir_ui_view.py`
- `addons/web`
- `addons/website_sale/controllers/main.py`

## Frequent sibling skills
- `odoo-build`
- `odoo-architecture`
