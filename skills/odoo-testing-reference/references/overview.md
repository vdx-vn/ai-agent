# Overview

Paths below are relative to:
- Docs repo: `<ODOO_DOCS_ROOT>`
- Source repo: `<ODOO_SOURCE_ROOT>`

## Primary routing rule
Use this skill only when the primary requested output is framework or test-authoring guidance. If the user asks whether current work is tested or safe, use `odoo-test`.

Replace the placeholders above with your local repo paths. All anchors below are relative to those roots. See `../../odoo-paths.md` for shared setup.

## Scope
Explain Odoo test framework primitives, tagging, and test-design patterns without acting as the live test-execution workflow skill.

## Primary artifact
Framework and test-authoring guidance for future or current test design, without claiming current-change readiness.

## Key checks
- Match test type to change surface and user-visible behavior.
- Use install vs post-install semantics correctly.
- Highlight tour or HttpCase needs for browser flows.
- Mention performance assertions when query count matters.

## Key docs anchors
- `content/developer/reference/backend/testing.rst`
- `content/developer/tutorials/unit_tests.rst`
- `content/developer/reference/cli.rst`

## Key source anchors
- `odoo/tests/common.py`
- `odoo/tests/form.py`
- `addons/account/tests`
- `addons/website_sale/tests`

## Frequent sibling skills
- `odoo-test`
- `odoo-performance`
- `odoo-view-ui`
