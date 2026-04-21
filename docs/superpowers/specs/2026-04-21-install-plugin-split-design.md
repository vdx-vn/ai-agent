# Install plugin split design

## Goal

Replace fake global Odoo project setup with clean split:
- global install manages only local plugin installation lifecycle
- per-project Odoo paths and test command stay in `odoo-skills project-setup`

## Problem

Current `tooling/setup_local.py` mixes two unrelated concerns:
1. install local Claude plugin from marketplace bundle
2. collect Odoo docs, source, config, and test command paths for this repo

This creates fake global state in repo-local `.claude/settings.local.json` and `.claude/odoo-skill-paths.json`, even though packaged runtime does not ship repo-local `.claude/skills/` materialization.

## Approved direction

Use compatibility-first rename.

- Add new entrypoint: `tooling/install_plugin.py`
- Keep `tooling/setup_local.py` as thin deprecated shim for one release window
- Move global install behavior to install-only flow
- Keep all Odoo project path collection in `odoo-skills project-setup`

## Behavior design

### `tooling/install_plugin.py`

Responsibilities:
- build runtime marketplace bundle in `dist/marketplace`
- run `claude plugin validate`
- add local marketplace `odoo-skills-dev`
- install `odoo-skills@odoo-skills-dev --scope local`
- uninstall plugin and remove marketplace on `--uninstall`
- clean `dist/marketplace` on uninstall

Non-responsibilities:
- do not ask for `--docs-root`
- do not ask for `--source-root`
- do not ask for `--odoo-bin`
- do not ask for `--config`
- do not write `.claude/settings.local.json`
- do not write `.claude/odoo-skill-paths.json`
- do not materialize `.claude/skills/`

CLI shape:
- `python3 -m tooling.install_plugin`
- `python3 -m tooling.install_plugin --uninstall`

### `tooling/setup_local.py`

Responsibilities:
- remain executable for compatibility
- print deprecation warning pointing to `tooling.install_plugin`
- delegate to same install-only implementation

Non-responsibilities:
- no legacy fake-global path behavior
- no separate logic fork

### `odoo-skills project-setup`

No functional scope change.

It remains only place that writes per-project:
- `.claude/settings.local.json` with `ODOO_TEST_BASE_CMD`
- `.claude/odoo-skill-paths.json` with `docsRoot`, `sourceRoot`, version metadata

## Documentation design

### README

Update onboarding flow to two phases:
1. install tooling/plugin locally
2. enter each Odoo project and run project setup

Primary commands:
- `python3 -m pip install -e .`
- `python3 -m tooling.install_plugin`
- `odoo-skills project-setup`

Also document fallback if `odoo-skills` command is not on `PATH`:
- `python3 -m tooling.cli project-setup`

Deprecation note:
- `python3 tooling/setup_local.py` still works temporarily but is deprecated

### Messaging

Global install text must stop implying Odoo docs/source paths are global plugin prerequisites.
Per-project docs must explicitly say those values belong to each Odoo project only.

## Test design

### New tests

- `tooling/install_plugin.py` direct execution by module works
- `tooling/install_plugin.py --uninstall` dispatch works
- `tooling/setup_local.py` shim delegates and warns

### Changed tests

Update current setup orchestration tests so install flow verifies only:
- build
- validate
- marketplace add
- plugin install
- uninstall rollback behavior
- no settings/state/materialization writes

Update README assertions to expect:
- `python3 -m tooling.install_plugin`
- `python3 -m tooling.cli project-setup` fallback guidance

### Removed expectations

Tests must stop expecting global install to:
- collect Odoo paths
- write `ODOO_TEST_BASE_CMD`
- write `docsRoot` or `sourceRoot`
- touch `.claude/skills/`

## Migration notes

Existing repo-local fake-global files may already exist from old flow.

Install-only uninstall should not delete or rewrite unrelated user-managed project files outside current repo.
For current repo:
- if uninstall sees old install metadata, remove only plugin-install-managed artifacts
- avoid pretending repo-local `.claude/settings.local.json` is still required for global install

Compatibility window:
- keep shim and deprecation warning now
- full removal can happen in later cleanup once docs and users migrate

## Acceptance criteria

- running global install never asks for Odoo project paths
- running global install never writes repo `.claude/settings.local.json`
- running global install never writes repo `.claude/odoo-skill-paths.json`
- `odoo-skills project-setup` remains path-owning command for Odoo projects
- README explains install vs project setup split clearly
- fallback command exists for environments where `odoo-skills` shell entrypoint is unavailable
- compatibility shim works and warns
- targeted tests pass

## Risks

### User confusion during transition
Mitigation: strong README wording plus deprecation warning in shim.

### Broken workflows relying on fake global files
Mitigation: compatibility shim keeps command alive while removing wrong behavior; project setup remains unchanged.

### Entry point availability confusion
Mitigation: document `python3 -m pip install -e .` before `odoo-skills project-setup`, and document `python3 -m tooling.cli project-setup` fallback.