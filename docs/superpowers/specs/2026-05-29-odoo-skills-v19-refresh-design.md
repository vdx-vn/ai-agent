# Design: Odoo Skills v19 Refresh + Token Slim

**Date:** 2026-05-29  
**Author:** Claude Code  
**Status:** Approved for implementation  

## Goal (3 Criteria → 3 Chosen Levers)

1. **Match Odoo 19** → Fix stale anchors + inject distilled v19 facts
2. **Save tokens, no accuracy/reliability/speed loss** → Slim repeated boilerplate in-place, keep each SKILL.md self-contained (no extra Read round-trips)
3. **Deliverable** → Design doc + implementation plan, commit, stop for review

## Evidence of Real v19 Drift (Not Guesses)

### ORM Core Relocated
- `odoo/orm/` subpackage new in v19; core models, fields, API moved here
- Affects anchors in: odoo-orm-modeling, odoo-architecture, odoo-integration-api, odoo-performance
- **odoo/__init__.py removed** → PEP 420 namespace package (no star imports)

### Dead Source Anchors (Verified in ce-19)
- `odoo/models.py` → `odoo/orm/models.py` (311 KB)
- `odoo/fields.py` → `odoo/orm/fields.py` (88 KB) + split files (fields_relational.py, fields_numeric.py, fields_temporal.py, fields_selection.py)
- `odoo/api.py` → `odoo/api/__init__.py` (shim) + `odoo/orm/decorators.py` (real defs)
- `odoo/modules/registry.py` → `odoo/orm/registry.py` (55 KB)
- `addons/hr_expense/models/hr_expense_sheet.py` → **model removed entirely**; expenses flattened to `hr.expense` with `former_sheet_id` breadcrumb

### Doc Structure Evolution
- ~9 doc anchors now stub landing pages (169–442 bytes): finance.rst, sales.rst, hr.rst, frontend.rst, services.rst, inventory.rst, manufacturing.rst, accounting.rst, fiscal_localizations.rst
- Real content moved to subdir: `content/applications/finance/` (was finance.rst stub), `content/applications/hr/` (was hr.rst stub), etc.
- Retarget needed for accurate doc links

### View Tag Rename
- `<tree>` → `<list>` (v19 uses `<list>` exclusively in sale views, stock views)
- Not captured in any current skill

### Skill Library Baseline
- 27 skills (7 sprint-task, 9 technical-ref, 11 business-ref)
- Each has: overview.md (routing + anchors), SKILL.md (workflow + example), checklist
- **Identical boilerplate repeats** across all 27: Workflow steps 1–5, Required inputs, Guardrails (same 50–80 words, word-for-word)
- Descriptions: ~30 words each, already lean (no trim target)

---

## Four Workstreams

### WS1 — Anchor Retargeting (Accuracy Fix)

**Scope:** Walk all 27 skills' `references/overview.md`. Re-point every dead/stub anchor to live v19 path.

**Anchor map (24 fixes across 12 skill files):**

| Skill File | Anchor | Old Path | New Path | Status |
|---|---|---|---|---|
| odoo-orm-modeling/references/overview.md | models | `odoo/models.py` | `odoo/orm/models.py` (v19 ORM package) | ✓ Done |
| odoo-orm-modeling/references/overview.md | fields | `odoo/fields.py` | `odoo/orm/fields.py` (+ split: fields_relational.py, fields_numeric.py, fields_temporal.py, fields_selection.py) | ✓ Done |
| odoo-orm-modeling/references/overview.md | api | `odoo/api.py` | `odoo/api/__init__.py` (re-export shim; decorators in `odoo/orm/decorators.py`) | ✓ Done |
| odoo-build/references/overview.md | Same 3 anchors | Same fixes | Same | ✓ Done |
| odoo-architecture/references/overview.md | registry | `odoo/modules/registry.py` | `odoo/orm/registry.py` (v19; odoo/modules/registry.py removed) | ✓ Done |
| odoo-think/references/overview.md | registry | Same | Same | ✓ Done |
| odoo-plan/references/overview.md | models | Same | Same | ✓ Done |
| odoo-review/references/overview.md | models | Same | Same | ✓ Done |
| odoo-business-expenses/references/overview.md | expense-sheet | `addons/hr_expense/models/hr_expense_sheet.py` | `addons/hr_expense/models/hr_expense.py` (v19: model removed; expenses flat; see `former_sheet_id`) | ✓ Done |
| odoo-business-accounting/references/overview.md | expense-sheet | Same | Same | ✓ Done |
| odoo-business-sales/references/overview.md | finance-stub | `content/applications/finance.rst` | `content/applications/finance/` (subdirectory; real content not in stub) | Pending |
| odoo-business-purchase/references/overview.md | finance-stub | Same | Same | Pending |
| odoo-business-inventory/references/overview.md | inventory-stub | `content/applications/inventory_and_mrp/inventory.rst` | `content/applications/inventory_and_mrp/inventory/` | Pending |
| odoo-business-manufacturing/references/overview.md | manufacturing-stub | `content/applications/inventory_and_mrp/manufacturing.rst` | `content/applications/inventory_and_mrp/manufacturing/` | Pending |
| odoo-business-hr/references/overview.md | hr-stub | `content/applications/hr.rst` | `content/applications/hr/` | Pending |
| odoo-business-timesheet-project-services/references/overview.md | services-stub | `content/applications/services.rst` | `content/applications/services/` | Pending |
| odoo-view-ui/references/overview.md | frontend-stub | `content/developer/reference/frontend.rst` | `content/developer/reference/frontend/` | Pending |
| odoo-integration-api/references/overview.md | api-stub | `content/developer/reference/backend/api.rst` | `content/developer/reference/backend/api/` | Pending |

**Verification:** Each new anchor confirmed to exist in ce-19 before write.

**Outcome:** All 27 skill overview.md files point to live v19 paths, zero stale links.

---

### WS2 — Distilled v19 Facts (Accuracy + Runtime Token Save)

**Scope:** Add tight `references/v19-notes.md` section per technical/business skill with ONLY high-signal, hallucination-preventing facts.

**Facts to capture (verified in ce-19):**

1. **ORM package move:** `odoo.models`, `odoo.fields`, `odoo.api` → new `odoo.orm.*` subpackage
2. **Namespace package:** `odoo/__init__.py` removed; explicit imports required
3. **View tag rename:** `<tree>` → `<list>`
4. **Dead model:** `hr.expense.sheet` removed; expenses flat on `hr.expense` with `former_sheet_id` breadcrumb
5. **Doc structure:** endpoint docs now thin toctrees; real content in subdirectories
6. **Deprecated signatures:** (if any; to be discovered per skill domain)
7. **New fields/methods:** (if any; to be discovered per skill domain)

**Target skills (12 technical + 3 high-impact business):**
- Technical: odoo-orm-modeling, odoo-architecture, odoo-security, odoo-integration-api, odoo-performance, odoo-testing-reference, odoo-view-ui, odoo-delivery-ops, odoo-upgrade-migration, odoo-think, odoo-plan, odoo-review
- Business: odoo-business-expenses, odoo-business-hr, odoo-business-accounting

**Format:** ~25-line cap per file; structured list (Rename → [old] → [new], Deprecated → [detail], New → [detail])

**Outcome:** Agent gets v19 facts without reading 88KB source files = runtime token save.

---

### WS3 — Boilerplate Slim In-Place (Token Save)

**Scope:** Trim redundant scaffolding across 27 SKILL.md + 27 checklists + 27 examples; keep routing distinctions intact.

**Redundancy target:** Identical 50–80 word blocks (Workflow steps 1–5, Required inputs, Guardrails).

**Examples:**
- **Before (SKILL.md):**
  ```
  ## Workflow

  1. **Collect inputs:** Gather user intent, decision constraints, scope boundaries, non-negotiables
  2. **Map artifacts:** Identify which Odoo business processes, documents, and flows are in scope
  3. **Read source:** Navigate to critical code anchors, understand data models, dependencies
  4. **Synthesize:** Compare user intent with discovered capabilities, flag unknowns, build assumptions
  5. **Draft output:** Assemble all findings into coherent structured form ready for user handoff
  
  [~5 more paragraphs of identical scaffolding]
  ```
  
- **After (SKILL.md):**
  ```
  ## Workflow

  Collect intent → Map artifacts → Read source → Synthesize findings → Draft output.
  
  [Keep routing-specific context; cut generic scaffold]
  ```

**Preserve:**
- Artifact definitions (e.g., "Structured review findings" vs. "Execution plan")
- Routing rules (boundary conditions, sibling skill references)
- Routing-critical examples
- Any custom guardrails (security, performance, business logic)

**Cut:**
- Generic workflow prose (identical across all 27)
- Repeated "Required inputs" preamble (same 40 words)
- Boilerplate checklist intro/outro

**Target reduction:** 15–25% per file, zero routing-fidelity loss.

**Outcome:** Meaningful per-invocation token reduction at runtime; each file still self-contained.

---

### WS4 — Validation & Commit

**Validation:**
1. Run validator: `odoo-skills-verify`
2. Build marketplace: `odoo-skills-build`
3. Run unit tests: `python3 -m unittest discover -s tests -p 'test_*.py' -v`
4. Smoke-install check: `odoo-skills-smoke-install`

**Commit:**
- Stage all `.md` changes: `git add skills/ docs/`
- Commit with message referencing design goals:
  ```
  [IMP] Odoo 19 skill refresh: anchor accuracy + v19 facts + boilerplate slim

  WS1: Retarget 24 dead/stub anchors to v19 paths (odoo/orm package, hr_expense consolidation)
  WS2: Add distilled v19-notes sections (orms, view tag rename, namespace package)
  WS3: Trim redundant boilerplate scaffolding (15-25% reduction, zero routing loss)
  WS4: Validate with full test suite + smoke-install

  Goals: Match Odoo 19 better. Save tokens without accuracy/reliability/speed loss.
  ```

---

## Success Criteria

1. ✓ All 24 anchor fixes verified to resolve in ce-19
2. ✓ All 27 SKILL.md files remain self-contained (no new Read dependencies)
3. ✓ WS2 sections: ~25 lines each, high-signal facts only
4. ✓ WS3 boilerplate cuts: 15–25% reduction, zero routing-fidelity drift
5. ✓ Full validator pass (odoo-skills-verify)
6. ✓ Full test suite pass (95/95 tests)
7. ✓ Smoke-install succeeds
8. ✓ Clean git commit with design traceability

---

## Timeline

- **WS1:** ~20 min (doc-stub retargeting; Batch B pending)
- **WS2:** ~30 min (v19-notes injection across 15 files)
- **WS3:** ~40 min (boilerplate trim + careful routing verification)
- **WS4:** ~10 min (validate + commit)

**Total:** ~100 min before usage exhaustion.

---

## Next Steps

1. Proceed with WS1 Batch B (doc-stub retargeting) — 14 anchors across 8 skills
2. Inject WS2 v19-notes sections into technical/business skills
3. Trim WS3 boilerplate in-place across 27 files
4. Run full WS4 validation and commit
5. User review before any further work
