# Examples

## Positive triggers
1. "Use this project’s local Odoo command and run sale tests against the current project state."
   - Expected: use `odoo-local-test-harness` as primary skill and require a target disposable db if execution is requested.
2. "This repo is on Odoo 17.0, but the local command differs from my 18.0 project."
   - Expected: use `odoo-local-test-harness` as primary skill.
3. "Clean the temporary Odoo test database before the run, then clean it automatically when the run ends even if Odoo leaves an idle connection behind."
   - Expected: use `odoo-local-test-harness` as primary skill.

## Negative triggers
1. "Explain TransactionCase vs HttpCase."
   - Expected: do not use `odoo-local-test-harness` as primary skill.
2. "Is this checkout patch safe before merge?"
   - Expected: do not use `odoo-local-test-harness` as primary skill.
3. "Run local Odoo tests, but this project does not define `odooTestBaseCmd` or `ODOO_TEST_BASE_CMD` yet."
   - Expected: stop and ask the user to run `odoo-skills project-setup` before using the harness.

## Tie-breaker
- Prompt: "Run the local Odoo command for this project with `--test-tags /sale` on a disposable db and clean it automatically afterward."
- Why this skill wins: the task depends on a project-local base command and shared cleanup, so `odoo-local-test-harness` should win over `odoo-delivery-ops`.
