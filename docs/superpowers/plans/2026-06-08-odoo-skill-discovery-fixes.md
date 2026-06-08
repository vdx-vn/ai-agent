# Odoo Skill Discovery Fixes Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make installed Odoo skills reliably discover project-local Odoo docs, CE source, and configured test commands from `.odoo-skills/project.json`.

**Architecture:** Keep project setup as the source of truth. Public skills must tell agents to read `.odoo-skills/project.json` before using docs/source anchors or local test commands, and the harness script must continue to resolve that file from nested addon directories.

**Tech Stack:** Markdown skill files, Python `unittest`, existing local harness script.

---

### Task 1: Add Discovery Contract Tests

**Files:**
- Modify: `tests/unit/test_reference_docs.py`
- Modify: `tests/unit/test_odoo_local_test_harness_docs.py`

- [ ] **Step 1: Write tests that fail on missing project-context guidance**

Add assertions that every Odoo overview reference either declares project-local path resolution or is explicitly non-Odoo-path oriented, and that harness docs require configured commands to be preferred over Docker or README snippets.

- [ ] **Step 2: Run targeted tests to verify failure**

Run: `rtk python3 -m unittest tests.unit.test_reference_docs tests.unit.test_odoo_local_test_harness_docs -v`

Expected before implementation: at least one assertion fails because current overview docs do not consistently mention `.odoo-skills/project.json`, `docsRoot`, and `sourceRoot`.

### Task 2: Patch Skill References

**Files:**
- Modify: `skills/*/references/overview.md` for Odoo skills with docs/source anchors
- Modify: `skills/odoo-paths.md`
- Modify: `docs/reference/odoo-paths.md`
- Modify: `docs/authoring/odoo-paths.md`

- [ ] **Step 1: Add a concise project-local resolution block**

For each Odoo overview with docs/source anchors, add this behavior: search upward from the current working directory for `.odoo-skills/project.json`; when found, use `docsRoot` and `sourceRoot`; only fall back to placeholders or manual discovery when the config is absent.

- [ ] **Step 2: Clarify the shared path docs**

Make the shared docs explicit that installed skills should prefer the project config over Docker Compose files, module READMEs, or ad hoc filesystem searches.

### Task 3: Tighten Harness Guidance

**Files:**
- Modify: `skills/odoo-local-test-harness/SKILL.md`
- Modify: `skills/odoo-local-test-harness/references/overview.md`
- Modify: `skills/odoo-local-test-harness/references/checklist.md`
- Modify: `skills/odoo-test/references/checklist.md`

- [ ] **Step 1: Make command precedence explicit**

State that `ODOO_TEST_BASE_CMD` or `.odoo-skills/project.json` wins over Docker Compose discovery, PostgreSQL image discovery, module README commands, and inferred `odoo-bin` commands.

- [ ] **Step 2: Preserve the current script behavior**

Do not replace `run_odoo_test.py`; its upward `.odoo-skills/project.json` lookup already supports nested addon directories.

### Task 4: Validate on SCA Addons

**Files:**
- No SCA source edits expected.

- [ ] **Step 1: Run targeted unit tests**

Run: `rtk python3 -m unittest tests.unit.test_reference_docs tests.unit.test_odoo_local_test_harness_docs tests.unit.test_run_odoo_test -v`

- [ ] **Step 2: Run harness dry-run from real addon directory**

Run from `/home/xmars/dev/vdx-vn/sca/addons/sources/extra-addons`: `rtk python3 /home/xmars/dev/vdx-vn/ai-agent-odoo-19/skills/odoo-local-test-harness/scripts/run_odoo_test.py --db tmp_sca_skill_discovery --update sca_mrp_master --test-tags /sca_mrp_master --dry-run`

Expected: the resolved base command comes from `/home/xmars/dev/vdx-vn/sca/addons/.odoo-skills/project.json`, not Docker probing.
