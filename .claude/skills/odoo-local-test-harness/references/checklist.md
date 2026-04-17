# Checklist

## Intake
- [ ] Confirm the request depends on project-local Odoo test execution.
- [ ] Read `ODOO_TEST_BASE_CMD` from `.claude/settings.local.json` or stop.
- [ ] Identify db name, test tags, install or update scope, and cleanup intent.
- [ ] Identify whether `odoo-test` or `odoo-delivery-ops` owns the final answer.

## Analysis
- [ ] Parse the base command with `shlex`, not shell concatenation.
- [ ] Confirm the base command already includes `-c` or `--config`.
- [ ] Preserve the configured `-c` or `--config` value from the base command.
- [ ] Confirm `ODOO_TEST_BASE_CMD` does not already include runtime-managed flags: `-d`, `--test-tags`, `--test-enable`, `-i`, `-u`, or `--stop-after-init`.
- [ ] Use shared cleanup for disposable databases and matching filestore state.
- [ ] Keep local config immutable unless the user asks to change it.

## Output
- [ ] Return resolved base command source.
- [ ] Return appended arguments.
- [ ] Return cleanup action performed or skipped.
- [ ] Return boundary decision with primary and sibling skills.
