# Overview

## Scope
Guide performance analysis and optimization for Odoo API and model code, especially ORM-heavy, query-heavy, and batch-heavy paths. Covers the full investigation stack from wall-time measurement down to query plan analysis.

## Primary artifact
A bottleneck diagnosis with a concrete measurement plan: which tool to use, what the output will show, and what to do next.

## The 4 investigation layers

```
Layer 1 — Shape    cProfile / ir.profile     CPU-bound vs DB-bound?
Layer 2 — Count    QueryTracer (existing)     which function fires the most queries?
Layer 3 — Time     QueryTracer + timing /     which query dominates wall time?
                   pg_stat_statements
Layer 4 — Plan     EXPLAIN (ANALYZE,BUFFERS)  why is that specific query slow?
```

Each layer answers a different question. Moving to the next layer only makes sense once the current layer points at a specific bottleneck.

## Key checks
- Look for searches or writes inside loops (N+1).
- Prefer batch reads and grouped computations over per-record access.
- Separate query-count problems (N+1) from single-query latency problems (missing index, bad plan).
- Check indexes before assuming query rewrite is needed.
- Distinguish cold-start (first page) from warm (paginated deep offset) behavior.

## Project-specific tooling (my_sun / MySGR v19)

| Tool | File | Notes |
|------|------|-------|
| QueryTracer (count) | `mysgr/ai_request_api/tests/test_n1_benchmark.py:57` | reusable context manager |
| QueryTracer (count) | `mysgr/ai_request_api/tests/test_list_api_bench.py:45` | copy; TODO extract to shared module |
| EXPLAIN ANALYZE helper | `mysgr/ai_request_api/tests/test_list_api_bench.py:131` | `_explain_analyze(sql, params, label)` |
| Standalone runner | `scripts/benchmark_n1.py` | no pytest; monkey-patches cursor directly |
| pg_stat_statements | postgres extension | check: `SELECT * FROM pg_stat_statements LIMIT 1;` |
| ir.profile | Odoo built-in | speedscope JSON; Settings > Technical > Profiling |

See `tooling.md` for code snippets and exact run commands.

## Frequent sibling skills
- `odoo-test` — regression tests and `assertQueryCount` once bottleneck is fixed
- `odoo-build` — implement the fix (index migration, prefetch, batch rewrite)
- `odoo-orm-modeling` — if the N+1 root cause is a field or compute design issue
