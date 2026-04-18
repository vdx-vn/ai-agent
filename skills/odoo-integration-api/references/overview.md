# Overview

Paths below are relative to:
- Docs repo: `<ODOO_DOCS_ROOT>`
- Source repo: `<ODOO_SOURCE_ROOT>`

## Primary routing rule
Use this skill only when the primary requested output is an external integration design or RPC/API decision.

Replace the placeholders above with your local repo paths. All anchors below are relative to those roots. See `../../odoo-paths.md` for shared setup.

## Scope
Guide Odoo external integration patterns, auth choices, RPC or HTTP approaches, and transaction boundaries for business operations.

## Primary artifact
Integration design guidance with auth model, data flow, safety considerations, and operational constraints.

## Key checks
- Use dedicated integration identities where possible.
- Keep business operations idempotent and transaction boundaries clear.
- Distinguish legacy RPC from newer HTTP patterns.
- Review auth, retry, and data-trust concerns.

## Key docs anchors
- `content/developer/reference/external_rpc_api.rst`
- `content/developer/reference/external_api.rst`
- `content/developer/reference/cli.rst`

## Key source anchors
- `odoo/http.py`
- `odoo/addons/base/models/ir_http.py`
- `addons/website_crm/controllers/website_form.py`

## Frequent sibling skills
- `odoo-security`
- `odoo-delivery-ops`
- `odoo-build`
