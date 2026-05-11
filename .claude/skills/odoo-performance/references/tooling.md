# Odoo Performance Tooling Reference

Project-specific paths and patterns for the `my_sun` (MySGR v19) repo.

---

## Run command (pytest-odoo)

```
ODOO_RC=/home/charlie/vdx/my_sun/odoo_config_test PYTHONPATH=/home/charlie/vdx/source_odoo/odoo /home/charlie/.pyenv/versions/odoo14/my_sun/bin/python -m pytest <test_file> --odoo-config=odoo_config_test -s --tb=short
```

---

## Layer 1 — Shape: CPU-bound vs DB-bound

### cProfile (in pytest)

```python
import cProfile, pstats, io

def test_my_api_profile(self):
    pr = cProfile.Profile()
    pr.enable()
    self._call_api()
    pr.disable()
    s = io.StringIO()
    pstats.Stats(pr, stream=s).sort_stats('cumulative').print_stats(30)
    print(s.getvalue())
```

**What it shows:** Top Python functions by cumulative time. If DB-heavy code dominates, most time lands in `execute()` → move to Layer 3. If Python functions dominate, fix the algorithm.

### ir.profile (flame graph)

From a test or cron context:
```python
from odoo.tools.profiler import Profiler
with Profiler():
    self.env['request.request'].get_data_for_list_api(...)
```

View at: `Settings > Technical > Profiling` or upload the JSON to speedscope.app.

---

## Layer 2 — Query count by function (N+1 detection)

### QueryTracer (existing)

Files:
- `mysgr/ai_request_api/tests/test_n1_benchmark.py:57`
- `mysgr/ai_request_api/tests/test_list_api_bench.py:45`

```python
with QueryTracer(env) as t:
    do_work()
t.report(label='my function')
# t.total = total query count
```

Output: 3 tables — by file, by function (`file:lineno: fn()`), by call chain (last 3 frames).

**Interpretation:**
- Same function appearing hundreds of times → N+1, add batch prefetch or move search outside loop.
- Same chain appearing many times → outer loop is the driver.

---

## Layer 3 — Query time (which SQL dominates wall time)

### Extend QueryTracer with timing

Add these fields and wrap `orig()` with `time.perf_counter()`:

```python
class QueryTracer:
    def __init__(self, env, top_n=20, slow_threshold_ms=50):
        ...
        self._slow: list[tuple[float, str]] = []
        self.total_db_ms = 0.0
        self.slow_threshold_ms = slow_threshold_ms

    # inside _tracked():
    t0 = time.perf_counter()
    result = orig(self_cr, query, params, log_exceptions)
    ms = (time.perf_counter() - t0) * 1000
    tracer.total_db_ms += ms
    if ms >= tracer.slow_threshold_ms:
        tracer._slow.append((ms, str(query)[:400]))
    # ... existing attribution code unchanged ...

    # in report():
    print(f'\nTotal DB time: {self.total_db_ms:.1f} ms')
    if self._slow:
        print(f'\n--- Slow queries (>{self.slow_threshold_ms}ms) ---')
        for ms, sql in sorted(self._slow, reverse=True):
            print(f'  {ms:7.1f}ms  {sql[:120]}')
```

**What it adds:** `Total DB time` aggregate + list of slow queries with SQL text. No log access needed.

### pg_stat_statements (aggregate across many calls)

Check if enabled:
```sql
SELECT * FROM pg_stat_statements LIMIT 1;
```

Reset + measure:
```bash
psql -p 5434 -U charlie mysgr_v19 -c "SELECT pg_stat_statements_reset();"
# trigger the API (cron, k6, or pytest)
psql -p 5434 -U charlie mysgr_v19 -c "SELECT query, calls, total_exec_time, mean_exec_time, rows FROM pg_stat_statements ORDER BY total_exec_time DESC LIMIT 20;"
```

**What it shows:** Aggregated over all calls. Finds queries that are individually fast but called 1000× (N+1) vs genuinely slow single queries. Parameters normalized to `$1`, `$2`.

---

## Layer 4 — Plan: why is a specific query slow

### EXPLAIN ANALYZE via cursor (existing helper)

```python
# Already exists in test_list_api_bench.py:131
def _explain_analyze(self, sql, params, label):
    cr = self.env.cr
    t = time.perf_counter()
    cr.execute('EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT) ' + sql, params)
    plan = '\n'.join(r[0] for r in cr.fetchall())
    ms = (time.perf_counter() - t) * 1000
    return ms, f'\n--- EXPLAIN ANALYZE: {label} ---\n{plan}\n'
```

**Safety:** EXPLAIN ANALYZE executes the query. Safe for SELECT. Skip for INSERT/UPDATE.

**What to look for in the plan:**
- `Seq Scan` on a large table → missing or unused index
- `rows=1 (actual rows=50000)` → bad planner estimate, trigger ANALYZE or add statistics
- `Buffers: shared hit=0 read=N` → cold cache; if always cold, check index usage
- `Nested Loop` over many rows → may need `Hash Join` via join order hint or intermediate CTE

### psql EXPLAIN (outside test, no log)

```bash
psql -p 5434 -U charlie mysgr_v19 -c "EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT) SELECT ..."
```

---

## Optimization: stored filter field + index for large tables

When a table is large (100k+ rows) and a WHERE clause combines multiple conditions, even individual column indexes may not help — the planner may fall back to a seq scan or expensive bitmap AND.

**Pattern:** merge the filter conditions into a single stored computed field; index that field.

### When to use

- The same multi-condition WHERE (`state = 'x' AND type_id = y AND active = True`) appears in hot paths (list API, cron, domain search).
- `EXPLAIN ANALYZE` shows `Seq Scan` or a slow `Bitmap Heap Scan` despite individual indexes existing.
- The combined selectivity is high (the stored value is `True` for a small minority of rows).

### Odoo implementation

```python
# models/request_request.py

class RequestRequest(models.Model):
    _name = 'request.request'

    # existing fields: state, type_id, active …

    is_open_internal = fields.Boolean(
        compute='_compute_is_open_internal',
        store=True,
        index=True,           # creates a btree index automatically
        compute_sudo=True,
    )

    @api.depends('state', 'type_id.is_internal', 'active')
    def _compute_is_open_internal(self):
        for rec in self:
            rec.is_open_internal = (
                rec.active
                and rec.state == 'open'
                and rec.type_id.is_internal
            )
```

The `store=True` + `index=True` combination:
1. persists the merged value in a DB column on every write
2. creates a B-tree index on that column automatically (Odoo `_auto_init`)

### Rewrite the domain

```python
# Before (multi-condition, potentially slow)
domain = [('state', '=', 'open'), ('type_id.is_internal', '=', True), ('active', '=', True)]

# After (single indexed column)
domain = [('is_open_internal', '=', True)]
```

### Caveats

- The stored field must be recomputed whenever any dependency changes; ensure all `@api.depends` paths are complete or the field will be stale.
- Use `compute_sudo=True` only when dependency fields are readable by all users.
- For very high write rates, the recompute overhead may outweigh the read gain — measure with `QueryTracer` before and after.
- Partial indexes (PostgreSQL-only, via raw SQL migration) are an alternative: `CREATE INDEX … WHERE state = 'open' AND active = true`. Use when you cannot or do not want to add a model field. Add via a `post_init_hook` or `_auto_init` override.

### Verify the index is used

```bash
psql -p 5434 -U charlie mysgr_v19 -c "EXPLAIN (ANALYZE, BUFFERS) SELECT id FROM request_request WHERE is_open_internal = true LIMIT 100;"
# Expect: Index Scan using request_request_is_open_internal_index
```

---

## Existing benchmark test files

| File | What it benchmarks | Key class/method |
|------|--------------------|-----------------|
| `mysgr/ai_request_api/tests/test_n1_benchmark.py` | `get_request_child_details()` on 138-child request | `QueryTracer`, `TestN1Benchmark` |
| `mysgr/ai_request_api/tests/test_list_api_bench.py` | `get_data_for_list_api()` with group_parent=True | `QueryTracer`, `_explain_analyze()` |
| `mysgr/ai_request_api/tests/test_subtasks_perf.py` | `get_request_subtasks()` prefetch batch | call-count assertions |
| `mysgr/ai_request_rating/tests/test_waiting_rate_api.py` | `get_data_for_waiting_rate_list_api()` | `assertQueryCount` |
| `scripts/benchmark_n1.py` | standalone monkey-patch runner | no pytest needed |

---

## Quick decision: which tool to reach for

```
Slow API reported
  → is it CPU or DB?
      cProfile or ir.profile  ──► mostly Python?  → fix algorithm
                              ──► mostly execute()?  ↓
  → how many queries?
      QueryTracer count  ──► many queries from one fn?  → N+1, fix with prefetch/batch
                         ──► few queries?  ↓
  → which query is slowest?
      QueryTracer + timing  ──► one query >> others?  → EXPLAIN ANALYZE
      pg_stat_statements    ──► one normalized SQL >> others?  → EXPLAIN ANALYZE
  → why is that query slow?
      EXPLAIN (ANALYZE, BUFFERS)  → seq scan? add index. bad estimate? ANALYZE table.
```
