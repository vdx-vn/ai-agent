# v19 Notes — ORM Modeling

## ORM package relocation
- Rename: `odoo/models.py` → `odoo/orm/models.py`
- Rename: `odoo/fields.py` → `odoo/orm/fields.py` + split files:
  - `odoo/orm/fields_relational.py`
  - `odoo/orm/fields_numeric.py`
  - `odoo/orm/fields_temporal.py`
  - `odoo/orm/fields_selection.py`
- Rename: `odoo/api.py` → `odoo/api/__init__.py` (re-export shim); real decorator defs in `odoo/orm/decorators.py`
- Rename: `odoo/modules/registry.py` → `odoo/orm/registry.py`

## Namespace package
- `odoo/__init__.py` removed (PEP 420 namespace package)
- Explicit imports required; star imports from `odoo` no longer work

## Import aliases (still valid in v19)
- `from odoo import models, fields, api` still resolves via namespace shims
- Direct imports (`from odoo.orm.models import BaseModel`) are now the canonical form

## View tag rename
- `<tree>` → `<list>` (v19 uses `<list>` exclusively; `<tree>` still parsed but deprecated)
