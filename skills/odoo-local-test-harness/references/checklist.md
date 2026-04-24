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
- [ ] Select `--db-mode auto|existing|disposable`.
- [ ] In auto mode, map install or update validation to disposable and other current-project-state validation to existing.
- [ ] In existing mode, prefer config `db_name`.
- [ ] Otherwise list accessible non-system DBs from the config connection settings.
- [ ] If multiple candidates exist, stop and ask the user which DB to use.
- [ ] Do not use `dbfilter` to narrow candidates.
- [ ] Disposable mode requires an explicit DB name.
- [ ] Use `--cleanup-before` only when a disposable database must be reset before execution.
- [ ] Keep automatic post-run cleanup for disposable databases and matching filestore state, including terminating leftover sessions before `dropdb` when needed.
- [ ] Skip DB/filestore cleanup in existing mode.
- [ ] Keep local config immutable unless the user asks to change it.

## Output
- [ ] Return resolved config path.
- [ ] Return resolved base command source.
- [ ] Return selected DB mode.
- [ ] Return selected DB or candidate list.
- [ ] Return appended arguments.
- [ ] Return cleanup action.
- [ ] Return boundary decision with primary and sibling skills.
