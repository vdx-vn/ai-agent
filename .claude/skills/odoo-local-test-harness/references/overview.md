# Overview

Paths below are relative to:
- Docs repo: `<ODOO_DOCS_ROOT>`
- Source repo: `<ODOO_SOURCE_ROOT>`

## Primary routing rule
Use this skill when the task depends on a project-local Odoo test command or shared local cleanup behavior. If the primary output is current-change validation evidence, compose with `odoo-test`. If the primary output is only CLI semantics, compose with `odoo-delivery-ops`.

Replace the placeholders above with your local repo paths. All anchors below are relative to those roots. See `../../odoo-paths.md` for shared setup.

## Scope
Provide a shared local harness for multi-project Odoo test execution where each project keeps its own `ODOO_TEST_BASE_CMD` and the harness owns appended runtime flags plus shared cleanup behavior.

## Primary artifact
A local execution-oriented answer that identifies the configured base command source, the runtime flags the harness will append, the cleanup action that applies, and the boundary decision with sibling skills.

## Key checks
- Read `ODOO_TEST_BASE_CMD` from `.claude/settings.local.json` before planning execution.
- Confirm the base command already includes `-c` or `--config`.
- Confirm `ODOO_TEST_BASE_CMD` does not already include runtime-managed flags such as `-d`, `--test-tags`, `--test-enable`, `-i`, `-u`, or `--stop-after-init`.
- Preserve the configured config path from the base command.
- Use `--cleanup-before` only when a disposable local database must be cleared before the run.
- Use shared automatic post-run cleanup only for disposable local database flows.
- Expect shared cleanup to terminate leftover sessions on the target disposable database before `dropdb`, so filestore removal is not blocked by idle connections.
- In dry-run mode, print resolved and final commands but skip cleanup execution and subprocess execution.

## Key docs anchors
- `content/developer/reference/backend/testing.rst`
- `content/developer/reference/cli.rst`
- `content/developer/reference/backend/performance.rst`

## Key source anchors
- `odoo/tools/config.py`
- `odoo/modules/loading.py`
- `odoo/tests/common.py`

## Frequent sibling skills
- `odoo-test`
- `odoo-delivery-ops`
- `odoo-testing-reference`
