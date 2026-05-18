# Checklist

## Intake
- [ ] Confirm the requested artifact belongs to `odoo-upgrade-migration`.
- [ ] Identify main module, bridge module, or business or technical entrypoint.
- [ ] Identify adjacent skills needed for composition.
- [ ] Identify nearest-neighbor skill and why it does not own the request.

## Analysis
- [ ] Name data preservation strategy explicitly.
- [ ] Check noupdate records and XML IDs affected by the change.
- [ ] Plan upgrade scripts by phase when needed.
- [ ] Require rehearsal and validation for data-shape changes.

## Production readiness
- [ ] Anchor the answer to Odoo <ODOO_MAJOR_VERSION> docs and current source paths.
- [ ] Separate this skill from the nearest neighbor skill explicitly.
- [ ] Name cross-app, security, or accounting effects when relevant.
- [ ] Redirect to task skills if the user needs workflow execution.

## Output
- [ ] Return migration approach
- [ ] Return script or data-move notes
- [ ] Return validation checklist
- [ ] Return rollout cautions
- [ ] Return boundary decision
- [ ] Name assumptions, blockers, or missing context.
- [ ] Redirect clearly if the request crosses this skill boundary.
