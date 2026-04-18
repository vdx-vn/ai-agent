# Examples

## Positive triggers
1. "This stock compute field causes N+1 queries."
   - Expected: use `odoo-performance` as primary skill.
2. "How should I profile this slow reconciliation action?"
   - Expected: use `odoo-performance` as primary skill.
3. "What indexing or batching issues do you see here?"
   - Expected: use `odoo-performance` as primary skill.

## Negative triggers
1. "Which addon should own this code?"
   - Expected: do not use `odoo-performance` as primary skill.
2. "What record rule should the manager have?"
   - Expected: do not use `odoo-performance` as primary skill.

## Tie-breaker
- Prompt: "Why is this batch posting action slow and how should we measure it?"
- Why this skill wins: The question is about hotspot diagnosis and measurement, so `odoo-performance` should win.

## Nearby skills to consider
- `odoo-test`
- `odoo-orm-modeling`
- `odoo-review`
