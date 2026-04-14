# Checklist

## Intake
- [ ] Confirm the requested artifact belongs to `odoo-orm-modeling`.
- [ ] Identify main module, bridge module, or business or technical entrypoint.
- [ ] Identify adjacent skills needed for composition.

## Analysis
- [ ] Prefer batch-safe recordset operations.
- [ ] Choose stored computes only when query or reporting needs justify it.
- [ ] Keep onchange UX-only and constrains business-validity oriented.
- [ ] Check multi-company and access implications of field design.

## Production readiness
- [ ] Anchor the answer to Odoo <ODOO_MAJOR_VERSION> docs and current source paths.
- [ ] Separate this skill from the nearest neighbor skill explicitly.
- [ ] Name cross-app, security, or accounting effects when relevant.
- [ ] Redirect to task skills if the user needs workflow execution.

## Output
- [ ] Return field or method pattern recommendation
- [ ] Return ORM anti-pattern warnings
- [ ] Return recordset or decorator guidance
- [ ] Return follow-up test notes
- [ ] Name assumptions, blockers, or missing context.
- [ ] Redirect clearly if the request crosses this skill boundary.
