# Overview

Paths below are relative to:
- Docs repo: `<ODOO_DOCS_ROOT>`
- Source repo: `<ODOO_SOURCE_ROOT>`

## Primary routing rule
Use this skill only when the primary requested output is performance diagnosis or optimization guidance.

Replace the placeholders above with your local repo paths. All anchors below are relative to those roots. See `../../odoo-paths.md` for shared setup.

## Scope
Guide performance analysis and optimization for Odoo code, especially ORM-heavy, query-heavy, and batch-heavy paths.

## Primary artifact
Performance guidance with hotspot hypotheses, optimization levers, and validation ideas.

## Key checks
- Look for searches or writes inside loops.
- Prefer batch reads and grouped computations.
- Consider indexes, prefetch, and query-count assertions.
- Separate algorithmic complexity from database-chatter issues.

## Key docs anchors
- `content/developer/reference/backend/performance.rst`
- `content/developer/reference/backend/orm.rst`
- `content/developer/reference/backend/testing.rst`

## Key source anchors
- `odoo/models.py`
- `odoo/fields.py`
- `odoo/tests/common.py`
- `addons/stock_account/models/stock_move.py`

## Frequent sibling skills
- `odoo-test`
- `odoo-orm-modeling`
- `odoo-review`
