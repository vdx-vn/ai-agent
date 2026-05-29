# v19 Notes — Review

## v19 facts to check during diff review

### ORM package relocation
- Flag imports from `odoo.models`, `odoo.fields`, `odoo.api` if they use old module paths
- `odoo/models.py`, `odoo/fields.py`, `odoo/api.py` removed; canonical paths now under `odoo/orm/`
- Flag: `from odoo.modules.registry import Registry` → should be `from odoo.orm.registry import Registry`

### Namespace package
- Flag: any code relying on `odoo.__init__` existing or importing via `import odoo; odoo.models`

### hr.expense.sheet removed
- Flag: any reference to `hr.expense.sheet` model, `expense_sheet_id` foreign keys, or old sheet reports

### View tag rename
- Flag: `<tree>` in new or modified XML view files; v19 standard is `<list>`
