# v19 Notes — Think (Scoping)

## High-impact v19 changes to flag during scoping

### ORM package relocation
- Any task touching model or field code: `odoo/models.py`, `odoo/fields.py`, `odoo/api.py` all moved to `odoo/orm/`
- Scope impact: addons with direct file-path references, migration scripts, or profiling tools may break

### Namespace package
- `odoo/__init__.py` removed; implicit `odoo` package star-imports no longer valid
- Scope risk: any addon or script assuming `odoo` has an `__init__.py`

### hr.expense.sheet removed
- `hr.expense.sheet` model gone in v19; expenses flat on `hr.expense` with `former_sheet_id`
- Scope risk: any task involving expense flows, reports, or ACLs referencing the old model

### View tag rename
- `<tree>` → `<list>`; scope risk for any UI or XML-patching task
