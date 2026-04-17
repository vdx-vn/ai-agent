# Known Errors & Solutions (Odoo 19)

## 1. `AttributeError: module 'odoo' has no attribute 'tools'`

Odoo 19 dropped `odoo/__init__.py` — it is a pure namespace package. Submodules are NOT auto-loaded.

**Fix:** Explicitly import before use: `import odoo.tools`  
Also ensure `PYTHONPATH` includes the Odoo source root (not the wrapper directory).

---

## 2. `pytest_odoo` crashes on Odoo 19

`pytest_odoo` uses `if hasattr(odoo, "tools"):` which always returns `False`.

**Fix:** Patch `site-packages/pytest_odoo.py`:

```python
# Change:
if hasattr(odoo, "tools"):
# To:
import odoo.tools
if True:
```

---

## 3. `KeyError: 'odoo.addons.<module>'`

Custom addons directory not registered in `odoo.addons` namespace.

**Fix:** Add `--odoo-addons-path=/path/to/your/addons`

---

## 4. `OPENERP_SERVER` deprecated

Use `ODOO_RC` instead. The old variable still works but emits a deprecation warning.

---

## 5. Module name starts with a digit (e.g. `3s_mobile_app_api`)

Python rejects it as an invalid identifier — pytest-odoo import fails before any test executes.

**Fix:** Use the standard Odoo runner only for these modules:

```bash
python odoo-bin -c odoo.conf -d <db> \
  --test-enable --test-tags=post_install -u 3s_module_name --stop-after-init
```

---

## 6. Migrated code failures (v14 → v19)

| Error | Fix |
|-------|-----|
| `_sql_constraints` attribute | Replace with `models.Constraint(...)` |
| `name_get()` called | Use `display_name` or `_compute_display_name` |
| `self.clear_caches()` | Replace with `self.env.invalidate_all()` |
| `request.jsonrequest` | Use `request.params.get('key')` |
| `request.env.uid = ...` | Use `request.env(user=user_id)` |

---

## 7. Test process hangs after results print

Pytest (or the Odoo runner) prints all results but never exits.

**Root cause:** `odoo.service.server.start()` (called by pytest-odoo) spawns non-daemon background threads — queue_job poller, bus, cron — that block Python's clean shutdown. `workers = N` (N > 0) also spawns worker subprocesses that outlive the test session.

### Fix A — pytest: add `conftest.py` at project root

```python
# conftest.py
import os
import pytest

@pytest.fixture(scope='session', autouse=True)
def _force_exit_after_session(request):
    """Hard-exit after session so Odoo background threads don't block pytest."""
    yield
    os._exit(0)
```

`os._exit(0)` bypasses Python cleanup intentionally — the threads cannot be joined cleanly. The DB transaction is already rolled back by `TransactionCase` before this runs.

### Fix B — Odoo runner: override workers to 0

`workers = 2` in `odoo_config` spawns subprocesses that never stop after `--stop-after-init`.

```bash
python odoo-bin -c odoo.conf -d <db> \
  --test-enable --test-tags=post_install -u <module> --stop-after-init \
  --workers=0
```

### Fix C — remove queue_job from server_wide_modules during tests

If `queue_job` is in `server_wide_modules`, its polling thread starts at server boot and never terminates. Either use Fix A/B, or pass `--server-wide-modules=web` when running tests.

---

## 8. Queue job partial success

Batch operations using `env.cr.savepoint()` only roll back the current record on failure — not the whole batch.

Always assert the full expected outcome, not just absence of exceptions.
