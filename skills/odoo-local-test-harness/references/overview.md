# Overview

Paths below are relative to:
- Docs tree: `current Odoo docs tree`
- Source tree: `current Odoo CE source tree`

## Project-local path resolution
Before using docs or source anchors, search upward from the current working directory for `.odoo-skills/project.json`. If it exists, read `docsRoot` as the Odoo docs tree and `sourceRoot` as the Odoo CE source tree. Prefer `.odoo-skills/project.json` over Docker Compose files, module READMEs, or ad hoc filesystem searches. If the config is absent, use the materialized placeholders above or ask for explicit roots.

## Primary routing rule
Use this skill when the task depends on a project-local Odoo test command or shared local cleanup behavior. If the primary output is current-change validation evidence, compose with `odoo-test`. If the primary output is only CLI semantics, compose with `odoo-delivery-ops`.

Resolve the roots above from project setup first; then treat docs anchors as relative to the current Odoo docs tree and source anchors as relative to the current Odoo CE source tree. See `../../odoo-paths.md` for shared setup.

## Scope
Provide a shared local harness for multi-project Odoo test execution where each project keeps its own `odooTestBaseCmd` / `ODOO_TEST_BASE_CMD` and the harness owns appended runtime flags plus shared cleanup behavior.

## Primary artifact
A local execution-oriented answer that identifies the configured base command source, the runtime flags the harness will append, the cleanup action that applies, and the boundary decision with sibling skills.

## Key checks
- Read the base command from `ODOO_TEST_BASE_CMD` when present, otherwise from `.odoo-skills/project.json`.
- Prefer the configured base command over Docker Compose files, PostgreSQL image discovery, module READMEs, or inferred `odoo-bin` commands.
- Confirm the base command already includes `-c` or `--config`.
- Confirm the base command does not already include runtime-managed flags such as `-d`, `--test-tags`, `--test-enable`, `-i`, `-u`, or `--stop-after-init`.
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
