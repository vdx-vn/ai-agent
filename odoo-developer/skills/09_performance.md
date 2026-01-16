# Skill: Odoo Performance

## Goal
Optimize slow code while keeping correctness.

## Checklist
- Avoid loops with `search()` inside (N+1)
- Use `read_group` for aggregates
- Batch write/create
- Pre-fetch related fields
- Use domains efficiently

## Guardrails
- Don't micro-optimize prematurely
- Raw SQL only with strong justification + explaination

## Example Prompt
"This report is slow. Identify N+1 patterns and refactor."
