# Skill: Odoo Migrations & Upgrades

## Goal
Make changes upgrade-safe and migrate data properly.

## When needed
- Field rename/type change
- Splitting models
- Changing selection keys
- New constraints affecting old data

## Tactics
- Pre-migration scripts: update existing records to valid state
- Use `post_init_hook` for initial data adjustments
- Maintain backward compatibility when possible

## Guardrails
- Do not delete columns blindly
- Keep old values mapped
- Test upgrade on a DB snapshot

## Example Prompt
"Rename field x_code to internal_code without breaking existing data."
