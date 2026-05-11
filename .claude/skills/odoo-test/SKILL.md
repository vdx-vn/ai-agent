---
name: odoo-test
description: "Validate a concrete Odoo change with install, update, workflow, security, and performance checks. Compose with `odoo-local-test-harness` when local execution depends on a project-specific base Odoo test command or shared DB and filestore cleanup. Design, implement, run, and validate Odoo addon tests. Covers test selection, fixture strategy, tagging, interpreter alignment, pytest-odoo usage, Odoo runner fallback, install/update regression, workflow/security/performance checks, and current-change validation. Use when the user wants to write, fix, run, review, or validate Odoo tests — including regression coverage for bug fixes, diagnosing flaky or failing tests, improving test quality, or producing validation evidence before merge or release."
---

# Odoo Test Skill

## Primary routing rule

Use this skill when the primary output is:
- writing, fixing, or reviewing Odoo tests
- running or choosing validation for current Odoo work
- validation evidence or a validation plan tied to a specific diff, addon, or bug
- diagnosing flaky or failing tests
- adding regression coverage for a bug fix

**Do not use this skill when:**
- the primary output is framework theory or general test-authoring advice → `odoo-testing-reference`
- the task is pre-merge code review without validation evidence → `odoo-review`
- the task is deployment orchestration only → `odoo-ship`

---

## Scope

Generic — works across Odoo projects, addon sets, and team members.
Do not assume a specific repository layout beyond standard Odoo addon conventions.

---

## Workflow (execute in order)

### Step 1 — Discover the environment

**Check env vars first** — the SessionStart hook detects Odoo projects and suggests these on first run:

| Env var | Contains | Used by |
|---------|----------|---------|
| `ODOO_TEST_BASE_CMD` | `python odoo-bin -c odoo.conf` | Odoo runner (append `-d`, `--test-enable`, `-u`, `--stop-after-init`) |
| `ODOO_PYTEST_BASE_CMD` | `ODOO_RC=... PYTHONPATH=... python -m pytest` | pytest-odoo (append `--odoo-config`, `--odoo-addons-path`, test file) |

If either env var is set, **use it directly** — do not re-discover interpreter or config.

If neither is set, check `CLAUDE.md`/`AGENTS.md` for project-specific paths. If still not documented, fall back to manual discovery and tell the user to configure the env vars in `.claude/settings.local.json`:

```bash
# Find project interpreter
ls .venv/bin/python 2>/dev/null || pyenv which python

# Confirm it can import odoo
.venv/bin/python -c "import odoo; print(odoo.__file__)"

# Find config file
ls *.conf odoo_config 2>/dev/null
```

**Never assume system `python` or `python3`.**

### Step 2 — Read existing patterns first (Grep → targeted Read)

```bash
# Find existing tests in the target addon
ls <addon>/tests/

# Find the base class used by existing tests
grep -r "class Test" <addon>/tests/ --include="*.py" -l

# Find common.py if it exists
ls <addon>/tests/common.py 2>/dev/null
```

Then Read only the matched files at the relevant lines. Do not load entire test files unless necessary.

### Step 3 — Choose the test type

| Situation | Use |
|-----------|-----|
| Business logic, ORM, compute fields | `TransactionCase` (default) |
| State machine / stage transitions | `TransactionCase` — assert state before and after each transition |
| View defaults, onchange, form restrictions | `Form` |
| Routes, controllers, browser behavior | `HttpCase` |
| Queued / async jobs | `TransactionCase` — call job method directly, mock queue dispatch |
| Multiple test files share setup | `common.py` base class |
| Single test file, no sharing needed | Inherit `TransactionCase` directly |

Also choose by change surface:
- unit, transaction, HTTP, JS, tour, or performance
- cover install and update paths when relevant
- include security and multi-company checks when behavior changes

### Step 4 — Write the test

**Minimal structure:**

```python
from odoo.models import Command
from odoo.tests import TransactionCase, tagged

@tagged('post_install', '-at_install')
class TestFeatureName(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.record = cls.env['my.model'].create({
            'name': 'Test Record',
            # Use Command for many2many: 'tag_ids': [Command.link(tag.id)]
        })

    def test_expected_behavior(self):
        # Arrange (already done in setUpClass)
        # Act
        self.record.action_confirm()
        # Assert observable outcome, not internal detail
        self.assertEqual(self.record.state, 'confirmed')
        # Prefer assertRecordValues for multi-field assertions:
        # self.assertRecordValues(self.record, [{'state': 'confirmed', 'field': val}])
```

**Rules:**
- Test names describe the expected behavior: `test_user_cannot_confirm_draft_request`
- Assert observable results — not temporary implementation details
- Keep tests independent: no shared mutable state, no order dependence
- Always add the new file to `tests/__init__.py`

### Step 5 — Prepare a test config (if not already present)

**Always use a dedicated test config file** — never run tests with the dev/production config. The dev config typically has `workers > 0` and `queue_job` in `server_wide_modules`, both of which cause the process to hang after `--stop-after-init` or after pytest finishes.

Check if a test config already exists (check `CLAUDE.md` or `AGENTS.md` first):

```bash
ls odoo_config_test *.test.conf 2>/dev/null
```

If none exists, **create one** based on the dev config with these changes:

```ini
# odoo_config_test  (copy of dev config with test overrides)
[options]
addons_path = ...        # same as dev
db_port = ...            # same as dev
http_port = 8099         # different port — avoids conflict with running dev server
db_user = ...            # same as dev
db_password = ...        # same as dev
db_name = ...            # same as dev
admin_passwd = ...       # same as dev
workers = 0              # REQUIRED: prevents worker subprocesses that never exit
server_wide_modules = web  # REQUIRED: drops queue_job poller thread
# omit: dev_mode, proxy_mode, gevent_port — not needed for tests
```

Key changes from dev config:

| Setting | Dev | Test | Why |
|---------|-----|------|-----|
| `workers` | 2+ | **0** | Worker subprocesses don't exit after `--stop-after-init` |
| `server_wide_modules` | `web,queue_job` | **`web`** | `queue_job` starts a polling thread that never stops |
| `http_port` | 8069 | **8099** | Avoids port conflict with the running dev server |
| `dev_mode` | set | omitted | Not needed during test runs |
| `gevent_port` | set | omitted | Not needed when `workers=0` |

Also add a `conftest.py` at the project root for pytest runs:

```python
# conftest.py — project root
import os
import pytest

@pytest.fixture(scope='session', autouse=True)
def _force_exit_after_session(request):
    yield
    os._exit(0)
```

### Step 6 — Run the test

**Check env vars first** (set by the SessionStart hook — see Step 1):

**If `ODOO_PYTEST_BASE_CMD` is set — use it for pytest:**

```bash
$ODOO_PYTEST_BASE_CMD -x <addon>/tests/<test_file>.py \
  --odoo-config=<test_config_file> --odoo-addons-path=<addons_path> -q
```

**If `ODOO_TEST_BASE_CMD` is set — use it for the Odoo runner:**

```bash
$ODOO_TEST_BASE_CMD -d <db_name> \
  --test-enable --test-tags=post_install -u <module_name> --stop-after-init
```

Use `-i` instead of `-u` when the module is not yet installed.

**If neither env var is set**, fall back to manual command construction (see Step 1) and tell the user to configure the env vars.

**Module name starts with a digit (`3s_*`)** — use Odoo runner only, pytest-odoo cannot import it.

Do not silently switch interpreters to find a pytest binary. If pytest is missing, tell the user first.

### Step 7 — Verify and close

Before marking done, check every item:

- [ ] The test would have **failed** on the buggy behavior (verified)
- [ ] The test **passes** with the fix applied
- [ ] Test name clearly describes the expected behavior
- [ ] Fixture is minimal — no unnecessary records
- [ ] Assertions cover the user-visible outcome (prefer `assertRecordValues` for multi-field checks)
- [ ] `Command` used for many2many fields in fixtures, not raw `[(4, id)]`
- [ ] `tests/__init__.py` includes the new test file
- [ ] Tags match the local project style

---

## Output contract

When validating a concrete change, always return:
- **evidence status**: executed, planned, or blocked
- **test matrix**: which test types were run and why
- **commands or suites run**
- **observed failures or outcomes**
- **remaining validation gaps**
- **boundary decision**: primary skill, composed siblings, deferred scope

Separate executed evidence from planned validation. If nothing ran, say so plainly.

---

## common.py — When to Create It

Create `common.py` only when:
- 2+ test files in the same addon share significant setup, OR
- dependent addons will inherit this addon's test infrastructure

Otherwise, inherit `TransactionCase` directly in the test file.

**Layered inheritance pattern (Odoo core style):**

```
TransactionCase
  └── UomCommon (uom/tests/common.py)
        └── ProductCommon (product/tests/common.py)
              └── SaleCommon (sale/tests/common.py)
```

**Rules for common.py:**
- Never put `def test_*` methods in it — infrastructure only
- Always call `super().setUpClass()` before adding new setup
- Each layer adds only what is NEW at that layer

---

## Advanced Patterns

→ See `references/patterns.md` for full code samples.

| Scenario | Pattern |
|----------|---------|
| Test depends on current date/time | `freeze_time` |
| Test sends email / notifications | `mock_mail_gateway` |
| Test expects `AccessError` | `assertRaises` + `mute_logger` |
| Test checks onchange / view defaults | `Form` object |
| Test uses a wizard | Create → set fields → call action → assert |
| Test guards against perf regression | `assertQueryCount` + `@warmup` |
| Test involves multiple companies | `setup_other_company` + `with_company` |
| Test checks WebSocket / bus messages | `assertBus` |
| Test data needs stable XML IDs | `_load_records` |
| Fixture with many2many fields | `Command.link` / `Command.set` |
| State machine / stage transitions | Assert state before and after each step |
| Queue / async job | Call job method directly; mock dispatch |

---

## Common Pitfalls

- Forgetting to add the file to `tests/__init__.py`
- Using `Form` when a direct ORM call is enough (slower, more fragile)
- Mutating shared `setUpClass` records across test methods
- Asserting implementation details instead of observable outcomes
- Depending on demo data without confirming it exists in the target environment
- Using `setUp` (per-test) for expensive record creation — use `setUpClass` instead

---

## Known Errors

→ See `references/errors.md` for full solutions.

| Error | Quick pointer |
|-------|--------------|
| `module 'odoo' has no attribute 'tools'` | Explicit `import odoo.tools` needed (Odoo 19 namespace pkg) |
| `pytest_odoo` crashes on startup | Patch `hasattr(odoo, "tools")` in site-packages |
| `KeyError: 'odoo.addons.<module>'` | Add `--odoo-addons-path=...` |
| `OPENERP_SERVER` warning | Switch to `ODOO_RC` |
| Module name starts with digit (`3s_*`) | Use Odoo runner, not pytest |
| Migrated v14→v19 code failures | See errors.md table |
| Test process hangs after results print | Add `conftest.py` with `os._exit(0)` (pytest) or `--workers=0` (Odoo runner) |
| Queue job partial success | Assert full outcome, not just no exception |

---

## Guardrails

- Stay inside this skill's responsibility; do not absorb neighboring tasks.
- Prefer Odoo `<ODOO_MAJOR_VERSION>` docs for functional rules and Odoo CE source for implementation truth.
- Call out docs or source mismatches instead of hiding them.
- Name permissions impact, migration impact, and cross-app modules whenever relevant.
- Name rollback or staging risk whenever release or data impact exists.

# Must hand off when
- If the user asks how Odoo testing primitives work in general, hand off to `odoo-testing-reference`.
- If the ask is a pre-merge reasoning review rather than validation evidence, hand off to `odoo-review`.
- Compose with business skills when workflow validation depends on domain process.
- If local execution depends on a project-specific base command or shared cleanup harness, compose with `odoo-local-test-harness`.

- `odoo-review`
- `odoo-testing-reference`
- `odoo-performance`
- `odoo-local-test-harness`

---

## References

- Read `references/overview.md` for scope, anchors, and pairings.
- Use `references/checklist.md` for deterministic validation checks.
- Use `references/examples.md` to compare trigger, boundary, and tie-breaker prompts.
- Use `references/patterns.md` for advanced test pattern code samples.
- Use `references/errors.md` for known error solutions.
