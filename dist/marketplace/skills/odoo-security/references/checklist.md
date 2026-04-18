# Checklist

## Intake
- [ ] Confirm the requested artifact belongs to `odoo-security`.
- [ ] Identify main module, bridge module, or business or technical entrypoint.
- [ ] Identify adjacent skills needed for composition.
- [ ] Identify nearest-neighbor skill and why it does not own the request.

## Analysis
- [ ] Model trust boundaries explicitly: public methods treat arguments as untrusted.
- [ ] Check ACL first, then record-rule composition.
- [ ] Look for sudo spread, raw SQL, unsafe HTML rendering, and eval misuse.
- [ ] Note config-secret or public-route exposure risks.

## Production readiness
- [ ] Anchor the answer to current Odoo docs and current source paths.
- [ ] Separate this skill from the nearest neighbor skill explicitly.
- [ ] Name cross-app, security, or accounting effects when relevant.
- [ ] Redirect to task skills if the user needs workflow execution.

## Output
- [ ] Return security findings
- [ ] Return access-control recommendations
- [ ] Return trust-boundary notes
- [ ] Return required tests or follow-ups
- [ ] Return boundary decision
- [ ] Name assumptions, blockers, or missing context.
- [ ] Redirect clearly if the request crosses this skill boundary.
