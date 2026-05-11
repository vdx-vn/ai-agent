# Performance Investigation Checklist

## Intake
- [ ] Confirm the request is performance diagnosis or measurement design (not generic ORM semantics).
- [ ] Identify the API endpoint, cron method, or model function under investigation.
- [ ] Identify what signal the user already has: timing complaint, query count, slow log, load test result.
- [ ] Check if an existing bench test already covers this path (see `tooling.md` file table).

## 4-layer decision tree

Work top-to-bottom. Stop at the layer that identifies the bottleneck.

### Layer 1 — Shape (CPU vs DB)
- [ ] Has the user already split CPU time from DB time? If not, prescribe cProfile or ir.profile first.
- [ ] If DB time dominates → proceed to Layer 2.
- [ ] If Python time dominates → look for algorithmic issues (nested loops, redundant recomputation).

### Layer 2 — Count (N+1 detection)
- [ ] Does the user have QueryTracer count output? If not, prescribe QueryTracer (existing in test files).
- [ ] Review by-function and by-chain output for a single function appearing many times.
- [ ] N+1 fix patterns:
  - `search([id=x])` in loop → `self.browse(ids)` outside loop
  - computed field accessed per-record → ensure `@api.depends`, let ORM batch
  - M2O/O2M read per record → `records.fetch([field])` before loop
  - permission check per record → cache by shared key (root_request_id, etc.)
- [ ] If count is low (< ~20 for a page render) → proceed to Layer 3.

### Layer 3 — Time (which query dominates)
- [ ] Does the user have per-query timing? If not, prescribe the QueryTracer timing extension (see `tooling.md`).
- [ ] Or prescribe pg_stat_statements if measuring across many calls / load test.
- [ ] Identify the top-1 or top-3 queries by elapsed ms.
- [ ] If one query is clearly dominant → proceed to Layer 4.

### Layer 4 — Plan (why is that query slow)
- [ ] Run `EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)` on the identified query.
- [ ] Use `_explain_analyze()` helper from `test_list_api_bench.py:131` when in a test context.
- [ ] Check for: Seq Scan on large table, bad row estimates, cold buffer reads, nested loop over many rows.
- [ ] Recommend: index addition, partial index, ANALYZE table, or query rewrite.

## Output checklist
- [ ] Name the bottleneck layer (CPU / count / time / plan).
- [ ] Prescribe the exact tool with a code snippet or command from `tooling.md`.
- [ ] State what the output will show and how to interpret it.
- [ ] Name the next layer to investigate if the tool is inconclusive.
- [ ] Name any existing bench test that already covers this path.
- [ ] State boundary: what `odoo-build` or `odoo-test` owns after diagnosis.

## Production readiness
- [ ] EXPLAIN ANALYZE is safe for SELECT but executes the query — warn if it's a write.
- [ ] pg_stat_statements resets affect all connections — note this is a shared operation.
- [ ] QueryTracer patches the cursor class — always used inside a test transaction that rolls back.
