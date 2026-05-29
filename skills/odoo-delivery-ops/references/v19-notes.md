# v19 Notes — Delivery Ops

## Namespace package
- `odoo/__init__.py` removed; deployment scripts that probe `odoo` package structure must handle namespace package

## ORM package relocation
- Registry moved to `odoo/orm/registry.py`; any ops script that imports `odoo.modules.registry.Registry` must update

## View tag rename
- `<tree>` → `<list>`; ops-side view generation or scaffold scripts must output `<list>` for list views
