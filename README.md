# odoo-skills

Public Claude Code plugin for Odoo-focused skills.

Install this once for your Claude Code user from this repository. Only set up a project separately if you want local Odoo repository integration such as docs/source paths and local test harness settings.

## Quickstart

Clone the repository somewhere convenient and install the editable package:

```bash
git clone git@github.com:vdx-vn/ai-agent
cd ai-agent
python3 -m pip install -e .
```

Then install the plugin for your Claude Code user and verify it is present:

```bash
odoo-skills install-plugin
claude plugin list --json
```

Fallback if the shell entrypoint is unavailable:

```bash
python3 -m tooling.install_plugin
claude plugin list --json
```

For detailed install, verification, troubleshooting, and uninstall guidance, see [docs/install.md](docs/install.md).

## Optional: configure a local Odoo project

Only do this if you want local Odoo docs/source paths and local test harness setup inside a specific Odoo repository.

Run this inside the Odoo repository you want to configure:

```bash
odoo-skills project-setup
# fallback
python3 -m tooling.cli project-setup
```

For prerequisites, prompts, written files, reruns, and examples, see [docs/project-setup.md](docs/project-setup.md).

## What this repository contains

This repository packages `odoo-skills`, a Claude Code plugin for Odoo workflows.

Runtime plugin payload stays small:
- `.claude-plugin/` - plugin metadata
- `skills/` - public shipped skill library
- `README.md`, `LICENSE`

Everything else supports authoring, validation, packaging, installation, optional project setup, or local development.

## Common workflows

Verify plugin metadata and docs contracts:

```bash
odoo-skills verify
# fallback
python3 -m tooling.cli verify
# legacy script
odoo-skills-verify
```

Build the runtime marketplace bundle:

```bash
odoo-skills build
# fallback
python3 -m tooling.cli build
# legacy script
odoo-skills-build
```

Smoke-test the local install flow:

```bash
odoo-skills smoke-install
# fallback
python3 -m tooling.cli smoke-install
# legacy script
odoo-skills-smoke-install
```

Run Claude Code directly with this repository as plugin source:

```bash
claude --plugin-dir .
claude --plugin-dir ~/.claude/plugins --plugin-dir .
```

Manual local marketplace flow:

```bash
odoo-skills build
claude plugin marketplace add ./dist/marketplace
claude plugin install odoo-skills@odoo-skills-dev --scope local
claude plugin list --json
```

Uninstall the plugin from Claude Code:

```bash
odoo-skills install-plugin --uninstall
# fallback
python3 -m tooling.install_plugin --uninstall
```

## Development commands

Install dev tooling entrypoints:

```bash
python3 -m pip install -e .
```

Run the full unittest suite:

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

Validate plugin metadata directly with Claude CLI:

```bash
claude plugin validate .
claude plugin validate dist/marketplace
```

## Deprecated compatibility shim

`python3 -m tooling.setup_local` is deprecated compatibility behavior kept for one release window.

Use `odoo-skills install-plugin` to install for your Claude Code user, then use `odoo-skills project-setup` only inside Odoo repositories that need local integration.

Deprecated commands:

```bash
python3 -m tooling.setup_local
python3 -m tooling.setup_local --uninstall
```
