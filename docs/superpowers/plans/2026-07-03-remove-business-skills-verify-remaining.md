# Remove odoo-business* Skills + Verify Remaining Skills Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Remove the 9 `odoo-business-*` reference skills from the plugin, scrub every reference to them, and verify the remaining odoo skills behave correctly via the full quality-gate stack plus a simulated end-to-end Odoo feature task.

**Architecture:** The skill inventory is locked in three places that must stay in sync: `skills/` directory membership, `docs/reference/skill-inventory.json` (drives `odoo-skills-verify`), and `tests/unit/test_public_skill_tree.py` (exact-set assertion). Removal is: update locks first (tests fail), delete directories (tests pass), scrub cross-references in remaining skills and docs, then run the packaging/install gates. Behavior verification is a scripted headless-Claude simulation of a small Odoo feature that exercises the task-skill pipeline (`odoo-think → odoo-plan → odoo-build → odoo-review → odoo-test`).

**Tech Stack:** Python 3 `unittest`, `tooling/` CLI entrypoints (`odoo-skills-verify`, `odoo-skills-build`, `odoo-skills-smoke-install`), Claude CLI (`claude --plugin-dir`, `claude -p`, `claude plugin validate`).

## Global Constraints

- **File deletion authorization:** The user explicitly requested removal of `odoo-business*` skills ("remove odoo-business* skills"). The ONLY deletions permitted by this plan are: the 9 directories `skills/odoo-business-sales`, `skills/odoo-business-purchase`, `skills/odoo-business-inventory`, `skills/odoo-business-manufacturing`, `skills/odoo-business-accounting`, `skills/odoo-business-hr`, `skills/odoo-business-timesheet-project-services`, `skills/odoo-business-expenses`, `skills/odoo-business-website-ecommerce`, and the test file `tests/unit/test_business_skill_contracts.py` (plus its `__pycache__` artifact, allowed per user memory). Delete NOTHING else. Use `git rm` so deletions are recoverable from git history.
- Main test command: `python3 -m unittest discover -s tests -p 'test_*.py' -v` (unittest, not pytest).
- `docs/superpowers/specs/2026-05-29-odoo-skills-v19-refresh-design.md` is a historical spec — do NOT edit it. All "no remaining references" checks must exclude `docs/superpowers/` and `.git/`.
- Do not touch the `caveman*`/`cavecrew` symlinks under `skills/` — they are intentionally tracked and listed in `REQUIRED_PUBLIC_SKILLS`.
- No unresolved `TODO`/`TBD`/`<ODOO_*>` markers may be introduced into `skills/` or `docs/reference/`.
- Work on branch `verify-odoo-19-skills`. Commit after each task. Commit messages end with `Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>`.

---

### Task 1: Update inventory locks (tests + JSON) — fail first

**Files:**
- Modify: `tests/unit/test_public_skill_tree.py:33-41`
- Modify: `docs/reference/skill-inventory.json`

**Interfaces:**
- Consumes: nothing.
- Produces: `REQUIRED_PUBLIC_SKILLS` set without business skills; `skill-inventory.json` `skills` list without the 9 `family: "business"` entries. Task 2 relies on the tree test failing with `Extra=[...9 business dirs...]` until directories are deleted.

- [ ] **Step 1: Remove the 9 business entries from the test's expected set**

In `tests/unit/test_public_skill_tree.py`, delete these 9 lines (currently lines 33–41 inside `REQUIRED_PUBLIC_SKILLS`):

```python
    "odoo-business-sales",
    "odoo-business-purchase",
    "odoo-business-inventory",
    "odoo-business-manufacturing",
    "odoo-business-accounting",
    "odoo-business-hr",
    "odoo-business-timesheet-project-services",
    "odoo-business-expenses",
    "odoo-business-website-ecommerce",
```

- [ ] **Step 2: Remove the 9 business skill objects from the inventory JSON**

In `docs/reference/skill-inventory.json`, delete each object in the `skills` array whose `name` starts with `odoo-business-` (there are exactly 9; their `family` value distinguishes them if any use `"business"`). Preserve JSON validity — check with:

```bash
python3 -c "import json; d=json.load(open('docs/reference/skill-inventory.json')); names=[s['name'] for s in d['skills']]; assert not [n for n in names if n.startswith('odoo-business-')], names; print(len(names), 'skills remain')"
```

Expected: `19 skills remain` (28 − 9).

- [ ] **Step 3: Run the tree test to verify it now fails on extras**

Run: `python3 -m unittest tests.unit.test_public_skill_tree -v`
Expected: FAIL — `test_public_skill_directories_match_exact_approved_set` reports `Extra=['odoo-business-accounting', ...]` listing all 9 business directories. This proves the lock is active.

- [ ] **Step 4: Commit**

```bash
git add tests/unit/test_public_skill_tree.py docs/reference/skill-inventory.json
git commit -m "test: drop odoo-business skills from inventory locks

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 2: Delete the business skill directories and their contract test

**Files:**
- Delete: `skills/odoo-business-sales/`, `skills/odoo-business-purchase/`, `skills/odoo-business-inventory/`, `skills/odoo-business-manufacturing/`, `skills/odoo-business-accounting/`, `skills/odoo-business-hr/`, `skills/odoo-business-timesheet-project-services/`, `skills/odoo-business-expenses/`, `skills/odoo-business-website-ecommerce/`
- Delete: `tests/unit/test_business_skill_contracts.py`

**Interfaces:**
- Consumes: failing tree test from Task 1.
- Produces: `skills/` tree with 19 odoo skills + `pylint-code-review` + caveman symlinks; test suite with no business-contract module. Tasks 3–5 assume these paths no longer exist.

- [ ] **Step 1: Remove exactly the authorized paths (user-authorized deletion — see Global Constraints)**

```bash
git rm -r skills/odoo-business-sales skills/odoo-business-purchase skills/odoo-business-inventory skills/odoo-business-manufacturing skills/odoo-business-accounting skills/odoo-business-hr skills/odoo-business-timesheet-project-services skills/odoo-business-expenses skills/odoo-business-website-ecommerce
git rm tests/unit/test_business_skill_contracts.py
rm -f tests/unit/__pycache__/test_business_skill_contracts.cpython-312.pyc
```

Do not run any other delete command. If `git rm` reports a path not found or extra untracked content inside these directories, STOP and report instead of forcing.

- [ ] **Step 2: Run the tree test to verify it passes**

Run: `python3 -m unittest tests.unit.test_public_skill_tree -v`
Expected: PASS (all tests OK).

- [ ] **Step 3: Run the full suite to surface any other test that referenced business skills**

Run: `python3 -m unittest discover -s tests -p 'test_*.py' -v`
Expected: PASS. If any test still imports or asserts business skills, fix that test in the same spirit as Task 1 (remove the business expectation, keep the rest intact) and note it in the commit message.

- [ ] **Step 4: Commit**

```bash
git add -A skills/ tests/
git commit -m "feat!: remove odoo-business reference skills

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 3: Scrub business-skill references from remaining skills (`odoo-view-ui`)

**Files:**
- Modify: `skills/odoo-view-ui/SKILL.md:38-48`
- Modify: `skills/odoo-view-ui/references/examples.md:19-23`
- Modify: `skills/odoo-view-ui/references/overview.md:39`

**Interfaces:**
- Consumes: business skills gone from tree (Task 2).
- Produces: `odoo-view-ui` self-contained on website-process questions; no `odoo-business` string anywhere under `skills/`. Task 6's simulation relies on this (no dangling handoff targets).

- [ ] **Step 1: Edit `skills/odoo-view-ui/SKILL.md`**

Replace the guardrail line (line 38):

```
- Keep customer journey or checkout process meaning with `odoo-business-website-ecommerce`; keep template, xpath, and action mechanics here.
```

with:

```
- Keep focus on template, xpath, and action mechanics; explain surrounding customer-journey behavior only as far as needed to justify the UI change.
```

Replace the hand-off bullet (line 42):

```
- If the UI question starts from website cart, checkout, portal, or public form entrypoints but the user mainly wants process meaning, compose with `odoo-business-website-ecommerce`.
```

with:

```
- If the question starts from website cart, checkout, portal, or public form entrypoints but the user mainly wants business-process meaning rather than UI structure, say the library has no dedicated business-process skill and answer the UI-mechanics portion from Odoo docs and CE source.
```

Delete the sibling bullet (line 48):

```
- `odoo-business-website-ecommerce`
```

- [ ] **Step 2: Edit `skills/odoo-view-ui/references/examples.md`**

Replace the tie-breaker rationale (line 19):

```
- Why this skill wins: The request is about UI behavior and action mechanics, so `odoo-view-ui` should win over `odoo-business-website-ecommerce`.
```

with:

```
- Why this skill wins: The request is about UI behavior and action mechanics, which is this skill's core domain.
```

Delete the nearby-skill bullet (line 23):

```
- `odoo-business-website-ecommerce`
```

- [ ] **Step 3: Edit `skills/odoo-view-ui/references/overview.md`**

Delete the frequent-sibling bullet (line 39):

```
- `odoo-business-website-ecommerce`
```

- [ ] **Step 4: Verify no business references remain under skills/**

Run: `grep -rn "odoo-business" skills/`
Expected: no output (exit code 1).

- [ ] **Step 5: Run validator layer that checks skill frontmatter/layout**

Run: `python3 -m unittest discover -s tests -p 'test_*.py' -v`
Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add skills/odoo-view-ui
git commit -m "fix: drop business-skill handoffs from odoo-view-ui

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 4: Scrub business references from reference docs and CLAUDE.md

**Files:**
- Modify: `docs/reference/trigger-matrix.md` (9 table rows at lines 31–39 + 4 boundary sections: "backend sales vs public storefront" line ~48, "UI mechanics vs public or portal customer journey" line ~49, "warehouse document vs MO or BoM" line ~50, "workforce policy vs expense claim lifecycle" line ~51)
- Modify: `docs/reference/library-manifest.md` (9 table rows at lines 29–37 + composition mention on line 14 + the "Business reference skills" group description)
- Modify: `docs/reference/shared-taxonomy.md` (routing sentence at line ~34; keep the "UI mechanics vs website business flow" concept but re-point it)
- Modify: `docs/reference/evaluation-harness.md` (7 references at lines ~43–64)
- Modify: `CLAUDE.md` ("Skill library design" section — the business reference skills bullet)

**Interfaces:**
- Consumes: final 19-skill inventory from Tasks 1–2.
- Produces: docs describing a two-group library (task skills + technical reference skills). Repo-wide check `grep -rn "odoo-business" --include='*' --exclude-dir=.git --exclude-dir=superpowers .` must return nothing.

- [ ] **Step 1: `docs/reference/trigger-matrix.md`**

Delete the 9 `| odoo-business-* |` table rows. For each boundary section that pits a technical skill against a business skill, rewrite the tie-breaker so the technical skill is the resolution and the business side is described as out-of-library. Pattern (apply to all 4 sections):

Before (example, "UI mechanics vs public or portal customer journey"):
> Mixed prompts route by primary requested output... use `odoo-business-website-ecommerce` for journey meaning, `odoo-view-ui` for template/xpath/action structure.

After:
> Mixed prompts route by primary requested output. Template, view, action, xpath, or OWL structure goes to `odoo-view-ui`. Pure customer-journey process explanation has no dedicated skill in this library; answer from Odoo docs and CE source without invoking a business skill.

Boundary sections that only compare two business skills (e.g., "warehouse document vs MO or BoM", "workforce policy vs expense claim lifecycle") should be deleted whole — both sides are gone.

- [ ] **Step 2: `docs/reference/library-manifest.md`**

Delete the 9 business rows (lines 29–37). On line 14, remove `odoo-business-website-ecommerce` from the composition list, leaving `odoo-build`, `odoo-architecture`. Update the library-overview prose: the library now has two groups (sprint task skills, technical reference skills); delete the "Business reference skills" group description.

- [ ] **Step 3: `docs/reference/shared-taxonomy.md`**

In the "UI mechanics vs website business flow" section (line ~34), replace:

```
Mixed website prompts route by primary requested output. If the user asks how the customer journey behaves, use `odoo-business-website-ecommerce`. If the user asks how a template, view, action, xpath, or OWL behavior should be structured, use `odoo-view-ui`.
```

with:

```
Mixed website prompts route by primary requested output. If the user asks how a template, view, action, xpath, or OWL behavior should be structured, use `odoo-view-ui`. Pure customer-journey process questions have no dedicated skill; answer from Odoo docs and CE source.
```

Keep the business-entrypoint vocabulary bullets (HR, Expenses, etc.) only if other docs still reference them; otherwise delete the ones that existed solely to disambiguate between two business skills.

- [ ] **Step 4: `docs/reference/evaluation-harness.md`**

Delete or rewrite the 7 evaluation cases whose expected skill is an `odoo-business-*` skill (lines ~43–64). If a case tests a boundary between a technical skill and a business skill, keep the case but change the expected outcome to the technical skill (mirroring Step 1's rewrites). If a case only tests business-vs-business routing, delete it.

- [ ] **Step 5: `CLAUDE.md`**

In "Skill library design", replace:

```
Public skills split into three groups:
```

with:

```
Public skills split into two groups:
```

and delete the bullet:

```
- business reference skills: sales, purchase, inventory, manufacturing, accounting, HR, timesheets/services, expenses, website/ecommerce
```

- [ ] **Step 6: Repo-wide reference check**

Run: `grep -rn "odoo-business" --exclude-dir=.git --exclude-dir=superpowers . | grep -v docs/superpowers/`
Expected: no output. (Historical spec under `docs/superpowers/specs/` is intentionally excluded and untouched.)

- [ ] **Step 7: Run full test suite**

Run: `python3 -m unittest discover -s tests -p 'test_*.py' -v`
Expected: PASS.

- [ ] **Step 8: Commit**

```bash
git add docs/reference CLAUDE.md
git commit -m "docs: remove business-skill routing from reference docs

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 5: Run packaging and install quality gates

**Files:**
- No source edits expected. Regenerates `dist/marketplace` (build output, not committed).

**Interfaces:**
- Consumes: cleaned tree from Tasks 1–4.
- Produces: proof the 19-skill plugin validates, builds, and installs. Task 6 requires this to pass first.

- [ ] **Step 1: Ensure tooling installed**

Run: `python3 -m pip install -e .`
Expected: exits 0.

- [ ] **Step 2: Verify**

Run: `odoo-skills-verify`
Expected: exits 0, no missing-skill or marker errors. If it complains about a skill listed in `skill-inventory.json` but missing on disk (or vice versa), the Task 1/2 sync is wrong — fix inventory JSON, not the validator.

- [ ] **Step 3: Build runtime bundle**

Run: `odoo-skills-build`
Expected: exits 0. Then confirm no business skill shipped:

```bash
ls dist/marketplace/*/skills/ 2>/dev/null || find dist/marketplace -maxdepth 3 -type d -name 'odoo-*' | sort
grep -rn "odoo-business" dist/marketplace && echo "FAIL: business refs in bundle" || echo "OK"
```

Expected: 19 odoo skill dirs, `OK`.

- [ ] **Step 4: Smoke install**

Run: `odoo-skills-smoke-install`
Expected: exits 0 (runs `claude plugin validate`, `marketplace add`, `plugin install`, `plugin list --json` in a temp HOME).

- [ ] **Step 5: Direct CLI validation**

Run: `claude plugin validate . && claude plugin validate dist/marketplace`
Expected: both report valid.

- [ ] **Step 6: Commit (only if any file changed; otherwise skip)**

```bash
git status --short
# if clean, no commit needed for this task
```

---

### Task 6: Behavior verification — simulated Odoo feature task through the skill pipeline

**Files:**
- Create: `docs/superpowers/plans/2026-07-03-business-removal-verification-report.md` (results report)
- Scratch workspace (not committed): `/tmp/claude-1000/-home-xmars-dev-vdx-vn-ai-agent/*/scratchpad/skill-sim/` — simulation transcripts

**Interfaces:**
- Consumes: passing gates from Task 5; plugin loadable via `claude --plugin-dir .`.
- Produces: written verification report with pass/fail per skill contract. Each skill's expected artifact comes from `docs/reference/skill-inventory.json` (`artifact` field).

**Simulated feature (fixed scenario for all prompts):**
> "In a custom addon `sale_express_shipping`, add a boolean field `express_shipping` on `sale.order`. When checked, automatically set `commitment_date` to tomorrow. Show the checkbox on the sale order form next to the payment terms. Restrict editing the field to Sales / Administrator. Include an automated test."

This scenario deliberately touches a *sales* entrypoint — the strongest probe that no remaining skill or routing doc tries to hand off to the deleted `odoo-business-sales`.

- [ ] **Step 1: Prepare transcript directory**

```bash
SIM=/tmp/claude-1000/-home-xmars-dev-vdx-vn-ai-agent/*/scratchpad
SIM=$(echo $SIM)/skill-sim && mkdir -p "$SIM" && echo "$SIM"
```

- [ ] **Step 2: Run the five pipeline prompts headless**

Each command loads the plugin from the repo and forces one skill. Run from repo root:

```bash
claude --plugin-dir . -p "Use the odoo-skills:odoo-think skill. Scope this request before any planning: <scenario text above>" > "$SIM/1-think.md"
claude --plugin-dir . -p "Use the odoo-skills:odoo-plan skill. Produce an execution plan for: <scenario text above>" > "$SIM/2-plan.md"
claude --plugin-dir . -p "Use the odoo-skills:odoo-build skill. Write the addon files (manifest, model, view XML, security, test) for: <scenario text above>. Output file contents inline; do not write to disk." > "$SIM/3-build.md"
claude --plugin-dir . -p "Use the odoo-skills:odoo-review skill. Review this implementation for architecture fit, correctness, and risk: <paste the file contents produced in 3-build.md>" > "$SIM/4-review.md"
claude --plugin-dir . -p "Use the odoo-skills:odoo-test skill. Produce a validation plan (install/update, workflow, security, performance checks) for: <scenario + summary of built files>" > "$SIM/5-test.md"
```

(Substitute `<scenario text above>` with the full scenario paragraph verbatim; for step 4 paste the actual build output.)

- [ ] **Step 3: Check each transcript against its skill contract**

For each output, verify against the `artifact` field in `docs/reference/skill-inventory.json`:

| Transcript | Must contain | Must NOT contain |
|---|---|---|
| `1-think.md` | impacted modules (`sale`), business entrypoint, risks/unknowns, decision framing; no code | implementation code; `odoo-business` |
| `2-plan.md` | ordered steps, file map (`models/`, `views/`, `security/`, `tests/`), acceptance criteria, test strategy | actual code changes; `odoo-business` |
| `3-build.md` | `__manifest__.py` depending on `sale`, model with `express_shipping` Boolean + onchange/compute or write-hook setting `commitment_date`, form-view xpath near `payment_term_id`, `ir.model.access` / group restriction, `TransactionCase` test | `<tree>` view tags (Odoo 19 uses `<list>`); `odoo-business` |
| `4-review.md` | findings split into required fixes / risks / optional improvements | `odoo-business` |
| `5-test.md` | install/update command semantics, `--test-tags` usage, security check, references local-test-harness composition where relevant | `odoo-business` |

Mechanical check for the hard invariant:

```bash
grep -l "odoo-business" "$SIM"/*.md && echo "FAIL: routed to removed skill" || echo "OK: no dangling routing"
```

Expected: `OK: no dangling routing`.

- [ ] **Step 4: Negative routing probe (deleted-skill territory)**

```bash
claude --plugin-dir . -p "Explain how the Odoo sales flow works from quotation to invoice." > "$SIM/6-negative.md"
grep -n "odoo-business" "$SIM/6-negative.md" && echo "FAIL" || echo "OK"
```

Expected: `OK` — Claude answers directly (or from Odoo docs) without attempting to invoke a nonexistent `odoo-business-sales` skill, and no error about a missing skill appears.

- [ ] **Step 5: Boundary probe for the rewritten odoo-view-ui guardrail**

```bash
claude --plugin-dir . -p "Use the odoo-skills:odoo-view-ui skill. How do I add a banner block to the website checkout page template?" > "$SIM/7-viewui.md"
grep -n "odoo-business" "$SIM/7-viewui.md" && echo "FAIL" || echo "OK"
```

Expected: `OK`, and the answer covers template/xpath mechanics without deferring to a removed skill.

- [ ] **Step 6: Write the verification report**

Create `docs/superpowers/plans/2026-07-03-business-removal-verification-report.md` with: scenario text, one row per probe (transcript file, contract checks passed/failed, notes), the mechanical grep results, and any contract deviations found. If any probe FAILS, fix the offending skill/doc, re-run that probe, and record both runs.

- [ ] **Step 7: Final full-gate re-run**

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
odoo-skills-verify
```

Expected: both pass.

- [ ] **Step 8: Commit**

```bash
git add docs/superpowers/plans/2026-07-03-business-removal-verification-report.md
git commit -m "docs: add business-removal skill verification report

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

## Self-Review Notes

- Spec coverage: removal (Tasks 1–2), reference scrub (Tasks 3–4), remaining-skill verification (Tasks 5–6), simulated feature test plan (Task 6). Covered.
- All deletions enumerated verbatim in Global Constraints and Task 2 Step 1; nothing else deleted.
- Inventory count consistency: 28 tracked skill entries − 9 business = 19 odoo skills; `pylint-code-review` is inside those 19? No — inventory JSON has 28 entries total including `pylint-code-review` and harness skills; Task 1 Step 2's assertion checks only that zero `odoo-business-` names remain and prints the count — if the printed count differs from 19, trust the zero-business assertion and record the actual count in the commit message.
- Line numbers cited (e.g., `SKILL.md:38-48`) are anchors from the current tree; if drift occurred, match on the quoted text, which is exact.
