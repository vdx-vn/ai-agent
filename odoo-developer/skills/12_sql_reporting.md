# Skill: Odoo SQL Reporting

## Goal
Build reporting models/views using SQL when ORM is not feasible.

## Patterns
- Create a non-auto model: `_auto = False`
- Define `init()` to create SQL view
- Use indexes if necessary

## Guardrails
- Must be read-only
- Ensure correct casting types (jsonb/translation fields)
- Support multi-company filtering

## Example Prompt
"Create a read-only report model combining sales + stock moves."
