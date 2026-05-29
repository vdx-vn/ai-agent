# v19 Notes — Testing Reference

## ORM package relocation
- `odoo/orm/models.py` replaces `odoo/models.py`; test imports like `from odoo.tests.common import TransactionCase` unchanged
- `odoo/orm/fields.py` replaces `odoo/fields.py`

## Namespace package
- `odoo/__init__.py` removed; test files that do `import odoo; odoo.models` must update to explicit import

## View tag rename
- `<tree>` → `<list>`; UI tests and tour scripts that target list views must use `<list>` tag

## hr.expense.sheet model removed
- `hr.expense.sheet` model removed in v19; expenses are flat on `hr.expense` with `former_sheet_id` breadcrumb
- Tests that create or assert `hr.expense.sheet` records must be updated
