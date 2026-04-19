---
name: odoo-local-test-harness
description: "Use when working across multiple local Odoo projects with different versions, where each project has its own base `odoo-bin` command but test execution should follow one shared harness for appending db, test tags, install or update flags, stop-after-init, and shared database or filestore cleanup."
---

# Odoo Local Test Harness

# Purpose
Run local Odoo tests across different projects and Odoo versions using one shared harness.
Project-specific setup lives in `.claude/settings.local.json` as `ODOO_TEST_BASE_CMD`.

# Primary routing rule
Use this skill when the task depends on a project-local Odoo test command or shared local cleanup behavior.
If the primary output is current-change validation evidence, compose with `odoo-test`.
If the primary output is only CLI semantics, compose with `odoo-delivery-ops`.

# Use this skill when
- a local Odoo project has its own base command and config path
- the user provides or updates a project-local `ODOO_TEST_BASE_CMD`
- tests need database names, test tags, install or update flags, or `--stop-after-init` appended safely
- local test setup must clean disposable databases or matching filestore state automatically after runs, with optional pre-run cleanup

# Do not use this skill when
- the task is only about Odoo testing primitives or framework selection
- the task is only about release readiness
- the task is only about functional business-process explanation

# Required inputs
- current repository root and local Odoo project context
- `.claude/settings.local.json` or the resolved `ODOO_TEST_BASE_CMD` value
- requested database name, test tags, install or update targets, and whether pre-run cleanup or dry-run is needed

## Config contract
Store per-project base command in `.claude/settings.local.json`:

```json
{
  "env": {
    "ODOO_TEST_BASE_CMD": "/path/to/python /path/to/odoo-bin -c /path/to/odoo.conf"
  }
}
```

Treat `ODOO_TEST_BASE_CMD` as immutable base command.
Parse it safely, then append normalized arguments. If it is missing, stop and ask the user to provide it.
The configured base command must already include `-c` or `--config`.
Do not pre-configure runtime-managed flags in `ODOO_TEST_BASE_CMD`; the harness owns `-d`, `--test-tags`, `--test-enable`, `-i`, `-u`, and `--stop-after-init`.

# Workflow
1. Read `ODOO_TEST_BASE_CMD` from local settings.
2. Read `references/overview.md` for routing, boundaries, and local execution anchors.
3. Parse it into argv through `scripts/run_odoo_test.py`, not shell concatenation.
4. Normalize `-d`, `--test-tags`, `--test-enable`, `-i`, `-u`, and `--stop-after-init`.
5. Run optional pre-run cleanup plus automatic post-run cleanup through `scripts/delete_unused_odoo_db.py` when the flow uses a disposable local database.
6. Return the resolved base command source, appended arguments, cleanup action, and boundary decision.

# Output contract
Return a concise result that includes:
- resolved base command source
- appended runtime arguments
- cleanup action performed or skipped
- boundary decision with primary and sibling skills

Dry-run semantics:
- still resolve and print the base command and final command
- skip cleanup execution and subprocess execution
- do not require the configured `-c` or `--config` path to exist in dry-run mode

## Compose with sibling skills
- `odoo-test`
- `odoo-delivery-ops`
- `odoo-testing-reference`

## References
- `references/overview.md`
- `references/checklist.md`
- `references/examples.md`
