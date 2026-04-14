# Examples

## Positive triggers
1. "Should this be a computed or stored field?"
   - Expected: use `odoo-orm-modeling` as primary skill.
2. "How should onchange vs constrains work here?"
   - Expected: use `odoo-orm-modeling` as primary skill.
3. "What is correct recordset-safe pattern for this write flow?"
   - Expected: use `odoo-orm-modeling` as primary skill.

## Negative triggers
1. "How should this menu item look?"
   - Expected: do not use `odoo-orm-modeling` as primary skill.
2. "What record rule should the accountant have?"
   - Expected: do not use `odoo-orm-modeling` as primary skill.

## Tie-breaker
- Prompt: "Should this approval flag be stored, computed, or onchange-only?"
- Why this skill wins: The primary decision is field semantics and ORM behavior, so `odoo-orm-modeling` should win.

## Nearby skills to consider
- `odoo-build`
- `odoo-performance`
- `odoo-security`
