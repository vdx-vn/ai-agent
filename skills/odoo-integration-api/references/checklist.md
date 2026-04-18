# Checklist

## Intake
- [ ] Confirm the requested artifact belongs to `odoo-integration-api`.
- [ ] Identify main module, bridge module, or business or technical entrypoint.
- [ ] Identify adjacent skills needed for composition.
- [ ] Identify nearest-neighbor skill and why it does not own the request.

## Analysis
- [ ] Use dedicated integration identities where possible.
- [ ] Keep business operations idempotent and transaction boundaries clear.
- [ ] Distinguish legacy RPC from newer HTTP patterns.
- [ ] Review auth, retry, and data-trust concerns.

## Production readiness
- [ ] Anchor the answer to current Odoo docs and current source paths.
- [ ] Separate this skill from the nearest neighbor skill explicitly.
- [ ] Name cross-app, security, or accounting effects when relevant.
- [ ] Redirect to task skills if the user needs workflow execution.

## Output
- [ ] Return integration pattern recommendation
- [ ] Return auth and user model
- [ ] Return transaction-boundary notes
- [ ] Return failure and retry considerations
- [ ] Return boundary decision
- [ ] Name assumptions, blockers, or missing context.
- [ ] Redirect clearly if the request crosses this skill boundary.
