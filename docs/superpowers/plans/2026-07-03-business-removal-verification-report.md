# Business-skill removal — behavioral verification report

Date: 2026-07-03
Branch: `verify-odoo-19-skills`
Scope: Task 6 of the `odoo-business-*` removal plan. Behaviorally verifies the remaining
25-entry skill library (17 `odoo-*` task/technical skills + `pylint-code-review` +
7 `caveman*`/`cavecrew` utility skills) by driving a small real Odoo feature through the
task-skill pipeline (`odoo-think` → `odoo-plan` → `odoo-build` → `odoo-review` → `odoo-test`)
plus two negative/boundary routing probes, all run headless against the actual plugin via
`claude --plugin-dir .`.

## Simulated feature (fixed scenario, used verbatim in every prompt)

> In a custom addon `sale_express_shipping`, add a boolean field `express_shipping` on
> `sale.order`. When checked, automatically set `commitment_date` to tomorrow. Show the
> checkbox on the sale order form next to the payment terms. Restrict editing the field to
> Sales / Administrator. Include an automated test.

This scenario deliberately touches a *sales* entrypoint — the strongest probe that no
remaining skill or routing doc tries to hand off to the deleted `odoo-business-sales` skill.

## Method

- Transcript directory: `/tmp/claude-1000/-home-xmars-dev-vdx-vn-ai-agent/ed28c1a7-a023-4951-893f-d95504d8f367/scratchpad/skill-sim/`
  (scratch only, not committed). Note: the brief's literal Step-1 glob
  (`/tmp/claude-1000/-home-xmars-dev-vdx-vn-ai-agent/*/scratchpad`) matched seven concurrent
  session scratchpads on this machine, which is expected in a multi-agent environment; the
  glob's word-splitting produced one harmless empty stray directory
  (`.../1c2f9b06-edca-437e-980f-d5ef074194db/scratchpad ` with a trailing space in the name)
  in an unrelated session's scratch tree. It is untracked, outside the repo, and left alone
  per the no-deletion-without-permission rule. The actual simulation ran from this session's
  own scratchpad, `.../ed28c1a7-a023-4951-893f-d95504d8f367/scratchpad/skill-sim/`.
- Each pipeline step ran as a separate headless `claude --plugin-dir . -p "..."` invocation
  from repo root, forcing the target skill by name (`Use the odoo-skills:<skill> skill.`).
- Step 4 (`odoo-review`) pasted the *actual* file contents produced by step 3 (`odoo-build`),
  not a re-description.
- Step 5 (`odoo-test`) was given the scenario plus a factual summary of the files step 3 built.
- All seven `claude` invocations exited 0 with empty stderr (no skill-not-found errors, no
  crashes).

## Per-probe results

| # | Transcript | Skill forced | Contract source (`skill-inventory.json` artifact) | Result | Notes |
|---|---|---|---|---|---|
| 1 | `1-think.md` | `odoo-skills:odoo-think` | "Risk-oriented scoping brief with module map, business entrypoint, cross-app impact, and open questions." | **PASS** | Contains impacted-module map (`sale`, no bridge addons needed), explicit business entrypoint (sale order form, Payment Terms area), 5 numbered risks/unknowns (mechanism choice, "tomorrow" definition, group-vs-ACL ambiguity, `commitment_date` collision with `sale_stock`, fresh-build caveat), explicit boundary/decision framing, and a hand-off note. No implementation code present. Zero `odoo-business` mentions. |
| 2 | `2-plan.md` | `odoo-skills:odoo-plan` | "Ordered execution plan with file map, acceptance criteria, test matrix, rollout notes, and open decisions." | **PASS** (minor note) | Ordered numbered steps, explicit file-tree map (`models/`, `views/`, `security/`, `tests/`), acceptance criteria section, test matrix table, rollout notes, and an explicit open decision (UI-only vs. enforced group restriction) requiring sign-off before build. Zero `odoo-business` mentions. Minor note: the plan includes a few short illustrative code fragments (e.g. one field declaration line, one `groups=` attribute value) inline in prose to pin down the mechanism decision — these are not complete/runnable files and don't constitute the "actual code changes" artifact reserved for `odoo-build`; judged consistent with the contract, not a deviation. |
| 3 | `3-build.md` | `odoo-skills:odoo-build` | "Concrete in-scope code or configuration changes plus noted assumptions and follow-up validation needs." | **PASS** | `__manifest__.py` depends on `["sale", "sales_team"]`; `models/sale_order.py` adds `express_shipping` Boolean plus `_onchange_express_shipping` onchange **and** `create`/`write` overrides that set `commitment_date` to tomorrow (write-path enforcement, not onchange-only); `views/sale_order_views.xml` xpaths `payment_term_id position="after"` and inserts the field with a `groups="sales_team.group_sale_manager"` restriction; `tests/test_sale_express_shipping.py` is a `TransactionCase` with 4 test methods covering create, write, no-op, and onchange paths. No `<tree>` tags used anywhere (Odoo 19 convention respected — this scenario didn't need a `<list>` view either, since it's a field addition to an existing form). Zero `odoo-business` mentions. Ends with an explicit "Boundary decision" section correctly identifying composed skills (`odoo-orm-modeling`, `odoo-view-ui`, `odoo-security`) and flagging that UI-level `groups=` alone doesn't stop RPC writes — a real defect, caught by design and confirmed independently by the review step below. |
| 4 | `4-review.md` | `odoo-skills:odoo-review` | "Structured findings on an existing diff or artifact, separated into required fixes, open risks, and optional improvements." | **PASS** | Findings explicitly split into severity tiers: "High — required fix" (write() re-stamps `commitment_date` on every truthy write, not just the False→True transition), "Medium — required fix or explicit sign-off needed" (view-level `groups=` is UI-only, not ORM-enforced — the exact defect flagged by the build step), and "Low — suggested improvements" (dead loop pattern in onchange, missing regression tests). Includes an "Untested risk areas" section and a "Not a concern" section (correctly noting no ACL needed since no new model was added). Zero `odoo-business` mentions. |
| 5 | `5-test.md` | `odoo-skills:odoo-test` | "Current-change validation evidence or validation plan tied to a specific diff, addon, bug, or runtime scenario." | **PASS** | Explicit install/update command semantics (`--stop-after-init -i sale_express_shipping`, `-u sale_express_shipping`), `--test-tags` usage in the test matrix and command block, a dedicated security-check row (non-Sales/Admin write attempt) correctly marked blocked pending the review's Medium fix, and explicit composition with `odoo-local-test-harness` (cites `.claude/settings.local.json:3` `ODOO_TEST_BASE_CMD` and flags that harness base points at CE 18 vs. the "19" in the scenario framing — a reasonable and correctly-scoped observation, not a defect). Zero `odoo-business` mentions. |
| 6 | `6-negative.md` | none forced (open question: "Explain how the Odoo sales flow works from quotation to invoice.") | N/A — negative probe | **PASS** | Claude answered directly with a quotation→confirm→deliver→invoice→payment walkthrough. No skill invocation attempted for a nonexistent `odoo-business-sales`, no error text, no `odoo-business` mention anywhere in output or stderr. |
| 7 | `7-viewui.md` | `odoo-skills:odoo-view-ui` ("How do I add a banner block to the website checkout page template?") | N/A — boundary probe for the rewritten guardrail | **PASS** | Answer covers template inheritance mechanics directly (`inherit_id="website_sale.checkout"`, xpath landmark stability cautions, `position="replace"` warning, multi-step render caution, tour-test follow-up) with an explicit "Boundary decision" section that composes with `odoo-build`/`odoo-architecture` — no deferral to any removed skill. Zero `odoo-business` mentions. |

## Mechanical hard-invariant check

```
$ grep -l "odoo-business" "$SIM"/*.md && echo "FAIL: routed to removed skill" || echo "OK: no dangling routing"
OK: no dangling routing
```

Also checked stderr captured from all seven `claude` invocations (`*.err` files): all seven are
0 bytes — no crash output, no skill-resolution errors, no `odoo-business` mentions there either.

## Summary

| Metric | Result |
|---|---|
| Pipeline probes (1–5) | 5 / 5 PASS |
| Negative/boundary probes (6–7) | 2 / 2 PASS |
| Total probes | 7 / 7 PASS |
| `odoo-business` mentions across all transcripts + stderr | 0 |
| CLI invocations with non-zero exit or stderr output | 0 / 7 |
| Contract deviations requiring a code/doc fix | 0 |

No probe failed. No skill or doc file required a fix. The full pipeline correctly composed
`odoo-orm-modeling`, `odoo-view-ui`, `odoo-security`, `odoo-testing-reference`, and
`odoo-local-test-harness` guidance under the primary task skills without ever referencing a
deleted `odoo-business-*` skill, and the build step's own self-identified security gap
(UI-only group restriction) was independently confirmed and escalated to "required fix" by
the review step, and correctly gated the security test rows in the test-plan step — evidence
that the surviving skill chain reasons coherently across steps, not just per-skill in
isolation.

## Final full-gate re-run (brief Step 7)

```
$ python3 -m unittest discover -s tests -p 'test_*.py' -v
... (full suite) ... OK

$ odoo-skills-verify
✅ ... all validators passed
```

See `.superpowers/sdd/task-6-report.md` for exact command output and exit codes.
