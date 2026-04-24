# Examples

## Positive triggers
1. "Test this stock customization against the current project database."
   - Expected: use `odoo-test` as primary skill and compose with `odoo-local-test-harness` if local execution is needed.
2. "What commands should I run to validate this module now?"
   - Expected: use `odoo-test` as primary skill.
3. "Check install and update regressions for this addon on a disposable database."
   - Expected: use `odoo-test` as primary skill.

## Negative triggers
1. "Explain Odoo test tags and HttpCase."
   - Expected: do not use `odoo-test` as primary skill.
2. "Review this diff for maintainability and risk before merge."
   - Expected: do not use `odoo-test` as primary skill.

## Tie-breaker
- Prompt: "Validate this checkout change now: reuse current project database for unit checks, but use a disposable database for install or update checks."
- Why this skill wins: The user wants current-change validation evidence, not framework education or review findings. `odoo-test` should win over `odoo-testing-reference` and `odoo-review` while composing with `odoo-local-test-harness` for local execution details.

## Nearby skills to consider
- `odoo-review`
- `odoo-testing-reference`
- `odoo-performance`
- `odoo-local-test-harness`
