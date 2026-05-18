# Examples

## Positive triggers

1. "The list API with group_parent=True takes 3 seconds on page 10. I need to understand where the time is going."
   - Expected: use `odoo-performance`. Layer 3 investigation — QueryTracer timing extension or pg_stat_statements.

2. "I ran QueryTracer on get_request_child_details and got 400 queries. Which function is responsible?"
   - Expected: use `odoo-performance`. User is at Layer 2 — read the by-function table, find the N+1 caller.

3. "I want to add a benchmark test for the new waiting-rate API so I can catch query regressions."
   - Expected: use `odoo-performance` (design the harness) + compose with `odoo-test` (write the test).

4. "The cron job was fine in v14 but is slow in v19. I'm checking with ir.cron + ir.profile but I can't see which query is slow."
   - Expected: use `odoo-performance`. Prescribe QueryTracer timing extension (Layer 3) + EXPLAIN ANALYZE (Layer 4).

5. "How do I check SQL that a function runs without going to the odoo log?"
   - Expected: use `odoo-performance`. Two options: QueryTracer timing captures SQL text inline; pg_stat_statements accumulates stats without log access.

6. "What's the fastest way to find the dominant query in a slow Odoo API?"
   - Expected: use `odoo-performance`. 4-layer decision tree: cProfile → QueryTracer count → QueryTracer time → EXPLAIN ANALYZE.

## Negative triggers

1. "How does `@api.depends` batching work for Many2one fields?"
   - Expected: do not use `odoo-performance` → `odoo-orm-modeling`.

2. "Which addon should own the permission cache model?"
   - Expected: do not use `odoo-performance` → `odoo-architecture`.

3. "Run the existing benchmark tests for the list API and show me the output."
   - Expected: do not use `odoo-performance` (execution only) → `odoo-test` or direct execution.

## Tie-breakers

- Prompt: "Why is this batch posting action slow and how should we measure it?"
  - Why this skill wins: hotspot diagnosis + measurement design is the primary output.

- Prompt: "I found a slow query in EXPLAIN ANALYZE, now write the index migration."
  - Why `odoo-build` wins: implementation is the primary output; `odoo-performance` may advise on the index design but `odoo-build` owns the artifact.

- Prompt: "Add assertQueryCount to the new subtask API test."
  - Why `odoo-test` wins: the primary output is a test artifact. `odoo-performance` advises on the query budget.
