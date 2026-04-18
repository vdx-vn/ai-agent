# Publish Checklist for `odoo-skills`

## Before tagging
- Run `python3 -m pip install -e .`
- Run `odoo-skills-verify`
- Run `odoo-skills-build`
- Run `odoo-skills-smoke-install`
- Run `claude --plugin-dir .`
- Run `claude plugin validate dist/marketplace`

## Marketplace metadata
- Confirm `.claude-plugin/plugin.json` version bumped
- Confirm `.claude-plugin/marketplace.json` plugin version matches
- Confirm plugin name is `odoo-skills`
- Confirm marketplace name is `odoo-skills-dev`

## Public docs
- Confirm `README.md` install instructions still work
- Confirm `LICENSE` is Apache-2.0
- Confirm `docs/reference/skill-inventory.json` matches the root `skills/` tree exactly

## Manual spot checks
- `/odoo-skills:odoo-think`
- `/odoo-skills:odoo-build`
- `/odoo-skills:odoo-test`
- `/odoo-skills:odoo-business-sales`
