# Odoo Test DB Mode Enforcement Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Enforce Odoo local test execution so current-state tests reuse an existing DB, while install/update/disposable tests require a named disposable DB and always clean its DB plus filestore afterward.

**Architecture:** Keep `run_odoo_test.py` as runtime gatekeeper for DB mode selection, command construction, and cleanup orchestration. Keep `delete_unused_odoo_db.py` as cleanup unit for PostgreSQL database and matching filestore deletion. Align shipped skill docs and reference examples with runtime behavior, then lock both with unit tests.

**Tech Stack:** Python 3, `unittest`, `unittest.mock`, Odoo CLI flags, PostgreSQL CLI tools (`psql`, `dropdb`), Markdown skill docs.

---

## File Structure

- Modify `skills/odoo-local-test-harness/scripts/run_odoo_test.py`
  - Responsibility: parse `ODOO_TEST_BASE_CMD`, choose DB mode, build Odoo command, print resolved execution plan, and run cleanup only for disposable DB mode.
- Modify `skills/odoo-local-test-harness/scripts/delete_unused_odoo_db.py`
  - Responsibility: validate DB name, terminate DB sessions, drop disposable DB, and remove matching filestore path safely. No broad refactor expected.
- Modify `tests/unit/test_run_odoo_test.py`
  - Responsibility: guard default existing DB behavior, disposable DB requirements, cleanup-after behavior, and printed cleanup action.
- Modify `tests/unit/test_delete_unused_odoo_db.py`
  - Responsibility: guard filestore path safety and cleanup order.
- Modify `tests/unit/test_odoo_local_test_harness_docs.py`
  - Responsibility: ensure shipped docs keep DB-mode and cleanup contract visible.
- Modify `skills/odoo-test/SKILL.md` and `skills/odoo-test/references/{overview.md,checklist.md,examples.md}`
  - Responsibility: state validation DB-mode rules from current-change validation perspective.
- Modify `skills/odoo-local-test-harness/SKILL.md` and `skills/odoo-local-test-harness/references/{overview.md,checklist.md,examples.md}`
  - Responsibility: state local harness execution, runtime flag ownership, DB resolution, and cleanup behavior.

---

### Task 1: Add runtime guardrail tests for DB mode and cleanup action

**Files:**
- Modify: `tests/unit/test_run_odoo_test.py`

- [ ] **Step 1: Add stdout capture import**

Add this import near existing imports at top of `tests/unit/test_run_odoo_test.py`:

```python
from contextlib import redirect_stdout
```

- [ ] **Step 2: Add auto current-state existing DB test**

Add this test method after `test_main_existing_mode_skips_cleanup_before_and_after`:

```python
    @patch("run_odoo_test.cleanup_database")
    @patch("run_odoo_test.subprocess.run")
    def test_main_auto_current_state_uses_existing_db_and_reports_cleanup_skipped(self, run_mock, cleanup_mock) -> None:
        stdout = io.StringIO()

        with redirect_stdout(stdout):
            exit_code = run_odoo_test.main(
                [
                    "--test-tags",
                    "/sale",
                ],
                env={
                    "ODOO_TEST_BASE_CMD": "python3 /opt/odoo/odoo-bin -c /tmp/odoo.conf"
                },
                resolve_existing_db_name=lambda _config_path: "existing_db",
            )

        self.assertEqual(exit_code, 0)
        cleanup_mock.assert_not_called()
        run_mock.assert_called_once_with(
            [
                "python3",
                "/opt/odoo/odoo-bin",
                "-c",
                "/tmp/odoo.conf",
                "-d",
                "existing_db",
                "--test-tags",
                "/sale",
                "--test-enable",
                "--stop-after-init",
            ],
            check=True,
        )
        output = stdout.getvalue()
        self.assertIn("Selected mode: existing", output)
        self.assertIn("Selected DB: existing_db", output)
        self.assertIn("Cleanup action: skipped (existing mode)", output)
```

- [ ] **Step 3: Add auto install missing DB rejection test**

Add this test method after the test from Step 2:

```python
    @patch("run_odoo_test.cleanup_database")
    @patch("run_odoo_test.subprocess.run")
    def test_main_auto_install_requires_explicit_disposable_db(self, run_mock, cleanup_mock) -> None:
        with self.assertRaises(SystemExit) as exc:
            run_odoo_test.main(
                [
                    "--install",
                    "sale",
                ],
                env={
                    "ODOO_TEST_BASE_CMD": "python3 /opt/odoo/odoo-bin -c /tmp/odoo.conf"
                },
            )

        self.assertIn("--db is required when --db-mode is disposable", str(exc.exception))
        run_mock.assert_not_called()
        cleanup_mock.assert_not_called()
```

- [ ] **Step 4: Add auto update disposable cleanup test**

Add this test method after the test from Step 3:

```python
    @patch("run_odoo_test.cleanup_database")
    @patch("run_odoo_test.subprocess.run")
    def test_main_auto_update_uses_disposable_db_and_reports_cleanup_after(self, run_mock, cleanup_mock) -> None:
        stdout = io.StringIO()

        with redirect_stdout(stdout):
            exit_code = run_odoo_test.main(
                [
                    "--update",
                    "stock",
                    "--db",
                    "tmp_odoo_test",
                ],
                env={
                    "ODOO_TEST_BASE_CMD": "python3 /opt/odoo/odoo-bin -c /tmp/odoo.conf"
                },
            )

        self.assertEqual(exit_code, 0)
        cleanup_mock.assert_called_once_with(
            db_name="tmp_odoo_test",
            config_path=Path("/tmp/odoo.conf"),
            dry_run=False,
        )
        run_mock.assert_called_once_with(
            [
                "python3",
                "/opt/odoo/odoo-bin",
                "-c",
                "/tmp/odoo.conf",
                "-d",
                "tmp_odoo_test",
                "-u",
                "stock",
                "--stop-after-init",
            ],
            check=True,
        )
        output = stdout.getvalue()
        self.assertIn("Selected mode: disposable", output)
        self.assertIn("Selected DB: tmp_odoo_test", output)
        self.assertIn("Cleanup action: automatic cleanup after run", output)
```

- [ ] **Step 5: Run focused test and verify failure before implementation**

Run:

```bash
python3 -m unittest tests.unit.test_run_odoo_test.RunOdooTestTests.test_main_auto_current_state_uses_existing_db_and_reports_cleanup_skipped tests.unit.test_run_odoo_test.RunOdooTestTests.test_main_auto_install_requires_explicit_disposable_db tests.unit.test_run_odoo_test.RunOdooTestTests.test_main_auto_update_uses_disposable_db_and_reports_cleanup_after -v
```

Expected before Task 2: command fails because stdout does not include `Cleanup action: skipped (existing mode)` and `Cleanup action: automatic cleanup after run`.

- [ ] **Step 6: Commit checkpoint only if user explicitly requested commits**

If commit workflow is explicitly approved, run:

```bash
git add tests/unit/test_run_odoo_test.py
git commit -m "test: lock Odoo test DB mode behavior"
```

---

### Task 2: Add cleanup action reporting to runtime harness

**Files:**
- Modify: `skills/odoo-local-test-harness/scripts/run_odoo_test.py`
- Test: `tests/unit/test_run_odoo_test.py`

- [ ] **Step 1: Add cleanup action helper**

In `skills/odoo-local-test-harness/scripts/run_odoo_test.py`, add this function after `maybe_cleanup`:

```python
def cleanup_action_description(*, db_mode: str, cleanup_before: bool, dry_run: bool) -> str:
    if dry_run:
        return "skipped (dry-run)"
    if db_mode == "existing":
        return "skipped (existing mode)"
    if cleanup_before:
        return "cleanup before run and automatic cleanup after run"
    return "automatic cleanup after run"
```

- [ ] **Step 2: Print cleanup action in main execution plan**

In `main`, replace the print block:

```python
    print("Resolved config path:", config_path)
    print("Selected mode:", db_mode)
    print("Selected DB:", selected_db)
    print("Resolved base command:", " ".join(shlex.quote(part) for part in base_argv))
    print("Final command:", " ".join(shlex.quote(part) for part in command))
```

with:

```python
    print("Resolved config path:", config_path)
    print("Selected mode:", db_mode)
    print("Selected DB:", selected_db)
    print(
        "Cleanup action:",
        cleanup_action_description(
            db_mode=db_mode,
            cleanup_before=args.cleanup_before,
            dry_run=args.dry_run,
        ),
    )
    print("Resolved base command:", " ".join(shlex.quote(part) for part in base_argv))
    print("Final command:", " ".join(shlex.quote(part) for part in command))
```

- [ ] **Step 3: Run Task 1 tests and verify pass**

Run:

```bash
python3 -m unittest tests.unit.test_run_odoo_test.RunOdooTestTests.test_main_auto_current_state_uses_existing_db_and_reports_cleanup_skipped tests.unit.test_run_odoo_test.RunOdooTestTests.test_main_auto_install_requires_explicit_disposable_db tests.unit.test_run_odoo_test.RunOdooTestTests.test_main_auto_update_uses_disposable_db_and_reports_cleanup_after -v
```

Expected after implementation: `OK`.

- [ ] **Step 4: Run full run_odoo_test unit module**

Run:

```bash
python3 -m unittest tests.unit.test_run_odoo_test -v
```

Expected: all tests in `tests.unit.test_run_odoo_test` pass.

- [ ] **Step 5: Commit checkpoint only if user explicitly requested commits**

If commit workflow is explicitly approved, run:

```bash
git add skills/odoo-local-test-harness/scripts/run_odoo_test.py tests/unit/test_run_odoo_test.py
git commit -m "feat: report Odoo test cleanup action"
```

---

### Task 3: Add cleanup safety guardrail tests

**Files:**
- Modify: `tests/unit/test_delete_unused_odoo_db.py`
- Modify only if needed: `skills/odoo-local-test-harness/scripts/delete_unused_odoo_db.py`

- [ ] **Step 1: Add path safety test**

Add this test method after `test_validate_db_name_rejects_invalid_values`:

```python
    def test_filestore_path_rejects_unsafe_db_names(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            conf = Path(tmp) / "odoo.conf"
            conf.write_text(f"[options]\ndata_dir = {Path(tmp) / 'data'}\n")

            for db_name in ["../evil", "nested/db", "nested\\db", "/absolute", ".", ".."]:
                with self.subTest(db_name=db_name):
                    with self.assertRaises(ValueError):
                        cleanup.filestore_path(conf, db_name)
```

- [ ] **Step 2: Add matching filestore target test**

Add this test method after the test from Step 1:

```python
    def test_filestore_path_uses_config_data_dir_and_db_name(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            conf = Path(tmp) / "odoo.conf"
            data_dir = Path(tmp) / "odoo-data"
            conf.write_text(f"[options]\ndata_dir = {data_dir}\n")

            self.assertEqual(
                cleanup.filestore_path(conf, "tmp_odoo_test"),
                (data_dir / "filestore" / "tmp_odoo_test").resolve(strict=False),
            )
```

- [ ] **Step 3: Run focused cleanup tests**

Run:

```bash
python3 -m unittest tests.unit.test_delete_unused_odoo_db.DeleteUnusedOdooDbTests.test_filestore_path_rejects_unsafe_db_names tests.unit.test_delete_unused_odoo_db.DeleteUnusedOdooDbTests.test_filestore_path_uses_config_data_dir_and_db_name -v
```

Expected: `OK`. If this fails, change only `validate_db_name` and `filestore_path` so invalid names raise `ValueError` before building command strings or paths.

- [ ] **Step 4: Run full cleanup unit module**

Run:

```bash
python3 -m unittest tests.unit.test_delete_unused_odoo_db -v
```

Expected: all tests in `tests.unit.test_delete_unused_odoo_db` pass.

- [ ] **Step 5: Commit checkpoint only if user explicitly requested commits**

If commit workflow is explicitly approved, run:

```bash
git add tests/unit/test_delete_unused_odoo_db.py skills/odoo-local-test-harness/scripts/delete_unused_odoo_db.py
git commit -m "test: lock Odoo cleanup filestore safety"
```

---

### Task 4: Expand docs contract tests

**Files:**
- Modify: `tests/unit/test_odoo_local_test_harness_docs.py`

- [ ] **Step 1: Extend expected snippets for `odoo-test`**

In `test_docs_describe_existing_and_disposable_db_modes`, update the snippets for `ROOT / "odoo-test" / "SKILL.md"` to this exact list:

```python
            ROOT / "odoo-test" / "SKILL.md": [
                "current-state validation uses an existing db by default",
                "install, update, or explicit disposable validation uses a disposable db",
                "never clean DB/filestore in existing mode",
                "always clean DB + filestore after disposable runs",
            ],
```

- [ ] **Step 2: Extend expected snippets for `odoo-test` overview and checklist**

Update the snippets for `ROOT / "odoo-test" / "references" / "overview.md"` to this exact list:

```python
            ROOT / "odoo-test" / "references" / "overview.md": [
                "current-project-state validation to existing db by default",
                "install, update, or explicit disposable validation to disposable db by default",
                "Existing-db validation must not clean DB or filestore",
                "Disposable-db validation must clean DB and filestore after execution",
            ],
```

Update the snippets for `ROOT / "odoo-test" / "references" / "checklist.md"` to this exact list:

```python
            ROOT / "odoo-test" / "references" / "checklist.md": [
                "Choose validation DB mode by change surface",
                "Use existing DB mode for current-project-state validation",
                "Use disposable DB mode for install, update, or explicit disposable validation",
                "Name cleanup expectations explicitly for the chosen DB mode",
                "Confirm existing mode skips DB/filestore cleanup",
                "Confirm disposable mode cleans DB + filestore after execution",
            ],
```

- [ ] **Step 3: Extend expected snippets for harness docs**

Update the snippets for `ROOT / "odoo-local-test-harness" / "SKILL.md"` to this exact list:

```python
            ROOT / "odoo-local-test-harness" / "SKILL.md": [
                "--db-mode auto|existing|disposable",
                "prefer config `db_name`",
                "multiple candidates",
                "existing mode must never clean DB/filestore",
                "install, update, or explicit disposable mode requires explicit `--db`",
                "automatic post-run cleanup of DB + filestore",
                "resolved config path",
                "selected DB mode",
            ],
```

Update the snippets for `ROOT / "odoo-local-test-harness" / "references" / "overview.md"` to this exact list:

```python
            ROOT / "odoo-local-test-harness" / "references" / "overview.md": [
                "Do not use `dbfilter` to narrow candidates",
                "selected DB or candidate list",
                "cleanup action",
                "Existing mode must not clean DB or filestore",
                "Disposable mode must clean DB and filestore after execution",
            ],
```

Update the snippets for `ROOT / "odoo-local-test-harness" / "references" / "checklist.md"` to this exact list:

```python
            ROOT / "odoo-local-test-harness" / "references" / "checklist.md": [
                "prefer config `db_name`",
                "If multiple candidates exist, stop and ask the user which DB to use",
                "Disposable mode requires an explicit DB name",
                "Existing mode must not clean DB/filestore",
                "Disposable mode must clean DB + filestore after execution",
            ],
```

- [ ] **Step 4: Run docs contract test and verify failure before docs edits**

Run:

```bash
python3 -m unittest tests.unit.test_odoo_local_test_harness_docs.OdooLocalTestHarnessDocsTests.test_docs_describe_existing_and_disposable_db_modes -v
```

Expected before Task 5: FAIL with missing snippet assertions for new wording.

- [ ] **Step 5: Commit checkpoint only if user explicitly requested commits**

If commit workflow is explicitly approved, run:

```bash
git add tests/unit/test_odoo_local_test_harness_docs.py
git commit -m "test: lock Odoo skill DB mode docs"
```

---

### Task 5: Update Odoo test skill docs

**Files:**
- Modify: `skills/odoo-test/SKILL.md`
- Modify: `skills/odoo-test/references/overview.md`
- Modify: `skills/odoo-test/references/checklist.md`
- Modify: `skills/odoo-test/references/examples.md`
- Test: `tests/unit/test_odoo_local_test_harness_docs.py`

- [ ] **Step 1: Update `skills/odoo-test/SKILL.md` use cases**

Replace the DB-mode bullets under `# Use this skill when` with:

```markdown
- run or choose validation for current Odoo work
- route current-state validation uses an existing db by default
- route install, update, or explicit disposable validation uses a disposable db
- enforce that existing mode must never clean DB/filestore
- enforce that disposable mode must always clean DB + filestore after disposable runs
- prepare confidence signal before merge or release
- triage failing validation for current work
```

- [ ] **Step 2: Update `skills/odoo-test/SKILL.md` workflow and output contract**

Replace workflow item 3:

```markdown
3. Apply the deterministic checks in `references/checklist.md`.
```

with:

```markdown
3. Apply the deterministic checks in `references/checklist.md`, including DB mode and cleanup expectations.
```

Add this output bullet after `- commands or suites run`:

```markdown
- selected DB mode and cleanup action
```

- [ ] **Step 3: Update `skills/odoo-test/references/overview.md` key checks**

Replace the first two DB-mode key checks with:

```markdown
- Route current-project-state validation to existing db by default.
- Route install, update, or explicit disposable validation to disposable db by default.
- Existing-db validation must not clean DB or filestore.
- Disposable-db validation must clean DB and filestore after execution.
```

- [ ] **Step 4: Update `skills/odoo-test/references/checklist.md` analysis checks**

Replace the DB-mode analysis bullets with:

```markdown
- [ ] Use existing DB mode for current-project-state validation unless the user explicitly wants disposable setup.
- [ ] Use disposable DB mode for install, update, or explicit disposable validation unless the user explicitly overrides.
- [ ] Confirm existing mode skips DB/filestore cleanup.
- [ ] Confirm disposable mode cleans DB + filestore after execution.
```

- [ ] **Step 5: Update `skills/odoo-test/references/examples.md` positive trigger**

Replace positive trigger 3 with:

```markdown
3. "Check install and update regressions for this addon on a disposable database, then clean its DB and filestore."
   - Expected: use `odoo-test` as primary skill and compose with `odoo-local-test-harness` when local execution is needed.
```

- [ ] **Step 6: Run docs contract test for `odoo-test` snippets**

Run:

```bash
python3 -m unittest tests.unit.test_odoo_local_test_harness_docs.OdooLocalTestHarnessDocsTests.test_docs_describe_existing_and_disposable_db_modes -v
```

Expected after this task: may still fail for harness snippets until Task 6; `odoo-test` snippets should no longer appear in failure output.

- [ ] **Step 7: Commit checkpoint only if user explicitly requested commits**

If commit workflow is explicitly approved, run:

```bash
git add skills/odoo-test/SKILL.md skills/odoo-test/references/overview.md skills/odoo-test/references/checklist.md skills/odoo-test/references/examples.md tests/unit/test_odoo_local_test_harness_docs.py
git commit -m "docs: clarify Odoo test DB mode contract"
```

---

### Task 6: Update local test harness docs

**Files:**
- Modify: `skills/odoo-local-test-harness/SKILL.md`
- Modify: `skills/odoo-local-test-harness/references/overview.md`
- Modify: `skills/odoo-local-test-harness/references/checklist.md`
- Modify: `skills/odoo-local-test-harness/references/examples.md`
- Test: `tests/unit/test_odoo_local_test_harness_docs.py`

- [ ] **Step 1: Update `skills/odoo-local-test-harness/SKILL.md` workflow DB-mode items**

Replace workflow items 4 through 6 with:

```markdown
4. In auto mode, default to existing for current-project-state validation and to disposable for install or update validation.
5. In existing mode, prefer config `db_name`; otherwise list accessible non-system databases from the config connection settings, stop on multiple candidates, do not use `dbfilter` to narrow candidates, and existing mode must never clean DB/filestore.
6. In disposable mode, install, update, or explicit disposable mode requires explicit `--db`; allow cleanup-before, and keep automatic post-run cleanup of DB + filestore through `scripts/delete_unused_odoo_db.py`, including terminating leftover sessions before `dropdb` when needed.
```

- [ ] **Step 2: Update `skills/odoo-local-test-harness/SKILL.md` output contract**

Replace this output bullet:

```markdown
- cleanup action performed or skipped
```

with:

```markdown
- cleanup action: skipped for existing mode, skipped for dry-run, automatic DB + filestore cleanup after disposable runs
```

- [ ] **Step 3: Update `skills/odoo-local-test-harness/references/overview.md` key checks**

Replace key checks from `- In auto mode...` through cleanup checks with:

```markdown
- In auto mode, use existing for current-project-state validation and disposable for install or update validation.
- In existing mode, prefer config `db_name`; otherwise list accessible non-system databases with the config connection settings.
- If multiple candidates exist, stop and return the candidate list so the user can choose which DB to use.
- Do not use `dbfilter` to narrow candidates.
- Existing mode must not clean DB or filestore.
- Use `--cleanup-before` only when a disposable local database must be cleared before the run.
- Disposable mode requires an explicit DB name.
- Disposable mode must clean DB and filestore after execution.
- Use shared automatic post-run cleanup only for disposable local database flows, and skip DB/filestore cleanup in existing mode.
- Expect shared cleanup to terminate leftover sessions on the target disposable database before `dropdb`, so filestore removal is not blocked by idle connections.
```

- [ ] **Step 4: Update `skills/odoo-local-test-harness/references/checklist.md` cleanup checks**

Replace cleanup-related analysis bullets with:

```markdown
- [ ] Disposable mode requires an explicit DB name.
- [ ] Existing mode must not clean DB/filestore.
- [ ] Use `--cleanup-before` only when a disposable database must be reset before execution.
- [ ] Disposable mode must clean DB + filestore after execution, including terminating leftover sessions before `dropdb` when needed.
- [ ] Skip DB/filestore cleanup in existing mode.
```

- [ ] **Step 5: Update `skills/odoo-local-test-harness/references/examples.md` positive triggers**

Replace positive trigger 3 with:

```markdown
3. "Run install validation on a named disposable Odoo test database, clean it before the run, and clean its DB plus filestore after the run even if Odoo leaves an idle connection behind."
   - Expected: use `odoo-local-test-harness` as primary skill and route install or update validation to disposable db by default.
```

Add this tie-breaker bullet after existing tie-breaker text:

```markdown
- Cleanup boundary: existing db mode skips cleanup; disposable db mode cleans DB plus filestore after execution.
```

- [ ] **Step 6: Run docs contract tests and verify pass**

Run:

```bash
python3 -m unittest tests.unit.test_odoo_local_test_harness_docs -v
```

Expected: all tests in `tests.unit.test_odoo_local_test_harness_docs` pass.

- [ ] **Step 7: Commit checkpoint only if user explicitly requested commits**

If commit workflow is explicitly approved, run:

```bash
git add skills/odoo-local-test-harness/SKILL.md skills/odoo-local-test-harness/references/overview.md skills/odoo-local-test-harness/references/checklist.md skills/odoo-local-test-harness/references/examples.md tests/unit/test_odoo_local_test_harness_docs.py
git commit -m "docs: clarify Odoo harness cleanup contract"
```

---

### Task 7: Run integration-level validation for changed area

**Files:**
- Validate: `skills/odoo-local-test-harness/scripts/run_odoo_test.py`
- Validate: `skills/odoo-local-test-harness/scripts/delete_unused_odoo_db.py`
- Validate: `skills/odoo-test/**`
- Validate: `skills/odoo-local-test-harness/**`
- Validate: `tests/unit/test_run_odoo_test.py`
- Validate: `tests/unit/test_delete_unused_odoo_db.py`
- Validate: `tests/unit/test_odoo_local_test_harness_docs.py`

- [ ] **Step 1: Run focused test suite**

Run:

```bash
python3 -m unittest tests.unit.test_run_odoo_test tests.unit.test_delete_unused_odoo_db tests.unit.test_odoo_local_test_harness_docs -v
```

Expected: all focused tests pass.

- [ ] **Step 2: Run full unit suite**

Run:

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

Expected: full suite passes.

- [ ] **Step 3: Run repo validator**

Run:

```bash
python3 -m tooling.cli verify
```

Expected: validation passes. If Claude CLI is unavailable in the environment, Python validator output should pass and CLI validation skip/failure should be reported exactly.

- [ ] **Step 4: Inspect git diff**

Run:

```bash
git diff -- skills/odoo-test skills/odoo-local-test-harness tests/unit/test_run_odoo_test.py tests/unit/test_delete_unused_odoo_db.py tests/unit/test_odoo_local_test_harness_docs.py
```

Expected: diff only changes runtime cleanup-action reporting, guardrail tests, and DB-mode/cleanup wording.

- [ ] **Step 5: Commit checkpoint only if user explicitly requested commits**

If commit workflow is explicitly approved, run:

```bash
git add skills/odoo-test skills/odoo-local-test-harness tests/unit/test_run_odoo_test.py tests/unit/test_delete_unused_odoo_db.py tests/unit/test_odoo_local_test_harness_docs.py
git commit -m "feat: enforce Odoo test DB mode contract"
```

---

## Self-Review

Spec coverage:

- Existing current-state validation uses existing DB: Task 1 tests it, Task 5 documents it.
- Install/update/disposable validation uses named disposable DB: Task 1 tests install/update paths, Task 5 and Task 6 document it.
- Existing mode never cleans DB/filestore: Task 1 tests cleanup skip, Task 4 locks docs wording.
- Disposable mode cleans DB + filestore after run: existing tests plus Task 1 and Task 6 lock behavior and wording.
- Filestore cleanup target from config and DB name: Task 3 tests it.
- Dry-run skips execution and cleanup: existing tests remain covered by Task 7 focused suite.
- Public docs match runtime scripts: Task 4, Task 5, and Task 6 cover docs contract.

Plan consistency:

- Function names match existing code: `run_odoo_test.main`, `choose_db_mode`, `cleanup_database`, `filestore_path`.
- New helper name `cleanup_action_description` is defined before use.
- Test imports match required stdout capture: `redirect_stdout` from `contextlib`.
- No new dependencies introduced.
