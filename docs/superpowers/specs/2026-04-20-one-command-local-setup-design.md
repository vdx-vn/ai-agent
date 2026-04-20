# One-Command Local Setup Design

## Goal

Make local installation easy for other users after `git clone`, with one command that installs plugin from this repository, asks for Odoo local paths, writes local materialization and harness config, and prints one uninstall or reset command.

## Problem

Current local setup asks users to know several separate steps:

- materialize Odoo path placeholders with long flags
- write `.claude/settings.local.json` manually for `ODOO_TEST_BASE_CMD`
- add local marketplace
- install plugin from that marketplace
- remember how to clean up local state later

This is too much ceremony for first-time users and too easy to misconfigure.

## Success Criteria

After cloning this repository, a user can run:

```bash
python3 tooling/setup_local.py
```

The command should:

1. ask for required local Odoo values when missing
2. materialize the local `.claude/skills/` copy with concrete docs and source paths
3. write local Odoo harness config into `.claude/settings.local.json`
4. build and validate local marketplace bundle
5. install `odoo-skills` into Claude with local scope
6. print a short success summary plus one uninstall command

A user should not need to manually run `claude plugin marketplace add`, `claude plugin install`, or `materialize_odoo_skill_paths.py` during normal setup.

## Non-Goals

- changing shipped runtime skill payload under `skills/`
- removing existing lower-level materialization utilities
- replacing advanced manual setup paths for power users or CI
- changing plugin packaging model away from local marketplace install
- changing Odoo skill routing or content beyond setup-related references

## User Experience

### Primary setup path

From repository root:

```bash
python3 tooling/setup_local.py
```

Interactive flow:

1. verify repository root and required local tools
2. ask for Odoo documentation root
3. ask for Odoo source root
4. detect Odoo version from those repos when possible; otherwise ask for version
5. ask how to build `ODOO_TEST_BASE_CMD`
   - preferred shortcut: ask for Python executable with default `python3`, `odoo-bin` path, and config path, then assemble command
   - fallback: let user paste full base command
6. materialize local `.claude/skills/` copy
7. write `.claude/odoo-skill-paths.json`
8. merge `.claude/settings.local.json`
9. build and validate `dist/marketplace`
10. add marketplace and install plugin locally in Claude
11. print summary and uninstall command

### Automation path

Same script supports flags for non-interactive use:

```bash
python3 tooling/setup_local.py \
  --docs-root /path/to/odoo/documentation \
  --source-root /path/to/odoo/odoo \
  --config /path/to/odoo.conf \
  --odoo-bin /path/to/odoo/odoo-bin \
  --yes
```

Supported flags should include:

- `--docs-root`
- `--source-root`
- `--version`
- `--python-bin`
- `--odoo-bin`
- `--config`
- `--base-cmd`
- `--yes`
- `--uninstall`

`--base-cmd` and `--odoo-bin` plus `--config` are mutually exclusive input styles for the harness base command.

## Command Surface

Add new top-level script:

- `tooling/setup_local.py`

Rationale:

- no prior `pip install -e .` needed
- shortest onboarding command
- keeps setup logic in repo-owned tooling
- allows later orchestration without expanding README command count

The script should be import-safe and testable, with a `main()` function and small helpers for:

- argument parsing
- interactive prompting
- path validation
- version detection
- settings merge
- marketplace and plugin command execution
- uninstall cleanup

## Setup Actions

### 1. Preflight

Validate:

- script runs from repository root or can resolve repo root from `__file__`
- `claude` CLI exists on `PATH`
- docs root exists and is a directory
- source root exists and is a directory
- if `--python-bin` is provided, it resolves to an executable
- either:
  - `odoo-bin` and config path both exist, or
  - `base-cmd` is provided explicitly

If any required input is missing in interactive mode, prompt for it. In non-interactive mode, fail with a direct error message.

### 2. Odoo version resolution

Reuse current materialization version detection rules:

- prefer explicit `--version`
- otherwise detect from git branch names
- otherwise detect from repo path names
- otherwise prompt in interactive mode
- otherwise fail in non-interactive mode

The accepted version format remains series form such as `17.0`, `18.0`, or `19.0`.

### 3. Local materialization

Reuse current placeholder replacement logic from `tooling/materialization/materialize_odoo_skill_paths.py` instead of duplicating it.

The setup script should call shared helpers or a shared internal function so one implementation owns:

- `<ODOO_DOCS_ROOT>` replacement
- `<ODOO_SOURCE_ROOT>` replacement
- `<ODOO_SERIES>` replacement
- `<ODOO_MAJOR_VERSION>` replacement
- `--force` style rematerialization behavior

Output remains project-local:

- `.claude/odoo-skill-paths.json`
- updated files under `.claude/skills/`

### 4. Harness config merge

Write `.claude/settings.local.json` if missing.

If the file exists:

- preserve unrelated top-level keys
- preserve unrelated `env` entries
- update only setup-managed keys

Initially the only managed settings key is:

- `env.ODOO_TEST_BASE_CMD`

Preferred generated value:

```json
{
  "env": {
    "ODOO_TEST_BASE_CMD": "/path/to/python /path/to/odoo-bin -c /path/to/odoo.conf"
  }
}
```

If the user supplied `--base-cmd`, store that exact value instead.

### 5. Marketplace build and install

Reuse existing build and smoke-install conventions:

1. build runtime subset into `dist/marketplace`
2. run `claude plugin validate dist/marketplace`
3. run `claude plugin marketplace add dist/marketplace`
4. run `claude plugin install odoo-skills@odoo-skills-dev --scope local`

This keeps install path aligned with current local marketplace metadata:

- marketplace name: `odoo-skills-dev`
- plugin name: `odoo-skills`
- scope: `local`

### 6. Success output

End with compact output that includes:

- installed plugin name and scope
- detected Odoo version
- written local files
- reminder that `.claude/settings.local.json` and `.claude/odoo-skill-paths.json` are local state
- one uninstall command:

```bash
python3 tooling/setup_local.py --uninstall
```

## Uninstall and Reset Flow

Uninstall uses same command surface:

```bash
python3 tooling/setup_local.py --uninstall
```

It should perform these actions in order:

1. run `claude plugin uninstall odoo-skills --scope local`
2. run `claude plugin marketplace remove odoo-skills-dev`
3. restore only recorded materialized `.claude/skills/` files to git state
4. remove `.claude/odoo-skill-paths.json`
5. remove setup-managed `env.ODOO_TEST_BASE_CMD` from `.claude/settings.local.json`
6. remove `dist/marketplace` because setup recreates it deterministically

Cleanup rules:

- ignore already-missing plugin or marketplace with clear output
- keep unrelated `.claude/settings.local.json` content intact
- if removing managed keys leaves empty `env` or empty file object, collapse cleanly
- do not delete `.claude/skills/` tree or unrelated local workspace files

## State Tracking

Extend `.claude/odoo-skill-paths.json` to include setup metadata in addition to current path and version data.

Required metadata:

- `docsRoot`
- `sourceRoot`
- `version`
- `majorVersion`
- `versionSource`
- `skillsRoot`
- `materializedAt`
- `mode`
- `materializedFiles`
- `setupManagedSettingsKeys`
- `pluginName`
- `marketplaceName`
- `installScope`
- `marketplacePath`
- `setupCompletedAt`

This file becomes setup state source for:

- safe re-runs
- rematerialization
- uninstall cleanup
- concise user-facing status output

## Idempotency

Repeated setup runs should succeed.

Rules:

- if paths or version change, rematerialize local `.claude/skills/` copy safely
- if marketplace already exists, update or replace it through standard Claude CLI behavior rather than failing early
- if plugin already exists in local scope, reinstall or update through standard install path
- if `.claude/settings.local.json` exists, merge only managed keys
- if uninstall runs twice, second run should exit cleanly with no destructive side effects

## Documentation Changes

### README.md

Replace current local development install section with short onboarding path:

```bash
git clone git@github.com:vdx-vn/ai-agent
cd ai-agent
python3 tooling/setup_local.py
```

Then add short subsections for:

- what the command prompts for
- non-interactive flags
- reinstall or rerun behavior
- uninstall command
- advanced manual setup fallback

### Setup guidance references

Update setup guidance that currently points users to long materialization command so it points to `python3 tooling/setup_local.py` first.

Affected places likely include:

- `.claude/skills/odoo-paths.md`
- `skills/odoo-paths.md`
- `tooling/materialization/suggest_odoo_skill_setup.py`
- `skills/scripts/suggest_odoo_skill_setup.py`
- tests that lock expected guidance strings

Keep manual materialization command documented as fallback for advanced users.

## Implementation Boundaries

Files expected to change:

- create `tooling/setup_local.py`
- update `README.md`
- update `tooling/materialization/materialize_odoo_skill_paths.py` to expose reusable helpers if needed
- update `tooling/materialization/suggest_odoo_skill_setup.py`
- update `skills/scripts/suggest_odoo_skill_setup.py`
- update `.claude/skills/odoo-paths.md`
- update `skills/odoo-paths.md`
- update relevant unit tests

Optional but acceptable:

- add shared JSON merge helper if setup logic would otherwise duplicate settings-local update behavior
- add unit tests dedicated to setup and uninstall orchestration

Not acceptable:

- broad refactor of packaging or validator stack unrelated to setup
- moving shipped skill source away from `skills/`
- changing runtime subset rules in build unless setup reveals a real install defect

## Testing Strategy

### Unit tests

Add or update tests for:

- argument parsing
- interactive fallback decisions
- version detection fallback behavior
- settings-local merge behavior
- setup metadata written into `.claude/odoo-skill-paths.json`
- uninstall cleanup behavior for empty and non-empty local settings
- suggestion-hook output updated to recommend setup command

### Integration-style tests

Test setup orchestration pieces without mutating real user home:

- temp repo fixture or temp local state
- patched subprocess calls for Claude CLI commands
- assertions on command order:
  - validate
  - marketplace add
  - plugin install
- assertions on uninstall command order:
  - plugin uninstall
  - marketplace remove

### Existing command compatibility

Keep existing lower-level commands working:

- `python3 tooling/materialization/materialize_odoo_skill_paths.py ...`
- `odoo-skills-build`
- `odoo-skills-smoke-install`

The new setup script is the recommended path, not a replacement for every lower-level tool.

## Risks and Mitigations

### Risk: setup script becomes second implementation of materialization logic

Mitigation: move reusable parts behind shared helpers and keep one source of truth for path and version replacement.

### Risk: uninstall removes user-owned local settings

Mitigation: track setup-managed keys explicitly and only remove those keys.

### Risk: setup fails if Claude marketplace add behaves differently when marketplace already exists

Mitigation: capture and normalize expected already-exists cases; if needed, remove then re-add within setup-owned flow.

### Risk: users without local Odoo config file cannot build `ODOO_TEST_BASE_CMD`

Mitigation: support direct `--base-cmd` entry and interactive pasted command fallback.

## Recommendation

Adopt one interactive setup script as first-class onboarding path. Keep existing low-level scripts for advanced or partial flows, but move all user-facing docs and hook guidance to the new one-command setup and matching one-command uninstall.
