# v19 Notes — Upgrade Migration

## ORM package relocation (breaking for migration scripts)
- `odoo/models.py` removed → `odoo/orm/models.py`
- `odoo/fields.py` removed → `odoo/orm/fields.py` (+ split: fields_relational, fields_numeric, fields_temporal, fields_selection)
- `odoo/api.py` removed → `odoo/api/__init__.py` shim; decorators in `odoo/orm/decorators.py`
- `odoo/modules/registry.py` removed → `odoo/orm/registry.py`
- Migration scripts using `from odoo.models import BaseModel` or similar must update

## Namespace package
- `odoo/__init__.py` removed in v19; PEP 420 namespace package
- Pre-v19 migration code doing `import odoo; odoo.fields` breaks

## hr.expense.sheet removed (v19 data migration)
- Model `hr.expense.sheet` removed; all expense data flattened to `hr.expense`
- `former_sheet_id` breadcrumb field left on `hr.expense` for traceability
- Migration scripts referencing `hr.expense.sheet` must target `hr.expense` instead

## View tag rename
- `<tree>` → `<list>`; migration scripts that generate or patch XML views must use `<list>`
