# Checklist

## Intake
- [ ] Confirm the requested artifact belongs to `odoo-test`.
- [ ] Identify main module, bridge module, or business or technical entrypoint.
- [ ] Identify adjacent skills needed for composition.
- [ ] Identify nearest-neighbor skill and why it does not own the request.
- [ ] Compose with `odoo-local-test-harness` when local execution depends on `ODOO_TEST_BASE_CMD` or shared cleanup.

## Analysis
- [ ] Choose test type by change surface: unit, transaction, HTTP, JS, tour, performance.
- [ ] Cover install and update paths when relevant.
- [ ] Include security and multi-company checks when behavior changes.
- [ ] Report gaps, not only pass or fail.

## Production readiness
- [ ] Name permissions or access impact when relevant.
- [ ] Name migration or data-shape impact when relevant.
- [ ] Name cross-app modules and bridge addons touched.
- [ ] Name rollback or staging concerns when release or data risk exists.

## Output
- [ ] Return evidence status: executed, planned, or blocked
- [ ] Return test matrix
- [ ] Return commands or suites run
- [ ] Return observed failures or outcomes
- [ ] Return remaining validation gaps
- [ ] Return boundary decision
- [ ] Name assumptions, blockers, or missing context.
- [ ] Redirect clearly if the request crosses this skill boundary.
