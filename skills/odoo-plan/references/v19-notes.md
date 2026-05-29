# v19 Notes — Plan

## v19 changes that affect implementation planning

### ORM package relocation
- Plans touching model/field/decorator code: source now in `odoo/orm/` subpackage
- File-edit steps must reference `odoo/orm/models.py`, `odoo/orm/fields.py`, `odoo/orm/decorators.py`
- Registry: `odoo/orm/registry.py` (was `odoo/modules/registry.py`)

### Namespace package
- `odoo/__init__.py` removed; plan steps that scaffold new addons must use explicit imports

### hr.expense.sheet removed
- Plans involving expense flows must target `hr.expense` model; `hr.expense.sheet` no longer exists
- `former_sheet_id` available on `hr.expense` for data continuity

### View tag rename
- Plan steps writing list views must use `<list>` tag, not `<tree>`
