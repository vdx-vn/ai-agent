# v19 Notes — Architecture

## ORM package relocation
- `odoo/orm/` is a new subpackage in v19; models, fields, decorators, registry moved here
- Old paths `odoo/models.py`, `odoo/fields.py`, `odoo/api.py`, `odoo/modules/registry.py` are removed
- New canonical paths: `odoo/orm/models.py`, `odoo/orm/fields.py`, `odoo/orm/decorators.py`, `odoo/orm/registry.py`

## Namespace package
- `odoo/__init__.py` removed; `odoo` is now a PEP 420 namespace package
- Addons must use explicit imports; implicit `odoo.*` star imports break

## Module boundary implication
- Inter-addon imports that relied on `odoo.models` or `odoo.fields` at module load now require
  explicit `from odoo.orm.models import ...` or the shim path `from odoo import models`
- Bridge modules using `from odoo.modules.registry import Registry` must update to `from odoo.orm.registry import Registry`

## View tag rename
- `<tree>` → `<list>` in XML view definitions
