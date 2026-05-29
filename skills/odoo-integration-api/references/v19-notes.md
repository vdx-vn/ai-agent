# v19 Notes — Integration API

## Namespace package
- `odoo/__init__.py` removed; external integrations that introspect `odoo` package structure must account for namespace package
- `odoo/http.py` remains at the same path (not moved into `odoo/orm/`)

## ORM package (relevant to server-side integration code)
- `odoo/orm/models.py` is the v19 home for model base classes
- Registry: `odoo/orm/registry.py` (moved from `odoo/modules/registry.py`)

## View tag rename
- `<tree>` → `<list>`; any integration that parses or constructs view XML should use `<list>`

## Doc structure
- `content/developer/reference/external_rpc_api.rst` and `content/developer/reference/external_api.rst`
  are the live integration doc anchors; `content/developer/reference/backend/api.rst` is a stub in v19
