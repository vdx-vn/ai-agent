# Checklist

## Intake
- [ ] Confirm the request depends on project-local Odoo test execution.
- [ ] Read `ODOO_TEST_BASE_CMD` from `.claude/settings.local.json` or stop.
- [ ] Identify db name, test tags, install or update scope, and whether pre-run cleanup or dry-run is needed.
- [ ] Identify whether `odoo-test` or `odoo-delivery-ops` owns the final answer.

## Analysis
- [ ] Parse the base command with `shlex`, not shell concatenation.
- [ ] Confirm the base command already includes `-c` or `--config`.
- [ ] Preserve the configured `-c` or `--config` value from the base command.
- [ ] Confirm `ODOO_TEST_BASE_CMD` does not already include runtime-managed flags: `-d`, `--test-tags`, `--test-enable`, `-i`, `-u`, or `--stop-after-init`.
- [ ] Use `--cleanup-before` only when a disposable database must be reset before execution.
- [ ] Keep automatic post-run cleanup for disposable databases and matching filestore state.
- [ ] Keep local config immutable unless the user asks to change it.

## Output
- [ ] Return resolved base command source.
- [ ] Return appended arguments.
- [ ] Return whether pre-run cleanup ran.
- [ ] Return that post-run cleanup is automatic for real runs.
- [ ] Return boundary decision with primary and sibling skills.
