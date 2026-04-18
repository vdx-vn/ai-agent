# Examples

## Positive triggers
1. "Reflect on this Odoo rollout."
   - Expected: use `odoo-reflect` as primary skill.
2. "What gaps remain after this customization shipped?"
   - Expected: use `odoo-reflect` as primary skill.
3. "Summarize lessons from this failed migration."
   - Expected: use `odoo-reflect` as primary skill.

## Negative triggers
1. "Plan how to build this feature."
   - Expected: do not use `odoo-reflect` as primary skill.
2. "Run validation commands now."
   - Expected: do not use `odoo-reflect` as primary skill.

## Tie-breaker
- Prompt: "What did we learn after this failed migration and what should we fix next?"
- Why this skill wins: The user wants a retrospective and follow-up actions, not another review or test run. `odoo-reflect` should win.

## Nearby skills to consider
- `odoo-review`
- `odoo-test`
