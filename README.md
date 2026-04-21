# odoo-skills

Public Claude Code plugin for Odoo-focused skills.

## Fastest local marketplace install

From repo root, build the runtime bundle and install from the local marketplace:

```bash
odoo-skills-build
claude plugin marketplace add ./dist/marketplace
claude plugin install odoo-skills@odoo-skills-dev
claude plugin list --json
```

Use this when you want the shortest local plugin install path. If the target repository is an Odoo project, run `odoo-skills project-setup` in that project after plugin install.

## What this repository is

This repository packages `odoo-skills`, Claude Code plugin for Odoo workflows.

Runtime plugin payload stays small:
- `.claude-plugin/` - plugin metadata
- `skills/` - public shipped skill library
- `LICENSE`

Everything else supports authoring, validation, packaging, installation, project setup, or local development.

## Install and use plugin

Claude Code does not need these skills copied into your Odoo project or `~/.claude/skills/`.

Correct workflow has 3 phases:
1. install repo entrypoints
2. install plugin into Claude Code
3. configure each Odoo project locally

## Phase 1: install repo entrypoints

Clone this repository anywhere convenient, then install editable package from repo root:

```bash
git clone git@github.com:vdx-vn/ai-agent
cd ai-agent
python3 -m pip install -e .
```

This step creates command-line entrypoints from `pyproject.toml`, including:
- `odoo-skills`
- `odoo-skills-install`
- `odoo-skills-verify`
- `odoo-skills-build`
- `odoo-skills-smoke-install`

If system Python blocks editable install with `externally-managed-environment`, use a virtual environment:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -e .
```

If you skip install step, commands like `odoo-skills project-setup` will fail with `odoo-skills: command not found`.

## Phase 2: install plugin into Claude Code

From repo root, install local marketplace bundle into Claude Code:

```bash
python3 -m tooling.install_plugin
```

Equivalent command surfaces after editable install:

```bash
odoo-skills install-plugin
odoo-skills-install
```

Install flow does only plugin bootstrap:
- builds runtime bundle at `dist/marketplace/`
- runs `claude plugin validate`
- adds local marketplace `odoo-skills-dev`
- installs `odoo-skills` into Claude Code with local scope

Install flow does **not** ask for:
- Odoo documentation path
- Odoo source path
- `odoo-bin`
- `odoo.conf`

Install flow does **not** write:
- repo `.claude/settings.local.json`
- repo `.claude/odoo-skill-paths.json`

## Phase 3: configure each Odoo project once

After plugin install, enter each Odoo project and save project-local Odoo paths and base test command with:

```bash
cd /path/to/odoo-project
odoo-skills project-setup
```

If shell entrypoint is unavailable on your `PATH`, use fallback:

```bash
python3 -m tooling.cli project-setup
```

Project setup prompts for:
- local Odoo documentation clone path
- local Odoo core source clone path
- Odoo version if auto-detection cannot infer it
- `odoo-bin` path from that Odoo core source tree
- Odoo config file path used by that project

It writes only project-local files:
- `.claude/settings.local.json`
- `.claude/odoo-skill-paths.json`

Run it again later with `--force` if project moves to different Odoo version or config path:

```bash
odoo-skills project-setup --force
# fallback
python3 -m tooling.cli project-setup --force
```

## What belongs to install step vs project step

Install step (`tooling.install_plugin`):
- plugin bundle build
- Claude marketplace registration
- Claude plugin install

Project step (`odoo-skills project-setup`):
- `docsRoot`
- `sourceRoot`
- version metadata
- `ODOO_TEST_BASE_CMD`

This repository is separate from your Odoo project.
Your Odoo project paths belong to each Odoo project only.

## Example with separate custom addons repository

If project code lives outside Odoo core, still use Odoo core for `--source-root` and project config for `--config`:

```bash
cd /path/to/odoo-project
odoo-skills project-setup \
  --docs-root /home/xmars/src/odoo/documentation \
  --source-root /home/xmars/src/odoo/odoo-community \
  --version 18.0 \
  --odoo-bin /home/xmars/src/odoo/odoo-community/odoo-bin \
  --config /etc/odoo/odoo.conf \
  --yes
```

Fallback:

```bash
python3 -m tooling.cli project-setup \
  --docs-root /home/xmars/src/odoo/documentation \
  --source-root /home/xmars/src/odoo/odoo-community \
  --version 18.0 \
  --odoo-bin /home/xmars/src/odoo/odoo-community/odoo-bin \
  --config /etc/odoo/odoo.conf \
  --yes
```

In this shape:
- Odoo core source might be `/home/xmars/src/odoo/odoo-community`
- custom addons might be `/home/xmars/dev/vdx-vn/g10-qms/addons`
- `addons_path` inside `/etc/odoo/odoo.conf` points at both Odoo core addons and custom addons

## Installed public skills

Sprint task skills:
- `odoo-think`
- `odoo-plan`
- `odoo-build`
- `odoo-review`
- `odoo-test`
- `odoo-ship`
- `odoo-reflect`

Technical reference skills:
- `odoo-architecture`
- `odoo-orm-modeling`
- `odoo-view-ui`
- `odoo-security`
- `odoo-testing-reference`
- `odoo-performance`
- `odoo-integration-api`
- `odoo-upgrade-migration`
- `odoo-delivery-ops`
- `odoo-local-test-harness`
- `pylint-code-review`

Business reference skills:
- `odoo-business-sales`
- `odoo-business-purchase`
- `odoo-business-inventory`
- `odoo-business-manufacturing`
- `odoo-business-accounting`
- `odoo-business-hr`
- `odoo-business-timesheet-project-services`
- `odoo-business-expenses`
- `odoo-business-website-ecommerce`

## Development commands

Install dev tooling:

```bash
python3 -m pip install -e .
```

Run validator:

```bash
odoo-skills verify
# fallback
python3 -m tooling.cli verify
# legacy script
odoo-skills-verify
```

Build runtime marketplace bundle:

```bash
odoo-skills build
# fallback
python3 -m tooling.cli build
# legacy script
odoo-skills-build
```

Smoke-test local install flow:

```bash
odoo-skills smoke-install
# fallback
python3 -m tooling.cli smoke-install
# legacy script
odoo-skills-smoke-install
```

Run full test suite:

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

## Validate plugin metadata directly with Claude CLI

```bash
claude plugin validate .
claude plugin validate dist/marketplace
```

## Run this repository directly as plugin source

For local development, you can run Claude Code with this repository as plugin source:

```bash
claude --plugin-dir .
```

If you also want default user plugins, add them too:

```bash
claude --plugin-dir ~/.claude/plugins --plugin-dir .
```

## Uninstall

Remove installed local plugin and generated marketplace bundle:

```bash
python3 -m tooling.install_plugin --uninstall
```

Equivalent command surfaces:

```bash
odoo-skills-install --uninstall
odoo-skills install-plugin --uninstall
```

This removes plugin install artifacts only. It does not remove per-project `.claude/settings.local.json` or `.claude/odoo-skill-paths.json` from your Odoo projects.

## Deprecated compatibility shim

`python3 -m tooling.setup_local` still exists as deprecated compatibility shim for one release window.

It now delegates to install-only flow and prints next-step guidance. It is no longer primary setup command.

Deprecated commands:

```bash
python3 -m tooling.setup_local
python3 -m tooling.setup_local --uninstall
```

## Advanced manual fallback

If you only want placeholder materialization in copied skill tree without project setup command, run:

```bash
python3 tooling/materialization/materialize_odoo_skill_paths.py \
  --docs-root /path/to/odoo/documentation \
  --source-root /path/to/odoo/source
```

Add `--version 18.0` or similar if auto-detection cannot infer Odoo series.

This rewrites placeholders in local `.claude/skills/` copy and writes `.claude/odoo-skill-paths.json`. It does not install plugin into Claude Code.

## Requirements

Recommended workflow expects:
- Python 3
- Claude Code CLI installed as `claude`
- local Odoo documentation clone
- local Odoo core source clone
- Odoo config file for each project

If `claude` is not installed, `tooling.install_plugin` exits with error.
