# Checklist

## Intake
- [ ] Confirm the requested artifact belongs to `odoo-test`.
- [ ] Identify main module, bridge module, or business or technical entrypoint.
- [ ] Identify adjacent skills needed for composition.
- [ ] Identify nearest-neighbor skill and why it does not own the request.
- [ ] Choose validation DB mode by change surface.
- [ ] Compose with `odoo-local-test-harness` when local execution depends on `ODOO_TEST_BASE_CMD`, config inspection, existing-db resolution, or disposable cleanup.

## Analysis
- [ ] Choose test type by change surface: unit, transaction, HTTP, JS, tour, performance.
- [ ] Use existing DB mode for unit-style validation on current project state unless the user explicitly wants disposable setup.
- [ ] Use disposable DB mode for install or update validation unless the user explicitly overrides.
- [ ] Cover install and update paths when relevant.
- [ ] Include security and multi-company checks when behavior changes.
- [ ] Report gaps, not only pass or fail.

## Production readiness
- [ ] Name permissions or access impact when relevant.
- [ ] Name migration or data-shape impact when relevant.
- [ ] Name cross-app modules and bridge addons touched.
- [ ] Name rollback or staging concerns when release or data risk exists.
- [ ] Name cleanup expectations explicitly for the chosen DB mode.

## Output
- [ ] Return evidence status: executed, planned, or blocked
- [ ] Return test matrix
- [ ] Return commands or suites run
- [ ] Return observed failures or outcomes
- [ ] Return remaining validation gaps
- [ ] Return boundary decision
- [ ] Name assumptions, blockers, or missing context.
- [ ] Redirect clearly if the request crosses this skill boundary.
