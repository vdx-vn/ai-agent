# v19 Notes — Security

## ORM package relocation
- ACL and record-rule evaluation logic now lives in `odoo/orm/models.py` (moved from `odoo/models.py`)
- `odoo/orm/decorators.py` holds `@api.constrains`, `@api.depends`, `@api.onchange` definitions
- Security checks (`_check_access`, `check_access_rights`) remain on model class — same API, different source path

## Namespace package
- `odoo/__init__.py` removed; addons importing `odoo.models` directly must use `from odoo import models` shim
  or `from odoo.orm.models import BaseModel`

## View tag rename
- `<tree>` → `<list>`; security-filtered list views should use `<list>` in v19
