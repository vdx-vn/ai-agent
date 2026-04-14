# Examples

## Positive triggers
1. "What downstream effect if MO consumes components late?"
   - Expected: use `odoo-business-manufacturing` as primary skill.
2. "How does BoM and work-center setup affect stock and accounting?"
   - Expected: use `odoo-business-manufacturing` as primary skill.
3. "Explain subassembly and subcontracting impact."
   - Expected: use `odoo-business-manufacturing` as primary skill.

## Negative triggers
1. "How do replenishment routes create transfers?"
   - Expected: do not use `odoo-business-manufacturing` as primary skill.
2. "What worker count should I use?"
   - Expected: do not use `odoo-business-manufacturing` as primary skill.

## Tie-breaker
- Prompt: "How does a BoM shortage affect component reservation and MO progress?"
- Why this skill wins: The entrypoint is MO and BoM behavior, so `odoo-business-manufacturing` should win over `odoo-business-inventory`.

## Nearby skills to consider
- `odoo-business-inventory`
- `odoo-business-purchase`
- `odoo-business-sales`
- `odoo-business-accounting`
