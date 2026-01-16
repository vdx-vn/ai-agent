# Skill: Odoo Debugging

## Goal
Diagnose bugs from logs/tracebacks and propose minimal fixes.

## Steps
1) Identify failing model/method from traceback
2) Determine data shape causing crash (nulls, unexpected type, missing rights)
3) Reproduce scenario
4) Fix with minimal blast radius
5) Add guard + test if it's a recurring category

## Common Odoo failures
- access error / missing ACL
- singleton error
- psycopg2 type casting
- computed field recursion
- cache miss from wrong env/company

## Example Prompt
"Here's a traceback from safe_eval cron, locate cause and fix."