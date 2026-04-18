# Checklist

## Intake
- [ ] Confirm the requested artifact belongs to `odoo-plan`.
- [ ] Identify main module, bridge module, or business or technical entrypoint.
- [ ] Identify adjacent skills needed for composition.
- [ ] Identify nearest-neighbor skill and why it does not own the request.

## Analysis
- [ ] Define the smallest safe change surface.
- [ ] Map each requirement to modules, files, and data or security implications.
- [ ] List validation by install, update, workflow, and regression.
- [ ] Call out migration, rollout, or approval decisions still open.

## Production readiness
- [ ] Name permissions or access impact when relevant.
- [ ] Name migration or data-shape impact when relevant.
- [ ] Name cross-app modules and bridge addons touched.
- [ ] Name rollback or staging concerns when release or data risk exists.

## Output
- [ ] Return ordered implementation steps
- [ ] Return target files and modules
- [ ] Return acceptance criteria and open decisions
- [ ] Return test matrix and rollout notes
- [ ] Return boundary decision
- [ ] Name assumptions, blockers, or missing context.
- [ ] Redirect clearly if the request crosses this skill boundary.
