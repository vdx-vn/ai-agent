# Checklist

## Intake
- [ ] Confirm the requested artifact belongs to `odoo-build`.
- [ ] Identify main module, bridge module, or business or technical entrypoint.
- [ ] Identify adjacent skills needed for composition.
- [ ] Identify nearest-neighbor skill and why it does not own the request.

## Analysis
- [ ] Prefer ORM-first patterns over raw SQL.
- [ ] Update security artifacts when data visibility changes.
- [ ] Keep module boundaries and dependencies tight.
- [ ] Avoid speculative abstractions and align with Odoo conventions.

## Production readiness
- [ ] Name permissions or access impact when relevant.
- [ ] Name migration or data-shape impact when relevant.
- [ ] Name cross-app modules and bridge addons touched.
- [ ] Name rollback or staging concerns when release or data risk exists.

## Output
- [ ] Return code changes
- [ ] Return changed file list
- [ ] Return follow-up validation needs
- [ ] Return boundary decision
- [ ] Name assumptions, blockers, or missing context.
- [ ] Redirect clearly if the request crosses this skill boundary.
