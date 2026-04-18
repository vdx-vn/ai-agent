# Overview

Paths below are relative to:
- Docs tree: `current Odoo docs tree`
- Source tree: `current Odoo CE source tree`

## Primary routing rule
Use this skill only when the primary requested output is a view, action, menu, template, or client-side UI decision.

Treat docs anchors as relative to the current Odoo docs tree and source anchors as relative to the current Odoo CE source tree. See `../../odoo-paths.md` for shared setup.

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
- `content/developer/reference/frontend.rst`
- `content/developer/reference/backend/http.rst`
- `content/contributing/development/coding_guidelines.rst`

## Key source anchors
- `odoo/addons/base/models/ir_ui_view.py`
- `addons/web`
- `addons/website_sale/controllers/main.py`

## Frequent sibling skills
- `odoo-build`
- `odoo-business-website-ecommerce`
- `odoo-architecture`
