---
name: odoo-performance
description: "Guide Odoo performance analysis: batching, query count, complexity, indexing, profiler usage, and cache or prefetch patterns. Use when the primary question is hotspot diagnosis, slow API investigation, query-count regression, N+1 detection, EXPLAIN ANALYZE interpretation, benchmark harness design, or scaling behavior. Trigger for any question about why an Odoo function or endpoint is slow, how many queries it fires, which SQL dominates the wall time, or how to measure or prevent performance regressions."
---

# Purpose
Guide performance investigation for Odoo API and model code. Produce a concrete measurement plan, identify the bottleneck layer (Python CPU vs DB query count vs DB query time), and recommend the right tool for each phase.

# Primary routing rule
Use this skill only when the primary requested output is performance diagnosis, measurement design, or optimization guidance. If the user wants to *implement* a fix after diagnosis, compose with `odoo-build`. If they want a regression test, compose with `odoo-test`.

# Use this skill when
- investigating why a specific API or cron job is slow
- designing a benchmark harness for an Odoo endpoint
- choosing between QueryTracer, cProfile, ir.profile, or pg_stat_statements
- identifying N+1 patterns or dominant query times
- reading or extending existing bench tests (`test_n1_benchmark.py`, `test_list_api_bench.py`)
- deciding when EXPLAIN ANALYZE is needed and how to run it inline
- deciding when to denormalize multi-condition WHERE clauses into a stored indexed field

# Do not use this skill when
- the primary output is generic ORM field semantics → `odoo-orm-modeling`
- the task is a release checklist or code review → `odoo-ship` / `odoo-review`
- the request is pure business-flow explanation

# Workflow (execute in order)

## Step 1 — Identify the bottleneck layer

Ask: is this CPU-bound or DB-bound? Pick the tool that answers that question first.

| Question | Tool | Where |
|----------|------|--------|
| Is it CPU or DB? | `cProfile` or `ir.profile` flame graph | pytest or Settings UI |
| Which function fires the most queries? | `QueryTracer` (count) | `test_n1_benchmark.py` or `test_list_api_bench.py` |
| Which query dominates wall time? | `QueryTracer` + timing extension | extend existing tracer |
| Which normalized SQL accumulates most time? | `pg_stat_statements` | psql direct query |
| Why is a specific query slow? | `EXPLAIN (ANALYZE, BUFFERS)` | inline via cursor |

Read `references/tooling.md` for implementation patterns and run commands for each tool.

## Step 2 — Match tool to question

Use the 4-layer decision tree in `references/checklist.md` to decide which layer the user is at and which tool to prescribe.

## Step 3 — Produce output

Return:
- bottleneck hypothesis (CPU / count / time / plan)
- tool recommendation with exact code pattern or command
- what the output will show and how to interpret it
- next layer to investigate if the first tool is inconclusive
- boundary decision

# Output contract
- bottleneck layer (CPU / query count / query time / plan)
- tool recommendation with code snippet or command
- measurement or profiler plan
- next steps if inconclusive
- boundary decision with primary skill and composed siblings

# Guardrails
- Never recommend "add a log line" as a performance measurement strategy.
- Always separate N+1 count issues from single-query latency issues — they have different fixes.
- If the user already has QueryTracer output showing counts, push to the timing layer, not back to count.
- Anchor recommendations to existing project infrastructure before suggesting new tooling.
- When EXPLAIN ANALYZE shows `Seq Scan` on a large table with a multi-condition WHERE, check whether a stored indexed field would be more appropriate than adding individual column indexes — see `references/tooling.md` → "stored filter field + index".

# Compose with sibling skills
- `odoo-test` — to turn a benchmark finding into a regression test with `assertQueryCount`
- `odoo-build` — to implement the fix after the bottleneck is identified
- `odoo-orm-modeling` — if N+1 root cause is a field or compute design issue

# References
- Read `references/tooling.md` for all tool patterns, code snippets, and run commands.
- Read `references/checklist.md` for the 4-layer decision tree and intake checklist.
- Read `references/examples.md` for trigger and boundary examples.
