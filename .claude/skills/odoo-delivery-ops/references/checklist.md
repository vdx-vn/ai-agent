# Checklist

## Intake
- [ ] Confirm the requested artifact belongs to `odoo-delivery-ops`.
- [ ] Identify main module, bridge module, or business or technical entrypoint.
- [ ] Identify adjacent skills needed for composition.

## Analysis
- [ ] Separate CLI semantics from migration strategy.
- [ ] Call out dangerous module reinit or update behavior.
- [ ] Mention worker and cron implications where relevant.
- [ ] Keep environment-specific cautions explicit.

## Production readiness
- [ ] Anchor the answer to Odoo <ODOO_MAJOR_VERSION> docs and current source paths.
- [ ] Separate this skill from the nearest neighbor skill explicitly.
- [ ] Name cross-app, security, or accounting effects when relevant.
- [ ] Redirect to task skills if the user needs workflow execution.

## Output
- [ ] Return command or flag guidance
- [ ] Return runtime cautions
- [ ] Return environment notes
- [ ] Return follow-up release checks
- [ ] Name assumptions, blockers, or missing context.
- [ ] Redirect clearly if the request crosses this skill boundary.
