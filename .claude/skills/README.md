# Odoo Skills Library

Claude Code skill library for Odoo <ODOO_MAJOR_VERSION> work. Skills are split into sprint task skills, technical reference skills, and business reference skills so routing stays narrow and production-safe.

Repos used by these skills:
- Docs: `<ODOO_DOCS_ROOT>`
- Source: `<ODOO_SOURCE_ROOT>`

## Path placeholders
- See `odoo-paths.md` for shared setup and usage rules.
- Set `<ODOO_DOCS_ROOT>` to your local clone of the Odoo documentation repo.
- Set `<ODOO_SOURCE_ROOT>` to your local clone of the Odoo source repo.
- Set `<ODOO_SERIES>` / `<ODOO_MAJOR_VERSION>` to the Odoo version you are targeting.
- Paths shown inside skills are relative to these placeholders unless explicitly noted otherwise.
- To materialize one project copy automatically, run `python3 .claude/skills/scripts/materialize_odoo_skill_paths.py --docs-root /path/to/odoo/documentation --source-root /path/to/odoo/source`.
- The materializer will auto-detect version from git branch or repo path when possible; otherwise pass `--version 18.0` or similar.
- Project hooks can suggest this command automatically when you start a new Odoo project or ask to set one up.

## Artifact-first routing
- Risks, impact, unknowns → `odoo-think`
- Ordered implementation steps and acceptance criteria → `odoo-plan`
- Code or config changes → `odoo-build`
- Findings on an existing diff or artifact → `odoo-review`
- Validation evidence for a concrete change → `odoo-test`
- Go or no-go release readiness and rollout sequencing → `odoo-ship`
- Retrospective and lessons learned → `odoo-reflect`
- Engineering rule or pattern questions → matching technical reference skill
- Business process meaning and cross-app flow → matching business reference skill

## Production guardrails
- Do not let one skill become a general Odoo catch-all.
- Anchor functional meaning to Odoo <ODOO_MAJOR_VERSION> docs and implementation truth to Odoo CE <ODOO_MAJOR_VERSION> source.
- Use entrypoints to break ties between adjacent business skills.
- Use requested output artifact to break ties between adjacent task skills.
- If a prompt mixes multiple asks, declare the primary skill and compose in order.

## Common composition recipes
- `odoo-think` → `odoo-plan` → `odoo-build` → `odoo-test` → `odoo-review` → `odoo-ship` → `odoo-reflect`
- `odoo-review` + `odoo-security` for diffs with exposure or permission changes
- `odoo-business-sales` + `odoo-business-inventory` + `odoo-business-accounting` for order-to-cash flows
- `odoo-business-website-ecommerce` + `odoo-business-sales` + `odoo-business-inventory` for cart-to-delivery flows
- `odoo-business-hr` + `odoo-business-expenses` + `odoo-business-accounting` for employee reimbursement flows

## Sprint task skills
- `odoo-think` — Risk-oriented scoping brief with module map, business entrypoint, cross-app impact, and open questions.
- `odoo-plan` — Ordered execution plan with file map, acceptance criteria, test matrix, rollout notes, and open decisions.
- `odoo-build` — Concrete in-scope code or configuration changes plus noted assumptions and follow-up validation needs.
- `odoo-review` — Structured findings on an existing diff or artifact, separated into required fixes, open risks, and optional improvements.
- `odoo-test` — Current-change validation evidence or validation plan tied to a specific diff, addon, bug, or runtime scenario.
- `odoo-ship` — Go or no-go rollout checklist with staging verification, release sequencing, rollback cautions, and production notes.
- `odoo-reflect` — Retrospective with lessons, remaining gaps, and concrete follow-up actions.

## Technical reference skills
- `odoo-architecture` — Architecture recommendation with target addon, dependency rationale, and bridge-module guidance.
- `odoo-orm-modeling` — ORM modeling guidance with field or method recommendations and anti-pattern checks.
- `odoo-view-ui` — UI guidance with view strategy, inheritance notes, and action or menu recommendations.
- `odoo-security` — Security assessment with trust boundaries, permission checks, exposure risks, and required safeguards.
- `odoo-testing-reference` — Framework and test-authoring guidance for future or current test design, without claiming current-change readiness.
- `odoo-performance` — Performance guidance with hotspot hypotheses, optimization levers, and validation ideas.
- `odoo-integration-api` — Integration design guidance with auth model, data flow, safety considerations, and operational constraints.
- `odoo-upgrade-migration` — Migration strategy with data-preservation plan, script notes, rollout order, and validation needs.
- `odoo-delivery-ops` — Operational mechanics guidance covering commands, flags, environment behavior, and runtime cautions.

## Business reference skills
- `odoo-business-sales` — Sales process map from a backend sales entrypoint, with downstream documents, roles, and cross-app impacts.
- `odoo-business-purchase` — Purchase process map with entrypoint, downstream documents, roles, and cross-app impacts.
- `odoo-business-inventory` — Inventory process map from a warehouse or stock-document entrypoint, with route logic, valuation, and cross-app effects.
- `odoo-business-manufacturing` — Manufacturing process map from a BoM or MO entrypoint, with operations, stock effects, and downstream cross-app impacts.
- `odoo-business-accounting` — Accounting process map with finance documents, posting impacts, and cross-app implications.
- `odoo-business-hr` — HR process map from a workforce entrypoint, with employee lifecycle touchpoints and cross-app dependencies.
- `odoo-business-timesheet-project-services` — Service-delivery process map with task, time, billing, and cross-app impacts.
- `odoo-business-expenses` — Expense process map from an expense-claim entrypoint, with states, roles, accounting impacts, and related HR links.
- `odoo-business-website-ecommerce` — Website and ecommerce process map from a public or portal entrypoint, with customer journey, downstream sales flow, and cross-app impacts.
