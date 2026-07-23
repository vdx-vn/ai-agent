# Checklist

## Intake
- [ ] Confirm the requested artifact belongs to `odoo-test`.
- [ ] Identify main module, bridge module, or business or technical entrypoint.
- [ ] Identify adjacent skills needed for composition.
- [ ] Identify nearest-neighbor skill and why it does not own the request.
- [ ] Confirm `odoo` (odoo-cli) is installed in the project's Python environment before running tests.

## Analysis
- [ ] Choose test type by change surface: unit, transaction, HTTP, JS, tour, performance.
- [ ] Run `odoo runtime-test --module <name...>` for the module(s) under change; add `--tests` for specific files and `--db` for the target database.
- [ ] Use `--init update` (or `--init install`) on `odoo runtime-test` to cover install and update paths when relevant.
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
- [ ] Return exact `odoo runtime-test` invocation(s) run
- [ ] Return the `output_file` path from the run's condensed JSON summary
- [ ] Return observed failures or outcomes
- [ ] Return remaining validation gaps
- [ ] Return boundary decision
- [ ] Name assumptions, blockers, or missing context.
- [ ] Redirect clearly if the request crosses this skill boundary.
