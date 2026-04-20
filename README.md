# odoo-skills

Public Claude Code plugin for Odoo-focused skills.

## What this repository is

This repository packages `odoo-skills`, a Claude Code plugin for Odoo workflows.

Runtime plugin payload is intentionally small:
- `.claude-plugin/` - plugin metadata
- `skills/` - public shipped skill library
- `LICENSE`

Everything else in this repository supports authoring, validation, packaging, local setup, or development.

## How Claude Code uses these skills

Claude Code does not need these skills to live in your Odoo project or in `~/.claude/skills/`.

Recommended setup works like this:
1. clone this repository anywhere convenient
2. run `tooling/setup_local.py`
3. the script builds runtime bundle at `dist/marketplace/`
4. the script registers that bundle as a local Claude marketplace
5. the script installs `odoo-skills` into Claude Code from that marketplace

After install, Claude Code reads the public Odoo skills from installed plugin bundle built from `dist/marketplace/skills/`.

Important:
- this repository is separate from your Odoo project
- `setup_local.py` does not copy skill files into your custom addons repository
- your Odoo project is referenced by paths and config, not by moving files into it

## Recommended local setup

Clone this repository anywhere convenient, then run the guided setup from repo root:

```bash
git clone git@github.com:vdx-vn/ai-agent
cd ai-agent
python3 tooling/setup_local.py
```

You do not clone this repository into your Odoo project.

The setup prompts for:
- your local Odoo documentation clone path
- your local Odoo core source clone path
- the Odoo version if auto-detection cannot infer it
- the `odoo-bin` path from that Odoo core source tree
- the Odoo config file path used by your project

Use these values as follows:
- `--docs-root`: local Odoo documentation clone
- `--source-root`: local Odoo Community or Enterprise source clone where `odoo-bin` lives
- `--odoo-bin`: path to `odoo-bin` inside that Odoo source tree
- `--config`: your project config file, for example `/etc/odoo/odoo.conf`

Your custom addons repository can live anywhere and is usually referenced through `addons_path` in `odoo.conf`. It is not the value for `--source-root` unless it is also your Odoo core source tree.

`setup_local.py` then:
- materializes local `.claude/skills` authoring copy for your chosen Odoo docs and source paths
- writes `.claude/odoo-skill-paths.json`
- stores `ODOO_TEST_BASE_CMD` in `.claude/settings.local.json`
- builds runtime plugin bundle at `dist/marketplace/`
- runs `claude plugin validate`
- adds local marketplace `odoo-skills-dev`
- installs `odoo-skills` into Claude Code with local scope

### Non-interactive example

```bash
python3 tooling/setup_local.py \
  --docs-root /path/to/odoo/documentation \
  --source-root /path/to/odoo/source \
  --version 18.0 \
  --odoo-bin /path/to/odoo/source/odoo-bin \
  --config /etc/odoo/odoo.conf \
  --yes
```

### Example with separate custom addons repository

If your project code lives outside Odoo core, keep using Odoo core for `--source-root` and your project config for `--config`:

```bash
python3 tooling/setup_local.py \
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
- `addons_path` inside `/etc/odoo/odoo.conf` points at both Odoo core addons and your custom addons

## Configure each Odoo project once

After you install the tooling once, enter each Odoo project and save its local Odoo paths with:

```bash
cd /path/to/odoo-project
odoo-skills project-setup
```

The command prompts for:
- your local Odoo documentation clone path
- your local Odoo core source clone path
- the Odoo version if auto-detection cannot infer it
- the `odoo-bin` path from that Odoo core source tree
- the Odoo config file path used by that project

It writes only project-local files:
- `.claude/settings.local.json`
- `.claude/odoo-skill-paths.json`

Run it again later with `--force` if the project moves to a different Odoo version or config path:

```bash
odoo-skills project-setup --force
```

## What setup changes

`tooling/setup_local.py` changes files in this repository and Claude plugin state.

It writes or updates:
- `.claude/settings.local.json`
- `.claude/odoo-skill-paths.json`
- materialized files under `.claude/skills/`
- `dist/marketplace/`

It also runs Claude plugin install commands for local plugin registration.

It does not:
- edit your custom addons repository
- edit Odoo core source
- edit `odoo.conf`
- create folders inside your Odoo project
- move skill files into your Odoo project

## Where files live after setup

Source and build locations in this repository:
- `skills/` - canonical public skill source shipped in plugin
- `.claude/skills/` - local materialized authoring copy for this repo
- `dist/marketplace/skills/` - packaged runtime skill payload used for local install

At runtime, Claude Code uses installed plugin payload from local marketplace install, not `.claude/skills/`.

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

## Uninstall

Remove local setup and installed local plugin:

```bash
python3 tooling/setup_local.py --uninstall
```

This removes managed local setup state from this repository and attempts to uninstall local Claude plugin registration created by setup.

## Advanced manual fallback

If you only want skill-path materialization without guided local install flow, run:

```bash
python3 tooling/materialization/materialize_odoo_skill_paths.py \
  --docs-root /path/to/odoo/documentation \
  --source-root /path/to/odoo/source
```

Add `--version 18.0` or similar if auto-detection cannot infer Odoo series.

This only rewrites placeholders in local `.claude/skills/` copy and writes `.claude/odoo-skill-paths.json`. It does not install plugin into Claude Code.

## Local development

### Run this repository directly as plugin source

For local development, you can run Claude Code with this repository as plugin source:

```bash
claude --plugin-dir .
```

If you also want default user plugins, add them too:

```bash
claude --plugin-dir ~/.claude/plugins --plugin-dir .
```

This mode is useful while editing plugin source in this repository.

### Validate plugin metadata

```bash
claude plugin validate .
claude plugin validate dist/marketplace
```

## Local marketplace install test

Build runtime bundle, add local marketplace, and install plugin from it:

```bash
odoo-skills-build
claude plugin marketplace add ./dist/marketplace
claude plugin install odoo-skills@odoo-skills-dev --scope local
claude plugin list --json
```

Slash-command equivalents:
- `/plugin marketplace add`
- `/plugin install odoo-skills@odoo-skills-dev`

## Development commands

Install dev tooling:

```bash
python3 -m pip install -e .
```

Run full test suite:

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

Run validator:

```bash
odoo-skills-verify
```

Build runtime marketplace bundle:

```bash
odoo-skills-build
```

Smoke-test local install flow:

```bash
odoo-skills-smoke-install
```

## Requirements

Recommended local setup expects:
- Python 3
- Claude Code CLI installed as `claude`
- local Odoo documentation clone
- local Odoo core source clone
- Odoo config file for your project

If `claude` is not installed, `tooling/setup_local.py` exits with error.
