# Overview

Paths below are relative to:
- Docs tree: `current Odoo docs tree`
- Source tree: `current Odoo CE source tree`

## Primary routing rule
Use this skill only when the primary requested output is validation for a concrete change now. If the user asks which Odoo test framework or tags to use in general, hand off to `odoo-testing-reference`.

Treat docs anchors as relative to the current Odoo docs tree and source anchors as relative to the current Odoo CE source tree. See `../../odoo-paths.md` for shared setup.

## Scope
Define and run validation for a current Odoo change, including install, update, workflow, security, and performance checks.

## Primary artifact
Current-change validation evidence or validation plan tied to a specific diff, addon, bug, or runtime scenario.

## Key checks
- Choose the smallest validation surface that can prove the current change.
- Use a named disposable database when local harness execution is requested.
- Compose with shared DB and filestore cleanup when local execution uses `odoo-local-test-harness`.
- Choose test type by change surface: unit, transaction, HTTP, JS, tour, performance.
- Cover install and update paths when relevant.
- Include security and multi-company checks when behavior changes.
- Report gaps, not only pass/fail.
- Compose with `odoo-local-test-harness` when local execution depends on `ODOO_TEST_BASE_CMD` or shared DB and filestore cleanup.

## Key docs anchors
- `content/developer/reference/backend/testing.rst`
- `content/developer/tutorials/unit_tests.rst`
- `content/developer/reference/backend/performance.rst`
- `content/developer/reference/cli.rst`

## Key source anchors
- `odoo/tests/common.py`
- `odoo/tests/form.py`
- `addons/account/tests`
- `addons/sale_stock/tests`
- `addons/purchase_stock/tests`

## Frequent sibling skills
- `odoo-testing-reference`
- `odoo-performance`
