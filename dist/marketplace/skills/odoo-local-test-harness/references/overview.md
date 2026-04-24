# Overview

Paths below are relative to:
- Docs tree: `current Odoo docs tree`
- Source tree: `current Odoo CE source tree`

## Primary routing rule
Use this skill when the task depends on a project-local Odoo test command or shared local cleanup behavior. If the primary output is current-change validation evidence, compose with `odoo-test`. If the primary output is only CLI semantics, compose with `odoo-delivery-ops`.

Treat docs anchors as relative to the current Odoo docs tree and source anchors as relative to the current Odoo CE source tree. See `../../odoo-paths.md` for shared setup.

## Scope
Provide a shared local harness for multi-project Odoo test execution where each project keeps its own `ODOO_TEST_BASE_CMD` and the harness owns appended runtime flags plus shared cleanup behavior.

## Primary artifact
A local execution-oriented answer that identifies the configured base command source, the runtime flags the harness will append, the cleanup action that applies, and the boundary decision with sibling skills.

## Key checks
- Read `ODOO_TEST_BASE_CMD` from `.claude/settings.local.json` before planning execution.
- Confirm the base command already includes `-c` or `--config`, then preserve and report the resolved config path.
- Confirm `ODOO_TEST_BASE_CMD` does not already include runtime-managed flags such as `-d`, `--test-tags`, `--test-enable`, `-i`, `-u`, or `--stop-after-init`.
- Select `--db-mode auto|existing|disposable`.
- In auto mode, use existing for current-project-state validation and disposable for install or update validation.
- In existing mode, prefer config `db_name`; otherwise list accessible non-system databases with the config connection settings.
- If multiple candidates exist, stop and return the candidate list so the user can choose which DB to use.
- Do not use `dbfilter` to narrow candidates.
- Use `--cleanup-before` only when a disposable local database must be cleared before the run.
- Disposable mode requires an explicit DB name.
- Use shared automatic post-run cleanup only for disposable local database flows, and skip DB/filestore cleanup in existing mode.
- Expect shared cleanup to terminate leftover sessions on the target disposable database before `dropdb`, so filestore removal is not blocked by idle connections.
- In dry-run mode, print resolved and final commands but skip cleanup execution and subprocess execution.
- Output should report selected DB mode, selected DB or candidate list, and cleanup action.

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
