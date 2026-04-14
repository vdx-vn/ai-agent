# Checklist

## Intake
- [ ] Confirm the requested artifact belongs to `odoo-test`.
- [ ] Identify main module, bridge module, or business or technical entrypoint.
- [ ] Identify adjacent skills needed for composition.

## Analysis
- [ ] Choose test type by change surface: unit, transaction, HTTP, JS, tour, performance.
- [ ] Cover install and update paths when relevant.
- [ ] Include security and multi-company checks when behavior changes.
- [ ] Report gaps, not only pass/fail.

## Production readiness
- [ ] Name permissions or access impact when relevant.
- [ ] Name migration or data-shape impact when relevant.
- [ ] Name cross-app modules and bridge addons touched.
- [ ] Name rollback or staging concerns when release or data risk exists.

## Output
- [ ] Return test matrix
- [ ] Return commands or suites run
- [ ] Return observed failures
- [ ] Return remaining validation gaps
- [ ] Name assumptions, blockers, or missing context.
- [ ] Redirect clearly if the request crosses this skill boundary.
