# Odoo test DB mode enforcement design

## Goal

Make Odoo test skill behavior deterministic and enforceable:

- Normal current-state validation runs against an existing configured database.
- Install, update, or explicit disposable runs require a named disposable database.
- Disposable runs clean database and matching filestore after execution.
- Existing-database runs never clean database or filestore.

## Scope

Update shipped skill instructions, local harness behavior, and tests together. Target files:

- `skills/odoo-test/SKILL.md`
- `skills/odoo-test/references/overview.md`
- `skills/odoo-test/references/checklist.md`
- `skills/odoo-test/references/examples.md`
- `skills/odoo-local-test-harness/SKILL.md`
- `skills/odoo-local-test-harness/references/overview.md`
- `skills/odoo-local-test-harness/references/checklist.md`
- `skills/odoo-local-test-harness/references/examples.md`
- `skills/odoo-local-test-harness/scripts/run_odoo_test.py`
- `skills/odoo-local-test-harness/scripts/delete_unused_odoo_db.py`
- `tests/unit/test_run_odoo_test.py`
- `tests/unit/test_delete_unused_odoo_db.py`
- `tests/unit/test_odoo_local_test_harness_docs.py`

No new Odoo runtime dependency, no package format change, no marketplace metadata change.

## Behavior contract

### Existing database mode

Use existing database mode for current-project-state validation when no install or update scope is requested.

Resolution order:

1. Use `db_name` from Odoo config if exactly one database is configured.
2. If config has no `db_name`, list accessible non-system PostgreSQL databases using config connection options.
3. If exactly one candidate exists, use it.
4. If multiple candidates exist, stop and show candidates.
5. Do not use `dbfilter` to narrow candidates.

Existing mode appends `-d <existing_db>` and optional test tags. It never calls cleanup before or after the run.

### Disposable database mode

Use disposable mode when any of these is true:

- explicit `--db-mode disposable`
- auto mode with `--install`
- auto mode with `--update`

Disposable mode requires explicit `--db <name>`. The harness must fail before running Odoo if no DB name is provided.

Disposable mode may run cleanup before execution only when `--cleanup-before` is passed. It must always run cleanup after execution from a `finally` block when not in dry-run mode.

Cleanup deletes:

- PostgreSQL database named by `--db`
- filestore directory for that database under configured `data_dir` or default Odoo data dir

Cleanup terminates leftover database sessions before `dropdb`.

### Dry-run mode

Dry-run prints resolved config path, selected DB mode, selected DB, base command, and final command. It does not require existing config file resolution in existing mode, does not execute Odoo, and does not run cleanup.

## Script enforcement

`run_odoo_test.py` remains the source of runtime enforcement.

Required checks:

- `choose_db_mode(auto, install=None, update=None)` returns `existing`.
- `choose_db_mode(auto, install=...)` returns `disposable`.
- `choose_db_mode(auto, update=...)` returns `disposable`.
- Disposable mode rejects missing `--db`.
- Existing mode resolves DB name and skips cleanup even when `--cleanup-before` is passed.
- Disposable mode runs cleanup after success, subprocess failure, and interruption.
- If both Odoo run and cleanup fail, preserve primary run failure for normal exceptions and interruptions.
- If Odoo succeeds but cleanup fails, surface cleanup failure.

`delete_unused_odoo_db.py` remains responsible for safe cleanup.

Required checks:

- validate DB names before using them in commands or paths.
- resolve filestore path under Odoo `data_dir` or default Odoo data dir.
- reject path traversal and absolute DB names.
- terminate sessions before `dropdb`.
- remove filestore only after database drop succeeds.

## Skill and reference enforcement

`odoo-test` must state DB mode choice as part of validation intake and output.

Required wording concepts:

- current-state validation uses existing DB by default.
- install or update validation uses disposable DB by default.
- cleanup expectations must be named in output.
- compose with `odoo-local-test-harness` when local execution needs `ODOO_TEST_BASE_CMD`, DB resolution, or cleanup.

`odoo-local-test-harness` must state runtime flags and cleanup ownership.

Required wording concepts:

- `ODOO_TEST_BASE_CMD` is immutable base command.
- base command must not include runtime-managed flags.
- harness owns `-d`, `--test-tags`, `--test-enable`, `-i`, `-u`, and `--stop-after-init`.
- existing mode skips DB and filestore cleanup.
- disposable mode requires explicit DB and cleans DB plus filestore after run.
- dry-run skips execution and cleanup.

## Test strategy

Run focused unit tests first:

```bash
python3 -m unittest tests.unit.test_run_odoo_test tests.unit.test_delete_unused_odoo_db tests.unit.test_odoo_local_test_harness_docs -v
```

Run full suite after edits:

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

Run repo validator if available:

```bash
python3 -m tooling.cli verify
```

## Acceptance criteria

- Existing current-state test command uses an existing DB, not an empty new DB.
- Install/update test command requires named disposable DB.
- Disposable cleanup-after runs on success and failure.
- Existing mode never deletes database or filestore.
- Filestore cleanup target is derived from Odoo config and DB name.
- Public skill docs describe the same behavior as runtime scripts.
- Focused tests and full unit suite pass.

## Risks

- Existing DB auto-discovery can be ambiguous. Mitigation: stop on multiple candidates and ask user to choose.
- Cleanup is destructive for disposable DB names. Mitigation: require explicit DB name and validate names/paths.
- Dry-run can hide missing config files. Mitigation: keep this limited to dry-run so users can preview commands before environment setup.
