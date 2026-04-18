# Checklist

## Intake
- [ ] Confirm the requested artifact belongs to `odoo-architecture`.
- [ ] Identify main module, bridge module, or business or technical entrypoint.
- [ ] Identify adjacent skills needed for composition.
- [ ] Identify nearest-neighbor skill and why it does not own the request.

## Analysis
- [ ] Check manifest dependencies and auto_install candidates.
- [ ] Prefer bridge modules when logic spans stable domains.
- [ ] Keep responsibilities cohesive and avoid dumping unrelated logic into a large addon.
- [ ] Name upgrade and test implications of placement.

## Production readiness
- [ ] Anchor the answer to Odoo <ODOO_MAJOR_VERSION> docs and current source paths.
- [ ] Separate this skill from the nearest neighbor skill explicitly.
- [ ] Name cross-app, security, or accounting effects when relevant.
- [ ] Redirect to task skills if the user needs workflow execution.

## Output
- [ ] Return recommended addon location
- [ ] Return dependency rationale
- [ ] Return bridge-module or extension guidance
- [ ] Return architecture risks
- [ ] Return boundary decision
- [ ] Name assumptions, blockers, or missing context.
- [ ] Redirect clearly if the request crosses this skill boundary.
