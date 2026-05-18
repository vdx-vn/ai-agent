# Overview

Paths below are relative to:
- Docs repo: `<ODOO_DOCS_ROOT>`
- Source repo: `<ODOO_SOURCE_ROOT>`

## Primary routing rule
Use this skill only when the primary requested output is a trust-boundary or exposure assessment. If the user wants a broad code review, use `odoo-review` and compose with this skill only when security is central.

Replace the placeholders above with your local repo paths. All anchors below are relative to those roots. See `../../odoo-paths.md` for shared setup.

## Scope
Guide Odoo security model including groups, ACL, record rules, controller auth, public methods, CSRF, sudo, SQL, XSS, and eval risks.

## Primary artifact
Security assessment with trust boundaries, permission checks, exposure risks, and required safeguards.

## Key checks
- Model trust boundaries explicitly: public methods treat arguments as untrusted.
- Check ACL first, then record-rule composition.
- Look for sudo spread, raw SQL, unsafe HTML rendering, and eval misuse.
- Note config-secret or public-route exposure risks.

## Key docs anchors
- `content/developer/reference/backend/security.rst`
- `content/developer/tutorials/restrict_data_access.rst`
- `content/contributing/development/coding_guidelines.rst`

## Key source anchors
- `odoo/addons/base/models/ir_rule.py`
- `odoo/addons/base/models/ir_model.py`
- `odoo/addons/base/models/ir_http.py`
- `odoo/http.py`
- `odoo/addons/base/models/ir_config_parameter.py`

## Frequent sibling skills
- `odoo-review`
- `odoo-build`
