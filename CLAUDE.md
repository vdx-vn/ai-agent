# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

This repository packages `odoo-skills`, a Claude Code plugin focused on Odoo workflows.

Runtime plugin payload is intentionally small:
- `.claude-plugin/` — plugin and local marketplace metadata
- `skills/` — canonical shipped public skill tree
- `README.md`, `LICENSE`

Everything else supports authoring, validation, packaging, or local development.

## Important commands

### Setup

```bash
python3 -m pip install -e .
```

Installs the dev tooling entrypoints from `pyproject.toml`:
- `odoo-skills-verify`
- `odoo-skills-build`
- `odoo-skills-smoke-install`

### Main development loop

Run full test suite:

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

Run one test module:

```bash
python3 -m unittest tests.unit.test_plugin_foundation -v
```

Run one test case or method:

```bash
python3 -m unittest tests.unit.test_build_plugin.BuildPluginTests -v
python3 -m unittest tests.unit.test_build_plugin.BuildPluginTests.test_build_marketplace_creates_runtime_subset_only -v
```

Run repo validator:

```bash
odoo-skills-verify
# or
python3 -m tooling.cli verify
```

Build runtime marketplace bundle:

```bash
odoo-skills-build
# or
python3 -m tooling.cli build
```

Smoke-test local install flow:

```bash
odoo-skills-smoke-install
# or
python3 -m tooling.cli smoke-install
```

Validate plugin metadata directly with Claude CLI:

```bash
claude plugin validate .
claude plugin validate dist/marketplace
```

Run plugin directly from this repo during development:

```bash
claude --plugin-dir .
```

Test local marketplace install manually:

```bash
claude plugin marketplace add ./dist/marketplace
claude plugin install odoo-skills@odoo-skills-dev --scope local
claude plugin list --json
```

### Release / publish checks

Before tagging or publishing, run:

```bash
python3 -m pip install -e .
odoo-skills-verify
odoo-skills-build
odoo-skills-smoke-install
claude --plugin-dir .
claude plugin validate dist/marketplace
```

## Architecture

### Canonical plugin source vs authoring source

`skills/` is canonical shipped skill source. Tests enforce exact directory membership and require `SKILL.md` for each public skill.

`.claude/skills/` is not packaged into the runtime build. Treat it as authoring and local Claude workspace material, not as the plugin payload. Build tests explicitly assert that `.claude/skills/`, `skill-creator/`, and `odoo-test/` are excluded from `dist/marketplace`.

When changing public plugin behavior, update `skills/` first and verify matching docs and inventory.

### Plugin metadata and packaging flow

- `.claude-plugin/plugin.json` defines plugin identity shipped to Claude Code.
- `.claude-plugin/marketplace.json` defines local dev marketplace metadata for install tests.
- `tooling/build_plugin.py` copies only runtime paths into `dist/marketplace`.
- `tooling/smoke_install.py` builds that runtime subset, swaps `HOME` to a temp directory, then runs `claude plugin validate`, `marketplace add`, `plugin install`, and `plugin list --json` to prove installability.
- `tooling/cli.py` is stable command surface for `verify`, `build`, and `smoke-install`.

If changing packaging, keep runtime subset behavior deterministic: build starts by deleting and recreating `dist/marketplace`.

### Validation stack

Validation has two layers:

1. Python validators in `tooling/validate_plugin.py`
   - load expected public skills from `docs/reference/skill-inventory.json`
   - require each `skills/<name>/SKILL.md`
   - enforce frontmatter shape through `tooling/validation/frontmatter.py`
   - enforce required section layout through `tooling/validation/layout.py`
   - block unresolved `<ODOO_*>`, `TODO`, and `TBD` markers through `tooling/validation/release.py`

2. Claude CLI validation
   - `odoo-skills-verify` also runs `claude plugin validate <root>` when CLI available

If adding or renaming public skills, update `skills/`, `docs/reference/skill-inventory.json`, and any tests that lock exact public inventory.

### Skill library design

Public skills split into three groups:
- sprint task skills: `odoo-think`, `odoo-plan`, `odoo-build`, `odoo-review`, `odoo-test`, `odoo-ship`, `odoo-reflect`
- technical reference skills: architecture, ORM, UI, security, testing, performance, integrations, upgrade, delivery ops, local test harness
- business reference skills: sales, purchase, inventory, manufacturing, accounting, HR, timesheets/services, expenses, website/ecommerce

Big idea: routing is artifact-first, not keyword-first.
- `docs/reference/trigger-matrix.md` defines hard boundaries and tie-breakers between adjacent skills.
- `docs/reference/library-manifest.md` summarizes skill class, artifact, tie-breaker, and composition rules.
- `docs/reference/skill-inventory.json` is machine-readable source of truth used by validators.

When editing skill behavior, preserve narrow routing boundaries. Neighbor collisions are intentional design surface in docs.

### Odoo path materialization and project hooks

This repo contains authoring support for Odoo-specific path placeholders.

- `tooling/materialization/materialize_odoo_skill_paths.py` replaces `<ODOO_DOCS_ROOT>`, `<ODOO_SOURCE_ROOT>`, `<ODOO_SERIES>`, and `<ODOO_MAJOR_VERSION>` inside a copied `.claude/skills` tree and writes `.claude/odoo-skill-paths.json`.
- `tooling/materialization/suggest_odoo_skill_setup.py` detects new Odoo-project context and suggests materialization or local test harness setup.
- `.claude/settings.json` wires that suggestion script into `SessionStart` and `UserPromptSubmit` hooks.

This materialization flow supports local Claude workspace usage. It is separate from packaged public `skills/` runtime payload.

### Local Odoo test harness helper

`skills/odoo-local-test-harness/` includes scripts and tests for building project-local Odoo test commands safely.

Core rule: `.claude/settings.local.json` must define `ODOO_TEST_BASE_CMD` under `env`. That base command must already include `-c` or `--config`, and must not include runtime-managed flags like `-d`, `--test-tags`, `-i`, `-u`, `--test-enable`, or `--stop-after-init`.

Harness scripts then append runtime flags and optional cleanup deterministically instead of using shell string concatenation.

### Test strategy

Main test suite uses `unittest`, not `pytest`.

Coverage is layered:
- foundation tests for plugin metadata and README install instructions
- inventory and contract tests for public skill tree and required SKILL.md sections
- validator tests for frontmatter, release markers, and verify command
- build tests for runtime subset contents
- integration smoke-install test for actual Claude CLI install flow when `claude` exists
- focused tests for local test harness scripts

## Files worth reading before major changes

- `README.md` — minimal plugin usage and local install flow
- `docs/reference/trigger-matrix.md` — routing boundaries between skills
- `docs/reference/library-manifest.md` — big-picture inventory and composition map
- `docs/release/publish.md` — release checklist
- `tooling/cli.py` — stable command entrypoints
- `tooling/build_plugin.py` and `tooling/smoke_install.py` — runtime packaging and install verification

## Repo-specific cautions

- Do not assume `.claude/skills/` changes affect shipped plugin behavior; packaged runtime comes from root `skills/`.
- Do not add unresolved `<ODOO_*>`, `TODO`, or `TBD` markers to public shipped skills.
- If you add a new public skill, also update `docs/reference/skill-inventory.json` and tests that enforce exact inventory.
- If you change release behavior, re-run `odoo-skills-build`, `odoo-skills-smoke-install`, and `claude plugin validate dist/marketplace`.
