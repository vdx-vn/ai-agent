# Checklist

## Intake
- [ ] Confirm the requested artifact belongs to `odoo-testing-reference`.
- [ ] Identify main module, bridge module, or business or technical entrypoint.
- [ ] Identify adjacent skills needed for composition.
- [ ] Identify nearest-neighbor skill and why it does not own the request.

## Analysis
- [ ] Match test type to change surface and user-visible behavior.
- [ ] Use install vs post-install semantics correctly.
- [ ] Highlight tour or HttpCase needs for browser flows.
- [ ] Mention performance assertions when query count matters.

## Production readiness
- [ ] Anchor the answer to Odoo <ODOO_MAJOR_VERSION> docs and current source paths.
- [ ] Separate this skill from the nearest neighbor skill explicitly.
- [ ] Name cross-app, security, or accounting effects when relevant.
- [ ] Redirect to task skills if the user needs workflow execution.

## Output
- [ ] Return recommended test types
- [ ] Return relevant test tags
- [ ] Return framework-specific cautions
- [ ] Return example test shape
- [ ] Return boundary decision
- [ ] Name assumptions, blockers, or missing context.
- [ ] Redirect clearly if the request crosses this skill boundary.
