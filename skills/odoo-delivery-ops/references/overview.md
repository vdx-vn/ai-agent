# Overview

Paths below are relative to:
- Docs repo: `<ODOO_DOCS_ROOT>`
- Source repo: `<ODOO_SOURCE_ROOT>`

## Primary routing rule
Use this skill only when the primary requested output is command, flag, worker, or environment semantics. If the user asks whether a release is ready, use `odoo-ship`.

Replace the placeholders above with your local repo paths. All anchors below are relative to those roots. See `../../odoo-paths.md` for shared setup.

## Scope
Guide Odoo CLI, runtime, and environment behavior, especially install or update semantics, workers, and Odoo.sh stage mechanics.

## Primary artifact
Operational mechanics guidance covering commands, flags, environment behavior, and runtime cautions.

## Key checks
- Separate CLI semantics from migration strategy.
- Call out dangerous module reinit or update behavior.
- Mention worker and cron implications where relevant.
- Keep environment-specific cautions explicit.
- Compose with `odoo-local-test-harness` when local runtime guidance depends on a project-specific `ODOO_TEST_BASE_CMD`.

## Key docs anchors
- `content/developer/reference/cli.rst`
- `content/administration/odoo_sh/getting_started/branches.rst`
- `content/administration/upgrade.rst`

## Key source anchors
- `odoo/tools/config.py`
- `odoo/modules/loading.py`
- `odoo/http.py`

## Frequent sibling skills
- `odoo-ship`
- `odoo-test`
- `odoo-upgrade-migration`
