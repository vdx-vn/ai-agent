# Checklist

## Intake
- [ ] Confirm the requested artifact belongs to `odoo-performance`.
- [ ] Identify main module, bridge module, or business or technical entrypoint.
- [ ] Identify adjacent skills needed for composition.
- [ ] Identify nearest-neighbor skill and why it does not own the request.

## Analysis
- [ ] Look for searches or writes inside loops.
- [ ] Prefer batch reads and grouped computations.
- [ ] Consider indexes, prefetch, and query-count assertions.
- [ ] Separate algorithmic complexity from database-chatter issues.

## Production readiness
- [ ] Anchor the answer to current Odoo docs and current source paths.
- [ ] Separate this skill from the nearest neighbor skill explicitly.
- [ ] Name cross-app, security, or accounting effects when relevant.
- [ ] Redirect to task skills if the user needs workflow execution.

## Output
- [ ] Return likely hotspots
- [ ] Return optimization recommendations
- [ ] Return measurement or profiler plan
- [ ] Return performance-test notes
- [ ] Return boundary decision
- [ ] Name assumptions, blockers, or missing context.
- [ ] Redirect clearly if the request crosses this skill boundary.
