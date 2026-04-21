# Install odoo-skills into Claude Code

Use this flow when you want `odoo-skills` available for your Claude Code user from this repository.

This installation step is user-local to your Claude Code environment. It does not require an Odoo repository, and it does not ask for Odoo docs paths, Odoo source paths, `odoo-bin`, or project config values.

## Prerequisites

- Python 3
- Claude Code CLI installed as `claude`
- This repository cloned locally

## Install

Clone the repository and install the editable package:

```bash
git clone git@github.com:vdx-vn/ai-agent
cd ai-agent
python3 -m pip install -e .
```

Then install the plugin into Claude Code:

```bash
odoo-skills install-plugin
```

Fallback if the shell entrypoint is unavailable:

```bash
python3 -m tooling.install_plugin
```

The install flow builds `dist/marketplace`, validates the plugin, adds the local marketplace, and installs `odoo-skills` for the current Claude user/environment with Claude plugin local scope.

## Verify

Confirm Claude Code sees the installed plugin:

```bash
claude plugin list --json
```

If you want to validate the plugin metadata directly:

```bash
claude plugin validate .
claude plugin validate dist/marketplace
```

If you are developing this repository, these commands are also useful:

```bash
odoo-skills verify
odoo-skills build
odoo-skills smoke-install
```

## Optional project setup

`install-plugin` only installs the Claude Code plugin for your user environment. It does not set up local Odoo repository integration.

If you also want local Odoo docs/source paths or local test harness configuration inside a specific Odoo repository, run `odoo-skills project-setup` in that repository afterward. That project-local step is separate from the user-local plugin install. See [project-setup.md](project-setup.md).

## Troubleshooting

### `odoo-skills: command not found`

The editable package is not installed in the Python environment on your current shell path. Re-run:

```bash
python3 -m pip install -e .
```

Then retry `odoo-skills install-plugin`, or use:

```bash
python3 -m tooling.install_plugin
```

### `externally-managed-environment` during pip install

Use a virtual environment:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -e .
```

### `claude` command not found

Install Claude Code CLI first, then re-run the install command.

### Plugin install looks stale

Re-run the install flow. It rebuilds the runtime marketplace bundle before installing.

## Uninstall

Remove the plugin install artifacts from Claude Code:

```bash
odoo-skills install-plugin --uninstall
```

Fallback:

```bash
python3 -m tooling.install_plugin --uninstall
```

This uninstall flow removes plugin install artifacts only. It does not remove `.claude/settings.local.json` or `.claude/odoo-skill-paths.json` from any Odoo repositories you may have configured separately.
