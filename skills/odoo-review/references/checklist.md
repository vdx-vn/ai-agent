# Checklist

## Intake
- [ ] Confirm the requested artifact belongs to `odoo-review`.
- [ ] Identify main module, bridge module, or business or technical entrypoint.
- [ ] Identify adjacent skills needed for composition.
- [ ] Identify nearest-neighbor skill and why it does not own the request.

## Analysis
- [ ] Inspect module fit and dependency choices.
- [ ] Check security, migration, and performance concerns at review depth.
- [ ] Look for cross-app breakage via bridge modules.
- [ ] Separate required fixes from optional improvements.

## Production readiness
- [ ] Name permissions or access impact when relevant.
- [ ] Name migration or data-shape impact when relevant.
- [ ] Name cross-app modules and bridge addons touched.
- [ ] Name rollback or staging concerns when release or data risk exists.

## Output
- [ ] Return evidence status: reasoned review only
- [ ] Return findings by severity
- [ ] Return required fixes
- [ ] Return suggested improvements
- [ ] Return untested risk areas
- [ ] Return boundary decision
- [ ] Name assumptions, blockers, or missing context.
- [ ] Redirect clearly if the request crosses this skill boundary.
