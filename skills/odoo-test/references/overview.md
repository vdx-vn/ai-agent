# Overview

Paths below are relative to:
- Docs tree: `current Odoo docs tree`
- Source tree: `current Odoo CE source tree`

## Project-local path resolution
Before using docs or source anchors, search upward from the current working directory for `.odoo-skills/project.json`. If it exists, read `docsRoot` as the Odoo docs tree and `sourceRoot` as the Odoo CE source tree. Prefer `.odoo-skills/project.json` over Docker Compose files, module READMEs, or ad hoc filesystem searches. If the config is absent, use the materialized placeholders above or ask for explicit roots.

## Primary routing rule
Use this skill only when the primary requested output is validation for a concrete change now. If the user asks which Odoo test framework or tags to use in general, hand off to `odoo-testing-reference`.

Resolve the roots above from project setup first; then treat docs anchors as relative to the current Odoo docs tree and source anchors as relative to the current Odoo CE source tree. See `../../odoo-paths.md` for shared setup.

## Scope
Define and run validation for a current Odoo change, including install, update, workflow, security, and performance checks.

## Primary artifact
Current-change validation evidence or validation plan tied to a specific diff, addon, bug, or runtime scenario.

## Key checks
- Choose the smallest validation surface that can prove the current change.
- Run tests with `odoo runtime-test --module <name...>` (odoo-cli, installed in the project's Python environment) — the only supported test-execution command; do not invoke `odoo-bin`/pytest-odoo directly.
- Use `--init update` on `odoo runtime-test` to cover install/update paths, `--tests` to target specific files, and `--db` to select the target database.
- Choose test type by change surface: unit, transaction, HTTP, JS, tour, performance.
- Cover install and update paths when relevant.
- Include security and multi-company checks when behavior changes.
- Report gaps, not only pass/fail.

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
