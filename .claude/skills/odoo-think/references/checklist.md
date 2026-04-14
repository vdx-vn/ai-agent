# Checklist

## Intake
- [ ] Confirm the requested artifact belongs to `odoo-think`.
- [ ] Identify main module, bridge module, or business or technical entrypoint.
- [ ] Identify adjacent skills needed for composition.
- [ ] Identify nearest-neighbor skill and why it does not own the request.

## Analysis
- [ ] Classify work as bug, feature, refactor, integration, migration, or ops.
- [ ] Identify primary addon, bridge addons, and downstream modules.
- [ ] Name the business entrypoint and likely downstream documents.
- [ ] Call out unknowns that block planning.

## Production readiness
- [ ] Name permissions or access impact when relevant.
- [ ] Name migration or data-shape impact when relevant.
- [ ] Name cross-app modules and bridge addons touched.
- [ ] Name rollback or staging concerns when release or data risk exists.

## Output
- [ ] Return problem statement
- [ ] Return impacted modules and bridge addons
- [ ] Return affected business flow and entrypoint
- [ ] Return top risks and unknowns
- [ ] Return boundary decision
- [ ] Name assumptions, blockers, or missing context.
- [ ] Redirect clearly if the request crosses this skill boundary.
