# v19 Notes — View UI

## View tag rename (primary change)
- `<tree>` → `<list>` exclusively in v19
- All list view XML must use `<list>` tag; `<tree>` is deprecated and will be removed
- Affects: view definitions, view inheritance, `ir.ui.view` records, domain references to list context

## Frontend doc structure
- `content/developer/reference/frontend.rst` is a thin toctree stub in v19
- Real frontend content: `content/developer/reference/frontend/` (subdirectory)

## ORM package (relevant to computed fields in views)
- `odoo/orm/fields.py` and `odoo/orm/decorators.py` are the v19 sources for field and compute decorators
- No change to view architecture or QWeb engine paths
