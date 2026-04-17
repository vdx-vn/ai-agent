---
name: odoo-test
description: "Reusable Odoo testing skill for designing, implementing, reviewing, and running addon tests. Covers test selection, fixture strategy, tagging, interpreter alignment, pytest-odoo usage, and fallback to the standard Odoo test runner. Use this skill whenever the user wants to write, fix, run, or review Odoo tests — including regression coverage for bug fixes, diagnosing flaky or failing tests, or improving test quality in any Odoo addon."
version: 2.1.0
---

# Odoo Test Skill

Use this skill when the user asks to:
- write Odoo tests
- add regression coverage for a bug fix
- review existing tests for quality or gaps
- diagnose why an Odoo test is flaky or failing
- run targeted addon tests with the Odoo runner or pytest-odoo

## Scope

Generic — works across different Odoo projects, addon sets, and team members.
Do not assume a specific repository layout beyond standard Odoo addon conventions.

---

## Workflow (execute in order)

### Step 1 — Discover the environment

**First: check `CLAUDE.md` (or project docs) for project-specific interpreter path, config file, DB name, and addons path.** These take precedence over the fallback discovery below.

If not documented, discover manually:

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

Also add a `conftest.py` at the project root for pytest runs (guards against any remaining background threads):

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

**First: check `CLAUDE.md`/`AGENTS.md` for the project's interpreter, test config, DB name, and addons path.**

**Check pytest first:**

```bash
<interpreter> -m pytest --version
<interpreter> -c "import pytest_odoo"
```

**If pytest-odoo available:**

```bash
ODOO_RC=<test_config_file> \
PYTHONPATH=<odoo_source_root> \
<interpreter> -m pytest -x <addon>/tests/<test_file>.py \
  --odoo-config=<test_config_file> -q
```

**If pytest missing, or module name starts with a digit (`3s_*`) — use Odoo runner:**

```bash
<interpreter> <odoo-bin> -c <test_config_file> -d <db_name> \
  --test-enable --test-tags=post_install -u <module_name> --stop-after-init
```

Use `-i` instead of `-u` when the module is not yet installed.

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
- Override parent factory methods to add module-specific defaults

---

## Advanced Patterns

→ See `reference/patterns.md` for full code samples.

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

→ See `reference/errors.md` for full solutions.

| Error | Quick pointer |
|-------|--------------|
| `module 'odoo' has no attribute 'tools'` | Explicit `import odoo.tools` needed (Odoo 19 namespace pkg) |
| `pytest_odoo` crashes on startup | Patch `hasattr(odoo, "tools")` in site-packages |
| `KeyError: 'odoo.addons.<module>'` | Add `--odoo-addons-path=...` |
| `OPENERP_SERVER` warning | Switch to `ODOO_RC` |
| Module name starts with digit (`3s_*`) | Use Odoo runner, not pytest |
| Migrated v14→v19 code failures | See errors.md table |
| Test process hangs after results print | See errors.md #7 — add `conftest.py` with `os._exit(0)` (pytest) or pass `--workers=0` (Odoo runner) |
| Queue job partial success | Assert full outcome, not just no exception |
