# v19 Notes — Performance

## ORM package relocation
- Query-plan and prefetch logic: `odoo/orm/models.py` (was `odoo/models.py`)
- Field lazy-loading and `_prefetch_ids`: now in `odoo/orm/fields.py`
- Registry cache: `odoo/orm/registry.py` (was `odoo/modules/registry.py`)

## Namespace package
- `odoo/__init__.py` removed; performance-profiling scripts that import from `odoo` package root must update

## View tag rename
- `<tree>` → `<list>`; list view performance analysis should reference `<list>` in v19 source
